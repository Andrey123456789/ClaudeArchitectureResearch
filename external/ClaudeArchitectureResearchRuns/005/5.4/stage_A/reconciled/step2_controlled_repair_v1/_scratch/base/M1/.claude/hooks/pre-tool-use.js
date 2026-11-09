'use strict';
// PreToolUse hook entry point (Bash, PowerShell).
// Denies NuGet/npm dependency changes until the add-dependency workflow has been
// applied, project-reference changes until the project-structure procedure has
// been applied, and npm peer-dependency override flags without approval. Only the
// command text is classified (scripts/lib/dependency-commands.js); no repository
// state is read.
// The decision is returned as hook JSON (see scripts/lib/hook-output.js).
// This is critical enforcement and fails closed: an internal error or malformed hook
// input (a leading byte-order mark is not malformed) denies the command, a failure to
// load the helpers exits with the blocking code 2, and settings.json declares
// onFailure "block" for any other crash or timeout.

let out = null;
try {
  out = require('../scripts/lib/hook-output.js');
  const { readStdinJson } = require('../scripts/lib/common.js');
  const { analyzeCommand } = require('../scripts/lib/dependency-commands.js');
  const input = readStdinJson();
  if (typeof input.tool_name !== 'string') throw new Error('hook input has no tool_name');
  const tool = input.tool_name;
  if (['Bash', 'PowerShell'].includes(tool)) {
    const result = analyzeCommand(input.tool_input && input.tool_input.command, tool);
    if (result.block) out.denyToolUse(result.message);
  }
  out.allow();
} catch (e) {
  if (out) out.denyOnFailure('pre-tool-use', e, 'dependency and project-reference routing could not be applied');
  process.stderr.write(`pre-tool-use hook failed (${e && e.message ? e.message : e}); the command was blocked.\n`);
  process.exit(2);
}
