#!/usr/bin/env node
// Level: 3-project | Owns: package manifest check — Central Package Management, explicit
// stable versions, deny/review lists, frontend packages not added by default.
// Usage: node .claude/scripts/check-packages.cjs   (exit 0 pass, 1 violations, 2 environment error)
'use strict';

const fs = require('fs');
const path = require('path');
const lib = require('./lib/project.cjs');

const PRERELEASE = /-(alpha|beta|rc|preview|pre|dev|nightly|canary|next)/i;

function nugetVersionProblem(version) {
  if (version === null || version === undefined || version.trim() === '') return 'missing version';
  if (version.includes('*')) return `floating version "${version}"`;
  if (/^[[(]/.test(version.trim())) return `version range "${version}"`;
  return null;
}

function npmVersionProblem(spec) {
  const v = String(spec).trim();
  if (v === '' || v === '*' || /^x(\.x)*$/i.test(v) || /^latest$/i.test(v) || v.includes('||') || /^[<>]/.test(v)) {
    return `floating version "${v}"`;
  }
  return null;
}

function checkPackages(root) {
  const policy = lib.readJson(path.join(root, '.claude', 'scripts', 'package-policy.json'));
  const frontendCheck = lib.requireModuleJson(root, 'frontend', 'check.json');
  const violations = [];
  const warnings = [];
  const rel = (file) => lib.toPosix(path.relative(root, file));

  const denied = new Map(Object.entries(policy.nuget.denied).map(([k, v]) => [k.toLowerCase(), v]));
  const review = new Map(Object.entries(policy.nuget.review).map(([k, v]) => [k.toLowerCase(), v]));

  // NuGet
  const projectFiles = lib.walk(root, (name) => name.endsWith('.csproj'));
  const centralFile = path.join(root, 'Directory.Packages.props');
  let central = null;
  if (fs.existsSync(centralFile)) {
    central = lib.parseMsbuild(lib.readText(centralFile));
    if ((central.properties.ManagePackageVersionsCentrally || '').toLowerCase() !== 'true') {
      violations.push('Directory.Packages.props: ManagePackageVersionsCentrally must be true (package-management.md).');
    }
    for (const pv of central.packageVersions) {
      const problem = nugetVersionProblem(pv.version);
      if (problem) violations.push(`Directory.Packages.props: ${pv.include} has ${problem}; use an explicit verified stable version (add-dependency).`);
      else if (PRERELEASE.test(pv.version)) warnings.push(`Directory.Packages.props: ${pv.include} ${pv.version} is a prerelease — allowed only when explicitly requested (add-dependency).`);
    }
  } else if (projectFiles.length > 0) {
    violations.push('Directory.Packages.props is missing; Central Package Management is required (package-management.md).');
  }

  const checkPackageId = (where, id) => {
    const key = (id || '').toLowerCase();
    if (denied.has(key)) violations.push(`${where}: ${id} is denied — ${denied.get(key)}.`);
    else if (review.has(key)) warnings.push(`${where}: ${id} needs review — ${review.get(key)}.`);
  };
  if (central) for (const pv of central.packageVersions) checkPackageId('Directory.Packages.props', pv.include);

  for (const file of projectFiles) {
    const msbuild = lib.parseMsbuild(lib.readText(file));
    for (const ref of msbuild.packageReferences) {
      if (ref.version) violations.push(`${rel(file)}: PackageReference ${ref.include} declares Version="${ref.version}"; versions belong in Directory.Packages.props (package-management.md).`);
      if (ref.versionOverride) warnings.push(`${rel(file)}: ${ref.include} uses VersionOverride — keep only with a documented reason.`);
      checkPackageId(rel(file), ref.include);
    }
  }

  // npm
  const notByDefault = new Set(((frontendCheck && frontendCheck.notByDefaultPackages) || []).map((p) => p.toLowerCase()));
  const npmDenied = new Map(Object.entries(policy.npm.denied).map(([k, v]) => [k.toLowerCase(), v]));
  for (const file of lib.walk(root, (name) => name === 'package.json')) {
    let manifest;
    try {
      manifest = JSON.parse(lib.readText(file));
    } catch (error) {
      violations.push(`${rel(file)}: invalid JSON (${error.message}).`);
      continue;
    }
    const sections = ['dependencies', 'devDependencies', 'optionalDependencies', 'peerDependencies'];
    let count = 0;
    for (const section of sections) {
      for (const [name, spec] of Object.entries(manifest[section] || {})) {
        count += 1;
        const problem = npmVersionProblem(spec);
        if (problem) violations.push(`${rel(file)}: ${name} has ${problem} (add-dependency).`);
        else if (PRERELEASE.test(String(spec))) warnings.push(`${rel(file)}: ${name}@${spec} is a prerelease — allowed only when explicitly requested.`);
        const key = name.toLowerCase();
        if (npmDenied.has(key)) violations.push(`${rel(file)}: ${name} is denied — ${npmDenied.get(key)}.`);
        if (notByDefault.has(key)) warnings.push(`${rel(file)}: ${name} is not part of the default frontend stack — keep it only for a concrete requirement (frontend.decision).`);
      }
    }
    if (count > 0 && !fs.existsSync(path.join(path.dirname(file), 'package-lock.json'))) {
      violations.push(`${rel(file)}: package-lock.json is missing next to it; commit a consistent lockfile (package-management.md).`);
    }
  }

  return { violations, warnings };
}

function main() {
  try {
    const root = lib.resolveRoot(__dirname);
    const { violations, warnings } = checkPackages(root);
    for (const w of warnings) console.log(`warning: ${w}`);
    if (violations.length) {
      console.log(`Package check: ${violations.length} violation(s)`);
      for (const v of violations) console.log(`  - ${v}`);
      process.exit(1);
    }
    console.log('Package check: PASS');
  } catch (error) {
    console.error(`Package check could not run: ${error.message}`);
    process.exit(2);
  }
}

if (require.main === module) main();

module.exports = { checkPackages };
