# Candidate K1 — Step 2 classification report

Protocol `step2-v1` with Addendum A1. Mechanical validation: **PASS**. This confirms structure and traceability, not semantic accuracy (see the challenge sample below and COVERAGE_LIMITATIONS.md).

## Counts

- Records classified: 1200 (union view: 1200).
- By classification: CANONICAL_ONLY 741, CANONICAL_PLUS_DELTA 87, EXTRA_PRODUCT 145, EXTRA_WORKFLOW 60, INTERNAL_ARCHITECTURE 91, MIXED 40, NON_NORMATIVE 32, UNCERTAIN 4
- CANONICAL_ONLY by strength: EQUIVALENT 608, WEAKER_THAN_CANONICAL 133 (`WEAKER_THAN_CANONICAL` is semantic coverage without strength equivalence; it is not equivalent to the policy).
- CANONICAL_ONLY by semantic coverage: FULL 185, PARTIAL 556
- By domain: INSTRUCTION_ARCHITECTURE 91, MIXED 15, NON_NORMATIVE 32, PRODUCT_ENGINEERING 668, UNCERTAIN 4, WORKFLOW_ENFORCEMENT 390
- By oracle relation: FULLY_ENTAILED 742, NOT_APPLICABLE 123, NOT_ENTAILED 212, PARTIALLY_ENTAILED 119, UNCERTAIN 4
- By confidence: HIGH 864, LOW 6, MEDIUM 330
- Provisional records: PROVISIONAL_NEW_CLAUSE/EXTRA_WORKFLOW 4
- Source-quote verification: VERIFIED 1200; primary anchors: EXACT_RANGE_MATCH 1200

## Policy coverage (traceability, not compliance)

- Semantic coverage: DIRECT_EVIDENCE 196
- Strength: EQUIVALENT_EVIDENCE_PRESENT 193, STRONGER_AND_WEAKER_EVIDENCE 3
- Non-DIRECT policies: none
- Policies without equal-strength evidence: GOV-007 (STRONGER_AND_WEAKER_EVIDENCE), API-014 (STRONGER_AND_WEAKER_EVIDENCE), API-019 (STRONGER_AND_WEAKER_EVIDENCE)
- Strength divergences preserved for Step 3 in `STRENGTH_DIVERGENCES.jsonl`: 282 (EQUIVALENT 79, INCOMPARABLE 7, PORTION_EQUIVALENT_WITH_REMAINDER 3, STRONGER_THAN_CANONICAL 45, WEAKER_THAN_CANONICAL 148).

## Corrections

- Corrections applied: 23 on 23 records (before/after in `CORRECTIONS.jsonl`; batch files unchanged). Classification changes: 1.
- By finding: AUDIT-A1-KNOWLEDGE 19, CHALLENGE-K1-R1 1, END-OF-RUN-CONSISTENCY 3
  - `FG-K1-d559be810c` COR-K1-0001: CANONICAL_ONLY -> EXTRA_PRODUCT. CANONICAL_ONLY did not survive the challenge: a useful Domain.Tests project for a simple Domain is not speculative under ARC-027, and FG-K1-0e4de41164 already reads the s

## Open and uncertain items

- UNCERTAIN classifications: 4; records with review_needed: 24; future human decisions: 7; potential Step-1 overmerges flagged: 0.
  - `FG-K1-a2b893ac20`: RUN-021 says 'only in a way consistent with successful underlying mutations'; the source allows earlier invalidation when the workflow accepts it
  - `FG-K1-15595975aa`: Step-1 conflict relation with FG-K1-351c8790c0
  - `FG-K1-86b870941f`: the reported MUST holds only for the explicit-request part; the allowance is what stays open
  - `FG-K1-c66cb200ef`: Step-1 conflict relation with FG-K1-351c8790c0

## Orphan and queue closure

- Items reviewed: 42 — ATTACH 27, NON_NORMATIVE 3, QUEUE 2, RESOLVED 10
  - QUEUE `RQ-K1-e08f0bf3c9`: Whether an approved workflow may authorize destructive Git operations stays open at FG-K1-15595975aa, FG-K1-86b870941f and FG-K1-c66cb200ef with a future human decision.
  - QUEUE `RQ-K1-ed63d4fc29`: How non-rewritable branches combine with the explicit-request route stays open between FG-K1-728e7fa972 and FG-K1-35d0c70586; the related approved-workflow allowance stays open at FG-K1-15595975aa wit

## Semantic challenge sample

- 23 challenged: REVISED_NEEDED 1, UPHELD 22. Resolution: NOT_NEEDED 22, RESOLVED_BY_CORRECTION 1.
- The sample is small and deterministic; it estimates defect types, not an overall accuracy rate.
  - REVISED_NEEDED `FG-K1-d559be810c` (round 1, challenged as CANONICAL_ONLY, now EXTRA_PRODUCT): 'A simple Domain needs no dedicated test project' is not entailed: a useful Domain.Tests project is not speculative under ARC-027. FG-K1-0e4de41164 already reads the same [RESOLVED_BY_CORRECTION COR-K1-0001]

## Validation

- No errors: keys, types, policy IDs, evidence, source-quote verification, required fields, strength resolutions, triggers/exceptions, 196 coverage rows, orphan closure, correction history, failed-challenge guard.
