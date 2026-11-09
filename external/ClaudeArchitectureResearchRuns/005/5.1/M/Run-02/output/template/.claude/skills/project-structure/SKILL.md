---
name: project-structure
description: >
  Use when creating a new solution, adding or removing a backend or test
  project, creating the Angular workspace, changing project references, or
  reorganizing repository structure. Scaffolding procedure with structural
  checks.
---

> Owner: scaffolding and restructuring procedure | Scope: common | Loads: on demand — workflow (routed by `CLAUDE.md` § Development Workflow) | Enforced: `.claude/scripts/check-architecture.mjs`, `.claude/scripts/check-dependencies.mjs`

# Project Structure

## Read First

Greenfield and restructuring work may touch no file that triggers path rules, so
read these owners explicitly before creating anything:

- `SPECIFICATION.md` and `CUSTOM_SETTINGS.md` (product inputs);
- `.claude/rules/architecture.md`, `.claude/rules/repository-structure.md`,
  `.claude/rules/persistence.md`, `.claude/rules/testing.md`,
  `.claude/rules/dependencies.md`;
- `.claude/rules/angular.md` when frontend scope exists.

The approved stack (`docs/technology-stack.md`) and architecture decisions
(`CLAUDE.md`) are already loaded.

Read the private references according to the task, not all at once:

- `references/solution-layout.md` — new repository or solution, top-level
  directories, frontend/tests/docs placement, shared repository files;
- `references/backend-layout.md` — Domain, Application, Infrastructure, Api
  internals, project references, backend test projects.

## Procedure

### 1. Determine Scope

Decide what the requested project actually needs: backend, Angular frontend,
test projects, documentation, external integrations, mapping,
containerization. Scaffold nothing optional merely because it may be useful
later. Anything beyond the default shape (an extra production project, layer,
or infrastructure category) is Reserved: raise a Decision Request
(`architecture-decision` workflow) before creating it.

### 2. Repository-Level Files

Keep the template's root files (`CLAUDE.md`, `SPECIFICATION.md`,
`CUSTOM_SETTINGS.md`, `.editorconfig`, `Directory.Build.props`,
`Directory.Packages.props`, `.claude/`, `docs/`). Add only what the project
needs, typically:

```bash
dotnet new sln -n ProjectName --format slnx   # .slnx is the default format
dotnet new globaljson --sdk-version <current stable 10.0 SDK> --roll-forward latestFeature
dotnet new gitignore
```

Select the current stable SDK of the target .NET line (no preview/RC unless
explicitly requested) and keep `.gitignore` covering `bin/`, `obj/`, `.vs/`,
`node_modules/`, `dist/`, `TestResults/`, `coverage/`, local secret or config
overrides, and `.claude/settings.local.json`. Do not ignore files that are part of
the Development configuration contract.

### 3. Backend Projects

```bash
dotnet new classlib -n ProjectName.Domain -o backend/ProjectName.Domain
dotnet new classlib -n ProjectName.Application -o backend/ProjectName.Application
dotnet new classlib -n ProjectName.Infrastructure -o backend/ProjectName.Infrastructure
dotnet new webapi --use-controllers -n ProjectName.Api -o backend/ProjectName.Api
dotnet sln ProjectName.slnx add backend/ProjectName.Domain backend/ProjectName.Application backend/ProjectName.Infrastructure backend/ProjectName.Api
```

After generation:

- remove per-project properties that `Directory.Build.props` already supplies
  (`TargetFramework`, `Nullable`, `ImplicitUsings`) unless a project genuinely
  differs;
- move any generated `PackageReference` versions into `Directory.Packages.props`
  (Central Package Management rejects versioned references with `NU1008`);
- the `webapi` template may add `Microsoft.AspNetCore.OpenApi` with
  `AddOpenApi()`/`MapOpenApi()`; replace it with the approved Swagger baseline
  (`swagger` skill, package via `add-dependency`);
- delete placeholder classes (`Class1.cs`, sample weather endpoints).

### 4. Project References

Add only the graph in `references/backend-layout.md` § Project References:

```bash
dotnet add backend/ProjectName.Application/ProjectName.Application.csproj reference backend/ProjectName.Domain/ProjectName.Domain.csproj
dotnet add backend/ProjectName.Infrastructure/ProjectName.Infrastructure.csproj reference backend/ProjectName.Application/ProjectName.Application.csproj backend/ProjectName.Domain/ProjectName.Domain.csproj
dotnet add backend/ProjectName.Api/ProjectName.Api.csproj reference backend/ProjectName.Application/ProjectName.Application.csproj backend/ProjectName.Infrastructure/ProjectName.Infrastructure.csproj
```

Never add an outward reference to make compilation easier; reconsider the
abstraction instead.

### 5. Packages

Add only baseline packages for capabilities present in the initial project, each
through the `add-dependency` workflow. Conditional technologies wait until their
capability is needed. Do not copy versions from examples or older projects.

### 6. Test Projects

Create only useful test projects, beside production projects under `backend/`:

```bash
dotnet new nunit -n ProjectName.Application.Tests -o backend/ProjectName.Application.Tests
dotnet new nunit -n ProjectName.IntegrationTests -o backend/ProjectName.IntegrationTests
```

`ProjectName.Domain.Tests` only when Domain has non-trivial behavior worth
testing independently; `ProjectName.Infrastructure.Tests` only for a concrete
need. Apply the same `Directory.Build.props` and Central Package Management
clean-up as in step 3, and give each test project only the references its scope
requires (`.claude/rules/testing.md` § Test Project References). Integration
tests need `Microsoft.AspNetCore.Mvc.Testing` and an accessible `Program`
(for example `public partial class Program { }` at the end of `Program.cs`).

### 7. Angular Workspace

When frontend scope exists, create the workspace under
`frontend/ProjectName.Web/` with the current Angular CLI and the baseline from
`docs/technology-stack.md`, for example:

```bash
npx @angular/cli@latest new ProjectName.Web --directory frontend/ProjectName.Web --routing --style scss --strict
```

Flag names change between CLI versions: check `ng new --help` for the installed
CLI (zoneless, SSR, and test-runner options) instead of guessing. Do not impose an
obsolete directory structure on what the CLI generates. Add Angular Material
with `ng add @angular/material` through `add-dependency`. Unit and component
tests stay colocated in the workspace; E2E tests, when required, live under
`frontend/ProjectName.Web/e2e/`.

### 8. Minimal Internal Directories

Inside each project, create only directories that hold code for the initial
implementation (`references/backend-layout.md` shows the target shape).

### 9. Development Configuration

For SQL Server, give `backend/ProjectName.Api/appsettings.Development.json` a
usable local connection string without secrets, for example on Windows:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\MSSQLLocalDB;Database=ProjectName;Trusted_Connection=True;TrustServerCertificate=True;"
  }
}
```

Adapt the database name. When local SQL Server needs credentials, keep the
non-secret structure in configuration and supply the secret with
`dotnet user-secrets`. Development seeding follows
`.claude/rules/persistence.md` § Development Seeding (pattern: `ef-core` skill).
Do not add Production credentials or Production migration automation.

### 10. Verify

```bash
node .claude/scripts/check-architecture.mjs
node .claude/scripts/check-dependencies.mjs
dotnet build ProjectName.slnx
dotnet test ProjectName.slnx
```

Build the Angular workspace when present (`npm run build` in
`frontend/ProjectName.Web`), inspect project references and the final tree,
confirm the Development configuration is valid, then run the `verify` workflow.
Do not report successful scaffolding when the solution does not build.

## Adding a Project Later

1. Confirm a new assembly is justified; a new production project is Reserved.
2. Identify its architectural or technical responsibility.
3. Add only the minimum references, preserving dependency direction.
4. Update shared build and package configuration when necessary.
5. Build and test the affected solution.

Do not split code into more projects merely to make the architecture look
sophisticated.

## Reorganizing an Existing Solution

1. Inspect the current tree and project references.
2. Identify a concrete structural problem.
3. Preserve behavior; move code in small, reviewable steps.
4. Update namespaces and references consistently; avoid unrelated feature work.
5. Verify after restructuring.

Do not force an established project to match this template when that provides no
concrete value.

## Stop Conditions

- A Reserved decision appears → Decision Request; continue only with
  non-Reserved scaffolding.
- The toolchain (SDK, Node.js, Angular CLI) is missing or incompatible → report
  it instead of editing configuration to compensate.
- The solution does not build after a bounded repair attempt → switch to the
  `build-fix` workflow.

## Completion

Report:

- the created or changed structure (tree excerpt) and project references;
- packages added (from `add-dependency` output);
- backend build, frontend build, tests, structural checks:
  PASS / NOT RUN / NOT APPLICABLE;
- open Decision Requests, if any.
