> Capability contract: architecture · Frame slot (required) · Maintainer metadata · Not auto-loaded; read during capability maintenance

# Capability Contract: architecture

## Purpose

The architecture frame defines the stable role vocabulary that other
instructions and the leaf capabilities use, maps those roles to concrete
projects and layers, owns placement, and supplies the architecture-check
specification. Binding rule: placement belongs to the frame; technique belongs
to the leaf.

## Stable Role Vocabulary

| Role | Meaning |
|---|---|
| core model | business concepts and genuine invariants, independent of infrastructure and transport |
| use-case layer | orchestration of use cases and the inward-facing contracts they need |
| use-case unit | the default orchestration unit for one use case |
| persistence-access contract | inward-facing, use-case-specific persistence interface |
| commit boundary | the abstraction that decides when a use case's changes are committed |
| adapter layer | implementations of persistence and external-service contracts |
| entry point | the HTTP endpoint mechanism that translates requests and outcomes |
| composition root | the place where all layers are registered and composed |
| test projects | the backend test-project roles and their allowed references |

Leaf capabilities bind to these roles. A leaf that must name a frame-specific
project or directory declares a `binds` entry in its manifest.

## Required Facets

| Facet | Location | Loading |
|---|---|---|
| planning | `docs/capabilities/architecture.md` — adopted style, role map, repository layout, patterns not adopted | always (import in `CLAUDE.md`) |
| rules | `.claude/rules/architecture.md` — layer and boundary rules | path (backend) |
| placement | `.claude/skills/project-structure/references/backend-layout.md` | explicit read by `project-structure` |
| architecture check | manifest `enforcement.architecture` | `.claude/scripts/check-architecture.js` |

## Replacement Notes

A replacement frame must supply every role mapping and facet above. Embedded
rules (error handling, API, performance, security) use the frame's layer names
as project vocabulary, so a frame replacement reviews them as part of the
change.

```json
{
  "slot": "architecture",
  "slotType": "frame",
  "required": true,
  "requiredFacets": {
    "planning": "docs/capabilities/architecture.md",
    "rules": ".claude/rules/architecture.md",
    "placement": ".claude/skills/project-structure/references/backend-layout.md"
  },
  "requiredProperties": ["adoptedStyle", "roleMap", "patternsNotAdopted", "repositoryLayout"],
  "requiredEnforcement": ["architecture", "detailTokens"],
  "roles": ["core model", "use-case layer", "use-case unit", "persistence-access contract", "commit boundary", "adapter layer", "entry point", "composition root", "test projects"]
}
```
