---
paths:
  - "backend/**/*.cs"
---

> Owner: expected vs. unexpected failures, HTTP error contracts, validation boundaries, exception logging, cancellation semantics, outbound dependency failure handling | Scope: backend | Loads: path (backend C#); read explicitly by `code-review` | Enforced: `code-review` checks

# Error Handling Rules

Technique: `aspnet-error-handling` skill; outbound clients and resilience:
`httpclient-factory` skill.

## Expected Outcomes

- Default: represent common expected outcomes (not found, rejected transition,
  duplicate, concurrency conflict, rejected business operation) explicitly with
  the simplest clear contract — `null`, `bool`, or a typed outcome — when that
  helps. Do not force a generic `Result<T>` pattern, and do not give Application
  outcome categories HTTP names such as `BadRequest` or `Unauthorized`; the API
  layer maps outcomes to HTTP.
- Do not establish business exceptions as the default architecture, and do not
  throw and catch exceptions merely to jump between normal expected branches.

## Unexpected Exceptions

- Default: unexpected failures propagate to centralized `IExceptionHandler`
  handling. Avoid repetitive catch/log/rethrow blocks in Controllers,
  Application Services, or repositories; catch only when the layer can recover,
  translate the failure into its own abstraction-level outcome, apply a defined
  fallback, add useful context while preserving the original exception, or
  perform required cleanup.
- Log an unexpected exception once, at the boundary that handles it; do not log
  the same exception again across repository, Application, Controller, and
  global handler.

## Error Contracts

- Default: `ProblemDetails` for non-validation HTTP failures and
  `ValidationProblemDetails` for request validation failures; keep
  machine-readable error contracts stable and safe for clients.
- Public API errors must not expose stack traces, SQL, connection strings,
  internal paths, secret values, or sensitive exception details.

## Validation Boundaries

- Validate each concern at the layer that owns it: API for transport and
  request-contract concerns, Application for use-case and straightforward
  workflow rules, Domain for non-trivial invariants it genuinely owns,
  Infrastructure for assumptions about external systems. Use FluentValidation
  for explicit request/use-case validators where appropriate; do not move Domain
  invariants into validators or duplicate one rule mechanically in every layer.

## Cancellation

- Normal client-request cancellation is not a server failure: do not map it to a
  generic `500` response or log it as an unhandled application error.
- Caller cancellation is not a transient dependency failure: do not retry because
  of it or convert it into repeated outbound attempts.

## External Dependency Failures

- External I/O calls must have a bounded execution time appropriate to the
  operation; avoid overlapping timeout mechanisms (per-attempt and total) whose
  combined behavior is unclear.
- Retry only when repeating the operation is safe; do not automatically retry
  state-changing operations without idempotency or another concrete
  duplicate-prevention mechanism.
- Default: when a dependency supplies `Retry-After` or equivalent rate-limit
  guidance, respect it where appropriate, and never retry indefinitely or
  aggressively.
- Use a fallback only when its result is semantically acceptable; do not hide
  correctness failures behind convenient default values.
