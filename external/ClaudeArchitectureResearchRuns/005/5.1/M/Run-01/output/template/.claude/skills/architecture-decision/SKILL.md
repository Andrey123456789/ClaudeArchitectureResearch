---
name: architecture-decision
description: >
  Use when a change may be Reserved (new pattern, project, persistence or
  infrastructure category, major library, auth architecture, breaking API or
  versioning, undefined product behavior or tunable value), when a request
  conflicts with an accepted decision, or when the user approves such a
  decision. Produces a Decision Request and records accepted decisions.
---

> Owns: Decision Request procedure and format, decision recording, headless handling of unresolved decisions | Scope: common | Loads: workflow (CLAUDE.md routing)

# Architecture Decision

Decision classes, the Reserved list, and the five-question test are owned by
`CLAUDE.md` (Decision Control). This workflow turns a Reserved or unclear
decision into an explicit request and records the outcome.

## 1. Classify

1. Check whether the choice is already Decided: `CLAUDE.md` (Architecture
   Defaults), `docs/technology-stack.md`, `SPECIFICATION.md`,
   `CUSTOM_SETTINGS.md`, or established project structure (rationale for past
   decisions: `docs/decisions/`). If Decided, follow it; stop here.
2. Apply the Reserved list and the five-question test. Any "yes" → Reserved.
3. If Delegated, proceed without a request, choosing the simplest compliant
   option, and mention the choice in the final report when it matters.

## 2. Raise a Decision Request

For a Reserved decision, stop implementing the affected part and present:

```markdown
### Decision Request: <short title>

**Context** — what requires the decision, which accepted decision or product
source is affected, and the constraint that makes it necessary now.

**Options**
1. <option> — consequences, cost to reverse, dependencies added/removed.
2. <option> — ...
(Include the current-baseline option whenever one exists.)

**Recommendation** — the preferred option and why; the smallest option that
satisfies the concrete current need.

**Blocked** — the work that cannot proceed until the decision is made.

**Proceeding with** — the policy-compliant, non-Reserved work that continues
meanwhile (or "nothing").
```

Raise concerns about the request itself first when it is questionable
(`CLAUDE.md`, Challenge Before Implementing).

## 3. Approval

- An explicit user instruction to adopt an option counts as approval.
- In an autonomous or headless run, never take a Reserved path: continue only
  with non-Reserved work and list every unresolved Decision Request in the final
  report.

## 4. Record the Accepted Decision

After approval, before or together with the implementation:

1. Architecture/stack decisions: write `docs/decisions/NNNN-<kebab-title>.md`
   (next free number) using the record format below, and update the Decided
   source it changes — `CLAUDE.md` (Architecture Defaults or Decision Control)
   or `docs/technology-stack.md` — so planning-time context stays accurate.
2. Product behavior: update `SPECIFICATION.md` (CLAUDE.md, Product Sources).
3. Tunable values: record in `CUSTOM_SETTINGS.md` and run `custom-settings`.
4. New dependencies: continue with `add-dependency`.

```markdown
# NNNN. <Title>

- Status: Accepted (<date>)
- Approved by: <who/which instruction>
- Supersedes: <record or "none">

## Context
## Decision
## Consequences
## Alternatives Considered
```

Superseded records stay in place with their status updated; they are history,
not active instructions. Do not create `docs/decisions/` until the first record
exists.
