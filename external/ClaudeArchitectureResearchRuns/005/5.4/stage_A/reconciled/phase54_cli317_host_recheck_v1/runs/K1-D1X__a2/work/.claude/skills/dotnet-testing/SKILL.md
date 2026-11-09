---
name: dotnet-testing
description: >
  Use when writing, reviewing, or debugging backend tests: NUnit fixtures,
  [TestCase] tables, mocks and fakes, WebApplicationFactory, test databases,
  FakeTimeProvider, HTTP stubs, test naming, regression tests.
---

> Kind: KNW | Scope: backend-tests | Capability: backend-testing/nunit | Loading: on-demand knowledge

# .NET Testing with NUnit

Policy: `.claude/rules/backend-tests/testing.md`, `.claude/rules/backend-tests/test-framework.md`, `.claude/rules/backend-tests/test-projects.md`. Regression tests and probe preservation: `development-workflow`, `verify`. Persistence-provider technique: the persistence knowledge facet named in the decision register.

Do not build test infrastructure without a concrete testing need; a small project does not need an enterprise-sized harness.

## NUnit basics

```csharp
[TestFixture]
public sealed class PriceCalculatorTests
{
    [TestCase(2, 10, 20)]
    [TestCase(3, 5, 15)]
    public void Calculate_WithValidInput_ReturnsExpectedTotal(int quantity, decimal price, decimal expected)
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

Arrange/Act/Assert is a useful default; comments are optional when the phases are obvious. Use the constraint model (`Assert.That(actual, Is...)`).

## Explicit case tables

Explicit cases (rule: `.claude/rules/backend-tests/testing.md`) are written as `[TestCase]` rows with the expected value as an argument, rather than `TestCaseSource` generators or computed expectations. A longer explicit table beats a shorter algorithmic test when it makes the business rules visible:

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

Prefer one observable scenario per test; multi-step tests fit when the sequence itself is the scenario (an entire workflow or a replace-set lifecycle).

## Unit and Application Service tests

Good unit-test candidates: non-trivial domain behavior that genuinely belongs to Domain, calculations, workflow/state transitions at the owning layer, validation logic, and Application orchestration with simple fakes or mocks when isolation gives useful feedback. Do not mock every collaborator mechanically, and do not forbid mocking project-owned abstractions when isolation helps.

Application Services can be tested by replacing repository and external-service abstractions with controlled doubles; assert the use-case result and meaningful side effects. "Repository method X was called once" is useful only when the interaction is part of the contract. When behavior depends heavily on persistence-technology semantics, transactions, DI wiring, serialization, or HTTP, prefer an integration test over reproducing the stack with mocks.

## ASP.NET Core integration tests

`WebApplicationFactory<Program>` exercises routing, model binding, serialization, middleware, authentication/authorization wiring, DI, Application services, repositories, and database persistence.

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

Configure the `Testing` environment to use isolated test resources so an integration test can never reach a Development or Production database. If top-level statements make `Program` inaccessible, add `public partial class Program;` to the Api project.

## Test database state

Choose the database strategy by what the test must prove (provider fidelity vs. application/API integration) and be explicit about the trade-off. Start from a known state with a simple strategy: recreate or reset the isolated database, use transactions when their semantics fit, seed only the data the test needs, use unique identifiers to avoid collisions. Never modify production data.

## Time-dependent code

Inject `TimeProvider` and control it with `FakeTimeProvider` (Microsoft.Extensions.TimeProvider.Testing):

```csharp
var time = new FakeTimeProvider(new DateTimeOffset(2026, 1, 1, 0, 0, 0, TimeSpan.Zero));
time.Advance(TimeSpan.FromDays(1));
```

## External services

Never call uncontrolled external services from normal test runs. At the boundary use a fake or mock abstraction (unit tests), a stub `HttpMessageHandler`, WireMock or another local fake server (HTTP integration), or a dedicated sandbox only when the test explicitly targets that integration. Keep slow or unreliable external-system tests out of ordinary fast runs.

## Test data

Keep test data explicit and minimal. Introduce builders, fixtures, or factories when repeated setup becomes hard to read; do not add a generic test-data framework for a few simple objects.

## Naming

`MethodOrScenario_StateOrCondition_ExpectedBehavior`, for example `CreateOrder_WithValidRequest_ReturnsCreated`, `CreateOrder_WithMissingCustomer_ReturnsValidationError`, `GetOrder_WithUnknownId_ReturnsNotFound`. Follow an established project convention when one exists.

## Regression tests and probe conversion

A regression test reproduces the failure before the fix and passes after it; skip it when the problem cannot realistically recur or is already covered. Convert temporary behavioral checks — ad-hoc HTTP/curl/PowerShell requests, temporary scripts or test methods, manual database checks, regression probes — into maintained tests, e.g. replace an ad-hoc REST request with a `WebApplicationFactory` integration test. When an existing test already covers the behavior, verify that it really exercises it instead of adding a duplicate. Review temporary probes before promoting them to permanent tests.

## Smoke tests, coverage, snapshots

"Smoke test" means a small set of fast checks that a built or deployed application is basically operational — not a synonym for every integration test. Coverage is diagnostic, not a target; prioritize meaningful behavior, edge cases, and risky integrations. Snapshot testing can help for large stable outputs, but do not add a snapshot library by default; explicit assertions are clearer for small or important contracts.

## Anti-patterns

Avoid assertions that merely repeat the implementation, assertion-free tests (unless the behavior is "does not throw"), arbitrary delays such as `Task.Delay` to make timing-sensitive tests pass, and Testcontainers when no provider fidelity is required.

## Decision guide

| Scenario | Default approach |
|---|---|
| Pure business rule | NUnit unit test with `[TestCase]` table |
| Application orchestration | Unit test with controlled boundary doubles when useful |
| Full API pipeline | `WebApplicationFactory<Program>` |
| Important persistence/provider behavior | Integration test against the actual provider |
| Time-dependent behavior | `TimeProvider` / `FakeTimeProvider` |
| External HTTP dependency | Stub handler or local fake server |
| Reproduced bug | Focused regression test |
| Temporary behavioral check | Convert to maintained coverage or confirm equivalent coverage |
| Deployment/basic health | Smoke test |
