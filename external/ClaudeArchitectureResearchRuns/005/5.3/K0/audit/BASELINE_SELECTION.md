# Baseline Selection — K0

## Decision

Use **K0 / Run-02** as the immutable baseline for Iteration 5.3.

Do not merge Run-01 files into it. Run-01 is evidence only.

## Why Run-02

Both raw runs implement the same K0 design point:

- seven Kinds: OP, DEC, STD, KNW, WF, ENF, IN;
- six declared Scopes: common, backend, backend-tests, frontend, delivery, repo/meta;
- one always-loaded decision register;
- STD organized scope-first;
- KNW and WF separated by responsibility/mechanism;
- embedded technologies rather than capability slots;
- no stability levels;
- no capability contracts/manifests/selection/facets;
- Kind × Scope human map;
- decision `Affects` relationships.

Run-02 is the better refinement baseline because it reaches the same architecture with less maintenance surface and a lower always-loaded cost:

| Measure | Run-01 | Run-02 |
|---|---:|---:|
| runtime files | 66 | **62** |
| runtime bytes | 356,264 | **324,363** |
| Markdown files | 56 | **55** |
| STD rule files | 15 | **14** |
| skills | 29 | 29 |
| generated always-loaded estimate | ~5.36k tokens | **~4.93k tokens** |
| instruction checker | PASS | PASS |
| JS syntax | PASS | PASS |

Run-02 also has a root-stable launcher relative to ordinary nested `cwd` (unlike Run-01's direct `node .claude/hooks/...` launcher) and project-level Git `ask` configuration.

## Important Run-01 advantages

Run-01 is materially stronger in several implementation details:

- its dependency command classifier handles package removal and the tested npm/pnpm/yarn global-option forms that Run-02 misses;
- it has an explicit repository-changing Git command classifier rather than relying on a partial `permissions.ask` list;
- its hook JSON parser tolerates a UTF-8 BOM because it parses the trimmed input;
- it preserves V2 wording/technique substantially more literally.

These are quality signals for 5.3, **not** permission to copy Run-01 files. The refinement must solve the underlying requirements from the frozen sources and defect evidence.

## Independent fidelity diagnostics

TF-IDF best-match diagnostics are not correctness metrics, but they help identify areas requiring manual review:

- normalized 194-policy mean best match: Run-01 ~0.390, Run-02 ~0.391;
- normalized policies below 0.25: Run-01 33, Run-02 29;
- V2-section mean best match: Run-01 ~0.517, Run-02 ~0.429;
- V2 sections below 0.25: Run-01 55, Run-02 123.

This means Run-02 appears at least as strong on normalized policy wording while being much more compressed relative to the original V2 technique/examples. A source-based V2 fidelity review is therefore mandatory.

## Promotion principle

The selected baseline is not assumed correct because its generated report says PASS. The 5.3 result must fix all independently confirmed defects while preserving K0 identity and the frozen policy oracle.

**A tie is not an improvement.**
