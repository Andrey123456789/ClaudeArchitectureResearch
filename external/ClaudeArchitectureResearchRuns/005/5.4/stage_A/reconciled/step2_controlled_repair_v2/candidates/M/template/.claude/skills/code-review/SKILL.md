---
name: code-review
description: >
  Use for code, PR, diff, or pre-merge reviews and the review gate after
  substantial work: correctness, specification conformance, security, data
  integrity, architecture, integrations, tests, performance.
---

> Owns: review procedure, review priorities, reviewer independence, findings format | Scope: common | Loads: workflow (routed from CLAUDE.md and development-workflow; preloaded by the code-reviewer agent)

# Code Review

## Independence

The review is independent and read-only: do not edit files or rewrite working
code during a review unless asked. This skill is the canonical review
procedure; the `code-reviewer` agent runs it in an isolated read-only context
and other workflows reference it instead of redefining review criteria.

Code review is not the completion checklist: `verify` runs the final
build/test/diff verification.

## Priorities

Prioritize findings in this order:

1. correctness;
2. security and authorization;
3. data integrity and persistence;
4. architectural boundary violations;
5. concurrency and integration behavior;
6. missing meaningful test coverage;
7. maintainability;
8. credible performance problems supported by evidence.

Do not elevate style preferences above behavioral defects or bury important
findings under them.

## Step 1: Establish Scope

Determine what is being reviewed: files supplied by the user, the working-tree
diff, a branch or PR diff, or a named feature or module. Read the changed code
and enough surrounding code — callers, contracts, dependencies — to understand
its behavior; do not review isolated lines.

## Step 2: Understand Intent

Identify the behavior added or changed, expected error cases, persistence or
external-system effects, and the tests intended to protect the behavior.

Read the `.claude/rules/*.md` files whose `paths` match the changed files, and
load specialized technique only where relevant:

```text
persistence / EF Core          -> ef-core
tests                          -> dotnet-testing
authentication / authorization -> authentication
HTTP semantics                 -> http-api
error handling                 -> aspnet-error-handling
outbound HTTP / resilience     -> httpclient-factory
caching                        -> caching
configuration / DI             -> configuration / dependency-injection
Angular                        -> angular
Docker / CI                    -> docker / ci-cd
security-sensitive changes     -> security-scan (see Step 5)
```

When `SPECIFICATION.md` is non-empty it is the authoritative product contract;
approved `CUSTOM_SETTINGS.md` values are part of the intended behavior.

## Specification Conformance

Review conformance in both directions against CLAUDE.md § Product Specification
and § Custom Settings:

- Is required behavior missing or weakened?
- Does the implementation introduce unapproved product behavior — new minimum
  or maximum lengths or numeric limits, reserved names or values, newly
  required fields, extra workflow restrictions, additional user-visible
  validation rules, or new or changed observable string-comparison semantics
  (case sensitivity, collation, culture/ordinal comparison, normalization,
  trimming)? A string semantic chosen through database configuration or a
  framework default still counts when the specification is silent.

A reasonable detail absent from the original specification is not a defect if
the user explicitly approved it and the durable project sources were
synchronized. Do not confuse internal implementation details with product
behavior.

## Step 3: Correctness

Look for concrete behavioral problems with a plausible execution path: wrong
conditions or state transitions, null/empty edge cases, incorrect async
behavior, incorrect cancellation handling, incorrect error mapping, resource
lifetime problems, unintended side effects, race conditions on shared state.
Do not invent hypothetical failures.

## Step 4: Architecture

For backend changes, check against `.claude/rules/architecture.md`:

- Does Domain stay independent of Application, Infrastructure, and API?
- Does Application stay free of Infrastructure and EF Core?
- Do Controllers stay thin, with Application Services orchestrating use cases?
- Is persistence accessed through specific repository abstractions, with
  `DbContext`, `DbSet`, `IQueryable`, and EF-specific APIs kept inside
  Infrastructure?
- Do repositories avoid committing normal use-case changes independently, with
  `IUnitOfWork` as the Application-facing commit boundary?
- Is the design proportional — no Rich Domain Model, DDD tactical patterns,
  CQRS/MediatR/VSA, extra layers, project-wide Result model, or similar
  consequential pattern without an approved need (CLAUDE.md § Decision
  Control)? Additional abstraction is not inherently better architecture.

Do not report a violation merely because the implementation differs from a
pattern this project has not adopted, and do not require MediatR, CQRS, Vertical
Slice Architecture, Minimal APIs, Rich Domain Models, Domain Events, or generic
repositories.

## Frontend Changes

When Angular code is in scope, check against `.claude/rules/angular.md`:
feature boundaries and component responsibility; HTTP calls behind a
data-access boundary; subscription and reactive-state lifetime; frontend error
handling; route guards not treated as server-side authorization; unnecessary
global or shared state; meaningful frontend test coverage. Do not apply backend
Clean Architecture project-boundary rules mechanically to Angular code.

## Step 5: Data and Security

Review changed data-access and security-sensitive code carefully. When
relevant, check transaction and commit behavior, destructive data changes, raw
SQL parameterization, authorization, input trust boundaries, secrets, sensitive
logging, concurrency, migrations, cache consistency, and — when a migration or
Domain change affects seeded entities — whether `DbSeeder` was reviewed and
updated.

Normal security review of changed code is part of every review. Run the full
`security-scan` procedure only when the user requested a security audit, the
change is materially security-sensitive, or a concrete finding justifies a
broader investigation; do not turn every review into a full OWASP audit.

## Step 6: Integrations

For external calls, check cancellation propagation, timeout strategy,
idempotency where relevant, retry safety, failure translation, and
disposal/lifetime behavior. Do not demand retries for operations that are not
safe to retry.

## Step 7: Tests

Determine whether changed behavior has useful maintained automated coverage,
focusing on behavior rather than line count. For bug fixes, look for a
regression test when recurrence is plausible; behavioral probes used during
implementation must be preserved per `verify` step 4. Do not request duplicate
tests when equivalent coverage already exists.

## Step 8: Performance

Report performance concerns only when credible, for example obvious N+1
database access, unbounded materialization, repeated expensive external calls,
blocking asynchronous I/O, or heavy allocation in a demonstrated hot path. Do
not recommend caching, compiled queries, pooling, `ValueTask`, or similar
optimizations speculatively.

## Optional Tooling

Use compiler diagnostics, analyzers, IDE/Roslyn tooling, or repository-specific
analysis when available. No MCP server or particular analyzer is required. Tool
output is evidence, not authority: read the code before turning a tool warning
into a finding.

## Output

Report findings ordered by severity. For each finding provide: severity,
file/location, what is wrong, why it matters, and the smallest reasonable fix.

- **Critical** — data loss, a security vulnerability, reliably broken core
  behavior, or another issue that should block use or merge immediately.
- **High** — a likely defect or architectural/data-integrity issue that should
  be fixed before merge.
- **Medium** — a real maintainability, robustness, or test gap that is not a
  likely immediate production failure.
- **Low** — a non-blocking improvement.

Do not invent findings to populate categories. When there are no meaningful
findings, say so and state any important areas that could not be verified. Do
not add filler praise to balance criticism.

## Review Discipline

Do not rewrite working code during a review unless asked, report formatting
already owned by tooling as a defect, demand personal style preferences, assume
every warning is a bug, or require patterns the project has intentionally not
adopted.
