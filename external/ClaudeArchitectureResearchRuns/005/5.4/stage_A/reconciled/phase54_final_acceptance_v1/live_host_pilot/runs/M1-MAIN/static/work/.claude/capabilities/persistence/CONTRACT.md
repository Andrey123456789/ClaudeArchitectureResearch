> Capability contract: persistence · Leaf slot (required) · Maintainer metadata · Not auto-loaded; read during capability maintenance

# Capability Contract: persistence

## Purpose

The persistence leaf supplies the persistence technology behind the frame's
persistence-access contracts and commit boundary. It binds to frame roles; it
does not decide placement.

A missing required facet or property is a conformance failure; resolving it
requires a Decision Request. Replacing the technology (for example with a
micro-ORM) must not silently lose the migration or seeding semantics. A
provider change (for example SQL Server to PostgreSQL) is a provider-variant
change inside this slot, not a new slot.

## Role Vocabulary Exposed to Other Instructions

| Role | Meaning |
|---|---|
| persistence-technology types | the technology types that must not leak into the core model or use-case layer |
| persistence session | the scoped unit shared by the repositories and the commit boundary of one use case |
| persistence-change workflow | the procedure for mappings, migrations, seed data, and schema-affecting settings |
| development seeder | the Development-only initializer of an empty database |

## Required Facets

| Facet | Location | Loading |
|---|---|---|
| planning | `docs/capabilities/persistence.md` | always (import in `CLAUDE.md`) |
| rules | `.claude/rules/persistence-technology.md` | path (backend) |
| workflow | `.claude/skills/persistence-change/SKILL.md` | workflow (routed from `CLAUDE.md`) |
| knowledge | a knowledge skill of the implementation | on demand |

## Required Properties

Persistence access and commit-boundary binding, migration mechanism, seeding
mechanism, provider variant, observable string-comparison semantics (also
declared in `docs/capability-selection.md`), and relational-testing
expectations.

```json
{
  "slot": "persistence",
  "slotType": "leaf",
  "required": true,
  "requiredFacets": {
    "planning": "docs/capabilities/persistence.md",
    "rules": ".claude/rules/persistence-technology.md",
    "workflow": ".claude/skills/persistence-change/SKILL.md",
    "knowledge": null
  },
  "requiredProperties": ["commitBinding", "migrationMechanism", "seedingMechanism", "providerVariant", "stringComparison", "relationalTesting"],
  "requiredEnforcement": ["technologyNamespaces", "coChange"],
  "roles": ["persistence-technology types", "persistence session", "persistence-change workflow", "development seeder"]
}
```
