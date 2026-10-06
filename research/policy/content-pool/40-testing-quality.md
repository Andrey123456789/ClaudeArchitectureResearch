# Testing & Quality

> Shared normalized content pool. Research artifact, not a runtime candidate file.
> Each policy ID must map to exactly one runtime normative owner in every experimental candidate.

Test strategy, isolation, readability, regression coverage and preservation of behavioral verification.

## TST-001 — NUnit is default backend test framework

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend-tests
- **Source:** `templates/v2-baseline/.claude/rules/testing.md#Framework`, `templates/v2-baseline/.claude/skills/testing/SKILL.md#Core Principles`

Use NUnit as the default .NET automated test framework; do not introduce a second framework without a concrete reason.

## TST-002 — Choose narrowest useful test level

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend-tests
- **Source:** `templates/v2-baseline/.claude/rules/testing.md#Test Level`, `templates/v2-baseline/.claude/skills/testing/SKILL.md#Core Principles`

Choose the narrowest test level that meaningfully verifies the behavior; use integration tests when framework/persistence/HTTP wiring is the subject; no fixed unit/integration ratio is required.

## TST-003 — Test behavior, not implementation details

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend-tests
- **Source:** `templates/v2-baseline/.claude/rules/testing.md#Behavior Over Implementation`, `templates/v2-baseline/.claude/skills/testing/SKILL.md#Core Principles`

Tests should verify observable behavior and normally survive internal refactoring; avoid testing private calls or reproducing implementation algorithms.

## TST-004 — Tests are deterministic and isolated

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend-tests
- **Source:** `templates/v2-baseline/.claude/rules/testing.md#Isolation`, `templates/v2-baseline/.claude/skills/testing/SKILL.md#Core Principles`

Tests must be deterministic, independent of execution order, and isolated from Production/Development data, uncontrolled external systems and shared mutable state.

## TST-005 — Prefer explicit test cases

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend-tests
- **Source:** `templates/v2-baseline/.claude/skills/testing/SKILL.md#Test Readability`

For small finite input/state spaces, prefer explicit declarative cases over loops, branching, LINQ or generated case machinery inside tests.

## TST-006 — Use integration tests for real composition

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend-tests
- **Source:** `templates/v2-baseline/.claude/skills/testing/SKILL.md#ASP.NET Core Integration Tests`

Use WebApplicationFactory-based integration testing when routing, binding, middleware, auth, DI, repositories, EF Core or database persistence is what the test must prove.

## TST-007 — Use provider fidelity when it matters

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend-tests
- **Source:** `templates/v2-baseline/.claude/skills/testing/SKILL.md#Test Database Strategy`

Use the actual database provider when relational/provider behavior matters; Testcontainers is optional, and do not claim provider fidelity from a different provider.

## TST-008 — Test data is known and owned by tests

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend-tests
- **Source:** `templates/v2-baseline/.claude/skills/testing/SKILL.md#Database State`

Tests start from a known state and own their setup; do not depend on development seeding or execution order.

## TST-009 — Meaningful bugs get regression coverage

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** workflow
- **Scope:** backend-tests
- **Source:** `templates/v2-baseline/.claude/skills/testing/SKILL.md#Regression Tests`

For a meaningful bug with plausible recurrence, add a regression test unless equivalent coverage already exists.

## TST-010 — Behavioral probes become maintained tests

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** workflow
- **Scope:** backend-tests
- **Source:** `templates/v2-baseline/.claude/rules/testing.md#Behavioral Verification`, `templates/v2-baseline/.claude/skills/testing/SKILL.md#Verification Performed During Implementation`, `templates/v2-baseline/.claude/skills/verify/SKILL.md#Preserve Behavioral Verification`

If an ad-hoc/manual behavioral probe uniquely demonstrates behavior, preserve that behavior in maintained automated coverage before completion unless equivalent coverage already exists.

## TST-011 — Do not chase coverage percentage

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** path
- **Scope:** backend-tests
- **Source:** `templates/v2-baseline/.claude/skills/testing/SKILL.md#Coverage`

Do not generate low-value tests merely to increase coverage percentage.

## TST-012 — Descriptive test naming

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend-tests
- **Source:** `templates/v2-baseline/.claude/rules/testing.md#Naming`, `templates/v2-baseline/.claude/skills/testing/SKILL.md#Test Naming`

Use descriptive test names that communicate scenario/condition and expected behavior.
