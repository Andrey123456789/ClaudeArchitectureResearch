> Always-loaded technology decisions, imported by CLAUDE.md. Owns: approved stack, conditional technologies, solution-layout defaults · Scope: common, backend, backend-tests, frontend, delivery · Loads: always, through the @ import in CLAUDE.md · Depends on: CLAUDE.md · Enforced by: .claude/scripts/check-manifests.mjs

# Technology Stack

These are Decided technology choices for this template. Use them; do not
silently select an alternative. Replacing a listed technology is a Reserved
decision (CLAUDE.md, Decision Control). Package versions are resolved when a
package is added (`add-dependency`); this file intentionally names no versions.

## Backend Platform

- .NET 10 LTS (latest stable servicing release of the 10 line), C# 14,
  ASP.NET Core, and ASP.NET Core Controllers.
- Moving to a preview or RC .NET or C# release requires approval.

## Persistence

- Entity Framework Core with Microsoft SQL Server
  (`Microsoft.EntityFrameworkCore.SqlServer`).
- Provider-specific concerns stay out of Application and Domain.

## Validation

- FluentValidation (`FluentValidation`,
  `FluentValidation.DependencyInjectionExtensions`) is the standard library for
  explicit request and use-case validation.
- Do not use a deprecated or legacy ASP.NET automatic-validation integration
  package unless a concrete project requirement justifies it.

## Logging

- Application code logs through the `Microsoft.Extensions.Logging`
  abstractions (`ILogger<T>`); Serilog (`Serilog.AspNetCore`) is the logging
  provider.
- Add sinks only when required; a Console sink is sufficient for local
  Development.

## API Documentation

- Swagger UI through `Swashbuckle.AspNetCore` is the default interactive API
  documentation and manual-testing surface for Controller APIs, served at
  `/swagger` in Development. Exposure in other environments is governed by
  `.claude/rules/api.md`.
- Built-in `AddOpenApi()` / `MapOpenApi()` is not the template default.

## Testing

- NUnit is the .NET test framework.
- Backend test projects live under `backend/` beside the production projects:
  typically `<Name>.Application.Tests` and `<Name>.IntegrationTests`;
  `<Name>.Domain.Tests` only when Domain contains non-trivial behavior.
- `Microsoft.AspNetCore.Mvc.Testing` with `WebApplicationFactory<Program>` is
  the baseline for ASP.NET Core integration tests.
- Testcontainers is conditional, not part of the baseline.
- Angular unit and component tests stay in the Angular workspace; Vitest is the
  baseline runner for new projects.

## Angular Frontend

- The latest stable Angular release supported by the selected Node.js
  environment, created with the current Angular CLI, which selects mutually
  compatible TypeScript and RxJS versions. Do not upgrade TypeScript beyond
  Angular's supported range.
- Baseline: standalone APIs, strict mode, routing, zoneless mode when supported
  by the selected stable version, SCSS, RxJS, Angular Material, Angular CDK,
  and Vitest.
- Not added by default: NgRx, Axios, Lodash, Bootstrap, Tailwind, or additional
  form, component, or state-management libraries. Use built-in Angular
  capabilities first and add an extra library only for a concrete need.
- Playwright is the approved default when frontend E2E coverage is required;
  it is not part of the minimal scaffold, and its tests stay in the frontend
  workspace.

## Conditional Technologies

Approved does not mean installed by default; add each technology only when its
capability is actually needed.

- **Mapping:** default: manual mapping for simple cases; Mapster (`Mapster`,
  `Mapster.DependencyInjection`) when mapping volume becomes repetitive or
  non-trivial. Another mapping framework requires approval.
- **Resilience:** Microsoft resilience packages, only when a real integration
  needs timeout, retry, circuit-breaker, or similar behavior. Package selection:
  `add-dependency`.
- **Containers:** Docker is optional infrastructure. Add container artifacts
  only when the project or its deployment actually needs them, never merely
  because the application can be containerized.
- **API versioning:** not adopted by default (Reserved). Package selection on
  adoption: `add-dependency`.
- **Testcontainers and Playwright:** see Testing and Angular Frontend.

## Solution Layout

- Default physical layout: production projects in `backend/<Name>.<Layer>/`
  (`Domain`, `Application`, `Infrastructure`, `Api`) with the backend test
  projects beside them; the Angular workspace in `frontend/<Name>.Web/`;
  maintained documentation in `docs/`. Keep these clearly separated and do not
  create a separate top-level `tests/` directory.
- Default: the `.slnx` solution format; use legacy `.sln` only when an external
  tool or project requirement needs it.
- Default: repository-level `Directory.Build.props` for genuinely shared .NET
  build settings and `Directory.Packages.props` as the home of Central Package
  Management (rules: `.claude/rules/dependencies.md`); project-specific settings
  stay in their own projects.
- `global.json` pins the stable SDK line of the target .NET release.
- Scaffolding and reorganization: `project-structure` workflow.
