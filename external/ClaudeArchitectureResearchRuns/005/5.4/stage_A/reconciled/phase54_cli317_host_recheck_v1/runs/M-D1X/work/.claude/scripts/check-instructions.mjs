#!/usr/bin/env node
// Instruction-structure checker for this repository's Claude instruction system.
//
// Usage (any OS, Node.js 18+), from the repository root (the top level of the
// current checkout or worktree; `git rev-parse --show-toplevel` prints it):
//   node .claude/scripts/check-instructions.mjs
// The instruction system checked is that of the active root resolved from the
// current directory (repo-root.mjs).
// Exit codes: 0 = all checks pass, 1 = failures, 2 = the checker could not run.
//
// Checks: required files; CLAUDE.md imports only docs/technology-stack.md;
// one-line "> Owns: ... | Scope: ... | Loads: ..." header on every instruction
// file; flat .claude/rules/ with non-empty `paths`; no Level:/Kind:
// classification lines; skill folder shape and frontmatter; required workflow
// and knowledge skills; user-only template-maintenance; thin read-only
// code-reviewer agent; private references used only by their owning skill;
// file, section (§), and skill references resolve; MAP.md lists every
// instruction file; the required hook registrations (REQUIRED_HOOKS) in exec
// form (no shell command strings), each handled by its script, with a
// fail-closed PreToolUse guard and fail-open advisory hooks; always-loaded
// size estimate.

import { readFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join, dirname, relative, sep } from 'node:path';
import { resolveActiveRoot } from './repo-root.mjs';

const REQUIRED_FILES = [
  'CLAUDE.md', 'docs/technology-stack.md', '.claude/MAP.md', '.claude/settings.json',
  '.claude/agents/code-reviewer.md', 'SPECIFICATION.md', 'CUSTOM_SETTINGS.md',
];
const WORKFLOW_SKILLS = [
  'development-workflow', 'project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings',
  'git-workflow', 'security-scan', 'add-dependency', 'architecture-decision', 'template-maintenance',
];
const KNOWLEDGE_SKILLS = [
  'ef-core', 'http-api', 'aspnet-error-handling', 'dotnet-testing', 'logging', 'httpclient-factory',
  'configuration', 'dependency-injection', 'caching', 'swagger', 'api-versioning', 'health-check',
  'docker', 'ci-cd', 'angular', 'modern-csharp', 'authentication',
];
const FORBIDDEN_SKILLS = ['serilog', 'resilience'];
const ALLOWED_IMPORTS = ['docs/technology-stack.md'];
const HEADER = /^> Owns: .+ \| Scope: .+ \| Loads: .+$/;
const BUDGET_WARN_TOKENS = 6000;
// Hook registrations the enforcement depends on: [event, tools the matcher must
// cover, script]. The dependency guard also runs after a failed shell call
// (PostToolUseFailure), which can leave changed manifests behind.
const REQUIRED_HOOKS = [
  ['PreToolUse', ['Bash', 'PowerShell'], 'dependency-guard.mjs'],
  ['PostToolUse', ['Bash', 'PowerShell'], 'dependency-guard.mjs'],
  ['PostToolUseFailure', ['Bash', 'PowerShell'], 'dependency-guard.mjs'],
  ['PostToolUse', ['Edit', 'Write', 'MultiEdit'], 'file-change.mjs'],
  ['Stop', [], 'stop-co-change.mjs'],
];

const failures = [];
const warnings = [];
const info = [];
const fail = (message) => failures.push(message);

const root = locateRoot();
const rel = (absolute) => relative(root, absolute).split(sep).join('/');
const abs = (relPath) => join(root, ...relPath.split('/'));
const read = (relPath) => readFileSync(abs(relPath), 'utf8');

// ---------------------------------------------------------------- file discovery
for (const file of REQUIRED_FILES) if (!existsSync(abs(file))) fail(`missing required file ${file}`);

const ruleFiles = listDir('.claude/rules');
const skillDirs = listDir('.claude/skills');
const agentFiles = listDir('.claude/agents');
const skillNames = skillDirs.filter((d) => statSync(abs(`.claude/skills/${d}`)).isDirectory());
const agentNames = agentFiles.filter((f) => f.endsWith('.md')).map((f) => f.replace(/\.md$/, ''));

const isMarkdownFile = (relPath) => relPath.endsWith('.md') && statSync(abs(relPath)).isFile();
const instructionFiles = ['CLAUDE.md', 'docs/technology-stack.md', '.claude/MAP.md'];
for (const f of ruleFiles) if (isMarkdownFile(`.claude/rules/${f}`)) instructionFiles.push(`.claude/rules/${f}`);
for (const f of agentFiles) {
  if (isMarkdownFile(`.claude/agents/${f}`)) instructionFiles.push(`.claude/agents/${f}`);
  else fail(`.claude/agents/${f}: agents are single Markdown files`);
}
const privateRefs = new Map(); // "skill/file.md" -> owner skill
for (const skill of skillNames) {
  const dir = `.claude/skills/${skill}`;
  for (const entry of listDir(dir)) {
    if (entry === 'SKILL.md') {
      instructionFiles.push(`${dir}/SKILL.md`);
    } else if (entry === 'references' && statSync(abs(`${dir}/references`)).isDirectory()) {
      for (const ref of listDir(`${dir}/references`)) {
        if (!isMarkdownFile(`${dir}/references/${ref}`)) {
          fail(`${dir}/references/${ref}: only Markdown files are allowed in references/`);
          continue;
        }
        instructionFiles.push(`${dir}/references/${ref}`);
        privateRefs.set(`${skill}/${ref}`, skill);
      }
    } else {
      fail(`${dir}/${entry}: unexpected entry (a skill folder holds SKILL.md and optional references/)`);
    }
  }
  if (!listDir(dir).includes('SKILL.md')) fail(`${dir}: missing SKILL.md`);
}
const existingInstructionFiles = instructionFiles.filter((f) => existsSync(abs(f)));

// ---------------------------------------------------------------- imports
const claude = existsSync(abs('CLAUDE.md')) ? read('CLAUDE.md') : '';
const imports = importsOf(claude);
for (const imp of imports) {
  if (!ALLOWED_IMPORTS.includes(imp)) fail(`CLAUDE.md imports ${imp}; only ${ALLOWED_IMPORTS.join(', ')} may be imported`);
  if (!existsSync(abs(imp))) fail(`CLAUDE.md import does not resolve: ${imp}`);
}
for (const required of ALLOWED_IMPORTS) if (!imports.includes(required)) fail(`CLAUDE.md must import ${required}`);
for (const file of existingInstructionFiles.filter((f) => f !== 'CLAUDE.md')) {
  if (importsOf(read(file)).length > 0) fail(`${file}: contains an @ import; only CLAUDE.md imports`);
}

// ---------------------------------------------------------------- headers and leakage
for (const file of existingInstructionFiles) {
  const { body } = splitFrontmatter(read(file));
  const firstLine = body.split(/\r?\n/).find((line) => line.trim() !== '') ?? '';
  if (!HEADER.test(firstLine.trim())) {
    fail(`${file}: first line after frontmatter must be "> Owns: ... | Scope: ... | Loads: ..."`);
  } else {
    const loads = firstLine.split('| Loads:')[1].toLowerCase();
    if (file.startsWith('.claude/rules/') && !loads.includes('path-scoped')) fail(`${file}: header must say Loads: path-scoped`);
    if (file.includes('/references/') && !loads.includes('private reference')) fail(`${file}: header must say Loads: private reference`);
    if (KNOWLEDGE_SKILLS.some((k) => file === `.claude/skills/${k}/SKILL.md`) && !loads.includes('on demand')) {
      fail(`${file}: knowledge skill header must say Loads: on demand`);
    }
    if (WORKFLOW_SKILLS.some((w) => file === `.claude/skills/${w}/SKILL.md`) && !/workflow|user-invoked/.test(loads)) {
      fail(`${file}: workflow skill header must say Loads: workflow (or user-invoked)`);
    }
  }
  for (const line of read(file).split(/\r?\n/)) {
    if (/^\s*(\*\*)?(Level|Kind)(\*\*)?\s*:/.test(line)) fail(`${file}: classification line "${line.trim()}" is not part of this instruction system`);
  }
}

// ---------------------------------------------------------------- rules
for (const entry of ruleFiles) {
  const path = `.claude/rules/${entry}`;
  if (statSync(abs(path)).isDirectory()) {
    fail(`${path}: .claude/rules/ must stay flat (no subdirectories)`);
    continue;
  }
  if (!entry.endsWith('.md')) {
    fail(`${path}: rule files must be Markdown`);
    continue;
  }
  const { data } = splitFrontmatter(read(path));
  const paths = data.paths;
  if (!Array.isArray(paths) || paths.length === 0 || paths.some((p) => typeof p !== 'string' || p.trim() === '')) {
    fail(`${path}: frontmatter must declare a non-empty "paths" list`);
  }
}

// ---------------------------------------------------------------- skills
for (const required of [...WORKFLOW_SKILLS, ...KNOWLEDGE_SKILLS]) {
  if (!skillNames.includes(required)) fail(`missing required skill .claude/skills/${required}`);
}
for (const forbidden of FORBIDDEN_SKILLS) {
  if (skillNames.includes(forbidden)) fail(`.claude/skills/${forbidden} competes with an existing knowledge skill; keep that depth as a private reference`);
}
const descriptions = [];
for (const skill of skillNames) {
  const path = `.claude/skills/${skill}/SKILL.md`;
  if (!existsSync(abs(path))) continue;
  const { data } = splitFrontmatter(read(path));
  if (data.name !== skill) fail(`${path}: frontmatter name "${data.name}" must equal the folder name`);
  const description = typeof data.description === 'string' ? data.description.trim() : '';
  if (!description) fail(`${path}: missing description`);
  if (description.length > 1024) fail(`${path}: description longer than 1024 characters`);
  const userOnly = String(data['disable-model-invocation']) === 'true';
  if (skill === 'template-maintenance' && !userOnly) fail(`${path}: must set disable-model-invocation: true (user-only workflow)`);
  if (KNOWLEDGE_SKILLS.includes(skill) && !/^Use when\b/.test(description)) {
    fail(`${path}: knowledge-skill description must start with a concrete trigger ("Use when ...")`);
  }
  if (!userOnly) descriptions.push(description);
}

// ---------------------------------------------------------------- agent
const agentPath = '.claude/agents/code-reviewer.md';
if (existsSync(abs(agentPath))) {
  const { data, body } = splitFrontmatter(read(agentPath));
  const disallowed = String(data.disallowedTools ?? '').split(/[,\s]+/);
  if (!disallowed.includes('Write') || !disallowed.includes('Edit')) fail(`${agentPath}: must disallow Write and Edit (read-only reviewer)`);
  if (!body.includes('`code-review`')) fail(`${agentPath}: must delegate to the code-review skill`);
  if (body.length > 1500) fail(`${agentPath}: agent body should stay a thin wrapper (<= 1500 characters)`);
  if (data.description) descriptions.push(String(data.description));
}

// ---------------------------------------------------------------- references
const headingsCache = new Map();
for (const file of existingInstructionFiles) {
  const text = stripFences(read(file));
  const ownerSkill = file.startsWith('.claude/skills/') ? file.split('/')[2] : null;

  // private references
  for (const m of text.matchAll(/skills\/([a-z0-9-]+)\/references\/([A-Za-z0-9_.-]+\.md)/g)) {
    if (file !== '.claude/MAP.md' && m[1] !== ownerSkill) fail(`${file}: references private reference ${m[0]} owned by ${m[1]}`);
  }
  for (const m of text.matchAll(/(?<![\w/])references\/([A-Za-z0-9_.-]+\.md)/g)) {
    if (file === '.claude/MAP.md') continue;
    if (!ownerSkill) {
      fail(`${file}: mentions references/${m[1]} but private references belong to their owning skill`);
    } else if (!privateRefs.has(`${ownerSkill}/${m[1]}`)) {
      fail(`${file}: references/${m[1]} does not exist in .claude/skills/${ownerSkill}/references/`);
    }
  }

  // backticked file paths
  for (const m of text.matchAll(/`([^`\s]+)`/g)) {
    const token = m[1];
    if (/[<>*{}$]|NNNN/.test(token) || /^https?:/.test(token)) continue;
    const isRepoPath = /^(\.claude|docs)\//.test(token);
    const isBareMd = /^[A-Za-z0-9_.-]+\.md$/.test(token);
    if (!isRepoPath && !isBareMd) continue;
    if (token.startsWith('docs/decisions')) continue; // created with the first decision record
    if (!resolveFileRef(token, file)) fail(`${file}: reference \`${token}\` does not resolve`);
  }

  // section references: "<file>.md § Heading" or "`skill` § Heading"
  for (const m of text.matchAll(/§\s+([A-Z][^\n]{0,80}(?:\n[^\n]{0,80})?)/g)) {
    const before = text.slice(Math.max(0, m.index - 160), m.index);
    const target = lastTarget(before);
    if (!target) {
      fail(`${file}: section reference "§ ${m[1].slice(0, 40)}" has no preceding file or skill`);
      continue;
    }
    const targetFile = target.endsWith('.md') ? resolveFileRef(target, file) : `.claude/skills/${target}/SKILL.md`;
    if (!targetFile || !existsSync(abs(targetFile))) {
      fail(`${file}: section reference target ${target} does not resolve`);
      continue;
    }
    if (!matchesHeading(targetFile, m[1])) fail(`${file}: ${target} has no heading matching "§ ${m[1].slice(0, 50)}"`);
  }

  // skill and agent names used as routing targets
  const known = new Set([...skillNames, ...agentNames]);
  const patterns = [
    /`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`\s+(?:skill|workflow|agent)\b/g,
    /\b(?:[Rr]un|through|via|[Uu]se|[Ff]ollow|agent:|Technique:|→|->)\s+(?:the\s+)?`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`/g,
    /^\|[^|\n]*\|\s*`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`/gm,
  ];
  for (const pattern of patterns) {
    for (const m of text.matchAll(pattern)) {
      if (!known.has(m[1])) fail(`${file}: routes to unknown skill or agent \`${m[1]}\``);
    }
  }
}

// ---------------------------------------------------------------- map
if (existsSync(abs('.claude/MAP.md'))) {
  const map = read('.claude/MAP.md');
  const listed = [...existingInstructionFiles, '.claude/settings.json', ...listDir('.claude/hooks').map((f) => `.claude/hooks/${f}`),
    ...listDir('.claude/scripts').map((f) => `.claude/scripts/${f}`)];
  for (const file of listed) {
    if (file === '.claude/MAP.md') continue;
    if (!map.includes(file)) fail(`.claude/MAP.md does not list ${file}`);
  }
  if (importsOf(claude).some((imp) => imp.endsWith('MAP.md'))) fail('MAP.md must not be imported (it is human-facing only)');
}

// ---------------------------------------------------------------- hooks
if (existsSync(abs('.claude/settings.json'))) {
  let settings;
  try {
    settings = JSON.parse(read('.claude/settings.json'));
  } catch (error) {
    fail(`.claude/settings.json is not valid JSON: ${error.message}`);
  }
  // Project hooks must use exec form: "command": "node" plus one argument, the
  // script path anchored at ${CLAUDE_PROJECT_DIR}. Claude Code substitutes the
  // placeholder without a shell; for this static check it resolves to the root
  // being checked. Shell command strings ("node .claude/hooks/x.mjs", "$VAR",
  // "%VAR%") depend on the current directory or on one shell and are rejected.
  const hookArg = /^\$\{CLAUDE_PROJECT_DIR\}\/\.claude\/hooks\/([A-Za-z0-9_.-]+\.mjs)$/;
  const execForm = '"command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs"]';
  for (const [event, groups] of Object.entries(settings?.hooks ?? {})) {
    for (const group of Array.isArray(groups) ? groups : []) {
      for (const hook of group.hooks ?? []) {
        const where = `settings.json ${event}`;
        if (hook.type !== 'command') {
          fail(`${where}: hook type "${hook.type}" is not supported; use a command hook in exec form (${execForm})`);
          continue;
        }
        if (hook.command !== 'node' || !Array.isArray(hook.args)) {
          fail(`${where}: hook ${JSON.stringify(hook.command)} is not in exec form; use ${execForm}`);
          continue;
        }
        if (hook.args.length !== 1 || typeof hook.args[0] !== 'string') {
          fail(`${where}: exec-form hook must pass exactly one argument, the script path (${execForm})`);
          continue;
        }
        const m = hookArg.exec(hook.args[0]);
        if (!m) {
          fail(`${where}: hook argument "${hook.args[0]}" must be "\${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs"`);
        } else if (!existsSync(abs(`.claude/hooks/${m[1]}`))) {
          fail(`${where}: hook script .claude/hooks/${m[1]} does not exist`);
        } else {
          // A script that dispatches on the event name must handle each event it is registered for.
          const source = read(`.claude/hooks/${m[1]}`);
          if (/\.hook_event_name\b/.test(source) && !new RegExp(`===\\s*'${event}'`).test(source)) {
            fail(`${where}: .claude/hooks/${m[1]} reads hook_event_name but does not handle "${event}"`);
          }
        }
        // The PreToolUse policy guard fails closed: a guard that cannot start,
        // crashes, rejects its input, or times out must block the tool call.
        // Advisory PostToolUse(Failure)/Stop hooks must not (the event already happened,
        // and a blocking Stop failure could loop).
        if (event === 'PreToolUse' && hook.onFailure !== 'block') {
          fail(`${where}: the policy guard must set "onFailure": "block" so a failing or timed-out guard blocks the tool call`);
        } else if (event !== 'PreToolUse' && hook.onFailure === 'block') {
          fail(`${where}: advisory hook must not set "onFailure": "block" (the event already happened; a failing Stop hook could loop)`);
        }
      }
    }
  }
  for (const [event, tools, script] of REQUIRED_HOOKS) {
    const registered = (Array.isArray(settings?.hooks?.[event]) ? settings.hooks[event] : []).some((group) => {
      const matcher = typeof group?.matcher === 'string' && !['', '*'].includes(group.matcher) ? group.matcher.split('|') : null;
      return tools.every((tool) => !matcher || matcher.includes(tool)) &&
        (group.hooks ?? []).some((hook) => hook?.args?.[0] === `\${CLAUDE_PROJECT_DIR}/.claude/hooks/${script}`);
    });
    if (!registered) {
      fail(`settings.json ${event}: required hook .claude/hooks/${script}${tools.length > 0 ? ` for ${tools.join('|')}` : ''} is not registered`);
    }
  }
}

// ---------------------------------------------------------------- budget
const alwaysChars = claude.length + imports.filter((i) => existsSync(abs(i))).reduce((n, i) => n + read(i).length, 0);
const listingChars = descriptions.reduce((n, d) => n + d.length + 40, 0);
const estimate = Math.round((alwaysChars + listingChars) / 4);
info.push(`always-loaded estimate: ~${estimate} tokens (CLAUDE.md + imports ${alwaysChars} chars, skill/agent listing ${listingChars} chars)`);
if (estimate > BUDGET_WARN_TOKENS) warnings.push(`always-loaded estimate ~${estimate} tokens exceeds ~${BUDGET_WARN_TOKENS}; check for content that belongs in a rule, workflow, or skill`);

// ---------------------------------------------------------------- report
for (const line of info) process.stdout.write(`INFO  ${line}\n`);
for (const line of warnings) process.stdout.write(`WARN  ${line}\n`);
for (const line of failures) process.stdout.write(`FAIL  ${line}\n`);
process.stdout.write(`check-instructions: ${existingInstructionFiles.length} instruction file(s), ${failures.length} failure(s), ${warnings.length} warning(s)\n`);
process.exit(failures.length > 0 ? 1 : 0);

// ---------------------------------------------------------------- helpers
function locateRoot() {
  let candidate;
  try {
    candidate = resolveActiveRoot(process.cwd());
  } catch (error) {
    process.stderr.write(`check-instructions: ${error.message}. Run it from the repository root.\n`);
    process.exit(2);
  }
  if (!existsSync(join(candidate, '.claude'))) {
    process.stderr.write(`check-instructions: "${candidate}" has no .claude directory to check.\n`);
    process.exit(2);
  }
  return candidate;
}

function listDir(relPath) {
  try {
    return readdirSync(abs(relPath)).sort();
  } catch {
    return [];
  }
}

function stripFences(text) {
  return text.replace(/^(```|~~~)[^\n]*\n[\s\S]*?^\1[^\n]*$/gm, '');
}

function importsOf(text) {
  return stripFences(text)
    .split(/\r?\n/)
    .map((line) => /^@(\S+)\s*$/.exec(line.trim()))
    .filter(Boolean)
    .map((m) => m[1].replace(/^\.\//, ''));
}

function splitFrontmatter(text) {
  const m = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/.exec(text);
  if (!m) return { data: {}, body: text };
  return { data: parseYamlSubset(m[1]), body: text.slice(m[0].length) };
}

// Minimal YAML subset: scalars, quoted scalars, folded/literal blocks, string lists.
function parseYamlSubset(source) {
  const data = {};
  const lines = source.split(/\r?\n/);
  for (let i = 0; i < lines.length; i += 1) {
    const m = /^([A-Za-z][\w-]*):\s*(.*)$/.exec(lines[i]);
    if (!m) continue;
    const key = m[1];
    const value = m[2].trim();
    if (value === '>' || value === '|' || value === '>-' || value === '|-') {
      const block = [];
      while (i + 1 < lines.length && (/^\s+\S/.test(lines[i + 1]) || lines[i + 1].trim() === '')) block.push(lines[(i += 1)].trim());
      data[key] = value.startsWith('>') ? block.join(' ').replace(/\s+/g, ' ').trim() : block.join('\n');
    } else if (value === '') {
      const items = [];
      while (i + 1 < lines.length && /^\s*-\s+/.test(lines[i + 1])) items.push(unquote(lines[(i += 1)].replace(/^\s*-\s+/, '').trim()));
      data[key] = items;
    } else {
      data[key] = unquote(value);
    }
  }
  return data;
}

function unquote(value) {
  return value.replace(/^(['"])(.*)\1$/, '$2');
}

function resolveFileRef(token, fromFile) {
  const clean = token.replace(/\/$/, '');
  const candidates = [clean, `${dirname(fromFile)}/${clean}`];
  if (/^[A-Za-z0-9_.-]+\.md$/.test(clean)) {
    candidates.push(`.claude/rules/${clean}`, `.claude/${clean}`);
    if (fromFile.startsWith('.claude/skills/')) candidates.push(`${fromFile.split('/').slice(0, 3).join('/')}/references/${clean}`);
  }
  if (clean === 'README.md') return 'README.md'; // created at scaffolding time
  return candidates.find((c) => existsSync(abs(c))) ?? null;
}

function lastTarget(before) {
  const matches = [...before.matchAll(/([A-Za-z0-9_./-]+\.md)|`([a-z][a-z0-9]*(?:-[a-z0-9]+)+)`/g)];
  if (matches.length === 0) return null;
  const last = matches[matches.length - 1];
  return last[1] ?? last[2];
}

function headingsOf(file) {
  if (!headingsCache.has(file)) {
    const headings = stripFences(read(file))
      .split(/\r?\n/)
      .filter((line) => /^#{1,6}\s/.test(line))
      .map((line) => normalizeHeading(line.replace(/^#{1,6}\s+/, '')));
    headingsCache.set(file, headings);
  }
  return headingsCache.get(file);
}

function normalizeHeading(text) {
  return text.replace(/^\d+\.\s+/, '').replace(/[`*]/g, '').trim().toLowerCase();
}

function matchesHeading(file, following) {
  const words = following.replace(/[`*]/g, '').split(/\s+/);
  const headings = headingsOf(file);
  for (let n = Math.min(words.length, 8); n >= 1; n -= 1) {
    const candidate = normalizeHeading(words.slice(0, n).join(' ').replace(/[.,;:!?)\]—]+$/, ''));
    if (headings.includes(candidate)) return true;
  }
  return false;
}
