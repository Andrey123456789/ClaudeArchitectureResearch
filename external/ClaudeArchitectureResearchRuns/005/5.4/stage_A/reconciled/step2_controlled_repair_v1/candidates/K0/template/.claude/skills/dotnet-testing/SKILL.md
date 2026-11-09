---
name: dotnet-testing
description: Use when writing or reviewing backend tests — NUnit cases, service tests, WebApplicationFactory, test databases and provider fidelity, Testcontainers, FakeTimeProvider, stubs, regression tests, probes.
---

> Kind: KNW | Scope: backend-tests | Owner: backend testing technique and examples | Loading: on demand (model-invoked knowledge)

# .NET Testing

Rules: `rules/backend-tests/testing.md`. Test stack: D-08. See also: `development-workflow` § Bug fix (regression tests), `verify` § 4 (probe preservation).

Test the risks that matter for the current project, and build test infrastructure only for a concrete testing need — a small project does not need an enterprise-sized harness.

## NUnit basics

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

Arrange/Act/Assert is a useful structure; the comments are optional when the phases are obvious.

## Readable cases

Optimize tests for clarity, not line count; test code should be simpler to reason about than the production behavior it verifies. Enumerate small finite cases with `[TestCase]` rather than loops, LINQ, `TestCaseSource` or logic that derives the expected value, and state expected results instead of computing them:

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

A longer explicit table beats a shorter algorithmic test when it makes the business rules visible. Prefer one observable scenario per test; multi-step tests fit when the sequence itself is the scenario (a whole workflow, a replace-set lifecycle).

## Unit tests

Good candidates: non-trivial domain behavior that genuinely belongs to Domain, calculations, workflow/state transitions at the owning layer, validation logic, Application orchestration with simple fakes or mocks. Mock or fake architectural boundaries when that clarifies the behavior; do not mock every collaborator mechanically, and do not forbid mocking project-owned abstractions when isolation helps.

## Application service tests

Replace repository and external-service abstractions with controlled test doubles and assert on the use-case result and meaningful side effects. "Repository method X was called once" is useful only when that interaction is part of the contract — not as the default assertion style. When important behavior depends on EF Core semantics, transactions, DI wiring, serialization or HTTP, an integration test is clearer than mocks reproducing the stack.

## ASP.NET Core integration tests

`WebApplicationFactory<Program>` exercises the real pipeline: routing, model binding, serialization, middleware, authentication/authorization wiring, DI, Application services, repositories, EF Core and persistence.

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

Configure the `Testing` environment with isolated test resources so an integration test cannot reach a development or production database by accident (`rules/backend-tests/testing.md` § Isolation and data). If top-level statements make `Program` inaccessible, expose it, for example with a `public partial class Program` declaration.

## Test database strategy

Provider fidelity matters for provider-specific SQL, constraints, transactions, locking and concurrency, indexes, raw SQL, provider-specific mappings and migrations — use the actual provider; Testcontainers is a good option for an isolated real database. When provider fidelity does not matter (primarily application/API integration), a lighter isolated relational database may be acceptable — state the trade-off. EF Core InMemory is not a relational substitute; for a true unit test a fake repository is often clearer.

## Database state

Start from a known state with a simple strategy: recreate or reset the isolated test database, use transactions when their semantics fit, seed only the data the test needs, use unique identifiers to avoid collisions.

## Persistence tests

Test repository implementations or EF mappings when there is meaningful persistence behavior: custom mappings, query filters, projections, non-trivial queries, relationships, concurrency, provider-specific behavior. One test per trivial `Add`/`Get` method adds coverage numbers, not value.

## Time-dependent code

```csharp
var time = new FakeTimeProvider(
    new DateTimeOffset(
        2026, 1, 1,
        0, 0, 0,
        TimeSpan.Zero));

time.Advance(TimeSpan.FromDays(1));
```

## External services

At the relevant boundary use a fake or mock abstraction (unit tests), a stub `HttpMessageHandler`, WireMock or another local fake server (HTTP integration), or a dedicated sandbox only when the test explicitly targets that integration. Keep slow or unreliable external-system tests separate from ordinary fast runs.

## Test data

Keep test data explicit and minimal. Introduce builders, fixtures or factories when repeated setup becomes hard to read — not a generic test-data framework for a few simple objects.

## Naming examples

```csharp
CreateOrder_WithValidRequest_ReturnsCreated
CreateOrder_WithMissingCustomer_ReturnsValidationError
GetOrder_WithUnknownId_ReturnsNotFound
```

## Regression tests

A regression test reproduces the failure before the fix and passes after it. It adds nothing for a problem that cannot realistically recur or is already covered.

## Turning probes into maintained tests

Typical temporary probes: HTTP requests used to check an endpoint, PowerShell or shell scripts exercising behavior, ad-hoc test methods, manual database checks, temporary regression probes. The maintained test does not need to keep the probe mechanism — an ad-hoc `curl` or REST request usually becomes an NUnit integration test with `WebApplicationFactory`. When an existing test already covers the behavior, confirm it really exercises it instead of adding a duplicate. Review temporary probes before keeping any of them as permanent tests.

## Smoke tests

"Smoke test" means a small set of fast checks that a built or deployed application is basically operational — not a synonym for every integration test.

## Coverage and snapshots

Coverage is diagnostic information, not a target; prioritize meaningful behavior, important edge cases and risky integrations. Snapshot testing can help for large stable outputs where explicit assertions get noisy; small or important response contracts read better with explicit assertions, and a snapshot library is not added by default.

## Common mistakes

Testing private details; mocking every class; hitting production resources; shared mutable state; assertions that repeat the implementation; assertion-free tests (unless the behavior is "does not throw"); `Task.Delay` to make timing-sensitive tests pass; Testcontainers without a provider-fidelity need; EF InMemory while claiming relational coverage.

## Decision guide

| Scenario | Approach |
|---|---|
| Pure business rule | NUnit unit test |
| Application orchestration | Unit test with controlled boundary doubles when useful |
| Full API pipeline | `WebApplicationFactory<Program>` |
| Important EF/provider behavior | Integration test with the actual provider |
| Simple API integration, provider irrelevant | Lightweight isolated relational test DB may suffice |
| Time-dependent behavior | `TimeProvider` / `FakeTimeProvider` |
| External HTTP dependency | Stub handler or local fake server |
| Reproduced bug | Focused regression test |
| Temporary behavioral probe | Maintained test or confirmed existing coverage |
| Deployment/basic health | Smoke test |
