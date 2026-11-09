# R02 HQ-01 / GOV-015 and 9.1: baseline and impact

**Target behavior.** Authority: a specific user request, or a pre-approval naming operation and scope. Generic "approved workflow", general task approval, or a workflow step mentioning a commit is no authority. Trigger: any repository-changing Git operation. Task-start check: pre-existing uncommitted changes (staged, unstaged, untracked) at the start of a task that will change files or repository state. Two options only: commit identified changes within a scope the user authorizes, or suspend the whole task. Headless without an adequate standing choice: pause, change nothing, report. Exception: changes made during the current task. Before destructive operations: re-check authority and preservation of foreign changes. Explicit request to rewrite a named branch including `main` is valid unless another policy forbids it.

**Original quotes.** `CLAUDE.md`: "Do not commit, push, merge, rebase, reset, force-push, delete branches, or perform other repository-changing Git operations unless explicitly requested." `git-workflow`: "Perform them only when explicitly requested or clearly required by an approved workflow" (M, M1, L0, K1), "required by an approved workflow" (L1, K0); "treat `main`, `master`, and other protected or shared branches as non-rewritable" (all six).

**Files.** `CLAUDE.md` and `git-workflow/SKILL.md` in all six; K0 `hooks/hook.cjs` reason text; map rows in M, L1, K0.

**Related policies.** GOV-015 (owner), GOV-014, GOV-016, GOV-019, GOV-020, GOV-017. Transitive consumers: `add-dependency` and dependency rules saying "commit package.json and package-lock.json", K1 `frontend-setup.md` "commit package-lock.json". They state what belongs in version control; the new clause "a workflow step that mentions committing is not that authority" closes that reading. No such line was edited.

**Shared semantics versus mechanism.** The obligation is equal in all six and delivered by the always-loaded operating policy, which each architecture already has. Procedure sits in each candidate's own `git-workflow`. K0 alone has a Git hook, it keeps asking, and only its reason text changes. No Git hook is added to the other five: forcing identical hooks is out of contract (§5).

**Regression risks.** Headless pause could read as authority for or against Reserved work (checked again at R05). A dirty generated tree in a future headless experiment now pauses: harness owners should supply a standing choice or a clean tree. Recorded in the final report as an experiment-design consequence.

**Interpretation recorded.** "Task" is read as a task that will change files or repository state, so a read-only inspection or review of a dirty tree does not trigger the gate. The register says «в начале работы». Applying it to read-only work would block `code-review` of uncommitted work. Listed in `UNRESOLVED_DECISIONS.jsonl` for the user.

**Pre-change controls.** Suite ran before the patch: 37 FAIL, 27 PASS, 2 NOT_RUN (`suite_pre.jsonl`). All 12 clause checks and all 24 mutation checks failed, as expected.
