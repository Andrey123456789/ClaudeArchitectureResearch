> **Capability manifest** · Capability: persistence/ef-core · Owns: facet list and declared properties of the EF Core implementation (provider variant SQL Server) · Scope: backend · Loading: maintainer-only (read by `template-maintenance` and the checkers)

# Module: persistence/ef-core

EF Core with the SQL Server provider (`Microsoft.EntityFrameworkCore.SqlServer`).
The module binds to the architecture frame only through stable roles, so it
declares no `binds:` coupling.

| Facet role | File | Loading |
|---|---|---|
| persistence-rule | `.claude/rules/persistence-technology.md` | path (backend code, project files, appsettings) |
| persistence-knowledge | `.claude/skills/ef-core/SKILL.md` | on demand |

```json
{
  "capability": "persistence/ef-core",
  "facets": [
    { "role": "persistence-rule", "path": ".claude/rules/persistence-technology.md", "loading": "path" },
    { "role": "persistence-knowledge", "path": ".claude/skills/ef-core/SKILL.md", "loading": "on-demand" }
  ],
  "properties": {
    "provider": "sqlserver",
    "technologyPackages": ["Microsoft.EntityFrameworkCore", "Microsoft.EntityFrameworkCore.*"],
    "technologyForbiddenInRoles": ["domain layer", "use-case layer"],
    "commitBoundaryBinding": "IUnitOfWork implementation delegates to the scoped AppDbContext.SaveChangesAsync; repositories share the scoped AppDbContext registered by AddDbContext",
    "migrationMechanism": "EF Core migrations in <role:adapter layer>/Persistence/Migrations, created with dotnet ef migrations add --project <adapter-layer project> --startup-project <composition-root project>; reviewed before commit; production via explicit deployment step",
    "seedingMechanism": "internal DbSeeder in <role:adapter layer>/Persistence/Seeding invoked from the composition root only in Development through SeedDevelopmentDataAsync; anchor-entity empty check; never migrates; never overwrites",
    "stringComparison": "database collation decides equality, uniqueness, and lookup; common SQL Server default collations are case-insensitive",
    "relationalTesting": "SQL Server provider (LocalDB or Testcontainers MsSql); the InMemory provider is not relational",
    "coChange": {
      "modelGlobs": ["<role:domain layer>/**/*.cs", "<role:adapter layer>/Persistence/Configurations/**/*.cs", "<role:adapter layer>/Persistence/*DbContext.cs"],
      "seederGlobs": ["<role:adapter layer>/Persistence/Seeding/**/*.cs"],
      "migrationGlobs": ["<role:adapter layer>/Persistence/Migrations/**/*.cs"]
    }
  },
  "usesRoles": ["domain layer", "use-case layer", "persistence-access contract", "commit boundary", "adapter layer", "composition root"],
  "binds": [],
  "leakTerms": ["EF Core", "Entity Framework", "EntityFrameworkCore", "ef-core", "DbContext", "DbSet", "SQL Server", "SqlServer", "sqlserver", "LocalDB", "MSSQLLocalDB"],
  "allowList": []
}
```
