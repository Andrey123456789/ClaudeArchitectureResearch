// Kind: ENF | Scope: common | Owns: deterministic package-manifest and project-reference checks | Loads: CLI (node .claude/scripts/check-manifests.mjs [root]) and post-edit hook
//
// Checks (owners in parentheses):
// - Central Package Management enabled; no versions on PackageReference (rules/common/dependencies.md § NuGet)
// - no floating versions; prerelease/range versions flagged (add-dependency § 2)
// - deprecated packages (add-dependency § 5); gated packages need an Adopted/Conditional register entry
// - backend project references follow the layer direction (rules/backend/architecture.md, rules/backend-tests/testing.md)
// - npm: lockfile present, no floating versions, build/test tooling not in runtime dependencies (rules/common/dependencies.md § npm)

import { existsSync, readdirSync, readFileSync } from 'node:fs';
import path from 'node:path';

const SKIP_DIRS = new Set(['bin', 'obj', 'node_modules', '.git', '.angular', 'dist', 'TestResults', 'coverage']);
const REGISTER = 'docs/architecture/decision-register.md';

const DEPRECATED_NUGET = new Map([
  ['microsoft.extensions.http.polly', 'deprecated; resilience packages: add-dependency § 5'],
  ['polly.extensions.http', 'deprecated; resilience packages: add-dependency § 5'],
  ['serilog.sinks.elasticsearch', 'deprecated; use Elastic.Serilog.Sinks (logging skill, Serilog reference)'],
]);

// Packages that need a recorded decision (an Adopted or Conditional register row naming them).
const GATED_NUGET = [
  [/^mediatr(\..+)?$/i, 'mediator/CQRS organization (DEC-ARCH-02)'],
  [/^automapper(\..+)?$/i, 'second mapping framework (DEC-MAP-01; CLAUDE.md § Decisions)'],
  [/^polly(\.core)?$/i, 'direct Polly usage (add-dependency § 5)'],
  [/^(xunit(\..+)?|mstest(\..+)?)$/i, 'second test framework (rules/backend-tests/testing.md)'],
  [/^(npgsql\.entityframeworkcore\..+|pomelo\.entityframeworkcore\..+|mongodb\..+)$/i, 'persistence technology change (DEC-DATA-01)'],
  [/^(masstransit(\..+)?|nservicebus(\..+)?|rabbitmq\.client|azure\.messaging\..+|confluent\.kafka)$/i, 'messaging infrastructure (CLAUDE.md § Decisions)'],
  [/^(hangfire(\..+)?|quartz(\..+)?)$/i, 'background-processing infrastructure (CLAUDE.md § Decisions)'],
  [/^(stackexchange\.redis|microsoft\.extensions\.caching\.stackexchangeredis)$/i, 'distributed cache (CLAUDE.md § Decisions)'],
  [/^asp\.versioning\..+$/i, 'API versioning (DEC-VER-01)'],
  [/^mapster(\..+)?$/i, 'conditional mapping (DEC-MAP-01)'],
  [/^testcontainers(\..+)?$/i, 'conditional test infrastructure (DEC-TEST-01)'],
];

const GATED_NPM = [
  [/^@ngrx\//, 'state-management library (DEC-WEB-02)'],
  [/^(axios|lodash|lodash-es|bootstrap|tailwindcss|@tailwindcss\/.+)$/, 'library not added by default (DEC-WEB-02)'],
  [/^@playwright\/test$/, 'conditional E2E tooling (DEC-WEB-03)'],
];

const NPM_TOOLING = /^(vitest|jest|karma(-.+)?|jasmine(-.+)?|typescript|eslint(-.+)?|prettier|@angular\/cli|@angular\/build|@angular-devkit\/.+|@angular\/compiler-cli|@playwright\/test|@types\/.+)$/;

const LAYER_REFERENCES = {
  Domain: [],
  Application: ['Domain'],
  Infrastructure: ['Application', 'Domain'],
  Api: ['Application', 'Infrastructure', 'Domain'],
};

function walk(root, predicate, dir = root, found = []) {
  if (!existsSync(dir)) return found;
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name)) walk(root, predicate, full, found);
    } else if (predicate(entry.name)) {
      found.push(full);
    }
  }
  return found;
}

const rel = (root, file) => path.relative(root, file).split(path.sep).join('/');

function approvedText(root) {
  const file = path.join(root, REGISTER);
  if (!existsSync(file)) return '';
  const text = readFileSync(file, 'utf8');
  // Only Adopted and Conditional sections approve a package; Not Adopted rows do not.
  return text
    .split(/^## /m)
    .filter((section) => /^(Adopted|Conditional)\b/.test(section))
    .join('\n')
    .toLowerCase();
}

// A package is approved when the Adopted/Conditional sections name it or one of its dotted/scoped
// prefixes (for example "Asp.Versioning" approves "Asp.Versioning.Mvc").
function isApproved(approved, id) {
  const segments = id.toLowerCase().replace(/^@/, '').split(/[./]/).filter(Boolean);
  for (let count = segments.length; count >= 1; count -= 1) {
    const prefix = segments.slice(0, count).join('.');
    if ((count > 1 || prefix.length > 4) && approved.includes(prefix)) {
      return true;
    }
  }
  return false;
}

export function projectLayer(projectName) {
  const parts = projectName.split('.');
  const last = parts[parts.length - 1];
  if (/^IntegrationTests$/i.test(last)) return { kind: 'integration-tests' };
  if (/^Tests$/i.test(last) && parts.length >= 2) {
    const tested = parts[parts.length - 2];
    return LAYER_REFERENCES[tested] ? { kind: 'tests', layer: tested } : { kind: 'unknown' };
  }
  return LAYER_REFERENCES[last] ? { kind: 'production', layer: last } : { kind: 'unknown' };
}

function versionProblems(id, version, source, findings) {
  if (!version) return;
  if (version.includes('*') || /^latest$/i.test(version)) {
    findings.push({ severity: 'error', file: source, message: `${id}: floating version "${version}" — select an exact stable version (add-dependency § 2)` });
  } else if (/^[[(]/.test(version) || /^[~^><=]/.test(version)) {
    findings.push({ severity: 'notice', file: source, message: `${id}: version range "${version}" — prefer the exact latest stable compatible version (add-dependency § 2)` });
  } else if (/-[0-9A-Za-z]/.test(version)) {
    findings.push({ severity: 'notice', file: source, message: `${id}: prerelease version "${version}" — only when explicitly requested (add-dependency § 2)` });
  }
}

function checkNuGet(root, findings) {
  const projects = walk(root, (name) => name.endsWith('.csproj'));
  const propsFile = path.join(root, 'Directory.Packages.props');
  const approved = approvedText(root);

  if (projects.length && !existsSync(propsFile)) {
    findings.push({ severity: 'error', file: 'Directory.Packages.props', message: 'missing — Central Package Management is required (rules/common/dependencies.md § NuGet)' });
  }
  if (existsSync(propsFile)) {
    const props = readFileSync(propsFile, 'utf8');
    if (!/<ManagePackageVersionsCentrally>\s*true\s*<\/ManagePackageVersionsCentrally>/i.test(props)) {
      findings.push({ severity: 'error', file: 'Directory.Packages.props', message: 'ManagePackageVersionsCentrally is not true (rules/common/dependencies.md § NuGet)' });
    }
    for (const match of props.matchAll(/<PackageVersion\b([^>]*)>/gi)) {
      const attributes = match[1];
      const id = (attributes.match(/\bInclude="([^"]+)"/i) ?? [])[1];
      const version = (attributes.match(/\bVersion="([^"]*)"/i) ?? [])[1];
      if (!id) continue;
      versionProblems(id, version, 'Directory.Packages.props', findings);
      packageGates(id, 'Directory.Packages.props', approved, findings);
    }
  }

  const byName = new Map(projects.map((file) => [path.basename(file, '.csproj').toLowerCase(), file]));
  for (const file of projects) {
    const source = rel(root, file);
    const text = readFileSync(file, 'utf8');
    for (const match of text.matchAll(/<PackageReference\b([^>]*?)(\/>|>([\s\S]*?)<\/PackageReference>)/gi)) {
      const attributes = match[1];
      const body = match[3] ?? '';
      const id = (attributes.match(/\bInclude="([^"]+)"/i) ?? [])[1] ?? '?';
      if (/\bVersion="/i.test(attributes) || /<Version>/i.test(body)) {
        findings.push({ severity: 'error', file: source, message: `${id}: version on PackageReference — versions belong in Directory.Packages.props (rules/common/dependencies.md § NuGet)` });
      } else if (/\bVersionOverride="/i.test(attributes) || /<VersionOverride>/i.test(body)) {
        findings.push({ severity: 'notice', file: source, message: `${id}: VersionOverride — needs a concrete, reported reason (rules/common/dependencies.md § NuGet)` });
      }
      packageGates(id, source, approved, findings);
    }

    const self = projectLayer(path.basename(file, '.csproj'));
    if (self.kind === 'unknown' || self.kind === 'integration-tests') continue;
    const allowed = self.kind === 'production'
      ? LAYER_REFERENCES[self.layer]
      : [self.layer, ...LAYER_REFERENCES[self.layer]];
    for (const match of text.matchAll(/<ProjectReference\b[^>]*\bInclude="([^"]+)"/gi)) {
      const targetName = path.basename(match[1].split('\\').join('/'), '.csproj');
      const target = projectLayer(targetName);
      if (target.kind !== 'production') continue;
      if (!allowed.includes(target.layer)) {
        const owner = self.kind === 'tests'
          ? 'rules/backend-tests/testing.md § Test Project References'
          : 'rules/backend/architecture.md § Dependency Direction';
        findings.push({ severity: 'error', file: source, message: `project reference to ${targetName} is not allowed for a ${self.layer}${self.kind === 'tests' ? ' test' : ''} project (${owner})` });
      }
      if (!byName.has(targetName.toLowerCase())) {
        findings.push({ severity: 'notice', file: source, message: `project reference ${match[1]} does not resolve to a project in the repository` });
      }
    }
  }
}

function packageGates(id, source, approved, findings) {
  const lower = id.toLowerCase();
  if (DEPRECATED_NUGET.has(lower)) {
    findings.push({ severity: 'error', file: source, message: `${id}: ${DEPRECATED_NUGET.get(lower)}` });
    return;
  }
  for (const [pattern, reason] of GATED_NUGET) {
    if (pattern.test(id) && !isApproved(approved, id)) {
      findings.push({ severity: 'notice', file: source, message: `${id}: ${reason} — needs a recorded decision or its register condition (architecture-decision)` });
    }
  }
}

function checkNpm(root, findings) {
  const approved = approvedText(root);
  const manifests = walk(root, (name) => name === 'package.json');
  for (const file of manifests) {
    const source = rel(root, file);
    let json;
    try {
      json = JSON.parse(readFileSync(file, 'utf8'));
    } catch (error) {
      findings.push({ severity: 'error', file: source, message: `invalid JSON (${error.message})` });
      continue;
    }
    if (!existsSync(path.join(path.dirname(file), 'package-lock.json'))) {
      findings.push({ severity: 'notice', file: source, message: 'no package-lock.json beside package.json (rules/common/dependencies.md § npm)' });
    }
    for (const section of ['dependencies', 'devDependencies']) {
      for (const [id, version] of Object.entries(json[section] ?? {})) {
        versionProblems(id, String(version), source, findings);
        for (const [pattern, reason] of GATED_NPM) {
          if (pattern.test(id) && !isApproved(approved, id)) {
            findings.push({ severity: 'notice', file: source, message: `${id}: ${reason} — needs a recorded decision or its register condition (architecture-decision)` });
          }
        }
        if (section === 'dependencies' && NPM_TOOLING.test(id)) {
          findings.push({ severity: 'notice', file: source, message: `${id}: build/test tooling in runtime dependencies — use devDependencies (rules/common/dependencies.md § npm)` });
        }
      }
    }
  }
}

export function checkManifests(root) {
  const findings = [];
  checkNuGet(root, findings);
  checkNpm(root, findings);
  return { findings, errors: findings.filter((f) => f.severity === 'error') };
}

export function formatFindings(findings) {
  return findings.map((f) => `- [${f.severity}] ${f.file}: ${f.message}`).join('\n');
}

const isEntryPoint = process.argv[1] && import.meta.url.endsWith(process.argv[1].split(/[\\/]/).pop());
if (isEntryPoint) {
  const root = path.resolve(process.argv[2] ?? process.env.CLAUDE_PROJECT_DIR ?? process.cwd());
  if (!existsSync(path.join(root, 'CLAUDE.md'))) {
    process.stderr.write(`check-manifests: ${root} is not the project root (CLAUDE.md not found); pass the root as the first argument.\n`);
    process.exit(2);
  }
  const { findings, errors } = checkManifests(root);
  process.stdout.write(findings.length ? `${formatFindings(findings)}\n` : 'check-manifests: no findings\n');
  process.exit(errors.length ? 1 : 0);
}
