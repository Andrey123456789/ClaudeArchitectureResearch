# External mechanics notes used by the independent audit

Source checked: official Claude Code Hooks Reference on 2026-10-19.

These are host/runtime mechanics, not candidate policy.

1. **Exec form.** A command hook runs in exec form when `args` is present. `command` is resolved as an executable and each `args` element is passed without shell tokenization. Path placeholders are substituted as plain strings. For Node hooks that reference a project path, `command: "node"` plus a script-path element in `args` is the preferred cross-platform shape.

2. **Project root vs active cwd/worktree.** `${CLAUDE_PROJECT_DIR}` remains the project root where the session started. Hook input `cwd` follows Claude after `cd` and points at the active worktree after Claude enters one. A hook may use the stable project root to locate its launcher, but checks of repository state must resolve from the input `cwd` rather than assuming launcher root == active worktree.

3. **Failure semantics.** On most events, a failed/timed-out hook does not automatically block the triggering action. `onFailure: "block"` is supported for policy hooks such as critical `PreToolUse` command hooks. It covers launch failure, crash/non-accepted exit, invalid required output, and timeout. Do not apply fail-closed semantics indiscriminately to Stop or post events where the action has already happened or continuation loops could result.

4. **Pre vs post events.** `PreToolUse` fires before a tool call and can deny it. `PostToolUse` fires after a tool call succeeds. `PostToolUseFailure` fires after a tool call fails and receives the same `tool_name` / `tool_input` plus error information. A failed shell call may still have partial filesystem side effects, so post-failure validation is relevant for actual-state enforcement.

5. **PowerShell/Bash matcher.** `Bash|PowerShell` is a supported matcher for covering both shell tools.

6. **Current-session live-hook limitation is not a refinement gate.** Moving an already-running Claude Desktop/Code session into a copied template/sandbox does not prove that the copied project's hook configuration has been reloaded for that session. This refinement therefore uses controlled process-level tests of the generated settings/scripts plus documented host semantics. Do not repeatedly relocate the current session or require a live hook-engine demonstration as a promotion condition.

7. **Verification boundary.** The task's acceptance criterion is the documented behavior of the generated template, not mutation-testing the verification harness itself. A small bounded set of negative checker fixtures is sufficient to show central structural predicates are enforced. Do not launch recursive audit-of-audit or mutation-analysis loops after the required matrix and confirmation audit pass.
