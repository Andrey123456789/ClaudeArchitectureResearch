> Always-loaded decision record (imported by `CLAUDE.md`) · Owns the approved technology stack and conditional technologies outside the four capability slots · Slot technologies: `docs/capability-selection.md` and `docs/capabilities/`

# Technology Stack

Approved technologies are Decided. When the project has an approved technology,
use it rather than silently selecting an alternative; replacing an approved
technology is Reserved (`CLAUDE.md` § Decision Control).

"Approved" does not mean "install by default": baseline packages support
capabilities the project actually has, and conditional technologies are added
only when their capability becomes necessary. This record holds no package
versions; versions are resolved at install time through `add-dependency`.

## Backend Platform

- .NET 10 LTS (latest stable servicing release of the line), C# 14, ASP.NET
  Core, and ASP.NET Core Controllers. Do not move to a preview/RC .NET or C#
  release without approval.
- Solution format: `.slnx` by default; use the legacy `.sln` format only when an
  external tool or project requirement requires it.
- Shared build configuration: repository-level `Directory.Build.props` for
  genuinely shared .NET settings (target framework, nullable, implicit usings,
  analysis/compiler settings) and `Directory.Packages.props` for NuGet Central
  Package Management; project-specific settings stay in their owning projects.
  `global.json` pins the stable SDK line.

## Validation and Logging

- FluentValidation (`FluentValidation`,
  `FluentValidation.DependencyInjectionExtensions`) is the standard library for
  explicit request and use-case validation.
- Application logging uses `ILogger<T>` with Serilog as the provider
  (`Serilog.AspNetCore`). Add sinks only when required; a Console sink is enough
  for a local baseline.

## API Documentation

- Swagger UI through `Swashbuckle.AspNetCore` is the default interactive API
  documentation and manual-testing surface in Development (`/swagger`); expose
  it outside Development only when deployment requirements justify it.
- Built-in `AddOpenApi()` / `MapOpenApi()` is not the template default when the
  requirement is interactive Swagger testing.

## Conditional Technologies

| Technology | Add only when |
|---|---|
| Mapster, Mapster.DependencyInjection | mapping volume becomes repetitive or non-trivial; manual mapping is fine for simple cases; keep mapping-library concerns out of Domain; no other mapping framework without approval |
| Microsoft.Extensions.Http.Resilience | a real outbound HTTP integration needs resilience behavior |
| Microsoft.Extensions.Resilience | a real non-HTTP resilience pipeline is needed |
| Docker and container artifacts | the project or its deployment actually needs containers; never merely because the application can be containerized |

Conditional technologies of the capability slots are recorded in
`docs/capabilities/`.
