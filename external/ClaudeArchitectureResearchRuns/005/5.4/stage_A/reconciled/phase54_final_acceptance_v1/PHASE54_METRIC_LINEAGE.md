# Phase 5.4 metric lineage

Every number below belongs to one universe and one version. Numbers from different universes are never added, turned into rates against each other, or used as strictness or quality scores. Raw record counts (including raw `MUST_NOT` counts) are not strictness metrics. Verified values come from machine-readable records named in the last column; `predecessor/PREDECESSOR_VERIFICATION.json` and `closure_review/CLOSURE_REVIEW.json` recheck the ones marked ✓.

## 1. Versions

| Version | What it is | Pin |
|---|---|---|
| **Original Phase 5.3 candidates** ("frozen") | The six templates as delivered by Phase 5.3 refinement and used as Stage A input | `frozen_sha256` per file in `step2_controlled_repair_v3/V3_FINAL_MANIFEST.json`; Codex `source_files` M 61, M1 80, L0 71, L1 86, K0 63, K1 87 |
| Step 2 v1, v2 | Controlled repairs (R01–R27; C01–C07 + C06B) | their own folders (unchanged) |
| **Step 2 v3 = normalized Phase 5.4 candidates** | v2 + Codex Pass 2/3 integration + PV2-01..04, PV2-03B, V3-Q10 | `V3_FINAL_MANIFEST.json` SHA-256 recorded in the release manifest |
| Step 3 v1 | Six-way comparison of v3 | `METRICS.json`, `POLICY_SIX_WAY_MATRIX.jsonl`, `POLICY_CELL_INDEX.jsonl` hashes in the release manifest; Step 3 input hashes equal the released files ✓ (CR-03) |
| Kit 76 | FAIR-02 contract, CP-01 experiment | `benchmark_readiness_fair02_cp01_v1/FILE_MANIFEST.json` ✓ (PV-09) |
| **Release phase54-final-v1** | Byte-identical copy of v3 | `release/CANDIDATE_FREEZE_MANIFEST.json` (`4058f10d…537f`) ✓ |

## 2. Researcher-induced normalization (original 5.3 → normalized 5.4)

| | M | M1 | L0 | L1 | K0 | K1 | Total |
|---|---|---|---|---|---|---|---|
| Files | 61 | 80 | 71 | 86 | 63 | 87 | 448 |
| Files changed vs original 5.3 | 18 | 16 | 16 | 16 | 17 | 21 | 104 |
| Files changed vs v2 | 7 | 6 | 3 | 3 | 3 | 4 | 26 |
| Distinct change rules touching the candidate | 15 | 13 | 13 | 11 | 15 | 14 | 21 rule ids |
| Files added or removed | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

The 21 rule ids are listed per file in `V3_FINAL_MANIFEST.json` (`rules`). These are researcher changes approved in the decision register and kits 61–74; they normalized wording, gates and checkers toward the common engineering contract. **Consequence:** every Phase 5.4 result describes the normalized candidates. None of it shows which original, uncorrected Phase 5.3 architecture was intrinsically better.

## 3. Universes and values

| # | Universe | Unit | Value | Source |
|---|---|---|---|---|
| U1 | Canonical policies | policy id | **196** (194 inventory + GOV-017/GOV-018) | Step 3 `UPSTREAM_FINGERPRINT.json` oracle ✓ |
| U2 | Canonical policy cells | (policy, candidate) | **1,176**; same identifiers in primary extraction, v3 coverage, v3 parity matrix and Step 3 cell index ✓ (PV-07, CR-05) | `POLICY_CELL_INDEX.jsonl` |
| U2a | Cell evidence level | cell | 1,176 FULL_SOURCE_COMPARED · 0 partial · 0 mechanical-only · 0 unverified ✓ | `METRICS.json` |
| U2b | Canonical compliance | cell | 1,156 EQUIVALENT · 20 STRICTER_THAN_CANONICAL · 0 WEAKER | `METRICS.json` |
| U3 | Normative semantic parity | policy | **165 FULL · 16 PARTIAL · 15 MEANINGFUL** · 0 context-dependent · 0 unverified ✓ | `POLICY_SIX_WAY_MATRIX.jsonl` |
| U3a | Recorded differences | atomic dimension | 35: 15 material (all ENFORCEMENT), 11 enforcement + 7 normative + 2 delivery non-material | `METRICS.json` |
| U3b | Roots (one source fact counted once) | root | 21 policy-level, **11 material** (all ENFORCEMENT) ✓ | `ROOT_CAUSE_SUMMARY.json` |
| U3c | Pairwise rows | (material dim, pair) | 225: 79 B_STRONGER · 51 A_STRONGER · 75 SAME · 20 INCOMPARABLE | `POLICY_PAIRWISE_DIFFERENCES.jsonl` |
| U4 | Classification records | v3 claim row | 6,498 (6,495 active) — lookup only, never a metric | v3 `REPAIRED_CLASSIFICATIONS.jsonl` |
| U5 | Candidate-specific extras | cluster | 797 clusters from 1,777 records: 19 GENUINE (10 roots + Q-01) · 172 ARCHITECTURE_SPECIFIC · 261 SAME_NORM · 344 REDUNDANT/NON_NORMATIVE · 1 UNRESOLVED; **not part of U1–U3** ✓ (CR-06) | `EXTRA_OBLIGATIONS_SIX_WAY.jsonl` |
| U6 | Codex evidence | finding | Pass 1: 132 findings + 20 samples → 152 ledger rows; Pass 2: 63, Pass 3: 148 → 211 adjudicated (160 non-normative, 29 candidate-unrepresented duty, 18 facet, 4 covered; 0 study-level new obligations) ✓ | `PASS1_REVIEW_LEDGER.jsonl`, `PASS2_PASS3_ADJUDICATION.jsonl` |
| U7 | Static behavior | check | v3: 44 suites, **3,416 PASS · 0 FAIL · 32 NOT_RUN** ✓; cold audit 263 PASS · 0 FAIL · 35 NOT_RUN · 9 FINDING; Step 3 probes 24 command cases × 6 × 2 runs; pilot static baseline 54 direct hook runs | `FINAL_SUITE_TALLY.json`, `HOOK_PROBE*_RESULTS.json`, `live_host_pilot/runs/*/static_result.json` |
| U8 | Live host | matrix row | candidate rows 56: **36 PASS · 6 FAIL · 14 NOT_RUN** (18 headless sessions); synthetic host diagnostic 5 rows: 2 PASS · 3 FAIL (separate scope) | `LIVE_HOST_PILOT_MATRIX.jsonl`, `live_host_pilot/PILOT_TOTALS.json` |
| U9 | Report completeness (FAIR-02) | synthetic fixture check | 103/103 (attempt 3); no real run scored yet | kit 76 `fair02/validation/` |
| U10 | Build behavior (CP-01) | build/format case | 6 cases × 2 replicates, SDK 10.0.403 ✓ | kit 76 `cp01/OBSERVED_VS_EXPECTED.json` |
| U11 | Release files | file | 448 released = 448 v3 = 448 original paths; 448 byte-identical ✓ | `release/CANDIDATE_FREEZE_MANIFEST.json` |

## 4. Lineage of the main claims

| Claim | Chain |
|---|---|
| "Normative parity at materiality" | U1 → U2 (owner text read per cell, Step 3) → U3 labels → U3a (0 material normative) — about the **normalized** v3 texts only |
| "11 material enforcement roots, no dominance" | U3a material dims (15) → U3b roots (11) → U3c pairs; static evidence U7; F-class reference gate now also LIVE_HOST_VERIFIED (U8, F1 rows) |
| "Hooks apply as designed on the host" | U7 static decisions → U8 live rows A, B, C, E, F (30 PASS) |
| "Declared fail-closed PreToolUse" | Configuration fact (v3, Step 3) → U8 D1 (6 FAIL) + synthetic DX1–DX5: **not applied by host 2.1.293** |
| "Reporting instruction identical for six" | kit 76 instruction hash → CR-07 assembly (six byte-identical prompts) → not embedded in any template (CR-02) |
| "M detects IDE0005 via dotnet format, not build" | U10 (CP-01) → M template unchanged (CR-09) |

## 5. What the numbers do not support

1. A ranking of the six candidates (Step 3 PROTOCOL §10 not met; no practical benchmark yet).
2. Any quality, productivity or benchmark-performance claim from U3–U8.
3. Any statement about the original Phase 5.3 architectures' intrinsic merit.
4. Interactive-mode host behavior (U8 interactive rows NOT_RUN).
5. Completeness of U5/U6 beyond the recorded universe (three of six Codex strategy families ran; Q-07).
6. Conclusions from stored modality counts (Q-06).
