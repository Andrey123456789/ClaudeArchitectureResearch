#!/usr/bin/env node
// Architecture check: validates backend project references and package boundaries against the
// selected frame's check specification (facet architecture.check) plus leaf adapters
// (persistence.enforcement, backend-testing.enforcement).
// Usage (from any directory of the project or a linked worktree):
//   node "$(git rev-parse --show-toplevel)/.claude/scripts/check-architecture.mjs"     (exit 1 on violations)
import { existsSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import {
  EncodingError, SetupError, listFiles, loadJsonFacet, parseCsproj, parseSelection, readText, resolveRoot, toPosix,
} from './lib/project.mjs';

// Platform fact: SDKs that reference a shared framework implicitly (no FrameworkReference in the project file).
const IMPLICIT_FRAMEWORKS = { 'microsoft.net.sdk.web': 'Microsoft.AspNetCore.App' };

// repoRoot: the project/worktree whose files are checked; configRoot: where the instruction configuration lives.
export function checkArchitecture(repoRoot, configRoot = repoRoot) {
  const selection = parseSelection(configRoot);
  const spec = loadJsonFacet(configRoot, selection, 'architecture', 'check');
  if (!spec) throw new SetupError('No architecture frame selected; the architecture slot is required.');
  const persistence = loadJsonFacet(configRoot, selection, 'persistence', 'enforcement');
  const testing = loadJsonFacet(configRoot, selection, 'backend-testing', 'enforcement');

  const violations = [];
  const warnings = [];
  const owner = '.claude/rules/1-architecture/frame/boundaries.md';

  for (const dir of spec.forbiddenTopLevelDirectories || []) {
    if (existsSync(path.join(repoRoot, dir))) {
      violations.push(`top-level '${dir}/' directory exists; backend tests live under ${spec.backendRoot}/ (decisions file, layout)`);
    }
  }

  const backend = path.join(repoRoot, spec.backendRoot);
  if (!existsSync(backend)) return { applicable: false, violations, warnings };

  const roleOf = (name) => {
    for (const [role, def] of Object.entries(spec.testRoles || {})) {
      if (new RegExp(def.projectPattern).test(name)) return { role, test: true, def };
    }
    for (const [role, def] of Object.entries(spec.roles)) {
      if (new RegExp(def.projectPattern).test(name)) return { role, test: false, def };
    }
    return null;
  };

  const projects = [];
  for (const file of listFiles(backend, (f) => f.toLowerCase().endsWith('.csproj'))) {
    const rel = toPosix(path.relative(repoRoot, file));
    let info;
    try {
      info = parseCsproj(readText(file, rel));
    } catch (error) {
      if (!(error instanceof EncodingError)) throw error;
      violations.push(`${error.message} (fix the file encoding before relying on the architecture check)`);
      continue;
    }
    const name = path.basename(file).replace(/\.csproj$/i, '');
    projects.push({ file, name, rel, info, role: roleOf(name) });
  }
  const byPath = new Map(projects.map((p) => [path.resolve(p.file).toLowerCase(), p]));
  const markers = ((testing && testing.testProjectMarkerPackages) || []).map((m) => m.toLowerCase());

  for (const p of projects) {
    const isMarkedTest = p.info.packages.some((pkg) => markers.includes((pkg.id || '').toLowerCase()));
    if (!p.role) {
      warnings.push(`${p.rel}: project name matches no role of the selected frame${isMarkedTest ? ' (references test packages)' : ''}; review placement (architecture.layout)`);
      continue;
    }
    if (isMarkedTest && !p.role.test) {
      warnings.push(`${p.rel}: production-role project references test packages`);
    }

    for (const ref of p.info.projects) {
      const target = byPath.get(path.resolve(path.dirname(p.file), ref.replace(/\\/g, '/')).toLowerCase());
      if (!target || !target.role) {
        warnings.push(`${p.rel}: reference '${ref}' does not resolve to a mapped backend project`);
        continue;
      }
      if (!p.role.test && target.role.test) {
        violations.push(`${p.rel} → ${target.name}: production project references a test project (${owner})`);
      } else if (!p.role.test && !p.role.def.mayReference.includes(target.role.role)) {
        violations.push(`${p.rel} → ${target.name}: ${p.role.role} must not reference ${target.role.role} (dependency direction, ${owner})`);
      } else if (p.role.test && !target.role.test && !(p.role.def.typicalReferences || []).includes(target.role.role)) {
        warnings.push(`${p.rel} → ${target.name}: broader than the typical ${p.role.role} references; keep test references narrow (${owner})`);
      }
    }

    if (!p.role.test && (spec.innerRoles || []).includes(p.role.role)) {
      const forbiddenFrameworks = spec.forbiddenFrameworkReferencesInInnerRoles || [];
      for (const fw of p.info.frameworks) {
        if (forbiddenFrameworks.some((f) => f.toLowerCase() === fw.toLowerCase())) {
          violations.push(`${p.rel}: ${p.role.role} must not reference framework '${fw}' (transport types, ${owner})`);
        }
      }
      // A forbidden shared framework also arrives implicitly through an SDK that references it, or through
      // packages of the same framework family (e.g. Microsoft.AspNetCore.App → Microsoft.AspNetCore.* packages).
      for (const sdk of p.info.sdks) {
        const fw = forbiddenFrameworks.find((f) => (IMPLICIT_FRAMEWORKS[sdk.toLowerCase()] || '').toLowerCase() === f.toLowerCase());
        if (fw) violations.push(`${p.rel}: ${p.role.role} must not use SDK '${sdk}', which implicitly references framework '${fw}' (transport types, ${owner})`);
      }
      for (const pkg of p.info.packages) {
        const fw = forbiddenFrameworks.find((f) => (pkg.id || '').toLowerCase().startsWith(`${f.replace(/\.App$/i, '')}.`.toLowerCase()));
        if (fw) violations.push(`${p.rel}: ${p.role.role} must not reference package '${pkg.id}' of framework '${fw}' (transport types, ${owner})`);
      }
      if (persistence && (persistence.forbiddenInRoles || []).includes(p.role.role)) {
        for (const pkg of p.info.packages) {
          if ((persistence.persistencePackagePrefixes || []).some((prefix) => (pkg.id || '').toLowerCase().startsWith(prefix.toLowerCase()))) {
            violations.push(`${p.rel}: ${p.role.role} must not reference persistence-implementation package '${pkg.id}' (${persistence.packageOwner})`);
          }
        }
      }
    }
  }
  return { applicable: true, violations, warnings };
}

if (import.meta.url === pathToFileURL(process.argv[1] || '').href) {
  try {
    const root = resolveRoot();
    const { applicable, violations, warnings } = checkArchitecture(root);
    if (!applicable) {
      console.log('Architecture check: NOT APPLICABLE (no backend directory).');
    }
    for (const w of warnings) console.log(`WARNING   ${w}`);
    for (const v of violations) console.log(`VIOLATION ${v}`);
    if (applicable) {
      console.log(`Architecture check: ${violations.length === 0 ? 'PASS' : 'FAIL'} (${violations.length} violation(s), ${warnings.length} warning(s)).`);
    }
    process.exit(violations.length === 0 ? 0 : 1);
  } catch (error) {
    console.error(`Architecture check could not run: ${error.message}`);
    process.exit(2);
  }
}
