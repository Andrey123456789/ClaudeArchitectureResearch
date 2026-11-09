<!-- Kind: DEC | Scope: common | Owns: accepted project and architecture decisions | Loads: always (imported by CLAUDE.md) -->
# Decision Register

Every entry is **Decided**: use the recorded choice and **do not** silently select an alternative technology; changing or replacing an entry is Reserved — run `architecture-decision`. An entry marked **Default** allows a deviation for a concrete reason that is reported (CLAUDE.md § Vocabulary). Conditional entries are approved but added only when their condition holds. `Details in` names the owner of detailed policy; `Affects` lists artifacts to update when the entry changes (STD = standard under `.claude/rules/`, WF/KNW = skill under `.claude/skills/`, ENF = hook, script or root build file).

## Adopted

| ID | Decision | Details in | Affects |
|---|---|---|---|
| DEC-ARCH-01 | Clean Architecture: `Domain`, `Application`, `Infrastructure`, `Api` projects at `backend/<Name>.<Layer>/`. Layer rules, default orchestration (Application Services) and persistence defaults (specific repositories, `IUnitOfWork`) live in the standards. | STD backend/architecture, STD backend/persistence | STD backend/architecture, STD backend/persistence, WF project-structure, WF code-review, KNW dependency-injection, KNW ef-core, ENF check-manifests |
| DEC-PLAT-01 | .NET 10 LTS (latest stable servicing), C# 14, ASP.NET Core with Controllers. Moving to a preview/RC .NET or C# release requires approval. | WF project-structure | ENF Directory.Build.props, WF project-structure, WF delivery-pipeline, KNW ci-cd, KNW docker, KNW modern-csharp |
| DEC-DATA-01 | EF Core with Microsoft SQL Server (`Microsoft.EntityFrameworkCore.SqlServer`); provider-specific concerns stay out of Application and Domain. | STD backend/persistence | STD backend/persistence, STD backend/operations, KNW ef-core, KNW dotnet-testing, WF project-structure |
| DEC-VAL-01 | FluentValidation (+ `FluentValidation.DependencyInjectionExtensions`) is the standard explicit request/use-case validation library; error contracts default to `ProblemDetails` / `ValidationProblemDetails`. | STD backend/error-handling | STD backend/error-handling, KNW aspnet-error-handling, WF project-structure |
| DEC-LOG-01 | Logging through `ILogger<T>` with Serilog as provider (`Serilog.AspNetCore`; sinks only when required). | STD backend/operations | STD backend/operations, KNW logging, WF project-structure |
| DEC-DOCS-01 | Swashbuckle (`Swashbuckle.AspNetCore`) Swagger UI is the default interactive API documentation and manual-testing surface in Development; outside Development only when requirements justify it. | STD backend/operations | STD backend/operations, STD backend/api, KNW swagger, WF verify, WF project-structure |
| DEC-BUILD-01 | **Default:** `.slnx` solution format (`.sln` only when a tool or requirement needs it); repository-level `Directory.Build.props` for genuinely shared .NET settings and `Directory.Packages.props` for Central Package Management; project-specific settings stay in their projects. | STD common/dependencies, WF project-structure | ENF Directory.Build.props, ENF Directory.Packages.props, ENF check-manifests, STD common/dependencies, WF project-structure |
| DEC-LAYOUT-01 | **Default:** backend production and test projects under `backend/`, Angular workspace at `frontend/<Name>.Web/`, maintained documentation in `docs/`, clearly separated; no top-level `tests/` directory. | STD common/structure, WF project-structure | STD common/structure, WF project-structure, KNW ci-cd, KNW docker, ENF check-instructions |
| DEC-TEST-01 | NUnit for .NET tests; backend test projects under `backend/` beside production projects; `WebApplicationFactory<Program>` (`Microsoft.AspNetCore.Mvc.Testing`) is the integration-test baseline; Testcontainers only when isolated real-provider tests justify it. | STD backend-tests/testing | STD backend-tests/testing, KNW dotnet-testing, WF project-structure, WF verify, ENF check-manifests |
| DEC-WEB-01 | Current stable Angular via Angular CLI (CLI-selected compatible TypeScript and RxJS), standalone APIs, strict mode, routing, zoneless mode when supported, SCSS, Angular Material and CDK, Vitest; npm workspace. | STD frontend/angular | STD frontend/angular, KNW angular, WF project-structure, KNW ci-cd |

## Not Adopted

| ID | Decision | Details in | Affects |
|---|---|---|---|
| DEC-ARCH-02 | CQRS handlers, MediatR, Kommand, Vertical Slice Architecture or similar mediator-based organization **must not** be introduced unless explicitly approved. Also not adopted: Rich Domain Model / DDD tactical patterns by default, event sourcing, a project-wide Result model, Minimal API endpoints, microservices. | CLAUDE.md § Decisions, STD backend/architecture | STD backend/architecture, STD backend/error-handling, WF code-review, WF project-structure, ENF check-manifests |
| DEC-WEB-02 | NgRx, Axios, Lodash, Bootstrap, Tailwind and additional form, component or state-management libraries **must not** be added by default; use built-in Angular capabilities first and add extras only for a concrete need. | STD frontend/angular | STD frontend/angular, KNW angular, ENF check-manifests |

## Conditional

| ID | Decision | Details in | Affects |
|---|---|---|---|
| DEC-MAP-01 | **Default:** manual mapping for simple cases; Mapster (+ `Mapster.DependencyInjection`) when mapping volume warrants it. | WF add-dependency | WF add-dependency, WF project-structure |
| DEC-RES-01 | **Default:** `Microsoft.Extensions.Http.Resilience` (HttpClient) and `Microsoft.Extensions.Resilience` (other pipelines) only when a real integration needs resilience. | STD backend/outbound-http, WF add-dependency | STD backend/outbound-http, KNW httpclient-factory, WF add-dependency, ENF check-manifests |
| DEC-VER-01 | API versioning is not adopted until a concrete compatibility need is approved; then `Asp.Versioning` with its Controller integration. | STD backend/api, WF add-dependency | STD backend/api, KNW api-versioning, KNW swagger, WF add-dependency |
| DEC-WEB-03 | **Default:** Playwright is the frontend E2E tool when E2E coverage is required; not part of the minimal scaffold. | KNW angular | KNW angular, WF project-structure |
| DEC-OPS-01 | Docker is optional: **do not** introduce it merely because the application can be containerized; add container artifacts only when the project or deployment needs them. | WF delivery-pipeline | KNW docker, KNW ci-cd, WF delivery-pipeline, STD backend/operations |
