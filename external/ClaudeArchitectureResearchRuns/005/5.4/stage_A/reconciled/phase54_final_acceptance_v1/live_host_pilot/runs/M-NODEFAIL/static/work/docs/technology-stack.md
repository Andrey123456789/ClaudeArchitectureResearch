> Owns: approved technology stack, conditional technologies, solution and build defaults | Scope: common | Loads: always (imported by CLAUDE.md)

# Technology Stack

When this stack defines a technology for a capability, use it rather than
silently selecting an alternative; replacing an approved technology is a
Reserved decision (CLAUDE.md § Decision Control). Package versions are resolved
at install time through `add-dependency`, never copied from memory or examples.

## Backend

- Platform: .NET 10 LTS on its latest stable servicing release, C# 14,
  ASP.NET Core, ASP.NET Core Controllers. Moving to a preview/RC .NET or C#
  release requires approval.
- Persistence: Entity Framework Core with Microsoft SQL Server
  (`Microsoft.EntityFrameworkCore.SqlServer`); provider-specific concerns stay
  out of Application and Domain.
- Validation: FluentValidation (`FluentValidation`,
  `FluentValidation.DependencyInjectionExtensions`) is the standard library for
  explicit request and use-case validation; do not use a deprecated or legacy
  ASP.NET automatic-validation integration package without a concrete
  requirement.
- Logging: application code logs through `ILogger<T>`; Serilog is the logging
  provider (`Serilog.AspNetCore`). Add sinks only when required — a Console sink
  is enough for local Development.
- API documentation: Swagger UI through `Swashbuckle.AspNetCore` is the default
  interactive API documentation and manual-testing surface in Development
  (`/swagger`); built-in `AddOpenApi()`/`MapOpenApi()` is not the template
  default. Expose Swagger UI outside Development only when requirements justify
  it.
- Testing: NUnit; `Microsoft.AspNetCore.Mvc.Testing` with
  `WebApplicationFactory<Program>` is the baseline for ASP.NET Core integration
  tests; backend test projects live under `backend/` beside the production
  projects.
- Solution format: `.slnx` by default; use legacy `.sln` only when an external
  tool or project requirement needs it.
- Shared build configuration: repository-level `Directory.Build.props` for
  genuinely shared .NET build settings and `Directory.Packages.props` for NuGet
  Central Package Management; project-specific settings stay in their owning
  projects.

## Frontend

- Angular: the latest stable release supported by the selected Node.js, created
  with the current Angular CLI, which selects compatible TypeScript and RxJS
  versions; standalone APIs, strict mode, routing, zoneless mode when supported,
  SCSS, Angular Material and Angular CDK, Vitest.
- Do not add NgRx, Axios, Lodash, Bootstrap, Tailwind, or additional form,
  component, or state-management libraries by default; use built-in Angular
  capabilities first and add an extra library only for a concrete need.

## Conditional Technologies

Approved, but added only when the capability is actually needed:

- Mapping: manual mapping is fine for simple cases; Mapster (`Mapster`,
  `Mapster.DependencyInjection`) is approved when mapping volume warrants it.
  No other mapping framework without approval; mapping-library concerns stay
  out of Domain.
- Resilience: the Microsoft resilience packages
  (`Microsoft.Extensions.Http.Resilience`, `Microsoft.Extensions.Resilience`) are
  approved only when a real integration needs resilience; package choice
  details live in `add-dependency`.
- Testcontainers: when isolated real-provider tests justify it.
- Playwright: the approved default when frontend E2E coverage is required; not
  part of the minimal baseline scaffold.
- Docker: do not introduce Docker merely because the application can be
  containerized; add container artifacts only when the project or deployment
  actually needs them.
