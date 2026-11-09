// Level 3 Project · enforcement asset: deterministic manifest checks used by claude-hook.mjs.
// Checks central package management, versions, the package deny/review lists, npm dependency
// categories, and production project-reference direction. Messages point to the owning rule or
// workflow; they do not restate policy.
import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import path from 'node:path';

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

// <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally> outside comments (element name and
// value in any case, no attributes).
function centralManagementEnabled(tokens) {
  const isSwitch = name => name?.toLowerCase() === 'managepackageversionscentrally';
  return tokens.some((token, index) => isSwitch(token.start) && !token.selfClosing && !token.malformed
    && Object.keys(token.attrs).length === 0
    && tokens[index + 1]?.text?.trim().toLowerCase() === 'true'
    && isSwitch(tokens[index + 2]?.end));
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
  if (!centralManagementEnabled(tokens)) {
    problems.push(`${location}: ManagePackageVersionsCentrally must be true → ${OWNER.packageManagement}`);
  }
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

export function checkManifestFile(root, file) {
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
  return files.flatMap(file => checkManifestFile(root, file));
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
