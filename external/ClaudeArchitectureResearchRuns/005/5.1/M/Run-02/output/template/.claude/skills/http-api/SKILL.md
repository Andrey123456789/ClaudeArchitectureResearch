---
name: http-api
description: >
  Use when choosing status codes or response shapes in controllers:
  Created/Accepted/NoContent, 400 vs. 422, 401/403/404, 409/412/428, 429 and
  Retry-After, 5xx, ETags and If-Match, idempotency keys, Location headers.
---

> Owner: HTTP status-code reference and controller response technique (normative core lives in rules) | Scope: backend | Loads: on demand — knowledge | Enforced: none

# HTTP API Semantics

Policy: `.claude/rules/api.md` § HTTP Semantics (layer ownership, success codes,
empty collections, 401/403, 409/412) and `.claude/rules/error-handling.md`
§ Error Contracts. Keep status-code behavior consistent across similar
endpoints.

## Successful Responses

### 200 OK

The operation completed and a representation is returned: successful `GET`,
`PUT`/`PATCH` returning the updated representation, a `POST` that performs an
operation without creating a resource, a query returning data.

```csharp
return Ok(response);
```

An empty collection is a successful collection result:

```http
200 OK

[]
```

Prefer `200` with `[]` over `204` for an empty collection; it preserves the
resource representation for clients.

### 201 Created

The request created a new API resource. Include a `Location` header when a
stable resource URI exists:

```csharp
return CreatedAtAction(
    nameof(GetById),
    new { id = created.Id },
    created);
```

`PUT` may also return `201` when it creates a resource at a previously
non-existing target URI. The question is whether the HTTP operation created an API
resource, not whether a row was inserted.

### 202 Accepted

Processing was accepted but is not complete: long-running operations,
background jobs, asynchronous imports, queued work. When practical, return an
operation identifier or a `Location` where progress can be observed:

```csharp
return AcceptedAtAction(
    nameof(GetOperation),
    new { id = operationId },
    response);
```

### 204 No Content

The operation succeeded and no body is needed: a successful `DELETE`, or an
update where returning the representation adds nothing. A `204` response has no
body.

```csharp
return NoContent();
```

Pick one convention for a repeated `DELETE` of an already absent resource — `204`
(the desired final state holds) or `404` (the addressed resource does not exist)
— and apply it consistently across equivalent resources.

## Conditional and Cache Responses

### 304 Not Modified

Only for a conditional request (`If-None-Match` / ETag, `If-Modified-Since`)
when the client's cached representation is still valid; the response carries no
representation. It is not a generic "nothing changed" business response.

## Client Request Errors

### 400 Bad Request

The HTTP request itself is invalid: malformed JSON, invalid shape, model-binding
failure, invalid formatting, missing required transport-level input. With
`[ApiController]`, many binding and validation failures are handled
automatically. Not for authentication failures.

### 401 Unauthorized

Authentication is missing or failed: no credentials, invalid or expired token,
challenge required. Authentication middleware normally produces it.

### 403 Forbidden

Authentication succeeded but the principal is not allowed: missing permission,
insufficient role, prohibited by authorization policy. Resending the same
credentials will not help.

### 404 Not Found

The addressed resource does not exist, or the API deliberately hides its
existence. A collection query such as `GET /api/orders?customerId=...` with zero
matches returns `200 []`.

### 406 Not Acceptable

The server cannot produce a representation acceptable under the client's
content negotiation (response format). Do not confuse it with `415`.

### 409 Conflict

The request is valid but conflicts with the current state: a duplicate where
uniqueness is part of resource state, a state transition incompatible with the
current state, a conflicting concurrent operation, an idempotency key reused with
a different payload.

```text
Order already completed
    + request asks to cancel it
    → 409 Conflict
```

Not for malformed syntax.

### 412 Precondition Failed

The client supplied a precondition that is false, for example
`If-Match: "version-7"` while the current version is `"version-8"`. Prefer `412`
over a generic `409` because an explicit HTTP precondition failed.

### 415 Unsupported Media Type

The server does not support the request body format (for example
`Content-Type: application/xml` on a JSON-only endpoint).

### 422 Unprocessable Content

The request is syntactically and structurally valid but its semantic or business
content is invalid: impossible business values, a business-rule rejection that is
not a state conflict, a semantically invalid combination such as
`startDate > endDate`.

Some APIs deliberately use `400` for both transport and semantic validation;
follow an established project convention. New APIs that distinguish the two use:

```text
400 → invalid HTTP/request contract
422 → structurally valid request, invalid semantics/business input
```

### 428 Precondition Required

The API contract requires a precondition the client did not send:

```text
missing required If-Match → 428
provided but stale If-Match → 412
```

Use `428` for other mandatory preconditions only when the contract explicitly
defines them.

### 429 Too Many Requests

Rate limiting rejected the request. Include `Retry-After` when the server knows
when another attempt is appropriate. Validation failures are not rate limiting.

## Server and Dependency Failures

### 500 Internal Server Error

Unexpected failure inside the application when no more specific controlled
outcome applies, produced by centralized exception handling with
`ProblemDetails`.

### 502 Bad Gateway

This API acts as an intermediary and received an invalid or unusable upstream
response. Not every dependency failure is a `502`.

### 503 Service Unavailable

The service is temporarily unable to handle the request: intentional
maintenance, a critical dependency unavailable for this operation, temporary
overload. Include `Retry-After` when a meaningful retry time is known.

### 504 Gateway Timeout

This API acts as an intermediary and an upstream service did not respond in
time. Not every internal `TaskCanceledException` is a `504`: distinguish a
client-cancelled request, our own operation timing out, and an upstream timeout —
the right response depends on which occurred and the role this API plays.

## Idempotency

- `GET` is safe and idempotent; `PUT` is idempotent; `DELETE` is idempotent in
  intended state semantics; `POST` generally is not.
- When a repeated `POST` must not create duplicate effects, consider an
  `Idempotency-Key` header associated with the request and result per the API
  contract; reusing a key with a materially different payload → `409`.
- Do not claim idempotency merely because duplicate requests are unlikely.

## Optimistic Concurrency

When HTTP-level optimistic concurrency is part of the contract, use standard
conditional requests rather than custom status codes:

```text
GET
→ ETag: "v7"

PUT/PATCH
→ If-Match: "v7"

current is still v7  → update succeeds
current changed to v8 → 412 Precondition Failed
If-Match required but absent → 428 Precondition Required
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

Machine-readable clients rely on stable error codes or contract fields in
`ProblemDetails`, not human-readable exception messages.

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
