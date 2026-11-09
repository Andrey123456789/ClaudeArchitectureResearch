> Level: 3 Project · Owns: repository layout technique (private reference of `project-structure`) · Scope: common · Loads: read by `project-structure` only

# Solution Layout

Target repository shape. It is a target, not a checklist: create only what the current scope needs (`code-organization.md`).

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

## Backend

All backend .NET projects, including backend test projects, live under `backend/`. The standard production projects are `<Name>.Domain`, `<Name>.Application`, `<Name>.Infrastructure` and `<Name>.Api`; internal layout is in `backend-layout.md`.

## Frontend

The Angular application lives outside the .NET tree in `frontend/<Name>.Web/`. The workspace owns its own `package.json`, `package-lock.json`, `angular.json`, tsconfig files, `src/` and `public/`. Accept the structure the current Angular CLI generates.

## Tests

| Project | Intent |
|---|---|
| `<Name>.Domain.Tests` | optional — non-trivial behavior that genuinely belongs to Domain |
| `<Name>.Application.Tests` | application-service and use-case behavior |
| `<Name>.IntegrationTests` | Api + Application + Infrastructure through the HTTP host (`WebApplicationFactory<Program>`) |
| `<Name>.Infrastructure.Tests` | optional — non-trivial Infrastructure behavior that benefits from its own assembly |

Angular unit and component tests stay inside the workspace, usually colocated with the code under test. Frontend E2E tests, when adopted, stay in the workspace too (for example `frontend/<Name>.Web/e2e/`). Never place Angular tests under `backend/`.

## Documentation

`docs/` holds maintained documentation; possible subdirectories are `architecture/`, `decisions/` and `api/`, created only when such documentation exists.

## Shared .NET build configuration

- `Directory.Build.props` — genuinely shared settings: `TargetFramework`, `Nullable`, `ImplicitUsings`, analyzer and code-style settings. Project-specific settings stay in the project file.
- `Directory.Packages.props` — Central Package Management; versions in one place.
- `global.json` — pins the intended SDK line: select the current stable SDK of the target .NET release (never RC/preview unless requested) and allow servicing through the chosen `rollForward` policy.
- `.editorconfig` — deterministic formatting and code-style configuration; prefer enforceable tooling configuration over restating mechanical formatting in instructions.

## Ignore patterns

Ignore generated and local artifacts: `bin/`, `obj/`, `.vs/`, `node_modules/`, `dist/`, `.angular/`, `TestResults/`, `coverage/`, and local secret or configuration overrides. Do not ignore files that are intentionally part of the Development configuration contract (for example a credential-free `appsettings.Development.json`).

## Optional infrastructure

Docker files, deployment manifests, Kubernetes, cloud infrastructure, messaging and additional services are created only for a concrete requirement (project decisions; Reserved categories in decision control).
