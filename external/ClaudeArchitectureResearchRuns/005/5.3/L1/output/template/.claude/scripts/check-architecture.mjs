#!/usr/bin/env node
// Architecture check: validates backend project references and package boundaries of the active
// project against the selected frame's check specification (facet architecture.check), the frame's
// technology bindings (architecture.enforcement), and leaf adapters (persistence.enforcement,
// backend-testing.enforcement).
// Usage (from any directory of the project or worktree to check):
//   node "$(git rev-parse --show-toplevel)/.claude/scripts/check-architecture.mjs"   (exit 1 on violations, 2 on setup errors)
import { existsSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import {
  EncodingError, SetupError, listFiles, loadJsonFacet, parseCsproj, parseSelection, readText, requireConfigRoot,
  resolveContext, toPosix,
} from './lib/project.mjs';

export function checkArchitecture({ activeRoot, configRoot }) {
  const selection = parseSelection(configRoot);
  const spec = loadJsonFacet(configRoot, selection, 'architecture', 'check');
  if (!spec) throw new SetupError('No architecture frame selected; the architecture slot is required.');
  const frameTech = loadJsonFacet(configRoot, selection, 'architecture', 'enforcement') || {};
  const persistence = loadJsonFacet(configRoot, selection, 'persistence', 'enforcement');
  const testing = loadJsonFacet(configRoot, selection, 'backend-testing', 'enforcement');

  const violations = [];
  const warnings = [];
  const owner = '.claude/rules/1-architecture/frame/boundaries.md';

  for (const dir of spec.forbiddenTopLevelDirectories || []) {
    if (existsSync(path.join(activeRoot, dir))) {
      violations.push(`top-level '${dir}/' directory exists; backend tests live under ${spec.backendRoot}/ (decisions file, architecture.layout)`);
    }
  }

  const backend = path.join(activeRoot, spec.backendRoot);
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
  for (const file of listFiles(backend, (f) => f.endsWith('.csproj'))) {
    const rel = toPosix(path.relative(activeRoot, file));
    let info;
    try { info = parseCsproj(readText(file)); } catch (error) {
      if (!(error instanceof EncodingError)) throw error;
      violations.push(`${rel}: cannot read project file — ${error.message}`);
      continue;
    }
    const name = path.basename(file, '.csproj');
    projects.push({ file, name, rel, info, role: roleOf(name) });
  }
  const byPath = new Map(projects.map((p) => [path.resolve(p.file).toLowerCase(), p]));
  const markers = (testing && testing.testProjectMarkerPackages) || [];
  const innerFrameworks = frameTech.innerRoleForbiddenFrameworks || [];

  for (const p of projects) {
    const isMarkedTest = p.info.packages.some((pkg) => markers.includes(pkg.id));
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
      for (const fw of p.info.frameworks) {
        if (innerFrameworks.includes(fw)) {
          violations.push(`${p.rel}: ${p.role.role} must not reference framework '${fw}' (transport types, ${owner})`);
        }
      }
      if (persistence && (persistence.forbiddenInRoles || []).includes(p.role.role)) {
        for (const pkg of p.info.packages) {
          if ((persistence.persistencePackagePrefixes || []).some((prefix) => (pkg.id || '').startsWith(prefix))) {
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
    const ctx = resolveContext(process.cwd());
    const configRoot = requireConfigRoot(ctx);
    const activeRoot = ctx.activeRoot || configRoot;
    const { applicable, violations, warnings } = checkArchitecture({ activeRoot, configRoot });
    console.log(`Architecture check of ${toPosix(activeRoot)}`);
    if (!applicable) console.log('Architecture check: NOT APPLICABLE (no backend directory).');
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
