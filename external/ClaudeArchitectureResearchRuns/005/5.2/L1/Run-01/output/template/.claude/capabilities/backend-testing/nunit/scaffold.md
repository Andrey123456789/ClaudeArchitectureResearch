> Level: 3-project | Capability: backend-testing/nunit (backend-testing.scaffold) | Owns: creation of NUnit test projects | Scope: backend-tests | Loads: read when project-structure names backend-testing.scaffold

# Backend Test Project Scaffold — NUnit

Create only useful test projects; names and references come from the frame
(`architecture.layout`, `architecture.boundaries`).

## Create a test project

```bash
dotnet new nunit -n <Name>.Application.Tests -o backend/<Name>.Application.Tests
dotnet sln <Name>.slnx add backend/<Name>.Application.Tests/<Name>.Application.Tests.csproj
dotnet add backend/<Name>.Application.Tests reference backend/<Name>.Application
```

The template emits versioned `PackageReference` entries: move each version into
`Directory.Packages.props` (Central Package Management) and leave the project
references versionless. Select versions through `add-dependency`.

Packages per test project: `NUnit`, `NUnit3TestAdapter`,
`Microsoft.NET.Test.Sdk`; optionally `NUnit.Analyzers`.

## Integration test project

- Add `Microsoft.AspNetCore.Mvc.Testing` and reference the Api host only.
- Expose `Program` to the test project if top-level statements hide it
  (`public partial class Program;` in the host).
- Configure a `Testing` environment that points to isolated test resources;
  never a Development or Production database.
- Add a real-provider container package only when the decision facet's
  conditional criterion is met.

## Verify

`dotnet test --list-tests` discovers the new tests; then run them with
`backend-testing.commands`.
