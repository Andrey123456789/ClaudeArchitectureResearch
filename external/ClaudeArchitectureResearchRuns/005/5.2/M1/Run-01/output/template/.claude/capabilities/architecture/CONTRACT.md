> **Capability contract** · Slot: architecture (required frame) · Owns: stable role vocabulary, required facets and properties, replacement obligations · Scope: backend, backend-tests · Loading: maintainer-only (read by `template-maintenance` and the checkers)

# Architecture Slot Contract

The architecture slot is the frame: it defines the backend layers and projects,
owns placement, dependency direction, and patterns not adopted, and supplies the
architecture-check specification. Leaf capabilities and workflows bind to its
stable roles instead of to frame-specific layer names.

Rule of thumb: placement belongs to the frame; technique belongs to the leaf.

## Stable Roles

| Role | Meaning |
|---|---|
| domain layer | business concepts independent of technology and transport |
| use-case layer | use-case orchestration plus the persistence and external-service abstractions it needs |
| use-case unit | the type that orchestrates one use case |
| persistence-access contract | the inward-facing abstraction for persistence needs of a use case |
| commit boundary | the abstraction that commits one use case's changes |
| adapter layer | technology implementations of inward abstractions (persistence, external services) |
| entry point | the HTTP-facing type that binds input, invokes a use-case unit, maps outcomes |
| composition root | where all registrations are composed at startup |
| test-project role | where backend test projects live and what they may reference |

## Required Facets

- `architecture-decision` — always-loaded planning record: adopted style, role
  mapping, patterns not adopted.
- `architecture-rule` — path-loaded rule for backend code: dependency direction,
  layer responsibilities, persistence-access/commit-boundary rules, registration
  and transport-contract placement, test-project references.
- `backend-layout` — `project-structure` reference describing the physical layout.

## Required Properties

- `roleMapping` — every stable role mapped.
- `layers` — layer name, project suffix, role, allowed project references.
- `compositionRootLayer` — the layer that hosts the composition root.
- `testProjects` — test-project suffixes and their allowed references.

## Replacement Obligations

A replacement frame must map every stable role, keep the frozen dependency and
placement semantics or raise a Decision Request for each change, and update the
leaf facets that state technology placement through these roles.

```json
{
  "slot": "architecture",
  "status": "required",
  "frame": true,
  "roles": ["domain layer", "use-case layer", "use-case unit", "persistence-access contract", "commit boundary", "adapter layer", "entry point", "composition root", "test-project role"],
  "requiredFacets": ["architecture-decision", "architecture-rule", "backend-layout"],
  "requiredProperties": ["roleMapping", "layers", "compositionRootLayer", "testProjects"]
}
```
