> Owns: repository-level scaffolding layout and file conventions (technique) | Scope: common | Loads: private reference, read only by the project-structure skill

# Solution Layout

Layout policy: CLAUDE.md § Architecture Defaults and
`.claude/rules/repository-structure.md`. This reference shows the target shape
used while scaffolding.

## Top-Level Layout

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

This is a target structure; create optional directories and projects only when
they are needed.

## Source Projects

The normal Clean Architecture projects are `ProjectName.Domain`,
`ProjectName.Application`, `ProjectName.Infrastructure`, and `ProjectName.Api`.
Project contents and references: `backend-layout.md`.

## Frontend

The Angular application lives outside the .NET tree in
`frontend/ProjectName.Web/`. The workspace owns its own `package.json`,
`package-lock.json`, `angular.json`, tsconfig files, `src/`, and `public/`.

Do not impose an obsolete Angular directory structure when the current Angular
CLI generates a different supported structure. Let the CLI select mutually
compatible Angular, TypeScript, and RxJS versions, and do not upgrade TypeScript
beyond Angular's supported range merely because a newer package exists.

## Tests

### Backend tests

Typical backend test projects and their intent:

```text
ProjectName.Domain.Tests        optional; non-trivial behavior that genuinely
                                belongs to Domain
ProjectName.Application.Tests   application-service and use-case behavior
ProjectName.IntegrationTests    API + Application + Infrastructure integration
                                (references the Api project for
                                WebApplicationFactory<Program>)
ProjectName.Infrastructure.Tests optional; only when it provides useful
                                separation
```

### Frontend tests

Frontend test placement: `project-structure` step 7.

## Documentation

Use `docs/` for maintained project documentation. Possible subdirectories are
`architecture/`, `decisions/`, and `api/`; create them only when the
corresponding documentation exists.

## Shared .NET Build Configuration

- `Directory.Build.props` — shared settings such as `TargetFramework`,
  `Nullable`, `ImplicitUsings`, and analysis/compiler settings. Do not place
  genuinely project-specific settings there.
- `Directory.Packages.props` — NuGet Central Package Management; versions are
  added through `add-dependency`.
- `global.json` — pin the repository to the intended supported .NET SDK line.
  When scaffolding, select the current stable SDK for the target .NET release
  (no RC/preview unless explicitly requested) and allow normal patch or
  feature-band servicing through the chosen `rollForward` policy.

## `.editorconfig`

Deterministic repository-wide formatting and code-style configuration lives
here. Prefer enforceable tooling configuration over restating mechanical
formatting rules in instructions.

## Git Ignore

Ignore generated and local artifacts where applicable:

```text
bin/
obj/
.vs/
node_modules/
dist/
.angular/
TestResults/
coverage/
local secret/config overrides
```

Do not ignore files that are intentionally part of the Development
configuration contract, such as a non-secret `appsettings.Development.json`.

## Optional Infrastructure

Docker files, deployment manifests, Kubernetes, cloud infrastructure, messaging
infrastructure, and additional services are created only when a concrete
requirement exists (`docs/technology-stack.md`, CLAUDE.md § Decision Control).
