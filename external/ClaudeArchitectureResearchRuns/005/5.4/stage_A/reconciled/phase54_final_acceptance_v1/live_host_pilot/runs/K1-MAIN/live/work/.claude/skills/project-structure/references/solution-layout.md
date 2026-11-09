> Kind: WF | Scope: common | Capability: — | Loading: read by `project-structure` when its step says so

# Solution Layout

Default physical repository layout (decision register: Project defaults). A target structure — create optional directories or projects only when needed.

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

## Source projects

All backend .NET projects, including backend test projects, live under `backend/`; their internal layout and references: `backend-layout.md`. The solution file uses `.slnx` (decision register).

## Frontend

The frontend workspace lives outside the .NET tree in `frontend/ProjectName.Web/` and owns its `package.json`, `package-lock.json`, framework configuration, `tsconfig` files, `src/`, and `public/`. Do not impose an obsolete directory structure when the current framework CLI generates a different supported one. Frontend unit/component tests stay inside the workspace (normally colocated with the code); frontend E2E tests, when introduced, also stay inside it (e.g. `frontend/ProjectName.Web/e2e/`). Never place frontend tests under `backend/`.

## Documentation

Use `docs/` for maintained project documentation; possible subdirectories include `architecture/` (the decision register), `decisions/` (decision records), and `api/`. Create them only when the corresponding documentation exists.

## Shared .NET build configuration

- `Directory.Build.props` — genuinely shared settings such as `TargetFramework`, `Nullable`, `ImplicitUsings`, and analysis/compiler settings; never project-specific settings.
- `Directory.Packages.props` — NuGet Central Package Management; versions in one place.
- `global.json` — pin the intended supported SDK line: select the current stable SDK for the target .NET release (no RC/preview unless explicitly requested) and allow servicing according to the chosen `rollForward` policy.
- `.editorconfig` — deterministic repository-wide formatting and code-style configuration; prefer enforceable tooling configuration over restating mechanical formatting rules in instructions.

## Git ignore

Ignore normal generated/local artifacts where applicable: `bin/`, `obj/`, `.vs/`, `node_modules/`, `dist/`, `TestResults/`, `coverage/`, local secret/config overrides, and the Claude Code local settings file (`settings.local.json` in `.claude/`). Do not ignore files that are intentionally part of the Development configuration contract.

## Optional infrastructure

Docker files, deployment manifests, Kubernetes, cloud infrastructure, messaging infrastructure, and additional services are introduced only for a concrete requirement (`delivery-change`).
