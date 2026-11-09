---
paths:
  - "backend/**/*Tests/**"
---
Kind: STD | Scope: backend-tests | Capability: — | Loading: path-scoped (backend test projects)

# Backend Testing Standards (framework-neutral)

Framework bindings: `.claude/rules/backend-tests/test-framework.md`. Technique: the backend-testing knowledge facet (decision register → Capability selection). Completion obligations for tests (preserving probes, regression tests): `verify`.

- Default: choose the narrowest test level that meaningfully verifies the behavior. Use unit tests for isolated logic, and integration tests when framework wiring, HTTP, persistence, serialization, authentication or component interaction is what matters. No fixed unit/integration ratio is required.
- Tests must verify observable behavior rather than implementation details, so that they survive ordinary internal refactoring. Avoid testing private methods, exact internal call sequences or incidental implementation classes, and do not reproduce the implementation's algorithm inside the test. Interaction verification is appropriate when the interaction itself is the specified behavior.
- Tests must be deterministic, independent of execution order, and isolated from Production and Development data, uncontrolled external systems, wall-clock time (use `TimeProvider`) and shared mutable state between unrelated tests. Never connect automated tests to Production data.
- Default: for small, finite input or state spaces, list explicit declarative cases instead of loops, branches, LINQ or generated case machinery inside tests. The test states the expected result instead of computing it.
- Default: use `WebApplicationFactory<Program>`-based integration tests when routing, model binding, middleware, authentication, dependency injection, repositories, the persistence technology or database persistence is what the test must prove. The test environment uses isolated resources.
- Default: use the actual database provider when relational or provider behavior matters; Testcontainers is a valid option, not a requirement. Never claim provider fidelity from a test that runs against a different provider.
- Tests start from a known state and own their setup. They never depend on development seeding or on the order of other tests.
- Do not write low-value tests merely to raise a coverage percentage.
- Default: give tests descriptive names that state the scenario or condition and the expected behavior, for example `MethodOrScenario_Condition_ExpectedBehavior`, unless the project has an established convention.
