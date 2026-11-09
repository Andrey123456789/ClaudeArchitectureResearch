# Cold audit attempt 1 (2026-11-06)

Result: 261 PASS, 35 NOT_RUN, 9 FINDING, 1 FAIL. Every suite re-run on final bytes (section I) passed with no failure.

The one FAIL was a false positive in the audit's own check A "no tool names a Codex pass after 0003". It matched two prose lines
that state the pruning rule: `fence.py` line 5 ("PASSES/pass_0004 and later are pruned before entry") and the note in `preflight_v3.py`
line 110 ("Codex area hashed with PASSES/pass_0004+ pruned before entry"). No code reads a later pass.

Fix for attempt 2, in `final_audit_v3.py`: lines that state the pruning are excepted, and a behavioral check was added that
`codex_prune` drops pass 0004 and later and keeps 0001 to 0003 (synthetic names). No candidate, data or gate file changed between
the attempts.
