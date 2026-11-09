// Manifest check: NuGet Central Package Management, package versions, deprecated and
// review-required packages, project-reference direction, and npm manifest hygiene.
// Usage: node .claude/scripts/check-manifests.mjs
// Exit codes: 0 = no violations (warnings may be printed), 1 = violations, 2 = setup error.
// Policy owners: .claude/rules/dependencies.md, .claude/rules/architecture.md,
// docs/technology-stack.md, .claude/skills/add-dependency/SKILL.md.
// The package lists below mirror docs/technology-stack.md and add-dependency; keep them in
// sync through the template-maintenance workflow.

import path from 'node:path';
import {
  SetupError, formatFindings, isMainModule, readText, resolveProjectRoot, walkFiles,
} from './lib/repo.mjs';

const OWNER = {
  cpm: '.claude/rules/dependencies.md (NuGet)',
  npm: '.claude/rules/dependencies.md (npm)',
  versions: 'add-dependency (Select the Version)',
  stack: 'docs/technology-stack.md',
  decision: 'CLAUDE.md (Decision Control)',
  references: '.claude/rules/architecture.md (Dependency Direction)',
  packages: 'add-dependency (Package choices)',
  layout: 'docs/technology-stack.md (Solution Layout)',
};

// Deprecated packages: always a violation.
const NUGET_DEPRECATED = new Map([
  ['Microsoft.Extensions.Http.Polly', OWNER.packages],
  ['Polly.Extensions.Http', OWNER.packages],
  ['Serilog.Sinks.Elasticsearch', 'logging skill (Elasticsearch)'],
]);

// Packages that need an explicit decision or justification: reported as warnings.
const NUGET_REVIEW = new Map([
  ['FluentValidation.AspNetCore', `${OWNER.stack} (Validation)`],
  ['MediatR', 'CLAUDE.md (Architecture Decisions)'],
  ['AutoMapper', `${OWNER.stack} (Conditional Technologies)`],
  ['Polly', OWNER.packages],
  ['Polly.Core', OWNER.packages],
  ['Microsoft.EntityFrameworkCore.InMemory', '.claude/rules/testing.md (Database Tests)'],
  ['Npgsql.EntityFrameworkCore.PostgreSQL', OWNER.decision],
  ['Pomelo.EntityFrameworkCore.MySql', OWNER.decision],
  ['MongoDB.Driver', OWNER.decision],
  ['MassTransit', OWNER.decision],
  ['RabbitMQ.Client', OWNER.decision],
  ['Azure.Messaging.ServiceBus', OWNER.decision],
  ['Confluent.Kafka', OWNER.decision],
  ['Hangfire.Core', OWNER.decision],
  ['Quartz', OWNER.decision],
  ['Microsoft.Extensions.Caching.StackExchangeRedis', OWNER.decision],
  ['Marten', OWNER.decision],
  ['EventStore.Client', OWNER.decision],
]);

const NPM_REVIEW = new Map([
  ['@ngrx/store', `${OWNER.stack} (Angular Frontend)`],
  ['@ngrx/signals', `${OWNER.stack} (Angular Frontend)`],
  ['axios', `${OWNER.stack} (Angular Frontend)`],
  ['lodash', `${OWNER.stack} (Angular Frontend)`],
  ['bootstrap', `${OWNER.stack} (Angular Frontend)`],
  ['tailwindcss', `${OWNER.stack} (Angular Frontend)`],
]);

const NPM_TOOLING = /^(@angular\/cli|@angular-devkit\/|@angular\/build$|@angular\/compiler-cli$|typescript$|vitest$|@vitest\/|@playwright\/test$|playwright$|eslint|prettier$|karma|jasmine|@types\/)/;

const LAYER_RANK = { Domain: 0, Application: 1, Infrastructure: 2, Api: 3 };

// Classifies a backend project by its file name: <Name>.<Layer>.csproj or a test project.
export function classifyProject(projectFile) {
  const name = path.basename(projectFile).replace(/\.csproj$/i, '');
  if (/IntegrationTests$/i.test(name)) return { name, kind: 'test', layer: 'Integration' };
  const test = name.match(/\.(Domain|Application|Infrastructure|Api)\.Tests?$/i);
  if (test) return { name, kind: 'test', layer: normalizeLayer(test[1]) };
  if (/Tests?$/i.test(name)) return { name, kind: 'test', layer: 'Unknown' };
  const prod = name.match(/\.(Domain|Application|Infrastructure|Api)$/i);
  if (prod) return { name, kind: 'production', layer: normalizeLayer(prod[1]) };
  return { name, kind: 'production', layer: 'Unknown' };
}

function normalizeLayer(value) {
  const lower = value.toLowerCase();
  return Object.keys(LAYER_RANK).find((layer) => layer.toLowerCase() === lower) ?? 'Unknown';
}

function attribute(tag, name) {
  const match = tag.match(new RegExp(`\\b${name}\\s*=\\s*"([^"]*)"`, 'i'));
  return match ? match[1] : null;
}

function isFloating(version) {
  return /\*|^latest$|^x$/i.test(version.trim()) || version.trim() === '';
}

function isPrerelease(version) {
  return /-[0-9A-Za-z]/.test(version);
}

function checkReferenceDirection(from, to, file, findings) {
  if (to.kind === 'test') {
    findings.push({ level: 'violation', file, message: `${from.name} references test project ${to.name}`, owner: OWNER.references });
    return;
  }
  if (from.kind === 'production') {
    if (from.layer === 'Unknown' || to.layer === 'Unknown') return;
    if (LAYER_RANK[to.layer] >= LAYER_RANK[from.layer]) {
      findings.push({ level: 'violation', file, message: `${from.layer} project ${from.name} references ${to.layer} project ${to.name} (outward or sideways dependency)`, owner: OWNER.references });
    }
    return;
  }
  if (from.layer === 'Integration' || from.layer === 'Unknown' || to.layer === 'Unknown') return;
  if (LAYER_RANK[to.layer] > LAYER_RANK[from.layer]) {
    findings.push({ level: 'violation', file, message: `test project ${from.name} references ${to.layer} project ${to.name}, broader than its ${from.layer} test scope`, owner: OWNER.references });
  }
}

function checkCsproj(root, file, findings) {
  const text = readText(root, file) ?? '';
  const project = classifyProject(file);
  if (file.startsWith('backend/') && project.kind === 'production' && project.layer === 'Unknown') {
    findings.push({ level: 'warning', file, message: `project ${project.name} does not follow <Name>.<Layer> naming; a new production project is a Reserved decision`, owner: `${OWNER.layout}; ${OWNER.decision}` });
  }
  for (const match of text.matchAll(/<PackageReference\b([^>]*?)(\/>|>([\s\S]*?)<\/PackageReference>)/gi)) {
    const attrs = match[1];
    const body = match[3] ?? '';
    const id = attribute(attrs, 'Include') ?? attribute(attrs, 'Update') ?? '(unknown)';
    if (attribute(attrs, 'Version') !== null || /<Version>/i.test(body)) {
      findings.push({ level: 'violation', file, message: `PackageReference ${id} carries a version`, owner: OWNER.cpm });
    }
    if (attribute(attrs, 'VersionOverride') !== null) {
      findings.push({ level: 'warning', file, message: `PackageReference ${id} uses VersionOverride`, owner: OWNER.cpm });
    }
    checkPackageId(id, file, findings);
  }
  for (const match of text.matchAll(/<ProjectReference\b[^>]*\bInclude\s*=\s*"([^"]+)"/gi)) {
    const target = path.posix.normalize(path.posix.join(path.posix.dirname(file), match[1].replace(/\\/g, '/')));
    checkReferenceDirection(project, classifyProject(target), file, findings);
  }
}

function checkPackageId(id, file, findings) {
  if (NUGET_DEPRECATED.has(id)) {
    findings.push({ level: 'violation', file, message: `${id} is a deprecated package`, owner: NUGET_DEPRECATED.get(id) });
  } else if (NUGET_REVIEW.has(id)) {
    findings.push({ level: 'warning', file, message: `${id} needs an approved decision or a stated justification`, owner: NUGET_REVIEW.get(id) });
  }
}

function checkPackagesProps(root, file, findings) {
  const text = readText(root, file) ?? '';
  if (!/<ManagePackageVersionsCentrally>\s*true\s*<\/ManagePackageVersionsCentrally>/i.test(text)) {
    findings.push({ level: 'violation', file, message: 'ManagePackageVersionsCentrally is not enabled', owner: OWNER.cpm });
  }
  const textWithoutComments = text.replace(/<!--[\s\S]*?-->/g, '');
  for (const match of textWithoutComments.matchAll(/<PackageVersion\b([^>]*?)\/?>/gi)) {
    const id = attribute(match[1], 'Include') ?? '(unknown)';
    const version = attribute(match[1], 'Version') ?? '';
    if (isFloating(version)) {
      findings.push({ level: 'warning', file, message: `PackageVersion ${id} uses a floating or empty version "${version}"; allowed only when explicitly requested`, owner: OWNER.versions });
    } else if (isPrerelease(version)) {
      findings.push({ level: 'warning', file, message: `PackageVersion ${id} uses prerelease version ${version}; allowed only when explicitly requested`, owner: OWNER.versions });
    }
    checkPackageId(id, file, findings);
  }
}

function checkPackageJson(root, file, allFiles, findings) {
  const text = readText(root, file);
  let manifest;
  try {
    manifest = JSON.parse(text ?? '');
  } catch (error) {
    findings.push({ level: 'violation', file, message: `package.json is not valid JSON (${error.message})`, owner: OWNER.npm });
    return;
  }
  const dependencies = manifest.dependencies ?? {};
  const devDependencies = manifest.devDependencies ?? {};
  const all = { ...dependencies, ...devDependencies };
  const lockFile = path.posix.join(path.posix.dirname(file), 'package-lock.json');
  if (Object.keys(all).length > 0 && !allFiles.includes(lockFile)) {
    findings.push({ level: 'violation', file, message: 'package-lock.json is missing next to package.json', owner: OWNER.npm });
  }
  for (const [name, version] of Object.entries(all)) {
    if (typeof version === 'string' && isFloating(version)) {
      findings.push({ level: 'warning', file, message: `${name} uses floating version "${version}"; allowed only when explicitly requested`, owner: OWNER.versions });
    }
    if (NPM_REVIEW.has(name)) {
      findings.push({ level: 'warning', file, message: `${name} is not part of the default frontend stack; it needs a concrete requirement`, owner: NPM_REVIEW.get(name) });
    }
  }
  for (const name of Object.keys(dependencies)) {
    if (NPM_TOOLING.test(name)) {
      findings.push({ level: 'warning', file, message: `${name} looks like build/test tooling but is listed in dependencies`, owner: OWNER.npm });
    }
  }
}

export function checkManifests(root) {
  const files = walkFiles(root);
  const findings = [];
  const csprojFiles = files.filter((f) => f.toLowerCase().endsWith('.csproj'));
  const packagesProps = files.filter((f) => path.posix.basename(f) === 'Directory.Packages.props');
  const packageJsons = files.filter((f) => path.posix.basename(f) === 'package.json');

  if (csprojFiles.length > 0 && !files.includes('Directory.Packages.props')) {
    findings.push({ level: 'violation', file: 'Directory.Packages.props', message: 'repository-level Directory.Packages.props is missing', owner: OWNER.cpm });
  }
  for (const file of packagesProps) checkPackagesProps(root, file, findings);
  for (const file of csprojFiles) checkCsproj(root, file, findings);
  for (const file of packageJsons) checkPackageJson(root, file, files, findings);

  return {
    findings,
    summary: `${csprojFiles.length} project file(s), ${packagesProps.length} Directory.Packages.props, ${packageJsons.length} package.json`,
  };
}

function main() {
  let root;
  try {
    root = resolveProjectRoot(import.meta.url);
  } catch (error) {
    process.stderr.write(`check-manifests: ${error.message}\n`);
    process.exit(2);
  }
  const { findings, summary } = checkManifests(root);
  const violations = findings.filter((f) => f.level === 'violation');
  process.stdout.write(`check-manifests: checked ${summary}.\n`);
  if (findings.length > 0) process.stdout.write(`${formatFindings('Findings:', findings)}\n`);
  process.stdout.write(violations.length > 0
    ? `check-manifests: FAIL (${violations.length} violation(s)).\n`
    : 'check-manifests: PASS.\n');
  process.exit(violations.length > 0 ? 1 : 0);
}

if (isMainModule(import.meta.url)) {
  try {
    main();
  } catch (error) {
    if (!(error instanceof SetupError)) process.stderr.write(`check-manifests: unexpected error: ${error.stack ?? error}\n`);
    process.exit(2);
  }
}
