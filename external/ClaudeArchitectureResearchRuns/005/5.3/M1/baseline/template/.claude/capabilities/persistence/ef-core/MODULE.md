> Capability: persistence/ef-core · Module manifest · Provider variant: sqlserver · Maintainer metadata · Not auto-loaded

# Module: persistence/ef-core

The selected persistence implementation: Entity Framework Core with the SQL
Server provider. It defines the persistence-technology types and the
persistence session for the frame's architecture rules, owns Development
seeding and the migration procedure, and supplies the namespace list and
co-change patterns used by the architecture check and the stop hook.

Provider-variant content (SQL Server) is confined to the sections listed in
`providerVariantSections`; a provider change edits only those sections, the
provider property in `docs/capability-selection.md`, and the declared
string-comparison property.

`binds`: the knowledge examples, migration command, and co-change patterns use
the frame's project and directory names.

## Manifest

```json
{
  "slot": "persistence",
  "implementation": "ef-core",
  "facets": {
    "planning": ["docs/capabilities/persistence.md"],
    "rules": [".claude/rules/persistence-technology.md"],
    "workflow": [".claude/skills/persistence-change/SKILL.md"],
    "knowledge": [".claude/skills/ef-core/SKILL.md"]
  },
  "properties": {
    "commitBinding": "IUnitOfWork implemented over the scoped AppDbContext; repositories stage changes; one SaveChangesAsync per use case",
    "migrationMechanism": "EF Core migrations created with dotnet ef from the adapter-layer project; reviewed as source code; production migration is an explicit deployment step",
    "seedingMechanism": "internal DbSeeder in the adapter layer, Development-only, empty-database-only, no schema creation",
    "providerVariant": "sqlserver",
    "stringComparison": "database/column collation; SQL Server default collations are case-insensitive and accent-sensitive",
    "relationalTesting": "provider fidelity uses SQL Server; EF Core InMemory is non-relational"
  },
  "providerVariantSections": [
    "docs/capabilities/persistence.md#persistence-ef-core-provider-variant-sql-server",
    ".claude/rules/persistence-technology.md#relational-testing-binding",
    ".claude/rules/persistence-technology.md#local-development-database-provider-variant-sql-server",
    ".claude/skills/ef-core/SKILL.md#registration-provider-variant-sql-server",
    ".claude/skills/ef-core/SKILL.md#project-setup"
  ],
  "binds": [
    { "target": "architecture/clean-architecture", "reason": "knowledge examples, the migration command, and co-change patterns use the frame's project and directory names" }
  ],
  "leakTokens": ["EF Core", "Entity Framework", "EntityFrameworkCore", "DbContext", "DbSet", "DbSeeder", "AppDbContext", "dotnet ef", "EnsureCreated", "Database.Migrate", "IEntityTypeConfiguration", "AsNoTracking", "ExecuteUpdateAsync", "ExecuteDeleteAsync", "EF.Compile", "ef-core", "SQL Server", "SqlServer", "LocalDB", "MSSQLLocalDB"],
  "enforcement": {
    "technologyNamespaces": ["Microsoft.EntityFrameworkCore"],
    "coChange": {
      "model": ["backend/*.Domain/**/*.cs", "backend/*.Infrastructure/Persistence/Configurations/**/*.cs"],
      "companions": {
        "seed data": ["backend/*.Infrastructure/Persistence/Seeding/**"],
        "migrations": ["backend/*.Infrastructure/Persistence/Migrations/**"]
      },
      "owner": ".claude/skills/persistence-change/SKILL.md"
    }
  }
}
```
