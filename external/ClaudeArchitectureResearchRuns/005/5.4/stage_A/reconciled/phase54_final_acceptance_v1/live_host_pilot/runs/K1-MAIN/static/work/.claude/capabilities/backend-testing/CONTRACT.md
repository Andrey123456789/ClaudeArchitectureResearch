> Kind: — (slot contract) | Scope: repo/meta | Capability: backend-testing | Loading: not loaded (read by `architecture-decision`, `template-maintenance`, and the structure checker)

# Slot Contract: backend-testing

- Slot type: required leaf
- Cardinality: exactly one implementation
- Binds: architecture (test-project placement and references belong to the frame)

The framework-neutral testing standard (`.claude/rules/backend-tests/testing.md`) stays unchanged when the implementation is replaced. The knowledge facet keeps the shared skill name `dotnet-testing`.

## Required items

| Item | An implementation must provide |
|---|---|
| `framework-standard` | The default-framework standard for backend tests |
| `integration-host-binding` | How integration tests host the API (declared property) |
| `knowledge` | The `dotnet-testing` knowledge facet |
| `test-scaffold` | A scaffolding facet for creating test projects |
| `framework-consistency-check` | A deterministic check that flags additional test frameworks |

## Facet roles

Role-named facet locations; every implementation provides exactly these (file names never change with the implementation).

| Kind | Scope | Location |
|---|---|---|
| DEC | common | `docs/architecture/decision-register.md` (capability-selection row) |
| STD | backend-tests | `.claude/rules/backend-tests/test-framework.md` |
| KNW | backend-tests | knowledge facet named in the decision register |
| WF | backend-tests | `.claude/skills/project-structure/references/test-setup.md` |
| ENF | backend-tests | `.claude/scripts/facets/test-framework.cjs` |
