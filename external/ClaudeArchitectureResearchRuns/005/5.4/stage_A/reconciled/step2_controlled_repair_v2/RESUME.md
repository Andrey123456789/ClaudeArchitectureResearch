# Resume instruction (standalone)

**State: complete.** All changes in `_tools/order.py` have a checkpoint, the cold audit ran on final bytes, and `FINAL_PARITY_AND_CONSISTENCY_REPORT.md` holds the results and the Step 3 recommendation. Nothing is left to run. Step 3 was not started and needs its own instruction. To confirm the state, run `PYTHONPATH=_tools python -B _tools/verify_final.py`. The rest of this file applies only if a change is reopened.

Run root: `stage_A/reconciled/step2_controlled_repair_v2/`. Contract: `_STAGE_A_KIT/71_CLAUDE_STEP2_PARITY_CLOSURE_TASK_EN.md`. Decisions: `_STAGE_A_KIT/72_APPROVAL_AND_HANDOFF_EN.md`, then `62_APPROVED_DECISIONS_AND_GATES_EN.md`. Do not start Step 3.

Do not rely on any chat claim. Verify first, from this folder:

```bash
PYTHONPATH=_tools python -B _tools/fence.py verify
```

Then read `STATUS.json` for the last change and result, and re-run the gate of the last checkpointed change before doing anything else:

```bash
PYTHONPATH=_tools python -B _tools/gate.py <last change in CHECKPOINTS/>
```

Rules:

1. Never write outside this folder. Never read, list or hash `stage_A/codex_iterative_search*`. No Git command on the research folder. Git runs only in fixtures under `_scratch/runs`.
2. `_tools/order.py` holds `V2_ORDER`. A change is added there only when it is declared in `_rules/<CHANGE>/DECLARATION.md`.
3. Change flow: `DECLARATION.md`; `_tools/suites/<CHANGE with _>.py`; add to `V2_ORDER`; `python -B _tools/suite_run.py <CHANGE> pre` and confirm the negatives fail on the old bytes; `_rules/<CHANGE>/patches.py`; `python -B _tools/patcher.py apply <CHANGE>`; `python -B _tools/disposition.py list` and write `dispositions.py`, `updates.py`, `review.py`, and `supersede.py` if a v1 review quote is retired; `python -B _tools/gate.py <CHANGE>`.
4. A failed gate writes no checkpoint. Repair that change or roll it back with `python -B _tools/patcher.py rollback <CHANGE> "<reason>"`, then re-run the whole gate. Do not start the next change.
5. A v1 suite may change only with a row in `_tools/adaptations.py`, a stated reason and a named negative test. The gate fails otherwise.
6. `sandbox.cleanup_runs` clears `_scratch/runs` at gate end. Do not run a suite or audit while a gate runs.

Change order and scope: contract section 3, C01 to C07, then a separate cold audit (`_tools/final_audit_v2.py`) and `FINAL_PARITY_AND_CONSISTENCY_REPORT.md`.
