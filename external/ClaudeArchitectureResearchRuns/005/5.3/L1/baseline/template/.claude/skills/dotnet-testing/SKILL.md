---
name: dotnet-testing
description: NUnit testing technique for .NET backends. Use when writing, reviewing, debugging, or organizing tests — [TestFixture]/[TestCase], application-service tests with test doubles, WebApplicationFactory integration tests, test databases and Testcontainers, FakeTimeProvider, HTTP stubs, regression tests.
---

> Level: 2-technology · Capability: backend-testing/nunit · Facet: backend-testing.knowledge · Owns: backend testing technique and examples · Loading: on demand

# .NET Testing (NUnit)

Rules: `.claude/rules/0-core/testing.md` (neutral policy) and `backend-testing.framework` (NUnit bindings). Probe-to-test preservation: `verify` step 4. Commands: `backend-testing.commands`. This skill adds technique only; do not build test infrastructure the project does not need yet.

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

Arrange/Act/Assert is a useful structure; comments are optional when the phases are obvious.

## Readable case tables

A longer explicit table beats a shorter algorithmic test when it makes business rules visible:

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

Prefer one observable scenario per test; a multi-step test fits when the sequence is the scenario (a whole workflow or replace-set lifecycle).

## Unit and application-service tests

Good unit candidates: non-trivial domain behavior that genuinely belongs to the domain model, calculations, workflow/state transitions at their owning layer, validation logic, orchestration with simple fakes. Replace persistence-access contracts and external abstractions with controlled doubles; assert the use-case result and meaningful side effects. "Method X was called once" is useful only when that interaction is the contract. When behavior depends on ORM semantics, transactions, DI wiring, serialization, or HTTP, prefer an integration test over reproducing the stack with mocks. Do not mock every collaborator mechanically, and do not forbid mocking project-owned abstractions when isolation helps.

## Host integration tests

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

Covers routing, binding, serialization, middleware, auth wiring, DI, use-case units, repositories, and persistence. Configure the `Testing` environment with isolated resources so a test can never reach a Development or Production database. If top-level statements hide `Program`, add `public partial class Program;`.

## Test databases

- Subjects where provider fidelity matters (fidelity rule: backend test rules): provider SQL, constraints, transactions, locking/concurrency, indexes, raw SQL, provider mappings, migrations. Testcontainers gives an isolated real-provider database when that is worth it (provider package: `persistence.commands`).
- Mainly API/application integration where provider specifics are irrelevant → a lighter isolated relational database may do; state the trade-off.
- For a true unit test a fake repository is usually clearer than any in-memory provider (relational-fidelity binding: `persistence.access`).
- Known state: recreate or reset the isolated database, use transactions when their semantics fit, seed only what each test needs, use unique identifiers to avoid collisions.
- Persistence tests target meaningful behavior — custom mappings, query filters, projections, non-trivial queries, relationships, concurrency, provider behavior — not every trivial `Add`/`Get`.

## Time, external services, test data

- `FakeTimeProvider` controls time: `var time = new FakeTimeProvider(new DateTimeOffset(2026, 1, 1, 0, 0, 0, TimeSpan.Zero)); time.Advance(TimeSpan.FromDays(1));`
- External services: fake/mock abstractions for unit tests, a stub `HttpMessageHandler`, WireMock or another local fake server for HTTP integration, a sandbox only when the test explicitly targets that integration; keep slow or flaky external tests out of the fast run.
- Keep test data explicit and minimal; add builders/fixtures when repeated setup hurts readability, not a generic data framework for a few objects.

## Regression tests and probes

A regression test reproduces the failure before the fix and passes after it. Converting a temporary probe: a curl, PowerShell, or REST check becomes a host integration test; a manual database check becomes a persistence test; reuse existing coverage when it already exercises the behavior, after confirming it really does.

## Naming examples

`CreateOrder_WithValidRequest_ReturnsCreated`, `CreateOrder_WithMissingCustomer_ReturnsValidationError`, `GetOrder_WithUnknownId_ReturnsNotFound`.

## Other terms

"Smoke test" means a small set of fast checks that a built or deployed application is basically operational — not every integration test. Coverage percentage is diagnostic only. Snapshot testing can help for large stable outputs but is not added by default; explicit assertions suit small or important contracts.

## Anti-patterns

Testing private details; mocking every class; hitting production resources; shared mutable state; assertions that repeat the implementation; assertion-free tests (unless the behavior is "does not throw"); `Task.Delay` to make timing pass; real-provider containers when fidelity is irrelevant; in-memory providers claimed as relational coverage; keeping temporary probes as permanent tests without review.
