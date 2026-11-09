# V3-0-BASELINE-REPLAY: declaration

Written before any v3 change.

**Change.** None to candidate bytes or data. v3 starts from an exact copy of the verified v2 final state (`bootstrap_v3.py`, `V3_BASELINE_MANIFEST.json`).

**Why a gate.** The ported tools (three-level change history, two-level tool integrity, the widened fence, the v2-to-v3 crosswalk) must reproduce v2 exactly before they judge any v3 change. A tool defect found here cannot be mistaken for the effect of a correction.

**Expected.**

- All six candidate trees equal `V2_FINAL_MANIFEST.json` byte for byte; no v3 change-log row exists.
- The dataset replay from the frozen baseline, through all v1 and v2 rule data, equals v2's three stored view files record for record, and every row of `V2_TO_V3_CROSSWALK.jsonl` is `UNCHANGED`.
- Each data file copied from v2 equals its v2 bytes, and the 1,176 coverage cells equal v2's.
- All 27 v1 suites and all 9 v2 change suites pass on v3 bytes with the same tallies as v2's cold audit (2,184 pass, 0 fail, 20 not run) apart from rows the v3 suite itself adds.
- The fence matches the preflight snapshot.

**Files, claims and policies affected.** None.
