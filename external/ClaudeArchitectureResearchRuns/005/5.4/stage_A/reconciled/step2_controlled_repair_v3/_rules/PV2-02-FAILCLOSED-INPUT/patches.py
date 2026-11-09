"""PV2-02 patches: M and M1 shell PreToolUse guards block invalid hook input in the script. See DECLARATION.md."""
REASON = 'PV2-02 (approved): script-level fail-closed handling of malformed, empty, non-object and commandless shell PreToolUse input in M and M1.'
POLICIES = ['DEP-025']
EVIDENCE = 'Direct runs before the change: M exits 1 on malformed/empty input and allows array, string, no-tool_input, no-command, blank and non-string commands; M1 allows no-tool_input, no-command, blank and non-string commands and a missing or wrong event.'

M_IO = '.claude/hooks/hook-io.mjs'
M_GUARD = '.claude/hooks/dependency-guard.mjs'
M_TM = '.claude/skills/template-maintenance/SKILL.md'
M_MAP = '.claude/MAP.md'
M1_PRE = '.claude/hooks/pre-tool-use.js'

PATCHES = [
    ('M', M_IO,
     """//   1  hook could not run (environment problem) - reported to the user; work is
//      not blocked, except for the PreToolUse guard, which settings.json
//      registers with "onFailure": "block" (fail closed)
//   2  PreToolUse block - stderr is shown to Claude and the tool call is cancelled
""",
     """//   1  hook could not run (environment problem) - reported to the user; work is
//      not blocked, except for the PreToolUse guard, which settings.json
//      registers with "onFailure": "block" (fail closed)
//   2  PreToolUse block - stderr is shown to Claude and the tool call is cancelled.
//      The dependency guard also uses it for hook input it cannot read or
//      classify (readInput with blockTool as the handler), so invalid shell input
//      is blocked by the script itself, not only by onFailure.
"""),
    ('M', M_IO,
     """// Reads the hook event JSON from stdin.
export function readInput() {
  let raw;
  try {
    raw = readFileSync(0, 'utf8');
  } catch (error) {
    fail(`cannot read hook input from stdin: ${error.message}`);
  }
  raw = raw.replace(/^﻿+/, ''); // Windows PowerShell may prepend one or more UTF-8 byte-order marks
  if (!raw.trim()) {
    fail('hook input on stdin is empty; this script expects Claude Code hook JSON.');
  }
  try {
    return JSON.parse(raw);
  } catch (error) {
    fail(`hook input is not valid JSON: ${error.message}`);
  }
}
""",
     """// Reads the hook event JSON from stdin. `onInvalid` handles input that cannot
// be read or parsed: advisory hooks report it (fail, exit 1); the dependency
// guard passes a handler that blocks (exit 2).
export function readInput(onInvalid = fail) {
  let raw;
  try {
    raw = readFileSync(0, 'utf8');
  } catch (error) {
    onInvalid(`cannot read hook input from stdin: ${error.message}`);
  }
  raw = raw.replace(/^﻿+/, ''); // Windows PowerShell may prepend one or more UTF-8 byte-order marks
  if (!raw.trim()) {
    onInvalid('hook input on stdin is empty; this script expects Claude Code hook JSON.');
  }
  try {
    return JSON.parse(raw);
  } catch (error) {
    onInvalid(`hook input is not valid JSON: ${error.message}`);
  }
}
"""),
    ('M', M_GUARD,
     """// Registered in .claude/settings.json in exec form:
//   "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/dependency-guard.mjs"]
// Manual test (from the repository root; "cwd" defaults to the current directory):
//   echo '{"hook_event_name":"PreToolUse","tool_input":{"command":"npm --prefix frontend i x --force"}}' | node .claude/hooks/dependency-guard.mjs
""",
     """// Registered in .claude/settings.json in exec form:
//   "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/dependency-guard.mjs"]
// Invalid input fails closed in the script (exit 2): unreadable, empty or
// non-JSON input, JSON that is not an object, an event this script does not
// handle, and - for a PreToolUse shell call - a missing tool_name, tool_input or
// non-empty tool_input.command string. A PreToolUse call for another tool has
// nothing to gate and is allowed. onFailure "block" stays the backstop for a
// crash or timeout.
// Manual test (from the repository root; "cwd" defaults to the current directory):
//   echo '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"npm --prefix frontend i x --force"}}' | node .claude/hooks/dependency-guard.mjs
"""),
    ('M', M_GUARD,
     """const input = readInput();
const event = input.hook_event_name;
const command = input.tool_input?.command;
if (typeof command !== 'string' || command.trim() === '') done();
""",
     """const input = readInput(invalidInput);
if (input === null || typeof input !== 'object' || Array.isArray(input)) invalidInput('hook input is not a JSON object');
const event = input.hook_event_name;
if (!['PreToolUse', 'PostToolUse', 'PostToolUseFailure'].includes(event)) {
  invalidInput(`hook input has no hook_event_name this script handles (got ${JSON.stringify(event)})`);
}
if (event === 'PreToolUse') {
  if (typeof input.tool_name !== 'string') invalidInput('PreToolUse hook input has no tool_name string');
  if (!['Bash', 'PowerShell'].includes(input.tool_name)) done(); // not a shell call: nothing for this guard to gate
  const toolInput = input.tool_input;
  if (toolInput === null || typeof toolInput !== 'object' || Array.isArray(toolInput)) invalidInput('PreToolUse hook input has no tool_input object');
  if (typeof toolInput.command !== 'string' || toolInput.command.trim() === '') invalidInput('PreToolUse hook input has no non-empty tool_input.command string');
}
const command = input.tool_input?.command;
if (typeof command !== 'string' || command.trim() === '') done(); // PostToolUse / PostToolUseFailure: nothing to check
"""),
    ('M', M_GUARD,
     """function unquote(token) {""",
     """// Invalid hook input: the guard cannot classify the call, so it blocks (exit 2).
function invalidInput(reason) {
  blockTool(`Blocked: ${reason}. The dependency guard cannot classify this shell call, so it fails closed; report the hook input problem to the user.`);
}

function unquote(token) {"""),
    ('M', M_TM,
     """  PreToolUse guard also sets `"onFailure": "block"`, so a guard that cannot run
  blocks the tool call; advisory post-tool and Stop hooks do not.""",
     """  PreToolUse guard also sets `"onFailure": "block"`, so a guard that cannot run
  blocks the tool call, and the guard itself blocks (exit 2) shell hook input it
  cannot read or classify, including a call with no command; advisory post-tool
  and Stop hooks do not block."""),
    ('M', M_MAP,
     """the PreToolUse guard fails closed (`"onFailure": "block"`, so Node.js must be available), advisory hooks fail open""",
     """the PreToolUse guard fails closed (`"onFailure": "block"`, so Node.js must be available, and the guard itself blocks hook input it cannot read or classify), advisory hooks fail open"""),
    ('M1', M1_PRE,
     """// This is critical enforcement and fails closed: an internal error or malformed hook
// input (a leading byte-order mark is not malformed) denies the command, a failure to
// load the helpers exits with the blocking code 2, and settings.json declares
// onFailure "block" for any other crash or timeout.
""",
     """// This is critical enforcement and fails closed: an internal error or malformed hook
// input (a leading byte-order mark is not malformed) denies the command, a failure to
// load the helpers exits with the blocking code 2, and settings.json declares
// onFailure "block" for any other crash or timeout. Malformed means: not a JSON
// object, an event other than PreToolUse, no tool_name, and - for Bash or
// PowerShell - no tool_input object with a non-empty command string. Another tool
// has nothing to gate and is allowed.
"""),
    ('M1', M1_PRE,
     """  const input = readStdinJson();
  if (typeof input.tool_name !== 'string') throw new Error('hook input has no tool_name');
  const tool = input.tool_name;
  if (['Bash', 'PowerShell'].includes(tool)) {
    const result = analyzeCommand(input.tool_input && input.tool_input.command, tool);
    if (result.block) out.denyToolUse(result.message);
  }
""",
     """  const input = readStdinJson();
  if (input.hook_event_name !== 'PreToolUse') throw new Error(`hook input is not a PreToolUse event (got ${JSON.stringify(input.hook_event_name)})`);
  if (typeof input.tool_name !== 'string') throw new Error('hook input has no tool_name');
  const tool = input.tool_name;
  if (['Bash', 'PowerShell'].includes(tool)) {
    const toolInput = input.tool_input;
    if (!toolInput || typeof toolInput !== 'object' || Array.isArray(toolInput)) throw new Error('shell hook input has no tool_input object');
    if (typeof toolInput.command !== 'string' || toolInput.command.trim() === '') throw new Error('shell hook input has no non-empty tool_input.command string');
    const result = analyzeCommand(toolInput.command, tool);
    if (result.block) out.denyToolUse(result.message);
  }
"""),
]
