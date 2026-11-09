'use strict';
// PreToolUse hook entry point (Bash, PowerShell).
// Denies dependency add/update/remove commands until the add-dependency
// workflow has been applied, and stops npm peer-dependency override flags.
// The decision is returned as hook JSON (see scripts/lib/hook-output.js); a hook
// failure is reported visibly instead of silently skipping enforcement.

const common = require('../scripts/lib/common.js');
const out = require('../scripts/lib/hook-output.js');
const { analyzeCommand } = require('../scripts/lib/dependency-commands.js');

try {
  const input = common.readStdinJson();
  const tool = input.tool_name || '';
  if (['Bash', 'PowerShell'].includes(tool)) {
    const result = analyzeCommand(input.tool_input && input.tool_input.command);
    if (result.block) out.denyToolUse(result.message);
  }
  out.allow();
} catch (e) {
  out.fail('pre-tool-use', e, 'dependency routing was not applied');
}
