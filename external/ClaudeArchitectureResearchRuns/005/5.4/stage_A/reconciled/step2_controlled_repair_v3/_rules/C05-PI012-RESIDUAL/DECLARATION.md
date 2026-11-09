# C05-PI012-RESIDUAL: declaration (contract section 2, step A)

Written before any disposition of this change. Data only: no candidate byte changes.

**Scope.** Two unique K0 scan-layer records that appear as four rows in the 79 and 230 queues, and the 21 `do not X when Y` leads from v1's extension scan, reproduced by `_tools/pi012_scan.py` (22, 8, 21, as v1 reported). Each lead is read at source. A count is not closed for its own sake.

**Authority.** Register `HQ-06`; kit 72: "Do not automatically elevate specialized security-audit criteria into universal MUST_NOT obligations"; register 9.2 (K0 deserialization is a security-audit criterion); approved addendum A2 rule 3: a triggered prohibition keeps A1.3 force and stays visible as class `TRIGGERED`. Alternative option D is not imposed.

## Atomic dispositions

- **D1, D2.** `FG-K0-0ef1e5ed3d` and `FG-K0-6d06b21a93`. Close as a scan criterion only if source context supports it. If it does not, keep `UNCERTAIN` and do not make it a `MUST_NOT` strength fact.
- **D3 onward.** One row per lead. A change is made only where the stored fact is wrong: a lost condition, or a claim that does not say what the source says.

## Per-claim gate

`_tools/claimgate.py` applies dispositions one at a time, in process, and after each one checks: the source quote resolves on current bytes; all-candidate record invariants; coverage on 1,176 cells against the previous state; the 103 corrections and 31 original open records; the PI-012 review counts; template bytes unchanged. A failure stops the sequence.

Template suites do not re-run per claim, because a data disposition cannot change a template byte and the gate proves that with hashes. They all re-run in the full gate that closes the change.

## Negative cases

A lead forced to `DEFAULT` by form alone must fail. An open record closed with no adjudication row must fail. A scan criterion given a `MUST_NOT` strength link must fail. Removing an adjudication row must reopen the record.

## Repair after the first gate

The first C05 gate failed on one regression, R27 section E: `FG-M-290b3bdb9e` read `SAME` with a modality that differs from the policy class and no resolution code. No checkpoint was written.

**Cause.** `recompute_strength` rebuilds `strength_resolution` from `strength_resolution_code`. A frozen record holds its reading only in `strength_resolution`, so any update that set any field wiped the reading. This path has been in use since C01. The per-claim gate did not see it: coverage cells do not depend on this field, and the gate did not compare fields a disposition had not declared.

**Damage, all v1 against v2 records.** Five readings differed. Two are deliberate C01 edits that name the code (`FG-L0-9551e9cc12`, `FG-L1-f2ee786a8d`). Three are the defect, all from C05: `FG-M-290b3bdb9e` lost `SL`; `FG-M1-14b23b94ae` and `FG-M1-6af8ce03db` kept the code and lost its source. No coverage cell gained a direct witness.

**v1.** Ten frozen readings are gone in v1. Eight are named by R01 or R25. `FG-K0-341d9608ae` is named by R19. `FG-M-f19c99c143` is not named, but R17 re-read the record as `STRONGER`, which replaces the old reading. No v1 defect found, and nothing changes there.

**Repair.** v2 updates go through `apply_v2_set`, which keeps a stored reading unless the update names the code. v1 rules keep `apply_set`, so they replay byte for byte. `claimgate.py` now fails on any field a disposition changed without declaring it. The new C05 checks failed on the old view (`suite_pre_repair.jsonl`) before the repair. The per-claim gate ran again as attempt 2; its log rows supersede attempt 1, which stays in the logs.
