#!/usr/bin/env node
// Claude Code Stop hook: co-change reminders based on the Git working tree.
//   - Domain/persistence model changed but the development seeder did not;
//   - EF Core migration files changed (review before committing);
//   - production code changed without any test change.
// Each distinct set of reminders is shown once (state is kept in the Git
// directory, or in CLAUDE_HOOK_STATE_DIR when set), and nothing is reported
// while stop_hook_active is true, so the hook cannot create a stop loop.
// Configured in .claude/settings.json as: node .claude/hooks/stop-co-change.mjs
// Manual test: echo '{"hook_event_name":"Stop","stop_hook_active":false}' | node .claude/hooks/stop-co-change.mjs

import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, writeFileSync, readdirSync, mkdirSync } from 'node:fs';
import { join, resolve, relative, sep, isAbsolute } from 'node:path';
import { readInput, projectRoot, respond, done } from './hook-io.mjs';

const STATE_FILE = 'claude-co-change-state.json';
const SKIP_DIRS = new Set(['bin', 'obj', 'node_modules', '.git', '.vs']);

const input = readInput();
if (input.stop_hook_active === true) done();

const root = projectRoot();

let topLevel;
let gitDir;
let status;
try {
  topLevel = git(['rev-parse', '--show-toplevel']).trim();
  gitDir = git(['rev-parse', '--absolute-git-dir']).trim();
  status = git(['status', '--porcelain=v1', '--untracked-files=all', '-z']);
} catch (error) {
  const reason = error.code === 'ENOENT' ? 'git is not installed or not on PATH' : 'the project is not inside a Git repository';
  respond({ systemMessage: `Co-change check skipped: ${reason}.` });
}

const changed = parseStatus(status)
  .map((path) => toProjectRelative(resolve(topLevel, path)))
  .filter((path) => path !== null);
if (changed.length === 0) done();

const isBackendTest = (p) => /^backend\/[^/]*Tests\//i.test(p);
const isMigration = (p) => /^backend\/.+\/Migrations\/[^/]+\.cs$/i.test(p);
const isSeeder = (p) => /^backend\/.+(\/Seeding\/|DbSeeder[^/]*\.cs$)/i.test(p);
const isModel = (p) => !isBackendTest(p) && (
  /^backend\/[^/]+\.Domain\/.+\.cs$/i.test(p) ||
  /^backend\/.+\/Persistence\/Configurations\/.+\.cs$/i.test(p) ||
  /^backend\/.+DbContext\.cs$/i.test(p));
const isBackendProduction = (p) => /^backend\/.+\.cs$/i.test(p) && !isBackendTest(p) && !isMigration(p);
const isFrontendTest = (p) => /^frontend\/.+(\.spec\.ts$|\/e2e\/)/i.test(p);
const isFrontendProduction = (p) => /^frontend\/[^/]+\/src\/.+\.ts$/i.test(p) && !isFrontendTest(p);

const reminders = [];
if (changed.some(isModel) && !changed.some(isSeeder) && seederExists()) {
  reminders.push('Domain or persistence model files changed but the development seeder did not: confirm the seeded ' +
    'entities are unaffected or update DbSeeder (development-workflow, Persistence model and migrations).');
}
if (changed.some(isMigration)) {
  reminders.push('EF Core migration files changed: review them before committing (development-workflow, Persistence model and migrations).');
}
const backendGap = changed.some(isBackendProduction) && !changed.some(isBackendTest);
const frontendGap = changed.some(isFrontendProduction) && !changed.some(isFrontendTest);
if (backendGap || frontendGap) {
  reminders.push('Production code changed without test changes: confirm regression coverage for bug fixes and that ' +
    'behavioral probes are preserved as maintained tests (development-workflow, Bug fixes; verify, step 4).');
}
if (reminders.length === 0) done();

const fingerprint = createHash('sha256')
  .update(JSON.stringify({ reminders, changed: [...changed].sort() }))
  .digest('hex');
const stateDir = (process.env.CLAUDE_HOOK_STATE_DIR ?? '').trim() || gitDir;
const statePath = join(stateDir, STATE_FILE);
try {
  if (existsSync(statePath) && JSON.parse(readFileSync(statePath, 'utf8')).fingerprint === fingerprint) done();
} catch {
  // Unreadable state: fall through and remind again.
}
try {
  mkdirSync(stateDir, { recursive: true });
  writeFileSync(statePath, JSON.stringify({ fingerprint }), 'utf8');
} catch {
  // Without writable state the reminder may repeat on a later stop; it is still shown now.
}

respond({
  decision: 'block',
  reason: 'Co-change check (shown once for this set of changes):\n- ' + reminders.join('\n- ') +
    '\nAddress each item or state briefly why it does not apply, then finish.',
});

function git(args) {
  return execFileSync('git', args, { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
}

function parseStatus(raw) {
  const fields = raw.split('\0');
  const paths = [];
  for (let i = 0; i < fields.length; i += 1) {
    const entry = fields[i];
    if (entry.length < 4) continue;
    const code = entry.slice(0, 2);
    paths.push(entry.slice(3));
    if (code.includes('R') || code.includes('C')) i += 1; // skip the rename/copy source path
  }
  return paths;
}

function toProjectRelative(absolute) {
  const rel = relative(root, absolute);
  if (!rel || rel.startsWith('..') || isAbsolute(rel)) return null;
  return rel.split(sep).join('/');
}

function seederExists() {
  const backend = join(root, 'backend');
  if (!existsSync(backend)) return false;
  const stack = [backend];
  while (stack.length > 0) {
    const dir = stack.pop();
    let entries;
    try {
      entries = readdirSync(dir, { withFileTypes: true });
    } catch {
      continue;
    }
    for (const entry of entries) {
      if (entry.isDirectory()) {
        if (entry.name === 'Seeding') return true;
        if (!SKIP_DIRS.has(entry.name)) stack.push(join(dir, entry.name));
      } else if (/^DbSeeder.*\.cs$/i.test(entry.name)) {
        return true;
      }
    }
  }
  return false;
}
