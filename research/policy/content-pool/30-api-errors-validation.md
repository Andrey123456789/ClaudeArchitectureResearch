# API, Errors & Validation

> Shared normalized content pool. Research artifact, not a runtime candidate file.
> Each policy ID must map to exactly one runtime normative owner in every experimental candidate.

HTTP semantics, error contracts, validation ownership, expected outcomes and exception policy.

## API-001 — HTTP semantics belong to API

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/http-api/SKILL.md#Core Principles`

HTTP status codes and transport response semantics belong to the API layer; Application/Domain must not return IActionResult or ASP.NET Core status codes.

## API-002 — Use structured error contracts

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/http-api/SKILL.md#Core Principles`, `templates/v2-baseline/.claude/skills/error-handling/SKILL.md#ProblemDetails`

Use ProblemDetails for non-validation HTTP failures and ValidationProblemDetails for request validation; keep machine-readable contracts stable and safe.

## API-003 — Use semantic success statuses

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/http-api/SKILL.md#Successful Responses`

Choose 200/201/202/204 according to actual HTTP semantics; do not return 200 for every outcome, 201 merely for an internal row insert, or 202 for already-completed work.

## API-004 — Empty collections return success

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/http-api/SKILL.md#200 OK`

A successful collection query with zero matches normally returns 200 with an empty collection, not 404.

## API-005 — 401/403 semantics

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/http-api/SKILL.md#401 Unauthorized`, `templates/v2-baseline/.claude/skills/authentication/SKILL.md#401 vs 403`

Use 401 when authentication is missing/failed and 403 when an authenticated principal is not permitted; deliberate 404 hiding requires a consistent security policy.

## API-006 — Conflict and precondition semantics

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/http-api/SKILL.md#409 Conflict`

Use 409 for valid requests conflicting with current state; use 412 when an explicit HTTP precondition such as If-Match fails.

## API-007 — Unexpected exceptions handled centrally

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/error-handling/SKILL.md#Unexpected Exceptions`

Unexpected failures normally propagate to centralized IExceptionHandler handling; avoid repetitive catch/log/rethrow blocks.

## API-008 — Do not leak failure internals

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/error-handling/SKILL.md#Global Exception Handler`

Do not expose stack traces, SQL details, connection strings, internal paths, secret values, or sensitive exception details in public API errors.

## API-009 — Expected outcomes are not system failures

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/error-handling/SKILL.md#Expected Application Outcomes`

Represent common expected outcomes explicitly when useful, but do not force a generic Result<T> pattern or use HTTP-named outcome categories in Application.

## API-010 — Validation stays at owning boundary

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/error-handling/SKILL.md#Request Validation`

Use FluentValidation for explicit request/use-case validation where appropriate; keep transport validation, Application rules and Domain invariants at their owning boundaries.

## API-011 — Exceptions are not normal branch control

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/error-handling/SKILL.md#Exceptions for Domain or Application Rules`

Do not establish business exceptions as the default architecture or throw/catch exceptions merely to jump between normal expected branches.

## API-012 — Log unexpected exceptions once

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/skills/error-handling/SKILL.md#Error Logging`

Unexpected exceptions should normally be logged once at the boundary that handles them; do not repeatedly log the same exception across repository, application, controller and global handler.
