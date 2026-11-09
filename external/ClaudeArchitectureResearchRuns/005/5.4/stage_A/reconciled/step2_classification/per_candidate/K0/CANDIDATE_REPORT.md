# Candidate K0 — Step 2 classification report

Protocol `step2-v1` with Addendum A1. Mechanical validation: **PASS**. This confirms structure and traceability, not semantic accuracy (see the challenge sample below and COVERAGE_LIMITATIONS.md).

## Counts

- Records classified: 1077 (union view: 1077).
- By classification: CANONICAL_ONLY 687, CANONICAL_PLUS_DELTA 71, EXTRA_PRODUCT 129, EXTRA_WORKFLOW 59, INTERNAL_ARCHITECTURE 70, MIXED 30, NON_NORMATIVE 27, UNCERTAIN 4
- CANONICAL_ONLY by strength: EQUIVALENT 559, WEAKER_THAN_CANONICAL 128 (`WEAKER_THAN_CANONICAL` is semantic coverage without strength equivalence; it is not equivalent to the policy).
- CANONICAL_ONLY by semantic coverage: FULL 179, PARTIAL 508
- By domain: INSTRUCTION_ARCHITECTURE 70, MIXED 10, NON_NORMATIVE 27, PRODUCT_ENGINEERING 599, UNCERTAIN 4, WORKFLOW_ENFORCEMENT 367
- By oracle relation: FULLY_ENTAILED 687, NOT_APPLICABLE 97, NOT_ENTAILED 192, PARTIALLY_ENTAILED 97, UNCERTAIN 4
- By confidence: HIGH 746, LOW 7, MEDIUM 324
- Provisional records: PROVISIONAL_FACET_OVERLAY/EXTRA_PRODUCT 1, PROVISIONAL_FACET_OVERLAY/EXTRA_WORKFLOW 1, PROVISIONAL_FACET_OVERLAY/INTERNAL_ARCHITECTURE 1, PROVISIONAL_FACET_OVERLAY/NON_NORMATIVE 4, PROVISIONAL_NEW_CLAUSE/EXTRA_WORKFLOW 5, PROVISIONAL_NEW_CLAUSE/INTERNAL_ARCHITECTURE 3
- Source-quote verification: VERIFIED 1077; primary anchors: EXACT_RANGE_MATCH 1077

## Policy coverage (traceability, not compliance)

- Semantic coverage: DIRECT_EVIDENCE 196
- Strength: EQUIVALENT_EVIDENCE_PRESENT 194, STRONGER_AND_WEAKER_EVIDENCE 2
- Non-DIRECT policies: none
- Policies without equal-strength evidence: API-014 (STRONGER_AND_WEAKER_EVIDENCE), API-019 (STRONGER_AND_WEAKER_EVIDENCE)
- Strength divergences preserved for Step 3 in `STRENGTH_DIVERGENCES.jsonl`: 255 (EQUIVALENT 77, INCOMPARABLE 7, PORTION_EQUIVALENT_WITH_REMAINDER 1, STRONGER_THAN_CANONICAL 31, WEAKER_THAN_CANONICAL 139).

## Corrections

- Corrections applied: 19 on 19 records (before/after in `CORRECTIONS.jsonl`; batch files unchanged). Classification changes: 2.
- By finding: AUDIT-A1-KNOWLEDGE 15, END-OF-RUN-CONSISTENCY 2, ORPHAN-CLOSE-K0 2
  - `FG-K0-4a3249f563` COR-K0-0003: CANONICAL_ONLY -> CANONICAL_PLUS_DELTA. The record's claim includes the servicing clause, which DEP-008 does not state; a stronger claim is never CANONICAL_ONLY (C1). Same reading as FG-M-f830eb5293 and FG-M1-e
  - `FG-K0-9e37b30e93` COR-K0-0004: CANONICAL_ONLY -> CANONICAL_PLUS_DELTA. Same clause as FG-K0-4a3249f563 inside the register's defaults.

## Open and uncertain items

- UNCERTAIN classifications: 4; records with review_needed: 24; future human decisions: 4; potential Step-1 overmerges flagged: 1.
  - `FG-K0-1744942b6f`: Step-1 conflict relation with FG-K0-be5767708f
  - `FG-K0-70ec2ad24c`: Step-1 conflict relation with FG-K0-be5767708f
  - `FG-K0-e58b79e6e7`: the reported MUST holds only for the explicit-request part; the allowance is what stays open
  - `FG-K0-47988fe869`: FG-K0-9522259b92 reads the same list; the condition's reach cannot be decided from the text

## Orphan and queue closure

- Items reviewed: 40 — ATTACH 22, NON_NORMATIVE 9, QUEUE 2, RESOLVED 7
  - QUEUE `RQ-K0-498dda5045`: How non-rewritable branches combine with the explicit-request route stays open between FG-K0-93bf76a2fb and FG-K0-6a618a21a6; the related approved-workflow allowance stays open at FG-K0-70ec2ad24c wit
  - QUEUE `RQ-K0-fcaa300fdb`: Whether an approved workflow may authorize destructive Git operations stays open at FG-K0-70ec2ad24c, FG-K0-1744942b6f and FG-K0-e58b79e6e7 with a future human decision.

## Semantic challenge sample

- 23 challenged: UPHELD 23. Resolution: NOT_NEEDED 23.
- The sample is small and deterministic; it estimates defect types, not an overall accuracy rate.

## Validation

- No errors: keys, types, policy IDs, evidence, source-quote verification, required fields, strength resolutions, triggers/exceptions, 196 coverage rows, orphan closure, correction history, failed-challenge guard.
