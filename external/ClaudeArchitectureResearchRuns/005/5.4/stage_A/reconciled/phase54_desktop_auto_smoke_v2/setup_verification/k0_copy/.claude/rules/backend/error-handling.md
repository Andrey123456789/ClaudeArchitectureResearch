---
paths:
  - "backend/**/*.cs"
---

> Kind: STD | Scope: backend | Owner: failure handling — unexpected exceptions, expected outcomes, validation boundaries, error exposure, exception logging, request cancellation | Loading: path-scoped

# Error Handling Standard

Validation library: D-05.

See also: `rules/backend/api.md` (error contract format and status semantics).

## Unexpected failures

- Default: unexpected failures propagate to centralized `IExceptionHandler` handling; avoid repetitive catch/log/rethrow blocks in Controllers, Application Services and repositories. Catch an exception only where the layer can recover, translate it into its own abstraction-level outcome, apply a defined fallback, add useful context while preserving the original exception, or perform required cleanup.
- Public API errors must not expose stack traces, SQL, connection strings, internal paths, secret values or sensitive exception details.
- Unexpected exceptions must be logged once — by default at the boundary that handles them — and must not be logged repeatedly across repository, Application, Controller and global handler.

## Expected outcomes

- Default: represent common expected outcomes explicitly when useful (`null`, `bool`, a typed outcome), but do not force a generic `Result<T>` pattern, and do not use HTTP-named outcome categories (`BadRequest`, `Unauthorized`, `Forbidden`, ...) in Application. A project-wide Result model is Reserved (CLAUDE.md § Decisions).
- Do not establish business exceptions as the default architecture, and do not throw and catch exceptions merely to jump between normal expected branches.

## Validation boundaries

- Use FluentValidation for explicit request and use-case validation where appropriate, and keep each concern at its owning boundary: API validates transport and request-contract concerns, Application enforces use-case and straightforward workflow rules, Domain protects non-trivial invariants it genuinely owns, Infrastructure validates assumptions about external systems. Do not move Domain invariants into FluentValidation merely because the library is available, and do not duplicate the same rule mechanically at every layer.

## Cancellation

- Normal client-request cancellation is not a server failure: do not map it to a generic 500 response or log it as an unhandled application error.
