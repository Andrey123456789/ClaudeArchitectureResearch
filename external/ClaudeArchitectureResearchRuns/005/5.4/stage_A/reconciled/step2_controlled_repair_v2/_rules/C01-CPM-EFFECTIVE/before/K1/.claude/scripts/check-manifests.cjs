// Kind: ENF | Scope: common | Capability: — | Loading: command (manifest hooks, verify): node "<root>/.claude/scripts/check-manifests.cjs" [file ...]
// Conforms: .claude/rules/backend/dependencies.md, .claude/rules/frontend/dependencies.md, docs/architecture/decision-register.md
'use strict';

const fs = require('fs');
const path = require('path');
const lib = require('./lib.cjs');

// Static composition: one role-named facet check per capability slot (no discovery).
// "required" facets must exist; the optional frontend slot may be absent when its selection is "none".
const FACETS = [
  { slot: 'architecture', file: 'facets/architecture-style.cjs', required: true },
  { slot: 'persistence', file: 'facets/persistence-technology.cjs', required: true },
  { slot: 'backend-testing', file: 'facets/test-framework.cjs', required: true },
  { slot: 'frontend', file: 'facets/frontend-framework.cjs', required: false },
];

const OWNER_NUGET = '.claude/rules/backend/dependencies.md';
const OWNER_NPM = '.claude/rules/frontend/dependencies.md';
const OWNER_WORKFLOW = 'add-dependency workflow';
const REGISTER = 'docs/architecture/decision-register.md';
const OWNER_LAYOUT = `${REGISTER} (Project defaults)`;

// Approved-stack exceptions owned by the add-dependency workflow.
const NUGET_DENY = new Map([
  ['microsoft.extensions.http.polly', 'deprecated resilience integration package'],
  ['polly.extensions.http', 'deprecated resilience integration package'],
]);
const NUGET_EXCEPTION = new Map([
  ['polly', 'direct Polly usage is a documented exception'],
  ['polly.core', 'direct Polly usage is a documented exception'],
]);
const NPM_TOOLING = ['typescript', 'vitest', 'eslint', 'prettier', 'jest', '@playwright/test', 'karma', 'jasmine-core'];

function loadFacets() {
  const facets = {};
  for (const facet of FACETS) {
    const abs = path.join(__dirname, facet.file);
    if (!fs.existsSync(abs)) {
      if (facet.required) {
        throw new Error(`Required capability facet check missing for slot "${facet.slot}": ${lib.toPosix(path.relative(path.join(__dirname, '..', '..'), abs))}`);
      }
      continue;
    }
    facets[facet.slot] = require(abs);
  }
  return facets;
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

function loadVersionExceptions(root) {
  const rel = 'dependency-version-exceptions.json';
  if (!lib.exists(root, rel)) return { entries: [], problem: null };
  try {
    const entries = JSON.parse(lib.readText(root, rel)).exceptions;
    if (!Array.isArray(entries)) throw new Error('"exceptions" is not a list');
    const valid = entries.filter(validVersionException);
    return { entries: valid, problem: valid.length === entries.length ? null : 'exception entry ignored: it needs ecosystem, an exact package, version, manifest, requested_by "user", and the request text' };
  } catch (err) {
    return { entries: [], problem: `unreadable exception record (${err.message}); no exception applies` };
  }
}

function approvedVersionException(exceptions, ecosystem, id, version, rel) {
  const wanted = ecosystem === 'nuget' ? id.toLowerCase() : id;
  return exceptions.some((e) => e.ecosystem === ecosystem && (ecosystem === 'nuget' ? e.package.toLowerCase() : e.package) === wanted
    && e.version.trim() === String(version).trim() && e.manifest.replace(/\\/g, '/') === String(rel).replace(/\\/g, '/'));
}

function exceptionFindings(ctx) {
  return ctx.versionExceptions.problem ? [lib.finding('error', 'dependency-version-exceptions.json', ctx.versionExceptions.problem, OWNER_WORKFLOW)] : [];
}

function makeContext(root) {
  const facets = loadFacets();
  return {
    root,
    facets,
    versionExceptions: loadVersionExceptions(root),
    // The architecture frame owns placement: leaves classify projects through it.
    roleOf: name => facets.architecture.roleOf(name),
  };
}

function parseProject(root, rel, source) {
  const text = lib.stripXmlComments(source === undefined ? lib.readText(root, rel) : source);
  const dir = path.posix.dirname(rel);
  const projectTag = lib.xmlElements(text, 'Project')[0];
  const sdk = (projectTag && projectTag.attrs.Sdk) || '';
  const packages = lib.xmlElements(text, 'PackageReference').map(e => ({
    id: e.attrs.Include || e.attrs.Update || '',
    version: e.attrs.Version || e.child.Version || '',
    versionOverride: e.attrs.VersionOverride || e.child.VersionOverride || '',
  }));
  // Only an Include adds a reference edge (Update/Remove items or a missing Include reference nothing).
  const projectRefs = lib.xmlElements(text, 'ProjectReference').filter(e => e.attrs.Include).map(e => {
    const include = e.attrs.Include.replace(/\\/g, '/');
    const target = path.posix.normalize(path.posix.join(dir, include));
    return { include, target, name: path.posix.basename(target).replace(/\.(cs|fs|vb)proj$/i, '') };
  });
  const frameworkRefs = lib.xmlElements(text, 'FrameworkReference').map(e => e.attrs.Include || '');
  return { rel, name: path.posix.basename(rel).replace(/\.(cs|fs|vb)proj$/i, ''), sdk, packages, projectRefs, frameworkRefs };
}

function checkProjectFile(ctx, rel) {
  const project = parseProject(ctx.root, rel);
  const findings = [];
  for (const pkg of project.packages) {
    if (pkg.version) {
      findings.push(lib.finding('error', rel, `PackageReference "${pkg.id}" declares a version (central package management)`, OWNER_NUGET));
    }
    if (pkg.versionOverride) {
      findings.push(lib.finding('warn', rel, `PackageReference "${pkg.id}" uses VersionOverride; record the reason`, OWNER_NUGET));
    }
    const denied = NUGET_DENY.get(pkg.id.toLowerCase());
    if (denied) findings.push(lib.finding('error', rel, `"${pkg.id}": ${denied}`, OWNER_WORKFLOW));
  }
  for (const facet of Object.values(ctx.facets)) {
    if (facet.checkProject) findings.push(...facet.checkProject(ctx, project));
  }
  return findings;
}

function checkPackagesProps(ctx, rel) {
  const text = lib.stripXmlComments(lib.readText(ctx.root, rel));
  const findings = exceptionFindings(ctx);
  if (!/<ManagePackageVersionsCentrally>\s*true\s*<\/ManagePackageVersionsCentrally>/i.test(text)) {
    findings.push(lib.finding('error', rel, 'ManagePackageVersionsCentrally is not enabled', OWNER_NUGET));
  }
  const packages = lib.xmlElements(text, 'PackageVersion').map(e => ({
    id: e.attrs.Include || '',
    version: e.attrs.Version || e.child.Version || '',
  }));
  for (const pkg of packages) {
    const id = pkg.id.toLowerCase();
    if (approvedVersionException(ctx.versionExceptions.entries, 'nuget', pkg.id, pkg.version, rel)) {
      findings.push(lib.finding('warn', rel, `PackageVersion "${pkg.id}" ${pkg.version} is an approved exception recorded in dependency-version-exceptions.json`, OWNER_WORKFLOW));
    } else if (!pkg.version || /[*\[\](),]/.test(pkg.version)) {
      findings.push(lib.finding('error', rel, `PackageVersion "${pkg.id}" has a missing, floating, or range version "${pkg.version}"`, OWNER_WORKFLOW));
    } else if (pkg.version.includes('-')) {
      findings.push(lib.finding('warn', rel, `PackageVersion "${pkg.id}" ${pkg.version} is a prerelease; allowed only when explicitly requested`, OWNER_WORKFLOW));
    }
    if (NUGET_DENY.has(id)) findings.push(lib.finding('error', rel, `"${pkg.id}": ${NUGET_DENY.get(id)}`, OWNER_WORKFLOW));
    if (NUGET_EXCEPTION.has(id)) findings.push(lib.finding('warn', rel, `"${pkg.id}": ${NUGET_EXCEPTION.get(id)}`, OWNER_WORKFLOW));
  }
  for (const facet of Object.values(ctx.facets)) {
    if (facet.checkCentralPackages) findings.push(...facet.checkCentralPackages(ctx, rel, packages));
  }
  return findings;
}

function npmVersionIsFloating(spec) {
  const s = String(spec).trim().toLowerCase();
  return s === '' || s === '*' || s === 'x' || s === 'latest' || s === 'next';
}

function checkPackageJson(ctx, rel) {
  let pkg;
  try {
    pkg = JSON.parse(lib.readText(ctx.root, rel));
  } catch (err) {
    return [lib.finding('error', rel, `package.json is not valid JSON (${err.message})`, OWNER_NPM)];
  }
  const findings = exceptionFindings(ctx);
  for (const section of ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']) {
    for (const [name, spec] of Object.entries(pkg[section] || {})) {
      if (approvedVersionException(ctx.versionExceptions.entries, 'npm', name, String(spec), rel)) {
        findings.push(lib.finding('warn', rel, `${section}.${name} "${spec}" is an approved exception recorded in dependency-version-exceptions.json`, OWNER_WORKFLOW));
      } else if (npmVersionIsFloating(spec)) {
        findings.push(lib.finding('error', rel, `${section}.${name} uses a floating version "${spec}"`, OWNER_WORKFLOW));
      } else if (/\d-(alpha|beta|rc|next|canary|dev|preview)/i.test(String(spec))) {
        findings.push(lib.finding('warn', rel, `${section}.${name} "${spec}" is a prerelease; allowed only when explicitly requested`, OWNER_WORKFLOW));
      }
    }
  }
  for (const name of Object.keys(pkg.dependencies || {})) {
    if (NPM_TOOLING.includes(name) || name.startsWith('@types/')) {
      findings.push(lib.finding('warn', rel, `build/test tooling "${name}" is in runtime dependencies`, OWNER_NPM));
    }
  }
  for (const facet of Object.values(ctx.facets)) {
    if (facet.checkPackageJson) findings.push(...facet.checkPackageJson(ctx, rel, pkg));
  }
  return findings;
}

function isManifest(rel) {
  const base = path.posix.basename(rel);
  return rel.endsWith('.csproj') || base === 'Directory.Packages.props' || base === 'package.json';
}

function checkFile(root, rel, ctx = makeContext(root)) {
  if (!lib.exists(root, rel)) return [];
  const base = path.posix.basename(rel);
  try {
    if (rel.endsWith('.csproj')) return checkProjectFile(ctx, rel);
    if (base === 'Directory.Packages.props') return checkPackagesProps(ctx, rel);
    if (base === 'package.json') return checkPackageJson(ctx, rel);
  } catch (err) {
    return [lib.finding('error', rel, `manifest could not be read (${err.message})`, base === 'package.json' ? OWNER_NPM : OWNER_NUGET)];
  }
  return [];
}

function checkAll(root) {
  const ctx = makeContext(root);
  const findings = [];
  for (const rel of lib.walk(root, '', isManifest)) findings.push(...checkFile(root, rel, ctx));
  if (lib.exists(root, 'tests')) {
    findings.push(lib.finding('warn', 'tests/', 'top-level tests directory; backend tests live beside production projects', OWNER_LAYOUT));
  }
  for (const rel of lib.walk(root, 'frontend', r => path.posix.basename(r) === 'package.json')) {
    const lock = path.posix.join(path.posix.dirname(rel), 'package-lock.json');
    if (!lib.exists(root, lock)) findings.push(lib.finding('warn', rel, 'no package-lock.json next to package.json', OWNER_NPM));
  }
  return findings;
}

// ---------- recorded approvals for Reserved project-reference changes ----------

/** A real calendar date in the register's ISO form YYYY-MM-DD; placeholders such as TBD or pending are not dates. */
function isIsoDate(value) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  if (!m) return false;
  const [year, month, day] = m.slice(1).map(Number);
  const leap = (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
  const days = [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1] || 0;
  return day >= 1 && day <= days;
}

/** Text of accepted decisions: register rows with a valid Date, plus the docs/decisions/ records they link. */
function acceptedDecisionText(root) {
  if (!lib.exists(root, REGISTER)) return '';
  const text = lib.readText(root, REGISTER);
  const start = text.indexOf('## Accepted decisions');
  if (start < 0) return '';
  const rows = [];
  for (const line of text.slice(start).split(/\r?\n/).slice(1)) {
    if (/^#{1,6}\s/.test(line)) break;
    if (!/^\s*\|/.test(line) || /^\s*\|\s*:?-/.test(line)) continue;
    const cells = line.trim().replace(/^\||\|$/g, '').split('|').map(c => c.trim());
    if (!isIsoDate(cells[0])) continue; // undated, placeholder, or invalid Date: not an accepted decision
    let row = cells.join(' ');
    for (const m of row.matchAll(/docs\/decisions\/[\w.-]+\.md/g)) {
      if (lib.exists(root, m[0])) row += `\n${lib.readText(root, m[0])}`;
    }
    rows.push(row);
  }
  return rows.join('\n').replace(/→/g, '->').replace(/[ \t]+/g, ' ');
}

const escapeRegex = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

/** An edge is approved when an accepted decision lists it as `From -> To`. */
function isApprovedEdge(approvals, from, to) {
  return new RegExp(`(?<![\\w.])${escapeRegex(from)}\\s*->\\s*${escapeRegex(to)}(?![\\w.])`, 'i').test(approvals);
}

/** A project addition or removal is approved when an accepted decision names the project. */
function isApprovedProject(approvals, name) {
  return new RegExp(`(?<![\\w.])${escapeRegex(name)}(?![\\w.])`, 'i').test(approvals);
}

module.exports = { checkFile, checkAll, isManifest, makeContext, parseProject, acceptedDecisionText, isApprovedEdge, isApprovedProject, loadVersionExceptions };

if (require.main === module) {
  const root = lib.commandRoot(__dirname);
  const args = process.argv.slice(2);
  let findings;
  if (args.length === 0) {
    findings = checkAll(root);
  } else {
    const ctx = makeContext(root);
    findings = [];
    for (const arg of args) {
      const rel = lib.relInside(root, path.resolve(process.cwd(), arg));
      if (!rel) throw new Error(`Path is outside the project ${root}: ${arg}`);
      findings.push(...checkFile(root, rel, ctx));
    }
  }
  if (findings.length) process.stdout.write(`${lib.formatFindings(findings)}\n`);
  const errors = findings.filter(f => f.severity === 'error').length;
  process.stdout.write(`check-manifests (${root}): ${errors} error(s), ${findings.length - errors} warning(s)\n`);
  process.exitCode = errors ? 1 : 0;
}
