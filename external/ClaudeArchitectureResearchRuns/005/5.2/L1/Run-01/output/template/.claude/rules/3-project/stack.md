---
paths:
  - "**/*"
---
> Level: 3-project | Owns: approved stack, conditional technologies, repository layout and build defaults | Scope: common | Loads: always (imported by CLAUDE.md)

# Project Stack and Layout

Use the approved technology below rather than silently selecting an
alternative; replacing an approved technology requires approval. "Approved" does
not mean "install by default" — add a technology when its capability is needed
(`add-dependency`). Persistence, backend testing, and frontend technology are
capability selections (see capability selection).

## Backend platform (decided)

.NET 10 LTS (latest stable servicing release), C# 14, ASP.NET Core, ASP.NET Core
Controllers. Moving to a preview/RC .NET or C# release requires approval.

## Approved baseline (decided)

- Validation: FluentValidation (with FluentValidation.DependencyInjectionExtensions)
  is the standard library for explicit request and use-case validation.
- Logging: application code logs through `ILogger<T>`; Serilog is the provider
  (Serilog.AspNetCore); add sinks only when required (Console for local runs).
- API documentation and interactive testing: Swagger UI via
  Swashbuckle.AspNetCore at `/swagger` is the Development surface; exposure
  beyond Development only when requirements justify it
  (`2-technology/backend-technologies.md`).

## Conditional technologies (approved, added only on concrete need)

- Mapping: manual mapping for simple cases; Mapster (with
  Mapster.DependencyInjection) when mapping volume warrants it. Another mapping
  framework requires approval.
- Resilience: Microsoft.Extensions.Http.Resilience / Microsoft.Extensions.Resilience
  only when a real integration needs resilience behavior.
- API versioning: Asp.Versioning Controller integration once versioning is adopted.
- Containers: Docker is optional infrastructure. Do not introduce Docker merely
  because the application can be containerized; add container artifacts only
  when the project or deployment actually needs them.

## Layout and build defaults

- Solution format: `.slnx` by default; legacy `.sln` only when an external tool
  or project requirement needs it.
- Repository-level `Directory.Build.props` holds genuinely shared .NET build
  settings and `Directory.Packages.props` holds Central Package Management
  versions; project-specific settings stay in their owning projects.
- Layout: backend production and test projects at `backend/<Name>.<Layer>/`,
  the frontend workspace at `frontend/<Name>.Web/`, maintained documentation in
  `docs/`, kept clearly separated. Do not create a separate top-level `tests/`
  directory.
