---
paths:
  - "Directory.Build.props"
  - "Directory.Packages.props"
  - "global.json"
  - "*.slnx"
---

> Level: 3 Project · Owns: approved stack, conditional technologies, project defaults, repository layout · Scope: common · Loads: always (imported by CLAUDE.md)

# Project Decisions

Technology selections for the roles in the architecture overview. Entries are **Decided**; replacing one is Reserved. Versions are resolved at install time through `add-dependency`, never copied from examples.

## Approved stack

- **Backend platform:** .NET 10 LTS (latest stable servicing), C# 14, ASP.NET Core; **ASP.NET Core Controllers** are the HTTP entry point. A preview/RC .NET or C# release requires approval.
- **Persistence:** EF Core with Microsoft SQL Server (`Microsoft.EntityFrameworkCore.SqlServer`); provider-specific concerns stay out of Application and Domain.
- **Validation:** FluentValidation (`FluentValidation`, `FluentValidation.DependencyInjectionExtensions`) is the standard library for explicit request and use-case validation.
- **Logging:** application code uses `ILogger<T>`; Serilog (`Serilog.AspNetCore`) is the provider; sinks only when required (Console as local baseline).
- **API documentation:** Swagger UI via `Swashbuckle.AspNetCore` is the Development interactive documentation and manual-testing surface (`/swagger`), not built-in `AddOpenApi()`/`MapOpenApi()`; exposure: `.claude/rules/2-technology/aspnet-core.md`.
- **Backend tests:** NUnit; `WebApplicationFactory<Program>` (`Microsoft.AspNetCore.Mvc.Testing`) is the integration-test baseline; Testcontainers is conditional; test projects live under `backend/`.
- **Frontend:** current stable Angular with CLI-selected compatible TypeScript and RxJS; standalone APIs, strict mode, routing, zoneless when the stable version supports it, SCSS, Angular Material and CDK, Vitest.
- **Packages:** NuGet Central Package Management; npm for the Angular workspace (`.claude/rules/3-project/conventions.md`).
- **Solution and build (default):** `.slnx` (legacy `.sln` only when a tool or requirement needs it); repository-level `Directory.Build.props` for genuinely shared .NET settings and `Directory.Packages.props` for central versions; project-specific settings stay in projects.

## Conditional technologies (approved, not installed by default)

- **Mapster** (`Mapster`, `Mapster.DependencyInjection`) when mapping becomes repetitive or non-trivial; manual mapping is fine for simple cases; another mapping framework requires approval; no mapping concerns in Domain.
- **Resilience:** `Microsoft.Extensions.Http.Resilience` (HttpClient) and `Microsoft.Extensions.Resilience` (non-HTTP) only when a real integration needs resilience. Direct Polly is an explicit, documented exception; never the deprecated `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`.
- **Testcontainers** when isolated real-provider tests justify it. **Playwright** when frontend E2E coverage is required (not in the minimal scaffold).
- **Asp.Versioning** (Controller integration, `Asp.Versioning.Mvc`) only after API versioning is adopted.
- **Docker:** **must not** be introduced merely because the application can be containerized; add container artifacts only when the project or deployment needs them.

## Not added by default

- **Must not** add NgRx, Axios, Lodash, Bootstrap, Tailwind, or extra form, component or state-management libraries by default; use built-in Angular capabilities first and add one only for a concrete need.
- Mediator libraries (MediatR, Kommand) implement the mediator organization the architecture overview lists as not adopted. Minimal API endpoint groups are not created unless explicitly requested.

## Repository layout (default)

Keep backend production and test projects, the frontend workspace and documentation clearly separated: `backend/<Name>.<Layer>/` (Domain, Application, Infrastructure, Api) with backend test projects beside them (no top-level `tests/`), `frontend/<Name>.Web/` (Angular workspace and its tests), `docs/` for maintained documentation. Create only what the scope needs; procedure: `project-structure`.
