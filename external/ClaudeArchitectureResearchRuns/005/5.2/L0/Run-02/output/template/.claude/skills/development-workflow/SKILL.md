---
name: development-workflow
description: >
  Run for any implementation task (new app, feature, bug fix, refactor, performance
  change), from product inputs through co-changes, code review, and verification.
---

> Level: 3 Project · Owns: implementation procedure and completion sequence (workflow) · Scope: common · Loads: on invocation (routed from CLAUDE.md) · Depends on: CLAUDE.md, .claude/rules/** (owner reads)

# Development Workflow

Policy stays with its owners (CLAUDE.md, `.claude/rules/`). This workflow owns the order of work and the obligations attached to its steps.

## 1. Frame the task

1. Determine the requested scope and which areas it touches (backend, frontend, tests, delivery, documentation).
2. For a new application or a substantial feature, read `SPECIFICATION.md` (and any feature specification) before planning or implementing, and read `CUSTOM_SETTINGS.md` when tunable values are involved.
3. Check the request against CLAUDE.md → Challenge questionable requests and → Decision control. Raise concerns and Decision Requests now, before writing code (headless runs: CLAUDE.md → Decision control).

## 2. Read the governing owners

Path-scoped rules load only when matching files are read, so read the owners explicitly whenever they may not have loaded yet — always for greenfield work, new projects, or new features in an area you have not opened:

| Work touches | Read |
|---|---|
| Backend code | `.claude/rules/1-architecture/backend-layers.md`, `persistence-boundary.md`, `entry-points.md`, `outcomes.md`; `.claude/rules/2-technology/csharp.md`, `aspnet-core.md`, `ef-core.md`, `fluentvalidation.md`, `logging.md`; `.claude/rules/0-core/runtime-principles.md`, `security-principles.md`, `logging-principles.md` |
| Persistence model or Development data | `.claude/rules/3-project/data-lifecycle.md` |
| Backend tests | `.claude/rules/0-core/testing-principles.md`, `.claude/rules/2-technology/dotnet-testing.md` |
| Frontend | `.claude/rules/1-architecture/frontend-structure.md`, `.claude/rules/2-technology/angular.md` |
| Projects, solution, or layout | run `project-structure` instead of improvising |
| Dependencies | run `add-dependency` |

Use the relevant knowledge skill (`ef-core`, `http-api`, `angular`, …) for technique.

## 3. Inspect before changing

Before any non-trivial change, inspect the relevant existing code — callers, contracts, tests, configuration — and apply the rules and skills that govern it.

## 4. Implement

- Keep the change inside the requested scope (CLAUDE.md → Simplicity and scope).
- **Bug fixes:** for a meaningful bug with plausible recurrence, add a regression test that fails before the fix and passes after it, unless equivalent coverage already exists (default).
- **Performance-motivated changes:** identify the actual bottleneck or cost, preserve observable behavior, use the simplest effective optimization, keep or add tests for the affected behavior, and benchmark or profile when the optimization is non-obvious or complex.
- **Approved product decisions:** when a new behavioral rule is approved, update the durable source of truth in the same change — `SPECIFICATION.md` when appropriate; tunable values go through `custom-settings`.

## 5. Co-changes

- **Seed data:** whenever a Domain or persistence change affects seeded entities (new required or renamed properties, changed relationships or enum/status values, new meaningful states, changed invariants), update the maintained development seeder in the same change so that recreating the Development database at this revision yields valid, representative data (`3-project/data-lifecycle.md`).
- **Migrations:** create schema changes as new EF Core migrations from the Infrastructure project with the Api project as startup project, for example `dotnet ef migrations add <Name> --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api`. Treat migrations as source code: review each generated migration before committing it, paying particular attention to destructive schema changes, unexpected column recreation, data migrations, indexes, foreign keys, and delete behavior.
- **Tests:** changed behavior gets maintained automated coverage at the right level (`0-core/testing-principles.md`).

## 6. Review and verify

1. For substantial feature work or a newly implemented application, run `code-review` (or the `code-reviewer` agent) before the final verification, and address real findings.
2. Before declaring implementation complete, run `verify`. A change is not complete while verification fails or is unreported.

## 7. Report

Summarize what changed, the `verify` result block, unresolved Decision Requests, and remaining known issues.
