#!/usr/bin/env node
// Instruction-structure checker for the level-first instruction system with replaceable capabilities.
// Validates: headers and levels, rule paths, capability selection and module manifests, facet ownership,
// always-loaded imports, implementation-name leakage, platform-only vocabulary in Core/Architecture,
// facet/path/skill references, private references, required workflows/knowledge, agent, hooks, map coverage.
// Usage: node .claude/scripts/check-instructions.mjs        (exit 1 on violations, 2 on setup errors)
import { existsSync, readdirSync, statSync } from 'node:fs';
import path from 'node:path';
import { listFiles, parseSelection, readText, resolveRoot, toPosix } from './lib/project.mjs';

const LEVELS = ['0-core', '1-architecture', '2-technology', '3-project'];
const SLOTS = { architecture: 'required', persistence: 'required', 'backend-testing': 'required', frontend: 'optional' };
const REQUIRED_WORKFLOWS = ['development-workflow', 'project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings',
  'git-workflow', 'security-scan', 'add-dependency', 'architecture-decision', 'template-maintenance'];
const REQUIRED_SHARED_KNOWLEDGE = ['http-api', 'aspnet-error-handling', 'logging', 'httpclient-factory', 'configuration',
  'dependency-injection', 'caching', 'swagger', 'api-versioning', 'health-check', 'docker', 'ci-cd', 'modern-csharp', 'authentication'];
// Concrete non-platform technologies that Core and Architecture artifacts must not name.
const NON_PLATFORM_TOKENS = ['FluentValidation', 'Serilog', 'Swashbuckle', 'Swagger', 'Mapster', 'Polly', 'Testcontainers',
  'MediatR', 'Kommand', 'Redis', 'Docker', 'npm', 'Playwright', 'Vitest'];
const LEAK_ALLOWED = new Set(['.claude/rules/3-project/decisions.md', '.claude/INSTRUCTION_MAP.md']);

const violations = [];
const warnings = [];
const fail = (file, msg) => violations.push(`${file}: ${msg}`);
const warn = (file, msg) => warnings.push(`${file}: ${msg}`);

function splitFrontmatter(text) {
  const normalized = text.replace(/\r\n/g, '\n');
  if (!normalized.startsWith('---\n')) return { fm: '', body: normalized };
  const end = normalized.indexOf('\n---', 4);
  if (end < 0) return { fm: '', body: normalized };
  return { fm: normalized.slice(4, end), body: normalized.slice(end + 4) };
}

function parseHeader(body) {
  const line = body.split('\n').find((l) => l.trim() !== '') || '';
  if (!line.startsWith('> Level: ')) return null;
  const fields = {};
  for (const part of line.slice(2).split(' · ')) {
    const idx = part.indexOf(':');
    if (idx > 0) fields[part.slice(0, idx).trim()] = part.slice(idx + 1).trim();
  }
  return fields;
}

function tokenRegex(token) {
  const escaped = token.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return new RegExp(`(?<![A-Za-z0-9-])${escaped}(?![A-Za-z0-9-])`);
}

function main() {
  const root = resolveRoot();
  const rel = (abs) => toPosix(path.relative(root, abs));
  const exists = (p) => existsSync(path.join(root, p));
  const claude = path.join(root, '.claude');

  const artifactPaths = [
    'CLAUDE.md',
    '.claude/INSTRUCTION_MAP.md',
    ...['rules', 'skills', 'agents', 'capabilities'].flatMap((d) => listFiles(path.join(claude, d), (f) => f.endsWith('.md')).map(rel)),
  ].filter((p) => exists(p));
  const docs = new Map();
  for (const p of artifactPaths) {
    const text = readText(path.join(root, p));
    const { fm, body } = splitFrontmatter(text);
    docs.set(p, { text, fm, body, header: parseHeader(body) });
  }

  // Headers.
  for (const [p, d] of docs) {
    if (!d.header) { fail(p, 'missing one-line header starting with "> Level: "'); continue; }
    if (!LEVELS.includes(d.header.Level)) fail(p, `unknown Level '${d.header.Level}'`);
    if (!d.header.Owns) fail(p, 'header lacks "Owns:"');
    if (!d.header.Loading) fail(p, 'header lacks "Loading:"');
    if ('Kind' in d.header) fail(p, 'header uses a "Kind:" field; classify by Level and Capability only');
  }

  // Selection record and capability directories.
  const selection = parseSelection(root);
  const selected = {};
  for (const [slot, requirement] of Object.entries(SLOTS)) {
    const row = selection.find((r) => r.slot === slot);
    if (!row) { fail('.claude/rules/3-project/decisions.md', `selection record lacks slot '${slot}'`); continue; }
    if (requirement === 'required' && !row.selected) fail('.claude/rules/3-project/decisions.md', `required slot '${slot}' has no selected implementation`);
    selected[slot] = row.selected;
    const slotDir = path.join(claude, 'capabilities', slot);
    if (!existsSync(path.join(slotDir, 'CONTRACT.md'))) fail(`.claude/capabilities/${slot}`, 'missing CONTRACT.md');
    const impls = existsSync(slotDir) ? readdirSync(slotDir).filter((e) => statSync(path.join(slotDir, e)).isDirectory()) : [];
    const expected = row.selected ? [row.selected] : [];
    if (impls.sort().join(',') !== expected.join(',')) {
      fail(`.claude/capabilities/${slot}`, `implementations present [${impls.join(', ')}] differ from selection [${expected.join(', ')}] (static composition: only selected modules ship)`);
    }
  }
  for (const row of selection) if (!(row.slot in SLOTS)) fail('.claude/rules/3-project/decisions.md', `unknown slot '${row.slot}' (only the four agreed slots exist)`);

  // Module manifests.
  const modules = [];
  for (const [slot, impl] of Object.entries(selected)) {
    if (!impl) continue;
    const manifestPath = `.claude/capabilities/${slot}/${impl}/MODULE.md`;
    const doc = docs.get(manifestPath);
    if (!doc) { fail(manifestPath, 'missing module manifest'); continue; }
    const capability = `${slot}/${impl}`;
    const tokensLine = doc.body.match(/^- leak-tokens:\s*(.+)$/m);
    const facets = [...doc.body.matchAll(/^\|\s*`([a-z-]+\.[a-z-]+)`\s*\|\s*`([^`]+)`\s*\|\s*([a-z0-9-]+)\s*\|/gm)]
      .map((m) => ({ facet: m[1], file: m[2], level: m[3] }));
    if (!tokensLine) fail(manifestPath, 'missing "- leak-tokens:" line');
    if (facets.length === 0) fail(manifestPath, 'facet table is empty or malformed');
    if (doc.header && doc.header.Capability !== capability) fail(manifestPath, `header Capability must be '${capability}'`);
    const tokens = tokensLine ? tokensLine[1].split(',').map((t) => t.trim()).filter(Boolean) : [];
    for (const f of facets) {
      if (!f.facet.startsWith(`${slot}.`)) fail(manifestPath, `facet '${f.facet}' does not belong to slot '${slot}'`);
      if (!exists(f.file)) { fail(manifestPath, `facet file missing: ${f.file}`); continue; }
      if (f.file.endsWith('.md')) {
        const fd = docs.get(f.file);
        if (fd && fd.header) {
          if (fd.header.Capability !== capability) fail(f.file, `must declare "Capability: ${capability}" (listed in ${manifestPath})`);
          if (fd.header.Facet !== f.facet) fail(f.file, `must declare "Facet: ${f.facet}"`);
          if (fd.header.Level !== f.level) fail(f.file, `Level '${fd.header.Level}' differs from manifest level '${f.level}'`);
        }
      } else if (f.file.endsWith('.json')) {
        try { JSON.parse(readText(path.join(root, f.file))); } catch { fail(f.file, 'invalid JSON'); }
      }
    }
    modules.push({ slot, impl, capability, manifestPath, facets, tokens, dir: `.claude/capabilities/${slot}/${impl}/` });
  }
  const ownerOf = (p) => modules.find((m) => p.startsWith(m.dir) || m.facets.some((f) => f.file === p || (f.file.endsWith('/SKILL.md') && p.startsWith(f.file.replace(/SKILL\.md$/, '')))));

  // Capability declarations must match manifests.
  for (const [p, d] of docs) {
    if (!d.header || !d.header.Capability) continue;
    const m = modules.find((x) => x.capability === d.header.Capability);
    if (!m) { fail(p, `declares Capability '${d.header.Capability}', which is not a selected module`); continue; }
    if (!(p.startsWith(m.dir) || m.facets.some((f) => f.file === p))) fail(p, `declares Capability '${m.capability}' but is not listed in ${m.manifestPath}`);
  }

  // Rules.
  for (const [p, d] of docs) {
    if (!p.startsWith('.claude/rules/')) continue;
    const parts = p.split('/');
    const levelDir = parts[2];
    if (!LEVELS.includes(levelDir)) fail(p, `rule outside a level directory (${LEVELS.join(', ')})`);
    if (d.header && d.header.Level !== levelDir) fail(p, `header Level '${d.header.Level}' does not match directory '${levelDir}'`);
    const pathsBlock = d.fm.match(/^paths:\s*\n((?:\s+-\s+.+\n?)+)/m);
    if (!pathsBlock || !/-\s+"?[^"\s]+"?/.test(pathsBlock[1])) fail(p, 'rule must declare non-empty "paths:" frontmatter');
    if (parts.length > 4 && d.header && !d.header.Capability) fail(p, 'rule in a capability subdirectory must declare "Capability:"');
  }

  // Always-loaded surface: CLAUDE.md imports.
  const imports = [...docs.get('CLAUDE.md').body.matchAll(/^@(\S+)\s*$/gm)].map((m) => m[1]);
  for (const imp of imports) {
    if (!exists(imp)) { fail('CLAUDE.md', `import does not resolve: @${imp}`); continue; }
    const d = docs.get(imp);
    if (d && d.header && !/^always/.test(d.header.Loading)) fail(imp, 'imported by CLAUDE.md but header Loading is not "always"');
  }
  for (const [p, d] of docs) {
    if (p !== 'CLAUDE.md' && d.header && /^always/.test(d.header.Loading) && !imports.includes(p)) fail(p, 'declares "Loading: always" but is not imported by CLAUDE.md');
  }

  // Implementation-name leakage.
  for (const [p, d] of docs) {
    if (LEAK_ALLOWED.has(p)) continue;
    const owner = ownerOf(p);
    for (const m of modules) {
      if (owner === m) continue;
      for (const token of m.tokens) {
        if (tokenRegex(token).test(d.body)) fail(p, `names '${token}' from module ${m.capability}; use slot/facet/role vocabulary or move the content into the module`);
      }
    }
  }

  // Core and Architecture use platform vocabulary only.
  for (const [p, d] of docs) {
    if (!d.header || !['0-core', '1-architecture'].includes(d.header.Level)) continue;
    for (const token of NON_PLATFORM_TOKENS) {
      if (tokenRegex(token).test(d.body)) fail(p, `Level ${d.header.Level} names concrete technology '${token}'`);
    }
  }

  // Facet references.
  for (const [p, d] of docs) {
    for (const m of d.body.matchAll(/(?<![\w./-])(architecture|persistence|backend-testing|frontend)\.([a-z][a-z-]*)(?![\w-])/g)) {
      const [ref, slot] = [m[0], m[1]];
      const mod = modules.find((x) => x.slot === slot);
      if (!mod) { if (SLOTS[slot] === 'required') fail(p, `facet reference '${ref}' but slot '${slot}' has no module`); continue; }
      if (!mod.facets.some((f) => f.facet === ref)) fail(p, `facet reference '${ref}' is not declared in ${mod.manifestPath}`);
    }
  }

  // Skills and agents.
  const skillsDir = path.join(claude, 'skills');
  const skills = existsSync(skillsDir) ? readdirSync(skillsDir).filter((e) => existsSync(path.join(skillsDir, e, 'SKILL.md'))) : [];
  const agents = listFiles(path.join(claude, 'agents'), (f) => f.endsWith('.md')).map((f) => path.basename(f, '.md'));
  const moduleKnowledge = modules.flatMap((m) => m.facets.filter((f) => f.facet.endsWith('.knowledge')).map((f) => f.file.split('/')[2]));
  for (const name of [...REQUIRED_WORKFLOWS, ...REQUIRED_SHARED_KNOWLEDGE, ...moduleKnowledge]) {
    if (!skills.includes(name)) fail(`.claude/skills/${name}`, 'required skill is missing');
  }
  for (const name of skills) {
    const p = `.claude/skills/${name}/SKILL.md`;
    const d = docs.get(p);
    const fmName = (d.fm.match(/^name:\s*(.+)$/m) || [])[1];
    const description = (d.fm.match(/^description:\s*(.+)$/m) || [])[1];
    if (fmName !== name) fail(p, `frontmatter name '${fmName}' must equal directory '${name}'`);
    if (!description) fail(p, 'missing description');
    else if (description.length > 360) warn(p, `description is ${description.length} chars; keep skill listings compact`);
    const userOnly = /^disable-model-invocation:\s*true\s*$/m.test(d.fm);
    if (name === 'template-maintenance' && !userOnly) fail(p, 'must set disable-model-invocation: true (user-only workflow)');
    if (name !== 'template-maintenance' && userOnly) fail(p, 'must stay model-invocable');
  }
  const reviewer = docs.get('.claude/agents/code-reviewer.md');
  if (!reviewer) fail('.claude/agents/code-reviewer.md', 'missing code-reviewer agent');
  else {
    const disallowed = (reviewer.fm.match(/^disallowedTools:\s*(.+)$/m) || [])[1] || '';
    if (!/\bWrite\b/.test(disallowed) || !/\bEdit\b/.test(disallowed)) fail('.claude/agents/code-reviewer.md', 'must disallow Write and Edit (read-only reviewer)');
    if (!reviewer.body.includes('`code-review`')) fail('.claude/agents/code-reviewer.md', 'must delegate to the code-review skill');
  }

  // Named skill/agent references.
  const known = new Set([...skills, ...agents]);
  for (const [p, d] of docs) {
    const re = /`([a-z][a-z0-9-]*)`(?=\s+(?:skill|workflow|agent)\b)|(?:\brun|→|Technique:|Procedure:|Procedures:)\s+`([a-z][a-z0-9-]*)`/g;
    for (const m of d.body.matchAll(re)) {
      const name = m[1] || m[2];
      if (!known.has(name)) fail(p, `references unknown skill or agent '${name}'`);
    }
  }

  // Path references.
  for (const [p, d] of docs) {
    for (const m of d.body.matchAll(/`(\.claude\/[^`\s]+|references\/[^`\s]+)`/g)) {
      const target = m[1].replace(/[.,;:]+$/, '');
      if (/[<*>]/.test(target)) continue;
      const resolved = target.startsWith('references/') ? path.posix.join(path.posix.dirname(p), target) : target;
      if (!exists(resolved)) fail(p, `path reference does not resolve: ${target}`);
    }
  }

  // Skill-private references are used only by their owning skill (the map may list them).
  for (const p of docs.keys()) {
    const m = p.match(/^\.claude\/skills\/([^/]+)\/references\/(.+)$/);
    if (!m) continue;
    for (const [other, d] of docs) {
      if (other === p || other === '.claude/INSTRUCTION_MAP.md' || other.startsWith(`.claude/skills/${m[1]}/`)) continue;
      const ownRelative = other.startsWith('.claude/skills/') && d.body.includes(`references/${m[2]}`);
      if (d.body.includes(`${m[1]}/references/${m[2]}`) || ownRelative) fail(other, `depends on private reference ${p} of skill '${m[1]}'`);
    }
  }

  // Human map coverage.
  const map = docs.get('.claude/INSTRUCTION_MAP.md');
  if (!map) fail('.claude/INSTRUCTION_MAP.md', 'missing instruction map');
  else {
    for (const p of docs.keys()) if (p !== '.claude/INSTRUCTION_MAP.md' && !map.body.includes(p)) fail('.claude/INSTRUCTION_MAP.md', `does not list ${p}`);
    if (imports.includes('.claude/INSTRUCTION_MAP.md')) fail('CLAUDE.md', 'the instruction map must not be auto-loaded');
  }

  // Hooks: shell-neutral commands that resolve to existing scripts.
  const settingsPath = path.join(claude, 'settings.json');
  if (!existsSync(settingsPath)) fail('.claude/settings.json', 'missing');
  else {
    const settings = JSON.parse(readText(settingsPath));
    for (const [event, groups] of Object.entries(settings.hooks || {})) {
      for (const group of groups) {
        for (const hook of group.hooks || []) {
          const cmd = hook.command || '';
          if (/[$%`]/.test(cmd)) fail('.claude/settings.json', `${event} hook relies on shell expansion: ${cmd}`);
          const m = cmd.match(/^node\s+(\S+\.mjs)(\s|$)/);
          if (!m) fail('.claude/settings.json', `${event} hook is not a plain "node <script>.mjs" command: ${cmd}`);
          else if (!exists(m[1])) fail('.claude/settings.json', `${event} hook script missing: ${m[1]}`);
        }
      }
    }
  }

  for (const w of warnings) console.log(`WARNING   ${w}`);
  for (const v of violations) console.log(`VIOLATION ${v}`);
  console.log(`Instruction check: ${violations.length === 0 ? 'PASS' : 'FAIL'} (${docs.size} artifacts, ${violations.length} violation(s), ${warnings.length} warning(s)).`);
  process.exit(violations.length === 0 ? 0 : 1);
}

try {
  main();
} catch (error) {
  console.error(`Instruction check could not run: ${error.message}`);
  process.exit(2);
}
