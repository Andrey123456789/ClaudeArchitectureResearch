---
paths:
  - "backend/**"
---
Kind: STD | Scope: backend | Capability: — | Loading: path-scoped (backend/**)

# Error Handling and Validation Standards

Technique and examples: `aspnet-error-handling` knowledge skill. Status-code semantics: `.claude/rules/backend/http-api.md`.

## Error contracts

- Default: use `ProblemDetails` for non-validation HTTP failures and `ValidationProblemDetails` for request validation failures. Keep machine-readable contract fields, such as stable error codes, stable and safe; clients must not have to rely on human-readable exception messages.
- Public API errors must not expose stack traces, SQL, connection strings, internal paths, secret values or sensitive exception details.

## Unexpected failures

- Default: unexpected failures propagate to centralized `IExceptionHandler` handling. Avoid repetitive catch/log/rethrow blocks; catch an exception only to recover, translate it into the current layer's outcome, apply a defined fallback, add useful context while preserving the original exception, or perform required cleanup.
- Log an unexpected exception once, at the boundary that handles it. Do not log the same exception again in repositories, Application services, controllers and the global exception handler.
- Normal client-request cancellation must not be mapped to a generic 500 response or logged as an unhandled application failure.

## Expected outcomes

- Default: represent common expected outcomes explicitly when useful (`null`, `bool` or a typed outcome). Do not force a generic `Result<T>` pattern, and do not use HTTP-named outcome categories (`BadRequest`, `Unauthorized`, `Forbidden`, ...) in Application; use names such as `Validation`, `NotFound`, `Conflict` or `BusinessRuleViolation` and map them in the Api layer.
- Do not establish business exceptions as the default architecture, and do not throw and catch exceptions merely to move between normal expected branches.

## Validation boundaries

- Use FluentValidation for explicit request and use-case validation where appropriate, and keep each concern at its owning boundary: transport and request-contract validation in Api, use-case and straightforward workflow rules in Application, genuinely non-trivial invariants in Domain, and assumptions about external systems in Infrastructure. Do not move Domain invariants into validators, and do not duplicate the same rule mechanically in every layer.
