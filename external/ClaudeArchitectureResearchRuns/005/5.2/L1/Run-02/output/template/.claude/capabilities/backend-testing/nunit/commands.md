> Level: 2-technology · Capability: backend-testing/nunit · Facet: backend-testing.commands · Owns: backend test scaffold packages and commands · Scope: backend-tests · Loading: read by `project-structure`, `verify`, `build-fix`

# NUnit Commands

Test-project names and locations come from `architecture.layout`. Install packages only through `add-dependency`.

## Scaffold

```bash
dotnet new nunit --name <TestProjectName> --output backend/<TestProjectName>
dotnet sln <Name>.slnx add backend/<TestProjectName>/<TestProjectName>.csproj
dotnet add backend/<TestProjectName> reference <production project per architecture.layout>
```

`dotnet new nunit` writes package versions into the project file; move them into `Directory.Packages.props` and keep the `PackageReference` entries versionless.

| Package | Purpose |
| --- | --- |
| `NUnit`, `NUnit3TestAdapter`, `Microsoft.NET.Test.Sdk` | framework, runner adapter, test host |
| `NUnit.Analyzers` | analyzer for NUnit usage (template default) |
| `Microsoft.AspNetCore.Mvc.Testing` | `WebApplicationFactory<Program>` integration tests |
| `Microsoft.Extensions.TimeProvider.Testing` | `FakeTimeProvider` when time control is useful |

## Run

```bash
dotnet test                                   # whole solution
dotnet test backend/<TestProjectName>         # one test project
dotnet test --no-build                        # after a successful build
dotnet test --filter "FullyQualifiedName~<Fixture>"
dotnet test --filter "TestCategory=<Category>"   # NUnit [Category]
```
