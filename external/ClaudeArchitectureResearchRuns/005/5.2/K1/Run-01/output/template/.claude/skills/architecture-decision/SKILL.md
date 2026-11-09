---
name: architecture-decision
description: Use when a change needs a Reserved decision (architecture style, new project or layer, persistence or infrastructure category, major library, project-wide convention, auth architecture, breaking API change or versioning, capability selection, product behavior or tunable value), to issue a Decision Request and record the approved outcome.
---
Kind: WF | Scope: common | Capability: — | Loading: on invocation (routed from CLAUDE.md and development-workflow)

# Architecture Decision

Classification (Decided, Delegated, Reserved), the Reserved list and the five-question test: `CLAUDE.md` → Decision control. This workflow owns the Decision Request and recording procedure.

## 1. Prepare the Decision Request

Read the current entry in the decision register and any related record in `docs/decisions/`. For a capability change, also read the slot's `CONTRACT.md` and the selected module's `MODULE.md` (`.claude/capabilities/<slot>/`). Then present:

```text
Decision Request: <short title>

Context: <what requires the decision; affected boundary, contract, behavior or capability>
Options:
  1. <option> — <consequences, cost to reverse>
  2. <option> — <consequences, cost to reverse>
Recommendation: <option and reason; the smallest policy-compliant choice>
Blocked: <work that waits for the decision>
Proceeding with: <non-Reserved work that continues meanwhile, or "nothing">
```

For a capability replacement, list every required mechanism of the slot contract that the new implementation lacks, with the proposed alternative.

## 2. Wait for approval

Do not implement the Reserved part before explicit approval. In an autonomous or headless run, continue only with the "Proceeding with" work and report the open Decision Request.

## 3. Record the approved decision

- Engineering decisions (architecture, stack, conditional technology, convention, capability selection or variant): update the decision register entry and add a decision record `docs/decisions/NNNN-<kebab-title>.md` (create the directory with the first record) containing date, status `Accepted`, context, decision, consequences, and the decision it supersedes, if any.
- Capability selection or variant change: after recording, the user runs `template-maintenance` to swap modules or provider bindings.
- Product behavior: when a new behavioral rule is approved, update the durable source of truth, including `SPECIFICATION.md` when appropriate.
- Tunable values: record them in `CUSTOM_SETTINGS.md` and run `custom-settings`.

## Public API version deprecation

When deprecating an externally consumed API version (a public-contract decision):

1. mark the deprecation in the versioning metadata;
2. document the replacement version;
3. communicate a realistic migration and removal timeline to consumers;
4. keep the old version working for the promised support period, and do not remove it without considering the published support contract.

Technique: `api-versioning` knowledge skill.

## Output

The Decision Request as above, or, after approval, the list of updated register entries, decision records and product sources.
