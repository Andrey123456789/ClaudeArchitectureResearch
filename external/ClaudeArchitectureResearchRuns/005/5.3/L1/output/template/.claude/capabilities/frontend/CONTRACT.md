> Level: 2-technology · Owns: frontend slot contract (maintainer metadata) · Scope: frontend · Loading: never auto-loaded

# Slot Contract: frontend (optional leaf)

Framework-neutral frontend structural policy stays outside the module in `.claude/rules/0-core/frontend.md`; browser security stays in `.claude/rules/0-core/security.md`; package-manager conventions stay in `.claude/rules/3-project/package-management.md`.

## Required facets (when selected)

| Facet | Form | Level | Loading | Must provide |
| --- | --- | --- | --- | --- |
| `frontend.framework` | rule | 2 | path: frontend | framework-specific rules |
| `frontend.stack` | rule | 3 | always (imported by `CLAUDE.md`) | selected frontend technology decisions and approved optional libraries |
| `frontend.commands` | workflow-read reference | 2 | read by workflows | scaffold, clean install, build, test, lint, audit commands, build-fix notes |
| `frontend.enforcement` | enforcement data (JSON) | 2 | hooks | manifest deny/approval lists, framework CLI commands that change dependencies |
| knowledge skill | skill | 2 | on demand | framework technique, examples, security hotspots |

## Removal

Clearing the optional selection removes the frontend without hunting: follow the finite removal steps in the selected module's manifest (selection row `none`, delete the listed files, remove the stack import from `CLAUDE.md`, remove the map rows and module-specific ignore entries), then run the instruction checker. Neutral rules stay; they only load for `frontend/**` paths, and `frontend.*` facet references from workflows then do not apply. Changing the selection is Reserved and requires an ADR.
