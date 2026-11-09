// Kind: ENF | Scope: repo/meta | Owns: instruction-structure checker (Kind x Scope placement, headers, paths, references, decision register, hooks, budget) | Loads: CLI (node .claude/scripts/check-instructions.mjs [root]) and post-edit hook
//
// Structural predicates of this instruction system:
// - every instruction file starts (after frontmatter) with "<!-- Kind: K | Scope: S | Owns: ... | Loads: ... -->"
// - Kind determines location and mechanism: OP = CLAUDE.md, DEC = decision register (+ ADRs),
//   STD = .claude/rules/<scope>/*.md with paths:, WF/KNW = .claude/skills/<name>/SKILL.md, WF agents
// - standards: scope directory matches header, canonical paths present, no numbered procedures,
//   skill mentions only on Technique:/Workflow: lines, DEC IDs cited instead of restated
// - knowledge skills hold no "must" statements; skill-private references are used only by their skill
// - decision rows exist only in the register; Details in / Affects targets exist; MAP Affects list matches
// - every @import, path, section and skill reference resolves; hook commands are shell-neutral
// - no Level: headers, ordered rule directories, standalone serilog/resilience skills

import { existsSync, readdirSync, readFileSync, statSync } from 'node:fs';
import path from 'node:path';

const KINDS = ['OP', 'DEC', 'STD', 'KNW', 'WF', 'ENF', 'IN'];
const SCOPES = ['common', 'backend', 'backend-tests', 'frontend', 'delivery', 'repo/meta'];
const RULE_SCOPE_DIRS = ['common', 'backend', 'backend-tests', 'frontend', 'delivery'];
export const SCOPE_GLOBS = {
  common: ['backend/**', 'frontend/**', '*.slnx', '*.props', 'global.json', '**/*.yml', '**/*.yaml', '**/Dockerfile*', '**/.env*'],
  backend: ['backend/**'],
  'backend-tests': ['backend/**/*Tests/**'],
  frontend: ['frontend/**'],
  delivery: ['**/Dockerfile*', '**/*.yml', '**/*.yaml', '**/.dockerignore'],
};
const REQUIRED_WORKFLOWS = ['project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings', 'git-workflow',
  'security-scan', 'add-dependency', 'architecture-decision', 'template-maintenance'];
const USER_ONLY_WORKFLOWS = ['template-maintenance'];
const REQUIRED_KNOWLEDGE = ['ef-core', 'http-api', 'aspnet-error-handling', 'dotnet-testing', 'logging', 'httpclient-factory',
  'configuration', 'dependency-injection', 'caching', 'swagger', 'api-versioning', 'health-check', 'docker', 'ci-cd',
  'angular', 'modern-csharp', 'authentication'];
const FORBIDDEN_SKILLS = ['serilog', 'resilience'];
const REGISTER = 'docs/architecture/decision-register.md';
const MAP = '.claude/MAP.md';
const HEADER = /^<!-- Kind: ([^|]+?) \| Scope: ([^|]+?) \| Owns: ([^|]+?) \| Loads: (.+?) -->$/;
const DEC_ID = /\bDEC-[A-Z]+-\d{2}\b/g;
const BUDGET_TARGET_TOKENS = 5000;

const posix = (p) => p.split(path.sep).join('/');

function listFiles(root, dir, predicate, found = []) {
  const full = path.join(root, dir);
  if (!existsSync(full)) return found;
  for (const entry of readdirSync(full, { withFileTypes: true })) {
    const relative = dir ? `${dir}/${entry.name}` : entry.name;
    if (entry.isDirectory()) listFiles(root, relative, predicate, found);
    else if (predicate(relative)) found.push(relative);
  }
  return found;
}

function splitFrontmatter(text) {
  const normalized = text.replace(/\r\n/g, '\n');
  if (!normalized.startsWith('---\n')) return { frontmatter: null, body: normalized };
  const end = normalized.indexOf('\n---\n', 4);
  if (end < 0) return { frontmatter: null, body: normalized, broken: true };
  return { frontmatter: normalized.slice(4, end), body: normalized.slice(end + 5) };
}

function frontmatterValue(frontmatter, key) {
  const match = frontmatter?.match(new RegExp(`^${key}:\\s*(.*)$`, 'm'));
  return match ? match[1].trim() : null;
}

function frontmatterList(frontmatter, key) {
  if (!frontmatter) return null;
  const lines = frontmatter.split('\n');
  const start = lines.findIndex((line) => line.startsWith(`${key}:`));
  if (start < 0) return null;
  const inline = lines[start].slice(key.length + 1).trim();
  if (inline.startsWith('[')) return inline.slice(1, -1).split(',').map((v) => v.trim().replace(/^["']|["']$/g, '')).filter(Boolean);
  const values = [];
  for (const line of lines.slice(start + 1)) {
    const item = line.match(/^\s+-\s+(.*)$/);
    if (!item) break;
    values.push(item[1].trim().replace(/^["']|["']$/g, ''));
  }
  return values;
}

function frontmatterDescription(frontmatter) {
  const lines = frontmatter?.split('\n') ?? [];
  const start = lines.findIndex((line) => line.startsWith('description:'));
  if (start < 0) return null;
  const inline = lines[start].slice('description:'.length).trim();
  if (inline && inline !== '>' && inline !== '|') return inline;
  const parts = [];
  for (const line of lines.slice(start + 1)) {
    if (!/^\s+/.test(line)) break;
    parts.push(line.trim());
  }
  return parts.join(' ');
}

// Text outside fenced code blocks and indented example blocks.
function prose(text) {
  const out = [];
  let fenced = false;
  for (const line of text.split('\n')) {
    if (/^\s*```/.test(line)) { fenced = !fenced; continue; }
    if (fenced || /^( {4}|\t)/.test(line)) continue;
    out.push(line);
  }
  return out.join('\n');
}

function headings(text) {
  return prose(text).split('\n').filter((l) => /^#{1,6} /.test(l)).map((l) => l.replace(/^#{1,6} /, '').trim());
}

function hasHeading(text, wanted) {
  const target = wanted.trim().toLowerCase();
  return headings(text).some((h) => {
    const lower = h.toLowerCase();
    if (/^\d+$/.test(target)) return lower.startsWith(`${target}.`) || lower === target;
    return lower === target || lower.startsWith(`${target} `) || lower.replace(/^\d+\.\s*/, '') === target;
  });
}

export function classify(relativePath) {
  if (relativePath === 'CLAUDE.md') return { expectedKind: 'OP' };
  if (relativePath === REGISTER || /^docs\/decisions\/[^/]+\.md$/.test(relativePath)) return { expectedKind: 'DEC' };
  if (relativePath === MAP) return { expectedKind: 'none' };
  if (/^\.claude\/rules\/.+\.md$/.test(relativePath)) return { expectedKind: 'STD' };
  if (/^\.claude\/agents\/[^/]+\.md$/.test(relativePath)) return { expectedKind: 'WF' };
  const skill = relativePath.match(/^\.claude\/skills\/([^/]+)\/(SKILL\.md|references\/.+\.md)$/);
  if (skill) return { expectedKind: 'WF|KNW', skill: skill[1], isReference: skill[2] !== 'SKILL.md' };
  if (relativePath === 'CUSTOM_SETTINGS.md' || relativePath === 'SPECIFICATION.md') return { expectedKind: 'IN' };
  return null;
}

function resolveAffectsToken(root, token) {
  const match = token.trim().match(/^(STD|WF|KNW|ENF)\s+(\S+)$/);
  if (!match) return { ok: token.trim().startsWith('CLAUDE.md'), detail: 'unrecognized target' };
  const [, kind, name] = match;
  if (kind === 'STD') return { ok: existsSync(path.join(root, '.claude', 'rules', `${name}.md`)) };
  if (kind === 'WF' || kind === 'KNW') {
    const file = path.join(root, '.claude', 'skills', name, 'SKILL.md');
    if (!existsSync(file)) return { ok: false };
    const header = splitFrontmatter(readFileSync(file, 'utf8')).body.split('\n')[0].match(HEADER);
    return { ok: !!header && header[1].trim() === kind, detail: `${name} is not Kind ${kind}` };
  }
  const candidates = [
    path.join(root, '.claude', 'hooks', `${name}.mjs`),
    path.join(root, '.claude', 'scripts', `${name}.mjs`),
    path.join(root, name),
  ];
  return { ok: candidates.some((c) => existsSync(c)) };
}

export function parseRegister(text) {
  const rows = [];
  for (const line of text.replace(/\r\n/g, '\n').split('\n')) {
    const cells = line.split('|').map((c) => c.trim());
    if (cells.length >= 6 && /^DEC-[A-Z]+-\d{2}$/.test(cells[1])) {
      rows.push({ id: cells[1], decision: cells[2], details: cells[3], affects: cells[4] });
    }
  }
  return rows;
}

export function checkInstructions(root) {
  const errors = [];
  const warnings = [];
  const err = (file, message) => errors.push({ file, message });
  const warn = (file, message) => warnings.push({ file, message });

  const files = [
    'CLAUDE.md', REGISTER, MAP, 'SPECIFICATION.md', 'CUSTOM_SETTINGS.md',
    ...listFiles(root, '.claude/rules', (p) => p.endsWith('.md')),
    ...listFiles(root, '.claude/skills', (p) => p.endsWith('.md')),
    ...listFiles(root, '.claude/agents', (p) => p.endsWith('.md')),
    ...listFiles(root, 'docs/decisions', (p) => p.endsWith('.md')),
  ].filter((p, i, all) => all.indexOf(p) === i);

  for (const required of ['CLAUDE.md', REGISTER, MAP, '.claude/settings.json', 'SPECIFICATION.md', 'CUSTOM_SETTINGS.md', '.claude/agents/code-reviewer.md']) {
    if (!existsSync(path.join(root, required))) err(required, 'required file is missing');
  }

  const texts = new Map();
  const kinds = new Map();
  for (const file of files) {
    const full = path.join(root, file);
    if (!existsSync(full)) continue;
    const text = readFileSync(full, 'utf8').replace(/\r\n/g, '\n');
    texts.set(file, text);
    const info = classify(file);
    if (!info) { err(file, 'markdown file in an instruction location that matches no Kind'); continue; }
    if (file === 'SPECIFICATION.md' && text.trim() === '') { kinds.set(file, 'IN'); continue; }
    const { frontmatter, body, broken } = splitFrontmatter(text);
    if (broken) err(file, 'unterminated YAML frontmatter');
    const firstLine = body.split('\n')[0];
    if (info.expectedKind === 'none') {
      if (!/^<!-- Kind: none \(human reference\) \| Scope: repo\/meta \|.*Loads: never auto-loaded -->$/.test(firstLine)) err(file, 'map header must declare Kind: none (human reference) and Loads: never auto-loaded');
      continue;
    }
    const header = firstLine.match(HEADER);
    if (!header) { err(file, 'first line (after frontmatter) is not a "<!-- Kind | Scope | Owns | Loads -->" header'); continue; }
    const kind = header[1].trim();
    const scope = header[2].trim();
    kinds.set(file, kind);
    if (!KINDS.includes(kind)) err(file, `unknown Kind "${kind}"`);
    if (!SCOPES.includes(scope)) err(file, `unknown Scope "${scope}"`);
    if (info.expectedKind !== 'WF|KNW' && kind !== info.expectedKind) err(file, `Kind ${kind} does not match its location (expected ${info.expectedKind})`);
    if (info.expectedKind === 'WF|KNW' && !['WF', 'KNW'].includes(kind)) err(file, `skills hold only WF or KNW, found ${kind}`);
    if (/^Level:/m.test(prose(body)) || /\| Level: /.test(firstLine)) err(file, 'Level: classification is not part of this instruction system');

    if (info.expectedKind === 'STD') {
      const parts = file.split('/');
      const scopeDir = parts[2];
      if (parts.length !== 4) err(file, 'standards live directly in .claude/rules/<scope>/');
      if (!RULE_SCOPE_DIRS.includes(scopeDir)) err(file, `rules directory "${scopeDir}" is not a scope directory`);
      if (scopeDir !== scope) err(file, `Scope ${scope} does not match directory ${scopeDir}`);
      const globs = frontmatterList(frontmatter, 'paths');
      if (!globs || !globs.length) err(file, 'standard has no paths: frontmatter');
      else for (const glob of SCOPE_GLOBS[scope] ?? []) if (!globs.includes(glob)) err(file, `paths: is missing the ${scope} scope glob "${glob}"`);
      const proseBody = prose(body);
      if (/^\s*\d+\.\s/m.test(proseBody)) err(file, 'numbered steps found — procedures belong in workflows');
      for (const line of proseBody.split('\n')) {
        if (/`[a-z0-9-]+`\s+(knowledge skill|skill|workflow)|\.claude\/skills\//.test(line)
          && !/^(Technique|Workflow):/.test(line.trim())) {
          err(file, `skill reference outside a Technique:/Workflow: line: "${line.trim().slice(0, 80)}"`);
        }
      }
    }

    if (info.skill) {
      const skillFile = `.claude/skills/${info.skill}/SKILL.md`;
      if (info.isReference) {
        const owner = texts.get(skillFile) ?? (existsSync(path.join(root, skillFile)) ? readFileSync(path.join(root, skillFile), 'utf8') : '');
        const ownerHeader = splitFrontmatter(owner.replace(/\r\n/g, '\n')).body.split('\n')[0].match(HEADER);
        if (ownerHeader && ownerHeader[1].trim() !== kind) err(file, `private reference Kind ${kind} differs from its skill (${ownerHeader[1].trim()})`);
      } else {
        const name = frontmatterValue(frontmatter, 'name');
        const description = frontmatterDescription(frontmatter);
        if (name !== info.skill) err(file, `frontmatter name "${name}" does not match directory "${info.skill}"`);
        if (!description) err(file, 'missing description');
        else if (!/^(Use |User-invoked only)/.test(description)) err(file, 'description is not trigger-first ("Use ..." or "User-invoked only")');
        const userOnly = frontmatterValue(frontmatter, 'disable-model-invocation') === 'true';
        if (USER_ONLY_WORKFLOWS.includes(info.skill) !== userOnly) err(file, USER_ONLY_WORKFLOWS.includes(info.skill) ? 'must be user-invoked only (disable-model-invocation: true)' : 'disable-model-invocation is reserved for user-only workflows');
        if (kind === 'KNW' && REQUIRED_WORKFLOWS.includes(info.skill)) err(file, 'required workflow is classified as KNW');
        if (kind === 'WF' && REQUIRED_KNOWLEDGE.includes(info.skill)) err(file, 'required knowledge skill is classified as WF');
      }
      if (kind === 'KNW' && /\bmust\b/i.test(prose(body))) err(file, 'knowledge contains "must" statements — normative policy belongs to a standard');
    }
  }

  // Required skill sets and forbidden standalone skills.
  const skillDirs = existsSync(path.join(root, '.claude/skills')) ? readdirSync(path.join(root, '.claude/skills')).filter((d) => statSync(path.join(root, '.claude/skills', d)).isDirectory()) : [];
  for (const name of [...REQUIRED_WORKFLOWS, ...REQUIRED_KNOWLEDGE]) if (!skillDirs.includes(name)) err(`.claude/skills/${name}`, 'required skill is missing');
  for (const name of FORBIDDEN_SKILLS) if (skillDirs.includes(name)) err(`.claude/skills/${name}`, 'standalone skill duplicates knowledge ownership (use the owning skill\'s references/)');
  for (const dir of skillDirs) if (!existsSync(path.join(root, '.claude/skills', dir, 'SKILL.md'))) err(`.claude/skills/${dir}`, 'skill directory without SKILL.md');
  if (existsSync(path.join(root, '.claude/rules'))) {
    for (const dir of readdirSync(path.join(root, '.claude/rules'))) {
      if (!RULE_SCOPE_DIRS.includes(dir)) err(`.claude/rules/${dir}`, 'rules are organized by scope directories only (no ordered or level directories)');
    }
  }

  // Decision register.
  const registerText = texts.get(REGISTER) ?? '';
  const rows = parseRegister(registerText);
  const ids = new Set();
  for (const row of rows) {
    if (ids.has(row.id)) err(REGISTER, `duplicate decision ID ${row.id}`);
    ids.add(row.id);
    for (const [column, value] of [['Details in', row.details], ['Affects', row.affects]]) {
      if (!value) { err(REGISTER, `${row.id}: empty ${column}`); continue; }
      for (const token of value.split(',')) {
        const resolved = resolveAffectsToken(root, token.replace(/§.*$/, ''));
        if (!resolved.ok) err(REGISTER, `${row.id}: ${column} target "${token.trim()}" does not resolve${resolved.detail ? ` (${resolved.detail})` : ''}`);
      }
    }
  }
  for (const [file, text] of texts) {
    if (file !== REGISTER && /^\|\s*DEC-[A-Z]+-\d{2}\s*\|/m.test(text)) err(file, 'decision rows belong only in the decision register');
    for (const id of new Set(text.match(DEC_ID) ?? [])) if (!ids.has(id)) err(file, `cites unknown decision ${id}`);
  }

  // MAP: catalog covers every instruction file; Affects list matches the register.
  const mapText = texts.get(MAP) ?? '';
  for (const file of files) if (file !== MAP && existsSync(path.join(root, file)) && !mapText.includes(file.replace(/^\.claude\//, ''))) err(MAP, `catalog does not list ${file}`);
  const mapAffects = new Map();
  for (const line of mapText.split('\n')) {
    const match = line.match(/^- (DEC-[A-Z]+-\d{2}) → (.+)$/);
    if (match) mapAffects.set(match[1], match[2].split(',').map((t) => t.trim()).sort().join(', '));
  }
  for (const row of rows) {
    const expected = row.affects.split(',').map((t) => t.trim()).sort().join(', ');
    if (mapAffects.get(row.id) !== expected) err(MAP, `decision → Affects entry for ${row.id} differs from the register`);
  }
  for (const id of mapAffects.keys()) if (!ids.has(id)) err(MAP, `Affects entry for unknown decision ${id}`);

  // References: @imports, paths, section references, skill/agent names.
  for (const [file, text] of texts) {
    const body = prose(text);
    for (const match of body.matchAll(/^@(\S+)$/gm)) if (!existsSync(path.join(root, match[1]))) err(file, `@import ${match[1]} does not resolve`);
    for (const match of body.matchAll(/`((?:\.claude\/|docs\/|rules\/|references\/)[^`*<>]+?)`/g)) {
      const target = match[1].replace(/\/$/, '');
      if (/[*]|<|NNNN/.test(target)) continue;
      const candidates = target.startsWith('rules/') ? [path.join(root, '.claude', target)]
        : target.startsWith('references/') ? [path.join(root, path.dirname(file), target)]
          : [path.join(root, target)];
      if (!candidates.some((c) => existsSync(c))) err(file, `path ${target} does not resolve`);
    }
    for (const match of body.matchAll(/(CLAUDE\.md|\.claude\/MAP\.md|`(rules\/[^`]+\.md)`|`([a-z0-9-]+)`) § ([A-Za-z0-9][A-Za-z0-9 ,/'-]*[A-Za-z0-9]|\d)/g)) {
      let targetFile = null;
      if (match[1] === 'CLAUDE.md') targetFile = 'CLAUDE.md';
      else if (match[1] === '.claude/MAP.md') targetFile = MAP;
      else if (match[2]) targetFile = `.claude/${match[2]}`;
      else if (match[3]) targetFile = `.claude/skills/${match[3]}/SKILL.md`;
      const targetText = texts.get(targetFile) ?? (existsSync(path.join(root, targetFile)) ? readFileSync(path.join(root, targetFile), 'utf8') : null);
      if (targetText === null) { err(file, `section reference to missing ${targetFile}`); continue; }
      const section = match[4].replace(/[.,]$/, '');
      const candidates = [section, ...section.split(/\s+/).map((_, i, words) => words.slice(0, words.length - i).join(' '))]
        .map((candidate) => candidate.replace(/[.,;:]+$/, ''));
      if (!candidates.some((c) => c && hasHeading(targetText, c))) err(file, `section "§ ${section}" not found in ${targetFile}`);
    }
    for (const match of body.matchAll(/`([a-z0-9]+(?:-[a-z0-9]+)*)`(?=\s+(?:workflow|knowledge skill|skill|skills|knowledge skills)\b|\s*,\s*`[a-z0-9-]+`\s+(?:knowledge )?skills?\b)/g)) {
      if (!skillDirs.includes(match[1])) err(file, `skill \`${match[1]}\` does not exist`);
    }
    for (const match of body.matchAll(/(?:Run|run|→)\s+`([a-z][a-z0-9]*(?:-[a-z0-9]+)*)`/g)) {
      if (!skillDirs.includes(match[1])) err(file, `workflow \`${match[1]}\` does not exist`);
    }
    for (const match of body.matchAll(/agent `([a-z0-9-]+)`/g)) {
      if (!existsSync(path.join(root, '.claude/agents', `${match[1]}.md`))) err(file, `agent ${match[1]} does not exist`);
    }
    // Skill-private references are used only by their own skill (the map only catalogs them).
    for (const match of text.matchAll(/skills\/([a-z0-9-]+)\/references\//g)) {
      if (file !== MAP && !file.startsWith(`.claude/skills/${match[1]}/`)) err(file, `uses the private references of skill ${match[1]}`);
    }
  }

  // Hooks: shell-neutral node commands that resolve to existing scripts.
  const settingsFile = path.join(root, '.claude/settings.json');
  if (existsSync(settingsFile)) {
    let settings = null;
    try { settings = JSON.parse(readFileSync(settingsFile, 'utf8')); } catch (e) { err('.claude/settings.json', `invalid JSON (${e.message})`); }
    for (const [event, groups] of Object.entries(settings?.hooks ?? {})) {
      for (const group of groups) {
        for (const hook of group.hooks ?? []) {
          const command = hook.command ?? '';
          const match = command.match(/^node (\.claude\/(?:hooks|scripts)\/[A-Za-z0-9._-]+\.mjs)$/);
          if (!match) err('.claude/settings.json', `${event} hook command "${command}" is not "node .claude/<hooks|scripts>/<file>.mjs"`);
          else if (!existsSync(path.join(root, match[1]))) err('.claude/settings.json', `${event} hook script ${match[1]} is missing`);
          if (/[$%]/.test(command)) err('.claude/settings.json', `${event} hook command relies on shell variable expansion`);
        }
      }
    }
  }

  // Always-loaded budget: CLAUDE.md, its @imports, and model-visible skill descriptions.
  let chars = (texts.get('CLAUDE.md') ?? '').length;
  for (const match of (texts.get('CLAUDE.md') ?? '').matchAll(/^@(\S+)$/gm)) chars += (texts.get(match[1]) ?? '').length;
  for (const dir of skillDirs) {
    const text = texts.get(`.claude/skills/${dir}/SKILL.md`);
    if (!text) continue;
    const { frontmatter } = splitFrontmatter(text);
    if (frontmatterValue(frontmatter, 'disable-model-invocation') === 'true') continue;
    chars += dir.length + (frontmatterDescription(frontmatter) ?? '').length + 4;
  }
  const alwaysLoadedTokens = Math.round(chars / 4);
  if (alwaysLoadedTokens > BUDGET_TARGET_TOKENS * 1.2) warn('CLAUDE.md', `always-loaded estimate ${alwaysLoadedTokens} tokens exceeds the ~${BUDGET_TARGET_TOKENS} target`);

  return { errors, warnings, alwaysLoadedTokens, fileCount: files.length };
}

export function formatFindings(findings) {
  return findings.map((f) => `- ${f.file}: ${f.message}`).join('\n');
}

const isEntryPoint = process.argv[1] && import.meta.url.endsWith(process.argv[1].split(/[\\/]/).pop());
if (isEntryPoint) {
  const root = path.resolve(process.argv[2] ?? process.env.CLAUDE_PROJECT_DIR ?? process.cwd());
  if (!existsSync(path.join(root, 'CLAUDE.md'))) {
    process.stderr.write(`check-instructions: ${root} is not the project root (CLAUDE.md not found); pass the root as the first argument.\n`);
    process.exit(2);
  }
  const result = checkInstructions(root);
  if (result.errors.length) process.stdout.write(`Errors:\n${formatFindings(result.errors)}\n`);
  if (result.warnings.length) process.stdout.write(`Warnings:\n${formatFindings(result.warnings)}\n`);
  process.stdout.write(`check-instructions: ${result.fileCount} instruction files, ${result.errors.length} errors, ${result.warnings.length} warnings, always-loaded estimate ~${result.alwaysLoadedTokens} tokens\n`);
  process.exit(result.errors.length ? 1 : 0);
}
