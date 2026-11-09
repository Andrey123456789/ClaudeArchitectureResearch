---
paths:
  - "backend/**/*Tests/**/*.cs"
  - "backend/**/*Tests/*.csproj"
---

> Path-scoped rule. Owns: backend test framework use, test level, behavior focus, readability, test doubles, provider fidelity, determinism and isolation, test-data ownership, coverage discipline, naming · Scope: backend-tests · Loads: when backend test files are in context · Depends on: CLAUDE.md, docs/technology-stack.md

# Testing Rules

Regression tests for bug fixes: `development-workflow`. Preserving behavioral
probes as maintained tests: `verify`. Technique: `dotnet-testing` skill.

## Framework

- Default: NUnit, the stack's test framework, for .NET automated tests; in an
  established project that deliberately uses another framework, follow that
  convention. Do not introduce a second test framework without a concrete
  reason.

## Test Level

- Default: choose the narrowest test level that meaningfully verifies the
  behavior — unit tests for isolated business, domain, or application logic;
  integration tests when framework wiring, HTTP, EF Core, persistence,
  serialization, authentication, or component interaction is what matters.
  There is no required unit/integration ratio.
- Default: use `WebApplicationFactory<Program>`-based integration tests when
  routing, binding, middleware, authentication, dependency injection,
  repositories, EF Core, or database persistence is what the test must prove.

## Behavior Over Implementation

- Tests must verify observable behavior rather than implementation details and
  must survive internal refactoring: do not make them depend on private
  methods, exact internal call sequences, specific implementation classes, or
  incidental refactoring details, unless the interaction itself is the
  specified behavior. Do not reproduce the implementation's algorithm to compute
  expected results.

## Readability

- Default: for small finite input or state spaces, write explicit declarative
  cases (for example `[TestCase]`) instead of loops, branching, LINQ, or
  generated case machinery inside tests. Prefer one observable scenario per
  test; a multi-step test fits when the sequence itself is the behavior.

## Test Doubles

- Use fakes, stubs, or mocks when they make an isolated test clearer; do not
  mock every dependency mechanically. When behavior depends on real EF Core,
  provider, or HTTP semantics, prefer an integration test over reproducing that
  behavior with mocks.

## Database Tests

- Default: use the actual database provider when relational or provider
  behavior matters. Testcontainers is one option, not a requirement. Do not
  claim provider fidelity from a different provider, and do not use EF Core
  InMemory while claiming to verify relational behavior.

## Isolation and Test Data

- Tests must be deterministic, independent of execution order, and isolated
  from Production and Development data, uncontrolled external systems, and
  shared mutable state between unrelated tests; use `TimeProvider` rather than
  wall-clock timing where time matters.
- Tests must start from a known state and own their setup; they must not depend
  on development seed data or on other tests having run.

## Coverage

- Do not generate low-value tests merely to increase a coverage percentage.

## Naming

- Default: descriptive test names that state the scenario or condition and the
  expected behavior, for example `MethodOrScenario_Condition_ExpectedBehavior`;
  follow an established project convention when one exists.
