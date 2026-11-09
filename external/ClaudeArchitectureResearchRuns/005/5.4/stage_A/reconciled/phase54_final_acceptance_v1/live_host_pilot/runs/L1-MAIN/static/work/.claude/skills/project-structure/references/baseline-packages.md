> Level: 3-project · Owns: baseline non-slot package list and Development configuration technique (private reference of `project-structure`) · Loading: read by `project-structure`

# Baseline Packages

Approved technologies are decided in the decisions file; this list maps them to packages. Resolve every version at install time through `add-dependency`. Slot packages come from the module command facets (`persistence.commands`, `backend-testing.commands`, `frontend.commands`).

| Capability | Package(s) | Project | When |
| --- | --- | --- | --- |
| Validation | `FluentValidation`, `FluentValidation.DependencyInjectionExtensions` | use-case project | baseline when validation is needed |
| Logging provider | `Serilog.AspNetCore` (+ sinks only when required; Console is enough locally) | entry-point project | baseline |
| Interactive API docs | `Swashbuckle.AspNetCore` | entry-point project | baseline |
| Host integration tests | `Microsoft.AspNetCore.Mvc.Testing` | integration-test project | with the first integration test |
| Mapping | `Mapster`, `Mapster.DependencyInjection` | where mapping lives | only when mapping volume warrants it |
| Outbound HTTP resilience | `Microsoft.Extensions.Http.Resilience` | implementation project | only when a real integration needs it |
| Non-HTTP resilience | `Microsoft.Extensions.Resilience` | implementation project | only when such a pipeline is needed |
| API versioning | `Asp.Versioning.Mvc`, `Asp.Versioning.Mvc.ApiExplorer` | entry-point project | only after versioning is adopted |

Do not use deprecated or legacy ASP.NET automatic-validation integration packages, `Microsoft.Extensions.Http.Polly`, or `Polly.Extensions.Http`. Do not make the built-in `AddOpenApi()`/`MapOpenApi()` endpoint the template default when the requirement is interactive Swagger UI testing.

## Development configuration

The entry-point project carries `appsettings.json` and `appsettings.Development.json`. The local database connection default follows the persistence dev-config rule; real usernames, passwords, tokens, production hosts, and production connection strings are never committed. Configure the launch profile so a Development run can open `/swagger` directly when that helps, keeping HTTP/HTTPS URLs consistent with the profile.
