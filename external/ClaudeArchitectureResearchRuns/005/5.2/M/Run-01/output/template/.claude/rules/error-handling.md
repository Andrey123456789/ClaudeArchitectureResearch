---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
---

> Path-scoped rule. Owns: expected outcomes, exception flow, error contracts, validation boundaries, request cancellation, logging practice, outbound-dependency failure handling · Scope: backend · Loads: when backend C# or appsettings files are in context · Depends on: CLAUDE.md, docs/technology-stack.md

# Error Handling and Logging Rules

HTTP status semantics: `api.md`. Sensitive data in logs: `security.md`.
Technique: `aspnet-error-handling`, `logging`, and `httpclient-factory` skills.

## Expected Outcomes

- Default: represent common expected outcomes explicitly with the simplest
  contract that communicates the use case — `null`, `bool`, an explicit typed
  outcome, or a deliberately adopted Result model. Do not force a generic
  `Result<T>` pattern, and do not name Application outcome categories after
  HTTP semantics (`BadRequest`, `Unauthorized`, `InternalServerError`); prefer
  names such as `Validation`, `NotFound`, `Conflict`, or
  `BusinessRuleViolation`, mapped to HTTP in the API layer.
- Do not establish business exceptions as the default architecture, and do not
  throw and catch exceptions merely to jump between normal expected branches.

## Unexpected Exceptions

- Default: unexpected failures propagate to centralized `IExceptionHandler`
  handling. Catch an exception only when the current layer can recover,
  translate it into its own abstraction-level outcome, perform a defined
  fallback, add useful context while preserving the original exception, or
  perform required cleanup. Avoid repetitive catch/log/rethrow blocks.
- Log an unexpected exception once, at the boundary that handles it; do not log
  the same exception again across repositories, Application Services,
  Controllers, and the global handler.

## Error Contracts

- Default: `ProblemDetails` for non-validation HTTP failures and
  `ValidationProblemDetails` for request validation failures. Keep
  machine-readable error contracts stable and safe; human-readable exception
  messages are not the contract.
- Public API errors must not expose stack traces, SQL, connection strings,
  internal paths, secret values, or sensitive exception details.

## Validation Boundaries

- Validate each concern at the boundary that owns it: Api validates
  transport/request concerns; Application enforces use-case and straightforward
  workflow rules; Domain protects non-trivial invariants it genuinely owns;
  Infrastructure validates assumptions about external systems when needed.
- Use FluentValidation for explicit request and use-case validation where
  appropriate. Do not move Domain invariants into validators merely because the
  library is available, and do not duplicate the same rule mechanically at every
  layer.

## Request Cancellation

- Normal client-request cancellation is not a server failure: do not map it to
  a generic `500` response or log it as an unhandled application error.

## Logging

- Default: write log statements through `ILogger<T>` as structured message
  templates with stable property names; do not interpolate values into the
  message string.
- Default: when Serilog is configured, register it with
  `builder.Services.AddSerilog(...)` rather than `Host.UseSerilog()`, keep log
  levels, sinks, and overrides in environment-aware configuration, and keep
  Serilog-specific APIs at composition and provider boundaries while application
  code depends on `ILogger<T>`.

## Outbound Dependencies

- Every external I/O call must have a bounded execution time appropriate to the
  operation; avoid overlapping timeout mechanisms whose combined behavior is
  unclear.
- Retry only when repeating the operation is safe; do not automatically retry
  state-changing operations without idempotency or another concrete
  duplicate-prevention mechanism.
- Default: respect `Retry-After` or equivalent rate-limit guidance where
  appropriate; never retry indefinitely or aggressively.
- Use a fallback only when its result is semantically acceptable; do not hide
  correctness failures behind convenient default values.
- Caller cancellation is not a transient dependency failure: do not retry it or
  convert it into repeated outbound attempts.
