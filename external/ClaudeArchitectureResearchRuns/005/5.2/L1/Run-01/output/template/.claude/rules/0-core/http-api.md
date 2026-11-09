---
paths:
  - "backend/**/*"
---
> Level: 0-core | Owns: HTTP response semantics, error contracts, API compatibility and versioning need | Scope: backend | Loads: path (backend files)

# HTTP API Rules

## Error contracts

Default: use `ProblemDetails` for non-validation HTTP failures and
`ValidationProblemDetails` for request-validation failures. Keep
machine-readable error contracts stable and safe; clients rely on stable codes
or contract fields, never on human-readable exception messages.

## Status semantics

- Choose `200`/`201`/`202`/`204` by the actual HTTP semantics of the outcome.
  Do not return `200` for every outcome, `201` merely because a row was inserted
  internally (`201` means a new API resource; include `Location` when a stable
  URI exists), or `202` for work already completed synchronously. A `204`
  response carries no body.
- Default: a successful collection query with zero matches returns `200` with
  an empty collection, not `404`.
- Use `401` when authentication is missing or failed and `403` when an
  authenticated principal is not permitted. Returning `404` to hide a protected
  resource requires a deliberate, consistent security policy.
- Use `409` for a valid request that conflicts with the current state; use `412`
  when an explicit HTTP precondition such as `If-Match` fails.
- Keep status-code behavior consistent across equivalent endpoints.

## Compatibility and versioning

- Do not introduce API versioning merely because an API exists; add it when
  published compatibility or coexisting client generations create a concrete
  need (adopting it is a Reserved decision).
- Once an API version is relied on by external clients, do not make silent
  breaking changes: a breaking contract change requires a new version or
  another explicitly approved compatibility strategy. Compilation success does
  not establish compatibility.
- Default: when explicit versioning is required, use one strategy
  consistently; URL-segment versioning is the default unless project
  requirements justify another.

Detailed status-code reference and examples: `http-api`. Deprecation procedure:
`architecture-decision`.
