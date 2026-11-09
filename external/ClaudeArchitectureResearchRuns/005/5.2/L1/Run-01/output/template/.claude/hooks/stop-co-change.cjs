// Level: 3-project | Owns: Stop-hook co-change reminders — seed/migration rules from the
// selected persistence module (persistence.co-change) resolved through the frame's named
// locations, plus a test-change reminder. Fires at most once per stop (no loop).
// Feedback uses Claude Code JSON output on stdout with exit code 0 (shell-independent);
// exit 1 + stderr reports that the check could not run.
'use strict';

const path = require('path');
const { spawnSync } = require('child_process');
const lib = require('../scripts/lib/project.cjs');

function git(root, args) {
  const result = spawnSync('git', args, { cwd: root, encoding: 'utf8' });
  if (result.error) throw new lib.EnvironmentError(`git is not available (${result.error.message})`);
  if (result.status !== 0) throw new lib.EnvironmentError(`git ${args[0]} failed: ${(result.stderr || '').trim()}`);
  return result.stdout;
}

function changedFiles(root) {
  const prefix = git(root, ['rev-parse', '--show-prefix']).trim();
  const out = git(root, ['status', '--porcelain=v1', '--untracked-files=all', '--', '.']);
  return out.split(/\r?\n/).filter(Boolean).map((line) => {
    let file = line.slice(3);
    if (file.includes(' -> ')) file = file.split(' -> ')[1];
    file = file.replace(/^"|"$/g, '');
    return prefix && file.startsWith(prefix) ? file.slice(prefix.length) : file;
  });
}

function toRegex(locations, ref) {
  const base = locations[ref.location];
  if (base === undefined) {
    throw new lib.EnvironmentError(`co-change rule refers to unknown frame location "${ref.location}" (architecture.check)`);
  }
  return lib.globToRegExp(`${base}${ref.path}`);
}

function main() {
  let input;
  try {
    input = lib.readStdinJson();
  } catch (error) {
    process.stderr.write(`[co-change] could not read hook input: ${error.message}\n`);
    process.exit(1);
  }
  if (input.stop_hook_active) process.exit(0);

  try {
    const root = lib.resolveRoot(__dirname);
    const frame = lib.requireModuleJson(root, 'architecture', 'check.json');
    const coChange = lib.requireModuleJson(root, 'persistence', 'co-change.json');
    const files = changedFiles(root);
    if (files.length === 0) process.exit(0);

    const reminders = [];
    for (const rule of coChange.rules || []) {
      const when = (rule.when || []).map((ref) => toRegex(frame.locations, ref));
      const unless = (rule.unless || []).map((ref) => toRegex(frame.locations, ref));
      const fired = files.some((f) => when.some((re) => re.test(f)));
      const satisfied = files.some((f) => unless.some((re) => re.test(f)));
      if (fired && !satisfied) reminders.push(rule.message);
    }

    const backend = lib.globToRegExp(`${frame.backendRoot || 'backend'}/**/*.cs`);
    const tests = lib.globToRegExp(`${frame.locations['test-project role']}**`);
    const productionChanged = files.some((f) => backend.test(f) && !tests.test(f) && !/\/Migrations\//.test(f));
    const testsChanged = files.some((f) => tests.test(f));
    if (productionChanged && !testsChanged) {
      reminders.push('Backend production code changed without test changes: confirm the changed behavior is covered by maintained tests (regression and probe preservation: `develop`, `verify`).');
    }

    if (reminders.length) {
      process.stdout.write(JSON.stringify({
        decision: 'block',
        reason: `[co-change] Review before finishing:\n- ${reminders.join('\n- ')}\nIf already handled, say so briefly and finish.`,
      }));
    }
    process.exit(0);
  } catch (error) {
    process.stderr.write(`[co-change] skipped: ${error.message}. Review seed, migration, and test co-changes manually (persistence.workflow, verify).\n`);
    process.exit(1);
  }
}

main();
