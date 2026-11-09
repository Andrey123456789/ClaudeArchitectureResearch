---
paths:
  - "backend/**/*Tests/**"
---

> Level: 0 Core · Owns: framework-neutral testing principles · Scope: backend-tests · Loads: path; read explicitly by `verify`, `build-fix`, `code-review`

# Testing Principles

## Choosing and writing tests

- **Default:** choose the narrowest test level that meaningfully verifies the behavior — unit tests for isolated logic; integration tests when framework wiring, HTTP, persistence, serialization, authentication or component interaction is what must be proven. No fixed unit/integration ratio is required, and behavior naturally verified at an integration boundary needs no duplicate unit test.
- **Must** verify observable behavior that survives internal refactoring. Do not test private methods, exact internal call sequences or incidental implementation details, and do not reproduce the implementation's algorithm in the test. Interaction verification is appropriate only when the interaction itself is the specified behavior.
- **Default:** for small finite input or state spaces, write explicit declarative cases instead of loops, branching, LINQ or generated case machinery inside tests; state expected results rather than computing them; one observable scenario per test unless the sequence itself is the behavior.
- **Default:** use descriptive names that state scenario, condition and expected behavior — `MethodOrScenario_Condition_ExpectedBehavior` unless the project has an established convention.
- **Must not** add low-value tests merely to raise a coverage percentage.

## Isolation and data

- **Must** keep tests deterministic, independent of execution order, and isolated from Production and Development data, uncontrolled external systems and shared mutable state. Control time through the time abstraction instead of wall-clock waits.
- **Must** start every test from a known state that the test suite owns. Tests never depend on development seed data or on the execution order of other tests, and never connect to Production data.
- **Default:** use the actual database provider when relational or provider-specific behavior matters (constraints, transactions, locking/concurrency, indexes, raw SQL, provider mappings, migrations). Containerized real-provider databases are optional. Never claim provider fidelity from a different or in-memory provider.

## Regression and behavioral verification

- **Default:** when fixing a meaningful bug whose recurrence is plausible, add a regression test that fails before the fix and passes after it, unless equivalent coverage already exists.
- **Must** preserve behavior that an ad-hoc probe uniquely demonstrated — a temporary HTTP request, script, database check or throwaway test — as maintained automated coverage before completion, unless an existing test already exercises that behavior (confirm that it does). The temporary mechanism itself need not remain. Builds, compiler checks, static analysis, formatting and running the existing suite need no new tests. Completion is never declared on a behavioral check that exists only outside the maintained suite.
