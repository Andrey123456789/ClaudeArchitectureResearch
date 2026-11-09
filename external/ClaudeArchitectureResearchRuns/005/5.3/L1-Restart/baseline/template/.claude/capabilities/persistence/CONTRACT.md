> Level: 2-technology · Owns: persistence slot contract (maintainer metadata) · Scope: backend · Loading: never auto-loaded

# Slot Contract: persistence (required leaf)

Covers more than the ORM name: access and commit-boundary binding, migrations, seeding, provider variant, observable string-comparison defaults, relational testing expectations, and implementation-specific workflow and enforcement. Placement comes from the architecture frame; this slot supplies technique.

## Required facets

| Facet | Form | Level | Loading | Must provide |
| --- | --- | --- | --- | --- |
| `persistence.access` | rule | 2 | path: backend | confinement of the implementation, repository-contract leak rule, bindings for persistence context, commit boundary, relational fidelity |
| `persistence.seeding` | rule | 2 | path: backend | Development seeding mechanism and constraints |
| `persistence.dev-config` | rule | 3 | path: backend | local Development connection default |
| `persistence.workflow` | workflow-read procedure | 2 | read by workflows | model/seed co-change, migration creation and review, schema-affecting setting changes |
| `persistence.commands` | workflow-read reference | 2 | read by workflows | scaffold packages, migration and verification commands |
| `persistence.enforcement` | enforcement data (JSON) | 2 | hooks, scripts | packages forbidden in inner roles, model/seed/migration path globs |
| knowledge skill | skill | 2 | on demand | implementation technique |

## Declared properties (selection record)

Provider variant, default string-comparison/case-sensitivity semantics, migration mechanism, seeding mechanism.

## Obligations

- A missing required facet is a conformance failure: raise a Decision Request instead of shipping the module.
- Replacing the implementation (for example an ORM with a micro-ORM) must not silently lose migration or seeding semantics; the new module states its migration and seeding mechanisms explicitly.
- A database-provider change (one relational provider for another) is a variation inside this slot, not a new slot: update the declared properties, `persistence.dev-config`, the relational-fidelity binding, and commands. It is Reserved and observable string-comparison changes need approval.
