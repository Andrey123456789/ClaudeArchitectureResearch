---
name: project-structure
description: >
  Use when creating a solution, adding or removing backend or test projects,
  changing project references, placing the frontend workspace, or
  reorganizing repository structure.
---

> Workflow skill. Owns: the scaffolding and structural-change procedure, including its greenfield rule reads and completion checks · Scope: common · Loads: on invocation; routed by CLAUDE.md · Depends on: CLAUDE.md, docs/technology-stack.md, .claude/rules/

# Project Structure

The approved stack and default layout are in `docs/technology-stack.md`
(always loaded). Layer rules: `architecture.md`; physical-structure rule:
`repository-layout.md`.

## References

Read only what the task needs:

- `references/solution-layout.md` — creating a repository or solution,
  reorganizing top-level directories, adding frontend, tests, or docs, deciding
  where shared repository files belong.
- `references/backend-layout.md` — creating or reorganizing Domain,
  Application, Infrastructure, or Api projects, adding project references,
  deciding where backend files belong.

## Scaffolding a New Solution

### 1. Determine Scope

Before creating files, determine what the request actually needs: backend,
Angular frontend, test projects, documentation, external integrations,
mapping, containerization. Scaffold optional infrastructure only when the
request needs it (`repository-layout.md`).

### 2. Read the Governing Rules

New files are not in context yet, so read `architecture.md`, `persistence.md`,
`repository-layout.md`, and `dependencies.md` explicitly before generating
code. Use the baseline from `docs/technology-stack.md`; conditional
technologies are added only when the project needs their capability.

### 3. Create Repository-Level Structure

Read `references/solution-layout.md`. Create only the required top-level
directories and repository-wide files: the `.slnx` solution, `global.json`,
`.gitignore`, `README.md`; keep the template's `Directory.Build.props`,
`Directory.Packages.props`, and `.editorconfig`.

### 4. Create Backend Projects

Read `references/backend-layout.md`. The normal backend is
`<Name>.Domain`, `<Name>.Application`, `<Name>.Infrastructure`, and
`<Name>.Api` under `backend/`, targeting the approved .NET version (inherited
from `Directory.Build.props`).

### 5. Add Project References

Add only the references allowed by `architecture.md` (Dependency Direction),
also when compilation seems to need another one.

### 6. Add Packages

Add baseline packages through `add-dependency`; resolve versions at
implementation time and never copy versions from examples or older content.

### 7. Add Test Projects

Create only useful test projects, beside the production projects under
`backend/`: typically `<Name>.Application.Tests` and `<Name>.IntegrationTests`;
`<Name>.Domain.Tests` only when Domain has non-trivial behavior worth testing
independently; `<Name>.Infrastructure.Tests` or another focused project only for
a concrete testing need. Angular unit/component tests stay in
`frontend/<Name>.Web/`, colocated per current Angular conventions; E2E tests,
when used, also stay in the frontend workspace (for example
`frontend/<Name>.Web/e2e/`).

### 8. Create the Angular Application

When frontend scope exists, create the workspace in `frontend/<Name>.Web/` with
the current Angular CLI and the stack's baseline options. Frontend structure
follows `angular.md` and the `angular` skill.

### 9. Add Minimal Internal Directories

Inside each project, create only the directories the initial implementation
uses.

### 10. Configure Development Persistence

For SQL Server, add the Development configuration described in `persistence.md`
(Local Development Database Configuration) and the seeder described there and
in the `ef-core` skill. Do not add Production credentials or production
migration automation (`development-workflow`, Database deployment).

### 11. Verify

Before declaring scaffolding complete: restore backend dependencies; build the
.NET solution; build the Angular application when present; run relevant tests
when present; inspect project references
(`node .claude/scripts/check-manifests.mjs`) and source boundaries
(`node .claude/scripts/check-architecture.mjs`); inspect the final repository
tree; confirm the Development configuration is valid. Then run `verify`. Do not
report successful scaffolding when the solution does not build.

## Adding a Project Later

A new production project, layer, or assembly, or a change to the reference
graph, is Reserved (CLAUDE.md, Decision Control) — run `architecture-decision`
first. After approval:

1. identify the project's architectural or technical responsibility;
2. add only the minimum required references, preserving dependency direction;
3. update shared build/package configuration when necessary;
4. build and test the affected solution.

Adding a focused test project needs no approval but follows step 7.

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

A structure task is complete when: the physical structure matches the
requested scope; project references respect the architecture rules; the
approved baseline technology is used; no unnecessary projects or speculative
directories were introduced; the backend builds; the frontend builds when
present; relevant tests pass; the local Development configuration is usable;
no unrelated code was reorganized.
