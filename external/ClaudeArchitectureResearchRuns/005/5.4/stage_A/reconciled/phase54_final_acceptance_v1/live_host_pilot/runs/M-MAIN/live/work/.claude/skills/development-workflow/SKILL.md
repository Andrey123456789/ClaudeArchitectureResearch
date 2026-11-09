---
name: development-workflow
description: >
  Use for any implementation change - feature, bug fix, refactor, performance
  work, persistence or migration change, generated code, API version, CI/CD -
  from first inspection through the review and verification gates.
---

> Owns: implementation step order, change-specific co-change obligations, review and verification gates | Scope: common | Loads: workflow (routed from CLAUDE.md; Stop hook reminders point here)

# Development Workflow

Governing policy lives in CLAUDE.md, `docs/technology-stack.md`, and
`.claude/rules/`. This workflow owns the order of work and the obligations that
attach to specific kinds of change.

## 1. Prepare

1. For a new application or a substantial feature, read `SPECIFICATION.md`
   (and `CUSTOM_SETTINGS.md`) before planning or implementing.
2. Inspect the relevant existing code before making any non-trivial change.
3. Apply the applicable rules and skills: read every `.claude/rules/*.md` whose
   `paths` match the areas you will create or change (path rules load only when
   matching files are opened, so read them explicitly for new files and
   greenfield work), and load the knowledge skills for the technologies
   involved.
4. Classify open decisions with CLAUDE.md § Decision Control. Reserved →
   `architecture-decision` before implementing that part.
5. If the request looks questionable, raise the concern and an alternative
   before implementing (CLAUDE.md § Core Defaults).

## 2. Implement

- Route sub-tasks to their workflows: dependency changes → `add-dependency`;
  `CUSTOM_SETTINGS.md` changes → `custom-settings`; new projects or structural
  changes → `project-structure`.
- When a new behavioral rule is approved, update the durable source of truth —
  `SPECIFICATION.md` when appropriate, and `CUSTOM_SETTINGS.md` (through
  `custom-settings`) for tunable values.

## 3. Change-Specific Obligations

### Persistence model and migrations

- Whenever a Domain or persistence change affects seeded entities — new
  required properties, removed or renamed properties, changed relationships,
  new required related entities, changed enum/status values, new meaningful
  states, changed Domain invariants — update the development seeder
  (`DbSeeder`) in the same change, so that recreating the Development database
  at this revision produces valid, representative data. Migrating an existing
  Development database does not require the seeder to patch rows it already
  seeded.
- Treat EF Core migrations as source code: review every generated migration
  before committing it, paying particular attention to destructive schema
  changes, unexpected column recreation, data migrations, indexes, foreign keys,
  and delete behavior. When a migration changes entities represented in the
  seed graph, review `DbSeeder` together with it. Command technique: `ef-core`
  skill.

### Bug fixes

- For a meaningful bug with plausible recurrence, add by default a regression
  test that reproduces the failure before the fix and passes after it, unless
  equivalent coverage already exists.

### Performance-motivated changes

1. Identify the actual bottleneck or cost.
2. Preserve observable behavior.
3. Use the simplest optimization that addresses the problem.
4. Add or preserve tests for behavior affected by the optimization.
5. Benchmark or profile when the optimization is non-obvious or complex.

### Generated output

- When generated output (OpenAPI clients, source generators, EF Core
  migrations, Angular build output) is wrong, or when its source contract or
  configuration changes, by default fix or update the authoritative source and
  regenerate, then review the regenerated changes. Do not manually patch
  disposable generated output unless the repository or its generation workflow
  intentionally treats that output as maintained source. For a changed API
  contract consumed by Angular: verify the backend contract, regenerate the
  client with the project's normal workflow, review it, then fix handwritten
  frontend code against it.

### API version deprecation

- When deprecating an externally consumed API version, mark it deprecated in
  the versioning metadata, document the replacement version, communicate a
  realistic migration and removal timeline to consumers, and keep the old
  version working for the promised support period. Do not remove it without
  considering its published support contract. Technique: `api-versioning`.

### CI/CD and deployment

- CI definitions stay in source control, reproduce the repository's supported
  build and test commands, and must not hide build or test failures.
- Frontend CI uses scripts that actually exist in `package.json` and `npm ci`
  when a maintained lockfile supports it; do not invent npm scripts or
  reflexively replace lockfile-based installs.
- Do not apply production database migrations automatically from normal
  application startup by default: production migration is an explicit
  deployment operation at a controlled point, using approved credentials and
  failing visibly, and deployment never runs Development seeding in Production.
  An exception needs the user's explicit request naming it and its scope, recorded
  through `architecture-decision`; a generic workflow approval is not one, and it
  never allows Development seeding in Production.
  Technique: `ci-cd`, `docker`.

## 4. Review and Verify

1. For substantial feature work or a newly implemented application, run
   `code-review` (or delegate to the `code-reviewer` agent) and address the
   findings before the final verification.
2. Before declaring any implementation work complete, run `verify` at the depth
   appropriate to the change's scope and risk.
3. Build or test failures that need diagnosis go through `build-fix`, then back
   to `verify`.

## Output

Report what changed, Delegated choices worth noting, unresolved Decision
Requests, the `verify` report, and any change-specific obligation that was not
applicable and why.
