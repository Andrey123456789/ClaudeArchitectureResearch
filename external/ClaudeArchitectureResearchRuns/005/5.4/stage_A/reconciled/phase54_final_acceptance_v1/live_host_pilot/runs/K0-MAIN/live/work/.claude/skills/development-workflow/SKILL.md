---
name: development-workflow
description: Use before planning or implementing any non-trivial change — new app, feature, bug fix, refactor, performance, persistence or public API change. Orders spec reading, inspection, implementation, co-change obligations, review, verify.
---

> Kind: WF | Scope: common | Owner: development procedure for non-trivial changes, including change-specific co-change obligations | Loading: workflow (model- or user-invoked)

# Development Workflow

Governing policy: CLAUDE.md (product sources, engineering defaults, decisions, challenge obligation). This workflow owns the order of work and the change-specific obligations below.

## 1. Establish intent

1. For a new application or substantial feature, read `SPECIFICATION.md` and `CUSTOM_SETTINGS.md` before planning or implementing.
2. Check the request against CLAUDE.md § Engineering defaults (challenge obligation) and § Product sources (gaps, string semantics, tunable values).
3. Classify every decision the plan needs as Decided, Delegated or Reserved (CLAUDE.md § Decisions). For Reserved decisions raise a Decision Request; after approval use `architecture-decision`.

## 2. Inspect before changing

1. Inspect the relevant existing code before any non-trivial change — the code being changed, its callers, contracts, tests and established conventions — and apply the standards and knowledge for the touched areas.
2. Standards load automatically when files in their scope are read. When planning before files are opened, read the standards for the scopes you will change: `.claude/rules/common/`, `backend/`, `backend-tests/`, `frontend/`.
3. Load the knowledge skill for each technology involved:

| Area | Knowledge |
|---|---|
| EF Core, queries, migrations, seeding | `ef-core` |
| Controllers, status codes, idempotency, ETags | `http-api` |
| Exceptions, ProblemDetails, validation | `aspnet-error-handling` |
| Backend tests | `dotnet-testing` |
| Logging, Serilog | `logging` |
| Outbound HTTP, resilience | `httpclient-factory` |
| Options, secrets, environments | `configuration` |
| Service registration, lifetimes | `dependency-injection` |
| Caching | `caching` |
| Swagger/OpenAPI | `swagger` |
| API versions, compatibility | `api-versioning` |
| Health endpoints | `health-check` |
| Authentication, authorization | `authentication` |
| Modern C# features | `modern-csharp` |
| Angular | `angular` |
| Dockerfiles, Compose | `docker` |
| Pipelines | `ci-cd` |

## 3. Implement

- Stay within the requested scope.
- Route sub-tasks: packages → `add-dependency`; projects or repository structure → `project-structure`; `CUSTOM_SETTINGS.md` values → `custom-settings`; pipelines, containers, deployment → `delivery-pipeline`.

## 4. Change-specific obligations

### Bug fix

- Default: for a meaningful bug with plausible recurrence, add a regression test that fails before the fix and passes after it, unless equivalent coverage already exists.

### Persistence or model change

- Whenever a Domain or persistence change affects seeded entities, update the development seeder in the same change. Affecting changes include new required properties, removed or renamed properties, changed relationships, new required related entities, changed enum or status values, new meaningful states and changed Domain invariants. Recreating an empty Development database at this revision must yield valid, representative seed data; the seeder does not patch rows that were already seeded.
- Treat EF Core migrations as source code: review every generated migration before committing it, paying particular attention to destructive schema changes, unexpected column recreation, data migrations, indexes, foreign keys and delete behavior. Review the seeder together with any migration that affects seeded entities.
- Seeding behavior: `rules/backend/persistence.md`. Technique: `ef-core`.

### Performance-motivated change

1. Identify the actual bottleneck or cost.
2. Preserve observable behavior.
3. Use the simplest optimization that addresses the problem.
4. Add or maintain tests for behavior the optimization affects.
5. Benchmark or profile when the optimization is non-obvious or complex.

### Public API contract change

- Classify the change as compatible or breaking (technique: `api-versioning`); a breaking change to a relied-on contract follows `rules/backend/api.md` § Versioning; it is Reserved.
- Deprecating an externally consumed API version: mark the deprecation in versioning metadata, document the replacement version, communicate a realistic migration and removal timeline, and keep the old version working for the promised support period. Do not remove a deprecated version without considering its published support contract.

## 5. Review and verify

1. For substantial feature work or a newly implemented application, run `code-review` (agent `code-reviewer`) before the final verification.
2. Before declaring implementation complete, run `verify` with checks appropriate to the scope and risk of the change.

## Output

- What changed and why; Delegated decisions taken; Decision Requests raised or still unresolved; the verification report (see also: `verify` § Report).
