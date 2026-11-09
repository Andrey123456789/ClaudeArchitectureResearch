---
paths:
  - "backend/**/*.cs"
---

> Level: 1 Architecture · Owns: expected outcomes vs exceptions, centralized failure handling, validation boundaries · Scope: backend · Loads: path rule · Depends on: CLAUDE.md, .claude/rules/1-architecture/backend-layers.md

# Outcomes, Exceptions, and Validation Boundaries

Framework bindings (central exception handler, validation library) live in `.claude/rules/2-technology/`. Logging of exceptions: `0-core/logging-principles.md`.

## Expected outcomes

- Represent common expected outcomes explicitly when useful — `null`, `bool`, an explicit typed outcome, or a deliberately adopted Result model — using the simplest contract that communicates the use case (default).
- Do not force a generic `Result<T>` pattern on the project merely because an operation can fail, and do not use HTTP-named outcome categories (such as `BadRequest`, `Unauthorized`, `InternalServerError`) in Application; describe Application semantics (`Validation`, `NotFound`, `Conflict`, `BusinessRuleViolation`) and map them to HTTP in Api.
- Do not establish custom business exceptions as the default architecture, and do not throw and catch exceptions merely to jump between normal expected branches of a use case.

## Unexpected failures

- Unexpected failures propagate to centralized boundary handling (default). Avoid repetitive catch/log/rethrow blocks in entry points, Application Services, and repositories.
- Catch an exception only when the current layer can meaningfully recover, translate it into its own abstraction-level outcome, perform a defined fallback, add useful context while preserving the original exception, or perform required cleanup. Do not swallow failures to continue execution.

## Validation boundaries

Validate each concern at the layer that owns it:

- Api validates transport and request-contract concerns.
- Application enforces use-case input rules and straightforward workflow rules.
- Domain protects non-trivial invariants that genuinely belong to Domain.
- Infrastructure validates assumptions about external systems when needed.

Do not duplicate the same rule mechanically at every layer, and do not move Domain invariants into request validators merely because a validation library is available.
