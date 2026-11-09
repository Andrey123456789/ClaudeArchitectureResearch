---
paths:
  - "backend/**/*Tests/**/*"
---

> Level: 0-core · Owns: framework-neutral backend test policy — levels, behavior focus, determinism and isolation, readability, relational fidelity, test data, coverage, naming · Scope: backend-tests · Loading: path

# Backend Test Rules

- Default: choose the narrowest test level that meaningfully verifies the behavior — unit tests for isolated logic, integration tests when framework wiring, HTTP, persistence, serialization, authentication, or component interaction is the subject. No fixed unit/integration ratio is required.
- Test observable behavior, not implementation details: write tests that survive internal refactoring; do not assert private calls or incidental call sequences or reproduce the implementation's algorithm. Interaction checks fit only when the interaction is the specified behavior.
- Tests must be deterministic, independent of execution order, and isolated from Production and Development data, uncontrolled external systems, and shared mutable state (and from wall-clock timing where `TimeProvider` can make time deterministic).
- Default: for small finite input/state spaces, list explicit declarative cases instead of loops, branching, LINQ, or generated case machinery inside tests, and state expected results instead of computing them.
- Default: use `WebApplicationFactory`-based integration tests when routing, binding, middleware, authentication, DI, repositories, the ORM, or database persistence is what the test must prove.
- Default: use the actual database provider when relational or provider behavior matters (an isolated real-provider container is optional, not required); never claim provider fidelity from a test that runs on a different provider.
- Tests start from a known state and own their setup; they never depend on development seed data or on the order of other tests.
- Do not generate low-value tests merely to raise a coverage percentage.
- Default: use descriptive names that state scenario/condition and expected behavior, such as `MethodOrScenario_Condition_ExpectedBehavior`; follow an established project convention when one exists.

Framework binding: `backend-testing.framework`. Technique: the backend-testing knowledge skill named in the capability selection.
