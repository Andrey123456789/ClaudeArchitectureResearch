---
name: architecture-decision
description: Use when a Reserved decision is needed (pattern, project, persistence, infrastructure, major library, auth, breaking API, undefined product behavior) or an accepted decision is approved or changed.
---

> Kind: WF | Scope: common | Owner: decision request, recording and propagation procedure | Loading: workflow (model- or user-invoked)

# Architecture Decision

Decision classes, the Reserved list and the headless rule: CLAUDE.md § Decisions. Accepted project and architecture decisions: `docs/architecture/decision-register.md`.

## 1. Classify

1. State the decision and the options in one or two sentences.
2. Apply CLAUDE.md § Decisions. If the decision is Decided, follow the existing entry; if Delegated, decide and proceed. Continue only for Reserved decisions or changes to accepted ones.
3. Find what it touches: the register entry and its **Affects** list, the relevant standards, knowledge, workflows and enforcement.

## 2. Request

Present a Decision Request and wait for approval:

```text
Decision Request: <title>
Context: <need, constraints, current decision it would change>
Options: <2-3 options with trade-offs, including keeping the current decision>
Recommendation: <option and reason>
Blocked: <work that cannot proceed until decided>
Proceeding with: <policy-compliant non-Reserved work continuing meanwhile, or "nothing">
```

An explicit user instruction to adopt a specific option counts as approval. In an autonomous or headless run, continue only with the "Proceeding with" path and report the request as unresolved.

## 3. Record the approved outcome

- **Product behavior** — when a new behavioral rule is approved, update the durable source of truth, including `SPECIFICATION.md` when appropriate.
- **Tunable value** — record it in `CUSTOM_SETTINGS.md`, then run `custom-settings`.
- **Project or architecture decision**
  1. Add or update the register entry: next free stable ID (never reuse a retired ID), one-sentence decision, **Details in** owner, **Affects** list. Keep the register a summary, not a policy manual.
  2. When rationale, alternatives or consequences need more than the register sentence, add an ADR `docs/decisions/NNNN-<slug>.md` (template below) and cite it in **Details in**.
  3. Superseding a decision: mark the old ADR `Superseded by NNNN` and replace the register entry; do not keep two active entries for one choice.

```markdown
# NNNN: <decision title>

Status: Accepted | Superseded by NNNN
Date: YYYY-MM-DD
Register: D-xx

## Context
## Decision
## Alternatives considered
## Consequences
```

## 4. Propagate

1. Edit every artifact in the entry's **Affects** list so that each keeps only its own responsibility: standards cite the ID, knowledge adjusts technique, workflows adjust commands, enforcement adjusts checks (for example the deny-lists in `.claude/scripts/check-dependencies.cjs`). Example: replacing the backend test framework touches the testing standard, the testing knowledge skill, scaffolding commands and test-related checks.
2. Add newly affected artifacts to **Affects**; remove ones that no longer depend on the decision.
3. Changes to `.claude/` instruction files are instruction-system maintenance: ask the user to run `/template-maintenance` for structural changes, and run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.cjs"` after any edit.

## Output

The Decision Request (when pending) or the recorded outcome: register entry, ADR path if any, artifacts updated, checker result.
