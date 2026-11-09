---
paths:
  - "backend/**/*Tests/**/*.cs"
  - "backend/**/*Tests/*.csproj"
---

> **Policy rule** · Owns: framework-independent backend test policy (levels, behavior focus, readability, isolation, fidelity, coverage, naming) · Scope: backend-tests · Loading: path (backend test projects)

# Testing Rules

## Framework

The backend test framework is the selected backend-testing capability; its rule
facet is `test-framework.md`. Technique and examples: the `dotnet-testing` skill.

## Test Level

Choose the narrowest test level that meaningfully verifies the behavior.

- Use unit tests for isolated business/domain/application logic.
- Use integration tests when framework wiring, HTTP, persistence technology,
  persistence, serialization, authentication, or component interaction is what
  matters.
- Default: when routing, model binding, middleware, authentication/authorization
  wiring, DI, repositories, the persistence technology, or database persistence is
  what the test must prove, use a `WebApplicationFactory<Program>`-based
  integration test.
- Do not require integration tests for every behavior.
- Do not require unit tests for behavior that is naturally verified through an
  integration boundary.

There is no required unit/integration test ratio.

## Behavior Over Implementation

Test observable behavior rather than private implementation details.

Do not make tests depend unnecessarily on:

- private methods;
- exact internal call sequences;
- specific implementation classes;
- incidental refactoring details.

Interaction verification is appropriate when the interaction itself is part of
the behavior being specified.

## Test Readability

Keep test code simpler to reason about than the production behavior it
verifies.

Default: use explicit, declarative test cases rather than loops, branches, generated test
matrices, or code that computes the expected result when the relevant cases
can reasonably be listed directly.

Prefer one observable scenario per test. A multi-step test is appropriate when
the sequence itself is the behavior being verified.

Detailed test-structure guidance belongs to the `dotnet-testing` skill.

## Test Doubles

Use fakes, stubs, or mocks when they make an isolated test clearer.

Do not mock every dependency mechanically.

Do not forbid mocking project-owned abstractions when isolation is useful.

When important behavior depends on real persistence-technology, provider, or HTTP
semantics, prefer an integration test instead of reproducing that behavior
through mocks.

## Database Tests

Do not use an in-memory or other non-relational substitute while claiming to
verify relational database behavior (the persistence capability declares its
relational-testing binding).

Use the actual database provider when relational or provider behavior matters,
and do not claim provider fidelity from a test that runs against a different
provider.

Testcontainers is a valid option for isolated real-provider tests, but it is
not mandatory for every project or integration test.

Never connect automated tests to Production data.

## Isolation

Tests must be deterministic, independent of execution order, and start from a
known state.

Do not rely on:

- shared mutable state between unrelated tests;
- wall-clock timing when `TimeProvider` can make time deterministic;
- uncontrolled external services;
- Development or Production seed data.

Tests own their own setup and test data.

## Behavioral Verification

Preserving behavior proven by temporary probes as maintained tests is a
completion obligation owned by `verify` → Preserve Behavioral Verification.

## Coverage

Coverage is diagnostic information, not a quality target by itself. Do not
generate low-value tests merely to increase a coverage percentage.

## Naming

Use descriptive test names that communicate scenario and expected behavior.

A useful default is:

```text
MethodOrScenario_Condition_ExpectedBehavior
```

Follow an existing project naming convention when one is already established.
