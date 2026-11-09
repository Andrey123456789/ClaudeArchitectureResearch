> Level: 2-technology | Capability: backend-testing/nunit (backend-testing.commands) | Owns: commands for running and diagnosing NUnit tests | Scope: backend-tests | Loads: read when a workflow step names backend-testing.commands

# Backend Test Commands — NUnit

Run from the repository root; use the repository's actual `.slnx` and project
paths.

| Purpose | Command |
|---|---|
| All tests after a build | `dotnet test --no-build` |
| All tests including build | `dotnet test` |
| One test project | `dotnet test backend/<Name>.Application.Tests/<Name>.Application.Tests.csproj` |
| One fixture or namespace | `dotnet test --filter "FullyQualifiedName~OrdersApiTests"` |
| One test | `dotnet test --filter "Name=CreateOrder_WithValidRequest_ReturnsCreated"` |
| A category (`[Category("Integration")]`) | `dotnet test --filter "TestCategory=Integration"` |
| List discovered tests | `dotnet test --list-tests` |
| Release configuration (CI) | `dotnet test --no-build --configuration Release` |

Use `--no-build` only right after a successful build.

## Discovery and failure diagnosis

- No tests discovered: check the framework package references
  (`backend-testing.rules`, reported by the architecture check); fixtures and
  test methods must be public; `[TestFixture]` classes need a public
  parameterless constructor unless parameterized fixtures are intended.
- `[OneTimeSetUp]` failures mark every test in the fixture as failed — read the
  first failure's setup exception before individual assertions.
- `WebApplicationFactory<Program>` cannot find `Program`: expose it from the
  host (for example `public partial class Program;`).
- Integration tests touching the wrong database: check the `Testing`
  environment configuration (`backend-testing.scaffold`).
