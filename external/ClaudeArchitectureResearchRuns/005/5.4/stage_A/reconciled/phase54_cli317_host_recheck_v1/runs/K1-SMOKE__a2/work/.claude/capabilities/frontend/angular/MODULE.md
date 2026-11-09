> Kind: — (module manifest) | Scope: repo/meta | Capability: frontend/angular | Loading: not loaded (read by `architecture-decision`, `template-maintenance`, and the structure checker)

# Module: frontend / angular

- Slot: frontend
- Implementation: angular
- Variant: —
- Names: Angular, angular
- Binds: —

## Facets

| Kind | Scope | File | Loading | Provides |
|---|---|---|---|---|
| DEC | common | `docs/architecture/decision-register.md` | always (capability-selection block) | selection, stack properties, libraries not added by default |
| STD | frontend | `.claude/rules/frontend/frontend-framework.md` | path-scoped | Angular-specific standards |
| KNW | frontend | `.claude/skills/angular/SKILL.md` | on-demand | Angular technique |
| WF | frontend | `.claude/skills/project-structure/references/frontend-setup.md` | read by `project-structure` | workspace scaffolding |
| ENF | frontend | `.claude/scripts/facets/frontend-framework.cjs` | manifest hook, `verify` | non-default library and tooling-category checks |

## Contract coverage

| Item | Provided by |
|---|---|
| `stack-properties` | DEC capability selection |
| `framework-standard` | STD `frontend-framework.md` |
| `knowledge` | KNW `angular` |
| `workspace-scaffold` | WF `frontend-setup.md` |
| `library-check` | ENF `frontend-framework.cjs` |
