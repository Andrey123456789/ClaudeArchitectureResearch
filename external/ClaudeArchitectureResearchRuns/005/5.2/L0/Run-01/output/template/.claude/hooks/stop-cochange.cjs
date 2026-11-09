// Level: 3 Project | Stop hook: co-change reminders (seed data, migration review, tests, product sources).
// Reminds once per distinct working-tree state; never re-blocks while stop_hook_active is set, so it
// cannot create an execution loop. Owners: develop (change-type obligations), verify, custom-settings.
'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { execFileSync } = require('child_process');
const { projectRoot, readInput, feedback, fail } = require('./lib.cjs');

const root = projectRoot();
const input = readInput();
if (input.stop_hook_active) process.exit(0);

const stateDir = path.join(root, '.claude', 'hooks', '.state');
const stateFile = path.join(stateDir, 'stop.json');

function readState() {
  try {
    return JSON.parse(fs.readFileSync(stateFile, 'utf8'));
  } catch {
    return {};
  }
}

function writeState(state) {
  fs.mkdirSync(stateDir, { recursive: true });
  fs.writeFileSync(stateFile, JSON.stringify(state, null, 2));
}

let status;
try {
  status = execFileSync('git', ['status', '--porcelain=v1', '-uall'], { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
} catch (error) {
  const state = readState();
  if (state.gitNoticeSession !== input.session_id) {
    writeState({ ...state, gitNoticeSession: input.session_id });
    fail('stop-cochange: co-change reminders skipped — git status failed (not a Git repository, or Git is not installed). ' +
      'Run the develop change-type checks manually.');
  }
  process.exit(0);
}

const entries = status.split(/\r?\n/).filter(Boolean).map(line => ({
  code: line.slice(0, 2),
  file: line.slice(3).replace(/^"|"$/g, '').split(' -> ').pop()
}));
const files = entries.map(e => e.file);
const isTest = f => /(^|\/)[^/]*Tests\//.test(f) || /\.spec\.ts$/.test(f);

const reminders = [];
const modelChanged = files.some(f => /^backend\/[^/]+\.Domain\/.+\.cs$/.test(f) ||
  /^backend\/[^/]+\.Infrastructure\/.*(Configurations|Migrations)\/.+\.cs$/.test(f));
const seederChanged = files.some(f => /Seeding\/.+\.cs$/.test(f));
if (modelChanged && !seederChanged) {
  reminders.push('Domain or persistence model files changed without seeder changes: confirm seeded entities are unaffected ' +
    'or update the seeder (develop, "Persistence and Model Changes").');
}
const newMigrations = entries.filter(e => /Migrations\/.+\.cs$/.test(e.file) && /\?|A/.test(e.code));
if (newMigrations.length) {
  reminders.push(`New migration files (${newMigrations.length}): review them before committing (develop, "Persistence and Model Changes").`);
}
const productionChanged = files.some(f => (/^backend\/.+\.cs$/.test(f) || /^frontend\/.+\.ts$/.test(f)) && !isTest(f));
const testsChanged = files.some(isTest);
if (productionChanged && !testsChanged) {
  reminders.push('Production code changed without test changes: confirm regression and behavioral coverage ' +
    '(develop, "Bug Fixes"; verify, step 4).');
}
if (files.includes('CUSTOM_SETTINGS.md')) {
  reminders.push('CUSTOM_SETTINGS.md changed: confirm the custom-settings workflow synchronized every affected surface.');
}
if (files.includes('SPECIFICATION.md')) {
  reminders.push('SPECIFICATION.md changed: confirm the implementation and CUSTOM_SETTINGS.md are consistent with it.');
}

if (!reminders.length) process.exit(0);

const fingerprint = crypto.createHash('sha1').update(JSON.stringify([reminders, entries])).digest('hex');
const state = readState();
if (state.fingerprint === fingerprint) process.exit(0);
writeState({ ...state, fingerprint });
feedback(`Co-change reminders (shown once for this working-tree state):\n- ${reminders.join('\n- ')}`);
