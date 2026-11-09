// Architecture check: fast source-level heuristics for backend layer boundaries.
// Usage: node .claude/scripts/check-architecture.mjs
// Exit codes: 0 = no violations (warnings may be printed), 1 = violations, 2 = setup error.
// Policy owners: .claude/rules/architecture.md, .claude/rules/persistence.md,
// .claude/skills/development-workflow/SKILL.md (Database deployment).
// Findings are evidence for review, not a substitute for it: comments or strings can
// produce false positives, and many boundary rules are not mechanically checkable.

import {
  SetupError, formatFindings, isMainModule, readText, resolveProjectRoot, walkFiles,
} from './lib/repo.mjs';
import { classifyProject } from './check-manifests.mjs';

const OWNER = {
  domain: '.claude/rules/architecture.md (Domain)',
  application: '.claude/rules/architecture.md (Application)',
  api: '.claude/rules/architecture.md (API)',
  repositories: '.claude/rules/persistence.md (Repositories)',
  seeding: '.claude/rules/persistence.md (Development Seeding)',
  deployment: 'development-workflow (Database deployment)',
};

const DOMAIN_FORBIDDEN = [
  [/^\s*using\s+Microsoft\.EntityFrameworkCore\b/m, 'Domain uses EF Core'],
  [/^\s*using\s+Microsoft\.AspNetCore\b/m, 'Domain uses ASP.NET Core'],
  [/^\s*using\s+System\.Net\.Http\b/m, 'Domain uses HTTP client types'],
];

const APPLICATION_FORBIDDEN = [
  [/^\s*using\s+Microsoft\.EntityFrameworkCore\b/m, 'Application uses EF Core', OWNER.application],
  [/\bDbContext\b|\bDbSet\s*</, 'Application references DbContext/DbSet', OWNER.application],
  [/^\s*using\s+Microsoft\.AspNetCore\b/m, 'Application uses ASP.NET Core types', OWNER.application],
  [/\bIActionResult\b|\bActionResult\s*</, 'Application returns MVC action results', OWNER.application],
  [/\bHttpResponseMessage\b/, 'Application exposes HttpResponseMessage', OWNER.application],
  [/\bIQueryable\s*</, 'Application exposes IQueryable', OWNER.repositories],
  [/\bIGenericRepository\s*</, 'Application depends on a generic repository contract', OWNER.repositories],
];

const APPLICATION_REVIEW = [
  [/\bHybridCache\b|\bIDistributedCache\b|\bIMemoryCache\b/, 'Application uses cache infrastructure APIs directly; confirm a deliberate boundary abstraction', OWNER.application],
];

function projectOf(file) {
  const parts = file.split('/');
  if (parts[0] !== 'backend' || parts.length < 3) return null;
  return { dir: `backend/${parts[1]}`, ...classifyProject(`${parts[1]}.csproj`) };
}

function stripComments(source) {
  return source.replace(/\/\*[\s\S]*?\*\//g, '').replace(/^\s*\/\/.*$/gm, '');
}

export function checkArchitecture(root) {
  const files = walkFiles(root, 'backend').filter((f) => f.endsWith('.cs'));
  const findings = [];
  for (const file of files) {
    const project = projectOf(file);
    if (!project || project.kind !== 'production') continue;
    const source = stripComments(readText(root, file) ?? '');
    const inMigrations = /\/Migrations\//.test(file);

    if (project.layer === 'Domain') {
      for (const [pattern, message] of DOMAIN_FORBIDDEN) {
        if (pattern.test(source)) findings.push({ level: 'violation', file, message, owner: OWNER.domain });
      }
    }

    if (project.layer === 'Application') {
      for (const [pattern, message, owner] of APPLICATION_FORBIDDEN) {
        if (pattern.test(source)) findings.push({ level: 'violation', file, message, owner });
      }
      for (const [pattern, message, owner] of APPLICATION_REVIEW) {
        if (pattern.test(source)) findings.push({ level: 'warning', file, message, owner });
      }
    }

    if (project.layer === 'Api') {
      const isController = /\/Controllers\//.test(file) || /class\s+\w+Controller\b/.test(source);
      if (isController && /\bDbContext\b/.test(source)) {
        findings.push({ level: 'violation', file, message: 'Controller accesses DbContext', owner: OWNER.api });
      }
      if (isController && /^\s*using\s+[\w.]+\.Infrastructure(\.[\w.]+)?\s*;/m.test(source)) {
        findings.push({ level: 'violation', file, message: 'Controller imports an Infrastructure namespace', owner: OWNER.api });
      }
      if (/\.Migrate(Async)?\s*\(/.test(source)) {
        findings.push({ level: 'warning', file, message: 'API startup applies migrations; confirm this never runs automatically against Production', owner: OWNER.deployment });
      }
    }

    if (/\/Seeding\//.test(file) && /\.Migrate(Async)?\s*\(|\bEnsureCreated(Async)?\s*\(/.test(source)) {
      findings.push({ level: 'violation', file, message: 'the development seeder creates or migrates the schema', owner: OWNER.seeding });
    }

    if (project.layer === 'Infrastructure' && !inMigrations && !/\/Seeding\//.test(file) &&
        /\bEnsureCreated(Async)?\s*\(/.test(source)) {
      findings.push({ level: 'warning', file, message: 'EnsureCreated bypasses migrations; confirm this is intended', owner: OWNER.deployment });
    }
  }
  const projects = new Set(files.map((f) => projectOf(f)?.dir).filter(Boolean));
  return { findings, summary: `${files.length} C# file(s) in ${projects.size} backend project(s)` };
}

function main() {
  let root;
  try {
    root = resolveProjectRoot(import.meta.url);
  } catch (error) {
    process.stderr.write(`check-architecture: ${error.message}\n`);
    process.exit(2);
  }
  const { findings, summary } = checkArchitecture(root);
  if (summary.startsWith('0 ')) {
    process.stdout.write('check-architecture: NOT APPLICABLE (no C# files under backend/).\n');
    process.exit(0);
  }
  const violations = findings.filter((f) => f.level === 'violation');
  process.stdout.write(`check-architecture: checked ${summary}.\n`);
  if (findings.length > 0) process.stdout.write(`${formatFindings('Findings:', findings)}\n`);
  process.stdout.write(violations.length > 0
    ? `check-architecture: FAIL (${violations.length} violation(s)).\n`
    : 'check-architecture: PASS.\n');
  process.exit(violations.length > 0 ? 1 : 0);
}

if (isMainModule(import.meta.url)) {
  try {
    main();
  } catch (error) {
    if (!(error instanceof SetupError)) process.stderr.write(`check-architecture: unexpected error: ${error.stack ?? error}\n`);
    process.exit(2);
  }
}
