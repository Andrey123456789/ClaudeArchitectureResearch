---
paths:
  - "backend/**/*Tests/**/*"
---

> Kind: STD | Scope: backend-tests | Capability: — | Loading: path-scoped (frontmatter paths)

# Backend Testing Standard (framework-neutral)

The selected test framework adds its rules in `test-framework.md`; test-project references are governed by `test-projects.md`.

## Level and focus

- Default: the narrowest test level that meaningfully verifies the behavior; integration tests when framework wiring, HTTP, persistence, serialization, or authentication is the subject. No fixed unit/integration ratio is required.
- Tests must verify observable behavior, not implementation details: they survive internal refactoring, do not test private calls or exact internal call sequences, and do not reproduce the implementation's algorithm. Interaction verification is appropriate only when the interaction itself is the specified behavior.
- Default: `WebApplicationFactory`-based integration tests when routing, model binding, middleware, authentication/authorization, dependency injection, repositories, the persistence technology, or database persistence is what the test must prove.
- Default: the actual database provider when relational or provider behavior matters (Testcontainers is optional); never claim provider fidelity from a test that runs against a different provider.

## Determinism and data

- Tests must be deterministic, independent of execution order, and isolated from Production and Development data, uncontrolled external systems, and shared mutable state.
- Tests must start from a known state and own their setup; never depend on development seed data or on the order in which other tests run.

## Readability and value

- Default: for small finite input/state spaces, explicit declarative cases instead of loops, branches, LINQ, or generated case machinery inside tests; expected results are stated by the test, not computed.
- Default: descriptive test names that communicate scenario/condition and expected behavior, e.g. `MethodOrScenario_Condition_ExpectedBehavior`, unless the project has an established convention.
- Must not generate low-value tests merely to increase a coverage percentage.

Technique: the backend-testing knowledge facet named in the decision register. Regression tests and probe preservation: `development-workflow`, `verify`.
