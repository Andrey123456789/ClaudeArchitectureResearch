> Kind: — (slot contract) | Scope: repo/meta | Capability: architecture | Loading: not loaded (read by `architecture-decision`, `template-maintenance`, and the structure checker)

# Slot Contract: architecture

- Slot type: required frame
- Cardinality: exactly one implementation
- Binds: — (the frame binds no slot; leaves bind to it)
- Stable role vocabulary usable by non-slot artifacts: Domain, Application, Infrastructure, Api (host and composition root), Application Service, repository contract, Unit of Work (`IUnitOfWork`, commit boundary), test projects.

Placement belongs to the frame; technique belongs to the leaves (persistence, backend-testing), which declare their frame bindings with `Binds:`.

## Required items

| Item | An implementation must provide |
|---|---|
| `role-map` | The concrete projects for each backend role under `backend/<Name>.<Layer>/` |
| `dependency-direction` | Allowed and forbidden references between roles |
| `domain-modeling` | The default domain modeling style and when richer modeling needs approval |
| `use-case-orchestration` | The default orchestration mechanism for use cases |
| `commit-boundary-placement` | Where the commit-boundary contract lives and who decides to commit |
| `composition-root` | Where dependency registration and composition happen |
| `transport-contracts` | Where transport-specific contracts live relative to Application models |
| `test-project-placement` | Test project location and allowed production references |
| `not-adopted-styles` | Declared styles/patterns that are not adopted (decision register) |
| `scaffold-layout` | A scaffolding facet for creating the backend projects and references |
| `reference-check` | A deterministic check of project references |

## Facet roles

Role-named facet locations; every implementation provides exactly these (file names never change with the implementation).

| Kind | Scope | Location |
|---|---|---|
| DEC | common | `docs/architecture/decision-register.md` (capability-selection row) |
| STD | backend | `.claude/rules/backend/architecture-style.md` |
| STD | backend-tests | `.claude/rules/backend-tests/test-projects.md` |
| WF | backend | `.claude/skills/project-structure/references/backend-layout.md` |
| ENF | backend | `.claude/scripts/facets/architecture-style.cjs` |
