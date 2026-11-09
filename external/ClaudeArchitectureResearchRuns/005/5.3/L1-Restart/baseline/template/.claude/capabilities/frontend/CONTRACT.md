> Level: 2-technology · Owns: frontend slot contract (maintainer metadata) · Scope: frontend · Loading: never auto-loaded

# Slot Contract: frontend (optional leaf)

Framework-neutral frontend structural policy stays outside the module in `.claude/rules/0-core/frontend.md`; browser security stays in `.claude/rules/0-core/security.md`; package-manager conventions stay in `.claude/rules/3-project/package-management.md`.

## Required facets (when selected)

| Facet | Form | Level | Loading | Must provide |
| --- | --- | --- | --- | --- |
| `frontend.framework` | rule | 2 | path: frontend | framework-specific rules |
| `frontend.stack` | rule | 3 | always (imported by `CLAUDE.md`) | selected frontend technology decisions and approved optional libraries |
| `frontend.commands` | workflow-read reference | 2 | read by workflows | scaffold, clean install, build, test, lint, audit commands, build-fix notes |
| `frontend.enforcement` | enforcement data (JSON) | 2 | hooks | manifest deny/approval lists |
| knowledge skill | skill | 2 | on demand | framework technique, examples, security hotspots |

## Removal

Clearing the optional selection removes the frontend without hunting: set the selection row to `none`, delete the files listed in the module manifest, remove the `frontend-stack.md` import line from `CLAUDE.md`, then run `node .claude/scripts/check-instructions.mjs`. Neutral rules stay; they only load for `frontend/**` paths. Changing the selection is Reserved and requires an ADR.
