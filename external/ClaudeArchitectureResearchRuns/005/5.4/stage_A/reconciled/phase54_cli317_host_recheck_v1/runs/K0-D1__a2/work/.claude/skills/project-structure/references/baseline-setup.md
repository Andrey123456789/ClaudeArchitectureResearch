> Kind: WF | Scope: common | Owner: baseline packages and Development configuration for new applications (private to project-structure) | Loading: read by project-structure only

# Baseline Setup

Package and technology selection comes from the decision register; install every package through `add-dependency` with the version resolved at install time.

## Backend baseline packages

Install the packages each decision names, plus the scaffold packages below, in these projects:

| Capability (decision) | Additional scaffold packages | Project |
|---|---|---|
| Persistence (D-04) | `Microsoft.EntityFrameworkCore.Design` where migrations are created | provider in Infrastructure; Api as migrations startup project |
| Validation (D-05) | — | Application |
| Logging (D-06) | Console sink for a simple local baseline | Api |
| API documentation (D-07) | — | Api |
| Tests (D-08) | `NUnit3TestAdapter`, `Microsoft.NET.Test.Sdk` | test projects |

Conditional packages (D-11 to D-15) are added only when their capability is needed. Swagger setup technique, including why the built-in OpenAPI endpoint is not the Swagger UI surface: `swagger`.

## Development database configuration

`appsettings.Development.json` with a usable, credential-free local connection string. A suitable Windows default:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\MSSQLLocalDB;Database=ProjectName;Trusted_Connection=True;TrustServerCertificate=True;"
  }
}
```

Adapt the database name. When local SQL Server needs credentials, keep the non-secret structure in configuration and supply the secret value through user-secrets or another approved local secret mechanism. Never commit usernames/passwords, tokens, production hosts or production connection strings.

Development seeding: Development only, seed when empty, representative entity states, never automatic Production seeding — implementation technique in `ef-core` § Development seeding.

## Swagger launch

Expose Swagger UI at `/swagger` in Development and set the launch profile to open it (`"launchBrowser": true`, `"launchUrl": "swagger"`), with application URLs that match the profile (technique: `swagger`).

## Angular workspace

Use the latest stable Angular release supported by the selected Node.js environment and create the workspace with the current Angular CLI so that it selects mutually compatible Angular, TypeScript and RxJS versions — do not upgrade TypeScript beyond Angular's supported range independently. Select standalone APIs, strict mode, routing, SCSS and zoneless mode when the selected stable version supports it; add Angular Material and CDK with the Angular CLI. Configure the decided unit-test runner (D-09); add E2E tooling only under D-13.
