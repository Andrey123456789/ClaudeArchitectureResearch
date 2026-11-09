---
name: architecture-decision
description: >
  Use when a choice is Reserved or unclear (new pattern, project, infrastructure,
  major library, breaking API change, versioning, deprecation) or a Decision Request
  is answered.
---

> Level: 1 Architecture · Owns: Decision Request preparation, decision recording, API version deprecation procedure (workflow) · Scope: common · Loads: on invocation · Depends on: CLAUDE.md, .claude/rules/1-architecture/overview.md

# Architecture Decision

Decision classes, the Reserved list, the five-question test, and the Decision Request fields are owned by CLAUDE.md → Decision control. This workflow owns how a request is prepared and how the outcome is recorded.

## 1. Classify

1. State the choice in one sentence.
2. Check whether it is already Decided: the product inputs, `1-architecture/overview.md`, `3-project/decisions.md`, the governing rule files, or the established project structure.
3. Otherwise apply the Reserved list and the five-question test. Delegated → proceed and mention it in the report. Reserved → continue.

## 2. Prepare the Decision Request

- **Context** — the requirement or problem, the current decision it touches, and evidence (files, constraints, measurements).
- **Options** — normally two or three realistic options, including the smallest change that satisfies the requirement within current decisions; for each: consequences, cost to reverse, affected levels and files.
- **Recommendation** — one option with the reason.
- **Blocked** — the work that cannot proceed until the decision is made.
- **Proceeding with** — the non-Reserved work that continues meanwhile, or "nothing".

Do not implement the Reserved option before approval.

In an autonomous or headless run, proceed with a Reserved change only when the request already holds an explicit approval of that specific change and its scope. Record it as usual, quoting the approving text and its scope, implement only that scope, and list it in a decision log in the final report (approval quote, scope, what was implemented). A broad instruction such as "do whatever is needed" is not approval. A Reserved choice the approval does not cover stops that part of the work: do not decide it, continue with the "Proceeding with" work, and list the Decision Request as unresolved.

## 3. Record an accepted decision

An explicit user instruction counts as approval. After approval, in the same change:

1. Add an entry to the matching decision summary — architecture-level decisions (styles, patterns, layers, boundaries) in `.claude/rules/1-architecture/overview.md` → Accepted architecture decisions; stack, conditional technology, and project-default decisions in `.claude/rules/3-project/decisions.md` → Accepted project decisions. Entry: date · decision · scope · consequences · files updated.
2. Update the owning rule module at the right level when the decision changes a rule (for example a technology replacement edits the Level 2 module, the Level 3 decisions, and any workflow or asset where the technology is embedded), so that no rule contradicts the decision.
3. If the decision changes product behavior, synchronize the product inputs (`development-workflow` → Implement, approved product decisions).

A rejected request is not recorded as a decision; mention it in the report.

## 4. Deprecating a published API version

When deprecating an externally consumed API version:

1. mark the version deprecated in the versioning metadata;
2. document the replacement version;
3. communicate a realistic migration period and removal timeline to consumers;
4. keep the old version working for the promised support period;
5. do not remove it without considering its published support contract — removal is itself a Reserved breaking change.
