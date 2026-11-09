---
name: project-structure
description: >
  Use when creating a solution, adding or removing a project, or reorganizing repository structure: scaffolding, references, test projects, Angular workspace.
---

> Level: 3 Project | Owns: scaffolding and restructuring procedure | Scope: common | Loads: workflow skill (model-invoked; routed from CLAUDE.md) | Depends on: CLAUDE.md, 0-core/*, 1-architecture/*, 2-technology/*, 3-project/*

# Project Structure

Architecture and stack policy are owned by the rules; this workflow applies
them to the physical repository. Read only the references the task needs:

- `references/solution-layout.md` — new repository, top-level directories,
  shared repository files, frontend/test/docs placement;
- `references/backend-layout.md` — Domain/Application/Infrastructure/Api
  projects, internal directories, project and test references;
- `references/technology-stack.md` — baseline packages, Angular CLI options,
  Development database configuration.

## Scaffold a New Solution

1. **Determine scope.** Decide what the project actually needs now: backend,
   Angular frontend, test projects, docs, external integrations, mapping,
   containerization (proportionality: CLAUDE.md, Scope and Simplicity).
2. **Load the governing rules.** Path-scoped rules have not fired yet in an
   empty repository. Read the rule modules for every scope you will create
   (`develop` → Rule Reads table), at minimum
   `.claude/rules/1-architecture/backend-layers.md`,
   `1-architecture/persistence-boundary.md`, `1-architecture/frontend-structure.md`,
   `3-project/data-lifecycle.md`, and `0-core/structure-principles.md`.
3. **Repository-level structure.** Following `references/solution-layout.md`,
   create only the required top-level directories and repository files; keep
   the template's `Directory.Build.props`, `Directory.Packages.props`, and
   `.editorconfig`; add `global.json` pinned to the current stable SDK of the
   approved .NET line.
4. **Backend projects.** Create `<Name>.Domain`, `<Name>.Application`,
   `<Name>.Infrastructure`, `<Name>.Api` under `backend/` and add them to
   `<Name>.slnx` (`references/backend-layout.md`).
5. **Project references.** Add only the references in
   `references/backend-layout.md`; never add an outward reference to make
   compilation easier. These standard references are Decided, so append the
   marker comment `# project-structure:approved` to each
   `dotnet add <project> reference <target>` command (the dependency-guard hook
   blocks unmarked reference changes).
6. **Packages.** Add the baseline packages whose capability exists in the
   initial project (`references/technology-stack.md`,
   `0-core/dependency-hygiene.md`); run `add-dependency` for each, resolving
   versions at install time.
7. **Test projects.** Create only useful ones beside the production projects —
   typically `<Name>.Application.Tests` and `<Name>.IntegrationTests`;
   `<Name>.Domain.Tests` only when Domain has non-trivial behavior,
   `<Name>.Infrastructure.Tests` only for a concrete need.
8. **Angular workspace.** When frontend scope exists, create
   `frontend/<Name>.Web/` with the current Angular CLI and the baseline options
   (`references/technology-stack.md`); frontend unit tests stay colocated in the
   workspace, E2E tests (when required) under `frontend/<Name>.Web/e2e/`.
9. **Internal directories.** Create the directories the initial
   implementation fills (`0-core/structure-principles.md`).
10. **Development persistence.** Configure the Development connection and
    seeding per `3-project/data-lifecycle.md`; add no Production credentials or
    Production migration automation.
11. **Verify.** Restore, build the .NET solution, build the Angular app when
    present, run tests when present, inspect project references
    (`node .claude/scripts/check-manifests.cjs`), inspect the final tree, and
    confirm the Development configuration; then run `verify`. Do not report
    successful scaffolding when the solution does not build.

## Add a Project Later

Adding a production project or changing the reference graph is Reserved
(CLAUDE.md): run `architecture-decision` first. After approval: identify its
responsibility, add the minimum references, preserve dependency direction,
update shared build/package configuration if needed, and build and test.

## Reorganize an Existing Solution

Inspect the current tree and references, name the concrete structural problem,
preserve behavior, move code in small reviewable steps, update namespaces and
references consistently, avoid unrelated feature work, and verify. Do not force
an established project to match this template when that gives no concrete value.

## Complete

The task is complete when the structure matches the requested scope,
references respect the boundaries, the approved stack is used, no speculative
projects or directories exist, backend and frontend build, relevant tests pass,
the Development configuration is usable, and no unrelated code was moved.
