> Level: 2-technology · Capability: persistence/ef-core · Owns: implementation manifest (maintainer metadata) · Scope: backend · Loading: never auto-loaded

# Module: persistence/ef-core

EF Core with the SQL Server provider (provider variant `sqlserver`).

- binds: architecture/clean-architecture — `commands.md` and `workflow.md` name the implementation-layer and entry-point projects (`<Name>.Infrastructure`, `<Name>.Api`) as the migration and startup projects, and the `ef-core` skill shows the frame's `Persistence/` folder placement.
- leak-tokens: EF Core, Entity Framework, DbContext, DbSet, SQL Server, SqlServer, AppDbContext, DbSeeder, ef-core

## Facets

| Facet | File | Level | Loading |
| --- | --- | --- | --- |
| `persistence.access` | `.claude/rules/2-technology/persistence/access.md` | 2-technology | path |
| `persistence.seeding` | `.claude/rules/2-technology/persistence/seeding.md` | 2-technology | path |
| `persistence.dev-config` | `.claude/rules/3-project/development-database.md` | 3-project | path |
| `persistence.workflow` | `.claude/capabilities/persistence/ef-core/workflow.md` | 2-technology | workflow-read |
| `persistence.commands` | `.claude/capabilities/persistence/ef-core/commands.md` | 2-technology | workflow-read |
| `persistence.enforcement` | `.claude/capabilities/persistence/ef-core/enforcement.json` | 2-technology | enforcement data |
| `persistence.knowledge` | `.claude/skills/ef-core/SKILL.md` | 2-technology | on demand |

## Declared properties

Recorded in the selection record (`.claude/rules/3-project/decisions.md`): provider variant `sqlserver`; default string comparison follows the database default collation (typically case-insensitive); migrations are EF Core migrations; seeding is the Development-only `DbSeeder`.
