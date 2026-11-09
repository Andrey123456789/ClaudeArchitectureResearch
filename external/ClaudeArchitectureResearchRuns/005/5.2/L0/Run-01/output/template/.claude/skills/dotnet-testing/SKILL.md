---
name: dotnet-testing
description: >
  Use for NUnit tests: TestCase tables, service tests with fakes, WebApplicationFactory integration tests, test databases, FakeTimeProvider, HTTP stubs.
---

> Level: 2 Technology | Owns: NUnit and ASP.NET Core testing technique | Scope: backend-tests | Loads: knowledge skill (on demand) | Depends on: 0-core/testing-principles.md, 2-technology/backend-testing.md

# .NET Testing Technique

Policy owners (routing): test principles → `0-core/testing-principles.md`;
framework and integration-test bindings → `2-technology/backend-testing.md`;
regression tests → `develop`; preserving behavioral probes → `verify`.

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
rules visible. Prefer `[TestCase]` over `TestCaseSource` or loops for small
finite spaces. Multi-step tests fit when the sequence itself is the scenario.

## Unit and Application Service Tests

Good unit candidates: non-trivial domain behavior that belongs to Domain,
calculations, workflow/state transitions at their owning layer, validation, and
orchestration with simple fakes. Replace repositories and external-service
abstractions with controlled doubles; assert on the use-case result and
meaningful side effects. Verify an interaction ("repository called once") only
when the interaction is part of the contract. Do not mock every collaborator
mechanically; when behavior depends on EF Core semantics, transactions, DI,
serialization, or HTTP, write an integration test instead.

## WebApplicationFactory Integration Tests

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

Covers routing, binding, serialization, middleware, auth wiring, DI,
Application services, repositories, EF Core, and persistence. Point the
`Testing` environment's configuration at isolated test resources (isolation
rule: `0-core/testing-principles.md`). If top-level statements hide `Program`,
add `public partial class Program;`.

## Test Databases

- Provider fidelity matters (provider SQL, constraints, transactions, locking,
  indexes, raw SQL, provider mappings, migrations): use SQL Server — for example
  a Testcontainers instance or a dedicated isolated database.
- Provider fidelity does not matter: a lighter isolated relational database can
  serve API integration tests; state the trade-off.
- EF Core InMemory may suit a narrow test where relational semantics are
  irrelevant, but a fake repository is often clearer.
- Known state: recreate/reset the isolated database, use transactions when they
  fit, seed only what the test needs, use unique identifiers.

## Persistence Tests

Test repositories or mappings when there is meaningful behavior — custom
mappings, query filters, projections, non-trivial queries, relationships,
concurrency, provider behavior — not one test per trivial `Add`/`Get`.

## Time

```csharp
var time = new FakeTimeProvider(new DateTimeOffset(2026, 1, 1, 0, 0, 0, TimeSpan.Zero));
time.Advance(TimeSpan.FromDays(1));
```

## External Services

Use a fake abstraction for unit tests, a stub `HttpMessageHandler` or a local
fake server (e.g. WireMock) for HTTP integration, and a dedicated sandbox only
for tests that explicitly target that integration; keep slow or unreliable
external tests out of the fast run.

## Test Data, Regressions, Probes

- Keep data explicit and minimal; add builders or fixtures only when repeated
  setup hurts readability — no generic test-data framework for a few objects.
- A regression test reproduces the failure before the fix and passes after.
- Replace a temporary probe with a maintained test, e.g. an ad-hoc `curl` call
  becomes a `WebApplicationFactory` test; do not keep the probe itself.
- "Smoke test" means a few fast checks that a built or deployed app is
  operational, not every integration test.
- Snapshot testing is optional for large stable outputs; no snapshot library by
  default.

## Avoid

Assertion-free tests (unless the behavior is "does not throw"), `Task.Delay`
to make timing tests pass, Testcontainers where provider fidelity is not
needed, and keeping temporary probes as permanent tests without review.
