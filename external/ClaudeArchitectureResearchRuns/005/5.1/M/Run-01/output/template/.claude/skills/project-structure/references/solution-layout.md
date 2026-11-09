> Owns: illustrative repository tree and repository-file examples for scaffolding | Scope: common | Loads: private reference of project-structure (read on demand by that workflow only)

# Solution Layout — Examples

Layout policy: `docs/technology-stack.md` (Repository Layout). This file shows
the target shape; it is not a requirement to create every entry.

## Target Tree

```text
<Name>/
├── backend/
│   ├── <Name>.Domain/
│   ├── <Name>.Application/
│   ├── <Name>.Application.Tests/
│   ├── <Name>.Infrastructure/
│   ├── <Name>.Api/
│   └── <Name>.IntegrationTests/
├── frontend/
│   └── <Name>.Web/
├── docs/
├── .claude/
├── CLAUDE.md
├── SPECIFICATION.md
├── CUSTOM_SETTINGS.md
├── <Name>.slnx
├── Directory.Build.props
├── Directory.Packages.props
├── global.json
├── .editorconfig
├── .gitignore
└── README.md
```

## Frontend Workspace

The Angular workspace owns its own `package.json`, `package-lock.json`,
`angular.json`, `tsconfig*.json`, `src/`, and `public/`. Use the structure the
current Angular CLI generates rather than an obsolete layout. Angular tests stay
inside the workspace, never under `backend/`.

## Backend Test Intent

| Project | Purpose |
|---|---|
| `<Name>.Domain.Tests` (optional) | Non-trivial behavior that genuinely belongs to Domain |
| `<Name>.Application.Tests` | Application-service / use-case behavior |
| `<Name>.IntegrationTests` | Api + Application + Infrastructure through `WebApplicationFactory<Program>` |
| `<Name>.Infrastructure.Tests` (optional) | Focused Infrastructure behavior when separation helps |

## Documentation

`docs/` may later contain `architecture/`, `decisions/`, or `api/` — create each
only when its documentation exists.

## Shared Build Files

- `Directory.Build.props`: `TargetFramework`, `Nullable`, `ImplicitUsings`,
  analysis/compiler settings shared by all projects.
- `Directory.Packages.props`: central `PackageVersion` entries.
- `global.json`: pins the intended SDK line, for example:

```json
{
  "sdk": {
    "version": "<current stable 10.0 SDK>",
    "rollForward": "latestFeature"
  }
}
```

## `.gitignore` Entries

`bin/`, `obj/`, `.vs/`, `node_modules/`, `dist/`, `TestResults/`, `coverage/`,
and local secret/config overrides. Do not ignore files that are part of the
Development configuration contract (such as `appsettings.Development.json`).

## Local SQL Server Configuration Example

A suitable Windows Development default (adapt the database name; no credentials):

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\MSSQLLocalDB;Database=<Name>;Trusted_Connection=True;TrustServerCertificate=True;"
  }
}
```

When local SQL Server needs credentials, keep this structure and supply the
secret through `dotnet user-secrets`.

## Optional Infrastructure

Docker files, deployment manifests, Kubernetes, cloud infrastructure, messaging,
and additional services are added only for a concrete requirement (several are
Reserved).
