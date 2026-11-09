---
paths:
  - "backend/**/*.cs"
---

> **Policy rule** · Owns: expected outcomes, exception flow, error logging boundary, HTTP error contracts, cancellation as non-failure, validation boundaries · Scope: backend · Loading: path (backend C# files)

# Error Handling Rules

## Expected Outcomes

Do not use exceptions casually for normal expected control flow.

Represent expected outcomes using the simplest contract that communicates the
use case clearly.

Depending on the situation this may be:

- `null`;
- `bool`;
- an explicit typed outcome;
- a deliberately adopted `Result<T>` pattern.

`Result<T>` is not mandatory.

Do not introduce a Result abstraction throughout the project solely because an
operation can fail.

Application outcome categories describe Application or business semantics
(for example `Validation`, `NotFound`, `Conflict`, `BusinessRuleViolation`), not
HTTP transport semantics; do not name Application categories `BadRequest`,
`Unprocessable`, `Unauthorized`, `Forbidden`, or `InternalServerError` merely
because they map to HTTP codes. The API layer maps them to HTTP.

Do not establish custom business exceptions as the default architecture, and do
not throw and catch exceptions merely to jump between normal branches of a use
case. Typed exceptions for selected cases require a consistent project-level
decision.

## Unexpected Exceptions

Default: unexpected failures propagate to an appropriate outer boundary.

In ASP.NET Core APIs, use centralized exception handling such as
`IExceptionHandler`.

Do not add broad `try/catch` blocks throughout Controllers, Application Services,
or repositories merely to log and rethrow the same failure.

Catch an exception when the current layer can meaningfully:

- recover;
- translate it into its own abstraction-level outcome;
- perform a defined fallback;
- add useful context while preserving the original exception;
- perform required cleanup.

## Logging

Log an unexpected exception once, at the boundary that handles it.

Do not log the same exception repeatedly across Infrastructure, Application,
Controller, and the global exception handler.

Default: expected outcomes such as not-found, validation failures, or rejected
business operations are not logged as application errors. Logging rules:
`backend-runtime.md`; technique: the `logging` skill.

## HTTP Errors

HTTP error semantics belong to the API layer.

Default: use `ProblemDetails` for non-validation HTTP failures and
`ValidationProblemDetails` for request validation failures. Keep the
machine-readable contract (status, stable error code when clients need one, safe
title/detail, trace identifier when appropriate) stable and safe; human-readable
exception messages are not the machine-readable contract.

Do not expose raw exception messages, stack traces, SQL, connection strings,
internal paths, secret values, or other sensitive implementation details in public
API errors. Development diagnostics may show more through development tooling;
public contracts stay safe.

HTTP status semantics: `api.md`.

## Cancellation

Normal client-request cancellation is not an unexpected server failure. Do not
map it to a generic `500` response or log it as an unhandled application error.

Cancellation propagation: `performance.md`; caller cancellation and retries:
`backend-runtime.md`.

## Validation Boundaries

Validate concerns at the layer that owns them.

- API validates transport/request concerns.
- Application enforces use-case rules and straightforward workflow rules.
- Domain protects non-trivial domain invariants when the Domain genuinely owns
  that behavior.
- Infrastructure validates assumptions made about external systems when needed.

Use FluentValidation for explicit request and use-case validation where
appropriate. Do not move Domain invariants into FluentValidation merely because
the library is available.

Do not duplicate the same validation mechanically at every layer.

Detailed implementation guidance belongs to the `aspnet-error-handling` skill.
