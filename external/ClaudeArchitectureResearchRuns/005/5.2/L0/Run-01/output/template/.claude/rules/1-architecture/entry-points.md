---
paths:
  - "backend/**/*.cs"
---

> Level: 1 Architecture | Owns: HTTP entry-point responsibilities, HTTP response semantics, API contracts, versioning, documentation truth | Scope: backend | Loads: path | Depends on: 1-architecture/backend-layers.md

# Entry Points

## Responsibilities

- HTTP entry points are thin: they bind and validate HTTP input, invoke
  Application services, and translate Application outcomes into HTTP responses.
- Entry points must not contain business logic, access the persistence context
  or concrete repositories, or construct infrastructure services manually.
- HTTP status codes and transport response semantics belong to the Api layer;
  Application and Domain must not return web-framework result types or HTTP
  status codes.

## Contracts

- Do not duplicate equivalent DTOs across Api and Application merely to create
  layer-shaped types; introduce transport-specific request/response contracts
  when separation from Application models provides a concrete boundary benefit.
- Do not create separate Domain or persistence models merely because the
  external API has multiple versions; isolate version-specific transport
  contracts at the API boundary when practical.

## HTTP Semantics

- Choose `200`, `201`, `202`, or `204` from the actual HTTP semantics: do not
  return `200` for every outcome, `201` merely because a row was inserted
  internally, or `202` for work that already completed.
- Default: a successful collection query with zero matches returns `200` with
  an empty collection, not `404`.
- Use `401` when authentication is missing or failed and `403` when an
  authenticated principal is not permitted; returning `404` to hide a resource
  requires a deliberate, consistent security policy.
- Use `409` for a valid request that conflicts with current state; use `412`
  when an explicit HTTP precondition such as `If-Match` fails.

## Versioning

- Do not introduce API versioning merely because an API exists; add it when
  published compatibility or coexisting client generations create a concrete
  need (adopting it is Reserved: CLAUDE.md, Decision Control).
- Once an API version is relied on by external clients, avoid silent breaking
  changes; a breaking contract change normally requires a new version or
  another explicitly approved compatibility strategy.
- Default: when explicit versioning is required, use one strategy
  consistently; URL-segment versioning is the default unless project
  requirements justify another.

## Documentation

- API documentation metadata must describe the API that actually runs —
  routes, important response statuses, schemas, and authentication behavior —
  considering the whole pipeline; do not document speculative responses.

Web-framework binding: → `2-technology/aspnet-core.md`. Status-code depth: → `http-api` skill.
