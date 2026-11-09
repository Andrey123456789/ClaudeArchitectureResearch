# PV2-01-GIT-GATING: declaration

Written before the first edit of this change. Authority: kit 74 Part B PV2-01 and decision D-PV2-01 (approved; no further approval needed). Applied after PV2-02, because M and M1 Git gating runs in the same scripts and relies on their input validation.

**Change.** M, M1, L0, L1 and K1 ask the user to confirm repository-changing Git commands before they run, in each candidate's own PreToolUse hook and output form, with the classification K0 already uses:

| Candidate | Hook | Where Git is classified | Ask output |
|---|---|---|---|
| M | `.claude/hooks/dependency-guard.mjs` | new quote-aware `gitCommands` (M's own dependency parser stays minimal) | `askTool` in `hook-io.mjs` (JSON, exit 0) |
| M1 | `.claude/hooks/pre-tool-use.js` | `gitOperations` in `scripts/lib/dependency-commands.js`, on its existing lexer | `askToolUse` in `scripts/lib/hook-output.js` |
| L0 | `.claude/hooks/claude-hook.mjs` (`pre-bash`) | `classifySegment`, on its existing tokenizer and wrapper recursion | `ask` (JSON, exit 0) |
| L1 | `.claude/hooks/pre-shell-command.mjs` | `analyze`, on its existing segments and tokens | its `decide('ask', ...)` |
| K1 | `.claude/hooks/dispatch.cjs` + `scripts/classify-command.cjs` | `visit`, finding kind `git-change` | JSON ask on stdout, exit 0 |

The read-only/repository-changing table is K0's (`hook.cjs` lines 185-234), placed as one identical block in the five (`git_block.js`). No dispatcher, file or architecture identity is transplanted: each candidate keeps its hook files, parsers, outputs and messages.

**Semantics (common).**

- Read-only Git (`status`, `diff`, `log`, `show`, `blame`, `rev-parse`, listing forms of `branch`, `tag`, `stash`, `remote`, `config --get`, ...) runs without a Git prompt.
- Every other subcommand, unrecognized ones included, asks: `commit`, `add`, `push` (force too), `reset`, `checkout <ref>`, `switch`, `clean`, `branch -D`, `tag v1`, `stash`, `rebase`, `merge`, `pull`, `fetch`, `rm`, `mv`, `restore`, `config <key> <value>`, ...
- Global options (`-C <path>`, `-c <k=v>`, `--git-dir`, `--work-tree`, `--no-pager`) are skipped first; wrappers (`bash -c`, `sh -c`, `cmd /c`, `pwsh -Command`, `powershell -Command`), environment prefixes (`VAR=x`, `env`), the PowerShell call operator and quoted executable paths are handled by each candidate's tokenizer; every segment of a multi-command line is classified.
- A deny or block from an existing non-Git guard (peer bypass, unapproved dependency or project-reference change) still wins: Git never turns a deny into an ask.
- The ask reason names the authority rule. The ask is not authorization: `CLAUDE.md` § Git (HQ-01, GOV-015) still requires an explicit request or a named pre-approval; the dirty-tree task-start check, the headless pause, scoped commits and an explicitly authorized `main` rewrite are unchanged.
- No commit step is added anywhere.

**Files.** Hooks and helpers listed above; each candidate's `git-workflow` skill gets K0's "Enforced by" sentence with the not-authorization clause; each candidate's map row for the hook names the Git ask.

**Claims and policies.** `GOV-015` (repository-changing Git only when explicitly requested), linked HQ-01 reading. One added claim per changed candidate, classified as K0's record of the same hook behavior.

**Expected behavior.** A common fixture matrix (read-only, mutating, global options, wrappers, combined lines, quoted paths, deny-wins, malformed input) gives the same decision in all six hooks by direct execution. How a live host shows `ask`, and what a user answers, is NOT_RUN.

**Remaining differences, reported.** K0 classifies the first recognized tool anywhere in a segment, so `echo git commit` asks in K0 and is allowed elsewhere (an over-approximation in K0, not changed). Git run by scripts or other programs is classified by no candidate.

**Regression adaptation.** v2 `final_audit_v2.py` recorded "only K0 has a Git hook" as a finding; v3's audit replaces that row. No v1 or v2 suite asserted that the other five lack a Git hook (R02 tests K0's hook only).
