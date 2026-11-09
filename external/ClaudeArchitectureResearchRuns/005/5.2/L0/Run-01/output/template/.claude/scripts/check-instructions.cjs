// Level: 3 Project | Instruction-structure checker for the stability-level instruction system.
// Validates: level-first rule layout, classification headers, `paths` on every rule and scope coverage,
// stratified always-loaded imports, technology neutrality of levels 0-1, declared conformance
// dependencies (same or more stable level, resolvable, acyclic), routing-pointer discipline for
// references to more volatile levels, skill-private references, skill/agent references, hook command
// portability, the required workflow/knowledge/agent set, and instruction-map coverage.
// Usage: node .claude/scripts/check-instructions.cjs            (check; exit 1 on errors)
//        node .claude/scripts/check-instructions.cjs --rules-for <path>   (list rule modules for a path)
'use strict';

const fs = require('fs');
const path = require('path');

const LEVEL_DIRS = { '0-core': 0, '1-architecture': 1, '2-technology': 2, '3-project': 3 };
const LEVEL_NAMES = ['Core', 'Architecture', 'Technology', 'Project'];
const SCOPES = new Set(['common', 'backend', 'backend-tests', 'frontend', 'delivery', 'repo/meta']);
const ALWAYS_IMPORTS = ['.claude/rules/1-architecture/overview.md', '.claude/rules/3-project/decisions.md'];
const REQUIRED_WORKFLOWS = ['develop', 'project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings',
  'git-workflow', 'security-scan', 'add-dependency', 'architecture-decision', 'template-maintenance'];
const REQUIRED_KNOWLEDGE = ['ef-core', 'http-api', 'aspnet-error-handling', 'dotnet-testing', 'logging',
  'httpclient-factory', 'configuration', 'dependency-injection', 'caching', 'swagger', 'api-versioning',
  'health-check', 'docker', 'ci-cd', 'angular', 'modern-csharp', 'authentication'];
const FORBIDDEN_SKILLS = ['serilog', 'resilience'];
const USER_ONLY_SKILLS = ['template-maintenance'];
// Concrete technologies that levels 0 and 1 must not name (the fixed platform .NET/C#/TypeScript is allowed).
const DENIED_TECHNOLOGIES = ['EF Core', 'Entity Framework', 'DbContext', 'DbSet', 'NUnit', 'xUnit', 'MSTest',
  'Angular', 'RxJS', 'Vitest', 'Playwright', 'Serilog', 'FluentValidation', 'Swashbuckle', 'Swagger',
  'SQL Server', 'SqlServer', 'Docker', 'Kubernetes', 'Mapster', 'AutoMapper', 'Polly', 'MediatR', 'Kommand',
  'Testcontainers', 'WebApplicationFactory', 'IExceptionHandler', 'ValidationProblemDetails', 'IActionResult',
  'ASP.NET', 'NgRx', 'Redis', 'npm', 'NuGet', 'GitHub Actions'];
const HEADER = /^> Level: ([0-3]) (Core|Architecture|Technology|Project) \| Owns: (.+?) \| Scope: (.+?) \| Loads: (.+?) \| Depends on: (.+)$/;
const RULE_REF = /(?:\.claude\/rules\/)?([0-3]-(?:core|architecture|technology|project))\/([a-z0-9-]+\.md)/g;

function resolveRoot() {
  const root = path.resolve(process.env.CLAUDE_PROJECT_DIR || process.cwd());
  if (!fs.existsSync(path.join(root, '.claude'))) {
    throw new Error(`check-instructions: cannot locate the project root (no .claude directory in "${root}"). ` +
      'Run from the repository root or set CLAUDE_PROJECT_DIR.');
  }
  return root;
}

const toPosix = p => p.split(path.sep).join('/');

function globToRegExp(glob) {
  let re = '';
  for (let i = 0; i < glob.length; i++) {
    const c = glob[i];
    if (c === '*') {
      if (glob[i + 1] === '*') {
        if (glob[i + 2] === '/') { re += '(?:.*/)?'; i += 2; } else { re += '.*'; i += 1; }
      } else {
        re += '[^/]*';
      }
    } else if (c === '?') {
      re += '[^/]';
    } else {
      re += c.replace(/[.+^${}()|[\]\\]/g, '\\$&');
    }
  }
  return new RegExp(`^${re}$`);
}

function parseFrontmatter(text) {
  const normalized = text.replace(/\r\n/g, '\n');
  if (!normalized.startsWith('---\n')) return { data: {}, body: normalized };
  const end = normalized.indexOf('\n---', 4);
  if (end < 0) return { data: {}, body: normalized, error: 'unterminated frontmatter' };
  const lines = normalized.slice(4, end).split('\n');
  const data = {};
  let key = null;
  let mode = null;
  for (const line of lines) {
    const pair = line.match(/^([A-Za-z][\w-]*):\s*(.*)$/);
    if (pair) {
      key = pair[1];
      const value = pair[2].trim();
      if (value === '>' || value === '|') { data[key] = ''; mode = 'text'; } else if (value === '') { data[key] = []; mode = 'list'; } else { data[key] = value.replace(/^["']|["']$/g, ''); mode = null; }
      continue;
    }
    if (key && mode === 'list') {
      const item = line.match(/^\s+-\s+(.*)$/);
      if (item) data[key].push(item[1].trim().replace(/^["']|["']$/g, ''));
    } else if (key && mode === 'text' && line.trim()) {
      data[key] = `${data[key]} ${line.trim()}`.trim();
    }
  }
  return { data, body: normalized.slice(end + 4).replace(/^\n/, '') };
}

function listFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  const out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...listFiles(full)); else out.push(full);
  }
  return out;
}

function loadArtifacts(root, errors) {
  const artifacts = [];
  const add = (file, type, extra = {}) => {
    const rel = toPosix(path.relative(root, file));
    const text = fs.readFileSync(file, 'utf8');
    const { data, body, error } = parseFrontmatter(text);
    if (error) errors.push(`${rel}: ${error}`);
    const headerLine = body.split('\n').find(l => l.trim()) || '';
    const header = headerLine.match(HEADER);
    artifacts.push({ rel, type, text, data, body, headerLine, header, ...extra });
  };

  const claude = path.join(root, 'CLAUDE.md');
  if (fs.existsSync(claude)) add(claude, 'memory'); else errors.push('CLAUDE.md is missing');

  const rulesDir = path.join(root, '.claude', 'rules');
  if (!fs.existsSync(rulesDir)) errors.push('.claude/rules is missing');
  for (const entry of fs.existsSync(rulesDir) ? fs.readdirSync(rulesDir, { withFileTypes: true }) : []) {
    if (!entry.isDirectory()) { errors.push(`.claude/rules/${entry.name}: rule files must live inside a level directory`); continue; }
    if (!(entry.name in LEVEL_DIRS)) { errors.push(`.claude/rules/${entry.name}: unknown level directory (allowed: ${Object.keys(LEVEL_DIRS).join(', ')})`); continue; }
    for (const file of listFiles(path.join(rulesDir, entry.name))) {
      const depth = toPosix(path.relative(path.join(rulesDir, entry.name), file)).split('/').length;
      if (depth > 2) errors.push(`${toPosix(path.relative(root, file))}: nest rule modules at most one directory below the level directory`);
      if (file.endsWith('.md')) add(file, 'rule', { dirLevel: LEVEL_DIRS[entry.name] });
    }
  }
  for (const level of Object.keys(LEVEL_DIRS)) {
    if (!fs.existsSync(path.join(rulesDir, level))) errors.push(`.claude/rules/${level} is missing`);
  }

  const skillsDir = path.join(root, '.claude', 'skills');
  for (const entry of fs.existsSync(skillsDir) ? fs.readdirSync(skillsDir, { withFileTypes: true }) : []) {
    if (!entry.isDirectory()) continue;
    const skillFile = path.join(skillsDir, entry.name, 'SKILL.md');
    if (!fs.existsSync(skillFile)) { errors.push(`.claude/skills/${entry.name}: SKILL.md is missing`); continue; }
    add(skillFile, 'skill', { skill: entry.name });
    for (const file of listFiles(path.join(skillsDir, entry.name))) {
      const rel = toPosix(path.relative(path.join(skillsDir, entry.name), file));
      if (rel === 'SKILL.md') continue;
      if (/^references\/[^/]+\.md$/.test(rel)) add(file, 'reference', { skill: entry.name });
      else errors.push(`.claude/skills/${entry.name}/${rel}: unexpected file (skills hold SKILL.md and references/*.md)`);
    }
  }

  const agentsDir = path.join(root, '.claude', 'agents');
  for (const file of listFiles(agentsDir).filter(f => f.endsWith('.md'))) add(file, 'agent');
  return artifacts;
}

function levelOf(artifact) {
  return artifact.header ? Number(artifact.header[1]) : null;
}

function checkInstructions(root = resolveRoot()) {
  const errors = [];
  const warnings = [];
  const info = [];
  const artifacts = loadArtifacts(root, errors);
  const byRel = new Map(artifacts.map(a => [a.rel, a]));
  const skills = new Set(artifacts.filter(a => a.type === 'skill').map(a => a.skill));
  const agents = new Set(artifacts.filter(a => a.type === 'agent').map(a => a.data.name));
  const rules = artifacts.filter(a => a.type === 'rule');

  // Headers and per-type predicates.
  for (const a of artifacts) {
    if (!a.header) { errors.push(`${a.rel}: first line must be the classification header "> Level: <n> <Name> | Owns: … | Scope: … | Loads: … | Depends on: …"`); continue; }
    const level = levelOf(a);
    if (LEVEL_NAMES[level] !== a.header[2]) errors.push(`${a.rel}: level ${level} must be named ${LEVEL_NAMES[level]}`);
    if (/\b(Kind|Contract|Slot|Capability|Manifest):/.test(a.headerLine)) errors.push(`${a.rel}: header must not use Kind/Contract/Slot/Capability/Manifest fields`);
    for (const scope of a.header[4].split(/,\s*/)) {
      if (!SCOPES.has(scope)) errors.push(`${a.rel}: unknown scope "${scope}"`);
    }
    if (a.type === 'rule') {
      if (level !== a.dirLevel) errors.push(`${a.rel}: header level ${level} does not match its level directory`);
      const paths = Array.isArray(a.data.paths) ? a.data.paths : [];
      if (!paths.length) errors.push(`${a.rel}: rule files must declare a non-empty "paths" list`);
      for (const scope of a.header[4].split(/,\s*/)) {
        const ok = {
          'common': () => paths.includes('**/*') || (paths.includes('backend/**') && paths.includes('frontend/**')),
          'backend': () => paths.some(p => p.startsWith('backend/') || p.startsWith('**/')),
          'backend-tests': () => paths.some(p => p.startsWith('backend/') || p.startsWith('**/')),
          'frontend': () => paths.some(p => p.startsWith('frontend/') || p.startsWith('**/')),
          'delivery': () => paths.some(p => /Dockerfile|compose|\.github/.test(p)),
          'repo/meta': () => true
        }[scope];
        if (ok && !ok()) errors.push(`${a.rel}: paths do not cover declared scope "${scope}"`);
      }
    }
    if (a.type === 'skill') {
      if (a.data.name !== a.skill) errors.push(`${a.rel}: frontmatter name must equal the directory name "${a.skill}"`);
      const description = String(a.data.description || '');
      if (!description) errors.push(`${a.rel}: description is required`);
      if (description.length > 1024) errors.push(`${a.rel}: description exceeds 1024 characters`);
      const userOnly = String(a.data['disable-model-invocation']) === 'true';
      if (USER_ONLY_SKILLS.includes(a.skill) && !userOnly) errors.push(`${a.rel}: user-only skill must set disable-model-invocation: true`);
    }
    if (a.type === 'agent') {
      if (!a.data.name || !a.data.description) errors.push(`${a.rel}: agents need name and description`);
    }
  }

  // Stratified always-loaded decisions.
  const memory = byRel.get('CLAUDE.md');
  if (memory) {
    if (levelOf(memory) !== 0) errors.push('CLAUDE.md: must be Level 0 Core');
    const imports = [...memory.body.matchAll(/^@(\S+)$/gm)].map(m => m[1]);
    for (const required of ALWAYS_IMPORTS) {
      if (!imports.includes(required)) errors.push(`CLAUDE.md: must import ${required}`);
    }
    for (const imported of imports) {
      if (!ALWAYS_IMPORTS.includes(imported)) errors.push(`CLAUDE.md: unexpected import ${imported} (only the architecture and project decision summaries are always-loaded imports)`);
      if (!fs.existsSync(path.join(root, imported))) errors.push(`CLAUDE.md: import ${imported} does not resolve`);
    }
  }

  // Technology neutrality of levels 0 and 1.
  for (const a of artifacts.filter(x => levelOf(x) !== null && levelOf(x) <= 1)) {
    const text = [a.data.description || '', a.body]
      .join('\n')
      .replace(/^@.*$/gm, '')
      .replace(/`[a-z0-9][a-z0-9\-/.*<>]*`/g, '');
    for (const term of DENIED_TECHNOLOGIES) {
      const pattern = new RegExp(`(^|[^A-Za-z0-9])${term.replace(/[.+^${}()|[\]\\]/g, '\\$&')}([^A-Za-z0-9]|$)`, 'i');
      if (pattern.test(text)) errors.push(`${a.rel}: Level ${levelOf(a)} must not name the concrete technology "${term}" (move the binding to 2-technology or 3-project)`);
    }
  }

  // Declared conformance dependencies.
  const graph = new Map();
  const resolveDependency = token => {
    if (token === 'CLAUDE.md') return ['CLAUDE.md'];
    const glob = token.match(/^([0-3]-[a-z]+)\/\*$/);
    if (glob) return rules.filter(r => r.rel.startsWith(`.claude/rules/${glob[1]}/`)).map(r => r.rel);
    if (/^[0-3]-[a-z]+\/[a-z0-9-]+\.md$/.test(token)) return [`.claude/rules/${token}`];
    const skill = token.match(/^skills\/([a-z0-9-]+)$/);
    if (skill) return [`.claude/skills/${skill[1]}/SKILL.md`];
    return null;
  };
  for (const a of artifacts.filter(x => x.header)) {
    const tokens = a.header[6].trim() === 'none' ? [] : a.header[6].split(/,\s*/);
    const edges = [];
    for (const token of tokens) {
      const targets = resolveDependency(token.trim());
      if (!targets) { errors.push(`${a.rel}: unrecognized dependency "${token}"`); continue; }
      if (!targets.length) { errors.push(`${a.rel}: dependency "${token}" matches nothing`); continue; }
      for (const target of targets) {
        if (target === a.rel) continue;
        const t = byRel.get(target);
        if (!t) { errors.push(`${a.rel}: dependency ${target} does not exist`); continue; }
        if (levelOf(t) > levelOf(a)) errors.push(`${a.rel}: Level ${levelOf(a)} must not depend on more volatile Level ${levelOf(t)} (${target})`);
        edges.push(target);
      }
    }
    graph.set(a.rel, edges);
  }
  const state = new Map();
  const visit = (node, trail) => {
    if (state.get(node) === 'done') return;
    if (state.get(node) === 'active') { errors.push(`dependency cycle: ${[...trail, node].join(' -> ')}`); return; }
    state.set(node, 'active');
    for (const next of graph.get(node) || []) visit(next, [...trail, node]);
    state.set(node, 'done');
  };
  for (const node of graph.keys()) visit(node, []);

  // References: rule files, routing discipline, private references, .claude paths, skill and agent names.
  for (const a of artifacts) {
    const own = levelOf(a);
    const lines = a.body.split('\n');
    const headerIndex = lines.findIndex(l => l.trim());
    const body = lines.slice(headerIndex + 1).join('\n');
    for (const paragraph of body.split(/\n\s*\n/)) {
      for (const m of paragraph.matchAll(RULE_REF)) {
        const target = `.claude/rules/${m[1]}/${m[2]}`;
        const t = byRel.get(target);
        if (!t) { errors.push(`${a.rel}: reference ${target} does not resolve`); continue; }
        if (own !== null && levelOf(t) > own && !paragraph.includes('→') && !/^@/m.test(paragraph)) {
          errors.push(`${a.rel}: reference to more volatile ${target} must be written as a "→" routing pointer`);
        }
      }
    }
    for (const m of a.body.matchAll(/skills\/([a-z0-9-]+)\/references\/[a-z0-9-]+\.md/g)) {
      if (a.skill !== m[1]) errors.push(`${a.rel}: skill-private reference of "${m[1]}" may be used only by that skill`);
    }
    if (a.type === 'skill') {
      for (const m of a.body.matchAll(/`references\/([a-z0-9-]+\.md)`/g)) {
        if (!fs.existsSync(path.join(root, '.claude', 'skills', a.skill, 'references', m[1]))) errors.push(`${a.rel}: references/${m[1]} does not exist`);
      }
    }
    if (a.type === 'reference') {
      const owner = byRel.get(`.claude/skills/${a.skill}/SKILL.md`);
      const name = path.posix.basename(a.rel);
      if (!owner || !owner.body.includes(`references/${name}`)) errors.push(`${a.rel}: private reference is not referenced by its owning SKILL.md`);
    }
    for (const m of a.body.matchAll(/`(\.claude\/[A-Za-z0-9_\-/.]+)`/g)) {
      const target = m[1].replace(/[.,;:]+$/, '');
      if (!fs.existsSync(path.join(root, target))) errors.push(`${a.rel}: path ${target} does not exist`);
    }
    const names = [
      ...a.body.matchAll(/`([a-z][a-z0-9-]*)`\s+(?:skill|workflow|agent)\b/g),
      ...a.body.matchAll(/\brun\s+`([a-z][a-z0-9-]*)`/gi),
      ...a.body.matchAll(/→\s+(?:run\s+)?`([a-z][a-z0-9-]*)`/g)
    ].map(m => m[1]);
    for (const name of new Set(names)) {
      if (!skills.has(name) && !agents.has(name)) errors.push(`${a.rel}: referenced skill or agent "${name}" does not exist`);
    }
  }

  // Required workflow, knowledge, and agent set.
  for (const name of [...REQUIRED_WORKFLOWS, ...REQUIRED_KNOWLEDGE]) {
    if (!skills.has(name)) errors.push(`required skill "${name}" is missing`);
  }
  for (const name of FORBIDDEN_SKILLS) {
    if (skills.has(name)) errors.push(`standalone "${name}" skill duplicates a private reference of another knowledge skill`);
  }
  const reviewer = artifacts.find(a => a.type === 'agent' && a.data.name === 'code-reviewer');
  if (!reviewer) errors.push('code-reviewer agent is missing');
  else {
    if (!/Write/.test(reviewer.data.disallowedTools || '') || !/Edit/.test(reviewer.data.disallowedTools || '')) errors.push(`${reviewer.rel}: must disallow Write and Edit`);
    if (!reviewer.body.includes('code-review')) errors.push(`${reviewer.rel}: must delegate to the code-review workflow`);
  }

  // Hook commands: shell-neutral and resolvable.
  const settingsFile = path.join(root, '.claude', 'settings.json');
  if (!fs.existsSync(settingsFile)) errors.push('.claude/settings.json is missing');
  else {
    let settings = {};
    try { settings = JSON.parse(fs.readFileSync(settingsFile, 'utf8')); } catch (e) { errors.push(`.claude/settings.json: invalid JSON (${e.message})`); }
    for (const [event, groups] of Object.entries(settings.hooks || {})) {
      for (const group of groups) {
        for (const hook of group.hooks || []) {
          const command = String(hook.command || '');
          if (/\$|%[A-Za-z_]+%/.test(command)) errors.push(`.claude/settings.json ${event}: hook command must not rely on shell environment expansion`);
          const script = command.match(/'\.claude','hooks','([^']+)'/);
          if (!script) errors.push(`.claude/settings.json ${event}: hook command must launch a script under .claude/hooks through node`);
          else if (!fs.existsSync(path.join(root, '.claude', 'hooks', script[1]))) errors.push(`.claude/settings.json ${event}: hook script ${script[1]} does not exist`);
        }
      }
    }
  }

  // Human map coverage.
  const mapFile = path.join(root, '.claude', 'INSTRUCTION_MAP.md');
  if (!fs.existsSync(mapFile)) errors.push('.claude/INSTRUCTION_MAP.md is missing');
  else {
    const map = fs.readFileSync(mapFile, 'utf8');
    const expected = artifacts.map(a => (a.rel === 'CLAUDE.md' ? 'CLAUDE.md' : a.rel.replace(/^\.claude\//, '')));
    for (const file of listFiles(path.join(root, '.claude', 'hooks')).concat(listFiles(path.join(root, '.claude', 'scripts')))) {
      const rel = toPosix(path.relative(path.join(root, '.claude'), file));
      if (!rel.startsWith('hooks/.state/')) expected.push(rel);
    }
    for (const item of expected) {
      if (!map.includes(item)) errors.push(`.claude/INSTRUCTION_MAP.md: does not list ${item}`);
    }
  }

  // Always-loaded budget (approximation: 4 characters per token).
  const always = [memory ? memory.text : '', ...ALWAYS_IMPORTS.map(f => (byRel.get(f) || {}).text || '')].join('');
  const listings = artifacts.filter(a => a.type === 'skill' && String(a.data['disable-model-invocation']) !== 'true')
    .map(a => `${a.data.name}: ${a.data.description}`).join('\n');
  const tokens = Math.round((always.length + listings.length) / 4);
  info.push(`always-loaded surface ≈ ${tokens} tokens (memory + imports ≈ ${Math.round(always.length / 4)}, skill listings ≈ ${Math.round(listings.length / 4)})`);
  if (tokens > 6000) warnings.push(`always-loaded surface ≈ ${tokens} tokens exceeds the ~5k target`);

  return { errors, warnings, info };
}

function rulesFor(root, target) {
  const artifacts = loadArtifacts(root, []);
  const rel = toPosix(path.relative(root, path.resolve(root, target)));
  return artifacts
    .filter(a => a.type === 'rule' && Array.isArray(a.data.paths) && a.data.paths.some(p => globToRegExp(p).test(rel)))
    .map(a => `${a.rel} — ${a.header ? a.header[3] : ''}`);
}

module.exports = { checkInstructions, rulesFor, globToRegExp };

if (require.main === module) {
  try {
    const root = resolveRoot();
    const index = process.argv.indexOf('--rules-for');
    if (index > 0) {
      const target = process.argv[index + 1];
      if (!target) throw new Error('usage: --rules-for <path>');
      const matches = rulesFor(root, target);
      console.log(matches.length ? matches.join('\n') : 'no path-scoped rule matches this path');
      process.exit(0);
    }
    const { errors, warnings, info } = checkInstructions(root);
    for (const line of info) console.log(`INFO ${line}`);
    for (const line of warnings) console.log(`WARN ${line}`);
    for (const line of errors) console.log(`ERROR ${line}`);
    console.log(errors.length ? `check-instructions: ${errors.length} error(s)` : 'check-instructions: OK');
    process.exit(errors.length ? 1 : 0);
  } catch (error) {
    console.error(error.message);
    process.exit(2);
  }
}
