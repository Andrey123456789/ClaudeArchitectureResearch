---
name: persistence-change
description: >
  Procedure for setting up or changing the persistence model: entities, entity
  mappings, the database context, migrations, and development seed data,
  including migration review and seed co-change. Use when adding or changing
  persisted entities, relationships, constraints, indexes, migrations, or the
  development seed dataset.
---

> Kind: WF | Scope: backend | Capability: persistence/ef-core | Loading: on-demand workflow

# Persistence Change — EF Core (variant: sqlserver)

Read first: `.claude/rules/backend/persistence.md`, `.claude/rules/backend/persistence-technology.md`, `.claude/rules/backend/architecture-style.md`. Technique: `ef-core`.

## A. Initial setup (new solution)

1. Packages through `add-dependency`: `Microsoft.EntityFrameworkCore.SqlServer` in Infrastructure; `Microsoft.EntityFrameworkCore.Design` where design-time tooling needs it (startup project); the `dotnet-ef` tool as a local tool when the project uses the CLI.
2. In Infrastructure `Persistence/`: `AppDbContext` (configurations applied from the assembly), entity configurations in `Configurations/`, repositories in `Repositories/`, `UnitOfWork` implementing the Application `IUnitOfWork`, and `Seeding/DbSeeder.cs` plus the initialization extension.
3. Register persistence in Infrastructure's `AddInfrastructure(configuration)` using the `DefaultConnection` connection string.
4. `appsettings.Development.json` connection string per `persistence-technology.md` (Variant: sqlserver). A suitable Windows LocalDB default, adapted to the project's database name:

   ```json
   {
     "ConnectionStrings": {
       "DefaultConnection": "Server=(localdb)\\MSSQLLocalDB;Database=ProjectName;Trusted_Connection=True;TrustServerCertificate=True;"
     }
   }
   ```
5. Create the initial migration (section B), apply it locally, then let Development startup seed the empty database.

## B. Model or mapping change

1. Change the entity and its configuration within the role rules of the read-first standards.
2. If the schema changes, create a **new** migration:

   ```bash
   dotnet ef migrations add <Name> --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api
   ```

   Regenerate or edit an uncommitted migration only when that matches the project's migration workflow; never casually alter migrations that are already applied or shared.
3. Review the generated migration as source code before it is committed, paying particular attention to destructive schema changes, unexpected column recreation, data migrations, indexes, foreign keys, and delete behavior.
4. Seed co-change: whenever the Domain or persistence change affects seeded entities — new required or removed/renamed properties, changed relationships, new required related entities, changed enum/status values, new meaningful states, changed invariants — update the maintained development seeder in the same change, so that recreating an empty Development database at this revision yields valid, representative data. Existing seeded rows are not patched automatically.
5. Apply locally (`dotnet ef database update --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api`), or drop and recreate the local database when a fresh dataset is needed.
6. Add or update persistence/integration tests when provider behavior, mappings, constraints, or non-trivial queries changed (provider fidelity: `ef-core`, Testing).

## C. Verify

Build, run the affected tests, start the API against a freshly recreated Development database when seeding or the schema changed, and run `node "<root>/.claude/scripts/check-cochange.cjs"` (`<root>`: the active repository root; command form in `verify`, Risk-scoped checks). Continue with `verify`.

## Report

Model changes, migration name and review notes (destructive operations called out), seeder updates, and verification results.
