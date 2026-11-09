# Resume instruction (standalone) — Step 2 v3: Codex Pass 2+3 integration and post-v2 parity closure

Contract: `_STAGE_A_KIT/74_CLAUDE_STAGE_A_STEP2_PASS23_INTEGRATION_TASK_EN.md` (authoritative; approves PV2-01..04).
Decision record: `Stage_A_Step2_Post_V2_Approved_Decisions_EN.md` (repository root).
Run root: `stage_A/reconciled/step2_controlled_repair_v3/`. Write nowhere else. Do not start Step 3 or benchmarks.

Trust `STATE.json`, `CHECKPOINTS/`, `GATE_LOG.jsonl`, `GATE_ATTEMPTS/` and `ADJUDICATION_CHECKPOINTS/`, not chat.

## Phases

| Phase | What | Done when |
|---|---|---|
| P0 PREFLIGHT | `python -B _tools/preflight_v3.py` | `PREFLIGHT_RESULT.json` status PASS (done) |
| P1 BOOTSTRAP | `_tools/bootstrap_v3.py`, then gate `V3-0-BASELINE-REPLAY` | checkpoint (done) |
| P2 ADJUDICATION | `_tools/adj_workbench.py`, `_adjudication/decisions.py`, `_tools/adj_build.py` | 30 files in `ADJUDICATION_CHECKPOINTS/` (done) |
| P2b 86 RECORDS | `_adjudication/modality86/review.py`, `_tools/m86_build.py` (run with V3-D02) | `MARKED_NEVER_86_REVIEW.jsonl` |
| P3 CHANGES | one at a time, `_tools/order.py` `V3_ORDER` (nine changes; the last two, PV2-03B-CPM-IMPORT-PROVEN and V3-Q10-PACKAGEVERSION-VERSION, came from the user's 2026-11-06 instruction, evidence in `_investigation/`) | checkpoint per change (done) |
| P4 COLD AUDIT | `_tools/final_audit_v3.py` (about 40 minutes); attempt logs in `AUDIT_ATTEMPTS/` | `FINAL_AUDIT_RESULTS.jsonl` with no FAIL |
| P5 REPORTS | `_tools/v3_report.py`, `_tools/v3_metrics.py`, then `FINAL_PASS2_PASS3_INTEGRATION_AND_PARITY_REPORT.md` | `STATE.json` phase COMPLETE |

## Change flow (each change)

1. `_rules/<CHANGE>/DECLARATION.md`, then `_tools/suites/<CHANGE with _>.py`, then add the change to `V3_ORDER`.
2. `PYTHONPATH=_tools python -B _tools/suite_run.py <CHANGE> pre`: the negatives must fail on the old bytes.
3. Template change: `_rules/<CHANGE>/patches.py`, `python -B _tools/patcher.py apply <CHANGE>`; then `_tools/disp_draft.py <CHANGE> <C...>` and a reviewed `dispositions.py`.
4. Data: `updates.py` (UPDATES, ADDED with `review_reading` and `review_phrases`; v3 ids `V3A-<C>-NNN`), `review.py`; for UPDATES also `claims.py` and `python -B _tools/claimgate.py <CHANGE>`.
5. Suite adaptations that belong to a change are applied with it (`_adaptation_patches/`): `c07_for_d02.py` is still pending (apply with V3-D02).
6. `python -B _tools/gate.py <CHANGE>`. A failed gate writes no checkpoint: repair or `patcher.py rollback <CHANGE> "<reason>"`, then re-run the whole gate. Keep the attempt log in `GATE_ATTEMPTS/`.

## Rules

1. Never write outside this folder. Read-only: inputs, primary/replica/independent, Step 1, Pass 1 augmented union, Step 2, the audit, v1, v2, the kit and the whole Codex area. Never list or read `PASSES/pass_0004` or later.
2. No Git command on the research folder. Git runs only in fixtures under `_scratch/runs`.
3. Run every tool as `PYTHONPATH=_tools python -B _tools/<tool>.py` from this folder.
4. `sandbox.cleanup_runs` clears `_scratch/runs` at gate end: never run a suite or the audit while a gate runs.
5. A v1 or v2 suite or tool may change only with a row in `_tools/adaptations.py` (V3_ADAPTATIONS; tests need a reason and a named negative test).
6. Write code with the Write/Edit tools: Bash heredocs collapse backslashes. Keep apostrophes out of single-quoted Python strings in `adaptations.py`.
7. Changes outside this folder that no v3 tool made are recorded once in `EXTERNAL_EVENTS.json` (`_tools/external_events.py record`); the fence and R27 tolerate only those files with their recorded bytes. A new external change fails the gate again: record it only after checking what it is.
8. `suite_run.py <change> post` writes `_rules/<change>/suite_post.jsonl`: never use the label `post` on an earlier change (use another label for a re-check).

## Status

COMPLETE (2026-11-06): nine changes gated, cold audit attempt 3 with no FAIL, all reports written. See `FINAL_PASS2_PASS3_INTEGRATION_AND_PARITY_REPORT.md`. Nothing pending in this task; Step 3 not started. Open user decisions are in `UNRESOLVED_AND_USER_DECISION_QUEUE.jsonl`.
