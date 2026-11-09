---
paths:
  - "backend/**/*.cs"
---

> Level: 1 Architecture | Owns: expected outcomes vs. exceptions, centralized unexpected-failure handling, exception logging boundary, validation boundaries | Scope: backend | Loads: path | Depends on: 1-architecture/backend-layers.md

# Outcomes

## Expected Outcomes

- Default: represent common expected outcomes (not found, rejected transition,
  duplicate, concurrency conflict, rule rejection) explicitly when useful, using
  the simplest contract that communicates the use case (`null`, `bool`, a typed
  outcome). Do not force a generic `Result<T>` pattern, and do not use
  HTTP-named outcome categories (`BadRequest`, `Unauthorized`, `Forbidden`, ...)
  in Application; prefer semantic names such as `NotFound`, `Conflict`, or
  `BusinessRuleViolation`.
- Do not establish business exceptions as the default architecture, and do not
  throw and catch exceptions merely to jump between normal expected branches.

## Unexpected Failures

- Default: unexpected failures propagate to centralized handling at the outer
  boundary; avoid repetitive catch/log/rethrow blocks in entry points,
  Application Services, or repositories. Catch only to recover, translate into
  the current layer's own outcome, perform a defined fallback, add context while
  preserving the original exception, or clean up.
- Log an unexpected exception once, at the boundary that handles it; do not log
  the same exception again in repository, Application, entry point, and the
  global handler.

## Validation Boundaries

- Keep validation at its owning boundary: the Api layer validates transport and
  request-contract concerns, Application enforces use-case and straightforward
  workflow rules, Domain protects non-trivial invariants it genuinely owns, and
  Infrastructure validates assumptions about external systems. Do not duplicate
  the same rule mechanically in every layer.

Centralized handler and validation-library bindings: → `2-technology/aspnet-core.md`, `3-project/decisions.md`.
