---
name: http-api
description: HTTP status-code and response-semantics reference for ASP.NET Core Controllers. Use when designing or reviewing endpoints, ActionResult returns, Created/Accepted/NoContent, 400 vs 422, 409 vs 412 vs 428, 406 vs 415, 429 and Retry-After, 502/503/504, ETags, conditional requests, idempotency keys.
---

> Level: 2-technology · Owns: HTTP semantics reference and controller examples · Loading: on demand

# HTTP API Semantics

Rules: `.claude/rules/0-core/http-api.md` (response, failure, versioning rules) and the role rule that HTTP semantics belong to the entry point. Keep status behavior consistent across similar endpoints.

## Success responses

- **200 OK** — successful `GET`; `PUT`/`PATCH` returning the updated representation; a `POST` that performs an operation without creating a resource; a query returning data (an empty collection is `200` with `[]`, which is clearer for clients than `204`).
- **201 Created** — the HTTP operation created a new API resource; include `Location` when a stable URI exists. `PUT` may return `201` when it creates the target resource.

  ```csharp
  return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
  ```

- **202 Accepted** — processing accepted but incomplete (long-running operation, background job, async import, queued work); return an operation id or a `Location` where progress is observable: `AcceptedAtAction(nameof(GetOperation), new { id = operationId }, response)`.
- **204 No Content** — success with no body (`DELETE`, updates where returning the representation adds nothing); a `204` never carries a body. Choose one convention for repeated `DELETE` of an absent resource — `204` (final state holds) or `404` (resource absent) — and apply it consistently across equivalent resources.
- **304 Not Modified** — only for conditional requests (`If-None-Match`/ETag, `If-Modified-Since`) when the cached representation is still valid; never a generic "nothing changed" business response.

## Client errors

- **400 Bad Request** — the request itself is invalid: malformed JSON, invalid shape, model-binding failure, invalid formatting, missing transport-level input. `[ApiController]` handles many of these automatically. Never use `400` for authentication failure.
- **401 / 403** — authentication missing or failed vs. authenticated but not permitted (missing permission, insufficient role, policy prohibits the operation); the client cannot fix `403` by resending the same credentials. Authentication/authorization middleware normally produces these.
- **404 Not Found** — the addressed resource does not exist, or the API deliberately hides it.
- **406 Not Acceptable** — the server cannot produce a representation the client accepts (response negotiation). **415 Unsupported Media Type** — the server does not support the request body format (`Content-Type: application/xml` on a JSON-only endpoint).
- **409 Conflict** — valid request conflicting with current state: duplicate where uniqueness is resource state, incompatible state transition (cancelling a completed order), conflicting concurrent operation, idempotency key reused with a different payload. Not for malformed syntax.
- **412 Precondition Failed** — a supplied precondition is false (`If-Match: "version-7"` while the resource is at `"version-8"`).
- **422 Unprocessable Content** — structurally valid request with invalid semantics or business input (`startDate > endDate`, business rejection that is not a state conflict). Some APIs use `400` for both; follow an established convention. New APIs that distinguish them: `400` = invalid HTTP/request contract, `422` = valid structure, invalid semantics.
- **428 Precondition Required** — the contract requires a precondition the client omitted (missing required `If-Match` → `428`; stale `If-Match` → `412`).
- **429 Too Many Requests** — rate limiting rejected the request; include `Retry-After` when known. Never use it for validation failures.

## Server and dependency failures

- **500** — unexpected internal failure without a more specific controlled outcome; centralized handling and `ProblemDetails`.
- **502 Bad Gateway** — this API acts as an intermediary and received an invalid or unusable upstream response; do not map every dependency failure to `502`.
- **503 Service Unavailable** — temporarily unable to serve (maintenance, a critical dependency unavailable for this operation, overload); include `Retry-After` when meaningful.
- **504 Gateway Timeout** — as an intermediary, the upstream did not answer in time. Distinguish client cancellation, our own timeout, and upstream timeout; not every `TaskCanceledException` is a `504`.

## Idempotency and concurrency

`GET` is safe and idempotent; `PUT` is idempotent; `DELETE` is idempotent in intended final state; `POST` generally is not. For a `POST` that must not create duplicate effects, consider an `Idempotency-Key` stored with the request/result per the contract; claim idempotency only when it is implemented.

For HTTP-level optimistic concurrency prefer standard conditional requests: `GET` → `ETag: "v7"`; `PUT`/`PATCH` with `If-Match: "v7"`; unchanged → success; changed → `412`; required but absent → `428`. Do not replace these with custom status codes.

## Controller mapping

```csharp
[HttpPost]
public async Task<ActionResult<OrderResponse>> Create(CreateOrderRequest request, CancellationToken cancellationToken)
{
    var result = await orders.CreateAsync(request, cancellationToken);
    return CreatedAtAction(nameof(GetById), new { id = result.Id }, result);
}
```

Machine-readable clients rely on stable error codes or contract fields, never on human-readable exception messages.

## Decision guide

| Situation | Response |
| --- | --- |
| Query with representation | `200` |
| Empty collection | `200` + `[]` |
| Resource created | `201` + `Location` when available |
| Accepted, incomplete | `202` |
| Success without body | `204` |
| Conditional cache hit | `304` |
| Malformed/contract-invalid request | `400` |
| Missing/invalid authentication | `401` |
| Authenticated but forbidden | `403` |
| Resource absent | `404` |
| No acceptable response representation | `406` |
| Current-state conflict | `409` |
| Supplied precondition failed | `412` |
| Unsupported request content type | `415` |
| Valid structure, invalid semantics | `422` |
| Required precondition absent | `428` |
| Rate limited | `429` + `Retry-After` when known |
| Unexpected internal failure | `500` |
| Bad upstream response (intermediary) | `502` |
| Temporarily unavailable | `503` |
| Upstream timeout (intermediary) | `504` |
