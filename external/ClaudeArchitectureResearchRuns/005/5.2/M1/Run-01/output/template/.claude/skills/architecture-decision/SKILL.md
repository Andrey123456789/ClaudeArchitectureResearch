---
name: architecture-decision
description: >
  Run when a choice may be Reserved (new pattern, project, infrastructure, major
  library, auth, breaking API, undefined product value, capability change) or an
  approved decision needs an ADR.
---

> **Workflow skill** · Owns: Decision Request procedure, ADR recording, decision-source synchronization · Scope: common · Loading: on demand (routed from `CLAUDE.md` → Decision Control)

# Architecture Decision

Decision classes, the Reserved list, the five-question test, and the headless rule
are defined in `CLAUDE.md` → Decision Control.

## 1. Classify

1. Identify the decision and the sources that already settle it: `SPECIFICATION.md`,
   `CUSTOM_SETTINGS.md`, `docs/technology-stack.md`, `docs/architecture.md`,
   `docs/capability-selection.md`, existing ADRs in `docs/decisions/`, existing
   code, and the rules.
2. Decided → follow it. Delegated → decide and continue. Reserved → step 2.

## 2. Raise a Decision Request

Stop only the blocked part of the work and present:

```text
Decision Request: <short title>

Context:        <what forces the decision; relevant sources>
Options:        <2-4 options with trade-offs, including the policy-compliant default>
Recommendation: <option and reason>
Blocked:        <work that cannot proceed until this is decided>
Proceeding with: <compliant non-Reserved work continuing meanwhile>
```

In an autonomous or headless run, do not wait and do not decide: continue only
with the "Proceeding with" path and list every unresolved Decision Request in the
final report.

## 3. Record the Approved Decision

After explicit approval (an explicit user instruction counts as approval):

1. Write an ADR in `docs/decisions/NNNN-<kebab-title>.md` (create the directory
   with the first ADR), numbering sequentially:

   ```markdown
   # NNNN. <Title>

   Status: Accepted (<YYYY-MM-DD>)

   ## Context
   ## Decision
   ## Alternatives Considered
   ## Consequences
   ```

2. Update the durable decision source the ADR changes: `docs/technology-stack.md`
   (stack or conditional technology), `docs/capability-selection.md` (slot
   selection or declared property), the selected architecture frame's planning
   facet `docs/architecture.md` (adopted architecture or patterns), or
   `SPECIFICATION.md` / `CUSTOM_SETTINGS.md` (product behavior or values; then run
   `custom-settings` when settings change).
3. A capability replacement or removal also needs the user-run
   `template-maintenance` workflow, which reads the slot contract and manifests.
4. Then implement through `development-workflow`.

## Output

Report each decision with its class; for Reserved ones, the Decision Request or
the ADR path that records the approval.
