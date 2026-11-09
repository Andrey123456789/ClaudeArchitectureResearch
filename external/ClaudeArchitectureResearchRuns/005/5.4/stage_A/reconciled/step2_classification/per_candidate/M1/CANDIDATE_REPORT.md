# Candidate M1 — Step 2 classification report

Protocol `step2-v1` with Addendum A1. Mechanical validation: **PASS**. This confirms structure and traceability, not semantic accuracy (see the challenge sample below and COVERAGE_LIMITATIONS.md).

## Counts

- Records classified: 1113 (union view: 1113).
- By classification: CANONICAL_ONLY 732, CANONICAL_PLUS_DELTA 73, EXTRA_PRODUCT 134, EXTRA_WORKFLOW 52, INTERNAL_ARCHITECTURE 72, MIXED 13, NON_NORMATIVE 34, UNCERTAIN 3
- CANONICAL_ONLY by strength: EQUIVALENT 616, WEAKER_THAN_CANONICAL 116 (`WEAKER_THAN_CANONICAL` is semantic coverage without strength equivalence; it is not equivalent to the policy).
- CANONICAL_ONLY by semantic coverage: FULL 209, PARTIAL 523
- By domain: INSTRUCTION_ARCHITECTURE 72, MIXED 8, NON_NORMATIVE 34, PRODUCT_ENGINEERING 648, UNCERTAIN 3, WORKFLOW_ENFORCEMENT 348
- By oracle relation: FULLY_ENTAILED 732, NOT_APPLICABLE 106, NOT_ENTAILED 189, PARTIALLY_ENTAILED 83, UNCERTAIN 3
- By confidence: HIGH 705, LOW 5, MEDIUM 403
- Provisional records: PROVISIONAL_FACET_OVERLAY/EXTRA_PRODUCT 2, PROVISIONAL_FACET_OVERLAY/INTERNAL_ARCHITECTURE 2, PROVISIONAL_FACET_OVERLAY/NON_NORMATIVE 3, PROVISIONAL_NEW_CLAUSE/EXTRA_WORKFLOW 2, PROVISIONAL_NEW_CLAUSE/INTERNAL_ARCHITECTURE 3
- Source-quote verification: VERIFIED 1113; primary anchors: EXACT_RANGE_MATCH 1113

## Policy coverage (traceability, not compliance)

- Semantic coverage: DIRECT_EVIDENCE 196
- Strength: EQUIVALENT_EVIDENCE_PRESENT 196
- Non-DIRECT policies: none
- Policies without equal-strength evidence: none
- Strength divergences preserved for Step 3 in `STRENGTH_DIVERGENCES.jsonl`: 252 (EQUIVALENT 82, INCOMPARABLE 7, PORTION_EQUIVALENT_WITH_REMAINDER 1, STRONGER_THAN_CANONICAL 39, WEAKER_THAN_CANONICAL 123).

## Corrections

- Corrections applied: 24 on 24 records (before/after in `CORRECTIONS.jsonl`; batch files unchanged). Classification changes: 3.
- By finding: AUDIT-A1-KNOWLEDGE 20, CHALLENGE-M1-R1 2, END-OF-RUN-CONSISTENCY 2
  - `FG-M1-6d1354f485` COR-M1-0001: CANONICAL_ONLY -> EXTRA_PRODUCT. CANONICAL_ONLY did not survive the challenge: a health check that reports a static quality score is cheap and deterministic, so API-018 is satisfied while the claim is no
  - `FG-M1-db168a29a4` COR-M1-0003: CANONICAL_ONLY -> CANONICAL_PLUS_DELTA. The claim places unit and component tests in the workspace and E2E under e2e/, which DEP-024 does not state. Same reading as L0, L1, K0 and K1.
  - `FG-M1-0545a425c5` COR-M1-0004: CANONICAL_ONLY -> CANONICAL_PLUS_DELTA. The record's claim includes the servicing clause, which DEP-008 does not state; a stronger claim is never CANONICAL_ONLY (C1). FG-M1-ee2a76fc04 already reads the clause a

## Open and uncertain items

- UNCERTAIN classifications: 3; records with review_needed: 10; future human decisions: 4; potential Step-1 overmerges flagged: 0.
  - `FG-M1-57aa941363`: whether deliberate pre-mutation invalidation (cache cleared, source unchanged on failure) is 'consistent with successful underlying mutations' cannot be decided from RUN-021's text; Step-1 APPARENT_CONFLICT with FG-M1-a0
  - `FG-M1-6a3f471ef0`: whether 'clearly required by an approved workflow' counts as an explicit request under GOV-015 (permission widening vs equivalent) cannot be decided from the texts
  - `FG-M1-a876ee45ce`: Step-1 UNRESOLVED relation with FG-M1-51dccbe9d9: the condition's reach cannot be decided from the text

## Orphan and queue closure

- Items reviewed: 57 — ATTACH 39, NON_NORMATIVE 8, QUEUE 6, RESOLVED 4
  - QUEUE `PRIMARY:M1:ORPHAN:ORPHAN-M1-0114`: 'Apply the selected output-cache policy through controller or action metadata' is prescriptive technique with no group of its own.
  - QUEUE `PRIMARY:M1:ORPHAN:ORPHAN-M1-0135`: 'Expose it ... for example with a public partial class Program' is a conditional technique with no group of its own.
  - QUEUE `PRIMARY:M1:ORPHAN:ORPHAN-M1-0276`: 'Useful default structure' has a direction, so it is not plainly NN, and no group holds it. Same open item as AUG1-UR-CIS-M1-U0011.
  - QUEUE `AUG1-UR-CIS-M1-U0011`: Same open item as orphan 12: AAA as a 'useful default'.
  - QUEUE `RQ-M1-9ddc258eac`: Pre-mutation invalidation versus RUN-021 stays open: FG-M1-57aa941363 is UNCERTAIN with a FUTURE_HUMAN_DECISIONS entry.
  - QUEUE `RQ-M1-df8468f760`: The reach of the startup condition stays open: FG-M1-a876ee45ce is UNCERTAIN with a FUTURE_HUMAN_DECISIONS entry.

## Semantic challenge sample

- 23 challenged: REVISED_NEEDED 2, UPHELD 21. Resolution: NOT_NEEDED 21, RESOLVED_BY_CORRECTION 2.
- The sample is small and deterministic; it estimates defect types, not an overall accuracy rate.
  - REVISED_NEEDED `FG-M1-6d1354f485` (round 1, challenged as CANONICAL_ONLY, now EXTRA_PRODUCT): Counterexample: a health check returning a static quality score is cheap and deterministic, so API-018 is satisfied while the claim is not. Not entailed. [RESOLVED_BY_CORRECTION COR-M1-0001]
  - REVISED_NEEDED `FG-M1-39e2cd090f` (round 1, challenged as MIXED, now MIXED): The subclauses dropped 'enabling or disabling the optional frontend slot', which the claim names and ARC-020 does not cover. [RESOLVED_BY_CORRECTION COR-M1-0002]

## Validation

- No errors: keys, types, policy IDs, evidence, source-quote verification, required fields, strength resolutions, triggers/exceptions, 196 coverage rows, orphan closure, correction history, failed-challenge guard.
