# PI-012 sensitivity

Recomputed from `PI012_79_REVIEW.jsonl`, `PI012_230_REVIEW.jsonl`, `PI012_EXTENSION_REVIEW.jsonl` and `_rules/R01-HQ06-PI012/OVERLAY.jsonl`. Label and modality counts, not a strictness comparison.

## Cases read

| List | Rows | CORRECT | UPHOLD | UNRESOLVED |
|---|---:|---:|---:|---:|
| 79 flat negatives | 79 | 55 | 22 | 2 |
| 230 residual leads | 230 | 105 | 123 | 2 |
| Extension (same-class scan outside both lists) | 30 | 22 | 8 | 0 |

Unique cases by original stable key: 263 (76 keys sit on both lists). `MUST` and `MUST_NOT` are one force class: where only the token polarity differs the stored token stays and the row says so.

## By form

| Form | Result | Cases |
|---|---|---:|
| APPROVAL_GATE | UPHOLD | 14 |
| BY_REFERENCE | CORRECT | 2 |
| BY_REFERENCE | UPHOLD | 12 |
| CHARACTERIZATION | CORRECT | 5 |
| CHARACTERIZATION | UPHOLD | 1 |
| ELLIPTICAL | UPHOLD | 5 |
| EXCEPTION_DENIED | UPHOLD | 6 |
| EXPLICIT_DEFAULT | CORRECT | 6 |
| LABEL | CORRECT | 6 |
| LABEL | UPHOLD | 1 |
| MARKED | CORRECT | 15 |
| MARKED | UPHOLD | 77 |
| NEG_DECLARATIVE | CORRECT | 17 |
| OBLIGATION_REMOVED | CORRECT | 1 |
| OTHER | CORRECT | 9 |
| OTHER | UNRESOLVED | 2 |
| OTHER | UPHOLD | 4 |
| PERMISSION_CONDITION | CORRECT | 56 |
| PERMISSION_CONDITION | UPHOLD | 7 |
| POSITIVE_IMPERATIVE | CORRECT | 11 |
| TRIGGERED | UPHOLD | 6 |

## `MUST_NOT` records by candidate under each reading

| Candidate | Baseline (rule rejected) | Approved addendum | Option D: only-when and do-not-unless stay binding, other forms follow the addendum |
|---|---:|---:|---:|
| M | 199 | 183 | 193 |
| M1 | 231 | 217 | 224 |
| L0 | 183 | 171 | 177 |
| L1 | 201 | 185 | 196 |
| K0 | 180 | 160 | 167 |
| K1 | 223 | 207 | 218 |

The addendum picks `DEFAULT` as the common value for permission-granting conditionals in knowledge text. Option D is the alternative the decision wording does not fully exclude; see the addendum, section "Uncertainty kept".

## Policy cells

Coverage `status` moved on 0 of 1,176 cells. `strength_status` moved on 0 cells.

## Classes kept visible

- **Triggered prohibitions** (`do not X when Y`): 6 cases in the reviewed set stay at `MUST_NOT` under A1.3, class `TRIGGERED`. A scan outside the reviewed set found 21 more (bound, not a census). If a later decision reads them with `only when`, these move to `DEFAULT`.
- **Security-sensitive `DEFAULT` lines:** `FG-K0-0cf8d7ed7b`, `FG-K0-345276aafe`, `FG-K1-c7d26b5b93`, `FG-L0-ff8742f01e`, `FG-L1-a0b4d693e7`, `FG-M-4afc784153`, `FG-M1-1629ce14d0`. The rule owners stay binding where the coverage rows show them.
- **Approval gates** (`unless explicitly requested`, `only when explicitly requested`, `unless asked`) stay binding in every form, under C8.
- **Wording splits kept because the marked form falls under frozen A1.3, not under the approved equivalence:** `FG-M-f49bbb7f3e` and `FG-M1-4efa9a2d0d`; `FG-M-9050e41bb6` and `FG-M1-7390ef4e06`; `FG-L1-27906e338d` and `FG-M-58080e9816`, `FG-M1-915d8195be`; `FG-K0-87b93f63f7` and the "never hide" lines in M, L1, K1; `FG-M-f08ed79dde`, `FG-M1-b7c8a98af1` and `FG-L0-bd2c887b48`, `FG-L1-0cdd9708ae`. Step 3 must not count these as strictness differences.
- **Source differences that are real:** L1 `FG-L1-e0afa72103` and K1 `FG-K1-6ee32b45c6` write "Never" where M, M1, L0, K0 write "Not retried:".

## Disagreement with the audit on the 79

- `FG-K0-0ef1e5ed3d`: audit `MUST_NOT`, here `MUST_NOT` (UNRESOLVED)
- `FG-K0-6d06b21a93`: audit `MUST_NOT`, here `MUST_NOT` (UNRESOLVED)

The audit and this reading are the same model family, so agreement is weak evidence of correctness.

## Bounds, not a census

- The 79 are a floor from one scan. The 230 are a heuristic: stored `MUST` or `MUST_NOT` on knowledge text where the closest sentence has no must-like word.
- The extension scan looked at the sentence closest to the claim on knowledge-only records outside both lists: 22 `do not ... unless/without`, 8 `only when`, 21 `do not ... when/if`. A sentence the heuristic does not pick is missed, so these are lower bounds.
- Records with evidence in rule files or workflow skills were not read under this rule; the frozen readings hold there.
