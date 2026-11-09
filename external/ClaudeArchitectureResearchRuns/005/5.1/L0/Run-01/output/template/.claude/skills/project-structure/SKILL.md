---
name: project-structure
description: >
  Use when creating a new application, adding or removing a project, or
  reorganizing the repository: solution and project scaffolding, references,
  test projects, Angular workspace, Development configuration.
---

> Level: 3 Project · Owns: scaffolding and structural-change procedure · Scope: common · Loads: on demand (model- or user-invoked)

# Project Structure

## Read first

In a new or restructured repository, path-scoped rules may not have loaded yet. Before creating files, read the owners that govern what you are about to create:

- `.claude/rules/1-architecture/backend-layers.md`, `persistence-boundary.md`, `entry-points.md`, `outcomes.md`, `code-organization.md`
- `.claude/rules/1-architecture/frontend-structure.md` and `.claude/rules/2-technology/angular.md` when frontend scope exists
- `.claude/rules/2-technology/csharp.md`, `aspnet-core.md`, `ef-core.md`
- `.claude/rules/3-project/conventions.md`, `.claude/rules/3-project/data-lifecycle.md`

The architecture overview, project decisions and decision control are always loaded. This workflow does not redefine their rules.

Private references — read according to the task, not all at once:

- `references/solution-layout.md` — repository tree, shared build files, tests and docs placement, ignore patterns.
- `references/backend-layout.md` — internal project layout, registration files, project-reference graph, test references.

## Procedure

### 1. Determine scope

Decide what the request actually needs before creating anything: backend, Angular frontend, test projects, documentation, external integrations, mapping, containerization. Scaffold nothing for hypothetical future use (`code-organization.md`, project decisions). A new production project or layer beyond the four standard backend projects is Reserved.

### 2. Repository-level files

Read `references/solution-layout.md`. Typical commands (confirm flags with `--help` for the installed SDK):

```bash
dotnet new sln -n <Name>                      # .NET 10 SDK creates <Name>.slnx
dotnet new globaljson --sdk-version <latest stable 10.0.x> --roll-forward latestFeature
dotnet new gitignore
```

Keep the template's `.editorconfig`, `Directory.Build.props` and `Directory.Packages.props`; do not overwrite them with generated defaults.

### 3. Backend projects

Read `references/backend-layout.md`.

```bash
dotnet new classlib -n <Name>.Domain         -o backend/<Name>.Domain
dotnet new classlib -n <Name>.Application    -o backend/<Name>.Application
dotnet new classlib -n <Name>.Infrastructure -o backend/<Name>.Infrastructure
dotnet new webapi --use-controllers -n <Name>.Api -o backend/<Name>.Api
dotnet sln <Name>.slnx add backend/<Name>.Domain backend/<Name>.Application backend/<Name>.Infrastructure backend/<Name>.Api
```

Delete template placeholders (`Class1.cs`, sample controllers and models) that the initial implementation does not use.

### 4. Project references

Add only the references in `references/backend-layout.md` (Project References):

```bash
dotnet add backend/<Name>.Application reference backend/<Name>.Domain
dotnet add backend/<Name>.Infrastructure reference backend/<Name>.Application backend/<Name>.Domain
dotnet add backend/<Name>.Api reference backend/<Name>.Application backend/<Name>.Infrastructure
```

A missing type is solved by the abstraction boundary, not by an extra reference (`backend-layers.md`).

### 5. Packages

Add packages through the `add-dependency` workflow. Baseline per project when its capability is present:

| Project | Baseline packages |
|---|---|
| Application | `FluentValidation`, `FluentValidation.DependencyInjectionExtensions` (when validators exist) |
| Infrastructure | `Microsoft.EntityFrameworkCore.SqlServer` |
| Api | `Swashbuckle.AspNetCore`, `Serilog.AspNetCore`, `Microsoft.EntityFrameworkCore.Design` (`PrivateAssets="all"`, for migrations tooling) |
| Integration tests | `Microsoft.AspNetCore.Mvc.Testing` |

`dotnet new` templates write versioned `PackageReference` items; move every version into `Directory.Packages.props` (Central Package Management) or the build fails with NU1008. Conditional technologies (Mapster, resilience, Testcontainers, Playwright, Asp.Versioning, Docker) are added only when their capability is required.

### 6. Test projects

```bash
dotnet new nunit -n <Name>.Application.Tests -o backend/<Name>.Application.Tests
dotnet new nunit -n <Name>.IntegrationTests  -o backend/<Name>.IntegrationTests
```

Create only useful test projects. Add `<Name>.Domain.Tests` only when Domain holds non-trivial behavior worth testing on its own, and `<Name>.Infrastructure.Tests` only for a concrete need. Keep test references narrow (`references/backend-layout.md`, Test References). If top-level statements hide `Program` from `WebApplicationFactory<Program>`, add `public partial class Program;` to the Api project.

### 7. Angular workspace

When frontend scope exists, create the workspace under `frontend/<Name>.Web/` with the current stable Angular CLI:

```bash
npx @angular/cli@latest new <Name>.Web --directory frontend/<Name>.Web --style scss --routing --strict --skip-git
```

Select zoneless change detection when the CLI version offers it (check `ng new --help`), confirm the configured test runner is Vitest, then add Angular Material through `add-dependency` (`ng add @angular/material`). Do not impose an obsolete directory structure on what the current CLI generates; feature organization follows `frontend-structure.md`.

### 8. Minimal internal directories

Create only directories that receive real code in the initial implementation (`code-organization.md`). No empty trees for future capabilities.

### 9. Development configuration and persistence

- Configure the local Development connection string in `backend/<Name>.Api/appsettings.Development.json` as `data-lifecycle.md` describes; no production credentials, no production migration automation.
- Register persistence in `Infrastructure/DependencyInjection.cs` and compose layers in `Program.cs` (`AddApplication()`, `AddInfrastructure(builder.Configuration)`).
- Configure Swagger UI for Development and a Development launch profile (`"launchUrl": "swagger"`) whose URLs match the actual HTTP/HTTPS ports.
- When entities exist, add the development seeder and its Development-only startup call (`ef-core` skill, Development Seeding).

### 10. Verify the structure

```bash
dotnet build <Name>.slnx
dotnet test <Name>.slnx
node .claude/scripts/check-architecture.mjs
npm run build          # in frontend/<Name>.Web when present
```

Inspect project references and the final repository tree, confirm the Development configuration starts the API (Swagger UI reachable at `/swagger`), then run the `verify` workflow. Never report successful scaffolding while the solution does not build.

## Adding a project later

1. Confirm a new assembly is justified (Reserved: decision control).
2. Name its architectural or technical responsibility.
3. Add only the minimum references, preserving dependency direction.
4. Update shared build or package configuration when necessary.
5. Build and test the affected solution.

## Reorganizing an existing solution

1. Inspect the current tree and project references.
2. Name the concrete structural problem being solved.
3. Preserve behavior; move code in small reviewable steps.
4. Update namespaces and references consistently; avoid unrelated feature work.
5. Verify after restructuring.

Do not force an established project to match this template when doing so provides no concrete value.

## Stop conditions

Stop and raise a Decision Request when the request needs a new layer or production project, an architectural pattern from the not-adopted list, a replacement of an approved technology, or new infrastructure categories.

## Completion

Report: created/changed projects and directories, project references, packages added (with versions), commands run with PASS / NOT RUN / NOT APPLICABLE, and any open Decision Requests.
