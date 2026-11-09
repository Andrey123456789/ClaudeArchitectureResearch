---
name: code-review
description: >
  Review a diff, PR, files, or finished feature for defects: correctness,
  security, data integrity, architecture boundaries, integration, tests,
  performance.
---
> Level: 1-architecture | Owns: code-review procedure, review priorities, findings format | Scope: common | Loads: on demand (skill; preloaded by the code-reviewer agent)

# Code Review

Review the actual changed behavior and report concrete defects or risks. Code
review is not the completion checklist — `verify` runs the build/test/diff
verification.

## Priorities

Prioritize findings in this order: correctness; security and authorization;
data integrity and persistence; architecture-boundary violations; concurrency
and integration behavior; missing meaningful tests; maintainability; credible
performance problems. Never elevate style preferences above defects.

## 1. Establish scope

Determine what is reviewed — files supplied by the user, the working-tree diff,
a branch/PR diff, or a named feature — and read enough surrounding code
(callers, contracts, dependencies) to understand the changed behavior. Do not
review isolated lines.

## 2. Understand intent

Identify the behavior added or changed, the governing rules, expected error
cases, persistence or external-system effects, and the tests meant to protect
it. Read the rules and knowledge skills that govern the changed area. The
product contract is defined by the product sources under product governance;
approved `CUSTOM_SETTINGS.md` values are part of the intended behavior.

## 3. Specification conformance (both directions)

1. Required behavior is not missing or weakened.
2. No unapproved product behavior was introduced — new length or numeric
   limits, reserved names or values, new or changed observable string semantics
   (case sensitivity, collation, culture/ordinal comparison, normalization,
   trimming — product governance), newly required fields, extra workflow
   restrictions, or additional user-visible validation rules.

A detail absent from the specification is not a defect when the user approved
it and the durable sources were synchronized. Do not confuse internal
implementation details with product behavior.

## 4. Correctness

Look for wrong conditions or state transitions, null/empty edge cases,
incorrect async or cancellation handling, incorrect error mapping, resource
lifetime problems, unintended side effects, and races on shared state. Do not
invent failures without a plausible execution path.

## 5. Architecture

- Role boundaries (`role-boundaries.md`) and the frame mapping
  (`architecture.boundaries`) hold: domain model independent; use-case units
  free of persistence-technology and transport types; entry points thin;
  use-case units orchestrate; specific persistence-access contracts;
  persistence technology confined to the persistence implementation;
  persistence-access implementations do not commit independently; the commit
  boundary remains the use-case-facing commit point. Run
  `node .claude/scripts/check-architecture.cjs` when references changed.
- Proportionality: simple CRUD/workflow applications keep the domain model
  simple; abstraction count matches actual complexity; consequential patterns
  (Rich Domain/DDD tactical, CQRS/mediator/Vertical Slice, extra layers,
  project-wide Result models) do not appear without approval.
- Do not report a violation merely because the code differs from a pattern the
  project has not adopted, and do not require such patterns.

## 6. Frontend (when the `frontend` slot is selected and in scope)

Apply `frontend.knowledge` and `frontend-structure.md`: feature boundaries and
component responsibility, HTTP calls behind a data-access boundary,
subscription/reactive-state lifetime, frontend error handling, route guards not
treated as server authorization, no unnecessary global/shared state, meaningful
frontend tests. Do not apply backend project-boundary rules mechanically to
frontend code.

## 7. Data and security

Check, when relevant: transaction and commit behavior, destructive data
changes, raw SQL parameterization, authorization, input trust boundaries,
secrets, sensitive logging, concurrency, migrations (`persistence.workflow`
review step), development seed consistency when the model of seeded entities
changed, and cache consistency. Use the full `security-scan` only when the user
asked for a security audit, the change is materially security-sensitive, or a
concrete finding justifies broader investigation.

## 8. Integrations

For external calls check cancellation propagation, timeout strategy,
idempotency, retry safety, failure translation, and disposal/lifetime. Do not
demand retries for operations that are unsafe to retry.

## 9. Tests

Check that changed behavior has useful maintained automated coverage — behavior,
not line count. For a bug fix, look for a regression test when recurrence is
plausible; for behavioral probes used during implementation, check that the
verified behavior was preserved (`verify`). Do not demand duplicate tests when
equivalent coverage exists.

## 10. Performance

Report only credible problems: obvious N+1 access, unbounded materialization,
repeated expensive remote calls, blocking async I/O, heavy allocation in a
demonstrated hot path. Do not recommend caching, compiled queries, pooling, or
`ValueTask` speculatively.

## Specialized guidance

Load only what the changed area needs: persistence → `persistence.knowledge`;
backend tests → `backend-testing.knowledge`; authentication/authorization →
`authentication`; HTTP semantics → `http-api`; error handling →
`aspnet-error-handling`; external HTTP → `httpclient-factory`; caching →
`caching`; configuration/DI → `configuration` / `dependency-injection`;
frontend → `frontend.knowledge`; containers/CI → `docker` / `ci-cd`.

## Tooling

Use compiler diagnostics, analyzers, and repository search when useful; no MCP
server or specific analyzer is required. Tool output is evidence, not
authority — read the code before turning a warning into a finding.

## Output

For each finding: severity, file/location, what is wrong, why it matters, and
the smallest reasonable fix, ordered by severity.

- **Critical** — data loss, security vulnerability, reliably broken core
  behavior, or another issue that should block use or merge immediately.
- **High** — likely defect or architectural/data-integrity issue that should be
  fixed before merge.
- **Medium** — real maintainability, robustness, or test gap worth addressing,
  not a likely immediate production failure.
- **Low** — non-blocking improvement.

Do not manufacture findings to populate categories. When there are no
meaningful findings, say so and name the important areas that could not be
verified.

## Review discipline

Do not rewrite working code during a review unless asked, report formatting
owned by tooling as a defect, demand personal style preferences, treat every
warning as a bug, or add filler praise to balance criticism.
