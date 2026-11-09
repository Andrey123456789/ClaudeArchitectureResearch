---
name: dotnet-testing
description: >
  Use when writing or fixing NUnit tests: unit tests with fakes,
  WebApplicationFactory integration tests, test databases and Testcontainers,
  FakeTimeProvider, HttpMessageHandler stubs, test data builders, regression
  tests, probe-to-test conversion.
---

> Owner: .NET testing technique and NUnit examples (normative policy lives in rules) | Scope: backend-tests | Loads: on demand — knowledge | Enforced: none

# .NET Testing

Policy: `.claude/rules/testing.md` (framework, levels, behavior focus, isolation,
provider fidelity, readability, regression and probe preservation, coverage,
naming, test references). Test only the risks that matter for the current
project; a small project does not need an enterprise-sized test harness.

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

Arrange / Act / Assert is a useful structure; the comments are optional when the
phases are obvious.

## Explicit Case Tables

State expected results in the test instead of computing them with logic that
risks reproducing the implementation. A longer explicit table beats a shorter
algorithmic test when it makes the rules visible:

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

Prefer one observable scenario per test; a multi-step test fits when the
sequence itself is the scenario (a whole workflow or a replace-set lifecycle).

## Unit Tests

Good candidates: non-trivial domain behavior that genuinely belongs to Domain,
calculations, workflow/state transitions at the owning layer, validation logic,
and Application orchestration with simple fakes or mocks when isolation gives
useful feedback. Fake or mock architectural boundaries when that makes the
behavior clearer, but do not mock every collaborator mechanically, and do not
forbid mocking project-owned abstractions when isolation helps.

## Application Service Tests

Replace repository and external-service abstractions with controlled test
doubles and assert the use-case result and meaningful side effects. A
"repository method X was called once" verification is useful only when that
interaction is part of the contract. When the important behavior depends on EF
Core semantics, transactions, DI wiring, serialization, or HTTP, an integration
test is clearer than reproducing the stack with mocks.

## ASP.NET Core Integration Tests

`WebApplicationFactory<Program>` exercises routing, model binding,
serialization, middleware, authentication/authorization wiring, DI, Application
services, repositories, EF Core, and persistence:

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

Configure the `Testing` environment to use isolated test resources so a test can
never reach a Development or Production database. If top-level statements make
`Program` inaccessible, add `public partial class Program { }`.

Replace services for a test with `ConfigureTestServices`:

```csharp
builder.ConfigureTestServices(services =>
{
    services.RemoveAll<IPaymentGateway>();
    services.AddSingleton<IPaymentGateway, FakePaymentGateway>();
});
```

## Test Database Strategy

Provider fidelity matters for provider-specific SQL, constraints, transactions,
locking or concurrency, indexes, raw SQL, provider-specific mappings, and
migrations: use SQL Server, for example through Testcontainers when an isolated
real database is useful.

When fidelity does not matter (primarily application/API integration), a lighter
isolated relational database can be acceptable — state the trade-off. EF Core
InMemory may fit a narrowly scoped test where relational semantics are
irrelevant, but a fake repository is often clearer for a true unit test.

## Database State

Choose a simple strategy for a known starting state: recreate or reset the
isolated test database, use transactions when their semantics fit, seed only the
data each test requires, use unique identifiers to avoid collisions.

## Persistence Tests

Test repository implementations or EF mappings when there is meaningful
persistence behavior: custom mappings, query filters, projections, non-trivial
queries, relationships, concurrency, provider-specific behavior. Do not write one
test per trivial `Add`/`Get` method.

## Time-Dependent Code

```csharp
var time = new FakeTimeProvider(
    new DateTimeOffset(
        2026, 1, 1,
        0, 0, 0,
        TimeSpan.Zero));

time.Advance(TimeSpan.FromDays(1));
```

`FakeTimeProvider` comes from `Microsoft.Extensions.TimeProvider.Testing`
(add it through the `add-dependency` workflow).

## External Services

At the relevant boundary, use a fake or mock abstraction for unit tests, a stub
`HttpMessageHandler`, WireMock or another local fake server for HTTP integration,
or a dedicated sandbox only when the test explicitly targets that integration.
Keep slow or unreliable external-system tests out of the ordinary fast run.

## Test Data

Keep test data explicit and minimal. Introduce builders, fixtures, or factories
when repeated setup becomes hard to read; a generic test-data framework for a few
simple objects is overhead.

## Test Naming

```csharp
CreateOrder_WithValidRequest_ReturnsCreated
CreateOrder_WithMissingCustomer_ReturnsValidationError
GetOrder_WithUnknownId_ReturnsNotFound
```

Follow an existing project naming convention if one is established.

## Regression Tests

A regression test reproduces the failure before the fix and passes after it.
Skip it when the problem cannot realistically recur or an existing test already
covers it.

## Converting Temporary Probes

Probes that must become maintained tests (`.claude/rules/testing.md`
§ Regression and Behavioral Verification) include temporary HTTP requests,
PowerShell or shell scripts exercising behavior, ad-hoc test methods, manual
database checks, and temporary regression probes. The maintained test need not
keep the mechanism: an ad-hoc `curl` or REST request usually becomes an NUnit
`WebApplicationFactory` test. If an existing test already covers the behavior,
confirm it actually exercises it instead of adding a duplicate. Review a
temporary probe before keeping it as a permanent test.

## Smoke Tests

"Smoke test" means a small set of fast checks that a built or deployed
application is basically operational — not a synonym for every integration
test.

## Coverage and Snapshots

Coverage is diagnostic information; prioritize meaningful behavior, important
edge cases, and risky integrations. Snapshot testing can help with large stable
outputs where explicit assertions get noisy, but do not add a snapshot library by
default; explicit assertions are clearer for small or important contracts.

## Common Mistakes

- assertion-free tests (unless the behavior is explicitly "does not throw");
- arbitrary delays such as `Task.Delay` to make timing-sensitive tests pass;
- Testcontainers where no provider fidelity is required;
- shared mutable fixtures between unrelated tests.

## Decision Guide

| Scenario | Technique |
|---|---|
| Pure business rule | NUnit unit test |
| Application orchestration | Unit test with controlled boundary doubles |
| Full API pipeline | `WebApplicationFactory<Program>` |
| Important EF/provider behavior | Integration test on the actual provider |
| Simple API integration, provider-agnostic | Lightweight isolated relational test DB |
| Time-dependent behavior | `TimeProvider` / `FakeTimeProvider` |
| External HTTP dependency | Stub handler or local fake server |
| Reproduced bug | Focused regression test |
| Temporary behavioral check | Convert to maintained coverage or confirm existing coverage |
| Deployment/basic health | Smoke test |
