---
name: project-structure
description: >
  Use when creating a solution, adding or removing a project, or reorganizing
  repository structure: scaffolding steps, project references, test projects,
  Angular placement, Development configuration.
---

> Owns: scaffolding and restructuring procedure | Scope: common | Loads: workflow (routed from CLAUDE.md and development-workflow); private references references/solution-layout.md, references/backend-layout.md

# Project Structure

## Before You Start

Greenfield work happens before any path-scoped rule has loaded, so read these
owners explicitly:

- CLAUDE.md § Architecture Defaults (layout) and `docs/technology-stack.md`;
- `.claude/rules/repository-structure.md`, `.claude/rules/architecture.md`,
  `.claude/rules/dependencies.md`, and `.claude/rules/persistence.md`;
- `.claude/rules/angular.md` when there is frontend scope.

Read the references this workflow owns according to the task — not all of them
by default:

- `references/solution-layout.md` — new repository or solution, top-level
  directories, frontend/tests/docs placement, shared repository files,
  `global.json`, `.gitignore`;
- `references/backend-layout.md` — Domain, Application, Infrastructure, and Api
  project contents, project references, test project references, Development
  configuration.

## Goals

1. Explicit project boundaries, with dependency direction enforced through
   project references.
2. Production projects, test projects, frontend, and documentation organized
   according to the approved layout.
3. The approved technology stack.
4. No speculative projects, abstractions, or directories.
5. A solution that builds immediately and is verified before completion.

## Scaffolding Procedure

### 1. Determine Scope

Before creating files, determine what the requested project actually needs:
backend, Angular frontend, test projects, documentation, external integrations,
mapping, containerization. Do not scaffold optional infrastructure merely
because it may be useful later.

### 2. Confirm the Stack

Use the baseline stack from `docs/technology-stack.md`. Add conditional
technologies such as Mapster or the resilience packages only when the project
actually requires their capability.

### 3. Create Repository-Level Structure

Following `references/solution-layout.md`, create only the required top-level
directories and repository-wide files (`<Name>.slnx`, `global.json`,
`.gitignore`, `README.md`). This template already provides `.editorconfig`,
`Directory.Build.props`, and `Directory.Packages.props`; keep them at the
repository root.

### 4. Create Backend Projects

Following `references/backend-layout.md`, create `<Name>.Domain`,
`<Name>.Application`, `<Name>.Infrastructure`, and `<Name>.Api` under
`backend/`. The target framework comes from `Directory.Build.props`; remove
duplicated shared properties (target framework, nullable, implicit usings) that
`dotnet new` writes into each project file.

### 5. Add Project References

Add only the references described in `references/backend-layout.md`; they
enforce the dependency direction in `.claude/rules/architecture.md`. Never add
an outward reference to make compilation easier.

### 6. Add Packages

Add baseline packages through `add-dependency`: versions are resolved at
implementation time and recorded in `Directory.Packages.props`; never copy
stale versions from examples.

### 7. Add Test Projects

Create only useful test projects, placed as CLAUDE.md § Architecture Defaults
describes — typically `<Name>.Application.Tests` and `<Name>.IntegrationTests`. Create `<Name>.Domain.Tests` only when Domain contains
non-trivial behavior worth testing independently — a Domain made mainly of
entities and enums does not need one — and `<Name>.Infrastructure.Tests` only
for a concrete testing need. Angular unit/component tests are normally
colocated with the code they test, following current Angular conventions; E2E
tests, when used, go under the workspace (for example `frontend/<Name>.Web/e2e/`).
Never place frontend tests under `backend/`.

### 8. Create the Angular Application

When frontend scope exists, create the workspace under `frontend/<Name>.Web/`
with the current Angular CLI and the baseline from `docs/technology-stack.md`.
Frontend architecture: `.claude/rules/angular.md` and the `angular` skill.

### 9. Add Minimal Internal Directories

Create only directories required by the initial implementation; no empty
directory trees for hypothetical capabilities.

### 10. Configure Development Persistence

For SQL Server projects, create the Development configuration described in
`references/backend-layout.md` (policy: `.claude/rules/persistence.md`).
Development seeding implementation: `ef-core` skill. Do not add Production
credentials, and do not wire automatic Production migration at normal application
startup; a separately approved, controlled deployment-time migration step belongs
to `development-workflow` § CI/CD and deployment.

### 11. Verify

Before declaring scaffolding complete: restore backend dependencies, build the
.NET solution, build the Angular application when present, run relevant tests
when present, inspect project references
(`node .claude/scripts/check-manifests.mjs`, run from the repository root —
`git rev-parse --show-toplevel`), inspect the final repository tree,
and confirm the Development configuration is valid. Then run `verify`. Never
report successful scaffolding for a solution that does not build.

## Adding a Project Later

1. Determine whether a new assembly is actually justified — a new production
   project is Reserved (CLAUDE.md § Decision Control).
2. Identify its architectural or technical responsibility.
3. Add only the minimum required references, preserving dependency direction.
4. Update shared build/package configuration when necessary.
5. Build and test the affected solution.

Do not split code into additional projects merely to make the architecture look
more sophisticated.

## Reorganizing an Existing Solution

1. Inspect the current tree and project references.
2. Identify a concrete structural problem.
3. Preserve behavior.
4. Move code in small reviewable steps.
5. Update namespaces and references consistently.
6. Avoid unrelated feature work.
7. Verify after restructuring.

Do not force an established project to match this template when doing so
provides no concrete value.

## Completion

A project-structure task is complete when the physical structure matches the
requested scope, project references respect the architectural boundaries, the
approved baseline technology is used, no unnecessary projects or speculative
directories were introduced, the backend builds, the frontend builds when
present, relevant tests pass, the local Development configuration is usable, and
no unrelated code was reorganized.
