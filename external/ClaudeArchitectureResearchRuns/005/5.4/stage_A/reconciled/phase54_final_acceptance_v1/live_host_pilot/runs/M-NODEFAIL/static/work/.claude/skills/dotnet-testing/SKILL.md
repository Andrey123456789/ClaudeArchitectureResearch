---
name: dotnet-testing
description: >
  Use when writing or reviewing .NET tests with NUnit: unit tests, test doubles,
  WebApplicationFactory integration tests, test databases, FakeTimeProvider,
  HTTP stubs, probes turned into tests.
---

> Owns: .NET testing technique and examples (no policy) | Scope: backend-tests | Loads: on demand (knowledge skill)

# .NET Testing

Policy owners: framework, test level, behavior focus, isolation, provider
fidelity, data ownership, readability, coverage, and naming —
`.claude/rules/testing.md`; regression tests for bug fixes —
`development-workflow`; preserving behavioral probes — `verify` step 4.

Test the risks that matter for the current project; keep test infrastructure
proportional (CLAUDE.md § Core Defaults) — a small project does not need an
enterprise-sized test harness.

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

Arrange / Act / Assert is a useful default structure; comments are optional when
the phases are obvious.

## Explicit Case Tables

Test code should be simpler to reason about than the production behavior it
verifies; optimize tests for clarity rather than minimum line count. Prefer:

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

A longer explicit case table beats a shorter algorithmic test when it makes the
business rules immediately visible. Multi-step tests suit scenarios where the
sequence is the behavior, such as an entire workflow or a replace-set lifecycle.

## Unit Tests

Good candidates: non-trivial domain behavior that genuinely belongs to Domain;
calculations; workflow/state transitions at the layer that owns them;
validation logic; application orchestration with simple fakes or mocks when
isolation gives useful feedback.

## Test Doubles

Use fakes, stubs, or mocks when they make an isolated test clearer; do not mock
every collaborator mechanically, and do not forbid mocking project-owned
abstractions when isolation is useful. Mock or fake architectural boundaries
when that clarifies the behavior under test.

## Application Service Tests

Application Services can be unit-tested by replacing repository and
external-service abstractions with controlled test doubles. Focus assertions on
the use-case result and meaningful side effects. A verification such as
"repository method X was called once" is useful only when that interaction is
part of the contract; it is not the default assertion style. When important
behavior depends heavily on EF Core semantics, transactions, DI wiring,
serialization, or HTTP, prefer an integration test over reproducing the stack
with mocks.

## ASP.NET Core Integration Tests

`WebApplicationFactory<Program>` exercises the real HTTP pipeline: routing,
model binding, serialization, middleware, authentication/authorization wiring,
dependency injection, Application services, repositories, EF Core, and database
persistence.

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

Configure the `Testing` environment to use isolated test resources so an
integration test can never reach a Development or Production database. If
top-level statements make `Program` inaccessible to the test project, expose it,
for example with a `public partial class Program` declaration.

## Test Database Strategy

Use the actual provider when the test covers provider-specific SQL,
constraints, transactions, locking or concurrency, indexes, raw SQL,
provider-specific mappings, or migrations; Testcontainers is a good option when
an isolated real database is useful. When provider fidelity does not matter, a
lighter isolated relational database may be acceptable for tests that are mainly
about application/API integration — state the trade-off explicitly. EF Core
InMemory may fit a narrowly scoped test where relational semantics are
irrelevant, but a fake repository is often clearer for a true unit test.

## Database State

Choose a simple strategy for starting from a known state: recreate or reset the
isolated test database, use transactions when their semantics fit, seed only the
data the test needs, and use unique identifiers to prevent collisions.

## Persistence Tests

Test repository implementations or EF mappings when there is meaningful
persistence behavior to verify — custom mappings, query filters, projections,
non-trivial queries, relationships, concurrency, provider-specific behavior —
not one test per trivial `Add`/`Get` method.

## Time-Dependent Code

Inject `TimeProvider` and control it with `FakeTimeProvider`:

```csharp
var time = new FakeTimeProvider(
    new DateTimeOffset(
        2026, 1, 1,
        0, 0, 0,
        TimeSpan.Zero));

time.Advance(TimeSpan.FromDays(1));
```

## External Services

At the relevant boundary use a fake or mock abstraction for unit tests, a stub
`HttpMessageHandler`, WireMock or another local fake server for HTTP
integration, or a dedicated sandbox only when the test explicitly targets that
integration. Keep slow or unreliable external-system tests separate from
ordinary fast runs.

## Test Data

Keep test data explicit and minimal. Introduce builders, fixtures, or factories
when repeated setup becomes hard to read — not a generic test-data framework for
a few simple objects.

## Test Naming Examples

```csharp
CreateOrder_WithValidRequest_ReturnsCreated
CreateOrder_WithMissingCustomer_ReturnsValidationError
GetOrder_WithUnknownId_ReturnsNotFound
```

## Regression Tests

A regression test reproduces the failure before the fix and passes after it. Do
not add one for a problem that cannot realistically recur or that existing tests
already cover.

## Turning Probes into Tests

When a probe must become maintained coverage (`verify` step 4): replay an ad-hoc
HTTP request as a `WebApplicationFactory` test that sends the same request and
asserts the observed response; replace a manual database check with an
integration test that asserts the persisted state; turn a temporary regression
probe into a focused regression test. Review a temporary probe before keeping
it as a permanent test rather than committing it as-is.

## Smoke Tests

"Smoke test" means a small set of fast checks that a built or deployed
application is basically operational — not a synonym for every integration
test.

## Coverage

Coverage is diagnostic information, not a quality target by itself. Prioritize
meaningful behavior, important edge cases, and risky integrations.

## Snapshot Testing

Snapshot testing can help for large, stable outputs where explicit assertions get
noisy. Do not introduce a snapshot library by default; for small or important
response contracts, explicit assertions are usually clearer.

## Anti-Patterns

Avoid assertions that merely repeat the implementation, assertion-free tests
(unless the behavior is explicitly "does not throw"), arbitrary delays such as
`Task.Delay` to make timing-sensitive tests pass, and Testcontainers when no
provider fidelity is required.

## Decision Guide

| Scenario | Default approach |
|---|---|
| Pure business rule | NUnit unit test |
| Application orchestration | Unit test with controlled boundary doubles when useful |
| Full API pipeline | `WebApplicationFactory<Program>` |
| Important EF/provider behavior | Integration test using the actual provider |
| Simple API integration, provider specifics irrelevant | Lightweight isolated relational test database may be enough |
| Time-dependent behavior | `TimeProvider` / `FakeTimeProvider` |
| External HTTP dependency | Stub handler or local fake server |
| Reproduced bug | Focused regression test |
| Temporary behavioral probe | Convert to maintained coverage or confirm existing coverage |
| Deployment/basic health | Smoke test |
