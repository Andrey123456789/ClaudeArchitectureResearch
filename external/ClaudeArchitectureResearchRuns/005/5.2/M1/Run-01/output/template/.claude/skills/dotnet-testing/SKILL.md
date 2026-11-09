---
name: dotnet-testing
description: >
  .NET backend test technique: unit vs. integration, WebApplicationFactory, test
  databases and provider fidelity, Testcontainers, FakeTimeProvider, stubs, test
  data, naming.
---

> **Knowledge skill** · Owns: .NET backend testing technique and examples · Scope: backend-tests · Loading: on demand

# Testing

## Rules

Framework-independent test policy: `testing.md`. Test-framework rules and
vocabulary binding: `test-framework.md`. Framework syntax and commands:
`references/test-framework.md`. Completion obligations (regression tests,
behavioral probes): `development-workflow` and `verify`.

No fixed ratio of unit, integration, and end-to-end tests is required; test the
risks that matter for the current project, and do not build test infrastructure
without a concrete testing need — a small project does not require an
enterprise-sized test harness.

## Test Structure

Arrange / Act / Assert is a useful default structure, but comments are not
mandatory when the phases are already obvious. Framework attributes, fixtures,
and assertion syntax: `references/test-framework.md`.

## Test Readability

Optimize tests for clarity rather than minimum line count (rule: `testing.md` →
Test Readability).

Expected results should normally be stated by the test, not calculated by logic
that risks reproducing the implementation under test.

A longer explicit case table is preferable to a shorter but algorithmic test
when the explicit form makes the business rules immediately visible; see the
case-table example in `references/test-framework.md`.

Multi-step tests are appropriate when the sequence itself is the scenario, such
as verifying an entire workflow or replace-set lifecycle.

## Unit Tests

Use unit tests for behavior that can be meaningfully exercised without
infrastructure.

Good candidates include:

- non-trivial domain behavior when such behavior genuinely belongs to Domain;
- calculations;
- workflow/state transitions at the layer that owns them;
- validation logic;
- application orchestration with simple fakes or mocks when isolation provides
  useful feedback.

Do not mock every collaborator mechanically.

Mock or fake architectural boundaries when doing so makes the behavior under
test clearer.

Do not test that a private method was called or that implementation details
happen in a particular sequence unless that sequence is itself observable
behavior.

## Application Service Tests

Application services may be unit-tested by replacing repository and external
service abstractions with controlled test doubles.

Focus assertions on the use-case result and meaningful side effects.

A mock verification such as "repository method X was called once" is useful only
when that interaction is itself part of the contract. Do not make interaction
verification the default assertion style.

If a service's important behavior depends heavily on persistence-technology
semantics, transaction behavior, DI wiring, serialization, or HTTP, prefer an
integration test instead of reproducing the whole stack with mocks.

## ASP.NET Core Integration Tests

Use `WebApplicationFactory<Program>` when the test should exercise the real HTTP
pipeline.

This can cover:

- routing;
- model binding;
- serialization;
- middleware;
- authentication/authorization wiring;
- dependency injection;
- Application services;
- repositories;
- the persistence technology;
- database persistence.

A complete fixture in the selected framework's syntax is in
`references/test-framework.md`. The essential host setup:

```csharp
var factory = new WebApplicationFactory<Program>()
    .WithWebHostBuilder(builder =>
    {
        builder.UseEnvironment("Testing");
    });

using var client = factory.CreateClient();
```

Configure the `Testing` environment to use isolated test resources so that an
integration test can never reach a development or production database
(`testing.md` → Isolation).

If top-level statements make `Program` inaccessible to the test project, expose
it as required by `WebApplicationFactory`, for example with a public partial
`Program` declaration.

## Test Database Strategy

Use the database strategy that matches what the test is intended to prove.

### Provider fidelity matters

Use the actual database provider when the test covers behavior such as:

- provider-specific SQL;
- constraints;
- transactions;
- locking or concurrency;
- indexes;
- raw SQL;
- provider-specific mappings;
- migrations.

Testcontainers is a good option when an isolated real database is useful; it is
not mandatory for every integration test or every project.

### Provider fidelity does not matter

A lighter isolated relational database may be acceptable for tests whose purpose
is primarily application/API integration.

Be explicit about the trade-off (`testing.md` → Database Tests).

### In-memory substitutes

An in-memory, non-relational substitute does not reproduce relational semantics.
It may be acceptable for a narrowly scoped test where relational semantics are
irrelevant, but a fake repository is often clearer for a true unit test. The
selected persistence technology's specifics: the persistence knowledge facet.

## Database State

Choose a simple strategy for reaching a known state (`testing.md` → Isolation):

- recreate or reset the isolated test database;
- use transactions when their semantics fit;
- seed only data required by the test;
- use unique identifiers to prevent collisions.

## Persistence Tests

Test repository implementations or persistence mappings when there is meaningful
persistence behavior to verify.

Examples include:

- custom mappings;
- query filters;
- projections;
- non-trivial queries;
- relationships;
- concurrency behavior;
- provider-specific behavior.

Do not write one repository test for every trivial `Add` and `Get` method merely
to increase coverage numbers.

## Time-Dependent Code

Use `TimeProvider` rather than reading the system clock directly from logic that
needs deterministic tests.

Use `FakeTimeProvider` when controlling time is useful.

```csharp
var time = new FakeTimeProvider(
    new DateTimeOffset(
        2026, 1, 1,
        0, 0, 0,
        TimeSpan.Zero));

time.Advance(TimeSpan.FromDays(1));
```

## External Services

Keep uncontrolled external services out of normal automated tests
(`testing.md` → Isolation). At the relevant boundary, use one of:

- a fake or mock abstraction for unit tests;
- a stub `HttpMessageHandler`;
- WireMock or another local fake server for HTTP integration;
- a dedicated sandbox only when the test explicitly targets that integration.

Keep external-system tests separate from ordinary fast test runs when they are
slow or unreliable.

## Test Data

Keep test data explicit and minimal.

Introduce test builders, fixtures, or factories when repeated setup becomes
hard to read.

Do not introduce a generic test-data framework for a few simple objects.

## Test Naming

Use descriptive names that state behavior.

A useful convention is:

```text
MethodOrScenario_StateOrCondition_ExpectedBehavior
```

For example:

```csharp
CreateOrder_WithValidRequest_ReturnsCreated
CreateOrder_WithMissingCustomer_ReturnsValidationError
GetOrder_WithUnknownId_ReturnsNotFound
```

Follow an existing project naming convention if one is already established.

## Regression Tests

When to add one: `development-workflow` → Change-Specific Obligations. A good
regression test reproduces the failure before the fix and passes after it.

## Verification Performed During Implementation

Preserving behavior verified by temporary probes is owned by `verify` → Preserve
Behavioral Verification. A typical conversion: an ad-hoc `curl`, PowerShell, or
REST request becomes a `WebApplicationFactory` integration test.

## Smoke Tests

Use "smoke test" for a small set of fast checks that establish that a built or
deployed application is basically operational.

Do not use the term as a synonym for every integration test.

## Coverage

Coverage policy: `testing.md` → Coverage. Prioritize meaningful behavior,
important edge cases, and risky integrations.

## Snapshot Testing

Snapshot testing may be useful for large stable outputs where explicit
assertions become noisy.

Do not introduce a snapshot library by default.

For small or important response contracts, explicit assertions are usually
clearer.

## Anti-Patterns

Avoid:

- mocking every class in the system;
- assertions that merely repeat the implementation;
- assertion-free tests unless the behavior under test is explicitly "does not
  throw";
- arbitrary delays such as `Task.Delay` to make timing-sensitive tests pass;
- Testcontainers when no provider fidelity is required;
- preserving temporary probes as permanent tests without review.

## Decision Guide

| Scenario | Default approach |
|---|---|
| Pure business rule | Unit test |
| Application orchestration | Unit test with controlled boundary doubles when useful |
| Full API pipeline | `WebApplicationFactory<Program>` |
| Important persistence/provider behavior | Integration test using the actual provider |
| Simple API integration where provider specifics are irrelevant | Lightweight isolated relational test DB may be sufficient |
| Time-dependent behavior | `TimeProvider` / `FakeTimeProvider` |
| External HTTP dependency | Stub handler or local fake server |
| Reproduced bug | Focused regression test |
| Temporary behavioral check | Convert to maintained coverage or confirm equivalent existing coverage |
| Deployment/basic health | Smoke test |
