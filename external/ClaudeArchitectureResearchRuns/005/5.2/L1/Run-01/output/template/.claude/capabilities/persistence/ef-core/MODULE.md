> Level: 2-technology | Capability: persistence/ef-core (module manifest) | Owns: facet list and declared properties of the EF Core persistence implementation | Scope: backend | Loads: never (maintainer metadata)

# Module — `persistence/ef-core`

- Slot: `persistence` (required leaf) — selected; provider variant `sqlserver`.
- binds: `architecture` — code examples in `ef-core`, `workflow.md`, and
  `scaffold.md` use the current frame's contract names (`IUnitOfWork`,
  `I<Entity>Repository`) and project paths (`backend/<Name>.Infrastructure`,
  `backend/<Name>.Api`). Prose binds only to roles and the named location
  `persistence implementation`.

- leak terms: `EF Core`, `Entity Framework`, `EntityFrameworkCore`, `DbContext`,
  `DbSet`, `AppDbContext`, `ef-core`, `SQL Server`, `SqlServer`, `LocalDB`, `MSSQL`

## Facets

| Facet | File | Level | Loading |
|---|---|---|---|
| `persistence.decision` | `.claude/rules/3-project/persistence-stack.md` | 3 | always (CLAUDE.md import) |
| `persistence.rules` | `.claude/rules/2-technology/data-access.md` | 2 | path `backend/**/*` |
| `persistence.knowledge` | `.claude/skills/ef-core/SKILL.md` | 2 | on demand |
| `persistence.workflow` | `.claude/capabilities/persistence/ef-core/workflow.md` | 2 | read by workflows |
| `persistence.scaffold` | `.claude/capabilities/persistence/ef-core/scaffold.md` | 3 | read by `project-structure` |
| `persistence.co-change` | `.claude/capabilities/persistence/ef-core/co-change.json` | — | stop hook |

## Declared properties

| Property | Value |
|---|---|
| provider variant | `sqlserver` (Microsoft.EntityFrameworkCore.SqlServer) |
| migration mechanism | EF Core code-first migrations, reviewed as source; applied explicitly, never from production startup |
| seeding mechanism | internal `DbSeeder`, Development-only, empty database only |
| default string comparison | database collation; SQL Server default collations are case-insensitive — observable semantics need product approval |
| relational test fidelity | a real SQL Server instance (LocalDB or an isolated container) |
