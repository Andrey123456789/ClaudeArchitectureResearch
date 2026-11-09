Kind: DEC | Scope: backend | Capability: persistence/ef-core | Loading: module manifest, read on demand

# Module: persistence/ef-core

- slot: persistence (required leaf)
- implementation: ef-core
- variant: sqlserver
- aliases: EF Core, Entity Framework, EntityFrameworkCore, ef-core, DbContext, DbSet, DbSeeder, SQL Server, SqlServer, sqlserver, LocalDB, MSSQL
- binds: architecture (Infrastructure persistence area, Application persistence port, commit boundary)

## Facets

| Kind | Facet | Scope | Loading |
|---|---|---|---|
| DEC | `docs/architecture/decision-register.md` (section "persistence → ef-core (sqlserver)") | common | always (imported by CLAUDE.md) |
| STD | `.claude/rules/backend/persistence-technology.md` | backend | path-scoped (backend/**) |
| KNW | `.claude/skills/ef-core/SKILL.md` | backend | on invocation |
| WF | `.claude/capabilities/persistence/ef-core/workflow-facet.md` | backend | read by `development-workflow`, `project-structure`, `custom-settings`, `verify`, `code-review`, `build-fix`, `security-scan` |
| ENF | `.claude/scripts/facets/persistence/enforcement.json` | backend | read by `check-architecture.mjs` and the Stop hook |

## Declared properties

Decided properties (provider, containment, observable string semantics) are recorded in the decision register section of this module. Where each contract mechanism is implemented:

| Contract mechanism | Implemented in |
|---|---|
| commit-boundary binding | STD facet → Role bindings |
| migration mechanism | WF facet → Model or schema change, Production migration artifacts |
| seeding mechanism | STD facet → Development seeding; KNW facet → Development seeding |
| provider variant | register (`sqlserver`); STD facet → Development database configuration |
| observable properties | register section; KNW facet → DbContext configuration (collations) |
| testing implications | STD facet → Role bindings (provider-fidelity target); KNW facet → Testing implications |

Packages: `Microsoft.EntityFrameworkCore.SqlServer` (Infrastructure), `Microsoft.EntityFrameworkCore.Design` (Api, design time), local tool `dotnet-ef`.
