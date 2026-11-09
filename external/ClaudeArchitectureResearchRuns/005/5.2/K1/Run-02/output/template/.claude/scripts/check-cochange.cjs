// Kind: ENF | Scope: common | Capability: — | Loading: command (Stop hook, verify): node .claude/scripts/check-cochange.cjs
'use strict';

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const lib = require('./lib.cjs');
const manifests = require('./check-manifests.cjs');

const STATE_FILE = 'claude-cochange-state.json';
const MAX_FINGERPRINTS = 50;

function git(root, args) {
  const result = spawnSync('git', args, { cwd: root, encoding: 'utf8', windowsHide: true });
  if (result.error) throw new Error(`git could not be started (${result.error.message})`);
  return result;
}

/** Working-tree changes relative to HEAD, or null when root is not inside a Git work tree. */
function workingTreeChanges(root) {
  const inside = git(root, ['rev-parse', '--is-inside-work-tree']);
  if (inside.status !== 0 || inside.stdout.trim() !== 'true') return null;
  const status = git(root, ['status', '--porcelain=v1', '-uall']);
  if (status.status !== 0) throw new Error(`git status failed: ${status.stderr.trim()}`);
  const prefix = git(root, ['rev-parse', '--show-prefix']).stdout.trim();
  const changes = [];
  for (const line of status.stdout.split(/\r?\n/)) {
    if (!line.trim()) continue;
    let file = line.slice(3);
    if (file.includes(' -> ')) file = file.split(' -> ')[1];
    file = file.replace(/^"|"$/g, '');
    if (prefix && !file.startsWith(prefix)) continue;
    changes.push({ status: line.slice(0, 2), path: file.slice(prefix.length) });
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

function fingerprint(changes, reminders) {
  const data = JSON.stringify({ c: changes.map(c => c.path).sort(), r: reminders.map(r => r.id).sort() });
  return crypto.createHash('sha256').update(data).digest('hex').slice(0, 16);
}

function stateFile(root) {
  const gitDir = git(root, ['rev-parse', '--absolute-git-dir']);
  if (gitDir.status !== 0) throw new Error(`git rev-parse failed: ${gitDir.stderr.trim()}`);
  return path.join(gitDir.stdout.trim(), STATE_FILE);
}

/** Returns true when this fingerprint was not reported before (and records it). */
function isNew(root, print) {
  const file = stateFile(root);
  let state = { fingerprints: [] };
  if (fs.existsSync(file)) {
    try {
      state = JSON.parse(fs.readFileSync(file, 'utf8'));
    } catch {
      state = { fingerprints: [] };
    }
  }
  if (state.fingerprints.includes(print)) return false;
  state.fingerprints = [...state.fingerprints, print].slice(-MAX_FINGERPRINTS);
  fs.writeFileSync(file, JSON.stringify(state));
  return true;
}

/**
 * mode "hook": report only reminder sets not reported before (no repeated blocking).
 * mode "cli": always report.
 */
function run(root, mode = 'cli') {
  const changes = workingTreeChanges(root);
  if (changes === null) return { applicable: false, reminders: [] };
  const reminders = changes.length ? collectReminders(root, changes) : [];
  if (mode === 'hook' && reminders.length && !isNew(root, fingerprint(changes, reminders))) {
    return { applicable: true, reminders: [] };
  }
  return { applicable: true, reminders };
}

function format(reminders) {
  return reminders.map(r => `- ${r.message} -> ${r.owner}`).join('\n');
}

module.exports = { run, format, workingTreeChanges };

if (require.main === module) {
  const root = lib.rootFrom(__dirname, 2);
  const result = run(root, 'cli');
  if (!result.applicable) {
    process.stdout.write('check-cochange: NOT APPLICABLE (not a Git work tree)\n');
  } else if (result.reminders.length) {
    process.stdout.write(`check-cochange: ${result.reminders.length} reminder(s)\n${format(result.reminders)}\n`);
  } else {
    process.stdout.write('check-cochange: no co-change reminders\n');
  }
}
