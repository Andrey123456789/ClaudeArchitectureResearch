# Stage A, Step 1: Union Reconciliation Report

Experiment 005, phase 5.4. Scope: lossless, provenance-preserving union of candidate rule claims for candidates M, M1, L0, L1, K0 and K1 from the primary run (`stage_A/primary/`), the replica run (`stage_A/replica/`) and the Codex blind run (`stage_A/independent/`). Protocol: `MERGE_PROTOCOL.md` (v1.2.2; see its change log). Generated 2026-10-28.

This report does **not** classify claims as truly EXTRA or ORACLE, compare strictness, adjudicate discrepancies or unify engineering requirements; those belong to Steps 2-4. Every original label (`ORACLE_LINKED`, `EXTRA`, `LINK_UNCERTAIN`, `POTENTIAL_*`, `AMBIGUOUS`, ...) is kept only as attributed provenance in `MERGED_FINDINGS.jsonl` (`original_labels`), never as a validated conclusion.

## 1. Input records: expected versus actual

Counts were re-derived for this report directly from the raw input files (non-empty lines parsed as JSON; unparseable lines: 0) and compared with the expected figures from the task and with the two output ledgers.

| Run / type | Expected | Raw files | SOURCE_RECORD_INDEX | Match |
| --- | --- | --- | --- | --- |
| PRIMARY CONSTRAINT | 5,131 | 5,131 | 5,131 | yes |
| REPLICA CONSTRAINT | 1,765 | 1,765 | 1,765 | yes |
| CODEX BLIND_FINDING | 813 | 813 | 813 | yes |
| PRIMARY POLICY | 1,176 | 1,176 | 1,176 | yes |
| REPLICA POLICY | 1,176 | 1,176 | 1,176 | yes |
| PRIMARY ORPHAN | 1,626 | 1,626 | 1,626 | yes |
| REPLICA ORPHAN | 396 | 396 | 396 | yes |
| **Total** | **12,083** | **12,083** | **12,083** | yes |

Result: the expected total of 12,083 is confirmed by the raw files (12,083) and by `SOURCE_RECORD_INDEX.jsonl` (12,083); `RECORD_ACCOUNTING.jsonl` has 12,083 rows, one per input record. No discrepancy was found, so none needed investigation.

Per candidate (raw files):

| Candidate | P constraints | R constraints | Codex findings | P policies | R policies | P orphans | R orphans | Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M | 851 | 241 | 106 | 196 | 196 | 283 | 65 | 1,938 |
| M1 | 930 | 247 | 120 | 196 | 196 | 283 | 69 | 2,041 |
| L0 | 813 | 248 | 116 | 196 | 196 | 235 | 51 | 1,855 |
| L1 | 852 | 254 | 142 | 196 | 196 | 258 | 55 | 1,953 |
| K0 | 810 | 389 | 133 | 196 | 196 | 270 | 66 | 2,060 |
| K1 | 875 | 386 | 196 | 196 | 196 | 297 | 90 | 2,236 |

### Accounting dispositions (all candidates)

| Disposition | Records | Meaning |
| --- | --- | --- |
| LINKED_TO_FINDING | 7,709 | every primary/replica constraint and every Codex finding is linked to at least one finding group through its claim units |
| POLICY_CROSS_REFERENCE | 2,352 | policy rows are cross-references to the oracle policy set, never counted as independently confirmed rules |
| ORPHAN_CONTEXT_LINKED | 1,799 | orphan records linked to findings as context by source location |
| ORPHAN_PENDING_REVIEW | 223 | orphan records with no co-located finding; kept, flagged for Step 2 |
| **Total** | **12,083** |  |

## 2. Union and deduplication results

| Candidate | Input records | Claim units | Records split | Finding groups | Semantic-duplicate groups | Merge decisions | Singleton groups | Codex normalized | Multi-run regions reviewed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M | 1,938 | 1,414 | 112 | 995 | 377 | 385 | 618 | 106/106 | 602/602 |
| M1 | 2,041 | 1,485 | 100 | 1,101 | 340 | 354 | 761 | 120/120 | 684/684 |
| L0 | 1,855 | 1,334 | 94 | 965 | 338 | 340 | 627 | 116/116 | 514/514 |
| L1 | 1,953 | 1,401 | 84 | 1,028 | 338 | 342 | 690 | 142/142 | 559/559 |
| K0 | 2,060 | 1,569 | 154 | 1,062 | 447 | 458 | 615 | 133/133 | 542/542 |
| K1 | 2,236 | 1,833 | 225 | 1,196 | 541 | 567 | 655 | 196/196 | 447/447 |
| **Total** | **12,083** | **9,036** | **769** | **6,347** | **2,381** | **2,446** | **3,966** | **813/813** | **3,348/3,348** |

* **Exact versus semantic deduplication.** `EXACT_DUPLICATE` requires identical `normative_action`, `modality`, `trigger_scope` and `exceptions` after harmless normalization. No reviewer issued an `EXACT_DUPLICATE` directive, so there are **0 exact-duplicate groups**. All 2,446 merge decisions are `SEMANTIC_DUPLICATE`, each with an explicit S (scope) / M (modality) / E (exceptions) / T (timing) rationale. This includes pairs whose action text is word-for-word identical, because their attributed scope and exception fields are written differently by each run.
* **Splits.** A record that bundles several obligations was split into claim units (`#a`, `#b`, ...) before merging (769 records). A split never deletes text: every part keeps the original record key, and `RECORD_ACCOUNTING.jsonl` links the record to all its parts.
* **Singletons** are retained claims, not rejected ones. Every singleton has a recorded basis: `REVIEWED_NO_DUPLICATE_FOUND` (co-located with records from other runs, reviewed, not merged) or `NO_CO_LOCATED_RECORD_FROM_OTHER_RUN`.

Groups by supporting runs (count of groups, not a measure of correctness):

| Candidate | PRIMARY | REPLICA | CODEX | PRIMARY+REPLICA | PRIMARY+CODEX | REPLICA+CODEX | PRIMARY+REPLICA+CODEX |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M | 474 | 93 | 51 | 224 | 112 | 5 | 36 |
| M1 | 586 | 106 | 69 | 239 | 64 | 5 | 32 |
| L0 | 476 | 84 | 67 | 222 | 84 | 2 | 30 |
| L1 | 521 | 93 | 78 | 217 | 86 | 3 | 30 |
| K0 | 375 | 131 | 109 | 336 | 55 | 4 | 52 |
| K1 | 369 | 123 | 164 | 294 | 156 | 5 | 85 |
| **Total** | **2,801** | **630** | **538** | **1,532** | **557** | **24** | **265** |

Singleton basis:

* `NO_CO_LOCATED_RECORD_FROM_OTHER_RUN`: 298
* `REVIEWED_NO_DUPLICATE_FOUND`: 3,668

**Counts are not comparable across agents.** The primary run produced 5,131 constraints and the replica run 1,765 for the same snapshots. The runs segment text at different granularity: replica records and Codex findings often bundle several obligations into one record. Of the 769 split records, 387 are replica, 342 Codex and 40 primary (counted from the `SPLIT` lines in `_review/`). A raw-count difference therefore says nothing about coverage or correctness. Only the claim unit, after splitting and merging, is a stable unit of account, and even it is reviewer-dependent. No majority vote or record count was used to decide anything.

## 3. Uncertain, related and conflicting cases (not merged)

`MERGE_REVIEW_QUEUE.jsonl` is the unresolved-cases list. Nothing in it is adjudicated.

| Candidate | Apparent conflict | Unresolved | Related-but-distinct | Attribution disagreement | Queue items | Orphans pending review |
| --- | --- | --- | --- | --- | --- | --- |
| M | 6 | 1 | 463 | 203 | 673 | 70 |
| M1 | 5 | 1 | 617 | 168 | 791 | 48 |
| L0 | 5 | 1 | 569 | 179 | 754 | 27 |
| L1 | 6 | 1 | 661 | 174 | 842 | 24 |
| K0 | 9 | 0 | 532 | 245 | 786 | 27 |
| K1 | 12 | 0 | 709 | 348 | 1,069 | 27 |
| **Total** | **43** | **4** | **3,551** | **1,317** | **4,915** | **223** |

Related-but-distinct subtypes (all candidates):

| Subtype | BROADER_NARROWER | COMPOUND_PART | DETAIL_DIFFERENCE | DIFFERENT_LAYER | DIFFERENT_SCOPE | DIFFERENT_STRENGTH | EXAMPLE_GENERAL | OVERLAP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Relations | 76 | 677 | 105 | 87 | 5 | 308 | 463 | 1,830 |

* **Apparent conflicts** come mostly from Codex "tension" findings and are stored as group pairs. Examples: Git operations only on explicit request versus high-risk operations permitted by an approved workflow (K1); protected branches being non-rewritable versus force-push on explicit request (K0, K1); the certificate-validation prohibition versus a local `TrustServerCertificate=True` example (K0, K1); and the Async-suffix coding default versus an analyzer keyed to the `async` modifier (K0, K1).
* **DIFFERENT_STRENGTH** pairs (308) are the clearest Step 2 inputs: the same statement with, for example, MUST in one run and DEFAULT or PREFER in the other. They were never merged.
* **Attribution disagreements** (1,317) are merged groups whose runs attributed different labels or policy IDs. The merge concerns the claim only; the conflicting attributions are preserved side by side.
* **Orphans pending review** (223) are orphan records with no co-located claim. They are retained in `RECORD_ACCOUNTING.jsonl` and were not dropped because of their original non-normative label.

## 4. Examples

### 4.1 Valid deduplication: K1 group `FG-K1-e39ebf7fad`

* Members: `PRIMARY:K1:CONSTRAINT:RULE-K1-0324` and `REPLICA:K1:CONSTRAINT:RULE-K1-0211`, both MUST and both citing `.claude/skills/code-review/SKILL.md` line 47.
* Both state a two-way specification-conformance review: no missing or weakened required behavior, no unapproved behavior (limits, reserved values, string-comparison semantics including database/framework defaults, required fields, workflow restrictions, validation), and approved synchronized details are not drift.
* The replica adds "internal implementation details are not product behavior". The decision was first left as `DETAIL_DIFFERENCE` because the full line had not been checked. On resume, line 47 of the immutable snapshot (`inputs/K1/output/template/.claude/skills/code-review/SKILL.md`) was read in full. It contains *"Do not confuse internal implementation details with product behavior."* The clause is therefore part of the shared cited text. Under rule F6 the pair is a semantic duplicate, with the difference noted in the rationale (`_review/K1/06_r241-r290.dec`, decision `MD-K1-f9800483`). The run labels and differing policy-ID attributions (GOV-008/010 versus GOV-001/005) are kept, so the group is flagged `attribution_disagreement`.

### 4.2 Intentionally non-merged broader/narrower pair: K1 `FG-K1-493b0ae5c9` versus `FG-K1-8c2a0fe6ef`

* Broader: `PRIMARY:K1:CONSTRAINT:RULE-K1-0149` + `REPLICA:K1:CONSTRAINT:RULE-K1-0078` (DEFAULT): compiled queries, ValueTask, pooling, custom serialization, aggressive caching and raw SQL for performance only for a *measured or clearly demonstrated* need.
* Narrower: `PRIMARY:K1:CONSTRAINT:RULE-K1-0393` + `CODEX:K1:BLIND_FINDING:BF-K1-0082#a`: compiled queries only for a *measured* hot path where compilation/cache-lookup overhead is *material* (`ef-core/SKILL.md` line 128, confirmed in the 12-quote spot-check).
* They share topic and run but differ in trigger: "clearly demonstrated" is accepted by one and not the other. Merging them would erase that difference, so they are linked as `RELATED_BUT_DISTINCT:BROADER_NARROWER`. Because Codex `BF-K1-0082` reports exactly this tension, the pair is also an `APPARENT_CONFLICT` for Step 2.

### 4.3 Suspicious Codex finding retained, not validated: K1 `FG-K1-6f6e2b2831`

* `CODEX:K1:BLIND_FINDING:BF-K1-0046` (classification AMBIGUOUS, assessment UNCERTAIN, confidence LOW) reports that an illustrative C# `field`-keyword setter in `modern-csharp/SKILL.md` lines 63-70 trims and rejects whitespace without a local approval caveat, so copying it could add unapproved string normalization.
* Neither Claude run recorded a constraint for that example. The finding is a speculation about how an example might be copied, not a statement of a rule.
* It was **retained** as a singleton (`REVIEWED_NO_DUPLICATE_FOUND`) with a neutral reviewer paraphrase marked "attributed, not a verdict". Its original labels and policy IDs (GOV-006, GOV-003) are kept. It was neither promoted to a rule nor discarded. Whether the example is normative is a Step 2 question.

## 5. Provenance and source verification

* Every finding group carries `source_record_keys`, `claim_unit_ids`, `clause_ids` and `occurrence_ids`, tracing back to exact input records (input file plus ordinal) and source locations (path and lines in the frozen `inputs/` snapshots).
* `SOURCE_CLAUSES.jsonl` stores the exact excerpt for every clause. Clause anchors by basis: evidence segment 16,731; Codex quote narrowed by the reviewer within the quoted range 925; full Codex quote range 468. All 6,347 groups have `source_verification_status = ALL_LOCATIONS_VERIFIED`, i.e. every member clause has `location_status = VERIFIED_RANGE` against the immutable snapshots.
* `SOURCE_VERIFICATION_ISSUES.jsonl` has 187 rows, all severity INFO, type `INCOMPLETE_CITATION_NO_SEGMENT_QUOTE` (M1: 1, K0: 119, K1: 67). These are primary-run segments with an empty quote, verified by line range only. There are no ERROR or WARNING issues.
* Quotation check: for each candidate a deterministic sample of 12 reviewer-narrowed anchors (`_tools/spotcheck.py <C> 12`) was read against the exact excerpt; verdicts are in `_review/<C>/anchor_spotcheck_verdicts.txt`. Result: 72 anchors sampled; 70 OK on first reading; 2 marked FIXED (M `CL-M-72baef7687-b47d26` and L0 `CL-L0-67c1fb349d-cf165c`, where the reviewer's paraphrase over-stated a restriction ('only when' versus the source's 'when'). The paraphrase was corrected before that candidate's checkpoint; the excerpt and claim unit were unchanged). No sampled excerpt failed to support its anchor. For K1, two further lines were read in full from the snapshot to settle decisions (`code-review/SKILL.md` L47; `swagger/SKILL.md` L13, which does not say "Development", so R0319#a versus P0568 stayed `DETAIL_DIFFERENCE`). `CLAUDE.md` L43-44 confirmed that the replica's exception for EXTRA-K1-0048 comes from L44, not the shared cited line.

## 6. Validation

`VALIDATE_STAGE1_UNION.py` (run without flags) checks structurally:

* the input manifest hashes;
* every input record accounted for exactly once;
* every claim unit grouped exactly once;
* that each decision references existing claim units;
* that every region is reviewed and every Codex finding normalized;
* the checkpoint hashes against current outputs;
* that the top-level ledgers are the concatenation of the per-candidate ledgers;
* that all deliverables are present.

It cannot prove that a semantic-equivalence judgment is correct.

Actual result of `python VALIDATE_STAGE1_UNION.py` (no flags): **PASS_WITH_OPEN_ISSUES**.

* Errors: 0; warnings: 0.
* Validator info: `input_manifest_files_verified` = 484; `input_manifest_sha256` = ae237fc0c8d1cfb1cec07c5371561e746c1b96146b82878ee8f7289d7c7d0311.
* "Open issues" are the review-queue items, orphans pending review and INFO verification issues counted above. They are intended Step 2 inputs, not defects.

## 7. Methodological limitations

1. **Reviewer judgment.** Semantic-duplicate and relation decisions are one reviewer's reading under the frozen predicates. Rationales are recorded per decision but not independently re-adjudicated. Relation recording is selective, not exhaustive (protocol v1.2.1 note). Step 2 should use `CO_LOCATION_INDEX.jsonl` to find every co-located pair.
2. **Protocol evolution.** v1.2 was adopted during M (from region r151); v1.2.1 and v1.2.2 are documentation corrections with no change to any predicate or decision. The checkpoints record the protocol hash in force when written: M differs from M1-K1, and the current file (v1.2.2) post-dates all six.
3. **Truncated replica records in K0.** `REPLICA:K0:CONSTRAINT:EXTRA-K0-0010` and `EXTRA-K0-0014` are cut at a `|` in the replica's own output, which shifts their fields. They were kept as-is, related only via `RD OVERLAP`, and documented in `_review/K0/04_*.dec`.
4. **Line-range-only verification.** 187 primary segments have no quote and are verified by line range only (INFO issues above).
5. **Codex normalization.** Every Codex finding (813/813) has a reviewer-written normalized claim (`CX`) or split (`SPLIT`) with an anchored line range. These paraphrases are attributed, not verdicts; the original explanation, scenario, labels and confidence are kept in `SOURCE_RECORD_INDEX.jsonl`. Codex findings with no co-located Claude record (for K1, the 12 in `_review/K1/11_codex_noncolocated.dec`, mostly checker/hook implementation behavior) remain singletons (`NO_CO_LOCATED_RECORD_FROM_OTHER_RUN`).
6. **Modality labels without proven equivalence** (for example `ENFORCED_DEFAULT` versus `DEFAULT (configuration)`, `DECIDED` versus `MUST`) were treated as different strengths, so they were never merged. Some of these may prove equivalent in Step 2.
7. **Apparent conflicts observed without a Codex report.** One was recorded and marked as such: K1 protected-branch non-rewrite versus force-push on explicit request, mirroring the Codex-reported K0 case.

## 8. Instructions for Step 2

1. Start from `MERGED_FINDINGS.jsonl` (6,347 groups). Treat `original_labels` and `original_claimed_policy_ids` as claims to adjudicate, not facts.
2. Work through `MERGE_REVIEW_QUEUE.jsonl` in this order:
   * `APPARENT_CONFLICT` (43) and `UNRESOLVED` (4);
   * `RELATED_BUT_DISTINCT:DIFFERENT_STRENGTH` (308), then `BROADER_NARROWER` and `DETAIL_DIFFERENCE`;
   * `ATTRIBUTION_DISAGREEMENT` (1,317).
3. Review the 223 `ORPHAN_PENDING_REVIEW` rows in `RECORD_ACCOUNTING.jsonl`. Original labels are not grounds for discarding them.
4. Use `CO_LOCATION_INDEX.jsonl` for every co-located pair that was reviewed and not merged.
5. Do not compare raw run counts (section 2). Compare at the group/claim-unit level, and keep cross-candidate comparisons for Stage 3+.
6. To re-check integrity before Step 2 run `python VALIDATE_STAGE1_UNION.py`. To trace any group back to source, follow `clause_ids` into `SOURCE_CLAUSES.jsonl` (exact excerpt, path, lines).

## 9. Deliverables

* `MERGE_PROTOCOL.md`: frozen predicates, DSL, change log.
* `SOURCE_RECORD_INDEX.jsonl`: one row per input record (12,083), raw record preserved.
* `SOURCE_CLAUSES.jsonl`: normalized source clauses with exact excerpts.
* `SOURCE_OCCURRENCES.jsonl`: source locations per claim.
* `MERGED_FINDINGS.jsonl`: finding groups with full provenance.
* `MERGE_DECISIONS.jsonl`: every merge decision with rationale and decision-file line.
* `RECORD_ACCOUNTING.jsonl`: input-to-output accounting, one row per input record.
* `MERGE_REVIEW_QUEUE.jsonl`: unresolved-cases list (relations, conflicts, attribution disagreements).
* `CO_LOCATION_INDEX.jsonl`: co-located pairs and their review outcome.
* `SOURCE_VERIFICATION_ISSUES.jsonl`: source verification issues (187 INFO).
* `VALIDATE_STAGE1_UNION.py`: executable validator.
* `CHECKPOINTS/`: per-candidate checkpoints with input/output/decision-file SHA-256.
* `_review/<C>/`: reviewer decision files and spot-check verdicts.
* `_tools/`: builder and helper scripts.

## Appendix A. Input hashes

Input manifest SHA-256 (all checkpoints): `ae237fc0c8d1cfb1cec07c5371561e746c1b96146b82878ee8f7289d7c7d0311`.

| Candidate | Checkpoint (UTC) | Input file | SHA-256 |
| --- | --- | --- | --- |
| M | 2026-10-28T08:33:38+00:00 | `stage_A/independent/M/blind/BLIND_COMPLETE.json` | `cb82be5addbc8702a85b1bb59ee68cf75fd95141272eb69e248e4732c31560e7` |
|  |  | `stage_A/independent/M/blind/BLIND_FINDINGS.jsonl` | `3c1bfbde46df6fe6137c74bc196b47600ac33b40c3abfd979f9d4a805cc99dee` |
|  |  | `stage_A/independent/M/blind/FILE_REVIEW_LEDGER.jsonl` | `55a652477aad8938b280c1855bec52e6fa49e273b47b02c2cd6a99cf871e4dc4` |
|  |  | `stage_A/primary/M/ORPHAN_CANDIDATES.jsonl` | `2bc3d0f2f40dedb95aee296679e3e1f275e400ceb74507f0280d5d6b9ef1eabe` |
|  |  | `stage_A/primary/M/constraints.jsonl` | `ea017c6e7b8dc699f6dd0bcf01da35c734f3643244219fac15256ec30eb741f3` |
|  |  | `stage_A/primary/M/coverage_ranges.jsonl` | `80db5e10d8a6a3d305dcdb5d15448f34de30849510c0d7cc729ec58de8e5f65b` |
|  |  | `stage_A/primary/M/files.jsonl` | `7885289910009debcd51041e5c63f0f6668ebaef345f7876c1161364e5c6ec20` |
|  |  | `stage_A/primary/M/policies.jsonl` | `b98f2580764ec13d53a7289e184e6cae413c7669939e64fba5e27e0e546c0944` |
|  |  | `stage_A/replica/M/ORPHAN_CANDIDATES.jsonl` | `34e727598f5910f64dc649fef27290e22448dac8061542838909e34c3f090aa0` |
|  |  | `stage_A/replica/M/constraints.jsonl` | `d02324643150cec4b0d4cc7b93c3a31f218539f3873070c5552eb039988fffed` |
|  |  | `stage_A/replica/M/coverage_ranges.jsonl` | `e22adc2615c3f0d950ad495f953b806cd88535e0d468a6fe2b0b1145554e5904` |
|  |  | `stage_A/replica/M/files.jsonl` | `d0527d41e53dd77b9507a5d6cf7c216c74a338585fb4c8993070670d8429ae26` |
|  |  | `stage_A/replica/M/policies.jsonl` | `3e86d4650a9e5c92ea64076f45cf1caa4027e199fcb6fddb4e71bd84801ba64b` |
| M1 | 2026-10-28T09:02:34+00:00 | `stage_A/independent/M1/blind/BLIND_COMPLETE.json` | `7955eba88a49f08facdc37e825ff24c11dd7688d31cbae6ea28708d43046c3cb` |
|  |  | `stage_A/independent/M1/blind/BLIND_FINDINGS.jsonl` | `3ac1670c9af83012018380edd4a442786c0f63fbafeb65cc17af6d4d5ebe08be` |
|  |  | `stage_A/independent/M1/blind/FILE_REVIEW_LEDGER.jsonl` | `ff219eb6b0ec4502824520e354a78c6d509d6473bea26072a78e4f292be3f7bf` |
|  |  | `stage_A/primary/M1/ORPHAN_CANDIDATES.jsonl` | `ceb449cc4944b21ebbf751cb5b710365351e21ca7e67e4153c0ee70ea300ca1f` |
|  |  | `stage_A/primary/M1/constraints.jsonl` | `8a0b3e411c6cd0a2515385ddce8ffe357c671af5e45da023753f8718999ea73e` |
|  |  | `stage_A/primary/M1/coverage_ranges.jsonl` | `31488e228c910126b6eab8d8b3ace69b097a4b441080d1b1ea587ceb797c7fde` |
|  |  | `stage_A/primary/M1/files.jsonl` | `4eca40a672222d18c260a121a81a316dd098014d24b30e448de3924c3614c8d1` |
|  |  | `stage_A/primary/M1/policies.jsonl` | `b1f397edad9a492c440e91d73019fca9d0719b33105e3e70284c8cf0956d2d34` |
|  |  | `stage_A/replica/M1/ORPHAN_CANDIDATES.jsonl` | `0c412ee978dd5fb3db0cc21cfb21bd66d4a95f9d4a049ae486fc5fca4391bc31` |
|  |  | `stage_A/replica/M1/constraints.jsonl` | `fc17a978f837408456d7489198380d8dd3981e1478c2bd4f70e35ca59baf9328` |
|  |  | `stage_A/replica/M1/coverage_ranges.jsonl` | `6186de9514a1829cfe7762511ebec00e2dadf8cead65e3bb682c3339f49eba46` |
|  |  | `stage_A/replica/M1/files.jsonl` | `ad4090209af0afb9ce156a979feb2df162a2545b4a7936d2a9ee262307c9accf` |
|  |  | `stage_A/replica/M1/policies.jsonl` | `67ddd709230b13c7fd2df2bcdbdada0074fd62d2dc05546243313559a3d0ba95` |
| L0 | 2026-10-28T15:05:44+00:00 | `stage_A/independent/L0/blind/BLIND_COMPLETE.json` | `43ce0aeefba5715d33b89a38827072e2cfc04c585423beaf845b19eea24d0d62` |
|  |  | `stage_A/independent/L0/blind/BLIND_FINDINGS.jsonl` | `b985f2e43f0844d886fba59c2611424813f5c8a588dd59d5936f565d84a7eba9` |
|  |  | `stage_A/independent/L0/blind/FILE_REVIEW_LEDGER.jsonl` | `d34a094284f8fcb31d8092530ba4322ac9d1971c0ec57210cd2c7055e42abd85` |
|  |  | `stage_A/primary/L0/ORPHAN_CANDIDATES.jsonl` | `8f7314b23ed3ba283a458f22e99edf56d9df843b6875239ce9bd7f6a0dd5b704` |
|  |  | `stage_A/primary/L0/constraints.jsonl` | `46b34c6e65eac953d3042443431be87cd253d87757f0e9c802311a8e311048bf` |
|  |  | `stage_A/primary/L0/coverage_ranges.jsonl` | `4c741f2c82e0cada01f223fc99e8cd886324449e54d3a44df5ddc61281b4c77a` |
|  |  | `stage_A/primary/L0/files.jsonl` | `be34b60efd481c64501d4efa3a4678572c4747cd77a89fa36771a112eda93e1a` |
|  |  | `stage_A/primary/L0/policies.jsonl` | `611595f8da8e05ec18e28e402b50cb0d86f9254f53b283024757e42b6f39d3ee` |
|  |  | `stage_A/replica/L0/ORPHAN_CANDIDATES.jsonl` | `4ad4824acb658c1877f3a9385b5c73907e070823cfa051d4ff8f5733d09c2c8d` |
|  |  | `stage_A/replica/L0/constraints.jsonl` | `9d8df30f3787c36871271dd79ccb76003d6bd2ffd2a82c3dd5b28ad31b132f6d` |
|  |  | `stage_A/replica/L0/coverage_ranges.jsonl` | `0976f943cba132be3af1a99ac3600f6fa9d197655bb2248bdc5730ba0424e03d` |
|  |  | `stage_A/replica/L0/files.jsonl` | `b1c8e7747b9488a20005aca4b29ad752df0c32d4ff1edca11adc40bee5e9bba5` |
|  |  | `stage_A/replica/L0/policies.jsonl` | `331906fff7d12dbe2f74f452c8fcc49a940a108a1937a3b0048920b82e8378fd` |
| L1 | 2026-10-28T15:34:33+00:00 | `stage_A/independent/L1/blind/BLIND_COMPLETE.json` | `8f76eb9fcefb34086ab68963151f52488e2482a51167373f625b19a26ab8f1a2` |
|  |  | `stage_A/independent/L1/blind/BLIND_FINDINGS.jsonl` | `429c63aa456b3f8f6d6abc2113904321f8cdfe912cbefd3cee35ae7409aa6ece` |
|  |  | `stage_A/independent/L1/blind/FILE_REVIEW_LEDGER.jsonl` | `cb3ca6778dec7ba8a64503f36b3b5dce1fd65a097cae312799e333589cc5c67c` |
|  |  | `stage_A/primary/L1/ORPHAN_CANDIDATES.jsonl` | `f36b2a51d573dd3c3300208f6eb84e7344471246f9d095cb4aaf46063f22dfc4` |
|  |  | `stage_A/primary/L1/constraints.jsonl` | `8684ed24bff5495cb41dfc74c0c2556803fd93e75d05d054f0f5e888571c612b` |
|  |  | `stage_A/primary/L1/coverage_ranges.jsonl` | `47a6c3ae595d2f7b45d58367fca5a1abde02568a2dba5a5c5e355cc156bffc86` |
|  |  | `stage_A/primary/L1/files.jsonl` | `d4da68f53e83e7fbcbe07a157a8cfe343a6a73d40803465050dc515cbdd2e365` |
|  |  | `stage_A/primary/L1/policies.jsonl` | `044b867dd7067d3a90d6fc9bd938beb45a09733822a5a4195b858eb656dea86c` |
|  |  | `stage_A/replica/L1/ORPHAN_CANDIDATES.jsonl` | `fb37e150216c90615e16a896c916d1457e298cfce651c35884a963c18b93d3c4` |
|  |  | `stage_A/replica/L1/constraints.jsonl` | `59e82d62689379293fe8e76094e99ed6424f860f7812ff651831d58fe97b571e` |
|  |  | `stage_A/replica/L1/coverage_ranges.jsonl` | `29516bdf2ac012422f2d97de5b72c049489300cd5aa2350fbd0c77811f369732` |
|  |  | `stage_A/replica/L1/files.jsonl` | `1e71bc683ee3c39abe06258bb26d0e7d087fbd17dc891a12af03a24a60fbbe87` |
|  |  | `stage_A/replica/L1/policies.jsonl` | `884f513c032bba3f60db51bec8fba9f804d899be204adc2d04483efd3ef553cf` |
| K0 | 2026-10-28T16:00:26+00:00 | `stage_A/independent/K0/blind/BLIND_COMPLETE.json` | `a9104deadf0a870183a0ade6f18a05f4e434ff3f239c031a41e9546943c296e4` |
|  |  | `stage_A/independent/K0/blind/BLIND_FINDINGS.jsonl` | `4ed5a70f614feeec05657e19d64fde9a7b65091e23d502a49d4f86bd0ed66cf3` |
|  |  | `stage_A/independent/K0/blind/FILE_REVIEW_LEDGER.jsonl` | `3dbf6e4967d3d673f964b28c3858cb50e9ea7842a3d5f00cdfdaef261eb474fd` |
|  |  | `stage_A/primary/K0/ORPHAN_CANDIDATES.jsonl` | `f4ab8eb27eb889ca75d80b0a1005c4fcb00405944f59bb476d6714f89228858f` |
|  |  | `stage_A/primary/K0/constraints.jsonl` | `888deeb19839c51de09507024c47d13ee526663813232c00688167a9ffa7b848` |
|  |  | `stage_A/primary/K0/coverage_ranges.jsonl` | `870e4f0367b56c5b313c2d6de42b13d7e71a69124458b00b515f94093b19acc1` |
|  |  | `stage_A/primary/K0/files.jsonl` | `2fa14427b25d1355e0229064b638e2b59af65fa3c89f7e638df0de1f6723cef2` |
|  |  | `stage_A/primary/K0/policies.jsonl` | `beaf6851751ca21ed26a8e21a2c3c5c918e015add5e16a95a04c08159d259a6d` |
|  |  | `stage_A/replica/K0/ORPHAN_CANDIDATES.jsonl` | `924c5928ada55e5a65a40af4de439f20c1c9e2a7fe2eaece9634a5b960429984` |
|  |  | `stage_A/replica/K0/constraints.jsonl` | `710e53ab32c3b14503f203f03f421548cc1faea61f1795e063c64028ad7d3bf8` |
|  |  | `stage_A/replica/K0/coverage_ranges.jsonl` | `c0144c6350132bf4d1f3ea33dae11e41c070dc26a105617bffbe003c415388be` |
|  |  | `stage_A/replica/K0/files.jsonl` | `cf7cc5b6d0c98eaeb28508b26ec6480120c6ac86ae6dbe0308450a2515256777` |
|  |  | `stage_A/replica/K0/policies.jsonl` | `07bbd41939dce5b37ed86362c426fc3d8f2a6736055b338a8ef3e730c96f42bc` |
| K1 | 2026-10-28T20:23:20+00:00 | `stage_A/independent/K1/blind/BLIND_COMPLETE.json` | `e7915f89de35e9b8079ae8588dd3d72c3712b6d73e6eb93032946f7f9c36d6e0` |
|  |  | `stage_A/independent/K1/blind/BLIND_FINDINGS.jsonl` | `a8dca5858bc0d5e8ef9c319f3a547697d316785b0f5aaebd7b7f48fcc6128959` |
|  |  | `stage_A/independent/K1/blind/FILE_REVIEW_LEDGER.jsonl` | `e48e3d3d86b1e15fe59de81347dfe34d2349103b2eaa8bd0e472fadb0a07364e` |
|  |  | `stage_A/primary/K1/ORPHAN_CANDIDATES.jsonl` | `aca8ad329ed47939319460da22ea778c3755cfa1e2f32b696ad65e8cac8605dd` |
|  |  | `stage_A/primary/K1/constraints.jsonl` | `8b6e246c8691ca25cc1735216b0df8043fb0cd9de2a11292dc5152692061e591` |
|  |  | `stage_A/primary/K1/coverage_ranges.jsonl` | `e60dafcc55d1c4bf2cfbd16b4d95206930a51644dbac27df4ae41cd2c3cc5bba` |
|  |  | `stage_A/primary/K1/files.jsonl` | `1b9d27cd888954f47114383801cfbb473d0151748420f97983df279500c823b6` |
|  |  | `stage_A/primary/K1/policies.jsonl` | `2db37df4430dd6eaf10dac1f32f1d3b5896a85cc3d60cd84c62babbb1596cc6b` |
|  |  | `stage_A/replica/K1/ORPHAN_CANDIDATES.jsonl` | `2924bdb98dcb5a0f2fb44dab0fec415c1bf407d78604d47f2126fde0209ae922` |
|  |  | `stage_A/replica/K1/constraints.jsonl` | `03b1260fb9f306c42a4ad9ba233327663ba9ba41294c4e2f0e8b5512ed94516b` |
|  |  | `stage_A/replica/K1/coverage_ranges.jsonl` | `343af2c88874a28633ae331ea0949e55769433d24e32d18cce5c5e877769fb62` |
|  |  | `stage_A/replica/K1/files.jsonl` | `c4a5e69cbb7e3eb8b655d5248ea6e512949ca433e79e985ffef13b6446cf7a57` |
|  |  | `stage_A/replica/K1/policies.jsonl` | `a58c05178e65521dfe6878d97913701345c24a8d9179ec21214c4040ed5006b6` |

