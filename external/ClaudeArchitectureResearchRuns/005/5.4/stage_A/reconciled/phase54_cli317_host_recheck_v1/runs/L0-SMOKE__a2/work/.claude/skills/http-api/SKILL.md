---
name: http-api
description: >
  Use when choosing Controller responses: status codes, Created/Accepted/NoContent,
  Location and Retry-After, ETags and preconditions, idempotency keys, upstream
  failures.
---

> Level: 2 Technology · Owns: HTTP API response technique and status-code reference (knowledge) · Scope: backend · Loads: on invocation · Depends on: .claude/rules/1-architecture/entry-points.md, .claude/rules/2-technology/aspnet-core.md

# HTTP API Semantics

Policy owners: entry-point responsibilities, success/empty-collection/401/403/409/412 semantics, versioning, documentation truth → `.claude/rules/1-architecture/entry-points.md`; ProblemDetails types and Controllers → `2-technology/aspnet-core.md`; failure exposure → `0-core/security-principles.md`. This skill adds technique and the less-common cases. Keep status-code behavior consistent across similar endpoints.

## Success responses in ASP.NET Core

```csharp
return Ok(response);                                   // 200 with a representation

return CreatedAtAction(nameof(GetById),                // 201 + Location for a new resource
    new { id = created.Id }, created);

return AcceptedAtAction(nameof(GetOperation),          // 202 + where to observe progress
    new { id = operationId }, response);

return NoContent();                                    // 204 — never with a body
```

- `PUT` may return 201 when it creates a resource at a previously non-existing URI.
- 202 fits long-running operations, background jobs, asynchronous imports, queued processing; return an operation identifier or a `Location` when practical.
- 204 fits a successful `DELETE` or an update whose representation adds no value. For repeated `DELETE` of an absent resource choose one convention — 204 (desired state holds) or 404 (resource absent) — and use it consistently across equivalent resources.
- For an empty collection (`entry-points.md`), `200` with `[]` also beats `204`: it preserves the resource representation for clients.

## Less-common statuses

| Situation | Response |
|---|---|
| Conditional request; client's cached representation still valid (`If-None-Match`/ETag, `If-Modified-Since`) | `304` (no representation; not a business "nothing changed") |
| Malformed JSON, invalid shape, binding failure, missing transport-level input | `400` (not for authentication failure) |
| Cannot produce a representation acceptable to the client's content negotiation | `406` |
| Request body media type not supported (e.g. XML to a JSON-only endpoint) | `415` |
| Structurally valid request with invalid semantics (e.g. `startDate > endDate`) | `422` — or `400` when the project deliberately uses 400 for both; follow the established convention |
| Contract requires a precondition (e.g. `If-Match`) but it is absent | `428` |
| Rate limiting rejected the request | `429` + `Retry-After` when known (never for validation failures) |
| Unexpected internal failure | `500` via centralized handling and ProblemDetails |
| Acting as intermediary; upstream returned an invalid/unusable response | `502` (do not convert every dependency failure to 502) |
| Temporarily unable to serve (maintenance, required dependency down, chosen overload semantics) | `503` + `Retry-After` when meaningful |
| Acting as intermediary; upstream did not respond in time | `504` |

`401` means authentication is missing, invalid, or expired; authentication middleware normally produces it. The client generally cannot fix `403` by resending the same credentials.

Distinguish three cancellation/timeout cases before choosing a response: the client cancelled the incoming request; our own operation timed out; an upstream dependency timed out. Not every `TaskCanceledException` is a 504.

## Conflicts and duplicates

Typical 409 cases: a duplicate where uniqueness is part of resource state; a state transition incompatible with the current state (order already completed + cancel request); a conflicting concurrent operation; an idempotency key reused with a different payload. 409 is never for malformed syntax.

## Idempotency

`GET` is safe and idempotent; `PUT` is idempotent; `DELETE` is idempotent in intended state; `POST` generally is not. When a repeated `POST` must not duplicate effects, consider an `Idempotency-Key` that the server associates with the request and its result; a reused key with a materially different payload → `409`. Do not claim idempotency merely because duplicates are unlikely.

## Optimistic concurrency

```text
GET          → ETag: "v7"
PUT/PATCH    → If-Match: "v7"
still v7     → update succeeds
now v8       → 412 Precondition Failed
If-Match required but absent → 428 Precondition Required
```

Use standard conditional-request semantics instead of custom status codes.

## Controller translation

```csharp
[HttpPost]
public async Task<ActionResult<OrderResponse>> Create(
    CreateOrderRequest request,
    CancellationToken cancellationToken)
{
    var result = await orders.CreateAsync(request, cancellationToken);
    return CreatedAtAction(nameof(GetById), new { id = result.Id }, result);
}
```

Application expresses outcomes without `IActionResult`, `ProblemDetails`, or status codes; the Controller maps them.

## ProblemDetails

Machine-readable clients rely on stable error codes or contract fields, never on human-readable exception messages. Error-handling technique: the `aspnet-error-handling` skill.
