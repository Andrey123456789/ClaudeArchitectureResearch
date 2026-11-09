---
name: http-api
description: Use when designing or reviewing Controller endpoints and responses — status codes, Created/Accepted/NoContent, validation and conflict responses, 401/403, conditional requests and ETags, idempotency keys, rate limiting, upstream failures, Location and Retry-After headers.
---
<!-- Kind: KNW | Scope: backend | Owns: HTTP status-code reference and response technique | Loads: on demand (model-invoked) -->
# HTTP API Semantics

Standards: `rules/backend/api.md` (status ownership, success statuses, empty collections, 401/403, 409/412) and `rules/backend/error-handling.md` (ProblemDetails, error exposure). This skill is the detailed status-code reference. Keep status behavior consistent across similar endpoints.

## Successful Responses

### 200 OK

The operation completed and a representation is returned: successful `GET`; `PUT`/`PATCH` returning the updated representation; a `POST` that performs an operation without creating a resource; a query returning data.

```csharp
return Ok(response);
```

An empty collection is still a successful collection result:

```http
200 OK

[]
```

`200` with `[]` preserves the resource representation and is clearer for clients than `204`.

### 201 Created

The request created a new API resource. Include a `Location` header when a stable resource URI exists:

```csharp
return CreatedAtAction(
    nameof(GetById),
    new { id = created.Id },
    created);
```

`PUT` may also return `201` when it creates a resource at a previously non-existing target URI. The question is whether the HTTP operation created a resource, not whether a row was inserted.

### 202 Accepted

Processing was accepted but is not complete when the response is sent — long-running operations, background jobs, asynchronous imports, queued processing. When practical, return an operation identifier or a `Location` where progress can be observed:

```csharp
return AcceptedAtAction(
    nameof(GetOperation),
    new { id = operationId },
    response);
```

### 204 No Content

The operation completed and no body is needed — successful `DELETE`, or an update where returning the representation adds no value. A `204` response has no body.

```csharp
return NoContent();
```

For a repeated `DELETE` of an already absent resource, either `204` (the desired final state holds) or `404` (the addressed resource does not exist) is valid — pick one convention and use it for equivalent resources.

## Conditional and Cache Responses

### 304 Not Modified

Only for a conditional request (`If-None-Match` / ETag, `If-Modified-Since`) whose cached representation is still valid; it carries no representation. Not a generic "nothing changed" business response.

## Client Request Errors

### 400 Bad Request

The HTTP request itself is invalid: malformed JSON, invalid request shape, model-binding failure, invalid formatting, missing required transport-level input, or a request that cannot be interpreted under the API contract. With `[ApiController]`, many binding and validation failures are handled automatically. Not for authentication failure.

### 401 Unauthorized

Despite the name: authentication is missing or failed — no required credentials, invalid or expired token, challenge required. Authentication middleware normally produces it.

### 403 Forbidden

Authentication succeeded but the principal may not perform the operation — missing permission, insufficient role, operation prohibited by policy. Resending the same credentials does not help. Hiding protected resources behind `404` instead: `rules/backend/api.md` § Status Codes.

### 404 Not Found

The addressed resource does not exist, or the API deliberately hides its existence. A collection query such as `GET /api/orders?customerId=...` with zero matches is `200` with `[]`.

### 406 Not Acceptable

The server cannot produce a representation acceptable to the client's content negotiation — about the response format, unlike `415`.

### 409 Conflict

A valid request conflicts with the current state: duplicate resource where uniqueness is part of resource state, incompatible state transition, conflicting concurrent operation, an idempotency key reused with a different payload.

```text
Order already completed
    + request asks to cancel it
    → 409 Conflict
```

Not for malformed syntax.

### 412 Precondition Failed

A client-supplied precondition is false — for example `If-Match: "version-7"` while the current version is `"version-8"`. Prefer it over a generic `409` because an explicit HTTP precondition failed.

### 415 Unsupported Media Type

The server does not support the request representation, for example `Content-Type: application/xml` on a JSON-only endpoint. `415` concerns the request body format; `406` the acceptable response formats.

### 422 Unprocessable Content

The request is syntactically and structurally valid, but its semantic or business content is invalid: impossible business values, a business-rule rejection that is not a state conflict, a semantically invalid combination of valid fields (for example `startDate > endDate`). Some APIs deliberately use `400` for both transport and semantic validation — follow an established project convention. New APIs that distinguish them:

```text
400 → invalid HTTP/request contract
422 → structurally valid request, invalid semantics/business input
```

### 428 Precondition Required

The API contract requires a precondition the client did not send — for example a `PUT` that requires `If-Match`:

```text
missing required If-Match → 428
provided but stale If-Match → 412
```

Use `428` for other mandatory preconditions only when the API contract defines them as such.

### 429 Too Many Requests

Rate limiting rejected the request; include `Retry-After` when the server knows when another attempt is appropriate. Not for application-level validation failures.

## Server and Dependency Failures

### 500 Internal Server Error

Unexpected failure inside the application when no more specific controlled outcome exists; produced by centralized exception handling with `ProblemDetails`, without internal details (`aspnet-error-handling` skill).

### 502 Bad Gateway

This API acts as an intermediary and received an invalid or unusable upstream response. Avoid converting every dependency failure into `502` mechanically.

### 503 Service Unavailable

The service temporarily cannot handle the request — intentional maintenance, a critical dependency unavailable for this operation, or temporary overload when the service chooses `503` semantics. Include `Retry-After` when a meaningful retry time is known.

### 504 Gateway Timeout

This API acts as an intermediary and an upstream service did not respond within the required time. Not for every internal `TaskCanceledException` — distinguish a client-cancelled request, our own operation timing out, and an upstream timeout; the correct response depends on which occurred and what role this API plays.

## Idempotency

Typically `GET` is safe and idempotent, `PUT` is idempotent, `DELETE` is idempotent in intended state semantics, and `POST` is not. When a repeated `POST` is not allowed to create duplicate effects, consider an idempotency key:

```http
Idempotency-Key: ...
```

The server associates the key with the request/result according to the API contract; reuse of a key with a materially different payload is a reasonable `409`. Do not claim idempotency merely because duplicate requests are unlikely.

## Optimistic Concurrency

When HTTP-level optimistic concurrency is part of the contract, prefer standard conditional request semantics over custom status codes:

```text
GET
→ ETag: "v7"

PUT/PATCH
→ If-Match: "v7"

current is still v7
→ update succeeds

current changed to v8
→ 412 Precondition Failed

If-Match required but absent
→ 428 Precondition Required
```

## Controller Responsibility

Controllers translate Application outcomes into HTTP outcomes:

```csharp
[HttpPost]
public async Task<ActionResult<OrderResponse>> Create(
    CreateOrderRequest request,
    CancellationToken cancellationToken)
{
    var result = await orders.CreateAsync(
        request,
        cancellationToken);

    return CreatedAtAction(
        nameof(GetById),
        new { id = result.Id },
        result);
}
```

## ProblemDetails

`ProblemDetails` for structured HTTP errors, `ValidationProblemDetails` for request validation failures; machine-readable clients rely on stable error codes or contract fields, not human-readable exception messages.

## Decision Guide

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
| Cannot produce acceptable response representation | `406` |
| Current-state conflict | `409` |
| Supplied precondition failed | `412` |
| Unsupported request content type | `415` |
| Valid request structure but invalid semantics | `422` |
| Required precondition absent | `428` |
| Rate limited | `429` + `Retry-After` when known |
| Unexpected internal failure | `500` |
| Invalid/failed upstream response while acting as intermediary | `502` |
| Temporarily unavailable | `503` |
| Upstream timeout while acting as intermediary | `504` |
