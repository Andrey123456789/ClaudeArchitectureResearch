---
name: code-review
description: >
  Use to review a diff, PR, branch, or completed change for correctness,
  architecture, data-integrity, security, test, and credible performance
  defects. Procedure behind the code-reviewer agent.
---

> Workflow skill. Owns: the review procedure, defect prioritization, finding discipline, and review output format · Scope: common · Loads: on invocation; preloaded by the code-reviewer agent · Depends on: CLAUDE.md, .claude/rules/

# Code Review

Review the actual changed behavior and identify concrete defects or risks.
Code review is not the completion checklist; `verify` runs the final
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
8. performance problems supported by a credible reason or evidence.

Do not elevate style preferences above defects, and do not bury important
findings under them.

## Step 1: Establish Scope

Determine what is reviewed: files supplied by the user, the working-tree diff,
a branch/PR diff, or a named feature or module. Read the changed code and enough
surrounding code — callers, contracts, dependencies — to understand its
behavior; do not review isolated lines.

## Step 2: Read the Governing Sources

- Read the rule files for every affected area (CLAUDE.md, Workflows); review
  does not rely on rules having loaded already.
- Load technique only for the changed areas: persistence → `ef-core`; tests →
  `dotnet-testing`; authentication/authorization → `authentication`; HTTP
  semantics → `http-api`; error handling → `aspnet-error-handling`; outbound
  HTTP → `httpclient-factory`; caching → `caching`; configuration/DI →
  `configuration`, `dependency-injection`; Angular → `angular`; Docker/CI →
  `docker`, `ci-cd`.
- Identify the intended behavior, expected error cases, persistence or
  external-system effects, and the tests meant to protect the behavior.

## Step 3: Specification Conformance

Check by reference against CLAUDE.md (Product Sources), in both directions:

- [ ] Required behavior from a non-empty `SPECIFICATION.md` and approved
  `CUSTOM_SETTINGS.md` values is present and not weakened.
- [ ] No unapproved product behavior was invented — for example new length or
  numeric limits, reserved names or values, new or changed observable
  string-comparison semantics (case sensitivity, collation, culture/ordinal,
  normalization, trimming), newly required fields, extra workflow restrictions,
  or additional user-visible validation rules. Database configuration or
  framework defaults do not make string semantics an internal detail.
- [ ] An approved addition is not a defect when the durable product sources were
  synchronized; internal implementation details are not product behavior.

## Step 4: Correctness

Look for wrong conditions or state transitions, null/empty edge cases,
incorrect async or cancellation handling, incorrect error mapping, resource
lifetime problems, unintended side effects, and race conditions where shared
state exists. Do not invent hypothetical failures without a plausible execution
path.

## Step 5: Architecture

Check by reference:

- [ ] dependency direction, Domain independence, thin Controllers, Application
  Services orchestration — `architecture.md`;
- [ ] specific repositories, no leaked `DbContext`/`DbSet`/`IQueryable`,
  repositories not committing independently, `IUnitOfWork` as commit boundary —
  `persistence.md`;
- [ ] no not-adopted pattern (CQRS, MediatR, Vertical Slice Architecture, Rich
  Domain Model, project-wide Result, extra layers) without an approved decision
  — CLAUDE.md (Architecture Decisions);
- [ ] abstraction count proportional to actual complexity — CLAUDE.md (Change
  Discipline).

Do not report a violation merely because the code differs from a pattern this
project has not adopted, and do not require such patterns.

For Angular code, check by reference `angular.md` and `security.md`: feature
boundaries and component responsibility, HTTP behind a data-access boundary,
subscription lifetime, frontend error handling, route guards not treated as
server authorization, unnecessary global state, meaningful frontend tests. Do
not apply backend project-boundary rules mechanically to Angular code.

## Step 6: Data and Security

When relevant: commit and transaction behavior, destructive data changes, raw
SQL parameterization, authorization, input trust boundaries, secrets, sensitive
logging, concurrency, migrations (`development-workflow`, Migrations), seed-data
consistency when seeded entities changed (`development-workflow`, Seed data),
and cache consistency. Perform a normal security review of changed code; use
the full `security-scan` procedure only when the user asked for a security
audit, the change is materially security-sensitive, or a concrete finding
justifies broader investigation.

## Step 7: Integrations

For external calls check cancellation propagation, timeout strategy,
idempotency, retry safety, failure translation, and disposal/lifetime behavior
(`error-handling.md`, Outbound Dependencies). Do not demand retries for
operations that are not safe to retry.

## Step 8: Tests

Determine whether changed behavior has useful maintained automated coverage,
focusing on behavior rather than line count. For bug fixes look for a regression
test when recurrence is plausible (`development-workflow`, Bug fixes); for
behavioral probes see `verify` (Preserve Behavioral Verification). Do not request
duplicate tests when equivalent coverage exists.

## Step 9: Performance

Report performance concerns only with a credible reason — obvious N+1 access,
unbounded materialization, repeated expensive external calls, blocking async
I/O, high-volume allocation in a demonstrated hot path. Do not recommend
compiled queries, pooling, caching, `ValueTask`, or similar optimizations
speculatively.

## Tooling

Use compiler diagnostics, analyzers, IDE/Roslyn tooling, or repository scripts
when available; no MCP server or specific analyzer is required. Tool output is
evidence, not authority: read the code before turning a warning into a finding.

## Output

Report findings ordered by severity. For each finding give: severity,
file/location, what is wrong, why it matters, and the smallest reasonable fix.

- **Critical** — data loss, security vulnerability, reliably broken core
  behavior, or another issue that should block use or merge immediately.
- **High** — likely defect or architectural/data-integrity issue that should be
  fixed before merge.
- **Medium** — real maintainability, robustness, or test gap worth addressing,
  but not a likely immediate production failure.
- **Low** — non-blocking improvement.

Do not manufacture findings to populate categories. If there are no meaningful
findings, say so and name any important areas that could not be verified. Do
not add filler praise to balance criticism.

## Review Discipline

Do not rewrite working code during a review unless asked; do not report
formatting already owned by tooling as a defect; do not demand personal style
preferences; do not assume every warning is a bug.
