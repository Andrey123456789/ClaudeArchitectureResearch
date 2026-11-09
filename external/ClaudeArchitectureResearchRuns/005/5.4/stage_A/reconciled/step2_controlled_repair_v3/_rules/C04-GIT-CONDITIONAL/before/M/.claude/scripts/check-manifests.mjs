#!/usr/bin/env node
// Manifest checker: NuGet Central Package Management, package version forms,
// deprecated or approval-gated packages, npm manifest hygiene, and backend
// project-reference direction.
//
// Usage (any OS, Node.js 18+), from the repository root (the top level of the
// current checkout or worktree; `git rev-parse --show-toplevel` prints it):
//   node .claude/scripts/check-manifests.mjs              scan the whole repository
//   node .claude/scripts/check-manifests.mjs <file> ...   check specific manifests
// The repository checked is the active root resolved from the current directory
// (repo-root.mjs), not the checkout the script is installed in; <file>
// arguments are relative to the current directory.
//
// Exit codes: 0 = no violations, 1 = violations found, 2 = the checker could not run,
// 3 = no violations found, but the proof of effective Central Package Management did
// not run (report it as NOT RUN, never as passed).
// Rule owners: .claude/rules/dependencies.md, .claude/rules/architecture.md
// (Project References), and the add-dependency skill. Used by the hooks in
// .claude/hooks/.

import { spawnSync } from 'node:child_process';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, resolve, dirname, basename, relative, sep, isAbsolute } from 'node:path';
import { fileURLToPath } from 'node:url';
import { resolveActiveRoot, canonical } from './repo-root.mjs';

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
  const result = { violations: [], notes: [], notRun: [], checked: [], versionExceptions: [] };
  loadVersionExceptions(root, result);
  const targets = files && files.length > 0 ? files.map((f) => canonical(resolve(root, f))) : discover(root);
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
    } else if (!CPM_CHAIN_FILES.has(name)) {
      continue;
    }
    result.checked.push(rel);
  }
  reportCpm(root, targets, result);
  return result;
}

// The projects whose effective state these targets can change: a project itself, or every project below a chain file.
function cpmProjects(root, targets) {
  const projects = new Set();
  const all = () => discover(root).filter((file) => basename(file).toLowerCase().endsWith('.csproj')).map((file) => toRel(root, file));
  for (const file of targets) {
    const rel = toRel(root, file);
    if (rel === null || !existsSync(file)) continue;
    const name = basename(file);
    if (name.toLowerCase().endsWith('.csproj')) projects.add(rel);
    else if (CPM_CHAIN_FILES.has(name)) {
      const dir = dirname(rel);
      for (const project of all()) if (dir === '.' || project.startsWith(`${dir}/`)) projects.add(project);
    }
  }
  return [...projects];
}

function reportCpm(root, targets, result) {
  for (const project of cpmProjects(root, targets)) {
    const outcome = effectiveCpm(root, project);
    for (const message of outcome.errors) result.violations.push({ file: project, message: `${message} (.claude/rules/dependencies.md, NuGet)` });
    for (const message of outcome.notices) result.notes.push({ file: project, message: `${message} (add-dependency)` });
    if (outcome.notRun) result.notRun.push({ file: project, message: cpmNotRunMessage(outcome.notRun) });
  }
}

export function formatResult(result) {
  const lines = [];
  for (const v of result.violations) lines.push(`VIOLATION ${v.file}: ${v.message}`);
  for (const n of result.notes) lines.push(`NOTE      ${n.file}: ${n.message}`);
  for (const n of result.notRun) lines.push(`NOT_RUN   ${n.file}: ${n.message}`);
  return lines;
}

export function discover(root) {
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
        if (lower.endsWith('.csproj') || CPM_CHAIN_FILES.has(entry.name) || entry.name === 'package.json') {
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

// Elements with one tag name (case-insensitive) in comment-free XML, in document
// order, as { attrs, body }. A start tag ends at the first ">" outside a quoted
// value and never runs into another tag, because "<" cannot occur in a legal
// attribute value. body is the content of a paired element, or null when the
// element is self-closing or unclosed. Only the static XML is read: MSBuild
// evaluation (properties, conditions, imports, item lists) is not performed.
function elements(xml, name) {
  const starts = [...xml.matchAll(new RegExp(`<${name}(?=[\\s/>])((?:[^<>"']|"[^<"]*"|'[^<']*')*?)(/?)>`, 'gi'))];
  const close = new RegExp(`</${name}\\s*>`, 'gi');
  return starts.map((m, i) => {
    let body = null;
    if (!m[2]) {
      const from = m.index + m[0].length;
      close.lastIndex = from;
      const end = close.exec(xml);
      if (end && (i + 1 === starts.length || end.index < starts[i + 1].index)) body = xml.slice(from, end.index);
    }
    return { attrs: attributes(m[1]), body };
  });
}

// Attributes of one start tag as lower-case name -> value. Single- and
// double-quoted values are equivalent; character and predefined entity
// references are decoded and the value is trimmed (as MSBuild trims item
// specifications). Reading stops at the first token that is not name="value"
// or name='value', so malformed input yields no guessed attribute.
function attributes(text) {
  const attrs = {};
  const attribute = /\s*([A-Za-z_:][\w.:-]*)\s*=\s*(?:"([^"]*)"|'([^']*)')/y;
  for (let m = attribute.exec(text); m !== null; m = attribute.exec(text)) {
    attrs[m[1].toLowerCase()] = decodeReferences(m[2] ?? m[3]).trim();
  }
  return attrs;
}

const XML_ENTITIES = { lt: '<', gt: '>', amp: '&', quot: '"', apos: "'" };

function decodeReferences(value) {
  return value.replace(/&(?:#x([0-9A-Fa-f]+)|#([0-9]+)|(lt|gt|amp|quot|apos));/g, (reference, hex, decimal, named) => {
    if (named) return XML_ENTITIES[named];
    const code = hex ? parseInt(hex, 16) : Number(decimal);
    return code <= 0x10ffff ? String.fromCodePoint(code) : reference;
  });
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
  for (const { attrs } of elements(readXml(propsFile), 'PackageVersion')) {
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
  for (const { attrs } of elements(xml, 'PackageVersion')) {
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

// DEP-003 exception: a floating or prerelease version is accepted only when
// dependency-version-exceptions.json records the user's explicit request for
// exactly this ecosystem, package, version, and manifest. There is no global switch.
function validVersionException(e) {
  if (typeof e !== 'object' || e === null) return false;
  if (e.ecosystem !== 'npm' && e.ecosystem !== 'nuget') return false;
  if (typeof e.package !== 'string' || !e.package.trim() || /[*?]/.test(e.package)) return false;
  if (typeof e.version !== 'string' || !e.version.trim()) return false;
  if (typeof e.manifest !== 'string' || !e.manifest.trim()) return false;
  if (e.requested_by !== 'user') return false;
  return typeof e.request === 'string' && e.request.trim() !== '';
}

function loadVersionExceptions(root, result) {
  const file = join(root, 'dependency-version-exceptions.json');
  if (!existsSync(file)) return;
  try {
    const entries = JSON.parse(readFileSync(file, 'utf8')).exceptions;
    if (!Array.isArray(entries)) throw new Error('"exceptions" is not a list');
    for (const e of entries) {
      if (validVersionException(e)) result.versionExceptions.push(e);
      else result.violations.push({ file: 'dependency-version-exceptions.json', message: 'exception entry ignored: it needs ecosystem, an exact package, version, manifest, requested_by "user", and the request text (add-dependency)' });
    }
  } catch (error) {
    result.violations.push({ file: 'dependency-version-exceptions.json', message: `unreadable exception record (${error.message}); no exception applies (add-dependency)` });
  }
}

function approvedVersionException(result, ecosystem, id, version, rel) {
  const wanted = ecosystem === 'nuget' ? id.toLowerCase() : id;
  return result.versionExceptions.some((e) => e.ecosystem === ecosystem && (ecosystem === 'nuget' ? e.package.toLowerCase() : e.package) === wanted
    && e.version.trim() === String(version).trim() && e.manifest.replace(/\\/g, '/') === String(rel).replace(/\\/g, '/'));
}

function checkNuGetVersion(id, version, rel, result) {
  if (version === undefined || version.trim() === '') {
    result.violations.push({ file: rel, message: `${id}: PackageVersion has no Version` });
    return;
  }
  const v = version.trim();
  if (approvedVersionException(result, 'nuget', id, v, rel)) {
    result.notes.push({ file: rel, message: `${id}: version "${v}" - approved exception recorded in dependency-version-exceptions.json` });
  } else if (v.includes('*') || /^[[(]/.test(v) || v.includes(',')) {
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
  const packageRefs = elements(xml, 'PackageReference');
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
  for (const { attrs, body } of packageRefs) {
    const id = attrs.include ?? attrs.update ?? '(missing Include)';
    checkNuGetId(id, rel, result);
    const childVersion = body !== null && elements(body, 'Version').length > 0;
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
  for (const { attrs } of elements(xml, 'ProjectReference')) {
    if (!attrs.include) continue;
    const targetName = basename(attrs.include.replace(/\\/g, '/')).replace(/\.csproj$/i, '');
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
      if (approvedVersionException(result, 'npm', name, spec, rel)) {
        result.notes.push({ file: rel, message: `${section}.${name}: version "${spec}" - approved exception recorded in dependency-version-exceptions.json` });
      } else if (['', '*', 'x', 'X', 'latest', 'next'].includes(spec) || /(^|\.)[xX*]$/.test(spec) || /^>=?[^<]*$/.test(spec)) {
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

// Effective Central Package Management (DEP-006): MSBuild evaluates each project; the XML text is never taken as proof of the setting.
// Needs the .NET SDK (8.0.100 or later, for -getProperty) and no network: nothing is restored or built. A project is in violation,
// proven, or NOT_RUN when the proof is unavailable; NOT_RUN never counts as passed. Contexts: default, Configuration=Release and,
// for a multi-targeted project, each TargetFramework. Hooks share a time budget so a manifest edit stays responsive; the command has none.
const CPM_CHAIN_FILES = new Set(['Directory.Packages.props', 'Directory.Build.props', 'Directory.Build.targets']);
const CPM_QUERY = ['ManagePackageVersionsCentrally', 'CentralPackageVersionsFileImported', 'CentralPackageFloatingVersionsEnabled', 'TargetFrameworks'].map((name) => `-getProperty:${name}`).concat('-getItem:PackageReference', '-getItem:PackageVersion');
const CPM_TOOLING_GAP = /MSB1001|MSB4236|compatible \.NET SDK|No \.NET SDKs? (?:was|were) found/i;
const CPM_RUN_LIMIT_MS = 120000;
const cpmState = { budgetMs: 20000, started: 0, outcomes: new Map() };

function msbuildState(root, project, extra) {
  cpmState.started ||= Date.now();
  const left = cpmState.budgetMs ? cpmState.budgetMs - (Date.now() - cpmState.started) : CPM_RUN_LIMIT_MS;
  if (left <= 0) return { notRun: 'the hook time budget ran out; run the manifest check command' };
  const run = spawnSync('dotnet', ['msbuild', project, '-nologo', ...CPM_QUERY, ...extra], { cwd: root, encoding: 'utf8', timeout: Math.min(left, CPM_RUN_LIMIT_MS), maxBuffer: 1 << 24, windowsHide: true, env: { ...process.env, DOTNET_NOLOGO: '1', DOTNET_CLI_TELEMETRY_OPTOUT: '1' } });
  if (run.error) return { notRun: run.error.code === 'ENOENT' ? 'the .NET SDK (dotnet) is not available' : `dotnet msbuild did not finish (${run.error.code || run.error.message})` };
  const output = `${run.stdout || ''}\n${run.stderr || ''}`;
  if (run.status !== 0) {
    const line = output.split(/\r?\n/).find((l) => /error/i.test(l)) || output.trim().split(/\r?\n/)[0] || `exit code ${run.status}`;
    return CPM_TOOLING_GAP.test(output) ? { notRun: `the .NET SDK cannot evaluate it: ${line.trim().slice(0, 240)}` } : { failure: line.trim().slice(0, 300) };
  }
  try {
    return { state: JSON.parse(run.stdout) };
  } catch {
    return { notRun: 'dotnet msbuild printed no evaluation result' };
  }
}

// { errors, notices, notRun } for one project, evaluated once per process.
function effectiveCpm(root, project) {
  const key = `${root}\0${project}`;
  if (cpmState.outcomes.has(key)) return cpmState.outcomes.get(key);
  const errors = new Set();
  const notices = new Set();
  let notRun = null;
  const contexts = [['default', []], ['Configuration=Release', ['-p:Configuration=Release']]];
  for (let i = 0; i < contexts.length; i += 1) {
    const [label, extra] = contexts[i];
    const run = msbuildState(root, project, extra);
    if (run.notRun) {
      notRun = run.notRun;
      break;
    }
    if (run.failure) {
      errors.add(`could not be evaluated by MSBuild in context ${label}: ${run.failure}`);
      break;
    }
    const props = run.state.Properties || {};
    const items = run.state.Items || {};
    if (i === 0) {
      for (const tfm of (props.TargetFrameworks || '').split(';').map((t) => t.trim()).filter(Boolean)) contexts.push([`TargetFramework=${tfm}`, [`-p:TargetFramework=${tfm}`]]);
    }
    const value = (props.ManagePackageVersionsCentrally || '').trim().toLowerCase();
    if (value !== 'true') {
      errors.add(`effective ManagePackageVersionsCentrally is "${value || 'unset'}" in context ${label}; it must be true`);
      continue;
    }
    if ((props.CentralPackageVersionsFileImported || '').trim().toLowerCase() !== 'true') {
      errors.add(`Directory.Packages.props is not imported in context ${label}; the setting alone manages nothing`);
      continue;
    }
    const declared = new Map((items.PackageVersion || []).map((item) => [item.Identity.toLowerCase(), item.Version || '']));
    for (const ref of items.PackageReference || []) {
      if (String(ref.IsImplicitlyDefined).toLowerCase() === 'true') continue;
      if (ref.Version) errors.add(`effective PackageReference ${ref.Identity} has version ${ref.Version} in context ${label}; versions belong in Directory.Packages.props`);
      else if (!ref.VersionOverride && !declared.has(ref.Identity.toLowerCase())) errors.add(`effective PackageReference ${ref.Identity} has no PackageVersion in context ${label}`);
    }
    if ((props.CentralPackageFloatingVersionsEnabled || '').trim().toLowerCase() !== 'true') {
      for (const [id, version] of declared) {
        if (version.includes('*')) notices.add(`PackageVersion ${id} ${version} floats: restore rejects it (NU1011) unless CentralPackageFloatingVersionsEnabled is true`);
      }
    }
  }
  const outcome = { errors: [...errors], notices: [...notices], notRun };
  cpmState.outcomes.set(key, outcome);
  return outcome;
}

function cpmNotRunMessage(reason) {
  return `NOT_RUN effective Central Package Management was not proven: ${reason}. Report this check as NOT RUN, not as passed; confirm with dotnet msbuild <project> -getProperty:ManagePackageVersionsCentrally.`;
}

function isMain() {
  if (!process.argv[1]) return false;
  const self = canonical(fileURLToPath(import.meta.url));
  const invoked = canonical(process.argv[1]);
  return process.platform === 'win32' ? self.toLowerCase() === invoked.toLowerCase() : self === invoked;
}

if (isMain()) {
  let root;
  try {
    root = resolveActiveRoot(process.cwd());
  } catch (error) {
    process.stderr.write(`check-manifests: ${error.message}. Run it from the repository root.\n`);
    process.exit(2);
  }
  cpmState.budgetMs = 0;
  const result = checkManifests(root, process.argv.slice(2).map((file) => resolve(process.cwd(), file)));
  for (const line of formatResult(result)) process.stdout.write(`${line}\n`);
  process.stdout.write(`check-manifests: ${result.checked.length} manifest(s) checked, ${result.violations.length} violation(s), ${result.notes.length} note(s), ${result.notRun.length} not run\n`);
  process.exit(result.violations.length > 0 ? 1 : result.notRun.length > 0 ? 3 : 0);
}
