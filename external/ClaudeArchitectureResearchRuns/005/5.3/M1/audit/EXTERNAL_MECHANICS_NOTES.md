# External mechanics notes — Claude Code hooks

These notes are external runtime-mechanics evidence used only to make the generated template work correctly with current Claude Code. They do not alter the frozen policy oracle or M1 architecture.

Verified against the current Claude Code Hooks reference on 2026-10-18:
https://code.claude.com/docs/en/hooks

## Script launch vs active repository/worktree root

- `${CLAUDE_PROJECT_DIR}` is the project root where the session started.
- When Claude enters a worktree, `${CLAUDE_PROJECT_DIR}` **stays at the original project root**.
- Hook input JSON field `cwd` follows Claude and becomes the worktree/current directory.
- Therefore it is valid to use `${CLAUDE_PROJECT_DIR}` to locate the hook script itself, but repository checks must derive the active checkout/worktree from hook input `cwd`, not from the script's own location.

## Exec form

Current Claude Code supports command hooks with:

```json
{
  "type": "command",
  "command": "node",
  "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/pre-tool-use.js"]
}
```

When `args` is present, Claude Code uses exec form: no shell tokenization, each argument is passed directly, and path placeholders are substituted as plain strings. The documentation recommends exec form whenever a hook references a path placeholder. The `node` + script-path pattern is explicitly described as cross-platform.

## Failure behavior

On most events, a hook that crashes or times out is non-blocking by default. For policy enforcement that must fail closed, current Claude Code supports:

```json
"onFailure": "block"
```

For this template, apply fail-closed behavior deliberately to critical **PreToolUse** enforcement. Do not blindly put it on Stop, where the documented semantics differ and `onFailure` has no effect.

## `cwd`

Hook input has a documented common `cwd` field: current working directory when the hook is invoked. Use it as the starting point for resolving the active Git worktree/repository root, while still enforcing that paths stay within the allowed project/worktree boundary.
