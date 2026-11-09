> **Capability contract** · Slot: frontend (optional leaf) · Owns: required facets and properties, enable/disable and replacement obligations · Scope: frontend · Loading: maintainer-only (read by `template-maintenance` and the checkers)

# Frontend Slot Contract

The optional frontend slot supplies the frontend framework. Framework-independent
frontend structure policy stays outside the module (`frontend.md`), as do npm
and lockfile policy (`dependencies.md`) and browser security (`security.md`).

## Required Facets (when enabled)

- `frontend-stack` — always-loaded planning record of the selected technology
  baseline, default-excluded libraries, and conditional E2E tooling.
- `frontend-framework-rule` — path-loaded framework-specific rule for the
  frontend workspace.
- `frontend-knowledge` — on-demand knowledge skill with technique, scaffold and
  verify commands, build-fix and security-review cues.

## Required Properties (when enabled)

- `workspace` — workspace location.
- `packageManager` — package manager.
- `commands` — scaffold, build, and test commands.
- `notByDefaultPackages` — packages excluded by default (checked by
  `check-dependencies.mjs`).

## Enable, Disable, Replace

Disabling clears the selection row (`none (disabled)`), removes the facet-table
row and the import of the stack facet from `docs/capability-selection.md`, deletes
the module's facets and directory, and removes their entries from
`.claude/MAP.md`; `frontend.md` remains. Other artifacts refer to the slot's facets
only by role, so nothing else changes. Replacing the framework supplies the same facet roles and
properties under the role-based file names.

```json
{
  "slot": "frontend",
  "status": "optional",
  "frame": false,
  "requiredFacets": ["frontend-stack", "frontend-framework-rule", "frontend-knowledge"],
  "requiredProperties": ["workspace", "packageManager", "commands", "notByDefaultPackages"]
}
```
