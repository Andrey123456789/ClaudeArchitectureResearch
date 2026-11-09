> Level: 2-technology | Capability: frontend/angular (module manifest) | Owns: facet list and declared properties of the Angular frontend implementation | Scope: frontend | Loads: never (maintainer metadata)

# Module — `frontend/angular`

- Slot: `frontend` (optional leaf) — selected.
- binds: none (the frontend reaches the backend only through the published
  HTTP contract).

- leak terms: `Angular`

## Facets

| Facet | File | Level | Loading |
|---|---|---|---|
| `frontend.decision` | `.claude/rules/3-project/frontend-stack.md` | 3 | always (CLAUDE.md import) |
| `frontend.rules` | `.claude/rules/2-technology/frontend-framework.md` | 2 | path `frontend/**/*` |
| `frontend.knowledge` | `.claude/skills/angular/SKILL.md` | 2 | on demand |
| `frontend.commands` | `.claude/capabilities/frontend/angular/commands.md` | 2 | read by workflows |
| `frontend.scaffold` | `.claude/capabilities/frontend/angular/scaffold.md` | 3 | read by `project-structure` |
| `frontend.check` | `.claude/capabilities/frontend/angular/check.json` | — | hooks, `check-packages.cjs` |

## Declared properties

| Property | Value |
|---|---|
| workspace | `frontend/<Name>.Web/` |
| package manager | npm (`package-lock.json` committed) |
| unit test runner | Vitest (via the Angular CLI) |
| E2E (conditional) | Playwright under `frontend/<Name>.Web/e2e/` |
