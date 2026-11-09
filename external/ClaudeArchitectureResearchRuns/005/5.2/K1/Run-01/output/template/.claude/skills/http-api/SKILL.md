---
name: http-api
description: Use when choosing HTTP status codes or response shapes for ASP.NET Core controllers — Created/Accepted/NoContent, validation and conflict responses, 401/403, ETags and If-Match preconditions, idempotency keys, rate limiting, upstream failures, Location and Retry-After headers.
---
Kind: KNW | Scope: backend | Capability: — | Loading: on invocation

# HTTP API Semantics

Rules: `.claude/rules/backend/http-api.md` (layer ownership, success/empty-collection/auth/conflict semantics) and `.claude/rules/backend/error-handling.md` (error contracts). This skill holds definitions, examples and the less common codes. Keep status-code behavior consistent across similar endpoints.

## Successful responses

### 200 OK

The operation completed and a representation is returned: a successful `GET`, a `PUT` or `PATCH` returning the updated representation, a `POST` that performs an operation without creating a resource, or a query returning data. Empty collection results: `.claude/rules/backend/http-api.md` → Status semantics.

```csharp
return Ok(response);
```

### 201 Created

The request created a new API resource. Include `Location` when a stable resource URI exists. `PUT` may also return `201` when it creates a resource at a previously non-existing URI.

```csharp
return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
```

### 202 Accepted

Processing was accepted but is not complete when the response is sent: long-running operations, background jobs, asynchronous imports, queued processing. When practical, return an operation identifier or a `Location` where the client can observe progress.

```csharp
return AcceptedAtAction(nameof(GetOperation), new { id = operationId }, response);
```

### 204 No Content

The operation completed and no body is needed: a successful `DELETE`, or an update where returning the representation adds no value. A `204` response must not contain a body. For repeated `DELETE` of an already absent resource, choose one convention (`204` because the desired state holds, or `404` because the resource does not exist) and apply it consistently to equivalent resources.

## Conditional and cache responses

### 304 Not Modified

Only for a conditional request (`If-None-Match`/ETag, `If-Modified-Since`) whose cached representation is still valid. It carries no representation and is not a generic "nothing changed" business response.

## Client request errors

- **400 Bad Request**: the HTTP request itself is invalid: malformed JSON, invalid request shape, model-binding failure, invalid formatting, missing required transport-level input. `[ApiController]` produces many of these automatically. Not for authentication failure.
- **401 Unauthorized**: authentication is missing or failed (no credentials, invalid or expired token, challenge required). Authentication middleware normally produces it.
- **403 Forbidden**: authenticated, but the principal is not allowed (missing permission, insufficient role, prohibited by policy). Resending the same credentials does not help. Hiding protected resources behind `404`: `.claude/rules/backend/http-api.md` → Status semantics.
- **404 Not Found**: the addressed resource does not exist, or the API deliberately hides it.
- **406 Not Acceptable**: the server cannot produce a representation acceptable to the client's content negotiation (response format). Not to be confused with `415`.
- **409 Conflict**: a valid request conflicts with the current state: a duplicate where uniqueness is part of resource state, an incompatible state transition (an already completed order asked to cancel), a conflicting concurrent operation, or an idempotency key reused with a different payload. Not for malformed syntax.
- **412 Precondition Failed**: a client-supplied precondition is false, for example `If-Match: "version-7"` while the resource is at `"version-8"`.
- **415 Unsupported Media Type**: the server does not support the request body format (`Content-Type: application/xml` for a JSON-only endpoint).
- **422 Unprocessable Content**: the request is syntactically and structurally valid but its semantic or business content is invalid (for example `startDate > endDate`), when that is not a state conflict. Some APIs deliberately use `400` for both transport and semantic validation; follow an established project convention. APIs that distinguish them use `400` for an invalid request contract and `422` for structurally valid but semantically invalid input.
- **428 Precondition Required**: the contract requires a precondition the client did not send (missing required `If-Match` → `428`; stale `If-Match` → `412`). Use it for other preconditions only when the contract explicitly defines them as mandatory.
- **429 Too Many Requests**: rate limiting rejected the request; include `Retry-After` when the server knows when another attempt is appropriate. Validation failures are not rate limiting.

## Server and dependency failures

- **500 Internal Server Error**: an unexpected failure without a more specific controlled outcome, produced by centralized exception handling with `ProblemDetails` and without internal details.
- **502 Bad Gateway**: this API acts as an intermediary and receives an invalid or unusable upstream response. Do not convert every dependency failure into `502` mechanically.
- **503 Service Unavailable**: the service temporarily cannot handle the request (maintenance, a critical dependency unavailable for this operation, deliberate overload shedding); include `Retry-After` when meaningful.
- **504 Gateway Timeout**: this API acts as an intermediary and an upstream service did not respond in time. Distinguish a client-cancelled request, a timeout of our own operation and an upstream timeout; not every `TaskCanceledException` is a `504`.

## Idempotency

`GET` is safe and idempotent; `PUT` is idempotent; `DELETE` is idempotent in its intended state semantics; `POST` is generally not idempotent. When a repeated `POST` must not duplicate effects, consider an `Idempotency-Key` header associated with the request and result according to the API contract; reuse of a key with a materially different payload is reasonably a `409`. Do not claim idempotency merely because duplicates are unlikely.

## Optimistic concurrency

When HTTP-level optimistic concurrency is part of the contract, use the standard conditional flow instead of custom status codes:

```text
GET                          → ETag: "v7"
PUT/PATCH with If-Match: "v7"
  current still v7           → update succeeds
  current changed to v8      → 412 Precondition Failed
  If-Match required, absent  → 428 Precondition Required
```

## Controller responsibility

Responsibilities: `.claude/rules/backend/architecture-style.md` → Api and `.claude/rules/backend/http-api.md` → Layer ownership. Example of the translation:

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

## Decision guide

| Situation | Default response |
|---|---|
| Successful query with representation | `200` |
| Resource created | `201` + `Location` when available |
| Processing accepted but incomplete | `202` |
| Successful operation with no body | `204` |
| Conditional cache hit | `304` |
| Malformed or contract-invalid request | `400` |
| Missing or invalid authentication | `401` |
| Authenticated but forbidden | `403` |
| Resource absent | `404` |
| Cannot produce an acceptable representation | `406` |
| Current-state conflict | `409` |
| Supplied precondition failed | `412` |
| Unsupported request content type | `415` |
| Valid structure but invalid semantics | `422` |
| Required precondition absent | `428` |
| Rate limited | `429` + `Retry-After` when known |
| Unexpected internal failure | `500` |
| Invalid upstream response as intermediary | `502` |
| Temporarily unavailable | `503` |
| Upstream timeout as intermediary | `504` |
