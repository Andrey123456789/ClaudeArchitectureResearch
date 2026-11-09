---
name: code-review
description: Use for code reviews, PR reviews, reviewing a diff, or a defect-focused second pass over completed .NET or frontend changes. Reviews correctness, specification conformance, architecture boundaries, data integrity, security, integrations, tests and credible performance risks.
---
Kind: WF | Scope: common | Capability: — | Loading: on invocation; preloaded by the code-reviewer agent

# Code Review

Goal: review the actual changed behavior and identify concrete defects or risks. Code review is not the completion checklist; `verify` runs the final build, test and diff verification.

## Priorities

Prioritize findings in this order: correctness; security and authorization; data integrity and persistence; architectural boundary violations; concurrency and integration behavior; missing meaningful tests; maintainability; performance problems supported by evidence. Do not elevate style preferences above behavioral defects or bury important findings under them.

## 1. Establish scope

Determine what is reviewed: files supplied by the user, the current working-tree diff, a branch or PR diff, or a named feature or module. Read enough surrounding code (callers, contracts, dependencies) to understand the changed behavior; do not review isolated lines.

## 2. Understand intent and load owners

- Identify the behavior added or changed, the expected error cases, persistence and external-system effects, and the tests intended to protect it.
- Read the standards that govern the changed area from `.claude/rules/<scope>/` (they may not be loaded in a review context). For slot concerns, use the selected modules' knowledge facets (decision register → Capability selection).
- Product contract: `SPECIFICATION.md` and approved `CUSTOM_SETTINGS.md` values (`CLAUDE.md` → Product behavior, Tunable settings).

## 3. Specification conformance

Review conformance in both directions (`CLAUDE.md` → Product behavior, Tunable settings):

- Is required behavior missing or weakened?
- Does the implementation add unapproved product behavior: new limits or lengths, reserved values, new observable string-comparison semantics (case sensitivity, collation, culture or ordinal comparison, normalization, trimming), newly required fields, extra workflow restrictions or user-visible validation rules?

A detail absent from the specification is not a defect when the user approved it and the durable sources were synchronized. A newly chosen observable string-comparison behavior is not an internal detail merely because database configuration or a framework default expresses it. Do not confuse internal implementation details with product behavior.

## 4. Correctness

Look for wrong conditions or state transitions, null or empty edge cases, incorrect async or cancellation handling, incorrect error mapping, resource-lifetime problems, unintended side effects, and races where shared state exists. Do not invent hypothetical failures without a plausible execution path.

## 5. Architecture

- Backend boundaries hold? (`.claude/rules/backend/architecture.md`, `.claude/rules/backend/architecture-style.md`, persistence standards). Run `node .claude/scripts/check-architecture.mjs` when references or packages changed.
- Complexity proportional? No pattern, layer, abstraction or project-wide model the register does not adopt, without approval (`CLAUDE.md` → Decision control).
- Do not report a violation merely because the code differs from a pattern this project has not adopted, and do not require patterns it has not adopted.

## 6. Frontend changes

When frontend code is in scope, check it against `.claude/rules/frontend/` and the frontend knowledge facet: feature boundaries and component responsibility, the data-access boundary, subscription and reactive-state lifetime, error-contract handling, route guards not treated as authorization, unnecessary global or shared state, meaningful frontend tests. Do not apply backend project-boundary rules mechanically to frontend source code.

## 7. Data and security

When relevant, check commit and transaction behavior, destructive data changes, raw SQL parameterization, authorization, input trust boundaries, secrets, sensitive logging, concurrency, migrations (persistence workflow facet → Model or schema change), cache consistency, and whether a Domain or persistence change that affects seeded entities updated the development seeder. Use the full `security-scan` only when the user asked for a security audit, the change is materially security-sensitive, or a concrete finding justifies broader investigation; do not turn every review into a full OWASP audit.

## 8. Integrations

For external calls, check cancellation propagation, timeouts, idempotency, retry safety, failure translation and disposal or lifetime behavior (`.claude/rules/backend/integrations.md`). Do not demand retries for operations that are not safe to retry.

## 9. Tests

Does the changed behavior have useful maintained automated coverage? Focus on behavior, not line count. For a bug fix, look for a regression test when recurrence is plausible. Behavior proven by temporary probes must be preserved as maintained tests (`verify` → step 4). Do not request duplicate tests when equivalent coverage exists.

## 10. Performance

Report performance findings only for a credible reason: obvious N+1 database access, unbounded materialization, blocking asynchronous I/O, repeated expensive remote calls, or high-volume allocation in a demonstrated hot path. Do not recommend compiled queries, pooling, caching, `ValueTask` or similar optimizations speculatively.

## Tooling

Compiler diagnostics, analyzers, IDE tooling and repository scripts are evidence, not authority, and no MCP server or specific analyzer is required. Read the code before turning a tool warning into a finding.

## Output

Report findings ordered by severity. For each finding give the severity, file and location, what is wrong, why it matters, and the smallest reasonable fix.

- **Critical**: data loss, a security vulnerability, reliably broken core behavior, or another issue that should block use or merge immediately.
- **High**: a likely defect or architectural or data-integrity issue that should be fixed before merge.
- **Medium**: a real maintainability, robustness or test gap that is not a likely immediate production failure.
- **Low**: a non-blocking improvement.

Do not manufacture findings to populate categories. When there are no meaningful findings, say so and name the important areas that could not be verified.

## Review discipline

Do not rewrite working code during a review unless asked, report formatting that tooling owns as a defect, demand personal style preferences, assume every warning is a bug, or add filler praise to balance criticism.
