---
name: http-api
description: >
  Use when choosing or reviewing HTTP status codes and response semantics in
  controllers: Created/Accepted/NoContent, 4xx/5xx mapping, ETags and
  preconditions, idempotency keys, Retry-After.
---

> Level: 2 Technology · Owns: detailed HTTP response technique · Scope: backend · Loads: on demand (knowledge skill)

# HTTP API Semantics

Policy owners: `.claude/rules/1-architecture/entry-points.md` (responsibilities, success/401/403/409/412 semantics, empty collections), `.claude/rules/2-technology/aspnet-core.md` (problem-details contracts), `.claude/rules/1-architecture/outcomes.md` (outcome mapping). Keep status behavior consistent across similar endpoints.

## Success responses

| Status | Typical use | ASP.NET Core |
|---|---|---|
| `200 OK` | successful `GET`; `PUT`/`PATCH` returning the updated representation; a `POST` operation that creates no resource; a query returning data (including `[]`) | `Ok(response)` |
| `201 Created` | the request created a new API resource; `PUT` creating a resource at a previously absent URI | `CreatedAtAction(nameof(GetById), new { id = created.Id }, created)` |
| `202 Accepted` | long-running, background, queued or asynchronous-import work not complete at response time; return an operation id or a status `Location` | `AcceptedAtAction(nameof(GetOperation), new { id = operationId }, response)` |
| `204 No Content` | successful `DELETE`; an update where returning the representation adds nothing | `NoContent()` |

Repeated `DELETE` of an already-absent resource may return `204` (desired state holds) or `404` (addressed resource does not exist). Both are valid; pick one convention and apply it to equivalent resources.

## Conditional and cache responses

`304 Not Modified` answers a conditional request (`If-None-Match`/ETag, `If-Modified-Since`) when the client's cached representation is still valid; it carries no representation and is never a generic "nothing changed" business response.

## Client errors

| Status | Meaning | Not for |
|---|---|---|
| `400 Bad Request` | malformed JSON, invalid shape, model-binding failure, invalid formatting, missing transport-level input (`[ApiController]` produces many automatically) | authentication failure |
| `401 Unauthorized` | credentials missing, invalid or expired; challenge required (produced by authentication middleware) | authenticated-but-forbidden |
| `403 Forbidden` | authenticated principal lacks the permission, role or policy; resending the same credentials will not help | unauthenticated callers |
| `404 Not Found` | the addressed resource does not exist, or the API deliberately hides it | empty collection results |
| `406 Not Acceptable` | cannot produce a representation acceptable to the client's `Accept` | unsupported request body type |
| `409 Conflict` | valid request conflicting with current state: duplicate under a uniqueness rule, incompatible state transition, conflicting concurrent operation, idempotency key reused with a different payload | malformed syntax |
| `412 Precondition Failed` | a supplied precondition (`If-Match: "v7"` while current is `"v8"`) is false | a generic conflict |
| `415 Unsupported Media Type` | request `Content-Type` not supported | response negotiation |
| `422 Unprocessable Content` | syntactically valid request with invalid semantics (`startDate > endDate`, business rejection that is not a state conflict) | transport errors |
| `428 Precondition Required` | the contract requires a precondition (e.g. `If-Match`) and none was sent | a stale precondition (`412`) |
| `429 Too Many Requests` | rate limiter rejected the request; add `Retry-After` when known | validation failures |

Some APIs deliberately use `400` for both transport and semantic validation — follow an established convention. New APIs that distinguish them use `400` for an invalid HTTP/request contract and `422` for a structurally valid request with invalid semantics.

## Server and dependency failures

| Status | Use |
|---|---|
| `500 Internal Server Error` | unexpected failure without a more specific controlled outcome; produced by central exception handling with a safe `ProblemDetails` body |
| `502 Bad Gateway` | this API acts as an intermediary and receives an invalid or unusable upstream response — not a blanket mapping for every dependency failure |
| `503 Service Unavailable` | temporarily unable to handle the request (maintenance, a critical dependency unavailable for this operation, deliberate overload shedding); add `Retry-After` when meaningful |
| `504 Gateway Timeout` | this API acts as an intermediary and an upstream did not answer in time |

Distinguish a client-cancelled request, our own timeout and an upstream timeout before choosing a response; not every `TaskCanceledException` is a `504`.

## Idempotency

`GET` is safe and idempotent, `PUT` is idempotent, `DELETE` is idempotent in intended state, `POST` generally is not. When a repeated `POST` must not duplicate effects, support an `Idempotency-Key` header and associate the key with the request and result per the API contract; a reused key with a materially different payload → `409`. Never claim idempotency because duplicates are merely unlikely.

## Optimistic concurrency over HTTP

```text
GET            -> ETag: "v7"
PUT/PATCH      -> If-Match: "v7"
current is v7  -> update succeeds
current is v8  -> 412 Precondition Failed
If-Match required but absent -> 428 Precondition Required
```

Use standard conditional-request semantics instead of custom status codes.

## Controller mapping example

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

Give machine-readable clients stable error codes or contract fields in the problem-details body (`aspnet-core.md`).

## Decision guide

| Situation | Response |
|---|---|
| Successful query with representation | `200` |
| Empty collection | `200` + `[]` |
| Resource created | `201` + `Location` when available |
| Accepted, incomplete processing | `202` |
| Success without a body | `204` |
| Conditional cache hit | `304` |
| Malformed / contract-invalid request | `400` |
| Missing or invalid authentication | `401` |
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
| Bad upstream response as intermediary | `502` |
| Temporarily unavailable | `503` |
| Upstream timeout as intermediary | `504` |
