# Experiment 005 / Phase 5.4 / Stage A / Step 2 — Independent Review of Submitted Snapshot

Date: 2026-11-02. Input: `step2_classification.zip` (submitted snapshot). Reviewer: independent structural replication and targeted evidence-based semantic challenge.

## Verdict

**PARTIAL / STRUCTURAL PASS FOR M / SEMANTIC CORRECTIONS REQUIRED / NOT READY FOR STEP 3.**

The archive contains completed classification outputs for **M only** (1,003 records of a 6,402-record augmented union, 15.67%). There are no full-run `CLASSIFICATIONS.jsonl` or candidate checkpoints for M1, L0, L1, K0, K1. This is not a completed Step 2 package. The snapshot alone does not reveal whether Claude was still running elsewhere.

## Independently replicated checks

- Retrieved the immutable inputs and Step-1 union from the previously submitted `5.4(1).zip`, the augmented union from `step1_union_augmented_pass1.zip`, and reconstructed the run environment.
- `python -B _tools/preflight.py --verify`: **manifest rows 484, manifest mismatches 0, hashed input files 505, changed 0**.
- Augmented union: 6,402 input records, distributed M 1,003; M1 1,113; L0 972; L1 1,037; K0 1,077; K1 1,200.
- M: 1,003 unique output keys, exactly matching the 1,003 M input keys; type breakdown 995 ORIGINAL_GROUP, 1 PROVISIONAL_NEW_CLAUSE, 7 PROVISIONAL_FACET_OVERLAY.
- All 20 M batch-checkpoint SHA-256 hashes match both compiled batch outputs and corresponding decision files. Reconstructed combined batch records match `CLASSIFICATIONS.jsonl` in exact order and content. All five M candidate-level checkpoint SHA-256 hashes matched the submitted outputs.
- Re-ran `python -B _tools/candidate.py M report` in a separate analysis copy: **PASS, 0 structural errors**.
- All 196 M policy coverage entries exist and are marked DIRECT_EVIDENCE; this denotes traceability **not** policy compliance or equivalence.
- Checked 2,966 source occurrence references independently against immutable file ranges and `SOURCE_OCCURRENCES.jsonl`: exact quote matches; 0 mismatches. Eight remaining referenced ranges are outside the occurrence index. One such reference (`AUG1-NC-CIS-M-0007-a`) has null `location_status`; the file/range exists but its quote-verification provenance should be explicitly recorded.
- Calibration has 38 records across all six candidates; the protocol freeze exists. Five calibration/protocol issues remain OPEN_FOR_HUMAN_REVIEW.

## M classification outcomes

| Classification | Count |
|---|---:|
| CANONICAL_ONLY | 708 |
| CANONICAL_PLUS_DELTA | 59 |
| EXTRA_PRODUCT | 116 |
| EXTRA_WORKFLOW | 46 |
| INTERNAL_ARCHITECTURE | 48 |
| MIXED | 5 |
| NON_NORMATIVE | 18 |
| UNCERTAIN | 3 |
| **Total** | **1,003** |

There are 6 `review_needed` records, 4 `future_human_decision` records, 5 orphan dispositions remaining QUEUE among 79 reviewed orphan/queue items, and 18 challenged records of which **17 UPHELD and 1 REVISED_NEEDED**.

## Actionable semantic defects / review targets

1. **Confirmed unresolved failed challenge — `FG-M-22cae42396`.** M `dotnet-testing/SKILL.md:237–238` states both that coverage is diagnostic and that tests should prioritize meaningful behavior, important edge cases and risky integrations. Canonical TST-011 only prohibits low-value tests generated to chase coverage. The candidate's positive prioritization clause is not logically entailed. Claude's own `SEMANTIC_CHALLENGES.jsonl` marks this classification `REVISED_NEEDED`, yet `CLASSIFICATIONS.jsonl` still labels it `CANONICAL_ONLY`, `FULLY_ENTAILED`, `HIGH`, `review_needed=false`. Resolve it in an explicitly logged correction (likely split into canonical and added normative portions); then refresh batch, candidate outputs and checkpoint hashes. Do not call M semantically accepted while the failed challenge is outstanding.
2. **Missing reported trigger — `FG-M-1c4fc44b5e`.** The primary source `ci-cd/SKILL.md:148–150` explicitly conditions build-once/promote preference on the deployment model supporting artifact promotion. The record says `trigger=UNKNOWN_NOT_REPORTED`, and its own challenged note acknowledges this field gap. Add the source-backed condition; retain the provisional assessment until verified.
3. **Plausible false NON_NORMATIVE — `FG-M-d0b6a09cce`.** `ef-core/SKILL.md:387–389` says generated idempotent migration scripts are *often preferable* for controlled production deployment. The fixed rubric includes preference as potentially normative; Claude labelled this `NON_NORMATIVE`. Rechallenge the meaning, modality, scope and whether this is conditional guidance rather than an inert example. The evidence alone does not settle the proper category without context; record a justification if NON_NORMATIVE is retained.
4. **Protocol issue `PI-001` / C1.** In M, 32 records are labeled `CANONICAL_ONLY` while `strength_vs_canonical=WEAKER`. The task defines CANONICAL_ONLY as same strength; the protocol explicitly provides a different operational interpretation and flags this for review. Resolve or document a formal controlled qualification, including the distinction between logical entailment of a weaker statement and sufficient policy coverage; do not silently present all CANONICAL_ONLY entries as same-strength parity.
5. **Protocol issue `PI-002` / C7.** Oracle `DEFAULT` has unspecified deviation-reporting semantics. The protocol records the issue and interim classification. This remains a cross-candidate methodological uncertainty important before strictness comparison.
6. **Evidence/provenance auditability.** 50 M classification triggers contain `UNKNOWN_NOT_REPORTED` and 49 exceptions do likewise. These are not automatically defects (some source records genuinely omit conditions), but additional review is warranted for source passages whose triggers or exceptions are explicit, especially the 11 EXTRA_PRODUCT records with unknown triggers. The validator checks file existence and required fields, not source-backed semantic correctness.

## Recommended disposition

Continue the **same Claude Code Step 2 session**; preserve immutable prior-stage inputs and the frozen protocol. Before producing final Step 2, fix the known failed challenge, the explicit trigger omission, the questioned preference classification, and the relevant methodological notes; log any rebuild and revalidate M. Then finish M1, L0, L1, K0 and K1 with the same rubric and checkpoint scheme. Final Step 2 acceptance requires all 6,402 records exactly once, all 1,176 policy coverage entries, candidate reports, unresolved queues, complete SHA-256 validation, and final summary/report. The five documented protocol issues and source-dependent uncertainties must not be silently represented as settled. No modifications to candidate templates and no Step 3 execution are authorized in this step.

### Scope and limitations

This independent review replicated the structural gate, full occurrence-backed evidence location matching for M, and targeted semantic challenges. It did **not** independently re-adjudicate the semantic truth of all 1,003 M classifications, nor classify the remaining 5,399 records. The results do not establish full semantic accuracy.
