'use strict';
// Hook result helpers. Decisions are returned as Claude Code hook JSON on stdout
// with exit code 0, so the result does not depend on how the launching shell
// (bash, cmd.exe, or PowerShell) propagates native exit codes. Output is ASCII-only.
// Failures are reported on stderr with exit code 1 (non-blocking, visible).

function ascii(text) {
  return String(text).replace(/[^\x09\x0a\x0d\x20-\x7e]/g, (c) => `\\u${c.charCodeAt(0).toString(16).padStart(4, '0')}`);
}

function emit(payload) {
  process.stdout.write(`${ascii(JSON.stringify(payload))}\n`);
  process.exit(0);
}

// PreToolUse: deny the tool call and return the reason to Claude.
function denyToolUse(reason) {
  emit({ hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: 'deny', permissionDecisionReason: reason } });
}

// PostToolUse and Stop: return the reason to Claude (Stop: Claude continues once to address it).
function block(reason) {
  emit({ decision: 'block', reason });
}

function allow() {
  process.exit(0);
}

function fail(hookName, error, consequence) {
  process.stderr.write(`${hookName} hook failed (${error && error.message ? error.message : error}); ${consequence}.\n`);
  process.exit(1);
}

module.exports = { denyToolUse, block, allow, fail, ascii };
