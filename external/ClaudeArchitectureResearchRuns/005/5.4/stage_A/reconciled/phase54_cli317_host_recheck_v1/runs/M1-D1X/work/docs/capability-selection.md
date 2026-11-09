> Capability selection record · Always loaded (imported by `CLAUDE.md`) · Changing a selection is Reserved and requires an ADR (`architecture-decision` workflow)

# Capability Selection

Static composition: each required slot has exactly one selected implementation;
the optional slot has zero or one. Only selected implementations have runtime
facets.

| Slot | Slot type | Status | Selected implementation | Declared properties |
|---|---|---|---|---|
| architecture | frame, required | selected | clean-architecture | — |
| persistence | leaf, required | selected | ef-core | provider: sqlserver |
| backend-testing | leaf, required | selected | nunit | — |
| frontend | leaf, optional | selected | angular | — |

## Declared Observable Properties

- persistence / string comparison: equality, uniqueness, ordering, and lookup
  in database queries follow the database and column collation. SQL Server
  default collations compare case-insensitively and accent-sensitively. This is
  a technology default, not an approved product semantic; changing the
  effective collation is a product decision (`CLAUDE.md` § Product Sources).

## Where Each Selection Lives

- Planning-time decisions of each selected implementation:
  `docs/capabilities/<slot>.md` (imported by `CLAUDE.md`).
- Slot contracts and implementation manifests (maintainer metadata, read only
  during capability maintenance): `.claude/capabilities/<slot>/CONTRACT.md` and
  `.claude/capabilities/<slot>/<implementation>/MODULE.md`.
