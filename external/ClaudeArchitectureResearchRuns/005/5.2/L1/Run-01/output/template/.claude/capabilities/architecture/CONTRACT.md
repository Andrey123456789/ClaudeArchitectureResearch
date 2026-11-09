> Level: 1-architecture | Capability: architecture (slot contract) | Owns: requirements every architecture-frame implementation must satisfy | Scope: backend | Loads: never (maintainer metadata)

# Slot Contract — `architecture` (required frame)

The architecture slot is a **frame**, not an ordinary leaf. Its implementation
maps every stable role (`.claude/rules/1-architecture/roles.md`) to concrete
projects and locations and owns placement. Leaf capabilities bind to roles and
named frame locations, never to the frame's layer names: placement belongs to
the frame, technique belongs to the leaf.

Exactly one implementation is selected (static composition).

## Required facets

| Facet | Level | Location | Loading | Must provide |
|---|---|---|---|---|
| `architecture.decision` | 1 | `.claude/rules/1-architecture/` rule with `Capability:` header | always (CLAUDE.md import) | adopted architecture; patterns explicitly not adopted |
| `architecture.boundaries` | 1 | `.claude/rules/1-architecture/` rule | path `backend/**/*` | mapping of every role; dependency direction; test-project references; layer responsibilities |
| `architecture.layout` | 1 | `<module>/layout.md` | read by `project-structure` | physical project and directory layout used when scaffolding |
| `architecture.check` | — | `<module>/check.json` | read by `.claude/scripts/check-architecture.cjs` and the stop hook | project classification, allowed references, role and named locations |

## Conformance

- Every role in `roles.md` is mapped; every production layer and test-project
  role is classified by the check specification.
- Frame facets are Level 1: they name no concrete technology beyond the fixed
  platform vocabulary and no leaf implementation.
- The check specification exposes the named locations leaves rely on
  (currently `persistence implementation`).

## Replacement

Changing the frame is Reserved and requires an ADR. Replace it with the
user-invoked `template-maintenance` workflow: add the new module with every
required facet, update the capability selection record and the `CLAUDE.md`
decision import, remove the old module's facets, and run
`node .claude/scripts/check-instructions.cjs`.
