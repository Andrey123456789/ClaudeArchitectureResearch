---
name: project-structure
description: Use when creating a new solution, scaffolding the backend or frontend, adding or removing projects, changing project references, or reorganizing repository-level structure. Scaffolds only what the requested scope needs and verifies the result builds.
---

> Level: 3-project · Owns: scaffolding and restructuring procedure · Loading: on invocation

# Project Structure

Policy lives elsewhere: boundaries in `.claude/rules/1-architecture/`, stack and layout defaults in the decisions file, structure discipline in `.claude/rules/0-core/engineering.md`. Read references only as needed:

- `references/solution-layout.md` — new repository/solution, top-level directories, shared repository files;
- `references/baseline-packages.md` — baseline non-slot packages and Development configuration;
- `architecture.layout` — backend projects, internal directories, project references, test projects;
- `.claude/rules/2-technology/backend-platform.md` — entry-point mechanism and its folder, other concrete platform bindings;
- `persistence.commands`, `backend-testing.commands`, `frontend.commands` — slot scaffolding.

## Scaffolding procedure

1. **Determine scope** — backend, frontend, test projects, documentation, external integrations, mapping, containerization. Do not scaffold optional infrastructure because it may be useful later.
2. **Read the stack** — decisions file and `references/baseline-packages.md`; conditional technologies only when the capability is actually needed.
3. **Repository level** — create only the required top-level directories and repository files (`references/solution-layout.md`).
4. **Backend projects** — create the projects from `architecture.layout` on the approved .NET target.
5. **Project references** — add only the references `architecture.layout` shows; never an outward reference to make compilation easier. The project-graph hook asks for confirmation of every reference command; confirm only references the approved layout shows.
6. **Packages** — through `add-dependency`, resolving versions at install time; never copy stale versions from examples.
7. **Test projects** — only useful ones, placed and referenced per `architecture.layout`, scaffolded with `backend-testing.commands`. Frontend unit/component tests stay inside the frontend workspace; E2E (when used) under `frontend/<Name>.Web/e2e/`.
8. **Frontend** — when in scope, create the workspace under `frontend/<Name>.Web/` with `frontend.commands`.
9. **Internal directories** — only those the initial implementation uses; no empty trees for hypothetical capabilities.
10. **Development persistence** — Development configuration per the persistence dev-config rule; seeding per the persistence seeding rule; no Production credentials or Production migration automation.
11. **Verify** — restore, build the solution, build the frontend when present, run tests when present, inspect project references (`node "$(git rev-parse --show-toplevel)/.claude/scripts/check-architecture.mjs"`), inspect the final tree, confirm Development configuration works; then run `verify`. Never report scaffolding as successful when the solution does not build.

## Adding a project later

1. Confirm a new assembly is actually justified — a new production project or layer is Reserved.
2. Identify its architectural or technical responsibility.
3. Add only the minimum references, preserving dependency direction.
4. Update shared build/package configuration when necessary.
5. Build and test the affected solution.

## Reorganizing an existing solution

1. Inspect the current tree and project references.
2. Identify a concrete structural problem.
3. Preserve behavior.
4. Move code in small reviewable steps.
5. Update namespaces and references consistently.
6. Avoid unrelated feature work.
7. Verify after restructuring.

Do not force an established project to match this template when that gives no concrete value.

## Not introduced by default

Check against decision control (`CLAUDE.md`), the patterns not adopted (imported adopted-architecture rule), and engineering discipline before scaffolding any of: MediatR-style mediators, CQRS handler trees, Vertical Slice Architecture, Domain Events, Specifications, SharedKernel, BuildingBlocks, EventBus, messaging, microservices, Kubernetes, cloud-specific projects, state-management frameworks, Docker without a containerization need, and generic `Common`/`Helpers`/`Utils` directories.

## Completion

The structure matches the requested scope, references respect boundaries, approved technology is used, nothing speculative was added, backend and frontend (when present) build, relevant tests pass, local Development configuration works, and no unrelated code was reorganized.
