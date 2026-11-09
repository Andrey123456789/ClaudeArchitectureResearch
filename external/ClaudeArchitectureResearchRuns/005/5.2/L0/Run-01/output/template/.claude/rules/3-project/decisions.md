---
paths:
  - "**/*"
---

> Level: 3 Project | Owns: approved stack, conditional technologies, project defaults, repository layout, accepted project decisions | Scope: common | Loads: always (imported by CLAUDE.md) | Depends on: 1-architecture/overview.md

# Project Decisions

When this project has an approved technology, use it; do not silently select an
alternative. Replacing an approved technology requires approval.

## Approved Stack (Decided)

- **Backend platform:** .NET 10 LTS (latest stable servicing release), C# 14,
  ASP.NET Core, ASP.NET Core Controllers. Moving to a preview or RC .NET or C#
  release requires approval.
- **Persistence:** EF Core with Microsoft SQL Server
  (`Microsoft.EntityFrameworkCore.SqlServer`). Provider-specific concerns stay
  out of Application and Domain.
- **Validation:** FluentValidation is the standard library for explicit
  request and use-case validation.
- **Logging:** application code logs through `ILogger<T>`; Serilog
  (`Serilog.AspNetCore`) is the logging provider.
- **API documentation:** Swashbuckle (`Swashbuckle.AspNetCore`) Swagger UI is
  the default Development surface for interactive API documentation and manual
  testing (environment exposure: → `2-technology/aspnet-core.md`).
- **Backend tests:** NUnit; ASP.NET Core integration tests use
  `WebApplicationFactory<Program>` (`Microsoft.AspNetCore.Mvc.Testing`);
  Testcontainers is conditional; backend test projects live under `backend/`
  beside the production projects.
- **Frontend:** current stable Angular with the TypeScript and RxJS versions
  the Angular CLI selects, standalone APIs, strict mode, routing, zoneless mode
  when supported, SCSS, Angular Material and CDK, Vitest.

## Conditional Technologies (Default)

- Mapping: manual mapping for simple cases; Mapster (`Mapster`,
  `Mapster.DependencyInjection`) is approved when mapping volume warrants it.
- Resilience: Microsoft resilience packages are approved only when a real
  integration needs resilience behavior (package choice: `add-dependency`).
- Frontend E2E: Playwright is the approved default when E2E coverage is
  required; it is not part of the minimal baseline scaffold.
- API versioning: the versioning package is added only after versioning is
  approved (package choice: `add-dependency`).

## Not Added by Default

- Frontend: do not add NgRx, Axios, Lodash, Bootstrap, Tailwind, or extra form,
  component, or state-management libraries by default; use built-in Angular
  capabilities first and add an extra library only for a concrete need.
- Containers: Docker is optional infrastructure. Do not introduce it merely
  because the application can be containerized; add container artifacts only
  when the project or deployment needs them.
- MediatR and Kommand are mediator libraries; adopting them falls under the
  Not Adopted architecture decision.

## Project Defaults

- Solution format: `.slnx` by default; use legacy `.sln` only when an external
  tool or project requirement needs it.
- Shared .NET build settings live in repository-level `Directory.Build.props`
  and package versions in `Directory.Packages.props` (Central Package
  Management); project-specific settings stay in their own projects.
- Repository layout: keep backend production and test projects, the frontend
  workspace, and documentation clearly separated; do not create a separate
  top-level `tests/` directory.

```text
backend/<Name>.Domain/  <Name>.Application/  <Name>.Infrastructure/  <Name>.Api/
backend/<Name>.Application.Tests/  <Name>.IntegrationTests/   (test projects)
frontend/<Name>.Web/                                          (Angular workspace and its tests)
docs/
<Name>.slnx  Directory.Build.props  Directory.Packages.props  global.json  .editorconfig
```

## Accepted Project Decisions

Recorded by `architecture-decision`. None yet.
