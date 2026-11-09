> **Planning-time decision record** · Owns: approved technology stack, conditional technologies, solution format, shared build configuration, repository layout · Scope: common, backend, backend-tests · Loading: always (imported by `CLAUDE.md`)

# Technology Stack

These are the approved default technologies for newly scaffolded projects. The
architecture style, persistence technology and provider, backend test framework,
and frontend framework are capability selections: see `capability-selection.md`.

When the project has an approved technology, use it; do not silently select an
alternative. Replacing an approved technology requires approval (Reserved).

Resolve concrete package versions at install time through the `add-dependency`
workflow; this record intentionally contains no versions.

## Backend Platform

- .NET 10 LTS (latest stable servicing release of the 10 line), C# 14,
  ASP.NET Core, and ASP.NET Core Controllers as the HTTP endpoint model.
- Do not move to a preview/RC .NET or C# release without approval.

## Persistence

The selected persistence capability (technology and provider variant in
`capability-selection.md`) is the default persistence stack. Provider-specific
concerns stay out of Application and Domain.

## Validation and Logging

- FluentValidation (`FluentValidation`,
  `FluentValidation.DependencyInjectionExtensions`) is the standard library for
  explicit request and use-case validation. Do not add a deprecated or legacy
  ASP.NET automatic-validation integration package.
- Application logging uses `ILogger<T>` (Microsoft.Extensions.Logging
  abstractions) with Serilog as the provider (`Serilog.AspNetCore`). Add sinks
  only when required; a Console sink is sufficient for a local baseline.

## API Documentation

Swashbuckle.AspNetCore with Swagger UI at `/swagger` is the default Development
interactive API documentation and manual testing surface for the Controller API.
Do not make built-in `AddOpenApi()` / `MapOpenApi()` the default. Expose Swagger UI
outside Development only when deployment requirements explicitly justify it.

## Backend Testing

- Test framework: the selected backend-testing capability.
- Backend test projects live under `backend/` alongside the production projects.
- `Microsoft.AspNetCore.Mvc.Testing` / `WebApplicationFactory<Program>` is the
  baseline for ASP.NET Core integration tests.
- Testcontainers is conditional, not part of the baseline dependency set.

## Conditional Technologies

"Approved" does not mean "install by default"; add these only when their
capability is actually needed:

- Mapping: manual mapping is fine for simple cases; Mapster
  (`Mapster`, `Mapster.DependencyInjection`) is approved when mapping volume
  becomes repetitive or non-trivial. Do not introduce another mapping framework
  without approval, and keep mapping-library concerns out of Domain.
- Resilience: the Microsoft resilience packages are approved only when a real
  integration needs resilience behavior (package choice: `add-dependency`).
- Testcontainers: when isolated real-provider tests justify it.
- Docker: do not introduce Docker merely because the application can be
  containerized; add container artifacts only when the project or its deployment
  actually needs them.

## Solution and Build Configuration

- Use the `.slnx` solution format by default; use a legacy `.sln` only when an
  external tool or project requirement requires it.
- Use repository-level `Directory.Build.props` for genuinely shared .NET build
  settings and `Directory.Packages.props` for NuGet Central Package Management;
  keep project-specific settings in their owning projects.
- `global.json` pins the repository to the intended stable SDK line.

## Repository Layout

Keep backend production and test projects (`backend/<Name>.<Layer>/`), the
frontend workspace (`frontend/<Name>.Web/`), and documentation (`docs/`) clearly
separated according to this layout. Do not create a separate top-level `tests/`
directory. Layer and project roles are defined by the architecture frame
(`architecture.md`).
