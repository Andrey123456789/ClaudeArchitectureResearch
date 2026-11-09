// Kind: ENF | Scope: common | Capability: — | Loading: Stop hook (.claude/settings.json) | Co-change reminders (seed data, migrations, tests, product inputs) once per distinct set per session, never looping
import { spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { EnforcementError, projectRoot, readStdinJson, loadEnforcement, matchesAny, toRootRelative, stableHash } from '../scripts/lib/common.mjs';

function git(root, args) {
  return spawnSync('git', ['-C', root, ...args], { encoding: 'utf8', timeout: 10000, windowsHide: true });
}

// Read-only Git queries: the hook never changes repository state.
function changedFiles(root) {
  const top = git(root, ['rev-parse', '--show-toplevel']);
  if (top.error) {
    return { error: `git is not available (${top.error.message})` };
  }
  if (top.status !== 0) {
    return { error: 'the project is not inside a Git repository' };
  }
  const toplevel = top.stdout.trim();
  const status = git(root, ['-c', 'core.quotepath=false', 'status', '--porcelain=v1', '-z', '--untracked-files=all']);
  if (status.status !== 0) {
    return { error: `git status failed (${status.stderr.trim()})` };
  }
  const files = [];
  const entries = status.stdout.split('\0').filter(Boolean);
  for (let i = 0; i < entries.length; i++) {
    const entry = entries[i];
    const code = entry.slice(0, 2);
    const relative = toRootRelative(root, path.join(toplevel, entry.slice(3)));
    if (relative) {
      files.push(relative);
    }
    if (code.includes('R') || code.includes('C')) {
      i++; // the next entry is the original path of a rename or copy
    }
  }
  return { files };
}

function evaluate(rules, files) {
  const messages = [];
  for (const rule of rules) {
    const triggering = files.filter((f) => matchesAny(f, rule.when) && !matchesAny(f, rule.exclude ?? []));
    if (triggering.length === 0) {
      continue;
    }
    if ((rule.unless ?? []).length > 0 && files.some((f) => matchesAny(f, rule.unless))) {
      continue;
    }
    messages.push(rule.message);
  }
  return messages;
}

function alreadyEmitted(stateFile, key) {
  let keys = [];
  if (existsSync(stateFile)) {
    try {
      keys = JSON.parse(readFileSync(stateFile, 'utf8'));
    } catch {
      keys = [];
    }
  }
  if (keys.includes(key)) {
    return true;
  }
  writeFileSync(stateFile, JSON.stringify([...keys, key]));
  return false;
}

async function main() {
  const input = await readStdinJson();
  if (input.stop_hook_active) {
    return; // Claude is already continuing because of this hook: never block twice in a row.
  }
  const root = projectRoot();
  const stateFile = path.join(tmpdir(), `claude-cochange-${stableHash(`${root}|${input.session_id ?? 'no-session'}`)}.json`);
  const { policy, facets } = loadEnforcement(root);

  const changes = changedFiles(root);
  if (changes.error) {
    const message = `Co-change reminders are not available: ${changes.error}.`;
    if (!alreadyEmitted(stateFile, stableHash(message))) {
      process.stdout.write(`${JSON.stringify({ systemMessage: message })}\n`);
    }
    return;
  }

  const rules = [...(policy.coChange ?? []), ...facets.flatMap((f) => f.coChange ?? [])];
  const messages = evaluate(rules, changes.files);
  if (messages.length === 0 || alreadyEmitted(stateFile, stableHash(messages.join('\n')))) {
    return;
  }
  const reason = `Co-change check on uncommitted files (address each item or state why it does not apply):\n${messages.map((m) => `- ${m}`).join('\n')}`;
  process.stdout.write(`${JSON.stringify({ decision: 'block', reason })}\n`);
}

main().then(
  () => process.exit(0),
  (error) => {
    const detail = error instanceof EnforcementError ? error.message : error.stack;
    process.stderr.write(`Co-change Stop hook failed (reminders did not run): ${detail}\n`);
    process.exit(1);
  },
);
