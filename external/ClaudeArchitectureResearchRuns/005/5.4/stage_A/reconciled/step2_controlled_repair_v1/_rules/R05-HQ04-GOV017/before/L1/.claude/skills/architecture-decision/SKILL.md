---
name: architecture-decision
description: Use when a Reserved decision is approved or must be proposed — new pattern, project or layer, persistence or infrastructure change, stack replacement, capability selection change, API versioning — to write the Decision Request, record an ADR, and update the decision files.
---

> Level: 0-core · Owns: decision recording procedure — Decision Request, ADR, stratified decision-file updates · Loading: on invocation

# Architecture Decision

Classification (Decided / Delegated / Reserved) and the approval duty: `CLAUDE.md` § Decision control.

## 1. Decision Request (before approval)

```text
Decision Request: <title>
Context: <problem, constraints, affected code>
Options: <2-3 options with trade-offs>
Recommendation: <option and why>
Blocked: <work that waits for the decision>
Proceeding with: <non-Reserved work continuing meanwhile>
```

In autonomous or headless runs, list unresolved Decision Requests in the final report instead of deciding.

## 2. Record an approved decision

1. Write an ADR at `docs/decisions/NNNN-<kebab-title>.md` (create `docs/decisions/` with the first ADR):

   ```markdown
   # NNNN. <Title>
   Status: Accepted (<date>) · Approved by: <user or reference>
   ## Context
   ## Decision
   ## Consequences
   ## Alternatives considered
   ```

2. Update the decision file at the level the decision belongs to — never a single cross-level register:
   - adopted style, role mapping, or patterns not adopted → the frame's style rule (`.claude/rules/1-architecture/frame/`);
   - stack, conditional technology, layout default → `.claude/rules/3-project/decisions.md`;
   - frontend stack → the frontend stack rule;
   - product behavior or tunable value → `SPECIFICATION.md` / `CUSTOM_SETTINGS.md` (then `custom-settings`).
3. Record the change as a decision summary line pointing to the ADR; do not restate rules that live elsewhere.

## 3. Capability selection change

Changing a slot implementation (or clearing the optional frontend) always needs an ADR. Then: replace or remove the module per its slot contract and manifest (`.claude/capabilities/<slot>/`), update the selection row and declared properties, update the `CLAUDE.md` import if an always-loaded facet changed, and run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.mjs"`. A changed declared property that affects observable behavior (for example string comparison) also needs product approval.

## Report

Decision, ADR path, decision files updated, follow-up work (structure, dependencies, migrations).
