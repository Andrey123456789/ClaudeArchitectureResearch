---
paths:
  - "backend/**/*Tests/**/*.cs"
  - "backend/**/*Tests/*.csproj"
---

> Path rule · Scope: backend-tests · Owns framework-independent test policy: level, behavior focus, readability, isolation, data ownership, provider fidelity, coverage, and naming

# Testing Rules

Test framework and its conventions: `.claude/rules/test-framework.md`.
Preserving behavioral probes and regression coverage: `verify` and
`development-workflow`. Technique: `dotnet-testing` skill.

## Test Level

Choose the narrowest test level that meaningfully verifies the behavior. Use
unit tests for isolated business, domain, or application logic; use integration
tests when framework wiring, HTTP, persistence, serialization, authentication,
or component interaction is what matters. No fixed unit/integration ratio is
required, and neither level is required for behavior naturally verified by the
other.

Use `WebApplicationFactory<Program>`-based integration tests when routing,
binding, middleware, authentication/authorization, dependency injection,
repositories, or database persistence is what the test must prove.

## Behavior Over Implementation

Tests verify observable behavior and survive internal refactoring. Avoid
depending on private methods, exact internal call sequences, specific
implementation classes, or incidental refactoring details, and do not reproduce
implementation algorithms in tests. Interaction verification is appropriate
when the interaction itself is part of the specified behavior.

## Test Readability

For small finite input or state spaces, prefer explicit declarative test cases
over loops, branches, LINQ, or generated case machinery inside tests; state
expected results rather than computing them. Prefer one observable scenario per
test; a multi-step test is appropriate when the sequence itself is the behavior.

## Test Doubles

Use fakes, stubs, or mocks when they make an isolated test clearer; do not mock
every dependency mechanically, and do not forbid mocking project-owned
abstractions. When important behavior depends on real persistence, provider, or
HTTP semantics, prefer an integration test over reproducing that behavior with
mocks.

## Database Tests

Use the actual database provider when relational or provider-specific behavior
matters; an isolated real-provider setup such as Testcontainers is optional,
not mandatory for every project or integration test. Do not claim provider
fidelity from a different or non-relational provider; the provider binding is
in `.claude/rules/persistence-technology.md`.

## Isolation and Test Data

- Tests must be deterministic, independent of execution order, and isolated from
  Production and Development data, uncontrolled external systems, and shared
  mutable state between unrelated tests. Do not rely on wall-clock timing when
  `TimeProvider` can make time deterministic. Never connect automated tests to
  Production data.
- Tests start from a known state and own their setup; they do not depend on
  development seed data or on execution order.

## Coverage

Coverage is diagnostic information. Do not generate low-value tests merely to
increase a coverage percentage.

## Naming

By default use descriptive test names that communicate the scenario or
condition and the expected behavior, for example
`MethodOrScenario_Condition_ExpectedBehavior`; follow an established project
convention when one exists.
