---
name: code-review
description: Use for code reviews, PR reviews, reviewing a diff, or an independent defect-focused review of completed backend or frontend changes. Checks correctness, specification conformance, architecture boundaries, data integrity, security, integrations, tests, and credible performance risks.
---

> Level: 0-core · Owns: review procedure, finding priorities, severity scale, review output · Loading: on invocation (also preloaded by the `code-reviewer` agent)

# Code Review

Review the actual changed behavior and report concrete defects or risks. Review is not the completion checklist — `verify` runs the final build/test/diff checks.

## Priorities

Prioritize findings: correctness; security and authorization; data integrity and persistence; architectural boundary violations; concurrency and integration behavior; missing meaningful tests; maintainability; performance problems supported by evidence. Never rank style preferences above behavioral defects.

## 1. Establish scope

Determine what is reviewed — files supplied by the user, the working-tree diff, a branch/PR diff, or a named feature. Read the changed code and enough surrounding code (callers, contracts, dependencies) to understand its behavior; never review isolated lines.

## 2. Load the governing rules

Read the rule files whose `paths` match the changed files (`.claude/rules/**`) — a separate review context may not have them loaded — and the knowledge skill for each specialized area touched: persistence, backend tests, and frontend use the knowledge skills named in the capability selection; HTTP semantics → `http-api`; error handling → `aspnet-error-handling`; authentication → `authentication`; outbound HTTP → `httpclient-factory`; caching → `caching`; configuration/DI → `configuration` / `dependency-injection`; containers/CI → `docker` / `ci-cd`; security-sensitive changes → `security-scan` when warranted.

## 3. Understand intent and specification conformance

Identify the behavior added or changed, expected error cases, persistence or external effects, and the tests meant to protect it. When `SPECIFICATION.md` is non-empty it is the product contract; approved `CUSTOM_SETTINGS.md` values are intended behavior.

Check conformance in both directions against the product-input policy (`CLAUDE.md` § Product inputs): required behavior is not missing or weakened, and no unapproved behavior was added — new length or numeric limits, reserved names or values, newly required fields, extra workflow restrictions, additional user-visible validation, or new or changed observable string-comparison semantics (case sensitivity, collation, culture/ordinal, normalization, trimming), even when expressed only through database configuration or framework defaults. A detail absent from the specification is not a defect if the user approved it and the durable sources were synchronized. Do not confuse internal implementation details with product behavior.

## 4. Correctness

Look for wrong conditions or state transitions, null/empty edge cases, incorrect async or cancellation handling, incorrect error mapping, resource-lifetime problems, unintended side effects, and races on shared state. Do not invent failures without a plausible execution path.

## 5. Architecture

Check the boundary rules under `.claude/rules/1-architecture/` (role rules and the frame's boundaries) and the persistence access rule, and run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-architecture.mjs"` when project references or packages changed. Also check proportionality: simple CRUD/workflow code keeps the domain model simple; abstraction count matches actual complexity; patterns the project has not adopted (imported adopted-architecture rule; Reserved list in `CLAUDE.md`) do not appear without approval. Do not report a violation merely because code differs from a pattern the project has not adopted, and do not demand such patterns.

## 6. Frontend changes

Apply the frontend rules and the frontend knowledge skill: feature boundaries and component responsibility, HTTP calls behind a data-access boundary, subscription and reactive-state lifetime, frontend error handling, route guards not treated as authorization, unnecessary global/shared state, meaningful frontend tests. Do not apply backend project-boundary rules mechanically to frontend code.

## 7. Data and security

When relevant check commit behavior, destructive data changes, raw SQL parameterization, authorization, input trust boundaries, secrets, sensitive logging, concurrency, migrations (`persistence.workflow`, including the seed co-change step), and cache consistency.

## 8. Integrations

For external calls check cancellation propagation, timeout strategy, idempotency, retry safety, failure translation, and disposal/lifetime. Do not demand retries for operations that are not safe to retry.

## 9. Tests

Check that changed behavior has useful automated coverage, focusing on behavior rather than line count; look for a regression test on bug fixes where recurrence is plausible; check that behavioral probes were preserved (`verify` step 4). Do not request duplicate tests when equivalent coverage exists.

## 10. Performance

Report performance only for credible problems — obvious N+1 access, unbounded materialization, repeated expensive external calls, blocking async I/O, high-volume allocation in a demonstrated hot path. Do not recommend compiled queries, pooling, caching, `ValueTask`, or similar optimizations speculatively.

## Tooling

Compiler diagnostics, analyzers, and repository tools are evidence, not authority; no MCP server or specific analyzer is required. Read the code before turning a tool warning into a finding.

## Output

For each finding: severity, file/location, what is wrong, why it matters, smallest reasonable fix — ordered by severity:

- **Critical** — data loss, security vulnerability, reliably broken core behavior; blocks use or merge.
- **High** — likely defect or architecture/data-integrity issue; fix before merge.
- **Medium** — real maintainability, robustness, or test gap; not a likely immediate failure.
- **Low** — non-blocking improvement.

Do not manufacture findings to populate categories. If there are no meaningful findings, say so and name important areas that could not be verified.

## Discipline

Do not rewrite working code during a review unless asked, report formatting already owned by tooling, demand personal style preferences, assume every warning is a bug, require patterns the project has not adopted, or add filler praise to balance criticism.
