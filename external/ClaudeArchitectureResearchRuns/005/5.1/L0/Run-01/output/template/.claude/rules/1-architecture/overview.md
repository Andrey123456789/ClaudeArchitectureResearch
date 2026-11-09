---
paths:
  - "docs/architecture/**"
  - "docs/decisions/**"
---

> Level: 1 Architecture · Owns: adopted architecture and patterns not adopted (decision summary) · Scope: backend, frontend · Loads: always (imported by CLAUDE.md)

# Architecture Overview

Decision summary for planning. Rules are owned by the modules named in each line.

## Adopted (Decided)

- **Backend: Clean Architecture** with four roles — Domain, Application, Infrastructure, Api (HTTP entry points and composition root). Dependencies point inward. Rules: `backend-layers.md`.
- **Use cases:** Application Services orchestrate; Application owns the repository, unit-of-work and external-service abstractions it needs; Infrastructure implements them. Rules: `backend-layers.md`, `persistence-boundary.md`.
- **Domain:** simple entities by default. Rules: `backend-layers.md`.
- **HTTP surface:** thin entry points, protocol-correct semantics, explicit API evolution. Rules: `entry-points.md`.
- **Outcomes and failures:** expected outcomes are explicit; unexpected failures go to central handling; validation stays at its owning boundary. Rules: `outcomes.md`.
- **Frontend:** single-page application organized by feature with an explicit data-access boundary. Rules: `frontend-structure.md`.
- **Physical structure** follows actual responsibilities. Rules: `code-organization.md`.

All module paths above are in `.claude/rules/1-architecture/`.

## Not adopted (Decided — adopting any of these is Reserved)

- **Must not** introduce CQRS handlers, mediator-based request dispatch or organization, or Vertical Slice Architecture unless explicitly approved. A service becoming too large is a signal to reconsider its responsibilities, not a reason to adopt another pattern.
- Event sourcing, microservices, messaging or background-processing infrastructure, distributed caching.
- Rich Domain Model and DDD tactical patterns — adoption criterion in `backend-layers.md`.
- A project-wide Result/railway model — `outcomes.md`.
- Generic repository contracts exposed to Application — `persistence-boundary.md`.

## Recording

Accepted architecture decisions are recorded in this file (and in `docs/decisions/` when the project keeps decision records) through the `architecture-decision` workflow.
