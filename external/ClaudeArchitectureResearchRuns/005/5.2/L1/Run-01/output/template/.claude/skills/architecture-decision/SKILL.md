---
name: architecture-decision
description: >
  Run for a Reserved decision: Decision Request, ADR for an approved decision,
  owning-artifact update, capability-selection change, API version deprecation.
---
> Level: 0-core | Owns: decision recording procedure (ADR + owning decision artifact) and API version deprecation procedure | Scope: common | Loads: on demand (skill)

# Architecture Decision

Decision classes, the Reserved list, and the Decision Request format are owned
by decision control (always loaded). This workflow turns a decision into a
durable record.

## 1. Classify

Confirm the decision is Reserved (decision control, five-question test). A
Delegated decision needs no ADR; a Decided one is followed, not reopened.

## 2. Request

Present the Decision Request (Context, Options, Recommendation, Blocked,
Proceeding with). Continue only with the non-Reserved work it lists. In an
autonomous or headless run, stop here and report the request as unresolved.

## 3. Record the approved decision

Record the approval (decision control defines what counts as approval) as an
ADR in `docs/decisions/NNNN-<short-title>.md` (create the directory with the
first ADR):

```markdown
# NNNN. <Title>

- Status: Accepted
- Date: <YYYY-MM-DD>
- Approved by: <who / which instruction>

## Context
## Decision
## Consequences
## Alternatives considered
```

## 4. Update the owning decision artifact

Decisions stay stratified at the level that owns them:

| Decision | Update |
|---|---|
| adopted architecture, patterns adopted/not adopted | `architecture.decision`, and `architecture.boundaries` when mapping or references change |
| project reference graph or a new production project | `architecture.boundaries` and `architecture.check` |
| approved or conditional technology, layout, build defaults | `.claude/rules/3-project/stack.md` |
| capability selection or provider variant | `.claude/rules/3-project/capability-selection.md`; the module swap itself is done by the user through `/template-maintenance` |
| product behavior or tunable value | `SPECIFICATION.md` / `CUSTOM_SETTINGS.md` (product governance, `custom-settings`) |

Do not create a single cross-level decision register.

## 5. Implement

Implement through `develop`, then `verify`.

## API version deprecation

When deprecating an externally consumed API version:

1. mark the version deprecated in the versioning metadata;
2. document the replacement version;
3. communicate a realistic migration and removal timeline to consumers;
4. keep the old version working for the promised support period;
5. never remove the version without considering its published support contract.

Technique: `api-versioning`.
