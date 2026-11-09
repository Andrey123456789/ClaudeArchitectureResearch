# External Mechanics Notes — Claude Code hooks

Verified against the current official Claude Code hooks reference before this refactor.

These host mechanics are inputs to the K0 refinement and should not be rediscovered through a live-session relocation experiment.

1. Command hooks support **exec form** when `args` is present: `command` is resolved as the executable and each argument is passed directly rather than being shell-tokenized.
2. Path placeholders such as `${CLAUDE_PROJECT_DIR}` can be passed as exec-form arguments.
3. `${CLAUDE_PROJECT_DIR}` remains the project/configuration root where the session started; it is not a reliable synonym for the active linked-worktree root.
4. Hook input field `cwd` follows Claude's active working directory and is the correct starting point for active checkout/worktree discovery.
5. `PreToolUse` fires before a tool call and can deny it.
6. `PostToolUse` fires after a successful tool call.
7. `PostToolUseFailure` fires after a failed tool call. A failed shell command may already have produced filesystem side effects, so relevant actual-state validation belongs on this path too.
8. Most command-hook failures/timeouts are not inherently policy-blocking; current Claude Code supports explicit `onFailure: "block"` for policy hooks that must fail closed.
9. The matcher `Bash|PowerShell` covers both shell tool families.
10. A hook configuration loaded for the current session should not be "tested" by moving that already-running session into another sandbox and assuming different `.claude/settings.json` will dynamically become the active hook configuration.

## Refinement implication

Keep two concepts separate:

- **launcher/config root** — where the hook executable/script is located;
- **active repository/worktree root** — what the hook inspects and enforces.

Use stable configuration paths to launch the hook. Resolve active repository state from hook input `cwd` and bounded Git discovery.

For shell-driven repository mutations, command text is sufficient only for pre-routing. After success or failure, inspect the actual resulting active-worktree state using the bounded per-worktree model specified in `REFINEMENT_TASK.md`.
