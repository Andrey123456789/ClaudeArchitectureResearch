// Owner: mechanical backend architecture checks — project reference direction, test-project reference scope, forbidden layer dependencies in C# sources | Scope: backend, backend-tests | Loads: CLI (`node .claude/scripts/check-architecture.mjs [files...]`), PostToolUse hook, `verify`, `project-structure` | Enforced: exit code 1 on errors
// Policy owners: .claude/rules/architecture.md, .claude/rules/api.md, .claude/rules/testing.md

import path from 'node:path';
import { projectRoot, rel, walk, readText, exists, finding, reportCli, isMain } from './lib.mjs';

const ARCH = '.claude/rules/architecture.md';
const API = '.claude/rules/api.md';
const TESTING = '.claude/rules/testing.md';

/** Classifies a project name such as "Shop.Application" or "Shop.IntegrationTests". */
export function classifyProject(name) {
  if (/Tests?$/.test(name)) {
    let target = 'Integration';
    if (/\.Domain\./.test(name)) target = 'Domain';
    else if (/\.Application\./.test(name)) target = 'Application';
    else if (/\.Infrastructure\./.test(name)) target = 'Infrastructure';
    return { kind: 'test', target, prefix: name.split('.')[0] };
  }
  const match = /^(.+)\.(Domain|Application|Infrastructure|Api)$/.exec(name);
  if (match) {
    return { kind: 'production', layer: match[2], prefix: match[1] };
  }
  return null;
}

// Allowed direct references per production layer; anything else is an error.
const PRODUCTION_ALLOWED = {
  Domain: [],
  Application: ['Domain'],
  Infrastructure: ['Application', 'Domain'],
  Api: ['Application', 'Infrastructure', 'Domain'],
};

// Test projects: [allowed, tolerated-with-warning]; anything else is an error.
const TEST_ALLOWED = {
  Domain: [['Domain'], []],
  Application: [['Application', 'Domain'], []],
  Infrastructure: [['Infrastructure', 'Application', 'Domain'], ['Api']],
  Integration: [['Api'], ['Infrastructure', 'Application', 'Domain']],
};

function projectName(file) {
  return path.posix.basename(file, '.csproj');
}

function checkProjectReferences(root, file, findings) {
  const xml = readText(root, file);
  if (xml === null) return;
  const self = classifyProject(projectName(file));
  if (!self) return;
  for (const match of xml.matchAll(/<ProjectReference\b[^>]*\bInclude\s*=\s*"([^"]+)"/g)) {
    const referenced = path.posix.basename(match[1].replace(/\\/g, '/'), '.csproj');
    const other = classifyProject(referenced);
    if (!other) continue;
    if (self.kind === 'production') {
      if (other.kind === 'test') {
        findings.push(finding('error', file, `production project references test project '${referenced}'`, `${ARCH} § Dependency Direction`));
      } else if (!PRODUCTION_ALLOWED[self.layer].includes(other.layer)) {
        findings.push(finding('error', file, `${self.layer} must not reference ${other.layer} ('${referenced}')`, `${ARCH} § Dependency Direction`));
      }
    } else if (other.kind === 'production') {
      const [allowed, tolerated] = TEST_ALLOWED[self.target];
      if (tolerated.includes(other.layer)) {
        findings.push(finding('warning', file, `test project references ${other.layer} ('${referenced}'); keep it only if the test scope requires it`, `${TESTING} § Test Project References`));
      } else if (!allowed.includes(other.layer)) {
        findings.push(finding('error', file, `${self.target} test project must not reference ${other.layer} ('${referenced}')`, `${TESTING} § Test Project References`));
      }
    }
  }
}

/** Finds the backend project directory a source file belongs to. */
function owningProject(file) {
  const parts = file.split('/');
  const index = parts.indexOf('backend');
  if (index < 0 || parts.length < index + 3) return null;
  const info = classifyProject(parts[index + 1]);
  return info ? { info, parts: parts.slice(index + 2) } : null;
}

function codeLines(text) {
  return text.split(/\r?\n/).map((line, i) => ({ line, number: i + 1 }))
    .filter(({ line }) => !/^\s*(\/\/|\*|\/\*)/.test(line));
}

function usingPattern(namespaces) {
  return new RegExp(`^\\s*(global\\s+)?using\\s+(static\\s+)?(?:\\w+\\s*=\\s*)?(${namespaces})\\b`);
}

function checkSource(root, file, findings) {
  const project = owningProject(file);
  if (!project || project.info.kind !== 'production') return;
  const text = readText(root, file);
  if (text === null) return;
  const { layer, prefix } = project.info;
  const escapedPrefix = prefix.replace(/\./g, '\\.');
  const rules = [];

  if (layer === 'Domain') {
    rules.push([usingPattern(`Microsoft\\.EntityFrameworkCore|Microsoft\\.AspNetCore|System\\.Net\\.Http|Microsoft\\.Extensions\\.Caching`), 'error', 'Domain imports an infrastructure, HTTP, persistence, or caching namespace', `${ARCH} § Domain`]);
    rules.push([usingPattern(`${escapedPrefix}\\.(Application|Infrastructure|Api)`), 'error', 'Domain depends on an outer layer', `${ARCH} § Dependency Direction`]);
    rules.push([/\b(IActionResult|ActionResult<|ProblemDetails|StatusCodes\.)/, 'error', 'Domain uses ASP.NET Core HTTP result types', `${API} § HTTP Semantics`]);
  }
  if (layer === 'Application') {
    rules.push([usingPattern('Microsoft\\.EntityFrameworkCore'), 'error', 'Application imports EF Core', `${ARCH} § Application`]);
    rules.push([usingPattern('Microsoft\\.AspNetCore\\.(Mvc|Http|Routing)'), 'error', 'Application imports ASP.NET Core transport types', `${ARCH} § Application`]);
    rules.push([usingPattern(`${escapedPrefix}\\.(Infrastructure|Api)`), 'error', 'Application depends on an outer layer', `${ARCH} § Dependency Direction`]);
    rules.push([/\w*DbContext\b|\bDbSet</, 'error', 'Application uses DbContext/DbSet', `${ARCH} § Application`]);
    rules.push([/\b(IActionResult|ActionResult<|ProblemDetails\b|StatusCodes\.)/, 'error', 'Application returns ASP.NET Core HTTP result types', `${API} § HTTP Semantics`]);
    rules.push([usingPattern('Microsoft\\.Extensions\\.Caching'), 'warning', 'Application imports cache infrastructure; confirm a deliberate boundary abstraction', `${ARCH} § Application`]);
    rules.push([/\bHttpResponseMessage\b/, 'warning', 'Application references HttpResponseMessage; remote transport belongs in Infrastructure', `${ARCH} § Application`]);
    if (/interface\s+I\w*Repository\b/.test(text)) {
      rules.push([/\bIQueryable</, 'error', 'repository contract exposes IQueryable', `${ARCH} § Repositories`]);
    }
    rules.push([/\bIGenericRepository\b/, 'error', 'Application depends on a generic repository contract', `${ARCH} § Repositories`]);
  }
  if (layer === 'Infrastructure') {
    rules.push([usingPattern(`${escapedPrefix}\\.Api`), 'error', 'Infrastructure depends on the Api project', `${ARCH} § Dependency Direction`]);
  }
  if (layer === 'Api' && project.parts.includes('Controllers')) {
    rules.push([/\w*DbContext\b|\bDbSet</, 'error', 'Controller accesses DbContext', `${ARCH} § API`]);
    rules.push([usingPattern(`${escapedPrefix}\\.Infrastructure`), 'error', 'Controller imports Infrastructure', `${ARCH} § API`]);
  }

  for (const { line, number } of codeLines(text)) {
    for (const [pattern, level, message, owner] of rules) {
      if (pattern.test(line)) {
        findings.push(finding(level, `${file}:${number}`, message, owner));
      }
    }
  }
}

/** Checks the given repository-relative files, or the whole backend when none are given. */
export function checkArchitecture(root, files) {
  const targets = files && files.length > 0
    ? files
    : walk(root, 'backend', (f) => f.endsWith('.csproj') || f.endsWith('.cs'));
  const findings = [];
  for (const file of targets) {
    if (!exists(root, file)) continue;
    if (file.endsWith('.csproj')) checkProjectReferences(root, file, findings);
    else if (file.endsWith('.cs')) checkSource(root, file, findings);
  }
  return findings;
}

if (isMain(import.meta.url)) {
  const root = projectRoot();
  const files = process.argv.slice(2).map((file) => rel(root, path.resolve(file)));
  reportCli('Architecture check', checkArchitecture(root, files));
}
