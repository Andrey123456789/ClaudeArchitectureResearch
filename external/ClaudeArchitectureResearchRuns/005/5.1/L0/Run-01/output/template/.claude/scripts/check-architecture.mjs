#!/usr/bin/env node
// Level: 3 Project · Owns: mechanical backend architecture check (project references, forbidden namespaces) · Enforcement asset
// Policy owners: .claude/rules/1-architecture/backend-layers.md, persistence-boundary.md, entry-points.md
// Usage: node .claude/scripts/check-architecture.mjs [--root <dir>]
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const LAYERS_OWNER = '.claude/rules/1-architecture/backend-layers.md';
const ENTRY_OWNER = '.claude/rules/1-architecture/entry-points.md';
const PERSISTENCE_OWNER = '.claude/rules/1-architecture/persistence-boundary.md';

// Which project kinds each project kind may reference (backend/<Name>.<Layer> convention).
const ALLOWED_REFERENCES = {
  domain: [],
  application: ['domain'],
  infrastructure: ['application', 'domain'],
  api: ['application', 'infrastructure', 'domain'],
  'test-domain': ['domain'],
  'test-application': ['application', 'domain'],
  'test-infrastructure': ['infrastructure', 'application', 'domain'],
  'test-integration': ['api'],
};

const FORBIDDEN_NAMESPACES = {
  domain: ['Microsoft.EntityFrameworkCore', 'Microsoft.AspNetCore', 'System.Net.Http', 'Microsoft.Extensions.Caching'],
  application: ['Microsoft.EntityFrameworkCore', 'Microsoft.AspNetCore'],
};

const FORBIDDEN_PACKAGE_PREFIXES = {
  domain: ['Microsoft.EntityFrameworkCore', 'Microsoft.AspNetCore', 'Microsoft.Extensions.Caching'],
  application: ['Microsoft.EntityFrameworkCore', 'Microsoft.AspNetCore'],
};

export function classifyProject(projectName) {
  if (/\.Domain\.Tests$/.test(projectName)) return 'test-domain';
  if (/\.Application\.Tests$/.test(projectName)) return 'test-application';
  if (/\.Infrastructure\.Tests$/.test(projectName)) return 'test-infrastructure';
  if (/IntegrationTests$/.test(projectName)) return 'test-integration';
  if (/Tests?$/.test(projectName)) return 'test-other';
  if (/\.Domain$/.test(projectName)) return 'domain';
  if (/\.Application$/.test(projectName)) return 'application';
  if (/\.Infrastructure$/.test(projectName)) return 'infrastructure';
  if (/\.Api$/.test(projectName)) return 'api';
  return 'other';
}

function walk(directory, predicate, results = []) {
  if (!existsSync(directory)) return results;
  for (const entry of readdirSync(directory)) {
    if (entry === 'bin' || entry === 'obj' || entry === 'node_modules' || entry.startsWith('.')) continue;
    const full = path.join(directory, entry);
    if (statSync(full).isDirectory()) walk(full, predicate, results);
    else if (predicate(full)) results.push(full);
  }
  return results;
}

const rel = (root, file) => path.relative(root, file).split(path.sep).join('/');

export function checkProjectFile(root, csprojPath) {
  const findings = [];
  const absolute = path.resolve(root, csprojPath);
  if (!existsSync(absolute)) return findings;
  const name = path.basename(absolute, '.csproj');
  const kind = classifyProject(name);
  const xml = readFileSync(absolute, 'utf8');
  const display = rel(root, absolute);

  if (kind in ALLOWED_REFERENCES) {
    for (const match of xml.matchAll(/<ProjectReference\s+Include="([^"]+)"/g)) {
      const target = path.basename(match[1].replace(/\\/g, '/'), '.csproj');
      const targetKind = classifyProject(target);
      if (targetKind === 'other') continue;
      if (targetKind.startsWith('test')) {
        findings.push(`ERROR ${display}: references test project ${target} (owner: ${LAYERS_OWNER})`);
      } else if (!ALLOWED_REFERENCES[kind].includes(targetKind)) {
        const what = kind.startsWith('test') ? 'broader production reference than the test scope needs' : 'reference against the dependency direction';
        findings.push(`ERROR ${display}: ${what}: ${name} -> ${target} (owner: ${LAYERS_OWNER})`);
      }
    }
  }

  for (const prefix of FORBIDDEN_PACKAGE_PREFIXES[kind] ?? []) {
    const packagePattern = new RegExp(`<PackageReference\\s+Include="(${prefix.replace(/\./g, '\\.')}[^"]*)"`, 'g');
    for (const match of xml.matchAll(packagePattern)) {
      findings.push(`ERROR ${display}: ${kind} project references package ${match[1]} (owner: ${LAYERS_OWNER})`);
    }
    if (prefix === 'Microsoft.AspNetCore' && /<FrameworkReference\s+Include="Microsoft\.AspNetCore\.App"/.test(xml)) {
      findings.push(`ERROR ${display}: ${kind} project references the ASP.NET Core shared framework (owner: ${LAYERS_OWNER})`);
    }
  }

  for (const namespace of FORBIDDEN_NAMESPACES[kind] ?? []) {
    if (new RegExp(`<Using\\s+Include="${namespace.replace(/\./g, '\\.')}`).test(xml)) {
      findings.push(`ERROR ${display}: global using ${namespace} in a ${kind} project (owner: ${LAYERS_OWNER})`);
    }
  }
  return findings;
}

function checkSourceFiles(root, projectDirectory, kind) {
  const findings = [];
  const files = walk(projectDirectory, (file) => file.endsWith('.cs'));
  for (const file of files) {
    const text = readFileSync(file, 'utf8');
    const display = rel(root, file);
    for (const namespace of FORBIDDEN_NAMESPACES[kind] ?? []) {
      const usingPattern = new RegExp(`^\\s*(global\\s+)?using\\s+(static\\s+)?${namespace.replace(/\./g, '\\.')}(\\.|;)`, 'm');
      if (usingPattern.test(text)) {
        findings.push(`ERROR ${display}: ${kind} code uses ${namespace} (owner: ${LAYERS_OWNER})`);
      }
    }
    if (kind === 'application') {
      if (/\bHttpResponseMessage\b/.test(text)) {
        findings.push(`WARN  ${display}: HttpResponseMessage in Application — remote transport belongs to Infrastructure (owner: ${LAYERS_OWNER})`);
      }
      if (/\binterface\s+I\w*Repository\b/.test(text) && /\bIQueryable</.test(text)) {
        findings.push(`ERROR ${display}: repository contract exposes IQueryable<T> (owner: ${PERSISTENCE_OWNER})`);
      }
      if (/\bIGenericRepository</.test(text)) {
        findings.push(`ERROR ${display}: Application depends on a generic repository contract (owner: ${PERSISTENCE_OWNER})`);
      }
    }
    if (kind === 'api' && /[\\/]Controllers[\\/]/.test(file)) {
      if (/^\s*using\s+Microsoft\.EntityFrameworkCore/m.test(text) || /DbContext\b/.test(text)) {
        findings.push(`ERROR ${display}: controller accesses the persistence context (owner: ${ENTRY_OWNER})`);
      }
    }
  }
  return findings;
}

export function checkArchitecture(root) {
  const backend = path.join(root, 'backend');
  const findings = [];
  if (!existsSync(backend)) return { findings, projects: 0 };
  const projects = walk(backend, (file) => file.endsWith('.csproj'));
  for (const project of projects) {
    findings.push(...checkProjectFile(root, project));
    const kind = classifyProject(path.basename(project, '.csproj'));
    if (kind === 'domain' || kind === 'application' || kind === 'api') {
      findings.push(...checkSourceFiles(root, path.dirname(project), kind));
    }
  }
  return { findings, projects: projects.length };
}

const invokedDirectly = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (invokedDirectly) {
  const rootIndex = process.argv.indexOf('--root');
  const root = path.resolve(rootIndex > -1 ? process.argv[rootIndex + 1] : process.env.CLAUDE_PROJECT_DIR || process.cwd());
  const { findings, projects } = checkArchitecture(root);
  if (projects === 0) {
    console.log('Architecture check: NOT APPLICABLE (no backend projects found)');
    process.exit(0);
  }
  for (const finding of findings) console.log(finding);
  const errors = findings.filter((finding) => finding.startsWith('ERROR')).length;
  console.log(`Architecture check: ${errors === 0 ? 'PASS' : 'FAIL'} (${projects} projects, ${errors} errors, ${findings.length - errors} warnings)`);
  process.exit(errors === 0 ? 0 : 1);
}
