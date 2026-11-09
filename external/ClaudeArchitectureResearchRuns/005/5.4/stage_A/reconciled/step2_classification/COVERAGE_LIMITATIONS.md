# Coverage limitations: Stage A / Step 2

Protocol step2-v1 with Addendum A1. Read this before using any count from this folder.

**Structural coverage does not prove semantic completeness.** Every one of the 6,402 records has a label and every policy row has a status. That does not show that all normative content of the candidates was found, or that every label is right. This run does not claim "zero remaining normative orphans".

## What the coverage does and does not cover

1. **The classified universe is the Pass 1 augmented union.** Step 2 did no new global extraction. A normative clause that neither Step 1 nor Pass 1 surfaced is not in these files unless a reader met it in an open-item review.
2. **Codex Pass 2 is still running and was not used.** Its findings may add clauses or facets that this dataset lacks.
3. **`DIRECT_EVIDENCE` means traceable evidence in this dataset.** It is not a compliance or freeze-readiness result, and `NOT_EVIDENCED` would not have meant a violation.
4. **38 of the 1,176 rows are `DIRECT_EVIDENCE` by a written reviewer override.** No single record fully covered those policies, so the reviewer checked several partial records clause by clause under C13. The note is in `reviewer_override_note` on each row.
5. **Hooks, scripts and settings were read statically (C10).** Nothing was executed. Reported bypasses and parser gaps, such as the guard gap noted at `FG-K1-e32ee646e0`, remain unverified.

## Strength and modality

6. **Rows with no equal-strength evidence:** K0: API-014, API-019; K1: GOV-007, API-014, API-019. These have stronger and weaker evidence only, shown as `STRONGER_AND_WEAKER_EVIDENCE`. The record may restate the policy's content while differing in force.
7. **The end-of-run A1.3 audit gives a floor for this defect class, not a full count.** It found records at MUST or MUST_NOT whose whole evidence, in a knowledge skill or private reference, has no must-like word. It changed the modality of 152 of them (145 A, 4 B and 3 C). A record is not reached if a must-like word appears anywhere in its evidence, including in another clause of a broad group.
8. **79 flat negatives stay at MUST_NOT,** 4 of them in M1 now coded as check by reference. They say "no X", "not X", "only when" or "without", with no must, never or do not. A1.3 addresses positive imperatives and does not settle these (PI-012, still open). The list is category N in `_decisions/A13_AUDIT_FINDINGS.jsonl`.
9. **The audit changed modality and strength, not classification.** Its corrections moved no record to another label, and all 1,176 rows kept their coverage status.

## Reader and process limits

10. **One reader made these decisions.** An independent review covered candidate M only, and this session applied its lessons to the rest. M1, L0, L1, K0 and K1 have had no independent review.
11. **Label use may have drifted during the run, so counts need care across candidates.** MIXED counts rise in processing order (M 6, M1 13, L0 23, L1 23, K0 30, K1 40), and INTERNAL_ARCHITECTURE counts also vary (M 47, M1 72, L0 49, L1 61, K0 70, K1 91). Part of this may come from the sources and part from the reader splitting compound records more readily later on. This run did not separate the two. Do not treat these counts as a difference between candidates without re-reading the records.
12. **Correction counts measure process, not quality.** M has the most corrections because it was read before Addendum A1 and then audited. Its batches stayed as checkpointed, with fixes applied as an overlay.
13. **Semantic challenges are samples.** 153 frozen samples were challenged, and 5 needed a revised reading. They show kinds of defects and are not an accuracy rate.
14. **NON_NORMATIVE was missed by the first challenge round in five candidates.** The round-1 pool asked for HIGH confidence, and every NN record in M1, L0, L1, K0 and K1 is MEDIUM. The validator found this, and a frozen round 2 added 5 NN samples per candidate, all upheld (PI-013). Five samples per candidate is thin.
15. **Reading-consistency aids were hints only.** `prior.py`, and scratch search scripts used late in the run, showed how finished candidates read similar text. They were used to keep readings consistent and are not a strictness comparison. Notes such as "Same reading as M1" record that consistency check. Each label still rests on the candidate's own source.
16. **The primary anchor of a broad Step-1 group can be its first clause,** not the clause the claim rests on (for example `FG-K0-aa5d11a7f5`). Use `evidence_refs` for the full evidence.
17. **Calibration:** 37 of 38 keys agree on class and modality. `FG-L0-1927451833` agrees on class but reads SHOULD where calibration read DEFAULT. `CALIBRATION.jsonl` was recompiled after a schema addition, and `PROTOCOL_FREEZE.json` records this as an amendment beside the original hash.

## Step-1 queue

18. **Only 47 of the 4,915 queue items were adjudicated one by one** (the conflicts and unresolved items). The other 4,868 (relations and attribution disagreements) are recorded mechanically in `STEP1_QUEUE_DISPOSITIONS.jsonl`. The reviewer saw them in batch views, and every named group is classified, but none received its own decision.
19. **Overmerge review is shallow.** `POTENTIAL_OVERMERGES.jsonl` holds 1 explicit flag and 32 MIXED records with several source ranges, found by rule. Groups whose members share a label were not examined for overmerging, and no Step-1 group was split.

## Known reading differences kept on purpose

These are recorded so that later work does not mistake them for candidate differences. They are not strictness findings.

| Records | Difference | Why it stays |
|---|---|---|
| `FG-M-2dfeb68001` and the Delegated records of M1 to K1 | M: CO with a permission code. The others: CD on GOV-005 | M carries the narrowed Delegated scope at the sibling record `FG-M-ae349c2f55`, and this record claims only the permission |
| `FG-L0-59496c6b6d` and `FG-K0-0865f7332f` | L0: CO advisory reminder. K0: XP on a Reserved reference graph | The wording differs. L0's hook asks to confirm the mapped layout or an approved decision; K0's says the change is Reserved |
| `FG-K1-2b15ea3da2` and the Swagger step in M1, L0, L1, K0 | K1: CO with a note. The others: UN on how far a condition reaches | The others hold a separate reported record on the question, and K1 has none. The same doubt may apply to K1 |
| `FG-M-567f30944c`, `FG-K0-77da905ab7` and `FG-K1-05e23d2c2a` | CO where the source keeps a "concrete requirement" exception. CD where it does not | The source text differs |
