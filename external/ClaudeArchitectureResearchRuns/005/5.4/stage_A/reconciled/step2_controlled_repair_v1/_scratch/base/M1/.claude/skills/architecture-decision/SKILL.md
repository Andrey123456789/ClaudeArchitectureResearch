---
name: architecture-decision
description: >
  Use when a change may be Reserved, when the user approves or rejects a
  Decision Request, when a product rule or capability selection changes, or
  before deprecating an API version.
---

> Workflow · Owns the decision procedure, Decision Request shape, decision recording, capability-selection changes, and public API version deprecation · Policy: `CLAUDE.md` § Decision Control

# Architecture Decision

## 1. Classify

Classify the decision with `CLAUDE.md` § Decision Control (classes, Reserved
list, five-question test). Decided and Delegated decisions need no request.

## 2. Raise a Decision Request

```text
Decision Request: <short title>

Context:
<what triggered the decision; the relevant facts, constraints, and owners>

Options:
1. <option> — <consequences, cost to reverse>
2. <option> — <consequences, cost to reverse>

Recommendation:
<preferred option and why>

Blocked:
<work that cannot proceed until the decision is made>

Proceeding with:
<policy-compliant, non-Reserved work that continues meanwhile, or "nothing">
```

## 3. Wait for the Decision

- Interactive session: wait for an explicit answer before implementing the
  Reserved part; an explicit user instruction counts as approval.
- Autonomous or headless run: continue only on the non-Reserved path named in
  "Proceeding with", and list every unresolved Decision Request in the final
  report.

## 4. Record the Accepted Decision

Record the outcome in the same change that implements it:

- architecture, stack, convention, or public-contract decisions → an ADR in
  `docs/decisions/NNNN-short-title.md` (Status, Context, Decision,
  Consequences), and update the affected decision record
  (`docs/technology-stack.md` or `docs/capabilities/<slot>.md`);
- new product behavior → when a new behavioral rule is approved, update the
  durable source of truth, including `SPECIFICATION.md` when appropriate;
- tunable values → `CUSTOM_SETTINGS.md` through the `custom-settings` workflow.

A rejected request is recorded only when the rejection itself is a durable
decision, for example a pattern explicitly ruled out.

## 5. Capability Selection Changes

Changing a slot selection, enabling or disabling the optional frontend slot, or
changing a declared property such as the persistence provider variant is
Reserved and requires an ADR. An observable declared-property change (for
example the effective string-comparison behavior) must not happen silently;
treat it as a product decision as well.

After approval, record the ADR and the new selection intent. Applying the
replacement changes the instruction system, so ask the user to run
`/template-maintenance` (§ Capability Replacement).

## 6. Public API Version Deprecation

When deprecating an externally consumed API version:

1. mark the deprecation in the versioning metadata;
2. document the replacement version;
3. communicate a realistic migration period and the removal timing to
   consumers;
4. keep the old version working for the promised support period.

Do not remove an externally consumed version without considering its published
support contract; removing it is a breaking public API change (Reserved).
