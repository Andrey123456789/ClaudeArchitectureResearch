---
name: project-structure
description: >
  Scaffold or restructure the physical solution: repository layout, backend
  projects and references, test projects, frontend workspace, shared build
  files, Development persistence, structural verification. Use when creating a
  new solution, adding/removing projects, or reorganizing repository structure.
---

> Kind: WF | Scope: common | Capability: — | Loading: on-demand workflow

# Project Structure

Read first — path-scoped standards have not loaded yet when no backend or frontend files exist: `.claude/rules/common/structure.md`, `.claude/rules/backend/architecture-style.md`, `.claude/rules/backend-tests/test-projects.md`, `.claude/rules/backend/dependencies.md`, and `.claude/rules/frontend/frontend.md` when frontend scope exists. The approved stack and default layout live in the decision register. This workflow owns the scaffolding procedure and does not redefine them.

## References (read according to the task — not all at once)

| Reference | Role | Read when |
|---|---|---|
| `references/solution-layout.md` | Repository layout, shared build files, docs | creating a repository/solution, reorganizing top-level directories, placing shared files |
| `references/backend-layout.md` | Architecture frame: backend projects, folders, references | creating or reorganizing backend projects or project references |
| `references/test-setup.md` | Backend-testing facet: test project creation | adding backend test projects |
| `references/frontend-setup.md` | Frontend facet: workspace creation | creating the frontend workspace |

Persistence setup is owned by `persistence-change` (section A).

## Goals

Explicit project boundaries; dependency direction enforced through project references; production projects, test projects, frontend, and documentation organized per the layout default; approved technology only; no speculative projects, abstractions, or directories; an immediately buildable result verified before completion.

## Scaffolding procedure

1. **Determine scope** — backend, frontend, test projects, documentation, external integrations, mapping, containerization. Do not scaffold optional infrastructure because it may be useful later (Docker only when containerization is needed).
2. **Use the approved stack** from the decision register; conditional technologies only when their capability is required. Resolve package versions at install time through `add-dependency`; never copy versions from examples or older template content.
3. **Repository level** — read `references/solution-layout.md`; create only required top-level directories and shared configuration files.
4. **Backend projects and references** — read `references/backend-layout.md`; create the four backend projects and only the references it lists. Never add an outward reference to make compilation easier. Projects and project references change the project reference graph (Reserved): first record the requested scaffold through `architecture-decision` — its accepted decision lists each project reference as `From -> To` — because the dependency and reference hook blocks unrecorded `dotnet add/remove … reference` commands and reports unrecorded reference changes after edits.
5. **Test projects** — read `references/test-setup.md`; create only useful test projects (placement and references per `references/backend-layout.md`).
6. **Frontend** — when frontend scope exists, read `references/frontend-setup.md` and create the workspace under `frontend/<Name>.Web/`. Frontend architecture belongs to the frontend standards and knowledge facet; do not duplicate it here.
7. **Minimal internal directories** — only directories the initial implementation needs; no empty trees for hypothetical capabilities.
8. **Development persistence** — run `persistence-change` (initial setup). Never add Production credentials, and do not wire automatic Production migration at normal application startup; a separately approved, controlled deployment-time migration step belongs to `delivery-change`.
9. **Verify** — restore backend dependencies; build the .NET solution; build the frontend when present; run relevant tests when present; inspect project references (`node "<root>/.claude/scripts/check-manifests.cjs"`; `<root>`: the active repository root, command form in `verify`); inspect the final repository tree; confirm the Development configuration is valid. Then run `verify`. Never report successful scaffolding when the result does not build.

## Adding a project later

1. Determine whether a new assembly is actually justified — a new production project or layer is Reserved (`architecture-decision`).
2. Identify its architectural/technical responsibility.
3. Add only the minimum required references, preserving dependency direction; each new reference is recorded first (`architecture-decision`).
4. Update shared build/package configuration when necessary.
5. Build and test the affected solution.

Never split code into additional projects merely to make the architecture look more sophisticated.

## Reorganizing an existing solution

1. Inspect the current tree and project references.
2. Identify a concrete structural problem.
3. Preserve behavior; move code in small reviewable steps.
4. Update namespaces and references consistently; avoid unrelated feature work.
5. Verify after restructuring.

Do not force an established project to match this template when doing so provides no concrete value.

## Do not introduce by default

MediatR, CQRS handler trees, Vertical Slice Architecture, Domain Events, Specifications, SharedKernel, BuildingBlocks, EventBus, messaging, microservices, Kubernetes, cloud-specific projects, state-management frameworks — each requires an approved need (decision register; `CLAUDE.md`, Decision control).

## Completion

The task is complete when the structure matches the requested scope, references respect the architecture, approved technology is used, no unnecessary projects or speculative directories exist, the backend builds, the frontend builds when present, relevant tests pass, the local Development configuration is usable, and no unrelated code was reorganized.
