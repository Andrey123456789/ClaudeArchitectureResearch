# Metric impact, v2 to v3

Three layers, never mixed: data labels (classification records), policy cells (1,176 coverage and strength statuses) and template behavior (checker and hook outcomes from direct script runs). Live-host behavior is NOT_RUN. v2 results stay as reported in v2. Machine-readable: `V3_METRIC_CROSSWALK.json`.

## 1. Data labels

Rows: 6472 in v2, 6498 in v3; active: 6469 in v2, 6495 in v3.

| Candidate | Rows v2 | Rows v3 | Classification change | Modality change |
|---|---:|---:|---|---|
| M | 1015 | 1019 | CANONICAL_ONLY +2, EXTRA_WORKFLOW +2 | MUST +1, MUST_NOT +3 |
| M1 | 1126 | 1131 | CANONICAL_ONLY +1, EXTRA_WORKFLOW +4 | DEFAULT +3, MUST +1, MUST_NOT +1 |
| L0 | 984 | 988 | CANONICAL_ONLY +1, EXTRA_WORKFLOW +3 | DEFAULT +3, MUST_NOT +1 |
| L1 | 1048 | 1053 | CANONICAL_ONLY +1, EXTRA_WORKFLOW +4 | DEFAULT +4, MUST_NOT +1 |
| K0 | 1088 | 1093 | EXTRA_WORKFLOW +5 | DEFAULT +5 |
| K1 | 1211 | 1214 | CANONICAL_ONLY +1, EXTRA_WORKFLOW +2 | DEFAULT +2, MUST_NOT +1 |

Crosswalk statuses (`V2_TO_V3_CROSSWALK.jsonl`): ADDED_V3 26, ANCHOR_SHIFT_ONLY 404, CLAIM_REWORDED 21, CLASSIFICATION_CHANGED 1, UNCHANGED 6046.

By change: PV2-01-GIT-GATING/ADDED_V3 5; PV2-02-FAILCLOSED-INPUT/ADDED_V3 2; PV2-03-K0-CPM-ROOT/CLAIM_REWORDED 3; PV2-03B-CPM-IMPORT-PROVEN/CLAIM_REWORDED 3; PV2-04-M-FRONTEND-TESTS/ADDED_V3 1; V3-D01-PASS23-OVERLAY/ADDED_V3 18; V3-D01-PASS23-OVERLAY/CLAIM_REWORDED 14; V3-D02-MODALITY86/CLASSIFICATION_CHANGED 1; V3-Q10-PACKAGEVERSION-VERSION/CLAIM_REWORDED 3.

Classification or modality changed on an existing record: FG-M-8b2c02178e (M) CANONICAL_PLUS_DELTA/DEFAULT -> CANONICAL_PLUS_DELTA/MUST_NOT by V3-D02-MODALITY86. Added records carry their own labels (ADDED_V3).

Raw label or modality counts are not a strictness metric: the "do not" records were not reviewed (Q-06), and the counts depend on extraction granularity (Codex Pass 2/3 showed uneven scan-prompt extraction).

## 2. Policy cells (1,176)

Cells whose coverage status or strength status moved against v2: **0**. Cells whose witness links changed (more or other source records, same statuses): 6 (K1/GOV-015, L0/GOV-015, L1/GOV-015, M/DEP-024, M/GOV-015, M1/GOV-015).

Strength statuses in v3: EQUIVALENT_EVIDENCE_PRESENT 1171, STRONGER_AND_WEAKER_EVIDENCE 5. Same labels do not prove semantic parity: see `POLICY_PARITY_MATRIX.jsonl` check levels.

## 3. Template behavior

| Change | Candidates | Direction | What changed | Own suite pre (old bytes) | Own suite post (new bytes) |
|---|---|---|---|---|---|
| PV2-02-FAILCLOSED-INPUT | M, M1 | stricter | Malformed, empty or non-object shell PreToolUse input, and a missing, blank or non-string command, are refused in the script (M: exit 2; M1: deny). Before, M exited 1 on malformed input and M and M1 allowed a missing command. | FAIL 44, NOT_RUN 2, PASS 45 | NOT_RUN 2, PASS 89 |
| PV2-01-GIT-GATING | M, M1, L0, L1, K1 | stricter | Repository-changing Git commands return ask (K0 table, byte-identical block); read-only Git still runs without a prompt; an existing non-Git deny still wins. Before, only K0 asked. | FAIL 252, NOT_RUN 3, PASS 228 | NOT_RUN 3, PASS 480 |
| PV2-03-K0-CPM-ROOT | K0 | false positive removed | A nested Directory.Packages.props managing every project no longer errors (root-only mandate removed); per-project effective CPM still proven by MSBuild. | FAIL 20, NOT_RUN 1, PASS 65 | NOT_RUN 1, PASS 85 |
| PV2-04-M-FRONTEND-TESTS | M | stricter (text) | M project-structure step 7 bans frontend tests under backend/ (record V3A-M-030, MUST_NOT). No candidate enforces it by a checker. | FAIL 6, NOT_RUN 2, PASS 40 | NOT_RUN 2, PASS 46 |
| V3-D01-PASS23-OVERLAY | all six (data only) | none | Data overlay from Codex Pass 2/3 adjudication: 18 added scan-prompt records and 14 facet rewordings. No template byte changed. | n/a | n/a |
| V3-D02-MODALITY86 | M (data only) | none | One stored modality corrected (FG-M-8b2c02178e DEFAULT -> MUST_NOT). No template byte changed. | FAIL 3, NOT_RUN 1, PASS 93 | FAIL 1, NOT_RUN 1, PASS 95 |
| PV2-03B-CPM-IMPORT-PROVEN | K0, M | false positive removed | A central file MSBuild imports from outside the project ancestors (DirectoryPackagesPropsPath) is accepted when MSBuild proves CPM on and the file imported; before, K0 errored and M errored and its hook blocked the edit. Without the SDK the static error stays (Q-11). | FAIL 22, NOT_RUN 1, PASS 107 | NOT_RUN 1, PASS 129 |
| V3-Q10-PACKAGEVERSION-VERSION | M1, K0, M | stricter (M1, K0); false positive removed (M) | A PackageVersion with no version errors in M1 and K0 (before: accepted); K0 reads a Version child element (empty or floating child versions now error); M accepts a valid Version child element (before: error). | FAIL 36, NOT_RUN 1, PASS 124 | NOT_RUN 1, PASS 160 |

Template files changed against v2: M 7, M1 6, L0 3, L1 3, K0 3, K1 4 (total 26).

Enforcement metrics that compare candidates must use the v3 behavior above, not v2: Git gating (ask) now exists in all six hooks; invalid shell PreToolUse input (malformed, empty, array, no command, non-string command) is refused in the script by all six (cold audit section E), while a blank command and event/tool mismatches still differ (Q-02, Q-03); central-package checks agree in all six with the .NET SDK and differ without it (Q-11).

## 4. Live behavior

NOT_RUN: ask display and answer, deny, exit 2, onFailure, headless behavior, a live agent task, real application, registry, CI.
