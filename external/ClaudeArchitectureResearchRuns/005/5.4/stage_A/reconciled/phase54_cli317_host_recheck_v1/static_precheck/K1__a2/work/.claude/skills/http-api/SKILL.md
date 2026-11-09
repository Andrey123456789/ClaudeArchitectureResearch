---
name: http-api
description: >
  Use when choosing HTTP status codes or response semantics for controllers:
  201/202/204, 400 vs 422, 401 vs 403, 404, 409/412/428, 429, 502/503/504,
  idempotency keys, ETags, Location, Retry-After.
---

> Kind: KNW | Scope: backend | Capability: — | Loading: on-demand knowledge

# HTTP API Semantics

Policy: `.claude/rules/backend/api.md`. Exception/failure handling: `aspnet-error-handling`. Keep status-code behavior consistent across similar endpoints.

## Successful responses

- **200 OK** — the operation completed and a representation is returned: successful `GET`; `PUT`/`PATCH` returning the updated representation; a `POST` that performs an operation without creating a resource; a query returning data (`return Ok(response);`). Empty collections: `200` with `[]` (rule: `.claude/rules/backend/api.md`), which also preserves the representation better than `204`.
- **201 Created** — the request created a new API resource; include `Location` when a stable resource URI exists. `PUT` may return `201` when it creates a resource at a previously non-existing URI. The question is whether the HTTP operation created a resource, not whether a row was inserted.

  ```csharp
  return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
  ```

- **202 Accepted** — processing accepted but not complete (long-running operation, background job, asynchronous import, queued processing); return an operation identifier or a `Location` for progress when practical (`AcceptedAtAction(...)`).
- **204 No Content** — completed with no body needed (successful `DELETE`, an update where returning the representation adds nothing). A `204` response must not contain a body. Choose consistently whether repeated `DELETE` of an absent resource returns `204` (desired state holds) or `404` (resource absent); do not mix conventions between equivalent resources.

## Conditional and cache responses

**304 Not Modified** only for a conditional request (`If-None-Match`/ETag, `If-Modified-Since`) whose cached representation is still valid; it carries no representation and is not a generic "nothing changed" business response.

## Client errors

- **400 Bad Request** — the HTTP request itself is invalid: malformed JSON, invalid shape, model-binding failure, invalid formatting, missing transport-level input. `[ApiController]` handles many of these automatically. Never use `400` for authentication failure.
- **401 Unauthorized** — authentication is missing or failed (no credentials, invalid or expired token, challenge required); normally produced by authentication middleware.
- **403 Forbidden** — authenticated but not allowed (missing permission, insufficient role, prohibited by policy); resending the same credentials does not help. An API that deliberately hides protected resources may return `404` instead, as a consistent policy.
- **404 Not Found** — the addressed resource does not exist, or its existence is deliberately hidden. A zero-match collection query (`GET /api/orders?customerId=...`) is not a `404` case (see 200 OK).
- **406 Not Acceptable** — no representation acceptable to the client's content negotiation (response format); not `415`.
- **409 Conflict** — a valid request conflicts with current state: duplicate resource where uniqueness is part of the state, incompatible state transition (an already completed order asked to cancel), conflicting concurrent operation, an idempotency key reused with a different payload. Not for malformed syntax.
- **412 Precondition Failed** — a supplied precondition is false, e.g. `If-Match: "version-7"` while the resource is at `"version-8"`.
- **415 Unsupported Media Type** — the request body format is unsupported (e.g. `Content-Type: application/xml` on a JSON-only endpoint).
- **422 Unprocessable Content** — structurally valid request with invalid semantics or business input (e.g. `startDate > endDate`, a business rule rejection that is not a state conflict). Some APIs deliberately use `400` for both; follow an established convention. New APIs that distinguish them: `400` = invalid HTTP/request contract, `422` = valid structure, invalid semantics.
- **428 Precondition Required** — the contract requires a precondition the client omitted (missing required `If-Match` → `428`; stale `If-Match` → `412`). Use it for other preconditions only when the contract defines them as mandatory.
- **429 Too Many Requests** — rate limiting rejected the request; include `Retry-After` when known. Never represent validation failure as rate limiting.

## Server and dependency failures

- **500 Internal Server Error** — unexpected failure without a more specific controlled outcome; centralized exception handling and `ProblemDetails`, without stack traces, SQL, internal paths, credentials, or exception details.
- **502 Bad Gateway** — acting as an intermediary and receiving an invalid or unusable upstream response; do not map every dependency failure to `502`.
- **503 Service Unavailable** — temporarily unable to handle the request (maintenance, a critical dependency the operation needs is down, chosen overload semantics); include `Retry-After` when meaningful.
- **504 Gateway Timeout** — acting as an intermediary and an upstream did not respond in time. Distinguish client cancellation of the incoming request, our own operation timing out, and an upstream timeout; not every `TaskCanceledException` is a `504`.

## Idempotency

`GET` is safe and idempotent, `PUT` idempotent, `DELETE` idempotent in intended state, `POST` generally not. For a `POST` that must not duplicate effects, consider an `Idempotency-Key` header associated with the request/result per the API contract; reuse with a materially different payload → `409`. Do not claim idempotency because duplicates are merely unlikely.

## Optimistic concurrency

When HTTP-level optimistic concurrency is part of the contract, use standard conditional semantics: `GET` → `ETag: "v7"`; `PUT`/`PATCH` with `If-Match: "v7"`; still v7 → success; changed to v8 → `412`; required `If-Match` absent → `428`. Do not replace these with custom status codes.

## Controller responsibility

```csharp
[HttpPost]
public async Task<ActionResult<OrderResponse>> Create(CreateOrderRequest request, CancellationToken cancellationToken)
{
    var result = await orders.CreateAsync(request, cancellationToken);

    return CreatedAtAction(nameof(GetById), new { id = result.Id }, result);
}
```

Application expresses meaningful outcomes without `IActionResult`, `ProblemDetails`, or status codes; the controller maps them.

## ProblemDetails

`ProblemDetails` for structured HTTP errors, `ValidationProblemDetails` for request validation failures. Machine-readable clients rely on stable error codes or contract fields, never on human-readable exception messages.

## Decision guide

| Situation | Default response |
|---|---|
| Successful query with representation | `200` |
| Empty collection | `200` + `[]` |
| Resource created | `201` + `Location` when available |
| Processing accepted but incomplete | `202` |
| Successful operation with no body | `204` |
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
| Invalid upstream response as intermediary | `502` |
| Temporarily unavailable | `503` |
| Upstream timeout as intermediary | `504` |
