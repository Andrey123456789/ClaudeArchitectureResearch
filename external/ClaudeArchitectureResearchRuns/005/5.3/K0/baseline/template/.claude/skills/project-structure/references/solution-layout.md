> Kind: WF | Scope: common | Owner: repository layout reference for scaffolding (private to project-structure) | Loading: read by project-structure only

# Solution Layout

Target repository shape for scaffolding. Create optional directories and projects only when needed; do not make the repository match the diagram for its own sake.

```text
ProjectName/
├── backend/
│   ├── ProjectName.Domain/
│   ├── ProjectName.Application/
│   ├── ProjectName.Application.Tests/
│   ├── ProjectName.Infrastructure/
│   ├── ProjectName.Api/
│   └── ProjectName.IntegrationTests/
├── frontend/
│   └── ProjectName.Web/
├── docs/
├── .claude/
├── CLAUDE.md
├── SPECIFICATION.md
├── CUSTOM_SETTINGS.md
├── ProjectName.slnx
├── Directory.Build.props
├── Directory.Packages.props
├── global.json
├── .editorconfig
├── .gitignore
└── README.md
```

## Backend

All backend .NET projects, backend test projects included, live under `backend/`. Detailed backend layout: `backend-layout.md`.

Test project intent:

```text
Domain.Tests        optional; non-trivial behavior that genuinely belongs to Domain
Application.Tests   application-service / use-case behavior
IntegrationTests    API + Application + Infrastructure integration
```

Integration tests may reference the API project for `WebApplicationFactory<Program>`.

## Frontend

The Angular workspace lives outside the .NET tree, in `frontend/ProjectName.Web/`, and owns its `package.json`, `package-lock.json`, `angular.json`, tsconfig files, `src/` and `public/`. Do not impose an obsolete Angular directory structure when the current Angular CLI generates a different supported one.

Angular unit and component tests stay in the workspace, usually colocated with the code they test. E2E tests, when adopted, also stay in the workspace, for example `frontend/ProjectName.Web/e2e/`. Angular tests never go under `backend/`.

## Documentation

`docs/` holds maintained project documentation. Possible subdirectories: `architecture/` (the decision register lives in `docs/architecture/decision-register.md`), `decisions/` (ADRs), `api/`. Create them only when the corresponding documentation exists.

## Shared .NET build configuration

- `Directory.Build.props` — genuinely shared project settings: `TargetFramework`, `Nullable`, `ImplicitUsings`, analysis and compiler settings. Project-specific settings stay in their projects.
- `Directory.Packages.props` — Central Package Management; package versions in one place.
- `global.json` — pin the intended supported .NET SDK line. When scaffolding, select the current stable SDK of the target .NET release (no RC/preview SDK unless explicitly requested) and allow patch/feature-band servicing through the chosen `rollForward` policy.

## `.editorconfig`

Repository-wide formatting and code-style configuration lives here; prefer enforceable tooling configuration over restating mechanical formatting rules in instructions.

## `.gitignore`

Ignore generated and local artifacts where applicable: `bin/`, `obj/`, `.vs/`, `node_modules/`, `dist/`, `TestResults/`, `coverage/`, local secret/config overrides, `.claude/.hook-state/`. Do not ignore files that are intentionally part of the Development configuration contract.

## Optional infrastructure

Docker files, deployment manifests, Kubernetes, cloud infrastructure, messaging infrastructure and additional services are introduced only for a concrete requirement.
