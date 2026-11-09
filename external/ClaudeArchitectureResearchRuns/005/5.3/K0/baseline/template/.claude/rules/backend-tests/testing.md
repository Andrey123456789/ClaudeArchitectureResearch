---
paths:
  - "backend/**/*Tests/**/*.cs"
  - "backend/**/*Tests/*.csproj"
---

> Kind: STD | Scope: backend-tests | Owner: backend automated tests — framework, level, behavior focus, isolation, data, fidelity, coverage, naming, test-project references | Loading: path-scoped

# Backend Testing Standard

Test stack and project location: D-08. Architecture direction: D-01.

## Framework and level

- Default: NUnit (D-08) for backend automated tests; in an established project that deliberately uses another framework, follow it. Do not introduce a second test framework without a concrete reason.
- Default: choose the narrowest test level that meaningfully verifies the behavior — unit tests for isolated logic, integration tests when framework wiring, HTTP, EF Core, persistence, serialization, authentication or component interaction is the subject. No fixed unit/integration ratio is required.
- Default: use `WebApplicationFactory`-based integration tests when routing, binding, middleware, authentication, DI, repositories, EF Core or database persistence is what the test must prove.

## Behavior

- Tests must verify observable behavior, not implementation details: do not depend on private methods, exact internal call sequences, specific implementation classes or incidental refactoring details, and do not reproduce the implementation algorithm to compute expectations. Interaction verification is appropriate when the interaction itself is the specified behavior.
- Default: for small finite input or state spaces, explicit declarative cases (for example `[TestCase]` rows) instead of loops, branching, LINQ or generated case machinery inside tests.
- Default: descriptive test names that communicate scenario or condition and expected behavior, such as `MethodOrScenario_Condition_ExpectedBehavior`, unless the project has an established convention.
- Do not generate low-value tests merely to increase a coverage percentage.

## Isolation and data

- Tests must be deterministic, independent of execution order, and isolated from Production and Development data, uncontrolled external systems and shared mutable state, and must not rely on wall-clock timing when `TimeProvider` can make time deterministic. Never connect automated tests to Production data.
- Tests must start from a known state and own their setup; they must not depend on development seeding or on test execution order.
- Default: use the actual database provider when relational or provider behavior matters (Testcontainers is optional). Never claim provider fidelity from a different provider, including EF Core InMemory.

## Test project references

- Test projects must not reference production projects more broadly than their test scope requires; they follow the same inward dependency discipline as production code.
