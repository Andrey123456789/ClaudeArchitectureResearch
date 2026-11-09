---
paths:
  - "backend/**/*"
---

> Kind: STD | Scope: backend | Capability: — | Loading: path-scoped (frontmatter paths)

# HTTP API, Errors, and Validation Standard

## HTTP semantics

- HTTP status codes and transport response semantics belong to the Api layer; Application and Domain must not return `IActionResult` or ASP.NET Core status codes.
- Success statuses must follow actual HTTP semantics (200/201/202/204): never 200 for every outcome, 201 merely because a row was inserted internally, or 202 for work that already completed.
- Default: a successful collection query with zero matches returns 200 with an empty collection, not 404.
- Use 401 when authentication is missing or failed and 403 when an authenticated principal is not permitted. Returning 404 to hide a protected resource requires a deliberate, consistent security policy.
- Use 409 for a valid request that conflicts with current state, and 412 when an explicit HTTP precondition such as `If-Match` fails.

## Error contracts and exceptions

- Default: `ProblemDetails` for non-validation HTTP failures and `ValidationProblemDetails` for request validation failures; keep machine-readable error contracts stable and safe.
- Default: unexpected failures propagate to centralized `IExceptionHandler` handling; avoid repetitive catch/log/rethrow blocks.
- Never expose stack traces, SQL, connection strings, internal paths, secret values, or sensitive exception details in public API errors.
- Log an unexpected exception once, at the boundary that handles it; never log the same exception again across repository, Application, controller, and global handler.
- Normal client-request cancellation must not be mapped to a generic 500 or logged as an unhandled application failure.

## Expected outcomes and validation

- Default: represent common expected outcomes explicitly when useful (`null`, `bool`, a typed outcome); do not force a generic `Result<T>` pattern, and do not use HTTP-named outcome categories in Application.
- Use FluentValidation for explicit request/use-case validation where appropriate. Validation must stay at its owning boundary: transport/request concerns in Api, use-case and straightforward workflow rules in Application, non-trivial invariants in Domain, assumptions about external systems in Infrastructure when needed; do not duplicate the same rule mechanically at every layer.
- Must not establish business exceptions as the default architecture or throw and catch exceptions merely to jump between normal expected branches.

Technique: `http-api`, `aspnet-error-handling`.
