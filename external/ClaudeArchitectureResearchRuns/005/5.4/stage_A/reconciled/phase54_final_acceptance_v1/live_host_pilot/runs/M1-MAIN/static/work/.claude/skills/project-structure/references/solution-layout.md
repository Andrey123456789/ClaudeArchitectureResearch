> Private reference of `project-structure` · Repository-level layout technique · Layout decision: `docs/capabilities/architecture.md` § Repository Layout

# Solution Layout

## Top-Level Layout

```text
ProjectName/
├── backend/                 # <Name>.<Layer> projects and backend test projects (backend-layout.md)
├── frontend/
│   └── ProjectName.Web/     # when the frontend slot is selected
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

This is a target structure, not a requirement to create every optional
directory or project immediately. Use the `.slnx` solution format (see the
technology stack for the `.sln` exception).

## Source Projects

All backend .NET projects, including backend test projects, live under
`backend/`. The project list and internal layout are in `backend-layout.md`.

## Frontend

The frontend workspace lives outside the .NET `backend` tree, under
`frontend/ProjectName.Web/`, and owns its own `package.json`,
`package-lock.json`, framework configuration, and source tree. Do not impose an
obsolete directory structure when the current framework CLI generates a
different supported structure; workspace setup is in the frontend skill
§ Scaffolding.

## Tests

- Backend tests: beside the production projects under `backend/` (see
  `backend-layout.md`).
- Frontend unit and component tests: inside the frontend workspace, typically
  colocated with the code they test according to current framework conventions.
- Frontend E2E tests, when introduced: inside the frontend workspace, for
  example `frontend/ProjectName.Web/e2e/`.

Do not place frontend tests under `backend/`.

## Documentation

Use `docs/` for maintained project documentation. Possible subdirectories are
`architecture/`, `decisions/` (ADRs), and `api/`; create them only when
corresponding documentation exists.

## Shared .NET Build Configuration

- `Directory.Build.props` — shared settings such as `TargetFramework`,
  `Nullable`, `ImplicitUsings`, analysis/compiler settings; no genuinely
  project-specific settings. Remove properties that `dotnet new` duplicates in
  project files.
- `Directory.Packages.props` — NuGet Central Package Management; versions in one
  place (`.claude/rules/dependencies.md`).
- `global.json` — pin the intended stable SDK line; when scaffolding, select the
  current stable SDK for the target .NET release (no RC/preview SDK unless
  explicitly requested) and allow normal servicing through the chosen
  `rollForward` policy.

## `.editorconfig`

Keep deterministic repository-wide formatting and code-style configuration in
`.editorconfig`; prefer enforceable tooling configuration over restating
mechanical formatting rules in instructions.

## Git Ignore

Ignore generated and local artifacts where applicable: `bin/`, `obj/`, `.vs/`,
`node_modules/`, `dist/`, `TestResults/`, `coverage/`, and local secret or
config overrides. Do not ignore files that are intentionally part of the
Development configuration contract.

## Optional Infrastructure

Examples that stay out of a new repository until a concrete requirement exists
(`.claude/rules/physical-structure.md`, `docs/technology-stack.md`): Docker
files, deployment manifests, Kubernetes resources, cloud infrastructure,
messaging infrastructure, additional services.
