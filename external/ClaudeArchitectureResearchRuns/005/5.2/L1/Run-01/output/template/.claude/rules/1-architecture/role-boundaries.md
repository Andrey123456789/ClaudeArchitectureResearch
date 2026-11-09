---
paths:
  - "backend/**/*"
---
> Level: 1-architecture | Owns: role-level boundary invariants for backend code and test projects | Scope: backend, backend-tests | Loads: path (backend files)

# Role Boundaries

Roles are defined in `roles.md`; the selected architecture frame maps them to
projects (`architecture.boundaries`). "Persistence-technology types" are the
types of the selected persistence implementation; its rules facet lists them.

## Domain model

- The domain model must stay independent of the persistence technology, ASP.NET
  Core, HTTP, and external-service implementation concerns.
- Default: simple domain entities. For CRUD-oriented applications and
  straightforward workflows, keep entities simple and enforce use-case and
  workflow rules in use-case units. Validation rules, immutable fields, status
  transitions, or allowed/forbidden edits do not by themselves justify a Rich
  Domain Model.
- Move behavior into the domain model only when non-trivial domain invariants
  or behavior materially benefit from domain-level encapsulation independently
  of a particular use case. Otherwise a Rich Domain Model or DDD tactical
  pattern requires approval, unless the approved specification already requires
  that design.
- Do not add factory methods, private setters, transition methods, Aggregate
  Roots, Domain Events, Specifications, Domain Services, systematic Value
  Objects, or similar DDD constructs merely to make a simple model appear more
  domain-driven.

## Use-case units and contracts

- Use-case units and the contracts they own must not depend on
  persistence-technology types (context and set types, persistence-backed
  deferred queries, query expressions, provider-specific types) or on ASP.NET
  Core transport types; keep infrastructure implementation details out of them.
- HTTP status codes and transport response semantics belong to entry points;
  use-case units and the domain model must not return `IActionResult` or ASP.NET
  Core status codes.
- A use-case unit becoming too large is a signal to reconsider its
  responsibilities, not an automatic reason to introduce another pattern.

## Entry points and composition

- ASP.NET Core Controllers are the default HTTP entry point. Entry points stay
  thin: bind and validate HTTP input, invoke use-case units, and translate
  outcomes into HTTP responses.
- Entry points must not contain business logic, access persistence-technology
  types or concrete persistence-access implementations, or construct adapters
  manually.
- Default: the host's `Program.cs` is the composition root and may register
  adapter implementations; entry points never consume adapter implementation
  types directly.
- Default: keep registration close to the owning role — the use-case side
  registers use-case services, the adapter side registers persistence
  implementations and adapters, and the composition root composes them.
- Do not duplicate equivalent DTOs between entry points and use-case units
  merely to create layer-shaped types; introduce transport-specific
  request/response contracts when the separation provides a concrete boundary
  benefit.
- Do not create separate domain or persistence models merely because the
  external API has multiple versions; isolate version-specific transport
  contracts at the entry point when practical.

## Persistence access and commit boundary

- Default: specific persistence-access contracts that represent cohesive
  use-case persistence needs, not table-mirroring generic CRUD contracts. In an
  approved DDD design, Aggregate Roots are natural contract boundaries.
- Persistence-access contracts must not expose persistence-backed deferred
  queries, context or set types, query expressions, or provider-specific types;
  they return materialized entities, collections, projections, or explicit
  result models. Query construction stays in the persistence implementation.
- Use-case units must not depend on a generic CRUD contract. A generic base may
  exist only inside the persistence implementation, where it removes genuine
  duplication without replacing the technology's query capabilities;
  use-case-specific queries belong in concrete implementations.
- Default: the commit boundary is the normal commit point of a use case —
  persistence-access implementations stage changes and do not commit
  independently, and the use-case unit decides when the operation is ready to
  commit.
- Persistence-access implementations participating in one use case must share
  the same scoped unit of work. They are injected explicitly into their
  consumers; the commit-boundary contract must not become a repository container
  or service locator.
- Default: do not introduce explicit transaction APIs until a concrete use case
  requires control beyond the normal commit.
- The persistence technology is an adapter detail: use it normally and fully
  inside the persistence implementation (do not cripple it to preserve a
  generic abstraction), but never leak its concepts into use-case units or the
  domain model.

## Other adapters

- Keep cache technology out of the domain model, and do not leak infrastructure
  cache APIs into use-case units without a deliberate boundary abstraction.
- Adapters translate remote HTTP responses into use-case-facing contracts; do
  not leak `HttpResponseMessage` or remote transport concerns into use-case
  units unless the use case explicitly models HTTP.

## Test projects

Do not give backend test projects broader production references than their
test scope requires; they follow the same dependency discipline as the
production architecture.
