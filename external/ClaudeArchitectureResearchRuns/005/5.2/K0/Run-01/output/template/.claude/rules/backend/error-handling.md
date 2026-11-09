---
paths:
  - "backend/**"
---
<!-- Kind: STD | Scope: backend | Owns: error contracts, exception flow, expected outcomes, validation boundaries, cancellation outcomes | Loads: path-scoped (backend/**) -->
# Backend Error Handling and Validation Standards

## Error Contracts

- **Default:** `ProblemDetails` for non-validation HTTP failures and `ValidationProblemDetails` for request validation. Keep machine-readable error contracts stable and safe: clients rely on stable codes or contract fields, not on human-readable exception messages.
- Public API errors **must not** expose stack traces, SQL, connection strings, internal paths, secret values or sensitive exception details.

## Exception Flow

- **Default:** unexpected failures propagate to centralized `IExceptionHandler` handling. Catch an exception only when the current layer can recover, translate it into its own abstraction-level outcome, apply a defined fallback, add useful context while preserving the original exception, or perform required cleanup; avoid repetitive catch/log/rethrow blocks.
- **Must not** establish business exceptions as the default architecture, or throw and catch exceptions merely to jump between normal expected branches.
- **Default:** represent common expected outcomes explicitly when useful (`null`, `bool`, a typed outcome), without forcing a generic `Result<T>` pattern and without HTTP-named outcome categories such as `BadRequest` or `Unauthorized` in Application.
- Unexpected exceptions **must** be logged once, at the boundary that handles them, and **must not** be logged again across repository, Application, controller and global handler.

## Validation Boundaries

- Validation **must** stay at its owning boundary: Api validates transport and request concerns, Application enforces use-case and straightforward workflow rules, Domain protects non-trivial invariants it genuinely owns, Infrastructure validates assumptions about external systems. Use FluentValidation (DEC-VAL-01) for explicit request/use-case validation where appropriate; do not move Domain invariants into validators, and do not duplicate the same rule mechanically at every layer.

## Cancellation Outcomes

- Normal client-request cancellation **must not** be mapped to a generic `500` response or logged as an unhandled application failure.

Technique: `aspnet-error-handling`, `http-api` knowledge skills.
