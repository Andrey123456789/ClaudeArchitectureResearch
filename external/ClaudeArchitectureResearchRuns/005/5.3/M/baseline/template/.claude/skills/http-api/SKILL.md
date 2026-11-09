---
name: http-api
description: >
  Use when choosing HTTP status codes or response shapes in Controllers:
  2xx/4xx/5xx results, Location, ETags and preconditions, idempotency keys, rate
  limiting, Retry-After.
---

> Owns: HTTP status-code reference and response examples (no policy) | Scope: backend | Loads: on demand (knowledge skill)

# HTTP API Semantics

Policy owners: status semantics, versioning, Swagger, and health endpoints —
`.claude/rules/api.md`; error contracts and exception handling —
`.claude/rules/error-handling.md`.

## Successful Responses

### 200 OK

Typical cases: successful `GET`; `PUT`/`PATCH` returning the updated
representation; a `POST` that performs an operation without creating a
resource; a query returning data.

```csharp
return Ok(response);
```

An empty collection is still a successful collection result:

```http
200 OK

[]
```

`200` with `[]` preserves the resource representation and is clearer for clients
than `204` for an empty collection.

### 201 Created

Include a `Location` header identifying the created resource when a stable
resource URI exists:

```csharp
return CreatedAtAction(
    nameof(GetById),
    new { id = created.Id },
    created);
```

`PUT` may also return `201` when it creates a resource at a previously
non-existing target URI. The question is whether the HTTP operation created a new
API resource.

### 202 Accepted

For accepted but incomplete processing — long-running operations, background
jobs, asynchronous imports, queued processing. When practical, return an
operation identifier or a `Location` where the client can observe progress:

```csharp
return AcceptedAtAction(
    nameof(GetOperation),
    new { id = operationId },
    response);
```

### 204 No Content

For a successful operation with no response body, such as `DELETE` or an update
where returning the representation adds no value:

```csharp
return NoContent();
```

Choose consistently whether a repeated `DELETE` of an already absent resource
returns `204` (the desired final state holds) or `404` (the addressed resource
does not exist); either can be valid, but do not mix them between equivalent
resources.

## Conditional and Cache Responses

### 304 Not Modified

Only for a conditional request (`If-None-Match`/ETag, `If-Modified-Since`)
when the client's cached representation is still valid. It carries no normal
representation and is not a generic "nothing changed" business response.

## Client Request Errors

### 400 Bad Request

The HTTP request itself is invalid: malformed JSON, invalid request shape,
model-binding failure, invalid formatting, missing required transport-level
input, or a request that cannot be interpreted according to the API contract.
With `[ApiController]`, many binding and validation failures are handled
automatically. Not for authentication failure.

### 401 Unauthorized

Despite the name, authentication is missing or failed: no required credentials,
an invalid or expired token, or an authentication challenge is required.
Authentication middleware normally produces this response.

### 403 Forbidden

Authentication succeeded but the principal may not perform the operation —
missing permission, insufficient role, a resource operation prohibited by
policy. Resending the same credentials generally cannot fix it.

### 404 Not Found

The addressed resource does not exist, or the API deliberately hides its
existence. For collection queries such as `GET /api/orders?customerId=...`, zero
matches produce `200` with `[]`.

### 406 Not Acceptable

The server cannot produce a representation acceptable under the client's
content negotiation. This concerns the response representation — do not confuse
it with `415`.

### 409 Conflict

Typical cases: a duplicate where uniqueness is part of the resource state; a
state transition incompatible with the current state; a conflicting concurrent
operation; an idempotency key reused with a different payload.

```text
Order already completed
    + request asks to cancel it
    -> 409 Conflict
```

Not for malformed request syntax.

### 412 Precondition Failed

The client supplied a conditional precondition that is false — for example
`If-Match: "version-7"` while the current version is `"version-8"`. That is
normally `412`, not a generic `409`, because an explicit HTTP precondition
failed.

### 415 Unsupported Media Type

The server does not support the request representation, for example
`Content-Type: application/xml` on a JSON-only endpoint. `415` concerns the
request body format; `406` concerns acceptable response formats.

### 422 Unprocessable Content

The request is syntactically and structurally valid, but its semantic or
business content cannot be processed — impossible business values, a business
rule rejection that is not a state conflict, a semantically invalid combination
of valid fields (for example `startDate > endDate`).

Some APIs deliberately use `400` for both transport and semantic validation;
follow an established project convention. For new APIs that distinguish them:

```text
400 -> invalid HTTP/request contract
422 -> structurally valid request, invalid semantics/business input
```

### 428 Precondition Required

The API contract requires a precondition the client did not provide, for example
a `PUT /api/orders/123` that requires `If-Match`:

```text
missing required If-Match -> 428
provided but stale If-Match -> 412
```

Use `428` for other mandatory preconditions only when the contract explicitly
defines them.

### 429 Too Many Requests

Rate limiting rejected the request. Include `Retry-After` when the server knows
when another attempt is appropriate. Do not represent validation failure as rate
limiting.

## Server and Dependency Failures

### 500 Internal Server Error

Unexpected failure inside the application when no more specific controlled
outcome applies, produced through centralized exception handling and
`ProblemDetails` without internal details.

### 502 Bad Gateway

This API acts as an intermediary and received an invalid or unusable response
from an upstream service. Do not convert every dependency failure into `502`
mechanically.

### 503 Service Unavailable

The service is temporarily unable to handle the request: intentional
maintenance, a critical dependency unavailable for this operation, or temporary
overload when the service chooses `503` semantics. Include `Retry-After` when a
meaningful retry time is known.

### 504 Gateway Timeout

This API acts as an intermediary and an upstream service did not respond in
time. Do not return `504` for every internal `TaskCanceledException`;
distinguish a client-cancelled request, our own operation timing out, and an
upstream dependency timing out — the correct response depends on which occurred
and on the role this API plays.

## Idempotency

Method semantics matter for retries and duplicate handling: `GET` is safe and
idempotent; `PUT` is idempotent; `DELETE` is idempotent in intended state
semantics; `POST` is generally not idempotent.

For operations where a repeated `POST` must not create duplicate effects,
consider an idempotency key:

```http
Idempotency-Key: ...
```

The server associates the key with the request and result according to the API
contract; reuse of the same key with a materially different payload is a
reasonable `409`. Do not claim idempotency merely because duplicate requests
are unlikely.

## Optimistic Concurrency

When HTTP-level optimistic concurrency is part of the contract, prefer standard
conditional request semantics over custom status codes:

```text
GET           -> ETag: "v7"
PUT/PATCH     -> If-Match: "v7"
current is v7 -> update succeeds
current is v8 -> 412 Precondition Failed
If-Match required but absent -> 428 Precondition Required
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

## Decision Guide

Rows for 200/201/202/204, empty collections, 401/403, and 409/412 summarize
`.claude/rules/api.md` § HTTP Semantics, which owns them.

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
