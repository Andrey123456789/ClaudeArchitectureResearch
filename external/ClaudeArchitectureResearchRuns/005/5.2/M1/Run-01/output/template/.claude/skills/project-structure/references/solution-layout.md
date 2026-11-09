> **Private reference** of `project-structure` · Owns: repository-level layout technique and examples · Scope: common · Loading: on demand (read by `project-structure`)

# Solution Layout

This reference defines the default physical repository layout.

Use it together with `architecture-style.md`. The approved layout decision lives
in `docs/technology-stack.md` → Repository Layout.

# Top-Level Layout

```text
ProjectName/
├── backend/
│   ├── ProjectName.<Layer>/            architecture frame projects (backend-layout.md)
│   ├── ProjectName.<Layer>.Tests/
│   └── ProjectName.IntegrationTests/
│
├── frontend/
│   └── ProjectName.Web/                frontend workspace (when enabled)
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

This is a target structure.

Do not create optional directories or projects merely to make the repository
match the diagram.

The solution format follows `docs/technology-stack.md` → Solution and Build
Configuration.

# Source Projects

All backend .NET projects, including backend test projects, live under:

```text
backend/
```

The layer projects and their references are defined by the architecture frame:

```text
backend-layout.md
```

# Frontend

The frontend workspace lives outside the .NET `backend` tree:

```text
frontend/
└── ProjectName.Web/
```

The frontend workspace owns its own:

```text
package.json
package-lock.json
framework workspace configuration
tsconfig files
src/
public/
```

Do not manually impose an obsolete directory structure when the current framework
CLI generates a different supported structure.

Detailed frontend structure belongs to `frontend.md` and the frontend knowledge
facet.

# Tests

## Backend Tests

Backend .NET test projects are placed with the production projects (decision:
`docs/technology-stack.md` → Repository Layout):

```text
backend/
```

Typical projects are:

```text
ProjectName.Application.Tests/
ProjectName.IntegrationTests/
```

Create `ProjectName.Domain.Tests/` only when Domain contains non-trivial behavior
that is useful to test independently.

Optional focused test projects such as:

```text
ProjectName.Infrastructure.Tests/
```

should be introduced only when they provide useful separation.

Typical intent:

Domain.Tests
    optional; non-trivial domain behavior when such behavior genuinely belongs
    to Domain

Application.Tests
    application-service/use-case behavior

IntegrationTests
    API + Application + Infrastructure integration

Integration tests may reference the API project for
WebApplicationFactory<Program>.

Keeping backend tests under `backend/` is the approved layout
(`docs/technology-stack.md` → Repository Layout).

## Frontend Tests

Frontend test placement inside the frontend workspace (including E2E tests, for
example `frontend/ProjectName.Web/e2e/`) is described in `project-structure` →
7. Add Test Projects.

# Documentation

Use:

```text
docs/
```

for maintained project documentation.

Possible directories include:

```text
architecture/
decisions/
api/
```

Create them only when corresponding documentation exists.

Do not create empty documentation trees.

# Shared .NET Build Configuration

The decision to use repository-level build/package configuration is recorded in
`docs/technology-stack.md` → Solution and Build Configuration; this section lists
what typically goes where.

## `Directory.Build.props`

Use it for shared .NET project settings such as:

```text
TargetFramework
Nullable
ImplicitUsings
analysis/compiler settings
```

## `Directory.Packages.props`

Use NuGet Central Package Management.

Keep package versions in one place rather than repeating versions across
individual project files.

Approved technology choices are defined in:

```text
docs/technology-stack.md
```

Dependency version, security, and license policy is defined in:

```text
.claude/rules/dependencies.md
add-dependency workflow
```

## `global.json`

Pin the repository to the intended supported .NET SDK line.

When scaffolding, select the current stable SDK for the target .NET release.

Do not select an RC/preview SDK unless explicitly requested.

Allow normal patch/feature-band servicing according to the repository's chosen
`rollForward` policy.

# `.editorconfig`

Keep deterministic repository-wide formatting and code-style configuration here.

Prefer enforceable tooling configuration over duplicating mechanical formatting
rules in Claude instructions.

# Git Ignore

Ignore normal generated/local artifacts, including where applicable:

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

Do not ignore files that are intentionally part of the Development configuration
contract.

# Optional Infrastructure

Docker files, deployment manifests, Kubernetes, cloud infrastructure, messaging
infrastructure, and additional services are introduced only for a concrete
requirement (`docs/technology-stack.md` → Conditional Technologies;
`repository-structure.md`).
