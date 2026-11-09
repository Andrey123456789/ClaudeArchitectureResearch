> Private reference of the project-structure workflow. Owns: repository-level layout examples and shared-file guidance · Scope: common · Loads: read by project-structure when creating or reorganizing the repository · Depends on: .claude/skills/project-structure/SKILL.md

# Solution Layout

Layout decisions (top-level separation, `.slnx`, shared build files, no
top-level `tests/`): `docs/technology-stack.md` (Solution Layout). Structure
proportionality: `.claude/rules/repository-layout.md`.

## Target Top-Level Layout

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

This is a target, not a checklist: create optional directories or projects
only when they are needed.

## Backend

All backend .NET projects, including backend test projects, live under
`backend/`. Typical test-project intent:

```text
Domain.Tests        optional; non-trivial behavior that genuinely belongs to Domain
Application.Tests   application-service / use-case behavior
IntegrationTests    Api + Application + Infrastructure integration
```

Integration tests may reference the Api project for
`WebApplicationFactory<Program>`. Backend project detail: `backend-layout.md`.

## Frontend

The Angular application lives outside the .NET tree in
`frontend/ProjectName.Web/` and owns its own `package.json`,
`package-lock.json`, `angular.json`, tsconfig files, `src/`, and `public/`. Do
not impose an obsolete Angular directory structure when the current Angular CLI
generates a different supported one.

Angular tests stay inside the Angular workspace, typically colocated with the
code they test; E2E tests, when introduced, go to a folder such as
`frontend/ProjectName.Web/e2e/` (test locations: `docs/technology-stack.md`,
Testing).

## Documentation

`docs/` holds maintained project documentation. Possible subdirectories include
`architecture/`, `decisions/` (decision records written by the
`architecture-decision` workflow), and `api/` — each created only when the
corresponding documentation exists.

## Shared .NET Build Configuration

- `Directory.Build.props` — shared settings such as `TargetFramework`,
  `Nullable`, `ImplicitUsings`, and analysis/compiler settings. Genuinely
  project-specific settings stay in their projects.
- `Directory.Packages.props` — Central Package Management; versions are kept in
  one place (`.claude/rules/dependencies.md`).
- `global.json` — pins the repository to the intended stable SDK line; select
  the current stable SDK for the target .NET release (no RC/preview SDK unless
  explicitly requested) and allow normal patch/feature-band servicing according
  to the chosen `rollForward` policy.

## `.editorconfig`

Keep deterministic repository-wide formatting and code-style configuration
here; prefer enforceable tooling configuration over restating mechanical
formatting rules in instructions.

## `.gitignore`

Ignore normal generated and local artifacts where applicable:

```text
bin/
obj/
.vs/
node_modules/
dist/
TestResults/
coverage/
local secret/config overrides
```

Do not ignore files that are intentionally part of the Development
configuration contract.

## Optional Infrastructure

Docker files, deployment manifests, Kubernetes, cloud infrastructure, messaging
infrastructure, and additional services are introduced only for a concrete
requirement (`docs/technology-stack.md`, Conditional Technologies; CLAUDE.md,
Decision Control).
