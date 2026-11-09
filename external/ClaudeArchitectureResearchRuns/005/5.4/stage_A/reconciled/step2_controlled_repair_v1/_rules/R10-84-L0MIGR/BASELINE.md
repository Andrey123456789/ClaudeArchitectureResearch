# R10 item 8.4 L0 production migrations: baseline and impact

**Target.** No automatic Production migrations at normal app startup by default. Separately approved controlled deployment-time migration steps remain possible. Credential and no-Development-seeding guarantees stay.

**Original.** WF-019: "Do not automatically apply production database migrations from normal application startup by default; treat production migration as an explicit deployment operation using approved credentials and never run Development seeding in Production." L0 `project-structure:70`: "Never add Production credentials or Production migration automation." L0 `delivery-pipeline:33-35` already follows WF-019.

**Files.** L0 `project-structure/SKILL.md` only. L0 is `Level: 3 Project` there, so naming stays in bounds. `delivery-pipeline` is the existing procedure owner; the pointer is a routing pointer.

**Parity lead, not edited.** M (`project-structure:112`), M1 (`:92`), L1 (`:29`), K1 (`:40`) keep the same scaffold wording; K0 already says "no automatic production migration step". L1 `development-workflow:42` says "Never apply" with no "by default". The register approves L0 only. Recorded in `UNRESOLVED_DECISIONS.jsonl`.
