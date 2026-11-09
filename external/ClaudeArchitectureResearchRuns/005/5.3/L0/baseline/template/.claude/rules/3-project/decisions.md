---
paths:
  - "*.slnx"
  - "**/*.csproj"
  - "**/Directory.Build.props"
  - "**/Directory.Packages.props"
  - "frontend/**/package.json"
---

> Level: 3 Project · Owns: approved stack, conditional technologies, repository defaults, accepted project decisions (decision summary) · Scope: common · Loads: always (imported by CLAUDE.md) · Depends on: CLAUDE.md, .claude/rules/1-architecture/overview.md

# Project Decisions

This template targets an ASP.NET Core backend and an Angular frontend built on the adopted architecture.

## Approved technology (Decided)

When an approved technology covers a need, use it rather than silently selecting an alternative; replacing one is Reserved. Resolve package versions at install time through `add-dependency`; never copy versions from examples.

| Area | Approved baseline |
|---|---|
| Backend platform | .NET 10 LTS (latest stable servicing release), C# 14, ASP.NET Core, ASP.NET Core Controllers. Moving to a preview/RC .NET or C# release requires approval. |
| Persistence | EF Core with Microsoft SQL Server (`Microsoft.EntityFrameworkCore.SqlServer`); used only inside Infrastructure per `1-architecture/persistence-boundary.md`. |
| Validation | FluentValidation (`FluentValidation`, `FluentValidation.DependencyInjectionExtensions`) is the standard explicit request/use-case validation library. |
| Logging | Application code logs through `ILogger<T>`; Serilog (`Serilog.AspNetCore`) is the provider; add sinks only when required (Console is enough locally). |
| API documentation | Swashbuckle (`Swashbuckle.AspNetCore`) Swagger UI is the default Development interactive documentation and manual-testing surface; exposure beyond Development follows `2-technology/aspnet-core.md`. |
| Backend tests | NUnit. Backend test projects live under `backend/` alongside the production projects. `Microsoft.AspNetCore.Mvc.Testing` / `WebApplicationFactory<Program>` is the integration-test baseline. Testcontainers is conditional. |
| Frontend | Current stable Angular with CLI-selected compatible TypeScript and RxJS; standalone APIs, strict mode, routing, zoneless mode when supported, SCSS, Angular Material and CDK, Vitest. |

## Conditional technologies (approved, not installed by default)

| Technology | Add only when |
|---|---|
| Mapster, `Mapster.DependencyInjection` | mapping volume is repetitive or non-trivial — manual mapping is fine for simple cases |
| `Microsoft.Extensions.Http.Resilience`, `Microsoft.Extensions.Resilience` | a real integration needs resilience behavior |
| Testcontainers | isolated real-provider tests justify it |
| Playwright | frontend E2E coverage is required — it is the approved default then, but not part of the minimal scaffold |
| Docker / container artifacts | the project or its deployment actually needs containers — never merely because the application can be containerized |

## Not added by default

- Frontend: do not add NgRx, Axios, Lodash, Bootstrap, Tailwind, or additional form, component, or state-management libraries by default; use built-in Angular capabilities first and add an extra library only for a concrete need.
- Backend: mediator libraries such as MediatR or Kommand (mediator-based organization is not adopted — `1-architecture/overview.md`); another mapping framework without approval.

## Repository defaults

- Solution format: `.slnx` by default; use legacy `.sln` only when an external tool or project requirement requires it.
- Repository-level `Directory.Build.props` holds genuinely shared .NET build settings and `Directory.Packages.props` holds Central Package Management versions; project-specific settings stay in their owning projects.
- Physical layout: backend production and test projects under `backend/<Name>.<Layer>/`, the Angular workspace under `frontend/<Name>.Web/`, maintained documentation under `docs/`. Keep them clearly separated and do not create a separate top-level `tests/` directory. Project mapping: `layout.md`.

## Accepted project decisions

Approved stack or default changes are recorded here by `architecture-decision` (date · decision · scope · consequences · modules/workflows updated).

None yet.
