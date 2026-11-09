# R27 contract 6: final cumulative audit

**Type.** Audit. No template edit and no data change. Writes `FINAL_AUDIT_RESULTS.jsonl`, `SAME_TASK_MATRIX.json`, `WORKING_COPY_MANIFEST.json`.

**Starts from the final bytes.** `_tools/final_audit.py` reads the six working copies, the frozen inputs and the repaired view. It does not read gate results or checkpoints. It re-runs each hook and checker on fresh copies.

**Sections.**

| Section | What it checks |
|---|---|
| A | Inputs and writes: hashes rebuilt, files outside the root newer than the run start, no Step 3 |
| B | Provenance: each file that differs from its input is in the change log, with matching hash |
| C | Loaders: settings hooks, skills, imports, syntax, each candidate's own checkers, architecture invariants |
| D | The same hypothetical task across six: executed hook and checker results, plus required text with its loading class |
| E | The seven named interactions, each an attempt to break an earlier gate |
| F | Data: 79, 230, 103, 4 clauses, qualified cells, 31 open records, counts, replay, 1,176 cells |

**Status words.** `PASS`, `FAIL`, `NOT_RUN`, and `FINDING`. A `FINDING` is a real tension that a rule does not resolve and the user did not ask to change. It is listed in the report and does not count as `PASS`.

**The cold read is in `review.py`.** Excerpts for the changed rules were printed from the final bytes and read side by side.

**Limits.** The same model and the same session wrote the rules and this audit, so it is a self-audit. All 1,176 cells get mechanical checks. Only the changed policies were read side by side. A fresh-session reviewer is the next step if independent assurance is wanted.
