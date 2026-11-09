---
paths:
  - "backend/**/*.cs"
  - "backend/**/*.csproj"
  - "frontend/**/*"
---

> Level: 1 Architecture · Owns: adopted architecture, patterns not adopted, accepted architecture decisions (decision summary) · Scope: backend, frontend · Loads: always (imported by CLAUDE.md) · Depends on: CLAUDE.md

# Architecture Overview

## Adopted architecture (Decided)

- **Backend: Clean Architecture** is the default architectural style, with four layers and inward-pointing dependencies:
  - **Domain** — business concepts, independent of infrastructure and transport;
  - **Application** — use-case orchestration and the inward-facing abstractions use cases need;
  - **Infrastructure** — persistence and external-service implementations of those abstractions;
  - **Api** — HTTP entry points and the composition root.
- **Frontend:** a separate client workspace that communicates with the backend only through the published HTTP API and is organized by feature.

Summary of the owning rules (same directory, loaded by path; workflows read them explicitly):

| Topic | Owner |
|---|---|
| Layer dependencies, Domain/Application responsibilities, composition and dependency injection | `backend-layers.md` |
| Repositories, Unit of Work, persistence-framework boundary | `persistence-boundary.md` |
| Api entry points and the public HTTP contract | `entry-points.md` |
| Expected outcomes, exceptions, validation boundaries | `outcomes.md` |
| Frontend structure, HTTP boundary, frontend state | `frontend-structure.md` |
| Physical code organization, test-project references | `code-organization.md` |

## Patterns not adopted

**Owned here:** CQRS handlers, mediator-based organization (with any mediator library), and Vertical Slice Architecture are not adopted. Introducing them requires approval.

Also not adopted by default (decision summary — the owning rule decides when an exception is justified):

- Rich Domain Model and DDD tactical patterns — `backend-layers.md` → Domain;
- a project-wide Result / railway-oriented model — `outcomes.md`;
- generic repository contracts consumed by Application — `persistence-boundary.md`;
- event sourcing, microservices, and new infrastructure categories — Reserved per CLAUDE.md → Decision control.

Reviews must not require or enforce patterns this architecture has not adopted.

## Accepted architecture decisions

Approved architecture changes are recorded here by `architecture-decision` (date · decision · scope · consequences · owning rule updated).

None yet.
