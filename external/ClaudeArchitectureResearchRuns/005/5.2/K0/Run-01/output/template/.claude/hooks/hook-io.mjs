// Kind: ENF | Scope: repo/meta | Owns: shared hook input/output helpers | Loads: imported by the hook entry points in this directory
//
// Exit codes follow the Claude Code hook contract:
//   0 - nothing to report;
//   1 - the hook itself could not run (shown to the user; enforcement was NOT applied);
//   2 - feedback for Claude (blocks a PreToolUse call or a Stop; reported after a PostToolUse call).

import { existsSync } from 'node:fs';
import path from 'node:path';

export async function readHookInput(hookName) {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  const raw = Buffer.concat(chunks).toString('utf8').trim();
  if (!raw) {
    fail(hookName, 'no hook input received on stdin');
  }
  try {
    return JSON.parse(raw);
  } catch (error) {
    fail(hookName, `hook input is not valid JSON (${error.message})`);
  }
}

// The project root is the directory holding both CLAUDE.md and .claude/settings.json.
// CLAUDE_PROJECT_DIR is read here (not expanded by a shell) so hook commands stay shell-neutral.
export function resolveProjectRoot(hookName, input) {
  const candidates = [process.env.CLAUDE_PROJECT_DIR, input?.cwd, process.cwd()].filter(Boolean);
  for (const candidate of candidates) {
    let dir = path.resolve(candidate);
    for (;;) {
      if (isProjectRoot(dir)) {
        return dir;
      }
      const parent = path.dirname(dir);
      if (parent === dir) {
        break;
      }
      dir = parent;
    }
  }
  fail(hookName, `cannot locate the project root (CLAUDE.md + .claude/settings.json) from: ${candidates.join(', ')}`);
}

export function isProjectRoot(dir) {
  return existsSync(path.join(dir, 'CLAUDE.md')) && existsSync(path.join(dir, '.claude', 'settings.json'));
}

// Converts an absolute or root-relative path to a forward-slash path relative to the root.
// Returns null when the path lies outside the root.
export function toProjectRelative(root, filePath) {
  const absolute = path.resolve(root, filePath);
  const relative = path.relative(root, absolute);
  if (relative.startsWith('..') || path.isAbsolute(relative)) {
    return null;
  }
  return relative.split(path.sep).join('/');
}

export function fail(hookName, message) {
  process.stderr.write(`[${hookName}] ${message}. The check was not applied.\n`);
  process.exit(1);
}

export function feedback(message) {
  process.stderr.write(message.endsWith('\n') ? message : `${message}\n`);
  process.exit(2);
}
