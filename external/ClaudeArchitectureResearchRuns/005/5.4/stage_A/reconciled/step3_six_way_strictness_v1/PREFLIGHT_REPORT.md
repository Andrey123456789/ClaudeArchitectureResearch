# Preflight report — Step 3 (six-way strictness comparison, v1)

- **Tool:** `_tools/preflight.py` (read-only toward every predecessor). Raw result: `PREFLIGHT_RESULT.json`; every attempt: `PREFLIGHT_HISTORY/`.
- **Outcome:** **PASS** on the first attempt (2026-11-06). Step 3 is not blocked.

## What was verified

| Check | Result | Evidence |
|---|---|---|
| P01 v3 `STATE.json` | PASS | phase `COMPLETE`, result `PASS_WITH_DOCUMENTED_NOT_RUN`, `step3_started: false`, recommendation `CONDITIONAL_GO` |
| P02 nine checkpoints | PASS | V3-0-BASELINE-REPLAY, PV2-02, PV2-01, PV2-03, PV2-04, V3-D01, V3-D02, PV2-03B, V3-Q10; each `PASS_WITH_DOCUMENTED_NOT_RUN`, 1,176 policy rows |
| P03 final checkpoint vs dataset bytes | PASS | V3-Q10 tally 3,416 PASS / 32 NOT_RUN; 6,498 rows, 6,495 active, 1,176 cells; SHA-256 of `REPAIRED_CLASSIFICATIONS.jsonl`, `REPAIRED_POLICY_COVERAGE.jsonl`, `ORIGINAL_TO_REPAIRED_CLAIMS.jsonl` and `V2_TO_V3_CROSSWALK.jsonl` match the checkpoint and `DATASET_MANIFEST.json` |
| P04 448 template files | PASS | M 61, M1 80, L0 71, L1 86, K0 63, K1 87; every SHA-256 matches `V3_FINAL_MANIFEST.json`; no missing or extra file |
| P05 changes against the frozen inputs | PASS | M 18, M1 16, L0 16, L1 16, K0 17, K1 21 = **104** files; every `frozen_sha256` recomputed from `inputs/<C>/output/template/` |
| P06 changes against v2 | PASS | M 7, M1 6, L0 3, L1 3, K0 3, K1 4 = **26** files; every `v2_sha256` recomputed from the v2 tree |
| P07 canonical oracle | PASS | 194 policies in `inventory.json` + GOV-017/018 in `shared-research-invariants.json` = **196** unique ids; both files byte-identical in all six inputs |
| P08 policy cells | PASS | `REPAIRED_POLICY_COVERAGE.jsonl` and `POLICY_PARITY_MATRIX.jsonl`: 1,176 rows each, 196 ids per candidate, no duplicate |
| P09 classification universe | PASS | 6,498 rows (6,495 active, **3 inactive kept**), unique keys; per candidate M 1,019, M1 1,131, L0 988, L1 1,053, K0 1,093, K1 1,214 |
| P10 v2→v3 claim crosswalk | PASS | 6,498 rows; UNCHANGED 6,046, ANCHOR_SHIFT_ONLY 404, CLAIM_REWORDED 21, CLASSIFICATION_CHANGED 1, ADDED_V3 26 |
| P11 suite tally | PASS | 44 suites; 3,416 PASS, 0 FAIL, 32 NOT_RUN (inherited evidence, not a Step 3 test) |
| P12 cold audit | PASS | 307 rows: 263 PASS, 0 FAIL, 35 NOT_RUN, 9 FINDING (inherited) |
| P13 Codex provenance | PASS | Pass 2 63 + Pass 3 148 = 211 adjudication rows, 30 adjudication checkpoints; Pass 1 review at `step1_union_augmented_pass1/REVIEW_REPORT.md`. Not re-adjudicated. |
| P14 decision queue | PASS | Q-01 to Q-13 present |
| P15 gate attempts | PASS | 16 attempts in `GATE_LOG.jsonl`: 9 passing, 7 failed (kept) |
| P16 environment | INFO | see below |

## Environment notes (not blocking)

- **S3-ENV-01.** `step2_controlled_repair_v1.zip` and `step2_controlled_repair_v2.zip` are absent. These are convenience archives. The v2 tree was verified file by file through P06 (all 448 `v2_sha256` values), and v3 recorded the same absence (PRE-W01, ENV-01 / Q-13).
- **S3-ENV-02.** `step2_controlled_repair_v3.zip` is present but is **not** the archive v3 recorded as ENV-02 (`e804fcc8…`, 21,287,678 bytes, 10:27). The current file is `05bf86e5…`, 30,344,199 bytes, modified 2026-11-06 21:15, after v3 completed. Step 3 compared its 8,698 entries with the v3 tree: **all 8,698 are byte-identical to the tree**, none absent, none different. It is a re-made archive of the final v3 tree, made outside any session. Step 3 reads the tree, not the archive.

## Fingerprint for resumption

- `UPSTREAM_FINGERPRINT.json`: aggregate SHA-256 of all 8,698 v3 files, SHA-256 of the key v3 reports and datasets, of each of the 448 candidate files, and of the kit, decision records and oracle files.
- `UPSTREAM_V3_TREE_HASHES.json`: per-file SHA-256 of the v3 tree.
- On every later run `preflight.py` re-verifies all checks and adds `P17-RESUME-INPUT-INTEGRITY`, which fails on any byte change since the fingerprint. It never overwrites the stored fingerprint.
