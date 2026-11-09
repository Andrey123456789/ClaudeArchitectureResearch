---
paths:
  - "backend/**/*Tests/**/*"
---
> Level: 0-core | Owns: framework-neutral backend test policy — levels, behavior focus, determinism, isolation, fidelity, naming | Scope: backend-tests | Loads: path (backend test projects)

# Testing Rules

The test framework and its specific rules come from the `backend-testing`
selection (`backend-testing.rules`).

## Test level

Default: choose the narrowest test level that meaningfully verifies the
behavior — unit tests for isolated domain/use-case logic, integration tests when
framework wiring, HTTP, persistence, serialization, authentication, or component
interaction is what matters. No fixed unit/integration ratio is required; do not
require integration tests for every behavior or unit tests for behavior that is
naturally verified at an integration boundary.

Default: use `WebApplicationFactory`-based integration tests when routing,
model binding, middleware, authentication/authorization, dependency injection,
persistence implementations, or database persistence is what the test must
prove.

## Behavior over implementation

Tests must verify observable behavior and survive internal refactoring: do not
make them depend unnecessarily on private methods, exact internal call
sequences, specific implementation classes, or incidental refactoring details,
and do not reproduce the implementation's algorithm to compute expected
results. Interaction verification is appropriate only when the interaction is
itself the specified behavior.

Default: for small finite input/state spaces, use explicit declarative cases
instead of loops, branches, LINQ, or generated case machinery inside tests;
state expected results instead of calculating them.

## Determinism and isolation

- Tests must be deterministic, independent of execution order, and isolated from
  Production and Development data, uncontrolled external systems, and shared
  mutable state; use `TimeProvider` instead of wall-clock timing.
- Tests start from a known state and own their setup; they must not depend on
  development seeding or on other tests. Never connect automated tests to
  Production data.

## Database fidelity

Default: use the actual database provider (declared in the capability
selection) when relational or provider behavior matters; an isolated
container-hosted instance is optional, not mandatory. Never claim provider
fidelity from a different provider, including an in-memory provider.

## Value and naming

- Do not generate low-value tests merely to increase a coverage percentage.
- Default: descriptive test names that state scenario/condition and expected
  behavior, e.g. `MethodOrScenario_Condition_ExpectedBehavior`, or the project's
  established convention.

Regression and probe-preservation duties: `develop` and `verify`. Technique:
`backend-testing.knowledge`.
