> Level: 1-architecture · Owns: architecture slot contract (maintainer metadata) · Scope: backend · Loading: never auto-loaded

# Slot Contract: architecture (required frame)

The architecture slot is a **frame**: it maps the stable role vocabulary (`.claude/rules/1-architecture/roles.md`, outside every module) to concrete projects and owns placement. Leaf slots depend on roles, not on frame terms. Placement belongs to the frame; technique belongs to the leaf.

## Required facets

| Facet | Form | Level | Loading | Must provide |
| --- | --- | --- | --- | --- |
| `architecture.style` | rule | 1 | always (imported by `CLAUDE.md`) | adopted style, role → project mapping, patterns not adopted |
| `architecture.boundaries` | rule | 1 | path: backend | dependency direction, layer responsibilities, placement of persistence-access contracts and commit boundary, composition root, test-project references |
| `architecture.layout` | workflow-read reference | 1 | read by `project-structure` | physical project tree, project-reference graph, internal directories |
| `architecture.check` | enforcement data (JSON) | 1 | read by `.claude/scripts/check-architecture.mjs` and hooks | role → project-name pattern and path globs, allowed references per role, inner roles, test-project roles — no package identifiers |
| `architecture.enforcement` | enforcement data (JSON) | 2 | read by `.claude/scripts/check-architecture.mjs` and hooks | technology bindings of the frame's checks: framework references forbidden in inner roles, packages of patterns not adopted |

## Obligations

- Express every role in `roles.md`; never contradict a role-level rule.
- Keep Level 1 facets technology-neutral: concrete framework, library, and package names belong to Level 2 (`architecture.enforcement`, the persistence module, the backend technology rules).
- Keep leaf technology out of frame facets (refer to persistence-implementation types generically; the persistence module binds them).
- List the frame-specific vocabulary as `frame-terms:` in the module manifest. Leaf bindings that cannot be expressed through roles must be declared by the leaf as `binds:` in its manifest; the checker requires the declaration wherever a leaf uses a frame term. Code identifiers in frame facets belong to two classes, each proven by the frame's own facets rather than by the manifest: frame code names in `frame-terms` (a registration extension named `Add` plus a layer the style facet maps to a project, or the code spelling of a multi-word concept the facets state in plain words, such as an interface for the Unit of Work) and `placement-examples:` that the layout facet places (in a directory tree, as a folder path, or as a naming variant of a placed example). Any other code identifier is a Level 2 binding.

## Replacement

Changing the frame is Reserved and requires an ADR (`architecture-decision`). A replacement module supplies every facet above, updates the selection record and the `CLAUDE.md` import of its style facet, and passes `node "$(git rev-parse --show-toplevel)/.claude/scripts/check-instructions.mjs"`.
