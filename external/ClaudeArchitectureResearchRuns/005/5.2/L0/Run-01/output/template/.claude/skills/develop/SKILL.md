---
name: develop
description: >
  Use before planning or changing application code (feature, bug fix, refactor, new app): spec reading, rule loading, change-type obligations, review, completion via verify.
---

> Level: 3 Project | Owns: development procedure and change-type obligations | Scope: common | Loads: workflow skill (model-invoked; routed from CLAUDE.md) | Depends on: CLAUDE.md, 0-core/*, 1-architecture/*, 2-technology/*, 3-project/*

# Develop

## 1. Frame the Work

1. For a new application or a substantial feature, read `SPECIFICATION.md`
   (and `CUSTOM_SETTINGS.md`) before planning or implementing.
2. Classify the decisions the work needs (CLAUDE.md, Decision Control). For a
   Reserved decision, stop that part and run `architecture-decision`.
3. Check the request against the challenge obligation (CLAUDE.md).

## 2. Rule Reads (Load the Governing Rules)

1. Inspect the relevant existing code before a non-trivial change, and apply the
   rules and skills that govern it.
2. Path-scoped rules load when matching files are read. When you will create
   files in an area whose rules are not yet in context — a new application, a
   new project, the first file of a feature — read the modules for that scope
   explicitly before writing:

| Scope | Read before writing |
|---|---|
| Backend code | `0-core/` security, logging, dependency-hygiene, structure, error-exposure, health, performance, caching, integration principles; `1-architecture/` backend-layers, persistence-boundary, entry-points, outcomes; `2-technology/` csharp, dotnet-runtime, aspnet-core, ef-core, logging; `3-project/data-lifecycle.md` |
| Backend tests | `0-core/testing-principles.md`, `2-technology/backend-testing.md`, plus the backend-code row for the code under test |
| Frontend | `0-core/` security, logging, dependency-hygiene, structure principles; `1-architecture/frontend-structure.md`; `2-technology/angular.md` |
| Package manifests | `2-technology/package-management.md`, then run `add-dependency` |
| Container files | `2-technology/containers.md` |

All paths are under `.claude/rules/`. To list the modules that apply to a path:
`node .claude/scripts/check-instructions.cjs --rules-for <path>`.

## 3. Implement

- Keep the change inside the requested scope (CLAUDE.md, Scope and Simplicity).
- Package additions or updates: run `add-dependency`.
- `CUSTOM_SETTINGS.md` additions or changes: run `custom-settings`.
- When a new behavioral rule is approved, update the durable source of truth in
  the same change, including `SPECIFICATION.md` when appropriate.

## 4. Change-Type Obligations

### Persistence and Model Changes

- Whenever a Domain or persistence change affects seeded entities (new required
  properties, renamed or removed properties, changed relationships or
  enum/status values, new meaningful states, changed invariants), update the
  maintained development seeder in the same change.
- Treat EF Core migrations as source code. Review every generated migration
  before committing it, paying particular attention to destructive schema
  changes, unexpected column recreation, data migrations, indexes, foreign
  keys, and delete behavior. Create migrations from Infrastructure with the Api
  project as startup project:
  `dotnet ef migrations add <Migration> --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api`.

### Bug Fixes

- Default: for a meaningful bug with plausible recurrence, add a regression test
  that fails before the fix and passes after it, unless equivalent coverage
  already exists.

### Performance Changes

- A performance-motivated change identifies the actual bottleneck, preserves
  observable behavior, uses the simplest effective optimization, adds or keeps
  tests for affected behavior, and is benchmarked or profiled when the
  optimization is non-obvious or complex.

### API Deprecation

- When deprecating an externally consumed API version, mark it deprecated in
  the versioning metadata, document the replacement, communicate a realistic
  migration and removal timeline, and keep the old version working for the
  promised support period; do not remove it without considering its published
  support contract.

### CI/CD and Deployment

- CI definitions stay in source control, reproduce the repository's supported
  build and test commands, and must not hide build or test failures.
- In CI, use frontend scripts that actually exist in `package.json` and use
  `npm ci` when a maintained lockfile supports it; do not invent npm scripts or
  reflexively replace lockfile-based installs.
- Do not apply production database migrations automatically from normal
  application startup. Production migration is an explicit deployment
  operation at a controlled point, using approved credentials and failing
  visibly; deployment never runs Development seeding
  (`3-project/data-lifecycle.md`).

Technique: `ci-cd` and `docker` skills.

## 5. Review and Complete

1. For substantial feature work or a newly implemented application, run
   `code-review` (or delegate to the `code-reviewer` agent) before the final
   verification, and fix confirmed findings.
2. Before declaring implementation complete, run `verify` at the depth the
   scope and risk require.
3. Report: what changed, Delegated decisions taken, unresolved Decision
   Requests, and the `verify` report.
