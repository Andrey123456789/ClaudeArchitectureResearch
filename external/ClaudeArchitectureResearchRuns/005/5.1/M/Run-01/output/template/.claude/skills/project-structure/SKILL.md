---
name: project-structure
description: >
  Use when creating a new solution, scaffolding the backend or Angular
  workspace, adding or removing projects, changing project references, or
  reorganizing repository-level structure. Scaffolding and restructuring
  procedure with structural verification.
---

> Owns: scaffolding and restructuring procedure, structural completion checks | Scope: common | Loads: workflow (CLAUDE.md routing); private references references/solution-layout.md, references/backend-layout.md

# Project Structure

Structure policy lives elsewhere and this workflow does not redefine it:
repository layout, solution format, and stack in `docs/technology-stack.md`;
speculative-structure limits in `CLAUDE.md` (Core Defaults); dependency
direction and test-project references in `.claude/rules/architecture.md`.

## 1. Read the Governing Policy

Path-scoped rules have not loaded yet for files that do not exist. Read
`.claude/rules/architecture.md` and `.claude/rules/dependencies.md` before
creating anything; read `.claude/rules/persistence.md` before configuring
Development persistence and `.claude/rules/angular.md` before creating frontend
code.

## 2. Determine Scope

Decide what the request actually needs — backend, Angular frontend, test
projects, documentation, external integrations, mapping, containerization. Do
not scaffold optional infrastructure, directories, or test projects because they
may be useful later. A new production project/layer or reference-graph change
in an existing solution is Reserved (`architecture-decision`).

## 3. Create Repository-Level Files

Read `references/solution-layout.md`. Create only the required top-level
directories and repository-wide files (`<Name>.slnx`, `global.json` pinned to the
current stable SDK of the target .NET release with an explicit `rollForward`
policy, `.gitignore`, `README.md`). This template already provides
`.editorconfig`, `Directory.Build.props`, and `Directory.Packages.props`; adjust
them rather than replacing them.

## 4. Create Backend Projects

Read `references/backend-layout.md`. Create the needed Clean Architecture
projects under `backend/` (Domain, Application, Infrastructure, Api) targeting
the approved .NET version, and add only the project references the dependency
direction allows. Never add an outward reference to make compilation easier.

## 5. Add Packages

Install baseline packages for capabilities present in the initial project only,
each through `add-dependency` (versions resolved at install time, never copied
from examples). Conditional technologies wait for their trigger.

## 6. Add Test Projects

Create only useful backend test projects under `backend/` — typically
`<Name>.Application.Tests` and `<Name>.IntegrationTests`; add
`<Name>.Domain.Tests` only when Domain has non-trivial behavior worth testing
independently, and `<Name>.Infrastructure.Tests` only for a concrete need. Use
NUnit. Angular unit/component tests stay in the Angular workspace (colocated
per current Angular conventions); E2E tests, when adopted, live under
`frontend/<Name>.Web/e2e/`.

## 7. Create the Angular Application

When frontend scope exists, create the workspace under `frontend/<Name>.Web/`
with the current Angular CLI and the baseline from `docs/technology-stack.md`
(for example `ng new <Name>.Web --directory frontend/<Name>.Web --routing
--style scss --strict`; add zoneless/Material per the current CLI options).
Feature layout: `angular` skill.

## 8. Add Minimal Internal Directories

Inside each project create only directories required by the initial
implementation; no empty trees for hypothetical capabilities.

## 9. Configure Development Persistence

For SQL Server, configure `appsettings.Development.json` per `persistence.md`
(see the LocalDB example in `references/solution-layout.md`). Development
seeding follows `persistence.md` with technique in `ef-core`. Add no Production
credentials or Production migration automation.

## Adding a Project Later

1. Confirm a new assembly is actually justified and approved.
2. Identify its single responsibility.
3. Add only the minimum references that preserve dependency direction.
4. Update shared build/package configuration when necessary.
5. Build and test the affected solution.

## Reorganizing an Existing Solution

1. Inspect the current tree and project references.
2. Name the concrete structural problem being solved.
3. Preserve behavior; move code in small reviewable steps.
4. Update namespaces and references consistently; avoid unrelated feature work.
5. Verify after restructuring.

Do not force an established project to match this template when that provides no
concrete value.

## Completion

Before declaring structure work complete:

- [ ] backend dependencies restore and the .NET solution builds;
- [ ] the Angular application builds when present;
- [ ] relevant tests pass when present;
- [ ] `node .claude/scripts/check-manifests.mjs` passes (references, Central
      Package Management);
- [ ] the final tree matches the requested scope with no speculative projects or
      empty directories (CLAUDE.md, Core Defaults);
- [ ] local Development configuration is valid;
- [ ] no unrelated code was reorganized.

Then run `verify`. Never report successful scaffolding for a solution that does
not build.
