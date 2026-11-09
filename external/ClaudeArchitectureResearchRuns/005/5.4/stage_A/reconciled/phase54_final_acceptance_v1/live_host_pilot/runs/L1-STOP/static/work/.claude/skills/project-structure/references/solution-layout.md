> Level: 3-project · Owns: repository-level layout technique (private reference of `project-structure`) · Loading: read by `project-structure`

# Solution Layout

Target repository shape. Create optional directories and projects only when needed; backend project names and internals come from `architecture.layout`.

```text
<Name>/
├── backend/                 # every .NET project, including backend test projects
│   └── <Name>.<Layer>/
├── frontend/
│   └── <Name>.Web/          # frontend workspace: package.json, package-lock.json, framework config, src/, public/
├── docs/                    # maintained documentation only (architecture/, decisions/, api/ when content exists)
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

## Frontend workspace

The frontend workspace owns its manifest, lockfile, framework configuration, and sources. Do not impose an obsolete directory structure when the current CLI generates a different supported one. Frontend tests stay inside the workspace (colocated unit/component tests; E2E under `e2e/` when used) — never under `backend/`.

## Shared .NET configuration

- `Directory.Build.props` — genuinely shared settings: `TargetFramework`, `Nullable`, `ImplicitUsings`, analysis/compiler settings. Project-specific settings stay in their projects.
- `Directory.Packages.props` — Central Package Management; versions in one place (approved technologies: decisions file; version, security, and license procedure: `add-dependency`).
- `global.json` — pin the intended SDK line: the current stable SDK of the target .NET release (no RC/preview unless explicitly requested), with a `rollForward` policy that allows normal patch/feature-band servicing.
- `.editorconfig` — deterministic formatting and code-style configuration; prefer enforceable tooling configuration over restating mechanical formatting rules in instructions.

## Git ignore

Ignore generated and local artifacts: `bin/`, `obj/`, `.vs/`, `node_modules/`, `dist/`, `TestResults/`, `coverage/`, local secret/config overrides. Do not ignore files that are intentionally part of the Development configuration contract.

## Optional infrastructure

Docker files, deployment manifests, Kubernetes, cloud infrastructure, messaging infrastructure, and additional services appear only when a concrete requirement exists.
