---
name: dotnet-testing
description: >
  Use when writing, reviewing or debugging backend tests: NUnit cases,
  application-service tests, WebApplicationFactory integration tests, test
  databases and Testcontainers, FakeTimeProvider, HTTP stubs.
---

> Level: 2 Technology · Owns: NUnit and ASP.NET Core test technique · Scope: backend-tests · Loads: on demand (knowledge skill)

# .NET Testing

Policy owners: `.claude/rules/0-core/testing-principles.md` (level, behavior focus, readability, isolation, provider fidelity, regression, probe preservation, coverage, naming), `.claude/rules/2-technology/aspnet-core.md` (integration-test use), `.claude/rules/2-technology/ef-core.md` (InMemory is not relational). A small project does not need an enterprise-sized test harness.

## NUnit basics

```csharp
[TestFixture]
public sealed class PriceCalculatorTests
{
    [TestCase(2, 10, 20)]
    [TestCase(3, 5, 15)]
    public void Calculate_WithValidInput_ReturnsExpectedTotal(int quantity, decimal price, decimal expected)
    {
        var calculator = new PriceCalculator();

        var result = calculator.Calculate(quantity, price);

        Assert.That(result, Is.EqualTo(expected));
    }
}
```

Arrange/Act/Assert is a useful default; comments are optional when the phases are obvious.

## Explicit cases

Enumerate small finite spaces with `[TestCase]` instead of loops, LINQ, `TestCaseSource` generators or logic that computes the expectation:

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

A longer explicit table beats a shorter algorithmic test when it makes the rules visible. Multi-step tests fit when the sequence is the scenario (a full workflow or replace-set lifecycle).

## Unit and application-service tests

Good unit targets: non-trivial domain behavior, calculations, state transitions at the owning layer, validation logic, application orchestration with simple fakes. Replace repository and external-service abstractions with controlled doubles; assert the use-case result and meaningful side effects. Verify an interaction ("repository called once") only when that interaction is the contract. When the behavior depends on EF Core semantics, transactions, DI wiring, serialization or HTTP, write an integration test instead of mocking the stack. Do not mock every collaborator mechanically.

## ASP.NET Core integration tests

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

The `Testing` environment points at isolated test resources. Override services with `builder.ConfigureTestServices(...)` when a dependency must be replaced. If top-level statements hide `Program`, add `public partial class Program;` to the Api project.

## Test databases

| Goal | Option |
|---|---|
| Provider behavior (SQL, constraints, transactions, locking, indexes, raw SQL, mappings, migrations) | real SQL Server — LocalDB in development, or Testcontainers (`Testcontainers.MsSql`) for an isolated container |
| Application/API integration where provider specifics are irrelevant | a lighter isolated relational database, stating the trade-off explicitly |
| True unit test | a fake repository |

Known starting state: recreate or reset the test database (`EnsureDeletedAsync`/`MigrateAsync` per fixture, or a reset tool such as Respawn if the project adopts it), wrap tests in transactions when their semantics fit, seed only the data each test needs, and use unique identifiers to avoid collisions.

## Persistence tests

Test repositories and mappings when there is real persistence behavior: custom mappings, query filters, projections, non-trivial queries, relationships, concurrency, provider-specific behavior. One test per trivial `Add`/`Get` method is coverage padding.

## Time

```csharp
var time = new FakeTimeProvider(new DateTimeOffset(2026, 1, 1, 0, 0, 0, TimeSpan.Zero));
time.Advance(TimeSpan.FromDays(1));
```

`FakeTimeProvider` comes from `Microsoft.Extensions.TimeProvider.Testing` (add it through `add-dependency`); advancing fake time replaces `Task.Delay` in timing-sensitive tests.

## External services

Unit tests fake the Application abstraction; adapter tests use a stub `HttpMessageHandler`; HTTP integration may use WireMock.Net or another local fake server; a dedicated sandbox only when the test explicitly targets that integration. Keep slow or unreliable external-system tests out of the fast default run (for example `[Category("External")]`).

## Test data

Keep test data explicit and minimal; introduce builders or fixtures only when repeated setup becomes hard to read. No generic test-data framework for a few objects.

## Naming

`MethodOrScenario_StateOrCondition_ExpectedBehavior`, for example `CreateOrder_WithValidRequest_ReturnsCreated`, `CreateOrder_WithMissingCustomer_ReturnsValidationError`, `GetOrder_WithUnknownId_ReturnsNotFound`.

## Regression tests and probe conversion

A regression test reproduces the failure before the fix and passes after it. An ad-hoc `curl`, PowerShell or REST probe becomes, for example, an NUnit `WebApplicationFactory` test of the same request and assertion; a manual database check becomes a persistence test against the real provider. Review a temporary probe before keeping any of it as a permanent test.

## Smoke tests, coverage, snapshots

- "Smoke test" means a few fast checks that a built or deployed application is basically operational — not a synonym for integration tests.
- Coverage numbers are diagnostic; prioritize meaningful behavior, edge cases and risky integrations.
- Snapshot testing can help with large stable outputs; it is not a default dependency, and explicit assertions are clearer for small or important contracts.

## Review cues

Assertion-free tests (unless the behavior is "does not throw"), assertions that repeat the implementation, shared mutable state, production resources, arbitrary delays, Testcontainers without a fidelity need, EF InMemory presented as relational coverage.

## Decision guide

| Scenario | Typical approach |
|---|---|
| Pure business rule | NUnit unit test with `[TestCase]` |
| Application orchestration | Unit test with boundary doubles |
| Full API pipeline | `WebApplicationFactory<Program>` |
| Important EF/provider behavior | Integration test on SQL Server |
| Time-dependent behavior | `TimeProvider` + `FakeTimeProvider` |
| External HTTP dependency | Stub handler or local fake server |
| Reproduced bug | Focused regression test |
| Temporary behavioral probe | Maintained test or confirmed existing coverage |
| Deployment basic health | Smoke test |
