// Kind: ENF | Scope: repo/meta | Owner: instruction-structure checker — Kind/Scope headers and locations, mechanism per Kind, rule paths per scope, the single decision register and its Affects, references and sections, Kind conformance direction and routing pointers, skill privacy, hook configuration, root-aware commands, map coverage, absence of levels and capability machinery | Loading: run by /template-maintenance and by the post-change hook
//
// Usage (from any directory of the repository or worktree, Bash or PowerShell):
//   node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.cjs"   exit 1 when a structural problem is found
//   --root <dir> overrides the checked repository root (default: the Git work tree of the current directory).
'use strict';

const fs = require('fs');
const path = require('path');

const KINDS = ['OP', 'DEC', 'STD', 'KNW', 'WF', 'ENF', 'IN'];
const SCOPES = ['common', 'backend', 'backend-tests', 'frontend', 'delivery', 'repo/meta'];
const RULE_SCOPES = ['common', 'backend', 'backend-tests', 'frontend', 'delivery'];
const REQUIRED_WORKFLOWS = ['development-workflow', 'project-structure', 'verify', 'code-review', 'build-fix', 'custom-settings', 'git-workflow', 'security-scan', 'add-dependency', 'architecture-decision', 'delivery-pipeline', 'template-maintenance'];
const REQUIRED_KNOWLEDGE = ['ef-core', 'http-api', 'aspnet-error-handling', 'dotnet-testing', 'logging', 'httpclient-factory', 'configuration', 'dependency-injection', 'caching', 'swagger', 'api-versioning', 'health-check', 'docker', 'ci-cd', 'angular', 'modern-csharp', 'authentication'];
const USER_ONLY_WORKFLOWS = ['template-maintenance'];
const RETIRED_SKILL_NAMES = ['testing', 'error-handling', 'serilog', 'resilience'];
const NON_SKILL_TOKENS = new Set(['pre-tool-use', 'post-tool-use', 'post-tool-use-failure', 'code-reviewer', 'lodash-es', 'kebab-case', 'repo/meta']);
const ROOT_FILES = ['CLAUDE.md', 'SPECIFICATION.md', 'CUSTOM_SETTINGS.md', 'Directory.Build.props', 'Directory.Packages.props', '.editorconfig'];
const REGISTER = 'docs/architecture/decision-register.md';
const MAP = '.claude/MAP.md';
const MD_HEADER = /^> Kind: (\S+) \| Scope: (\S+) \| Owner: (.+?) \| Loading: (.+)$/;
const CODE_HEADER = /^(?:\/\/|#|<!--)\s*Kind: (\S+) \| Scope: (\S+) \| Owner: (.+?) \| Loading: (.+?)(?:\s*-->)?$/;
const FORBIDDEN_FIELD = /(^|\|)\s*(?:>\s*)?(Level|Capability|Slot|Facet|Contract|Module)\s*:\s/;

// Conformance direction WF → KNW → STD → DEC → OP, and ENF → STD / DEC: the Kinds each Kind may conform to.
// Same-Kind dependencies are allowed but must stay acyclic. References to product inputs are reads, and references
// to enforcement assets name files or tools; neither is a conformance dependency. Enforcement declares its own
// conformance in its header (Owner field) and in "Conforms to:" comment lines.
const CONFORMS_TO = {
  OP: [],
  DEC: ['DEC', 'OP'],
  STD: ['STD', 'DEC', 'OP'],
  KNW: ['KNW', 'STD', 'DEC', 'OP'],
  WF: ['WF', 'KNW', 'STD', 'DEC', 'OP'],
  ENF: ['ENF', 'STD', 'DEC'],
  IN: ['OP', 'DEC'],
};
// A routing pointer may point in any direction: references after one of these labels on the same line, a workflow
// invocation ("run", "use", "invoke", "switch to", "→", a slash command, "agent"), a section whose heading names
// routing, a private reference naming its own skill, the register's Details in / Affects cells, imports, and
// enforcement messages.
const ROUTING_LABEL = /\b(see also|workflow|technique|procedure|enforced by|loading)\s*:/i;
const INVOCATION = /(?:\b(?:run|runs|use|invoke|switch to)\b[^`.;]{0,24}|→\s*|\(agent\s+)$/i;
const DECLARATION = /^\s*(?:\/\/|#|<!--)\s*Conforms to:/;

// Hook registrations of the enforcement design: host event, event argument, tools the matchers must cover.
const REQUIRED_HOOKS = [
  { event: 'PreToolUse', arg: 'pre-tool-use', tools: ['Bash', 'PowerShell'], failClosed: true },
  { event: 'PostToolUse', arg: 'post-tool-use', tools: ['Edit', 'Write', 'MultiEdit', 'NotebookEdit', 'Bash', 'PowerShell'] },
  { event: 'PostToolUseFailure', arg: 'post-tool-use-failure', tools: ['Bash', 'PowerShell'] },
  { event: 'Stop', arg: 'stop', tools: [] },
];
const HOOK_SCRIPT_ARG = /^\$\{CLAUDE_PROJECT_DIR\}\/\.claude\/hooks\/([^/\\]+)$/;
const CWD_RELATIVE_COMMAND = /\bnode\s+\.?\/?\.claude[\\/]/;

// Markdown with fenced blocks blanked out; malformed fences are reported.
function fences(text, report) {
  const lines = text.split('\n');
  let open = -1;
  lines.forEach((line, i) => {
    if (!/^\s*```/.test(line)) {
      if (open >= 0) lines[i] = '';
      return;
    }
    if (open < 0) open = i;
    else if (line.trim() === '```') open = -1;
    else report(i + 1, 'a closing code fence must stand on its own line');
    lines[i] = '';
  });
  if (open >= 0) report(open + 1, 'code fence is never closed');
  return lines.join('\n');
}

function splitFrontmatter(text) {
  if (!text.startsWith('---\n')) return { fm: null, body: text, offset: 0 };
  const end = text.indexOf('\n---\n', 4);
  if (end < 0) return { fm: null, body: text, offset: 0 };
  return { fm: text.slice(4, end), body: text.slice(end + 5), offset: text.slice(0, end + 5).split('\n').length - 1 };
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

function shingles(text, n = 8) {
  const words = text.toLowerCase().replace(/[`*_]/g, '').split(/[^a-z0-9.#+<>-]+/).filter(Boolean);
  const set = new Set();
  for (let i = 0; i + n <= words.length; i += 1) set.add(words.slice(i, i + n).join(' '));
  return set;
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

function check(rootDir) {
  const ROOT = path.resolve(rootDir);
  const errors = [];
  const info = [];
  const err = (file, message) => errors.push(`${file}: ${message}`);
  const exists = (rel) => fs.existsSync(path.join(ROOT, rel));
  const read = (rel) => fs.readFileSync(path.join(ROOT, rel), 'utf8').replace(/^﻿/, '').replace(/\r\n/g, '\n');

  const walk = (relDir, out = []) => {
    const abs = path.join(ROOT, relDir);
    if (!fs.existsSync(abs)) return out;
    const entries = fs.readdirSync(abs, { withFileTypes: true });
    if (entries.length === 0) err(relDir, 'empty directory; create directories only for real content.');
    for (const entry of entries) {
      const rel = relDir ? `${relDir}/${entry.name}` : entry.name;
      if (entry.isDirectory()) {
        if (!['.hook-state', 'node_modules', '.git', 'bin', 'obj', 'dist'].includes(entry.name)) walk(rel, out);
      } else {
        out.push(rel);
      }
    }
    return out;
  };

  // -------------------------------------------------------------------------
  // Artifacts: location determines the expected Kind and mechanism
  // -------------------------------------------------------------------------

  const files = [...walk('.claude'), ...walk('docs'), ...ROOT_FILES.filter(exists)];
  const artifacts = [];

  const locationKind = (rel) => {
    if (rel === 'CLAUDE.md') return 'OP';
    if (rel === REGISTER) return 'DEC';
    if (rel === 'CUSTOM_SETTINGS.md') return 'IN';
    if (/^\.claude\/rules\/.+\.md$/.test(rel)) return 'STD';
    if (/^\.claude\/skills\/[^/]+\/SKILL\.md$/.test(rel)) return 'SKILL';
    if (/^\.claude\/skills\/[^/]+\/references\/.+\.md$/.test(rel)) return 'REFERENCE';
    if (/^\.claude\/agents\/[^/]+\.md$/.test(rel)) return 'WF';
    if (/^\.claude\/(hooks|scripts)\/[^/]+\.cjs$/.test(rel) || ['.editorconfig', 'Directory.Build.props', 'Directory.Packages.props'].includes(rel)) return 'ENF-CODE';
    return null;
  };

  const ignored = new Set(['SPECIFICATION.md', MAP, '.claude/settings.json', '.claude/settings.local.json']);
  for (const rel of files) {
    if (/(^|\/)\d+-[^/]*\//.test(`${rel}`) || /^\.claude\/rules\/\d/.test(rel)) err(rel, 'numbered or level-ordered directories are not used; organize by Kind and Scope.');
    if (/^\.claude\/.*(contract|manifest|slot|capabilit|facet)/i.test(rel)) err(rel, 'capability contracts, module manifests, slots or facets are not part of this system.');
    if (/^\.claude\/rules\/[^/]+$/.test(rel)) err(rel, 'rule files live inside a scope directory.');
    if (ignored.has(rel) || rel.startsWith('docs/decisions/')) continue;
    const expected = locationKind(rel);
    if (!expected) {
      if (rel.startsWith('.claude/') || rel.startsWith('docs/architecture/')) err(rel, 'unclassified file in the instruction system; place it by Kind and Scope (see .claude/MAP.md).');
      continue;
    }
    const text = read(rel);
    if (expected === 'ENF-CODE') {
      const m = text.split('\n')[0].match(CODE_HEADER);
      if (!m && ROOT_FILES.includes(rel)) continue; // project-owned build/format file without the template header
      if (!m) { err(rel, 'missing first-line header "Kind: ENF | Scope: … | Owner: … | Loading: …".'); continue; }
      artifacts.push({ rel, expected: 'ENF', kind: m[1], scope: m[2], loading: m[4].toLowerCase(), header: text.split('\n')[0], fm: {}, body: text, offset: 0, code: true });
      continue;
    }
    const { fm, body, offset } = splitFrontmatter(text);
    const firstLine = body.split('\n').find((l) => l.trim() !== '') || '';
    const m = firstLine.match(MD_HEADER);
    if (!m) { err(rel, 'first body line must be the header "> Kind: … | Scope: … | Owner: … | Loading: …".'); continue; }
    artifacts.push({ rel, expected, kind: m[1], scope: m[2], loading: m[4].toLowerCase(), header: firstLine, fm: parseFrontmatter(fm), body, offset, code: false });
  }

  const byRel = new Map(artifacts.map((a) => [a.rel, a]));
  const skillDirs = exists('.claude/skills')
    ? fs.readdirSync(path.join(ROOT, '.claude/skills'), { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name)
    : [];
  const agentNames = walk('.claude/agents').map((f) => path.basename(f, '.md'));

  for (const a of artifacts) {
    if (!KINDS.includes(a.kind)) err(a.rel, `unknown Kind "${a.kind}".`);
    if (!SCOPES.includes(a.scope)) err(a.rel, `unknown Scope "${a.scope}".`);
    if (FORBIDDEN_FIELD.test(a.header)) err(a.rel, 'header carries a level/capability field; this system classifies by Kind and Scope only.');
    if (!a.code) {
      a.prose = fences(a.body, (line, message) => err(a.rel, `line ${line + a.offset}: ${message}.`));
      a.prose.split('\n').forEach((line, i) => {
        if (FORBIDDEN_FIELD.test(line)) err(a.rel, `line ${i + 1 + a.offset}: "Level:"/capability fields are not used; classify by Kind and Scope.`);
      });
    }

    if (['OP', 'DEC', 'IN', 'STD', 'WF', 'ENF'].includes(a.expected) && a.kind !== a.expected) {
      err(a.rel, `Kind ${a.kind} does not match its location and mechanism (expected ${a.expected}).`);
    }
    if ((a.expected === 'OP' || a.expected === 'DEC') && !a.loading.includes('always')) err(a.rel, 'OP/DEC must load always.');
    if (a.expected === 'IN' && !a.loading.includes('input')) err(a.rel, 'IN is read as product input.');

    if (a.expected === 'STD') {
      const dir = a.rel.split('/')[2];
      if (a.rel.split('/').length !== 4) err(a.rel, 'standards live directly in .claude/rules/<scope>/<topic>.md.');
      if (!RULE_SCOPES.includes(dir)) err(a.rel, `rules directory "${dir}" is not a scope (${RULE_SCOPES.join(', ')}).`);
      if (dir !== a.scope) err(a.rel, `Scope ${a.scope} does not match its directory ${dir}.`);
      if (!a.loading.includes('path-scoped')) err(a.rel, 'STD must be path-scoped.');
      const globs = [].concat(a.fm.paths || []);
      if (globs.length === 0) err(a.rel, 'rule must declare non-empty "paths".');
      for (const g of globs) if (!globInScope(g, a.scope)) err(a.rel, `path glob "${g}" is outside the ${a.scope} scope territory.`);
      a.prose.split('\n').forEach((line, i) => {
        if (/^\s*\d+\.\s/.test(line) || /^#+\s*(Step|Procedure)\b/i.test(line)) err(a.rel, `line ${i + 1 + a.offset}: procedures belong in a workflow, not in a standard.`);
      });
    }

    if (a.expected === 'SKILL') {
      const name = a.rel.split('/')[2];
      if (a.fm.name !== name) err(a.rel, `frontmatter name "${a.fm.name}" must equal the directory name "${name}".`);
      if (!a.fm.description || String(a.fm.description).length < 20) err(a.rel, 'skill needs a concrete description.');
      const userOnly = String(a.fm['disable-model-invocation']).toLowerCase() === 'true';
      if (a.kind === 'KNW') {
        if (!a.loading.includes('on demand')) err(a.rel, 'KNW must load on demand.');
        if (userOnly) err(a.rel, 'knowledge skills must stay model-invocable.');
        if (REQUIRED_WORKFLOWS.includes(name)) err(a.rel, `"${name}" is a workflow and must be Kind WF.`);
      } else if (a.kind === 'WF') {
        if (!a.loading.includes('workflow')) err(a.rel, 'WF must load as a workflow.');
        if (REQUIRED_KNOWLEDGE.includes(name)) err(a.rel, `"${name}" is a knowledge skill and must be Kind KNW.`);
        if (USER_ONLY_WORKFLOWS.includes(name) && !userOnly) err(a.rel, 'user-only workflow must set disable-model-invocation: true.');
      } else {
        err(a.rel, `skills are Kind WF or KNW; Kind ${a.kind} needs its own mechanism and location.`);
      }
    }

    if (a.expected === 'REFERENCE') {
      const owner = byRel.get(`.claude/skills/${a.rel.split('/')[2]}/SKILL.md`);
      if (owner && owner.kind !== a.kind) err(a.rel, `private reference Kind ${a.kind} differs from its skill (${owner.kind}).`);
      if (!a.loading.includes('only')) err(a.rel, 'private reference must state that only its skill reads it.');
    }

    if ((a.expected === 'SKILL' || a.expected === 'REFERENCE') && a.kind === 'KNW') {
      a.prose.split('\n').forEach((line, i) => {
        if (/\b(must|never|requires approval)\b/i.test(line) && !/(rules\/|CLAUDE\.md|D-\d\d)/.test(line)) {
          err(a.rel, `line ${i + 1 + a.offset}: normative wording in knowledge without an owner reference; move the rule to its standard and point to it.`);
        }
      });
    }

    if (a.rel.startsWith('.claude/agents/')) {
      const name = path.basename(a.rel, '.md');
      if (a.fm.name !== name) err(a.rel, `frontmatter name "${a.fm.name}" must equal the file name "${name}".`);
      if (!a.loading.includes('agent')) err(a.rel, 'agents load as delegated agents.');
    }
  }

  for (const required of REQUIRED_WORKFLOWS) if (!exists(`.claude/skills/${required}/SKILL.md`)) err('.claude/skills', `required workflow "${required}" is missing.`);
  for (const required of REQUIRED_KNOWLEDGE) if (!exists(`.claude/skills/${required}/SKILL.md`)) err('.claude/skills', `required knowledge skill "${required}" is missing.`);
  if (!exists('.claude/agents/code-reviewer.md')) err('.claude/agents', 'code-reviewer agent is missing.');
  else if (!/code-review/.test(read('.claude/agents/code-reviewer.md').replace(/code-reviewer/g, ''))) err('.claude/agents/code-reviewer.md', 'agent must delegate to the code-review workflow.');

  // -------------------------------------------------------------------------
  // The single always-loaded decision register
  // -------------------------------------------------------------------------

  const decisions = new Map();
  const registerKey = (rel) => (rel.startsWith('.claude/skills/') ? `skills/${rel.split('/')[2]}` : rel.startsWith('.claude/') ? rel.slice('.claude/'.length) : rel);
  const resolveRegisterPath = (target) => {
    if (target.startsWith('docs/') || target.startsWith('.claude/') || ROOT_FILES.includes(target)) return target;
    return `.claude/${target}`;
  };
  const registerTargetKind = (target) => {
    const rel = resolveRegisterPath(target);
    const direct = byRel.get(rel) || byRel.get(`${rel}/SKILL.md`);
    return direct ? direct.kind : null;
  };

  const decArtifacts = artifacts.filter((a) => a.kind === 'DEC');
  if (decArtifacts.length !== 1 || decArtifacts[0].rel !== REGISTER) err(REGISTER, `exactly one decision register (${REGISTER}) must carry Kind DEC; found ${decArtifacts.map((a) => a.rel).join(', ') || 'none'}.`);
  const imports = exists('CLAUDE.md') ? [...read('CLAUDE.md').matchAll(/^@(\S+)\s*$/gm)].map((m) => m[1]) : [];
  if (imports.length !== 1 || imports[0] !== REGISTER) err('CLAUDE.md', `must import exactly the decision register ("@${REGISTER}"); imports make content always-loaded (found: ${imports.join(', ') || 'none'}).`);

  if (exists(REGISTER)) {
    for (const line of read(REGISTER).split('\n')) {
      if (!/^\| D-/.test(line)) continue;
      const cells = line.split('|').slice(1, -1).map((c) => c.trim());
      const [id, decision, details, affects] = cells;
      if (!/^D-\d\d$/.test(id)) { err(REGISTER, `malformed decision ID "${id}".`); continue; }
      if (decisions.has(id)) err(REGISTER, `duplicate decision ID ${id}.`);
      if (cells.length !== 4) err(REGISTER, `${id}: rows need ID | Decision | Details in | Affects.`);
      const affectsList = (affects || '').split(',').map((s) => s.trim()).filter((s) => s && s !== '—');
      const detailsList = (details || '').split(',').map((s) => s.trim().replace(/\s*§.*$/, '')).filter((s) => s && s !== '—');
      decisions.set(id, { id, decision: decision || '', affects: affectsList });
      if (!decision) err(REGISTER, `${id}: decision summary is empty.`);
      if (new Set(affectsList).size !== affectsList.length) err(REGISTER, `${id}: Affects lists a target twice.`);
      for (const target of affectsList) {
        if (!exists(resolveRegisterPath(target))) { err(REGISTER, `${id}: Affects target "${target}" does not exist.`); continue; }
        const kind = registerTargetKind(target);
        if (kind && !['STD', 'KNW', 'WF', 'ENF'].includes(kind)) err(REGISTER, `${id}: Affects target "${target}" is Kind ${kind}; Affects lists dependent STD/KNW/WF/ENF artifacts.`);
      }
      for (const target of detailsList) {
        if (!exists(resolveRegisterPath(target))) err(REGISTER, `${id}: Details in target "${target}" does not exist.`);
        else if (!affectsList.includes(target)) err(REGISTER, `${id}: Details in target "${target}" must also be listed in Affects.`);
      }
      if (/(rules\/|skills\/|scripts\/)/.test(decision || '')) err(REGISTER, `${id}: the Decision cell must not depend on standards, knowledge or workflows; use Details in / Affects.`);
    }
  }

  for (const a of artifacts) {
    if (a.rel === REGISTER) continue;
    for (const id of new Set([...a.body.matchAll(/\bD-\d\d\b/g)].map((m) => m[0]))) {
      const d = decisions.get(id);
      if (!d) err(a.rel, `cites unknown decision ${id}.`);
      else if (!d.affects.includes(registerKey(a.rel))) err(a.rel, `cites ${id} but is not listed in its Affects (${registerKey(a.rel)}).`);
    }
  }
  for (const rel of walk('')) {
    if (rel !== REGISTER && /\.md$/.test(rel) && /^\| D-\d\d \|/m.test(read(rel))) err(rel, 'decision entries are defined only in the decision register.');
  }
  const decisionShingles = [...decisions.values()].map((d) => [d.id, shingles(d.decision)]);
  for (const a of artifacts) {
    if (a.rel === REGISTER || a.code) continue;
    const own = shingles(a.prose);
    for (const [id, set] of decisionShingles) {
      const overlap = [...set].filter((s) => own.has(s));
      if (overlap.length > 0) err(a.rel, `restates decision ${id} ("${overlap[0]}…"); cite the ID instead.`);
    }
  }

  // -------------------------------------------------------------------------
  // References, sections, privacy and Kind conformance direction
  // -------------------------------------------------------------------------

  const skillOf = (rel) => (rel.match(/^\.claude\/skills\/([^/]+)\//) || [])[1] || null;
  const resolveRef = (token, fromRel) => {
    if (/[<*{}\s$"]|\.\.\.|NNNN/.test(token) || token.endsWith('/')) return undefined; // placeholder, command or location
    if (token.startsWith('.claude/') || token.startsWith('docs/')) return token;
    if (ROOT_FILES.includes(token)) return token;
    if (/^(rules|skills|scripts|hooks|agents)\//.test(token)) return `.claude/${token}`;
    if (token.startsWith('references/')) return skillOf(fromRel) ? `.claude/skills/${skillOf(fromRel)}/${token}` : null;
    const bare = token.replace(/^\//, '');
    if (skillDirs.includes(bare)) return `.claude/skills/${bare}/SKILL.md`;
    if (agentNames.includes(bare)) return `.claude/agents/${bare}.md`;
    return undefined;
  };
  const targetKind = (rel) => {
    if (rel === 'SPECIFICATION.md' || rel === 'CUSTOM_SETTINGS.md') return 'IN';
    if (rel === '.claude/settings.json') return 'ENF';
    const a = byRel.get(rel) || byRel.get(`${rel.replace(/\/$/, '')}/SKILL.md`);
    return a ? a.kind : null;
  };
  const headingsOf = (rel) => {
    if (!exists(rel) || fs.statSync(path.join(ROOT, rel)).isDirectory()) return [];
    return fences(read(rel), () => {}).split('\n').filter((l) => /^#{1,4}\s/.test(l)).map((l) => l.replace(/^#+\s*/, '').trim().toLowerCase());
  };
  const sectionExists = (rel, section) => {
    const wanted = section.toLowerCase().trim();
    return headingsOf(rel).some((h) => h === wanted || h.startsWith(`${wanted}.`) || h.startsWith(`${wanted} `)
      || h.replace(/^(step\s+)?\d+[.)]?\s*(—\s*)?/, '') === wanted);
  };

  // References of one line: { token, target, index }. Prose lines use backticks, the operating-policy file name
  // and decision IDs; enforcement comment lines may also name paths and multi-word skill names without backticks.
  const lineRefs = (line, fromRel, bareNames) => {
    const refs = [];
    for (const m of line.matchAll(/`([^`]+)`/g)) {
      const token = m[1].replace(/\\/g, '').replace(/[.,;:)]+$/, '');
      refs.push({ token, target: resolveRef(token, fromRel), index: m.index });
    }
    const plain = line.replace(/`[^`]*`/g, (s) => ' '.repeat(s.length));
    for (const m of plain.matchAll(/\bCLAUDE\.md\b/g)) refs.push({ token: 'CLAUDE.md', target: 'CLAUDE.md', index: m.index });
    for (const m of plain.matchAll(/\bD-\d\d\b/g)) refs.push({ token: m[0], target: REGISTER, index: m.index });
    if (bareNames) {
      for (const m of plain.matchAll(/(?:^|[\s(])((?:\.claude\/|docs\/)?(?:rules|skills|scripts|hooks|agents|architecture)\/[\w./-]+\.(?:md|cjs|json))/g)) {
        const token = m[1].replace(/[.,;:)]+$/, '');
        refs.push({ token, target: resolveRef(token, fromRel) ?? (exists(token) ? token : null), index: m.index });
      }
      for (const m of plain.matchAll(/\b([a-z][a-z0-9]*(?:-[a-z0-9]+)+)\b/g)) {
        if (skillDirs.includes(m[1]) || agentNames.includes(m[1])) refs.push({ token: m[1], target: resolveRef(m[1], fromRel), index: m.index });
      }
    }
    return refs;
  };

  const SECTION_REF = /(?:`([^`]+)`|\b(CLAUDE\.md|(?:\.claude\/)?(?:rules|skills)\/[\w./-]+\.md|[a-z][a-z0-9]*(?:-[a-z0-9]+)+))\s*§\s*([^.;,)\n—'"`\\]+?)(?=\s*(?:[.;,)\n—'"`\\]|\(|$| and §| and `))/g;
  const checkSections = (a, line, lineNo) => {
    for (const m of line.matchAll(SECTION_REF)) {
      const target = (m[1] || m[2]).replace(/\\/g, '').replace(/^\//, '');
      let rel = resolveRef(target, a.rel);
      if (rel === undefined && target === 'CLAUDE.md') rel = 'CLAUDE.md';
      if (!rel) {
        if (m[2] && !skillDirs.includes(target) && /-/.test(target) && !target.includes('/')) continue; // plain hyphenated words
        err(a.rel, `line ${lineNo}: section reference target "${target}" does not resolve.`);
        continue;
      }
      if (!exists(rel)) continue; // reported as a broken reference
      for (const section of m[3].split(/\s+and\s+§\s*/)) {
        const s = section.replace(/[–-]\d+$/, '').trim();
        if (!sectionExists(rel, s)) err(a.rel, `line ${lineNo}: section "§ ${section.trim()}" not found in ${rel}.`);
      }
    }
  };

  const edges = [];
  for (const a of artifacts) {
    const lines = a.code ? a.body.split('\n') : a.prose.split('\n');
    let routingSection = false;
    lines.forEach((line, index) => {
      const lineNo = index + 1 + a.offset;
      if (!a.code && /^#{1,6}\s/.test(line)) routingSection = /routing/i.test(line);
      const isComment = a.code && /^\s*(\/\/|#|<!--)/.test(line);
      if (a.code && !isComment) { checkSections(a, line, lineNo); return; } // enforcement code and messages: routing pointers only

      let routingFrom = Infinity;
      const label = line.match(ROUTING_LABEL);
      if (label) routingFrom = label.index;
      if (routingSection || /^@\S+\s*$/.test(line)) routingFrom = 0;
      if (a.rel === REGISTER && /^\|\s*D-\d\d/.test(line)) routingFrom = line.split('|', 3).join('|').length; // Details in / Affects cells
      if (a.code && index > 0 && !DECLARATION.test(line)) routingFrom = 0; // descriptive comment, not a conformance declaration

      for (const ref of lineRefs(line, a.rel, a.code)) {
        const routing = ref.index >= routingFrom || ref.token.startsWith('/') || INVOCATION.test(line.slice(0, ref.index))
          || (a.rel.includes('/references/') && ref.target === `.claude/skills/${skillOf(a.rel)}/SKILL.md`);
        const bare = ref.token.replace(/^\//, '');
        if (RETIRED_SKILL_NAMES.includes(bare)) err(a.rel, `line ${lineNo}: "${bare}" is not a skill here (renamed or merged); use the current skill name.`);
        const skillContext = !a.code && (routingFrom !== Infinity || /^\s*\|/.test(line) || /→|\b(run|runs|use|follow|skill|workflow|technique|knowledge|load|invoke|see)\b/i.test(line));
        if (skillContext && ref.target === undefined && /^[a-z][a-z0-9]*(-[a-z0-9]+)+$/.test(bare) && !NON_SKILL_TOKENS.has(bare) && !SCOPES.includes(bare)) {
          err(a.rel, `line ${lineNo}: unknown skill or agent \`${bare}\`.`);
        }
        if (ref.target === undefined) continue;
        if (ref.target === null || !exists(ref.target)) { err(a.rel, `line ${lineNo}: reference \`${ref.token}\` does not resolve.`); continue; }
        const refSkill = skillOf(ref.target);
        if (/\/references\//.test(ref.target) && refSkill !== skillOf(a.rel)) err(a.rel, `line ${lineNo}: \`${ref.token}\` is private to the ${refSkill} skill.`);
        const tk = targetKind(ref.target);
        if (routing || !tk || tk === 'IN' || (tk === 'ENF' && a.kind !== 'ENF') || ref.target === a.rel) continue;
        if (!(CONFORMS_TO[a.kind] || []).includes(tk)) {
          err(a.rel, `line ${lineNo}: conformance dependency ${a.kind} → ${tk} (\`${ref.token}\`) violates the Kind direction WF → KNW → STD → DEC → OP, ENF → STD/DEC; mark it as a routing pointer ("See also:", "Workflow:", "Technique:") or move the content to its owner.`);
        } else {
          edges.push([a.rel, ref.target]);
        }
      }
      if (!a.code || isComment) checkSections(a, line, lineNo);
    });
  }

  const graph = new Map();
  for (const [from, to] of edges) graph.set(from, new Set([...(graph.get(from) || []), to]));
  const visiting = new Set();
  const done = new Set();
  const visit = (node, trail) => {
    if (done.has(node)) return;
    if (visiting.has(node)) { err(node, `conformance dependency cycle: ${[...trail, node].join(' -> ')}.`); return; }
    visiting.add(node);
    for (const next of graph.get(node) || []) visit(next, [...trail, node]);
    visiting.delete(node);
    done.add(node);
  };
  for (const node of graph.keys()) visit(node, []);

  // Manual tool invocations must work from any directory of the repository or worktree.
  for (const rel of [...artifacts.map((a) => a.rel), ...(exists(MAP) ? [MAP] : [])]) {
    read(rel).split('\n').forEach((line, i) => {
      if (CWD_RELATIVE_COMMAND.test(line)) err(rel, `line ${i + 1}: tool invocation is relative to the current directory; use node "$(git rev-parse --show-toplevel)/.claude/…".`);
    });
  }

  // -------------------------------------------------------------------------
  // Hook configuration (exec form, scripts, events, matchers, failure mode)
  // -------------------------------------------------------------------------

  if (!exists('.claude/settings.json')) {
    err('.claude/settings.json', 'settings with hook configuration are missing.');
  } else {
    let settings = null;
    try { settings = JSON.parse(read('.claude/settings.json')); } catch (e) { err('.claude/settings.json', `invalid JSON: ${e.message}`); }
    const registrations = [];
    for (const [event, groups] of Object.entries(settings?.hooks || {})) {
      for (const group of Array.isArray(groups) ? groups : []) {
        for (const hook of group.hooks || []) {
          const where = `.claude/settings.json: ${event}`;
          const args = Array.isArray(hook.args) ? hook.args : null;
          if (hook.type !== 'command') { errors.push(`${where} hook must be a command hook.`); continue; }
          if (typeof hook.command !== 'string' || !/^[\w.-]+$/.test(hook.command)) errors.push(`${where} hook command must name an executable only (exec form); found "${hook.command}".`);
          if (!args || args.length < 2 || !args.every((x) => typeof x === 'string')) { errors.push(`${where} hook needs exec-form "args": [<script>, <event>].`); continue; }
          const script = args[0].match(HOOK_SCRIPT_ARG);
          if (!script) errors.push(`${where} hook script argument must be "\${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>".`);
          else if (!exists(`.claude/hooks/${script[1]}`)) errors.push(`${where} hook script .claude/hooks/${script[1]} is missing.`);
          if (args.slice(1).some((x) => /\$|%[A-Za-z_]+%/.test(x))) errors.push(`${where} hook arguments rely on variable expansion.`);
          const scriptEvents = script && exists(`.claude/hooks/${script[1]}`) ? ((read(`.claude/hooks/${script[1]}`).match(/const EVENTS = \[([^\]]*)\]/) || [])[1] || '').match(/'[^']+'/g)?.map((s) => s.slice(1, -1)) || [] : [];
          if (script && !scriptEvents.includes(args[1])) errors.push(`${where} hook event argument "${args[1]}" is not handled by ${script[1]}.`);
          if (!(Number(hook.timeout) > 0)) errors.push(`${where} hook needs a positive timeout.`);
          if (hook.onFailure !== undefined && !(event === 'PreToolUse' && hook.onFailure === 'block')) errors.push(`${where} hook sets onFailure "${hook.onFailure}"; only critical PreToolUse policy hooks fail closed.`);
          registrations.push({ event, arg: args[1], matcher: group.matcher, onFailure: hook.onFailure });
        }
      }
    }
    for (const required of REQUIRED_HOOKS) {
      const matching = registrations.filter((r) => r.event === required.event && r.arg === required.arg);
      if (matching.length === 0) { errors.push(`.claude/settings.json: required ${required.event} hook ("${required.arg}") is not registered.`); continue; }
      for (const tool of required.tools) {
        if (!matching.some((r) => { try { return new RegExp(`^(?:${r.matcher || '.*'})$`).test(tool); } catch { return false; } })) {
          errors.push(`.claude/settings.json: ${required.event} hook ("${required.arg}") does not match ${tool}.`);
        }
      }
      if (required.failClosed && matching.some((r) => r.onFailure !== 'block')) errors.push(`.claude/settings.json: ${required.event} policy hook must fail closed ("onFailure": "block").`);
    }
  }

  // -------------------------------------------------------------------------
  // Human map
  // -------------------------------------------------------------------------

  if (!exists(MAP)) {
    err(MAP, 'human-facing instruction map is missing.');
  } else {
    const map = read(MAP);
    if (!/^> Instruction map \|.*\| Loading: not loaded/.test(map)) err(MAP, 'map header must state that the map is not loaded.');
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

  // -------------------------------------------------------------------------
  // Always-loaded surface (informational)
  // -------------------------------------------------------------------------

  let alwaysChars = 0;
  for (const rel of ['CLAUDE.md', REGISTER]) if (exists(rel)) alwaysChars += read(rel).length;
  for (const a of artifacts) {
    const listed = (a.expected === 'SKILL' && String(a.fm['disable-model-invocation']).toLowerCase() !== 'true') || a.rel.startsWith('.claude/agents/');
    if (listed) alwaysChars += String(a.fm.name || '').length + String(a.fm.description || '').length + 8;
  }
  info.push(`always-loaded surface ≈ ${alwaysChars} characters (≈ ${Math.round(alwaysChars / 4)} tokens) including skill and agent listings`);

  return { errors, info, artifacts: artifacts.length, edges };
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const rootIndex = args.indexOf('--root');
  const start = rootIndex >= 0 ? args[rootIndex + 1] : process.cwd();
  const resolved = require('./repo.cjs').resolveRoot(start);
  if (!resolved) {
    console.log(`ERROR cannot resolve a repository root from ${start}.`);
    process.exit(1);
  }
  const result = check(resolved.root);
  for (const e of result.errors) console.log(`ERROR ${e}`);
  for (const i of result.info) console.log(`INFO  ${i}`);
  console.log(`check-instructions: ${resolved.root}: ${result.artifacts} artifact(s), ${result.errors.length} error(s).`);
  process.exit(result.errors.length > 0 ? 1 : 0);
}

module.exports = { check };
