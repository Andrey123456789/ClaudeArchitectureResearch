# Candidate L0 — Step 2 classification report

Protocol `step2-v1` with Addendum A1. Mechanical validation: **PASS**. This confirms structure and traceability, not semantic accuracy (see the challenge sample below and COVERAGE_LIMITATIONS.md).

## Counts

- Records classified: 972 (union view: 972).
- By classification: CANONICAL_ONLY 647, CANONICAL_PLUS_DELTA 62, EXTRA_PRODUCT 119, EXTRA_WORKFLOW 45, INTERNAL_ARCHITECTURE 49, MIXED 23, NON_NORMATIVE 25, UNCERTAIN 2
- CANONICAL_ONLY by strength: EQUIVALENT 538, WEAKER_THAN_CANONICAL 109 (`WEAKER_THAN_CANONICAL` is semantic coverage without strength equivalence; it is not equivalent to the policy).
- CANONICAL_ONLY by semantic coverage: FULL 190, PARTIAL 457
- By domain: INSTRUCTION_ARCHITECTURE 49, MIXED 11, NON_NORMATIVE 25, PRODUCT_ENGINEERING 566, UNCERTAIN 2, WORKFLOW_ENFORCEMENT 319
- By oracle relation: FULLY_ENTAILED 647, NOT_APPLICABLE 74, NOT_ENTAILED 169, PARTIALLY_ENTAILED 80, UNCERTAIN 2
- By confidence: HIGH 612, LOW 5, MEDIUM 355
- Provisional records: PROVISIONAL_FACET_OVERLAY/EXTRA_PRODUCT 1, PROVISIONAL_FACET_OVERLAY/INTERNAL_ARCHITECTURE 3, PROVISIONAL_NEW_CLAUSE/EXTRA_WORKFLOW 2, PROVISIONAL_NEW_CLAUSE/INTERNAL_ARCHITECTURE 1
- Source-quote verification: VERIFIED 972; primary anchors: EXACT_RANGE_MATCH 972

## Policy coverage (traceability, not compliance)

- Semantic coverage: DIRECT_EVIDENCE 196
- Strength: EQUIVALENT_EVIDENCE_PRESENT 196
- Non-DIRECT policies: none
- Policies without equal-strength evidence: none
- Strength divergences preserved for Step 3 in `STRENGTH_DIVERGENCES.jsonl`: 231 (EQUIVALENT 66, INCOMPARABLE 12, STRONGER_THAN_CANONICAL 31, WEAKER_THAN_CANONICAL 122).

## Corrections

- Corrections applied: 20 on 20 records (before/after in `CORRECTIONS.jsonl`; batch files unchanged). Classification changes: 2.
- By finding: AUDIT-A1-KNOWLEDGE 18, CHALLENGE-L0-R1 1, END-OF-RUN-CONSISTENCY 1
  - `FG-L0-7650a991ec` COR-L0-0001: EXTRA_PRODUCT -> NON_NORMATIVE. EXTRA_PRODUCT did not survive the challenge: WebApplicationFactory<Program> needs Program accessible and 'for example' leaves the form open, so the scenario does not dist
  - `FG-L0-f8b039b8cf` COR-L0-0002: CANONICAL_ONLY -> CANONICAL_PLUS_DELTA. The record's claim includes the servicing clause, which DEP-008 does not state; a stronger claim is never CANONICAL_ONLY (C1). Same reading as FG-M-f830eb5293 and FG-M1-e

## Open and uncertain items

- UNCERTAIN classifications: 2; records with review_needed: 9; future human decisions: 2; potential Step-1 overmerges flagged: 0.
  - `FG-L0-6fde2a7a8f`: whether 'clearly required by an approved workflow' counts as an explicit request under GOV-015 (permission widening vs equivalent) cannot be decided from the texts
  - `FG-L0-084aeff176`: Step-1 UNRESOLVED relation with FG-L0-ad2b418693: the condition's reach cannot be decided from the text

## Orphan and queue closure

- Items reviewed: 36 — ATTACH 22, NON_NORMATIVE 6, QUEUE 3, RESOLVED 5
  - QUEUE `PRIMARY:L0:ORPHAN:ORPHAN-L0-0230`: 'Also review production debug flags, certificate-validation bypass, insecure URLs, verbose production errors and committed .env files' is a scan-layer checklist imperative (EXC-015) with no group of i
  - QUEUE `RQ-L0-95acff3859`: Whether the startup condition also covers the Swagger step stays open at FG-L0-084aeff176 with a future human decision.
  - QUEUE `RQ-L0-dc2b0aef9c`: The 'approved workflow' allowance stays open at FG-L0-6fde2a7a8f with a future human decision.

## Semantic challenge sample

- 23 challenged: REVISED_NEEDED 1, UPHELD 22. Resolution: NOT_NEEDED 22, RESOLVED_BY_CORRECTION 1.
- The sample is small and deterministic; it estimates defect types, not an overall accuracy rate.
  - REVISED_NEEDED `FG-L0-7650a991ec` (round 1, challenged as EXTRA_PRODUCT, now NON_NORMATIVE): The scenario does not distinguish. A test using WebApplicationFactory<Program> needs Program accessible, and 'for example' leaves the form open, so any behavior meeting T [RESOLVED_BY_CORRECTION COR-L0-0001]

## Validation

- No errors: keys, types, policy IDs, evidence, source-quote verification, required fields, strength resolutions, triggers/exceptions, 196 coverage rows, orphan closure, correction history, failed-challenge guard.
