---
paths:
  - "backend/**/*.cs"
---

> Path rule · Scope: backend · Owns expected-outcome, exception, exception-logging, HTTP error-contract, cancellation-response, and validation-boundary policy

# Error Handling Rules

HTTP status semantics: `.claude/rules/api.md`. Technique and examples:
`aspnet-error-handling` skill.

## Expected Outcomes

- Do not use exceptions casually for normal expected control flow. Represent
  common expected outcomes (not found, transition not allowed, duplicate,
  concurrency conflict, rejected business operation) explicitly when that
  improves clarity, using the simplest contract that communicates the use case:
  `null`, `bool`, an explicit typed outcome, or a deliberately adopted
  `Result<T>` pattern.
- Do not force a generic `Result<T>` pattern: it is not mandatory and is not
  introduced throughout the project merely because an operation can fail.
- Application outcome categories describe Application or business semantics
  (`Validation`, `NotFound`, `Conflict`, `BusinessRuleViolation`), not HTTP
  transport semantics; do not use HTTP-named categories such as `BadRequest`,
  `Unauthorized`, or `InternalServerError` in Application.
- Do not establish custom business exceptions as the default architecture, and
  do not throw and catch exceptions merely to jump between normal branches of a
  use case. Typed exceptions for selected cases are a consistent project-level
  decision when used.

## Unexpected Exceptions

By default, unexpected failures propagate to centralized handling at the outer
boundary; in ASP.NET Core APIs use `IExceptionHandler`. Avoid repetitive
catch/log/rethrow blocks in Controllers, Application Services, or repositories.

Catch an exception only when the current layer can meaningfully recover,
translate it into its own abstraction-level outcome, perform a defined fallback,
add useful context while preserving the original exception, or perform required
cleanup. Never swallow exceptions to continue execution.

## Exception Logging

Log an unexpected exception once, at the boundary that handles it. Do not log
the same exception repeatedly across repository, Application, Controller, and
the global exception handler. Expected outcomes such as not found or validation
rejection are not logged as application errors.

## HTTP Error Contracts

- By default use `ProblemDetails` for non-validation HTTP failures and
  `ValidationProblemDetails` for request-validation failures; keep the
  machine-readable error contract stable and safe, and do not make
  human-readable exception messages the machine-readable contract.
- Do not expose stack traces, SQL details, connection strings, internal paths,
  secret values, raw exception messages, or other sensitive exception details in
  public API errors.

## Cancellation

Normal client-request cancellation is not a server failure: do not map it to a
generic `500` response and do not log it as an unhandled application error.
Token propagation: `.claude/rules/performance.md` § Async and Cancellation.

## Validation Boundaries

Validate each concern at the layer that owns it. Use FluentValidation for
explicit request and use-case validation where appropriate.

- API validates transport and request-contract concerns.
- Application enforces use-case rules and straightforward workflow rules.
- Domain protects non-trivial domain invariants when the Domain genuinely owns
  that behavior; do not move Domain invariants into FluentValidation merely
  because the library is available.
- Infrastructure validates assumptions about external systems when needed.

Do not duplicate the same validation mechanically at every layer.
