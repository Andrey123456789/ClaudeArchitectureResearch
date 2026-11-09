#!/usr/bin/env node
// Owns: structural validation of this instruction system (flat topical rules,
// one-line ownership headers, explicit rule paths, required workflow/knowledge
// skills, private-reference ownership, resolvable imports and references,
// complete MAP, existing hook scripts).
// Scope: repo/meta. Loads: run manually and by the template-maintenance workflow.
//
// Usage: node .claude/scripts/check-instructions.mjs [repoRoot]

import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, relative, dirname, basename, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(process.argv[2] ?? join(dirname(fileURLToPath(import.meta.url)), '..', '..'));
const errors = [];
const err = (file, msg) => errors.push(`${file}: ${msg}`);
const rel = (p) => relative(root, p).replace(/\\/g, '/');
const read = (p) => readFileSync(join(root, p), 'utf8');

const WORKFLOWS = ['project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings', 'git-workflow',
  'security-scan', 'add-dependency', 'architecture-decision', 'template-maintenance'];
const KNOWLEDGE = ['ef-core', 'http-api', 'aspnet-error-handling', 'dotnet-testing', 'logging', 'httpclient-factory',
  'configuration', 'dependency-injection', 'caching', 'swagger', 'api-versioning', 'health-check', 'docker', 'ci-cd',
  'angular', 'modern-csharp', 'authentication'];
const FORBIDDEN_SKILLS = ['serilog', 'resilience'];
const HEADER = /^> Owns: .+ \| Scope: .+ \| Loads: .+$/;

function walk(dir, out = []) {
  if (!existsSync(dir)) return out;
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) walk(full, out);
    else out.push(full);
  }
  return out;
}

function splitFrontmatter(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  return m ? { fm: m[1], body: text.slice(m[0].length) } : { fm: null, body: text };
}

// ---- Collect instruction artifacts -------------------------------------------------
const artifacts = ['CLAUDE.md', 'docs/technology-stack.md', '.claude/MAP.md'];
const rulesDir = join(root, '.claude/rules');
const skillsDir = join(root, '.claude/skills');
const agentsDir = join(root, '.claude/agents');
for (const f of walk(rulesDir)) artifacts.push(rel(f));
for (const f of walk(skillsDir)) if (f.endsWith('.md')) artifacts.push(rel(f));
for (const f of walk(agentsDir)) artifacts.push(rel(f));

for (const a of artifacts) if (!existsSync(join(root, a))) err(a, 'missing');

// ---- Flat rules with explicit paths ------------------------------------------------
if (existsSync(rulesDir)) {
  for (const entry of readdirSync(rulesDir)) {
    if (statSync(join(rulesDir, entry)).isDirectory()) err(`.claude/rules/${entry}`, 'rules directory must stay flat');
  }
  for (const f of walk(rulesDir)) {
    const { fm } = splitFrontmatter(readFileSync(f, 'utf8'));
    if (!fm || !/^paths:\s*\r?\n(\s+-\s*\S.*\r?\n?)+/m.test(fm)) err(rel(f), 'rule must declare non-empty frontmatter paths');
  }
}

// ---- Headers and forbidden classification fields --------------------------------------
for (const a of artifacts.filter((p) => existsSync(join(root, p)))) {
  const { fm, body } = splitFrontmatter(read(a));
  const first = body.split(/\r?\n/).find((l) => l.trim() !== '') ?? '';
  if (!HEADER.test(first)) err(a, 'first line after frontmatter must be "> Owns: ... | Scope: ... | Loads: ..."');
  if (/^\s*(Level|Kind)\s*:/m.test((fm ?? '') + '\n' + first)) err(a, 'Level:/Kind: classification is not used in this template');
}

// ---- CLAUDE.md imports ------------------------------------------------------------------
const claude = existsSync(join(root, 'CLAUDE.md')) ? read('CLAUDE.md') : '';
if (!/^@docs\/technology-stack\.md\s*$/m.test(claude)) err('CLAUDE.md', 'must import @docs/technology-stack.md');
for (const m of claude.matchAll(/^@(\S+)\s*$/gm)) if (!existsSync(join(root, m[1]))) err('CLAUDE.md', `import @${m[1]} does not resolve`);

// ---- Skills -------------------------------------------------------------------------------
const skillNames = existsSync(skillsDir) ? readdirSync(skillsDir).filter((d) => statSync(join(skillsDir, d)).isDirectory()) : [];
for (const name of [...WORKFLOWS, ...KNOWLEDGE]) if (!skillNames.includes(name)) err(`.claude/skills/${name}`, 'required skill missing');
for (const name of FORBIDDEN_SKILLS) if (skillNames.includes(name)) err(`.claude/skills/${name}`, 'must be a private reference, not a standalone skill');
for (const name of skillNames) {
  const p = `.claude/skills/${name}/SKILL.md`;
  if (!existsSync(join(root, p))) { err(p, 'missing'); continue; }
  const { fm } = splitFrontmatter(read(p));
  if (!fm) { err(p, 'missing frontmatter'); continue; }
  if (!new RegExp(`^name:\\s*${name}\\s*$`, 'm').test(fm)) err(p, 'frontmatter name must match the directory');
  if (!/^description:/m.test(fm)) err(p, 'missing description');
  const userOnly = /^disable-model-invocation:\s*true\s*$/m.test(fm);
  if (name === 'template-maintenance' && !userOnly) err(p, 'must set disable-model-invocation: true');
}

// ---- Agent -------------------------------------------------------------------------------
const agentPath = '.claude/agents/code-reviewer.md';
if (existsSync(join(root, agentPath))) {
  const { fm } = splitFrontmatter(read(agentPath));
  if (!/^\s*-\s*code-review\s*$/m.test(fm ?? '')) err(agentPath, 'must preload the code-review skill');
  if (!/disallowedTools:.*\bWrite\b.*\bEdit\b/.test(fm ?? '')) err(agentPath, 'must be read-only (disallow Write and Edit)');
} else err(agentPath, 'missing');

// ---- Private references ------------------------------------------------------------------
const privateRefs = walk(skillsDir).filter((f) => /[\\/]references[\\/]/.test(f)).map(rel);
for (const ref of privateRefs) {
  const owner = ref.split('/').slice(0, 3).join('/') + '/';
  const token = `references/${basename(ref)}`;
  for (const a of artifacts) {
    if (a === '.claude/MAP.md' || a.startsWith(owner) || !existsSync(join(root, a))) continue;
    if (read(a).includes(token)) err(a, `refers to ${ref}, which is private to ${owner}`);
  }
}

// ---- Backticked path references resolve ---------------------------------------------------
const ruleNames = existsSync(rulesDir) ? readdirSync(rulesDir) : [];
const rootDocs = ['CLAUDE.md', 'SPECIFICATION.md', 'CUSTOM_SETTINGS.md', 'SKILL.md', 'README.md'];
for (const a of artifacts.filter((p) => existsSync(join(root, p)))) {
  const text = read(a);
  for (const m of text.matchAll(/`([^`\s]+)`/g)) {
    const token = m[1].replace(/[),.;:]+$/, '');
    if (/[<>*{}$]|NNNN/.test(token)) continue;
    if (/^(\.claude|docs)\//.test(token)) {
      if (token.endsWith('/') ? !existsSync(join(root, token)) && !token.startsWith('docs/decisions') : !existsSync(join(root, token))) {
        err(a, `reference ${token} does not resolve`);
      }
    } else if (/^references\/[\w.-]+\.md$/.test(token)) {
      if (!existsSync(join(root, dirname(a), token))) err(a, `reference ${token} does not resolve`);
    } else if (/^[\w.-]+\.md$/.test(token) && !rootDocs.includes(token) && !ruleNames.includes(token)) {
      err(a, `reference ${token} does not resolve to a rule or root document`);
    }
  }
}

// ---- Settings hooks ---------------------------------------------------------------------------
const settingsPath = '.claude/settings.json';
let settingsText = '';
if (existsSync(join(root, settingsPath))) {
  settingsText = read(settingsPath);
  try { JSON.parse(settingsText); } catch (e) { err(settingsPath, `invalid JSON: ${e.message}`); }
  for (const m of settingsText.matchAll(/\.claude\/hooks\/[\w.-]+/g)) if (!existsSync(join(root, m[0]))) err(settingsPath, `${m[0]} does not exist`);
} else err(settingsPath, 'missing');

// ---- MAP completeness ----------------------------------------------------------------------------
const enforcement = [settingsPath, '.editorconfig', 'Directory.Build.props', 'Directory.Packages.props',
  ...walk(join(root, '.claude/hooks')).map(rel), ...walk(join(root, '.claude/scripts')).map(rel)];
if (existsSync(join(root, '.claude/MAP.md'))) {
  const map = read('.claude/MAP.md');
  for (const a of [...artifacts, ...enforcement, 'SPECIFICATION.md', 'CUSTOM_SETTINGS.md']) {
    if (a !== '.claude/MAP.md' && !map.includes(a)) err('.claude/MAP.md', `does not list ${a}`);
  }
}

// ---- Always-loaded surface estimate ---------------------------------------------------------------
const descriptions = skillNames
  .map((n) => join(skillsDir, n, 'SKILL.md'))
  .filter(existsSync)
  .map((f) => (splitFrontmatter(readFileSync(f, 'utf8')).fm ?? '').match(/description:([\s\S]*?)(\n\S|$)/)?.[1] ?? '')
  .join('');
const alwaysChars = claude.length + (existsSync(join(root, 'docs/technology-stack.md')) ? read('docs/technology-stack.md').length : 0) + descriptions.length;
console.log(`Always-loaded estimate: ~${Math.round(alwaysChars / 4)} tokens (CLAUDE.md + technology-stack.md + skill descriptions)`);

if (errors.length) {
  console.log(`Instruction check: ${errors.length} problem(s)\n- ${errors.join('\n- ')}`);
  process.exit(1);
}
console.log(`Instruction check: PASS (${artifacts.length} instruction files)`);
