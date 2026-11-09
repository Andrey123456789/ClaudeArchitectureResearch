---
name: dotnet-testing
description: >
  Use for .NET tests: NUnit [Test] and [TestCase], Assert.That,
  WebApplicationFactory integration tests, test databases, FakeTimeProvider,
  HTTP stubs, builders.
---
> Level: 2-technology | Capability: backend-testing/nunit (backend-testing.knowledge) | Owns: NUnit and .NET test technique and examples | Scope: backend-tests | Loads: on demand (skill)

# .NET Testing with NUnit

Policy: `testing.md` (framework-neutral) and `test-framework.md` (NUnit).
Commands: `backend-testing.commands`. Examples use the current frame's
test-project and host names.

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
        var calculator = new PriceCalculator();

        var result = calculator.Calculate(quantity, price);

        Assert.That(result, Is.EqualTo(expected));
    }
}
```

Arrange/Act/Assert is a useful structure; comments are optional when the phases
are obvious. Use the constraint model (`Assert.That(actual, Is...)`).

## Explicit cases

List small finite case spaces as `[TestCase]` rows rather than generating them
with loops, LINQ, `TestCaseSource`, or logic that derives the expected value:

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
business rules visible. One observable scenario per test; multi-step tests fit
when the sequence itself is the scenario (a whole workflow or a replace-set
lifecycle).

## Unit tests and test doubles

Good unit-test targets: non-trivial domain behavior, calculations,
workflow/state transitions at the role that owns them, validation logic, and
use-case orchestration with simple fakes. Use fakes, stubs, or mocks when they
make an isolated test clearer; do not mock every collaborator mechanically, and
do not forbid mocking project-owned abstractions when isolation helps.

Use-case units can be unit-tested by replacing persistence-access and
external-service contracts with controlled doubles; assert on the use-case
result and meaningful side effects. "Method X was called once" is useful only
when the interaction is the contract. When the behavior depends on real
persistence, transaction, DI, serialization, or HTTP semantics, write an
integration test instead of re-creating the stack with mocks.

## ASP.NET Core integration tests

`WebApplicationFactory<Program>` exercises routing, model binding,
serialization, middleware, authentication/authorization wiring, DI, use-case
units, persistence implementations, and the database.

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
        var response = await _client.PostAsJsonAsync(
            "/api/orders",
            new CreateOrderRequest("customer-1"));

        Assert.That(response.StatusCode, Is.EqualTo(HttpStatusCode.Created));
    }
}
```

The `Testing` environment must point to isolated test resources. If top-level
statements hide `Program`, add `public partial class Program;` to the host.

## Test database strategy

Pick the strategy by what the test must prove.

- **Provider fidelity matters** (provider-specific SQL, constraints,
  transactions, locking/concurrency, indexes, raw SQL, provider mappings,
  migrations): run against the provider declared in the capability selection
  (`relational test fidelity`). An isolated container-hosted instance is a good
  option, not a requirement.
- **Provider fidelity does not matter** (primarily API/application
  integration): a lighter isolated relational database may be acceptable — state
  the trade-off explicitly.
- **In-memory providers** are not relational; use them only for narrow tests
  where relational semantics are irrelevant — a fake repository is often
  clearer for a true unit test.

## Database state

Start every test from a known state: recreate or reset the isolated database,
use transactions when their semantics fit, seed only the data the test needs,
and use unique identifiers to avoid collisions.

## Persistence tests

Test repository implementations or mappings when there is meaningful behavior —
custom mappings, query filters, projections, non-trivial queries,
relationships, concurrency, provider-specific behavior — not every trivial
`Add`/`Get`.

## Time-dependent code

```csharp
var time = new FakeTimeProvider(
    new DateTimeOffset(2026, 1, 1, 0, 0, 0, TimeSpan.Zero));

time.Advance(TimeSpan.FromDays(1));
```

## External services

Use a fake or mock contract for unit tests, a stub `HttpMessageHandler` or a
local fake server (for example WireMock) for HTTP integration, and a dedicated
sandbox only for tests that explicitly target that integration. Keep slow or
unreliable external-system tests out of ordinary fast runs.

## Test data

Keep data explicit and minimal; add builders, fixtures, or factories when
repeated setup becomes hard to read — not a generic framework for a few objects.

## Naming

`MethodOrScenario_StateOrCondition_ExpectedBehavior`, for example
`CreateOrder_WithValidRequest_ReturnsCreated`,
`CreateOrder_WithMissingCustomer_ReturnsValidationError`,
`GetOrder_WithUnknownId_ReturnsNotFound`.

## Regression tests and probes

When `develop` calls for a regression test, write it so that it reproduces the
reported failure first.
A temporary probe (an ad-hoc `curl`/PowerShell request, a manual database
check) becomes, for example, an integration test using `WebApplicationFactory`;
review a temporary probe before keeping it as a permanent test.

## Smoke tests and snapshots

"Smoke test" means a few fast checks that a built or deployed application is
basically operational — not a synonym for every integration test. Snapshot
testing can help for large stable outputs; do not add a snapshot library by
default, and prefer explicit assertions for small or important contracts.

## Anti-patterns

Testing private details; mocking every class; shared mutable state; assertions
that repeat the implementation; assertion-free tests (unless "does not throw" is
the behavior); `Task.Delay` to make timing pass; container databases when no
provider fidelity is needed; in-memory providers while claiming relational
coverage.

## Decision guide

| Scenario | Default approach |
|---|---|
| Pure business rule | NUnit unit test with `[TestCase]` rows |
| Use-case orchestration | Unit test with controlled contract doubles |
| Full API pipeline | `WebApplicationFactory<Program>` |
| Important provider behavior | Integration test on the declared provider |
| Time-dependent behavior | `TimeProvider` / `FakeTimeProvider` |
| External HTTP dependency | Stub handler or local fake server |
| Reproduced bug | Focused regression test |
| Temporary behavioral probe | Maintained test or confirmed equivalent coverage |
