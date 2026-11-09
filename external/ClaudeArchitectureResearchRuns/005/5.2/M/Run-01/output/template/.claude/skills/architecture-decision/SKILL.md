---
name: architecture-decision
description: >
  Use when a choice is Reserved (CLAUDE.md, Decision Control) or the user asks
  to adopt, change, or record an architecture, stack, convention, or
  public-contract decision.
---

> Workflow skill. Owns: the Decision Request procedure and format, decision recording, propagation of accepted decisions to planning-time owners · Scope: common · Loads: on invocation; routed by CLAUDE.md · Depends on: CLAUDE.md, docs/technology-stack.md

# Architecture Decision

Decision classes, the Reserved list, and the five-question test: CLAUDE.md
(Decision Control).

## 1. Confirm the Class

- Decided → follow it; nothing to request.
- Delegated → decide it, and mention it in the work report when notable.
- Reserved, but already required by the specification or the established
  project structure → treat it as Decided and cite the source.
- Reserved otherwise → continue with step 2.

## 2. Write the Decision Request

```text
Decision Request: <short title>

Context: <what must be decided and why now; the requirement that triggers it;
the accepted decision, default, or rule it touches>

Options:
1. <option> — <consequences, risks, cost to reverse>
2. <option> — ...
(include the policy-compliant option that changes nothing, when one exists)

Recommendation: <option and reason>

Blocked: <work that cannot proceed until the decision is made>

Proceeding with: <non-Reserved work that continues meanwhile, or "nothing">
```

Keep options concrete and comparable; do not present a Reserved choice as
already made.

## 3. Wait for Approval

- Do not implement the Reserved part before approval. An explicit user
  instruction to adopt the option counts as approval; record it in step 4.
- In an autonomous or headless run, do not decide. Continue only with the
  "Proceeding with" work and include the Decision Request in the final report.

## 4. Record the Decision

After approval:

1. Create `docs/decisions/NNNN-<kebab-case-title>.md` (next free number; create
   the directory on first use) from the template below.
2. When the decision changes a planning-time default, update its owner in the
   same change: CLAUDE.md (Architecture Decisions — move the item between
   Adopted and Not adopted, or add it) or `docs/technology-stack.md` (stack and
   conditional technologies).
3. Product behavior and tunable values are recorded in `SPECIFICATION.md` and
   `CUSTOM_SETTINGS.md` (`custom-settings`), not in decision records.
4. Rules are written so that an approved decision does not contradict them.
   If a rule still contradicts the accepted decision, list the needed rule
   change in the report for the user-invoked `/template-maintenance` workflow.

## Decision Record Template

```markdown
# NNNN. <Title>

Status: Accepted
Date: YYYY-MM-DD
Approved by: <person, and where the approval was given>

## Context

<forces, requirement, the default or decision being changed>

## Decision

<what was decided, stated as a rule other work can follow>

## Consequences

<what changes for code, dependencies, tests, operations; what becomes harder>

## Alternatives Considered

<options rejected and why>
```

## Superseding a Decision

Changing an accepted decision is itself Reserved. After approval, create a new
record, set the old record's status to `Superseded by NNNN`, and update the
planning-time owners as in step 4.

## Output

Report the Decision Request (pending) or the created record and the owners
updated (accepted).
