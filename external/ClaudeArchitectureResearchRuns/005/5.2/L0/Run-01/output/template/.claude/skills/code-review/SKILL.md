---
name: code-review
description: >
  Use for code reviews, PR or diff reviews, and independent review of completed .NET/Angular work: defects, security, data integrity, architecture, tests.
---

> Level: 3 Project | Owns: review procedure, review priorities, finding discipline, review output | Scope: common | Loads: workflow skill (model-invoked; preloaded by the `code-reviewer` agent) | Depends on: CLAUDE.md, 0-core/*, 1-architecture/*, 2-technology/*, 3-project/*

# Code Review

Review the actual changed behavior and identify concrete defects or risks. Code
review is not the completion checklist; `verify` runs the final checks.

## Priorities

Prioritize correctness, security and authorization, data integrity and
persistence, architecture-boundary violations, concurrency and integration
behavior, missing meaningful tests, maintainability, and credible performance
problems — in that order. Do not elevate style preferences above defects, and
do not report formatting already owned by tooling as a defect.

## Step 1 — Establish Scope

Determine what is reviewed: supplied files, working-tree diff, branch/PR diff,
or a named feature. Read the changed code and enough surrounding code (callers,
contracts, dependencies) to understand its behavior.

## Step 2 — Understand Intent

Identify the behavior added or changed, expected error cases, persistence or
external effects, and the tests meant to protect it. Read the rule modules that
govern the changed area (`develop` → Rule Reads table) and relevant knowledge
skills: persistence → `ef-core`; tests → `dotnet-testing`; auth →
`authentication`; HTTP → `http-api`; errors → `aspnet-error-handling`; outbound
HTTP → `httpclient-factory`; caching → `caching`; configuration/DI →
`configuration`, `dependency-injection`; Angular → `angular`; Docker/CI →
`docker`, `ci-cd`.

## Step 3 — Product Conformance

Check both directions against `SPECIFICATION.md` and `CUSTOM_SETTINGS.md`
(CLAUDE.md, Product Governance):

- required behavior is not missing or weakened;
- no unapproved behavior was invented — new limits, reserved values, string
  comparison/collation/normalization/trimming semantics, newly required fields,
  extra workflow restrictions, additional validation rules.

An approved detail that was synchronized into the durable sources is not a
defect. Do not confuse internal implementation details with product behavior.

## Step 4 — Correctness

Look for wrong conditions or state transitions, null/empty edge cases,
incorrect async or cancellation handling, incorrect error mapping, resource
lifetime problems, unintended side effects, and races on shared state. Do not
invent failures without a plausible execution path.

## Step 5 — Architecture (check by reference)

- Reference direction and layer responsibilities (`1-architecture/backend-layers.md`)?
- Thin entry points and correct HTTP semantics (`1-architecture/entry-points.md`)?
- Specific repositories, no query leakage, Unit of Work as commit boundary
  (`1-architecture/persistence-boundary.md`)?
- Outcomes, exception flow, validation boundaries (`1-architecture/outcomes.md`)?
- Proportionality: no unapproved patterns from the consequential gate
  (`1-architecture/overview.md`)? Do not report a violation merely because code
  differs from a pattern this project has not adopted.
- Seed data reviewed when Domain/persistence changes affect seeded entities
  (`develop`, persistence changes)?

For Angular code, use `1-architecture/frontend-structure.md` and
`2-technology/angular.md`; do not apply backend project rules to Angular.

## Step 6 — Data, Security, Integrations

Check commit behavior, destructive changes, migrations, raw SQL
parameterization, authorization, input trust, secrets, sensitive logging,
concurrency, and cache consistency (Core principles). For external calls, check
cancellation, time bounds, retry safety and idempotency, failure translation,
and lifetime. Run the full `security-scan` only when the user asked for a
security audit, the change is materially security-sensitive, or a concrete
finding justifies broader investigation.

## Step 7 — Tests

Check that changed behavior has meaningful maintained coverage, that a bug fix
has a regression test when recurrence is plausible, and that behavior proven by
temporary probes is preserved (`verify`, step 4). Do not demand duplicate tests.

## Step 8 — Performance

Report only credible problems: obvious N+1 access, unbounded materialization,
blocking async I/O, repeated expensive remote calls, heavy allocation in a
demonstrated hot path. Do not recommend speculative optimizations.

## Tooling

Compiler diagnostics, analyzers, and repository tools are evidence, not
authority; no MCP server or specific analyzer is required. Read the code before
turning a tool warning into a finding.

## Output

For each finding: severity, file/location, problem, why it matters, smallest
reasonable fix — ordered by severity:

- **Critical** — data loss, security vulnerability, reliably broken core
  behavior; blocks use or merge.
- **High** — likely defect or architecture/data-integrity issue to fix before merge.
- **Medium** — real maintainability, robustness, or test gap.
- **Low** — non-blocking improvement.

Do not invent findings to populate categories. When there are no meaningful
findings, say so and name important areas that could not be verified. Do not
rewrite code during a review unless asked, and do not add filler praise.
