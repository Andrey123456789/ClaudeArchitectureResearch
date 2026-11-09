---
name: http-api
description: >
  Use for Controller response design: status codes, Created/Accepted/NoContent, 400 vs 422, preconditions and ETags, idempotency keys, 429, 5xx.
---

> Level: 2 Technology | Owns: HTTP response technique for Controllers | Scope: backend | Loads: knowledge skill (on demand) | Depends on: 1-architecture/entry-points.md, 2-technology/aspnet-core.md

# HTTP API Technique

Policy owners (routing): entry-point responsibilities and core status semantics
(`200`/`201`/`202`/`204`, empty collections, `401`/`403`, `409`/`412`) →
`1-architecture/entry-points.md`; error contracts → `2-technology/aspnet-core.md`.
This skill supplies the mechanics and the less common codes. Keep status-code
behavior consistent across similar endpoints.

## Success Responses

```csharp
return Ok(response);                                              // 200 with representation
return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);  // 201 + Location
return AcceptedAtAction(nameof(GetOperation), new { id = operationId }, response); // 202 + status resource
return NoContent();                                               // 204, never with a body
```

- `200`: successful `GET`, `PUT`/`PATCH` returning the updated representation,
  a `POST` operation that creates no resource. For empty collections (rule in
  `entry-points.md`), `200 []` is also clearer for clients than `204`.
- `201`: include `Location` when a stable resource URI exists; `PUT` may return
  `201` when it creates the resource at a previously non-existing URI.
- `202`: for long-running, queued, or background processing, return an
  operation id or a `Location` where progress can be observed.
- `204`: typical for `DELETE` or an update whose representation adds no value.
  For repeated `DELETE` of an absent resource, choose `204` or `404` once and
  apply it consistently across equivalent resources.

## Conditional Requests and Concurrency

- `304 Not Modified` only answers a conditional request (`If-None-Match`/ETag,
  `If-Modified-Since`) whose cached representation is still valid — never a
  generic "nothing changed".
- Optimistic concurrency flow: `GET` → `ETag: "v7"`; `PUT` with `If-Match: "v7"`
  succeeds while current; current is `v8` → `412`; `If-Match` required but
  missing → `428 Precondition Required`. Do not replace these with custom codes.

## Client Errors

| Code | Use |
|---|---|
| `400` | Malformed JSON, invalid shape, binding failure, missing transport input (`[ApiController]` handles much of it) — not for authentication |
| `404` | Addressed resource absent or deliberately hidden |
| `406` | Cannot produce a representation acceptable to the client (response format) |
| `409` | Duplicate where uniqueness is resource state, incompatible transition, concurrent conflict, idempotency key reused with a different payload |
| `415` | Request body media type not supported (request format) |
| `422` | Structurally valid request with invalid semantics (e.g. `startDate > endDate`); follow an existing project convention if it uses `400` for both |
| `429` | Rate limiting rejected the request; add `Retry-After` when known; never for validation |

## Server and Dependency Failures

- `500`: unexpected internal failure via centralized handling and
  `ProblemDetails`, without internals.
- `502`: this API is an intermediary and the upstream response was invalid or
  unusable; not every dependency failure is `502`.
- `503`: temporarily unable to serve (maintenance, required dependency down,
  overload); add `Retry-After` when meaningful.
- `504`: this API is an intermediary and the upstream did not respond in time.
  Distinguish client cancellation, our own timeout, and an upstream timeout
  before choosing.

## Idempotency

`GET` is safe and idempotent; `PUT` and `DELETE` are idempotent in intended
state; `POST` generally is not. When a repeated `POST` must not duplicate
effects, accept an `Idempotency-Key`, associate it with the request and result,
and return `409` when the key is reused with a materially different payload. Do
not claim idempotency merely because duplicates are unlikely.

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

Machine-readable clients rely on stable error codes or contract fields, not
human-readable messages.
