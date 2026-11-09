#!/usr/bin/env node
// Owns: Stop-time co-change reminders (seeder, migration review, test coverage)
// based on the uncommitted change set. Never loops: it stays silent when
// stop_hook_active is set or when the same reminder was already given for an
// unchanged change set.
// Scope: backend, frontend. Loads: Stop hook from .claude/settings.json.

import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';

function readStdin() {
  return new Promise((done) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (chunk) => (data += chunk));
    process.stdin.on('end', () => done(data));
  });
}

function git(root, args) {
  try {
    return execFileSync('git', args, { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
  } catch {
    return null;
  }
}

let input = {};
try { input = JSON.parse((await readStdin()) || '{}'); } catch { process.exit(0); } // never fail the tool call on bad input
if (input.stop_hook_active) process.exit(0);

const root = resolve(process.env.CLAUDE_PROJECT_DIR ?? input.cwd ?? process.cwd());
const status = git(root, ['status', '--porcelain', '--untracked-files=all']);
if (status === null) process.exit(0); // not a Git repository or Git unavailable

const changed = status
  .split(/\r?\n/)
  .filter(Boolean)
  .map((line) => line.slice(3).split(' -> ').pop().replace(/"/g, '').replace(/\\/g, '/'));
if (changed.length === 0) process.exit(0);

const isTest = (f) => /^backend\/[^/]*Tests\//i.test(f) || /\.spec\.ts$/i.test(f) || /\/e2e\//i.test(f);
const isMigration = (f) => /\/Migrations\//.test(f) && !/ModelSnapshot\.cs$/.test(f);
const isModel = (f) =>
  /^backend\/[^/]+\.Domain\/.+\.cs$/i.test(f) || /\/Persistence\/Configurations\/.+\.cs$/.test(f) || isMigration(f);
const isSeeder = (f) => /\/Seeding\//.test(f);
const isProduction = (f) =>
  !isTest(f) && !isMigration(f) && (/^backend\/.+\.cs$/i.test(f) || /^frontend\/.+\.ts$/i.test(f));

const reminders = [];
const tracked = git(root, ['ls-files']) ?? '';
const hasSeeder = /\/Seeding\//.test(tracked) || changed.some(isSeeder);

if (hasSeeder && changed.some(isModel) && !changed.some(isSeeder)) {
  reminders.push(
    'Domain/persistence model files changed without a seeder change: confirm seeded entities are unaffected ' +
      'or update the seeder (.claude/rules/persistence.md, Development Data Seeding).',
  );
}
if (changed.some(isMigration)) {
  reminders.push('Migrations changed: review them before committing (.claude/rules/persistence.md, Migrations).');
}
if (changed.some(isProduction) && !changed.some(isTest)) {
  reminders.push(
    'Production code changed without test changes: confirm coverage and preserved behavioral probes ' +
      '(verify workflow, step 4).',
  );
}
if (reminders.length === 0) process.exit(0);

// Remind once per distinct change set.
const fingerprint = createHash('sha256').update(root + '\n' + [...changed].sort().join('\n') + reminders.join('\n')).digest('hex');
const stateFile = join(tmpdir(), `claude-stop-check-${createHash('sha256').update(root).digest('hex').slice(0, 16)}`);
let previous = '';
try { previous = readFileSync(stateFile, 'utf8'); } catch { /* first run */ }
if (previous === fingerprint) process.exit(0);
try { writeFileSync(stateFile, fingerprint); } catch { /* best effort */ }

process.stdout.write(
  JSON.stringify({
    decision: 'block',
    reason: `Before finishing, address or explicitly confirm:\n- ${reminders.join('\n- ')}`,
  }),
);
process.exit(0);
