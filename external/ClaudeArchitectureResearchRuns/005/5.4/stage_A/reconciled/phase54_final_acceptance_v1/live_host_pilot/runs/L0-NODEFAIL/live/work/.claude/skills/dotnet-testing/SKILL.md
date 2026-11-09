---
name: dotnet-testing
description: >
  Use when writing or reviewing .NET tests: NUnit, TestCase tables, service unit
  tests, WebApplicationFactory, test databases, Testcontainers, FakeTimeProvider, HTTP
  stubs.
---

> Level: 2 Technology · Owns: .NET test technique and examples (knowledge) · Scope: backend-tests · Loads: on invocation · Depends on: .claude/rules/0-core/testing-principles.md, .claude/rules/2-technology/dotnet-testing.md

# .NET Testing

Policy owners: test level, behavior focus, isolation, provider fidelity, readability, naming, coverage → `.claude/rules/0-core/testing-principles.md`; NUnit, `WebApplicationFactory`, EF InMemory → `2-technology/dotnet-testing.md`; regression tests → `development-workflow`; preserving behavioral probes → `verify` step 4. This skill is technique only. Do not build test infrastructure without a concrete testing need.

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

Arrange / Act / Assert is a useful structure; comments are optional when the phases are obvious.

## Explicit case tables

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

A longer explicit table beats a shorter algorithmic test when it makes the business rules visible. Prefer `[TestCase]` over loops, LINQ, or `TestCaseSource` that derives expectations. Multi-step tests fit when the sequence itself is the scenario (a whole workflow or replace-set lifecycle).

## Unit tests

Good candidates: non-trivial domain behavior that belongs to Domain, calculations, workflow/state transitions at the owning layer, validation logic, Application orchestration with simple fakes or mocks. Mock or fake architectural boundaries when that clarifies the behavior; do not mock every collaborator mechanically.

Application Services can be unit-tested with controlled repository and external-service doubles; assert the use-case result and meaningful side effects. "Repository method X was called once" is useful only when that interaction is part of the contract. When behavior depends heavily on EF Core semantics, transactions, DI wiring, serialization, or HTTP, prefer an integration test.

## Integration tests with WebApplicationFactory

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

This exercises routing, binding, serialization, middleware, auth wiring, DI, Application services, repositories, EF Core, and persistence. Configure the `Testing` environment so it can never reach a Development or Production database. If top-level statements hide `Program`, add `public partial class Program;`.

## Test database strategy

- Provider fidelity matters (provider-specific SQL, constraints, transactions, locking/concurrency, indexes, raw SQL, provider mappings, migrations): use the real provider; Testcontainers is a good option for an isolated real database, not a requirement for every test.
- Fidelity does not matter (primarily API/application integration): a lighter isolated relational database may be acceptable — state the trade-off.
- EF Core InMemory may suit a narrow test where relational semantics are irrelevant, but a fake repository is often clearer for a true unit test.

Known starting state: recreate or reset the isolated database, use transactions when their semantics fit, seed only the data each test needs, use unique identifiers to avoid collisions.

## Persistence tests

Test repositories or mappings when there is meaningful behavior: custom mappings, query filters, projections, non-trivial queries, relationships, concurrency, provider-specific behavior — not one test per trivial `Add`/`Get`.

## Time, external services, test data

```csharp
var time = new FakeTimeProvider(new DateTimeOffset(2026, 1, 1, 0, 0, 0, TimeSpan.Zero));
time.Advance(TimeSpan.FromDays(1));
```

For external dependencies use a fake/mock abstraction (unit tests), a stub `HttpMessageHandler`, WireMock or another local fake server, or a dedicated sandbox only when the test explicitly targets that integration; keep slow or unreliable external tests out of the fast run. Keep test data explicit and minimal; introduce builders, fixtures, or factories only when repeated setup becomes hard to read.

## Naming and regression tests

```csharp
CreateOrder_WithValidRequest_ReturnsCreated
CreateOrder_WithMissingCustomer_ReturnsValidationError
GetOrder_WithUnknownId_ReturnsNotFound
```

When regression tests are required: `development-workflow` → Implement.

## Turning probes into tests

Typical probes: temporary HTTP requests, PowerShell/shell scripts exercising behavior, ad-hoc test methods, manual database checks, temporary regression probes. An ad-hoc `curl`/PowerShell/REST request usually becomes an NUnit `WebApplicationFactory` test; if an existing test already covers the behavior, verify it actually exercises it instead of adding a duplicate. Review temporary probes before keeping them as permanent tests.

## Smoke and snapshot tests

"Smoke test" means a small set of fast checks that a built or deployed application is basically operational — not a synonym for every integration test. Snapshot testing can help for large stable outputs; do not add a snapshot library by default, and prefer explicit assertions for small or important contracts.

## Anti-patterns

Mocking every class; assertion-free tests (unless the behavior is "does not throw"); `Task.Delay` to make timing tests pass; Testcontainers without a fidelity need.

## Decision guide

| Scenario | Approach |
|---|---|
| Pure business rule | NUnit unit test |
| Application orchestration | unit test with boundary doubles when useful |
| Full API pipeline | `WebApplicationFactory<Program>` |
| Important EF/provider behavior | integration test on the actual provider |
| Simple API integration, provider irrelevant | lightweight isolated relational database |
| Time-dependent behavior | `TimeProvider` / `FakeTimeProvider` |
| External HTTP dependency | stub handler or local fake server |
| Reproduced bug | focused regression test |
| Deployment/basic health | smoke test |
