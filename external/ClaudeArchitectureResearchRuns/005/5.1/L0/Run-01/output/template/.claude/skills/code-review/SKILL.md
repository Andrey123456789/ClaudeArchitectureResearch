---
name: code-review
description: >
  Use for code reviews, PR or diff reviews, and the pre-verify review of
  substantial work: correctness, spec conformance, architecture, data, security,
  tests, performance; severity-ranked findings.
---

> Level: 3 Project · Owns: review procedure, severity scale and findings format · Scope: common · Loads: on demand (model- or user-invoked; preloaded by the `code-reviewer` agent)

# Code Review

Review the actual changed behavior and report concrete defects or risks. Review is not the completion checklist — `verify` runs the final checks.

## Read first

- `.claude/rules/0-core/completion-contract.md` (Review) — independence, priorities, no manufactured findings.
- The rule modules that govern the changed area (map: `.claude/INSTRUCTION-MAP.md`). Path rules load when you read changed files; read a module explicitly when its files were not opened.

## Step 1 — Establish scope

Determine what is reviewed: files supplied by the user, the working-tree diff, a branch/PR diff, or a named feature. Read enough surrounding code — callers, contracts, dependencies — to understand the changed behavior; never review isolated lines.

## Step 2 — Understand intent

Identify the behavior added or changed, the governing rules, expected error cases, persistence or external-system effects, and the tests meant to protect it. Load the matching knowledge skill only when the area needs depth:

    persistence / EF Core          -> ef-core
    tests                          -> dotnet-testing
    authentication/authorization   -> authentication
    HTTP semantics                 -> http-api
    error handling / validation    -> aspnet-error-handling
    outbound HTTP / resilience     -> httpclient-factory
    caching                        -> caching
    configuration / DI             -> configuration / dependency-injection
    Angular                        -> angular
    Docker / CI                    -> docker / ci-cd
    security-sensitive change      -> security-scan (see Step 5)

## Step 3 — Specification conformance (owner: product governance)

Check both directions:

- [ ] Required behavior is present and not weakened.
- [ ] No unapproved product behavior: new length or numeric limits, reserved names or values, newly required fields, extra workflow restrictions, additional user-visible validation, or new or changed observable string semantics (case sensitivity, collation, culture/ordinal comparison, normalization, trimming) — including when expressed only through database configuration or framework defaults.
- [ ] Approved values match `CUSTOM_SETTINGS.md`.

A detail absent from the original specification is not a defect when the user approved it and the durable sources were synchronized. Do not confuse internal implementation details with product behavior.

## Step 4 — Correctness

Look for wrong conditions or state transitions, null/empty edge cases, incorrect async or cancellation behavior, incorrect error mapping, resource-lifetime problems, unintended side effects, and races where shared state exists. Report only failures with a plausible execution path.

## Step 5 — Architecture, data and security

Check by reference — each item points to its owner:

- [ ] Dependency direction and layer responsibilities (`backend-layers.md`); project references (`node .claude/scripts/check-architecture.mjs`).
- [ ] Thin entry points; HTTP semantics in Api; response semantics (`entry-points.md`).
- [ ] Specific repositories, unit-of-work commit boundary, no persistence-framework leakage (`persistence-boundary.md`, `ef-core.md`).
- [ ] Expected outcomes, central failure handling, validation at the owning boundary (`outcomes.md`).
- [ ] Proportionality: no Rich Domain, DDD tactical patterns, CQRS/mediator/VSA, extra layers or project-wide Result without approval (architecture overview); extra abstraction is not better architecture by itself.
- [ ] Transactions and commit behavior, destructive data changes, migrations (`ef-core.md`), development seeder updated when seeded entities changed (`data-lifecycle.md`), cache consistency (`runtime-principles.md`).
- [ ] Raw SQL parameterization, authorization, input trust, secrets, sensitive logging, CORS/TLS (`security-principles.md`, `logging-principles.md`).
- [ ] Frontend: feature boundaries, component responsibility, data-access boundary, subscription lifetime, error-contract handling, guards not treated as authorization, no unnecessary global state (`frontend-structure.md`, `angular.md`). Backend project-boundary rules are not applied mechanically to Angular code.

Run the full `security-scan` only when the user asked for a security audit, the change is materially security-sensitive, or a concrete finding justifies broader investigation.

Do not report a violation merely because the code differs from a pattern this project has not adopted.

## Step 6 — Integrations

For external calls: cancellation propagation, bounded time, idempotency, retry safety, failure translation, disposal and lifetime (`runtime-principles.md`, `csharp.md`). Do not demand retries for operations that are unsafe to retry.

## Step 7 — Tests

Does changed behavior have useful maintained coverage (behavior, not line count)? For bugs, is there a regression test when recurrence is plausible? Was probe-verified behavior preserved (`testing-principles.md`)? Do not request duplicates of existing coverage.

## Step 8 — Performance

Report only credible problems — obvious N+1 access, unbounded materialization, repeated expensive external calls, blocking async I/O, heavy allocation in a demonstrated hot path. Do not recommend compiled queries, pooling, caching, `ValueTask` or similar optimizations speculatively.

## Tooling

Compiler diagnostics, analyzers and repository search are evidence, not authority; read the code before turning a warning into a finding. No specific MCP server or analyzer is required.

## Output

Findings ordered by severity. For each: **severity**, **file/location**, **problem**, **why it matters**, **smallest reasonable fix**.

- **Critical** — data loss, security vulnerability, reliably broken core behavior; blocks use or merge.
- **High** — likely defect or architectural/data-integrity issue; fix before merge.
- **Medium** — real maintainability, robustness or test gap; not an immediate production failure.
- **Low** — non-blocking improvement.

If nothing meaningful was found, say so and list the important areas that could not be verified.

## Discipline

Do not rewrite working code during a review unless asked, report formatting owned by tooling as a defect, demand personal style preferences, assume every warning is a bug, or add filler praise to balance criticism.
