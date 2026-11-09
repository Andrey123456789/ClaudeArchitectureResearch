---
name: develop
description: >
  Run for any implementation task (feature, bug fix, refactor, performance
  change, new app): inspect, read product sources, implement via change-type
  steps, review, verify.
---
> Level: 0-core | Owns: development procedure — inspection, product-source reading, change-type routing, review and completion gates | Scope: common | Loads: on demand (skill, routed from CLAUDE.md)

# Develop

## 1. Inspect

- Inspect the relevant existing code before making any non-trivial change, and
  apply the rules and skills that govern the affected area. Path-scoped rules
  load with the files; read a capability facet when a step below names it.
- Determine the affected scopes (backend roles, backend tests, frontend,
  delivery, repository) — later checks depend on them.

## 2. Read product sources

- Before planning or implementing a new application or a substantial feature,
  read `SPECIFICATION.md`; read `CUSTOM_SETTINGS.md` when tunable values are
  involved.
- Apply product governance and decision control (always loaded): challenge
  questionable requests, never invent product behavior, and raise a Decision
  Request for every Reserved choice.

## 3. Plan

Classify the decisions the change needs and plan the smallest change that
satisfies the request within policy.

## 4. Implement

| The change touches | Do |
|---|---|
| entities, mappings, migrations, or seeding | read and follow `persistence.workflow` |
| a package dependency | `add-dependency` before installing |
| a `CUSTOM_SETTINGS.md` value | `custom-settings` |
| solution, projects, or repository structure | `project-structure` |
| CI/CD, container builds, or deployment | `delivery` |
| a Reserved decision | Decision Request; after approval `architecture-decision` |
| backend technique | knowledge skills (`http-api`, `aspnet-error-handling`, `persistence.knowledge`, `authentication`, ...) |
| frontend code | `frontend.knowledge` |

### Bug fix

Default: for a meaningful bug with plausible recurrence, add a regression test
that fails before the fix and passes after it, unless equivalent coverage
already exists.

### Performance-motivated change

1. Identify the actual bottleneck or cost.
2. Preserve observable behavior.
3. Use the simplest optimization that addresses the problem.
4. Add or maintain tests for the behavior affected by the optimization.
5. Benchmark or profile when the optimization is non-obvious or complex.

### Approved product rule

When a new behavioral rule is approved during the task, update the durable
source of truth in the same change — `SPECIFICATION.md` when appropriate, and
`CUSTOM_SETTINGS.md` through `custom-settings` for tunable values.

## 5. Review

For substantial feature work or a newly implemented application, run
`code-review` (preferably through the `code-reviewer` agent) before the final
verification, and resolve confirmed findings.

## 6. Verify and report

Before declaring implementation complete, run `verify` at the depth the scope
and risk require. Report with the `verify` reporting shape and list every
unresolved Decision Request.
