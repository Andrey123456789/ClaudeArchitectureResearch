---
name: architecture-decision
description: >
  Use when a change would be a Reserved decision (new project or layer,
  infrastructure category, major library, persistence or auth change, breaking
  API or versioning, project-wide convention, not-adopted pattern) or when the
  user approves one.
---

> Owner: Reserved-decision procedure and decision records | Scope: common | Loads: on demand — workflow (routed by `CLAUDE.md` § Decision Control) | Enforced: none (human approval)

# Architecture Decision

Decision classes, the Reserved list, the five-question test, and the Decision
Request fields: `CLAUDE.md` § Decision Control.

## 1. Classify

Apply the classes and the five-question test. Decided or Delegated → stop here
and proceed normally. Product behavior or tunable values the product sources do
not define → follow `CLAUDE.md` § Product Sources instead: the outcome is
recorded in `SPECIFICATION.md` or `CUSTOM_SETTINGS.md`, not in an ADR.

## 2. Prepare the Decision Request

```text
Decision Request: <short title>

Context:         what triggered it; the requirement it serves; constraints
Options:         1. <simplest compliant option, including "do nothing">
                 2. <option> — trade-offs, cost, reversibility
                 3. ...
Recommendation:  <option and why>
Blocked:         <work that waits for the decision>
Proceeding with: <non-Reserved work continuing meanwhile>
```

Name the instruction files the decision would change (for example
`docs/technology-stack.md` or a rule) and the code that would follow the new
convention.

## 3. Obtain Approval

- Interactive: ask and wait; continue only with the "Proceeding with" work.
- Autonomous or headless: do not decide. Continue on a policy-compliant
  non-Reserved path and include the Decision Request in the final report under
  "Open Decision Requests".
- An explicit user instruction to adopt the option counts as approval; record it
  in step 4.

## 4. Record the Decision

Create `docs/decisions/` if it does not exist and add
`docs/decisions/NNNN-<kebab-case-title>.md`, numbering sequentially:

```markdown
# NNNN. <Title>

Status: Accepted | Superseded by NNNN
Date: <YYYY-MM-DD>
Approved by: <user or role>

## Context
## Decision
## Consequences
## Alternatives Considered
## Instruction Changes
<files whose decision text or rules change, or "none">
```

To supersede a decision, add a new record and mark the old one
`Superseded by NNNN`; never rewrite history in an accepted record.

## 5. Update the Planning-Time Decisions

Make the accepted decision visible at planning time with a one-line entry that
links the ADR:

- technology adopted, replaced, or made conditional → `docs/technology-stack.md`;
- architecture default or "Not adopted" entry changed →
  `CLAUDE.md` § Architecture Decisions.

If the decision changes normative text in a rule or skill, list the change in the
ADR's "Instruction Changes" section and ask the user to apply it through
`/template-maintenance`; do not restructure rules or skills from this workflow.

## 6. Implement

Continue through the owning workflow: `add-dependency` for packages,
`project-structure` for projects and references, then `verify`. A breaking API
change, a new API version, or the deprecation or removal of a version follows
`.claude/rules/api.md` § Versioning — read it before changing the contract.

## Output

```text
Decision:         <title> — Accepted / Pending approval / Rejected
Record:           docs/decisions/NNNN-<title>.md / none
Updated:          <planning-time files>
Pending changes:  <instruction changes awaiting /template-maintenance>
```
