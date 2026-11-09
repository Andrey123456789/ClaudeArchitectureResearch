> Level: 2-technology | Capability: persistence/ef-core (persistence.workflow) | Owns: procedure for model, schema, migration, and seed changes | Scope: backend | Loads: read when a workflow step names persistence.workflow

# Persistence Change Procedure — EF Core

Run this when a change touches entities, entity configurations, `AppDbContext`,
migrations, or the development seeder. Paths below use the current frame
locations (`backend/<Name>.Infrastructure` is the adapter project,
`backend/<Name>.Api` the composition-root host).

## 1. Inspect

Read the affected entities, their `IEntityTypeConfiguration<T>` mappings, the
latest migration, and `DbSeeder` before editing.

## 2. Change the model

Change entities and mappings. Keep mapping configuration in entity
configurations, not in domain entities, where practical. Observable string
semantics (collation, case sensitivity) follow product governance.

## 3. Keep the seeder current

Whenever a domain or persistence change affects seeded entities, update the
maintained development seeder in the same change. Triggers include new required
properties, removed or renamed properties, changed relationships, new required
related entities, changed enum or status values, new meaningful entity states,
and changed domain invariants. When a migration reflects a model change that
affects the seeded entity graph, review and update `DbSeeder` together with
that migration.

Already-seeded local rows are not patched automatically. The goal: recreating
the Development database at any revision produces seed data that is valid and
representative for that revision.

## 4. Create the migration

```bash
dotnet ef migrations add <MigrationName> --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api
```

Use the repository's local `dotnet-ef` tool (added through `add-dependency`).
To redo an unapplied, uncommitted migration, remove it with
`dotnet ef migrations remove` (same `--project`/`--startup-project`) and add it
again.

## 5. Review the migration

EF Core migrations are source code: review every generated migration before
committing it, paying particular attention to destructive schema changes,
unexpected column recreation, data migrations, indexes, foreign keys, and delete
behavior.

## 6. Apply locally (Development only)

```bash
dotnet ef database update --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api
```

For the current seed dataset in an existing local database, recreate it
explicitly, then start the host in Development so the seeder fills the empty
schema:

```bash
dotnet ef database drop --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api
dotnet ef database update --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api
```

## 7. Production

Production schema changes are an explicit deployment step (`delivery`). For a
controlled deployment, generate a reviewed script:

```bash
dotnet ef migrations script --idempotent --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api --output artifacts/migrations.sql
```

## 8. Tests

Provider-sensitive persistence and integration tests run against a real SQL
Server instance (declared relational test fidelity) and own their test data.
