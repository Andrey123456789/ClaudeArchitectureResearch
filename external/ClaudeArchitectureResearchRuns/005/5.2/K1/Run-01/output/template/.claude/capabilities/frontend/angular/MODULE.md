Kind: DEC | Scope: frontend | Capability: frontend/angular | Loading: module manifest, read on demand

# Module: frontend/angular

- slot: frontend (optional leaf)
- implementation: angular
- aliases: Angular, angular, NgModule, RxJS, @angular
- binds: —

## Facets

| Kind | Facet | Scope | Loading |
|---|---|---|---|
| DEC | `docs/architecture/decision-register.md` (section "frontend → angular") | common | always (imported by CLAUDE.md) |
| STD | `.claude/rules/frontend/frontend-framework.md` | frontend | path-scoped (frontend/**) |
| KNW | `.claude/skills/angular/SKILL.md` | frontend | on invocation |
| WF | `.claude/capabilities/frontend/angular/workflow-facet.md` | frontend | read by `project-structure`, `verify`, `build-fix`, `code-review`, `security-scan` |
| ENF | `.claude/scripts/facets/frontend/enforcement.json` | frontend | read by the dependency hooks, `check-manifests.mjs` and the Stop hook |

## Declared properties

Decided properties (stack, libraries not added by default, E2E tool) are recorded in the decision register section of this module. Implementation facts:

- Workspace: `frontend/<Name>.Web/`, created by the Angular CLI; unit and component tests are colocated (`*.spec.ts`); E2E tests, when used, live in `frontend/<Name>.Web/e2e/`.
- Package manager: npm with a committed `package-lock.json`.
