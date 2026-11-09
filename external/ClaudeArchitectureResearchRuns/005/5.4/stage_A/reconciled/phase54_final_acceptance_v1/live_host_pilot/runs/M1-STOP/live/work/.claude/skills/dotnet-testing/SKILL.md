---
name: dotnet-testing
description: >
  Use for .NET tests: NUnit fixtures, [TestCase] tables, Assert.That, service
  unit tests, WebApplicationFactory integration tests, test databases,
  Testcontainers, FakeTimeProvider, test project setup.
---

> Capability: backend-testing/nunit · Knowledge skill · Technique only · Policy: `.claude/rules/testing.md`, `.claude/rules/test-framework.md` · Probe preservation: `verify`

# .NET Testing with NUnit

Do not build test infrastructure without a concrete testing need; a small
project does not require an enterprise-sized test harness. Test the risks that
matter for the current project.

## NUnit Basics

```csharp
[TestFixture]
public sealed class PriceCalculatorTests
{
    [TestCase(2, 10, 20)]
    [TestCase(3, 5, 15)]
    public void Calculate_WithValidInput_ReturnsExpectedTotal(
        int quantity,
        decimal price,
        decimal expected)
    {
        // Arrange
        var calculator = new PriceCalculator();

        // Act
        var result = calculator.Calculate(quantity, price);

        // Assert
        Assert.That(result, Is.EqualTo(expected));
    }
}
```

Arrange / Act / Assert is a useful default structure; comments are optional
when the phases are obvious.

## Explicit Case Tables

A longer explicit case table is preferable to a shorter algorithmic test when
it makes the business rules immediately visible:

```csharp
[TestCase(TaskStatus.Created, TaskStatus.InProgress, true)]
[TestCase(TaskStatus.Created, TaskStatus.Completed, false)]
[TestCase(TaskStatus.InProgress, TaskStatus.Completed, true)]
public void IsTransitionAllowed_ReturnsExpected(
    TaskStatus current,
    TaskStatus target,
    bool expected)
{
    var actual = TaskWorkflowRules.IsTransitionAllowed(current, target);

    Assert.That(actual, Is.EqualTo(expected));
}
```

Multi-step tests fit when the sequence itself is the scenario, such as a whole
workflow or a replace-set lifecycle.

## Unit Tests

Good candidates: non-trivial domain behavior that genuinely belongs to Domain,
calculations, workflow/state transitions at the owning layer, validation logic,
and application orchestration with simple fakes or mocks when isolation gives
useful feedback. Mock or fake architectural boundaries when that makes the
behavior under test clearer.

## Application Service Tests

Replace repository and external-service abstractions with controlled test
doubles and focus assertions on the use-case result and meaningful side
effects. A verification such as "repository method X was called once" is
useful only when that interaction is part of the contract. When important
behavior depends on persistence semantics, transactions, DI wiring,
serialization, or HTTP, prefer an integration test.

## ASP.NET Core Integration Tests

`WebApplicationFactory<Program>` exercises the real pipeline: routing, model
binding, serialization, middleware, authentication/authorization wiring,
dependency injection, Application services, repositories, and database
persistence.

```csharp
[TestFixture]
public sealed class OrdersApiTests
{
    private WebApplicationFactory<Program> _factory = null!;
    private HttpClient _client = null!;

    [OneTimeSetUp]
    public void OneTimeSetUp()
    {
        _factory = new WebApplicationFactory<Program>()
            .WithWebHostBuilder(builder =>
            {
                builder.UseEnvironment("Testing");
            });

        _client = _factory.CreateClient();
    }

    [OneTimeTearDown]
    public void OneTimeTearDown()
    {
        _client.Dispose();
        _factory.Dispose();
    }

    [Test]
    public async Task CreateOrder_WithValidRequest_ReturnsCreated()
    {
        var request = new CreateOrderRequest(
            "customer-1");

        var response = await _client.PostAsJsonAsync(
            "/api/orders",
            request);

        Assert.That(
            response.StatusCode,
            Is.EqualTo(HttpStatusCode.Created));
    }
}
```

Configure the `Testing` environment to use isolated test resources so an
integration test can never reach a development or production database. If
top-level statements make `Program` inaccessible, expose it for
`WebApplicationFactory`, for example with a `public partial class Program`
declaration.

## Test Database Strategy

Provider fidelity matters for provider-specific SQL, constraints, transactions,
locking/concurrency, indexes, raw SQL, provider-specific mappings, and
migrations — use the actual provider (`.claude/rules/persistence-technology.md`
§ Relational Testing Binding); Testcontainers is a good option for an isolated
real database. When provider fidelity does not matter, a lighter isolated
relational database may be acceptable for application/API integration tests;
state the trade-off. For a true unit test, a fake repository is often clearer
than any database.

## Database State

Choose a simple strategy that gives every test a known state: recreate or reset
the isolated test database, use transactions when their semantics fit, seed
only the data the test needs, or use unique identifiers to prevent collisions.

## Persistence Tests

Test repository implementations or mappings when there is meaningful
persistence behavior: custom mappings, query filters, projections, non-trivial
queries, relationships, concurrency, provider-specific behavior. Do not write a
test for every trivial `Add`/`Get` method.

## Time-Dependent Code

Read time through `TimeProvider` and control it with `FakeTimeProvider`:

```csharp
var time = new FakeTimeProvider(
    new DateTimeOffset(
        2026, 1, 1,
        0, 0, 0,
        TimeSpan.Zero));

time.Advance(TimeSpan.FromDays(1));
```

## External Services

At the relevant boundary use a fake or mock abstraction for unit tests, a stub
`HttpMessageHandler`, WireMock or another local fake server for HTTP
integration, or a dedicated sandbox only when the test explicitly targets that
integration. Keep slow or unreliable external-system tests separate from
ordinary fast runs.

## Test Data

Keep test data explicit and minimal. Introduce builders, fixtures, or factories
when repeated setup becomes hard to read; do not introduce a generic test-data
framework for a few simple objects.

## Test Naming Examples

```csharp
CreateOrder_WithValidRequest_ReturnsCreated
CreateOrder_WithMissingCustomer_ReturnsValidationError
GetOrder_WithUnknownId_ReturnsNotFound
```

## Converting Probes

Typical temporary probes to convert (`verify` § Preserve Behavioral
Verification): HTTP requests used to check an endpoint, PowerShell or shell
scripts that exercise behavior, ad-hoc test methods, manual database checks,
temporary regression probes. For example, replace an ad-hoc `curl` or REST
request with an NUnit integration test using `WebApplicationFactory`. Review a
temporary probe before keeping it as a permanent test.

## Smoke Tests

"Smoke test" means a small set of fast checks that a built or deployed
application is basically operational, not a synonym for every integration test.

## Snapshot Testing

Snapshot testing may help for large stable outputs where explicit assertions
become noisy; do not introduce a snapshot library by default. Explicit
assertions are usually clearer for small or important response contracts.

## Review Checks

Check-by-reference against `.claude/rules/testing.md`: private implementation
details tested; every class mocked; production resources reached; shared
mutable state between tests; assertions that repeat the implementation;
assertion-free tests (unless the behavior is "does not throw"); arbitrary delays
such as `Task.Delay`; Testcontainers without a provider-fidelity need; an
in-memory provider claimed as relational coverage.

## Test Project Setup

- Create test projects with the NUnit template (`dotnet new nunit`) at the
  locations and with the references the `project-structure` workflow defines,
  then remove properties duplicated by `Directory.Build.props` and package
  versions duplicated by Central Package Management.
- Packages (through `add-dependency`): `NUnit`, `NUnit3TestAdapter`,
  `Microsoft.NET.Test.Sdk`; `Microsoft.AspNetCore.Mvc.Testing` for integration
  tests; `Microsoft.Extensions.TimeProvider.Testing` when `FakeTimeProvider` is
  needed.
- Run a subset with `dotnet test --filter "FullyQualifiedName~OrdersApiTests"`.

## Decision Guide

| Scenario | Default approach |
|---|---|
| Pure business rule | NUnit unit test |
| Application orchestration | Unit test with controlled boundary doubles when useful |
| Full API pipeline | `WebApplicationFactory<Program>` |
| Important persistence/provider behavior | Integration test using the actual provider |
| Simple API integration where provider specifics are irrelevant | Lightweight isolated relational test database may be sufficient |
| Time-dependent behavior | `TimeProvider` / `FakeTimeProvider` |
| External HTTP dependency | Stub handler or local fake server |
| Reproduced bug | Focused regression test |
| Temporary behavioral check | Convert to maintained coverage or confirm equivalent existing coverage |
| Deployment/basic health | Smoke test |
