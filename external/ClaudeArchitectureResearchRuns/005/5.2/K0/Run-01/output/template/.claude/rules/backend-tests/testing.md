---
paths:
  - "backend/**/*Tests/**"
---
<!-- Kind: STD | Scope: backend-tests | Owns: test framework use, test level, behavior focus, isolation, readability, test-project references | Loads: path-scoped (backend/**/*Tests/**) -->
# Backend Test Standards

Test stack and test-project placement: DEC-TEST-01.

## Framework and Level

- **Default:** NUnit (DEC-TEST-01) for .NET tests; do not introduce a second test framework without a concrete reason. In an established project that deliberately uses another framework, follow its convention.
- **Default:** the narrowest test level that meaningfully verifies the behavior — unit tests for isolated business, domain or application logic; integration tests when framework wiring, HTTP, EF Core, persistence, serialization, authentication or component interaction is what matters. No fixed unit/integration ratio is required.
- **Default:** `WebApplicationFactory`-based integration tests when routing, binding, middleware, authentication/authorization, DI, repositories, EF Core or database persistence is what the test must prove.
- **Default:** the actual database provider when relational or provider behavior matters (Testcontainers is optional); do not claim provider fidelity from a different provider, and do not use EF Core InMemory while claiming relational behavior.

## Behavior and Isolation

- Tests **must** verify observable behavior rather than implementation details, so they survive internal refactoring: no dependence on private methods, exact internal call sequences, specific implementation classes or incidental refactoring details, and no reproduction of the implementation's algorithm. Interaction verification is appropriate when the interaction itself is the specified behavior.
- Tests **must** be deterministic, independent of execution order, and isolated from Production and Development data, uncontrolled external systems and shared mutable state; use `TimeProvider` rather than wall-clock timing.
- Tests **must** start from a known state they own and **must not** depend on development seeding or on the order in which other tests run.

## Readability and Value

- **Default:** for small finite input or state spaces, explicit declarative cases (for example NUnit `[TestCase]`) instead of loops, branching, LINQ or generated case machinery inside tests; expected results are stated by the test, not computed.
- **Must not** generate low-value tests merely to increase a coverage percentage.
- **Default:** descriptive test names that state scenario or condition and expected behavior, such as `MethodOrScenario_Condition_ExpectedBehavior`, unless the project has an established convention.

## Test Project References

- Backend test projects **must not** reference more production projects than their test scope requires; they keep the inward dependency discipline of the production architecture.

Workflow: behavioral probes — `verify` § 4; regression tests for bug fixes — `development-workflow` § Co-change Obligations.
Technique: `dotnet-testing` knowledge skill.
