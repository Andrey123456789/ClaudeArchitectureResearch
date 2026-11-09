---
paths:
  - "**/*"
---
> Level: 3-project | Owns: capability selection record (decision summary for slot selections and declared properties) | Scope: common | Loads: always (imported by CLAUDE.md)

# Capability Selection

Composition is static: each required slot has exactly one selected
implementation, the optional slot has zero or one, only selected implementations
ship, and implementations are never selected at runtime.

| Slot | Kind | Selected | Knowledge skill | Declared properties |
|---|---|---|---|---|
| architecture | required frame | clean-architecture | — | backend layers Domain, Application, Infrastructure, Api |
| persistence | required leaf | ef-core | `ef-core` | provider variant: sqlserver; migrations: code-first migrations applied as an explicit step; seeding: Development-only seeder for an empty database; default string comparison: database collation (SQL Server default collations are case-insensitive); relational test fidelity: a real SQL Server instance |
| backend-testing | required leaf | nunit | `dotnet-testing` | packages: NUnit, NUnit3TestAdapter, Microsoft.NET.Test.Sdk |
| frontend | optional leaf | angular | `angular` | workspace `frontend/<Name>.Web/`; package manager: npm |

## Facet resolution

Outside a module, refer to a facet by role as `<slot>.<facet>`:

- `<slot>.decision` — always loaded (imported by `CLAUDE.md`);
- `<slot>.rules` and `architecture.boundaries` — path-scoped rules, loaded automatically;
- `<slot>.knowledge` — the knowledge skill in the table above;
- `layout`, `workflow`, `commands`, `scaffold` — read
  `.claude/capabilities/<slot>/<selected>/<facet>.md` when a workflow step names it;
- `check`, `co-change` — enforcement data read by `.claude/scripts/` and hooks.

When the optional `frontend` slot is empty, skip every `frontend.*` step.

## Changing a selection

Changing a selection or provider variant is Reserved and requires an ADR
(`architecture-decision`). A declared-property change that affects observable
product behavior must not happen silently. A required facet missing from a
selected module is a conformance failure: raise a Decision Request.
