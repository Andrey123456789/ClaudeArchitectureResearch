---
name: code-review
description: >
  Use for code reviews, PR reviews, or reviewing a diff of completed .NET/Angular
  changes: correctness, spec conformance, architecture, data, security, tests,
  performance.
---

> Level: 3 Project · Owns: review procedure, review priorities, findings format (workflow) · Scope: common · Loads: on invocation; preloaded by the `code-reviewer` agent · Depends on: CLAUDE.md, .claude/rules/** (owner reads)

# Code Review

Review the actual changed behavior and identify concrete defects or risks. Code review is not the completion checklist — `verify` runs the build/test/diff verification.

## Priorities

Prioritize correctness, security and authorization, data integrity and persistence, architectural boundary violations, concurrency and integration behavior, missing meaningful tests, maintainability, and credible performance problems — in that order. Never elevate style preferences above behavioral defects, and do not report formatting already owned by tooling as a defect.

## 1. Establish scope

Determine what is reviewed: files supplied by the user, the working-tree diff, a branch/PR diff, or a named feature. Read the changed code and enough surrounding code — callers, contracts, dependencies — to understand the behavior; never review isolated lines.

## 2. Understand intent and read the owners

Identify the behavior being added or changed, expected error cases, persistence or external effects, and the tests meant to protect it. Read the rule files that govern the changed area (they may not have loaded): `.claude/rules/1-architecture/*` for boundaries, `.claude/rules/0-core/*` for security, logging, testing, runtime principles, and the Level 2/3 modules for the technologies involved. Use knowledge skills (`ef-core`, `dotnet-testing`, `authentication`, `http-api`, `aspnet-error-handling`, `httpclient-factory`, `caching`, `configuration`, `dependency-injection`, `angular`, `docker`, `ci-cd`) only when relevant to the changed area.

## 3. Specification conformance

Check both directions against the product inputs (CLAUDE.md → Product governance): required behavior must not be missing or weakened, and the implementation must not silently add unapproved behavior — new limits, reserved values, newly required fields, extra workflow restrictions, additional user-visible validation, or new observable string-comparison semantics (case sensitivity, collation, culture/ordinal, normalization, trimming), even when expressed through database configuration or framework defaults. A detail the user explicitly approved and that was synchronized into the durable sources is not a defect. Do not confuse internal implementation details with product behavior.

## 4. Correctness

Look for wrong conditions or state transitions, null/empty edge cases, incorrect async or cancellation handling, incorrect error mapping, resource-lifetime problems, unintended side effects, and race conditions where shared state exists. Do not invent failures without a plausible execution path.

## 5. Architecture

Check the changed code against the Level 1 rules (`backend-layers.md`, `persistence-boundary.md`, `entry-points.md`, `outcomes.md`) and their Level 2 bindings: Domain independence, Application free of Infrastructure and persistence-framework types, thin entry points, Application Services orchestrating use cases, specific repository abstractions, the Unit of Work as commit boundary. Also check proportionality: abstraction count justified by actual complexity, and no consequential pattern without approval. Never report a violation merely because the code differs from a pattern this architecture has not adopted (`1-architecture/overview.md`).

## Frontend changes

When Angular code is in scope, check `1-architecture/frontend-structure.md` and `2-technology/angular.md`: feature boundaries and component responsibility, HTTP calls behind data-access boundaries, subscription and reactive-state lifetime, frontend error handling, route guards not treated as authorization, unnecessary global/shared state, meaningful frontend tests. Do not apply backend project-boundary rules mechanically to Angular code.

## 6. Data and security

Review transaction and commit behavior, destructive data changes, raw SQL parameterization, authorization, input trust boundaries, secrets, sensitive logging, concurrency, migrations (reviewed as `development-workflow` → Co-changes requires), development seed-data consistency when Domain or persistence changes affect seeded entities, and cache consistency. Use the full `security-scan` only when the user requested a security audit, the change is materially security-sensitive, or a concrete finding justifies broader investigation.

## 7. Integrations

For external calls check cancellation propagation, timeout strategy, idempotency, retry safety, failure translation, and disposal/lifetime behavior (`0-core/runtime-principles.md`). Do not demand retries for operations that are not safe to retry.

## 8. Tests

Check whether changed behavior has useful maintained automated coverage — behavior, not line count. For bugs, look for a regression test when recurrence is plausible. Behavioral probes used during implementation must be preserved as `verify` step 4 requires. Do not request duplicate tests when equivalent coverage exists.

## 9. Performance

Report performance only for a credible reason: obvious N+1 access, unbounded materialization, repeated expensive remote calls, blocking async I/O, high-volume allocation in a demonstrated hot path. Do not recommend caching, compiled queries, pooling, `ValueTask`, or similar optimizations speculatively.

## Tooling

Compiler diagnostics, analyzers, IDE/Roslyn tooling, and repository search are useful evidence, not authority; no MCP server or specific analyzer is required. Read the code before turning a tool warning into a finding.

## Output

Report findings ordered by severity. For each: severity · file/location · problem · why it matters · smallest reasonable fix.

- **Critical** — data loss, security vulnerability, reliably broken core behavior; blocks use/merge.
- **High** — likely defect or architectural/data-integrity issue that should be fixed before merge.
- **Medium** — real maintainability, robustness, or test gap, not a likely immediate production failure.
- **Low** — non-blocking improvement.

Never invent findings to populate categories. When there are no meaningful findings, say so and state the important areas that could not be verified. Do not rewrite working code during a review unless asked, demand personal style preferences, assume every warning is a bug, or add filler praise.
