# Independent review — Experiment 005, Phase 5.4, Stage A / Step 2 (final archive)

**Review date:** 2026-11-03.  
**Reviewed submission:** `step2_classification(1).zip`.  
**Verdict:** **STRUCTURAL PASS / SEMANTIC CONDITIONAL ACCEPTANCE**. Step 2 is complete as a *classified, traceable dataset*, but it is not a fully independent semantic validation or a definitive cross-candidate strictness baseline. A targeted remediation and audit are recommended before Step 3 is used for decisive comparisons.

## What was independently verified

The archive was extracted to a separate workspace. The initial `5.4(1).zip` supplied the immutable `inputs/` and `step1_union/` trees; `step1_union_augmented_pass1.zip` supplied the augmented view and Pass 1 overlay. The submitted Step 2 tree was copied unchanged to that isolated workspace.

The original project validator was **executed independently** from the reconstructed Step 2 directory:

```sh
python -B _tools/finalize.py validate
```

It reproduced **18/18 PASS gates; 0 failed gates**, including `INPUT_SHA256_UNCHANGED`, `ALL_6402_RECORDS_EXACTLY_ONCE`, `ALL_1176_COVERAGE_ROWS_EXACTLY_ONCE`, `EVIDENCE_RE_READ_FROM_IMMUTABLE_FILES`, `CHECKPOINT_INTEGRITY`, `CORRECTIONS_HAVE_BEFORE_AFTER_PROVENANCE`, and `CODEX_PASS2_NOT_CONSUMED`. This was a validator replay, not an independent proof that every classification is substantively correct.

Counts independently parsed from `per_candidate/*/CLASSIFICATIONS.jsonl`:

| Candidate | Records | CO | CD | XP | XW | IA | MX | NN | UN |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| M | 1003 | 699 | 65 | 120 | 46 | 47 | 6 | 17 | 3 |
| M1 | 1113 | 732 | 73 | 134 | 52 | 72 | 13 | 34 | 3 |
| L0 | 972 | 647 | 62 | 119 | 45 | 49 | 23 | 25 | 2 |
| L1 | 1037 | 674 | 80 | 124 | 57 | 61 | 23 | 15 | 3 |
| K0 | 1077 | 687 | 71 | 129 | 59 | 70 | 30 | 27 | 4 |
| K1 | 1200 | 741 | 87 | 145 | 60 | 91 | 40 | 32 | 4 |
| **TOTAL** | **6402** | **4180** | **438** | **771** | **319** | **390** | **135** | **150** | **19** |

All 6,402 classification rows report verified source quotation ranges. There are 1,176 policy-coverage rows, all marked `DIRECT_EVIDENCE`; **38** require reviewer overrides assembling partial clauses. These coverage statuses are evidence-traceability statuses, **not parity or compliance certifications**.

Pass 1 additions are fully retained: all **26** provisional new clauses (17 `EXTRA_WORKFLOW`, 9 `INTERNAL_ARCHITECTURE`) and all **29** provisional facets (7 additional obligations, 22 factual clarifications) have Step 2 records. None of these labels alone establishes a new mandatory product requirement.

## Previously reported issues in M — resolved with provenance

1. `FG-M-22cae42396`: changed from `CANONICAL_ONLY` to `MIXED`, with a separate extra-product subclause for prioritising meaningful behavior, edge cases and risky integrations; see `COR-M-0001`.
2. `FG-M-1c4fc44b5e`: conditional trigger restored — **when the deployment model supports artifact promotion**; see `COR-M-0003`.
3. `FG-M-d0b6a09cce`: "often preferable" is now treated as normative `SHOULD` / `EXTRA_PRODUCT`, rather than `NON_NORMATIVE`; see `COR-M-0004`.

The correction log contains **252 corrections**, including **24 classification changes**. The end-of-run A1.3 audit changed modality for **152** records and check-by-reference codes for **4** records; these were performed without changing their classifications. This is an important signal of initial modality sensitivity, not proof that all remaining strength judgements are correct.

## Independent semantic finding — K1 Swagger UI check requires reclassification review

`FG-K1-2b15ea3da2` is `CANONICAL_ONLY`, `oracle_relation=FULLY_ENTAILED`, `strength_vs_canonical=SAME`, `modality=DEFAULT`. Its actual source at `inputs/K1/output/template/.claude/skills/swagger/SKILL.md:70` says, among other actions, to **open the Development Swagger UI and confirm it loads** when API behavior changes.

The four linked canonical policies (`WF-006`, `WF-005`, `API-016`, `TST-010`) require relevant build/tests, verifying startup when appropriate, accurate Swagger/OpenAPI metadata, and preserving unique manual coverage. None specifically requires **opening the UI and confirming its rendering**. A distinguishing scenario exists: check generated OpenAPI metadata, startup and tests successfully without opening the browser UI. This satisfies those policy clauses but not the literal K1 instruction. Under the frozen rule for independently testable additional constraints, the classification seems to have missed an **extra workflow verification method or subclause**. Check whether it is a conditional DEFAULT, and whether the compound claim should be represented as `CANONICAL_PLUS_DELTA` or `MIXED`. Do not presume any corresponding claim in the other five candidates is identical. This is a **source-grounded review finding**, not a wholesale rejection of K1.

The submitted `COVERAGE_LIMITATIONS.md` itself recognizes inconsistent treatment of the Swagger UI condition between K1 and several other candidates. The exact source text deserves targeted review before comparative strictness.

## Open limitations that affect Step 3

- **19** `UNCERTAIN` records and **4** records with an uncertain subclause, **24** future-human-decision entries (overlapping themes, not 24 necessarily distinct policy choices), **21** queued orphan reviews, **33** low-confidence records and **90** review-needed records (overlapping groups), plus **33** potential overmerges. None should silently become a strictness or compliance fact.
- The final A1.3 audit left **79** flat-negative records at `MUST_NOT` pending methodological issue **PI-012**: **71** are `CANONICAL_ONLY`, **8** are `EXTRA_PRODUCT`. Negative declaratives and prohibitions should be normalized consistently before ranking mandatory constraints.
- **38** policy coverage rows use overrides; **five** canonical policies have no equal-strength evidence in K0/K1 (`K0`: API-014 and API-019; `K1`: GOV-007, API-014 and API-019), despite `DIRECT_EVIDENCE`. Retain these strength qualifiers.
- The 4,915 Step 1 queue records are *accounted for*, but **4,868** relations/attribution disagreements are mechanically recorded without individual adjudication; **47** conflict/unresolved items were adjudicated one by one. `STEP1_MERGE_QUEUE_ACCOUNTED` therefore cannot be interpreted as full semantic dispute resolution.
- `MIXED` classification increases from 6 in M to 40 in K1; a later tendency to split compound records may account for some of the difference. No comparative conclusion should follow from raw label counts.
- Hooks/settings/checkers were inspected statically, not executed; host-compatibility and reported bypasses cannot be claimed as runtime-verified.
- Five candidates M1/L0/L1/K0/K1 were not independently semantic-reviewed during the Claude run; the current independent spot-check is not an exhaustive second audit. The 153 challenge samples cannot be used as a statistical error rate.

## Decision and next actions

1. **Accept the structural execution of Stage A / Step 2 as complete**; preserve this directory and all prior snapshots unchanged.
2. **Do not certify the semantics as final yet.** Request a narrow correction for `FG-K1-2b15ea3da2` and harmonize treatment of comparable Swagger UI clauses without forcing source-distinct statements into the same category.
3. Before definitive Stage A / Step 3 comparison, perform a bounded independent semantic audit covering all five not-yet-reviewed candidates, especially `MIXED`, `CANONICAL_PLUS_DELTA`, `EXTRA_*`, overrides and normative strengths. Do not rerun the whole 6,402-record classification by default.
4. Resolve **PI-012** (79 flat negatives), at minimum establish a documented normalization rule and uncertainty markers for comparative outputs. Audit the five no-equal-strength policy rows and 33 suspected overmerges that could materially distort comparisons.
5. Carry truly irresolvable governance ambiguities into Step 3 explicitly as `UNRESOLVED`, reserving substantive policy choices for the human decision gate before unification. No human decision is necessary merely to complete Step 2's mechanical classification.

**Bottom line:** **Stage A / Step 2 is structurally finished and reproducible. Semantic status is a conditional PASS, not a verified final parity baseline. Step 3 may be prepared in parallel, but definitive candidate-to-candidate comparisons should not rely on unreviewed modality or unresolved classifications.**
