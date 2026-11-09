# Iteration 005 / 5.3 / L1

Controlled refinement workspace for Candidate **L1 — Stability-first + Replaceable Capabilities**.

Selected raw baseline: **5.2 / L1 / Run-02**.

Run-01 is comparative evidence only and is intentionally not present as a template to copy from.

This refinement contract was updated before the first L1 5.3 execution to incorporate defects and process failures discovered while refining M and M1. The update does not alter the frozen candidate, baseline, source corpus, or raw evidence. It strengthens the bounded test matrix and the STOP rule so known cross-candidate enforcement failures are addressed in the first L1 pass without recursive verification work.

## Execute

Open a **fresh Claude Desktop Code session** with this `L1/` directory as the workspace root.

Invoke `/goal` with the exact contents of `GOAL_PROMPT.txt`.

Do not manually patch `baseline/`, `source/`, `audit/`, or the candidate definition. Refinement writes only under `output/`.

## Promotion rule

The refined result is accepted only when it is demonstrably **STRICTLY_BETTER** than the immutable baseline under the cumulative gate in `REFINEMENT_TASK.md`.

A tie is not an improvement.

A clean required confirmation audit is sufficient evidence of convergence. Do not reopen a clean result for mutation-analysis, audit-of-audit, live-hook relocation, repeated baseline proving, or open-ended shell fuzzing.
