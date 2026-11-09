---
paths:
  - "backend/**/*Tests/**/*.cs"
  - "backend/**/*Tests/*.csproj"
---

> Owns: backend test framework use, test level, behavior focus, isolation, provider fidelity, test data ownership, readability, coverage, naming | Scope: backend-tests | Loads: path-scoped (backend test projects)

# Testing Rules

Regression tests for bug fixes: `development-workflow`. Preserving behavioral
probes as tests: `verify`. Technique and examples: `dotnet-testing` skill.

## Framework

Use NUnit, the approved framework in `docs/technology-stack.md`, as the default
.NET test framework, and do not introduce a second test framework without a
concrete reason. An established project that deliberately uses another
framework keeps its convention.

## Test Level

- Choose the narrowest test level that meaningfully verifies the behavior: unit
  tests for isolated business, domain, or application logic; integration tests
  when framework wiring, HTTP, EF Core, persistence, serialization,
  authentication, or component interaction is what matters. No fixed
  unit/integration ratio is required: do not require integration tests for
  every behavior, or unit tests for behavior that is naturally verified through
  an integration boundary.
- Use `WebApplicationFactory<Program>`-based integration tests when routing,
  model binding, middleware, authentication/authorization, dependency
  injection, repositories, EF Core, or database persistence is what the test
  must prove.

## Behavior Over Implementation

Tests verify observable behavior and survive internal refactoring by default.
Do not make tests depend on private methods, exact internal call sequences,
specific implementation classes, or incidental refactoring details, and do not
reproduce the implementation algorithm in the test. Interaction verification is
appropriate when the interaction itself is part of the specified behavior.

## Readability

For small finite input or state spaces, prefer explicit declarative cases (for
example `[TestCase]`) over loops, branches, LINQ, generated case machinery, or
code that computes the expected result. Prefer one observable scenario per test;
a multi-step test fits when the sequence itself is the behavior.

## Isolation and Test Data

- Tests must be deterministic, independent of execution order, and isolated
  from Production and Development data, uncontrolled external systems,
  wall-clock timing (use `TimeProvider`), and shared mutable state. Never
  connect automated tests to Production data.
- Tests start from a known state and own their setup; they do not depend on
  development seeding or on the execution order of other tests.

## Database Tests

Use the actual database provider when relational or provider behavior matters;
Testcontainers is an approved option, not a requirement. Do not claim provider
fidelity from a different provider, and do not use EF Core InMemory while
claiming to verify relational database behavior.

## Coverage

Do not generate low-value tests merely to increase a coverage percentage.

## Naming

Use descriptive test names that communicate the scenario or condition and the
expected behavior. The default pattern is
`MethodOrScenario_Condition_ExpectedBehavior` unless the project already has an
established convention.
