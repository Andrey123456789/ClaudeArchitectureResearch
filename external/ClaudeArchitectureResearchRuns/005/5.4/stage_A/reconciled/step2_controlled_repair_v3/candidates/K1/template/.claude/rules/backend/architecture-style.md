---
paths:
  - "backend/**/*"
---

> Kind: STD | Scope: backend | Capability: architecture/clean-architecture | Loading: path-scoped (frontmatter paths)

# Architecture Style — Clean Architecture Frame

Placement belongs to this frame; technique belongs to the leaf capabilities that bind to it.

| Role | Project | Responsibility |
|---|---|---|
| Domain | `backend/<Name>.Domain` | Business concepts, independent of infrastructure and transport |
| Application | `backend/<Name>.Application` | Use-case orchestration; persistence, external-service, and commit-boundary abstractions |
| Infrastructure | `backend/<Name>.Infrastructure` | Implementations of Application abstractions (persistence, external adapters) |
| Api | `backend/<Name>.Api` | HTTP entry point and composition root |

## Dependency direction

- Dependencies must point inward: Domain references no other application project; Application references Domain; Infrastructure references Application and Domain; Api references Application and may reference Infrastructure only for composition and dependency registration. Inner layers never depend on outer layers, and Domain and Application never reference Infrastructure-specific types.
- If a feature seems to need an outward reference, reconsider the abstraction boundary instead of adding the reference.

## Domain

- Domain must stay independent of the persistence technology, ASP.NET Core, HTTP, and external-service implementation concerns.
- Default: simple domain entities. Straightforward CRUD and workflow rules, including validation rules, immutable fields, status transitions, and allowed or forbidden edits, belong in Application Services and do not by themselves justify a richer model.
- Move behavior into Domain only when non-trivial domain invariants or behavior materially benefit from domain-level encapsulation independent of a particular use case. Otherwise a Rich Domain Model or DDD tactical patterns require approval, unless the approved specification already requires them.
- Must not add factories, private setters, transition methods, Aggregate Roots, Domain Events, Specifications, Domain Services, systematic Value Objects, or similar DDD constructs merely to make a simple model look domain-driven.
- When an approved DDD design contains Aggregate Roots, they are the natural repository-boundary candidates.

## Application

- Default: Application Services orchestrate use cases, coordinating Domain objects, repositories, external-service abstractions, and the Unit of Work. A service growing too large is a signal to reconsider its responsibilities, not an automatic reason for another pattern.
- Application must define the persistence and external-service abstractions its use cases require and keep infrastructure implementation details out.
- Application must not depend on persistence-technology types or APIs (database context, entity sets, query or provider types) or on ASP.NET Core transport types.

## Commit boundary

- Default: `IUnitOfWork` is the commit boundary of an Application use case; repositories stage changes and Application Services decide when the operation is ready to commit.
- Repositories participating in one use case must share the same scoped Unit of Work and therefore the same persistence context; repositories are injected explicitly into their consumers, and `IUnitOfWork` must not become a repository container or service locator.

## Composition and contracts

- Default: `Program.cs` in Api is the application composition root and may register Infrastructure implementations.
- Default: registration stays near the owning layer: Application registers Application services, Infrastructure registers persistence and adapters, and Api composes them (`AddApplication()`, `AddInfrastructure(configuration)`).
- Must not duplicate equivalent DTOs across Api and Application merely to create layer-shaped types; introduce transport-specific request/response contracts in Api when separation from Application models provides a concrete boundary benefit.

Enforced by: `.claude/scripts/facets/architecture-style.cjs` (project references; run by hooks and `verify`). Scaffolding layout: `project-structure`.
