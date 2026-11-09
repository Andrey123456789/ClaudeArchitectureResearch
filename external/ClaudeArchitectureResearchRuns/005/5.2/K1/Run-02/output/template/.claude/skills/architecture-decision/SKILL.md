---
name: architecture-decision
description: >
  Raise a Decision Request for a Reserved choice, record an accepted decision in
  the decision register, or change a capability selection or provider variant
  against its slot contract. Use for new patterns, layers, projects,
  infrastructure, major libraries, auth architecture, breaking API changes, or
  reopening a recorded decision.
---

> Kind: WF | Scope: common | Capability: — | Loading: on-demand workflow

# Architecture Decision

Governing policy: `CLAUDE.md` (Decision control) defines Decided / Delegated / Reserved and the Reserved test. This workflow owns the request, recording, and selection-change procedures.

## 1. Classify

Apply the Reserved list and five-question test from `CLAUDE.md`. Delegated → proceed without this workflow. Decided → follow the existing record; reopening it is itself Reserved.

## 2. Decision Request

Present the request and stop the affected work until the user answers:

```text
Decision Request: <short title>
Context:         <requirement, constraint, or trigger; affected boundary/contract>
Options:         <2-3 realistic options with trade-offs, reversibility, cost>
Recommendation:  <option and why, citing the governing policy/decision>
Blocked:         <work that cannot proceed without the decision>
Proceeding with: <compliant non-Reserved work continuing meanwhile, or "nothing">
```

Headless or autonomous runs follow `CLAUDE.md` (Decision control); the *Proceeding with* field names the compliant path actually taken.

## 3. Record an accepted decision

After approval:

1. Add a row to the decision register's *Accepted decisions* table (date, decision, scope, record link); update the affected register section (stack, conditional technology, project default, or capability selection).
2. For a consequential or non-obvious decision, add `docs/decisions/NNNN-short-title.md` (context, decision, alternatives considered, consequences, date, approver).
3. When the decision changes instruction content (standards, knowledge, workflows), ask the user to run the user-invoked `template-maintenance` workflow; afterwards run `node .claude/scripts/check-instructions.cjs`.
4. Implement through the normal workflows (`development-workflow`, `add-dependency`, `project-structure`).

## 4. Change a capability selection

Capability slots (architecture, persistence, backend-testing, frontend) compose statically; a selection change is Reserved.

1. Read `.claude/capabilities/<slot>/CONTRACT.md` and the current module manifest (`.claude/capabilities/<slot>/<implementation>/MODULE.md`).
2. For the proposed implementation, map every contract item to a concrete mechanism. An item without a mechanism (for example a persistence implementation without a migration mechanism) must be named in the Decision Request under *Blocked* — never silently dropped.
3. After approval, in a user-invoked `template-maintenance` session: replace the module directory and its facets (role-based facet file names stay the same), update the register's capability selection row, remove every facet of the old implementation, and run `node .claude/scripts/check-instructions.cjs` until it reports no leak, manifest, or contract errors.
4. Migrate the product code through the normal workflows.

A provider variant change inside a slot (for example a different database provider for the same persistence technology) is a Reserved persistence-technology change but not a new slot: update the module's `Variant:` line, its variant-specific facet sections, the register row, and the affected provider-dependent tests.

## 5. Report

List the decision, its class, approval source, register/record updates, and any request still unresolved.
