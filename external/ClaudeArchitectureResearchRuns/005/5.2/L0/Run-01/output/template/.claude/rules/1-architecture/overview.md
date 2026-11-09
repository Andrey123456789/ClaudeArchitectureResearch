---
paths:
  - "**/*"
---

> Level: 1 Architecture | Owns: adopted architecture, patterns not adopted, consequential-architecture approval gate | Scope: common | Loads: always (imported by CLAUDE.md) | Depends on: CLAUDE.md

# Architecture Decisions

## Adopted

- Clean Architecture is the adopted backend architecture: `Domain`,
  `Application`, `Infrastructure`, and `Api` projects with inward-pointing
  dependencies.
- The frontend is a separate client of the published HTTP contract with a
  feature-oriented structure.

Detailed architecture policy is path-scoped (routing pointers):

- → backend layers, references, composition: `1-architecture/backend-layers.md`
- → repositories and Unit of Work: `1-architecture/persistence-boundary.md`
- → HTTP entry points and API contracts: `1-architecture/entry-points.md`
- → outcomes, exceptions, validation boundaries: `1-architecture/outcomes.md`
- → frontend structure: `1-architecture/frontend-structure.md`

## Not Adopted

Do not introduce CQRS handlers, mediator-based organization, or Vertical Slice
Architecture unless explicitly approved.

## Consequential Architecture Gate

These choices require explicit approval unless the specification or the
established project structure already requires them:

- a Rich Domain Model, Aggregate Roots, or systematic DDD tactical patterns;
- the patterns listed under Not Adopted;
- event sourcing;
- a project-wide Result or railway-oriented programming model;
- new architectural layers or production projects;
- multiple persistence contexts or persistence boundaries;
- a substantially different persistence technology;
- messaging or background-processing infrastructure;
- distributed caching;
- microservices;
- a new authentication or authorization architecture;
- replacing an approved baseline framework or library.

Routine local implementation decisions already constrained by the
specification, the approved stack, existing code, or these rules do not require
approval.

## Accepted Architecture Decisions

Recorded by `architecture-decision`. None yet.
