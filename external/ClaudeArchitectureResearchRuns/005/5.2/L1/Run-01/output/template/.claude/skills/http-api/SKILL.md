---
name: http-api
description: >
  Use when choosing HTTP status codes or response shapes: 2xx/4xx/5xx,
  ProblemDetails, Location, Retry-After, ETag and If-Match, idempotency keys,
  rate limits.
---
> Level: 2-technology | Owns: detailed HTTP status-code reference and Controller examples | Scope: backend | Loads: on demand (skill)

# HTTP API Semantics

Normative semantics for success codes, empty collections, 401/403, 409/412,
error contracts, and versioning need are owned by `http-api.md`; response
semantics belong to entry points (`role-boundaries.md`). This skill is the
detailed reference.

## Success responses — mechanics

```csharp
return Ok(response);                                   // 200 with representation

return CreatedAtAction(nameof(GetById),                // 201 + Location
    new { id = created.Id }, created);

return AcceptedAtAction(nameof(GetOperation),          // 202 + status resource
    new { id = operationId }, response);

return NoContent();                                    // 204, no body
```

- `200` typical cases: successful `GET`; `PUT`/`PATCH` returning the updated
  representation; a `POST` that performs an operation without creating a
  resource. An empty collection is `200` with `[]` (not `204`, which drops the
  representation clients expect).
- `201`: `PUT` may also return `201` when it creates the resource at a
  previously non-existing URI.
- `202`: long-running operations, background jobs, asynchronous imports, queued
  processing; return an operation identifier or a status `Location` when
  practical.
- `204`: successful `DELETE`, or an update where returning the representation
  adds nothing. Choose one convention for repeated `DELETE` of an absent
  resource (`204` because the desired state holds, or `404`) and apply it
  consistently to equivalent resources.

## Conditional and cache responses

`304 Not Modified` only for a conditional request (`If-None-Match`/ETag,
`If-Modified-Since`) whose cached representation is still valid; never as a
generic "nothing changed" business response.

## Client errors

| Code | Use for | Not for |
|---|---|---|
| `400` | malformed JSON, invalid request shape, model-binding failure, missing transport-level input (`[ApiController]` handles much of this) | authentication failure |
| `401` / `403` | see `http-api.md`; produced by authentication/authorization middleware rather than hand-made in controllers | — |
| `404` | the addressed resource does not exist, or a deliberate hiding policy | zero matches in a collection |
| `406` | the server cannot produce a representation acceptable to the client | unsupported request body (`415`) |
| `409` / `412` | see `http-api.md`; `409` cases: uniqueness that is part of resource state, state transition incompatible with current state, conflicting concurrent operation, idempotency key reused with a different payload | malformed syntax |
| `415` | unsupported request `Content-Type` | response negotiation (`406`) |
| `422` | structurally valid request whose semantic/business content is invalid (e.g. `startDate > endDate`) | — |
| `428` | a required precondition (e.g. `If-Match`) is absent | a supplied but stale precondition (`412`) |
| `429` | rate limiting rejected the request; include `Retry-After` when known | validation failures |

Some APIs use `400` for both transport and semantic validation; follow an
established project convention. New APIs that distinguish them use `400` for an
invalid request contract and `422` for valid structure with invalid semantics.

## Server and dependency failures

- `500` — unexpected internal failure without a more specific controlled
  outcome; produced by centralized exception handling with `ProblemDetails`.
- `502` — this API acts as an intermediary and received an invalid or unusable
  upstream response; do not convert every dependency failure into `502`.
- `503` — temporarily unable to handle the request (maintenance, a critical
  dependency unavailable, chosen overload behavior); include `Retry-After` when
  meaningful.
- `504` — this API acts as an intermediary and an upstream did not respond in
  time. Distinguish client cancellation, our own timeout, and an upstream
  timeout; not every `TaskCanceledException` is a `504`.

## Idempotency

`GET` is safe and idempotent; `PUT` is idempotent; `DELETE` is idempotent in
intended state; `POST` generally is not. When a repeated `POST` must not create
duplicate effects, consider an `Idempotency-Key` header associated with the
request and result by the API contract; reuse with a materially different
payload → `409`. Do not claim idempotency merely because duplicates are
unlikely.

## Optimistic concurrency over HTTP

```text
GET            → ETag: "v7"
PUT/PATCH      → If-Match: "v7"
still v7       → update succeeds
changed to v8  → 412 Precondition Failed
If-Match required but absent → 428 Precondition Required
```

Do not replace standard precondition semantics with custom status codes.

## Controller responsibility

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

The use-case unit expresses the outcome; the controller maps it to HTTP.

## Quick lookup

| Situation | Response |
|---|---|
| Conditional cache hit | `304` |
| Malformed or contract-invalid request | `400` |
| Cannot produce an acceptable representation | `406` |
| Unsupported request content type | `415` |
| Valid structure, invalid semantics | `422` |
| Required precondition absent | `428` |
| Rate limited | `429` + `Retry-After` when known |
| Unexpected internal failure | `500` |
| Bad upstream response as intermediary | `502` |
| Temporarily unavailable | `503` |
| Upstream timeout as intermediary | `504` |
| 2xx choice, empty collections, 401/403, 409/412 | `http-api.md` |
