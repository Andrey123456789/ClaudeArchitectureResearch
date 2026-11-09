---
paths:
  - "backend/**/*"
---
> Level: 1-architecture | Capability: architecture/clean-architecture (architecture.decision) | Owns: adopted architecture and patterns not adopted | Scope: backend | Loads: always (imported by CLAUDE.md)

# Adopted Architecture

Adopted: Clean Architecture with the backend layers Domain, Application,
Infrastructure, and Api. Role placement, project references, and layer
responsibilities: `layering.md` (loads for backend files).

Not adopted: CQRS command/query handlers, mediator libraries or mediator-based
request dispatch, Vertical Slice Architecture, or similar mediator-based
organization. Do not introduce them unless explicitly approved.
