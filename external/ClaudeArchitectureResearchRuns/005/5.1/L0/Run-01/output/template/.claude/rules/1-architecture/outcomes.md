---
paths:
  - "backend/**"
---

> Level: 1 Architecture · Owns: expected outcomes vs exceptions, central failure handling, validation boundaries, cancellation outcome · Scope: backend · Loads: path

# Outcomes and Failures

## Expected outcomes

- **Default:** represent common expected outcomes explicitly with the simplest contract that communicates the use case — `null`, `bool`, or an explicit typed outcome. Do not force a generic `Result<T>` pattern; a project-wide Result model is a Reserved decision.
- **Default:** name Application outcome categories by application or business meaning (`Validation`, `NotFound`, `Conflict`, `BusinessRuleViolation`), never by HTTP names (`BadRequest`, `Unprocessable`, `Unauthorized`, `Forbidden`, `InternalServerError`); the Api layer maps them to HTTP.
- **Must not** establish business exceptions as the default architecture, or throw and catch exceptions merely to jump between normal expected branches.

## Unexpected failures

- **Default:** unexpected failures propagate to one centralized handler at the outer boundary. Avoid repetitive catch/log/rethrow blocks in entry points, services and repositories. Catch an exception only to recover, translate it into the current layer's own outcome, apply a defined fallback, add context while preserving the original exception, or perform required cleanup — never to swallow it and continue.
- **Must not** map normal client-request cancellation to a generic `500` response or log it as an unhandled application failure.

## Validation boundaries

- **Must** validate each concern at the layer that owns it:
  - Api — transport and request-contract concerns;
  - Application — use-case input and straightforward workflow rules, using the project's standard explicit validation library where a validator is clearer;
  - Domain — non-trivial invariants that the Domain genuinely owns;
  - Infrastructure — assumptions about external systems, when needed.

  Do not move Domain invariants into request validators merely because a validation library is available, and do not duplicate the same rule mechanically at every layer.
