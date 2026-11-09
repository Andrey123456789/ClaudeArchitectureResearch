---
paths:
  - "backend/**/*Tests/**/*.cs"
  - "backend/**/*Tests/*.csproj"
---

> Owns: backend test framework, test level, behavior focus, isolation, test data ownership, provider fidelity, coverage, naming | Scope: backend-tests | Loads: path

# Testing Rules

Test-project references: `architecture.md`. Preserving behavioral probes and
regression coverage before completion: `verify` workflow. Technique:
`dotnet-testing` skill (frontend tests: `angular` skill).

## Framework

NUnit (`docs/technology-stack.md`) is the default. Follow an established project
that deliberately uses another framework, but do not introduce a second
framework without a concrete reason.

## Test Level

By default, choose the narrowest test level that meaningfully verifies the
behavior: unit tests for isolated business/domain/application logic;
`WebApplicationFactory`-based integration tests when routing, binding,
middleware, authentication, DI, repositories, EF Core, serialization, or
database persistence is what the test must prove. No unit/integration ratio is
required.

## Behavior Over Implementation

Tests verify observable behavior and survive internal refactoring. Do not depend
on private methods, exact internal call sequences, specific implementation
classes, or reproduced implementation algorithms; interaction verification is
appropriate only when the interaction itself is the specified behavior.

## Readability

For small finite input/state spaces, prefer explicit declarative cases (for
example `[TestCase]`) over loops, branches, LINQ, or generated case machinery
inside tests, and state expected results rather than computing them. Prefer one
observable scenario per test unless the sequence itself is the behavior.

## Isolation and Test Data

- Tests must be deterministic, independent of execution order, and isolated
  from Production/Development data, uncontrolled external systems, and shared
  mutable state (use `TimeProvider` instead of wall-clock timing).
- Tests start from a known state and own their setup; never depend on
  development seeding.

## Database Tests

By default, use the actual database provider when relational/provider behavior
matters; Testcontainers is optional. Never claim provider fidelity from a
different provider (including EF Core InMemory).

## Test Doubles

Use fakes, stubs, or mocks when they make an isolated test clearer; do not mock
every dependency mechanically. When important behavior depends on real
EF Core/provider/HTTP semantics, prefer an integration test.

## Coverage

Do not generate low-value tests merely to increase a coverage percentage.

## Naming

Use descriptive names that communicate scenario/condition and expected
behavior, for example `MethodOrScenario_Condition_ExpectedBehavior`, unless the
project has an established convention.
