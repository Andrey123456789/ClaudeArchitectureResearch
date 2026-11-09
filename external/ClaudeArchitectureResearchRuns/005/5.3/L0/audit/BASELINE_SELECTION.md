# L0 baseline selection

## Decision

Select **Run-02** as the immutable baseline for L0 refinement.

## Why Run-02

Both runs implement the same L0 design point: four stability levels, level-first rules, stratified always-loaded architecture/project decisions, embedded technologies, no capabilities, no Kind taxonomy, and the same trigger-role model.

Run-02 is preferable because:

- Levels 0/1 are clean of the concrete-technology leakage independently found in Run-01 (`ProblemDetails` and an Angular-named routing pointer in Level 1).
- Its Windows hook input parser correctly tolerates a UTF-8 BOM; Run-01 fails on such input.
- Its structure is more consolidated: 71 runtime files versus 78, while preserving the same candidate identity and required workflow/knowledge surfaces.
- Its primary audit explicitly removed technology-named Level 0/1 pointers and tightened the neutrality checker.
- It was produced under the bounded 5.2.2 protocol, whereas Run-01 was affected by the earlier post-convergence protocol behavior; usage figures are therefore not a fair basis for choosing Run-01.

Run-02 is not defect-free. Its enforcement layer has material cwd/worktree/fail-open/command-classification defects documented in `DEFECT_DOSSIER.md`. Those are targeted refinement defects, not reasons to prefer the structurally less clean Run-01.

## Summary metrics

| Metric | Run-01 | Run-02 |
|---|---:|---:|
| Runtime files | 78 | 71 |
| Runtime bytes | 269,166 | 305,547 |
| Markdown files | 66 | 63 |
| Markdown bytes | 219,933 | 257,463 |
| Always-loaded estimate | ~4,385 tokens | ~5,002 tokens |
| Rule modules | 27 | 24 |
| Skill directories | 28 | 29 |
| Level 0/1 concrete-tech leakage found independently | yes | no |
| UTF-8 BOM hook input | fails | passes |
| Instruction checker | PASS | PASS |

The larger Run-02 text corpus is not by itself a defect. Refinement should reduce unnecessary context only when this is demonstrably possible without policy, trigger, scope, or V2-detail loss.
