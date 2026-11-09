> **Capability contract** · Slot: persistence (required leaf) · Owns: required facets and properties, replacement obligations · Scope: backend · Loading: maintainer-only (read by `template-maintenance` and the checkers)

# Persistence Slot Contract

The persistence slot supplies the persistence technology and its provider
variant. Placement comes from the architecture frame's stable roles (adapter
layer, persistence-access contract, commit boundary, composition root); the
implementation supplies technique, mechanisms, and technology-specific rules.

## Required Facets

- `persistence-rule` — path-loaded rule for backend code: technology boundary and
  usage inside the adapter layer, development seeding, provider configuration,
  mechanisms.
- `persistence-knowledge` — on-demand knowledge skill with technique and examples.

## Required Properties

- `provider` — provider variant (a provider change stays inside this slot).
- `technologyPackages` and `technologyForbiddenInRoles` — packages that must not
  be referenced by the listed frame roles.
- `commitBoundaryBinding` — how the commit boundary and repositories share one
  scoped persistence context.
- `migrationMechanism` — how schema migrations are created, reviewed, and applied.
- `seedingMechanism` — how Development-only, empty-database, non-migrating,
  non-overwriting, invariant-preserving seeding is implemented.
- `stringComparison` — the observable default string-comparison semantics.
- `relationalTesting` — what provider-fidelity tests run against.
- `coChange` — model, seeder, and migration file patterns for co-change checks
  (role tokens such as `<role:adapter layer>` are resolved through the frame).

## Replacement Obligations

A replacement (for example a different ORM or micro-ORM) must not silently lose
migration or seeding semantics: every required facet and property must be
supplied, and the seeding rules (Development-only, empty-database detection, no
schema creation, no overwrite of existing data, invariant-preserving
representative data, tests owning their setup) must be restated in the new rule
facet. A missing facet or property is a conformance failure and a Decision
Request. A provider change (for example to PostgreSQL) updates `provider`,
`stringComparison`, `relationalTesting`, and the provider configuration section,
and is itself Reserved.

```json
{
  "slot": "persistence",
  "status": "required",
  "frame": false,
  "requiredFacets": ["persistence-rule", "persistence-knowledge"],
  "requiredProperties": ["provider", "technologyPackages", "technologyForbiddenInRoles", "commitBoundaryBinding", "migrationMechanism", "seedingMechanism", "stringComparison", "relationalTesting", "coChange"]
}
```
