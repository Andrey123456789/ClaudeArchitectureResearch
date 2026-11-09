# L0 Run-02 defect dossier — pre-run hardened for 5.3

All items below are mandatory refinement targets unless the refinement audit proves the stated observation is factually wrong. Do not weaken the requirement to make the checker pass.

The dossier includes the original L0 findings plus cross-cutting enforcement gaps discovered before L0 refinement began, so they can be fixed in the **first** controlled-refinement pass rather than through repeated corrective iterations.

## D1 — Critical — Hook launcher breaks after a nested `cd`

Current settings use commands such as:

`node .claude/hooks/claude-hook.mjs pre-bash`

The exact configured command succeeds only while cwd is the repository/worktree root. From a nested project directory it fails before the hook script starts (`MODULE_NOT_FOUND`). Claude Code hook input explicitly tracks cwd changes, so root-only operation is not sufficient.

**Required result:** every configured hook entry point launches reliably from repository root, nested directories, and worktrees on Windows Claude Desktop. Prefer current Claude Code exec-form (`command` + `args`) with a stable launcher path.

## D2 — High — Launcher root and active repository/worktree root are not modeled separately

The current hook computes project root from the script location. That happens to work when the relative launcher resolves to the active worktree copy, but it cannot robustly solve both nested cwd and worktree semantics.

Current Claude Code behavior distinguishes:

- `${CLAUDE_PROJECT_DIR}`: original project/session root, stable even when Claude enters a worktree;
- hook input `cwd`: follows Claude after `cd` and when working in a worktree.

**Required result:** distinguish the stable launcher/config root from the **active repository/worktree root**. Read hook JSON first, resolve the active root from `input.cwd` (for example with bounded `git -C <cwd> rev-parse --show-toplevel` when Git semantics are needed), and run manifest/status/co-change checks against that active root. Do not accidentally inspect or mutate the main checkout when Claude is operating in a worktree.

## D3 — High — Critical PreToolUse failure can fail open

The settings do not specify `onFailure: "block"`. The hook uses exit 1 when enforcement cannot run. Under current Claude Code hook semantics, most hook failures/timeouts allow the action to continue unless failure behavior is explicitly blocking.

**Required result:** critical dependency/project-reference PreToolUse enforcement must fail closed when its launcher/script is missing, crashes, cannot parse required input, produces invalid required output, or times out. Configure and test the appropriate `onFailure` behavior. PostToolUse/PostToolUseFailure/Stop behavior must not be made blocking merely for symmetry when the underlying action already occurred; failures there must remain visible and must not be falsely reported as successful enforcement.

## D4 — High — Project-reference mutation is not reliably routed before/after execution

Behavioral test:

`dotnet add Foo.Api.csproj reference Foo.Domain.csproj`

Current Run-02 results:

- `pre-bash`: exit 0, no routing/block;
- `post-bash`: exit 0, no message when static manifest checks find no violation.

Changing the project reference graph is a Reserved decision in the shared task. A structurally legal reference is still a graph change that requires the decision/workflow path.

**Required result:** detect all supported add/remove project-reference forms before mutation, route them to the authoritative project-structure/architecture-decision process, and prevent silent Reserved graph changes. Post-mutation validation remains useful but is not a substitute for the pre-decision gate.

## D5 — High — npm-family global options bypass mutation/force classification

Verified misses include:

- `npm --prefix frontend install x --force`
- `pnpm --dir frontend add x --force`
- `yarn --cwd frontend add x --force`

All currently pass pre and post classification silently. The parser treats the option value (`frontend`) as the subcommand.

**Required result:** parse npm/pnpm/yarn command shape robustly enough to skip recognized global options and their values before identifying the subcommand. Cover `.cmd`/`.exe` forms and force/legacy-peer flags before or after the subcommand. Preserve the distinction between restore-only installs and dependency mutations.

## D6 — High — The structure checker rejects the safer hook configuration

`check-instructions.mjs` currently requires a single shell-form string matching:

`node <script>.mjs <event>`

A controlled test replacing those entries with current exec-form (`command: "node"`, `args: [...]`) made the checker fail all four hook entries.

**Required result:** update the checker to validate intended behavior, not obsolete serialization. It must validate executable, path placeholder/launcher target, event args, script existence, Windows-safe exec form, critical `onFailure` semantics, and every required event registration added by this refinement.

## D7 — Medium — Manual checker instructions are cwd-relative and documentation overclaims cwd robustness

The map advertises `node .claude/...` commands and describes the hook command as working across shells, but root-relative commands are not reliable after `cd` into a nested directory.

**Required result:** make manual validation procedures explicitly root-stable. Either ensure the workflow first resolves/enters the active repository/worktree root or provide an equally cross-platform runner. Update map/workflow claims so they match tested behavior.

## D8 — Medium — Stop reminder fingerprint ignores subsequent content changes

The Stop hook hashes only the modified file/status set plus reminder strings. Behavioral test:

1. modify production file A without tests -> reminder emitted;
2. edit file A again, keeping the same Git status and same file set -> Stop exits 0 because the fingerprint is unchanged.

The second edit may materially change whether the reminder has been addressed.

**Required result:** include a bounded digest of relevant working-tree content/diff state in the fingerprint (or another deterministic equivalent) so materially changed content can trigger a fresh reminder, while unchanged-state suppression and `stop_hook_active` still prevent loops.

## D9 — High — Successful shell mutations are validated from command text, not actual resulting state

Current `post-bash` returns immediately unless `dependencyChange(tokens)` recognizes the command. Therefore a successful Bash/PowerShell command can modify `.csproj`, `Directory.Packages.props`, `package.json`, or project references through another mechanism and bypass deterministic post-change validation.

Representative bypass classes include a script/program that edits a manifest, a PowerShell file rewrite, or a Git operation that changes checked-out manifest contents without looking like a dependency command.

**Required result:** after successful Bash/PowerShell calls, compare a bounded per-worktree manifest/project state and validate what actually changed. Keep command-text parsing for pre-routing and explanatory context, but do not rely on it as the sole post-change detector. Avoid an expensive full-repository validation after every unrelated shell call once safe state has been established.

## D10 — High — Failed shell calls with partial side effects have no post-failure validation path

Current settings have `PostToolUse` but no `PostToolUseFailure` handler. A Bash/PowerShell call can modify a manifest/project file and then fail; the successful `PostToolUse` path does not represent that tool outcome.

**Required result:** register and handle `PostToolUseFailure` for Bash|PowerShell. Inspect the actual active-worktree state after the failure and apply the same relevant deterministic validation. A failed command that changed no relevant state should stay quiet. Do not try to "block" an already failed/completed tool call; return visible/contextual findings using the event's supported semantics.

## D11 — High — Fresh-state HEAD transitions, deletions, and moves are not covered by a persistent actual-state model

Current Run-02 has no per-worktree manifest snapshot/HEAD state. This leaves multiple related gaps:

- first shell event in a fresh state changes HEAD to a revision containing an invalid manifest, leaving a clean worktree;
- later HEAD transitions change committed manifests;
- tracked manifest/project file deletion can disappear from file-by-file validation;
- rename/move may appear as delete + add and must not vanish silently;
- same-file shell rewrite should be detected even if the Git path set is unchanged.

**Required result:** maintain bounded state per active worktree sufficient to detect the documented actual-state changes. A safe design may perform one full manifest validation/snapshot on first shell observation, then compare content/HEAD state on later observations and validate only relevant changes. Deletions/moves must be reported/routed deterministically. Deliberately skipped directories/repositories must not later be falsely reported as removed tracked manifests.

## D12 — Medium/High — Windows encoding robustness is incomplete for generated/edited manifest content

Hook JSON already strips one UTF-8 BOM, which must be preserved. However manifest readers use `readFileSync(..., 'utf8')` directly. Windows PowerShell 5.1 workflows can produce BOM-tagged UTF-16 files; blindly decoding them as UTF-8 can create false findings or parsing failures unrelated to policy.

**Required result:** keep normal UTF-8 and UTF-8-BOM hook input working, and make relevant manifest/project text readers robust for the Windows encodings the workflow can produce, including BOM-tagged UTF-16LE/UTF-16BE where applicable. Malformed or odd-length encoded files must fail visibly/deterministically rather than crashing unpredictably.

## Required non-regression guards

The refinement must preserve the properties Run-02 currently gets right:

- exactly four L0 levels and the same stability dependency direction;
- no capability/contracts/slots/Kind taxonomy;
- zero trigger-role deltas and no reduced minimum scope;
- no concrete technology names in Levels 0/1 beyond the candidate's fixed-platform interpretation;
- the two stratified always-loaded decision summaries remain separate;
- 196 policy owners remain complete and semantically faithful;
- no broken internal references;
- no research metadata or non-English runtime content;
- `SPECIFICATION.md` remains an input, not an instruction layer.

The corrected structure checker must also prove its own central predicates with a small bounded set of negative fixtures: disallowed Level 0/1 technology, reverse level dependency, broken reference, missing fail-closed PreToolUse configuration, and missing required `PostToolUseFailure` registration.

## Quality-improvement targets (not permission for churn)

These are secondary. Apply only when demonstrably better and regression-free:

1. Try to reduce the ~5.0k always-loaded estimate toward Run-01's ~4.4k by removing redundant trigger descriptions or prose, **without** moving policies between trigger classes, weakening routing, or losing decision content.
2. Re-review the frozen V2 baseline for useful technique/examples lost through consolidation. Restore only material content, not text merely to increase lexical similarity.
3. Keep Run-02's relatively compact 71-file structure unless a new file has a concrete ownership/trigger/enforcement justification.

Do not turn these quality reviews into repeated optimization cycles after mandatory correctness has converged.
