---
paths:
  - "**/*"
---

> Level: 3-project · Owns: approved stack, conditional technologies, layout defaults, capability selection record (designated decision summary) · Scope: common · Loading: always (imported by CLAUDE.md)

# Project Decisions

When an approved technology exists here, use it rather than silently selecting an alternative; replacing it is Reserved (CLAUDE.md decision control; record with `architecture-decision`).

## Backend stack

- Decided: .NET 10 LTS (latest stable servicing release), C# 14, ASP.NET Core, ASP.NET Core Controllers. Moving to a preview/RC .NET or C# release requires approval.
- Decided: FluentValidation is the standard explicit request/use-case validation library; application logging uses `ILogger<T>` with Serilog as the provider.
- Decided: Swashbuckle Swagger UI is the interactive API documentation and manual-testing surface for Development (`/swagger`); expose it outside Development only when deployment requirements explicitly justify it.
- Default: manual mapping for simple cases; Mapster is approved when mapping volume warrants it; Microsoft resilience packages are approved only when a real integration needs resilience.
- Default: `.slnx` solution format; legacy `.sln` only when an external tool or project requirement needs it.
- Default: repository-level `Directory.Build.props` for genuinely shared .NET build settings and `Directory.Packages.props` for Central Package Management; project-specific settings stay in their own projects.

## Layout and optional infrastructure

- Default: keep backend production and test projects (`backend/<Name>.<Layer>/`), the frontend workspace (`frontend/<Name>.Web/`), and documentation (`docs/`) clearly separated as approved; never create a separate top-level tests directory.
- Do not introduce Docker merely because the application can be containerized; add container artifacts only when the project or deployment needs them.

## Capability selection

Static composition: each required slot has exactly one selected implementation, the optional slot zero or one; only selected modules ship.

| Slot | Requirement | Selected | Knowledge skill | Declared properties |
| --- | --- | --- | --- | --- |
| architecture | required frame | clean-architecture | — | role mapping: imported adopted-architecture rule |
| persistence | required | ef-core | `ef-core` | Decided: EF Core with Microsoft SQL Server (`Microsoft.EntityFrameworkCore.SqlServer`); provider-specific concerns stay out of the use-case layer and domain model. Provider variant: sqlserver. Default string comparison: database default collation (typically case-insensitive) — relying on it for observable behavior needs approval. Migrations: EF Core migrations. Seeding: Development-only seeder. |
| backend-testing | required | nunit | `dotnet-testing` | Decided: NUnit; backend test projects live under `backend/` beside production projects; `WebApplicationFactory<Program>` is the integration-test baseline; Testcontainers is conditional. |
| frontend | optional | angular | `angular` | Decided stack: imported frontend stack rule. |

Facet resolution: module rule facets live in `.claude/rules/` and load by import or path. A workflow-read facet `<slot>.<facet>` (`layout`, `check`, `workflow`, `commands`, `enforcement`) resolves to `.claude/capabilities/<slot>/<selected>/<facet>.md` (`.json` for `check` and `enforcement` data); a slot's knowledge skill is the one named in its row. A cleared optional slot (`none`) means its facets do not apply.
