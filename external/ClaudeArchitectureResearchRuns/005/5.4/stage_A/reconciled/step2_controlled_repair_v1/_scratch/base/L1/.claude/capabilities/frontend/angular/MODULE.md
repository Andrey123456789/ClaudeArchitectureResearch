> Level: 2-technology · Capability: frontend/angular · Owns: implementation manifest (maintainer metadata) · Scope: frontend · Loading: never auto-loaded

# Module: frontend/angular

Angular workspace at `frontend/<Name>.Web/`, managed with the Angular CLI and npm.

- binds: none
- leak-tokens: Angular, RxJS, NgModule, NgRx, Vitest

## Facets

| Facet | File | Level | Loading |
| --- | --- | --- | --- |
| `frontend.framework` | `.claude/rules/2-technology/frontend/framework.md` | 2-technology | path |
| `frontend.stack` | `.claude/rules/3-project/frontend-stack.md` | 3-project | always (imported by `CLAUDE.md`) |
| `frontend.commands` | `.claude/capabilities/frontend/angular/commands.md` | 2-technology | workflow-read |
| `frontend.enforcement` | `.claude/capabilities/frontend/angular/enforcement.json` | 2-technology | enforcement data |
| `frontend.knowledge` | `.claude/skills/angular/SKILL.md` | 2-technology | on demand |

## Removal

Delete every file in the table plus this directory, remove the `@.claude/rules/3-project/frontend-stack.md` line from `CLAUDE.md`, set the frontend selection row to `none`, remove the module's rows from `.claude/INSTRUCTION_MAP.md`, and run `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.mjs"`.
