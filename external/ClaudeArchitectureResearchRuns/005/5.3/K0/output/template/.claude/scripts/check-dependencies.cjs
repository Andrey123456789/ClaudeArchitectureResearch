// Kind: ENF | Scope: common | Owner: manifest checks — Central Package Management, version hygiene, package deny-lists, npm categories and lockfile, project-reference direction and integrity | Loading: run by verify/add-dependency and by the post-change hook
//
// Usage (from any directory of the repository or worktree, Bash or PowerShell):
//   node "$(git rev-parse --show-toplevel)/.claude/scripts/check-dependencies.cjs"            scan every manifest (exit 1 on errors)
//   node "$(git rev-parse --show-toplevel)/.claude/scripts/check-dependencies.cjs" <file>...  check specific manifests
//   --root <dir> overrides the checked repository root (default: the Git work tree of the current directory).
// Conforms to: rules/common/dependencies.md, rules/backend/architecture.md, rules/backend-tests/testing.md and the decision register (D-01, D-02, D-05, D-10, D-11, D-12, D-17, D-18).
// Findings point to their owners; version-selection findings point to the `add-dependency` workflow.
'use strict';

const fs = require('fs');
const path = require('path');
const { resolveRoot, readText } = require('./repo.cjs');

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

// Manifests the repository scan and the post-change hook track: outside build output, dependency caches and dot-directories.
function isTrackedManifest(rel) {
  return isManifest(rel) && !rel.split('/').slice(0, -1).some((segment) => SKIP_DIRS.has(segment) || segment.startsWith('.'));
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

// One start-tag reader for every manifest element the checks use: attributes in any order, whitespace around `=`,
// values in either matching XML quote delimiter ("…" or '…'). A start tag whose attributes cannot be read (unclosed
// or mismatched quote, unquoted value) is marked malformed instead of being guessed at or skipped.
const XML_ATTRIBUTE = /\s+([A-Za-z_][\w.:-]*)\s*=\s*(?:"([^"<]*)"|'([^'<]*)')/y;
const XML_TAG_END = /\s*(\/?)>/y;

// Elements named `name` in document order: { line, attributes: Map, content } (content: text of a paired element
// up to its closing tag, '' when self-closing) or { line, malformed: true }.
function xmlElements(text, name) {
  const elements = [];
  for (const open of text.matchAll(new RegExp(`<${name}(?=[\\s/>])`, 'g'))) {
    const line = text.slice(0, open.index).split('\n').length;
    const attributes = new Map();
    let at = open.index + open[0].length;
    for (;;) {
      XML_ATTRIBUTE.lastIndex = at;
      const m = XML_ATTRIBUTE.exec(text);
      if (!m) break;
      if (!attributes.has(m[1])) attributes.set(m[1], m[2] ?? m[3]);
      at = XML_ATTRIBUTE.lastIndex;
    }
    XML_TAG_END.lastIndex = at;
    const end = XML_TAG_END.exec(text);
    if (!end) {
      elements.push({ line, malformed: true });
      continue;
    }
    const close = end[1] ? -1 : text.indexOf(`</${name}>`, XML_TAG_END.lastIndex);
    elements.push({ line, attributes, content: close >= 0 ? text.slice(XML_TAG_END.lastIndex, close) : '' });
  }
  return elements;
}

// Reports an unreadable element (an error, so it is never accepted silently); true when the element is readable.
function readable(rel, name, element, result) {
  if (!element.malformed) return true;
  result.errors.push(`${rel}: <${name}> at line ${element.line} is not well-formed XML (unclosed or mismatched attribute quote, or an unquoted value); fix it so the manifest can be checked.`);
  return false;
}

// ProjectReference targets as written (backslashes normalized), in document order, in either quote style.
function projectReferences(text) {
  return xmlElements(text, 'ProjectReference')
    .map((element) => element.attributes?.get('Include'))
    .filter(Boolean)
    .map((include) => include.replace(/\\/g, '/'));
}

function checkCsproj(rootDir, rel, text, result) {
  const projectName = path.basename(rel, '.csproj');
  for (const element of xmlElements(text, 'PackageReference')) {
    if (!readable(rel, 'PackageReference', element, result)) continue;
    const { attributes, content } = element;
    const include = attributes.get('Include') || '?';
    if (attributes.has('Version') || /<Version>/.test(content)) {
      result.errors.push(`${rel}: PackageReference ${include} has a version; versions belong in Directory.Packages.props (rules/common/dependencies.md § NuGet).`);
    }
    if (attributes.has('VersionOverride')) {
      result.notices.push(`${rel}: PackageReference ${include} uses VersionOverride; it needs a concrete, reported reason (rules/common/dependencies.md § NuGet).`);
    }
    checkNugetName(rel, include, result);
  }
  for (const element of xmlElements(text, 'ProjectReference')) readable(rel, 'ProjectReference', element, result);

  const self = classifyProject(projectName);
  for (const reference of projectReferences(text)) {
    const target = path.basename(reference, '.csproj');
    if (!reference.includes('$(') && !fs.existsSync(path.resolve(rootDir, path.dirname(rel), reference))) {
      result.errors.push(`${rel}: ProjectReference ${reference} points to a project that does not exist (project-structure).`);
    }
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
  for (const element of xmlElements(text, 'PackageVersion')) {
    if (!readable(rel, 'PackageVersion', element, result)) continue;
    const include = element.attributes.get('Include');
    const version = element.attributes.get('Version');
    if (!include || version === undefined) continue;
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

// Checks one manifest of the repository at rootDir. A missing file yields no findings (removals are reported by the caller).
function checkFile(rootDir, rel) {
  const result = { errors: [], notices: [] };
  const full = path.join(rootDir, rel);
  if (!fs.existsSync(full)) return result;
  const decoded = readText(full);
  if (decoded.error) {
    result.errors.push(`${rel}: ${decoded.error}; save it as UTF-8 (or UTF-16 with a byte-order mark) so it can be checked.`);
    return result;
  }
  const text = decoded.text;
  const name = rel.split('/').pop();
  if (name.endsWith('.csproj')) checkCsproj(rootDir, rel, text, result);
  else if (name === 'Directory.Packages.props') checkPackagesProps(rel, text, result);
  else if (name === 'package.json') checkPackageJson(rootDir, rel, text, result);
  return result;
}

// Every tracked manifest below rootDir; nested repositories and worktrees (directories with their own .git) are not descended into.
function findManifests(rootDir, dir = rootDir, found = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name) && !entry.name.startsWith('.') && !fs.existsSync(path.join(full, '.git'))) findManifests(rootDir, full, found);
    } else if (entry.isFile()) {
      const rel = path.relative(rootDir, full).split(path.sep).join('/');
      if (isTrackedManifest(rel)) found.push(rel);
    }
  }
  return found;
}

function checkRepository(rootDir) {
  const total = { errors: [], notices: [], files: [] };
  const files = findManifests(rootDir);
  if (files.some((f) => f.endsWith('.csproj')) && !files.includes('Directory.Packages.props')) {
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
  const rootIndex = args.indexOf('--root');
  const explicitRoot = rootIndex >= 0 ? args[rootIndex + 1] : null;
  const targets = args.filter((a, i) => !a.startsWith('--') && !(rootIndex >= 0 && i === rootIndex + 1));
  const resolved = resolveRoot(explicitRoot || process.cwd());
  if (!resolved) {
    console.log(`ERROR  cannot resolve a repository root from ${explicitRoot || process.cwd()}.`);
    process.exit(1);
  }
  const rootDir = resolved.root;
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
  console.log(`check-dependencies: ${rootDir}: ${result.files.length} manifest(s), ${result.errors.length} error(s), ${result.notices.length} notice(s).`);
  process.exit(result.errors.length > 0 ? 1 : 0);
}

if (require.main === module) main(process.argv.slice(2));

module.exports = { isManifest, isTrackedManifest, checkFile, checkRepository, classifyProject, projectReferences };
