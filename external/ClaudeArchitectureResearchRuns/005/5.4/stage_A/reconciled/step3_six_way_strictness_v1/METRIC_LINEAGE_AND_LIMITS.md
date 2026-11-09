# Metric lineage and limits — Stage A Step 3 (v1)

Every count below belongs to exactly one universe. Counts from different universes are never added, compared as rates, or used as strictness measures. Machine-readable values: `METRICS.json` (Step 3), v3 `V3_METRIC_CROSSWALK.json`, `FINAL_SUITE_TALLY.json`, `FINAL_AUDIT_RESULTS.jsonl`.

## 1. Universes

| Universe | Unit | Size | Used for |
|---|---|---|---|
| U1 Policies | canonical policy id | 196 (194 inventory + GOV-017/018) | Six-way labels |
| U2 Cells | (candidate, policy) | 1,176 | Evidence levels, owners, canonical compliance |
| U3 Atomic dimensions | analyst-written D1, D2 … per policy | per policy (see matrix) | Pairwise labels; only differences are recorded |
| U4 Classification records | v3 claim row | 6,498 rows (6,495 active, 3 inactive kept) | Owner lookup, extras input; never a strictness measure |
| U5 Extra-obligation clusters | deduplicated cluster | 797 clusters from 1,777 active extra records | Extras inventory |
| U6 Static behavior | direct script run | v3 suites (3,448 checks) + Step 3 probes (24 command cases × 6 candidates × 2 runs) | Enforcement facts |
| U7 Live host | agent session | 0 (NOT_RUN) | — |
| U8 Files | template file | 448 v3 files; 104 changed vs frozen; 26 changed vs v2 | Change bearing |

## 2. Lineage v2 → v3 → Step 3

| Quantity | v2 | v3 | Step 3 | Note |
|---|---|---|---|---|
| Classification rows (U4) | 6,472 | 6,498 | 6,498 read, unchanged | v3 crosswalk: 6,046 UNCHANGED, 404 ANCHOR_SHIFT_ONLY, 21 CLAIM_REWORDED, 26 ADDED_V3, 1 CLASSIFICATION_CHANGED |
| Active rows | 6,469 | 6,495 | 6,495 | 3 inactive rows kept (FG-M1-668bf4f9ad, FG-L0-149e95678a, FG-K0-a769f55ff5) |
| Policy cells (U2) | 1,176 | 1,176 | 1,176 | Identical cell universe |
| Cell strength status | 1,171 EQUIVALENT_EVIDENCE · 5 STRONGER_AND_WEAKER | same (no cell moved) | 5 STRONGER_AND_WEAKER cells challenged: all resolve to the recorded labels (API-014 FULL; API-019, GOV-007 PARTIAL) | Mixed labels reflect record linkage, not candidate-specific weakness |
| Cell check level | — | 1,079 MECHANICAL_WITNESS_ONLY · 54 SOURCE_REVIEWED_V2 · 30 CLAUSE_REVIEWED_V2 · 13 SOURCE_REVIEWED_V3 | 1,176 FULL_SOURCE_COMPARED (a) · 0 PARTIAL (b) · 0 MECHANICAL (c) · 0 UNVERIFIED (d) | See section 4 for what "FULL" means and its limits |
| Partial witnesses | — | 38 cells (override, clause witnesses) | 38 read; every one carries a Step 3 cell note naming the lines read | |
| Canonical compliance (cells) | — | — | 1,156 EQUIVALENT · 20 STRICTER_THAN_CANONICAL | Separate axis from pairwise strictness |
| Policy labels (U1) | — | (v3 has no six-way labels) | FULL 165 · PARTIAL 16 · MEANINGFUL 15 · CONTEXT_DEPENDENT 0 · UNVERIFIED 0 | New in Step 3; v2/v3 labels were not copied |
| Recorded differences (U3) | — | — | 35 (15 material, all ENFORCEMENT; 11 ENFORCEMENT, 7 NORMATIVE, 2 DELIVERY non-material) | 225 pair rows = 15 material dims × 15 pairs |
| Roots (one source fact counted once) | — | — | 21 policy-level (11 material) + 11 extras-level (10 genuine, 1 Q-01) | `ROOT_CAUSE_SUMMARY.json` |
| Extras (U5) | — | 1,777 active extra records | 797 clusters: 19 GENUINE · 172 ARCHITECTURE_SPECIFIC · 261 SAME_NORM · 344 REDUNDANT/NON_NORMATIVE · 1 UNRESOLVED (Q-01) | 455 proposals accepted, 342 decided by override |
| Changed files (U8) | 26 changed vs v2 | 104 changed vs frozen | 96 bear on a P1 comparison (current bytes read); 8 bear only on meta or wiring (section 5) | `V3_CHANGED_FILES_IMPACT.jsonl` |

## 3. v3 suites, attempts and audit (inherited, not re-run)

- **44 suites** in `FINAL_SUITE_TALLY.json`: 27 v1 suites (R01–R27), 8 v2-era suites (C01–C07 plus C06B), 9 v3 suites (PV2-01, PV2-02, PV2-03, PV2-03B, PV2-04, V3-0, V3-D01, V3-D02, V3-Q10). Final replay on the final bytes: **3,416 PASS · 0 FAIL · 32 NOT_RUN**.
- **Discrepancy documented, not corrected:** the v3 report (`FINAL_PASS2_PASS3_INTEGRATION_AND_PARITY_REPORT.md:222`) says "all 27 v1 suites, all 9 v2 suites and all 9 v3 suites", which sums to 45. The tally lists 44; the v2-era group has 8 suites. The total of 44 is consistent everywhere else (report lines 12 and 236).
- **Gate attempts (`GATE_LOG.jsonl`, 16 rows):** 9 rules, each with a final passing gate; 7 earlier attempts failed or crashed and were re-gated (V3-0 ×2, PV2-02 ×1, PV2-01 ×1, PV2-04 ×2, V3-D02 ×1). Early failures are not part of the final tally.
- **Cold audit:** attempt 1 had one false-positive FAIL (audit's own scan); attempt 2 was aborted; attempt 3 (final): 263 PASS · 0 FAIL · 35 NOT_RUN · 9 FINDING (307 checks).

## 4. Codex provenance (used as recorded, not re-adjudicated)

| Layer | v3 record | In the Step 3 extras universe |
|---|---|---|
| Pass 1 (pass_0001) | 26 new-clause proposals, 29 facets → AUG1-NC / AUG1-FX records (55 rows, 25 active extras) | 17 AUG1-NC + 8 AUG1-FX extra records; 12 facet overlays on union records |
| Pass 2 / Pass 3 | 211 adjudications (63 pass 2, 148 pass 3): NON_NORMATIVE 160, CANDIDATE_UNREPRESENTED_DUTY 29, FACET_OF_EXISTING 18, ALREADY_COVERED 4; overlays ADD 29, APPEND 18; 30 issue clusters CL01–CL30 | 20 V3A extra records; overlays PASS2_ADD 10, PASS3_ADD 19, PASS2_APPEND 1, PASS3_APPEND 6 |
| v1/v2 repairs | REP-* (66 active extras), NCP-* (4) | carried as V1_V2_REPAIR / V2_NEW_CLAUSE |

Step 3 changed no classification record and re-applied no Codex edit. Two v3 claim texts were found not to match the current lines (FG-L1-5a6df8a726, FG-M1-159a4ef4c3; see `OPEN_DECISIONS_AND_SENSITIVITY.md` section 4); they are noted, not edited.

## 5. Changed files that bear on no P1 comparison

M `.claude/MAP.md`, M `.claude/hooks/hook-io.mjs`, M `.claude/skills/template-maintenance/SKILL.md`, M1 `.claude/MAP.md`, M1 `.claude/hooks/pre-tool-use.js`, M1 `.claude/scripts/lib/hook-output.js`, L0 `.claude/INSTRUCTION_MAP.md`, L1 `.claude/scripts/lib/project.mjs`. Human maps and template maintenance are not loaded for study tasks; the hook files carry PV2-01/PV2-02 wiring, whose behavior is covered by the inherited v3 suites (Git gating, malformed input) and appears in the extras inventory (fail-closed clusters X0225–X0229, X0448), not in a canonical policy cell.

## 6. What "FULL_SOURCE_COMPARED" means here, and its limits

- For every cell, Step 3 read the current v3 lines of the cell's owner records for every atomic dimension, side by side with the other five (dossiers built from the v3 bytes), and opened the template files where an excerpt was truncated, an owner was missing (Step 2 overrides, 38 partial witnesses) or a condition could sit nearby. Anchors and stored quotes were re-resolved by gate B for every cited key.
- It does **not** mean every line of every file was read, nor that enforcement behavior was executed: checker logic outside the three probes is source-read; live-host effects are NOT_RUN.
- Readers are one analyst family (same-family self-review); see `SEMANTIC_CHALLENGE_LOG.jsonl`.

## 7. Conclusions that cannot be made

1. A global ranking of the six candidates (PROTOCOL section 10 not met: no material normative difference exists).
2. Any claim about code quality, productivity or benchmark performance from strictness or enforcement counts.
3. Any live-agent effect of hooks, prompts or Stop blocks (Q-08 NOT_RUN).
4. Completeness of the extras universe beyond recorded clauses (Q-07: three of six Codex strategy families).
5. Conclusions from stored modality counts (Q-06: 492 soft-stored "do not" records unreviewed as a class; Step 3 did not use stored modality).
6. Build-time behavior of code-style settings (no build was run).
