---
name: development-workflow
description: >
  Use for every implementation task — feature, bug fix, refactor, performance
  change, migration, API deprecation, CI/CD or deployment change — from product
  sources to review and verify.
---

> Workflow skill. Owns: the implementation procedure and change-type obligations (product-source sync, seed data, migrations, regression tests, performance changes, API deprecation, CI/CD, database deployment) · Scope: common · Loads: on invocation, routed by CLAUDE.md · Depends on: CLAUDE.md, docs/technology-stack.md, .claude/rules/

# Development Workflow

## 1. Establish Inputs

1. For a new application or substantial feature, read `SPECIFICATION.md` before
   planning or implementing; also read `CUSTOM_SETTINGS.md` and any feature
   specification supplied with the task.
2. Inspect the relevant existing code before making a non-trivial change.
3. Read the rule files for every affected area (CLAUDE.md, Workflows). For
   greenfield work read them before writing code, because matching files are not
   in context yet.
4. Classify consequential choices (CLAUDE.md, Decision Control). Route a
   Reserved choice to `architecture-decision` before implementing that part;
   ask about material product ambiguity (CLAUDE.md, Product Sources).
5. Raise material concerns about the request and propose alternatives before
   implementing it (CLAUDE.md, Change Discipline).

## 2. Implement

Apply the rules; use knowledge skills for technique. Route specialized work:

| Work | Workflow |
|---|---|
| New solution, new or reorganized projects | `project-structure` |
| Dependency added, updated, or removed | `add-dependency` |
| `CUSTOM_SETTINGS.md` value added, changed, or removed | `custom-settings` |
| Build or test failure | `build-fix` |

## 3. Change-Type Obligations

Apply every item that matches the change.

- **Approved product rules** — when a new behavioral rule is approved, update
  the durable source of truth in the same change, including `SPECIFICATION.md`
  when appropriate.
- **Seed data** — whenever a Domain or persistence change affects seeded
  entities (new required properties, removed or renamed properties, changed
  relationships or required related entities, changed enum or status values,
  new meaningful states, changed invariants), update the maintained development
  seeder in the same change, so that recreating the Development database at this
  revision yields valid, representative data. Existing local databases are not
  patched (`persistence.md`, Development Seeding).
- **Migrations** — EF Core migrations are reviewed source code: review every
  generated migration before committing it, with particular attention to
  destructive schema changes, unexpected column recreation, data migrations,
  indexes, foreign keys, and delete behavior. When the migration affects seeded
  entities, review the seeder together with it.
- **Bug fixes** — default: for a meaningful bug with plausible recurrence, add
  a regression test that fails before the fix and passes after it, unless
  equivalent coverage already exists.
- **Performance-motivated changes** — identify the actual bottleneck or cost,
  preserve observable behavior, use the simplest optimization that addresses
  it, add or keep tests for the affected behavior, and benchmark or profile when
  the optimization is non-obvious or complex.
- **API version deprecation** — mark the deprecation in versioning metadata,
  document the replacement version, communicate a realistic migration and
  removal timeline, and keep the old version working for the promised support
  period. Do not remove an externally consumed version without considering its
  published support contract.
- **CI/CD** — keep pipeline definitions in source control, reproduce the
  repository's supported build and test commands, and never hide build or test
  failures. For the frontend, use only scripts that exist in `package.json` and
  use `npm ci` when a maintained lockfile supports it; do not invent npm scripts
  or reflexively replace lockfile-based installs. Technique: `ci-cd` skill.
- **Database deployment** — do not apply production database migrations
  automatically from normal application startup by default. Production
  migration is an explicit deployment operation using approved credentials, and
  Development seeding never runs in Production.

## 4. Review

For substantial feature work or a newly implemented application, run the
`code-review` workflow (or delegate to the `code-reviewer` agent) before final
verification, and fix confirmed findings.

## 5. Verify

Before declaring implementation complete, run the `verify` workflow appropriate
to the scope and risk of the change.

## Stop Conditions

Stop and ask at the stop points of CLAUDE.md (Product Sources, Decision
Control). In an autonomous or headless run, continue only with non-Reserved
work and list every open Decision Request in the final report.

## Output

Report: what changed; Delegated decisions worth noting; every deviation from a
default with its reason; open Decision Requests; the `verify` report.
