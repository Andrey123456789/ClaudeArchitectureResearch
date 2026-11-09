---
paths:
  - "backend/**/*Tests/**/*.cs"
  - "backend/**/*Tests/*.csproj"
  - "frontend/**/*.spec.ts"
  - "frontend/**/e2e/**/*"
---

> Level: 0 Core · Owns: framework-neutral testing principles · Scope: backend-tests (also applied to frontend tests) · Loads: path rule · Depends on: CLAUDE.md

# Testing Principles

Test-framework bindings live in `.claude/rules/2-technology/`. Regression and probe-preservation steps: `development-workflow` and `verify`.

## Test level

- Choose the narrowest test level that meaningfully verifies the behavior (default). Use unit tests for isolated logic; use integration tests when framework wiring, HTTP, persistence, serialization, authentication, or component interaction is what the test must prove. No fixed unit/integration ratio is required.

## Behavior

- Tests must verify observable behavior so that they survive internal refactoring. Do not make tests depend unnecessarily on private methods, exact internal call sequences, specific implementation classes, or incidental refactoring details, and do not reproduce the implementation's algorithm in a test; interaction verification is appropriate when the interaction itself is the specified behavior.
- When provider behavior matters, test against the actual database provider; never claim provider fidelity from a test that runs on a different provider (default).

## Isolation and data

- Tests must be deterministic, independent of execution order, and isolated from Production and Development data, uncontrolled external systems, and shared mutable state between unrelated tests.
- Tests must start from a known state and own their setup; they never depend on development seeding or on other tests having run.

## Readability

- For small finite input/state spaces, prefer explicit declarative cases over loops, branching, LINQ, or generated case machinery inside tests; state expected results instead of computing them (default).
- Use descriptive test names that communicate the scenario or condition and the expected behavior (default), for example `MethodOrScenario_Condition_ExpectedBehavior`; follow an established project convention when one exists.

## Value

- Do not generate low-value tests merely to increase a coverage percentage; coverage is diagnostic information, not a target.
