> Owner: approved technology stack and conditional technologies | Scope: common | Loads: always (imported by `CLAUDE.md`) | Enforced: `.claude/scripts/check-dependencies.mjs`, `Directory.Build.props`, `Directory.Packages.props`

# Technology Stack

These are Decided choices. When the project has an approved technology, use it
rather than silently selecting an alternative; replacing one requires approval
(`CLAUDE.md` § Decision Control). Package changes go through the
`add-dependency` workflow, which resolves versions at install time — this file
pins none.

## Backend

- Platform: .NET 10 LTS on its latest stable servicing release, C# 14, ASP.NET
  Core, ASP.NET Core Controllers. Moving to a preview or RC .NET or C# release
  requires approval.
- Solution format: `.slnx` by default; legacy `.sln` only when an external tool
  or project requirement needs it.
- Build configuration: default is repository-level `Directory.Build.props` for
  genuinely shared .NET build settings and `Directory.Packages.props` for NuGet
  Central Package Management; project-specific settings stay in their projects.
- Persistence: Entity Framework Core with Microsoft SQL Server
  (`Microsoft.EntityFrameworkCore.SqlServer`); provider-specific concerns stay
  out of Application and Domain (`.claude/rules/architecture.md`).
- Validation: FluentValidation (`FluentValidation`,
  `FluentValidation.DependencyInjectionExtensions`) is the standard library for
  explicit request and use-case validation; no deprecated or legacy ASP.NET
  automatic-validation integration package.
- Logging: `Microsoft.Extensions.Logging` abstractions (`ILogger<T>`) with
  Serilog as the provider (`Serilog.AspNetCore`); add sinks only when required
  (a Console sink is enough for local Development).
- API documentation: Swagger UI through `Swashbuckle.AspNetCore` is the
  interactive documentation and manual testing surface, reachable at `/swagger`
  in Development; built-in `AddOpenApi()`/`MapOpenApi()` is not the default.
  Exposure outside Development: `.claude/rules/api.md` § Swagger.
- Testing: NUnit; backend test projects live under `backend/` beside the
  production projects; `Microsoft.AspNetCore.Mvc.Testing` with
  `WebApplicationFactory<Program>` is the baseline for ASP.NET Core integration
  tests.

## Conditional Technologies

Approved, but added only when the capability is actually needed:

- Mapping: manual mapping for small or simple cases; Mapster (`Mapster`,
  `Mapster.DependencyInjection`) when mapping volume becomes repetitive or
  non-trivial. Another mapping framework requires approval; no mapping-library
  concerns in Domain.
- Resilience: `Microsoft.Extensions.Http.Resilience` for outbound `HttpClient`
  and `Microsoft.Extensions.Resilience` for non-HTTP pipelines, only when a real
  integration needs timeout, retry, circuit-breaker, or similar behavior. Never
  add `Microsoft.Extensions.Http.Polly` or `Polly.Extensions.Http`; a direct
  Polly reference is an explicit exception that must document why the
  Microsoft.Extensions APIs are insufficient.
- Testcontainers: when isolated real-provider tests justify it.
- API versioning: the Controller integration of `Asp.Versioning`, added only
  after the project adopts API versioning (a Reserved decision).
- Docker: container artifacts only when the project or its deployment actually
  needs them, not merely because the application can be containerized.
- Playwright: the approved default when frontend E2E coverage is required; not
  part of the minimal scaffold.

## Frontend

- The latest stable Angular release supported by the selected Node.js, created
  with the current Angular CLI; let the CLI choose mutually compatible TypeScript
  and RxJS versions.
- Standalone APIs, strict mode, routing, zoneless mode when the selected stable
  Angular supports it, SCSS, RxJS, Angular Material and Angular CDK, and Vitest
  for unit and component tests. Package manager:
  `.claude/rules/dependencies.md` § npm.
- Do not add NgRx, Axios, Lodash, Bootstrap, Tailwind, or additional form,
  component, or state-management libraries by default; use built-in Angular
  capabilities first and add an extra library only for a concrete requirement.
