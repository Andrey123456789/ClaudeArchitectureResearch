Kind: WF | Scope: backend | Capability: persistence/ef-core | Loading: read by workflows at persistence steps

# Workflow Facet: persistence / ef-core (SQL Server)

Persistence procedures for EF Core with SQL Server. Before using them, read `.claude/rules/backend/persistence.md` and `.claude/rules/backend/persistence-technology.md` if they are not loaded. Technique and code: `ef-core` knowledge skill.

## Persistence area layout

Inside `backend/<Name>.Infrastructure/Persistence/` (placement by the architecture frame):

```text
Persistence/
├── AppDbContext.cs
├── UnitOfWork.cs
├── Configurations/       IEntityTypeConfiguration<T> mappings
├── Repositories/         concrete repositories (frame placement)
├── Migrations/           EF Core migrations
└── Seeding/
    ├── DbSeeder.cs
    └── DatabaseInitializationExtensions.cs
```

## Setup

1. Add packages through `add-dependency`: `Microsoft.EntityFrameworkCore.SqlServer` in Infrastructure, `Microsoft.EntityFrameworkCore.Design` in the Api startup project for migration tooling, and the `dotnet-ef` tool in a local tool manifest (`dotnet new tool-manifest`, then `dotnet tool install dotnet-ef`).
2. Register `AppDbContext`, the repositories and `IUnitOfWork` in Infrastructure `DependencyInjection.cs` (`ef-core` skill → Registration).
3. Add a non-secret local connection string to `backend/<Name>.Api/appsettings.Development.json`. A suitable Windows default:

   ```json
   {
     "ConnectionStrings": {
       "DefaultConnection": "Server=(localdb)\\MSSQLLocalDB;Database=<Name>;Trusted_Connection=True;TrustServerCertificate=True;"
     }
   }
   ```

   When local SQL Server needs credentials, keep the non-secret structure in configuration and supply the secret through `dotnet user-secrets`.
4. Create the seeder and its initialization extension (`ef-core` skill → Development seeding) and call it from `Program.cs` inside `if (app.Environment.IsDevelopment())`.
5. Create and apply the initial migration locally:

   ```bash
   dotnet ef migrations add InitialCreate --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api
   dotnet ef database update --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api
   ```

## Model or schema change

1. Update the entity and its `IEntityTypeConfiguration<T>` mapping.
2. Create a migration: `dotnet ef migrations add <ChangeName> --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api`.
3. Treat EF Core migrations as source code: review every generated migration before committing it, paying particular attention to destructive schema changes, unexpected column recreation, data migrations, indexes, foreign keys and delete behavior.
4. When the change affects seeded entities, update `DbSeeder` in the same change (`development-workflow` → Implement).
5. Validate locally: apply the migration, then recreate an empty Development database (`dotnet ef database drop`, `dotnet ef database update`, start the application) and confirm the seed data is valid for the migrated schema. Migrating an existing Development database does not require patching already seeded rows.

## Schema-affecting `CUSTOM_SETTINGS.md` change

When a changed setting affects schema constraints, indexes, column lengths or other persistence metadata:

1. update the EF Core mapping;
2. create a new migration through the steps above; edit or regenerate a migration only while it is uncommitted and only when that matches the project's normal migration workflow, and do not casually alter existing migrations;
3. verify that Development seeding remains valid;
4. add or update provider-sensitive persistence or integration tests when provider behavior matters.

## Production migration artifacts

Production migrations are applied by the deployment, never by normal application startup. Produce reviewable artifacts in CI or locally:

```bash
dotnet ef migrations script --idempotent --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api --output artifacts/migrations.sql
```

A migration bundle (`dotnet ef migrations bundle`) is an alternative when the deployment runs executables.

## Verification commands

- Pending model changes without a migration: `dotnet ef migrations has-pending-model-changes --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api`.
- Runtime smoke: the Development database is reachable, migrations are applied, and the seeder populates an empty database.

## Build-fix cues

- Migration or model-snapshot errors: fix the model or configuration and regenerate an uncommitted migration; committed migrations are maintained source and are changed only by new migrations.
- Provider or design-time errors (`Unable to create a DbContext`): check the startup project, `Microsoft.EntityFrameworkCore.Design` and the Development connection string.

## Security review cues

- Raw SQL: `FromSql`, `FromSqlInterpolated` and `ExecuteSql` with interpolated values are parameterized; `FromSqlRaw` and `ExecuteSqlRaw` are safe only with explicit parameters, never with concatenated or interpolated untrusted input.
- Committed `appsettings*.json` connection strings must not carry real credentials.
