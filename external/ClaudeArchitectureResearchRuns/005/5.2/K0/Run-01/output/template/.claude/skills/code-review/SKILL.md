---
name: code-review
description: Use to review a diff, PR, branch or completed implementation for defects — correctness, architecture boundaries, data integrity, security, integrations, tests and credible performance risks. Read-only; reports findings by severity.
---
<!-- Kind: WF | Scope: common | Owns: review procedure, finding priorities, finding discipline, review output | Loads: workflow invocation; preloaded by agent code-reviewer -->
# Code Review

Review the actual changed behavior and report concrete defects or risks. Code review is not the completion checklist — `verify` runs the final build, test and diff verification. Do not edit or rewrite code during a review unless asked.

## Priorities

Findings **must** be prioritized in this order: correctness → security and authorization → data integrity and persistence → architecture boundary violations → concurrency and integration behavior → missing meaningful tests → maintainability → performance problems supported by evidence. **Never** elevate style preferences above defects; formatting already owned by tooling is not a defect.

## 1. Establish Scope

Determine what is reviewed: explicit files, the working-tree diff, a branch/PR diff, or a named feature or module. Read enough surrounding code — callers, contracts, dependencies — to understand the changed behavior; do not review isolated lines.

## 2. Understand Intent and Load Standards

Identify the behavior added or changed, expected error cases, persistence or external-system effects, and the tests meant to protect it. **Must** read the standards of every touched scope (`.claude/rules/<scope>/*.md`); they are the review criteria. Load knowledge skills only for touched areas:

    persistence / EF Core          -> ef-core
    tests                          -> dotnet-testing
    authentication / authorization -> authentication
    HTTP semantics                 -> http-api
    errors / validation            -> aspnet-error-handling
    outbound HTTP / resilience     -> httpclient-factory
    caching                        -> caching
    configuration / DI             -> configuration / dependency-injection
    Angular                        -> angular
    Docker / CI                    -> docker / ci-cd

Do not require patterns the project has not adopted (decision register § Not Adopted) — a difference from such a pattern is not a violation.

## 3. Specification Conformance

Check both directions against `SPECIFICATION.md` and `CUSTOM_SETTINGS.md` (CLAUDE.md § Product Inputs):

- [ ] required behavior is not missing or weakened;
- [ ] no unapproved limits, reserved names or values, newly required fields, workflow restrictions, defaults or user-visible validation rules;
- [ ] no silently chosen observable string semantics (case, collation, culture/ordinal, normalization, trimming), including through database configuration or framework defaults.

A detail absent from the original specification is not a defect when the user approved it and the durable sources were synchronized. Do not confuse internal implementation details with product behavior.

## 4. Correctness

Look for wrong conditions or state transitions, null/empty edge cases, incorrect async behavior or cancellation handling, incorrect error mapping, resource lifetime problems, unintended side effects, and races where shared state exists. Report only failures with a plausible execution path.

## 5. Architecture

Backend (`rules/backend/architecture.md`, `rules/backend/persistence.md`):

- [ ] Domain independent; Application free of Infrastructure and EF Core types;
- [ ] Controllers thin; Application Services orchestrate use cases;
- [ ] specific repository abstractions; no `DbContext`, `DbSet` or `IQueryable` leaks; repositories do not commit independently; `IUnitOfWork` is the commit boundary;
- [ ] abstraction count justified by actual complexity; no Reserved pattern without a recorded decision.

Frontend (`rules/frontend/*.md`): feature boundaries and component responsibility; HTTP kept behind data-access services; subscription and reactive-state lifetime; error handling; route guards not treated as server authorization; no unnecessary global/shared state; meaningful frontend tests. Do not apply backend project-boundary rules mechanically to Angular code.

## 6. Data and Security

When relevant, check transaction and commit behavior, destructive data changes, raw SQL parameterization, authorization, input trust boundaries, secrets, sensitive logging, concurrency, cache consistency, migrations reviewed, and the development seeder updated when the seeded model changed (`development-workflow` § Co-change Obligations).

Use the full `security-scan` only when the user requested a security audit, the change is materially security-sensitive, or a concrete finding justifies broader investigation; an ordinary review is not an OWASP audit.

## 7. Integrations

For external calls check cancellation propagation, timeout strategy, idempotency, retry safety, failure translation and disposal/lifetime (`rules/backend/outbound-http.md`). Do not demand retries for operations that are unsafe to retry.

## 8. Tests

Check that changed behavior has useful maintained coverage, that a bug fix has a regression test when recurrence is plausible, and that behavioral probes were preserved (`verify` § 4). Do not demand duplicate tests when equivalent coverage exists.

## 9. Performance

Report performance problems only with a credible reason: obvious N+1 access, unbounded materialization, blocking async I/O, repeated expensive remote calls, clearly expensive work in a demonstrated hot path. Do not recommend caching, compiled queries, pooling, `ValueTask` or similar optimizations speculatively.

## Tooling

Use compiler diagnostics, analyzers, IDE/Roslyn tooling or repository search when useful; no MCP server or specific analyzer is required. Tool output is evidence, not authority — inspect the code before reporting a warning as a defect.

## Output

For each finding give severity, file/location, what is wrong, why it matters and the smallest reasonable fix, ordered by severity:

- **Critical** — data loss, security vulnerability, reliably broken core behavior; blocks use or merge.
- **High** — likely defect or architecture/data-integrity issue that should be fixed before merge.
- **Medium** — real maintainability, robustness or test gap that is not a likely immediate production failure.
- **Low** — non-blocking improvement.

**Must not** manufacture findings to populate categories: when there are no meaningful findings, say so and name important areas that could not be verified. No filler praise to balance criticism, and no demands based on personal style preferences.
