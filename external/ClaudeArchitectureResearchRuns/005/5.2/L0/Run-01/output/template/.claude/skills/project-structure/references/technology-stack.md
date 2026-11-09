> Level: 3 Project | Owns: baseline package and CLI scaffolding details (private to `project-structure`) | Scope: common | Loads: on demand by `project-structure` | Depends on: 3-project/decisions.md, 3-project/data-lifecycle.md

# Technology Stack — Scaffolding Details

The approved stack is decided in `.claude/rules/3-project/decisions.md`. This
reference lists the packages and options used to scaffold it. Resolve every
version at install time through `add-dependency`; never copy versions from
examples.

## Baseline Packages by Capability

| Capability | Project | Packages |
|---|---|---|
| Persistence | Infrastructure | `Microsoft.EntityFrameworkCore.SqlServer` (+ `Microsoft.EntityFrameworkCore.Design` in the startup project for migrations tooling) |
| Validation | Application | `FluentValidation`, `FluentValidation.DependencyInjectionExtensions` |
| Logging | Api | `Serilog.AspNetCore` (Console sink for a simple local baseline) |
| API documentation | Api | `Swashbuckle.AspNetCore` |
| Unit tests | test projects | NUnit, NUnit test adapter, `Microsoft.NET.Test.Sdk` |
| Integration tests | IntegrationTests | `Microsoft.AspNetCore.Mvc.Testing` |

Add a package only when its capability exists in the initial project.

## Conditional Packages

| Trigger | Packages |
|---|---|
| Meaningful mapping volume | `Mapster`, `Mapster.DependencyInjection` |
| Outbound HTTP needs resilience | `Microsoft.Extensions.Http.Resilience` |
| Non-HTTP resilience pipeline | `Microsoft.Extensions.Resilience` |
| Isolated real-provider tests | Testcontainers |
| Required frontend E2E | Playwright |
| Approved API versioning | `Asp.Versioning.Mvc`, `Asp.Versioning.Mvc.ApiExplorer` |

## Development Database

`appsettings.Development.json` shape (adapt the database name):

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\MSSQLLocalDB;Database=<Name>;Trusted_Connection=True;TrustServerCertificate=True;"
  }
}
```

When local SQL Server needs credentials, keep the non-secret structure in
configuration and set the secret with `dotnet user-secrets`.

## Swagger in Development

Configure Swagger generation and UI so a Development run exposes `/swagger`;
set `launchBrowser: true` and `launchUrl: "swagger"` in the launch profile when
helpful, with URLs that match the profile's actual HTTP/HTTPS ports. Do not use
the built-in `AddOpenApi()`/`MapOpenApi()` as the interactive default.

## Angular Workspace

Create the workspace with the current Angular CLI on a supported Node.js
version, e.g. `ng new <Name>.Web --directory frontend/<Name>.Web --routing
--style=scss --strict` (zoneless when the selected stable version supports it),
then `ng add @angular/material`. Let the CLI choose compatible Angular,
TypeScript, and RxJS versions; do not upgrade TypeScript beyond Angular's
supported range. Vitest is the unit-test runner for new workspaces.
