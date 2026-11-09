---
name: project-structure
description: Use when creating a new solution or application, adding or removing projects, adding the frontend workspace, or reorganizing repository-level structure, shared build files, project references or test projects.
---
Kind: WF | Scope: repo/meta | Capability: — | Loading: on invocation (routed from CLAUDE.md)

# Project Structure

Scaffolding and restructuring procedure. Layout, solution format and shared build files: decision register → Repository defaults. Structure standard: `.claude/rules/common/repository-structure.md`. Slot-specific steps come from the selected modules' workflow facets (decision register → Capability selection); do not redefine their content here.

## 1. Determine the scope

Before creating files, decide what the request actually needs: backend, frontend, test projects, documentation, external integrations, mapping, containerization. Do not scaffold optional infrastructure, conditional technologies or anything the register lists as not adopted merely because it may be useful later; typical speculative additions are SharedKernel or BuildingBlocks projects, an EventBus or messaging, Domain Events or Specifications, microservices, Kubernetes or cloud-specific projects, deployment manifests and state-management frameworks. Adding a production project or layer to an existing solution is Reserved.

## 2. Repository-level files

Create only the required top-level directories and repository-wide files:

- the `.slnx` solution: `dotnet new sln --format slnx -n <Name>` (or the SDK's default `.slnx` output);
- `global.json` pinned to the current stable SDK of the approved .NET release (`dotnet new globaljson --sdk-version <version> --roll-forward latestFeature`), never an RC or preview SDK unless explicitly requested;
- `.gitignore` (`dotnet new gitignore`) covering `bin/`, `obj/`, `.vs/`, `node_modules/`, `dist/`, `TestResults/`, `coverage/` and local secret or configuration overrides, without ignoring files that belong to the Development configuration contract;
- `README.md`; `docs/` subdirectories (`architecture/`, `decisions/`, `api/`) only when the corresponding documentation exists.

The template already provides `.editorconfig`, `Directory.Build.props` and `Directory.Packages.props`; keep them, and keep project-specific settings in their projects.

## 3. Backend projects and references

Follow the architecture workflow facet: projects, references, directories per layer, then `node .claude/scripts/check-architecture.mjs`.

## 4. Packages

Use the approved baseline from the decision register and add conditional packages only when their capability is needed. Every package goes through `add-dependency`; resolve versions at install time and never copy versions from examples or older content.

## 5. Persistence

Follow the persistence workflow facet → Setup (provider package, registration, Development configuration, seeder, initial migration). Do not add production credentials or production migration automation.

## 6. Test projects

Create only useful test projects, placed by the architecture workflow facet and created with the backend-testing workflow facet, including its architecture-conformance adapter in the integration-test project. Frontend unit and component tests stay inside the frontend workspace.

## 7. Frontend workspace

When the scope includes a frontend, follow the frontend workflow facet → Scaffold the workspace, under `frontend/<Name>.Web/`.

## 8. Minimal internal directories

Inside each project, create only the directories the initial implementation needs.

## 9. Verify

Before declaring scaffolding complete: restore backend dependencies, build the solution, build the frontend when present, run the relevant tests when present, inspect project references (`check-architecture.mjs`) and the final repository tree, and confirm that the Development configuration is valid. Then run `verify`. Do not report successful scaffolding when the generated solution does not build.

## Adding or reorganizing projects later

Use the architecture workflow facet sections "Adding a project later" and "Reorganizing an existing solution".

## Completion checklist

- Physical structure matches the requested scope; no unnecessary projects or speculative directories (`repository-structure.md`).
- Project references respect the architecture standards (`check-architecture.mjs` passes).
- Approved baseline technology is used (decision register).
- The backend builds, the frontend builds when present, relevant tests pass, and the local Development configuration is usable.
- No unrelated code was reorganized.
