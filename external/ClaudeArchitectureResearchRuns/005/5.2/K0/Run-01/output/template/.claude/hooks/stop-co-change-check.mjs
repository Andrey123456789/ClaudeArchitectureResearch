// Kind: ENF | Scope: repo/meta | Owns: Stop-time co-change reminders (seed data, migrations, tests) | Loads: Stop hook
//
// Blocks a stop once with reminders when the working tree shows a co-change gap. It never blocks
// twice in a row (stop_hook_active) and does not repeat an identical reminder (state kept in .git).

import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { readHookInput, resolveProjectRoot, fail, feedback } from './hook-io.mjs';

const HOOK = 'stop-co-change-check';
const STATE_FILE = 'claude-co-change-reminder.json';

const isTestPath = (p) => /(^|\/)[^/]*Tests\//i.test(p);
const isMigration = (p) => /\/Migrations\/[^/]+\.cs$/i.test(p);
const isSeeder = (p) => /\/Seeding\//i.test(p);
const isModelPath = (p) => /^backend\/[^/]+\.Domain\/.+\.cs$/i.test(p)
  || /\/Persistence\/Configurations\/.+\.cs$/i.test(p)
  || /\/Persistence\/AppDbContext\.cs$/i.test(p)
  || isMigration(p);

export function parsePorcelain(output) {
  return output
    .split(/\r?\n/)
    .filter((line) => line.length > 3)
    .map((line) => line.slice(3))
    .map((entry) => (entry.includes(' -> ') ? entry.split(' -> ').pop() : entry))
    .map((entry) => entry.replace(/^"|"$/g, '').split('\\').join('/'));
}

function hasSeeder(root) {
  const backend = path.join(root, 'backend');
  if (!existsSync(backend)) return false;
  const stack = [backend];
  while (stack.length) {
    const dir = stack.pop();
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      if (entry.isDirectory()) {
        if (!['bin', 'obj', 'node_modules', '.git'].includes(entry.name)) stack.push(path.join(dir, entry.name));
      } else if (entry.name === 'DbSeeder.cs') {
        return true;
      }
    }
  }
  return false;
}

export function reminders(changed, seederExists) {
  const result = [];
  const backendProduction = changed.filter((p) => p.startsWith('backend/') && p.endsWith('.cs') && !isTestPath(p));
  const model = changed.filter(isModelPath);
  if (model.length && seederExists && !changed.some(isSeeder)) {
    result.push('Domain/persistence model files changed without a development-seeder change: confirm seeded entities are unaffected or update the seeder — development-workflow § Co-change Obligations.');
  }
  if (changed.some(isMigration)) {
    result.push('EF Core migration files changed: review every generated migration before committing — development-workflow § Co-change Obligations.');
  }
  if (backendProduction.length && !changed.some(isTestPath)) {
    result.push('Backend production code changed without test changes: confirm coverage and preserved behavioral probes — verify § 4; regression tests: development-workflow § Co-change Obligations.');
  }
  return result;
}

function git(root, args) {
  const result = spawnSync('git', args, { cwd: root, encoding: 'utf8' });
  if (result.error || result.status !== 0) {
    fail(HOOK, `"git ${args.join(' ')}" failed (${result.error?.message ?? result.stderr.trim()}); co-change reminders need a Git working tree`);
  }
  return result.stdout;
}

const isEntryPoint = process.argv[1] && import.meta.url.endsWith(process.argv[1].split(/[\\/]/).pop());
if (isEntryPoint) {
  const input = await readHookInput(HOOK);
  if (input?.stop_hook_active === true) {
    process.exit(0);
  }
  const root = resolveProjectRoot(HOOK, input);
  const changed = parsePorcelain(git(root, ['status', '--porcelain=v1', '--untracked-files=all']));
  const found = reminders(changed, hasSeeder(root));
  if (!found.length) {
    process.exit(0);
  }
  const gitDir = path.resolve(root, git(root, ['rev-parse', '--git-dir']).trim());
  const statePath = path.join(gitDir, STATE_FILE);
  const fingerprint = createHash('sha256').update(JSON.stringify({ found, changed: [...changed].sort() })).digest('hex');
  const previous = existsSync(statePath) ? JSON.parse(readFileSync(statePath, 'utf8')).fingerprint : null;
  if (previous === fingerprint) {
    process.exit(0);
  }
  writeFileSync(statePath, JSON.stringify({ fingerprint }), 'utf8');
  feedback(`Co-change check before stopping:\n- ${found.join('\n- ')}\nAddress these or state why they do not apply, then finish.`);
}
