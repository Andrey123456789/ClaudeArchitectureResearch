// Instruction-structure check for this template's instruction system.
// Usage: node .claude/scripts/check-instructions.mjs
// Exit codes: 0 = structure valid, 1 = violations, 2 = setup error.
// Verifies: required files, CLAUDE.md imports, a flat rule directory with explicit `paths`,
// one-line ownership headers, the required workflow and knowledge skills, the user-only
// maintenance workflow, the thin reviewer agent, private-reference ownership, internal
// references, an acyclic dependency graph that keeps always-loaded and path-scoped
// policy independent of on-demand material, shell-neutral hook commands, MAP coverage,
// and prints an always-loaded size estimate.
// Structure owner: .claude/skills/template-maintenance/SKILL.md; map: .claude/MAP.md.

import fs from 'node:fs';
import path from 'node:path';
import {
  SetupError, exists, formatFindings, isMainModule, readText, resolveProjectRoot, walkFiles,
} from './lib/repo.mjs';

const REQUIRED_WORKFLOWS = [
  'development-workflow', 'project-structure', 'verify', 'code-review', 'build-fix',
  'custom-settings', 'git-workflow', 'security-scan', 'add-dependency',
  'architecture-decision', 'template-maintenance',
];

const REQUIRED_KNOWLEDGE = [
  'ef-core', 'http-api', 'aspnet-error-handling', 'dotnet-testing', 'logging',
  'httpclient-factory', 'configuration', 'dependency-injection', 'caching', 'swagger',
  'api-versioning', 'health-check', 'docker', 'ci-cd', 'angular', 'modern-csharp',
  'authentication',
];

const USER_ONLY_SKILLS = ['template-maintenance'];
const MERGED_SKILLS = ['serilog', 'resilience'];
const SCOPES = new Set(['common', 'backend', 'backend-tests', 'frontend', 'delivery', 'repo/meta']);
const ALWAYS_LOADED = ['CLAUDE.md', 'docs/technology-stack.md'];
const ON_DEMAND_PATHS = ['docs/decisions/'];
// Generic file and folder names used in prose, and project files created by scaffolding.
const GENERIC_TOKENS = new Set(['SKILL.md', 'README.md', 'references/', 'MAP.md']);
const MAX_DESCRIPTION = 400;

function parseFrontmatter(text) {
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?/);
  if (!match) return { data: null, body: text };
  const data = {};
  let currentKey = null;
  for (const line of match[1].split(/\r?\n/)) {
    const item = line.match(/^\s+-\s+(.*)$/);
    if (item && currentKey) {
      if (!Array.isArray(data[currentKey])) data[currentKey] = [];
      data[currentKey].push(item[1].trim().replace(/^["']|["']$/g, ''));
      continue;
    }
    const pair = line.match(/^([A-Za-z][\w-]*):\s*(.*)$/);
    if (pair) {
      currentKey = pair[1];
      const value = pair[2].trim();
      data[currentKey] = value === '>' || value === '|' || value === '' ? '' : value.replace(/^["']|["']$/g, '');
      continue;
    }
    if (currentKey && typeof data[currentKey] === 'string' && /^\s+\S/.test(line)) {
      data[currentKey] = `${data[currentKey]} ${line.trim()}`.trim();
    }
  }
  return { data, body: text.slice(match[0].length) };
}

function parseHeader(body) {
  const line = body.split(/\r?\n/).find((l) => l.trim() !== '');
  if (!line || !line.startsWith('> ')) return null;
  const field = (name) => {
    const m = line.match(new RegExp(`${name}:\\s*([^·]+)`));
    return m ? m[1].trim() : null;
  };
  return { line, owns: field('Owns'), scope: field('Scope'), loads: field('Loads'), dependsOn: field('Depends on') };
}

function instructionFiles(files) {
  return files.filter((f) =>
    ALWAYS_LOADED.includes(f) || f === '.claude/MAP.md' ||
    /^\.claude\/rules\/[^/]+\.md$/.test(f) ||
    /^\.claude\/skills\/[^/]+\/SKILL\.md$/.test(f) ||
    /^\.claude\/skills\/[^/]+\/references\/[^/]+\.md$/.test(f) ||
    /^\.claude\/agents\/[^/]+\.md$/.test(f));
}

function skillOf(file) {
  const m = file.match(/^\.claude\/skills\/([^/]+)\//);
  return m ? m[1] : null;
}

function checkImports(root, findings) {
  const visited = new Set();
  const visit = (file, chain) => {
    if (chain.includes(file)) {
      findings.push({ level: 'violation', file, message: `import cycle: ${[...chain, file].join(' -> ')}` });
      return;
    }
    if (visited.has(file)) return;
    visited.add(file);
    const text = readText(root, file);
    if (text === null) {
      findings.push({ level: 'violation', file: chain.at(-1), message: `@ import target ${file} does not exist` });
      return;
    }
    for (const m of text.matchAll(/^@(\S+)\s*$/gm)) {
      visit(path.posix.normalize(path.posix.join(path.posix.dirname(file), m[1])), [...chain, file]);
    }
  };
  visit('CLAUDE.md', []);
  if (!visited.has('docs/technology-stack.md')) {
    findings.push({ level: 'violation', file: 'CLAUDE.md', message: 'does not import docs/technology-stack.md' });
  }
  return [...visited];
}

function checkRules(root, findings) {
  const dir = path.join(root, '.claude', 'rules');
  if (!fs.existsSync(dir)) {
    findings.push({ level: 'violation', file: '.claude/rules/', message: 'rule directory is missing' });
    return;
  }
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const file = `.claude/rules/${entry.name}`;
    if (entry.isDirectory()) {
      findings.push({ level: 'violation', file, message: 'rule directory must stay flat (no subdirectories)' });
      continue;
    }
    if (!entry.name.endsWith('.md')) continue;
    const { data } = parseFrontmatter(readText(root, file) ?? '');
    if (!data || !Array.isArray(data.paths) || data.paths.length === 0) {
      findings.push({ level: 'violation', file, message: 'rule must declare a non-empty `paths` list in frontmatter' });
    }
  }
}

function checkSkills(root, files, findings) {
  const skills = new Map();
  for (const file of files.filter((f) => /^\.claude\/skills\/[^/]+\/SKILL\.md$/.test(f))) {
    const name = skillOf(file);
    const { data } = parseFrontmatter(readText(root, file) ?? '');
    skills.set(name, data ?? {});
    if (!data) {
      findings.push({ level: 'violation', file, message: 'missing YAML frontmatter' });
      continue;
    }
    if (data.name !== name) findings.push({ level: 'violation', file, message: `frontmatter name "${data.name}" does not match directory "${name}"` });
    if (!data.description) findings.push({ level: 'violation', file, message: 'missing description' });
    else if (data.description.length > MAX_DESCRIPTION) findings.push({ level: 'warning', file, message: `description is ${data.description.length} characters; keep it concise and trigger-first` });
    const userOnly = String(data['disable-model-invocation'] ?? '').toLowerCase() === 'true';
    if (USER_ONLY_SKILLS.includes(name) && !userOnly) findings.push({ level: 'violation', file, message: 'user-only workflow must set disable-model-invocation: true' });
  }
  for (const name of [...REQUIRED_WORKFLOWS, ...REQUIRED_KNOWLEDGE]) {
    if (!skills.has(name)) findings.push({ level: 'violation', file: `.claude/skills/${name}/SKILL.md`, message: 'required skill is missing' });
  }
  for (const name of MERGED_SKILLS) {
    if (skills.has(name)) findings.push({ level: 'violation', file: `.claude/skills/${name}/`, message: 'competing standalone skill; this depth belongs to a private reference of its owning skill' });
  }
  return skills;
}

function checkAgent(root, findings) {
  const file = '.claude/agents/code-reviewer.md';
  const text = readText(root, file);
  if (text === null) {
    findings.push({ level: 'violation', file, message: 'reviewer agent is missing' });
    return;
  }
  const { data, body } = parseFrontmatter(text);
  const disallowed = String(data?.disallowedTools ?? '');
  for (const tool of ['Write', 'Edit']) {
    if (!new RegExp(`\\b${tool}\\b`).test(disallowed)) findings.push({ level: 'violation', file, message: `agent must disallow ${tool}` });
  }
  if (!body.includes('code-review')) findings.push({ level: 'violation', file, message: 'agent must delegate to the code-review skill' });
}

function resolveToken(root, file, token, skills) {
  const clean = token.replace(/[),.;:]+$/, '');
  if (/[<>*]|NNNN/.test(clean) || GENERIC_TOKENS.has(clean)) return true;
  if (ON_DEMAND_PATHS.some((p) => clean.startsWith(p))) return true;
  if (clean.startsWith('.claude/') || clean.startsWith('docs/')) {
    return exists(root, clean.replace(/\/$/, ''));
  }
  if (clean.startsWith('references/')) {
    const skill = skillOf(file);
    return skill ? exists(root, `.claude/skills/${skill}/${clean}`) : false;
  }
  if (/^[\w.-]+\.md$/.test(clean)) {
    const candidates = [clean, `.claude/rules/${clean}`, path.posix.join(path.posix.dirname(file), clean)];
    return candidates.some((c) => exists(root, c));
  }
  return true;
}

function checkReferences(root, files, skills, findings) {
  const knownSkills = new Set(skills.keys());
  const agents = new Set(walkFiles(root, '.claude/agents').map((f) => path.posix.basename(f, '.md')));
  for (const file of files) {
    const text = readText(root, file) ?? '';
    const prose = text.replace(/```[\s\S]*?```/g, '');
    for (const m of prose.matchAll(/`([^`\s]+)`/g)) {
      if (!resolveToken(root, file, m[1], skills)) findings.push({ level: 'violation', file, message: `reference \`${m[1]}\` does not resolve` });
    }
    for (const m of prose.matchAll(/\[[^\]]+\]\(([^)#\s]+)(#[^)]*)?\)/g)) {
      if (/^[a-z]+:/.test(m[1])) continue;
      if (!exists(root, path.posix.normalize(path.posix.join(path.posix.dirname(file), m[1])))) {
        findings.push({ level: 'violation', file, message: `link target ${m[1]} does not resolve` });
      }
    }
    for (const m of prose.matchAll(/`\/?([a-z][a-z0-9]*(?:-[a-z0-9]+)*)`(?:\s+\((?:agent|workflow)[^)]*\))?\s+(skills?|workflows?|agent)\b/g)) {
      const name = m[1];
      const kind = m[2];
      const ok = kind === 'agent' ? agents.has(name) : knownSkills.has(name);
      if (!ok) findings.push({ level: 'violation', file, message: `${kind} \`${name}\` does not exist` });
    }
  }
  const claude = readText(root, 'CLAUDE.md') ?? '';
  for (const m of claude.matchAll(/\|\s*`([a-z][a-z0-9-]+)`/g)) {
    if (!knownSkills.has(m[1])) findings.push({ level: 'violation', file: 'CLAUDE.md', message: `routing table names unknown workflow \`${m[1]}\`` });
  }
  for (const m of claude.matchAll(/`([a-z0-9-]+\.md)`/g)) {
    if (!['CLAUDE.md'].includes(m[1]) && !exists(root, `.claude/rules/${m[1]}`) && !exists(root, m[1])) {
      findings.push({ level: 'violation', file: 'CLAUDE.md', message: `rule \`${m[1]}\` does not exist` });
    }
  }
}

function checkPrivateReferences(root, files, findings) {
  const references = files.filter((f) => /^\.claude\/skills\/[^/]+\/references\/[^/]+\.md$/.test(f));
  for (const ref of references) {
    const owner = skillOf(ref);
    const fileName = path.posix.basename(ref);
    const ownerFile = `.claude/skills/${owner}/SKILL.md`;
    if (!(readText(root, ownerFile) ?? '').includes(`references/${fileName}`)) {
      findings.push({ level: 'violation', file: ownerFile, message: `does not route to its private reference references/${fileName}` });
    }
    for (const file of files) {
      if (file === ownerFile || file === '.claude/MAP.md' || skillOf(file) === owner) continue;
      const text = readText(root, file) ?? '';
      if (text.includes(`${owner}/references/`)) {
        findings.push({ level: 'violation', file, message: `uses private reference ${ref} of another skill` });
      }
    }
  }
}

function resolveDependency(root, entry) {
  const clean = entry.replace(/\s*\(.*\)$/, '').trim();
  if (clean.endsWith('/')) {
    return exists(root, clean.slice(0, -1))
      ? walkFiles(root, clean.slice(0, -1)).filter((f) => f.endsWith('.md'))
      : null;
  }
  return exists(root, clean) ? [clean] : null;
}

function checkHeadersAndDependencies(root, files, findings) {
  const graph = new Map();
  for (const file of files) {
    const text = readText(root, file) ?? '';
    const { body } = parseFrontmatter(text);
    const header = parseHeader(body);
    if (!header || !header.owns || !header.scope || !header.loads || !header.dependsOn) {
      findings.push({ level: 'violation', file, message: 'first line after frontmatter must be a one-line header with Owns, Scope, Loads, and Depends on' });
      continue;
    }
    for (const scope of header.scope.split(',').map((s) => s.trim())) {
      if (!SCOPES.has(scope)) findings.push({ level: 'violation', file, message: `unknown scope "${scope}"` });
    }
    const edges = [];
    if (header.dependsOn.toLowerCase() !== 'none') {
      for (const entry of header.dependsOn.split(',').map((s) => s.trim()).filter(Boolean)) {
        const targets = resolveDependency(root, entry);
        if (!targets) {
          findings.push({ level: 'violation', file, message: `dependency "${entry}" does not resolve` });
          continue;
        }
        edges.push(...targets.filter((t) => t !== file));
      }
    }
    graph.set(file, edges);
  }

  const normative = (f) => ALWAYS_LOADED.includes(f) || /^\.claude\/rules\//.test(f);
  for (const [file, edges] of graph) {
    for (const target of edges) {
      if (normative(file) && !normative(target)) {
        findings.push({ level: 'violation', file, message: `always-loaded or path-scoped policy depends on on-demand file ${target}` });
      }
      const refOwner = /\/references\//.test(target) ? skillOf(target) : null;
      if (refOwner && skillOf(file) !== refOwner) {
        findings.push({ level: 'violation', file, message: `depends on another skill's private reference ${target}` });
      }
    }
  }

  const state = new Map();
  const visit = (node, stack) => {
    if (state.get(node) === 'done') return;
    if (state.get(node) === 'active') {
      findings.push({ level: 'violation', file: node, message: `dependency cycle: ${[...stack, node].join(' -> ')}` });
      return;
    }
    state.set(node, 'active');
    for (const next of graph.get(node) ?? []) visit(next, [...stack, node]);
    state.set(node, 'done');
  };
  for (const node of graph.keys()) visit(node, []);
}

function checkSettings(root, findings) {
  const file = '.claude/settings.json';
  let settings;
  try {
    settings = JSON.parse(readText(root, file) ?? '');
  } catch (error) {
    findings.push({ level: 'violation', file, message: `not valid JSON (${error.message})` });
    return;
  }
  const commands = [];
  for (const groups of Object.values(settings.hooks ?? {})) {
    for (const group of groups ?? []) {
      for (const hook of group.hooks ?? []) if (hook.type === 'command') commands.push(hook.command);
    }
  }
  if (commands.length === 0) findings.push({ level: 'violation', file, message: 'no hook commands are registered' });
  for (const command of commands) {
    const m = String(command).match(/^node (\.claude\/(?:hooks|scripts)\/[\w.-]+\.mjs)((?: [\w.=-]+)*)$/);
    if (!m) {
      findings.push({ level: 'violation', file, message: `hook command "${command}" is not shell-neutral (expected: node .claude/<hooks|scripts>/<file>.mjs [args], no shell expansion)` });
    } else if (!exists(root, m[1])) {
      findings.push({ level: 'violation', file, message: `hook script ${m[1]} does not exist` });
    }
  }
}

function checkMap(root, files, findings) {
  const map = readText(root, '.claude/MAP.md');
  if (map === null) {
    findings.push({ level: 'violation', file: '.claude/MAP.md', message: 'instruction map is missing' });
    return;
  }
  const artifacts = [
    ...files.filter((f) => f !== '.claude/MAP.md'),
    ...walkFiles(root, '.claude/hooks'), ...walkFiles(root, '.claude/scripts'),
    '.claude/settings.json', 'SPECIFICATION.md', 'CUSTOM_SETTINGS.md',
    '.editorconfig', 'Directory.Build.props', 'Directory.Packages.props',
  ];
  for (const artifact of artifacts) {
    const short = artifact.replace(/^\.claude\//, '');
    const skill = artifact.match(/^\.claude\/skills\/([^/]+)\/SKILL\.md$/);
    const named = skill !== null && map.includes(`| \`${skill[1]}\` |`);
    if (!map.includes(artifact) && !map.includes(short) && !named) {
      findings.push({ level: 'violation', file: '.claude/MAP.md', message: `does not describe ${artifact}` });
    }
  }
}

function checkLeakage(root, files, findings) {
  for (const file of files) {
    const text = readText(root, file) ?? '';
    if (/^\s*>?\s*\**(Level|Kind)\**\s*:/m.test(text)) {
      findings.push({ level: 'violation', file, message: 'uses a Level/Kind classification field; this instruction system classifies by responsibility, scope, and loading only' });
    }
  }
}

function alwaysLoadedEstimate(root, imported, skills) {
  let chars = 0;
  for (const file of imported) chars += (readText(root, file) ?? '').length;
  for (const [name, data] of skills) {
    if (String(data['disable-model-invocation'] ?? '').toLowerCase() === 'true') continue;
    chars += name.length + String(data.description ?? '').length + 4;
  }
  return Math.round(chars / 4);
}

export function checkInstructions(root) {
  const findings = [];
  for (const required of ['CLAUDE.md', 'docs/technology-stack.md', '.claude/MAP.md', '.claude/settings.json']) {
    if (!exists(root, required)) findings.push({ level: 'violation', file: required, message: 'required file is missing' });
  }
  const files = instructionFiles(walkFiles(root));
  const imported = checkImports(root, findings);
  checkRules(root, findings);
  const skills = checkSkills(root, walkFiles(root, '.claude/skills'), findings);
  checkAgent(root, findings);
  checkHeadersAndDependencies(root, files, findings);
  checkPrivateReferences(root, files, findings);
  checkReferences(root, files, skills, findings);
  checkSettings(root, findings);
  checkMap(root, files, findings);
  checkLeakage(root, files, findings);
  return { findings, files, estimate: alwaysLoadedEstimate(root, imported, skills) };
}

function main() {
  let root;
  try {
    root = resolveProjectRoot(import.meta.url);
  } catch (error) {
    process.stderr.write(`check-instructions: ${error.message}\n`);
    process.exit(2);
  }
  const { findings, files, estimate } = checkInstructions(root);
  const violations = findings.filter((f) => f.level === 'violation');
  process.stdout.write(`check-instructions: checked ${files.length} instruction file(s).\n`);
  process.stdout.write(`check-instructions: always-loaded surface estimate ~${estimate} tokens (CLAUDE.md, imports, skill listing).\n`);
  if (findings.length > 0) process.stdout.write(`${formatFindings('Findings:', findings)}\n`);
  process.stdout.write(violations.length > 0
    ? `check-instructions: FAIL (${violations.length} violation(s)).\n`
    : 'check-instructions: PASS.\n');
  process.exit(violations.length > 0 ? 1 : 0);
}

if (isMainModule(import.meta.url)) {
  try {
    main();
  } catch (error) {
    if (!(error instanceof SetupError)) process.stderr.write(`check-instructions: unexpected error: ${error.stack ?? error}\n`);
    process.exit(2);
  }
}
