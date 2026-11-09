---
name: dotnet-testing
description: >
  Use when writing, reviewing, debugging, or organizing .NET tests: NUnit
  fixtures and TestCase tables, Application service tests with test doubles,
  WebApplicationFactory integration tests, test databases and Testcontainers,
  FakeTimeProvider, HTTP stubs, test data builders, or converting a temporary
  probe into a maintained test.
---

> Owns: .NET/NUnit testing technique and examples | Scope: backend-tests | Loads: on demand (knowledge skill)

# .NET Testing

Policy owners: framework, level, behavior focus, isolation, data ownership,
provider fidelity, coverage, naming → `.claude/rules/testing.md`; probe
preservation and regression coverage before completion → `verify` (step 4).
Frontend tests: `angular`.

Do not build test infrastructure without a concrete testing need; a small
project does not need an enterprise-sized harness.

## NUnit Basics

```csharp
[TestFixture]
public sealed class PriceCalculatorTests
{
    [TestCase(2, 10, 20)]
    [TestCase(3, 5, 15)]
    public void Calculate_WithValidInput_ReturnsExpectedTotal(
        int quantity, decimal price, decimal expected)
    {
        var calculator = new PriceCalculator();

        var result = calculator.Calculate(quantity, price);

        Assert.That(result, Is.EqualTo(expected));
    }
}
```

Arrange/Act/Assert is a useful structure; comments are optional when the phases
are obvious.

## Explicit Case Tables

```csharp
[TestCase(TaskStatus.Created, TaskStatus.InProgress, true)]
[TestCase(TaskStatus.Created, TaskStatus.Completed, false)]
[TestCase(TaskStatus.InProgress, TaskStatus.Completed, true)]
public void IsTransitionAllowed_ReturnsExpected(TaskStatus current, TaskStatus target, bool expected)
{
    var actual = TaskWorkflowRules.IsTransitionAllowed(current, target);

    Assert.That(actual, Is.EqualTo(expected));
}
```

A longer explicit table beats a shorter algorithmic test when it makes the
business rules visible. Multi-step tests fit when the sequence is the scenario
(a whole workflow or a replace-set lifecycle).

## Unit and Application Service Tests

Good unit candidates: Domain-owned non-trivial behavior, calculations,
workflow/state transitions at their owning layer, validation logic, and
Application orchestration with simple fakes. Replace repository and
external-service abstractions with controlled doubles and assert on the
use-case result and meaningful side effects; verify an interaction ("repository
X called once") only when it is part of the contract.

## ASP.NET Core Integration Tests

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
            .WithWebHostBuilder(builder => builder.UseEnvironment("Testing"));
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
        var response = await _client.PostAsJsonAsync("/api/orders", new CreateOrderRequest("customer-1"));

        Assert.That(response.StatusCode, Is.EqualTo(HttpStatusCode.Created));
    }
}
```

Point the `Testing` environment at isolated resources (for example override the
connection string in `ConfigureAppConfiguration` or replace the `DbContext`
registration in `ConfigureServices`); isolation requirements: `testing.md`. If
top-level statements hide `Program`, add `public partial class Program;`.

## Test Database Strategy

- Provider fidelity matters (provider SQL, constraints, transactions,
  locking/concurrency, indexes, raw SQL, provider mappings, migrations): use the
  real provider — LocalDB/SQL Server instance or Testcontainers when an
  isolated real database helps.
- Provider fidelity irrelevant (pure API/application integration): a lighter
  isolated relational database may do; state the trade-off.
- EF Core InMemory: only for narrow tests where relational semantics are
  irrelevant; a fake repository is usually clearer.

Known starting state options: recreate/reset the isolated database, use
transactions when their semantics fit, seed only the data each test needs, use
unique identifiers to avoid collisions.

## Persistence Tests

Test repositories or mappings when there is meaningful persistence behavior:
custom mappings, query filters, projections, non-trivial queries,
relationships, concurrency, provider-specific behavior — not every trivial
`Add`/`Get`.

## Time-Dependent Code

```csharp
var time = new FakeTimeProvider(new DateTimeOffset(2026, 1, 1, 0, 0, 0, TimeSpan.Zero));
time.Advance(TimeSpan.FromDays(1));
```

## External Services

At the boundary use a fake/mock abstraction (unit), a stub `HttpMessageHandler`,
WireMock or another local fake server (HTTP integration), or a dedicated sandbox
only when the test explicitly targets that integration. Keep slow or unreliable
external-system tests out of the fast default run.

## Test Data

Keep test data explicit and minimal. Introduce builders, fixtures, or factories
when repeated setup becomes hard to read; skip a generic test-data framework for
a few objects.

## Naming Examples

```text
CreateOrder_WithValidRequest_ReturnsCreated
CreateOrder_WithMissingCustomer_ReturnsValidationError
GetOrder_WithUnknownId_ReturnsNotFound
```

## Converting a Temporary Probe

Temporary HTTP requests, shell/PowerShell scripts, ad-hoc test methods, manual
database checks, and regression probes become maintained tests, for example an
ad-hoc `curl` call becomes an NUnit `WebApplicationFactory` test asserting the
same status and body. A regression test should fail before the fix and pass
after it. Review a temporary probe before keeping it as a permanent test.

## Smoke Tests and Snapshots

"Smoke test" means a few fast checks that a built or deployed application is
basically operational, not every integration test. Snapshot testing can help
for large stable outputs; do not add a snapshot library by default — explicit
assertions are clearer for small or important contracts.

## Pitfalls

Avoid mocking every class, assertions that repeat the implementation,
assertion-free tests (unless the behavior is "does not throw"), `Task.Delay` to
paper over timing, and Testcontainers where no provider fidelity is needed.

## Decision Guide

| Scenario | Technique |
|---|---|
| Pure business rule | NUnit unit test with `[TestCase]` table |
| Application orchestration | Unit test with boundary doubles |
| Full API pipeline | `WebApplicationFactory<Program>` |
| Important EF/provider behavior | Integration test on the real provider |
| Time-dependent behavior | `TimeProvider` + `FakeTimeProvider` |
| External HTTP dependency | Stub handler or local fake server |
| Reproduced bug | Focused regression test |
| Deployment/basic health | Smoke test |
