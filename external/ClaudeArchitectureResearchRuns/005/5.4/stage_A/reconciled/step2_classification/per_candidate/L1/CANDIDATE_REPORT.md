# Candidate L1 — Step 2 classification report

Protocol `step2-v1` with Addendum A1. Mechanical validation: **PASS**. This confirms structure and traceability, not semantic accuracy (see the challenge sample below and COVERAGE_LIMITATIONS.md).

## Counts

- Records classified: 1037 (union view: 1037).
- By classification: CANONICAL_ONLY 674, CANONICAL_PLUS_DELTA 80, EXTRA_PRODUCT 124, EXTRA_WORKFLOW 57, INTERNAL_ARCHITECTURE 61, MIXED 23, NON_NORMATIVE 15, UNCERTAIN 3
- CANONICAL_ONLY by strength: EQUIVALENT 545, WEAKER_THAN_CANONICAL 129 (`WEAKER_THAN_CANONICAL` is semantic coverage without strength equivalence; it is not equivalent to the policy).
- CANONICAL_ONLY by semantic coverage: FULL 196, PARTIAL 478
- By domain: INSTRUCTION_ARCHITECTURE 61, MIXED 9, NON_NORMATIVE 15, PRODUCT_ENGINEERING 597, UNCERTAIN 3, WORKFLOW_ENFORCEMENT 352
- By oracle relation: FULLY_ENTAILED 675, NOT_APPLICABLE 76, NOT_ENTAILED 184, PARTIALLY_ENTAILED 99, UNCERTAIN 3
- By confidence: HIGH 735, LOW 6, MEDIUM 296
- Provisional records: PROVISIONAL_FACET_OVERLAY/EXTRA_WORKFLOW 1, PROVISIONAL_FACET_OVERLAY/INTERNAL_ARCHITECTURE 2, PROVISIONAL_FACET_OVERLAY/NON_NORMATIVE 1, PROVISIONAL_NEW_CLAUSE/EXTRA_WORKFLOW 4, PROVISIONAL_NEW_CLAUSE/INTERNAL_ARCHITECTURE 1
- Source-quote verification: VERIFIED 1037; primary anchors: EXACT_RANGE_MATCH 1037

## Policy coverage (traceability, not compliance)

- Semantic coverage: DIRECT_EVIDENCE 196
- Strength: EQUIVALENT_EVIDENCE_PRESENT 196
- Non-DIRECT policies: none
- Policies without equal-strength evidence: none
- Strength divergences preserved for Step 3 in `STRENGTH_DIVERGENCES.jsonl`: 243 (EQUIVALENT 57, INCOMPARABLE 9, PORTION_EQUIVALENT_WITH_REMAINDER 3, STRONGER_THAN_CANONICAL 35, WEAKER_THAN_CANONICAL 139).

## Corrections

- Corrections applied: 21 on 21 records (before/after in `CORRECTIONS.jsonl`; batch files unchanged). Classification changes: 4.
- By finding: AUDIT-A1-KNOWLEDGE 17, END-OF-RUN-CONSISTENCY 4
  - `FG-L1-14607d9618` COR-L1-0001: CANONICAL_ONLY -> CANONICAL_PLUS_DELTA. The record's claim includes the servicing clause, which DEP-008 does not state; a stronger claim is never CANONICAL_ONLY (C1). Same reading as FG-M-f830eb5293 and FG-M1-e
  - `FG-L1-21ae6647aa` COR-L1-0002: CANONICAL_ONLY -> CANONICAL_PLUS_DELTA. ARC-008 names transport types, while the check rejects the framework and packages in Application whatever they are used for. C3 keeps CANONICAL_ONLY only for an identical
  - `FG-L1-591aa8deca` COR-L1-0003: CANONICAL_ONLY -> CANONICAL_PLUS_DELTA. Same check as FG-L1-21ae6647aa.
  - `FG-L1-f0cf2d0f61` COR-L1-0004: CANONICAL_ONLY -> CANONICAL_PLUS_DELTA. Same check as FG-L1-21ae6647aa; the prefix match is what reaches beyond transport types.

## Open and uncertain items

- UNCERTAIN classifications: 3; records with review_needed: 17; future human decisions: 3; potential Step-1 overmerges flagged: 0.
  - `FG-L1-37cd50d53e`: Step-1 conflict relation with FG-L1-bfdc2be3cc: a deliberate pre-mutation invalidation may or may not be 'consistent' under RUN-021
  - `FG-L1-3691accd41`: Step-1 conflict relation with FG-L1-736f7de527
  - `FG-L1-de692b7c3d`: Step-1 UNRESOLVED relation with FG-L1-a48ca2a20d: the condition's reach cannot be decided from the text

## Orphan and queue closure

- Items reviewed: 33 — ATTACH 20, NON_NORMATIVE 6, QUEUE 3, RESOLVED 4
  - QUEUE `RQ-L1-371cd81bbc`: Whether a deliberate pre-mutation invalidation fits RUN-021 stays open at FG-L1-37cd50d53e with a future human decision.
  - QUEUE `RQ-L1-c7201d2ee6`: Whether the conditions also cover the Swagger step stays open at FG-L1-de692b7c3d with a future human decision.
  - QUEUE `RQ-L1-e9fc5f03f5`: How non-rewritable branches combine with the approved-workflow allowance stays open at FG-L1-3691accd41 with a future human decision.

## Semantic challenge sample

- 23 challenged: UPHELD 23. Resolution: NOT_NEEDED 23.
- The sample is small and deterministic; it estimates defect types, not an overall accuracy rate.

## Validation

- No errors: keys, types, policy IDs, evidence, source-quote verification, required fields, strength resolutions, triggers/exceptions, 196 coverage rows, orphan closure, correction history, failed-challenge guard.
