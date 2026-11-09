> **Private reference** of `dotnet-testing` · Capability: backend-testing/nunit · Owns: NUnit syntax, examples, scaffold and run commands · Scope: backend-tests · Loading: on demand (read by `dotnet-testing`)

# Test Framework Reference — NUnit

Rules: `testing.md` (framework-independent) and `test-framework.md` (NUnit
default and vocabulary binding).

## Scaffold and Run

```bash
dotnet new nunit -n MyApp.Application.Tests -o backend/MyApp.Application.Tests
dotnet sln MyApp.slnx add backend/MyApp.Application.Tests/MyApp.Application.Tests.csproj
dotnet test
dotnet test --filter "FullyQualifiedName~OrdersApiTests"
dotnet test --filter "TestCategory=Integration"
```

After scaffolding, move package versions into `Directory.Packages.props`
(`add-dependency`) and keep the test project's references narrow
(`architecture-style.md` → Test Projects).

## NUnit Basics

Use normal NUnit conventions.

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

## Explicit Case Tables

For small finite input/state spaces, list the cases with `[TestCase]` rather than
generating them with loops, LINQ, `TestCaseSource`, or logic that derives the
expected result:

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

## Integration Test Fixture

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

If top-level statements make `Program` inaccessible to the test project, expose
it with a `public partial class Program;` declaration.

## Useful Features

- `Assert.Multiple(() => { ... })` reports several related assertions together.
- `[Category("Integration")]` separates slow or external-system suites from the
  fast run.
- `[NonParallelizable]` protects fixtures that share an isolated database;
  `[Parallelizable]` opts independent fixtures into parallel execution.
- `[CancelAfter(milliseconds)]` bounds an asynchronous test that receives a
  `CancellationToken` parameter.
