> Owner: private reference of the `project-structure` workflow — repository-level layout examples | Scope: common | Loads: read by `project-structure` only | Enforced: none

# Solution Layout

Target repository shape for a new solution. The layout decision itself is in
`CLAUDE.md` § Architecture Decisions and the stack in
`docs/technology-stack.md`; this file shows where things go.

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
│   ├── technology-stack.md
│   └── decisions/            # created with the first recorded decision
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

This is a target, not a checklist: create optional directories and projects only
when the project needs them (`.claude/rules/repository-structure.md`).

## Source Projects

All backend .NET projects, including backend test projects, live under
`backend/`. The normal Clean Architecture projects are `ProjectName.Domain`,
`ProjectName.Application`, `ProjectName.Infrastructure`, and `ProjectName.Api`;
their internals are in `references/backend-layout.md`.

## Frontend

The Angular application lives outside the .NET `backend` tree, in
`frontend/ProjectName.Web/`. The workspace owns its own `package.json`,
`package-lock.json`, `angular.json`, tsconfig files, `src/`, and `public/`.
Follow the structure the current Angular CLI generates rather than an obsolete
manual layout; feature organization inside `src/app/` is described in the
`angular` skill.

## Tests

Backend .NET test projects sit beside the production projects:

```text
ProjectName.Domain.Tests        optional; non-trivial behavior that genuinely belongs to Domain
ProjectName.Application.Tests   application-service and use-case behavior
ProjectName.IntegrationTests    API + Application + Infrastructure through WebApplicationFactory<Program>
ProjectName.Infrastructure.Tests optional; focused infrastructure behavior
```

Angular unit and component tests stay inside the Angular workspace, normally
colocated with the code they test; E2E tests, when introduced, live in
`frontend/ProjectName.Web/e2e/`. Angular tests do not go under `backend/`.

## Documentation

Use `docs/` for maintained project documentation. Possible subdirectories are
`architecture/`, `decisions/`, and `api/`; create one only when its documentation
exists.

## Shared Build Files

- `Directory.Build.props` — shared .NET settings such as `TargetFramework`,
  `Nullable`, `ImplicitUsings`, and analysis or compiler settings. Keep
  project-specific settings out of it.
- `Directory.Packages.props` — NuGet Central Package Management; all package
  versions in one place.
- `global.json` — pins the intended stable SDK line; allow normal patch and
  feature-band servicing through the chosen `rollForward` policy.
- `.editorconfig` — deterministic formatting and code-style configuration;
  prefer enforceable tooling configuration over restating mechanical formatting
  in instructions.

## Optional Infrastructure

Docker files, deployment manifests, Kubernetes, cloud infrastructure, messaging,
and additional services are introduced only when a concrete requirement exists
(`docs/technology-stack.md` § Conditional Technologies; new infrastructure
categories are Reserved).
