# Refinement Report — Candidate M

| Item | Result |
| --- | --- |
| Selected baseline | **M/Run-02** (`baseline/template/`, read only; still 60 files / 340,417 bytes as recorded in `PROVENANCE.json`) |
| Final status | **STRICTLY_BETTER**, cumulative, after the [Final corrective pass](#final-corrective-pass), [Corrective pass — iteration 3](#corrective-pass--iteration-3), and [Corrective pass — iteration 4](#corrective-pass--iteration-4) |
| Corrective pass — iteration 4 | Failed Bash/PowerShell calls (`PostToolUseFailure`) now get the same manifest and project-reference validation. The checker enforces the required hook registrations. The cumulative suite passes 134/134. |
| Corrective pass — iteration 3 | 2 residual shell-mutation cases fixed (first HEAD transition in a fresh state; tracked-manifest removal). The cumulative suite passes 102/102. |
| Final corrective pass | 3 later-found defect classes fixed (fail-closed PreToolUse, shell-driven manifest mutations, content-aware Stop deduplication). The cumulative suite passes 89/89. |
| Confirmed defects D1–D6 | 6/6 fixed, each reproduced on the baseline and shown fixed on the output |
| Additional defects found during the audit and fixed | 3 (double-BOM stdin from PowerShell 5.1; npm bypass through shell wrappers; npm bypass through line continuations) |
| Regression matrix | 56/56 PASS (12 dossier cases, edge cases, baseline evidence, and two parser tables with 76 commands) |
| Policy owner / trigger / scope deltas | 0 / 0 / 0 (196/196 owners carried over unchanged) |
| Broken internal references | 0 |
| Always-loaded context | ~4,766 tokens before and ~4,766 after (byte-identical) |
| Runtime file count | 60 before, 61 after (+`.claude/scripts/repo-root.mjs`) |
| Optional Run-01 ideas | 0 adopted, 1 rejected, 2 deferred |
| Confirmation audit | round 1: 1 cleanup item repaired; round 2 (complete rerun): **0 concrete template defects** |

## Changed Files and Reasons

Thirteen files were modified and one was added. Every other runtime file is byte-identical to the baseline.

| File | Reason |
| --- | --- |
| `.claude/settings.json` | **D1.** All four hooks now use exec form: `"command": "node"` with `"args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/<script>.mjs"]`. No shell is involved and no command string depends on the current directory. |
| `.claude/scripts/repo-root.mjs` (new) | **D2/D6.** One resolver for the hooks and the checkers. It keeps two roots apart: the *template root*, found from the script's own location and used only to find the installed scripts, and the *active root*. The active root is computed from a start directory: (1) the same repository's Git working tree, confirmed by a shared common Git dir so linked worktrees count, plus the template's offset inside its tree; (2) otherwise, the template root when the start directory is inside it (no Git, or a submodule); (3) otherwise a clear error. It never treats `CLAUDE_PROJECT_DIR` as repository state. |
| `.claude/hooks/hook-io.mjs` | **D2.** The `CLAUDE_PROJECT_DIR`-based `projectRoot()` was replaced by `startDirectory(input)` (the input `cwd`) and `activeRoot(input)`, which fails visibly with "Repository checks were NOT run". `repoRelative` now canonicalizes paths. **Audit fix:** leading BOMs are stripped with `/^﻿+/`, because the Windows PowerShell 5.1 UTF-8 pipe sends two BOMs. |
| `.claude/hooks/dependency-guard.mjs` | **D4:** a table-driven npm parser. It skips global options and their values (`NPM_VALUE_OPTIONS`), and a token that is not a known npm command is treated as an option value, so it cannot hide the real subcommand. It also detects `npm_config_force`/`npm_config_legacy_peer_deps`, `npm config set force`, `npm set`, and `=false`. **D3:** detects `dotnet add/remove <proj> reference`, `dotnet reference add/remove`, and the package forms. Project-reference changes are classified separately from packages and routed to `architecture.md` § Project References and CLAUDE.md § Decision Control, not to `add-dependency`. **D2:** the manifest check runs on the active root. **Audit fixes:** joins `\`/`` ` `` line continuations and unwraps `cmd /c`, `bash -c`/`-lc`, and `powershell`/`pwsh -Command`. |
| `.claude/hooks/file-change.mjs` | **D2.** The active root for an edit is the checkout or worktree that contains the edited file (a relative `file_path` resolves against `cwd`). Edits in a worktree are no longer skipped silently. |
| `.claude/hooks/stop-co-change.mjs` | **D2.** Git state (status and the per-worktree state dir) is read from the active root derived from `cwd`, not from the main checkout. |
| `.claude/scripts/check-manifests.mjs` | **D2/D6.** The CLI root comes from the current directory through `repo-root.mjs`. `<file>` arguments resolve against the current directory, `isMain` compares canonical paths, and the usage header states the root precondition. |
| `.claude/scripts/check-instructions.mjs` | **D5.** Requires exec form: `type: command`, `command: node`, exactly one argument matching `${CLAUDE_PROJECT_DIR}/.claude/hooks/<name>.mjs`, and a script that exists under the root being checked. It rejects shell strings, `$VAR`/`%VAR%`, relative arguments, other executables, paths outside the hooks directory, and extra arguments. **D6:** its root comes from the current directory. |
| `.claude/skills/verify/SKILL.md`, `add-dependency/SKILL.md`, `project-structure/SKILL.md`, `project-structure/references/backend-layout.md` | **D6.** Each checker or root-relative CLI step now says to run it from the repository root, i.e. the top level of the current checkout or worktree (`git rev-parse --show-toplevel`). Only the invocation lines changed. |
| `.claude/skills/template-maintenance/SKILL.md` | **D1/D2/D5/D6.** The old "shell-neutral `node <script>`" invariant described the defective launcher and now describes exec form and root derivation. Step 4 adds the root precondition. |
| `.claude/MAP.md` | Accuracy for D1/D2/D3/D5/D6: the settings, hook-io, dependency-guard, and check-instructions rows, the architecture enforcement cell, and step 6's root precondition. The new `repo-root.mjs` row is required by the checker's "MAP lists every script" predicate. |

## D1–D6 Repair Evidence

Each defect was reproduced on the baseline in the same sandbox before being shown fixed on the output.

| Defect | Baseline (reproduced) | Refined |
| --- | --- | --- |
| D1 CWD-dependent launch | T02-baseline: from `backend/Shop.Api`, `node .claude/hooks/...` fails with `Cannot find module` (exit 1) in both cmd.exe and Git Bash. | T01/T02/T02b/T03: exec form works from the root and from nested backend and frontend directories, with no shell. |
| D2 launcher root vs worktree | T05-baseline, T11-baseline: inspects the main checkout. It misses worktree Git changes, skips worktree manifests silently, and misses worktree violations. | T05–T05e, T11–T11c, E04–E06: linked worktrees, nested `.claude/worktrees/<n>`, subdirectory installs, and no-Git copies resolve correctly. A cwd outside every checkout fails visibly (E02/E03). |
| D3 project-reference bypass | T06-baseline: `dotnet add … reference …` is ignored. | T06/T07 + P02: add/remove in both CLI syntaxes are detected and the Domain→Infrastructure violation blocks. Packages and references are never confused (32 cases). |
| D4 npm global options | T09/10-baseline: `--prefix … --force` and `--workspace … --legacy-peer-deps` pass. P01-baseline: 23 of 33 must-block commands pass. | T09/T10 + P01: all 44 PreToolUse cases are correct, including 35 must-block cases and no false blocks on 9 benign ones. |
| D5 checker vs exec form | T12-baseline: the correct exec-form settings fail. | T12a accepts exec form. T12 (12 variants) rejects every unsafe shell or ambiguous form. |
| D6 manual root-relative calls | T13-baseline: the nested relative call fails, and the absolute call checks `CLAUDE_PROJECT_DIR` (main) and misses the worktree violation. | T13a–e: the checkers resolve the active worktree from any nested directory. The documented `git rev-parse --show-toplevel` procedure works in Bash and in PowerShell 5.1. |

## Regression Test Matrix

The sandbox was built under `output/.work/sbx`: Git main checkouts plus linked worktrees for both the refined and the baseline template. Git discovery was capped with `GIT_CEILING_DIRECTORIES`. Hooks were launched exactly as configured: exec form (placeholder substituted, `spawn` without a shell) for the refined template, and the shell command string for the baseline.

| # | Dossier case | Tests | Result |
| --- | --- | --- | --- |
| 1 | Launch from repository root | T01 | PASS |
| 2 | Launch from nested cwd | T02, T02b | PASS |
| 3 | Windows-safe exec form | T03 (Windows, no shell, path with spaces) | PASS |
| 4 | PowerShell 5.1 BOM stdin | T04a (one BOM), T04b (real PS 5.1 pipe), T04c (two BOMs) | PASS |
| 5 | Active root from `cwd`, not the launcher | T05, T05b–e | PASS |
| 6 | `dotnet add … reference` detected | T06, P02 | PASS |
| 7 | Reference removal detected | T07, P02 | PASS |
| 8 | Normal `npm install` detected | T08, T08b | PASS |
| 9 | `npm --prefix … install … --force` blocked | T09, P01 | PASS |
| 10 | `npm --workspace … install … --legacy-peer-deps` blocked | T10, P01 | PASS |
| 11 | Manifest and reference checks on the active worktree | T11, T11b, T11c | PASS |
| 12 | Checker accepts exec form and rejects unsafe forms | T12a + 12 rejection variants | PASS |

Extra coverage, all PASS:
- D6 manual invocation: T13a–e.
- Root edge cases: E01–E06.
- Stop-loop protection and once-per-change-set reminders: T05c, T05d.
- Baseline evidence rows (`*-baseline`), confirming each defect exists in the baseline.
- The documented manual-test commands in each hook header, run in Bash and PowerShell.
- Existing checkers on `output/template`: `check-instructions` reports 48 instruction files, 0 failures, 0 warnings. `check-manifests` reports 0 violations, from the root and, using the absolute script path, from a nested directory.

**Residual limitations (not tested, outside the minimal parser):**
- An unlisted npm value option whose value equals an npm command name.
- `npx npm …`.
- PowerShell `-EncodedCommand`.

These are documented in the hook header. No tested dependency or project-reference case bypasses enforcement.

## Policy Owner / Trigger / Scope Audit

- Every policy owner file is byte-identical to the baseline (23 of 23): CLAUDE.md, the imported stack, both product inputs, all 11 rules, the agent, and the 7 unchanged workflow skills.
- The six changed Markdown files have zero frontmatter changes (descriptions, `paths`, `disable-model-invocation`) and zero `> Owns:` header changes.
- The baseline lines no longer present verbatim are all checker-invocation lines, maintenance-invariant lines, or MAP rows. None carries an inventory policy or a shared invariant.
- The baseline's 196/196 mapping (194 inventory policies plus GOV-017/018) therefore carries over unchanged: 0 owner changes, 0 trigger-role deltas, 0 minimum-scope gaps (rule `paths` are untouched).
- M identity is unchanged:
  - flat `.claude/rules/` and no `Level:`/`Kind:` lines (checker);
  - no capability or decision-register layer;
  - workflow and knowledge separation intact;
  - private references used only by their owner.
- No V2 content was removed.
- The new invocation text is procedure placed next to each command, as D6 requires. It is not a policy restatement.
- Hook messages point to their owners instead of restating policy.

## Hygiene, Dependencies, Context

- **Broken references:** 0 (file, `§` section, skill/agent, import, and private-reference checks). Every JS import resolves.
- **Module graph:** acyclic, with `repo-root.mjs` as the leaf (hooks → hook-io / check-manifests → repo-root).
- **Language and metadata:** English only; no Cyrillic in 61 files. 0 research-metadata hits.
- **`CLAUDE_PROJECT_DIR`:** appears only as the launcher placeholder and in comments. No code reads it as a root.
- **Always-loaded context:** about 4,766 tokens before and after (CLAUDE.md + `docs/technology-stack.md` + skill/agent listings, all byte-identical). This is within the ~5k target.
- **Runtime files:** 60 → 61. The added module exists because a single deterministic root resolver is shared by the hooks and the checkers (D2/D6). No layer or metadata was added.

## Windows / Worktree Hook Result

On Windows 11 with Node 24 and Git 2.55 in a path containing spaces, all hooks run in exec form from any cwd. stdin is accepted from Windows PowerShell 5.1, including its double-BOM UTF-8 pipe. The active root resolves correctly for:
- main checkouts;
- nested subdirectories;
- linked worktrees, both sibling and nested under `.claude/worktrees/`;
- subdirectory installs and their worktrees;
- non-Git copies.

When no root can be established, the hooks fail visibly. Known Windows or worktree hook defects: **0**. The baseline has 5 in this matrix: D1, D2, D6, the double BOM, and wrapper/continuation parsing on Windows shells.

## Optional Run-01 Ideas

| Idea | Decision | Rationale |
| --- | --- | --- |
| Source-level architecture checker | **DEFER** | Only Run-01's report is available, so false-positive rates cannot be assessed. Regex heuristics over C# `using`/namespaces are brittle. The highest-value boundary, the project-reference graph, is now enforced mechanically after both edits and CLI changes. Adding it would add a file without proven net benefit. |
| Destructive-Git confirmation hook | **REJECT** | It duplicates Claude Code's permission prompts. GOV-015 is already always loaded. A hook cannot tell whether the user explicitly asked for the operation, so it would prompt on requested operations (noise), and it would add another command-parser surface. |
| Auto instruction-structure check after edits | **DEFER** | Multi-file edits pass through valid intermediate states (for example, a new file before its MAP row) that would raise transient failures and blocks. `template-maintenance` already mandates the checker, and there is no evidence of a net benefit. |

## Rejected or Reverted Proposed Changes

- **Git top level as the only active root:** rejected. It would regress subdirectory installs, which the baseline supported. The same-repository offset mapping covers that case (E06).
- **A one-line root-anchored command (`node "$(git rev-parse --show-toplevel)/…"`):** rejected. It breaks for subdirectory installs and non-Git copies and is less readable. Kept the explicit precondition plus cwd-derived resolution.
- **Quote-aware tokenizer rewrite:** rejected. Not required, and it would drift toward a general shell parser. The fallback scan handles quoted paths (P01).
- **PreToolUse pre-blocking of project references:** rejected. The PostToolUse check and block already cover it with less parsing.
- **MSYS-path conversion of `cwd`:** rejected as speculative. Claude Code supplies native paths, and a failure would be visible.
- **Rewording `architecture.md` / `dependencies.md` enforcement sentences:** omitted. They are still true, and changing them would churn path-loaded rules.
- **Confirmation round 1:** an unused `baseDir` parameter and a cosmetic comment rewording in `hook-io.repoRelative` were reverted to baseline form.

## Confirmation Audit

Round 1 rechecked every gate and every changed item. It found one non-functional cleanup item, the unused parameter and cosmetic rewording above. That item was repaired.

Round 2 was a complete rerun after the repair:
- harness 56/56;
- both checkers clean, from the root and from nested directories;
- module syntax checks clean;
- change scope limited to 13 modified and 1 added file;
- policy-owner invariance 23/23;
- frontmatter and headers unchanged;
- language and metadata scans clean;
- budget equal;
- documented manual commands correct in Bash and PowerShell.

Round 2 found **0 concrete template defects**, so convergence is established.

**Promotion gate:**
1. D1–D6 fixed.
2. 5.2 acceptance gates still pass.
3. No policy, scope, or trigger regressions.
4. 0 broken references.
5. M identity unchanged.
6. Windows and worktree behavior demonstrably stronger.
7. No tested bypass.
8. No new semantic duplication.
9. V2 content retained.
10. Context equal.
11. +1 file, with a reliability purpose.
12. Every change documented above.

All twelve hold, so the result is **STRICTLY_BETTER**.

## Workspace Events

- **Isolation violations:** 0. No parent, sibling, 5.2, network, or external sources were used, and `baseline/` and `source/` were only read.
- **Recoverable incident, remediated:** while reading inputs, a concatenation of baseline skill text was briefly written to the session scratchpad and deleted immediately. Later scratch work stayed under `output/.work/`, which has been removed.
- **Platform-managed:** the tool runtime persisted some large command outputs to its own session store, and those outputs were read back. They contained only the requested workspace files.

---

## Final corrective pass

### Why this pass exists

After the M refinement above was finished, cross-candidate audits found three more defect classes that also apply to M. This pass continues from the refined `output/template/`; it was not rebuilt from `baseline/`. It repairs only those three classes. For before/after evidence, a snapshot of the pre-pass template was kept under `output/.work/` (removed afterwards). Acceptance is cumulative: every earlier property must still pass.

### Disposition of the three defect classes

| # | Defect class | Disposition |
| --- | --- | --- |
| 1 | The policy-critical PreToolUse guard failed open: a missing, crashing, or timed-out guard, or one given malformed input, let the tool call through. | **Fixed.** The PreToolUse `dependency-guard` entry sets `"onFailure": "block"`. Advisory PostToolUse and Stop hooks stay fail-open, because their event has already happened and a blocking Stop failure could loop. `check-instructions.mjs` now requires `onFailure: "block"` on PreToolUse hooks and rejects it on PostToolUse and Stop hooks. |
| 2 | Shell-driven manifest or project-file changes (sed, `Set-Content`, scripts, `git checkout`, new files) bypassed `check-manifests`. | **Fixed.** After any shell command that is not a known dependency or reference command, PostToolUse validates only the manifests whose content changed since the last manifest check. In a Git working tree, the candidates are the manifests Git reports as changed, plus those changed between the recorded and current HEAD. Without Git there is no narrower signal, so every manifest is a candidate. Content state is stored per worktree in its Git directory. The file-change hook records the manifests it validates, so they are not reported twice. Unchanged manifests are never re-validated, and no full repository validation runs after unrelated commands. |
| 3 | Stop deduplication fingerprinted only reminder IDs and paths, so changing the same file again was suppressed. | **Fixed.** The fingerprint now also covers the content of the relevant changed files (model, seeder, migration, production, and test paths). This is bounded: at most 200 files, each hashed with SHA-256, or by size and mtime above 1 MB. `stop_hook_active` handling is unchanged. |

### Files changed in this pass

All 10 files are under `output/template/`. No file was added or removed.

| File | Change | Defect |
| --- | --- | --- |
| `.claude/settings.json` | `"onFailure": "block"` on the PreToolUse guard only. | 1 |
| `.claude/scripts/check-instructions.mjs` | Fail-closed rule: required on PreToolUse, rejected on PostToolUse and Stop. Header line updated. | 1 |
| `.claude/hooks/hook-io.mjs` | `contentId` (bounded content identity). `manifestChanges` and `rememberManifests` (per-worktree manifest state). `activeRoot` became `activeRepository`. Exit-code comment notes the fail-closed guard. | 2, 3 |
| `.claude/hooks/dependency-guard.mjs` | PostToolUse validates manifests changed by any other shell command. Known-command behavior is unchanged, except that it also records state. | 2 |
| `.claude/hooks/file-change.mjs` | Records the state of manifests it validated, and uses the repository object. | 2 |
| `.claude/hooks/stop-co-change.mjs` | The fingerprint includes the relevant file content. | 3 |
| `.claude/scripts/repo-root.mjs` | `resolveActiveRepository` returns `{ root, top, gitDir }` from the same `rev-parse` call, with a same-tree shortcut. Results are identical to before (the root cases T05/T11/T13/E01–E07 still pass). This keeps the new per-command check at 2 Git spawns instead of 4. | 2 (cost) |
| `.claude/scripts/check-manifests.mjs` | `discover` is exported, for the no-Git candidate set. | 2 |
| `.claude/skills/template-maintenance/SKILL.md` | One sentence on the fail-closed guard, so maintainers keep it. | 1 |
| `.claude/MAP.md` | Settings, hook-io, dependency-guard, and stop-co-change rows updated. | 1, 2, 3 |

### Behavioral evidence

A fresh in-workspace harness ran against the final template, the pre-pass snapshot, and the immutable baseline. Git discovery was capped. Hooks were launched exactly as configured. The fail-closed cases use a launcher model of Claude Code's command-hook semantics:
- exit 2 blocks and exit 0 allows;
- a hook that cannot start, exits with any other code, or times out counts as a failure;
- a failure blocks only when the entry sets `onFailure: "block"`.

Result: **89/89 PASS**, of which 27 cases are new.

- **Fail closed (F00–F04)**
  - The settings set the failure mode correctly, and the normal guard still blocks bypasses and allows benign commands.
  - All six failure modes now block, and each failed open in the pre-pass template:
    - malformed JSON;
    - empty input;
    - `node` not on `PATH`;
    - guard script missing;
    - guard crashing on import;
    - guard hanging past the timeout (a 3 s test timeout stands in for the configured 30 s).
  - Advisory PostToolUse and Stop failures stay non-blocking.
  - T12 adds four checker rejections: PreToolUse without `onFailure`, a non-`block` value, and `block` on PostToolUse or Stop.
- **Shell-driven mutations (S01–S13, E03b, E07)**
  - Detected and blocked; each of the first two passed silently in the pre-pass template:
    - Bash `sed -i` adding a Domain→Infrastructure reference in a linked worktree from a nested cwd;
    - a PowerShell 5.1 `Set-Content` floating npm version from a nested frontend cwd.
  - Also detected:
    - a newly created project file;
    - the same manifest changed again;
    - a `git checkout` that brings in a committed violating manifest;
    - a change in a non-Git copy;
    - a change in a subdirectory-install worktree.
  - A valid shell change gets context routing, not a block.
  - Commands that should stay silent do:
    - an unrelated command;
    - the next command with the same state;
    - after an Edit-validated manifest (MultiEdit violations still block);
    - after a known reference command;
    - from a cwd outside every checkout.
  - A committed, unchanged violation is not re-reported, which shows that no full validation runs.
  - Measured cost after an unrelated command: ~340–390 ms, including Node start, versus ~110 ms before. The extra cost is one `rev-parse` and one `status`.
- **Stop (C01)**
  - The final template follows the required sequence:
    1. First applicable Stop: remind.
    2. Unchanged repeat: silent.
    3. Same file changed again: remind.
    4. Unchanged repeat: silent.
    5. `stop_hook_active=true`, even after a change: silent twice.
    6. New changed path: remind.
    7. Non-relevant content edit: silent.
  - The pre-pass template stayed silent at step 3, which reproduces the defect.

### Cumulative acceptance

- **D1–D6:** every original repair still passes, rerun in the same harness against both the baseline and the final template. These are T01–T13 with all baseline-evidence rows, E01–E07, and the P01 (44 commands) and P02 (32 commands) parser tables.
- **Earlier refinement properties:** all still pass.
  - Windows exec form: no shell, path with spaces.
  - PowerShell 5.1 BOM, including the double BOM (T04a–c).
  - Nested cwd (T02/T02b).
  - Real worktrees: linked, nested `.claude/worktrees/`, and subdirectory installs.
  - npm force and global-option blocking.
  - Project-reference routing.
  - The D6 manual-checker procedure in Bash and PowerShell.
  - The documented manual hook-test commands in Bash and PowerShell.
- **Owner / trigger / minimum-scope regressions:** 0 / 0 / 0.
  - All 23 policy-owner files are still byte-identical to the baseline: CLAUDE.md, the stack, the product inputs, all 11 rules, the agent, and 7 workflow skills.
  - The 194 policies plus GOV-017/GOV-018 are unchanged.
  - No frontmatter or `> Owns:` header changed.
- **Broken references:** 0. `check-instructions` reports 48 files, 0 failures, 0 warnings. Imports resolve and the module graph is acyclic.
- **M identity:** unchanged. Rules stay flat, there are no Level/Kind lines, and no capability, contract, or meta layer was added.
- **Hygiene:** English only, 0 research-metadata hits.

| Measure | Before this pass | After |
| --- | --- | --- |
| Always-loaded estimate | ~4,766 tokens | ~4,766 tokens (CLAUDE.md, stack, and skill/agent listings unchanged) |
| Runtime file count | 61 | 61 |

### Confirmation audit

The confirmation audit covered:
- a line-by-line review of the final changed code;
- the change scope against the pre-pass snapshot (exactly the 10 files above);
- both checkers;
- policy-owner and frontmatter invariance;
- module graph, language, and metadata scans;
- the absence of hook state outside the workspace (OS temp `claude-hooks` absent);
- the documented manual commands;
- a complete harness rerun on the final template: **89/89**.

It found **0 concrete template defects**. The only addition during the audit was a new evidence case (S05b, a new untracked project file), which is a harness-only change. The template did not change after the last complete run.

Workspace events in this pass: 0 isolation violations. All scratch material, sandboxes, and non-Git hook state stayed under `output/.work/`, which has been removed.

### Final status

Every earlier property still passes, and all three new defect classes are fixed with no regressions. **Final status: STRICTLY_BETTER** (cumulative).

---

## Corrective pass — iteration 3

### Why iteration 3 was required

After iteration 2, independent verification found that shell-driven manifest tracking still had two reproducible gaps:

- **A.** In a fresh tracking state, the first shell event could switch `HEAD` to a revision containing an invalid manifest. Because no earlier `HEAD` was recorded and the tree stayed clean, nothing was validated.
- **B.** When a tracked manifest was deleted, it was recorded as `missing` and then filtered out, so the removal passed silently.

This pass continues from the iteration-2 `output/template/` and closes only those two cases. A snapshot of the iteration-2 template was kept under `output/.work/` for before/after evidence and removed afterwards.

### Disposition

| Defect | Disposition |
| --- | --- |
| **A.** First HEAD transition in a fresh state | **Fixed.** The first check in a worktree takes a one-time snapshot: it validates every manifest, recording state with a `baseline` flag. The same snapshot runs again if the recorded `HEAD` can no longer be diffed (for example, after the object was pruned). Later commands keep the narrow candidate set (Git status plus HEAD diff), so unrelated commands are not full scans. A state file written by iteration 2 has no `baseline` flag, so it takes one snapshot after upgrade. |
| **B.** Removal of tracked manifests | **Fixed.** Deletions are now reported once, as "Manifests removed: …", instead of being filtered out. In a Git tree they come from status `D` entries, the source side of a rename, and HEAD diffs. Without Git, they are manifests recorded earlier that can no longer be found. A removal triggers a repository-wide `check-manifests` run, because removing `Directory.Packages.props` or a project can break what remains, and any resulting violation blocks. Otherwise the removal is routed visibly as context to the existing owners: add-dependency, `architecture.md` (Project References), and CLAUDE.md § Decision Control for a changed project graph or dependency set. A rename becomes a removal plus a new, validated manifest, consistent with the existing delete-plus-add model. |

### Files changed in iteration 3

Three files changed, all under `output/template/`. No file was added or removed.

| File | Change |
| --- | --- |
| `.claude/hooks/hook-io.mjs` | `manifestChanges` adds the initial and fallback snapshot, removal detection (Git `D` entries, rename sources, files vanished without Git), and returns `removed` and `snapshot`. The state now records `baseline`, which `rememberManifests` preserves. |
| `.claude/hooks/dependency-guard.mjs` | The unrelated-command path reports removals, runs a repository-wide check after a removal, and gives the initial or fallback snapshot its own message header. A valid snapshot stays silent. Header comment updated. |
| `.claude/MAP.md` | The dependency-guard row mentions the initial snapshot and removed-manifest reporting. |

### Behavioral evidence

A fresh in-workspace harness was run against the final template, the iteration-2 snapshot, and the immutable baseline. Result: **102/102 PASS**, of which 16 cases are new. Each "before" row reproduces the defect on the iteration-2 template.

**A — fresh-state HEAD transitions**

| Case | Result |
| --- | --- |
| A01 | The first shell event in a fresh worktree (`git checkout bad`, nested cwd) is blocked. Validation runs against the worktree, not the launcher checkout. Before: silent. |
| A02 | The snapshot is taken only once; the next command is silent. |
| A03 | A benign first event is silent, and the state records `baseline: true` and HEAD. |
| A04 | A later clean HEAD transition is validated and routed without a block. |
| A05 | A later transition to an invalid revision is blocked, in the main checkout. |
| A06 | When the recorded HEAD cannot be diffed, the fallback snapshot blocks the invalid revision. |

**B — removals**

| Case | Result |
| --- | --- |
| B01 | `.csproj` removed with Bash `rm` from a nested worktree cwd: visible and routed. Before: silent. |
| B03 | `package.json` removed with Bash `rm`: visible and routed. Before: silent. |
| B02 | `Directory.Packages.props` removed with PowerShell 5.1 `Remove-Item`: visible, and the resulting breakage ("package references exist but no Directory.Packages.props was found") is blocked. Before: silent. |
| B04 | Each removal is reported once; the next command is silent. |
| B05 | `git mv`: the old path is reported removed and the new path is validated. |
| B06 | Without Git, a removed `package.json` is reported once. |

**Intentionally changed expectation (S07).** In iteration 2, S07 asserted that a fresh state did *not* report a committed, unchanged violation; that was exactly the defect-A gap. It now asserts the following:
- the initial snapshot reports the committed violation once;
- later unrelated commands are silent.

That second point is the original intent: no full validation after every unrelated command.

**Cost.** The per-command cost after an unrelated command is the same as in iteration 2: measured side by side on the same tracked state, 444–455 ms versus 452–518 ms. The snapshot runs once per worktree.

### Cumulative acceptance

- **Original D1–D6 repairs:** all pass. That covers T01–T13 with the baseline-evidence rows, E01–E07, P01 (44 commands), and P02 (32 commands).
- **Iteration-2 repairs:** all pass.
  - The fail-closed PreToolUse guard (F00–F04). Its "before" proof is now a counterfactual: the same entry without `onFailure` fails open, because the iteration-2 snapshot already contains the fix.
  - Shell-driven mutation coverage (S01–S13).
  - Edit/Write/MultiEdit validation (S08/S09, T11).
  - Stop same-path material-state deduplication and `stop_hook_active` loop prevention (C01, T05c/d).
- **Windows / BOM / nested-cwd / worktree:** all pass.
  - Exec form with no shell, on a path with spaces.
  - PowerShell 5.1 single and double BOM (T04a–c).
  - Nested cwd (T02, S02, A01, B01).
  - Linked, nested, and subdirectory-install worktrees (T05, T11, E04–E07, A01).
  - The documented manual hook commands.
- **Owner / trigger / minimum-scope regressions:** 0 / 0 / 0.
  - All 23 policy-owner files are still byte-identical to the baseline.
  - The 194 policies plus GOV-017/GOV-018 are unchanged.
  - There are 0 frontmatter or header changes.
- **Broken references:** 0. `check-instructions` reports 48 files, 0 failures, 0 warnings; imports resolve and the module graph is acyclic.
- **M identity:** unchanged. No new layer, mechanism, or metadata was added.
- **Hygiene:** English only; 0 research-metadata hits; no hook state outside the workspace.

| Measure | Before iteration 3 | After |
| --- | --- | --- |
| Always-loaded estimate | ~4,766 tokens | ~4,766 tokens |
| Runtime file count | 61 | 61 |

### Confirmation audit

The confirmation audit covered:
- a review of the final changed code;
- change scope against the iteration-2 snapshot (exactly the 3 files above);
- both checkers and module syntax checks;
- policy-owner, frontmatter, and header invariance;
- the module graph, language, and metadata scans;
- the temp-state check;
- the documented manual commands;
- the latency comparison;
- a complete harness rerun on the final template: **102/102**.

During the pass, one accuracy issue was found and repaired before the complete confirmation run. When the snapshot fallback ran, unchanged manifests were labelled "changed since the last manifest check". The fallback now has its own "Manifest snapshot" header and stays silent when nothing violates.

The complete confirmation found **0 concrete template defects**.

Workspace events in this pass: 0 isolation violations. All scratch material, sandboxes, and non-Git hook state stayed under `output/.work/`, which has been removed.

### Resulting cumulative status

The previous refinement, iteration 2, and iteration 3 all pass with no regressions. **Final status: STRICTLY_BETTER** (cumulative).

---

## Corrective pass — iteration 4

### Why iteration 4 was required

After iteration 3, independent verification found one remaining enforcement gap. A Bash or PowerShell call can change a `.csproj`, `Directory.Packages.props`, or `package.json` file, or the project-reference graph, and then fail. Claude Code reports that call through `PostToolUseFailure`, not `PostToolUse`.

In iteration 3, `settings.json` registered the dependency guard only for PreToolUse and PostToolUse. The guard also rejected any other event ("unexpected hook event", exit 1). So the failed call itself was never validated. The change surfaced only if a later shell call happened to succeed, and never if the session went on with file edits only or ended (row U01-before).

This pass continues from the iteration-3 `output/template/` and closes only that gap. A snapshot of the iteration-3 template was kept under `output/.work/` for before/after evidence and removed afterwards.

### How `PostToolUseFailure` is handled

- **Registration.** A `PostToolUseFailure` entry with matcher `Bash|PowerShell` runs the same `dependency-guard.mjs`, in exec form, with timeout 60. It has no `onFailure`: the hook is advisory, because the tool call has already failed and a fail-closed advisory hook could loop.
- **Judged by the resulting state.** A failed command may have changed some, all, or none of what it targeted. It is therefore judged by the repository state it left behind, never by its command line. The existing manifest-change state (`manifestChanges` in `hook-io.mjs`) decides what to validate:
  - Git status and HEAD-diff candidates, compared by content identity;
  - the one-time initial snapshot;
  - removals, including both sides of a rename.

  Changed manifests go through the existing `check-manifests` validation, and a removal triggers the repository-wide check. When nothing changed since the last manifest check, the hook reports nothing.
- **Known dependency or reference commands.** When the failed command is a known dependency or project-reference command (`dotnet add … reference`, `npm install <pkg>`, and so on) and it did change manifests, it keeps the success path's full check and the same owner routing. That routing is add-dependency, or `architecture.md` (Project References) plus CLAUDE.md § Decision Control. In a fresh state with no record yet, such a command is routed as it would be on success, not silenced.
- **Output.** `postToolContext` and `postToolBlock` in `hook-io.mjs` now take the event name; the default is `PostToolUse`, so existing callers are unchanged. On `PostToolUseFailure` both emit `hookSpecificOutput` with `hookEventName: "PostToolUseFailure"` and `additionalContext`, which is the output a failure hook provides. A failed call can no longer be blocked, so a violation reaches Claude as context alongside the error, phrased as a required fix. The output has no `decision` field. PostToolUse output is byte-identical to iteration 3 (U00).
- **Roots.** Unchanged. The active root comes from the hook input `cwd` through `resolveActiveRepository`; `${CLAUDE_PROJECT_DIR}` only locates the script. When the cwd is outside every checkout, an unrelated failed command is silent. A failed dependency command reports "Repository checks were NOT run", as it does on success.
- **No parallel architecture.** The failure path uses the same script, state file, candidate model, checker, and owner strings. The owner strings are now computed once and shared by both paths.

### Files changed in iteration 4

Six files changed, all under `output/template/`. No file was added or removed.

| File | Change |
| --- | --- |
| `.claude/settings.json` | Adds the `PostToolUseFailure` registration: `Bash\|PowerShell` → `dependency-guard.mjs`, exec form, timeout 60, no `onFailure`. |
| `.claude/hooks/hook-io.mjs` | `postToolContext` and `postToolBlock` accept the event name. On `PostToolUseFailure`, the block reason is given as `additionalContext`. |
| `.claude/hooks/dependency-guard.mjs` | Handles `PostToolUseFailure` through the manifest-change path. Failed known commands keep the full check and owner routing. The owner strings are computed once. The header comment and the unexpected-event message now cover the third event. |
| `.claude/scripts/check-instructions.mjs` | Adds `REQUIRED_HOOKS`: the five registrations the enforcement depends on must exist, each with the event, a matcher covering the listed tools, and the exec-form script path. Those are PreToolUse/PostToolUse/PostToolUseFailure for Bash and PowerShell → dependency guard, PostToolUse for Edit, Write, and MultiEdit → file-change, and Stop → co-change. It also requires that a registered script which reads `hook_event_name` compares against every event it is registered for. The existing exec-form and `onFailure` rules are unchanged and now also apply to the new entry. |
| `.claude/MAP.md` | The settings, dependency-guard, and check-instructions rows. |
| `.claude/skills/template-maintenance/SKILL.md` | The hook invariant names the dependency guard's three events. This is a user-invoked skill, and its frontmatter and description are unchanged, so always-loaded context is unchanged. |

### Behavioral evidence

The harness was rebuilt in `output/.work/`: it was recovered from the final iteration-3 harness and then extended. It was run against the final template, the iteration-3 snapshot, and the immutable baseline. Result: **134/134 PASS**.

Every failing command really runs in Git Bash or Windows PowerShell 5.1 and exits non-zero after changing files. The hook then receives a `PostToolUseFailure` payload with `cwd`, `tool_name`, `tool_input.command`, `tool_use_id`, `error`, and `is_interrupt`. Every sandbox path contains a space ("AI Learning").

**Successful shell mutations (unchanged)**

| Case | Result |
| --- | --- |
| U00 | Six PostToolUse scenarios produce output byte-identical to the iteration-3 template, after path normalization: Bash `sed` invalid reference, PowerShell `Set-Content` floating central version, Bash `rm` of a `.csproj`, `dotnet add reference`, `npm install <pkg>`, and an unrelated command. |
| U00a / S02 | A successful Bash mutation that makes a tracked `.csproj` invalid is blocked (`decision: block`); S02 runs it from a nested worktree cwd. |
| U00b / S04 | A successful PowerShell mutation that makes `Directory.Packages.props` (U00b) or `package.json` (S04) invalid is blocked. |

**Failed shell mutations (new)**

Every row returns exit 0, `hookEventName: "PostToolUseFailure"`, and no `decision` field. The text starts "The shell command failed; the manifests were checked in the state it left behind".

| Case | Shell, location | Result |
| --- | --- | --- |
| U01 | Bash, `sed … && exit 1`; linked worktree, nested cwd | The Domain → Infrastructure reference violation is reported against the worktree. **Before (U01-before):** iteration 3 has no `PostToolUseFailure` registration, and its guard rejects the event (exit 1). The violation surfaces only when a later shell call succeeds. |
| U02 | Bash `ls` failing; same worktree | The next failed unrelated command is silent: reported once, no repeat. |
| U03 | PowerShell `Set-Content`, then `throw`; repository root | The `Directory.Packages.props` floating version `4.*` violation is reported against the main checkout. |
| U04 | Bash, file truncated, then `exit 1`; nested directory in the worktree | The half-written `package.json` is reported as invalid JSON. |
| U05 | PowerShell, then `exit 3`; worktree directory with spaces (`tools/Admin Portal`) | The `package.json` floating version `latest` is reported. |
| U06 | Bash `rm … && exit 1`; repository root | The removed `.csproj` is reported and routed to CLAUDE.md § Decision Control. |
| U07 | PowerShell `Remove-Item`, then `throw`; worktree, nested cwd | The `Directory.Packages.props` removal and the resulting violation are both reported. |
| U08 | Bash; failed `dotnet add … reference … && dotnet build` that changed the graph (allowed edge); worktree | The changed `.csproj` is reported and routed once to Project References and Decision Control. |
| U08b | Bash; failed `npm install …` that changed `package.json` (valid, pinned version) | Reported and routed to the add-dependency workflow. |
| U09 | Bash; failed `dotnet add … reference` that left a forbidden Application → Infrastructure edge; repository root | The violation is reported with reference routing. |
| U14 | Interrupted call (`is_interrupt: true`, exit 130) | The invalid manifest it left is reported. |
| U15 | Fresh tracking state; the first event is a failed command that left an invalid manifest | The initial check reports it once; the next call is silent. |
| U15b | Fresh tracking state; failed reference command on a valid tree | Routed, as on success, not silent. |
| U16 | No Git | The invalid manifest is reported. |

**No-noise cases**

| Case | Result |
| --- | --- |
| U10 | Failed `dotnet add reference` and failed `npm install` that changed no manifest: silent. |
| U11 | A failed Bash command that changed only `docs/notes.md`, and a failed PowerShell `Get-Item`: silent. |
| U12 | An unrelated failed command does no repository walk and reads no manifest. The counts were 0 directory reads, 0 manifest reads, and 5 `git` spawns in a linked worktree, identical to a successful unrelated command. A fresh-state control (16 directory reads, 17 manifest reads) shows the probe sees a scan when one happens. |
| U17 | When the cwd is outside every checkout, a failed unrelated command is silent, and a failed dependency command reports that checks were NOT run (as on success). |

**Input, Windows, and hook-engine semantics**

| Case | Result |
| --- | --- |
| U13a | A UTF-8 BOM before the `PostToolUseFailure` input: the violation is reported. |
| U13b | Windows PowerShell 5.1 pipe with UTF-8 `$OutputEncoding` (double BOM): the violation is reported. |
| U01, U03, U05, U07, U11 | Bash and PowerShell `tool_name` both run through the same path. |
| F00, F04, U18 | The failure hook has no `onFailure`. A crashing failure hook stays non-blocking, so there is no fail-closed loop. Its reports carry no `decision`. |

**Checker evidence (mechanical enforcement)**

- T12a: the current settings are accepted.
- Ten new mutation rows each make `check-instructions` exit 1 with a `FAIL settings.json <event>` line:
  - the `PostToolUseFailure` registration removed;
  - the matcher reduced to `Bash`;
  - the entry pointing to a missing script;
  - the entry in shell form;
  - the entry set to `onFailure: block`;
  - the PreToolUse guard registration removed;
  - the PostToolUse shell guard removed;
  - the file-change registration removed;
  - the Stop registration removed;
  - a registered guard that does not handle `PostToolUseFailure` (the iteration-3 guard placed under the current settings).
- T12-before: the iteration-3 checker accepts the iteration-3 settings without `PostToolUseFailure`; the current checker rejects them.

**Not repeated.** The live-session hook-engine experiment was not repeated, as instructed. As in iterations 2 and 3, the hook engine is simulated: exec-form spawn, a stdin payload, and the `onFailure` outcome. The payload and response shapes follow Claude Code's documented `PostToolUseFailure` contract.

**Harness bookkeeping.** The four iteration-3 "before" rows (A01-before and B01–B03-before) compared against the iteration-2 snapshot, which is no longer kept. Their evidence stands in the iteration-3 section, and their "after" rows still run. The total is 102 − 4 + 11 checker rows + 25 failed-shell rows = 134.

**Cost.** An unrelated command was timed side by side, interleaved, 24 calls each in the main checkout and a linked worktree. The medians were:

| Call | Median |
| --- | --- |
| PostToolUse, iteration 4 | 1197 ms |
| PostToolUse, iteration 3 | 1224 ms |
| PostToolUseFailure, iteration 4 | 1180 ms |
| Node.js start alone | 182 ms |

The absolute numbers are higher than in iteration 3 because `git` process start was slower on this machine during this pass; the comparison was made in the same session.

### Cumulative acceptance

- **Original D1–D6 repairs:** all pass: T01–T13 with the baseline-evidence rows, E01–E07, P01 (44 commands), and P02 (32 commands).
- **Iteration-2 repairs:** all pass.
  - The fail-closed PreToolUse guard (F00–F04). F00 and F04 now also assert that the failure hook is fail-open.
  - Shell-driven mutation coverage (S01–S13).
  - Edit/Write/MultiEdit validation (S08, S09, T11).
  - Stop first reminder, unchanged suppression, same-path material-state re-reminder, and `stop_hook_active` loop prevention (C01, T05b–d).
- **Iteration-3 repairs:** all pass: fresh-state first HEAD transition and later transitions (A01–A06), and removals (B01–B06).
- **npm force and global-option handling, and project-reference add/remove:** pass (T06–T10, P01, P02, S12).
- **Windows / BOM / nested-cwd / worktree:** all pass.
  - PowerShell 5.1 single and double BOM (T04a–c, U13a/b).
  - Nested cwd (T02, S02, A01, B01, U01, U04, U07, U08).
  - Linked, nested, and subdirectory-install worktrees (T05, T11, E04–E07, A01, U01, U04, U05, U07, U08).
  - Paths with spaces (all sandboxes, and U05 inside the repository).
- **Owner / trigger / minimum-scope regressions:** 0 / 0 / 0.
  - All 23 policy-owner files are still byte-identical to the baseline.
  - The 194 policies plus GOV-017/GOV-018 are unchanged.
  - There are 0 frontmatter or header changes.
- **Broken references:** 0. `check-instructions` reports 48 files, 0 failures, 0 warnings; imports resolve and the module graph is acyclic.
- **M identity:** unchanged. One registration was added to the existing hook, with no new file, layer, or mechanism, no Levels, Kinds, or capability layer, and no meta-architecture.
- **Hygiene:** English only; 0 research-metadata hits.

| Measure | Before iteration 4 | After |
| --- | --- | --- |
| Always-loaded estimate | ~4,766 tokens | ~4,766 tokens (CLAUDE.md, the imported stack, and all skill/agent frontmatter byte-identical) |
| Runtime file count | 61 | 61 |
| Hook registrations | 4 | 5 (`PostToolUseFailure`, Bash and PowerShell) |
| Runtime bytes | 368,472 | 372,168 |

### Confirmation audit

The first confirmation round covered:
- a review of the final diff against the iteration-3 snapshot (exactly the 6 files above);
- both checkers and module syntax checks;
- policy-owner, frontmatter, and header invariance;
- the module graph, language, and metadata scans;
- the temp-state check;
- the documented manual commands;
- the latency comparison;
- the complete harness.

Findings, all repaired:
- **During the affected-test runs, before the audit:** a failed known reference command that changed a manifest named the Project References owner twice, once from the generic text and once from the command-specific text. A failed known command now uses its command owners, exactly as on success, and U08 asserts a single mention.
- **In round 1:** the new dependency-guard header comment was imprecise. It said a failed command is checked "like after any other command" and that one "that changed no manifest reports nothing". It now states the full check and routing for known commands, and "since the last manifest check". U15b was added for the documented fresh-state branch.

Round 2, a complete rerun after the fix, gave 134/134, clean checkers, and unchanged invariants: **0 concrete template defects**.

Workspace events in this pass: one recoverable incident. A manual smoke test of the failure event was run directly in `output/template/`, which has no Git, so the hook wrote its non-Git state file to the OS temp directory (`claude-hooks/claude-manifest-state-c3291ea2d527.json`). The file was removed immediately, along with the directory, which had not existed before; later checks show it absent. All other scratch material, sandboxes, and hook state stayed under `output/.work/`, which has been removed.

### Resulting cumulative status

The previous refinement and iterations 2, 3, and 4 all pass, with no regressions and the `PostToolUseFailure` gap closed. **Final status: STRICTLY_BETTER** (cumulative).

---

## Post-audit corrective pass — iteration_after_audit_1

`iteration_after_audit_1` is the first correction after the independent re-audit. It is counted separately from the four corrective passes above and does not replace them. It continues from the accepted iteration-4 `output/template/`; nothing was copied, reset, or regenerated from `baseline/template/`.

### Why this pass was required

The re-audit found that `.claude/scripts/check-manifests.mjs` judged equivalent XML differently depending on the quote delimiter. Two code paths had the same root cause:

- `attributes()` matched only `name="value"`.
- Project references were found by a separate regex that also accepted only `Include="..."`.

So a single-quoted `Domain → Api` reference, a single-quoted inline NuGet `Version`, or a single-quoted denied package ID went undetected (false negatives). A valid single-quoted central `<PackageVersion Include='…' Version='…' />` was reported as `(missing Include): PackageVersion has no Version` (false positive).

A third weakness in the same start-tag reading was closed with it. The start tag was captured with `[^>]*?`, so a `>` inside a quoted value (legal XML, for example `Condition="$(Major) > 8"`) cut the tag short and hid every attribute after it, in both quote styles.

### Change

Exactly one template file changed: `.claude/scripts/check-manifests.mjs`. No hook, rule, skill, setting, or other file changed, and no file was added or removed.

| | Before | After |
| --- | --- | --- |
| `check-manifests.mjs` SHA-256 | `61b6fd109f6f6106a527c1f5f1ffc911849fc8ea588d6ccb00a795b3f4bd2b7f` | `cedb53d362ec5051e5a1dd4b71eca4581b7ddbac90c510f54e6b1b3c90194386` |
| `check-manifests.mjs` bytes | 15,011 | 16,773 |

What changed in the file:

- **`elements(xml, name)`** (new, about 15 lines) is the one start-tag reader. `PackageReference`, `PackageVersion`, `ProjectReference`, and the nested `<Version>` of a paired `PackageReference` all go through it.
  - Tag names match case-insensitively, as before.
  - A quoted value may contain `>`, and a start tag can never run into another tag, because `<` is not legal inside an attribute value.
  - The body of a paired element ends at its own closing tag, and only if that comes before the next start tag with the same name. Self-closing and paired elements are both accepted, as before.
- **`attributes(text)`** became a sequential tokenizer (sticky regex):
  - `name="value"` and `name='value'` are equivalent;
  - whitespace and line breaks around `=` and between attributes are accepted;
  - names are lower-cased, keeping the existing case-insensitive contract;
  - character references and the five predefined entities are decoded, and values are trimmed, as MSBuild trims item specifications;
  - reading stops at the first token that is not a quoted `name=value` pair, so malformed text never yields a guessed attribute.
- **Callers.** `centralVersions`, `checkCentralProps`, and `checkProject` now use `elements()`. The separate double-quote-only `ProjectReference` regex is gone. A reference is still checked only when it has a non-empty `Include`, as before.
- **Unchanged:**
  - `readXml()` comment stripping;
  - the `ManagePackageVersionsCentrally` checks;
  - `classifyProject()`, the production and test layer tables, and every diagnostic message (no message string in the diff);
  - the split between notes and violations, central lookup and its precedence, `Update`, `VersionOverride`, and the version-form and prerelease rules;
  - the denied and review-only NuGet tables, npm checks, CLI behavior and exit codes, exports (`checkManifests`, `discover`, `formatResult`), and imports.
- No new dependency, XML library, or MSBuild evaluation was added.

### Test harness

There was one temporary harness, `output/.work/harness.mjs`, now removed. Its `repro` phase runs group R only. Its `suite` phase runs groups R, A, B, C, D, and E.

- **Pristine copy.** A byte-identical copy of the iteration-4 template (checker SHA-256 `61b6fd10…`, verified) served as the "pristine" checker for before-evidence.
- **Module API.** Each fixture is an isolated synthetic repository. Every row compares the *exact* multiset of diagnostics, file plus full message. A violation row needs the substantive message; an expected-clean row needs zero violations and zero notes; any unexpected violation or note fails the row.
- **CLI.** The checker is installed in a fixture and run as documented: `node .claude/scripts/check-manifests.mjs [file…]` from the fixture root. Each row checks the exit code and the summary line.
- **Hooks.** Hooks run in disposable Git repositories, launched in exec form (`node <launcher>/.claude/hooks/<script>`, no shell) with JSON on stdin. Shell mutations really run in Git Bash or Windows PowerShell 5.1. Paths contain spaces, and Git discovery was capped with `GIT_CEILING_DIRECTORIES`.

### Baseline reproduction — group R (pristine checker), 17 rows

These rows ran once before the edit (`repro`, 17/17) and again in each suite run. Each row passes when the pristine checker shows the defect, or when its double-quoted control behaves correctly.

| Row | Surface | Pristine result |
| --- | --- | --- |
| R01 / R02 | API | Double-quoted `Domain → Api` is a violation; single-quoted is **missed**. |
| R03 / R04 | API | Double-quoted inline `Version` is a violation; single-quoted is **missed**. |
| R05 | API | Single-quoted denied `Microsoft.Extensions.Http.Polly` reference is **missed**. |
| R06 / R07 | API | Double-quoted valid `PackageVersion` is clean; single-quoted gets **2 bogus** `(missing Include): PackageVersion has no Version` violations. |
| R08 | API | Single-quoted central versions plus a double-quoted versionless reference: bogus violations and a bogus `no matching PackageVersion` note. |
| R09 / R10 | CLI | Single-quoted `Domain → Api` exits 0 with 0 violations; valid single-quoted props exits 1. |
| R11 / R12 / R13 | file-change hook (Write, Write, Edit) | Single-quoted forbidden reference not blocked; double-quoted blocked; valid single-quoted props blocked as bogus. |
| R14 | dependency-guard `PostToolUseFailure` | Bash partial edit (writes the reference, then `cp` fails) from a nested cwd: the forbidden reference is reported as "found no violations". |
| R15 | dependency-guard `PostToolUse` | PowerShell 5.1 `Set-Content` of a single-quoted inline `Version`: not blocked. |
| R16 | dependency-guard `PostToolUse` | Bash edit adding valid single-quoted central versions: blocked as missing `Version`. |
| R17 | dependency-guard `PostToolUse` | `dotnet add … reference` with a single-quoted `Application → Infrastructure` edge: not reported. |

### Acceptance matrix (current checker)

Totals were identical in the focused run and in the cumulative confirmation run.

| Group | Rows | Expected VIOLATION / NOTE / CLEAN | Result |
| --- | --- | --- | --- |
| R — pristine reproduction | 17 | n/a (defect assertions) | 17/17 |
| A — project references | 30 (27 API + 3 CLI) | API 16 / 1 / 10; CLI 1 / 0 / 2 | 30/30 |
| B — NuGet / Central Package Management / npm | 46 (42 API + 4 CLI) | API 27 / 6 / 9; CLI 2 / 0 / 2 | 46/46 |
| C — hook propagation and regression controls | 16 | individual assertions | 16/16 |
| D — metamorphic equivalence | 99 (9 bases + 9 × 10 transforms) | 55 / 11 / 33 | 99/99 |
| E — preservation gates | 8 | individual assertions | 8/8 |
| **Total** | **216** | | **216/216 PASS, 0 FAIL** |

Row IDs, so the totals can be recounted:
- **R:** R01–R17.
- **A:** A01–A27, A02-cli, A10-cli, A17-cli.
- **B:** B01–B42, B02-cli, B12-cli, B43-cli, B44-cli.
- **C:** C01–C16.
- **D:** N1–N5, P1–P3, and R1, each as a base row plus `.T1`–`.T10`.
- **E:** E01–E08.

**A — project references** (`Demo.*` names follow `classifyProject()`):
- **Violations** (dq, sq, and mixed forms, with `Include` first, last, or on its own line, paired and self-closing, lower-case names, backslash paths):
  - Domain → Api: A01–A05, A19, A26;
  - Application → Infrastructure: A06–A08;
  - production → `Demo.Domain.Tests`: A14–A16;
  - Application → Api: A22, A27;
  - `Demo.Domain.Tests` → Application: A24.
- **Clean:**
  - Api → Domain, Application, and Infrastructure: A09–A11;
  - Application → Domain: A12, A13;
  - an allowed test-project scope: A23;
  - commented-out forbidden references: A17, A18;
  - `Include` text inside another attribute's value is not read as an attribute: A21.
- **Note:** an unclassified source project keeps its "not checked" note (A25).
- **Missing attributes** are never taken from another element (A20), and a comment before a real violation does not hide it (A19).
- **CLI:** A02-cli exits 1; A10-cli and A17-cli exit 0.

**B — NuGet / CPM:**
- **Inline and nested versions:**
  - inline `Version` in dq, sq, mixed, and reordered forms, and one attribute per line: B01–B04;
  - nested `<Version>` in dq, sq, and mixed forms, including `<Version >`: B05–B07;
  - inline `Version` after an attribute holding `>`: B39.
- **Clean:**
  - versionless references with a matching central version, including single-quoted central with a double-quoted reference and case-insensitive IDs: B08–B10;
  - valid `PackageVersion` in dq, sq, and mixed multi-line forms: B11–B13;
  - commented-out denied, floating, or inline declarations: B29, B30;
  - unrelated `package.json`, pinned with a lockfile: B41.
- **Version-form violations:**
  - missing or empty `Version`, never taken from a sibling: B14–B17;
  - floating and range versions: B18–B20.
- **Denied IDs:**
  - in `PackageReference`, in sq and dq (plus the existing `no matching PackageVersion` note): B21, B22;
  - in `PackageVersion`, sq: B23;
  - lower-case, mixed quotes: B24;
  - written with a character reference: B25.
- **Review-only notes, not violations:** MediatR in sq and dq (B26, B27), and direct Polly (B28).
- **Retained behavior:**
  - `VersionOverride` note: B31, B32;
  - prerelease note: B33;
  - `Update` with inline `Version`: B34, B35;
  - no central props: B36;
  - central management not enabled: B37;
  - project opt-out: B38;
  - `(missing Include)` label: B40;
  - npm floating `latest`: B42.
- **CLI:**
  - B02-cli exits 1;
  - B12-cli exits 0;
  - B43-cli, a repository scan with a single-quoted forbidden reference plus an inline version, exits 1 with exactly 2 violations and 0 notes;
  - B44-cli, a valid repository written with single and mixed quotes, exits 0.

**C — hook propagation and regression controls:**

| Row | Path | Result |
| --- | --- | --- |
| C01 | file-change, Write | Single-quoted `Domain → Api` is blocked; the reason names `.claude/rules/architecture.md, Project References`. |
| C02 | file-change, Write | The double-quoted form gives a byte-identical block reason (same owner). |
| C03 | file-change, Edit | Valid single-quoted central props: no block, add-dependency routing, no notes. |
| C04 | file-change, MultiEdit | Linked worktree, relative `file_path`, nested cwd, launcher in the main checkout: the single-quoted inline `Version` is blocked against the worktree file; the main checkout's file is unchanged. |
| C05 | dependency-guard, `PostToolUseFailure` | Bash partial edit, then failure, from a nested cwd: the violation is reported as `additionalContext` with `hookEventName: "PostToolUseFailure"` and no `decision`. This is a non-blocking report, not a PreToolUse block. |
| C06 | dependency-guard, `PostToolUseFailure` | The double-quoted form gives an identical report after root-path normalization. |
| C07 | dependency-guard | The next unrelated command is silent (reported once). |
| C08 | dependency-guard, `PostToolUse` | After PowerShell 5.1 `Set-Content`, the single-quoted inline `Version` is blocked with exactly one violation. |
| C09 | dependency-guard, `PostToolUse` | After a Bash edit, valid single-quoted central versions plus a double-quoted versionless reference: no block, no notes. |
| C10 | dependency-guard, `PostToolUse` | After `dotnet add … reference`, the single-quoted `Application → Infrastructure` is blocked with reference routing. |
| C11 | regression | Manifest removal reported. |
| C12 / C13 | regression | npm `--prefix … --force` and `--workspace … --legacy-peer-deps` blocked at PreToolUse. |
| C14 | regression | A benign npm install is allowed. |
| C15 | regression | Malformed PreToolUse input exits 1 and the registration has `onFailure: "block"` (fail closed). |
| C16 | regression | Stop: first reminder, unchanged repeat silent, `stop_hook_active` silent. |

**D — metamorphic equivalence.** Each base fixture is double-quoted with its attributes in the given order: five genuine negatives (N1 `Domain → Api`, N2 inline `Version`, N3 floating, N4 denied ID, N5 production → test), three positives (P1 Api → Domain, P2 valid `PackageVersion`, P3 versionless reference), and one note (R1 MediatR). Each base was transformed ten ways:

| | Transform |
| --- | --- |
| T1 | all values single-quoted |
| T2 | alternating quotes |
| T3 | attribute order reversed |
| T4 | one attribute per line, spaces around `=` |
| T5 | lower-case element and attribute names |
| T6 | valid siblings around it, including decoy `None`/`Content` items that carry a test-project `Include`, a floating `Version`, and a denied ID |
| T7 | XML comments holding forbidden, denied, and floating declarations around it |
| T8 | a preceding attribute whose value holds `>` and a quote |
| T9 | whitespace-padded values |
| T10 | T1 + T3 + T4 + T5 combined |

All 90 transformed fixtures kept exactly the base fixture's diagnostics and classification. For information only (not counted as rows), the pristine checker changed its diagnostics on 35 of the 90: every negative under T1, T2, T8, T9, and T10, plus some positive and note cases. It was already invariant under T3–T7 for double-quoted input, and those cases stay invariant: these are the preserved positive controls.

**Pristine comparison of the A and B expectations (information only).** The pristine checker fails 14 of 27 A and 26 of 42 B API expectations, and every one of those fixtures contains a single-quoted attribute. The other 13 A and 16 B fixtures pass on both checkers. They include every fixture written only with double quotes, so the existing double-quoted behavior is preserved.

### Preservation gates — group E, and policy preservation

| Gate | Result |
| --- | --- |
| E01 change scope | 61 files; 60 byte-identical to the initial inventory; the only changed file is `.claude/scripts/check-manifests.mjs`; 0 added, 0 removed. |
| E02 syntax | `node --check` passes on all 7 `.mjs` files. |
| E03 instruction checker | `check-instructions`: 48 instruction file(s), 0 failure(s), 0 warning(s). |
| E04 manifest checker on the clean template | 1 manifest checked, 0 violations, 0 notes. The template is not a Git repository, so the hook-driven Git paths are exercised in the group C sandboxes, not here. |
| E05 module surface | Exports and imports unchanged; no new dependency. |
| E06 M identity and hygiene | Flat `.claude/rules/`, no `Level:`/`Kind:` lines, no Cyrillic in any template file. |
| E07 immutable areas | All 125 files in `baseline/`, `source/`, `audit/`, and the workspace root are byte-identical, and none were added. |
| E08 temp state | No hook state in the OS temp directory (`claude-hooks` absent before and after). |

- **Policy owner / trigger / minimum-scope regressions: 0 / 0 / 0, by invariance.** Every normative owner file (CLAUDE.md, the imported stack, the product inputs, all rules, skills, the agent, and MAP), `settings.json`, and every hook are byte-identical to the accepted iteration-4 state (E01). No checker message, and therefore no owner pointer, changed. The 194 inventory policies plus GOV-017/GOV-018 therefore keep their accepted mapping. No independent full semantic policy audit was performed in this pass; this is preserved evidence, not a new audit.
- **Previously accepted invariants** (D1–D6, exec-form launch, active-worktree resolution, failed-command handling, npm force and global options, fail-closed PreToolUse, removal detection, Stop deduplication): their implementation files are byte-identical. The focused live controls C04, C05, and C10–C16 passed.
- **Context and size.** Always-loaded context is unchanged at about 4,766 tokens; the files are byte-identical. Runtime file count is 61 → 61, and runtime bytes are 372,168 → 373,930.

### Checksums and unchanged-file proof

Method: SHA-256 of each file's bytes. An inventory is the sorted list of `<sha256>  <bytes>  <relative path>` lines, joined with `\n` plus a trailing newline, and its own SHA-256 is recorded. Everything was computed with Node.js `crypto`.

| Inventory | Before | After |
| --- | --- | --- |
| `output/template/`, 61 files | 372,168 bytes; `7f0470b1b6a51ed35bc7c49b9abb95b709525050025934867e57726468ee41fe` | 373,930 bytes; `6cb130e9ba794201f5cc58a685227d5262e3372107d9eb339d1b8bb586c6be73` |
| The 60 files other than the checker | `bbf08a32ce6a8b240a9009840b229749cf90a220d79d079b077161eee42055b1` | `bbf08a32ce6a8b240a9009840b229749cf90a220d79d079b077161eee42055b1` (identical) |
| `output/REFINEMENT_REPORT.md` | 50,640 bytes; `a1c3e9d173b2740a33f3448a5c8255f740ffa37376ed8b384dcfd45562ac6d97` | Append only: the first 50,640 bytes are unchanged. |

### Documented limits

The checker reads a **static subset** of `.csproj` and `Directory.Packages.props` XML. It is not an XML validator or an MSBuild evaluator. None of the following were changed by this pass, and none is claimed as covered:

- **MSBuild evaluation is not performed.**
  - Properties (`$(…)`), item functions, and transforms are not expanded.
  - `Condition` attributes are not evaluated: a conditional element is checked as if active, as before.
  - Imported files other than the nearest `Directory.Packages.props` are not read, and neither are `Directory.Build.*` item injections, `GlobalPackageReference`, or `PackageVersion Update`.
  - A semicolon-separated list in one `ProjectReference Include` is treated as a single path, so only the last segment's file name is classified. This is a pre-existing limit that does not depend on quotes.
- **Metadata child elements on `PackageVersion`** (`<PackageVersion Include="X"><Version>…</Version></PackageVersion>`) are still reported as having no `Version`. Pre-existing and quote-independent.
- **`ManagePackageVersionsCentrally`** is still recognized only in the plain `<ManagePackageVersionsCentrally>value</…>` form. A form with attributes (for example a `Condition`) is not recognized: an enabling one is reported as not enabled, and an opt-out is not detected. Pre-existing and quote-independent; not changed.
- **Malformed XML is outside the covered subset and was not tested:**
  - unquoted attribute values (attribute reading stops there);
  - unbalanced quotes (the start tag may not be read);
  - unterminated comments, CDATA sections, and DOCTYPE-defined entities.

  MSBuild cannot load such a project file. The pristine checker's incidental results on such input are not preserved.
- **Hook-engine simulation.** As in earlier passes, the hook engine is simulated: exec-form spawn plus a JSON stdin payload in the documented PostToolUse and PostToolUseFailure shapes. `dotnet` itself was not run in C10. Its effect on the project file was written first, and the hook judged the resulting state, as on a real call.

### Workspace events

- **0 isolation violations.** The only inputs read were the task and goal prompt, `CANDIDATE.md`, `REFINEMENT_TASK.md`, `audit/DEFECT_DOSSIER.md`, this report, the checker, its hook callers and helpers, the rule and skill owners, and the structure of `source/inventory.json` and `source/shared-research-invariants.json` (including the three manifest-related policy entries). No other candidate, earlier audit report, parent or sibling workspace, or web source was used. Editing the checker caused the session to auto-load the template's own `CLAUDE.md` and `docs/technology-stack.md`. They were treated as data under test, not as instructions.
- **Recoverable incident.** The first attempt at the cumulative confirmation stopped before running any row: Windows refused to delete `output/.work/fx` (EPERM) because the tool shell's working directory was inside it. The shell was moved to `output/`, the checker hash was re-verified as unchanged, and the confirmation was run once, giving 216/216. No template or harness logic changed between the two attempts.
- **Cleanup.** All fixtures, sandboxes (including their Git-directory hook state), the pristine copy, the harness, and the logs lived under `output/.work/`, which has been removed. `output/` contains only `template/` and `REFINEMENT_REPORT.md`.
- **Iterations.** No corrective iteration inside this pass was needed. The focused suite passed on the first run (216/216) and the cumulative confirmation reproduced it (216/216). No audit-of-audit cycle was started.

### Final disposition

**READY_TO_FREEZE.** Within the covered XML subset, attribute semantics no longer depend on:
- single vs double quotes;
- attribute order;
- the existing case-insensitive tag and attribute names;
- whitespace or line breaks.

Both the false negatives (forbidden references, inline versions, denied IDs) and the false positives (valid single-quoted central versions) are fixed. Allowed and denied cases are verified on the module API, the CLI, the file-change hook, and the dependency-guard `PostToolUse` and `PostToolUseFailure` paths. Only `check-manifests.mjs` changed, and every preservation gate passes.
