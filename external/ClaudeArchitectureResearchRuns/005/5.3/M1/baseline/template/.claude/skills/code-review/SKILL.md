---
name: code-review
description: >
  Use to review completed changes, a diff, or a PR for defects: correctness,
  security, data integrity, architecture boundaries, integrations, tests,
  maintainability, credible performance.
---

> Workflow · Owns the review procedure, review priorities, finding discipline, and output shape · Review criteria are check-by-reference items pointing to the owning rules

# Code Review

## Goal

Review the actual changed behavior and identify concrete defects or risks.
Code review is not the completion checklist; `verify` runs the final
build/test/diff verification.

Review priorities, in order: correctness; security and authorization; data
integrity and persistence; architectural boundary violations; concurrency and
integration behavior; missing meaningful tests; maintainability; credible,
evidence-supported performance problems. Do not elevate style preferences above
behavioral defects.

## Step 1: Establish Scope

Determine what is reviewed — files supplied by the user, the working-tree diff,
a branch/PR diff, or a named feature. Read the changed code and enough
surrounding code (callers, contracts, dependencies) to understand its behavior;
do not review isolated lines.

## Step 2: Understand Intent and Load Owners

Identify the behavior being added or changed, expected error cases,
persistence or external-system effects, and the tests meant to protect it.

Path rules may not have loaded for files you only see in a diff. Read the
owning rules for every changed area (table in `development-workflow` § Inspect
Before Changing) and the relevant knowledge skills before judging conformance.

## Step 3: Product Conformance

Check against `CLAUDE.md` § Product Sources in both directions:

- Is required behavior from `SPECIFICATION.md` or `CUSTOM_SETTINGS.md` missing
  or weakened?
- Does the change introduce unapproved product behavior — new length or numeric
  limits, reserved names or values, newly required fields, extra workflow
  restrictions, additional user-visible validation, or newly chosen
  string-comparison semantics, including semantics expressed only through
  database collation or framework defaults?

A reasonable detail absent from the specification is not a defect when the user
explicitly approved it and the durable sources were synchronized. Do not
confuse internal implementation details with product behavior.

## Step 4: Correctness

Look for concrete behavioral problems: wrong conditions or state transitions,
null/empty edge cases, incorrect async or cancellation handling, incorrect error
mapping, resource-lifetime problems, unintended side effects, and race
conditions where shared state exists. Do not invent failures without a
plausible execution path.

## Step 5: Architecture

Check `.claude/rules/architecture.md` and `persistence-technology.md`:

- Does Domain stay independent of Application, Infrastructure, and Api?
- Does Application avoid Infrastructure and persistence-technology types?
- Do Controllers stay thin, with Application Services orchestrating use cases?
- Is persistence reached through specific repository abstractions, without
  queryable or persistence-technology types leaking out of Infrastructure?
- Do repositories avoid committing normal use cases, with `IUnitOfWork` as the
  commit boundary?
- Is complexity proportional — no Rich Domain Model, DDD tactical patterns,
  patterns listed as not adopted, extra layers, or project-wide Result model
  without an approved need (`CLAUDE.md` § Decision Control)?

Do not report a violation merely because the code differs from a pattern the
project has not adopted.

## Frontend Changes

When frontend code is in scope, check `.claude/rules/frontend.md` and
`frontend-framework.md`: feature boundaries and component responsibility, HTTP
calls behind the data-access boundary, subscription and reactive-state
lifetime, frontend error handling, route guards not treated as server-side
authorization, unnecessary global or shared state, and meaningful frontend
tests. Do not apply backend project-boundary rules mechanically to frontend
code.

## Step 6: Data and Security

Check, when relevant: commit and transaction behavior, destructive data
changes, raw SQL parameterization, authorization, input trust boundaries,
secrets, sensitive logging, concurrency, migrations, cache consistency
(`security.md`, `performance.md`), and — when a migration or model change
affects seeded entities — whether `persistence-change` § Seed Data was applied.

Use the full `security-scan` workflow only when the user requested a security
audit, the change is materially security-sensitive, or a concrete finding
justifies broader investigation; do not turn every review into a full OWASP
audit.

## Step 7: Integrations

For external calls check cancellation propagation, timeout strategy,
idempotency where relevant, retry safety, failure translation, and
disposal/lifetime behavior (`performance.md` § Outbound Calls). Do not demand
retries for operations that are not safe to retry.

## Step 8: Tests

Determine whether the changed behavior has useful maintained automated
coverage, focusing on behavior rather than line count. For a bug fix, look for
a regression test when recurrence is plausible. Check that behavioral probes
were preserved (`verify` § Preserve Behavioral Verification). Do not request
duplicate tests when equivalent coverage exists.

## Step 9: Performance

Report performance concerns only with a credible reason — obvious N+1 access,
unbounded materialization, repeated expensive external calls, blocking async
I/O, obvious high-volume allocation in a demonstrated hot path. Do not
recommend caching, compiled queries, pooling, `ValueTask`, or similar
optimizations speculatively.

## Tooling

Use compiler diagnostics, analyzers, repository search, or
`node .claude/scripts/check-architecture.js` when useful. No MCP server or
specific analyzer is required. Tool output is evidence, not authority: read the
code before turning a warning into a finding.

## Output

Report findings ordered by severity. For each finding give severity,
file/location, what is wrong, why it matters, and the smallest reasonable fix.

- **Critical** — data loss, security vulnerability, reliably broken core
  behavior, or another issue that should block use or merge immediately.
- **High** — likely defect or architectural/data-integrity issue that should be
  fixed before merge.
- **Medium** — real maintainability, robustness, or test gap that is not a
  likely immediate production failure.
- **Low** — non-blocking improvement.

Do not manufacture findings to populate categories. When there are no
meaningful findings, say so and name important areas that could not be
verified. Do not add filler praise to balance criticism.

## Review Discipline

Do not rewrite working code during a review unless asked, report formatting
already owned by tooling as a defect, demand personal style preferences, assume
every warning is a bug, or require patterns the project has intentionally not
adopted.
