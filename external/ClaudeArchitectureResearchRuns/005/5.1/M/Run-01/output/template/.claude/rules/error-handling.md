---
paths:
  - "backend/**/*.cs"
---

> Owns: expected vs. unexpected failure handling, validation boundaries, cancellation handling, application logging, outbound dependency failure semantics | Scope: backend | Loads: path

# Error Handling Rules

HTTP status semantics and public error contracts: `api.md`. Sensitive-data
logging: `security.md`. Technique: `aspnet-error-handling`, `logging`,
`httpclient-factory` skills.

## Expected Outcomes

- Represent common expected outcomes (not found, transition not allowed,
  duplicate, concurrency conflict, rejected business operation) with the
  simplest contract that communicates the use case — `null`, `bool`, an explicit
  typed outcome, or a deliberately adopted `Result<T>`. Do not force a generic
  `Result<T>` pattern merely because an operation can fail.
- Application outcome categories describe Application/business semantics (for
  example `Validation`, `NotFound`, `Conflict`, `BusinessRuleViolation`), not
  HTTP-named categories such as `BadRequest` or `Forbidden`.
- Do not establish business exceptions as the default architecture, and do not
  throw/catch exceptions merely to jump between normal expected branches.

## Unexpected Exceptions

Unexpected failures propagate by default to centralized handling
(`IExceptionHandler` in ASP.NET Core APIs). Avoid broad, repetitive
catch/log/rethrow blocks in Controllers, Application Services, or repositories.
Catch only when the current layer can recover, translate the failure into its
own abstraction-level outcome, perform a defined fallback, add useful context
while preserving the original exception, or perform required cleanup. Never
swallow an exception just to continue execution.

## Validation Boundaries

Use FluentValidation for explicit request/use-case validation where appropriate,
and keep each concern at the layer that owns it: API validates transport/request
concerns; Application enforces use-case and straightforward workflow rules;
Domain protects non-trivial invariants it genuinely owns; Infrastructure
validates assumptions about external systems when needed. Do not move Domain
invariants into FluentValidation merely because the library is available, and
do not duplicate the same rule mechanically at every layer.

## Cancellation

Normal client-request cancellation is not a server failure: do not map it to a
generic `500` or log it as an unhandled application error. Propagation of
`CancellationToken`: `performance.md`.

## Logging

- Log an unexpected exception once, at the boundary that handles it; do not log
  the same exception repeatedly across repository, Application, Controller, and
  the global handler. Expected outcomes such as not-found or validation
  rejection are normally not logged as errors.
- By default, use `ILogger<T>` structured message templates with stable property
  names; avoid string interpolation that turns structured values into opaque
  text.
- When configuring Serilog, use the DI-integrated `AddSerilog` registration by
  default and keep sinks, levels, and overrides in environment-aware
  configuration.

## Outbound Dependency Calls

- Every external I/O call must have a bounded execution time appropriate to the
  operation; avoid overlapping timeout mechanisms whose combined behavior is
  unclear (distinguish per-attempt from total-operation timeouts).
- Retry only when repeating the operation is safe. Do not automatically retry
  state-changing operations without idempotency or another concrete
  duplicate-prevention mechanism.
- By default, respect `Retry-After` or equivalent rate-limit guidance from a
  dependency where appropriate; never retry indefinitely or aggressively.
- Use a fallback only when its result is semantically acceptable; never hide a
  correctness failure behind a convenient default value.
- Caller cancellation is not a transient dependency failure: do not retry it or
  convert it into repeated outbound attempts.
