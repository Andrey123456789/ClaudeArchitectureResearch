---
name: code-review
description: Use for code reviews, PR or diff reviews, or an independent defect-focused pass over completed .NET/Angular changes. Canonical procedure of the code-reviewer agent.
---

> Kind: WF | Scope: common | Owner: code review procedure — priorities, steps, finding format, review discipline | Loading: workflow (model- or user-invoked; preloaded by the code-reviewer agent)

# Code Review

Goal: review the actual changed behavior and report concrete defects or risks. Code review is not the completion checklist — `verify` runs the final build/test/diff verification.

## Priorities

Prioritize findings in this order: correctness; security and authorization; data integrity and persistence; architectural boundary violations; concurrency and integration behavior; missing meaningful tests; maintainability; credible performance problems. Do not elevate style preferences above behavioral defects or bury important findings under them.

## Step 1 — Establish scope

Determine what is reviewed: files supplied by the user, the working-tree diff, a branch/PR diff, or a named feature or module. Read the changed code plus enough surrounding code — callers, contracts, dependencies — to understand its behavior; never review isolated lines without that context.

## Step 2 — Understand intent

Identify the behavior added or changed, expected error cases, persistence and external-system effects, and the tests meant to protect it. Read the standards for the scopes the change touches (`.claude/rules/<scope>/`) and load the knowledge skill for each changed technology area.

**Specification conformance** (CLAUDE.md § Product sources) — check both directions: required behavior is not missing or weakened, and the implementation does not introduce unapproved product behavior. Flag drift such as new length or numeric limits, reserved names or values, new or changed observable string-comparison semantics (case sensitivity, collation, culture/ordinal comparison, normalization, trimming — including when expressed only through database configuration or framework defaults), newly required fields, extra workflow restrictions or additional user-visible validation rules. A detail the user explicitly approved and recorded in the durable product sources is not drift; do not confuse internal implementation details with product behavior.

## Step 3 — Correctness

Look for wrong conditions or state transitions, null/empty edge cases, incorrect async or cancellation behavior, incorrect error mapping, resource-lifetime problems, unintended side effects and races on shared state. Report a failure only with a plausible execution path.

## Step 4 — Architecture

- Backend: check the change against `rules/backend/architecture.md` — Domain independence, Application free of Infrastructure/EF Core, thin Controllers, Application Services orchestrating use cases, specific repository abstractions, no `DbContext`/`DbSet`/`IQueryable` leaks, repositories not committing independently, `IUnitOfWork` as the commit boundary.
- Proportionality (CLAUDE.md § Engineering defaults, § Decisions): abstraction count justified by actual complexity; no unapproved Rich Domain Model, DDD tactical patterns, CQRS/MediatR/VSA, extra layers or project-wide Result model.
- Frontend: check against `rules/frontend/angular.md` — feature boundaries and component responsibility, HTTP behind a data-access boundary, subscription and reactive-state lifetime, frontend error handling, route guards not treated as authorization, unnecessary global state, meaningful frontend tests. Do not apply backend project-boundary rules mechanically to Angular code.
- Do not report a violation merely because the implementation differs from a pattern the project has not adopted (D-02).

## Step 5 — Data and security

When relevant check commit and transaction behavior, destructive data changes, raw SQL parameterization, authorization, input trust boundaries, secrets, sensitive logging, concurrency, migrations and cache consistency against `rules/common/security.md`, `rules/backend/security.md`, `rules/backend/persistence.md` and `rules/backend/caching.md`. When a migration or model change affects seeded entities, confirm the seeder obligation in `development-workflow` § Persistence or model change. Use the full `security-scan` only when the user requested a security audit, the change is materially security-sensitive, or a concrete finding justifies broader investigation — do not turn every review into a full OWASP audit.

## Step 6 — Integrations

For external calls check cancellation propagation, time limits, idempotency, retry safety, failure translation and disposal/lifetime against `rules/backend/integrations.md`. Do not demand retries for operations that are not safe to retry.

## Step 7 — Tests

Check whether changed behavior has useful maintained coverage (`rules/backend-tests/testing.md`), focusing on behavior rather than line count. For bug fixes look for the regression test (`development-workflow` § Bug fix); for behavioral probes, confirm preservation (`verify` § 4). Do not demand duplicate tests when equivalent coverage exists.

## Step 8 — Performance

Report performance only with a credible reason — obvious N+1 access, unbounded materialization, repeated expensive remote calls, blocking async I/O, high-volume allocation in a demonstrated hot path. Do not recommend compiled queries, pooling, caching, `ValueTask` or similar optimizations speculatively (`rules/backend/csharp.md` § Optimization).

## Tooling

Use compiler diagnostics, analyzers, IDE/Roslyn or repository analysis tools when available; no MCP server or specific analyzer is required. Tool output is evidence, not authority: read the code before turning a tool warning into a finding.

## Output

For each finding: severity, file/location, what is wrong, why it matters, the smallest reasonable fix. Order findings by severity:

- **Critical** — data loss, security vulnerability, reliably broken core behavior, or another issue that should block use or merge immediately.
- **High** — likely defect or architectural/data-integrity issue that should be fixed before merge.
- **Medium** — real maintainability, robustness or test gap worth addressing, not a likely immediate production failure.
- **Low** — non-blocking improvement.

Do not manufacture findings to populate categories. When there are no meaningful findings, say so and name the important areas that could not be verified. Do not add filler praise to balance criticism.

## Review discipline

Do not rewrite working code during a review unless asked; do not report formatting owned by tooling as a defect; do not demand personal style preferences; do not assume every warning is a bug; do not require patterns the project has not adopted (for example MediatR, CQRS, Vertical Slice Architecture, Minimal APIs, Rich Domain Models, Domain Events or generic repositories).
