---
name: project-structure
description: >
  Use when creating a solution, adding or removing projects or project
  references, or reorganizing repository structure: scaffolding procedure and
  structural verification.
---

> Workflow · Owns the scaffolding and restructuring procedure · Placement: architecture frame · Policy: the rules read in step 1

# Project Structure

## References

Read the references the task needs; do not load every reference by default.

- `references/solution-layout.md` — new repository or solution, top-level
  directories, shared repository files.
- `references/backend-layout.md` — backend projects, internal directories,
  project references, and test-project references (architecture frame).

Slot-specific setup lives in each selected implementation's knowledge skill
(names in `docs/capabilities/`): the persistence skill § Project Setup, the
backend-testing skill § Test Project Setup, and the frontend skill
§ Scaffolding.

## Scaffolding Procedure

### 1. Read the Owners

Path rules have not loaded for files that do not exist yet. Read
`.claude/rules/architecture.md`, `.claude/rules/physical-structure.md`, and
`.claude/rules/dependencies.md`; when frontend scope exists, also read
`.claude/rules/frontend.md` and `.claude/rules/frontend-framework.md`.

### 2. Determine Scope

Before creating files, determine what the project actually needs: backend,
frontend, test projects, documentation, external integrations, mapping,
containerization. Do not scaffold optional infrastructure merely because it may
be useful later.

### 3. Use the Approved Stack

Use the approved technologies in `docs/technology-stack.md` and
`docs/capabilities/`; add conditional technologies only when their capability
is required. Resolve every package version at install time through
`add-dependency`; never copy stale versions from examples.

### 4. Create Repository-Level Structure

Follow `references/solution-layout.md`. Create only the required top-level
directories and repository-wide files.

### 5. Create Backend Projects

Follow `references/backend-layout.md` for the normal backend projects and their
internal directories, using the target framework from the technology stack.

### 6. Add Project References

Add only the references listed in `references/backend-layout.md`; project
references enforce the dependency direction of `.claude/rules/architecture.md`.
Do not add an outward dependency to make compilation easier.

### 7. Add Packages

Add baseline packages for capabilities present in the initial project through
`add-dependency`.

### 8. Add Test Projects

Create only useful backend test projects, at the locations and with the
references given in `references/backend-layout.md`, using the backend-testing
skill § Test Project Setup. Frontend unit/component tests and E2E tests stay
inside the frontend workspace.

### 9. Create the Frontend Workspace

When frontend scope exists, create the workspace under `frontend/<Name>.Web/`
following the frontend skill § Scaffolding.

### 10. Add Minimal Internal Directories

Create only directories required by the initial implementation; no empty trees
for hypothetical capabilities.

### 11. Configure Development Persistence

Create the local Development configuration from the persistence skill § Project
Setup. Development data seeding follows `.claude/rules/persistence-technology.md`.
Do not add Production credentials, and do not wire automatic Production migration
at normal application startup; a separately approved, controlled deployment-time
migration step belongs to `verify` § Delivery Changes.

### 12. Verify

Restore backend dependencies, build the .NET solution, build the frontend when
present, run relevant tests, inspect project references
(`node "$(git rev-parse --show-toplevel)/.claude/scripts/check-architecture.js"`,
which works from any directory of the active repository or worktree), inspect
the final tree, and confirm the Development configuration is valid. Then run
`verify`. Do not report successful scaffolding when the generated solution does
not build.

## Adding a Project Later

1. Determine whether a new assembly is justified — a new production project or
   a changed reference graph is Reserved (`CLAUDE.md` § Decision Control).
2. Identify its architectural or technical responsibility.
3. Add only the minimum required references and preserve dependency direction.
4. Update shared build/package configuration when necessary.
5. Build and test the affected solution.

Do not split code into additional projects to make the architecture look more
sophisticated.

## Changing Project References

The pre-tool hook stops `dotnet add/remove ... reference` and
`dotnet reference add/remove` commands until this procedure has been applied.

1. Read `.claude/rules/architecture.md` (§ Dependency Direction, § Test Project
   References) and `references/backend-layout.md` (§ Project References, § Test
   References) if they have not loaded.
2. Classify the change with `CLAUDE.md` § Decision Control. Adding a reference
   that the layout prescribes for projects of the approved structure follows
   the Decided layout (Scaffolding Procedure, step 6); any other change to the
   reference graph is Reserved: raise it through `architecture-decision` first.
3. Re-run the same command with the trailing comment
   `# project-reference: checked`.
4. The post-command hook then runs the architecture check on the resulting
   references; fix every reported error.

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

## Do Not Introduce by Default

Check the scaffold against `CLAUDE.md` § Decision Control,
`docs/capabilities/architecture.md` § Patterns Not Adopted, and
`.claude/rules/physical-structure.md`. Typical items that need an actual
requirement or approval: MediatR, CQRS handler trees, Vertical Slice
Architecture, Domain Events, Specifications, SharedKernel, BuildingBlocks,
EventBus, messaging, microservices, Kubernetes, cloud-specific projects,
state-management frameworks, Docker (conditional technology).

## Completion

A project-structure task is complete when the physical structure matches the
requested scope, project references respect architectural boundaries, the
approved baseline technology is used, no unnecessary projects or speculative
directories were introduced, the backend builds, the frontend builds when
present, relevant tests pass, the local Development configuration is usable,
and no unrelated code was reorganized.
