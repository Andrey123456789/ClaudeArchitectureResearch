---
name: persistence-change
description: >
  Use when changing entities, mappings, the DbContext model, migrations,
  development seed data, or schema-affecting custom settings (EF Core change
  procedure).
---

> Capability: persistence/ef-core · Workflow facet · Owns the mapping, migration-review, seed co-change, and schema-impact procedure

# Persistence Change: EF Core

Rules: `.claude/rules/persistence-technology.md` and
`.claude/rules/architecture.md` — read them first if they have not loaded.
Technique: `ef-core` skill.

## 1. Assess the Impact

Identify the changed entities, relationships, constraints, indexes, and column
definitions; whether the change affects the schema; and whether it affects
entities represented in the development seed data.

## 2. Update the Mapping

Change the `IEntityTypeConfiguration<T>` mappings in the adapter layer; keep
persistence-specific configuration out of the core model where practical.

## 3. Migrations

Create migrations from the adapter-layer project with the composition-root
project as startup project:

```bash
dotnet ef migrations add AddOrderIndex --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api
```

Treat EF Core migrations as source code: review every generated migration before
committing it, paying particular attention to destructive schema changes,
unexpected column recreation, data migrations, indexes, foreign keys, and delete
behavior. When the change requires a new migration, do not casually alter
existing migrations; regenerate or edit an uncommitted migration only when that
matches the project's normal migration workflow.

## 4. Seed Data

Whenever Domain or persistence changes affect seeded entities, update the
development `DbSeeder` in the same change — for example new required
properties, removed or renamed properties, changed relationships, new required
related entities, changed enum/status values, new meaningful entity states, or
changed Domain invariants. When a migration reflects a model change that
affects the seeded entity graph, review and update `DbSeeder` together with
that migration.

A migration of an existing development database does not require the seeder to
patch already seeded rows. The goal: recreating the development database at any
revision produces seed data that is valid and representative for that
revision.

## 5. Schema-Affecting Settings

When a `CUSTOM_SETTINGS.md` change affects schema constraints, indexes, column
lengths, or other persistence metadata:

1. update the EF Core mapping;
2. create the appropriate migration according to step 3;
3. verify that Development seeding remains valid;
4. add or update provider-sensitive persistence or integration tests when
   provider behavior matters.

## 6. Verify

Build the affected projects, run the persistence and integration tests, and
confirm the migration applies to a freshly created Development database before
seeding. Production migration remains explicit deployment work (`verify`
§ Delivery Changes).
