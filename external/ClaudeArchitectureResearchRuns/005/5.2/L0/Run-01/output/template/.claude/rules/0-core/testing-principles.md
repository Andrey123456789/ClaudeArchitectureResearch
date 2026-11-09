---
paths:
  - "backend/**/*Tests/**"
---

> Level: 0 Core | Owns: framework-neutral test principles (level, behavior, isolation, fidelity, readability, data ownership, coverage, naming) | Scope: backend-tests | Loads: path | Depends on: none

# Testing Principles

- Default: choose the narrowest test level that meaningfully verifies the
  behavior. Use unit tests for isolated logic and integration tests when
  framework wiring, HTTP, persistence, serialization, authentication, or
  component interaction is the subject. No fixed unit/integration ratio is
  required.
- Tests verify observable behavior and normally survive internal refactoring;
  avoid testing private calls or reproducing the implementation algorithm.
  Interaction verification is appropriate when the interaction itself is part
  of the specified behavior.
- Tests must be deterministic, independent of execution order, and isolated
  from Production and Development data, uncontrolled external systems, and
  shared mutable state; do not rely on wall-clock timing where time can be made
  deterministic.
- Tests start from a known state and own their setup; they do not depend on
  development seed data or on other tests.
- Default: when relational or provider behavior matters, test against the
  actual database provider; never claim provider fidelity from a different
  provider.
- Default: for small finite input or state spaces, prefer explicit declarative
  cases over loops, branches, LINQ, or generated case machinery inside tests;
  state expected results instead of computing them.
- Do not generate low-value tests merely to raise a coverage percentage.
- Default: use descriptive names that state scenario or condition and expected
  behavior, for example `MethodOrScenario_Condition_ExpectedBehavior`.

Test framework and integration-test bindings: → `2-technology/backend-testing.md`.
