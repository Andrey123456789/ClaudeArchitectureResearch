> Kind: — (slot contract) | Scope: repo/meta | Capability: frontend | Loading: not loaded (read by `architecture-decision`, `template-maintenance`, and the structure checker)

# Slot Contract: frontend

- Slot type: optional leaf
- Cardinality: zero or one implementation; "none" means no frontend workspace, no facets, and the register row records `none`
- Workspace location: `frontend/<Name>.Web/` (shared layout convention)

The framework-neutral frontend standards (`.claude/rules/frontend/frontend.md`, `.claude/rules/frontend/security.md`, `.claude/rules/frontend/dependencies.md`) stay unchanged when the implementation is replaced.

## Required items

| Item | An implementation must provide |
|---|---|
| `stack-properties` | Declared stack and libraries not added by default (decision register) |
| `framework-standard` | Framework-specific frontend standards |
| `knowledge` | The framework knowledge facet |
| `workspace-scaffold` | A scaffolding facet for creating the workspace |
| `library-check` | A deterministic `package.json` check for non-default libraries and misplaced tooling |
