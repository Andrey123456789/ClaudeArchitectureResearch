// Kind: ENF | Scope: common | Capability: — | Loading: command (Stop hook, verify): node "<root>/.claude/scripts/check-cochange.cjs"
// Conforms: —
'use strict';

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const lib = require('./lib.cjs');
const manifests = require('./check-manifests.cjs');

const STATE_FILE = 'claude-cochange-state.json';
const MAX_FINGERPRINTS = 100;

function git(root, args) {
  const result = lib.git(root, args);
  if (!result) throw new Error('git could not be started');
  return result;
}

/** Working-tree changes relative to HEAD (read-only Git), or null when root is not inside a Git work tree. */
function workingTreeChanges(root) {
  const inside = git(root, ['rev-parse', '--is-inside-work-tree']);
  if (inside.status !== 0 || inside.stdout.trim() !== 'true') return null;
  const status = git(root, ['status', '--porcelain=v1', '-z', '-uall', '--no-renames']);
  if (status.status !== 0) throw new Error(`git status failed: ${status.stderr.trim()}`);
  const prefix = git(root, ['rev-parse', '--show-prefix']).stdout.trim();
  const changes = [];
  for (const entry of status.stdout.split('\0')) {
    if (!entry) continue;
    const file = entry.slice(3);
    if (prefix && !file.startsWith(prefix)) continue;
    changes.push({ status: entry.slice(0, 2), path: file.slice(prefix.length) });
  }
  return changes;
}

/** Framework-neutral reminder: backend production code changed without any backend test change. */
function testReminder(changes) {
  const isBackendCs = p => p.startsWith('backend/') && p.endsWith('.cs');
  const isTest = p => /^backend\/[^/]*Tests?\//.test(p);
  const production = changes.filter(c => isBackendCs(c.path) && !isTest(c.path) && !c.status.includes('D'));
  if (!production.length || changes.some(c => isTest(c.path))) return [];
  return [{
    id: 'tests',
    message: `backend production code changed (${production.length} file(s)) with no backend test change; confirm coverage and probe preservation`,
    owner: 'verify workflow (step 4), development-workflow (bug fixes)',
    paths: production.map(c => c.path),
  }];
}

function collectReminders(root, changes) {
  const ctx = manifests.makeContext(root);
  const reminders = [...testReminder(changes)];
  for (const facet of Object.values(ctx.facets)) {
    if (facet.cochange) reminders.push(...facet.cochange(ctx, changes));
  }
  return reminders;
}

/** Content identity of one reminder: its id plus the current bytes of every path that triggered it. */
function fingerprint(root, reminder) {
  const hash = crypto.createHash('sha256').update(reminder.id);
  for (const rel of [...(reminder.paths || [])].sort()) {
    hash.update(`\0${rel}\0`);
    try {
      hash.update(fs.readFileSync(path.join(root, rel)));
    } catch {
      hash.update('\0missing');
    }
  }
  return hash.digest('hex').slice(0, 24);
}

function stateFile(root) {
  const gitDir = git(root, ['rev-parse', '--absolute-git-dir']);
  if (gitDir.status !== 0) throw new Error(`git rev-parse failed: ${gitDir.stderr.trim()}`);
  return path.join(gitDir.stdout.trim(), STATE_FILE);
}

/** Reminders whose content identity was not reported before; records them (bounded, per worktree). */
function unreported(root, reminders) {
  const file = stateFile(root);
  let state = { fingerprints: [] };
  try {
    const loaded = JSON.parse(fs.readFileSync(file, 'utf8'));
    if (Array.isArray(loaded.fingerprints)) state = loaded;
  } catch {
    state = { fingerprints: [] };
  }
  const known = new Set(state.fingerprints);
  const fresh = reminders.filter(r => !known.has(fingerprint(root, r)));
  if (fresh.length) {
    state.fingerprints = [...state.fingerprints, ...fresh.map(r => fingerprint(root, r))].slice(-MAX_FINGERPRINTS);
    fs.writeFileSync(file, JSON.stringify(state));
  }
  return fresh;
}

/**
 * mode "hook": report only reminders whose triggering content was not reported before (no repeated blocking).
 * mode "cli": always report.
 */
function run(root, mode = 'cli') {
  const changes = workingTreeChanges(root);
  if (changes === null) return { applicable: false, reminders: [] };
  const reminders = changes.length ? collectReminders(root, changes) : [];
  if (mode === 'hook' && reminders.length) return { applicable: true, reminders: unreported(root, reminders) };
  return { applicable: true, reminders };
}

function format(reminders) {
  return reminders.map(r => `- ${r.message} -> ${r.owner}`).join('\n');
}

module.exports = { run, format, workingTreeChanges };

if (require.main === module) {
  const root = lib.commandRoot(__dirname);
  const result = run(root, 'cli');
  if (!result.applicable) {
    process.stdout.write(`check-cochange (${root}): NOT APPLICABLE (not a Git work tree)\n`);
  } else if (result.reminders.length) {
    process.stdout.write(`check-cochange (${root}): ${result.reminders.length} reminder(s)\n${format(result.reminders)}\n`);
  } else {
    process.stdout.write(`check-cochange (${root}): no co-change reminders\n`);
  }
}
