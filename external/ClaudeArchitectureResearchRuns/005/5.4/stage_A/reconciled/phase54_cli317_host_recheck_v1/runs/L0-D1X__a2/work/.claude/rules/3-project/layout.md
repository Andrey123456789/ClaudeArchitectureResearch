---
paths:
  - "*.slnx"
  - "backend/**/*.csproj"
  - "frontend/*/angular.json"
---

> Level: 3 Project · Owns: concrete layer-to-project mapping, test-project placement and typical references, frontend workspace location · Scope: backend, backend-tests, frontend · Loads: path rule · Depends on: CLAUDE.md, .claude/rules/1-architecture/backend-layers.md, .claude/rules/1-architecture/code-organization.md

# Repository Layout

Repository defaults (format, shared build files, top-level separation): `decisions.md`. Directory trees and scaffolding steps: `project-structure`.

## Layer-to-project mapping

| Layer (`1-architecture/backend-layers.md`) | Project |
|---|---|
| Domain | `backend/<Name>.Domain/` |
| Application | `backend/<Name>.Application/` |
| Infrastructure | `backend/<Name>.Infrastructure/` |
| Api | `backend/<Name>.Api/` (contains `Program.cs`) |

`ProjectReference` entries implement the Level 1 dependency direction; the project hook rejects outward references (Domain → any layer, Application → Infrastructure/Api, Infrastructure → Api).

## Test projects

Create only useful test projects, beside the production projects under `backend/`. Typical narrowest references:

| Test project | References |
|---|---|
| `<Name>.Application.Tests` | Application (Domain as needed) |
| `<Name>.IntegrationTests` | Api (exercises the host through `WebApplicationFactory<Program>`) |
| `<Name>.Domain.Tests` — only when Domain has non-trivial behavior | Domain |
| `<Name>.Infrastructure.Tests` — only for a concrete need | Infrastructure (narrower as required) |

## Frontend

The Angular workspace lives at `frontend/<Name>.Web/` and owns its `package.json`, `package-lock.json`, `angular.json`, tsconfig files, `src/`, and `public/`. Unit and component tests stay inside the workspace (colocated by Angular convention); E2E tests, when adopted, live in `frontend/<Name>.Web/e2e/`. Never place frontend tests under `backend/`.
