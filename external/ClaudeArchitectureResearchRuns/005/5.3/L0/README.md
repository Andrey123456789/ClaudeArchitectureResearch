# Iteration 005 / 5.3 — L0 controlled refinement

This workspace refines one selected raw L0 implementation from iteration 5.2.

Selected baseline: **L0 / Run-02**.

The baseline is immutable. Work only in `output/`.

## Pre-run prompt hardening

Before the first L0 refinement run, the refinement contract was hardened using failure classes already discovered elsewhere in iteration 5.3. No L0 baseline/template output was changed by this hardening.

The hardened task intentionally includes, from the first pass:

- nested-cwd and active-worktree root separation;
- fail-closed critical PreToolUse;
- actual-state validation after successful **and failed** Bash/PowerShell calls;
- `PostToolUseFailure` coverage;
- fresh/later HEAD transitions, same-file rewrites, deletions and moves;
- BOM/Windows text-encoding robustness;
- Stop material-state deduplication;
- a bounded convergence rule that forbids audit-of-audit, mutation-analysis, repeated live-hook relocation, and open-ended shell fuzzing after the documented matrix passes.

This is intended to avoid corrective-iteration churn while applying the same final quality bar to L0.

## Read order

1. `REFINEMENT_TASK.md`
2. `CANDIDATE.md`
3. `audit/DEFECT_DOSSIER.md`
4. `audit/BASELINE_SELECTION.md`
5. `audit/RUN_COMPARISON.md`
6. `audit/EXTERNAL_MECHANICS_NOTES.md`
7. frozen sources under `source/`
8. immutable implementation under `baseline/template/`

## Execution

Use a **fresh Claude Desktop Code session** rooted at this `L0/` directory and invoke `/goal` with the exact contents of `GOAL_PROMPT.txt`.

Do not move the running session into `output/template/` or a sandbox merely to make the copied template's hooks load live. The required process-level hook tests are sufficient under `REFINEMENT_TASK.md`.

Temporary test/audit tooling belongs in `output/.work/`. Keep it until the final report and confirmation audit are complete; remove it only at the end.

The purpose of 5.3 is not to redesign L0. It is to remove implementation defects so the later benchmark compares architectures rather than generation quality.
