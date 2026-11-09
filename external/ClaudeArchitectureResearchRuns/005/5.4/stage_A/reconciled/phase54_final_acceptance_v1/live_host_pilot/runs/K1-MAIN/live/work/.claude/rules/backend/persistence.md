---
paths:
  - "backend/**/*"
---

> Kind: STD | Scope: backend | Capability: — | Loading: path-scoped (frontmatter paths)

# Persistence Standard (technology-neutral)

The selected persistence technology adds its rules in `persistence-technology.md`.

## Repository contracts

- Default: specific repository interfaces that represent actual, cohesive Application persistence needs, not table-mirroring generic CRUD contracts. Repository interfaces are defined in Application and implemented in Infrastructure.
- Repository interfaces must not expose `IQueryable<T>`, database-context or entity-set types, query expressions, or provider-specific types; query construction stays in Infrastructure. Return materialized entities, collections, projections, or explicit result models.
- Application must not depend on `IGenericRepository<T>` or another generic CRUD contract. A generic repository or base class may exist only as an Infrastructure implementation detail that removes real duplication.

## Data access safety

- Database access must be parameterized; never build SQL by concatenating untrusted input. This includes raw SQL, micro-ORMs, and ADO.NET.

## Development seeding

- Default: an empty Development database receives a small, deterministic, representative seed dataset covering the main meaningful states and relationships.
- Automatic seeding runs only in Development; never automatically seed Production. The development seeder is not test setup; tests own their own setup.
- When representative data already exists, leave it unchanged. Never use the seeder for automatic synchronization, repair, upgrade, overwrite, or recreation of an existing Development database; developers recreate local databases explicitly when they need a fresh dataset.
- Seed entities must preserve current Domain invariants and valid relationships; prefer readable deterministic examples over exhaustive or random combinations.

Procedure for model, mapping, migration, and seed changes: `persistence-change`.
