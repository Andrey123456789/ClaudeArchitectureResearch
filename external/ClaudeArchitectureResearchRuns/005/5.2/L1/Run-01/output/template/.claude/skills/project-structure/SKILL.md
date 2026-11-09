---
name: project-structure
description: >
  Run to create a solution, add or remove projects, or reorganize repository
  structure: scaffolding order, references, test projects, frontend workspace.
---
> Level: 3-project | Owns: scaffolding and restructuring procedure | Scope: common | Loads: on demand (skill)

# Project Structure

Architecture policy is owned by the rules and the architecture frame; this
workflow orders the scaffolding steps and routes to capability facets. Read only
the facets a step needs.

## Goals

Keep project boundaries explicit; enforce dependency direction through project
references; keep backend, tests, frontend, and documentation organized per the
project layout; use the approved stack; avoid speculative projects,
abstractions, and directories; keep the solution buildable; verify the result.

## Scaffolding procedure

1. **Determine scope** — backend, frontend (only when the `frontend` slot is
   selected and requested), test projects, documentation, external
   integrations, mapping, containerization. Do not scaffold optional
   infrastructure because it may be useful later.
2. **Stack** — the project stack and the selected decision facets are always
   loaded; do not substitute alternatives. Conditional technologies wait for a
   concrete need.
3. **Repository-level structure** — read `references/solution-layout.md`;
   create only the required top-level directories and repository-wide files.
4. **Backend projects** — create them per `architecture.layout`, targeting the
   approved .NET version.
5. **Project references** — add only the references allowed by
   `architecture.boundaries`; never add an outward reference to make
   compilation easier. Check with `node .claude/scripts/check-architecture.cjs`.
6. **Packages** — follow `add-dependency` for every package; resolve versions at
   install time and never copy stale versions from examples.
7. **Test projects** — placement and references per `architecture.layout`;
   framework setup per `backend-testing.scaffold`. Create only useful test
   projects.
8. **Frontend** — when in scope, create the workspace per `frontend.scaffold`
   at `frontend/<Name>.Web/`; frontend tests stay inside that workspace.
9. **Internal directories** — only directories the initial implementation
   needs; no empty trees for hypothetical capabilities.
10. **Development persistence** — `persistence.scaffold`, then the initial
    migration via `persistence.workflow`. No Production credentials or
    Production migration automation.
11. **Verify** — restore and build the backend, build the frontend when
    present, run relevant tests, inspect project references, inspect the final
    tree, confirm the Development configuration is valid, then run `verify`.
    Never report successful scaffolding for a solution that does not build.

## Adding a project later

A new production project or layer is Reserved. After approval: identify its
responsibility, add only minimal references allowed by the frame (extend
`architecture.check` with its classification), update shared build/package
configuration when necessary, build and test. Do not split code into extra
projects to make the architecture look more sophisticated.

## Reorganizing an existing solution

1. Inspect the current tree and project references.
2. Identify a concrete structural problem.
3. Preserve behavior.
4. Move code in small reviewable steps.
5. Update namespaces and references consistently.
6. Avoid unrelated feature work.
7. Verify after restructuring.

Do not force an established project to match this template when that provides
no concrete value.

## Not introduced by default

MediatR or other mediator libraries, CQRS handler trees, Vertical Slice
Architecture, Domain Events, Specifications, SharedKernel, BuildingBlocks,
EventBus, messaging, microservices, Kubernetes, cloud-specific projects,
state-management frameworks — each needs a concrete requirement and, where
Reserved, approval. Containers follow the project stack's conditional rule.

## Completion

The physical structure matches the requested scope; references respect the
frame; the approved stack is used; no unnecessary projects or speculative
directories exist; backend and (when present) frontend build; relevant tests
pass; the local Development configuration is usable; nothing unrelated was
reorganized.
