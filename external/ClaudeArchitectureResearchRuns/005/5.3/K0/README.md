# Iteration 005 / 5.3 / K0

Controlled refinement workspace for **Candidate K0 — Kinds × Scopes, Embedded Capabilities**.

Selected immutable raw baseline: **5.2 / K0 / Run-02**.

Run-01 is comparative evidence only. Its template is intentionally absent so refinement cannot merge two independently generated implementations into a Frankenstein baseline.

## Pre-run protocol refactor

Before the first K0 5.3 execution, the refinement contract was strengthened using defects and process failures already observed while refining M, M1, L0, and L1.

The first K0 refinement therefore starts with the current common quality bar rather than discovering the same defects through later corrective passes. In particular, the contract now explicitly covers:

- `PostToolUseFailure` and failed shell calls with partial side effects;
- actual-state post-change validation rather than command-text-only validation;
- per-worktree fresh/later state and HEAD transitions;
- additions/deletions/moves/same-file rewrites;
- UTF-8 BOM and relevant UTF-16 Windows manifest encodings;
- material-state Stop deduplication;
- complete declared K0 Kind conformance direction including ENF;
- bounded Git-safety classifier tests;
- one persistent temporary harness until final confirmation;
- one clean cumulative confirmation audit as sufficient convergence evidence;
- an explicit prohibition on audit-of-audit, verifier mutation campaigns, live-session hook relocation, and open-ended shell/Git fuzzing after the documented matrix is clean.

This changes the **refinement procedure**, not the immutable raw baseline or Candidate K0 architecture.

## Execution

1. Open a **fresh** Claude Desktop Code session with this `K0/` directory as the workspace root.
2. Invoke `/goal` with the exact contents of `GOAL_PROMPT.txt`.
3. Do not modify `baseline/`, `source/`, or `audit/` while the goal is running.
4. The refinement writes only under `output/`.
5. Do not intervene unless Claude reports a genuine `BLOCKED` condition or requests a permission that crosses the workspace boundary.

No `/compact` is needed before this first K0 refinement run because the session should start clean.

## Promotion rule

The result is accepted only if it is demonstrably **STRICTLY_BETTER** than the immutable baseline and the complete cumulative confirmation gate passes.

A tie is not an improvement.
