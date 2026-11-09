> Level: 2-technology · Capability: persistence/ef-core · Facet: persistence.commands · Owns: persistence scaffold packages and commands · Scope: backend · Loading: read by `project-structure`, `verify`, `build-fix`, `persistence.workflow`

# EF Core Commands

Install packages only through `add-dependency` (latest stable compatible version, versions in `Directory.Packages.props`).

## Scaffold packages

| Package | Project | When |
| --- | --- | --- |
| `Microsoft.EntityFrameworkCore.SqlServer` | `<Name>.Infrastructure` | baseline persistence |
| `Microsoft.EntityFrameworkCore.Design` | `<Name>.Api` (startup project) | design-time services for migrations |
| `dotnet-ef` (local or global .NET tool) | repository tool manifest | migration commands |
| `Testcontainers.MsSql` | integration-test project | only when isolated real-provider tests justify it |

Register the context in `AddInfrastructure` with `options.UseSqlServer(configuration.GetConnectionString("DefaultConnection"))`; the Development connection string follows `persistence.dev-config`.

## Migrations

```bash
dotnet ef migrations add <MigrationName> --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api
dotnet ef migrations list --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api
dotnet ef migrations remove --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api   # only for an unapplied, uncommitted migration
dotnet ef migrations script --idempotent --output artifacts/migrations.sql --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api
```

## Local Development database

```bash
dotnet ef database update --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api    # Development only
dotnet ef database drop --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api      # explicit recreation for a fresh seed dataset
```

Never point these commands at Production; production migration is a deployment step.
