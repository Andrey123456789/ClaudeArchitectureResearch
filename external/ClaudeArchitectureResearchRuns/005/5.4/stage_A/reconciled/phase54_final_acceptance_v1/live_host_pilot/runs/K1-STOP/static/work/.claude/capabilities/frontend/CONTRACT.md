> Kind: — (slot contract) | Scope: repo/meta | Capability: frontend | Loading: not loaded (read by `architecture-decision`, `template-maintenance`, and the structure checker)

# Slot Contract: frontend

- Slot type: optional leaf
- Cardinality: zero or one implementation; "none" means no frontend workspace, no facets, and the register row records `none`
- Workspace location: `frontend/<Name>.Web/` (shared layout convention)
- Binds: — (independent leaf)

The framework-neutral frontend standards (`.claude/rules/frontend/frontend.md`, `.claude/rules/frontend/security.md`, `.claude/rules/frontend/dependencies.md`) stay unchanged when the implementation is replaced.

## Required items

| Item | An implementation must provide |
|---|---|
| `stack-properties` | Declared stack and libraries not added by default (decision register) |
| `framework-standard` | Framework-specific frontend standards |
| `knowledge` | The framework knowledge facet |
| `workspace-scaffold` | A scaffolding facet for creating the workspace |
| `library-check` | A deterministic `package.json` check for non-default libraries and misplaced tooling |

## Facet roles

Role-named facet locations; every implementation provides exactly these (file names never change with the implementation).

| Kind | Scope | Location |
|---|---|---|
| DEC | common | `docs/architecture/decision-register.md` (capability-selection row) |
| STD | frontend | `.claude/rules/frontend/frontend-framework.md` |
| KNW | frontend | knowledge facet named in the decision register |
| WF | frontend | `.claude/skills/project-structure/references/frontend-setup.md` |
| ENF | frontend | `.claude/scripts/facets/frontend-framework.cjs` |

With the selection `none`, these locations are absent; pointers to them from neutral artifacts stay valid and dormant.
