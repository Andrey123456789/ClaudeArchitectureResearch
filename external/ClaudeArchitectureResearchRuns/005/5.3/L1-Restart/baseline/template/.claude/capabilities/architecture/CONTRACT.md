> Level: 1-architecture · Owns: architecture slot contract (maintainer metadata) · Scope: backend · Loading: never auto-loaded

# Slot Contract: architecture (required frame)

The architecture slot is a **frame**: it maps the stable role vocabulary (`.claude/rules/1-architecture/roles.md`, outside every module) to concrete projects and owns placement. Leaf slots depend on roles, not on frame terms. Placement belongs to the frame; technique belongs to the leaf.

## Required facets

| Facet | Form | Level | Loading | Must provide |
| --- | --- | --- | --- | --- |
| `architecture.style` | rule | 1 | always (imported by `CLAUDE.md`) | adopted style, role → project mapping, patterns not adopted |
| `architecture.boundaries` | rule | 1 | path: backend | dependency direction, layer responsibilities, placement of persistence-access contracts and commit boundary, composition root, test-project references |
| `architecture.layout` | workflow-read reference | 1 | read by `project-structure` | physical project tree, project-reference graph, internal directories |
| `architecture.check` | enforcement data (JSON) | 1 | read by `.claude/scripts/check-architecture.mjs` and hooks | role → project-name pattern and path globs, allowed references per role, roles that must not reference persistence or transport packages, test-project roles |

## Obligations

- Express every role in `roles.md`; never contradict a role-level rule.
- Keep leaf technology out of frame facets (refer to persistence-implementation types generically; the persistence module binds them).
- Leaf bindings that cannot be expressed through roles must be declared by the leaf as `binds:` in its manifest.

## Replacement

Changing the frame is Reserved and requires an ADR (`architecture-decision`). A replacement module supplies every facet above, updates the selection record and the `CLAUDE.md` import of its style facet, and passes `node .claude/scripts/check-instructions.mjs`.
