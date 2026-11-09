---
paths:
  - "backend/**/*"
---
> Level: 0-core | Owns: exception flow, expected outcomes, failure logging, cancellation, safe error exposure | Scope: backend | Loads: path (backend files)

# Error Handling Rules

## Expected outcomes

- Default: represent common expected outcomes explicitly with the simplest
  contract that communicates the use case (`null`, `bool`, an explicit typed
  outcome, or a deliberately adopted `Result<T>`). Do not force a generic
  `Result<T>` pattern throughout the project merely because an operation can
  fail.
- Use-case outcome categories describe use-case or business semantics
  (`Validation`, `NotFound`, `Conflict`, `BusinessRuleViolation`), not HTTP
  transport names such as `BadRequest`, `Unprocessable`, `Unauthorized`,
  `Forbidden`, or `InternalServerError`; entry points map them to HTTP.
- Do not establish business exceptions as the default architecture, and do not
  throw and catch exceptions merely to jump between normal expected branches.

## Unexpected failures

- Default: unexpected failures propagate to centralized handling
  (`IExceptionHandler` in ASP.NET Core APIs). Do not add broad `try/catch`
  blocks in entry points, use-case units, or adapters merely to log and rethrow.
- Catch an exception only when the current layer can recover, translate it into
  its own abstraction-level outcome, perform a defined fallback, add useful
  context while preserving the original exception, or perform required cleanup.
  Never swallow an exception simply to continue.
- Log an unexpected exception once, at the boundary that handles it; do not log
  the same exception repeatedly across adapters, use-case units, entry points,
  and the global handler. By default, expected outcomes (not found, validation
  failure, rejected business operation) are not logged as application errors.

## Public error exposure

Do not expose stack traces, SQL statements, connection strings, internal paths,
secret values, or sensitive exception details in public API errors.

## Cancellation

Normal client-request cancellation is not a server failure: do not map it to a
generic `500` response or log it as an unhandled application failure.

Error-contract shapes and HTTP status semantics: `http-api.md`. Technique:
`aspnet-error-handling`.
