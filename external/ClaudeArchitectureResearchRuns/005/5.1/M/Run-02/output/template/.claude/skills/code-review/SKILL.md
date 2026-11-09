---
name: code-review
description: >
  Use for code reviews, PR or diff reviews, or a defect-focused second pass
  over completed .NET or Angular changes (before the final verify on
  substantial work). Canonical review procedure with severity-ranked findings.
---

> Owner: canonical code-review procedure, review priorities, finding discipline, and output shape | Scope: common | Loads: on demand — workflow (routed by `CLAUDE.md` § Development Workflow; preloaded by the `code-reviewer` agent) | Enforced: `code-reviewer` agent has read-only tools

# Code Review

## Role

A review is an independent, read-only pass: report findings and do not edit
files unless the user asks for fixes. This skill is the canonical review
procedure; agents and other workflows run it rather than defining their own
criteria. Code review is not the completion checklist — `verify` runs the final
build, test, and diff checks.

## Priorities

Prioritize findings in this order and never rank style preferences above
behavioral defects:

1. correctness;
2. security and authorization;
3. data integrity and persistence;
4. architectural boundary violations;
5. concurrency and integration behavior;
6. missing meaningful test coverage;
7. maintainability;
8. credible, evidence-backed performance problems.

## Step 1: Establish Scope

Determine what is reviewed: files the user supplied, the working-tree diff, a
branch/PR diff, or a named feature. Read enough surrounding code — callers,
contracts, dependencies — to understand the changed behavior; never review
isolated lines.

## Step 2: Understand Intent and Read the Governing Rules

Identify the behavior added or changed, expected error cases, persistence or
external-system effects, and the tests meant to protect it. Path rules may not
have loaded for files you only read in a diff, so read the owners for the
touched areas:

| Changed area | Read |
| --- | --- |
| Backend layering, controllers, repositories, DI | `.claude/rules/architecture.md` |
| Unit of Work, EF Core, seeding, migrations | `.claude/rules/persistence.md` |
| Status codes, versioning, Swagger, health | `.claude/rules/api.md` |
| Exceptions, validation, cancellation, outbound failures | `.claude/rules/error-handling.md` |
| Async, caching, query efficiency | `.claude/rules/performance.md` |
| C# style, usings, options, logging calls | `.claude/rules/coding-style.md` |
| Secrets, auth, CORS, sensitive logging | `.claude/rules/security.md` |
| Backend tests | `.claude/rules/testing.md` |
| Angular | `.claude/rules/angular.md` |
| CI, Docker | `.claude/rules/delivery.md` |
| New projects or directories | `.claude/rules/repository-structure.md` |

Load a knowledge skill only when the changed area needs depth: `ef-core`,
`dotnet-testing`, `authentication`, `http-api`, `aspnet-error-handling`,
`httpclient-factory`, `caching`, `configuration`, `dependency-injection`,
`angular`, `docker`, `ci-cd`.

## Specification Conformance

When `SPECIFICATION.md` is non-empty it is the product contract, and approved
values in `CUSTOM_SETTINGS.md` are part of intended behavior
(`CLAUDE.md` § Product Sources). Review conformance in both directions:

1. required behavior is not missing or weakened;
2. the implementation does not silently add unapproved behavior — new
   minimum/maximum lengths or numeric limits, reserved names or values, newly
   required fields, extra workflow restrictions, additional user-visible
   validation, or new observable string-comparison semantics (case sensitivity,
   collation, culture/ordinal comparison, normalization, trimming), including
   ones introduced through database configuration or framework defaults.

A detail absent from the original specification is not a defect when the user
approved it and the durable sources were synchronized. Do not confuse internal
implementation details with product behavior.

## Step 3: Correctness

Look for concrete problems with a plausible execution path: wrong conditions or
state transitions, null/empty edge cases, incorrect async behavior or
cancellation handling, incorrect error mapping, resource-lifetime problems,
unintended side effects, races on shared state.

## Step 4: Architecture

Check against `.claude/rules/architecture.md` and
`.claude/rules/persistence.md`:

- Does Domain stay independent of Application, Infrastructure, and Api?
- Does Application stay free of Infrastructure and EF Core types?
- Are Controllers thin, with Application Services orchestrating use cases?
- Is persistence reached through specific repository abstractions, without
  `DbContext`, `DbSet`, `IQueryable`, or EF-specific APIs leaking out of
  Infrastructure?
- Do repositories stage changes, with `IUnitOfWork` as the commit boundary?
- Is the design proportional — no Rich Domain Model, DDD tactical patterns,
  CQRS/MediatR/VSA, extra layers, or project-wide Result model without approval
  (`CLAUDE.md` § Architecture Decisions)?

`node .claude/scripts/check-architecture.mjs` finds the mechanical violations. Do
not report a violation merely because the code differs from a pattern this
project has not adopted, and do not require such patterns.

## Frontend Changes

With Angular code in scope, check against `.claude/rules/angular.md`: feature
boundaries and component responsibility, HTTP behind a data-access boundary,
subscription and reactive-state lifetime, frontend error handling, route guards
not treated as server authorization, unnecessary global or shared state, and
meaningful frontend tests. Do not apply backend project-boundary rules to
Angular source.

## Step 5: Data and Security

When relevant, check transaction and commit behavior, destructive data changes,
raw SQL parameterization, authorization, input trust boundaries, secrets,
sensitive logging, concurrency, migrations, cache consistency, and — when a
migration or Domain change affects seeded entities — whether the seeder was
updated. Run the full `security-scan` workflow only when the user asked for a
security audit, the change is materially security-sensitive, or a concrete
finding justifies broader investigation.

## Step 6: Integrations

For external calls, check cancellation propagation, timeouts, idempotency,
retry safety, failure translation, and disposal/lifetime behavior
(`.claude/rules/error-handling.md` § External Dependency Failures). Do not demand
retries for operations that are not safe to retry.

## Step 7: Tests

Check that changed behavior has useful maintained coverage, focusing on behavior
rather than line count (`.claude/rules/testing.md`): a regression test for a bug
with plausible recurrence, and maintained coverage for behavior that was only
verified by a temporary probe. Do not request duplicate tests when equivalent
coverage exists.

## Step 8: Performance

Report performance only for credible problems: obvious N+1 access, unbounded
materialization, blocking async I/O, repeated expensive remote calls, heavy
allocation in a demonstrated hot path. Do not recommend caching, compiled
queries, pooling, `ValueTask`, or similar optimizations speculatively.

## Tooling

Compiler diagnostics, analyzers, IDE/Roslyn tooling, and repository scripts are
useful evidence, not authority; no MCP server or particular analyzer is
required. Read the code before turning a tool warning into a finding.

## Output

Order findings by severity. For each give: severity, file/location, what is
wrong, why it matters, and the smallest reasonable fix.

- **Critical** — data loss, security vulnerability, reliably broken core
  behavior, or another issue that should block use or merge immediately.
- **High** — likely defect or architectural/data-integrity issue that should be
  fixed before merge.
- **Medium** — real maintainability, robustness, or test gap, not a likely
  immediate production failure.
- **Low** — non-blocking improvement.

Do not invent findings to populate categories. When there are no meaningful
findings, say so and name the important areas you could not verify.

## Review Discipline

Do not rewrite working code during a review unless asked, report formatting that
tooling already owns, demand personal style preferences, assume every warning is
a bug, require patterns the project has not adopted, or add filler praise to
balance criticism.
