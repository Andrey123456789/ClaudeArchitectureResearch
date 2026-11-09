# External Mechanics Notes — Claude Code hooks

Source checked during the independent audit:

- https://code.claude.com/docs/en/hooks

Relevant current behavior:

1. With `args` present, command hooks use **exec form**: `command` is the executable and `args` is passed directly without shell tokenization.
2. Path placeholders such as `${CLAUDE_PROJECT_DIR}` are substituted as plain argument strings in exec form.
3. `${CLAUDE_PROJECT_DIR}` remains the project root where the session started.
4. Hook-input `cwd` follows Claude after `cd` and when Claude enters a worktree.
5. On most events, hook failure/timeout is non-blocking by default.
6. Current Claude Code supports `onFailure: "block"` for policy-critical command hooks.
7. `PostToolUse` matching Edit/Write does not fire merely because a Bash command rewrote the same file; Bash/PowerShell need their own relevant coverage (or another supported file-change mechanism).

Refinement implication:

- use the original project root only to locate stable hook code when needed;
- use hook-input `cwd` to identify the active repository/worktree being inspected;
- prefer exec-form launching for path-bearing cross-platform command hooks;
- make critical PreToolUse policy enforcement fail closed.
