<!-- Kind: WF | Scope: common | Owns: repository layout reference (private to project-structure) | Loads: read by project-structure -->
# Solution Layout

Default physical repository layout used by `project-structure`. Layout decision: DEC-LAYOUT-01; build files: DEC-BUILD-01.

# Top-Level Layout

```text
ProjectName/
├── backend/
│   ├── ProjectName.Domain/
│   ├── ProjectName.Application/
│   ├── ProjectName.Application.Tests/
│   ├── ProjectName.Infrastructure/
│   ├── ProjectName.Api/
│   └── ProjectName.IntegrationTests/
│
├── frontend/
│   └── ProjectName.Web/
│
├── docs/
│
├── .claude/
│
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

This is a target structure; do not create optional directories or projects merely to match the diagram. The solution file uses the `.slnx` format (DEC-BUILD-01).

# Source Projects

All backend .NET projects, including backend test projects, live under `backend/`. The normal Clean Architecture projects are `ProjectName.Domain`, `ProjectName.Application`, `ProjectName.Infrastructure` and `ProjectName.Api`; their internal layout is in `backend-layout.md`.

# Frontend

The Angular application lives outside the .NET `backend` tree at `frontend/ProjectName.Web/`. The workspace owns its own `package.json`, `package-lock.json`, `angular.json`, tsconfig files, `src/` and `public/`. Do not impose an obsolete Angular directory structure when the current Angular CLI generates a different supported structure.

# Tests

## Backend Tests

Backend test projects live beside production projects under `backend/` (DEC-LAYOUT-01):

    Domain.Tests        optional; non-trivial domain behavior that genuinely belongs to Domain
    Application.Tests   application-service/use-case behavior
    IntegrationTests    API + Application + Infrastructure integration

`ProjectName.Infrastructure.Tests` or another focused project only when it provides useful separation. Integration tests may reference the Api project for `WebApplicationFactory<Program>`.

## Frontend Tests

Angular unit and component tests stay inside `frontend/ProjectName.Web/`, normally colocated with the source they test; E2E tests, when introduced, also stay in the workspace (for example `frontend/ProjectName.Web/e2e/`). Angular tests never go under `backend/`.

# Documentation

`docs/` holds maintained project documentation; possible directories include `architecture/` (the decision register lives here), `decisions/` (ADRs) and `api/`. Create them only when the corresponding documentation exists.

# Shared .NET Build Configuration

## `Directory.Build.props`

Shared .NET project settings such as `TargetFramework`, `Nullable`, `ImplicitUsings` and analysis/compiler settings. Project-specific settings stay in their projects.

## `Directory.Packages.props`

NuGet Central Package Management: package versions in one place (`rules/common/dependencies.md` § NuGet). Approved technologies: decision register; version, security and license checks: `add-dependency`.

## `global.json`

Pin the repository to the intended supported .NET SDK line: the current stable SDK for the target release (no RC/preview unless explicitly requested), with normal patch/feature-band servicing allowed through the chosen `rollForward` policy.

# `.editorconfig`

Deterministic repository-wide formatting and code-style configuration. Prefer enforceable tooling configuration over restating mechanical formatting rules in instructions.

# Git Ignore

Ignore generated and local artifacts where applicable: `bin/`, `obj/`, `.vs/`, `node_modules/`, `dist/`, `TestResults/`, `coverage/`, local secret/config overrides. Do not ignore files that are intentionally part of the Development configuration contract.

# Optional Infrastructure

Docker files, deployment manifests, Kubernetes, cloud infrastructure, messaging infrastructure and additional services are introduced only when a concrete requirement exists (DEC-OPS-01, CLAUDE.md § Decisions).
