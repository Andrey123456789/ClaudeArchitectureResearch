// Kind: ENF | Scope: repo/meta | Capability: — | Loading: command (instruction-edit hook, verify, template-maintenance): node .claude/scripts/check-instructions.cjs
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
const SLOTS = { architecture: 'required', persistence: 'required', 'backend-testing': 'required', frontend: 'optional' };
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
const HOOK_EVENTS = ['pre-bash', 'post-edit', 'stop'];
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

function parseHeader(body) {
  const line = body.split(/\r?\n/).find(l => l.trim() !== '');
  if (!line) return null;
  const m = HEADER_RE.exec(line.trim());
  if (!m) return { raw: line, invalid: true };
  const capability = m[3].trim().split(/\s+/)[0];
  return { raw: line, kind: m[1], scope: m[2], capability, loading: m[4] };
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
    if (rel === '.claude/settings.json') continue;
    const kinds = expectedKind(rel);
    if (!kinds) continue;
    const text = lib.readText(root, rel);
    const { frontmatter, body } = rel.endsWith('.md') ? splitFrontmatter(text) : { frontmatter: null, body: text };
    artifacts.set(rel, { rel, text, frontmatter, body, kinds, header: rel === 'SPECIFICATION.md' ? null : parseHeader(body) });
  }
  return artifacts;
}

// ---------- checks ----------

function checkHeaders(artifacts, out) {
  for (const a of artifacts.values()) {
    if (a.rel === 'SPECIFICATION.md') continue; // product input; intentionally empty in the template
    if (!a.header || a.header.invalid) {
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
    if (a.header && !a.header.invalid && a.header.scope !== scope) out.push(lib.finding(ERR, a.rel, `header Scope "${a.header.scope}" differs from directory scope "${scope}"`));
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
    else if (!target || !target.header || !['OP', 'DEC'].includes(target.header.kind)) out.push(lib.finding(ERR, 'CLAUDE.md', `only OP/DEC artifacts may be imported into the always-loaded surface: @${imp}`));
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

function resolveReference(root, artifacts, from, token, basenameIndex) {
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
    return { target: token, checked: true, missing: true, ambiguous: candidates.length > 1 };
  }
  return null;
}

function checkReferences(root, artifacts, skills, out) {
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
      if (skills.has(token) || agents.has(token)) continue; // routing pointer to an invocable skill/agent
      const ref = resolveReference(root, artifacts, a.rel, token, basenameIndex);
      if (!ref) {
        if (/^[a-z][a-z0-9]*(-[a-z0-9]+)+$/.test(token) && new RegExp(`\`${token}\`\\s+(workflow|skill)|run\\s+\`${token}\``, 'i').test(a.body)) {
          out.push(lib.finding(ERR, a.rel, `reference to unknown skill \`${token}\``));
        }
        continue;
      }
      if (ref.missing || !lib.exists(root, ref.target)) {
        out.push(lib.finding(ERR, a.rel, `${ref.ambiguous ? 'ambiguous' : 'unresolved'} reference \`${token}\``));
        continue;
      }
      edges.push({ from: a.rel, to: ref.target });
    }
  }
  const kindOf = rel => {
    const t = artifacts.get(rel);
    return t && t.header && !t.header.invalid ? t.header.kind : null;
  };
  const scopeOf = rel => {
    const t = artifacts.get(rel);
    return t && t.header && !t.header.invalid ? t.header.scope : null;
  };
  const conformance = [];
  for (const e of edges) {
    const priv = /^(\.claude\/skills\/[^/]+)\/references\//.exec(e.to);
    if (priv && !e.from.startsWith(`${priv[1]}/`)) {
      out.push(lib.finding(ERR, e.from, `skill-private reference ${e.to} is used outside its owning skill`));
      continue;
    }
    if (/\/SKILL\.md$/.test(e.to) || e.to.startsWith('.claude/agents/')) continue; // pointer
    const fromKind = kindOf(e.from);
    const toKind = kindOf(e.to);
    if (!(fromKind in RANK) || !(toKind in RANK)) continue; // ENF, IN, and maintenance metadata are not ranked
    if (RANK[toKind] > RANK[fromKind]) {
      out.push(lib.finding(ERR, e.from, `${fromKind} must not depend on ${toKind} artifact ${e.to} (direction WF -> KNW -> STD -> DEC -> OP)`));
      continue;
    }
    if (fromKind === 'STD' && toKind === 'STD' && !scopeCovers(scopeOf(e.to), scopeOf(e.from))) {
      out.push(lib.finding(ERR, e.from, `depends on ${e.to}, whose scope does not load reliably for "${scopeOf(e.from)}"`));
    }
    if (e.from !== e.to) conformance.push(e);
  }
  const cycle = findCycle(conformance);
  if (cycle) out.push(lib.finding(ERR, cycle[0], `conformance dependency cycle: ${cycle.join(' -> ')}`));
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

function registerSelection(artifacts, out) {
  const reg = artifacts.get(REGISTER);
  if (!reg) {
    out.push(lib.finding(ERR, REGISTER, 'decision register is missing'));
    return { selection: {}, block: '' };
  }
  const m = /<!-- slot-selection:begin -->([\s\S]*?)<!-- slot-selection:end -->/.exec(reg.body);
  if (!m) {
    out.push(lib.finding(ERR, REGISTER, 'capability-selection block markers are missing'));
    return { selection: {}, block: '' };
  }
  const selection = {};
  for (const line of m[1].split(/\r?\n/)) {
    const cells = line.trim().replace(/^\||\|$/g, '').split('|').map(c => c.trim());
    if (cells.length < 2) continue;
    const slot = cells[0].split(/\s+/)[0];
    if (slot in SLOTS) selection[slot] = cells[1].split(/[,\s]+/)[0];
  }
  return { selection, block: m[0] };
}

function checkCapabilities(root, artifacts, out) {
  const { selection, block } = registerSelection(artifacts, out);
  const slotDirs = new Set(lib.walk(root, '.claude/capabilities').map(r => r.split('/')[2]));
  const modules = [];
  for (const dir of slotDirs) if (!(dir in SLOTS)) out.push(lib.finding(ERR, `.claude/capabilities/${dir}`, 'only the agreed capability slots may exist'));
  for (const [slot, cardinality] of Object.entries(SLOTS)) {
    const base = `.claude/capabilities/${slot}`;
    if (!lib.exists(root, `${base}/CONTRACT.md`)) out.push(lib.finding(ERR, base, 'slot contract CONTRACT.md is missing'));
    const impls = [...new Set(lib.walk(root, base).map(r => r.split('/')).filter(p => p.length > 4).map(p => p[3]))];
    const selected = selection[slot];
    if (!selected) out.push(lib.finding(ERR, REGISTER, `no capability selection recorded for slot "${slot}"`));
    if (impls.length > 1) out.push(lib.finding(ERR, base, `multiple implementations present (${impls.join(', ')}); static composition allows one`));
    if (cardinality === 'required' && impls.length === 0) out.push(lib.finding(ERR, base, 'required slot has no implementation'));
    if (selected && selected !== 'none' && !impls.includes(selected)) out.push(lib.finding(ERR, base, `selected implementation "${selected}" has no module directory`));
    if (selected === 'none' && impls.length) out.push(lib.finding(ERR, base, 'selection is "none" but an implementation is present'));
    for (const impl of impls) {
      if (selected && impl !== selected) out.push(lib.finding(ERR, `${base}/${impl}`, 'unselected implementation must not be part of the runtime'));
      modules.push(checkModule(root, artifacts, slot, impl, out));
    }
  }
  const owned = new Map();
  for (const mod of modules.filter(Boolean)) for (const f of mod.files) owned.set(f, mod);
  for (const a of artifacts.values()) {
    const cap = a.header && !a.header.invalid ? a.header.capability : '—';
    if (!cap.includes('/')) continue;
    const mod = modules.find(m => m && m.id === cap);
    if (!mod) out.push(lib.finding(ERR, a.rel, `declares Capability ${cap}, which is not a selected module`));
    else if (!mod.files.includes(a.rel) && !a.rel.startsWith(`.claude/capabilities/${cap}/`)) out.push(lib.finding(ERR, a.rel, `facet is not listed in ${mod.manifest}`));
  }
  checkLeaks(artifacts, modules.filter(Boolean), block, out);
}

function checkModule(root, artifacts, slot, impl, out) {
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
  const binds = manifestField(m.body, 'Binds') || '—';
  const bound = binds.split(/[\s—-]+/)[0];
  if (binds !== '—' && !(bound in SLOTS && bound !== slot)) out.push(lib.finding(ERR, manifest, `"- Binds:" must name another slot or be "—"`));

  const files = [];
  for (const row of tableRows(m.body, '## Facets')) {
    const [kind, scope, fileCell] = row;
    const file = ((/`([^`]+)`/.exec(fileCell || '')) || [])[1];
    if (!file) {
      out.push(lib.finding(ERR, manifest, `facet row without a file: ${row.join(' | ')}`));
      continue;
    }
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
    const h = a && a.header;
    if (!h || h.invalid) continue;
    if (h.kind !== kind) out.push(lib.finding(ERR, file, `facet Kind ${h.kind} differs from manifest (${kind})`));
    if (h.scope !== scope) out.push(lib.finding(ERR, file, `facet Scope ${h.scope} differs from manifest (${scope})`));
    if (h.capability !== id) out.push(lib.finding(ERR, file, `facet must declare Capability: ${id}`));
    if (kind !== 'KNW') {
      const base = path.posix.basename(file).replace(/\.[^.]+$/, '').toLowerCase().replace(/[^a-z0-9]/g, '');
      const leaked = names.find(n => base.includes(n.toLowerCase().replace(/[^a-z0-9]/g, '')));
      if (leaked) out.push(lib.finding(ERR, file, `facet file name must be role-based, not "${leaked}"`));
    }
  }

  const contract = artifacts.get(`.claude/capabilities/${slot}/CONTRACT.md`);
  if (contract) {
    const required = tableRows(contract.body, '## Required items').map(r => ((/`([^`]+)`/.exec(r[0])) || [])[1]).filter(Boolean);
    const coverage = new Map(tableRows(m.body, '## Contract coverage').map(r => [((/`([^`]+)`/.exec(r[0])) || [])[1], r[1] || '']));
    for (const item of required) {
      const provided = (coverage.get(item) || '').trim();
      if (!provided) out.push(lib.finding(ERR, manifest, `contract item "${item}" has no provider`));
      else if (/^missing\b/i.test(provided)) out.push(lib.finding(ERR, manifest, `contract item "${item}" is missing; raise a Decision Request before selecting this implementation`));
    }
  }
  return { id, slot, impl, manifest, names, files };
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
  for (const [event, groups] of Object.entries(settings.hooks || {})) {
    for (const group of groups) {
      for (const hook of group.hooks || []) {
        const cmd = hook.command || '';
        if (/\$|%[A-Za-z_]+%/.test(cmd)) out.push(lib.finding(ERR, rel, `${event} hook relies on shell variable expansion: ${cmd}`));
        if (!/^node\s/.test(cmd)) out.push(lib.finding(ERR, rel, `${event} hook must launch node directly (shell-neutral): ${cmd}`));
        const script = (/(\.claude\/hooks\/[\w.-]+\.cjs)/.exec(cmd) || [])[1];
        if (!script || !lib.exists(root, script)) out.push(lib.finding(ERR, rel, `${event} hook script not found: ${script || cmd}`));
        const evt = (/\.main\('([\w-]+)'\)/.exec(cmd) || [])[1];
        if (!HOOK_EVENTS.includes(evt)) out.push(lib.finding(ERR, rel, `${event} hook dispatches unknown event "${evt}"`));
      }
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

function check(root) {
  const out = [];
  const files = collect(root);
  const artifacts = parseAll(root, files);
  checkHeaders(artifacts, out);
  checkRules(root, artifacts, out);
  const imports = checkImports(root, artifacts, out);
  const skills = skillsOf(artifacts);
  checkSkills(root, artifacts, skills, out);
  checkAgent(artifacts, out);
  checkReferences(root, artifacts, skills, out);
  checkCapabilities(root, artifacts, out);
  checkMap(root, files, out);
  checkSettings(root, out);
  checkVocabulary(artifacts, out);
  const tokens = alwaysLoadedTokens(artifacts, skills, imports);
  if (tokens > BUDGET_WARN_TOKENS) out.push(lib.finding(WARN, 'CLAUDE.md', `always-loaded surface is about ${tokens} tokens (target about 5k)`));
  out.budget = tokens;
  return out;
}

module.exports = { check };

if (require.main === module) {
  const root = lib.rootFrom(__dirname, 2);
  const findings = check(root);
  if (findings.length) process.stdout.write(`${lib.formatFindings(findings)}\n`);
  const errors = findings.filter(f => f.severity === 'error').length;
  process.stdout.write(`check-instructions: ${errors} error(s), ${findings.length - errors} warning(s); always-loaded surface about ${findings.budget} tokens\n`);
  process.exitCode = errors ? 1 : 0;
}
