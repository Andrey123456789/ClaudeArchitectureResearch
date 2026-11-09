#!/usr/bin/env node
// Level: 3 Project · Owns: structural check of the level-first instruction system · Enforcement asset
// Procedure owner: template-maintenance workflow. Usage: node .claude/scripts/check-instructions.mjs [--root <dir>]
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const LEVEL_DIRS = { '0-core': 0, '1-architecture': 1, '2-technology': 2, '3-project': 3 };
const LEVEL_NAMES = ['Core', 'Architecture', 'Technology', 'Project'];

const REQUIRED_SKILLS = [
  'project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings', 'git-workflow', 'security-scan',
  'add-dependency', 'architecture-decision', 'template-maintenance',
  'ef-core', 'http-api', 'aspnet-error-handling', 'dotnet-testing', 'logging', 'httpclient-factory', 'configuration',
  'dependency-injection', 'caching', 'swagger', 'api-versioning', 'health-check', 'docker', 'ci-cd', 'angular',
  'modern-csharp', 'authentication',
];
const COMPETING_SKILLS = ['serilog', 'resilience'];
const USER_ONLY_SKILLS = ['template-maintenance'];

// Levels 0 and 1 name no concrete technology beyond the fixed platform (.NET, C#, TypeScript).
const CONCRETE_TECHNOLOGY_TERMS = [
  'EF Core', 'Entity Framework', 'EntityFramework', 'DbContext', 'DbSet', 'NUnit', 'xUnit', 'MSTest', 'Angular', 'RxJS',
  'Serilog', 'FluentValidation', 'Swagger', 'Swashbuckle', 'OpenAPI', 'Docker', 'Kubernetes', 'SQL Server', 'SqlServer',
  'LocalDB', 'Mapster', 'Polly', 'MediatR', 'Kommand', 'Testcontainers', 'Playwright', 'Vitest', 'npm', 'NuGet',
  'ASP.NET', 'IActionResult', 'ActionResult', 'ProblemDetails', 'WebApplicationFactory', 'IExceptionHandler',
  'HybridCache', 'Redis', 'GitHub Actions', 'NgRx', 'Axios', 'Lodash', 'Bootstrap', 'Tailwind', 'IHttpClientFactory',
  'Microsoft.Extensions', 'Microsoft.AspNetCore', 'Microsoft.EntityFrameworkCore', 'appsettings', 'Asp.Versioning',
  'OpenTelemetry', 'user-secrets',
];

const escapeRegExp = (value) => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const termPattern = (term) => new RegExp(`(^|[^A-Za-z0-9])${escapeRegExp(term)}([^A-Za-z0-9]|$)`);

function listFiles(directory, predicate, results = []) {
  if (!existsSync(directory)) return results;
  for (const entry of readdirSync(directory)) {
    const full = path.join(directory, entry);
    if (statSync(full).isDirectory()) listFiles(full, predicate, results);
    else if (predicate(full)) results.push(full);
  }
  return results;
}

function splitFrontmatter(text) {
  const match = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/.exec(text);
  return match ? { frontmatter: match[1], body: text.slice(match[0].length) } : { frontmatter: null, body: text };
}

function readHeader(body) {
  const first = body.split(/\r?\n/).find((line) => line.trim() !== '') ?? '';
  const levelMatch = /^> Level: (\d) (Core|Architecture|Technology|Project)\b/.exec(first);
  if (levelMatch) return { line: first, level: Number(levelMatch[1]), name: levelMatch[2] };
  if (/^> Level: meta\b/.test(first)) return { line: first, level: 'meta' };
  return { line: first, level: null };
}

export function checkInstructions(root) {
  const failures = [];
  const rel = (file) => path.relative(root, file).split(path.sep).join('/');
  const claudeDir = path.join(root, '.claude');
  const rulesDir = path.join(claudeDir, 'rules');
  const skillsDir = path.join(claudeDir, 'skills');
  const agentsDir = path.join(claudeDir, 'agents');
  const mapFile = path.join(claudeDir, 'INSTRUCTION-MAP.md');
  const claudeMd = path.join(root, 'CLAUDE.md');

  const artifacts = [];
  if (existsSync(claudeMd)) artifacts.push(claudeMd);
  else failures.push('CLAUDE.md is missing');
  const ruleFiles = listFiles(rulesDir, (file) => file.endsWith('.md'));
  const skillFiles = listFiles(skillsDir, (file) => file.endsWith('.md'));
  const agentFiles = listFiles(agentsDir, (file) => file.endsWith('.md'));
  artifacts.push(...ruleFiles, ...skillFiles, ...agentFiles);
  if (existsSync(mapFile)) artifacts.push(mapFile);
  else failures.push('.claude/INSTRUCTION-MAP.md is missing');

  // Rule basename -> level, for bare-name references.
  const ruleLevelByName = new Map();
  const levelCounts = [0, 0, 0, 0];
  for (const file of ruleFiles) {
    const parts = rel(file).split('/');
    const levelDir = parts[2];
    if (parts.length !== 4 || !(levelDir in LEVEL_DIRS)) {
      failures.push(`${rel(file)}: rule files live directly in one of ${Object.keys(LEVEL_DIRS).join(', ')}`);
      continue;
    }
    levelCounts[LEVEL_DIRS[levelDir]] += 1;
    ruleLevelByName.set(path.basename(file), LEVEL_DIRS[levelDir]);
  }
  levelCounts.forEach((count, level) => {
    if (count < 2) failures.push(`.claude/rules/${Object.keys(LEVEL_DIRS)[level]}: a level holds cohesive modules, not a single file (found ${count})`);
  });

  const mapText = existsSync(mapFile) ? readFileSync(mapFile, 'utf8') : '';
  const knownBasenames = new Set([...ruleLevelByName.keys(), ...skillFiles.map((file) => path.basename(file))]);

  for (const file of artifacts) {
    const name = rel(file);
    const text = readFileSync(file, 'utf8');
    const { frontmatter, body } = splitFrontmatter(text);
    const header = readHeader(body);
    const isMap = file === mapFile;

    if (header.level === null) {
      failures.push(`${name}: first body line must be the classification header "> Level: <n> <Name> · Owns: … · Scope: … · Loads: …"`);
    } else if (header.level !== 'meta' && LEVEL_NAMES[header.level] !== header.name) {
      failures.push(`${name}: level number and name disagree in the header`);
    }
    if (header.level === 'meta' && !isMap) failures.push(`${name}: only the instruction map may use "Level: meta"`);
    if (/\bKind:/.test(text)) failures.push(`${name}: "Kind:" classification is not part of this instruction system`);

    if (name.startsWith('.claude/rules/')) {
      const expected = LEVEL_DIRS[name.split('/')[2]];
      if (header.level !== null && header.level !== expected) failures.push(`${name}: header level ${header.level} does not match its directory (level ${expected})`);
      if (!frontmatter || !/^paths:\s*\r?\n(\s+-\s+\S.*\r?\n?)+/m.test(frontmatter)) failures.push(`${name}: rule files must declare a non-empty "paths:" list`);
    }

    const level = typeof header.level === 'number' ? header.level : null;

    // Technology neutrality for Levels 0 and 1 (body only; frontmatter globs are loading metadata).
    if (level !== null && level <= 1) {
      for (const term of CONCRETE_TECHNOLOGY_TERMS) {
        if (termPattern(term).test(body)) failures.push(`${name}: Level ${level} names concrete technology "${term}"`);
      }
    }

    // Dependency direction: references point to the same or a more stable level.
    if (level !== null && !isMap) {
      for (const line of body.split(/\r?\n/)) {
        if (name === 'CLAUDE.md' && line.startsWith('@')) continue; // imports are loading edges
        for (const match of line.matchAll(/\.claude\/rules\/(\d)-[a-z-]+\/[A-Za-z0-9-]+\.md/g)) {
          if (Number(match[1]) > level) failures.push(`${name}: Level ${level} references more volatile ${match[0]}`);
        }
        for (const match of line.matchAll(/`([a-z0-9-]+\.md)`/g)) {
          const target = ruleLevelByName.get(match[1]);
          if (target !== undefined && target > level) failures.push(`${name}: Level ${level} references more volatile rule ${match[1]}`);
        }
      }
    }

    // References resolve.
    for (const match of body.matchAll(/`?(\.claude\/[A-Za-z0-9_./-]+\.(md|mjs|json))`?/g)) {
      if (!existsSync(path.join(root, match[1]))) failures.push(`${name}: broken reference ${match[1]}`);
    }
    if (name === 'CLAUDE.md') {
      for (const match of body.matchAll(/^@(\S+)/gm)) {
        if (!existsSync(path.join(root, match[1]))) failures.push(`CLAUDE.md: import does not resolve: ${match[1]}`);
      }
    }
    for (const match of body.matchAll(/`([a-z0-9-]+\.md)`/g)) {
      const basename = match[1];
      if (!knownBasenames.has(basename) && !existsSync(path.join(path.dirname(file), basename)) &&
          !existsSync(path.join(path.dirname(file), 'references', basename))) {
        failures.push(`${name}: reference to unknown file ${basename}`);
      }
    }

    // Skill-private references are used only by their owning skill.
    if (!isMap) {
      for (const match of body.matchAll(/references\/([A-Za-z0-9-]+\.md)/g)) {
        const owningDir = name.startsWith('.claude/skills/') ? name.split('/').slice(0, 3).join('/') : null;
        const local = owningDir && existsSync(path.join(root, owningDir, 'references', match[1]));
        if (!local) failures.push(`${name}: depends on another skill's private reference ${match[0]}`);
      }
    }

    if (mapText && !isMap && !mapText.includes(name)) failures.push(`${name}: not listed in .claude/INSTRUCTION-MAP.md`);
  }

  // Skills.
  for (const skill of REQUIRED_SKILLS) {
    if (!existsSync(path.join(skillsDir, skill, 'SKILL.md'))) failures.push(`.claude/skills/${skill}/SKILL.md is missing`);
  }
  for (const skill of COMPETING_SKILLS) {
    if (existsSync(path.join(skillsDir, skill))) failures.push(`.claude/skills/${skill}: competes with the owning knowledge skill; keep it as a private reference`);
  }
  for (const file of skillFiles.filter((file) => path.basename(file) === 'SKILL.md')) {
    const directory = path.basename(path.dirname(file));
    const { frontmatter } = splitFrontmatter(readFileSync(file, 'utf8'));
    if (!frontmatter || !new RegExp(`^name:\\s*${escapeRegExp(directory)}\\s*$`, 'm').test(frontmatter)) failures.push(`${rel(file)}: "name" must equal the directory name`);
    if (!frontmatter || !/^description:/m.test(frontmatter)) failures.push(`${rel(file)}: "description" is required`);
    const userOnly = Boolean(frontmatter && /^disable-model-invocation:\s*true\s*$/m.test(frontmatter));
    if (USER_ONLY_SKILLS.includes(directory) !== userOnly) failures.push(`${rel(file)}: disable-model-invocation must be ${USER_ONLY_SKILLS.includes(directory)}`);
  }

  // Reviewer agent stays thin and read-only.
  const reviewer = path.join(agentsDir, 'code-reviewer.md');
  if (!existsSync(reviewer)) failures.push('.claude/agents/code-reviewer.md is missing');
  else {
    const reviewerText = readFileSync(reviewer, 'utf8');
    if (!/disallowedTools:.*\bWrite\b.*\bEdit\b/.test(reviewerText)) failures.push('.claude/agents/code-reviewer.md: must disallow Write and Edit');
    if (!/code-review/.test(reviewerText)) failures.push('.claude/agents/code-reviewer.md: must delegate to the code-review workflow');
  }

  return { failures, artifacts: artifacts.length };
}

const invokedDirectly = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (invokedDirectly) {
  const rootIndex = process.argv.indexOf('--root');
  const root = path.resolve(rootIndex > -1 ? process.argv[rootIndex + 1] : process.env.CLAUDE_PROJECT_DIR || process.cwd());
  const { failures, artifacts } = checkInstructions(root);
  for (const failure of failures) console.log(`FAIL ${failure}`);
  console.log(`Instruction check: ${failures.length === 0 ? 'PASS' : 'FAIL'} (${artifacts} artifacts, ${failures.length} failures)`);
  process.exit(failures.length === 0 ? 0 : 1);
}
