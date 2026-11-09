# Cold audit attempt 2 (2026-11-06): aborted after section E

Sections A to E had run (log: `final_audit_v3.attempt2.ABORTED.log`). Section A again had one FAIL from the same check, "no tool names a
Codex pass after 0003". This time the hit was the audit's own new behavioral test, which wrote synthetic names such as
pass_0004 literally in `final_audit_v3.py`. The run was stopped, because it could only repeat that FAIL. No candidate, data or gate
file changed. Fix for attempt 3: the test builds its names from numbers. A section-A dry run on the fixed tool gave no FAIL.
