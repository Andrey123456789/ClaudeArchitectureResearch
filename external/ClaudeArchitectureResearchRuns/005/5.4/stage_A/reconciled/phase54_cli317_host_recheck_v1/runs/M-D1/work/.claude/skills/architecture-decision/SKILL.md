---
name: architecture-decision
description: >
  Use when a change is Reserved under CLAUDE.md Decision Control, or when a
  Decision Request is approved, rejected, or deferred: request format and
  decision recording.
---

> Owns: Decision Request format, decision recording procedure | Scope: common | Loads: workflow (routed from CLAUDE.md § Decision Control)

# Architecture Decision

Decision classes, the Reserved list, the five-question test, and headless-run
behavior: CLAUDE.md § Decision Control.

## 1. Confirm the Class

Apply CLAUDE.md § Decision Control. Delegated → proceed without this workflow.
Decided → follow it; reopening it is itself Reserved.

## 2. Decision Request

Stop the Reserved part of the work and present:

```text
Decision Request: <short title>

Context: <what requires the decision; which accepted decision, rule, or
         product source it touches>
Options: <realistic alternatives, including staying within current decisions,
         with trade-offs and reversal cost>
Recommendation: <preferred option and why>
Blocked: <work that cannot continue until this is decided>
Proceeding with: <compliant non-Reserved work continuing meanwhile, or "nothing">
```

In an autonomous or headless run, proceed with a Reserved change only when the
request already holds an explicit approval of that specific change and its
scope. Record it as usual, quoting the approving text and its scope, implement
only that scope, and list it in a decision log in the final report (approval
quote, scope, what was implemented). A broad instruction such as "do whatever is
needed" is not approval. A Reserved choice the approval does not cover stops
that part of the work: do not decide it, continue with the "Proceeding with"
work, and list the Decision Request as unresolved.

## 3. Record an Accepted Decision

An explicit approval — including an explicit instruction in the original request
— is recorded before the Reserved part is implemented:

1. Add a record `docs/decisions/<NNNN>-<short-title>.md` (create the directory
   with the first record) containing: Status (Accepted), Date, Context,
   Decision, Alternatives considered, Consequences.
2. Update the planning-time owner so the decision is visible when planning:
   - architecture style, pattern, layer, or approval-boundary decisions →
     CLAUDE.md § Architecture Defaults;
   - technology adoption, replacement, or activation of a conditional
     technology → `docs/technology-stack.md`;
   - product behavior or tunable values → `SPECIFICATION.md`, or
     `CUSTOM_SETTINGS.md` through `custom-settings`.
3. When the decision needs new constraints in a path-scoped rule, edit the
   owning `.claude/rules/` file in place — one owner, no copies elsewhere.
4. Implement the change through `development-workflow`.

## Rejected or Deferred

When the discussion is worth keeping, record it with Status Rejected or
Deferred, then continue with the compliant alternative.

## Output

The Decision Request (or the recorded decision and the files updated), and the
work that proceeded meanwhile.
