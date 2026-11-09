---
name: http-api
description: >
  Use when choosing HTTP status codes or response shapes in Controllers:
  2xx/4xx/5xx semantics, Location, ETags and preconditions, idempotency keys,
  rate limiting, Retry-After.
---

> Knowledge skill. Owns: HTTP status-code reference, response examples, idempotency and conditional-request technique · Scope: backend · Loads: on demand · Depends on: CLAUDE.md, .claude/rules/api.md, .claude/rules/error-handling.md

# HTTP API Semantics

Rules: `api.md` (HTTP semantics owned by the API layer, success statuses, empty
collections, 401/403, 409/412) and `error-handling.md` (ProblemDetails, safe
error exposure). This skill is the detailed reference.

## Successful Responses

### 200 OK

The operation completed and a representation is returned: successful `GET`;
`PUT`/`PATCH` returning the updated representation; a `POST` that performs an
operation without creating a resource; a query returning data.

```csharp
return Ok(response);
```

An empty collection is a successful collection result:

```http
200 OK

[]
```

`204` for an empty collection is also unusual: `200` with `[]` preserves the
resource representation and is clearer for clients.

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
non-existing target URI. The question is whether the HTTP operation created a
resource, not whether a row was inserted.

### 202 Accepted

Processing was accepted but is not complete when the response is sent — a
long-running operation, background job, asynchronous import, or queued
processing. When practical, return an operation identifier or a `Location`
where the client can observe progress:

```csharp
return AcceptedAtAction(
    nameof(GetOperation),
    new { id = operationId },
    response);
```

### 204 No Content

The operation completed and no body is needed — a successful `DELETE`, or an
update where returning the representation adds no value. A `204` response has no
body.

```csharp
return NoContent();
```

Choose consistently whether repeating `DELETE` on an already absent resource
returns `204` (the desired final state holds) or `404` (the addressed resource
does not exist); both conventions are valid, but do not mix them arbitrarily
between equivalent resources.

## Conditional and Cache Responses

### 304 Not Modified

Only for a conditional request (`If-None-Match` / ETag, `If-Modified-Since`)
when the client's cached representation is still valid. It carries no
representation and is not a generic "nothing changed" business response.

## Client Request Errors

### 400 Bad Request

The HTTP request itself is invalid: malformed JSON, invalid request shape,
model-binding failure, invalid formatting, missing required transport-level
input, or a request that cannot be interpreted according to the contract. With
`[ApiController]`, many binding and validation failures are handled
automatically. Not for authentication failures.

### 401 Unauthorized

Authentication is missing or failed: no credentials, invalid token, expired
token, challenge required. Authentication middleware produces it in most
cases.

### 403 Forbidden

Authentication succeeded but the principal may not perform the operation:
missing permission, insufficient role, resource operation prohibited by policy.
Resending the same credentials does not help. An API that deliberately hides
protected resources may return `404` instead, as a consistent security policy.

### 404 Not Found

The addressed resource does not exist, or the API deliberately hides its
existence. A collection query such as `GET /api/orders?customerId=...` with zero
matches returns `200 []`.

### 406 Not Acceptable

The server cannot produce a representation acceptable under the client's
content negotiation (response format). Not the same as `415`.

### 409 Conflict

A valid request conflicts with the current state: duplicate resource where
uniqueness is part of resource state; a state transition incompatible with the
current state; a conflicting concurrent operation; an idempotency key reused
with a different payload.

```text
Order already completed
    + request asks to cancel it
    -> 409 Conflict
```

Not for malformed request syntax.

### 412 Precondition Failed

A client-supplied conditional precondition is false — for example
`If-Match: "version-7"` while the current version is `"version-8"`. That is
`412`, not a generic `409`, because an explicit HTTP precondition failed.

### 415 Unsupported Media Type

The server does not support the request body format, for example
`Content-Type: application/xml` on a JSON-only endpoint. `415` concerns the
request body; `406` concerns acceptable response formats.

### 422 Unprocessable Content

The request is syntactically and structurally valid but its semantic or
business content cannot be processed — impossible business values, a business
rule rejection that is not a state conflict, a semantically invalid combination
of valid fields (for example `startDate > endDate`). Some APIs deliberately use
`400` for both transport and semantic validation; follow an established
project convention. For new APIs that distinguish them:

```text
400 -> invalid HTTP/request contract
422 -> structurally valid request, invalid semantics/business input
```

### 428 Precondition Required

The contract requires a precondition the client did not send, for example a
`PUT /api/orders/123` that requires `If-Match`:

```text
missing required If-Match -> 428
provided but stale If-Match -> 412
```

Use `428` for other preconditions only when the contract defines them as
mandatory.

### 429 Too Many Requests

Rate limiting rejected the request. Include `Retry-After` when the server knows
when another attempt is appropriate. Application validation failures are not
rate limiting.

## Server and Dependency Failures

### 500 Internal Server Error

An unexpected failure inside the application when no more specific controlled
outcome exists; produced through centralized exception handling and
`ProblemDetails`, without internal details.

### 502 Bad Gateway

This API acts as an intermediary and receives an invalid or unusable upstream
response. Do not convert every dependency failure into `502` mechanically.

### 503 Service Unavailable

The service is temporarily unable to handle the request — intentional
maintenance, a critical dependency unavailable for this operation, or temporary
overload when the service chooses `503` semantics. Include `Retry-After` when a
meaningful retry time is known.

### 504 Gateway Timeout

This API acts as an intermediary and an upstream service did not respond in
time. Do not return `504` for every internal `TaskCanceledException`;
distinguish a client-cancelled request, our own operation timing out, and an
upstream timeout — the correct response depends on which occurred and on this
API's role.

## Idempotency

Method semantics matter for retries and duplicate handling: `GET` is safe and
idempotent; `PUT` is idempotent; `DELETE` is idempotent in intended state
semantics; `POST` is generally not idempotent. When a repeated `POST` must not
create duplicate effects, consider an idempotency key:

```http
Idempotency-Key: ...
```

The server associates the key with the request and result according to the
contract; reuse with a materially different payload is reasonably answered with
`409`. Duplicates being unlikely does not make an operation idempotent.

## Optimistic Concurrency

When HTTP-level optimistic concurrency is part of the contract, use standard
conditional requests:

```text
GET           -> ETag: "v7"
PUT/PATCH     -> If-Match: "v7"
still v7      -> update succeeds
changed to v8 -> 412 Precondition Failed
If-Match required but absent -> 428 Precondition Required
```

Do not replace these semantics with arbitrary custom status codes.

## Controller Responsibility

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

Machine-readable clients rely on stable error codes or contract fields, not
human-readable exception messages. Keep status-code behavior consistent across
similar endpoints.

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
