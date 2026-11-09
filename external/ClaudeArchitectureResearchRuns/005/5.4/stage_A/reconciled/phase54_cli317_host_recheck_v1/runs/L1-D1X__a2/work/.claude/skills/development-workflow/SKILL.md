---
name: development-workflow
description: Use for any implementation work — new application or feature, bug fix, refactor, performance change, persistence change, CI/CD or deployment change. Owns step order: product sources, inspection, implementation, conditional co-changes, review, verification.
---

> Level: 0-core · Owns: implementation procedure and its conditional co-change steps · Loading: on invocation (routed from `CLAUDE.md`)

# Development Workflow

## 1. Product sources and decisions

- For a new application or substantial feature, read `SPECIFICATION.md` (and `CUSTOM_SETTINGS.md`) before planning or implementing.
- Check the request against the product-input, decision-control, and challenge policy in `CLAUDE.md`: raise concerns and Decision Requests before writing code; continue only with Decided or Delegated work.

## 2. Inspect

Inspect the relevant existing code before any non-trivial change. Identify the rules whose `paths` match the files you will change (`.claude/rules/**`) and read any that have not loaded yet; identify relevant knowledge skills.

## 3. Implement

- Follow the applicable rules. Route specialized work: dependencies → `add-dependency`; solution or project structure → `project-structure`; `CUSTOM_SETTINGS.md` → `custom-settings`; accepted Reserved decision → `architecture-decision`.
- When a new behavioral rule is approved during the work, update the durable source of truth in the same change — `SPECIFICATION.md` when appropriate, `CUSTOM_SETTINGS.md` for tunable values.

## 4. Conditional steps

**Persistence model, mapping, migration, or seed data** — run the `persistence.workflow` facet.

**Bug fix** — Default: for a meaningful bug with plausible recurrence, add a regression test that fails before the fix and passes after it, unless equivalent coverage already exists.

**Performance-motivated change**
1. Identify the actual bottleneck or cost.
2. Preserve observable behavior.
3. Use the simplest optimization that addresses the problem.
4. Add or keep tests for behavior affected by the optimization.
5. Benchmark or profile when the optimization is non-obvious or complex.

**Deprecating an externally consumed API version** — mark the deprecation in versioning metadata, document the replacement, communicate a realistic migration and removal timeline, and keep the old version working for the promised support period; never remove it without considering the published support contract.

**CI/CD, container, or deployment change** (technique: `ci-cd` and the Level-2 container technique)
- Keep CI definitions in source control, reproduce the repository's supported build and test commands, and never hide build or test failures.
- In CI, run only frontend scripts the frontend manifest declares; when a maintained lockfile exists, install with the lockfile-based clean install from `frontend.commands`. Never invent scripts or reflexively replace lockfile-based installs.
- Do not apply production database migrations automatically from normal application startup by default: production migration is an explicit deployment operation using approved credentials, and Development seeding never runs in Production. An exception needs the user's explicit request naming it and its scope, recorded through `architecture-decision`; a generic workflow approval is not one, and it never allows Development seeding in Production.

## 5. Review

For substantial feature work or a newly implemented application, run `code-review` (or the `code-reviewer` agent) before final verification.

## 6. Verify

Before declaring implementation complete, run `verify` at the scope and risk of the change.

## Output

Summarize what changed, Delegated decisions taken, open Decision Requests (Reserved), and the `verify` report.
