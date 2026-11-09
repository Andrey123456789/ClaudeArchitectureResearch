// Owner: mechanical dependency checks — Central Package Management, version form, deprecated/non-default packages, npm manifest hygiene | Scope: common | Loads: CLI (`node .claude/scripts/check-dependencies.mjs [files...]`), PostToolUse hook, `verify`, `add-dependency` | Enforced: exit code 1 on errors
// Policy owners: .claude/rules/dependencies.md, docs/technology-stack.md, .claude/skills/add-dependency/SKILL.md

import path from 'node:path';
import { projectRoot, rel, walk, readText, exists, finding, reportCli, isMain } from './lib.mjs';

const DEPENDENCY_RULES = '.claude/rules/dependencies.md';
const STACK = 'docs/technology-stack.md';
const ADD_DEPENDENCY = '.claude/skills/add-dependency/SKILL.md';

// Deprecated or explicitly excluded packages: always an error.
const BLOCKED_NUGET = new Map([
  ['Microsoft.Extensions.Http.Polly', `${STACK} § Conditional Technologies`],
  ['Polly.Extensions.Http', `${STACK} § Conditional Technologies`],
  ['Serilog.Sinks.Elasticsearch', '`logging` skill (deprecated sink)'],
  ['FluentValidation.AspNetCore', `${STACK} § Backend`],
]);

// Not part of the approved default: needs a concrete, approved reason.
const REVIEW_NUGET = new Map([
  ['Polly', `${STACK} § Conditional Technologies (direct Polly is a documented exception)`],
  ['MediatR', 'CLAUDE.md § Architecture Decisions (not adopted)'],
  ['AutoMapper', `${STACK} § Conditional Technologies (mapping)`],
  ['Microsoft.AspNetCore.OpenApi', `${STACK} § Backend (Swagger UI baseline)`],
]);

const REVIEW_NPM_PREFIXES = [
  ['@ngrx/', `${STACK} § Frontend`],
  ['axios', `${STACK} § Frontend`],
  ['lodash', `${STACK} § Frontend`],
  ['bootstrap', `${STACK} § Frontend`],
  ['tailwindcss', `${STACK} § Frontend`],
];

const NPM_TOOLING = [
  /^@types\//, /^typescript$/, /^vitest$/, /^@vitest\//, /^jsdom$/, /^@angular\/cli$/,
  /^@angular\/build$/, /^@angular-devkit\//, /^@angular\/compiler-cli$/, /^eslint/,
  /^@typescript-eslint\//, /^prettier$/, /^@playwright\/test$/, /^karma/, /^jasmine/,
];

const isManifest = (relative) =>
  relative.endsWith('.csproj') ||
  path.posix.basename(relative) === 'Directory.Packages.props' ||
  path.posix.basename(relative) === 'package.json';

function cpmEnabled(root) {
  const props = readText(root, 'Directory.Packages.props');
  return props !== null && /<ManagePackageVersionsCentrally>\s*true\s*<\/ManagePackageVersionsCentrally>/i.test(props);
}

function isPrerelease(version) {
  return /-[0-9A-Za-z]/.test(version.replace(/^[\^~=v]+/, ''));
}

function isFloating(version) {
  return /[*]/.test(version) || /^[[(]/.test(version.trim()) || /^(latest|next|x)$/i.test(version.trim()) || version.trim() === '';
}

function packageEntries(xml, element) {
  const entries = [];
  const pattern = new RegExp(`<${element}\\b([^>]*?)(/>|>([\\s\\S]*?)</${element}>)`, 'g');
  for (const match of xml.matchAll(pattern)) {
    const attributes = match[1];
    const body = match[3] ?? '';
    const include = /\b(?:Include|Update)\s*=\s*"([^"]+)"/.exec(attributes)?.[1];
    if (!include) {
      continue;
    }
    const version =
      /\bVersion\s*=\s*"([^"]*)"/.exec(attributes)?.[1] ??
      /<Version>\s*([^<]*)\s*<\/Version>/.exec(body)?.[1];
    const versionOverride = /\bVersionOverride\s*=\s*"([^"]*)"/.exec(attributes)?.[1];
    entries.push({ include, version, versionOverride });
  }
  return entries;
}

function checkNuGetName(file, id, findings) {
  if (BLOCKED_NUGET.has(id)) {
    findings.push(finding('error', file, `package '${id}' is deprecated or excluded`, BLOCKED_NUGET.get(id)));
  } else if (REVIEW_NUGET.has(id)) {
    findings.push(finding('warning', file, `package '${id}' is outside the approved default; keep it only with a recorded, approved reason`, REVIEW_NUGET.get(id)));
  }
}

function checkCsproj(root, file, findings) {
  const xml = readText(root, file);
  if (xml === null) {
    return;
  }
  const centrallyManaged = cpmEnabled(root);
  for (const entry of packageEntries(xml, 'PackageReference')) {
    checkNuGetName(file, entry.include, findings);
    if (centrallyManaged && entry.version !== undefined) {
      findings.push(finding('error', file, `PackageReference '${entry.include}' declares Version="${entry.version}"; versions belong in Directory.Packages.props`, `${DEPENDENCY_RULES} § NuGet`));
    }
    if (entry.versionOverride !== undefined) {
      findings.push(finding('warning', file, `PackageReference '${entry.include}' uses VersionOverride; confirm the concrete reason`, `${DEPENDENCY_RULES} § NuGet`));
    }
  }
}

function checkPackagesProps(root, file, findings) {
  const xml = readText(root, file);
  if (xml === null) {
    return;
  }
  if (!/<ManagePackageVersionsCentrally>\s*true\s*<\/ManagePackageVersionsCentrally>/i.test(xml)) {
    findings.push(finding('error', file, 'ManagePackageVersionsCentrally must be true', `${DEPENDENCY_RULES} § NuGet`));
  }
  const seen = new Set();
  for (const entry of packageEntries(xml, 'PackageVersion')) {
    checkNuGetName(file, entry.include, findings);
    const key = entry.include.toLowerCase();
    if (seen.has(key)) {
      findings.push(finding('error', file, `PackageVersion '${entry.include}' is declared more than once`, `${DEPENDENCY_RULES} § NuGet`));
    }
    seen.add(key);
    const version = entry.version ?? '';
    if (isFloating(version)) {
      findings.push(finding('warning', file, `PackageVersion '${entry.include}' uses a floating or range version '${version}' (allowed only when explicitly requested)`, `${ADD_DEPENDENCY} § 2. Select the Version`));
    } else if (isPrerelease(version)) {
      findings.push(finding('warning', file, `PackageVersion '${entry.include}' uses prerelease '${version}' (allowed only when explicitly requested)`, `${ADD_DEPENDENCY} § 2. Select the Version`));
    }
  }
}

function checkPackageJson(root, file, findings) {
  const text = readText(root, file);
  if (text === null) {
    return;
  }
  let manifest;
  try {
    manifest = JSON.parse(text);
  } catch (error) {
    findings.push(finding('error', file, `invalid JSON: ${error.message}`));
    return;
  }
  const sections = ['dependencies', 'devDependencies', 'optionalDependencies'];
  let count = 0;
  for (const section of sections) {
    const deps = manifest[section] ?? {};
    for (const [name, version] of Object.entries(deps)) {
      count += 1;
      const value = String(version);
      if (/^(file:|link:|workspace:|git|https?:)/.test(value)) {
        continue;
      }
      if (isFloating(value)) {
        findings.push(finding('warning', file, `${section}.${name} uses a floating version '${value}' (allowed only when explicitly requested)`, `${ADD_DEPENDENCY} § 2. Select the Version`));
      } else if (isPrerelease(value)) {
        findings.push(finding('warning', file, `${section}.${name} uses prerelease '${value}' (allowed only when explicitly requested)`, `${ADD_DEPENDENCY} § 2. Select the Version`));
      }
      if (section === 'dependencies' && NPM_TOOLING.some((pattern) => pattern.test(name))) {
        findings.push(finding('warning', file, `build/test tooling '${name}' is in dependencies; expected devDependencies`, `${DEPENDENCY_RULES} § npm`));
      }
      const review = REVIEW_NPM_PREFIXES.find(([prefix]) => name === prefix || name.startsWith(prefix));
      if (review) {
        findings.push(finding('warning', file, `'${name}' is not part of the default frontend stack; keep it only for a concrete requirement`, review[1]));
      }
    }
  }
  const dir = path.posix.dirname(file);
  const lockfiles = ['package-lock.json', 'npm-shrinkwrap.json', 'pnpm-lock.yaml', 'yarn.lock'];
  if (count > 0 && !lockfiles.some((lock) => exists(root, path.posix.join(dir, lock)))) {
    findings.push(finding('warning', file, 'no lockfile next to package.json; commit package-lock.json', `${DEPENDENCY_RULES} § npm`));
  }
}

/** Checks the given repository-relative files, or every manifest when none are given. */
export function checkDependencies(root, files) {
  const targets = (files && files.length > 0 ? files : walk(root, '.', isManifest)).filter(isManifest);
  const findings = [];
  for (const file of targets) {
    if (!exists(root, file)) {
      continue;
    }
    if (file.endsWith('.csproj')) {
      checkCsproj(root, file, findings);
    } else if (file.endsWith('Directory.Packages.props')) {
      checkPackagesProps(root, file, findings);
    } else {
      checkPackageJson(root, file, findings);
    }
  }
  return findings;
}

if (isMain(import.meta.url)) {
  const root = projectRoot();
  const files = process.argv.slice(2).map((file) => rel(root, path.resolve(file)));
  reportCli('Dependency check', checkDependencies(root, files));
}
