> Kind: DEC | Scope: common | Capability: — (capability selection: per slot) | Loading: always (imported by CLAUDE.md)

# Decision Register

Decided project decisions available at planning time. Follow them. Changing any entry is Reserved and goes through `architecture-decision`.

## Capability selection

<!-- slot-selection:begin -->
Static composition: exactly one implementation per required slot and zero or one for the optional slot; unselected implementations are not part of the runtime. Each manifest lists its facets: `.claude/capabilities/<slot>/<implementation>/MODULE.md`.

| Slot | Selected | Knowledge facet | Declared properties |
|---|---|---|---|
| architecture (required frame) | clean-architecture | — | Backend roles Domain, Application, Infrastructure, Api as `backend/<Name>.<Layer>/`; role rules in the architecture-style standard (loads with backend files). Not adopted: CQRS handlers, MediatR, Kommand, Vertical Slice Architecture, or similar mediator-based organization; introducing any of them requires explicit approval. |
| persistence (required leaf) | ef-core, provider variant sqlserver | `ef-core` | Default persistence: EF Core with Microsoft SQL Server (`Microsoft.EntityFrameworkCore.SqlServer`); provider-specific concerns stay out of Application and Domain. Migration mechanism: EF Core migrations. Seeding mechanism: dedicated Development seeder. String comparison follows database collation (SQL Server default collations are case-insensitive); observable semantics remain a product decision. Binds: architecture. |
| backend-testing (required leaf) | nunit | `dotnet-testing` | NUnit; backend test projects beside production projects under `backend/` (layout default below); `WebApplicationFactory<Program>` is the ASP.NET Core integration-test baseline; Testcontainers is conditional. Binds: architecture. |
| frontend (optional leaf) | angular | `angular` | Current stable Angular with compatible TypeScript/RxJS, standalone APIs, strict mode, routing, zoneless mode when supported, SCSS, Angular Material/CDK, Vitest. Not added by default: NgRx, Axios, Lodash, Bootstrap, Tailwind, or additional form/component/state libraries; use built-in Angular capabilities first and add extras only for a concrete need. |
<!-- slot-selection:end -->

## Platform and approved stack

Use the approved technology below; must not silently select an alternative. Replacing approved technology requires approval.

- Backend platform: .NET 10 LTS, C# 14, ASP.NET Core, ASP.NET Core Controllers. Moving to a preview/RC release requires approval.
- Validation: FluentValidation is the standard explicit request/use-case validation library.
- Logging: application code logs through `ILogger<T>`; Serilog is the logging provider.
- API documentation: Swashbuckle Swagger UI is the default Development interactive API documentation and testing surface (not built-in `AddOpenApi()`/`MapOpenApi()`); expose it outside Development only when requirements justify it.
- Default solution format: `.slnx`; legacy `.sln` only when an external tool or project requirement needs it.
- Default shared .NET configuration: repository-level `Directory.Build.props` for genuinely shared build settings and `Directory.Packages.props` for Central Package Management; project-specific settings stay in their owning projects.

## Conditional technologies

Approved, but added only when the capability is actually needed:

- Default mapping: manual mapping for simple cases; Mapster when mapping volume warrants it.
- Resilience: Microsoft resilience packages only when a real integration needs resilience.
- Default frontend E2E: Playwright when E2E coverage is required; not part of the baseline scaffold.
- Containers: must not introduce Docker merely because the application can be containerized; add container artifacts only when the project or its deployment needs them.

## Project defaults

- Default layout: production and backend test projects in `backend/<Name>.<Layer>/`, the frontend workspace in `frontend/<Name>.Web/`, documentation in `docs/`; no separate top-level `tests/` directory.

## Accepted decisions

Recorded by `architecture-decision`; optional detailed records live in `docs/decisions/`.

| Date | Decision | Scope | Record |
|---|---|---|---|
| — | No project-specific decisions recorded yet. | — | — |
