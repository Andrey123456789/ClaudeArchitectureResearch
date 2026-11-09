> Level: 3 Project · Owns: repository-level layout examples and shared-file guidance for `project-structure` (private reference) · Scope: common · Loads: read by `project-structure` only · Depends on: .claude/skills/project-structure/SKILL.md

# Solution Layout

The governing rules are `.claude/rules/3-project/decisions.md` (repository defaults) and `.claude/rules/3-project/layout.md` (project mapping). This file shows the target shape and repository-file technique.

## Target tree

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

This is a target, not a checklist: create optional directories and projects only when they are needed.

## Test intent

| Project | Intent |
|---|---|
| `<Name>.Domain.Tests` (optional) | non-trivial domain behavior that genuinely belongs to Domain |
| `<Name>.Application.Tests` | application-service/use-case behavior |
| `<Name>.IntegrationTests` | Api + Application + Infrastructure through the real host |

Frontend test and workspace placement: `.claude/rules/3-project/layout.md` → Frontend.

## Documentation

`docs/` holds maintained project documentation; subdirectories such as `architecture/`, `decisions/`, `api/` are created only when the corresponding documents exist.

## Shared .NET build configuration

- `Directory.Build.props` — typical shared settings: `TargetFramework`, `Nullable`, `ImplicitUsings`, analysis/compiler settings (policy: `.claude/rules/3-project/decisions.md` → Repository defaults).
- `Directory.Packages.props` — central package versions (policy: `.claude/rules/3-project/package-management.md`).
- `global.json` — pins the intended SDK line, for example:

```json
{
  "sdk": {
    "version": "10.0.100",
    "rollForward": "latestFeature"
  }
}
```

Select the current stable SDK of the target release at scaffolding time (the version above is illustrative; preview/RC lines: `.claude/rules/3-project/decisions.md`) and choose a `rollForward` policy that allows normal patch/feature-band servicing.

## `.editorconfig`

Deterministic repository-wide formatting and code-style configuration lives here; prefer enforceable tooling configuration over restating mechanical formatting in instructions.

## `.gitignore`

Ignore generated/local artifacts: `bin/`, `obj/`, `.vs/`, `node_modules/`, `dist/`, `TestResults/`, `coverage/`, local secret/config overrides, `.claude/settings.local.json`. Do not ignore files that are part of the Development configuration contract (for example a non-secret `appsettings.Development.json`).

## Optional infrastructure

Docker files, deployment manifests, Kubernetes, cloud infrastructure, messaging infrastructure, and additional services are not part of the target tree; adding one follows CLAUDE.md → Decision control and `.claude/rules/3-project/decisions.md`.
