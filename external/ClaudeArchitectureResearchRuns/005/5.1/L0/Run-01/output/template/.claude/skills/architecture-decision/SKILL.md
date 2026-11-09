---
name: architecture-decision
description: >
  Use when a change needs a Reserved decision (new pattern, layer, project,
  infrastructure, major library, persistence or auth change, breaking API
  change, undefined product behavior): Decision Request and recording.
---

> Level: 3 Project · Owns: Decision Request and decision-recording procedure · Scope: common · Loads: on demand (model- or user-invoked)

# Architecture Decision

Decision classes, the Reserved list and the five-question test are always loaded (decision control). This workflow is the procedure around them.

## 1. Classify

1. Is the choice already **Decided** (architecture overview, project decisions, product sources)? → follow it.
2. Is it **Delegated** (local, reversible, no boundary/dependency/convention/contract/behavior change)? → decide, proceed, and mention notable choices in the final report.
3. Otherwise, or if any of the five questions is answered yes → **Reserved**: continue below.

Product-behavior and tunable-value gaps are handled under product governance; this workflow then records the approved outcome (step 3).

## 2. Write the Decision Request

```markdown
## Decision Request: <short title>

**Context:** what requires the decision, which accepted decision or rule it touches, why now.
**Options:**
1. <option> — benefits, costs, reversibility, affected boundaries/dependencies.
2. <option> — ...
3. Keep the current decision — what that means for the request.
**Recommendation:** <option> because <reason>.
**Blocked:** <work that cannot proceed until decided>.
**Proceeding with:** <policy-compliant, non-Reserved work that continues meanwhile>.
```

Keep options realistic; include the simplest compliant alternative. In a headless or autonomous run, do not wait for an answer: continue only with the "Proceeding with" path and list every unresolved Decision Request in the final report.

## 3. Record an approved decision

An explicit user instruction counts as approval. Record the outcome where its class lives, in the same change that applies it:

| Decision | Record in |
|---|---|
| Architecture style, pattern, layer, boundary, adopted or newly rejected pattern | `.claude/rules/1-architecture/overview.md` (+ the governing Level 1 module when a rule changes) |
| Stack, conditional technology, project default, layout | `.claude/rules/3-project/decisions.md` |
| Product behavior | `SPECIFICATION.md` |
| Tunable value | `CUSTOM_SETTINGS.md` (then `custom-settings`) |
| Rationale worth preserving | `docs/decisions/NNNN-<slug>.md` (when the project keeps decision records) |

Changing a rule module is instruction maintenance: keep one owner per rule, respect the level model, and run `node .claude/scripts/check-instructions.mjs` afterwards (`template-maintenance` describes the full procedure for the user).

Decision record template:

```markdown
# NNNN. <Title>

Status: Accepted (<date>, approved by <who>)
Context: <forces and constraints>
Decision: <what was decided>
Consequences: <what becomes easier/harder; follow-up work>
Alternatives considered: <options and why not chosen>
```

## 4. Apply

Implement only what was approved. Update dependent artifacts the decision affects (project references, packages through `add-dependency`, tests, documentation), then continue the normal work loop (`code-review`, `verify`).

## Report

Decision class, Decision Request status (approved / pending / rejected), where it was recorded, and what work was blocked or proceeded.
