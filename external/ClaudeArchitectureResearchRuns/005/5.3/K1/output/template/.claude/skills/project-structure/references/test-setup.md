> Kind: WF | Scope: backend-tests | Capability: backend-testing/nunit | Loading: read by `project-structure` when its step says so

# Test Setup — NUnit

Scaffolding facet of the backend-testing capability. Placement and references: `backend-layout.md`; standards: `.claude/rules/backend-tests/`.

1. Create each useful test project from the NUnit template beside the production projects:

   ```bash
   dotnet new nunit --name ProjectName.Application.Tests --output backend/ProjectName.Application.Tests
   dotnet new nunit --name ProjectName.IntegrationTests --output backend/ProjectName.IntegrationTests
   dotnet sln ProjectName.slnx add backend/ProjectName.Application.Tests backend/ProjectName.IntegrationTests
   ```

2. Under Central Package Management, move the template's package versions into `Directory.Packages.props` and keep the project references versionless (`add-dependency` resolves current stable versions): `NUnit`, `NUnit3TestAdapter`, `Microsoft.NET.Test.Sdk`, and for integration tests `Microsoft.AspNetCore.Mvc.Testing`. Remove template packages the project does not use.
3. Add only the production project references the test scope requires (`dotnet add <test project> reference <production project>`), recorded first as `From -> To` through `architecture-decision` (`project-structure`, step 4).
4. Integration tests: expose `Program` to `WebApplicationFactory<Program>` when top-level statements hide it (e.g. `public partial class Program;` in Api) and configure an isolated `Testing` environment.
5. Testcontainers or other real-provider infrastructure only when provider fidelity requires it.
6. Build and run `dotnet test` to confirm the projects are discovered.

Technique: `dotnet-testing`.
