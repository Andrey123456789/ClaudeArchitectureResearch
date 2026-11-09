// Kind: ENF | Scope: repo/meta | Capability: — | Loading: command (instruction-change hooks, verify, template-maintenance): node "<root>/.claude/scripts/check-instructions.cjs"
// Conforms: docs/architecture/decision-register.md
'use strict';

// Validates the Kinds x Scopes + capability-slot structure of this instruction system.

const path = require('path');
const lib = require('./lib.cjs');

const KINDS = ['OP', 'DEC', 'STD', 'KNW', 'WF', 'ENF', 'IN', '—'];
const SCOPES = ['common', 'backend', 'backend-tests', 'frontend', 'delivery', 'repo/meta'];
const RULE_SCOPE_DIRS = ['common', 'backend', 'backend-tests', 'frontend', 'delivery'];
const CANONICAL_GLOBS = {
  common: '**/*',
  backend: 'backend/**/*',
  'backend-tests': 'backend/**/*Tests/**/*',
  frontend: 'frontend/**/*',
  delivery: null, // delivery rules declare their own CI/container globs
};
const SCOPE_PARENT = { 'backend-tests': 'backend', backend: 'common', frontend: 'common', delivery: 'common', 'repo/meta': 'common', common: null };
const RANK = { OP: 0, DEC: 1, STD: 2, KNW: 3, WF: 4 };
// ENF conformance targets (ENF -> STD / DEC); ENF is not part of the Markdown rank chain.
const ENF_TARGET_KINDS = ['STD', 'DEC'];
// Capability-slot identity of this instruction system. The required leaf -> frame bindings are fixed here, independent of contract or manifest prose.
const SLOTS = {
  architecture: { cardinality: 'required', type: 'required frame', binds: [] },
  persistence: { cardinality: 'required', type: 'required leaf', binds: ['architecture'] },
  'backend-testing': { cardinality: 'required', type: 'required leaf', binds: ['architecture'] },
  frontend: { cardinality: 'optional', type: 'optional leaf', binds: [] },
};
const FRAME = 'architecture';
const REQUIRED_WORKFLOWS = ['project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings', 'git-workflow',
  'security-scan', 'add-dependency', 'architecture-decision', 'template-maintenance'];
// Non-slot knowledge skills; slot knowledge facets are required through their contracts and manifests.
const REQUIRED_KNOWLEDGE = ['http-api', 'aspnet-error-handling', 'logging', 'httpclient-factory', 'configuration',
  'dependency-injection', 'caching', 'swagger', 'api-versioning', 'health-check', 'docker', 'ci-cd', 'modern-csharp', 'authentication'];
const FORBIDDEN_SKILLS = ['serilog', 'resilience'];
const ROOT_ARTIFACTS = ['CLAUDE.md', 'CUSTOM_SETTINGS.md', 'SPECIFICATION.md', '.editorconfig', 'Directory.Build.props', 'Directory.Packages.props'];
const REGISTER = 'docs/architecture/decision-register.md';
// Project-owned files that evolve with the product: header problems are warnings and the leak rule does not apply.
const PROJECT_OWNED = ['SPECIFICATION.md', 'CUSTOM_SETTINGS.md', '.editorconfig', 'Directory.Build.props', 'Directory.Packages.props'];
const MAP = '.claude/MAP.md';
const DISPATCHER = '.claude/hooks/dispatch.cjs';
const LAUNCHER = '${CLAUDE_PROJECT_DIR}/.claude/hooks/dispatch.cjs';
// Required hook coverage: event -> matcher tools; the dependency/reference guard is the only fail-closed hook.
const REQUIRED_HOOKS = {
  PreToolUse: { tools: ['Bash', 'PowerShell'], critical: true },
  PostToolUse: { tools: ['Edit', 'Write', 'MultiEdit', 'Bash', 'PowerShell'] },
  PostToolUseFailure: { tools: ['Bash', 'PowerShell'] },
  Stop: { tools: null },
};
const BUDGET_WARN_TOKENS = 6000;

const ERR = 'error';
const WARN = 'warn';

// ---------- collection and parsing ----------

function collect(root) {
  const files = new Set();
  for (const rel of ROOT_ARTIFACTS) if (lib.exists(root, rel)) files.add(rel);
  if (lib.exists(root, REGISTER)) files.add(REGISTER);
  for (const rel of lib.walk(root, '.claude', r => !r.endsWith('settings.local.json'))) files.add(rel);
  return [...files].sort();
}

function splitFrontmatter(text) {
  const m = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/.exec(text);
  if (!m) return { frontmatter: null, body: text };
  return { frontmatter: m[1], body: text.slice(m[0].length) };
}

function frontmatterValue(fm, key) {
  if (!fm) return null;
  const lines = fm.split(/\r?\n/);
  const idx = lines.findIndex(l => new RegExp(`^${key}:`).test(l));
  if (idx < 0) return null;
  const inline = lines[idx].slice(key.length + 1).trim();
  if (inline && inline !== '>' && inline !== '|') return inline.replace(/^["']|["']$/g, '');
  const block = [];
  for (let i = idx + 1; i < lines.length && /^\s+\S/.test(lines[i]); i++) block.push(lines[i].trim());
  return block.join(' ');
}

function frontmatterList(fm, key) {
  if (!fm) return [];
  const lines = fm.split(/\r?\n/);
  const idx = lines.findIndex(l => new RegExp(`^${key}:`).test(l));
  if (idx < 0) return [];
  const inline = lines[idx].slice(key.length + 1).trim();
  if (inline) return inline.replace(/^\[|\]$/g, '').split(',').map(s => s.trim().replace(/^["']|["']$/g, '')).filter(Boolean);
  const items = [];
  for (let i = idx + 1; i < lines.length && /^\s+-/.test(lines[i]); i++) items.push(lines[i].replace(/^\s+-\s*/, '').replace(/^["']|["']$/g, ''));
  return items;
}

const HEADER_RE = /^(?:>|\/\/|#|<!--)\s*Kind:\s*(\S+)(?:\s*\([^)]*\))?\s*\|\s*Scope:\s*([\w/-]+)\s*\|\s*Capability:\s*([^|]+?)\s*\|\s*Loading:\s*(.+?)\s*(?:-->)?\s*$/;
const CONFORMS_RE = /^(?:\/\/|#|<!--)\s*Conforms:\s*(.*?)\s*(?:-->)?\s*$/;

function contentLines(body) {
  return body.split(/\r?\n/).filter(l => l.trim() !== '');
}

function parseHeader(body) {
  const line = contentLines(body)[0];
  if (!line) return null;
  const m = HEADER_RE.exec(line.trim());
  if (!m) return { raw: line, invalid: true };
  const capability = m[3].trim().split(/\s+/)[0];
  return { raw: line, kind: m[1], scope: m[2], capability, loading: m[4] };
}

/** ENF conformance declaration on the line after the header: list of owner paths, [] for "—", null when absent. */
function parseConforms(body) {
  const line = contentLines(body)[1];
  const m = line ? CONFORMS_RE.exec(line.trim()) : null;
  if (!m) return null;
  const value = m[1].trim();
  return value === '—' ? [] : value.split(',').map(s => s.trim()).filter(Boolean);
}

function expectedKind(rel) {
  if (rel === 'CLAUDE.md') return ['OP'];
  if (rel === REGISTER) return ['DEC'];
  if (rel === 'CUSTOM_SETTINGS.md' || rel === 'SPECIFICATION.md') return ['IN'];
  if (rel === MAP || /^\.claude\/capabilities\/.+\/(CONTRACT|MODULE)\.md$/.test(rel)) return ['—'];
  if (/^\.claude\/rules\//.test(rel)) return ['STD'];
  if (/^\.claude\/skills\//.test(rel)) return ['KNW', 'WF'];
  if (/^\.claude\/agents\//.test(rel)) return ['WF'];
  if (/^\.claude\/(hooks|scripts)\//.test(rel) || ['.editorconfig', 'Directory.Build.props', 'Directory.Packages.props'].includes(rel)) return ['ENF'];
  return null;
}

function parseAll(root, files) {
  const artifacts = new Map();
  for (const rel of files) {
    if (rel === '.claude/settings.json') continue; // hook registration (JSON): validated by checkSettings
    const kinds = expectedKind(rel);
    if (!kinds) continue;
    const text = lib.readText(root, rel);
    const { frontmatter, body } = rel.endsWith('.md') ? splitFrontmatter(text) : { frontmatter: null, body: text };
    artifacts.set(rel, { rel, text, frontmatter, body, kinds, header: rel === 'SPECIFICATION.md' ? null : parseHeader(body) });
  }
  return artifacts;
}

const validHeader = a => a && a.header && !a.header.invalid;

// ---------- checks ----------

function checkHeaders(artifacts, out) {
  for (const a of artifacts.values()) {
    if (a.rel === 'SPECIFICATION.md') continue; // product input; intentionally empty in the template
    if (!validHeader(a)) {
      out.push(lib.finding(PROJECT_OWNED.includes(a.rel) ? WARN : ERR, a.rel, 'missing or malformed header "Kind | Scope | Capability | Loading" on the first content line'));
      continue;
    }
    if (/\bLevel\s*:/.test(a.header.raw)) out.push(lib.finding(ERR, a.rel, 'Level headers are not part of this instruction system'));
    if (!KINDS.includes(a.header.kind)) out.push(lib.finding(ERR, a.rel, `unknown Kind "${a.header.kind}"`));
    else if (!a.kinds.includes(a.header.kind)) out.push(lib.finding(ERR, a.rel, `Kind ${a.header.kind} is not allowed at this location (expected ${a.kinds.join('/')})`));
    if (!SCOPES.includes(a.header.scope)) out.push(lib.finding(ERR, a.rel, `unknown Scope "${a.header.scope}"`));
    const cap = a.header.capability;
    if (cap !== '—' && !/^[a-z-]+(\/[a-z0-9-]+)?$/.test(cap)) out.push(lib.finding(ERR, a.rel, `malformed Capability "${cap}"`));
  }
}

function checkRules(root, artifacts, out) {
  for (const dir of lib.walk(root, '.claude/rules').map(r => r.split('/')[2]).filter(Boolean)) {
    if (!RULE_SCOPE_DIRS.includes(dir)) out.push(lib.finding(ERR, `.claude/rules/${dir}`, 'rules are organized only by scope directory'));
  }
  for (const a of artifacts.values()) {
    if (!a.rel.startsWith('.claude/rules/')) continue;
    const parts = a.rel.split('/');
    if (parts.length !== 4) {
      out.push(lib.finding(ERR, a.rel, 'rule files live directly in .claude/rules/<scope>/ (no deeper hierarchy)'));
      continue;
    }
    const scope = parts[2];
    if (validHeader(a) && a.header.scope !== scope) out.push(lib.finding(ERR, a.rel, `header Scope "${a.header.scope}" differs from directory scope "${scope}"`));
    const paths = frontmatterList(a.frontmatter, 'paths');
    if (!paths.length) {
      out.push(lib.finding(ERR, a.rel, 'rule must declare frontmatter paths'));
      continue;
    }
    const canonical = CANONICAL_GLOBS[scope];
    if (canonical && !paths.includes(canonical)) out.push(lib.finding(ERR, a.rel, `paths must include the scope's canonical glob "${canonical}"`));
    a.paths = paths;
  }
}

function checkImports(root, artifacts, out) {
  const claude = artifacts.get('CLAUDE.md');
  if (!claude) {
    out.push(lib.finding(ERR, 'CLAUDE.md', 'missing'));
    return [];
  }
  const imports = claude.body.split(/\r?\n/).map(l => /^@(\S+)\s*$/.exec(l.trim())).filter(Boolean).map(m => lib.toPosix(path.posix.normalize(m[1])));
  if (!imports.includes(REGISTER)) out.push(lib.finding(ERR, 'CLAUDE.md', `must import the decision register (@${REGISTER})`));
  for (const imp of imports) {
    const target = artifacts.get(imp);
    if (!lib.exists(root, imp)) out.push(lib.finding(ERR, 'CLAUDE.md', `import does not resolve: @${imp}`));
    else if (!validHeader(target) || !['OP', 'DEC'].includes(target.header.kind)) out.push(lib.finding(ERR, 'CLAUDE.md', `only OP/DEC artifacts may be imported into the always-loaded surface: @${imp}`));
  }
  for (const a of artifacts.values()) {
    if (a.rel === 'CLAUDE.md' || !a.rel.endsWith('.md')) continue;
    if (/^@[\w.\/-]+\.md\s*$/m.test(a.body)) out.push(lib.finding(ERR, a.rel, 'only CLAUDE.md may contain @ imports'));
  }
  return imports;
}

function skillsOf(artifacts) {
  const skills = new Map();
  for (const a of artifacts.values()) {
    const m = /^\.claude\/skills\/([^/]+)\/SKILL\.md$/.exec(a.rel);
    if (m) skills.set(m[1], a);
  }
  return skills;
}

function checkSkills(root, artifacts, skills, out) {
  for (const dir of new Set(lib.walk(root, '.claude/skills').map(r => r.split('/')[2]))) {
    if (!skills.has(dir)) out.push(lib.finding(ERR, `.claude/skills/${dir}`, 'skill directory without SKILL.md'));
  }
  for (const [name, a] of skills) {
    if (frontmatterValue(a.frontmatter, 'name') !== name) out.push(lib.finding(ERR, a.rel, `frontmatter name must equal the directory name "${name}"`));
    const description = frontmatterValue(a.frontmatter, 'description') || '';
    if (!description) out.push(lib.finding(ERR, a.rel, 'frontmatter description is required'));
    else if (description.length > 450) out.push(lib.finding(WARN, a.rel, `description is long (${description.length} chars); keep it concise and trigger-first`));
    if (FORBIDDEN_SKILLS.includes(name)) out.push(lib.finding(ERR, a.rel, `standalone "${name}" skill competes with its owning knowledge skill; use a private reference`));
    const userOnly = frontmatterValue(a.frontmatter, 'disable-model-invocation') === 'true';
    if (name === 'template-maintenance' && !userOnly) out.push(lib.finding(ERR, a.rel, 'template-maintenance must set disable-model-invocation: true'));
  }
  for (const name of REQUIRED_WORKFLOWS) {
    const a = skills.get(name);
    if (!a) out.push(lib.finding(ERR, `.claude/skills/${name}/SKILL.md`, 'required workflow is missing'));
    else if (a.header && a.header.kind !== 'WF') out.push(lib.finding(ERR, a.rel, 'required workflow must be Kind WF'));
  }
  for (const name of REQUIRED_KNOWLEDGE) {
    const a = skills.get(name);
    if (!a) out.push(lib.finding(ERR, `.claude/skills/${name}/SKILL.md`, 'required knowledge skill is missing'));
    else if (a.header && a.header.kind !== 'KNW') out.push(lib.finding(ERR, a.rel, 'required knowledge skill must be Kind KNW'));
  }
}

function checkAgent(artifacts, out) {
  const rel = '.claude/agents/code-reviewer.md';
  const a = artifacts.get(rel);
  if (!a) {
    out.push(lib.finding(ERR, rel, 'code-reviewer agent is missing'));
    return;
  }
  const disallowed = (frontmatterValue(a.frontmatter, 'disallowedTools') || '').split(/[,\s]+/);
  for (const tool of ['Write', 'Edit']) if (!disallowed.includes(tool)) out.push(lib.finding(ERR, rel, `read-only reviewer must disallow ${tool}`));
  if (!/`code-review`/.test(a.body)) out.push(lib.finding(ERR, rel, 'agent must delegate to the code-review workflow'));
  const lines = a.body.split(/\r?\n/).filter(l => l.trim()).length;
  if (lines > 15) out.push(lib.finding(WARN, rel, `agent body has ${lines} lines; keep it a thin delegate`));
}

// ---------- references and dependency direction ----------

function resolveReference(root, artifacts, from, token, basenameIndex, dormant) {
  if (/[<>*{}\s]/.test(token) || /^https?:/.test(token)) return null;
  if (/^(\.claude\/|docs\/architecture\/)/.test(token) || ROOT_ARTIFACTS.includes(token)) {
    return { target: token.replace(/\/$/, ''), checked: true };
  }
  if (/^references\/[\w.-]+\.md$/.test(token)) {
    const skillDir = (/^(\.claude\/skills\/[^/]+)\//.exec(from) || [])[1];
    return skillDir ? { target: `${skillDir}/${token}`, checked: true } : { target: token, checked: true, missing: true };
  }
  if (/^[\w.-]+\.(md|cjs)$/.test(token)) {
    const sibling = path.posix.join(path.posix.dirname(from), token);
    if (lib.exists(root, sibling)) return { target: sibling, checked: true };
    const candidates = basenameIndex.get(token) || [];
    if (candidates.length === 1) return { target: candidates[0], checked: true };
    if (dormant.has(sibling)) return { target: sibling, checked: true };
    return { target: token, checked: true, missing: true, ambiguous: candidates.length > 1 };
  }
  return null;
}

/**
 * Markdown references: invocable skill/agent names, SKILL.md paths, and references to ENF artifacts are routing or
 * enforcement pointers; references to other non-invocable files are conformance dependencies and must follow
 * WF -> KNW -> STD -> DEC -> OP. ENF conformance is declared explicitly (checkEnforcement).
 */
function checkReferences(root, artifacts, skills, dormant, graph, out) {
  const basenameIndex = new Map();
  for (const rel of artifacts.keys()) {
    const base = path.posix.basename(rel);
    basenameIndex.set(base, [...(basenameIndex.get(base) || []), rel]);
  }
  const agents = new Set([...artifacts.keys()].filter(r => r.startsWith('.claude/agents/')).map(r => path.posix.basename(r, '.md')));
  const edges = [];
  for (const a of artifacts.values()) {
    if (!a.rel.endsWith('.md') || (a.header && a.header.kind === '—')) continue; // manifests and the map list facets; they are not dependents
    const tokens = [...a.body.matchAll(/`([^`\n]+)`/g)].map(m => m[1].trim());
    for (const token of tokens) {
      if (skills.has(token) || agents.has(token)) {
        graph.pointers.push({ from: a.rel, to: token, type: 'routing' });
        continue;
      }
      const ref = resolveReference(root, artifacts, a.rel, token, basenameIndex, dormant);
      if (!ref) {
        if (/^[a-z][a-z0-9]*(-[a-z0-9]+)+$/.test(token) && new RegExp(`\`${token}\`\\s+(workflow|skill)|run\\s+\`${token}\``, 'i').test(a.body)) {
          out.push(lib.finding(ERR, a.rel, `reference to unknown skill \`${token}\``));
        }
        continue;
      }
      if (dormant.has(ref.target) && !lib.exists(root, ref.target)) {
        graph.pointers.push({ from: a.rel, to: ref.target, type: 'dormant facet role' });
        continue;
      }
      if (ref.missing || !lib.exists(root, ref.target)) {
        out.push(lib.finding(ERR, a.rel, `${ref.ambiguous ? 'ambiguous' : 'unresolved'} reference \`${token}\``));
        continue;
      }
      edges.push({ from: a.rel, to: ref.target });
    }
  }
  const kindOf = rel => (validHeader(artifacts.get(rel)) ? artifacts.get(rel).header.kind : null);
  const scopeOf = rel => (validHeader(artifacts.get(rel)) ? artifacts.get(rel).header.scope : null);
  for (const e of edges) {
    const priv = /^(\.claude\/skills\/[^/]+)\/references\//.exec(e.to);
    if (priv && !e.from.startsWith(`${priv[1]}/`)) {
      out.push(lib.finding(ERR, e.from, `skill-private reference ${e.to} is used outside its owning skill`));
      continue;
    }
    if (/\/SKILL\.md$/.test(e.to) || e.to.startsWith('.claude/agents/')) {
      graph.pointers.push({ from: e.from, to: e.to, type: 'routing' });
      continue;
    }
    const fromKind = kindOf(e.from);
    const toKind = kindOf(e.to);
    if (toKind === 'ENF') {
      graph.pointers.push({ from: e.from, to: e.to, type: 'enforcement' });
      continue;
    }
    if (!(fromKind in RANK) || !(toKind in RANK)) continue; // IN and maintenance metadata are not ranked
    if (RANK[toKind] > RANK[fromKind]) {
      out.push(lib.finding(ERR, e.from, `${fromKind} must not depend on ${toKind} artifact ${e.to} (direction WF -> KNW -> STD -> DEC -> OP)`));
      continue;
    }
    if (fromKind === 'STD' && toKind === 'STD' && !scopeCovers(scopeOf(e.to), scopeOf(e.from))) {
      out.push(lib.finding(ERR, e.from, `depends on ${e.to}, whose scope does not load reliably for "${scopeOf(e.from)}"`));
    }
    if (e.from !== e.to) graph.conformance.push({ from: e.from, to: e.to, fromKind, toKind });
  }
}

function scopeCovers(outer, inner) {
  for (let s = inner; s; s = SCOPE_PARENT[s]) if (s === outer) return true;
  return false;
}

function findCycle(edges) {
  const graph = new Map();
  for (const e of edges) graph.set(e.from, [...(graph.get(e.from) || []), e.to]);
  const state = new Map();
  const stack = [];
  const visit = node => {
    state.set(node, 1);
    stack.push(node);
    for (const next of graph.get(node) || []) {
      if (state.get(next) === 1) return [...stack.slice(stack.indexOf(next)), next];
      if (!state.has(next)) {
        const found = visit(next);
        if (found) return found;
      }
    }
    stack.pop();
    state.set(node, 2);
    return null;
  };
  for (const node of graph.keys()) {
    if (!state.has(node)) {
      const found = visit(node);
      if (found) return found;
    }
  }
  return null;
}

// ---------- ENF conformance (ENF -> STD / DEC) ----------

const OWNER_PATH_RE = /(?:\.claude\/rules\/(?:[\w-]+\/)+[\w.-]+\.md|docs\/architecture\/decision-register\.md)/g;

const slotOfCapability = cap => (cap && cap.includes('/') ? cap.split('/')[0] : null);

/** May an artifact of capability `from` conform to an owner of capability `to`? (neutral owners always; facets only within their module or a bound frame) */
function capabilityAllows(from, to) {
  if (!to.includes('/')) return true;
  if (!from.includes('/')) return false;
  if (from === to) return true;
  const fromSlot = slotOfCapability(from);
  return SLOTS[fromSlot] && SLOTS[fromSlot].type.endsWith('leaf') && slotOfCapability(to) === FRAME;
}

function checkEnforcement(root, artifacts, graph, out) {
  for (const a of artifacts.values()) {
    if (!validHeader(a) || a.header.kind !== 'ENF') continue;
    const severity = PROJECT_OWNED.includes(a.rel) ? WARN : ERR;
    const declared = parseConforms(a.body);
    if (declared === null) {
      out.push(lib.finding(severity, a.rel, 'ENF artifact lacks its conformance declaration ("Conforms: <STD/DEC owner>, ..." or "Conforms: —") on the line after the header'));
      continue;
    }
    for (const target of declared) {
      const t = artifacts.get(target);
      if (!t || !lib.exists(root, target)) {
        out.push(lib.finding(ERR, a.rel, `conformance target does not exist: ${target}`));
        continue;
      }
      if (!validHeader(t)) {
        out.push(lib.finding(ERR, a.rel, `conformance target has no valid header: ${target}`));
        continue;
      }
      if (!ENF_TARGET_KINDS.includes(t.header.kind)) {
        out.push(lib.finding(ERR, a.rel, `ENF must not depend on ${t.header.kind} artifact ${target} (direction ENF -> STD / DEC)`));
        continue;
      }
      if (!capabilityAllows(a.header.capability, t.header.capability)) {
        out.push(lib.finding(ERR, a.rel, `ENF of capability ${a.header.capability} must not conform to ${target} of capability ${t.header.capability} (neutral owners, its own module, or a bound frame only)`));
        continue;
      }
      graph.conformance.push({ from: a.rel, to: target, fromKind: 'ENF', toKind: t.header.kind });
    }
    const conformsLine = contentLines(a.body)[1];
    const cited = new Set([...a.body.replace(conformsLine, '').matchAll(OWNER_PATH_RE)].map(m => m[0]));
    for (const owner of cited) {
      if (!declared.includes(owner)) out.push(lib.finding(ERR, a.rel, `cites policy owner ${owner} but does not declare it in "Conforms:"`));
    }
  }
}

// ---------- capability slots ----------

function tableRows(text, heading) {
  const start = text.indexOf(heading);
  if (start < 0) return [];
  const rows = [];
  for (const line of text.slice(start + heading.length).split(/\r?\n/)) {
    if (/^#{1,6}\s/.test(line)) break;
    if (!/^\|/.test(line.trim()) || /^\|\s*-/.test(line.trim())) continue;
    rows.push(line.trim().replace(/^\||\|$/g, '').split('|').map(c => c.trim()));
  }
  return rows.slice(1); // drop the header row
}

function manifestField(text, field) {
  const m = new RegExp(`^- ${field}:\\s*(.+)$`, 'm').exec(text);
  return m ? m[1].trim() : null;
}

/** "- Binds:" value -> { slots, reason }; null when the line is missing. */
function parseBinds(value) {
  if (value === null) return null;
  if (/^(—|-|none)(\s|$)/i.test(value)) return { slots: [], reason: value.replace(/^(—|-|none)\s*/i, '') };
  const m = /^([a-z][a-z0-9-]*(?:\s*,\s*[a-z][a-z0-9-]*)*)\s*(.*)$/i.exec(value);
  if (!m) return { slots: [value], reason: '' };
  return { slots: m[1].split(',').map(s => s.trim()), reason: m[2].replace(/^[—(:-]\s*/, '').replace(/\)\s*$/, '').trim() };
}

const firstCode = cell => ((/`([^`]+)`/.exec(cell || '')) || [])[1] || null;

function registerSelection(artifacts, out) {
  const reg = artifacts.get(REGISTER);
  if (!reg) {
    out.push(lib.finding(ERR, REGISTER, 'decision register is missing'));
    return { selection: {}, knowledge: {}, block: '' };
  }
  const m = /<!-- slot-selection:begin -->([\s\S]*?)<!-- slot-selection:end -->/.exec(reg.body);
  if (!m) {
    out.push(lib.finding(ERR, REGISTER, 'capability-selection block markers are missing'));
    return { selection: {}, knowledge: {}, block: '' };
  }
  const selection = {};
  const knowledge = {};
  for (const line of m[1].split(/\r?\n/)) {
    const cells = line.trim().replace(/^\||\|$/g, '').split('|').map(c => c.trim());
    if (cells.length < 2) continue;
    const slot = cells[0].split(/\s+/)[0];
    if (!(slot in SLOTS)) continue;
    if (slot in selection) out.push(lib.finding(ERR, REGISTER, `slot "${slot}" has more than one selection row (static composition allows one)`));
    selection[slot] = cells[1].split(/[,\s]+/)[0];
    knowledge[slot] = firstCode(cells[2]) || (cells[2] || '—').trim();
  }
  return { selection, knowledge, block: m[0] };
}

function contractOf(artifacts, slot) {
  const rel = `.claude/capabilities/${slot}/CONTRACT.md`;
  const c = artifacts.get(rel);
  if (!c) return null;
  return {
    rel,
    type: manifestField(c.body, 'Slot type'),
    binds: parseBinds(manifestField(c.body, 'Binds')),
    roles: tableRows(c.body, '## Facet roles').map(([kind, scope, location]) => ({ kind, scope, file: firstCode(location) })),
    required: tableRows(c.body, '## Required items').map(r => firstCode(r[0])).filter(Boolean),
  };
}

/** Binding obligations: the slot identity (SLOTS) first, then contract and manifest agreement. */
function checkBinds(slot, file, binds, out) {
  const model = SLOTS[slot];
  if (binds === null) {
    out.push(lib.finding(ERR, file, `binding: "- Binds:" is missing (${model.binds.length ? `${slot} must bind ${model.binds.join(', ')}` : 'declare "—" when independent'})`));
    return;
  }
  const allowed = model.type.endsWith('leaf') ? [FRAME] : [];
  for (const s of binds.slots) {
    if (!(s in SLOTS)) out.push(lib.finding(ERR, file, `binding: "- Binds:" names unknown slot "${s}"`));
    else if (s === slot) out.push(lib.finding(ERR, file, 'binding: a slot cannot bind itself'));
    else if (!allowed.includes(s)) out.push(lib.finding(ERR, file, `binding: ${slot} (${model.type}) must not bind ${s}; only leaves bind, and only to the ${FRAME} frame`));
  }
  for (const r of model.binds) {
    if (!binds.slots.includes(r)) out.push(lib.finding(ERR, file, `binding: required ${model.type} binding "${slot} -> ${r}" is missing from "- Binds:"`));
  }
  if (binds.slots.length && !binds.reason) out.push(lib.finding(ERR, file, `binding: "- Binds: ${binds.slots.join(', ')}" must state the bound role or reason`));
}

function checkCapabilities(root, artifacts, sel, out) {
  const { selection, knowledge, block } = sel;
  const slotDirs = new Set(lib.walk(root, '.claude/capabilities').map(r => r.split('/')[2]));
  const modules = [];
  for (const dir of slotDirs) if (!(dir in SLOTS)) out.push(lib.finding(ERR, `.claude/capabilities/${dir}`, 'only the agreed capability slots may exist'));
  for (const [slot, model] of Object.entries(SLOTS)) {
    const base = `.claude/capabilities/${slot}`;
    const contract = contractOf(artifacts, slot);
    if (!contract) out.push(lib.finding(ERR, base, 'slot contract CONTRACT.md is missing'));
    else {
      if (contract.type !== model.type) out.push(lib.finding(ERR, contract.rel, `"- Slot type:" must be "${model.type}"`));
      checkBinds(slot, contract.rel, contract.binds, out);
      if (!contract.roles.length) out.push(lib.finding(ERR, contract.rel, '"## Facet roles" table is missing'));
    }
    const impls = [...new Set(lib.walk(root, base).map(r => r.split('/')).filter(p => p.length > 4).map(p => p[3]))];
    const selected = selection[slot];
    if (!selected) out.push(lib.finding(ERR, REGISTER, `no capability selection recorded for slot "${slot}"`));
    if (selected === 'none' && model.cardinality === 'required') out.push(lib.finding(ERR, REGISTER, `required slot "${slot}" cannot be "none"`));
    if (impls.length > 1) out.push(lib.finding(ERR, base, `multiple implementations present (${impls.join(', ')}); static composition allows one`));
    if (model.cardinality === 'required' && impls.length === 0) out.push(lib.finding(ERR, base, 'required slot has no implementation'));
    if (selected && selected !== 'none' && !impls.includes(selected)) out.push(lib.finding(ERR, base, `selected implementation "${selected}" has no module directory`));
    if (selected === 'none') {
      if (impls.length) out.push(lib.finding(ERR, base, 'selection is "none" but an implementation is present'));
      if (knowledge[slot] && knowledge[slot] !== '—') out.push(lib.finding(ERR, REGISTER, `slot "${slot}" is "none" but names knowledge facet "${knowledge[slot]}"`));
      for (const role of contract ? contract.roles : []) {
        if (role.file && role.kind !== 'DEC' && lib.exists(root, role.file)) out.push(lib.finding(ERR, role.file, `facet role of slot "${slot}" is present although the selection is "none"`));
      }
    }
    for (const impl of impls) {
      if (selected && impl !== selected) out.push(lib.finding(ERR, `${base}/${impl}`, 'unselected implementation must not be part of the runtime'));
      modules.push(checkModule(root, artifacts, slot, impl, contract, knowledge[slot], out));
    }
  }
  for (const mod of modules.filter(Boolean)) {
    const contract = contractOf(artifacts, mod.slot);
    if (contract && contract.binds && mod.binds && [...contract.binds.slots].sort().join() !== [...mod.binds.slots].sort().join()) {
      out.push(lib.finding(ERR, mod.manifest, `binding: "- Binds:" (${mod.binds.slots.join(', ') || '—'}) differs from the slot contract (${contract.binds.slots.join(', ') || '—'})`));
    }
  }
  for (const a of artifacts.values()) {
    const cap = validHeader(a) ? a.header.capability : '—';
    if (!cap.includes('/')) continue;
    const mod = modules.find(m => m && m.id === cap);
    if (!mod) out.push(lib.finding(ERR, a.rel, `declares Capability ${cap}, which is not a selected module`));
    else if (!mod.files.includes(a.rel) && !a.rel.startsWith(`.claude/capabilities/${cap}/`)) out.push(lib.finding(ERR, a.rel, `facet is not listed in ${mod.manifest}`));
  }
  checkLeaks(artifacts, modules.filter(Boolean), block, out);
}

function checkModule(root, artifacts, slot, impl, contract, knowledgeFacet, out) {
  const id = `${slot}/${impl}`;
  const manifest = `.claude/capabilities/${id}/MODULE.md`;
  const m = artifacts.get(manifest);
  if (!m) {
    out.push(lib.finding(ERR, manifest, 'module manifest is missing'));
    return null;
  }
  if (m.header && m.header.capability !== id) out.push(lib.finding(ERR, manifest, `header Capability must be ${id}`));
  if (manifestField(m.body, 'Slot') !== slot) out.push(lib.finding(ERR, manifest, `"- Slot:" must be ${slot}`));
  if (manifestField(m.body, 'Implementation') !== impl) out.push(lib.finding(ERR, manifest, `"- Implementation:" must be ${impl}`));
  const names = (manifestField(m.body, 'Names') || '').split(',').map(s => s.trim()).filter(Boolean);
  if (!names.length) out.push(lib.finding(ERR, manifest, '"- Names:" (leak-check tokens) is required'));
  const binds = parseBinds(manifestField(m.body, 'Binds'));
  checkBinds(slot, manifest, binds, out);

  const files = [];
  const rows = [];
  for (const row of tableRows(m.body, '## Facets')) {
    const [kind, scope, fileCell] = row;
    const file = firstCode(fileCell);
    if (!file) {
      out.push(lib.finding(ERR, manifest, `facet row without a file: ${row.join(' | ')}`));
      continue;
    }
    rows.push({ kind, scope, file });
    if (!lib.exists(root, file)) {
      out.push(lib.finding(ERR, manifest, `facet file does not exist: ${file}`));
      continue;
    }
    if (kind === 'DEC') {
      if (file !== REGISTER) out.push(lib.finding(ERR, manifest, 'the DEC facet is the decision register capability-selection block'));
      continue;
    }
    files.push(file);
    const a = artifacts.get(file);
    if (!validHeader(a)) continue;
    const h = a.header;
    if (h.kind !== kind) out.push(lib.finding(ERR, file, `facet Kind ${h.kind} differs from manifest (${kind})`));
    if (h.scope !== scope) out.push(lib.finding(ERR, file, `facet Scope ${h.scope} differs from manifest (${scope})`));
    if (h.capability !== id) out.push(lib.finding(ERR, file, `facet must declare Capability: ${id}`));
    if (kind !== 'KNW') {
      const base = path.posix.basename(file).replace(/\.[^.]+$/, '').toLowerCase().replace(/[^a-z0-9]/g, '');
      const leaked = names.find(n => base.includes(n.toLowerCase().replace(/[^a-z0-9]/g, '')));
      if (leaked) out.push(lib.finding(ERR, file, `facet file name must be role-based, not "${leaked}"`));
    }
  }

  if (contract) {
    // Facet roles: the module provides exactly the contract's role-named locations (KNW: the register's knowledge facet).
    for (const role of contract.roles) {
      if (role.kind === 'KNW') {
        const expected = knowledgeFacet && knowledgeFacet !== '—' ? `.claude/skills/${knowledgeFacet}/SKILL.md` : null;
        if (!expected) out.push(lib.finding(ERR, REGISTER, `slot "${slot}" requires a knowledge facet named in its capability-selection row`));
        else if (!rows.some(r => r.kind === 'KNW' && r.file === expected && r.scope === role.scope)) out.push(lib.finding(ERR, manifest, `contract facet role KNW (${role.scope}) must be the register's knowledge facet ${expected}`));
        continue;
      }
      if (!role.file) continue;
      if (!rows.some(r => r.kind === role.kind && r.file === role.file && r.scope === role.scope)) out.push(lib.finding(ERR, manifest, `contract facet role ${role.kind} ${role.file} (${role.scope}) is not provided`));
    }
    for (const r of rows) {
      const declared = r.kind === 'KNW' ? contract.roles.some(role => role.kind === 'KNW') : contract.roles.some(role => role.file === r.file && role.kind === r.kind);
      if (!declared) out.push(lib.finding(ERR, manifest, `facet ${r.kind} ${r.file} is not a facet role of the slot contract`));
    }
    const coverage = new Map(tableRows(m.body, '## Contract coverage').map(r => [firstCode(r[0]), r[1] || '']));
    for (const item of contract.required) {
      const provided = (coverage.get(item) || '').trim();
      if (!provided) out.push(lib.finding(ERR, manifest, `contract item "${item}" has no provider`));
      else if (/^missing\b/i.test(provided)) out.push(lib.finding(ERR, manifest, `contract item "${item}" is missing; raise a Decision Request before selecting this implementation`));
    }
  }
  return { id, slot, impl, manifest, names, files, binds };
}

function escapeRegex(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function checkLeaks(artifacts, modules, registerBlock, out) {
  // Allowed: module facets and manifest, the maintainer map, the register's selection block and its accepted-decision log,
  // and project-owned product/build files (product inputs and package manifests legitimately name technologies).
  const reg = artifacts.get(REGISTER);
  const decisionLog = reg ? reg.text.slice(Math.max(0, reg.text.indexOf('## Accepted decisions'))) : '';
  for (const mod of modules) {
    const patterns = mod.names.map(n => ({ name: n, re: new RegExp(`(?<![A-Za-z0-9])${escapeRegex(n)}(?![A-Za-z0-9])`, 'i') }));
    for (const a of artifacts.values()) {
      if (mod.files.includes(a.rel) || a.rel.startsWith(`.claude/capabilities/${mod.id}/`) || a.rel === MAP || PROJECT_OWNED.includes(a.rel)) continue;
      const text = a.rel === REGISTER ? a.text.replace(registerBlock, '').replace(decisionLog, '') : a.text;
      const hit = patterns.find(p => p.re.test(text));
      if (hit) out.push(lib.finding(ERR, a.rel, `names the selected ${mod.slot} implementation ("${hit.name}") outside its module; refer to the slot/facet role`));
    }
  }
}

// ---------- map, settings, vocabulary, budget ----------

function checkMap(root, files, out) {
  if (!lib.exists(root, MAP)) {
    out.push(lib.finding(ERR, MAP, 'maintainer map is missing'));
    return;
  }
  const map = lib.readText(root, MAP);
  for (const rel of files) {
    if (rel === MAP) continue;
    if (!map.includes(`\`${rel}\``)) out.push(lib.finding(ERR, MAP, `artifact not listed: ${rel}`));
  }
  for (const m of map.matchAll(/`((?:\.claude\/|docs\/architecture\/)[^`\s<>*{}]+\.[a-z]+|CLAUDE\.md|SPECIFICATION\.md|CUSTOM_SETTINGS\.md|Directory\.(?:Build|Packages)\.props|\.editorconfig)`/g)) {
    if (!lib.exists(root, m[1])) out.push(lib.finding(ERR, MAP, `lists a missing artifact: ${m[1]}`));
  }
  for (const slot of Object.keys(SLOTS)) if (!new RegExp(`###\\s+${slot}\\b`).test(map)) out.push(lib.finding(ERR, MAP, `capability view lacks slot "${slot}"`));
}

function checkSettings(root, out) {
  const rel = '.claude/settings.json';
  if (!lib.exists(root, rel)) {
    out.push(lib.finding(ERR, rel, 'missing'));
    return;
  }
  let settings;
  try {
    settings = JSON.parse(lib.readText(root, rel));
  } catch (err) {
    out.push(lib.finding(ERR, rel, `invalid JSON (${err.message})`));
    return;
  }
  const hooks = settings.hooks || {};
  const dispatcher = lib.exists(root, DISPATCHER) ? lib.readText(root, DISPATCHER) : null;
  for (const event of Object.keys(hooks)) {
    if (!(event in REQUIRED_HOOKS)) out.push(lib.finding(ERR, rel, `unexpected hook event "${event}" (the dispatcher handles ${Object.keys(REQUIRED_HOOKS).join(', ')})`));
  }
  for (const [event, req] of Object.entries(REQUIRED_HOOKS)) {
    const groups = hooks[event];
    if (!Array.isArray(groups) || !groups.length) {
      out.push(lib.finding(ERR, rel, `${event} hook is missing`));
      continue;
    }
    const covered = new Set();
    for (const group of groups) {
      const where = `${event}${group.matcher ? ` [${group.matcher}]` : ''}`;
      const tools = String(group.matcher || '').split('|').map(s => s.trim()).filter(Boolean);
      if (req.tools && !tools.length) out.push(lib.finding(ERR, rel, `${where}: matcher must name ${req.tools.join('|')}`));
      if (!Array.isArray(group.hooks) || !group.hooks.length) {
        out.push(lib.finding(ERR, rel, `${where}: no hooks`));
        continue;
      }
      for (const hook of group.hooks) {
        const problems = [];
        if (hook.type !== 'command') problems.push('type must be "command"');
        if (hook.command !== 'node') problems.push(`must use exec form ("command": "node" with "args"), found command ${JSON.stringify(hook.command)}`);
        if (/\$|%[A-Za-z_]+%/.test(String(hook.command || ''))) problems.push('command relies on shell variable expansion');
        if (!Array.isArray(hook.args) || hook.args.length !== 2) {
          problems.push('"args" must be [launcher, event]');
        } else {
          if (hook.args[0] !== LAUNCHER) problems.push(`launcher argument must be "${LAUNCHER}" (found "${hook.args[0]}")`);
          else if (!dispatcher) problems.push(`hook target ${DISPATCHER} not found`);
          if (hook.args[1] !== event) problems.push(`dispatches "${hook.args[1]}" but is registered for ${event}`);
          else if (dispatcher && !new RegExp(`\\bEVENTS\\s*=\\s*\\{[^}]*\\b${event}\\s*:`).test(dispatcher)) problems.push(`${DISPATCHER} has no handler for ${event}`);
        }
        if (typeof hook.timeout !== 'number' || hook.timeout <= 0 || hook.timeout > 600) problems.push('needs a timeout in seconds (1-600)');
        if (req.critical && hook.onFailure !== 'block') problems.push('policy-critical hook must fail closed ("onFailure": "block")');
        if (!req.critical && hook.onFailure === 'block') problems.push('advisory hook must not block on failure');
        for (const p of problems) out.push(lib.finding(ERR, rel, `${where} hook: ${p}`));
        if (!problems.length) for (const t of tools) covered.add(t);
      }
    }
    for (const t of req.tools || []) {
      if (!covered.has(t)) out.push(lib.finding(ERR, rel, `${event} must cover ${t} with a valid hook (matcher)`));
    }
  }
}

function checkVocabulary(artifacts, out) {
  for (const a of artifacts.values()) {
    if (!a.header || !['OP', 'DEC', 'STD'].includes(a.header.kind)) continue;
    if (/\bnormally\b/i.test(a.body)) out.push(lib.finding(WARN, a.rel, 'ambiguous "normally" in normative text; use must/default/prefer'));
  }
}

function alwaysLoadedTokens(artifacts, skills, imports) {
  let chars = 0;
  for (const rel of ['CLAUDE.md', ...imports]) if (artifacts.get(rel)) chars += artifacts.get(rel).text.length;
  for (const [name, a] of skills) {
    if (frontmatterValue(a.frontmatter, 'disable-model-invocation') === 'true') continue;
    chars += name.length + (frontmatterValue(a.frontmatter, 'description') || '').length + 4;
  }
  for (const a of artifacts.values()) {
    if (a.rel.startsWith('.claude/agents/')) chars += (frontmatterValue(a.frontmatter, 'description') || '').length;
  }
  return Math.round(chars / 4);
}

/** Facet-role paths of optional slots selected "none": pointers to them from neutral artifacts are dormant, not broken. */
function dormantRolePaths(artifacts, selection) {
  const dormant = new Set();
  for (const [slot, model] of Object.entries(SLOTS)) {
    if (model.cardinality !== 'optional' || selection[slot] !== 'none') continue;
    const contract = contractOf(artifacts, slot);
    for (const role of contract ? contract.roles : []) if (role.file && role.kind !== 'DEC') dormant.add(role.file);
  }
  return dormant;
}

function check(root) {
  const out = [];
  const graph = { conformance: [], pointers: [] };
  const files = collect(root);
  const artifacts = parseAll(root, files);
  checkHeaders(artifacts, out);
  checkRules(root, artifacts, out);
  const imports = checkImports(root, artifacts, out);
  const skills = skillsOf(artifacts);
  checkSkills(root, artifacts, skills, out);
  checkAgent(artifacts, out);
  const sel = registerSelection(artifacts, out);
  checkReferences(root, artifacts, skills, dormantRolePaths(artifacts, sel.selection), graph, out);
  checkEnforcement(root, artifacts, graph, out);
  const cycle = findCycle(graph.conformance);
  if (cycle) out.push(lib.finding(ERR, cycle[0], `conformance dependency cycle: ${cycle.join(' -> ')}`));
  checkCapabilities(root, artifacts, sel, out);
  checkMap(root, files, out);
  checkSettings(root, out);
  checkVocabulary(artifacts, out);
  const tokens = alwaysLoadedTokens(artifacts, skills, imports);
  if (tokens > BUDGET_WARN_TOKENS) out.push(lib.finding(WARN, 'CLAUDE.md', `always-loaded surface is about ${tokens} tokens (target about 5k)`));
  out.budget = tokens;
  out.graph = graph;
  return out;
}

module.exports = { check };

if (require.main === module) {
  const root = lib.commandRoot(__dirname);
  const findings = check(root);
  if (findings.length) process.stdout.write(`${lib.formatFindings(findings)}\n`);
  const errors = findings.filter(f => f.severity === 'error').length;
  process.stdout.write(`check-instructions (${root}): ${errors} error(s), ${findings.length - errors} warning(s); always-loaded surface about ${findings.budget} tokens\n`);
  process.exitCode = errors ? 1 : 0;
}
