> Kind: DEC | Scope: common | Owner: project decision register — the single place where project and architecture decisions are recorded and summarized | Loading: always (imported by CLAUDE.md)

# Decision Register

Every entry is **Decided** (CLAUDE.md § Decisions). Changing an entry is Reserved: run `architecture-decision`, which updates the entry and every artifact in **Affects**. Policy detail stays with the **Details in** owner. Paths are relative to `.claude/` unless they start with `docs/` or name a repository-root file.

## Architecture

| ID | Decision | Details in | Affects |
|---|---|---|---|
| D-01 | Clean Architecture: `Domain`, `Application`, `Infrastructure` and `Api` production projects with inward dependencies; ASP.NET Core Controllers are the HTTP entry point; Application Services orchestrate use cases; specific repositories with `IUnitOfWork` as the commit boundary; simple Domain entities. | rules/backend/architecture.md | rules/backend-tests/testing.md, rules/backend/api.md, rules/backend/architecture.md, skills/build-fix, skills/code-review, skills/dependency-injection, skills/project-structure, scripts/check-dependencies.cjs |
| D-02 | Not adopted: CQRS handlers, MediatR, Kommand, Vertical Slice Architecture or similar mediator-based organization; introducing any of them requires explicit approval. Other styles that are not adopted are listed as Reserved in CLAUDE.md § Decisions. | — | rules/backend/architecture.md, skills/code-review, skills/project-structure, scripts/check-dependencies.cjs |

## Approved stack

| ID | Decision | Details in | Affects |
|---|---|---|---|
| D-03 | Backend platform: .NET 10 LTS on its latest stable servicing release, C# 14, ASP.NET Core, ASP.NET Core Controllers. Moving to a preview or RC .NET or C# release requires approval. | skills/project-structure | rules/backend/csharp.md, skills/ci-cd, skills/docker, skills/modern-csharp, skills/project-structure, Directory.Build.props |
| D-04 | Persistence: EF Core with Microsoft SQL Server (`Microsoft.EntityFrameworkCore.SqlServer`); provider-specific concerns stay out of Application and Domain. | rules/backend/architecture.md | rules/backend/architecture.md, rules/backend/persistence.md, skills/ef-core, skills/project-structure |
| D-05 | Validation: FluentValidation (`FluentValidation`, `FluentValidation.DependencyInjectionExtensions`) for explicit request and use-case validation. | rules/backend/error-handling.md | rules/backend/error-handling.md, skills/add-dependency, skills/aspnet-error-handling, skills/project-structure, scripts/check-dependencies.cjs |
| D-06 | Logging: `ILogger<T>` in application code with Serilog as the provider (`Serilog.AspNetCore`; sinks only as required). | rules/backend/hosting.md | rules/backend/hosting.md, skills/logging, skills/project-structure |
| D-07 | API documentation: Swashbuckle Swagger UI (`Swashbuckle.AspNetCore`) is the Development interactive documentation and manual-testing surface at `/swagger`; exposed outside Development only when requirements justify it. | rules/backend/api.md | rules/backend/api.md, skills/project-structure, skills/swagger, skills/verify |
| D-08 | Backend tests: NUnit; backend test projects live under `backend/` beside production projects; `WebApplicationFactory<Program>` (`Microsoft.AspNetCore.Mvc.Testing`) for ASP.NET Core integration tests; Testcontainers is conditional. | rules/backend-tests/testing.md | rules/backend-tests/testing.md, skills/dotnet-testing, skills/project-structure |
| D-09 | Frontend: current stable Angular created with the Angular CLI (CLI-selected compatible TypeScript and RxJS), standalone APIs, strict mode, routing, zoneless mode when supported, SCSS, Angular Material and CDK, Vitest; npm workspace. | rules/frontend/angular.md | rules/common/dependencies.md, rules/frontend/angular.md, skills/angular, skills/build-fix, skills/ci-cd, skills/project-structure |
| D-10 | Not added by default: NgRx, Axios, Lodash, Bootstrap, Tailwind, or additional form, component or state-management libraries; built-in Angular capabilities come first and extras need a concrete requirement. | rules/frontend/angular.md | rules/frontend/angular.md, skills/angular, skills/project-structure, scripts/check-dependencies.cjs |

## Conditional technologies

| ID | Decision | Details in | Affects |
|---|---|---|---|
| D-11 | Mapping: manual mapping for simple cases; Mapster (`Mapster`, `Mapster.DependencyInjection`) is approved when mapping volume warrants it. | — | skills/project-structure, scripts/check-dependencies.cjs |
| D-12 | Resilience: `Microsoft.Extensions.Http.Resilience` for HttpClient and `Microsoft.Extensions.Resilience` for other pipelines, approved only when a real integration needs resilience. | rules/backend/integrations.md | rules/backend/integrations.md, skills/add-dependency, skills/httpclient-factory, scripts/check-dependencies.cjs |
| D-13 | Frontend E2E: Playwright is the approved default when E2E coverage is required; it is not part of the minimal scaffold. | skills/angular | skills/angular, skills/project-structure |
| D-14 | Containers: Docker is optional; add container artifacts only when the project or its deployment actually needs them. | rules/backend/hosting.md | rules/backend/hosting.md, skills/ci-cd, skills/delivery-pipeline, skills/docker |
| D-15 | API versioning: not adopted until a published-compatibility need exists; when adopted, `Asp.Versioning` with its Controller integration. | rules/backend/api.md | rules/backend/api.md, skills/add-dependency, skills/api-versioning, skills/project-structure |

## Project defaults

| ID | Decision | Details in | Affects |
|---|---|---|---|
| D-16 | Solution format: `.slnx`; legacy `.sln` only when an external tool or project requirement needs it. | skills/project-structure | rules/common/repository-layout.md, skills/project-structure |
| D-17 | Shared .NET build configuration: repository-level `Directory.Build.props` for genuinely shared build settings and `Directory.Packages.props` for Central Package Management; project-specific settings stay in their own projects. | rules/common/dependencies.md | rules/common/dependencies.md, rules/common/repository-layout.md, skills/project-structure, scripts/check-dependencies.cjs, Directory.Build.props, Directory.Packages.props |
| D-18 | Repository layout: `backend/<Name>.<Layer>/` for production and backend test projects, `frontend/<Name>.Web/` for the Angular workspace, `docs/` for documentation; no separate top-level `tests/` directory. | skills/project-structure | rules/common/repository-layout.md, skills/project-structure, scripts/check-dependencies.cjs |
