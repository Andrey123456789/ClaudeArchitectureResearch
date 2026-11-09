# Candidate M — response to the independent review

Immutable inputs, the union, the augmented union and all checkpointed M batch files are unchanged: `preflight.py --verify` reports no changes, and assembly re-checks the batch hashes. Every record change is in `CORRECTIONS.jsonl`, with the full before record and a field-by-field diff.

| # | Finding | What changed | Where to check |
|---|---|---|---|
| 1 | `FG-M-22cae42396` stayed `CANONICAL_ONLY`/HIGH after a `REVISED_NEEDED` challenge | Now `MIXED`, confidence MEDIUM. S1: coverage is not a target, entailed by TST-011 but weaker (`CANONICAL_ONLY`, SHOULD_NOT). S2: prioritize meaningful behavior, edge cases and risky integrations (`EXTRA_PRODUCT`, DEFAULT), with a distinguishing scenario. | `COR-M-0001`; challenge resolution `RESOLVED_BY_CORRECTION` |
| 2 | `FG-M-1c4fc44b5e` lost its source condition | Trigger restored: "when the deployment model supports artifact promotion". The challenge row now shows `UPHELD_WITH_FIELD_CORRECTION`. | `COR-M-0003` |
| 3 | `FG-M-d0b6a09cce` "often preferable" | Reclassified from `NON_NORMATIVE` to `EXTRA_PRODUCT`, SHOULD, MEDIUM. It states a directional preference and shows the command to use. The hedge is kept. | `COR-M-0004`; `PI-006`; `PROTOCOL_ADDENDUM_A1.md` A1.4 |
| 4 | 32 `CANONICAL_ONLY` records marked `WEAKER` | Semantic coverage and strength equivalence are now separate fields on every record. Each of the 32 has a reviewed code: 14 advisory mechanism, 14 guidance restatement, 3 conditional narrowing, 1 permission. | `STRENGTH.dec`; `STRENGTH_DIVERGENCES.jsonl`; A1.2 |
| 5 | No explicit source-quote status; failed challenges could coexist with a passing report | Every record now has `source_quote_verification`, from re-reading the immutable file. An `OPEN_UNRESOLVED` challenge now fails validation. | A1.6, A1.7; `candidate.py validate` |

## Beyond the five findings

Checking finding 4 and finding 2 showed both were wider than the cited records, so I audited all of M.

**Strength audit (27 corrections).** A mechanical comparison of record modality with policy tag found 66 stronger and 45 weaker `CANONICAL_ONLY` links wrongly marked `SAME`. I reviewed them link by link.

- Most were false alarms: the mismatch was only against a secondary cited policy, or the record restated a clause inside the policy. These are annotated in `STRENGTH.dec` and do not change any record.
- 8 records had an overstated MUST, taken from a reported label on technique text; each is now DEFAULT.
- 4 records were wrongly `CANONICAL_ONLY` and were reclassified, including `FG-M-cf7afce3d7`, which has the same defect as finding 1.
- The remaining records got explicit strength values or narrower coverage links.

**Trigger audit (42 corrections).** 36 normative records had no reported trigger, and 7 had no exceptions statement, mostly Codex-only groups and provisional records. Each now states the condition from the source, or `NONE`.

**Effect on M**

| Measure | Before | After |
|---|---|---|
| `CANONICAL_ONLY` | 708 | 703 (664 equivalent, 39 weaker) |
| `CANONICAL_PLUS_DELTA` | 59 | 61 |
| `EXTRA_PRODUCT` | 116 | 119 |
| `NON_NORMATIVE` | 18 | 17 |
| `MIXED` | 5 | 6 |
| Classification changes | | 6 of 72 corrections |

Policy coverage stays 196 of 196 with direct evidence, and all 196 have equal-strength evidence.

**Second challenge round.** 20 further records were sampled from those not used in round 1, and all were upheld.

## Limits

- Challenge samples show which kinds of defects exist; they do not measure an accuracy rate. The audits found defects that the 18-record first round did not, so similar errors may remain in records no audit targets.
- Source-quote verification shows the cited text exists at the cited place, not that my reading of it is right.
- `SL`, `PC`, `CK` and `CR` codes are reviewer judgments and are open to human review (`PI-007`).
- `CANONICAL_ONLY` remains the label for entailed-but-weaker claims because the fixed label set has no alternative (`PI-001`). The `WEAKER_THAN_CANONICAL` value keeps them distinguishable.
