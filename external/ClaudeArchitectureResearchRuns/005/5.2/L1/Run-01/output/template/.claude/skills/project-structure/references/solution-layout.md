> Level: 3-project | Owns: repository-level layout details used while scaffolding (skill-private reference) | Scope: common | Loads: read by project-structure only

# Solution Layout

The binding layout convention is in the project stack; this reference shows the
target shape. Do not create optional directories or projects merely to match
the diagram.

## Top-level layout

```text
<Name>/
├── backend/
│   ├── <Name>.<Layer>/            # production projects (layers: architecture.layout)
│   └── <Name>.<...>Tests/         # backend test projects beside them
├── frontend/
│   └── <Name>.Web/                # only when the frontend slot is selected
├── docs/                          # maintained documentation, when it exists
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

Placement of backend production and test projects follows the project stack
layout; individual projects and directories: `architecture.layout`.

## Frontend

The frontend workspace lives outside the .NET `backend` tree in
`frontend/<Name>.Web/` and owns its manifest, lockfile, workspace configuration,
TypeScript configuration, `src/`, and `public/` (exact files:
`frontend.scaffold`). Do not impose an obsolete directory structure when the
current CLI generates a different supported one. Frontend unit and component
tests stay inside the workspace, normally colocated with the code; E2E tests,
when used, live in `frontend/<Name>.Web/e2e/`. Never place frontend tests under
`backend/`.

## Documentation

`docs/` holds maintained project documentation; possible subdirectories are
`architecture/`, `decisions/` (ADRs from `architecture-decision`), and `api/`.
Create them only when the corresponding documentation exists.

## Shared .NET build configuration

- `Directory.Build.props` — genuinely shared settings such as
  `TargetFramework`, `Nullable`, `ImplicitUsings`, and analysis/compiler
  settings; never project-specific settings.
- `Directory.Packages.props` — Central Package Management versions in one place.
- `global.json` — pins the intended SDK line: select the current stable SDK of
  the target .NET release (no RC/preview unless explicitly requested) and allow
  normal patch/feature-band servicing through the chosen `rollForward` policy.
- `.editorconfig` — deterministic repository-wide formatting and code style;
  prefer enforceable tooling configuration over restating mechanical formatting
  rules in instructions.

## `.gitignore`

Ignore generated and local artifacts where applicable: `bin/`, `obj/`, `.vs/`,
`node_modules/`, `dist/`, `TestResults/`, `coverage/`, local secret/config
overrides. Do not ignore files that are intentionally part of the Development
configuration contract.

## Optional infrastructure

Container files, deployment manifests, Kubernetes, cloud infrastructure,
messaging infrastructure, and additional services are introduced only for a
concrete requirement.
