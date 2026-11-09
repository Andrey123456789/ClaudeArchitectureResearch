---
name: code-review
description: >
  Run for code, PR, or diff reviews and independent defect-focused passes over
  completed changes; owns review priorities and the findings format.
---

> **Workflow skill** · Owns: review procedure, finding priorities, no-manufactured-findings output discipline · Scope: common · Loading: on demand (routed from `development-workflow`; preloaded by the `code-reviewer` agent)

# Code Review

## Goal

Review the actual changed behavior and identify concrete defects or risks.

Prioritize findings in this order:

1. correctness;
2. security and authorization;
3. data integrity and persistence;
4. architectural boundary violations;
5. concurrency and integration behavior;
6. missing meaningful test coverage;
7. maintainability;
8. credible performance problems supported by evidence.

Do not elevate style preferences above behavioral defects, and do not bury
important findings under them.

Code review is not the completion checklist. Use `verify` to run the final
build/test/diff verification.

## Step 1: Establish Scope

Determine what is being reviewed:

- explicit files supplied by the user;
- current working-tree diff;
- branch/PR diff;
- a named feature or module.

Inspect the changed code and enough surrounding code to understand its behavior.

Do not review isolated lines without understanding their callers and dependencies.

## Step 2: Understand Intent

Identify:

- the behavior being added or changed;
- relevant architecture rules;
- expected error cases;
- persistence or external-system effects;
- tests intended to protect the behavior.

Read the rules that govern each changed area (table in `development-workflow` →
Load the Governing Rules); path rules may not have loaded for files you only see
in a diff. Load specialized technique only when relevant, for example:

    persistence                    -> persistence knowledge facet
    backend tests                  -> dotnet-testing
    authentication / authorization -> authentication
    HTTP semantics                 -> http-api
    error handling                 -> aspnet-error-handling
    external HTTP                  -> httpclient-factory
    caching                        -> caching
    configuration / DI             -> configuration / dependency-injection
    frontend                       -> frontend knowledge facet
    Docker / CI                    -> docker / ci-cd

Capability facets are resolved in `docs/capability-selection.md`. Product sources
and their authority, including approved `CUSTOM_SETTINGS.md` values as intended
behavior: `CLAUDE.md` → Product Sources.

## Specification Conformance

Review conformance in both directions:

1. required behavior must not be missing or weakened;
2. the implementation must not silently introduce unapproved product behavior,
   restrictions, validation limits, workflow rules, or defaults.

A reasonable detail absent from the original specification is not automatically
a defect if the user explicitly approved it and the durable project sources were
synchronized.

Flag product drift when implementation invents behavior without approval, for
example:

- new maximum/minimum lengths or numeric limits;
- reserved names or values;
- new or changed observable string-comparison semantics, including case
  sensitivity, collation, culture/ordinal comparison, normalization, or
  trimming behavior;
- newly required fields;
- extra workflow restrictions;
- additional user-visible validation rules.

Do not confuse internal implementation details with product behavior; string
semantics follow `CLAUDE.md` → Product Sources.

## Step 3: Review Correctness

Look for concrete behavioral problems such as:

- wrong conditions or state transitions;
- null/empty edge cases;
- incorrect async behavior;
- incorrect cancellation handling;
- incorrect error mapping;
- resource lifetime problems;
- unintended side effects;
- race conditions where shared state exists.

Do not invent hypothetical failures without a plausible execution path.

## Step 4: Architecture

Verify the architecture frame's boundaries (`architecture-style.md`):

- Domain does not depend on Application, Infrastructure, or API.
- Application does not depend on Infrastructure or the persistence technology.
- Controllers remain thin.
- Application Services orchestrate use cases.
- persistence is accessed through specific repository abstractions.
- persistence-technology types and `IQueryable` do not leak from Infrastructure
  (`persistence-technology.md` lists the types).
- repositories do not independently commit normal use-case changes.
- `IUnitOfWork` remains the Application-facing commit boundary.

For project-reference changes, run `node .claude/scripts/check-architecture.mjs`.

Also check architectural proportionality:

- simple CRUD/workflow applications should normally keep Domain entities simple;
- abstraction count should be justified by actual complexity;
- Rich Domain Models, DDD tactical patterns, CQRS/MediatR/VSA, extra layers,
  project-wide Result models, or similar consequential patterns should not appear
  without an approved need;
- additional abstraction is not inherently better architecture.

Do not report a violation merely because the implementation differs from a
pattern not adopted by this project.

## Frontend Changes

When frontend code is in scope, read `frontend.md` and the frontend rule facet,
and use the frontend knowledge facet.

Review relevant concerns such as:

- feature boundaries and component responsibility;
- HTTP calls being kept behind an appropriate data-access boundary;
- subscription/reactive-state lifetime;
- frontend error handling;
- route guards not being treated as server-side authorization;
- unnecessary global/shared state;
- meaningful frontend test coverage.

Do not apply the backend architecture frame's project-boundary rules mechanically
to frontend source code.

## Step 5: Data and Security

Review changed data-access and security-sensitive code carefully.

Check, when relevant:

- transaction/commit behavior;
- destructive data changes;
- raw SQL parameterization;
- authorization;
- input trust boundaries;
- secrets;
- sensitive logging;
- concurrency;
- migrations;
- development seed-data consistency when Domain/persistence changes affect seeded entities;
- cache consistency.

When a migration or Domain-model change affects entities represented by
development seed data, verify that the development seeder was updated and the
migration was reviewed (`development-workflow` → Change-Specific Obligations).

Perform normal security review of changed code. Use the full `security-scan`
procedure only when the user requested a security audit, the change is materially
security-sensitive, or a concrete finding justifies broader investigation.

## Step 6: Integrations

For external calls, check:

- cancellation propagation;
- timeout strategy;
- idempotency where relevant;
- retry safety;
- failure translation;
- disposal/lifetime behavior.

Do not demand retries for operations that are not safe to retry.

## Step 7: Tests

Determine whether changed behavior has useful automated coverage.

Focus on behavior rather than line count.

For bugs, look for a regression test when recurrence is plausible.

For behavioral probes created during implementation, check `verify` → Preserve
Behavioral Verification.

Do not request duplicate tests when equivalent coverage already exists.

## Step 8: Performance

Report performance concerns when they are credible, for example:

- obvious N+1 database access;
- unbounded materialization;
- repeated expensive external calls;
- blocking async I/O;
- obvious high-volume allocation in a demonstrated hot path.

Do not recommend compiled queries, pooling, caching, `ValueTask`, or similar
micro-optimizations without a reason.

## Optional Tooling

Use compiler diagnostics, analyzers, IDE/Roslyn tooling, or repository-specific
analysis tools when available.

Tool output is evidence, not authority.

Do not require an MCP server or a particular analyzer for the review to work.

Read the code before turning a tool warning into a review finding.

## Output

For each finding provide:

- severity;
- file/location;
- what is wrong;
- why it matters;
- the smallest reasonable fix.

Suggested severity:

### Critical

Data loss, security vulnerability, reliably broken core behavior, or another
issue that should block use/merge immediately.

### High

Likely defect or architectural/data-integrity issue that should normally be
fixed before merge.

### Medium

Real maintainability, robustness, or test gap worth addressing, but not a likely
immediate production failure.

### Low

Non-blocking improvement.

Do not manufacture findings to populate every severity or category.

If no meaningful problem is found, say so and state any important areas that
could not be verified.

## Review Discipline

Do not:

- rewrite working code during a review unless asked;
- report formatting already owned by tooling as a defect;
- demand personal style preferences;
- assume every warning is a bug;
- require patterns the project has intentionally not adopted (for example
  MediatR, CQRS, Vertical Slice Architecture, Minimal APIs, Rich Domain Models,
  Domain Events, or generic repositories);
- praise filler solely to balance criticism.
