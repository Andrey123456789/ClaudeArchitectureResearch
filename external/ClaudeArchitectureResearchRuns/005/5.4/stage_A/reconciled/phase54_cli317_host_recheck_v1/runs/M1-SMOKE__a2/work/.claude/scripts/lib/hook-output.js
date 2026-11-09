'use strict';
// Hook result helpers. Decisions are returned as Claude Code hook JSON on stdout
// with exit code 0, so the result does not depend on how a launching shell
// propagates native exit codes. Output is ASCII-only.
// Failure policy: PreToolUse enforcement fails closed (an internal error denies the
// tool call); PostToolUse, PostToolUseFailure, and Stop failures are reported on
// stderr with exit code 1 (visible, non-blocking).

function ascii(text) {
  return String(text).replace(/[^\x09\x0a\x0d\x20-\x7e]/g, (c) => `\\u${c.charCodeAt(0).toString(16).padStart(4, '0')}`);
}

function emit(payload) {
  process.stdout.write(`${ascii(JSON.stringify(payload))}\n`);
  process.exit(0);
}

function errorText(error) {
  return error && error.message ? error.message : String(error);
}

// PreToolUse: deny the tool call and return the reason to Claude.
function denyToolUse(reason) {
  emit({ hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: 'deny', permissionDecisionReason: reason } });
}

// PreToolUse: an internal failure denies the tool call instead of silently allowing it.
function denyOnFailure(hookName, error, consequence) {
  denyToolUse(
    `${hookName} hook failed (${errorText(error)}); ${consequence}, so the command was blocked.\n` +
      'Report the hook failure to the user; the instruction system is repaired through the template-maintenance workflow.\n'
  );
}

// PostToolUse and Stop: return the reason to Claude (Stop: Claude continues once to address it).
function block(reason) {
  emit({ decision: 'block', reason });
}

// PostToolUseFailure: return the reason to Claude alongside the tool error.
function addContext(event, reason) {
  emit({ hookSpecificOutput: { hookEventName: event, additionalContext: reason } });
}

// PreToolUse: ask the user to confirm the tool call; the reason is shown with the prompt.
function askToolUse(reason) {
  emit({ hookSpecificOutput: { hookEventName: 'PreToolUse', permissionDecision: 'ask', permissionDecisionReason: reason } });
}

function allow() {
  process.exit(0);
}

function fail(hookName, error, consequence) {
  process.stderr.write(`${hookName} hook failed (${errorText(error)}); ${consequence}.\n`);
  process.exit(1);
}

module.exports = { denyToolUse, askToolUse, denyOnFailure, block, addContext, allow, fail, ascii };
