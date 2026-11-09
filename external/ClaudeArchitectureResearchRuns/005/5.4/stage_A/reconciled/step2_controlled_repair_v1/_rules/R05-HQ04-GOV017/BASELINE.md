# R05 HQ-04 / GOV-017: baseline and impact

**Target.** A headless run may implement a specific, previously explicitly approved Reserved change. It may not invent or approve a new Reserved decision. Vague authorization is insufficient. Approval evidence and scope are recorded, a decision log is output, and an unexpected Reserved choice stops that part of the work. No new autonomous approvals.

**Original quotes.** GOV-017: "Reserved changes require explicit approval and headless runs must not silently alter architecture." Six differently worded headless sentences: M "never make a Reserved decision", M1 "never silently make a Reserved decision", L0 and K0 "never make a Reserved decision silently", L1 "take only a policy-compliant non-Reserved path", K1 "never silently make or alter a Reserved decision". The audit flagged M alone but noted all six differ.

**Files.** `CLAUDE.md` and `architecture-decision/SKILL.md` in all six. No hook or checker carries this rule.

**Related policies.** GOV-017, GOV-015 (independence checked), GOV-005 (Delegated scope untouched).

**Shared versus architecture-specific.** Same sentence in each always-loaded owner, recording stays where each candidate records decisions: ADR plus decision owners in M and M1, stratified summaries in L0 and L1, the single register in K0 and K1. No register or hierarchy changes.

**Regression risks.** An approved Reserved change could read as Git authority (the suite and review check it doesn't). Budget: L0 CLAUDE gets longer; the gate reports always-loaded size and L0's checker warns over its guideline.
