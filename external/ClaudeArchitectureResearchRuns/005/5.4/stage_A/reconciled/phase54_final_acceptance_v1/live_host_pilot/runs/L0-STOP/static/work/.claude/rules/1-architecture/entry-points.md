---
paths:
  - "backend/**/*.cs"
  - "backend/**/*.csproj"
---

> Level: 1 Architecture · Owns: Api entry-point responsibilities and the public HTTP contract (status semantics, error contract shape, versioning, documentation truth) · Scope: backend · Loads: path rule · Depends on: CLAUDE.md, .claude/rules/1-architecture/backend-layers.md

# Entry Points and the HTTP Contract

Framework bindings (entry-point mechanism, result and error types) live in `.claude/rules/2-technology/`. Technique: `http-api` and `api-versioning` skills.

## Entry-point responsibilities

- HTTP entry points are thin: they bind and validate HTTP input, invoke Application services, and translate Application outcomes into HTTP responses.
- Entry points must not contain business logic, access the persistence context or concrete repositories, or construct infrastructure services manually.
- HTTP status codes and transport response semantics belong to Api. Application and Domain must not return web-framework result types or HTTP status codes.

## Contracts

- Do not duplicate equivalent DTOs across Api and Application merely to create layer-shaped types. Introduce transport-specific request/response contracts when separation from Application models provides a concrete boundary benefit.
- HTTP failures use a structured problem-details error contract whose machine-readable parts stay stable and safe for clients.

## Status semantics

- Choose 200/201/202/204 by actual HTTP semantics: do not return 200 for every outcome, 201 merely because a row was inserted internally, or 202 for work that already completed.
- A successful collection query with zero matches returns 200 with an empty collection, not 404 (default).
- Use 401 when authentication is missing or failed and 403 when an authenticated principal is not permitted. Returning 404 to hide a resource requires a deliberate, consistent security policy.
- Use 409 for a valid request that conflicts with current state; use 412 when an explicit HTTP precondition such as `If-Match` fails.

## Versioning

- Do not introduce API versioning merely because an API exists; add it when published compatibility or coexistence of client generations creates a concrete need.
- Once an API version is relied on by external clients, avoid silent breaking changes: a breaking contract change requires a new version or another explicitly approved compatibility strategy.
- When explicit versioning is required, use one strategy consistently; URL-segment versioning is the default unless project requirements justify another strategy.
- Do not create separate Domain or persistence models merely because the external API has several versions; isolate version-specific transport contracts at the Api boundary when practical.
- Deprecating or removing a published version follows `architecture-decision`.

## Documentation truth

- API documentation metadata must describe the API that actually runs — routes, important response statuses, schemas, and authentication behavior; do not document speculative responses.
