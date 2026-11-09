# External mechanics notes used by the independent audit

Source checked: official Claude Code Hooks Reference on 2026-10-20.

These are host/runtime mechanics, not L1 policy.

1. **Exec form.** A command hook runs in exec form when `args` is present. `command` is resolved as an executable and each argument is passed without shell tokenization. Path placeholders are substituted as argument data. For Node hooks that reference project files, `command: "node"` plus a script-path element in `args` is the preferred cross-platform shape.

2. **Project root vs active cwd/worktree.** `${CLAUDE_PROJECT_DIR}` remains the project root where the session started. Hook input `cwd` follows Claude after `cd` and points at the active worktree after Claude enters one. A hook may use the stable project root to locate its launcher, but checks of repository state must resolve from input `cwd`; launcher root is not automatically the active worktree root.

3. **Failure semantics.** On most events, a failed or timed-out hook does not automatically block the triggering action. `onFailure: "block"` is supported for critical policy hooks such as `PreToolUse`. It covers launch failure, crash/non-accepted exit, and timeout. Do not apply fail-closed semantics indiscriminately to Stop or post events where the action has already happened or where loops/noise would result.

4. **Pre vs post events.** `PreToolUse` fires before a tool call and can deny it. `PostToolUse` fires after a tool call succeeds. `PostToolUseFailure` fires after a tool call fails. A failed Bash/PowerShell call may still have partial filesystem side effects, so post-failure actual-state validation is required when repository-policy enforcement depends on resulting files.

5. **PowerShell/Bash matcher.** `Bash|PowerShell` is a supported matcher for covering both shell tools.

6. **Current-session live-hook limitation is not a refinement gate.** Moving an already-running Claude Desktop/Code session into a copied template/sandbox does not prove that the copied project's hook configuration has been reloaded. This refinement therefore uses controlled process-level tests of the generated settings/scripts plus documented host semantics. Do not repeatedly relocate the current session or require a live hook-engine demonstration as a promotion condition.

7. **Verification boundary.** The acceptance criterion is the documented behavior of the generated template, not mutation-testing the verification harness itself. A small bounded set of negative fixtures is sufficient to prove central structural predicates. Once the required matrix and one clean cumulative confirmation audit pass, stop.

8. **Windows encoding.** Hook input must tolerate the documented JSON stream plus the practical UTF-8-BOM case encountered through Windows tooling. Manifest/project text readers used by enforcement should deterministically handle the encodings the supported Windows workflow can create, including BOM-tagged UTF-16 where applicable, rather than silently mis-decoding or crashing.
