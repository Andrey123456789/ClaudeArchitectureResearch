> Owns: approved technology stack, conditional technologies, repository layout defaults | Scope: common | Loads: always (imported by CLAUDE.md)

# Technology Stack and Repository Layout

Everything here is Decided. When a technology is approved here, use it rather
than silently selecting an alternative; replacing it requires approval
(CLAUDE.md, Decision Control). This file pins no package versions: resolve them
at install time through `add-dependency`.

## Backend

- Platform: .NET 10 LTS (latest stable servicing release of the line), C# 14,
  ASP.NET Core, ASP.NET Core Controllers. Moving to a preview/RC .NET or C#
  release requires approval.
- Persistence: Entity Framework Core with Microsoft SQL Server
  (`Microsoft.EntityFrameworkCore.SqlServer`); provider-specific concerns stay
  out of Application and Domain.
- Validation: FluentValidation (`FluentValidation`,
  `FluentValidation.DependencyInjectionExtensions`) is the standard library for
  explicit request/use-case validation. Do not use a deprecated or legacy
  ASP.NET automatic-validation integration package without a concrete
  requirement.
- Logging: application code depends on `ILogger<T>`; Serilog
  (`Serilog.AspNetCore`) is the logging provider. Add sinks only when required;
  a Console sink is enough for a local Development baseline.
- API documentation: Swashbuckle (`Swashbuckle.AspNetCore`) Swagger UI is the
  default interactive documentation and manual-testing surface, exposed at
  `/swagger` in Development. Built-in `AddOpenApi()`/`MapOpenApi()` is not the
  template default. Expose Swagger UI outside Development only when deployment
  requirements explicitly justify it.
- Testing: NUnit is the .NET test framework; backend test projects live under
  `backend/` beside production projects; `Microsoft.AspNetCore.Mvc.Testing`
  (`WebApplicationFactory<Program>`) is the ASP.NET Core integration-test
  baseline.

## Frontend

- Current stable Angular, created with the current Angular CLI, with the
  CLI-selected compatible TypeScript and RxJS versions; standalone APIs, strict
  mode, routing, zoneless mode when supported by the selected stable version,
  SCSS, Angular Material, Angular CDK, and Vitest. Do not upgrade TypeScript
  beyond Angular's supported range.
- npm is the package manager unless the project deliberately adopts another.
- Do not add NgRx, Axios, Lodash, Bootstrap, Tailwind, or additional
  form/component/state-management libraries by default; use built-in Angular
  capabilities first and add an extra library only for a concrete need.

## Conditional Technologies

Approved, but added only when the capability is actually needed:

| Technology | Add when |
|---|---|
| Mapster + `Mapster.DependencyInjection` | Mapping volume becomes repetitive or non-trivial (manual mapping is fine for simple cases). Another mapping framework requires approval. |
| `Microsoft.Extensions.Http.Resilience` | Outbound `HttpClient` calls need resilience behavior. |
| `Microsoft.Extensions.Resilience` | A non-HTTP resilience pipeline is needed. |
| Testcontainers | Isolated real-provider tests are justified. |
| Playwright | Frontend E2E coverage is required; its tests stay in the frontend workspace. |
| `Asp.Versioning.Mvc` (Controller integration) | API versioning has been adopted (Reserved); not before. |
| Docker | The project or its deployment actually needs containers — never merely because the application can be containerized. |

Resilience: when resilience is required, prefer the Microsoft.Extensions
resilience packages above. Do not add `Microsoft.Extensions.Http.Polly` or
`Polly.Extensions.Http` (deprecated). Direct Polly configuration is an explicit
exception: use it only when a concrete requirement cannot be expressed through
the Microsoft.Extensions resilience APIs, and document why.

## Repository Layout

- Backend production and test projects: `backend/<Name>.<Layer>/` (for example
  `<Name>.Domain`, `<Name>.Application`, `<Name>.Infrastructure`, `<Name>.Api`,
  `<Name>.Application.Tests`, `<Name>.IntegrationTests`). Angular workspace:
  `frontend/<Name>.Web/`. Maintained documentation: `docs/`. Keep these areas
  clearly separated; do not create a separate top-level `tests/` directory.
- Use the `.slnx` solution format by default; use legacy `.sln` only when an
  external tool or project requirement needs it.
- Use repository-level `Directory.Build.props` for genuinely shared .NET build
  settings and `Directory.Packages.props` for Central Package Management; keep
  project-specific settings in their owning projects.
- Accepted architecture decision records live in `docs/decisions/`.
