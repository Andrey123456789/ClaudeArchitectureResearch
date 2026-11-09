Kind: WF | Scope: backend-tests | Capability: backend-testing/nunit | Loading: read by `project-structure`, `verify` and `build-fix`

# Workflow Facet: backend-testing / nunit

Test-project and test-run procedures for NUnit. Placement and references come from the architecture workflow facet; standards from `.claude/rules/backend-tests/`. Technique: `dotnet-testing` knowledge skill.

## Create a test project

Create only useful test projects. Their names, locations and project references come from the architecture workflow facet → Test-project placement. Commands:

```bash
dotnet new nunit -n <TestProject> -o backend/<TestProject>
dotnet sln <Name>.slnx add backend/<TestProject>
dotnet add backend/<TestProject> reference <projects assigned by the architecture facet>
```

- Move the package versions that the template generated (NUnit, NUnit3TestAdapter, NUnit.Analyzers, Microsoft.NET.Test.Sdk, coverlet.collector) into `Directory.Packages.props` through `add-dependency`, leaving versionless `PackageReference` entries.
- Remove properties that `Directory.Build.props` already provides.
- Integration-test project: create it the same way and add `Microsoft.AspNetCore.Mvc.Testing`. When top-level statements make `Program` inaccessible, add `public partial class Program;` to the Api project.
- Add `Microsoft.Extensions.TimeProvider.Testing` only when a test needs `FakeTimeProvider`, and Testcontainers only when isolated real-provider tests justify it.

## Install the architecture-conformance adapter

Copy `.claude/scripts/facets/backend-testing/ArchitectureConformanceTests.cs` to the location the architecture workflow facet assigns for it (Test-project placement) and set its namespace. The test runs `node .claude/scripts/check-architecture.mjs` from the repository root and fails with the checker's output when a project reference or package violates the architecture rules. Node.js must be available wherever backend tests run; the test fails clearly when it is not.

## Run tests

```bash
dotnet test
dotnet test backend/<Name>.Application.Tests/<Name>.Application.Tests.csproj
dotnet test --no-build
dotnet test --filter "FullyQualifiedName~OrdersApiTests"
dotnet test --filter "TestCategory=Integration"
```

Use the narrowest project or filter that reproduces a failure, then the affected projects, then the full suite when the change risk requires it.

## Build-fix cues

- Tests not discovered: check the NUnit3TestAdapter and Microsoft.NET.Test.Sdk references and that the project is a test project.
- NUnit.Analyzers diagnostics (`NUnit1xxx`/`NUnit2xxx`) point at incorrect attribute usage or assertions; fix the test rather than suppressing the analyzer.
- `WebApplicationFactory<Program>` cannot find `Program`: add the `public partial class Program;` declaration.
