---
name: project-structure
description: >
  Run when scaffolding a solution or projects, adding or removing projects,
  changing project references, or reorganizing repository structure.
---

> **Workflow skill** · Owns: scaffolding and restructuring procedure · Scope: common · Loading: on demand (routed from `CLAUDE.md` → Procedures and `development-workflow`)

# Project Structure

## Purpose

Use this skill when creating a new solution or changing its physical project
structure.

Architectural policy is defined in `.claude/rules/architecture-style.md`;
structural policy in `.claude/rules/repository-structure.md`; the approved stack
and layout in `docs/technology-stack.md` and `docs/capability-selection.md`
(always loaded).

Do not redefine or override architecture rules here.

Detailed implementation guidance belongs to the relevant specialized skills.

## References

Read supporting references according to the task.

### `references/solution-layout.md`

Read when:

- creating a new repository/solution;
- reorganizing top-level directories;
- adding frontend/tests/docs;
- deciding where shared repository files belong.

### `references/backend-layout.md` (architecture frame facet)

Read when:

- creating or reorganizing Domain, Application, Infrastructure, or API projects;
- adding project references;
- deciding where backend files/directories belong.

Do not load every reference merely because this skill was triggered.

## Goals

When scaffolding or reorganizing a solution:

1. Keep project boundaries explicit.
2. Enforce dependency direction through project references.
3. Keep production projects, test projects, frontend, and documentation clearly
   organized according to the repository layout.
4. Use the repository's approved technology stack.
5. Avoid speculative projects, abstractions, and directories.
6. Keep the generated solution immediately buildable.
7. Verify the resulting structure before completion.

## Default Shape

The normal repository contains:

```text
backend/
    <Name>.<Layer>/          layer projects defined by the architecture frame
    <Name>.<Layer>.Tests/    test projects following the frame's test-project role
    <Name>.IntegrationTests/

frontend/
    <Name>.Web/              frontend workspace (when the frontend capability is enabled)

docs/
```

This is a target organization, not a requirement to create every optional
directory or test project immediately.

Read `references/solution-layout.md` for the complete repository shape and
`references/backend-layout.md` for the backend projects.

## Scaffolding Procedure

### 1. Determine Scope

Before creating files, determine what the requested project actually needs:

```text
backend
frontend
test projects
documentation
external integrations
mapping
containerization
```

Do not scaffold optional infrastructure merely because it may be useful later.

### 2. Apply the Technology Stack

Use the baseline stack from `docs/technology-stack.md` and the selected
capabilities from `docs/capability-selection.md`. Do not silently substitute
alternative frameworks or libraries. Add conditional technologies only when the
project actually requires their capability.

### 3. Create Repository-Level Structure

Read:

```text
references/solution-layout.md
```

Create only the required top-level directories and repository-wide configuration
files.

### 4. Create Backend Projects

Read:

```text
references/backend-layout.md
```

Create the layer projects the architecture frame defines, using the approved .NET
target from `docs/technology-stack.md`.

### 5. Add Project References

Add only the references described in:

```text
references/backend-layout.md
```

Project references must enforce the dependency direction defined by
`architecture-style.md`. Do not add an outward dependency merely to make
compilation easier. Check the graph with:

```bash
node .claude/scripts/check-architecture.mjs
```

### 6. Add Packages

Use the approved baseline from `docs/technology-stack.md` and the packages the
selected capabilities declare in their knowledge facets. Resolve package versions
at implementation time through the `add-dependency` workflow; do not copy stale
versions from examples or historical template content.

`docs/technology-stack.md` defines the approved technologies; `dependencies.md`
and `add-dependency` define package version, security, and license policy.

### 7. Add Test Projects

Create only useful test projects. Backend test projects live beside the
production projects under `backend/` (`docs/technology-stack.md`).

Typical locations are:

```text
backend/
    <Name>.Application.Tests/
    <Name>.IntegrationTests/
```

Create `<Name>.Domain.Tests` only when Domain contains non-trivial behavior worth
testing independently; a simple Domain made primarily of entities and enums does
not need a dedicated test project. Add `<Name>.Infrastructure.Tests` or another
focused backend test project only when a concrete testing need justifies it.

Scaffold test projects with the backend-testing capability's commands
(`dotnet-testing` skill → `references/test-framework.md`).

Frontend unit/component tests remain inside the frontend workspace under
`frontend/<Name>.Web/`, normally colocated with the code they test; frontend E2E
tests, when used, also stay there (for example `frontend/<Name>.Web/e2e/`).

Detailed testing strategy belongs to the `dotnet-testing` skill and the frontend
knowledge facet.

### 8. Create the Frontend Workspace

When frontend scope exists and the frontend capability is enabled, create the
workspace under:

```text
frontend/<Name>.Web/
```

Use the frontend capability's stack decision and scaffold commands (frontend
knowledge facet). Frontend structure rules: `frontend.md` and the frontend rule facet; do not
duplicate them here.

### 9. Add Minimal Internal Directories

Inside each project, create directories required by the initial implementation.

Do not generate empty directory trees for hypothetical future capabilities.

### 10. Configure Development Persistence

Create the persistence capability's Development configuration and seeding setup
(`persistence-technology.md` → Provider Configuration and Development Seeding).

Do not add Production credentials (`security.md`) or Production migration
automation (`development-workflow` → Change-Specific Obligations).

### 11. Verify

Before declaring scaffolding complete:

```text
restore backend dependencies
build the .NET solution
build the frontend application when present
run relevant tests when present
inspect project references
inspect the final repository tree
confirm Development configuration is valid
```

Use the `verify` skill for the final completion workflow.

Do not report successful scaffolding when the generated solution does not build.

## Adding a Project Later

When adding a project to an existing solution:

1. Determine whether a new assembly is actually justified; adding a production
   project changes the reference graph and is Reserved (`CLAUDE.md` → Decision
   Control).
2. Identify its architectural/technical responsibility.
3. Add only the minimum required references.
4. Preserve dependency direction.
5. Update shared build/package configuration when necessary.
6. Build and test the affected solution.

Do not split code into additional projects merely to make the architecture look
more sophisticated.

## Reorganizing an Existing Solution

Before reorganizing:

1. Inspect the current tree and project references.
2. Identify a concrete structural problem.
3. Preserve behavior.
4. Move code in small reviewable steps.
5. Update namespaces/references consistently.
6. Avoid unrelated feature work.
7. Verify after restructuring.

Do not force an established project to match this template when doing so provides
no concrete value.

## Do Not Introduce by Default

Do not scaffold anything the current requirements do not need. Check against:
Reserved decisions (`CLAUDE.md`), patterns not adopted (`docs/architecture.md`),
speculative structure (`repository-structure.md`), conditional technologies
(`docs/technology-stack.md`), and libraries excluded by default in the frontend
stack decision.

## Completion

A project-structure task is complete when:

- the physical structure matches the requested scope;
- project references respect architectural boundaries;
- approved baseline technology is used;
- no unnecessary projects or speculative directories were introduced;
- backend builds;
- frontend builds when present;
- relevant tests pass;
- local Development configuration is usable;
- no unrelated code was reorganized.
