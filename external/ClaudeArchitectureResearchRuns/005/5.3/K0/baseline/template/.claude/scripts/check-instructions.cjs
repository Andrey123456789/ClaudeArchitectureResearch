// Kind: ENF | Scope: repo/meta | Owner: instruction-structure checker — Kind/Scope headers, mechanism per Kind, rule paths per scope, decision register integrity, references, dependency direction, skill privacy, hook commands, map coverage | Loading: run by /template-maintenance and the post-edit hook
//
// Usage: node .claude/scripts/check-instructions.cjs   (exit 1 when a structural problem is found)
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');

const KINDS = ['OP', 'DEC', 'STD', 'KNW', 'WF', 'ENF', 'IN'];
const SCOPES = ['common', 'backend', 'backend-tests', 'frontend', 'delivery', 'repo/meta'];
const RULE_SCOPES = ['common', 'backend', 'backend-tests', 'frontend', 'delivery'];
const REQUIRED_WORKFLOWS = ['development-workflow', 'project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings', 'git-workflow', 'security-scan', 'add-dependency', 'architecture-decision', 'delivery-pipeline', 'template-maintenance'];
const REQUIRED_KNOWLEDGE = ['ef-core', 'http-api', 'aspnet-error-handling', 'dotnet-testing', 'logging', 'httpclient-factory', 'configuration', 'dependency-injection', 'caching', 'swagger', 'api-versioning', 'health-check', 'docker', 'ci-cd', 'angular', 'modern-csharp', 'authentication'];
const USER_ONLY_WORKFLOWS = ['template-maintenance'];
const RETIRED_SKILL_NAMES = ['testing', 'error-handling', 'serilog', 'resilience'];
const NON_SKILL_TOKENS = new Set(['pre-tool-use', 'post-tool-use', 'code-reviewer', 'lodash-es', 'kebab-case', 'repo/meta']);
const ROOT_FILES = ['CLAUDE.md', 'SPECIFICATION.md', 'CUSTOM_SETTINGS.md', 'Directory.Build.props', 'Directory.Packages.props', '.editorconfig'];
const REGISTER = 'docs/architecture/decision-register.md';
const MAP = '.claude/MAP.md';
const MD_HEADER = /^> Kind: (\S+) \| Scope: (\S+) \| Owner: (.+?) \| Loading: (.+)$/;
const CODE_HEADER = /^(?:\/\/|#|<!--)\s*Kind: (\S+) \| Scope: (\S+) \| Owner: (.+?) \| Loading: (.+?)(?:\s*-->)?$/;
const ROUTING_PREFIX = /^\s*(?:[-*]\s*)?(?:See also|Workflow|Technique|Procedure|Enforced by):/;

const errors = [];
const info = [];
const err = (file, message) => errors.push(`${file}: ${message}`);

function exists(rel) {
  return fs.existsSync(path.join(ROOT, rel));
}

function read(rel) {
  return fs.readFileSync(path.join(ROOT, rel), 'utf8').replace(/\r\n/g, '\n');
}

function walk(relDir, out = []) {
  const abs = path.join(ROOT, relDir);
  if (!fs.existsSync(abs)) return out;
  for (const entry of fs.readdirSync(abs, { withFileTypes: true })) {
    const rel = relDir ? `${relDir}/${entry.name}` : entry.name;
    if (entry.isDirectory()) {
      if (!['.hook-state', 'node_modules', '.git', 'bin', 'obj', 'dist'].includes(entry.name)) walk(rel, out);
    } else {
      out.push(rel);
    }
  }
  return out;
}

function splitFrontmatter(text) {
  if (!text.startsWith('---\n')) return { fm: null, body: text };
  const end = text.indexOf('\n---\n', 4);
  if (end < 0) return { fm: null, body: text };
  return { fm: text.slice(4, end), body: text.slice(end + 5) };
}

function parseFrontmatter(fm) {
  const result = {};
  if (!fm) return result;
  let currentKey = null;
  for (const line of fm.split('\n')) {
    const item = line.match(/^\s+-\s+(.*)$/);
    if (item && currentKey) {
      result[currentKey] = [].concat(result[currentKey] || [], item[1].replace(/^["']|["']$/g, ''));
      continue;
    }
    const kv = line.match(/^([A-Za-z][\w-]*):\s*(.*)$/);
    if (kv) {
      currentKey = kv[1];
      result[currentKey] = kv[2] === '' ? [] : kv[2].replace(/^["']|["']$/g, '');
    }
  }
  return result;
}

function withoutCodeFences(text) {
  return text.replace(/```[\s\S]*?```/g, (block) => block.replace(/[^\n]/g, ' '));
}

// ---------------------------------------------------------------------------
// Artifact list
// ---------------------------------------------------------------------------

const files = [...walk('.claude'), ...walk('docs'), ...ROOT_FILES.filter(exists)];
const artifacts = []; // { rel, expectedKind, kind, scope, owner, loading, fm, body }

function classify(rel) {
  if (rel === 'CLAUDE.md') return 'OP';
  if (rel === REGISTER) return 'DEC';
  if (rel === 'CUSTOM_SETTINGS.md') return 'IN';
  if (/^\.claude\/rules\/.+\.md$/.test(rel)) return 'STD';
  if (/^\.claude\/skills\/[^/]+\/SKILL\.md$/.test(rel)) return 'SKILL';
  if (/^\.claude\/skills\/[^/]+\/references\/.+\.md$/.test(rel)) return 'REFERENCE';
  if (/^\.claude\/agents\/[^/]+\.md$/.test(rel)) return 'WF';
  if (/^\.claude\/(hooks|scripts)\/[^/]+\.cjs$/.test(rel) || ['.editorconfig', 'Directory.Build.props', 'Directory.Packages.props'].includes(rel)) return 'ENF-CODE';
  return null;
}

const ignored = new Set(['SPECIFICATION.md', MAP, '.claude/settings.json', '.claude/settings.local.json']);
for (const rel of files) {
  if (ignored.has(rel) || rel.startsWith('docs/decisions/')) continue;
  const cls = classify(rel);
  if (!cls) {
    if (rel.startsWith('.claude/') || rel.startsWith('docs/architecture/')) err(rel, 'unclassified file in the instruction system; place it by Kind and Scope (see .claude/MAP.md).');
    continue;
  }
  const text = read(rel);
  if (cls === 'ENF-CODE') {
    const m = text.split('\n')[0].match(CODE_HEADER);
    if (!m && ROOT_FILES.includes(rel)) continue; // project-owned build/format file edited without the template header
    if (!m) { err(rel, 'missing first-line header "Kind: ENF | Scope: … | Owner: … | Loading: …".'); continue; }
    artifacts.push({ rel, expectedKind: 'ENF', kind: m[1], scope: m[2], owner: m[3], loading: m[4], fm: {}, body: text });
    continue;
  }
  const { fm, body } = splitFrontmatter(text);
  const firstLine = body.split('\n').find((l) => l.trim() !== '') || '';
  const m = firstLine.match(MD_HEADER);
  if (!m) { err(rel, 'first body line must be the header "> Kind: … | Scope: … | Owner: … | Loading: …".'); continue; }
  artifacts.push({ rel, expectedKind: cls, kind: m[1], scope: m[2], owner: m[3], loading: m[4], fm: parseFrontmatter(fm), body });
}

const byRel = new Map(artifacts.map((a) => [a.rel, a]));
const skillDirs = fs.existsSync(path.join(ROOT, '.claude/skills'))
  ? fs.readdirSync(path.join(ROOT, '.claude/skills'), { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name)
  : [];
const agentNames = walk('.claude/agents').map((f) => path.basename(f, '.md'));

// ---------------------------------------------------------------------------
// Kind, Scope and mechanism
// ---------------------------------------------------------------------------

for (const a of artifacts) {
  if (!KINDS.includes(a.kind)) err(a.rel, `unknown Kind "${a.kind}".`);
  if (!SCOPES.includes(a.scope)) err(a.rel, `unknown Scope "${a.scope}".`);
  if (/(^\s*>?\s*|\| )Level:\s/m.test(a.kind === 'ENF' ? '' : withoutCodeFences(a.body))) err(a.rel, 'contains a "Level:" field; this system classifies by Kind and Scope only.');
  const loading = a.loading.toLowerCase();

  if (['OP', 'DEC', 'IN', 'STD', 'WF', 'ENF'].includes(a.expectedKind) && a.kind !== a.expectedKind) {
    err(a.rel, `Kind ${a.kind} does not match its location (expected ${a.expectedKind}).`);
  }
  if ((a.expectedKind === 'OP' || a.expectedKind === 'DEC') && !loading.includes('always')) err(a.rel, 'OP/DEC must load always.');

  if (a.expectedKind === 'STD') {
    const dir = a.rel.split('/')[2];
    if (a.rel.split('/').length !== 4) err(a.rel, 'standards live directly in .claude/rules/<scope>/<topic>.md.');
    if (!RULE_SCOPES.includes(dir)) err(a.rel, `rules directory "${dir}" is not a scope (${RULE_SCOPES.join(', ')}).`);
    if (dir !== a.scope) err(a.rel, `Scope ${a.scope} does not match its directory ${dir}.`);
    if (!loading.includes('path-scoped')) err(a.rel, 'STD must be path-scoped.');
    const globs = [].concat(a.fm.paths || []);
    if (globs.length === 0) err(a.rel, 'rule must declare non-empty "paths".');
    for (const g of globs) if (!globInScope(g, a.scope)) err(a.rel, `path glob "${g}" is outside the ${a.scope} scope territory.`);
    checkNoProcedure(a);
  }

  if (a.expectedKind === 'SKILL') {
    const name = a.rel.split('/')[2];
    if (a.fm.name !== name) err(a.rel, `frontmatter name "${a.fm.name}" must equal the directory name "${name}".`);
    if (!a.fm.description || String(a.fm.description).length < 20) err(a.rel, 'skill needs a concrete description.');
    const userOnly = String(a.fm['disable-model-invocation']).toLowerCase() === 'true';
    if (a.kind === 'KNW') {
      if (!loading.includes('on demand')) err(a.rel, 'KNW must load on demand.');
      if (userOnly) err(a.rel, 'knowledge skills must stay model-invocable.');
      if (REQUIRED_WORKFLOWS.includes(name)) err(a.rel, `"${name}" is a workflow and must be Kind WF.`);
      checkKnowledgeHasNoBareNorms(a);
    } else if (a.kind === 'WF') {
      if (!loading.includes('workflow')) err(a.rel, 'WF must load as a workflow.');
      if (REQUIRED_KNOWLEDGE.includes(name)) err(a.rel, `"${name}" is a knowledge skill and must be Kind KNW.`);
      if (USER_ONLY_WORKFLOWS.includes(name) && !userOnly) err(a.rel, 'user-only workflow must set disable-model-invocation: true.');
    } else {
      err(a.rel, 'skills are Kind WF or KNW.');
    }
  }

  if (a.expectedKind === 'REFERENCE') {
    const owner = byRel.get(`.claude/skills/${a.rel.split('/')[2]}/SKILL.md`);
    if (owner && owner.kind !== a.kind) err(a.rel, `private reference Kind ${a.kind} differs from its skill (${owner.kind}).`);
    if (!loading.includes('only')) err(a.rel, 'private reference must state that only its skill reads it.');
    if (a.kind === 'KNW') checkKnowledgeHasNoBareNorms(a);
  }

  if (a.rel.startsWith('.claude/agents/')) {
    const name = path.basename(a.rel, '.md');
    if (a.fm.name !== name) err(a.rel, `frontmatter name "${a.fm.name}" must equal the file name "${name}".`);
  }
}

function globInScope(glob, scope) {
  switch (scope) {
    case 'common': return true;
    case 'backend': return glob.startsWith('backend/') || ['Directory.Build.props', 'Directory.Packages.props', 'global.json', '*.slnx'].includes(glob);
    case 'backend-tests': return glob.startsWith('backend/') && glob.includes('Tests');
    case 'frontend': return glob.startsWith('frontend/');
    case 'delivery': return /Dockerfile|docker|compose|\.github\/|pipeline|gitlab-ci/i.test(glob);
    default: return false;
  }
}

function checkNoProcedure(a) {
  withoutCodeFences(a.body).split('\n').forEach((line, i) => {
    if (/^\s*\d+\.\s/.test(line) || /^#+\s*(Step|Procedure)\b/i.test(line)) err(a.rel, `line ${i + 1}: procedures belong in a workflow, not in a standard.`);
  });
}

function checkKnowledgeHasNoBareNorms(a) {
  withoutCodeFences(a.body).split('\n').forEach((line, i) => {
    if (/\b(must|never|requires approval)\b/i.test(line) && !/(rules\/|CLAUDE\.md|D-\d\d)/.test(line)) {
      err(a.rel, `line ${i + 1}: normative wording in knowledge without an owner reference; move the rule to its standard and point to it.`);
    }
  });
}

for (const required of REQUIRED_WORKFLOWS) if (!exists(`.claude/skills/${required}/SKILL.md`)) err('.claude/skills', `required workflow "${required}" is missing.`);
for (const required of REQUIRED_KNOWLEDGE) if (!exists(`.claude/skills/${required}/SKILL.md`)) err('.claude/skills', `required knowledge skill "${required}" is missing.`);
if (!exists('.claude/agents/code-reviewer.md')) err('.claude/agents', 'code-reviewer agent is missing.');
else if (!/code-review/.test(read('.claude/agents/code-reviewer.md').replace(/code-reviewer/g, ''))) err('.claude/agents/code-reviewer.md', 'agent must delegate to the code-review workflow.');
for (const rel of files) {
  if (/^\.claude\/rules\/[^/]+$/.test(rel)) err(rel, 'rule files live inside a scope directory.');
  if (/^\.claude\/rules\/\d/.test(rel)) err(rel, 'numbered rule hierarchies are not used; organize rules by scope.');
  if (/^\.claude\/.*(contract|manifest|slot|capabilit)/i.test(rel)) err(rel, 'capability contracts, module manifests or slots are not part of this system.');
}

// ---------------------------------------------------------------------------
// Decision register
// ---------------------------------------------------------------------------

const decisions = new Map();
if (!exists(REGISTER)) {
  err(REGISTER, 'decision register is missing.');
} else {
  for (const line of read(REGISTER).split('\n')) {
    if (!/^\| D-/.test(line)) continue;
    const cells = line.split('|').slice(1, -1).map((c) => c.trim());
    const [id, decision, details, affects] = cells;
    if (!/^D-\d\d$/.test(id)) { err(REGISTER, `malformed decision ID "${id}".`); continue; }
    if (decisions.has(id)) err(REGISTER, `duplicate decision ID ${id}.`);
    if (cells.length !== 4) err(REGISTER, `${id}: rows need ID | Decision | Details in | Affects.`);
    const affectsList = (affects || '').split(',').map((s) => s.trim()).filter((s) => s && s !== '—');
    decisions.set(id, { id, decision: decision || '', details: details || '', affects: affectsList });
    for (const target of affectsList) {
      const resolved = resolveRegisterPath(target);
      if (!resolved || !fs.existsSync(resolved)) err(REGISTER, `${id}: Affects target "${target}" does not exist.`);
    }
    for (const target of (details || '').split(',').map((s) => s.trim()).filter((s) => s && s !== '—')) {
      const resolved = resolveRegisterPath(target.replace(/\s*§.*$/, ''));
      if (!resolved || !fs.existsSync(resolved)) err(REGISTER, `${id}: Details in target "${target}" does not exist.`);
    }
    if (/(rules\/|skills\/|scripts\/)/.test(decision || '')) err(REGISTER, `${id}: the Decision cell must not depend on standards, knowledge or workflows; use Details in / Affects.`);
  }
  if (!/^@docs\/architecture\/decision-register\.md\s*$/m.test(exists('CLAUDE.md') ? read('CLAUDE.md') : '')) {
    err('CLAUDE.md', 'must import the decision register with "@docs/architecture/decision-register.md".');
  }
}

function resolveRegisterPath(target) {
  if (!target) return null;
  if (target.startsWith('docs/') || target.startsWith('.claude/') || ROOT_FILES.includes(target)) return path.join(ROOT, target);
  return path.join(ROOT, '.claude', target);
}

function registerKey(rel) {
  if (rel.startsWith('.claude/skills/')) return `skills/${rel.split('/')[2]}`;
  if (rel.startsWith('.claude/')) return rel.slice('.claude/'.length);
  return rel;
}

const citationExempt = new Set([REGISTER, MAP]);
for (const a of artifacts) {
  if (citationExempt.has(a.rel)) continue;
  const ids = new Set([...a.body.matchAll(/\bD-\d\d\b/g)].map((m) => m[0]));
  for (const id of ids) {
    const d = decisions.get(id);
    if (!d) { err(a.rel, `cites unknown decision ${id}.`); continue; }
    if (!d.affects.includes(registerKey(a.rel))) err(a.rel, `cites ${id} but is not listed in its Affects (${registerKey(a.rel)}).`);
  }
}
for (const rel of walk('')) {
  if (rel === REGISTER || !/\.md$/.test(rel)) continue;
  if (/^\| D-\d\d \|/m.test(read(rel))) err(rel, 'decision entries are defined only in the decision register.');
}

// Decision text is not restated outside the register (8-word overlap).
function shingles(text, n = 8) {
  const words = text.toLowerCase().replace(/[`*_]/g, '').split(/[^a-z0-9.#+<>-]+/).filter(Boolean);
  const set = new Set();
  for (let i = 0; i + n <= words.length; i += 1) set.add(words.slice(i, i + n).join(' '));
  return set;
}
const decisionShingles = new Map([...decisions.values()].map((d) => [d.id, shingles(d.decision)]));
for (const a of artifacts) {
  if (a.rel === REGISTER || a.kind === 'ENF') continue;
  const own = shingles(withoutCodeFences(a.body));
  for (const [id, set] of decisionShingles) {
    const overlap = [...set].filter((s) => own.has(s));
    if (overlap.length > 0) err(a.rel, `restates decision ${id} ("${overlap[0]}…"); cite the ID instead.`);
  }
}

// ---------------------------------------------------------------------------
// References, sections, privacy and dependency direction
// ---------------------------------------------------------------------------

function skillOf(rel) {
  const m = rel.match(/^\.claude\/skills\/([^/]+)\//);
  return m ? m[1] : null;
}

function resolveRef(token, fromRel) {
  if (/[<*{}\s]|\.\.\.|NNNN/.test(token) || token.endsWith('/')) return undefined; // placeholder or location, not an artifact
  if (token.startsWith('.claude/') || token.startsWith('docs/')) return token;
  if (ROOT_FILES.includes(token) || token === 'CLAUDE.md') return token;
  if (/^(rules|skills|scripts|hooks|agents)\//.test(token)) return `.claude/${token}`;
  if (token.startsWith('references/')) {
    const skill = skillOf(fromRel);
    return skill ? `.claude/skills/${skill}/${token}` : null;
  }
  return undefined; // not an instruction-system reference
}

function headingsOf(rel) {
  const abs = path.join(ROOT, rel);
  if (!fs.existsSync(abs) || fs.statSync(abs).isDirectory()) return [];
  return withoutCodeFences(read(rel)).split('\n')
    .filter((l) => /^#{1,4}\s/.test(l))
    .map((l) => l.replace(/^#+\s*/, '').trim().toLowerCase());
}

function sectionExists(rel, section) {
  const wanted = section.toLowerCase().trim();
  return headingsOf(rel).some((h) => h === wanted || h.startsWith(`${wanted}.`) || h.startsWith(`${wanted} `)
    || h.replace(/^(step\s+)?\d+[.)]?\s*(—\s*)?/, '') === wanted);
}

function targetKind(rel) {
  const a = byRel.get(rel);
  if (a) return a.kind;
  if (rel === 'CLAUDE.md') return 'OP';
  return null;
}

const conformanceEdges = [];
for (const a of artifacts) {
  if (a.rel === MAP) continue;
  const lines = withoutCodeFences(a.body).split('\n');
  lines.forEach((line, index) => {
    const routing = ROUTING_PREFIX.test(line);
    const skillContext = routing || /^\s*\|/.test(line) || /→|\b(run|runs|use|follow|skill|workflow|technique|knowledge|load|invoke|see)\b/i.test(line);
    const tokens = [...line.matchAll(/`([^`]+)`/g)].map((m) => m[1]);
    for (const raw of tokens) {
      const token = raw.replace(/[.,;:)]+$/, '');
      const bare = token.replace(/^\//, '');
      if (RETIRED_SKILL_NAMES.includes(bare)) err(a.rel, `line ${index + 1}: "${bare}" is not a skill here (renamed or merged); use the current skill name.`);
      if (skillContext && /^[a-z][a-z0-9]*(-[a-z0-9]+)+$/.test(bare) && !NON_SKILL_TOKENS.has(bare) && !SCOPES.includes(bare) && !skillDirs.includes(bare) && !agentNames.includes(bare)) {
        err(a.rel, `line ${index + 1}: unknown skill or agent \`${bare}\`.`);
      }
      const ref = resolveRef(token, a.rel);
      if (ref === undefined) continue;
      if (ref === null || !exists(ref)) { err(a.rel, `line ${index + 1}: reference \`${token}\` does not resolve.`); continue; }
      const refSkill = skillOf(ref);
      if (/\/references\//.test(ref) && refSkill !== skillOf(a.rel)) err(a.rel, `line ${index + 1}: \`${token}\` is private to the ${refSkill} skill.`);
      if (a.kind === 'STD' && /^\.claude\/(skills|agents)\//.test(ref) && !routing) err(a.rel, `line ${index + 1}: standards may only route to skills ("Workflow:"/"Technique:" lines).`);
      const tk = targetKind(ref);
      if (!routing && tk && ref !== a.rel && ['STD', 'DEC', 'OP'].includes(tk) && ['STD', 'KNW', 'WF', 'DEC'].includes(a.kind)) {
        conformanceEdges.push([a.rel, ref]);
      }
    }
    if (a.kind === 'STD' && !routing) {
      for (const m of line.matchAll(/\b(?:skill|workflow)\s+`([a-z-]+)`|`([a-z-]+)`\s+(?:skill|workflow)/g)) {
        err(a.rel, `line ${index + 1}: standards may only route to skills ("Workflow:"/"Technique:" lines): ${m[1] || m[2]}.`);
      }
    }
    // Section references: "<file or skill> § <Section>"
    const sectionRe = /(?:`([^`]+)`|(CLAUDE\.md))\s*§\s*([^.;,)\n—]+?)(?=\s*(?:[.;,)\n—]|\(|$| and §| and `))/g;
    for (const m of line.matchAll(sectionRe)) {
      const target = (m[1] || m[2]).replace(/^\//, '');
      let rel = resolveRef(target, a.rel);
      if (rel === undefined && skillDirs.includes(target)) rel = `.claude/skills/${target}/SKILL.md`;
      if (!rel || !exists(rel)) continue; // unresolved targets are reported above
      for (const section of m[3].split(/\s+and\s+§\s*/)) {
        const s = section.replace(/[–-]\d+$/, '').trim();
        if (!sectionExists(rel, s)) err(a.rel, `line ${index + 1}: section "§ ${section.trim()}" not found in ${rel}.`);
      }
    }
  });
}

// Conformance dependencies must be acyclic.
const graph = new Map();
for (const [from, to] of conformanceEdges) graph.set(from, new Set([...(graph.get(from) || []), to]));
const visiting = new Set();
const done = new Set();
function visit(node, trail) {
  if (done.has(node)) return;
  if (visiting.has(node)) { err(node, `conformance dependency cycle: ${[...trail, node].join(' -> ')}.`); return; }
  visiting.add(node);
  for (const next of graph.get(node) || []) visit(next, [...trail, node]);
  visiting.delete(node);
  done.add(node);
}
for (const node of graph.keys()) visit(node, []);

// ---------------------------------------------------------------------------
// Hook commands and map
// ---------------------------------------------------------------------------

if (exists('.claude/settings.json')) {
  let settings = null;
  try { settings = JSON.parse(read('.claude/settings.json')); } catch (e) { err('.claude/settings.json', `invalid JSON: ${e.message}`); }
  for (const [event, groups] of Object.entries(settings?.hooks || {})) {
    for (const group of groups) {
      for (const hook of group.hooks || []) {
        const command = String(hook.command || '');
        if (/\$|%[A-Za-z_]+%/.test(command)) err('.claude/settings.json', `${event} hook relies on shell variable expansion; resolve paths inside the script.`);
        const parts = command.match(/'\.claude','hooks','([^']+)'/);
        if (!parts) err('.claude/settings.json', `${event} hook does not use the shared node launcher.`);
        else if (!exists(`.claude/hooks/${parts[1]}`)) err('.claude/settings.json', `${event} hook script .claude/hooks/${parts[1]} is missing.`);
      }
    }
  }
} else {
  err('.claude/settings.json', 'settings with hook configuration are missing.');
}

if (!exists(MAP)) {
  err(MAP, 'human-facing instruction map is missing.');
} else {
  const map = read(MAP);
  for (const a of artifacts) if (!map.includes(a.rel)) err(MAP, `does not list ${a.rel}.`);
  for (const extra of ['SPECIFICATION.md', '.claude/settings.json']) if (!map.includes(extra)) err(MAP, `does not list ${extra}.`);
  const mapAffects = new Map();
  for (const m of map.matchAll(/^- (D-\d\d)\b[^\n]*?→\s*([^\n]+)$/gm)) mapAffects.set(m[1], m[2].split(',').map((s) => s.trim()).filter(Boolean));
  for (const [id, d] of decisions) {
    const shown = mapAffects.get(id);
    if (!shown) { err(MAP, `decision → Affects view lacks ${id}.`); continue; }
    if (shown.slice().sort().join('|') !== d.affects.slice().sort().join('|')) err(MAP, `Affects view for ${id} differs from the register.`);
  }
}

// ---------------------------------------------------------------------------
// Always-loaded surface (informational)
// ---------------------------------------------------------------------------

let alwaysChars = 0;
for (const rel of ['CLAUDE.md', REGISTER]) if (exists(rel)) alwaysChars += read(rel).length;
for (const a of artifacts) {
  const listed = (a.expectedKind === 'SKILL' && String(a.fm['disable-model-invocation']).toLowerCase() !== 'true') || a.rel.startsWith('.claude/agents/');
  if (listed) alwaysChars += String(a.fm.name || '').length + String(a.fm.description || '').length + 8;
}
info.push(`always-loaded surface ≈ ${alwaysChars} characters (≈ ${Math.round(alwaysChars / 4)} tokens) including skill and agent listings`);

function check() {
  return { errors: [...errors], info: [...info], artifacts: artifacts.length };
}

if (require.main === module) {
  for (const e of errors) console.log(`ERROR ${e}`);
  for (const i of info) console.log(`INFO  ${i}`);
  console.log(`check-instructions: ${artifacts.length} artifact(s), ${errors.length} error(s).`);
  process.exit(errors.length > 0 ? 1 : 0);
}

module.exports = { check: () => check() };
