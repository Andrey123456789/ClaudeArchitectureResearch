#!/usr/bin/env node
// Owns: mechanical checks of .NET and npm manifests (Central Package Management,
// version pinning, non-default packages, layer project references).
// Scope: backend, frontend manifests. Loads: run by the post-edit hook and by
// the verify / add-dependency / project-structure workflows.
//
// Usage: node .claude/scripts/check-manifests.mjs [repoRoot]
// Exit code 1 when findings exist. Messages point to the owning instruction file.

import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, relative, basename, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const SKIP_DIRS = new Set(['node_modules', 'bin', 'obj', '.git', 'dist', '.angular', 'TestResults', 'coverage']);

const STACK = 'docs/technology-stack.md';
const DEPS = '.claude/rules/dependencies.md';
const ARCH = '.claude/rules/architecture.md';

// NuGet packages that are deprecated, non-default, or Reserved per the owner file.
const NUGET_FLAGS = new Map([
  ['microsoft.extensions.http.polly', `deprecated integration package (${STACK}, Resilience)`],
  ['polly.extensions.http', `deprecated integration package (${STACK}, Resilience)`],
  ['polly', `direct Polly is an explicit, documented exception (${STACK}, Resilience)`],
  ['serilog.sinks.elasticsearch', 'deprecated sink package; see the logging skill reference'],
  ['fluentvalidation.aspnetcore', `legacy automatic-validation integration (${STACK}, Backend)`],
  ['mediatr', 'mediator-based organization is not adopted and requires approval (CLAUDE.md)'],
  ['automapper', `another mapping framework requires approval (${STACK}, Conditional Technologies)`],
]);

// npm packages not added by default.
const NPM_FLAGS = [
  [/^@ngrx\//, `not added by default; needs a concrete need (${STACK}, Frontend)`],
  [/^axios$/, `not added by default; needs a concrete need (${STACK}, Frontend)`],
  [/^lodash(-es)?$/, `not added by default; needs a concrete need (${STACK}, Frontend)`],
  [/^bootstrap$/, `not added by default; needs a concrete need (${STACK}, Frontend)`],
  [/^tailwindcss$/, `not added by default; needs a concrete need (${STACK}, Frontend)`],
];

// Build/test tooling that belongs in devDependencies.
const DEV_TOOLING = [
  /^typescript$/, /^@angular\/cli$/, /^@angular-devkit\//, /^@angular\/build$/,
  /^@angular\/compiler-cli$/, /^vitest$/, /^@vitest\//, /^jasmine/, /^karma/,
  /^@playwright\/test$/, /^playwright$/, /^eslint/, /^@typescript-eslint\//, /^prettier$/,
];

const LAYERS = ['Domain', 'Application', 'Infrastructure', 'Api'];
const FORBIDDEN_REFS = {
  Domain: ['Application', 'Infrastructure', 'Api'],
  Application: ['Infrastructure', 'Api'],
  Infrastructure: ['Api'],
  Api: [],
};

function walk(dir, out = []) {
  for (const entry of readdirSync(dir)) {
    if (SKIP_DIRS.has(entry)) continue;
    const full = join(dir, entry);
    let st;
    try { st = statSync(full); } catch { continue; }
    if (st.isDirectory()) walk(full, out);
    else out.push(full);
  }
  return out;
}

function layerOf(projectFile) {
  const name = basename(projectFile).replace(/\.csproj$/i, '');
  if (/tests?$/i.test(name)) return null;
  const last = name.split('.').pop();
  return LAYERS.find((l) => l.toLowerCase() === last.toLowerCase()) ?? null;
}

function isPrerelease(version) {
  return /\d-[0-9A-Za-z]/.test(version) || /\b(alpha|beta|rc|preview|nightly|dev|next|canary)\b/i.test(version);
}

function readXml(file) {
  return readFileSync(file, 'utf8').replace(/<!--[\s\S]*?-->/g, '');
}

function checkCsproj(file, rel, findings) {
  const xml = readXml(file);
  for (const m of xml.matchAll(/<PackageReference\b([^>]*)>/gi)) {
    const attrs = m[1];
    const id = (attrs.match(/\bInclude\s*=\s*"([^"]+)"/i) || [])[1];
    if (/\bVersion\s*=/i.test(attrs)) {
      findings.push([rel, `PackageReference ${id ?? ''} declares a Version; versions belong in Directory.Packages.props`, `${DEPS}, NuGet`]);
    }
    if (id && NUGET_FLAGS.has(id.toLowerCase())) {
      findings.push([rel, `package ${id}: ${NUGET_FLAGS.get(id.toLowerCase())}`, 'add-dependency workflow']);
    }
  }
  const layer = layerOf(file);
  if (!layer) return;
  for (const m of xml.matchAll(/<ProjectReference\b[^>]*\bInclude\s*=\s*"([^"]+)"/gi)) {
    const target = layerOf(m[1].replace(/\\/g, '/'));
    if (target && FORBIDDEN_REFS[layer].includes(target)) {
      findings.push([rel, `${layer} project references ${target} (outward dependency)`, `${ARCH}, Dependency Direction`]);
    }
  }
}

function checkPackagesProps(file, rel, findings) {
  const xml = readXml(file);
  if (!/<ManagePackageVersionsCentrally>\s*true\s*</i.test(xml)) {
    findings.push([rel, 'ManagePackageVersionsCentrally is not enabled', `${DEPS}, NuGet`]);
  }
  for (const m of xml.matchAll(/<PackageVersion\b([^>]*)>/gi)) {
    const id = (m[1].match(/\bInclude\s*=\s*"([^"]+)"/i) || [])[1] ?? '?';
    const version = (m[1].match(/\bVersion\s*=\s*"([^"]*)"/i) || [])[1] ?? '';
    if (/[*[\]()]/.test(version)) findings.push([rel, `${id} uses a floating/range version "${version}"`, 'add-dependency workflow']);
    else if (isPrerelease(version)) findings.push([rel, `${id} uses a prerelease version "${version}"`, 'add-dependency workflow']);
    if (NUGET_FLAGS.has(id.toLowerCase())) findings.push([rel, `package ${id}: ${NUGET_FLAGS.get(id.toLowerCase())}`, 'add-dependency workflow']);
  }
}

function checkPackageJson(file, rel, findings) {
  let pkg;
  try { pkg = JSON.parse(readFileSync(file, 'utf8')); } catch (e) {
    findings.push([rel, `invalid JSON: ${e.message}`, DEPS]);
    return;
  }
  for (const section of ['dependencies', 'devDependencies']) {
    for (const [name, spec] of Object.entries(pkg[section] ?? {})) {
      if (spec === '*' || /^(latest|next)$/i.test(spec)) findings.push([rel, `${name} uses a floating version "${spec}"`, 'add-dependency workflow']);
      else if (isPrerelease(spec)) findings.push([rel, `${name} uses a prerelease version "${spec}"`, 'add-dependency workflow']);
      for (const [re, msg] of NPM_FLAGS) if (re.test(name)) findings.push([rel, `${name}: ${msg}`, 'add-dependency workflow']);
      if (section === 'dependencies' && DEV_TOOLING.some((re) => re.test(name))) {
        findings.push([rel, `${name} is build/test tooling listed in dependencies`, `${DEPS}, npm`]);
      }
    }
  }
  if (!existsSync(join(dirname(file), 'package-lock.json'))) {
    findings.push([rel, 'no package-lock.json next to package.json', `${DEPS}, npm`]);
  }
}

export function checkManifests(root) {
  const findings = [];
  for (const file of walk(root)) {
    const rel = relative(root, file).replace(/\\/g, '/');
    const name = basename(file);
    if (/\.csproj$/i.test(name)) checkCsproj(file, rel, findings);
    else if (name === 'Directory.Packages.props') checkPackagesProps(file, rel, findings);
    else if (name === 'package.json' && !rel.startsWith('.claude/')) checkPackageJson(file, rel, findings);
  }
  return findings;
}

export function formatFindings(findings) {
  return findings.map(([file, msg, owner]) => `- ${file}: ${msg} (see ${owner})`).join('\n');
}

const isMain = process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const root = resolve(process.argv[2] ?? join(dirname(fileURLToPath(import.meta.url)), '..', '..'));
  const findings = checkManifests(root);
  if (findings.length) {
    console.log(`Manifest check: ${findings.length} finding(s)\n${formatFindings(findings)}`);
    process.exit(1);
  }
  console.log('Manifest check: PASS');
}
