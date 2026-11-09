> Kind: — (module manifest) | Scope: repo/meta | Capability: persistence/ef-core | Loading: not loaded (read by `architecture-decision`, `template-maintenance`, and the structure checker)

# Module: persistence / ef-core

- Slot: persistence
- Implementation: ef-core
- Variant: sqlserver
- Names: EF Core, ef-core, EFCore, Entity Framework, EntityFrameworkCore, DbContext, AppDbContext, DbSet, DbSeeder, SQL Server, sqlserver, SqlServer, MSSQL, LocalDB
- Binds: architecture — EF Core types live only in the Infrastructure role; `UnitOfWork` implements the Application `IUnitOfWork` over the shared scoped `AppDbContext`; persistence code sits in `Infrastructure/Persistence/`.

## Facets

| Kind | Scope | File | Loading | Provides |
|---|---|---|---|---|
| DEC | common | `docs/architecture/decision-register.md` | always (capability-selection block) | selection, variant, declared properties |
| STD | backend | `.claude/rules/backend/persistence-technology.md` | path-scoped | technology boundary, commit-boundary binding, seeding mechanism, sqlserver configuration |
| KNW | backend | `.claude/skills/ef-core/SKILL.md` | on-demand | EF Core technique, provider notes, testing with EF Core |
| WF | backend | `.claude/skills/persistence-change/SKILL.md` | on-demand | setup, migration, review, and seed co-change procedure |
| ENF | backend | `.claude/scripts/facets/persistence-technology.cjs` | manifest hook, Stop hook, `verify` | inner-layer package leak check, seed/migration co-change reminders |

## Contract coverage

| Item | Provided by |
|---|---|
| `technology-boundary` | STD `persistence-technology.md`; ENF `persistence-technology.cjs` |
| `commit-boundary-binding` | STD `persistence-technology.md`; KNW `ef-core` |
| `migration-mechanism` | EF Core migrations — WF `persistence-change`; KNW `ef-core` |
| `seeding-mechanism` | Dedicated `DbSeeder` — STD `persistence-technology.md`; KNW `ef-core` |
| `provider-variant` | sqlserver — STD `persistence-technology.md` (Variant section); DEC |
| `declared-properties` | DEC capability selection; KNW `ef-core` (SQL Server provider) |
| `testing-implications` | KNW `ef-core` (Testing with EF Core) |
| `change-workflow` | WF `persistence-change` |
| `knowledge` | KNW `ef-core` |
| `enforcement` | ENF `persistence-technology.cjs` |
