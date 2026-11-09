---
name: http-api
description: >
  Use when choosing HTTP status codes or response shapes in Controllers:
  2xx/4xx/5xx semantics, Location, ETags and preconditions, idempotency keys,
  429 and Retry-After, ProblemDetails.
---

> Knowledge skill · HTTP status-code reference and technique · Policy: `.claude/rules/api.md` § HTTP Semantics, `.claude/rules/error-handling.md`

# HTTP API Semantics

Keep status-code behavior consistent across similar endpoints. The decision
guide at the end summarizes the defaults.

## Successful Responses

### 200 OK

The operation completed and a representation is returned: a successful `GET`,
a `PUT`/`PATCH` returning the updated representation, a `POST` that performs an
operation without creating a resource, a successful query.

```csharp
return Ok(response);
```

An empty collection is still a successful collection result:

```http
200 OK

[]
```

`200` with `[]` preserves the resource representation and is clearer for
clients than `204` for an empty collection.

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
new API resource, not whether a row was inserted.

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
update where returning the representation adds no value. A `204` response must
not contain a body.

```csharp
return NoContent();
```

Choose consistently whether a repeated `DELETE` of an absent resource returns
`204` (the desired final state holds) or `404` (the addressed resource does not
exist); do not mix conventions between equivalent resources.

## Conditional and Cache Responses

### 304 Not Modified

Only for a conditional request (`If-None-Match`/ETag, `If-Modified-Since`)
when the client's cached representation is still valid. It carries no normal
representation and is not a generic "nothing changed" business response.

## Client Request Errors

### 400 Bad Request

The HTTP request itself is invalid: malformed JSON, invalid request shape,
model-binding failure, invalid formatting, missing required transport-level
input, or a request that cannot be interpreted under the API contract. With
`[ApiController]`, many binding and validation failures are handled
automatically. Not for authentication failure.

### 401 Unauthorized

Authentication is missing or failed — no credentials, invalid or expired token,
challenge required. Authentication middleware produces it by default.

### 403 Forbidden

Authentication succeeded but the principal is not allowed — missing
permission, insufficient role, or an operation prohibited by policy. The client
generally cannot fix it by resending the same credentials. An API that hides
the existence of protected resources may return `404` instead, as a deliberate
and consistent security policy.

### 404 Not Found

The addressed resource does not exist, or the API deliberately hides its
existence. A collection query such as `GET /api/orders?customerId=...` with
zero matches returns `200 []`.

### 406 Not Acceptable

The server cannot produce a representation acceptable under the client's
content negotiation. It concerns the response representation; do not confuse
it with `415`.

### 409 Conflict

The request is valid but conflicts with the current state: a duplicate where
uniqueness is part of the resource state, an incompatible state transition, a
conflicting concurrent operation, or an idempotency key reused with a different
payload.

```text
Order already completed
    + request asks to cancel it
    → 409 Conflict
```

Not for malformed syntax.

### 412 Precondition Failed

A supplied conditional precondition is false — for example `If-Match:
"version-7"` while the current version is `"version-8"`. That is `412`, not a
generic `409`, because an explicit HTTP precondition failed.

### 415 Unsupported Media Type

The server does not support the request representation, for example
`Content-Type: application/xml` on a JSON-only endpoint. `415` concerns the
request body format; `406` concerns acceptable response formats.

### 422 Unprocessable Content

The request is syntactically and structurally valid but its semantic or
business content is invalid — impossible business values, a business-rule
rejection that is not a state conflict, or a semantically invalid combination
such as `startDate > endDate`. Some APIs deliberately use `400` for both
transport and semantic validation; follow an established project convention.
For new APIs that distinguish them:

```text
400 → invalid HTTP/request contract
422 → structurally valid request, invalid semantics/business input
```

### 428 Precondition Required

The API contract requires a precondition the client did not provide, for
example a `PUT /api/orders/123` that requires `If-Match`:

```text
missing required If-Match → 428
provided but stale If-Match → 412
```

Use `428` for other mandatory preconditions only when the contract explicitly
defines them.

### 429 Too Many Requests

Rate limiting rejected the request. Include `Retry-After` when the server knows
when another attempt is appropriate. Do not represent validation failure as
rate limiting.

## Server and Dependency Failures

### 500 Internal Server Error

An unexpected failure inside the application when no more specific controlled
outcome exists; handled centrally with `ProblemDetails` and no internal details
(`error-handling.md` § HTTP Error Contracts).

### 502 Bad Gateway

This API acts as an intermediary and receives an invalid or unusable upstream
response. Do not convert every dependency failure into `502`.

### 503 Service Unavailable

The service is temporarily unable to handle the request — maintenance, a
critical dependency unavailable for this operation, or overload when the service
chooses `503` semantics. Include `Retry-After` when a meaningful retry time is
known.

### 504 Gateway Timeout

This API acts as an intermediary and an upstream service did not respond in
time. Not for every internal `TaskCanceledException`: distinguish a client that
cancelled the incoming request, an operation of our own that timed out, and an
upstream timeout; the external response depends on which occurred and the role
this API plays.

## Idempotency

`GET` is safe and idempotent, `PUT` is idempotent, `DELETE` is idempotent in
intended state semantics, `POST` is generally not idempotent. When a repeated
`POST` must not create duplicate effects, consider an `Idempotency-Key` header
whose key the server associates with the request and result; reusing a key with
a materially different payload is reasonably a `409`. Do not claim idempotency
merely because duplicate requests are unlikely.

## Optimistic Concurrency

When HTTP-level optimistic concurrency is part of the contract, prefer standard
conditional semantics:

```text
GET            → ETag: "v7"
PUT/PATCH      → If-Match: "v7"
current is v7  → update succeeds
current is v8  → 412 Precondition Failed
If-Match absent but required → 428 Precondition Required
```

Do not replace well-defined precondition semantics with custom status codes.

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
`ProblemDetails`, not on human-readable exception messages.

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
