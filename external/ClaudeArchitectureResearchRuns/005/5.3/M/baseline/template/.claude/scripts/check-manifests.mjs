#!/usr/bin/env node
// Manifest checker: NuGet Central Package Management, package version forms,
// deprecated or approval-gated packages, npm manifest hygiene, and backend
// project-reference direction.
//
// Usage (from the repository root, any OS, Node.js 18+):
//   node .claude/scripts/check-manifests.mjs              scan the whole repository
//   node .claude/scripts/check-manifests.mjs <file> ...   check specific manifests
//
// Exit codes: 0 = no violations, 1 = violations found, 2 = the checker could not run.
// Rule owners: .claude/rules/dependencies.md, .claude/rules/architecture.md
// (Project References), and the add-dependency skill. Used by the hooks in
// .claude/hooks/.

import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, resolve, dirname, basename, relative, sep, isAbsolute } from 'node:path';
import { fileURLToPath } from 'node:url';

const SKIP_DIRS = new Set([
  '.git', '.vs', '.idea', '.angular', 'node_modules', 'bin', 'obj', 'dist',
  'TestResults', 'coverage', 'artifacts',
]);

// Packages that must not be added.
const DENIED_NUGET = new Map([
  ['microsoft.extensions.http.polly', 'deprecated integration package - see add-dependency (package choices)'],
  ['polly.extensions.http', 'deprecated integration package - see add-dependency (package choices)'],
]);

// Packages that are allowed only with an explicit decision or reason.
const REVIEW_NUGET = new Map([
  ['mediatr', 'mediator-based organization is not adopted - requires an approved decision (CLAUDE.md, Architecture Defaults)'],
  ['polly', 'direct Polly usage is a documented exception - see add-dependency (package choices)'],
  ['polly.core', 'direct Polly usage is a documented exception - see add-dependency (package choices)'],
  ['fluentvalidation.aspnetcore', 'legacy automatic-validation integration - needs a concrete reason (docs/technology-stack.md)'],
  ['serilog.sinks.elasticsearch', 'deprecated sink package - see the logging skill'],
]);

const REVIEW_NPM_EXACT = new Set(['axios', 'lodash', 'bootstrap', 'tailwindcss']);
const REVIEW_NPM_PREFIX = ['@ngrx/'];
const NPM_TOOLING_EXACT = new Set([
  'typescript', 'vitest', 'jsdom', 'eslint', 'prettier', 'karma', 'jasmine-core',
  'playwright', '@playwright/test', '@angular/cli', '@angular/build', '@angular/compiler-cli',
]);
const NPM_TOOLING_PREFIX = ['@angular-devkit/', '@types/', 'karma-', '@vitest/', 'eslint-', '@typescript-eslint/'];

const LAYERS = ['Domain', 'Application', 'Infrastructure', 'Api'];
const PRODUCTION_ALLOWED = {
  Domain: [],
  Application: ['Domain'],
  Infrastructure: ['Domain', 'Application'],
  Api: ['Domain', 'Application', 'Infrastructure'],
};
// A test project may reference the layer it tests and the layers inward of it.
const TEST_ALLOWED = {
  Domain: ['Domain'],
  Application: ['Domain', 'Application'],
  Infrastructure: ['Domain', 'Application', 'Infrastructure'],
  Api: ['Domain', 'Application', 'Infrastructure', 'Api'],
};

export function checkManifests(root, files) {
  const result = { violations: [], notes: [], checked: [] };
  const targets = files && files.length > 0 ? files.map((f) => resolve(root, f)) : discover(root);
  const checkedProps = new Set();

  for (const file of targets) {
    const rel = toRel(root, file);
    if (rel === null) {
      result.notes.push({ file, message: 'outside the repository root - not checked' });
      continue;
    }
    if (!existsSync(file)) {
      result.notes.push({ file: rel, message: 'file does not exist (deleted?) - not checked' });
      continue;
    }
    const name = basename(file);
    if (name.toLowerCase().endsWith('.csproj')) {
      checkProject(root, file, result, checkedProps);
    } else if (name === 'Directory.Packages.props') {
      checkCentralProps(root, file, result, checkedProps);
    } else if (name === 'package.json') {
      checkPackageJson(root, file, result);
    } else {
      continue;
    }
    result.checked.push(rel);
  }
  return result;
}

export function formatResult(result) {
  const lines = [];
  for (const v of result.violations) lines.push(`VIOLATION ${v.file}: ${v.message}`);
  for (const n of result.notes) lines.push(`NOTE      ${n.file}: ${n.message}`);
  return lines;
}

function discover(root) {
  const found = [];
  const walk = (dir) => {
    let entries;
    try {
      entries = readdirSync(dir, { withFileTypes: true });
    } catch {
      return;
    }
    for (const entry of entries) {
      if (entry.isDirectory()) {
        if (!SKIP_DIRS.has(entry.name) && entry.name !== '.claude') walk(join(dir, entry.name));
      } else if (entry.isFile()) {
        const lower = entry.name.toLowerCase();
        if (lower.endsWith('.csproj') || entry.name === 'Directory.Packages.props' || entry.name === 'package.json') {
          found.push(join(dir, entry.name));
        }
      }
    }
  };
  walk(root);
  return found;
}

function toRel(root, file) {
  const rel = relative(root, file);
  if (rel.startsWith('..') || isAbsolute(rel)) return null;
  return rel.split(sep).join('/');
}

function readXml(file) {
  return readFileSync(file, 'utf8').replace(/<!--[\s\S]*?-->/g, '');
}

function attributes(text) {
  const attrs = {};
  for (const m of text.matchAll(/\b([A-Za-z]+)\s*=\s*"([^"]*)"/g)) attrs[m[1].toLowerCase()] = m[2];
  return attrs;
}

function findCentralProps(root, projectFile) {
  let dir = dirname(projectFile);
  for (;;) {
    const candidate = join(dir, 'Directory.Packages.props');
    if (existsSync(candidate)) return candidate;
    if (resolve(dir) === resolve(root)) return null;
    const parent = dirname(dir);
    if (parent === dir) return null;
    dir = parent;
  }
}

function centralVersions(propsFile) {
  const versions = new Map();
  const xml = readXml(propsFile);
  for (const m of xml.matchAll(/<PackageVersion\b([^>]*?)\/?>/gi)) {
    const attrs = attributes(m[1]);
    if (attrs.include) versions.set(attrs.include.toLowerCase(), attrs.version ?? '');
  }
  return versions;
}

function checkCentralProps(root, file, result, checkedProps) {
  const key = resolve(file);
  if (checkedProps.has(key)) return;
  checkedProps.add(key);
  const rel = toRel(root, file);
  const xml = readXml(file);
  if (!/<ManagePackageVersionsCentrally>\s*true\s*<\/ManagePackageVersionsCentrally>/i.test(xml)) {
    result.violations.push({ file: rel, message: 'ManagePackageVersionsCentrally is not enabled (.claude/rules/dependencies.md, NuGet)' });
  }
  for (const m of xml.matchAll(/<PackageVersion\b([^>]*?)\/?>/gi)) {
    const attrs = attributes(m[1]);
    const id = attrs.include ?? '(missing Include)';
    checkNuGetId(id, rel, result);
    checkNuGetVersion(id, attrs.version, rel, result);
  }
}

function checkNuGetId(id, rel, result) {
  const lower = id.toLowerCase();
  if (DENIED_NUGET.has(lower)) result.violations.push({ file: rel, message: `${id}: ${DENIED_NUGET.get(lower)}` });
  if (REVIEW_NUGET.has(lower)) result.notes.push({ file: rel, message: `${id}: ${REVIEW_NUGET.get(lower)}` });
}

function checkNuGetVersion(id, version, rel, result) {
  if (version === undefined || version.trim() === '') {
    result.violations.push({ file: rel, message: `${id}: PackageVersion has no Version` });
    return;
  }
  const v = version.trim();
  if (v.includes('*') || /^[[(]/.test(v) || v.includes(',')) {
    result.violations.push({ file: rel, message: `${id}: floating or range version "${v}" - pin the latest stable compatible version (add-dependency)` });
  } else if (/^\d+(\.\d+)*-/.test(v)) {
    result.notes.push({ file: rel, message: `${id}: prerelease version "${v}" - allowed only when explicitly requested (add-dependency)` });
  }
}

function classifyProject(name) {
  if (/\.IntegrationTests$/i.test(name)) return { test: true, layer: 'Api' };
  let m = name.match(/\.(Domain|Application|Infrastructure|Api)\.Tests$/i);
  if (m) return { test: true, layer: canonicalLayer(m[1]) };
  if (/\.?Tests$/i.test(name)) return { test: true, layer: null };
  m = name.match(/\.(Domain|Application|Infrastructure|Api)$/i);
  if (m) return { test: false, layer: canonicalLayer(m[1]) };
  return null;
}

function canonicalLayer(value) {
  return LAYERS.find((layer) => layer.toLowerCase() === value.toLowerCase());
}

function checkProject(root, file, result, checkedProps) {
  const rel = toRel(root, file);
  const xml = readXml(file);
  const projectName = basename(file).replace(/\.csproj$/i, '');

  // Central Package Management
  const packageRefs = [...xml.matchAll(/<PackageReference\b([^>]*?)(?:\/>|>([\s\S]*?)<\/PackageReference>)/gi)];
  if (/<ManagePackageVersionsCentrally>\s*false\s*<\/ManagePackageVersionsCentrally>/i.test(xml)) {
    result.violations.push({ file: rel, message: 'project opts out of Central Package Management (.claude/rules/dependencies.md, NuGet)' });
  }
  let central = null;
  if (packageRefs.length > 0) {
    const propsFile = findCentralProps(root, file);
    if (!propsFile) {
      result.violations.push({ file: rel, message: 'package references exist but no Directory.Packages.props was found above this project (.claude/rules/dependencies.md, NuGet)' });
    } else {
      checkCentralProps(root, propsFile, result, checkedProps);
      central = centralVersions(propsFile);
    }
  }
  for (const m of packageRefs) {
    const attrs = attributes(m[1]);
    const id = attrs.include ?? attrs.update ?? '(missing Include)';
    checkNuGetId(id, rel, result);
    const childVersion = m[2] && /<Version>\s*([^<]*)<\/Version>/i.exec(m[2]);
    if (attrs.version !== undefined || childVersion) {
      result.violations.push({ file: rel, message: `${id}: version declared in the project file - versions belong in Directory.Packages.props (.claude/rules/dependencies.md, NuGet)` });
    }
    if (attrs.versionoverride !== undefined) {
      result.notes.push({ file: rel, message: `${id}: VersionOverride "${attrs.versionoverride}" needs a concrete, documented reason` });
    }
    if (central && attrs.include && !central.has(attrs.include.toLowerCase())) {
      result.notes.push({ file: rel, message: `${id}: no matching PackageVersion in Directory.Packages.props` });
    }
  }

  // Project reference direction
  const source = classifyProject(projectName);
  for (const m of xml.matchAll(/<ProjectReference\b[^>]*?\bInclude\s*=\s*"([^"]+)"/gi)) {
    const targetName = basename(m[1].replace(/\\/g, '/')).replace(/\.csproj$/i, '');
    const target = classifyProject(targetName);
    if (!source) {
      result.notes.push({ file: rel, message: `reference to ${targetName} not checked: "${projectName}" does not follow the <Name>.<Layer> naming` });
      continue;
    }
    if (!source.layer) {
      result.notes.push({ file: rel, message: `reference to ${targetName} not checked: tested layer of "${projectName}" is unknown (use <Name>.<Layer>.Tests or <Name>.IntegrationTests)` });
      continue;
    }
    if (!target) {
      result.notes.push({ file: rel, message: `reference to ${targetName} not checked: target does not follow the <Name>.<Layer> naming` });
      continue;
    }
    if (target.test) {
      if (!source.test) result.violations.push({ file: rel, message: `production project references test project ${targetName}` });
      continue;
    }
    const allowed = (source.test ? TEST_ALLOWED : PRODUCTION_ALLOWED)[source.layer];
    if (!allowed.includes(target.layer)) {
      const kind = source.test ? `${source.layer} test project` : `${source.layer} project`;
      result.violations.push({
        file: rel,
        message: `${kind} must not reference ${targetName} (${target.layer}) - see .claude/rules/architecture.md, Project References`,
      });
    }
  }
}

function checkPackageJson(root, file, result) {
  const rel = toRel(root, file);
  let manifest;
  try {
    manifest = JSON.parse(readFileSync(file, 'utf8'));
  } catch (error) {
    result.violations.push({ file: rel, message: `invalid JSON: ${error.message}` });
    return;
  }
  const sections = ['dependencies', 'devDependencies', 'optionalDependencies'];
  let dependencyCount = 0;
  for (const section of sections) {
    const deps = manifest[section];
    if (!deps || typeof deps !== 'object') continue;
    for (const [name, rawSpec] of Object.entries(deps)) {
      dependencyCount += 1;
      const spec = String(rawSpec).trim();
      if (/^(file:|link:|workspace:|npm:|git|https?:|github:)/i.test(spec)) continue;
      if (['', '*', 'x', 'X', 'latest', 'next'].includes(spec) || /(^|\.)[xX*]$/.test(spec) || /^>=?[^<]*$/.test(spec)) {
        result.violations.push({ file: rel, message: `${section}.${name}: floating version "${spec}" - pin the latest stable compatible version (add-dependency)` });
      } else if (/\d+\.\d+\.\d+-/.test(spec)) {
        result.notes.push({ file: rel, message: `${section}.${name}: prerelease version "${spec}" - allowed only when explicitly requested (add-dependency)` });
      }
      if (REVIEW_NPM_EXACT.has(name) || REVIEW_NPM_PREFIX.some((p) => name.startsWith(p))) {
        result.notes.push({ file: rel, message: `${name}: not added by default - needs a concrete requirement (docs/technology-stack.md, Frontend)` });
      }
      if (section === 'dependencies' && (NPM_TOOLING_EXACT.has(name) || NPM_TOOLING_PREFIX.some((p) => name.startsWith(p)))) {
        result.notes.push({ file: rel, message: `${name}: build/test tooling listed in dependencies - devDependencies expected (.claude/rules/dependencies.md, npm)` });
      }
    }
  }
  if (dependencyCount > 0 && !existsSync(join(dirname(file), 'package-lock.json'))) {
    result.notes.push({ file: rel, message: 'no package-lock.json next to package.json - commit the lockfile (.claude/rules/dependencies.md, npm)' });
  }
}

function isMain() {
  if (!process.argv[1]) return false;
  const self = fileURLToPath(import.meta.url);
  const invoked = resolve(process.argv[1]);
  return process.platform === 'win32' ? self.toLowerCase() === invoked.toLowerCase() : self === invoked;
}

if (isMain()) {
  const fromEnv = (process.env.CLAUDE_PROJECT_DIR ?? '').trim();
  const root = fromEnv ? resolve(fromEnv) : resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
  if (!existsSync(join(root, '.claude'))) {
    process.stderr.write(`check-manifests: "${root}" is not a repository root with a .claude directory; set CLAUDE_PROJECT_DIR.\n`);
    process.exit(2);
  }
  const result = checkManifests(root, process.argv.slice(2));
  for (const line of formatResult(result)) process.stdout.write(`${line}\n`);
  process.stdout.write(`check-manifests: ${result.checked.length} manifest(s) checked, ${result.violations.length} violation(s), ${result.notes.length} note(s)\n`);
  process.exit(result.violations.length > 0 ? 1 : 0);
}
