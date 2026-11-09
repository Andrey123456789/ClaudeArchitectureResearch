// Level 3 Project · enforcement asset: deterministic manifest checks used by claude-hook.mjs.
// Checks central package management, versions, the package deny/review lists, npm dependency
// categories, and production project-reference direction. Messages point to the owning rule or
// workflow; they do not restate policy.
// Whole-repository command: node "$(git rev-parse --show-toplevel)/.claude/hooks/manifest-checks.mjs"
// Exit codes: 0 = no problems, 1 = problems, 3 = no problems, but the proof of effective Central Package
// Management did not run (report it as NOT RUN, never as passed).
import { spawnSync } from 'node:child_process';
import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const OWNER = {
  packageManagement: '.claude/rules/3-project/package-management.md',
  addDependency: '.claude/skills/add-dependency/SKILL.md',
  decisions: '.claude/rules/3-project/decisions.md',
  overview: '.claude/rules/1-architecture/overview.md',
  layers: '.claude/rules/1-architecture/backend-layers.md',
  fluentValidation: '.claude/rules/2-technology/fluentvalidation.md',
  logging: '.claude/skills/logging/references/serilog.md',
};

// Packages that must not be added (deprecated or replaced by the approved integration).
const DENY_NUGET = new Map([
  ['microsoft.extensions.http.polly', `deprecated resilience integration → ${OWNER.addDependency} (Conditional package bindings)`],
  ['polly.extensions.http', `deprecated resilience integration → ${OWNER.addDependency} (Conditional package bindings)`],
  ['serilog.sinks.elasticsearch', `deprecated package → ${OWNER.logging}`],
]);

// Packages that need an approved decision or a reported reason before they are added.
const REVIEW_NUGET = new Map([
  ['polly', `direct Polly is an explicit exception → ${OWNER.addDependency} (Conditional package bindings)`],
  ['mediatr', `mediator-based organization is not adopted (Reserved) → ${OWNER.overview}`],
  ['kommand', `mediator-based organization is not adopted (Reserved) → ${OWNER.overview}`],
  ['automapper', `another mapping framework requires approval → ${OWNER.decisions}`],
  ['fluentvalidation.aspnetcore', `legacy automatic-validation integration → ${OWNER.fluentValidation}`],
]);

const REVIEW_NPM = new Map([
  ['@ngrx/store', `not added by default → ${OWNER.decisions} (Not added by default)`],
  ['axios', `not added by default → ${OWNER.decisions} (Not added by default)`],
  ['lodash', `not added by default → ${OWNER.decisions} (Not added by default)`],
  ['bootstrap', `not added by default → ${OWNER.decisions} (Not added by default)`],
  ['tailwindcss', `not added by default → ${OWNER.decisions} (Not added by default)`],
]);

const NPM_TOOLING = [
  /^@angular\/cli$/, /^@angular\/build$/, /^@angular-devkit\//, /^@angular\/compiler-cli$/,
  /^typescript$/, /^vitest$/, /^@vitest\//, /^@playwright\/test$/, /^eslint$/, /^prettier$/,
  /^karma/, /^jasmine/, /^@types\//,
];

const LAYERS = ['Domain', 'Application', 'Infrastructure', 'Api'];
const ALLOWED_REFERENCES = {
  Domain: [],
  Application: ['Domain'],
  Infrastructure: ['Application', 'Domain'],
  Api: ['Application', 'Infrastructure', 'Domain'],
};

// Generated, restored, or local directories that never hold maintained manifests.
export const SKIP_DIRS = new Set(['node_modules', 'bin', 'obj', '.git', 'dist', '.angular', '.vs', 'TestResults']);

export function isManifest(filePath) {
  const base = path.basename(filePath);
  return base.endsWith('.csproj')
    || base === 'Directory.Packages.props'
    || base === 'Directory.Build.props'
    || base === 'Directory.Build.targets'
    || base === 'package.json'
    || base === '.npmrc';
}

// True when a repository-relative path lies inside a skipped directory.
export function inSkippedDir(relative) {
  return relative.split('/').slice(0, -1).some(part => SKIP_DIRS.has(part));
}

// Decodes manifest text the way Windows tooling may have written it: UTF-8 (with or without a
// byte-order mark) or BOM-tagged UTF-16LE/UTF-16BE (Windows PowerShell 5.1 redirection and Out-File).
// Malformed UTF-16 content throws a TextEncodingError instead of producing garbage.
export class TextEncodingError extends Error {}

export function decodeText(bytes) {
  const buffer = Buffer.isBuffer(bytes) ? bytes : Buffer.from(bytes ?? '');
  if (buffer.length >= 3 && buffer[0] === 0xef && buffer[1] === 0xbb && buffer[2] === 0xbf) {
    return buffer.subarray(3).toString('utf8');
  }
  const utf16 = buffer.length >= 2 && ((buffer[0] === 0xff && buffer[1] === 0xfe) || (buffer[0] === 0xfe && buffer[1] === 0xff));
  if (utf16) {
    const body = buffer.subarray(2);
    if (body.length % 2 !== 0) throw new TextEncodingError('UTF-16 content with an odd number of bytes');
    if (buffer[0] === 0xff) return body.toString('utf16le');
    const swapped = Buffer.from(body);
    swapped.swap16();
    return swapped.toString('utf16le');
  }
  return buffer.toString('utf8');
}

export function readText(file) {
  return decodeText(readFileSync(file));
}

function rel(root, file) {
  return path.relative(root, file).split(path.sep).join('/');
}

function acceptedDecisionsText(root) {
  // Approved exceptions are recorded in the two decision summaries (architecture-decision workflow).
  let text = '';
  for (const file of [OWNER.decisions, OWNER.overview]) {
    const abs = path.join(root, file);
    if (!existsSync(abs)) continue;
    let content;
    try {
      content = readText(abs);
    } catch {
      continue; // An unreadable summary records no exception; the package stays flagged.
    }
    const index = content.search(/^## Accepted /m);
    if (index >= 0) text += content.slice(index).toLowerCase();
  }
  return text;
}

function projectLayer(projectFile) {
  const name = path.basename(projectFile.replace(/\\/g, '/')).replace(/\.csproj$/i, '');
  if (/tests?$/i.test(name)) return 'Tests';
  const last = name.split('.').pop();
  return LAYERS.find(layer => layer.toLowerCase() === last.toLowerCase()) ?? null;
}

// One bounded, quote-aware reader for the MSBuild XML that the checks and declaredDependencies() share, so
// equivalent XML spellings give the same result: attribute values in double or single quotes, attributes in
// any order, whitespace and line breaks around '=' and between attributes, character and entity references,
// and '>' inside a quoted value. Comments, processing instructions, and declarations are inert; CDATA is
// text. It is not an XML parser or an MSBuild evaluator: properties, conditions, wildcards, imports, and
// ';'-separated item lists are not expanded.
const XML_NAME = '[A-Za-z_][\\w.:-]*';
const START_TAG = new RegExp(`<(${XML_NAME})`, 'y');
const END_TAG = new RegExp(`</(${XML_NAME})\\s*>`, 'y');
const ATTRIBUTE = new RegExp(`\\s+(${XML_NAME})\\s*=\\s*(?:"([^"<]*)"|'([^'<]*)')`, 'y');
const TAG_CLOSE = /\s*(\/?)>/y;
const SKIPPED = [['<!--', '-->'], ['<![CDATA[', ']]>', true], ['<?', '?>'], ['<!', '>']];
const ENTITIES = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'" };

function unescapeXml(text) {
  return text.replace(/&(?:#x([\da-fA-F]+)|#(\d+)|(amp|lt|gt|quot|apos));/g, (reference, hex, decimal, name) => {
    if (name) return ENTITIES[name];
    const code = hex !== undefined ? Number.parseInt(hex, 16) : Number(decimal);
    return code > 0 && code <= 0x10ffff ? String.fromCodePoint(code) : reference;
  });
}

// Tokens in document order: { text }, { end: name }, or { start: name, attrs, selfClosing, malformed, line }.
// A start tag that cannot be read (unquoted value, missing whitespace, unterminated quote, duplicate
// attribute) is marked malformed and opens no element, so it never swallows the elements after it.
function xmlTokens(content) {
  const tokens = [];
  let index = 0;
  while (index < content.length) {
    const open = content.indexOf('<', index);
    const stop = open < 0 ? content.length : open;
    if (stop > index) tokens.push({ text: unescapeXml(content.slice(index, stop)) });
    if (open < 0) break;
    index = open;
    const skipped = SKIPPED.find(([prefix]) => content.startsWith(prefix, index));
    if (skipped) {
      const [prefix, suffix, isText] = skipped;
      const close = content.indexOf(suffix, index + prefix.length);
      const end = close < 0 ? content.length : close;
      if (isText) tokens.push({ text: content.slice(index + prefix.length, end) });
      index = close < 0 ? content.length : end + suffix.length;
      continue;
    }
    END_TAG.lastIndex = index;
    const end = END_TAG.exec(content);
    if (end) {
      tokens.push({ end: end[1] });
      index = END_TAG.lastIndex;
      continue;
    }
    START_TAG.lastIndex = index;
    const start = START_TAG.exec(content);
    if (!start) {
      tokens.push({ text: '<' });
      index += 1;
      continue;
    }
    const token = { start: start[1], attrs: Object.create(null), selfClosing: true, malformed: false, line: 0 };
    let position = START_TAG.lastIndex;
    for (;;) {
      ATTRIBUTE.lastIndex = position;
      const attribute = ATTRIBUTE.exec(content);
      if (!attribute) break;
      if (attribute[1] in token.attrs) token.malformed = true;
      token.attrs[attribute[1]] = unescapeXml(attribute[2] ?? attribute[3]);
      position = ATTRIBUTE.lastIndex;
    }
    TAG_CLOSE.lastIndex = position;
    const close = TAG_CLOSE.exec(content);
    if (close) {
      token.selfClosing = close[1] === '/';
      position = TAG_CLOSE.lastIndex;
    } else {
      token.malformed = true;
    }
    if (token.malformed) token.line = content.slice(0, index).split('\n').length;
    tokens.push(token);
    index = position;
  }
  return tokens;
}

// Items of the given types in document order. Item metadata may be an attribute or a direct child element
// (`Version="1.0"` equals `<Version>1.0</Version>`); Include and Update are attributes.
function msbuildItems(tokens, types) {
  const items = [];
  tokens.forEach((token, index) => {
    if (!types.includes(token.start)) return;
    const children = Object.create(null);
    for (let i = index + 1, depth = 0, child = null; !token.selfClosing && i < tokens.length; i += 1) {
      const next = tokens[i];
      if (next.end !== undefined) {
        if (depth === 0) break;
        depth -= 1;
        if (depth === 0) child = null;
      } else if (next.start !== undefined) {
        if (depth === 0) children[next.start] = '';
        if (!next.selfClosing) {
          if (depth === 0) child = next.start;
          depth += 1;
        }
      } else if (depth === 1 && child !== null) {
        children[child] += next.text;
      }
    }
    items.push({ type: token.start, attrs: token.attrs, children, malformed: token.malformed, line: token.line });
  });
  return items;
}

function metadata(item, name) {
  return item.attrs[name] ?? item.children[name];
}

function itemId(item) {
  return (item.attrs.Include ?? item.attrs.Update)?.trim();
}

function reportMalformed(items, location, problems) {
  for (const item of items.filter(entry => entry.malformed)) {
    problems.push(`${location}: <${item.type}> at line ${item.line} is not well-formed XML (each attribute once, its value in " or ' quotes, attributes separated by whitespace); fix it so the declaration can be checked`);
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

function checkPackageId(id, location, problems, accepted) {
  const key = id.toLowerCase();
  if (DENY_NUGET.has(key)) problems.push(`${location}: package '${id}' — ${DENY_NUGET.get(key)}`);
  else if (REVIEW_NUGET.has(key) && !accepted.includes(key)) {
    problems.push(`${location}: package '${id}' needs a recorded decision or reported reason — ${REVIEW_NUGET.get(key)}`);
  }
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

function loadVersionExceptions(root, problems) {
  const file = path.join(root, 'dependency-version-exceptions.json');
  if (!existsSync(file)) return [];
  const label = 'dependency-version-exceptions.json';
  try {
    const entries = JSON.parse(readText(file)).exceptions;
    if (!Array.isArray(entries)) throw new Error('"exceptions" is not a list');
    const valid = entries.filter(validVersionException);
    if (valid.length !== entries.length) problems.push(`${label}: exception entry ignored: it needs ecosystem, an exact package, version, manifest, requested_by "user", and the request text → ${OWNER.addDependency}`);
    return valid;
  } catch (error) {
    problems.push(`${label}: unreadable exception record (${error.message}); no exception applies → ${OWNER.addDependency}`);
    return [];
  }
}

function approvedVersionException(exceptions, ecosystem, id, version, rel) {
  const wanted = ecosystem === 'nuget' ? id.toLowerCase() : id;
  return exceptions.some((e) => e.ecosystem === ecosystem && (ecosystem === 'nuget' ? e.package.toLowerCase() : e.package) === wanted
    && e.version.trim() === String(version).trim() && e.manifest.replace(/\\/g, '/') === String(rel).replace(/\\/g, '/'));
}

function checkVersion(version, location, problems) {
  if (!version || !version.trim()) problems.push(`${location}: empty version → ${OWNER.addDependency} (Select the version)`);
  else if (version.includes('*')) problems.push(`${location}: floating version '${version}' → ${OWNER.addDependency} (Select the version)`);
  else if (/-(alpha|beta|preview|rc|dev|nightly|pre)/i.test(version)) {
    problems.push(`${location}: prerelease version '${version}' is allowed only when explicitly requested → ${OWNER.addDependency} (Select the version)`);
  }
}

function checkProjectFile(content, file, location, problems, accepted) {
  const items = msbuildItems(xmlTokens(content), ['PackageReference', 'ProjectReference']);
  reportMalformed(items, location, problems);
  for (const item of items.filter(entry => entry.type === 'PackageReference')) {
    const id = itemId(item) ?? '(unknown)';
    if (metadata(item, 'Version') !== undefined) {
      problems.push(`${location}: PackageReference '${id}' declares a version; versions belong in Directory.Packages.props → ${OWNER.packageManagement}`);
    }
    if (metadata(item, 'VersionOverride') !== undefined) {
      problems.push(`${location}: PackageReference '${id}' uses VersionOverride — report the concrete reason → ${OWNER.packageManagement}`);
    }
    checkPackageId(id, location, problems, accepted);
  }

  const layer = projectLayer(file);
  if (!layer || layer === 'Tests') return;
  for (const target of projectReferences(items)) {
    const targetLayer = projectLayer(target);
    if (targetLayer === 'Tests') {
      problems.push(`${location}: production project references test project '${target}' → ${OWNER.layers}`);
    } else if (targetLayer && !ALLOWED_REFERENCES[layer].includes(targetLayer)) {
      problems.push(`${location}: outward reference ${layer} → ${targetLayer} ('${target}') violates the dependency direction → ${OWNER.layers}`);
    }
  }
}

function checkCentralPackages(content, location, problems, accepted, exceptions) {
  const tokens = xmlTokens(content);
  const items = msbuildItems(tokens, ['PackageVersion']);
  reportMalformed(items, location, problems);
  for (const item of items) {
    const id = itemId(item) ?? '(unknown)';
    const version = metadata(item, 'Version');
    if (!approvedVersionException(exceptions, 'nuget', id, version ?? '', location)) checkVersion(version, `${location} [${id}]`, problems);
    checkPackageId(id, location, problems, accepted);
  }
}

function checkPackageJson(content, location, problems, accepted, exceptions) {
  let manifest;
  try {
    manifest = JSON.parse(content);
  } catch (error) {
    problems.push(`${location}: not valid JSON (${error.message})`);
    return;
  }
  for (const section of ['dependencies', 'devDependencies']) {
    for (const [name, version] of Object.entries(manifest?.[section] ?? {})) {
      if (typeof version === 'string' && /^(\*|latest|x|)$/i.test(version.trim()) && !approvedVersionException(exceptions, 'npm', name, version, location)) {
        problems.push(`${location}: floating version '${version}' for '${name}' → ${OWNER.addDependency} (Select the version)`);
      }
      const key = name.toLowerCase();
      if (REVIEW_NPM.has(key) && !accepted.includes(key)) {
        problems.push(`${location}: '${name}' needs a recorded decision or concrete need — ${REVIEW_NPM.get(key)}`);
      }
      if (section === 'dependencies' && NPM_TOOLING.some(pattern => pattern.test(name))) {
        problems.push(`${location}: build/test tooling '${name}' is in dependencies → ${OWNER.packageManagement} (npm)`);
      }
    }
  }
}

function checkNpmrc(content, location, problems) {
  if (/^\s*(legacy-peer-deps|force)\s*=\s*true\s*$/im.test(content)) {
    problems.push(`${location}: peer-dependency bypass configured → ${OWNER.addDependency} (Install)`);
  }
}

// The projects whose effective state this file can change: a project itself, or every project below a chain file.
function cpmProjects(root, location) {
  const base = path.posix.basename(location);
  if (base.endsWith('.csproj')) return [location];
  if (!CPM_CHAIN_FILES.has(base)) return [];
  const dir = path.posix.dirname(location);
  return findManifests(root).map(file => rel(root, file)).filter(project => project.endsWith('.csproj') && (dir === '.' || project.startsWith(`${dir}/`)));
}

function checkEffectiveCpm(root, location, problems, reported) {
  for (const project of cpmProjects(root, location)) {
    if (reported.has(project)) continue;
    reported.add(project);
    const outcome = effectiveCpm(root, project);
    for (const message of outcome.errors) problems.push(`${project}: ${message} → ${OWNER.packageManagement}`);
    for (const message of outcome.notices) problems.push(`${project}: ${message} → ${OWNER.addDependency}`);
    if (outcome.notRun) problems.push(`${project}: ${cpmNotRunMessage(outcome.notRun)}`);
  }
}

export function checkManifestFile(root, file, reported = new Set()) {
  const problems = [];
  if (!existsSync(file)) return problems;
  const location = rel(root, file);
  let content;
  try {
    content = readText(file);
  } catch (error) {
    problems.push(`${location}: cannot be read as UTF-8 or BOM-tagged UTF-16 text (${error.message}); re-save it as UTF-8 so it can be checked`);
    return problems;
  }
  const accepted = acceptedDecisionsText(root);
  const base = path.basename(file);
  if (base.endsWith('.csproj') || base === 'Directory.Build.props') checkProjectFile(content, file, location, problems, accepted);
  else if (base === 'Directory.Packages.props') checkCentralPackages(content, location, problems, accepted, loadVersionExceptions(root, problems));
  else if (base === 'package.json') checkPackageJson(content, location, problems, accepted, loadVersionExceptions(root, problems));
  else if (base === '.npmrc') checkNpmrc(content, location, problems);
  checkEffectiveCpm(root, location, problems, reported);
  return problems;
}

// Fallback discovery outside Git: walks the tree, skipping generated directories and nested
// repositories or worktrees (directories that contain their own .git entry).
export function findManifests(root) {
  const found = [];
  const walk = (dir, top) => {
    let entries;
    try {
      entries = readdirSync(dir, { withFileTypes: true });
    } catch {
      return;
    }
    if (!top && entries.some(entry => entry.name === '.git')) return;
    for (const entry of entries) {
      if (entry.isDirectory()) {
        if (!SKIP_DIRS.has(entry.name)) walk(path.join(dir, entry.name), false);
      } else if (isManifest(entry.name)) {
        found.push(path.join(dir, entry.name));
      }
    }
  };
  walk(root, true);
  return found;
}

export function scanManifests(root, files = findManifests(root)) {
  const reported = new Set();
  return files.flatMap(file => checkManifestFile(root, file, reported));
}

function projectReferences(items) {
  return items
    .filter(item => item.type === 'ProjectReference')
    .map(item => item.attrs.Include?.trim())
    .filter(Boolean)
    .map(target => target.replace(/\\/g, '/'));
}

// Package identifiers (with versions) and project references declared by a manifest's content,
// used to detect added, changed, or removed dependencies and project-reference graph changes.
export function declaredDependencies(fileName, content) {
  const packages = new Map();
  const references = new Set();
  if (!content) return { packages, references };
  const base = path.basename(fileName);
  if (base === 'package.json') {
    try {
      const manifest = JSON.parse(content);
      for (const section of ['dependencies', 'devDependencies', 'peerDependencies']) {
        for (const [name, version] of Object.entries(manifest?.[section] ?? {})) packages.set(name, String(version));
      }
    } catch {
      // Invalid JSON is reported by checkPackageJson.
    }
    return { packages, references };
  }
  // The same reader as the checks, so a quote-only rewrite is dependency-neutral.
  const items = msbuildItems(xmlTokens(content), ['PackageReference', 'PackageVersion', 'ProjectReference']);
  for (const item of items.filter(entry => entry.type !== 'ProjectReference')) {
    const id = itemId(item);
    if (id) packages.set(id, (metadata(item, 'Version') ?? metadata(item, 'VersionOverride') ?? '').trim());
  }
  if (base.endsWith('.csproj')) for (const target of projectReferences(items)) references.add(target);
  return { packages, references };
}

// Human-readable differences between two declaredDependencies() results.
export function dependencyDelta(before, after) {
  const packages = [];
  for (const [id, version] of after.packages) {
    if (!before.packages.has(id)) packages.push(`added ${id}`);
    else if (before.packages.get(id) !== version) packages.push(`changed ${id}`);
  }
  for (const id of before.packages.keys()) if (!after.packages.has(id)) packages.push(`removed ${id}`);
  const key = target => target.toLowerCase();
  const beforeRefs = new Map([...before.references].map(target => [key(target), target]));
  const afterRefs = new Map([...after.references].map(target => [key(target), target]));
  const references = [];
  for (const [k, target] of afterRefs) if (!beforeRefs.has(k)) references.push(`added ${target}`);
  for (const [k, target] of beforeRefs) if (!afterRefs.has(k)) references.push(`removed ${target}`);
  return { packages, references };
}

export function isFile(file) {
  try {
    return statSync(file).isFile();
  } catch {
    return false;
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  cpmState.budgetMs = 0;
  const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
  const problems = scanManifests(root);
  const notRun = problems.filter(problem => problem.includes(': NOT_RUN ')).length;
  const notices = problems.filter(problem => problem.includes('floats: restore rejects it')).length;
  for (const problem of problems) console.log(problem);
  console.log(`manifest-checks: ${problems.length - notRun - notices} problem(s), ${notices} notice(s), ${notRun} not run`);
  process.exit(problems.length - notRun - notices > 0 ? 1 : notRun > 0 ? 3 : 0);
}
