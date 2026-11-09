// Kind: ENF | Scope: common | Owner: manifest checks — Central Package Management, version hygiene, package deny-lists, npm categories and lockfile, project-reference direction | Loading: run by verify/add-dependency and by the post-edit hook
//
// Usage: node .claude/scripts/check-dependencies.cjs            (scan the repository; exit 1 on errors)
//        node .claude/scripts/check-dependencies.cjs <file>...  (check specific manifests)
// Owners of the checked rules: .claude/rules/common/dependencies.md, .claude/rules/backend/architecture.md,
// .claude/rules/backend-tests/testing.md, decision register (D-01, D-05, D-10, D-11, D-12, D-17), add-dependency workflow.
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const SKIP_DIRS = new Set(['bin', 'obj', 'node_modules', '.git', 'dist', '.angular', 'TestResults', 'coverage']);

const DEPRECATED_NUGET = {
  'microsoft.extensions.http.polly': 'deprecated; use Microsoft.Extensions.Http.Resilience (D-12, add-dependency § Package-specific choices)',
  'polly.extensions.http': 'deprecated; use Microsoft.Extensions.Http.Resilience (D-12, add-dependency § Package-specific choices)',
  'serilog.sinks.elasticsearch': 'deprecated; use Elastic.Serilog.Sinks (logging knowledge)',
  'fluentvalidation.aspnetcore': 'deprecated automatic-validation integration; use FluentValidation.DependencyInjectionExtensions (D-05)',
};
const DECISION_NUGET = {
  mediatr: 'mediator-based organization is not adopted (D-02); requires an approved decision',
  automapper: 'mapping framework other than the approved one (D-11); requires an approved decision',
  polly: 'direct Polly is an explicit exception (add-dependency § Package-specific choices); document the reason',
};
const NOT_DEFAULT_NPM = ['@ngrx/', '@ngxs/', 'axios', 'lodash', 'lodash-es', 'bootstrap', 'ngx-bootstrap', '@ng-bootstrap/ng-bootstrap', 'tailwindcss', 'primeng'];
const DEV_TOOLING_NPM = [/^@angular\/cli$/, /^@angular-devkit\//, /^@angular\/build$/, /^@angular\/compiler-cli$/, /^typescript$/, /^vitest$/, /^@vitest\//, /^jsdom$/, /^@playwright\/test$/, /^karma/, /^jasmine/, /^@types\//, /^eslint/, /^@eslint\//, /^prettier$/];

const LAYERS = ['Domain', 'Application', 'Infrastructure', 'Api'];
const ALLOWED_PRODUCTION_REFERENCES = {
  Domain: [],
  Application: ['Domain'],
  Infrastructure: ['Application', 'Domain'],
  Api: ['Application', 'Infrastructure', 'Domain'],
};
const TYPICAL_TEST_REFERENCES = {
  'Domain.Tests': ['Domain'],
  'Application.Tests': ['Application', 'Domain'],
  'Infrastructure.Tests': ['Infrastructure', 'Application', 'Domain'],
  IntegrationTests: ['Api'],
};

function isManifest(rel) {
  const name = rel.split('/').pop();
  return name.endsWith('.csproj') || name === 'Directory.Packages.props' || name === 'package.json';
}

function classifyProject(projectName) {
  if (projectName.endsWith('.IntegrationTests') || projectName === 'IntegrationTests') return { kind: 'test', role: 'IntegrationTests' };
  const testMatch = projectName.match(/\.(Domain|Application|Infrastructure|Api)\.Tests$/);
  if (testMatch) return { kind: 'test', role: `${testMatch[1]}.Tests` };
  if (/Tests$/.test(projectName)) return { kind: 'test', role: 'other' };
  const layer = LAYERS.find((l) => projectName.endsWith(`.${l}`));
  return layer ? { kind: 'production', role: layer } : { kind: 'unknown', role: projectName };
}

function layerOf(projectName) {
  const c = classifyProject(projectName);
  return c.kind === 'production' ? c.role : c.kind === 'test' ? 'test' : 'unknown';
}

function checkCsproj(rel, text, result) {
  const projectName = path.basename(rel, '.csproj');
  const refRe = /<PackageReference\b([^>]*?)(\/>|>([\s\S]*?)<\/PackageReference>)/g;
  for (const m of text.matchAll(refRe)) {
    const attrs = m[1];
    const include = (attrs.match(/\bInclude\s*=\s*"([^"]+)"/) || [])[1] || '?';
    if (/\bVersion\s*=/.test(attrs) || /<Version>/.test(m[3] || '')) {
      result.errors.push(`${rel}: PackageReference ${include} has a version; versions belong in Directory.Packages.props (rules/common/dependencies.md § NuGet).`);
    }
    if (/\bVersionOverride\s*=/.test(attrs)) {
      result.notices.push(`${rel}: PackageReference ${include} uses VersionOverride; it needs a concrete, reported reason (rules/common/dependencies.md § NuGet).`);
    }
    checkNugetName(rel, include, result);
  }

  const projectRefs = [...text.matchAll(/<ProjectReference\b[^>]*\bInclude\s*=\s*"([^"]+)"/g)]
    .map((m) => path.basename(m[1].replace(/\\/g, '/'), '.csproj'));
  const self = classifyProject(projectName);
  for (const target of projectRefs) {
    const targetLayer = layerOf(target);
    if (self.kind === 'production') {
      if (targetLayer === 'test') {
        result.errors.push(`${rel}: production project references test project ${target} (rules/backend/architecture.md § Dependency direction).`);
      } else if (targetLayer !== 'unknown' && !ALLOWED_PRODUCTION_REFERENCES[self.role].includes(targetLayer)) {
        result.errors.push(`${rel}: ${self.role} must not reference ${targetLayer} (${target}); dependencies point inward (rules/backend/architecture.md § Dependency direction, D-01).`);
      } else if (targetLayer === 'unknown') {
        result.notices.push(`${rel}: reference to ${target}, which is not a recognized layer project; new production projects are Reserved (CLAUDE.md § Decisions).`);
      }
    } else if (self.kind === 'test' && TYPICAL_TEST_REFERENCES[self.role]) {
      const typical = TYPICAL_TEST_REFERENCES[self.role];
      if (targetLayer !== 'unknown' && targetLayer !== 'test' && !typical.includes(targetLayer)) {
        result.notices.push(`${rel}: ${self.role} references ${target}; confirm the test scope requires it (rules/backend-tests/testing.md § Test project references).`);
      }
    }
  }
  if (self.kind === 'unknown' && rel.startsWith('backend/')) {
    result.notices.push(`${rel}: project name does not follow backend/<Name>.<Layer> (D-18); new production projects are Reserved (CLAUDE.md § Decisions).`);
  }
}

function checkNugetName(rel, include, result) {
  const key = include.toLowerCase();
  if (DEPRECATED_NUGET[key]) result.errors.push(`${rel}: ${include} is ${DEPRECATED_NUGET[key]}.`);
  if (DECISION_NUGET[key]) result.notices.push(`${rel}: ${include}: ${DECISION_NUGET[key]}.`);
}

function checkPackagesProps(rel, text, result) {
  const cpm = text.match(/<ManagePackageVersionsCentrally>\s*(\w+)\s*<\/ManagePackageVersionsCentrally>/);
  if (!cpm || cpm[1].toLowerCase() !== 'true') {
    result.errors.push(`${rel}: ManagePackageVersionsCentrally must be true (D-17, rules/common/dependencies.md § NuGet).`);
  }
  for (const m of text.matchAll(/<PackageVersion\b[^>]*\bInclude\s*=\s*"([^"]+)"[^>]*\bVersion\s*=\s*"([^"]*)"/g)) {
    const [, include, version] = m;
    if (!version.trim() || /[*[\]()]/.test(version)) {
      result.errors.push(`${rel}: ${include} uses a floating or range version "${version}"; pin the verified stable version (add-dependency § 2).`);
    } else if (/-/.test(version)) {
      result.notices.push(`${rel}: ${include} ${version} is a prerelease; allowed only when explicitly requested (add-dependency § 2).`);
    }
    checkNugetName(rel, include, result);
  }
}

function checkPackageJson(rootDir, rel, text, result) {
  let json;
  try {
    json = JSON.parse(text);
  } catch (error) {
    result.errors.push(`${rel}: invalid JSON (${error.message}).`);
    return;
  }
  for (const section of ['dependencies', 'devDependencies', 'optionalDependencies']) {
    for (const [name, version] of Object.entries(json[section] || {})) {
      if (typeof version === 'string' && (/^(\*|latest|x)?$/i.test(version.trim()) || version.includes('*'))) {
        result.errors.push(`${rel}: ${section}.${name} uses floating version "${version}"; use the verified stable version (add-dependency § 2).`);
      }
      if (NOT_DEFAULT_NPM.some((p) => (p.endsWith('/') ? name.startsWith(p) : name === p))) {
        result.notices.push(`${rel}: ${name} is not added by default (D-10); it needs a concrete requirement.`);
      }
      if (section === 'dependencies' && DEV_TOOLING_NPM.some((re) => re.test(name))) {
        result.notices.push(`${rel}: ${name} is build/test tooling; it belongs in devDependencies (rules/common/dependencies.md § npm).`);
      }
    }
  }
  const lockfile = path.join(rootDir, path.dirname(rel), 'package-lock.json');
  if (!fs.existsSync(lockfile)) {
    result.notices.push(`${rel}: no package-lock.json next to package.json; commit a consistent lockfile (rules/common/dependencies.md § npm).`);
  }
}

function checkFile(rootDir, rel) {
  const result = { errors: [], notices: [] };
  const full = path.join(rootDir, rel);
  if (!fs.existsSync(full)) return result; // deleted or not yet written
  const text = fs.readFileSync(full, 'utf8');
  const name = rel.split('/').pop();
  if (name.endsWith('.csproj')) checkCsproj(rel, text, result);
  else if (name === 'Directory.Packages.props') checkPackagesProps(rel, text, result);
  else if (name === 'package.json') checkPackageJson(rootDir, rel, text, result);
  return result;
}

function findManifests(rootDir, dir = rootDir, found = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name) && !entry.name.startsWith('.')) findManifests(rootDir, path.join(dir, entry.name), found);
    } else {
      const rel = path.relative(rootDir, path.join(dir, entry.name)).split(path.sep).join('/');
      if (isManifest(rel)) found.push(rel);
    }
  }
  return found;
}

function checkRepository(rootDir) {
  const total = { errors: [], notices: [], files: [] };
  const files = findManifests(rootDir);
  const hasCsproj = files.some((f) => f.endsWith('.csproj'));
  if (hasCsproj && !files.includes('Directory.Packages.props')) {
    total.errors.push('Directory.Packages.props is missing at the repository root (D-17).');
  }
  for (const rel of files) {
    const r = checkFile(rootDir, rel);
    total.errors.push(...r.errors);
    total.notices.push(...r.notices);
    total.files.push(rel);
  }
  return total;
}

function main(args) {
  const rootDir = ROOT;
  const targets = args.filter((a) => !a.startsWith('--'));
  let result;
  if (targets.length > 0) {
    result = { errors: [], notices: [], files: [] };
    for (const target of targets) {
      const absolute = path.resolve(process.cwd(), target);
      const rel = path.relative(rootDir, absolute).split(path.sep).join('/');
      if (rel.startsWith('..') || path.isAbsolute(rel)) {
        result.errors.push(`${target}: outside the repository root ${rootDir}.`);
        continue;
      }
      if (!fs.existsSync(absolute)) {
        result.errors.push(`${target}: file not found.`);
        continue;
      }
      if (!isManifest(rel)) {
        result.errors.push(`${target}: not a supported manifest (*.csproj, Directory.Packages.props, package.json).`);
        continue;
      }
      const r = checkFile(rootDir, rel);
      result.errors.push(...r.errors);
      result.notices.push(...r.notices);
      result.files.push(rel);
    }
  } else {
    result = checkRepository(rootDir);
  }
  for (const e of result.errors) console.log(`ERROR  ${e}`);
  for (const n of result.notices) console.log(`NOTICE ${n}`);
  console.log(`check-dependencies: ${result.files.length} manifest(s), ${result.errors.length} error(s), ${result.notices.length} notice(s).`);
  process.exit(result.errors.length > 0 ? 1 : 0);
}

if (require.main === module) main(process.argv.slice(2));

module.exports = { isManifest, checkFile, checkRepository, classifyProject };
