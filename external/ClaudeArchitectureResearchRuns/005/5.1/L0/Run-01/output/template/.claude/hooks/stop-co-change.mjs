// Level: 3 Project · Owns: Stop-time co-change reminders (seeder, migrations, settings, tests) · Enforcement asset
// Loop safety: exits when stop_hook_active is set, and repeats a reminder only when the changed-file set changes.
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, readdirSync, statSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { readHookInput, projectDir, feedback } from './lib.mjs';

const input = readHookInput();
if (input?.stop_hook_active) process.exit(0);
const root = projectDir(input);

let status = '';
try {
  status = execFileSync('git', ['status', '--porcelain=v1', '-uall'], { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
} catch {
  process.exit(0); // not a Git repository or Git unavailable
}

const changed = status
  .split(/\r?\n/)
  .filter(Boolean)
  .map((line) => line.slice(3).replace(/^"|"$/g, ''))
  .map((entry) => (entry.includes(' -> ') ? entry.split(' -> ')[1] : entry))
  .sort();
if (!changed.length) process.exit(0);

const isTest = (file) => /^backend\/[^/]*Tests\//.test(file) || /\.spec\.ts$/.test(file) || /\/e2e\//.test(file);
const isMigration = (file) => /^backend\/[^/]+\.Infrastructure\/.*Migrations\/.+\.cs$/.test(file);
const isSeeder = (file) => /^backend\/[^/]+\.Infrastructure\/.*Seeding\/.+\.cs$/.test(file);
const isModel = (file) =>
  /^backend\/[^/]+\.Domain\/.+\.cs$/.test(file) ||
  /^backend\/[^/]+\.Infrastructure\/.*(Configurations\/.+|AppDbContext)\.cs$/.test(file) ||
  isMigration(file);
const isProductionCode = (file) =>
  (/^backend\/.+\.cs$/.test(file) && !isTest(file) && !isMigration(file)) ||
  (/^frontend\/.+\.(ts|html)$/.test(file) && !isTest(file));

function seederExists() {
  const backend = path.join(root, 'backend');
  if (!existsSync(backend)) return false;
  const stack = [backend];
  while (stack.length) {
    const directory = stack.pop();
    for (const entry of readdirSync(directory)) {
      if (entry === 'bin' || entry === 'obj') continue;
      const full = path.join(directory, entry);
      if (!statSync(full).isDirectory()) continue;
      if (entry === 'Seeding') return true;
      stack.push(full);
    }
  }
  return false;
}

const reminders = [];
if (changed.some(isModel) && !changed.some(isSeeder) && seederExists()) {
  reminders.push('Domain or persistence model changed without seeder changes: confirm the development seeder still matches (.claude/rules/3-project/data-lifecycle.md).');
}
if (changed.some(isMigration)) {
  reminders.push('Migration files changed: review them before completion (.claude/rules/2-technology/ef-core.md).');
}
if (changed.includes('CUSTOM_SETTINGS.md')) {
  reminders.push('CUSTOM_SETTINGS.md changed: confirm the custom-settings workflow ran (.claude/rules/0-core/product-governance.md).');
}
if (changed.some(isProductionCode) && !changed.some(isTest)) {
  reminders.push('Production code changed without test changes: confirm behavioral coverage (.claude/rules/0-core/testing-principles.md) and that verify ran.');
}
if (!reminders.length) process.exit(0);

const fingerprint = createHash('sha256').update(JSON.stringify([changed, reminders])).digest('hex');
const stateFile = path.join(os.tmpdir(), 'claude-co-change', `${createHash('sha256').update(root).digest('hex').slice(0, 16)}.txt`);
try {
  if (readFileSync(stateFile, 'utf8') === fingerprint) process.exit(0);
} catch {
  // no previous reminder for this project
}
try {
  mkdirSync(path.dirname(stateFile), { recursive: true });
  writeFileSync(stateFile, fingerprint);
} catch {
  // reminders still work without the de-duplication state
}

feedback(['Co-change reminders — address each one or state why it does not apply:', ...reminders.map((reminder) => `- ${reminder}`)]);
