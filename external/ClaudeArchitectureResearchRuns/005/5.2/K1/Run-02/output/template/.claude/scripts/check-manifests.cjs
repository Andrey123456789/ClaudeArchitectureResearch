// Kind: ENF | Scope: common | Capability: — | Loading: command (manifest hook, verify): node .claude/scripts/check-manifests.cjs [file ...]
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
const OWNER_LAYOUT = 'docs/architecture/decision-register.md (Project defaults)';

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

function makeContext(root) {
  const facets = loadFacets();
  return {
    root,
    facets,
    // The architecture frame owns placement: leaves classify projects through it.
    roleOf: name => facets.architecture.roleOf(name),
  };
}

function parseProject(root, rel) {
  const text = lib.stripXmlComments(lib.readText(root, rel));
  const dir = path.posix.dirname(rel);
  const sdk = (/<Project\b[^>]*\bSdk="([^"]+)"/.exec(text) || [])[1] || '';
  const packages = lib.xmlElements(text, 'PackageReference').map(e => ({
    id: e.attrs.Include || e.attrs.Update || '',
    version: e.attrs.Version || e.child.Version || '',
    versionOverride: e.attrs.VersionOverride || e.child.VersionOverride || '',
  }));
  const projectRefs = lib.xmlElements(text, 'ProjectReference').map(e => {
    const include = (e.attrs.Include || '').replace(/\\/g, '/');
    const target = path.posix.normalize(path.posix.join(dir, include));
    return { include, target, name: path.posix.basename(target).replace(/\.csproj$/i, '') };
  });
  const frameworkRefs = lib.xmlElements(text, 'FrameworkReference').map(e => e.attrs.Include || '');
  return { rel, name: path.posix.basename(rel).replace(/\.csproj$/i, ''), sdk, packages, projectRefs, frameworkRefs };
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
  const findings = [];
  if (!/<ManagePackageVersionsCentrally>\s*true\s*<\/ManagePackageVersionsCentrally>/i.test(text)) {
    findings.push(lib.finding('error', rel, 'ManagePackageVersionsCentrally is not enabled', OWNER_NUGET));
  }
  const packages = lib.xmlElements(text, 'PackageVersion').map(e => ({
    id: e.attrs.Include || '',
    version: e.attrs.Version || e.child.Version || '',
  }));
  for (const pkg of packages) {
    const id = pkg.id.toLowerCase();
    if (!pkg.version || /[*\[\](),]/.test(pkg.version)) {
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
  const findings = [];
  for (const section of ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']) {
    for (const [name, spec] of Object.entries(pkg[section] || {})) {
      if (npmVersionIsFloating(spec)) {
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
  if (rel.endsWith('.csproj')) return checkProjectFile(ctx, rel);
  if (base === 'Directory.Packages.props') return checkPackagesProps(ctx, rel);
  if (base === 'package.json') return checkPackageJson(ctx, rel);
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

module.exports = { checkFile, checkAll, isManifest, makeContext, parseProject };

if (require.main === module) {
  const root = lib.rootFrom(__dirname, 2);
  const args = process.argv.slice(2);
  let findings;
  if (args.length === 0) {
    findings = checkAll(root);
  } else {
    const ctx = makeContext(root);
    findings = [];
    for (const arg of args) {
      const rel = lib.relInside(root, arg);
      if (!rel) throw new Error(`Path is outside the project: ${arg}`);
      findings.push(...checkFile(root, rel, ctx));
    }
  }
  if (findings.length) process.stdout.write(`${lib.formatFindings(findings)}\n`);
  const errors = findings.filter(f => f.severity === 'error').length;
  process.stdout.write(`check-manifests: ${errors} error(s), ${findings.length - errors} warning(s)\n`);
  process.exitCode = errors ? 1 : 0;
}
