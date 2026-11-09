# Baseline Selection — L1

## Decision

Use **L1 / Run-02** as the immutable baseline for Iteration 5.3.

Do not merge Run-01 files into the baseline. Run-01 is comparative evidence only.

## Why Run-02

Both raw runs implement the same L1 design point:

- primary stability hierarchy `0 Core -> 1 Architecture -> 2 Technology -> 3 Project`;
- level-first rule organization;
- exactly four replaceable capability slots;
- `architecture` as the required frame;
- `persistence`, `backend-testing`, and `frontend` as leaves;
- static composition;
- contracts + manifests + runtime facets;
- L-style stratified decisions;
- no Kinds × Scopes taxonomy.

Run-02 is the better refinement baseline because it is materially smaller and cleaner in its capability composition:

| Measure | Run-01 | Run-02 |
|---|---:|---:|
| runtime files | 96 | **85** |
| runtime bytes | 340,449 | **298,925** |
| Markdown files | 80 | **69** |
| rule files | 27 | **18** |
| skill entry points | 29 | **28** |
| approximate always-loaded chars | ~19.1k | ~20.3k |
| approximate always-loaded tokens (chars/4) | ~4.77k | ~5.09k |

Run-02 also has:

- `PreToolUse` matching both Bash and PowerShell;
- BOM-tolerant hook-input parsing through `.trim()` before JSON parsing;
- a cleaner static capability selection record;
- tested optional-frontend removal;
- fewer runtime artifacts and less total maintenance surface.

## Important counterweight

Run-01 preserved V2 wording/technique more literally.

Independent lexical diagnostics (not promotion metrics) favored Run-01:

- policy-to-generated-text mean best TF-IDF similarity: Run-01 ~0.434, Run-02 ~0.394;
- V2 section-to-generated-text mean best TF-IDF similarity: Run-01 ~0.460, Run-02 ~0.401;
- V2 sections below 0.25 similarity: Run-01 103, Run-02 161.

These diagnostics do **not** prove semantic loss, but they make V2-fidelity review mandatory during refinement.

Run-02 is selected because the missing/over-compressed technique can be restored from the frozen V2 source, whereas its simpler topology is a better maintainable starting point.

## Promotion principle

The 5.3 result must be demonstrably better than Run-02, not merely different.

A tie is not an improvement.
