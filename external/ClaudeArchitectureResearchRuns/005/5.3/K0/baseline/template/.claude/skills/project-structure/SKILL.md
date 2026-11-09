---
name: project-structure
description: Use when creating a solution or app scaffold, adding or removing projects, changing project references, or reorganizing repository structure (frontend, tests, docs, shared build files).
---

> Kind: WF | Scope: common | Owner: scaffolding and repository restructuring procedure | Loading: workflow (model- or user-invoked)

# Project Structure

Governing owners: layout, solution format and shared build files D-16, D-17, D-18; platform D-03; stack D-04 to D-10; conditional technologies D-11 to D-15; layer dependencies `rules/backend/architecture.md`; structure discipline `rules/common/repository-layout.md`; test-project references `rules/backend-tests/testing.md`. This workflow owns the procedure only.

Read the references the task needs — not all of them by default:

- `references/solution-layout.md` — new repository or solution, top-level directories, frontend/tests/docs placement, shared repository files;
- `references/backend-layout.md` — Domain, Application, Infrastructure, Api projects, internal directories, project and test references;
- `references/baseline-setup.md` — baseline packages and Development configuration for a new application.

## New solution

1. **Determine scope.** Decide what the request needs: backend, Angular frontend, test projects, documentation, external integrations, mapping, containerization. Do not scaffold optional infrastructure because it may be useful later.
2. **Read the decisions.** Use the decided stack; conditional technologies only when the project needs their capability now.
3. **Repository-level structure.** Create only the required top-level directories and repository-wide files (`references/solution-layout.md`): `.slnx`, `Directory.Build.props`, `Directory.Packages.props`, `global.json`, `.editorconfig`, `.gitignore`, `README.md`.
4. **Backend projects.** Create `Domain`, `Application`, `Infrastructure`, `Api` under `backend/` (`references/backend-layout.md`), targeting the decided platform.
5. **Project references.** Add only the references in `references/backend-layout.md` § Project references; never add an outward reference to make compilation easier.
6. **Packages.** Add each baseline package through `add-dependency` (`references/baseline-setup.md`); resolve versions at install time and never copy versions from examples.
7. **Test projects.** Create only useful test projects beside production projects under `backend/` (typically `Application.Tests` and `IntegrationTests`; `Domain.Tests` only when Domain has non-trivial behavior; `Infrastructure.Tests` only for a concrete need). Angular unit/component tests stay in the Angular workspace; E2E tests, when adopted, under `frontend/<Name>.Web/e2e/`.
8. **Angular application.** When frontend scope exists, create the workspace under `frontend/<Name>.Web/` with the Angular CLI and the decided frontend options (`references/baseline-setup.md`). Frontend structure: `rules/frontend/angular.md`.
9. **Internal directories.** Create only directories the initial implementation needs.
10. **Development persistence.** Configure the Development database and seeding entry point (`references/baseline-setup.md`; `rules/backend/persistence.md`). Add no Production credentials and no automatic production migration step (`delivery-pipeline` § 3).
11. **Verify.** Restore backend dependencies, build the .NET solution, build the Angular application when present, run relevant tests when present, run `node .claude/scripts/check-dependencies.cjs`, inspect the final tree, confirm the Development configuration is usable, then run `verify`. Never report successful scaffolding for a solution that does not build.

## Adding a project later

1. Confirm a new assembly is justified (a new production project is Reserved — CLAUDE.md § Decisions).
2. Identify its architectural or technical responsibility.
3. Add only the minimum required references, preserving dependency direction.
4. Update shared build or package configuration when necessary.
5. Build and test the affected solution.

## Reorganizing an existing solution

1. Inspect the current tree and project references.
2. Identify a concrete structural problem.
3. Preserve behavior.
4. Move code in small, reviewable steps.
5. Update namespaces and references consistently.
6. Avoid unrelated feature work.
7. Verify after restructuring.

Do not force an established project to match this template when doing so provides no concrete value.

## Not scaffolded by default

MediatR, CQRS handler trees, Vertical Slice Architecture, Domain Events, Specifications, SharedKernel, BuildingBlocks, EventBus, messaging, microservices, Kubernetes, cloud-specific projects, state-management frameworks, Docker files and deployment manifests — each needs an actual requirement, and most are Reserved.

## Completion

The physical structure matches the requested scope; project references respect the architecture; the decided stack is used; no unnecessary projects or speculative directories exist; the backend builds; the frontend builds when present; relevant tests pass; the Development configuration is usable; no unrelated code was reorganized.
