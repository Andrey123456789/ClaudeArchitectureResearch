---
name: project-structure
description: >
  Use when creating a solution, scaffolding the backend/frontend, adding or removing
  projects, changing project references, or reorganizing the repository.
---

> Level: 3 Project · Owns: scaffolding and restructuring procedure (workflow) · Scope: common · Loads: on invocation · Depends on: CLAUDE.md, .claude/rules/** (owner reads)

# Project Structure

This workflow owns the steps. The structure it produces is governed by rules it must read first, because in a new or empty repository no path rule has fired yet.

## 0. Read the owners

Read before creating anything:

- `.claude/rules/1-architecture/backend-layers.md` and `code-organization.md` — layers, dependency direction, physical organization, test references;
- `.claude/rules/3-project/decisions.md` (already loaded) and `.claude/rules/3-project/layout.md` — stack, repository defaults, project mapping;
- `.claude/rules/3-project/package-management.md` and `data-lifecycle.md` — central package management, lockfile, Development database and seeding;
- `.claude/rules/2-technology/aspnet-core.md` and `angular.md` when creating the Api or the frontend.

Private references (read according to the task — not all at once):

- `references/solution-layout.md` — new repository/solution, top-level directories, shared repository files, `.gitignore`, `global.json`, docs;
- `references/backend-layout.md` — Domain/Application/Infrastructure/Api internals, where backend files belong, composition snippets.

## 1. Determine scope

Decide what the request actually needs: backend, Angular frontend, test projects, documentation, external integrations, mapping, containerization. Do not scaffold optional infrastructure because it may be useful later.

## 2. Repository-level structure

Create only the required top-level directories and repository files (`references/solution-layout.md`): the solution (`dotnet new sln -n <Name>` creates `<Name>.slnx` with the .NET 10 SDK), `global.json` (SDK selection in `references/solution-layout.md`), and the template's `Directory.Build.props`, `Directory.Packages.props`, `.editorconfig`, `.gitignore`.

## 3. Backend projects

```bash
dotnet new classlib -n <Name>.Domain -o backend/<Name>.Domain
dotnet new classlib -n <Name>.Application -o backend/<Name>.Application
dotnet new classlib -n <Name>.Infrastructure -o backend/<Name>.Infrastructure
dotnet new webapi --use-controllers -n <Name>.Api -o backend/<Name>.Api
dotnet sln <Name>.slnx add backend/<Name>.Domain backend/<Name>.Application backend/<Name>.Infrastructure backend/<Name>.Api
```

Remove template-generated version, `TargetFramework`, `Nullable`, or `ImplicitUsings` properties that `Directory.Build.props` already supplies.

## 4. Project references

Add only the references `layout.md` maps from the Level 1 dependency direction, as `<ProjectReference>` items in the project files (for example `<ProjectReference Include="..\<Name>.Domain\<Name>.Domain.csproj" />` in `<Name>.Application.csproj`). Never add an outward reference to make compilation easier. The project hook blocks `dotnet add/remove … reference` and `dotnet reference add/remove` (reference-graph changes: CLAUDE.md → Decision control), reports every reference change, and rejects outward references — include those reports in the scaffolding report.

## 5. Packages

Add baseline packages only for capabilities present in the initial project, each through `add-dependency` (versions resolved at install time). Conditional packages wait for their trigger.

## 6. Test projects

Create the useful NUnit test projects from `layout.md` → Test projects (optional ones only under its conditions), for example `dotnet new nunit -n <Name>.Application.Tests -o backend/<Name>.Application.Tests`, with the narrow references listed there. Expose `Program` to `WebApplicationFactory<Program>` when top-level statements make it inaccessible (for example `public partial class Program;`).

## 7. Angular workspace

When frontend scope exists, create it with the current Angular CLI under `frontend/<Name>.Web/` (for example `npx @angular/cli@latest new <Name>.Web --directory frontend/<Name>.Web --routing --style=scss --strict`, plus `--zoneless` when the CLI version offers it), using the baseline in `decisions.md` and letting the CLI select compatible Angular/TypeScript/RxJS versions. Do not impose an obsolete directory structure on what the current CLI generates; feature structure follows `frontend-structure.md`.

## 8. Minimal internal directories

Inside each project create only the directories the initial implementation needs (`references/backend-layout.md`); no empty trees for hypothetical capabilities.

## 9. Development configuration

For SQL Server projects create `appsettings.json` and `appsettings.Development.json` as `data-lifecycle.md` describes, and wire Development seeding per that rule. Configure Swagger UI for Development (`aspnet-core.md`) and a launch profile whose URLs agree with the configured HTTP/HTTPS ports. Never add Production credentials, and do not wire automatic Production migration at normal application startup; a separately approved, controlled deployment-time migration step belongs to `delivery-pipeline`.

## 10. Verify

Before declaring scaffolding complete: restore, build the .NET solution, build the Angular application when present, run relevant tests when present, inspect project references, inspect the final repository tree, and confirm the Development configuration is valid. Then run `verify`. Never report successful scaffolding for a solution that does not build.

## Adding a project later

1. Confirm a new assembly is justified — a new production project or layer is Reserved (CLAUDE.md → Decision control).
2. Identify its responsibility; add only the minimum references, preserving dependency direction.
3. Update shared build/package configuration when necessary; build and test the affected solution.

## Reorganizing an existing solution

Inspect the current tree and references, identify a concrete structural problem, preserve behavior, move code in small reviewable steps, update namespaces and references consistently, avoid unrelated feature work, and verify afterwards. Do not force an established project to match this template when that provides no concrete value.

## Not scaffolded by default

MediatR, CQRS handler trees, Vertical Slice Architecture, Domain Events, Specifications, SharedKernel, BuildingBlocks, EventBus, messaging, microservices, Kubernetes, cloud-specific projects, state-management frameworks, Docker, generic `Common`/`Helpers`/`Utils` directories — governed by `1-architecture/overview.md`, `code-organization.md`, and `3-project/decisions.md`.

## Completion

The physical structure matches the requested scope; references respect the architecture; the approved stack is used; no unnecessary projects or speculative directories exist; backend and frontend (when present) build; relevant tests pass; local Development configuration is usable; nothing unrelated was reorganized.
