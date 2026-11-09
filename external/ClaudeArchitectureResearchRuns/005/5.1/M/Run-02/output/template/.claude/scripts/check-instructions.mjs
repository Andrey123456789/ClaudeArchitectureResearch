// Owner: structural checks of the instruction system — headers, flat path-scoped rules, skill set and front matter, private references, pointers, imports, map coverage, hook wiring, always-loaded estimate | Scope: repo/meta | Loads: CLI (`node .claude/scripts/check-instructions.mjs`), PostToolUse hook after instruction edits, `template-maintenance` | Enforced: exit code 1 on errors
// Conventions checked here are defined in .claude/skills/template-maintenance/SKILL.md.

import fs from 'node:fs';
import path from 'node:path';
import { projectRoot, walk, readText, exists, finding, reportCli, isMain } from './lib.mjs';

const MAINTENANCE = '.claude/skills/template-maintenance/SKILL.md § Conventions';

export const WORKFLOW_SKILLS = [
  'project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings',
  'git-workflow', 'security-scan', 'add-dependency', 'architecture-decision',
  'template-maintenance',
];

export const KNOWLEDGE_SKILLS = [
  'ef-core', 'http-api', 'aspnet-error-handling', 'dotnet-testing', 'logging',
  'httpclient-factory', 'configuration', 'dependency-injection', 'caching',
  'swagger', 'api-versioning', 'health-check', 'docker', 'ci-cd', 'angular',
  'modern-csharp', 'authentication',
];

const COMPETING_SKILLS = ['serilog', 'resilience'];
const USER_ONLY_SKILLS = ['template-maintenance'];
const ROOT_FILES = ['CLAUDE.md', 'SPECIFICATION.md', 'CUSTOM_SETTINGS.md', 'Directory.Build.props', 'Directory.Packages.props', '.editorconfig'];
// Paths that exist only after first use or only on a developer machine.
const ON_DEMAND_PREFIXES = ['docs/decisions/', '.claude/settings.local.json'];
const HEADER = /^> Owner: .+ \| Scope: .+ \| Loads: .+ \| Enforced: .+$/;
const CODE_HEADER = /^(\/\/|#|<!--) Owner: .+ \| Scope: .+ \| Loads: .+ \| Enforced: .+/;

/** Splits optional YAML front matter from the body and parses a small YAML subset. */
export function parseFrontMatter(text) {
  const lines = text.split(/\r?\n/);
  if (lines[0] !== '---') {
    return { data: null, body: text, bodyLines: lines };
  }
  const end = lines.indexOf('---', 1);
  if (end < 0) {
    return { data: null, body: text, bodyLines: lines, error: 'unterminated front matter' };
  }
  const data = {};
  let key = null;
  let mode = null;
  for (const line of lines.slice(1, end)) {
    const top = /^([A-Za-z][\w-]*):\s*(.*)$/.exec(line);
    if (top) {
      key = top[1];
      const value = top[2].trim();
      if (value === '>' || value === '|' || value === '>-' || value === '|-') {
        data[key] = '';
        mode = 'text';
      } else if (value === '') {
        data[key] = [];
        mode = 'list';
      } else {
        data[key] = value.replace(/^["']|["']$/g, '');
        mode = null;
      }
      continue;
    }
    if (key && mode === 'list' && /^\s*-\s+/.test(line)) {
      data[key].push(line.replace(/^\s*-\s+/, '').trim().replace(/^["']|["']$/g, ''));
    } else if (key && mode === 'text' && line.trim() !== '') {
      data[key] = `${data[key]} ${line.trim()}`.trim();
    }
  }
  const bodyLines = lines.slice(end + 1);
  return { data, body: bodyLines.join('\n'), bodyLines };
}

function firstContentLine(lines) {
  return lines.find((line) => line.trim() !== '') ?? '';
}

function headings(text) {
  const result = [];
  let inFence = false;
  for (const line of text.split(/\r?\n/)) {
    if (/^\s*```/.test(line)) inFence = !inFence;
    if (inFence) continue;
    const match = /^#{1,6}\s+(.+?)\s*#*\s*$/.exec(line);
    if (match) result.push(match[1].trim());
  }
  return result;
}

function skillDirOf(file) {
  const match = /^\.claude\/skills\/([^/]+)\//.exec(file);
  return match ? match[1] : null;
}

function collectArtifacts(root) {
  const markdown = [
    'CLAUDE.md', 'docs/technology-stack.md', '.claude/MAP.md',
    ...walk(root, '.claude/rules', () => true),
    ...walk(root, '.claude/skills', (f) => f.endsWith('.md')),
    ...walk(root, '.claude/agents', (f) => f.endsWith('.md')),
  ].filter((f) => exists(root, f));
  const code = [
    ...walk(root, '.claude/hooks', (f) => f.endsWith('.mjs')),
    ...walk(root, '.claude/scripts', (f) => f.endsWith('.mjs')),
    '.editorconfig', 'Directory.Build.props', 'Directory.Packages.props',
  ].filter((f) => exists(root, f));
  return { markdown, code };
}

function checkHeaders(root, artifacts, findings) {
  for (const file of artifacts.markdown) {
    const text = readText(root, file) ?? '';
    const { data, bodyLines, error } = parseFrontMatter(text);
    if (error) findings.push(finding('error', file, error));
    const header = firstContentLine(bodyLines);
    if (!HEADER.test(header)) {
      findings.push(finding('error', file, 'missing one-line "> Owner: … | Scope: … | Loads: … | Enforced: …" header', MAINTENANCE));
    }
    if (/\b(Level|Kind):/.test(header) || (data && ('level' in data || 'kind' in data))) {
      findings.push(finding('error', file, 'Level/Kind classification is not part of this instruction system', MAINTENANCE));
    }
  }
  for (const file of artifacts.code) {
    const first = (readText(root, file) ?? '').split(/\r?\n/)[0];
    if (!CODE_HEADER.test(first)) {
      // Tooling may rewrite configuration files, so only scripts treat a lost header as an error.
      const level = file.endsWith('.mjs') ? 'error' : 'warning';
      findings.push(finding(level, file, 'missing one-line Owner/Scope/Loads/Enforced header comment', MAINTENANCE));
    }
  }
}

function checkRules(root, findings) {
  const dir = path.resolve(root, '.claude/rules');
  if (!fs.existsSync(dir)) {
    findings.push(finding('error', '.claude/rules', 'rules directory is missing'));
    return;
  }
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const file = `.claude/rules/${entry.name}`;
    if (entry.isDirectory()) {
      findings.push(finding('error', file, 'rules must stay flat (no subdirectories)', MAINTENANCE));
      continue;
    }
    if (!entry.name.endsWith('.md')) {
      findings.push(finding('error', file, 'only Markdown rule files belong in .claude/rules'));
      continue;
    }
    const { data } = parseFrontMatter(readText(root, file) ?? '');
    if (!data || !Array.isArray(data.paths) || data.paths.length === 0) {
      findings.push(finding('error', file, 'rule must declare a non-empty "paths" list', MAINTENANCE));
    }
  }
}

function checkSkills(root, findings) {
  const dir = path.resolve(root, '.claude/skills');
  const present = fs.existsSync(dir)
    ? fs.readdirSync(dir, { withFileTypes: true }).filter((e) => e.isDirectory()).map((e) => e.name)
    : [];
  for (const name of [...WORKFLOW_SKILLS, ...KNOWLEDGE_SKILLS]) {
    if (!present.includes(name)) {
      findings.push(finding('error', `.claude/skills/${name}`, 'required skill is missing'));
    }
  }
  for (const name of present) {
    const file = `.claude/skills/${name}/SKILL.md`;
    if (COMPETING_SKILLS.includes(name)) {
      findings.push(finding('error', `.claude/skills/${name}`, 'competing standalone skill; this depth is a private reference of logging or httpclient-factory', MAINTENANCE));
    }
    if (!exists(root, file)) {
      findings.push(finding('error', file, 'skill directory without SKILL.md'));
      continue;
    }
    const { data } = parseFrontMatter(readText(root, file) ?? '');
    if (!data) {
      findings.push(finding('error', file, 'missing front matter'));
      continue;
    }
    if (data.name !== name) {
      findings.push(finding('error', file, `front matter name "${data.name}" must equal directory name "${name}"`, MAINTENANCE));
    }
    if (!data.description) {
      findings.push(finding('error', file, 'missing description'));
    } else if (!USER_ONLY_SKILLS.includes(name) && !/^Use\b/.test(data.description)) {
      findings.push(finding('warning', file, 'description should be trigger-first ("Use when …")', MAINTENANCE));
    }
    if ('model' in data || 'effort' in data) {
      findings.push(finding('error', file, 'skills must not pin a model or effort level', MAINTENANCE));
    }
    const userOnly = String(data['disable-model-invocation'] ?? '') === 'true';
    if (USER_ONLY_SKILLS.includes(name) && !userOnly) {
      findings.push(finding('error', file, 'must set "disable-model-invocation: true" (user-invoked only)', MAINTENANCE));
    }
  }
}

function checkAgents(root, findings) {
  const file = '.claude/agents/code-reviewer.md';
  if (!exists(root, file)) {
    findings.push(finding('error', file, 'code-reviewer agent is missing'));
    return;
  }
  const { data } = parseFrontMatter(readText(root, file) ?? '');
  if (!data) {
    findings.push(finding('error', file, 'missing front matter'));
    return;
  }
  if (!String(data.skills ?? '').split(/[\s,]+/).includes('code-review')) {
    findings.push(finding('error', file, 'must preload the code-review workflow ("skills: code-review")'));
  }
  if (/\b(Write|Edit|MultiEdit|NotebookEdit)\b/.test(String(data.tools ?? 'all'))) {
    findings.push(finding('error', file, 'reviewer tools must exclude file-editing tools'));
  }
  for (const agent of walk(root, '.claude/agents', (f) => f.endsWith('.md'))) {
    const meta = parseFrontMatter(readText(root, agent) ?? '').data ?? {};
    if ('model' in meta || 'effort' in meta) {
      findings.push(finding('error', agent, 'agents must not pin a model or effort level', MAINTENANCE));
    }
  }
}

function checkImports(root, findings) {
  const text = readText(root, 'CLAUDE.md');
  if (text === null) {
    findings.push(finding('error', 'CLAUDE.md', 'CLAUDE.md is missing'));
    return;
  }
  const imports = [...text.matchAll(/^@(\S+)\s*$/gm)].map((m) => m[1]);
  if (!imports.includes('docs/technology-stack.md')) {
    findings.push(finding('error', 'CLAUDE.md', 'must import @docs/technology-stack.md (planning-time stack decisions)'));
  }
  for (const target of imports) {
    if (!exists(root, target)) {
      findings.push(finding('error', 'CLAUDE.md', `import @${target} does not resolve`));
    }
  }
}

function isOnDemand(token) {
  return ON_DEMAND_PREFIXES.some((prefix) => token.startsWith(prefix));
}

function resolveToken(root, file, token) {
  if (/[<>*{}]|NNNN|\s/.test(token)) return { kind: 'skip' };
  const skill = skillDirOf(file);
  if (token.startsWith('references/')) {
    if (!skill) return { kind: 'error', message: `private reference "${token}" used outside its owning skill` };
    return { kind: 'file', target: `.claude/skills/${skill}/${token}` };
  }
  const clean = token.replace(/:\d+$/, '');
  if (clean.startsWith('.claude/') || clean.startsWith('docs/') || ROOT_FILES.includes(clean)) {
    return { kind: 'file', target: clean.replace(/\/$/, ''), dir: clean.endsWith('/') };
  }
  return { kind: 'skip' };
}

function checkPointers(root, artifacts, findings) {
  const headingCache = new Map();
  const headingsOf = (target) => {
    if (!headingCache.has(target)) headingCache.set(target, headings(readText(root, target) ?? ''));
    return headingCache.get(target);
  };

  for (const file of artifacts.markdown) {
    const ownSkill = skillDirOf(file);
    for (const { start, text: line } of paragraphs(readText(root, file) ?? '')) {
      let target = null;
      const where = `${file}:${start}`;

      // Private references must not be reached from another skill or a shared file.
      for (const match of line.matchAll(/skills\/([a-z0-9-]+)\/references\//g)) {
        if (file !== '.claude/MAP.md' && match[1] !== ownSkill) {
          findings.push(finding('error', where, `points into the private references of skill "${match[1]}"`, MAINTENANCE));
        }
      }

      // Markdown links.
      for (const match of line.matchAll(/\[[^\]]*\]\(([^)\s]+)\)/g)) {
        const href = match[1].split('#')[0];
        if (!href || /^(https?:|mailto:)/.test(href)) continue;
        const resolved = path.posix.normalize(path.posix.join(path.posix.dirname(file), href));
        if (!exists(root, resolved)) findings.push(finding('error', where, `link target "${href}" does not exist`));
      }

      // Backticked tokens and § pointers, in reading order.
      const events = [];
      for (const match of line.matchAll(/`([^`]+)`(\s+(?:workflow|skill))?/g)) {
        events.push({ index: match.index, token: match[1], skillWord: Boolean(match[2]) });
      }
      for (const match of line.matchAll(/§\s+([^§]+)/g)) {
        events.push({ index: match.index, section: match[1] });
      }
      events.sort((a, b) => a.index - b.index);

      for (const event of events) {
        if (event.token !== undefined) {
          const token = event.token.trim();
          const slash = /^\/([a-z][a-z0-9-]*)$/.exec(token);
          if (event.skillWord || slash) {
            const name = slash ? slash[1] : token;
            if (/^[a-z][a-z0-9-]*$/.test(name)) {
              if (!exists(root, `.claude/skills/${name}/SKILL.md`)) {
                findings.push(finding('error', where, `skill or workflow "${name}" does not exist`));
              }
              target = `.claude/skills/${name}/SKILL.md`;
              continue;
            }
          }
          const resolved = resolveToken(root, file, token);
          if (resolved.kind === 'skip') {
            target = null;
          } else if (resolved.kind === 'error') {
            findings.push(finding('error', where, resolved.message, MAINTENANCE));
          } else if (resolved.kind === 'file') {
            if (isOnDemand(resolved.target + (resolved.dir ? '/' : ''))) {
              target = null;
            } else if (!exists(root, resolved.target)) {
              findings.push(finding('error', where, `reference "${token}" does not resolve`));
              target = null;
            } else {
              target = resolved.target.endsWith('.md') ? resolved.target : null;
            }
          }
        } else if (target) {
          const wanted = event.section.trim().toLowerCase();
          const match = headingsOf(target).some((h) => wanted.startsWith(h.toLowerCase()));
          if (!match) {
            findings.push(finding('error', where, `section "§ ${event.section.trim().slice(0, 40)}" not found in ${target}`));
          }
        }
      }
    }
  }
}

/** Paragraphs outside code fences, each joined into one line so pointers may wrap. */
function paragraphs(text) {
  const result = [];
  let current = null;
  let inFence = false;
  text.split(/\r?\n/).forEach((line, index) => {
    if (/^\s*```/.test(line)) {
      inFence = !inFence;
      current = null;
      return;
    }
    if (inFence || line.trim() === '') {
      current = null;
      return;
    }
    if (!current) {
      current = { start: index + 1, text: line.trim() };
      result.push(current);
    } else {
      current.text += ` ${line.trim()}`;
    }
  });
  return result;
}

function checkMap(root, findings) {
  const map = readText(root, '.claude/MAP.md');
  if (map === null) {
    findings.push(finding('error', '.claude/MAP.md', 'human instruction map is missing'));
    return;
  }
  const expected = [
    'CLAUDE.md', 'docs/technology-stack.md', 'SPECIFICATION.md', 'CUSTOM_SETTINGS.md',
    '.editorconfig', 'Directory.Build.props', 'Directory.Packages.props', '.claude/settings.json',
    ...walk(root, '.claude/rules', (f) => f.endsWith('.md')),
    ...walk(root, '.claude/skills', (f) => f.endsWith('.md')),
    ...walk(root, '.claude/agents', (f) => f.endsWith('.md')),
    ...walk(root, '.claude/hooks', (f) => f.endsWith('.mjs')),
    ...walk(root, '.claude/scripts', (f) => f.endsWith('.mjs')),
  ];
  for (const file of expected) {
    if (!map.includes(file)) {
      findings.push(finding('error', '.claude/MAP.md', `does not list ${file}`, MAINTENANCE));
    }
  }
}

function checkSettings(root, findings) {
  const file = '.claude/settings.json';
  const text = readText(root, file);
  if (text === null) {
    findings.push(finding('error', file, 'settings file is missing'));
    return;
  }
  let settings;
  try {
    settings = JSON.parse(text);
  } catch (error) {
    findings.push(finding('error', file, `invalid JSON: ${error.message}`));
    return;
  }
  const commands = Object.values(settings.hooks ?? {})
    .flat()
    .flatMap((group) => group.hooks ?? [])
    .map((hook) => hook.command ?? '');
  for (const command of commands) {
    for (const match of command.matchAll(/\.claude\/[\w./-]+\.mjs/g)) {
      if (!exists(root, match[0])) {
        findings.push(finding('error', file, `hook command references missing script ${match[0]}`));
      }
    }
  }
}

/** Rough always-loaded estimate: CLAUDE.md, its imports, and model-invocable skill descriptions. */
export function alwaysLoadedEstimate(root) {
  const claude = readText(root, 'CLAUDE.md') ?? '';
  let chars = claude.length;
  for (const match of claude.matchAll(/^@(\S+)\s*$/gm)) {
    chars += (readText(root, match[1]) ?? '').length;
  }
  let listing = 0;
  for (const file of walk(root, '.claude/skills', (f) => f.endsWith('/SKILL.md'))) {
    const { data } = parseFrontMatter(readText(root, file) ?? '');
    if (data && String(data['disable-model-invocation'] ?? '') !== 'true') {
      listing += String(data.name ?? '').length + String(data.description ?? '').length + 8;
    }
  }
  return { instructions: Math.round(chars / 4), skillListing: Math.round(listing / 4) };
}

export function checkInstructions(root) {
  const findings = [];
  const artifacts = collectArtifacts(root);
  checkHeaders(root, artifacts, findings);
  checkRules(root, findings);
  checkSkills(root, findings);
  checkAgents(root, findings);
  checkImports(root, findings);
  checkPointers(root, artifacts, findings);
  checkMap(root, findings);
  checkSettings(root, findings);
  const estimate = alwaysLoadedEstimate(root);
  if (estimate.instructions + estimate.skillListing > 6000) {
    findings.push(finding('warning', 'CLAUDE.md', `always-loaded estimate is ~${estimate.instructions + estimate.skillListing} tokens; move depth to rules or skills`, MAINTENANCE));
  }
  return findings;
}

if (isMain(import.meta.url)) {
  const root = projectRoot();
  const estimate = alwaysLoadedEstimate(root);
  console.log(`Always-loaded estimate: ~${estimate.instructions} tokens (CLAUDE.md + imports) + ~${estimate.skillListing} tokens (skill listing).`);
  reportCli('Instruction check', checkInstructions(root));
}
