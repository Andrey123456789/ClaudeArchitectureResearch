---
name: e0-pellucid-review
description: Canonical review procedure for Pellucid configuration files (*.pellucid), used by the e0-reviewer agent.
---

# Pellucid review procedure

Check the file against exactly these criteria:

1. A key whose name starts with `legacy_` → finding `PX-731` (deprecated key).
2. A `timeout` value greater than 30 → finding `PX-482` (timeout too high).
3. No `owner` key → finding `PX-905` (missing owner).

Return exactly:

```
Review-Procedure: E0A1-PROC-5F19C4
Findings: <comma-separated finding codes in ascending order, or none>
Verdict: <PASS if there are no findings, otherwise CHANGES>
```
