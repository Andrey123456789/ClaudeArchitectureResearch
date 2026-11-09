# Candidate M — Step 2 classification report

Protocol `step2-v1` with Addendum A1. Mechanical validation: **PASS**. This confirms structure and traceability, not semantic accuracy (see the challenge sample below and COVERAGE_LIMITATIONS.md).

## Counts

- Records classified: 1003 (union view: 1003).
- By classification: CANONICAL_ONLY 699, CANONICAL_PLUS_DELTA 65, EXTRA_PRODUCT 120, EXTRA_WORKFLOW 46, INTERNAL_ARCHITECTURE 47, MIXED 6, NON_NORMATIVE 17, UNCERTAIN 3
- CANONICAL_ONLY by strength: EQUIVALENT 611, WEAKER_THAN_CANONICAL 88 (`WEAKER_THAN_CANONICAL` is semantic coverage without strength equivalence; it is not equivalent to the policy).
- CANONICAL_ONLY by semantic coverage: FULL 365, PARTIAL 334
- By domain: INSTRUCTION_ARCHITECTURE 47, MIXED 6, NON_NORMATIVE 17, PRODUCT_ENGINEERING 601, UNCERTAIN 3, WORKFLOW_ENFORCEMENT 329
- By oracle relation: FULLY_ENTAILED 699, NOT_APPLICABLE 64, NOT_ENTAILED 168, PARTIALLY_ENTAILED 69, UNCERTAIN 3
- By confidence: HIGH 584, LOW 4, MEDIUM 415
- Provisional records: PROVISIONAL_FACET_OVERLAY/EXTRA_PRODUCT 1, PROVISIONAL_FACET_OVERLAY/EXTRA_WORKFLOW 1, PROVISIONAL_FACET_OVERLAY/INTERNAL_ARCHITECTURE 3, PROVISIONAL_FACET_OVERLAY/NON_NORMATIVE 2, PROVISIONAL_NEW_CLAUSE/INTERNAL_ARCHITECTURE 1
- Source-quote verification: VERIFIED 1003; primary anchors: EXACT_RANGE_MATCH 1003

## Policy coverage (traceability, not compliance)

- Semantic coverage: DIRECT_EVIDENCE 196
- Strength: EQUIVALENT_EVIDENCE_PRESENT 196
- Non-DIRECT policies: none
- Policies without equal-strength evidence: none
- Strength divergences preserved for Step 3 in `STRENGTH_DIVERGENCES.jsonl`: 212 (EQUIVALENT 84, INCOMPARABLE 4, PORTION_EQUIVALENT_WITH_REMAINDER 4, STRONGER_THAN_CANONICAL 28, WEAKER_THAN_CANONICAL 92).

## Corrections

- Corrections applied: 145 on 141 records (before/after in `CORRECTIONS.jsonl`; batch files unchanged). Classification changes: 12.
- By finding: AUDIT-A1-KNOWLEDGE 67, AUDIT-A1-STRENGTH 27, AUDIT-A1-TRIGGER 42, END-OF-RUN-CONSISTENCY 6, REVIEW-M-1 1, REVIEW-M-2 1, REVIEW-M-3 1
  - `FG-M-22cae42396` COR-M-0001: CANONICAL_ONLY -> MIXED. Round-1 challenge marked REVISED_NEEDED while the record stayed CANONICAL_ONLY/HIGH: the second source sentence is an independently testable positive requirement that TST
  - `FG-M-cf7afce3d7` COR-M-0002: CANONICAL_ONLY -> CANONICAL_PLUS_DELTA. Same defect class as FG-M-22cae42396 found while checking it: 'Test the risks that matter' is a positive test-selection statement GOV-012 does not entail.
  - `FG-M-d0b6a09cce` COR-M-0004: NON_NORMATIVE -> EXTRA_PRODUCT. 'Often preferable' states a directional preference between deployment options, followed by the command to use; it is not an option list, so NON_NORMATIVE under C5 was wro
  - `FG-M-261252b78a` COR-M-0013: CANONICAL_ONLY -> CANONICAL_PLUS_DELTA. Prohibition is stronger than DEP-026's DEFAULT, so CANONICAL_ONLY was not admissible.
  - `FG-M-3f8690d58a` COR-M-0014: CANONICAL_ONLY -> EXTRA_PRODUCT. GOV-012 concerns abstractions and architectural complexity, not documentation comments; the entailment claim does not hold.
  - `FG-M-aee26f0a5a` COR-M-0015: CANONICAL_ONLY -> EXTRA_PRODUCT. Document partitioning is not entailed by GOV-012 or API-016 (oracle EXC-008 treats it as tooling technique), and the MUST_NOT came from the reported label.
  - `FG-M-20991027fd` COR-M-0073: CANONICAL_ONLY -> EXTRA_PRODUCT. CANONICAL_ONLY does not hold: a health check reporting a static quality score is cheap and deterministic, so API-018 is satisfied while the claim is not. Same reading as 
  - `FG-M-cf162a91bf` COR-M-0074: CANONICAL_ONLY -> CANONICAL_PLUS_DELTA. This sentence has no 'concrete requirement' exception, unlike FG-M-567f30944c. DEP-010 names the library and DEP-004 asks for a deprecation check; neither bans the packag
  - `FG-M-e87f6b3e65` COR-M-0075: CANONICAL_ONLY -> CANONICAL_PLUS_DELTA. Stating the trade-off is a reporting duty on a DEFAULT deviation (C7), which CANONICAL_ONLY hid. Same reading as FG-M1-99049a9bc9, FG-L0-2eaedd2632, FG-L1-1d55c67f9b, FG-
  - `FG-M-aa674642ec` COR-M-0076: CANONICAL_ONLY -> CANONICAL_PLUS_DELTA. The claim is only the servicing clause, which DEP-008 does not state: a project on an older .NET 10 servicing release satisfies DEP-008. FG-M-f830eb5293 already reads it 
  - `FG-M-901f891529` COR-M-0077: INTERNAL_ARCHITECTURE -> CANONICAL_ONLY. The check enforces the reviewer's read-only tools and its delegation to code-review, which is what WF-010 states. Same reading as FG-M1-7e963eba7a, FG-L0-db0df1dfcb and F
  - `FG-M-0e415dbede` COR-M-0078: CANONICAL_ONLY -> CANONICAL_PLUS_DELTA. The claim places frontend tests inside the workspace, which DEP-024 does not state. Same reading as L0, L1, K0 and K1, and as COR on FG-M1-db168a29a4.

## Open and uncertain items

- UNCERTAIN classifications: 3; records with review_needed: 6; future human decisions: 4; potential Step-1 overmerges flagged: 0.
  - `FG-M-fd01a5254d`: whether deliberate pre-mutation invalidation (cache cleared, source unchanged on failure) is 'consistent with successful underlying mutations' cannot be decided from RUN-021's text; Step-1 APPARENT_CONFLICT with FG-M-5ed
  - `FG-M-58264ccd7d`: whether 'clearly required by an approved workflow' counts as an explicit request under GOV-015 (permission widening vs equivalent) cannot be decided from the texts
  - `FG-M-35f716b5eb`: the two sentences conflict for pre-approved Reserved changes in headless runs; the source does not resolve precedence (Step-1 UNRESOLVED queue item)

## Orphan and queue closure

- Items reviewed: 79 — ATTACH 51, NON_NORMATIVE 19, QUEUE 5, RESOLVED 4
  - QUEUE `PRIMARY:M:ORPHAN:ORPHAN-M-0092`: caching SKILL.md:111-112 'apply the selected output-cache policy through controller or action metadata' is prescriptive technique (DEFAULT under C5) not represented by any union group; potentially nor
  - QUEUE `AUG1-UR-CIS-M-0010-1`: Pass-1 methodology item: httpclient-factory SKILL.md:17-18 conditional reference-loading route ('for retries ... read references/resilience.md') is not represented by a union group; under C4 it would 
  - QUEUE `RQ-M-aeb3a36efd`: Cache pre-mutation invalidation vs RUN-021 remains open: FG-M-fd01a5254d is UNCERTAIN with a FUTURE_HUMAN_DECISIONS entry.
  - QUEUE `RQ-M-bc9b0e441b`: Headless-run approval ambiguity remains open: FG-M-35f716b5eb UNCERTAIN with a FUTURE_HUMAN_DECISIONS entry; FG-M-2b1be76983/FG-M-604133c8ba classified CANONICAL_PLUS_DELTA.
  - QUEUE `RQ-M-bff9a72ad8`: Same headless approval tension as item 78 (explicit instruction counts as approval vs never decide Reserved in headless runs).

## Semantic challenge sample

- 38 challenged: REVISED_NEEDED 1, UPHELD 37. Resolution: NOT_NEEDED 33, RESOLVED_BY_CORRECTION 1, UPHELD_WITH_FIELD_CORRECTION 4.
- The sample is small and deterministic; it estimates defect types, not an overall accuracy rate.
  - REVISED_NEEDED `FG-M-22cae42396` (round 1, challenged as CANONICAL_ONLY, now MIXED): dotnet-testing SKILL.md:237-238 also says 'Prioritize meaningful behavior, important edge cases, and risky integrations'; a test plan covering only happy paths without ch [RESOLVED_BY_CORRECTION COR-M-0001]

## Validation

- No errors: keys, types, policy IDs, evidence, source-quote verification, required fields, strength resolutions, triggers/exceptions, 196 coverage rows, orphan closure, correction history, failed-challenge guard.
