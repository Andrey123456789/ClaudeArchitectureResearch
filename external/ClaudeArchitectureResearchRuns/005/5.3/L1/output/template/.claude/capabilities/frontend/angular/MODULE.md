> Level: 2-technology · Capability: frontend/angular · Owns: implementation manifest (maintainer metadata) · Scope: frontend · Loading: never auto-loaded

# Module: frontend/angular

Angular workspace at `frontend/<Name>.Web/`, managed with the Angular CLI and npm.

- binds: none
- leak-tokens: Angular, RxJS, NgModule, NgRx, Vitest, ng add, ng update, @angular/, .angular/

## Facets

| Facet | File | Level | Loading |
| --- | --- | --- | --- |
| `frontend.framework` | `.claude/rules/2-technology/frontend/framework.md` | 2-technology | path |
| `frontend.stack` | `.claude/rules/3-project/frontend-stack.md` | 3-project | always (imported by `CLAUDE.md`) |
| `frontend.commands` | `.claude/capabilities/frontend/angular/commands.md` | 2-technology | workflow-read |
| `frontend.enforcement` | `.claude/capabilities/frontend/angular/enforcement.json` | 2-technology | enforcement data |
| `frontend.knowledge` | `.claude/skills/angular/SKILL.md` | 2-technology | on demand |

## Removal

1. Delete every file in the table (the knowledge skill with its directory) plus this directory.
2. Remove the `@.claude/rules/3-project/frontend-stack.md` line from `CLAUDE.md`.
3. Set the frontend row of the selection record to `| frontend | optional | none | — | — |`.
4. Remove the rows naming these files from `.claude/INSTRUCTION_MAP.md` (level tables and capability view) and the module's framework/stack pointers from its policy locator.
5. Remove the `.angular/` line from `.gitignore`.
6. Run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.mjs"`; it reports any remaining reference to this module.
