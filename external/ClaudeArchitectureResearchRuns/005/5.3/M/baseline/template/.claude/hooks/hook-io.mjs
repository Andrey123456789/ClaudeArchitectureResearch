// Shared helpers for the Claude Code hook entry points in this directory.
// Requires Node.js 18+; works the same on Windows, macOS, and Linux.
//
// Exit-code contract used by the hooks:
//   0  success (optional JSON on stdout for Claude Code)
//   1  hook could not run (environment problem) - reported to the user, work is not blocked
//   2  PreToolUse block - stderr is shown to Claude and the tool call is cancelled

import { readFileSync, existsSync } from 'node:fs';
import { dirname, resolve, relative, isAbsolute, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const hooksDir = dirname(fileURLToPath(import.meta.url));

// Project root: CLAUDE_PROJECT_DIR when Claude Code provides it, otherwise the
// directory two levels above this script (<root>/.claude/hooks).
export function projectRoot() {
  const fromEnv = (process.env.CLAUDE_PROJECT_DIR ?? '').trim();
  const root = fromEnv ? resolve(fromEnv) : resolve(hooksDir, '..', '..');
  if (!existsSync(resolve(root, '.claude'))) {
    fail(`cannot locate the project root: "${root}" has no .claude directory. ` +
      'Run Claude Code from the repository root or set CLAUDE_PROJECT_DIR.');
  }
  return root;
}

// Reads the hook event JSON from stdin.
export function readInput() {
  let raw;
  try {
    raw = readFileSync(0, 'utf8');
  } catch (error) {
    fail(`cannot read hook input from stdin: ${error.message}`);
  }
  raw = raw.replace(/^﻿/, ''); // Windows shells may prepend a UTF-8 byte-order mark
  if (!raw.trim()) {
    fail('hook input on stdin is empty; this script expects Claude Code hook JSON.');
  }
  try {
    return JSON.parse(raw);
  } catch (error) {
    fail(`hook input is not valid JSON: ${error.message}`);
  }
}

// Environment or input problem: report visibly instead of silently skipping.
export function fail(message) {
  process.stderr.write(`[hook error] ${message}\n`);
  process.exit(1);
}

// PreToolUse: cancel the tool call and tell Claude why.
export function blockTool(message) {
  process.stderr.write(`${message}\n`);
  process.exit(2);
}

// Emits a JSON response for Claude Code and exits successfully.
export function respond(payload) {
  process.stdout.write(JSON.stringify(payload));
  process.exit(0);
}

// Adds non-blocking context for Claude after a tool call.
export function postToolContext(text) {
  respond({ hookSpecificOutput: { hookEventName: 'PostToolUse', additionalContext: text } });
}

// Makes Claude address the reason after a tool call.
export function postToolBlock(reason) {
  respond({ decision: 'block', reason });
}

export function done() {
  process.exit(0);
}

// Repository-relative path with forward slashes, or null when outside the root.
export function repoRelative(root, filePath) {
  if (!filePath || typeof filePath !== 'string') return null;
  const absolute = isAbsolute(filePath) ? resolve(filePath) : resolve(root, filePath);
  const rel = relative(root, absolute);
  if (!rel || rel.startsWith('..') || isAbsolute(rel)) return null;
  return rel.split(sep).join('/');
}
