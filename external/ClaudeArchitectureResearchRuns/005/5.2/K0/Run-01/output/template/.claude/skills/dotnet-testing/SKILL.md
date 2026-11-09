---
name: dotnet-testing
description: Use when writing, reviewing, debugging or organizing .NET automated tests — NUnit fixtures and cases, Application Service unit tests, WebApplicationFactory integration tests, test databases and Testcontainers, FakeTimeProvider, external-service stubs, test data, naming, regression tests.
---
<!-- Kind: KNW | Scope: backend-tests | Owns: .NET testing technique and examples | Loads: on demand (model-invoked) -->
# .NET Testing

Standards: `rules/backend-tests/testing.md` (framework use, level, behavior focus, isolation, readability, references). Behavioral probes and verification: `verify` § 4. This skill shows how.

Test the risks that matter for the current project; a small project does not need an enterprise-sized test harness.

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

Arrange / Act / Assert is a useful default structure; the comments are optional when the phases are obvious.

## Test Readability

Test code should be simpler to reason about than the production behavior it verifies; optimize it for clarity rather than minimum line count. For small finite input/state spaces, enumerate cases with `[TestCase]` rather than loops, LINQ, `TestCaseSource` or logic deriving the expected result:

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

A longer explicit case table beats a shorter algorithmic test when it makes the business rules visible. Prefer one observable scenario per test; multi-step tests fit when the sequence itself is the scenario (a whole workflow, a replace-set lifecycle).

## Unit Tests

Good candidates: non-trivial domain behavior that genuinely belongs to Domain, calculations, workflow/state transitions at the owning layer, validation logic, application orchestration with simple fakes or mocks when isolation gives useful feedback. Avoid mocking every collaborator mechanically; fake architectural boundaries when that makes the behavior under test clearer.

## Test Doubles

Fakes, stubs or mocks fit when they make an isolated test clearer; mocking project-owned abstractions is fine when isolation is useful. When important behavior depends on real EF Core, provider or HTTP semantics, an integration test beats reproducing that behavior through mocks.

## Application Service Tests

Replace repository and external-service abstractions with controlled doubles and assert on the use-case result and meaningful side effects. "Repository method X was called once" is useful only when that interaction is part of the contract — not as the default assertion style. When a service's important behavior depends on EF Core semantics, transactions, DI wiring, serialization or HTTP, prefer an integration test.

## ASP.NET Core Integration Tests

`WebApplicationFactory<Program>` exercises the real HTTP pipeline: routing, model binding, serialization, middleware, authentication/authorization wiring, DI, Application services, repositories, EF Core and database persistence.

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

Configure the `Testing` environment with isolated test resources so an integration test can never reach a development or production database. If top-level statements make `Program` inaccessible to the test project, expose it, for example with a `public partial class Program` declaration.

## Test Database Strategy

Provider fidelity matters for provider-specific SQL, constraints, transactions, locking or concurrency, indexes, raw SQL, provider-specific mappings and migrations — use the actual provider there. Testcontainers is a good option when an isolated real database is useful, not a requirement for every project.

When provider fidelity does not matter, a lighter isolated relational database may be acceptable for tests that are primarily about application/API integration — be explicit about the trade-off. EF Core InMemory may suit a narrowly scoped test where relational semantics are irrelevant, but a fake repository is often clearer for a true unit test.

## Database State

Start each test from a known state with a strategy that fits the suite: recreate or reset the isolated test database, use transactions when their semantics fit, seed only the data a test needs, use unique identifiers to avoid collisions.

## Persistence Tests

Test repository implementations or EF mappings when there is meaningful persistence behavior: custom mappings, query filters, projections, non-trivial queries, relationships, concurrency behavior, provider-specific behavior. One test per trivial `Add`/`Get` method adds little.

## Time-Dependent Code

Logic reading the clock through `TimeProvider` can be tested with `FakeTimeProvider`:

```csharp
var time = new FakeTimeProvider(
    new DateTimeOffset(
        2026, 1, 1,
        0, 0, 0,
        TimeSpan.Zero));

time.Advance(TimeSpan.FromDays(1));
```

## External Services

At the relevant boundary use a fake or mock abstraction (unit tests), a stub `HttpMessageHandler`, WireMock or another local fake server (HTTP integration), or a dedicated sandbox only when the test explicitly targets that integration. Keep slow or unreliable external-system tests separate from ordinary fast runs.

## Test Data

Keep test data explicit and minimal. Introduce builders, fixtures or factories when repeated setup becomes hard to read — not a generic test-data framework for a few simple objects.

## Test Naming

`MethodOrScenario_StateOrCondition_ExpectedBehavior`, for example:

```csharp
CreateOrder_WithValidRequest_ReturnsCreated
CreateOrder_WithMissingCustomer_ReturnsValidationError
GetOrder_WithUnknownId_ReturnsNotFound
```

## Regression Tests

Write the regression test against the unfixed code first so it demonstrates the bug, then keep it once the fix turns it green. It adds little for a problem that cannot realistically recur or is already covered.

## Smoke Tests

"Smoke test" means a small set of fast checks establishing that a built or deployed application is basically operational — not a synonym for every integration test.

## Coverage

Coverage is diagnostic information, not a target: prioritize meaningful behavior, important edge cases and risky integrations.

## Snapshot Testing

Snapshot testing can help for large stable outputs where explicit assertions become noisy; no snapshot library by default, and explicit assertions are usually clearer for small or important response contracts.

## Anti-Patterns

Avoid testing private implementation details, mocking every class, hitting production resources, shared mutable state between tests, assertions that merely repeat the implementation, assertion-free tests (unless the behavior is "does not throw"), arbitrary `Task.Delay` waits, Testcontainers without a fidelity need, EF InMemory while claiming relational coverage, and keeping temporary probes as permanent tests without review.

## Decision Guide

| Scenario | Default approach |
|---|---|
| Pure business rule | NUnit unit test |
| Application orchestration | Unit test with controlled boundary doubles when useful |
| Full API pipeline | `WebApplicationFactory<Program>` |
| Important EF/provider behavior | Integration test on the actual provider |
| Simple API integration, provider specifics irrelevant | Lightweight isolated relational test DB may suffice |
| Time-dependent behavior | `TimeProvider` / `FakeTimeProvider` |
| External HTTP dependency | Stub handler or local fake server |
| Reproduced bug | Focused regression test |
| Temporary behavioral check | Convert to maintained coverage or confirm existing coverage (`verify` § 4) |
| Deployment/basic health | Smoke test |
