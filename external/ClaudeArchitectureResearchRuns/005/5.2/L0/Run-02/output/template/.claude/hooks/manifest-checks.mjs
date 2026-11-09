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

const SKIP_DIRS = new Set(['node_modules', 'bin', 'obj', '.git', 'dist', '.angular', '.vs', 'TestResults']);

export function isManifest(filePath) {
  const base = path.basename(filePath);
  return base.endsWith('.csproj')
    || base === 'Directory.Packages.props'
    || base === 'Directory.Build.props'
    || base === 'package.json'
    || base === '.npmrc';
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
    const content = readFileSync(abs, 'utf8');
    const index = content.search(/^## Accepted /m);
    if (index >= 0) text += content.slice(index).toLowerCase();
  }
  return text;
}

function projectLayer(projectFile) {
  const name = path.basename(projectFile).replace(/\.csproj$/i, '');
  if (/tests?$/i.test(name)) return 'Tests';
  const last = name.split('.').pop();
  return LAYERS.find(layer => layer.toLowerCase() === last.toLowerCase()) ?? null;
}

function attributes(tag) {
  const result = {};
  for (const match of tag.matchAll(/([A-Za-z]+)\s*=\s*"([^"]*)"/g)) result[match[1]] = match[2];
  return result;
}

function checkPackageId(id, location, problems, accepted) {
  const key = id.toLowerCase();
  if (DENY_NUGET.has(key)) problems.push(`${location}: package '${id}' — ${DENY_NUGET.get(key)}`);
  else if (REVIEW_NUGET.has(key) && !accepted.includes(key)) {
    problems.push(`${location}: package '${id}' needs a recorded decision or reported reason — ${REVIEW_NUGET.get(key)}`);
  }
}

function checkVersion(version, location, problems) {
  if (!version || !version.trim()) problems.push(`${location}: empty version → ${OWNER.addDependency} (Select the version)`);
  else if (version.includes('*')) problems.push(`${location}: floating version '${version}' → ${OWNER.addDependency} (Select the version)`);
  else if (/-(alpha|beta|preview|rc|dev|nightly|pre)/i.test(version)) {
    problems.push(`${location}: prerelease version '${version}' is allowed only when explicitly requested → ${OWNER.addDependency} (Select the version)`);
  }
}

function checkProjectFile(root, file, problems, accepted) {
  const content = readFileSync(file, 'utf8');
  const location = rel(root, file);
  for (const match of content.matchAll(/<PackageReference\b([^>]*?)(\/>|>([\s\S]*?)<\/PackageReference>)/g)) {
    const attrs = attributes(match[1]);
    const id = attrs.Include ?? attrs.Update ?? '(unknown)';
    if (attrs.Version !== undefined || /<Version>/.test(match[3] ?? '')) {
      problems.push(`${location}: PackageReference '${id}' declares a version; versions belong in Directory.Packages.props → ${OWNER.packageManagement}`);
    }
    if (attrs.VersionOverride !== undefined) {
      problems.push(`${location}: PackageReference '${id}' uses VersionOverride — report the concrete reason → ${OWNER.packageManagement}`);
    }
    checkPackageId(id, location, problems, accepted);
  }

  const layer = projectLayer(file);
  if (!layer || layer === 'Tests') return;
  for (const match of content.matchAll(/<ProjectReference\b[^>]*Include\s*=\s*"([^"]+)"/g)) {
    const target = match[1].replace(/\\/g, '/');
    const targetLayer = projectLayer(target);
    if (targetLayer === 'Tests') {
      problems.push(`${location}: production project references test project '${target}' → ${OWNER.layers}`);
    } else if (targetLayer && !ALLOWED_REFERENCES[layer].includes(targetLayer)) {
      problems.push(`${location}: outward reference ${layer} → ${targetLayer} ('${target}') violates the dependency direction → ${OWNER.layers}`);
    }
  }
}

function checkCentralPackages(root, file, problems, accepted) {
  const content = readFileSync(file, 'utf8');
  const location = rel(root, file);
  if (!/<ManagePackageVersionsCentrally>\s*true\s*<\/ManagePackageVersionsCentrally>/i.test(content)) {
    problems.push(`${location}: ManagePackageVersionsCentrally must be true → ${OWNER.packageManagement}`);
  }
  for (const match of content.matchAll(/<PackageVersion\b([^>]*?)\/?>/g)) {
    const attrs = attributes(match[1]);
    const id = attrs.Include ?? attrs.Update ?? '(unknown)';
    checkVersion(attrs.Version, `${location} [${id}]`, problems);
    checkPackageId(id, location, problems, accepted);
  }
}

function checkPackageJson(root, file, problems, accepted) {
  const location = rel(root, file);
  let manifest;
  try {
    manifest = JSON.parse(readFileSync(file, 'utf8'));
  } catch (error) {
    problems.push(`${location}: not valid JSON (${error.message})`);
    return;
  }
  for (const section of ['dependencies', 'devDependencies']) {
    for (const [name, version] of Object.entries(manifest[section] ?? {})) {
      if (typeof version === 'string' && /^(\*|latest|x|)$/i.test(version.trim())) {
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

function checkNpmrc(root, file, problems) {
  const content = readFileSync(file, 'utf8');
  if (/^\s*(legacy-peer-deps|force)\s*=\s*true\s*$/im.test(content)) {
    problems.push(`${rel(root, file)}: peer-dependency bypass configured → ${OWNER.addDependency} (Install)`);
  }
}

export function checkManifestFile(root, file) {
  const problems = [];
  if (!existsSync(file)) return problems;
  const accepted = acceptedDecisionsText(root);
  const base = path.basename(file);
  if (base.endsWith('.csproj') || base === 'Directory.Build.props') checkProjectFile(root, file, problems, accepted);
  else if (base === 'Directory.Packages.props') checkCentralPackages(root, file, problems, accepted);
  else if (base === 'package.json') checkPackageJson(root, file, problems, accepted);
  else if (base === '.npmrc') checkNpmrc(root, file, problems);
  return problems;
}

export function findManifests(root) {
  const found = [];
  const walk = dir => {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      if (entry.isDirectory()) {
        if (!SKIP_DIRS.has(entry.name)) walk(path.join(dir, entry.name));
      } else if (isManifest(entry.name)) {
        found.push(path.join(dir, entry.name));
      }
    }
  };
  walk(root);
  return found;
}

export function scanManifests(root) {
  return findManifests(root).flatMap(file => checkManifestFile(root, file));
}

// Package identifiers declared by a manifest's content (used to detect added or changed dependencies).
export function declaredPackages(fileName, content) {
  const packages = new Map();
  if (!content) return packages;
  const base = path.basename(fileName);
  if (base === 'package.json') {
    try {
      const manifest = JSON.parse(content);
      for (const section of ['dependencies', 'devDependencies', 'peerDependencies']) {
        for (const [name, version] of Object.entries(manifest[section] ?? {})) packages.set(name, String(version));
      }
    } catch {
      // Invalid JSON is reported by checkPackageJson.
    }
    return packages;
  }
  for (const match of content.matchAll(/<(PackageReference|PackageVersion)\b([^>]*?)\/?>/g)) {
    const attrs = attributes(match[2]);
    const id = attrs.Include ?? attrs.Update;
    if (id) packages.set(id, attrs.Version ?? attrs.VersionOverride ?? '');
  }
  return packages;
}

export function isFile(file) {
  try {
    return statSync(file).isFile();
  } catch {
    return false;
  }
}
