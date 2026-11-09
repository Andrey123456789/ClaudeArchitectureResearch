---
name: development-workflow
description: >
  Implementation procedure for any feature, bug fix, refactor, performance
  change, API change, or new application: read product sources, inspect code,
  plan with decision control, implement, review, verify, report. Use whenever
  you are about to change application code.
---

> Kind: WF | Scope: common | Capability: — | Loading: on-demand workflow

# Development Workflow

Governing policy: `CLAUDE.md` (product sources, decision control, engineering defaults) and the decision register. This workflow owns the sequence.

## 1. Read the product sources

Before planning or implementing a new application or a substantial feature, read `SPECIFICATION.md` and `CUSTOM_SETTINGS.md`. Handle gaps and conflicts per `CLAUDE.md` (Product sources).

## 2. Inspect before changing

Before any non-trivial change, inspect the relevant existing code and read the applicable standards in `.claude/rules/<scope>/` for the areas you will touch, then load the relevant knowledge skills. For persistence, backend tests, and frontend work, the decision register names the knowledge facet to load.

## 3. Plan

- Questionable request? Apply the challenge obligation in `CLAUDE.md` (Engineering defaults) before implementing.
- Classify each consequential choice per `CLAUDE.md` (Decision control); Reserved choices go to `architecture-decision`.
- Route specialized work to its workflow:

  | Work | Workflow |
  |---|---|
  | NuGet/npm package change | `add-dependency` |
  | Persistence entities, mappings, migrations, seed data | `persistence-change` |
  | `CUSTOM_SETTINGS.md` value | `custom-settings` |
  | New or restructured projects/directories | `project-structure` |
  | CI/CD, containers, deployment | `delivery-change` |

## 4. Implement

Keep the change inside the requested scope. Conditional obligations:

- **Bug fix:** default — for a meaningful bug whose recurrence is plausible, add a regression test that fails before the fix and passes after it, unless equivalent coverage already exists.
- **Performance-motivated change:** identify the actual bottleneck or cost, preserve observable behavior, use the simplest effective optimization, add or maintain tests for affected behavior, and benchmark or profile when the optimization is non-obvious or complex.
- **Deprecating an externally consumed API version:** mark the deprecation in versioning metadata, document the replacement version, communicate a realistic migration period and removal timeline, and keep the old version working for the promised support period; never remove it without considering its published support contract. Breaking changes and adopting versioning are Reserved (`architecture-decision`).

## 5. Synchronize durable sources

When a new behavioral rule is approved, update the durable source of truth in the same change, including `SPECIFICATION.md` when appropriate. Approved tunable values follow `custom-settings`; accepted engineering decisions follow `architecture-decision`.

## 6. Review

For substantial feature work or a newly implemented application, run `code-review` (or delegate to the `code-reviewer` agent) before the final verification, and fix confirmed findings.

## 7. Verify

Before declaring implementation complete, run `verify` at the depth the change's scope and risk require.

## 8. Report

Summarize what changed and why, the `verify` report, approvals obtained, and every unresolved Decision Request.
