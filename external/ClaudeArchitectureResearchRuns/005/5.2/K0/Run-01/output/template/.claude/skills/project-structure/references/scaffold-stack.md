<!-- Kind: WF | Scope: common | Owns: baseline scaffolding packages and configuration reference (private to project-structure) | Loads: read by project-structure -->
# Scaffold Stack

Concrete scaffolding details for the decisions in the register. The register owns the choices; `add-dependency` resolves every version at install time — never copy versions from examples or history.

# Backend Platform (DEC-PLAT-01)

Use the latest stable servicing release of the .NET 10 line and its default C# 14; the backend is an ASP.NET Core Web API with Controllers. Shared settings go into `Directory.Build.props` (target framework `net10.0`, nullable, implicit usings).

# Persistence (DEC-DATA-01)

Baseline package: `Microsoft.EntityFrameworkCore.SqlServer` (Infrastructure project), plus `Microsoft.EntityFrameworkCore.Design` where migrations are created and `dotnet-ef` as a local tool when the project uses it.

# Development Database Configuration

The Api project carries `appsettings.json` and `appsettings.Development.json`. Configuration standard: `rules/backend/operations.md` § Configuration. A suitable Windows Development default without credentials:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\MSSQLLocalDB;Database=ProjectName;Trusted_Connection=True;TrustServerCertificate=True;"
  }
}
```

Adapt the database name to the project. When local SQL Server requires credentials, keep the non-secret structure in configuration and supply the secret through user-secrets or another approved local secret mechanism. Development seeding: `rules/backend/persistence.md` § Development Seeding.

# Validation (DEC-VAL-01)

Baseline packages: `FluentValidation`, `FluentValidation.DependencyInjectionExtensions`. Do not add deprecated or legacy ASP.NET automatic-validation integration packages unless a concrete project requirement justifies it.

# Logging (DEC-LOG-01)

Baseline integration: `Serilog.AspNetCore`; a Console sink is enough for a local application, other sinks only when required. Setup technique: `logging` skill (Serilog reference).

# Mapping (DEC-MAP-01)

Manual mapping for small/simple mappings; `Mapster` and `Mapster.DependencyInjection` only when mapping volume becomes repetitive or non-trivial. No mapping-library concerns in Domain.

# Resilience (DEC-RES-01)

`Microsoft.Extensions.Http.Resilience` for outbound `HttpClient`, `Microsoft.Extensions.Resilience` for non-HTTP pipelines — only when a real integration needs timeout/retry/circuit-breaker behavior. Package choice details: `add-dependency` § Conditional Technology Packages.

# API Documentation and Interactive Testing (DEC-DOCS-01)

Baseline package: `Swashbuckle.AspNetCore`, configured so a Development run exposes `/swagger`. Setup technique, including why the built-in OpenAPI endpoint is not the default: `swagger` skill.

# Testing (DEC-TEST-01)

Test projects: `NUnit`, `NUnit3TestAdapter`, `Microsoft.NET.Test.Sdk`; integration tests add `Microsoft.AspNetCore.Mvc.Testing` for `WebApplicationFactory<Program>`. `Testcontainers` is not part of the baseline set (provider fidelity: `rules/backend-tests/testing.md`). The Angular test runner comes with the CLI baseline (DEC-WEB-01); Playwright only when E2E coverage is required (DEC-WEB-03). Technique: `dotnet-testing` skill.

# Angular Frontend (DEC-WEB-01)

Create the workspace with the current Angular CLI, using the latest stable Angular release supported by the selected Node.js environment, for example:

```bash
npx @angular/cli@latest new ProjectName.Web --directory frontend/ProjectName.Web --routing --style=scss --strict
```

Accept the CLI's zoneless and test-runner defaults when the selected stable version supports them (zoneless, Vitest); add Angular Material/CDK with `ng add @angular/material` through `add-dependency`. Let the Angular CLI select mutually compatible Angular, TypeScript and RxJS versions — do not upgrade TypeScript beyond Angular's supported range. Libraries not added by default: DEC-WEB-02.

# Dependency Minimalism

The approved stack names preferred technologies, not a list to install immediately: baseline packages support capabilities present in the initial project, conditional packages arrive only when their capability becomes necessary (`rules/common/dependencies.md` § Need).
