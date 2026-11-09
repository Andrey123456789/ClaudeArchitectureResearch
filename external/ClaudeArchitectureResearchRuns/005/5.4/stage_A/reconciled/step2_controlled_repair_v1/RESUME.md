> **State:** PASS_WITH_DOCUMENTED_NOT_RUN. Nothing to resume unless a reviewer reopens a rule. See `STATUS.json` and `FINAL_CONSISTENCY_REPORT.md`.
# Resume instruction (standalone)

Run root: `stage_A/reconciled/step2_controlled_repair_v1/`. Contract: `_STAGE_A_KIT/61_...TASK_EN.md`. User decisions: `_STAGE_A_KIT/62_...RU.md`.

1. Read `STATUS.json`: `resume_point` is the exact next rule. If it is the rule that just failed, repair or roll back that rule; do not start another.
2. Trust only `CHECKPOINTS/` and `GATE_LOG.jsonl`, never a chat claim. Verify first: `python -B _tools/fence.py verify` and re-run `python -B _tools/gate.py <last passed rule>`.
3. Never delete verified work. Never write outside this root. No `git add`, `commit`, `reset`, `rebase`, `push` on the research repository. Git commands run only in disposable fixtures under `_scratch/`.
4. Rule flow:
   - write `_rules/<RULE>/BASELINE.md` (step A), `_tools/suites/<RULE with _>.py` (step B, tests first; run and confirm the negatives fail),
   - `_rules/<RULE>/patches.py`, then `python -B _tools/patcher.py apply <RULE>` (step C; refuses unless the previous rule passed),
   - add dispositions for changed evidence with `_tools/disposition.py` (step E input), `_rules/<RULE>/review.py` (step D and E source review),
   - `python -B _tools/gate.py <RULE> [--touched C,C]` (steps E to H; writes the checkpoint only on PASS).
   - Roll back with `python -B _tools/patcher.py rollback <RULE> "<reason>"`.
5. Order: `_tools/order.py`. Matrix: `DECISION_IMPLEMENTATION_MATRIX.md`.
6. After the last rule gate: the final cold audit (`R27-FINAL`) and `FINAL_CONSISTENCY_REPORT.md`. Do not start Step 3.
