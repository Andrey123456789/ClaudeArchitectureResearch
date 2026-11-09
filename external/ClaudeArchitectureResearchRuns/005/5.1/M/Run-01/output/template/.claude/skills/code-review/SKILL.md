---
name: code-review
description: >
  Use for code reviews, PR reviews, reviewing a diff, or an independent
  defect-focused review of completed .NET/Angular changes — required before the
  final verify for substantial features or new applications. Covers
  correctness, specification conformance, architecture, data/security,
  integrations, tests, and credible performance risks.
---

> Owns: review procedure, finding priorities, review output and severity, review discipline | Scope: common | Loads: workflow (CLAUDE.md routing; preloaded by the code-reviewer agent)

# Code Review

Review the actual changed behavior and report concrete defects or risks. Code
review is not the completion checklist; `verify` runs the final checks.

## Priorities

Prioritize findings in this order: correctness; security and authorization;
data integrity and persistence; architectural boundary violations; concurrency
and integration behavior; missing meaningful tests; maintainability; credible,
evidence-backed performance problems. Never elevate style preferences above
behavioral defects, and do not report formatting owned by tooling.

## Step 1: Establish Scope

Determine what is reviewed: supplied files, working-tree diff, branch/PR diff,
or a named feature. Read enough surrounding code (callers, contracts,
dependencies) to understand the changed behavior; never review isolated lines.

## Step 2: Load the Governing Policy

Path-scoped rules may not have loaded for the files under review. Read the rules
governing the changed areas: `architecture.md`, `persistence.md`, `api.md`,
`error-handling.md`, `performance.md`, `coding-style.md`, `security.md`,
`testing.md`, `dependencies.md`, `angular.md`, `delivery.md` as relevant. Load
knowledge skills only for changed areas that need depth, for example: EF Core →
`ef-core`; tests → `dotnet-testing`; auth → `authentication`; HTTP semantics →
`http-api`; failures → `aspnet-error-handling`; outbound HTTP →
`httpclient-factory`; caching → `caching`; configuration/DI → `configuration`,
`dependency-injection`; Angular → `angular`; Docker/CI → `docker`, `ci-cd`.

Do not require patterns the repository has not adopted (CLAUDE.md, Architecture
Defaults) and do not report a violation merely because code differs from such a
pattern. Do not apply backend project-boundary rules mechanically to Angular
code.

## Step 3: Specification Conformance

Check both directions against `SPECIFICATION.md` and `CUSTOM_SETTINGS.md`
(CLAUDE.md, Product Sources):

- [ ] required behavior is not missing or weakened;
- [ ] no unapproved product behavior was introduced — for example new length or
      numeric limits, reserved names/values, newly required fields, extra
      workflow restrictions, additional user-visible validation, or observable
      string-comparison semantics (case, collation, culture/ordinal,
      normalization, trimming), including those expressed through database
      configuration or framework defaults.

A detail absent from the specification is not a defect if the user approved it
and the durable sources were synchronized. Do not confuse internal
implementation details with product behavior.

## Step 4: Correctness

Look for wrong conditions or state transitions, null/empty edge cases, incorrect
async or cancellation handling, incorrect error mapping, resource lifetime
problems, unintended side effects, and races on shared state. Do not invent
failures without a plausible execution path.

## Step 5: Architecture

- [ ] dependency direction, thin Controllers, Application Services
      orchestration, specific repositories, EF Core containment, `IUnitOfWork`
      commit boundary (`architecture.md`);
- [ ] architectural proportionality — abstraction count justified by actual
      complexity; no Reserved pattern without an approved decision (CLAUDE.md);
- [ ] seeder reviewed/updated when Domain/persistence changes affect seeded
      entities; migrations reviewed (`persistence.md`).

## Step 6: Frontend

When Angular code is in scope, check `angular.md`: feature boundaries, component
responsibility, HTTP behind data-access services, subscription lifetime, error
contract handling, no route guard treated as authorization (`security.md`),
no unnecessary global state, meaningful frontend tests.

## Step 7: Data, Security, Integrations

Check, when relevant: commit/transaction behavior, destructive data changes,
raw SQL parameterization, authorization, input trust boundaries, secrets,
sensitive logging, concurrency, migrations, cache consistency (`security.md`,
`performance.md`). For external calls: cancellation, bounded time, idempotency,
retry safety, failure translation, disposal/lifetime (`error-handling.md`). Use
the full `security-scan` only when the user requested an audit, the change is
materially security-sensitive, or a concrete finding justifies broader
investigation.

## Step 8: Tests

Determine whether changed behavior has useful maintained coverage, focusing on
behavior rather than line count (`testing.md`). For bug fixes, look for a
regression test when recurrence is plausible; check that behavioral probes were
preserved (`verify`, step 4). Do not request duplicate tests.

## Step 9: Performance

Report performance only with a credible reason — obvious N+1 access, unbounded
materialization, blocking async I/O, repeated expensive remote calls, heavy
allocation in a demonstrated hot path. Do not recommend caching, compiled
queries, pooling, `ValueTask`, or similar optimizations speculatively.

## Tooling

Use compiler diagnostics, analyzers, and repository tooling when available. Tool
output is evidence, not authority; read the code before turning a warning into a
finding. No MCP server or specific analyzer is required.

## Output

Report findings ordered by severity. For each: severity, file/location, what is
wrong, why it matters, smallest reasonable fix.

- **Critical** — data loss, security vulnerability, reliably broken core
  behavior; blocks use/merge.
- **High** — likely defect or architectural/data-integrity issue; fix before
  merge.
- **Medium** — real maintainability, robustness, or test gap; not a likely
  immediate failure.
- **Low** — non-blocking improvement.

Do not manufacture findings to populate categories. If no meaningful problem is
found, say so and name important areas that could not be verified. Do not add
filler praise, rewrite working code during a review unless asked, or demand
personal style preferences.
