// Shared helpers for the Claude Code hook entry points in this directory.
// Requires Node.js 18+; works the same on Windows, macOS, and Linux.
//
// Exit-code contract used by the hooks:
//   0  success (optional JSON on stdout for Claude Code)
//   1  hook could not run (environment problem) - reported to the user; work is
//      not blocked, except for the PreToolUse guard, which settings.json
//      registers with "onFailure": "block" (fail closed)
//   2  PreToolUse block - stderr is shown to Claude and the tool call is cancelled
//
// Roots: settings.json launches each hook through ${CLAUDE_PROJECT_DIR}, which
// only locates the script. The repository state a hook inspects is the active
// root, derived from the hook input - its "cwd", or the edited file's location
// for file events (.claude/scripts/repo-root.mjs).

import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync, statSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve, relative, isAbsolute, sep, join } from 'node:path';
import { resolveActiveRepository, canonical } from '../scripts/repo-root.mjs';
import { discover } from '../scripts/check-manifests.mjs';

// Reads the hook event JSON from stdin.
export function readInput() {
  let raw;
  try {
    raw = readFileSync(0, 'utf8');
  } catch (error) {
    fail(`cannot read hook input from stdin: ${error.message}`);
  }
  raw = raw.replace(/^﻿+/, ''); // Windows PowerShell may prepend one or more UTF-8 byte-order marks
  if (!raw.trim()) {
    fail('hook input on stdin is empty; this script expects Claude Code hook JSON.');
  }
  try {
    return JSON.parse(raw);
  } catch (error) {
    fail(`hook input is not valid JSON: ${error.message}`);
  }
}

// Directory the event happened in: the input "cwd" (resolved against the
// process directory when relative), or the process directory when absent.
export function startDirectory(input) {
  const cwd = typeof input.cwd === 'string' ? input.cwd.trim() : '';
  return cwd ? resolve(process.cwd(), cwd) : process.cwd();
}

// Active repository or worktree ({ root, top, gitDir }) for this event; reports
// and exits when it cannot be established, so no check silently runs against
// the wrong tree.
export function activeRepository(input) {
  try {
    return resolveActiveRepository(startDirectory(input));
  } catch (error) {
    fail(`${error.message}. Repository checks were NOT run.`);
  }
}

// Environment or input problem: report visibly instead of silently skipping.
export function fail(message) {
  process.stderr.write(`[hook error] ${message}\n`);
  process.exit(1);
}

// PreToolUse: cancel the tool call and tell Claude why.
export function blockTool(message) {
  process.stderr.write(`${message}\n`);
  process.exit(2);
}

// Emits a JSON response for Claude Code and exits successfully.
export function respond(payload) {
  process.stdout.write(JSON.stringify(payload));
  process.exit(0);
}

// Adds non-blocking context for Claude after a tool call (event: PostToolUse,
// or PostToolUseFailure after a tool call that failed).
export function postToolContext(text, event = 'PostToolUse') {
  respond({ hookSpecificOutput: { hookEventName: event, additionalContext: text } });
}

// Makes Claude address the reason after a tool call. A failed tool call cannot
// be blocked any more; the reason reaches Claude as context with the error.
export function postToolBlock(reason, event = 'PostToolUse') {
  if (event === 'PostToolUseFailure') postToolContext(reason, event);
  respond({ decision: 'block', reason });
}

export function done() {
  process.exit(0);
}

// Repository-relative path with forward slashes, or null when outside the root.
export function repoRelative(root, filePath) {
  if (!filePath || typeof filePath !== 'string') return null;
  const absolute = canonical(isAbsolute(filePath) ? filePath : resolve(root, filePath));
  const rel = relative(root, absolute);
  if (!rel || rel.startsWith('..') || isAbsolute(rel)) return null;
  return rel.split(sep).join('/');
}

// Bounded identity of a file's current content: SHA-256 of its bytes, or size
// and modification time above 1 MB; "missing" when the file does not exist.
export function contentId(file) {
  try {
    const stat = statSync(file);
    if (!stat.isFile()) return 'not-a-file';
    if (stat.size > 1024 * 1024) return `size:${stat.size}:mtime:${stat.mtimeMs}`;
    return createHash('sha256').update(readFileSync(file)).digest('hex');
  } catch {
    return 'missing';
  }
}

// ---------------------------------------------------------------- manifest state
// Manifests (.csproj, Directory.Packages.props, package.json) whose content
// differs from the last manifest check recorded for root, so a change made by
// any shell mechanism (sed, Set-Content, git checkout, a script) is validated
// once. The first check of a worktree (no snapshot recorded yet), or a HEAD
// change that cannot be diffed, takes a one-time snapshot of every manifest, so
// a revision reached by the first shell command cannot bring in an unchecked
// manifest. Afterwards the candidates in a Git working tree are the manifests
// Git reports as changed (deletions and both sides of a rename included), plus
// those changed between the recorded and the current HEAD (checkout, merge,
// reset); without Git no narrower signal exists, so every manifest is a
// candidate. A manifest that disappears is reported once as removed. State
// lives in the Git directory of the worktree (or CLAUDE_HOOK_STATE_DIR, or the
// temp directory without Git).

const MANIFEST_PATHSPECS = [':(glob,icase)**/*.csproj', ':(glob)**/Directory.Packages.props', ':(glob)**/package.json'];

export function isManifestPath(rel) {
  const parts = rel.split('/');
  const name = parts[parts.length - 1];
  if (parts.includes('node_modules') || parts[0] === '.claude') return false;
  return name.toLowerCase().endsWith('.csproj') || name === 'Directory.Packages.props' || name === 'package.json';
}

// repo: { root, top, gitDir } from resolveActiveRepository. Returns { changed:
// absolute paths of existing manifests to validate, removed: root-relative
// paths of manifests that disappeared, first: this is the worktree's initial
// snapshot, snapshot: every manifest was taken (initial, or the recorded HEAD
// could not be compared), save() }.
export function manifestChanges(repo) {
  const { root } = repo;
  const state = loadManifestState(repo);
  const candidates = new Set();
  let head = null;
  let snapshot = !state.baseline;
  if (repo.top) {
    const status = gitOutput(root, ['status', '--porcelain=v2', '-z', '--branch', '--untracked-files=all', '--', ...MANIFEST_PATHSPECS]);
    const fields = (status ?? '').split('\0');
    for (let i = 0; i < fields.length; i += 1) {
      const field = fields[i];
      if (field.startsWith('# branch.oid ')) head = /^[0-9a-f]{40,64}$/.test(field.slice(13)) ? field.slice(13) : null;
      else if (field.startsWith('1 ')) candidates.add(resolve(repo.top, afterFields(field, 8)));
      else if (field.startsWith('2 ')) {
        candidates.add(resolve(repo.top, afterFields(field, 9)));
        i += 1; // the next field is the rename or copy source: a removal for a rename
        if (fields[i]) candidates.add(resolve(repo.top, fields[i]));
      } else if (field.startsWith('u ')) candidates.add(resolve(repo.top, afterFields(field, 10)));
      else if (field.startsWith('? ')) candidates.add(resolve(repo.top, field.slice(2)));
    }
    if (head && state.head && state.head !== head) {
      const moved = gitOutput(root, ['diff', '--name-only', '-z', state.head, head, '--', ...MANIFEST_PATHSPECS]);
      if (moved === null) snapshot = true; // the recorded HEAD cannot be compared
      for (const path of (moved ?? '').split('\0').filter(Boolean)) candidates.add(resolve(repo.top, path));
    }
  }
  if (!repo.top || snapshot) for (const file of discover(root)) candidates.add(file);
  const files = {};
  for (const file of candidates) {
    const rel = repoRelative(root, file);
    if (rel && isManifestPath(rel)) files[rel] = contentId(file);
  }
  if (!repo.top) {
    // Without Git every manifest is recorded, so one no longer found was removed.
    for (const rel of Object.keys(state.files)) if (!(rel in files) && state.files[rel] !== 'missing') files[rel] = 'missing';
  }
  const rels = Object.keys(files).sort();
  const changed = rels.filter((rel) => files[rel] !== 'missing' && files[rel] !== state.files[rel]).map((rel) => resolve(root, rel));
  const removed = rels.filter((rel) => files[rel] === 'missing' && state.files[rel] !== 'missing');
  return {
    changed,
    removed,
    first: !state.baseline,
    snapshot,
    save: () => saveManifestState(repo, state, { head: head ?? state.head ?? null, baseline: true, files }),
  };
}

// Records manifests that were just validated (file-change hook), so a later
// shell command does not report them again.
export function rememberManifests(repo, absoluteFiles) {
  const state = loadManifestState(repo);
  const files = { ...state.files };
  for (const file of absoluteFiles) {
    const rel = repoRelative(repo.root, file);
    if (rel) files[rel] = contentId(file);
  }
  saveManifestState(repo, state, { head: state.head ?? null, baseline: state.baseline, files });
}

function afterFields(line, count) {
  let at = 0;
  for (let k = 0; k < count; k += 1) at = line.indexOf(' ', at) + 1;
  return line.slice(at);
}

function gitOutput(cwd, args) {
  try {
    return execFileSync('git', args, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'], timeout: 15000, windowsHide: true });
  } catch {
    return null;
  }
}

function manifestStatePath(repo) {
  const dir = (process.env.CLAUDE_HOOK_STATE_DIR ?? '').trim() || repo.gitDir || join(tmpdir(), 'claude-hooks');
  return join(dir, `claude-manifest-state-${createHash('sha256').update(repo.root).digest('hex').slice(0, 12)}.json`);
}

function loadManifestState(repo) {
  try {
    const state = JSON.parse(readFileSync(manifestStatePath(repo), 'utf8'));
    return { head: state.head ?? null, baseline: state.baseline === true, files: state.files && typeof state.files === 'object' ? state.files : {} };
  } catch {
    return { head: null, baseline: false, files: {} };
  }
}

function saveManifestState(repo, previous, next) {
  if (JSON.stringify(previous) === JSON.stringify(next)) return;
  const path = manifestStatePath(repo);
  try {
    mkdirSync(join(path, '..'), { recursive: true });
    writeFileSync(path, JSON.stringify(next), 'utf8');
  } catch {
    // Without writable state a change may be validated again later; it is still validated now.
  }
}
