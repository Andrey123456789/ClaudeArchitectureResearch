// Kind: ENF | Scope: repo/meta | Capability: — | Loading: required by .claude/hooks/dispatch.cjs (PostToolUse, PostToolUseFailure)
// Conforms: docs/architecture/decision-register.md, .claude/rules/backend/dependencies.md, .claude/rules/frontend/dependencies.md
'use strict';

// Post-execution inspection of the ACTUAL files of the active repository/worktree; command text is never consulted.
// A bounded snapshot (content hash per relevant file, project-reference edges, HEAD) is kept per worktree in its
// own Git directory. The first observation baselines against HEAD; later observations report what changed since
// the previous one. Reference-graph changes count only while they differ from HEAD (committed history and
// reverted edits are not pending changes).

const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');
const lib = require('./lib.cjs');
const manifests = require('./check-manifests.cjs');

const STATE_FILE = 'claude-actual-state.json';
const STATE_VERSION = 1;
const MAX_ENTRIES = 5000;
const REGISTER = 'docs/architecture/decision-register.md';
const PATHSPECS = ['CLAUDE.md', 'SPECIFICATION.md', 'CUSTOM_SETTINGS.md', REGISTER, '.claude', ':(glob)**/*.csproj', ':(glob)**/Directory.Packages.props', ':(glob)**/package.json'];
const OWNER_RESERVED = `architecture-decision workflow (record the approval as \`From -> To\` in ${REGISTER}, Accepted decisions)`;

const isFile = abs => {
  try {
    return fs.statSync(abs).isFile();
  } catch {
    return false;
  }
};

/** Relevance class of a repository-relative file path, or null (directory entries such as a nested Git root `x/` never are). */
function kindOf(rel) {
  if (!rel || rel.endsWith('/') || rel.split('/').some(seg => lib.IGNORED_DIRS.has(seg))) return null;
  if (manifests.isManifest(rel)) return 'manifest';
  if (rel === 'SPECIFICATION.md' || rel === 'CUSTOM_SETTINGS.md') return 'input';
  if (rel === 'CLAUDE.md' || rel === REGISTER || (rel.startsWith('.claude/') && !rel.endsWith('settings.local.json'))) return 'instruction';
  return null;
}

function gitContext(root) {
  const top = lib.git(root, ['rev-parse', '--show-toplevel']);
  if (!top || top.status !== 0 || lib.realpath(top.stdout.trim()) !== lib.realpath(root)) return null;
  const gitDir = lib.git(root, ['rev-parse', '--absolute-git-dir']);
  if (!gitDir || gitDir.status !== 0) return null;
  const head = lib.git(root, ['rev-parse', '-q', '--verify', 'HEAD^{commit}']);
  return { gitDir: gitDir.stdout.trim(), head: head && head.status === 0 ? head.stdout.trim() : null };
}

function statePath(root, ctx) {
  if (ctx) return path.join(ctx.gitDir, STATE_FILE);
  const key = crypto.createHash('sha1').update(lib.realpath(root).toLowerCase()).digest('hex').slice(0, 16);
  return path.join(os.tmpdir(), `claude-actual-state-${key}.json`);
}

/** Previous snapshot, or null when missing, unreadable, or inconsistent (deterministic re-baseline). */
function loadState(file, root) {
  try {
    const state = JSON.parse(fs.readFileSync(file, 'utf8'));
    if (state.v !== STATE_VERSION || state.root !== lib.realpath(root) || !state.entries || typeof state.entries !== 'object') return null;
    return state;
  } catch {
    return null;
  }
}

function saveState(file, state) {
  const tmp = `${file}.${process.pid}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(state));
  fs.renameSync(tmp, file);
}

function listRelevant(root, ctx) {
  let files;
  if (ctx) {
    const r = lib.git(root, ['ls-files', '-z', '--cached', '--others', '--exclude-standard', '--', ...PATHSPECS]);
    if (!r || r.status !== 0) throw new Error(`git ls-files failed: ${r ? r.stderr.trim() : 'git unavailable'}`);
    files = r.stdout.split('\0');
  } else {
    files = lib.walk(root, '', rel => !!kindOf(rel));
  }
  return [...new Set(files)].filter(rel => kindOf(rel) && isFile(path.join(root, rel))).sort();
}

/** Relevant paths that differ from HEAD (modified, added, deleted, untracked). */
function dirtyRelevant(root) {
  const r = lib.git(root, ['status', '--porcelain=v1', '-z', '-uall', '--no-renames', '--', ...PATHSPECS]);
  if (!r || r.status !== 0) throw new Error(`git status failed: ${r ? r.stderr.trim() : 'git unavailable'}`);
  return r.stdout.split('\0').filter(Boolean).map(e => e.slice(3)).filter(kindOf);
}

const hashBuffer = buf => crypto.createHash('sha1').update(buf).digest('hex');

function headBuffer(root, ctx, rel) {
  if (!ctx || !ctx.head) return null;
  const r = lib.git(root, ['show', `${ctx.head}:${rel}`], { encoding: 'buffer' });
  return r && r.status === 0 ? r.stdout : null;
}

function edgesOf(rel, buffer) {
  if (buffer === null) return null;
  const project = manifests.parseProject(null, rel, lib.decodeText(buffer, rel));
  return [...new Set(project.projectRefs.map(r => r.name))].sort();
}

/** Reference-graph findings for one project file: (current Δ base) ∩ (current Δ HEAD), minus recorded approvals. */
function graphFindings(rel, current, base, head, hasHead, approvals, roleOf) {
  const name = path.posix.basename(rel).replace(/\.csproj$/i, '');
  const key = s => s.toLowerCase();
  const cur = new Map((current || []).map(e => [key(e), e]));
  const bas = new Map((base || []).map(e => [key(e), e]));
  const hd = new Map((head || []).map(e => [key(e), e]));
  const changes = [];
  if (current !== null && base === null && (!hasHead || head === null) && roleOf(name).kind !== 'test') {
    if (!manifests.isApprovedProject(approvals, name)) changes.push(`project ${name} added`);
  }
  if (current === null && base !== null && (!hasHead || head !== null) && roleOf(name).kind !== 'test') {
    if (!manifests.isApprovedProject(approvals, name)) changes.push(`project ${name} removed`);
  }
  for (const [k, to] of cur) {
    if (!bas.has(k) && (!hasHead || !hd.has(k)) && !manifests.isApprovedEdge(approvals, name, to)) changes.push(`${name} -> ${to} added`);
  }
  for (const [k, to] of bas) {
    if (!cur.has(k) && (!hasHead || hd.has(k)) && !manifests.isApprovedEdge(approvals, name, to)) changes.push(`${name} -> ${to} removed`);
  }
  if (!changes.length) return [];
  return [lib.finding('error', rel, `project reference graph changed without a recorded approval (Reserved): ${changes.join('; ')}`, OWNER_RESERVED)];
}

/**
 * Observe the active root after a tool call. options.only = repository-relative path of a file edited by an
 * Edit/Write tool (that file is always validated; other files are left to the next shell observation).
 * Returns { findings, instructionErrors, reminders, firstObservation, changed }.
 */
function observe(root, options = {}) {
  const only = options.only || null;
  if (only && !kindOf(only)) return { findings: [], instructionErrors: [], reminders: [], firstObservation: false, changed: [] };
  const ctx = gitContext(root);
  const file = statePath(root, ctx);
  const prev = loadState(file, root);
  const head = ctx ? ctx.head : null;
  const headMoved = !!prev && prev.head !== head;
  const files = listRelevant(root, ctx);
  const tooMany = files.length > MAX_ENTRIES;

  const current = new Map();
  const bufferOf = rel => fs.readFileSync(path.join(root, rel));
  for (const rel of only && prev ? files.filter(f => f === only) : files) current.set(rel, hashBuffer(bufferOf(rel)));

  // Candidate paths: changed since the previous observation, or (first observation) differing from HEAD.
  const changed = new Set();
  if (only) changed.add(only);
  if (!prev || tooMany) {
    for (const rel of ctx ? dirtyRelevant(root) : only ? [] : files) changed.add(rel);
  } else if (!only) {
    for (const [rel, h] of current) if (!prev.entries[rel] || prev.entries[rel].h !== h) changed.add(rel);
    for (const rel of Object.keys(prev.entries)) if (!current.has(rel)) changed.add(rel);
  }

  const approvals = manifests.acceptedDecisionText(root);
  const mctx = manifests.makeContext(root);
  const findings = [];
  const reminders = [];
  let instructionChanged = false;
  const refsNow = new Map();
  // Change-attributed messages (product-input reminders, deleted manifests) apply only to pending changes:
  // with a HEAD, the file must differ from it (a checkout or reset is not an edit); without one, a previous
  // snapshot or an Edit/Write event must exist (an unborn first observation attributes nothing).
  const attributable = (rel, present) => {
    if (ctx && ctx.head) {
      const headBytes = headBuffer(root, ctx, rel);
      return present ? headBytes === null || !headBytes.equals(bufferOf(rel)) : headBytes !== null;
    }
    return !!prev || !!only;
  };
  for (const rel of [...changed].sort()) {
    const kind = kindOf(rel);
    const present = fs.existsSync(path.join(root, rel));
    if (kind === 'instruction') instructionChanged = true;
    if (kind === 'input' && attributable(rel, present)) {
      if (rel === 'CUSTOM_SETTINGS.md') reminders.push('CUSTOM_SETTINGS.md changed: run the custom-settings workflow to synchronize affected surfaces.');
      else reminders.push('SPECIFICATION.md changed: check consistency with CUSTOM_SETTINGS.md (CLAUDE.md, Product sources) and synchronize affected code, tests, and docs (development-workflow).');
    }
    if (kind !== 'manifest') continue;
    if (present) findings.push(...manifests.checkFile(root, rel, mctx));
    else if (!attributable(rel, present)) continue;
    else if (path.posix.basename(rel) === 'Directory.Packages.props') findings.push(lib.finding('error', rel, 'central package management file was deleted', '.claude/rules/backend/dependencies.md'));
    else if (path.posix.basename(rel) === 'package.json') findings.push(lib.finding('warn', rel, 'dependency manifest was deleted; dependency removals go through the add-dependency workflow', '.claude/rules/frontend/dependencies.md'));
    if (!rel.endsWith('.csproj')) continue;
    let cur = null;
    try {
      cur = present ? edgesOf(rel, bufferOf(rel)) : null;
      if (present) refsNow.set(rel, cur);
      const headEdges = ctx ? edgesOf(rel, headBuffer(root, ctx, rel)) : null;
      const prevEdges = prev && !tooMany ? (prev.entries[rel] ? prev.entries[rel].refs || [] : null) : headEdges;
      if (!ctx && !prev) continue; // no baseline outside Git before the first snapshot
      const base = prev && !tooMany && !headMoved ? prevEdges : headEdges;
      findings.push(...graphFindings(rel, cur, base, headEdges, !!ctx, approvals, mctx.roleOf));
    } catch (err) {
      findings.push(lib.finding('error', rel, `project file could not be read (${err.message})`, '.claude/rules/backend/dependencies.md'));
    }
  }

  let instructionErrors = [];
  if (instructionChanged) {
    instructionErrors = require('./check-instructions.cjs').check(root).filter(f => f.severity === 'error');
  }

  // Record the new snapshot (only the edited entry for an Edit/Write observation with an existing snapshot).
  if (!tooMany) {
    const entries = only && prev ? { ...prev.entries } : {};
    for (const [rel, h] of current) {
      const entry = { h };
      if (rel.endsWith('.csproj')) {
        try {
          entry.refs = refsNow.has(rel) ? refsNow.get(rel) : edgesOf(rel, bufferOf(rel));
        } catch {
          entry.refs = [];
        }
      }
      entries[rel] = entry;
    }
    if (only && prev && !current.has(only)) delete entries[only];
    saveState(file, { v: STATE_VERSION, root: lib.realpath(root), head: only && prev ? prev.head : head, entries });
  }
  return { findings, instructionErrors, reminders, firstObservation: !prev, changed: [...changed].sort() };
}

module.exports = { observe, kindOf, statePath, gitContext };
