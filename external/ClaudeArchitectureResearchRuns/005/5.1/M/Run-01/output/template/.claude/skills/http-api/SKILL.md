---
name: http-api
description: >
  Use when designing or reviewing Controller endpoints and responses: choosing
  status codes, Created/Accepted/NoContent results, Location and Retry-After
  headers, 400 vs 422, 406/415, conditional requests and ETags, 428,
  idempotency keys, rate limiting, or upstream 502/503/504 mapping.
---

> Owns: HTTP status-code reference, conditional-request and idempotency technique, Controller response examples | Scope: backend | Loads: on demand (knowledge skill)

# HTTP API Semantics

Core rules (status ownership, success codes, empty collections, 401/403,
409/412, ProblemDetails, no leaked internals) are owned by
`.claude/rules/api.md`. This skill is the detailed reference. Keep status-code
behavior consistent across similar endpoints.

## Success Responses

```csharp
return Ok(response);                                          // 200 with representation
return CreatedAtAction(nameof(GetById), new { id = created.Id }, created); // 201 + Location
return AcceptedAtAction(nameof(GetOperation), new { id = operationId }, response); // 202
return NoContent();                                           // 204, no body
```

Which success code applies is governed by `api.md`. Typical cases:

- `200`: successful `GET`, `PUT`/`PATCH` returning the updated representation,
  or a `POST` that performs an operation without creating a resource. For an
  empty collection return `Ok(Array.Empty<T>())`, not `NoContent()`.
- `201`: include `Location` when a stable URI exists; `PUT` may return `201`
  when it creates the target resource.
- `202`: long-running, background, import, or queued work; return an operation
  identifier or a status `Location` when practical.
- `204`: successful `DELETE`, or an update where returning the representation
  adds no value; a `204` never has a body. Choose consistently whether repeated
  `DELETE` of an absent resource returns `204` (final state holds) or `404`.

## Conditional and Cache Responses

`304 Not Modified` is only for conditional requests (`If-None-Match`/ETag,
`If-Modified-Since`) whose cached representation is still valid — never a generic
"nothing changed" business response.

## Client Errors

| Code | Use |
|---|---|
| `400` | Malformed JSON, invalid shape, binding failure, missing transport-level input; not for authentication failure. `[ApiController]` produces many automatically. |
| `401` / `403` | Semantics in `api.md`. Both are normally produced by authentication/authorization middleware rather than manufactured in Controllers; a client cannot fix `403` by resending the same credentials. |
| `404` | Addressed resource absent (deliberate hiding: `api.md`). |
| `406` | Cannot produce a representation acceptable to the client's `Accept` header. |
| `409` | Semantics in `api.md`. Examples: duplicate where uniqueness is resource state, incompatible transition, conflicting concurrent operation, idempotency key reused with a different payload. Not for malformed syntax. |
| `412` | Semantics in `api.md`. Example: `If-Match: "v7"` while the current version is `"v8"`. |
| `415` | Unsupported request `Content-Type` (request body format; contrast `406`). |
| `422` | Structurally valid request with semantically invalid content (for example `startDate > endDate`) when the API distinguishes it from `400`. Follow an established project convention if it uses `400` for both. |
| `428` | The contract requires a precondition (such as `If-Match`) and it is absent. |
| `429` | Rate limiting rejected the request; include `Retry-After` when known. Not for validation failures. |

## Server and Dependency Failures

| Code | Use |
|---|---|
| `500` | Unexpected internal failure without a more specific controlled outcome; centralized handling with safe `ProblemDetails`. |
| `502` | This API acts as an intermediary and received an invalid/unusable upstream response. Do not map every dependency failure to `502`. |
| `503` | Temporarily unable to serve (maintenance, required dependency down, overload); `Retry-After` when meaningful. |
| `504` | Acting as an intermediary and the upstream did not respond in time. |

Distinguish a client-cancelled request, our own timeout, and an upstream timeout
before choosing a response; do not return `504` for every
`TaskCanceledException`.

## Idempotency

`GET` is safe and idempotent, `PUT` idempotent, `DELETE` idempotent in intended
state, `POST` generally not. When repeated `POST`s must not duplicate effects,
consider an `Idempotency-Key` header associated with the request/result per the
API contract; a reused key with a materially different payload is a reasonable
`409`. Do not claim idempotency merely because duplicates are unlikely.

## Optimistic Concurrency

```text
GET        -> ETag: "v7"
PUT/PATCH  -> If-Match: "v7"
current v7 -> success
current v8 -> 412 Precondition Failed
If-Match required but absent -> 428 Precondition Required
```

Prefer these standard conditional semantics over custom status codes.

## Controller Translation

```csharp
[HttpPost]
public async Task<ActionResult<OrderResponse>> Create(
    CreateOrderRequest request, CancellationToken cancellationToken)
{
    var result = await orders.CreateAsync(request, cancellationToken);
    return CreatedAtAction(nameof(GetById), new { id = result.Id }, result);
}
```

Application expresses outcomes; the Controller maps them to HTTP. Exception and
outcome technique: `aspnet-error-handling`.

## Decision Guide

Success codes, empty collections, `401`/`403`, and `409`/`412`: `api.md`.

| Situation | Default response |
|---|---|
| Conditional cache hit | `304` |
| Malformed / contract-invalid request | `400` |
| Resource absent | `404` |
| Unacceptable response representation | `406` |
| Unsupported request content type | `415` |
| Valid structure, invalid semantics | `422` |
| Required precondition absent | `428` |
| Rate limited | `429` + `Retry-After` when known |
| Unexpected internal failure | `500` |
| Bad upstream response (intermediary) | `502` |
| Temporarily unavailable | `503` |
| Upstream timeout (intermediary) | `504` |
