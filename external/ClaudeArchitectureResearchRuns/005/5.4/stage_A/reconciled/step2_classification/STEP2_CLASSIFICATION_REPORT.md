# Stage A / Step 2 classification report

Protocol step2-v1 with Addendum A1. Experiment 005, Phase 5.4.

## Result

All 6,402 records of the augmented union are classified and all 1,176 policy rows are filled. The mechanical validator status is **PASS**. That is a structural result, and it does not prove the readings are right. `COVERAGE_LIMITATIONS.md` lists what remains weak.

Step 2 stops here. This run made no cross-candidate strictness comparison, changed no candidate template and started no unification. It did not read the running Codex Pass 2 search.

## Classification

| Candidate | Records | CO | CD | XP | XW | IA | MX | NN | UN |
|---|---|---|---|---|---|---|---|---|---|
| M | 1003 | 699 | 65 | 120 | 46 | 47 | 6 | 17 | 3 |
| M1 | 1113 | 732 | 73 | 134 | 52 | 72 | 13 | 34 | 3 |
| L0 | 972 | 647 | 62 | 119 | 45 | 49 | 23 | 25 | 2 |
| L1 | 1037 | 674 | 80 | 124 | 57 | 61 | 23 | 15 | 3 |
| K0 | 1077 | 687 | 71 | 129 | 59 | 70 | 30 | 27 | 4 |
| K1 | 1200 | 741 | 87 | 145 | 60 | 91 | 40 | 32 | 4 |
| **Total** | **6402** | **4180** | **438** | **771** | **319** | **390** | **135** | **150** | **19** |

CO canonical only, CD canonical plus delta, XP extra product, XW extra workflow, IA internal architecture, MX mixed, NN non-normative, UN uncertain.

These counts describe labels in this dataset. They do not rank the candidates, and label use may have drifted during the run (limitation 11).

| Domain | Records |
|---|---|
| INSTRUCTION_ARCHITECTURE | 390 |
| MIXED | 59 |
| NON_NORMATIVE | 150 |
| PRODUCT_ENGINEERING | 3679 |
| UNCERTAIN | 19 |
| WORKFLOW_ENFORCEMENT | 2105 |

| Oracle relation | Records |
|---|---|
| FULLY_ENTAILED | 4182 |
| NOT_APPLICABLE | 540 |
| NOT_ENTAILED | 1114 |
| PARTIALLY_ENTAILED | 547 |
| UNCERTAIN | 19 |

| Confidence | Records |
|---|---|
| HIGH | 4246 |
| LOW | 33 |
| MEDIUM | 2123 |

All 6,402 records passed a re-read of their evidence from the immutable files, covering 15,620 references. The full breakdown by candidate is in `CLASSIFICATION_SUMMARY.json`.

### Normative strength against the policies

| Candidate | Equivalent | Weaker | Stronger | Portion + remainder | Incomparable | Divergence rows |
|---|---|---|---|---|---|---|
| M | 611 | 91 | 28 | 30 | 4 | 212 |
| M1 | 616 | 121 | 39 | 22 | 7 | 252 |
| L0 | 538 | 116 | 30 | 14 | 11 | 231 |
| L1 | 545 | 137 | 35 | 28 | 9 | 243 |
| K0 | 559 | 138 | 27 | 27 | 7 | 255 |
| K1 | 608 | 140 | 40 | 33 | 7 | 282 |

## Policy coverage

| Candidate | DIRECT | of which by override | Equal-strength evidence | Stronger and weaker only |
|---|---|---|---|---|
| M | 196 | 0 | 196 | 0 |
| M1 | 196 | 6 | 196 | 0 |
| L0 | 196 | 8 | 196 | 0 |
| L1 | 196 | 4 | 196 | 0 |
| K0 | 196 | 10 | 194 | 2 |
| K1 | 196 | 10 | 193 | 3 |

`DIRECT_EVIDENCE` means traceable evidence, not compliance.

## Open items from Step 1 and Pass 1

All 223 pending orphans, 43 apparent conflicts, 4 unresolved items and 17 Pass 1 issues have a recorded outcome, as do all 26 proposals and all 29 facets (7 additional obligations, 22 factual clarifications).

| Candidate | ATTACH | NON_NORMATIVE | RESOLVED | QUEUE |
|---|---|---|---|---|
| M | 51 | 19 | 4 | 5 |
| M1 | 39 | 8 | 4 | 6 |
| L0 | 22 | 6 | 5 | 3 |
| L1 | 20 | 6 | 4 | 3 |
| K0 | 22 | 9 | 7 | 2 |
| K1 | 27 | 3 | 10 | 2 |

## Corrections and semantic challenges

| Candidate | Challenged | Upheld | Revised | Corrections | Label changes from corrections |
|---|---|---|---|---|---|
| M | 38 | 37 | 1 | 145 | 12 |
| M1 | 23 | 21 | 2 | 24 | 3 |
| L0 | 23 | 22 | 1 | 20 | 2 |
| L1 | 23 | 23 | 0 | 21 | 4 |
| K0 | 23 | 23 | 0 | 19 | 2 |
| K1 | 23 | 22 | 1 | 23 | 1 |

Every correction goes through `_decisions/<C>/CORRECTIONS.dec`, with the full record before the change and a hash after it in `per_candidate/<C>/CORRECTIONS.jsonl`. Batch files stayed as checkpointed. In all there are 252 corrections, 24 of which changed a label.

The end of the run added two sets:

- **18 consistency corrections** on reading differences listed during the run: health-check grading, the unconditional validation-package ban, the stated trade-off, the servicing-release clause, the reviewer checker, frontend test locations and the ASP.NET package check in inner layers.
- **156 A1.3 audit corrections** from a scan for MUST or MUST_NOT on knowledge-skill and private-reference text with no must-like word: 152 modality changes and 4 check-by-reference codes in M1. Each was read by hand. No label changed and every coverage status held.

153 frozen samples were challenged against the source and a counterexample. The validator found that round 1 had sampled no NON_NORMATIVE record in five candidates, so a round 2 was added for them.

## What stays unresolved

- **19 UNCERTAIN records and 4 records with an UNCERTAIN subclause.** They fall into four questions:
  1. May an approved workflow authorize destructive Git operations without an explicit request (GOV-015)? All six candidates.
  2. Is a deliberate pre-mutation cache invalidation compatible with RUN-021? M, M1, L1, K1.
  3. How far does the condition on the Swagger UI step reach? M1, L0, L1, K0.
  4. Does explicit approval in a headless run's original request allow a Reserved change? M.
- **24 future human decisions** in `FUTURE_HUMAN_DECISIONS.jsonl`. They are the questions above, plus whether a checker should honour DEP-003's explicit-request exception for floating versions (M, M1, K1).
- **21 open review items** in `ORPHAN_REVIEW_QUEUE.jsonl`, each with evidence. Most point to the questions above. The rest are prescriptive fragments that no group holds, such as output-cache metadata technique and the AAA "useful default".
- **33 LOW-confidence records and 90 flagged for review,** with reasons, in `UNCERTAIN_CLASSIFICATIONS.jsonl`.
- **33 potential overmerges** in `POTENTIAL_OVERMERGES.jsonl`. No group was split.
- **PI-012 is open:** how to read flat negatives in technique text. The affected records stay at MUST_NOT.

## Validation

| Gate | Status |
|---|---|
| `INPUT_SHA256_UNCHANGED` | PASS |
| `ALL_6402_RECORDS_EXACTLY_ONCE` | PASS |
| `ALL_1176_COVERAGE_ROWS_EXACTLY_ONCE` | PASS |
| `NO_UNDEFINED_CANONICAL_IDS` | PASS |
| `EVIDENCE_RE_READ_FROM_IMMUTABLE_FILES` | PASS |
| `NO_SILENT_DROP_OF_PROPOSALS_OR_FACETS` | PASS |
| `ORPHANS_CONFLICTS_UNRESOLVED_AND_PASS1_ISSUES_CLOSED` | PASS |
| `STEP1_MERGE_QUEUE_ACCOUNTED` | PASS |
| `CHECKPOINT_INTEGRITY` | PASS |
| `PROTOCOL_FROZEN` | PASS |
| `CALIBRATION_AGREES_OR_HAS_A_CORRECTION` | PASS |
| `SEMANTIC_CHALLENGES_RUN_AND_CLOSED` | PASS |
| `STRENGTH_TRIGGER_AND_EXCEPTIONS_RESOLVED` | PASS |
| `A1_3_AUDIT_NO_UNMARKED_MUST_ON_TECHNIQUE_TEXT` | PASS |
| `CORRECTIONS_HAVE_BEFORE_AFTER_PROVENANCE` | PASS |
| `CANDIDATE_VALIDATORS` | PASS |
| `CODEX_PASS2_NOT_CONSUMED` | PASS |
| `DELIVERABLES_PRESENT` | PASS |

To re-run:

```bash
python -B _tools/finalize.py build
python -B _tools/final_report.py
python -B _tools/finalize.py validate
```

## Files

- Per candidate: `per_candidate/<C>/` holds `CLASSIFICATIONS.jsonl`, `POLICY_COVERAGE.jsonl`, `CANDIDATE_REPORT.md`, `SEMANTIC_CHALLENGES.jsonl`, `ORPHAN_DISPOSITIONS.jsonl`, `CORRECTIONS.jsonl` and `STRENGTH_DIVERGENCES.jsonl`.
- Protocol: `CLASSIFICATION_PROTOCOL.md`, `PROTOCOL_ADDENDUM_A1.md`, `PROTOCOL_ISSUES.jsonl`, `PROTOCOL_FREEZE.json`, `CALIBRATION.jsonl`, `CALIBRATION_AGREEMENT.jsonl`.
- Aggregates: `CLASSIFICATION_SUMMARY.json`, `UNCERTAIN_CLASSIFICATIONS.jsonl`, `POTENTIAL_OVERMERGES.jsonl`, `FUTURE_HUMAN_DECISIONS.jsonl`, `ORPHAN_REVIEW_QUEUE.jsonl`, `STEP1_QUEUE_DISPOSITIONS.jsonl`, `COVERAGE_LIMITATIONS.md`, `VALIDATION_RESULT.json`.
- Reproducibility: `CHECKPOINTS/`, `_batches/`, `_decisions/`, `_tools/`, `INPUT_HASHES.json`.
