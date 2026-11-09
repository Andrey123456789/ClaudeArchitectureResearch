---
paths:
  - "backend/**/*.cs"
---

> Owns: HTTP error contracts, exception flow, expected outcomes, validation boundaries, failure logging, cancellation, dependency-failure handling | Scope: backend | Loads: path-scoped (backend C# files)

# Error Handling Rules

Status-code semantics: `api.md`. Implementation technique and examples:
`aspnet-error-handling` skill (outbound resilience depth: `httpclient-factory`).

## Error Contracts

Use `ProblemDetails` for non-validation HTTP failures and
`ValidationProblemDetails` for request validation by default. Keep
machine-readable error contracts (stable error codes or contract fields) stable
and safe; clients must not depend on human-readable exception messages.

## Unexpected Exceptions

- Unexpected failures propagate to centralized `IExceptionHandler` handling by
  default. Avoid broad `try/catch` blocks in Controllers, Application Services,
  or repositories that only log and rethrow. Catch an exception only when the
  current layer can recover, translate it into its own abstraction-level
  outcome, perform a defined fallback, add useful context while preserving the
  original exception, or perform required cleanup.
- Never expose stack traces, SQL details, connection strings, internal paths,
  secret values, or sensitive exception details in public API errors.

## Expected Outcomes

- Represent common expected outcomes explicitly when that improves clarity
  (`null`, `bool`, an explicit typed outcome, or a deliberately adopted
  `Result<T>`), but do not force a generic `Result<T>` pattern on the project.
  Application outcome categories describe Application or business semantics
  (`NotFound`, `Conflict`, `Validation`, `BusinessRuleViolation`), not HTTP
  names (`BadRequest`, `Unauthorized`, `Forbidden`, `InternalServerError`).
- Do not establish business exceptions as the default architecture, and do not
  throw and catch exceptions merely to jump between normal expected branches.

## Validation Boundaries

Use FluentValidation for explicit request and use-case validation where
appropriate, and keep each concern at the layer that owns it: API validates
transport/request concerns; Application enforces use-case and straightforward
workflow rules; Domain protects non-trivial invariants it genuinely owns;
Infrastructure validates assumptions about external systems. Do not move Domain
invariants into validators merely because the library is available, and do not
duplicate the same rule mechanically at every layer.

## Failure Logging

Log an unexpected exception once, at the boundary that handles it; do not log
the same exception repeatedly across repository, Application, Controller, and
the global exception handler. By default, expected outcomes such as not-found,
validation failures, or rejected business operations are not logged as
application errors.

## Cancellation

Normal client-request cancellation is not a server failure: do not map it to a
generic `500` response or log it as an unhandled application failure.
Propagating `CancellationToken`: `performance.md`.

## Dependency Failures and Resilience

- External I/O calls must have a bounded execution time appropriate to the
  operation. Distinguish per-attempt from total-operation timeouts and avoid
  overlapping timeout mechanisms whose combined behavior is unclear.
- Retry only when repeating the operation is safe: never automatically retry a
  state-changing operation (for example POST or PATCH) without an idempotency
  key, naturally idempotent semantics, or another concrete deduplication
  mechanism.
- When a dependency supplies `Retry-After` or equivalent rate-limit guidance,
  respect it where appropriate; do not retry indefinitely or aggressively.
- Use a fallback only when its result is semantically acceptable; do not hide
  correctness failures behind convenient default values.
- Caller cancellation is not a transient dependency failure: do not retry it or
  convert it into repeated outbound attempts.
