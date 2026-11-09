---
name: code-review
description: >
  Defect-focused review of completed .NET backend and frontend changes:
  specification conformance, correctness, architecture boundaries, data,
  security, integrations, tests, credible performance. Use for code reviews, PR
  reviews, reviewing a diff, or an independent second-pass review.
---

> Kind: WF | Scope: common | Capability: — | Loading: on-demand workflow (also preloaded by the `code-reviewer` agent)

# Code Review

## Role and independence

The review is independent and read-only: it reports findings and does not edit files or rewrite working code unless asked. This workflow is the canonical review procedure; the `code-reviewer` agent runs it without redefining it. Code review is not the completion checklist — `verify` runs the final build/test/diff verification.

## Priorities

Prioritize findings in this order: correctness; security and authorization; data integrity and persistence; architectural boundary violations; concurrency and integration behavior; missing meaningful tests; maintainability; credible performance problems. Never elevate style preferences above behavioral defects, and do not report formatting already owned by tooling.

## Step 1: Establish scope

Determine what is reviewed: supplied files, the working-tree diff, a branch/PR diff, or a named feature. Read enough surrounding code — callers, contracts, dependencies — to understand changed behavior; never review isolated lines.

## Step 2: Understand intent and load owners

Identify the behavior added or changed, expected error cases, persistence or external-system effects, and the tests meant to protect it. Read the standards that govern the changed area (`.claude/rules/<scope>/`) and load knowledge only where relevant:

```text
HTTP semantics / API errors      -> http-api / aspnet-error-handling
authentication / authorization   -> authentication
external HTTP / resilience       -> httpclient-factory
caching / configuration / DI     -> caching / configuration / dependency-injection
logging                          -> logging
persistence                      -> persistence knowledge facet (decision register)
backend tests                    -> backend-testing knowledge facet (decision register)
frontend                         -> frontend knowledge facet (decision register)
containers / pipelines           -> docker / ci-cd
security-sensitive change        -> security-scan, as justified below
```

Do not introduce or enforce patterns the repository has not adopted (see the decision register's not-adopted styles); differing from an unadopted pattern is not a finding.

## Step 3: Specification conformance

When `SPECIFICATION.md` is non-empty it is the product contract; approved `CUSTOM_SETTINGS.md` values are part of intended behavior. Review both directions: required behavior must not be missing or weakened, and the implementation must not introduce unapproved behavior — new lengths or numeric limits, reserved names or values, observable string-comparison semantics (case sensitivity, collation, culture/ordinal, normalization, trimming) including those expressed only through database configuration or framework defaults, newly required fields, extra workflow restrictions, additional user-visible validation. A detail the user explicitly approved and synchronized into the durable sources is not drift. Do not confuse internal implementation details with product behavior.

## Step 4: Correctness

Look for wrong conditions or state transitions, null/empty edge cases, incorrect async or cancellation handling, incorrect error mapping, resource lifetime problems, unintended side effects, and race conditions where shared state exists. Report only failures with a plausible execution path.

## Step 5: Architecture (check by reference)

When backend code is in scope, check against the loaded owners rather than a private checklist:

- [ ] Role and dependency rules — `.claude/rules/backend/architecture-style.md` and `.claude/rules/backend/architecture.md` (thin controllers, Application Services orchestrate, inward references, commit boundary).
- [ ] Repository contracts and persistence boundary — `.claude/rules/backend/persistence.md`, `.claude/rules/backend/persistence-technology.md`.
- [ ] Proportionality — consequential patterns or extra abstractions appear only with an approved need (`CLAUDE.md`, Decision control).
- [ ] When the persistence model changed: `persistence-change` steps were followed, including the development seeder.

When frontend code is in scope, check against `.claude/rules/frontend/` (feature boundaries, data-access boundary, subscription lifetime, error contract, route guards not treated as server authorization, no unnecessary global state, meaningful tests). Do not apply backend project-boundary rules mechanically to frontend code.

## Step 6: Data and security

Review transaction/commit behavior, destructive data changes, raw SQL parameterization, authorization, input trust boundaries, secrets, sensitive logging, concurrency, migrations, and cache consistency. Run the full `security-scan` procedure only when a security audit was requested, the change is materially security-sensitive, or a concrete finding justifies broader investigation — not for every ordinary review.

## Step 7: Integrations

For external calls check cancellation propagation, timeout strategy, idempotency, retry safety, failure translation, and disposal/lifetime behavior. Never demand retries for operations that are not safe to retry.

## Step 8: Tests

Check that changed behavior has useful maintained automated coverage, focusing on behavior rather than line count. For a bug fix, look for a regression test when recurrence is plausible; behavioral probes used during implementation must be preserved as maintained tests (`verify`, step 4). Do not request duplicate tests when equivalent coverage exists.

## Step 9: Performance

Report performance only for credible reasons: obvious N+1 access, unbounded materialization, blocking async I/O, repeated expensive remote calls, clearly expensive work or allocation in a demonstrated hot path. Do not recommend caching, compiled queries, pooling, `ValueTask`, or similar optimizations speculatively.

## Tooling

Use repository search, compiler diagnostics, analyzers, or other tools when available; no MCP server or specific analyzer is required. Tool output is evidence, not authority: read the code before turning a warning into a finding.

## Output

Report findings ordered by severity. Each finding: severity, file/location, what is wrong, why it matters, smallest reasonable fix.

- **Critical** — data loss, security vulnerability, reliably broken core behavior; blocks use/merge.
- **High** — likely defect or architectural/data-integrity issue to fix before merge.
- **Medium** — real maintainability, robustness, or test gap; not a likely immediate failure.
- **Low** — non-blocking improvement.

Never invent findings to populate a category. When there are no meaningful findings, say so and name important areas that could not be verified. No filler praise.
