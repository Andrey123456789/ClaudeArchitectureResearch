# Stage A primary extraction — six-candidate status (index only)

Extractor: Claude (primary). This index records verified saved state and the resume point. It contains no comparison, normalization or cross-candidate conclusions and does not replace any candidate's evidence.

| Candidate | State | Files | Non-blank lines | Policies (196) | Constraints (OL / EX / LU) | Orphans | Validators |
|---|---|---:|---:|---|---|---:|---|
| M | PRIMARY_COMPLETE | 61 | 7508 | 196 MATCHED | 851 (628 / 221 / 2) | 283 | 03 PASS, 07 PASS, queue 19/19 PASS |
| M1 | PRIMARY_COMPLETE | 80 | 8349 | 196 MATCHED | 930 (679 / 248 / 3) | 283 | 03 PASS, 07 PASS, queue 21/21 PASS |
| L0 | PRIMARY_COMPLETE | 71 | 4621 | 196 MATCHED | 813 (604 / 208 / 1) | 235 | 03 PASS, 07 PASS, queue 12/12 PASS |
| L1 | PRIMARY_COMPLETE | 86 | 4279 | 196 MATCHED | 852 (617 / 233 / 2) | 258 | 03 PASS, 07 PASS, queue 10/10 PASS |
| K0 | PRIMARY_COMPLETE | 63 | 5183 | 196 MATCHED | 810 (566 / 243 / 1) | 270 | 03 PASS, 07 PASS, queue 13/13 PASS |
| K1 | PRIMARY_COMPLETE | 87 | 5514 | 196 MATCHED | 875 (599 / 274 / 2) | 297 | 03 PASS, 07 PASS, queue 13/13 PASS |

`SETUP_5_4.py --verify`: PASS (484 input files unchanged) after K1 completion (all six candidates re-validated with 03 and 07: PASS).

Structural PASS is not a semantic completeness proof; the blind sweep must challenge each inventory.

## Resume point

- All six candidates have PRIMARY_COMPLETE extraction artifacts under `stage_A/primary/<candidate>/` (files.jsonl, coverage_ranges.jsonl, constraints.jsonl, policies.jsonl, EXTRA_CONSTRAINTS.md, ORPHAN_CANDIDATES.jsonl, ORPHAN_SWEEP_REPORT.md, EXTRACTION_REPORT.md, PROGRESS.json; annotation sources and validator output in `_work/`).
- No primary extraction work remains. Open LINK_UNCERTAIN items per candidate are listed in each ORPHAN_SWEEP_REPORT.md and are not resolved at Stage A.
- Structural PASS does not prove semantic completeness; the next Stage A step (blind/independent challenge of each inventory) is outside this primary extraction and has not been started here.
