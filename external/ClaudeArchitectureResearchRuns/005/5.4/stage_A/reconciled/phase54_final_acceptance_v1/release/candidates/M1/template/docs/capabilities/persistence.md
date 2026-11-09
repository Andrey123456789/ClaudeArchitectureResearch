> Capability: persistence/ef-core · Always-loaded planning decisions (imported by `CLAUDE.md`) · Owns the persistence technology decision

# Persistence: EF Core (provider variant: SQL Server)

- Persistence stack (Decided): Entity Framework Core with Microsoft SQL Server
  through `Microsoft.EntityFrameworkCore.SqlServer`. EF Core is used directly
  inside the adapter layer; provider-specific concerns stay out of the use-case
  layer and the core model.
- Rules: `.claude/rules/persistence-technology.md` (loads for backend code).
- Knowledge skill: `ef-core`.
- Model, mapping, migration, and seed-data changes: `persistence-change`
  workflow.
