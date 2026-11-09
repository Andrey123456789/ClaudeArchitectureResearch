# Stage A — Claude Run 2 (blind replica): six-candidate status index

Index only; it does not substitute for candidate evidence under `stage_A/replica/<candidate>/`.
Order: K1 → K0 → L1 → L0 → M1 → M. No cross-candidate comparison or ranking is made here.

| Candidate | State | Files | Batches | Policies M/PA/NE/UN | Constraints (OL/EXTRA/LU) | Orphans | Validator 11 | Validator 12 | Validator 13 |
|---|---|---|---|---|---|---|---|---|---|
| K1 | REPLICA_COMPLETE | 87 | 13/13 | 196/0/0/0 | 386 (338/45/3) | 90 | PASS | PASS | PASS |
| K0 | REPLICA_COMPLETE | 63 | 13/13 | 196/0/0/0 | 389 (346/41/2) | 66 | PASS | PASS | PASS |
| L1 | REPLICA_COMPLETE | 86 | 10/10 | 196/0/0/0 | 254 (217/35/2) | 55 | PASS | PASS | PASS |
| L0 | REPLICA_COMPLETE | 71 | 12/12 | 196/0/0/0 | 248 (216/30/2) | 51 | PASS | PASS | PASS |
| M1 | REPLICA_COMPLETE | 80 | 21/21 | 196/0/0/0 | 247 (211/34/2) | 69 | PASS | PASS | PASS |
| M | REPLICA_COMPLETE | 61 | 19/19 | 196/0/0/0 | 241 (213/26/2) | 65 | PASS | PASS | PASS |

All validator results are structural only (PASS (STRUCTURE ONLY)); they are not proof of semantic completeness. Per-candidate validator output: `stage_A/replica/<candidate>/_annotations/_validation.txt`.

Snapshot integrity after the run: `py .\SETUP_5_4.py --verify` → `VERIFICATION PASS: 484 files are unchanged; all six candidates covered.` (all six snapshots and work queues unchanged).

## Per-candidate artifacts

Each `stage_A/replica/<candidate>/` holds `files.jsonl`, `policies.jsonl`, `constraints.jsonl`, `coverage_ranges.jsonl`, `PROGRESS.json`, `EXTRA_CONSTRAINTS.md`, `EXTRACTION_REPORT.md`, `ORPHAN_CANDIDATES.jsonl`, `ORPHAN_SWEEP_REPORT.md`, and the annotation sources in `_annotations/` (`B###.ann`, `SWEEP.ann`, `POLICIES.ann`, `NOTES.md`, `_validation.txt`).

## Resume instructions

1. Tooling (Run-2 only, reads `inputs/**` and `_control` queues): `stage_A/replica/_tools/show.py` (viewer), `build.py` (compiles `_annotations/B###.ann`, `SWEEP.ann`, `POLICIES.ann` into the ledgers; `--final` requires all 196 policy rows), `sweep.py` (reverse-sweep helper), `report.py` (EXTRA_CONSTRAINTS.md, ORPHAN_SWEEP_REPORT.md, EXTRACTION_REPORT.md).
2. All six candidates are complete. To rebuild one: `py stage_A/replica/_tools/build.py --root . --candidate <C> --final`, then `py stage_A/replica/_tools/report.py . <C>`.
3. Validate: `py .\_STAGE_A_KIT\11_REPLICA_WORK_QUEUE_AND_PROGRESS.py check --root . --candidate <C>`, `py .\_STAGE_A_KIT\12_REPLICA_VALIDATE_STAGE_A.py --root . --candidate <C>`, `py .\_STAGE_A_KIT\13_REPLICA_VALIDATE_ORPHANS.py --root . --candidate <C>`.

## Blindness record

No exposure: `stage_A/primary/**`, `stage_A/independent/**`, `stage_A/reconciled/**`, `work/`, `5.3` and the stage_A resume note of another run were not opened. Only directory names of `stage_A/` were listed. `SETUP_5_4.py --verify` was run once at the end; it compares hashes of the snapshots with the frozen 5.3 sources without displaying their content.
