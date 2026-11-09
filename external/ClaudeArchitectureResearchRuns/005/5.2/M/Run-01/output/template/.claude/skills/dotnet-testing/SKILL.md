---
name: dotnet-testing
description: >
  Use when writing or fixing .NET tests: NUnit fixtures and TestCase tables,
  service unit tests, WebApplicationFactory integration tests, test databases,
  Testcontainers, FakeTimeProvider, HTTP stubs.
---

> Knowledge skill. Owns: .NET testing technique and examples · Scope: backend-tests · Loads: on demand · Depends on: CLAUDE.md, .claude/rules/testing.md

# .NET Testing

Rules: `testing.md`. Regression tests for bug fixes: `development-workflow`.
Preserving behavioral probes as maintained tests: `verify`.

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

Arrange / Act / Assert is a useful structure; the comments are optional when
the phases are obvious.

## Readable Case Tables

Enumerate small finite spaces explicitly rather than generating them with
loops, LINQ, `TestCaseSource`, or logic that derives the expected result:

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

A longer explicit table beats a shorter algorithmic test when it makes the
business rules immediately visible. Multi-step tests fit when the sequence is
the scenario, such as a whole workflow or a replace-set lifecycle.

## Unit Tests

Good candidates: non-trivial domain behavior that genuinely belongs to Domain,
calculations, workflow/state transitions at the owning layer, validation logic,
and application orchestration with simple fakes or mocks when isolation gives
useful feedback. Mock or fake architectural boundaries when that clarifies the
behavior under test.

## Application Service Tests

Replace repository and external-service abstractions with controlled test
doubles and assert on the use-case result and meaningful side effects. "Method X
was called once" is useful only when the interaction is part of the contract.
If important behavior depends on EF Core semantics, transactions, DI wiring,
serialization, or HTTP, write an integration test instead of reproducing the
stack with mocks.

## ASP.NET Core Integration Tests

`WebApplicationFactory<Program>` exercises the real pipeline: routing, model
binding, serialization, middleware, authentication/authorization wiring, DI,
Application services, repositories, EF Core, and persistence.

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

Configure the `Testing` environment with isolated test resources (isolation
rule: `testing.md`). If
top-level statements make `Program` inaccessible, expose it, for example with a
public partial `Program` declaration.

## Test Database Strategy

Use the actual provider when the test covers provider-specific SQL,
constraints, transactions, locking or concurrency, indexes, raw SQL,
provider-specific mappings, or migrations; Testcontainers is a good option when
an isolated real database is useful. When provider fidelity does not matter, a
lighter isolated relational database may be acceptable for application/API
integration tests — state the trade-off. EF Core InMemory may suit a narrowly
scoped test where relational semantics are irrelevant, but a fake repository is
often clearer for a true unit test.

## Database State

Start each test from a known state with a simple strategy: recreate or reset
the isolated test database, use transactions when their semantics fit, seed only
the data the test needs, and use unique identifiers to prevent collisions.

## Persistence Tests

Test repository implementations or EF mappings when there is meaningful
persistence behavior — custom mappings, query filters, projections, non-trivial
queries, relationships, concurrency, provider-specific behavior — not one test
per trivial `Add` and `Get`.

## Time-Dependent Code

```csharp
var time = new FakeTimeProvider(
    new DateTimeOffset(
        2026, 1, 1,
        0, 0, 0,
        TimeSpan.Zero));

time.Advance(TimeSpan.FromDays(1));
```

## External Services

Use a fake or mock abstraction for unit tests, a stub `HttpMessageHandler`,
WireMock or another local fake server for HTTP integration, and a dedicated
sandbox only when a test explicitly targets that integration. Keep slow or
unreliable external-system tests separate from fast runs.

## Test Data

Keep test data explicit and minimal; introduce builders, fixtures, or factories
when repeated setup becomes hard to read, not a generic test-data framework for
a few objects.

## Naming Examples

```csharp
CreateOrder_WithValidRequest_ReturnsCreated
CreateOrder_WithMissingCustomer_ReturnsValidationError
GetOrder_WithUnknownId_ReturnsNotFound
```

## Regression Tests

A regression test reproduces the failure before the fix and passes after it.
Skip it when the problem cannot realistically recur or is already covered.

## Turning Probes into Tests

Typical probes and their maintained replacements: a temporary `curl`,
PowerShell, or REST request → a `WebApplicationFactory` integration test; a
manual database check → a persistence or integration test; an ad-hoc test
method → a reviewed, named test in the right project.

## Smoke Tests

"Smoke test" means a small set of fast checks that a built or deployed
application is basically operational, not a synonym for every integration test.

## Snapshot Testing

Snapshots may help for large stable outputs where explicit assertions become
noisy; do not add a snapshot library by default, and use explicit assertions for
small or important contracts.

## Anti-Patterns

- testing private implementation details or mocking every class;
- assertions that merely repeat the implementation;
- assertion-free tests, unless the behavior is explicitly "does not throw";
- arbitrary delays such as `Task.Delay` to make timing-sensitive tests pass;
- Testcontainers where no provider fidelity is required;
- keeping temporary probes as permanent tests without review.

## Decision Guide

| Scenario | Default approach |
|---|---|
| Pure business rule | NUnit unit test |
| Application orchestration | Unit test with controlled boundary doubles when useful |
| Full API pipeline | `WebApplicationFactory<Program>` |
| Important EF/provider behavior | Integration test using the actual provider |
| Simple API integration, provider specifics irrelevant | Lightweight isolated relational test DB may suffice |
| Time-dependent behavior | `TimeProvider` / `FakeTimeProvider` |
| External HTTP dependency | Stub handler or local fake server |
| Reproduced bug | Focused regression test |
| Temporary behavioral probe | Convert to maintained coverage or confirm equivalent coverage |
| Deployment/basic health | Smoke test |
