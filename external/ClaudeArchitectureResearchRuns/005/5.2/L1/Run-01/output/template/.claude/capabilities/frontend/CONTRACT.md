> Level: 2-technology | Capability: frontend (slot contract) | Owns: requirements every frontend implementation must satisfy | Scope: frontend | Loads: never (maintainer metadata)

# Slot Contract — `frontend` (optional leaf)

Zero or one implementation is selected. Framework-neutral frontend structure
stays outside the module (`.claude/rules/1-architecture/frontend-structure.md`);
it is inert when no frontend exists. The implementation supplies only
framework-specific material.

## Required facets (when selected)

| Facet | Level | Location | Loading | Must provide |
|---|---|---|---|---|
| `frontend.decision` | 3 | `.claude/rules/3-project/` rule with `Capability:` header | always (CLAUDE.md import) | selected framework stack and default library limits |
| `frontend.rules` | 2 | `.claude/rules/2-technology/` rule named by role, with `Capability:` header | path `frontend/**/*` | framework-specific rules |
| `frontend.knowledge` | 2 | skill | on demand | framework technique, testing and security notes |
| `frontend.commands` | 2 | `<module>/commands.md` | read by `verify`, `build-fix`, `delivery`, `security-scan` | install, build, test, lint, audit commands; framework-specific build-fix notes |
| `frontend.scaffold` | 3 | `<module>/scaffold.md` | read by `project-structure` | workspace creation in `frontend/<Name>.Web/` |
| `frontend.check` | — | `<module>/check.json` | read by hooks and `check-packages.cjs` | framework dependency commands; packages not added by default |

## Clearing the selection

Remove the `frontend` row from the capability selection record and the
`frontend.decision` import from `CLAUDE.md`, delete the module directory and
every facet file listed in its `MODULE.md`, remove the slot's rows from the
capability view in `.claude/INSTRUCTION-MAP.md`, then run
`node .claude/scripts/check-instructions.cjs`. No other artifact names the
framework, so nothing else needs editing; every `frontend.*` workflow step is
skipped while the slot is empty.
