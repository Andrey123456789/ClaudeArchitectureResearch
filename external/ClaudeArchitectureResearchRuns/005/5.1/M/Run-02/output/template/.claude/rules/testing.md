---
paths:
  - "backend/**/*Tests/**/*.cs"
  - "backend/**/*Tests/*.csproj"
---

> Owner: backend test framework, test levels, behavior focus, isolation and test data, provider fidelity, readability, regression and probe preservation, coverage, naming, test-project references | Scope: backend-tests | Loads: path (backend test projects); read explicitly by `verify`, `code-review`, `build-fix`, `project-structure` | Enforced: `.claude/scripts/check-architecture.mjs` (test references), Stop hook test reminder

# Testing Rules

Technique and examples: `dotnet-testing` skill.

## Framework and Test Level

- Default: NUnit is the .NET test framework. Follow an established project that
  deliberately uses another framework, and do not introduce a second framework
  without a concrete reason.
- Default: choose the narrowest test level that meaningfully verifies the
  behavior; no unit/integration ratio is required. Use
  `WebApplicationFactory<Program>` integration tests when routing, model binding,
  middleware, authentication/authorization, dependency injection, repositories,
  EF Core, or database persistence is what the test must prove.
- Default: use the actual database provider when relational or provider behavior
  matters (Testcontainers is optional); do not claim provider fidelity from a
  different provider such as EF Core InMemory.

## Behavior and Readability

- Tests must verify observable behavior rather than implementation details, so
  that they normally survive internal refactoring; do not test private calls or
  reproduce implementation algorithms. Interaction verification is appropriate
  when the interaction itself is the specified behavior.
- Default: for small finite input or state spaces, list explicit declarative
  cases (for example `[TestCase]`) instead of loops, branching, LINQ, or
  generated case machinery inside tests.
- Default: descriptive names that state the scenario or condition and the
  expected behavior, such as `MethodOrScenario_Condition_ExpectedBehavior`.
- Do not generate low-value tests merely to increase a coverage percentage.

## Isolation and Test Data

- Tests must be deterministic, independent of execution order, and isolated from
  Production and Development data, uncontrolled external systems, shared mutable
  state, and wall-clock timing that `TimeProvider` can make deterministic.
- Tests start from a known state and own their setup; they must not depend on
  development seeding, and automated tests never connect to Production data.

## Regression and Behavioral Verification

- Default: for a meaningful bug with plausible recurrence, add a regression test
  unless equivalent coverage already exists.
- If an ad-hoc behavioral probe — a temporary HTTP request, script, manual
  database check, or throwaway test — uniquely demonstrated that behavior works,
  that behavior must be preserved in maintained automated tests before
  completion unless equivalent coverage already exists. The temporary mechanism
  itself need not remain; builds, compiler and analyzer runs, and running
  existing suites do not by themselves require new tests.

## Test Project References

- Do not give backend test projects broader production-project references than
  their test scope requires; keep the inward dependency discipline of the
  production architecture. Typical: `Domain.Tests` → Domain; `Application.Tests`
  → Application (and Domain as needed); `Infrastructure.Tests` → Infrastructure
  with narrower references as required; `IntegrationTests` → Api.
