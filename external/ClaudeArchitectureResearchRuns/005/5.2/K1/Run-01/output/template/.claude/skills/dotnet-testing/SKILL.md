---
name: dotnet-testing
description: Use when writing, reviewing, debugging or organizing .NET automated tests with NUnit — unit tests, WebApplicationFactory integration tests, test databases and Testcontainers, FakeTimeProvider, external-dependency stubs, test data, naming and regression tests.
---
Kind: KNW | Scope: backend-tests | Capability: backend-testing/nunit | Loading: on invocation

# .NET Testing with NUnit

Technique for backend tests. Rules: `.claude/rules/backend-tests/testing.md` and `.claude/rules/backend-tests/test-framework.md`. Completion obligations (probes become maintained tests, regression tests): `verify` → step 4. Test-project creation and commands: the backend-testing workflow facet.

Test the risks that matter for the current project. A small project does not need an enterprise-sized test harness; build test infrastructure only for a concrete testing need.

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

Arrange/Act/Assert is a useful default structure; the comments are optional when the phases are obvious.

## Readable test cases

Optimize tests for clarity rather than minimum line count. List cases with `[TestCase]` instead of generating them, and state expected results instead of computing them:

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

A longer explicit case table is preferable to a shorter algorithmic test when the explicit form makes the business rules visible. Prefer one observable scenario per test; a multi-step test fits when the sequence itself is the scenario, such as a whole workflow or a replace-set lifecycle.

## Unit tests

Good candidates: non-trivial domain behavior that genuinely belongs to Domain, calculations, workflow and state transitions at the layer that owns them, validation logic, and application orchestration with simple fakes or mocks when isolation gives useful feedback. Mock or fake architectural boundaries when that makes the behavior clearer; do not mock every collaborator mechanically, and do not forbid mocking project-owned abstractions when isolation is useful.

## Application service tests

Replace repository and external-service abstractions with controlled test doubles and assert the use-case result and meaningful side effects. A verification such as "repository method X was called once" is useful only when that interaction is part of the contract. When important behavior depends on persistence semantics, transactions, DI wiring, serialization or HTTP, prefer an integration test over reproducing the stack with mocks.

## ASP.NET Core integration tests

`WebApplicationFactory<Program>` exercises the real HTTP pipeline: routing, model binding, serialization, middleware, authentication and authorization wiring, dependency injection, Application services, repositories and database persistence.

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

Configure the `Testing` environment to use isolated test resources so an integration test can never reach a development or production database. If top-level statements make `Program` inaccessible, add `public partial class Program;` to the Api project.

## Test database strategy

- **Provider fidelity matters** (provider-specific SQL, constraints, transactions, locking or concurrency, indexes, raw SQL, provider mappings, migrations): use the production database provider; the persistence knowledge facet names it and how to run it. Testcontainers is a good option for an isolated real database, not a requirement for every test.
- **Provider fidelity does not matter** (primarily application/API integration): a lighter isolated relational database may be acceptable. State the trade-off explicitly and do not claim that the test verifies the production provider's behavior.
- An in-memory provider is not a relational database; for a true unit test a fake repository is usually clearer.

## Database state

Start every test from a known state: recreate or reset the isolated test database, use transactions when their semantics fit, seed only the data the test needs, and use unique identifiers to avoid collisions.

## Persistence tests

Test repository implementations or mappings when there is meaningful persistence behavior: custom mappings, query filters, projections, non-trivial queries, relationships, concurrency, provider-specific behavior. Do not write one test per trivial `Add` or `Get` to raise coverage.

## Time-dependent code

Use `TimeProvider` in the code under test and `FakeTimeProvider` (Microsoft.Extensions.TimeProvider.Testing) to control time:

```csharp
var time = new FakeTimeProvider(new DateTimeOffset(2026, 1, 1, 0, 0, 0, TimeSpan.Zero));

time.Advance(TimeSpan.FromDays(1));
```

## External services

Do not call uncontrolled external services from normal automated tests. At the boundary, use a fake or mock abstraction for unit tests, a stub `HttpMessageHandler`, WireMock or another local fake server for HTTP integration, or a dedicated sandbox only when the test explicitly targets that integration. Keep slow or unreliable external-system tests out of the fast default run (for example with `[Category("External")]`).

## Test data

Keep test data explicit and minimal. Introduce builders, fixtures or factories when repeated setup becomes hard to read; do not introduce a generic test-data framework for a few simple objects.

## Test naming

```csharp
CreateOrder_WithValidRequest_ReturnsCreated
CreateOrder_WithMissingCustomer_ReturnsValidationError
GetOrder_WithUnknownId_ReturnsNotFound
```

## Regression tests

A regression test reproduces the failure before the fix and passes after it. Skip it when the problem cannot realistically recur or an existing test already covers it.

## Behavioral checks performed during implementation

Typical probes that must end up as maintained coverage: temporary HTTP requests against an endpoint, temporary PowerShell or shell scripts, ad-hoc test methods, manual database checks, temporary regression probes. The permanent test does not need to keep the probe's mechanism: an ad-hoc `curl` request can become an NUnit integration test with `WebApplicationFactory<Program>`. When an existing test already covers the behavior, confirm that it actually exercises it instead of adding a duplicate.

## Smoke tests

"Smoke test" means a small set of fast checks that a built or deployed application is basically operational; it is not a synonym for every integration test.

## Coverage and snapshots

Coverage is diagnostic information, not a quality target. Snapshot testing can help for large, stable outputs where explicit assertions get noisy; do not add a snapshot library by default, and prefer explicit assertions for small or important response contracts.

## Anti-patterns

Review checks; the named standard owns each rule (`testing.md` unless noted):

- Tests of private details or exact call sequences, or assertions that repeat the implementation?
- Shared mutable state, execution-order dependence, production resources or development seed data?
- Assertion-free tests (unless the behavior is "does not throw") or arbitrary `Task.Delay` waits?
- Testcontainers where no provider fidelity is needed, or an in-memory provider claimed as relational coverage?
- Every class mocked mechanically?
- Temporary probes kept as permanent tests without review?

## Technique quick reference

| Scenario | NUnit technique |
|---|---|
| Small finite rule table | `[TestCase]` per case |
| Shared expensive setup | `[OneTimeSetUp]` / `[OneTimeTearDown]` on the fixture |
| HTTP pipeline | `WebApplicationFactory<Program>` created once per fixture |
| Time-dependent behavior | `FakeTimeProvider` |
| External HTTP dependency | Stub `HttpMessageHandler` or a local fake server |
| Slow external-system tests | `[Category("External")]`, excluded from the fast run |
| Run a subset | `dotnet test --filter` (backend-testing workflow facet) |
