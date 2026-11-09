---
name: architecture-decision
description: >
  Use when a change needs approval (Reserved decision) or the user approves or rejects one: Decision Request and recording.
---

> Level: 0 Core | Owns: Decision Request procedure and output shape, recording of accepted decisions | Scope: common | Loads: workflow skill (model-invoked; routed from CLAUDE.md) | Depends on: CLAUDE.md

# Architecture Decision

Decision classes, the Reserved list, the five-question test, and the headless
rule are in CLAUDE.md (Decision Control).

## 1. Classify

1. State the decision in one sentence.
2. Check whether it is already Decided (CLAUDE.md, the always-loaded decision
   summaries, or a recorded accepted decision). If Decided, follow it.
3. Apply the Reserved list and the five-question test. If no answer is yes and
   the choice is local and reversible, it is Delegated: decide, proceed, and
   mention it in the work report.

## 2. Issue a Decision Request

For a Reserved decision, stop the affected part of the work and present:

```text
Decision Request: <one-line decision>

Context: <requirement, constraint, or problem that forces the decision>
Options:
  1. <option> — <consequences, cost, reversibility>
  2. <option> — <consequences, cost, reversibility>
Recommendation: <option and reason; the smallest option that satisfies the need>
Blocked: <work that cannot proceed until the decision is made>
Proceeding with: <non-Reserved, policy-compliant work continuing meanwhile, or "nothing">
```

Include "keep the current decision" as an option whenever an accepted decision
would change. In an autonomous or headless run, do not wait: continue with the
non-Reserved path named in "Proceeding with" and list every unresolved Decision
Request in the final report.

## 3. Record the Outcome

An explicit user instruction counts as approval. Record an accepted decision
before implementing it, in the summary that owns its level:

- architecture style, pattern, layer, or boundary → "Accepted Architecture
  Decisions" in `.claude/rules/1-architecture/overview.md`;
- stack, conditional technology, project default, or layout → "Accepted Project
  Decisions" in `.claude/rules/3-project/decisions.md`;
- product behavior → `SPECIFICATION.md`; tunable value → `CUSTOM_SETTINGS.md`
  (then run `custom-settings`).

Each record is one line: date, decision, scope, and a pointer to rationale
(`docs/decisions/NNNN-<slug>.md` when a longer rationale is worth keeping).
When a decision changes a rule rather than adding an exception, ask the user to
run `/template-maintenance`.

A rejected option is not recorded as a decision; keep the current one.
