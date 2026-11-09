---
name: project-structure
description: Use when creating a new solution or application, adding or removing a backend, frontend or test project, changing project references, or reorganizing repository-level structure. Scaffolding procedure with layout and stack references.
---
<!-- Kind: WF | Scope: common | Owns: scaffolding, project-addition and restructuring procedure | Loads: workflow invocation -->
# Project Structure

Policy applied by this procedure — read before creating anything: decision register (DEC-ARCH-01, DEC-PLAT-01, DEC-BUILD-01, DEC-LAYOUT-01, DEC-TEST-01, DEC-WEB-01 and the conditional entries); `rules/backend/architecture.md` § Dependency Direction; `rules/common/structure.md`; `rules/common/dependencies.md`; `rules/backend-tests/testing.md` § Test Project References. This workflow does not redefine those rules.

## References

Read by task — not all at once:

- `references/solution-layout.md` — new repository or solution, top-level directories, frontend/tests/docs placement, shared repository files.
- `references/backend-layout.md` — Domain, Application, Infrastructure and Api projects, internal folders, project and test references.
- `references/scaffold-stack.md` — baseline packages per register entry, SQL Server Development configuration, Angular CLI baseline, test packages.

## Goals

1. Keep project boundaries explicit.
2. Enforce dependency direction through project references.
3. Keep production projects, test projects, frontend and documentation organized according to the layout decision.
4. Use the approved technology stack.
5. Avoid speculative projects, abstractions and directories.
6. Keep the generated solution immediately buildable.
7. Verify the resulting structure before completion.

## Default Shape

```text
backend/
    ProjectName.Domain/
    ProjectName.Application/
    ProjectName.Application.Tests/
    ProjectName.Infrastructure/
    ProjectName.Api/
    ProjectName.IntegrationTests/

frontend/
    ProjectName.Web/

docs/
```

This is a target organization, not a requirement to create every optional directory or test project immediately.

## Scaffolding Procedure

### 1. Determine Scope

Determine what the requested project actually needs: backend, Angular frontend, test projects, documentation, external integrations, mapping, containerization. Do not scaffold optional infrastructure merely because it may be useful later.

### 2. Read the Stack

Read the register and `references/scaffold-stack.md`. Do not silently substitute alternative frameworks or libraries; conditional technologies (Mapster, resilience packages, Testcontainers, Playwright, Docker) only when their capability is actually required.

### 3. Create Repository-Level Structure

Following `references/solution-layout.md`, create only the required top-level directories and repository-wide files (`.slnx`, `Directory.Build.props`, `Directory.Packages.props`, `global.json`, `.editorconfig`, `.gitignore`, `README.md`).

### 4. Create Backend Projects

Following `references/backend-layout.md`, create `ProjectName.Domain`, `ProjectName.Application`, `ProjectName.Infrastructure`, `ProjectName.Api` on the approved .NET target.

### 5. Add Project References

Add only the references allowed by `rules/backend/architecture.md` § Dependency Direction (commands in `references/backend-layout.md`). Never add an outward reference to make compilation easier.

### 6. Add Packages

Run `add-dependency` for every package: versions are resolved at implementation time, never copied from examples or historical content. The register says which technologies are approved; `add-dependency` owns version, security and license checks.

### 7. Add Test Projects

Create only useful test projects, beside the production projects under `backend/`: typically `ProjectName.Application.Tests` and `ProjectName.IntegrationTests`. Add `ProjectName.Domain.Tests` only when Domain has non-trivial behavior worth testing independently, and `ProjectName.Infrastructure.Tests` or another focused project only for a concrete need. Angular unit/component tests stay inside `frontend/ProjectName.Web/`, colocated per current Angular conventions; frontend E2E tests, when used, stay in the workspace (for example `frontend/ProjectName.Web/e2e/`).

### 8. Create the Angular Application

When frontend scope exists, create the workspace at `frontend/ProjectName.Web/` with the baseline from `references/scaffold-stack.md`. Feature layout belongs to `rules/frontend/angular.md` and the `angular` skill.

### 9. Add Minimal Internal Directories

Inside each project, create only the directories the initial implementation needs (`rules/common/structure.md`).

### 10. Configure Development Persistence

For SQL Server, create the Development configuration described in `references/scaffold-stack.md`. Development seeding follows `rules/backend/persistence.md` § Development Seeding. Do not add Production credentials or Production migration automation (`delivery-pipeline`).

### 11. Verify

Restore backend dependencies; build the .NET solution; build the Angular application when present; run relevant tests when present; inspect project references (`node .claude/scripts/check-manifests.mjs`); inspect the final repository tree; confirm the Development configuration is valid. Then run `verify`. Never report successful scaffolding when the generated solution does not build.

## Adding a Project Later

1. Determine whether a new assembly is actually justified — a new production project or layer is Reserved (CLAUDE.md § Decisions).
2. Identify its architectural or technical responsibility.
3. Add only the minimum required references.
4. Preserve dependency direction.
5. Update shared build/package configuration when necessary.
6. Build and test the affected solution.

Do not split code into more projects merely to make the architecture look more sophisticated.

## Reorganizing an Existing Solution

1. Inspect the current tree and project references.
2. Identify a concrete structural problem.
3. Preserve behavior.
4. Move code in small reviewable steps.
5. Update namespaces and references consistently.
6. Avoid unrelated feature work.
7. Verify after restructuring.

Do not force an established project to match this template when that provides no concrete value.

## Not Scaffolded by Default

Without a recorded decision (DEC-ARCH-02, CLAUDE.md § Decisions) do not scaffold MediatR, CQRS handler trees, Vertical Slice Architecture, Domain Events, Specifications, SharedKernel, BuildingBlocks, EventBus, messaging, microservices, Kubernetes, cloud-specific projects or state-management frameworks. Docker only per DEC-OPS-01. No generic `Common`, `Helpers` or `Utils` directories (`rules/common/structure.md`).

## Completion

The task is complete when the physical structure matches the requested scope, project references respect the architecture, the approved stack is used, no unnecessary projects or speculative directories exist, the backend builds, the frontend builds when present, relevant tests pass, local Development configuration is usable, and no unrelated code was reorganized.
