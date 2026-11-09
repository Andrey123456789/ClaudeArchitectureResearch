> Level: 3 Project | Owns: repository layout examples for scaffolding (private to `project-structure`) | Scope: common | Loads: on demand by `project-structure` | Depends on: 3-project/decisions.md

# Solution Layout

Target structure; create optional directories and projects only when needed.

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

All backend .NET projects, including test projects, live under `backend/`.
Typical test intent:

- `<Name>.Domain.Tests` — optional; non-trivial behavior that genuinely belongs
  to Domain.
- `<Name>.Application.Tests` — Application Service and use-case behavior.
- `<Name>.IntegrationTests` — Api + Application + Infrastructure through
  `WebApplicationFactory<Program>` (references the Api project).

Detailed backend layout: `backend-layout.md`.

## Frontend

The Angular workspace lives outside `backend/` in `frontend/<Name>.Web/` and
owns its `package.json`, `package-lock.json`, `angular.json`, tsconfig files,
`src/`, and `public/`. Do not impose an obsolete Angular directory structure
when the current CLI generates a different supported one. Angular tests stay in
the workspace (unit/component tests colocated; E2E under `e2e/` when used),
never under `backend/`.

## Documentation

`docs/` holds maintained project documentation; `architecture/`, `decisions/`,
or `api/` subdirectories are created only when such documents exist.

## Shared .NET Build Files

- `Directory.Build.props` — genuinely shared settings: `TargetFramework`,
  `Nullable`, `ImplicitUsings`, analysis/compiler settings.
- `Directory.Packages.props` — Central Package Management versions.
- `global.json` — pins the supported SDK line; pick the current stable SDK of
  the target .NET release (no RC/preview unless requested) and allow normal
  servicing through the chosen `rollForward` policy.

## Repository Files

- `.editorconfig` — deterministic formatting and style configuration; prefer
  enforceable tooling over duplicating mechanical formatting in instructions.
- `.gitignore` — `bin/`, `obj/`, `.vs/`, `node_modules/`, `dist/`,
  `TestResults/`, `coverage/`, local secret/config overrides, and the hook
  state directory; do not ignore files that belong to the Development
  configuration contract.

## Optional Infrastructure

Docker files, deployment manifests, Kubernetes, cloud infrastructure,
messaging, and additional services are added only for a concrete requirement.
