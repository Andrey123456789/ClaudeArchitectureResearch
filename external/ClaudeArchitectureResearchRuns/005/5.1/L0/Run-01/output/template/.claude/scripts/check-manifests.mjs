#!/usr/bin/env node
// Level: 3 Project · Owns: package-manifest checks (central versions, version form, listed packages, project references) · Enforcement asset
// Policy owners: .claude/rules/3-project/conventions.md, .claude/rules/0-core/dependency-hygiene.md,
//                .claude/rules/3-project/decisions.md, .claude/rules/1-architecture/backend-layers.md
// Usage: node .claude/scripts/check-manifests.mjs [--root <dir>]   (checks every manifest in the repository)
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { checkProjectFile } from './check-architecture.mjs';

const CONVENTIONS = '.claude/rules/3-project/conventions.md';
const HYGIENE = '.claude/rules/0-core/dependency-hygiene.md';
const DECISIONS = '.claude/rules/3-project/decisions.md';

// Packages that the project decisions list as not adopted, deprecated, conditional or otherwise needing attention.
const LISTED_NUGET = ['MediatR', 'Kommand', 'Microsoft.Extensions.Http.Polly', 'Polly.Extensions.Http', 'Polly', 'Polly.Core',
  'AutoMapper', 'Serilog.Sinks.Elasticsearch', 'FluentValidation.AspNetCore', 'xunit', 'xunit.v3', 'MSTest', 'MSTest.TestFramework',
  'Microsoft.EntityFrameworkCore.InMemory'];
const LISTED_NPM = [/^@ngrx\//, /^axios$/, /^lodash(-es)?$/, /^bootstrap$/, /^tailwindcss$/, /^@tailwindcss\//];
const DEV_TOOLING_NPM = [/^typescript$/, /^vitest$/, /^@vitest\//, /^@angular\/cli$/, /^@angular-devkit\//, /^@angular\/build$/,
  /^@angular\/compiler-cli$/, /^@playwright\/test$/, /^playwright$/, /^eslint/, /^@typescript-eslint\//, /^prettier$/,
  /^karma/, /^jasmine/, /^@types\//, /^jsdom$/];

const PRERELEASE_NUGET = /-(alpha|beta|preview|rc|dev|nightly|pre)/i;
const PRERELEASE_NPM = /-(alpha|beta|rc|next|canary|preview|nightly|dev)/i;

function checkCsproj(root, relativePath, xml) {
  const findings = [];
  for (const match of xml.matchAll(/<PackageReference\b([^>]*?)(\/>|>([\s\S]*?)<\/PackageReference>)/g)) {
    const attributes = match[1];
    const body = match[3] ?? '';
    const id = /Include="([^"]+)"/.exec(attributes)?.[1] ?? '?';
    if (/\sVersion="/.test(attributes) || /<Version>/.test(body)) {
      findings.push(`${id}: version declared in the project file — versions belong in Directory.Packages.props (${CONVENTIONS})`);
    }
    if (/VersionOverride="/.test(attributes)) {
      findings.push(`${id}: VersionOverride needs a reported reason (${CONVENTIONS})`);
    }
    if (LISTED_NUGET.includes(id)) {
      findings.push(`${id}: listed package — confirm against ${DECISIONS}`);
    }
  }
  findings.push(...checkProjectFile(root, relativePath).map((finding) => finding.replace(/^ERROR\s+[^:]+:\s*/, '')));
  return findings;
}

function checkCentralVersions(xml) {
  const findings = [];
  if (!/<ManagePackageVersionsCentrally>\s*true\s*<\/ManagePackageVersionsCentrally>/i.test(xml)) {
    findings.push(`ManagePackageVersionsCentrally is not enabled (${CONVENTIONS})`);
  }
  for (const match of xml.matchAll(/<PackageVersion\s+Include="([^"]+)"\s+Version="([^"]*)"/g)) {
    const [, id, version] = match;
    if (version.includes('*')) findings.push(`${id} ${version}: floating version (${HYGIENE})`);
    if (PRERELEASE_NUGET.test(version)) findings.push(`${id} ${version}: prerelease version (${HYGIENE})`);
    if (LISTED_NUGET.includes(id)) findings.push(`${id}: listed package — confirm against ${DECISIONS}`);
  }
  return findings;
}

function checkPackageJson(text) {
  const findings = [];
  let manifest;
  try {
    manifest = JSON.parse(text);
  } catch {
    return [`package.json is not valid JSON`];
  }
  for (const section of ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']) {
    for (const [name, version] of Object.entries(manifest[section] ?? {})) {
      if (typeof version !== 'string') continue;
      if (/^(\*|x|latest|)$/i.test(version.trim())) findings.push(`${name} "${version}": floating version (${HYGIENE})`);
      if (PRERELEASE_NPM.test(version)) findings.push(`${name} "${version}": prerelease version (${HYGIENE})`);
      if (LISTED_NPM.some((pattern) => pattern.test(name))) findings.push(`${name}: not added by default — confirm against ${DECISIONS}`);
      if (section === 'dependencies' && DEV_TOOLING_NPM.some((pattern) => pattern.test(name))) {
        findings.push(`${name}: build/test tooling in runtime dependencies (${CONVENTIONS})`);
      }
    }
  }
  return findings;
}

export function checkManifestFile(root, relativePath) {
  const absolute = path.resolve(root, relativePath);
  if (!existsSync(absolute) || /(^|\/)node_modules\//.test(relativePath)) return [];
  const text = readFileSync(absolute, 'utf8');
  const base = path.basename(relativePath);
  if (base.endsWith('.csproj')) return checkCsproj(root, relativePath, text);
  if (base === 'Directory.Packages.props') return checkCentralVersions(text);
  if (base === 'package.json') return checkPackageJson(text);
  return [];
}

function findManifests(directory, results = []) {
  if (!existsSync(directory)) return results;
  for (const entry of readdirSync(directory)) {
    if (['bin', 'obj', 'node_modules', 'dist'].includes(entry) || entry.startsWith('.')) continue;
    const full = path.join(directory, entry);
    if (statSync(full).isDirectory()) findManifests(full, results);
    else if (entry.endsWith('.csproj') || entry === 'Directory.Packages.props' || entry === 'package.json') results.push(full);
  }
  return results;
}

const invokedDirectly = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (invokedDirectly) {
  const rootIndex = process.argv.indexOf('--root');
  const root = path.resolve(rootIndex > -1 ? process.argv[rootIndex + 1] : process.env.CLAUDE_PROJECT_DIR || process.cwd());
  let total = 0;
  for (const file of findManifests(root)) {
    const relativePath = path.relative(root, file).split(path.sep).join('/');
    for (const finding of checkManifestFile(root, relativePath)) {
      console.log(`${relativePath}: ${finding}`);
      total += 1;
    }
  }
  console.log(`Manifest check: ${total === 0 ? 'PASS' : `${total} finding(s)`}`);
  process.exit(total === 0 ? 0 : 1);
}
