---
name: http-api
description: Use when choosing or reviewing Controller response semantics — status codes, Created/Accepted/NoContent, conflicts, 401/403, ETags and preconditions, idempotency, rate limiting, upstream failures.
---

> Kind: KNW | Scope: backend | Owner: HTTP status-code and API semantics reference with examples | Loading: on demand (model-invoked knowledge)

# HTTP API Semantics

Rules: `rules/backend/api.md` (status semantics, error contract, versioning), `rules/backend/error-handling.md` (failure handling). Error handling technique: `aspnet-error-handling`.

## Successful responses

**200 OK** — completed with a response representation: successful `GET`, `PUT`/`PATCH` returning the updated representation, a `POST` that performs an operation without creating a resource, a query returning data.

```csharp
return Ok(response);
```

Empty collections: `rules/backend/api.md` § HTTP semantics; `204` for an empty collection loses the representation and is less clear to clients.

**201 Created** — the request created a new API resource. Include `Location` when a stable resource URI exists. `PUT` may also return `201` when it creates a resource at a previously non-existing URI. An internal row insert alone is not "creation" in HTTP terms (`rules/backend/api.md` § HTTP semantics).

```csharp
return CreatedAtAction(
    nameof(GetById),
    new { id = created.Id },
    created);
```

**202 Accepted** — accepted but not complete when the response is sent: long-running operations, background jobs, asynchronous imports, queued processing. Return an operation identifier or a `Location` where progress can be observed.

```csharp
return AcceptedAtAction(
    nameof(GetOperation),
    new { id = operationId },
    response);
```

**204 No Content** — completed and no body is needed: successful `DELETE`, or an update whose representation adds no value. A `204` carries no body.

```csharp
return NoContent();
```

Repeated `DELETE` of an absent resource may return `204` (the desired final state holds) or `404` (the addressed resource does not exist); pick one convention and apply it consistently across equivalent resources.

## Conditional and cache responses

**304 Not Modified** — only for a conditional request (`If-None-Match`/ETag, `If-Modified-Since`) when the client's cached representation is still valid; it carries no representation. It is not a generic "nothing changed" business response.

## Client errors

**400 Bad Request** — the HTTP request itself is invalid: malformed JSON, invalid shape, model-binding failure, invalid formatting, missing transport-level input. `[ApiController]` produces many of these automatically. Authentication failures are not `400`.

**401 Unauthorized** — authentication is missing or failed: no credentials, invalid or expired token, challenge required. Authentication middleware produces it.

**403 Forbidden** — authenticated, but the principal may not perform the operation (missing permission, insufficient role, prohibited by policy). Resending the same credentials does not help. An API that deliberately hides protected resources may answer `404` instead, as a consistent policy.

**404 Not Found** — the addressed resource does not exist, or the API deliberately hides it. A collection query with zero matches (`GET /api/orders?customerId=...`) follows the empty-collection rule in `rules/backend/api.md` § HTTP semantics.

**406 Not Acceptable** — the server cannot produce a representation the client accepts (response content negotiation). **415 Unsupported Media Type** — the server does not support the request body format (for example `Content-Type: application/xml` on a JSON-only endpoint).

**409 Conflict** — a valid request conflicting with current resource or system state: duplicate resource where uniqueness is part of the state, incompatible state transition, conflicting concurrent operation, an idempotency key reused with a different payload. Example: cancelling an already completed order. Malformed syntax is not `409`.

**412 Precondition Failed** — the client supplied a conditional precondition that is false, for example `If-Match: "version-7"` while the resource is at `"version-8"`. That is `412`, not a generic `409`.

**422 Unprocessable Content** — syntactically and structurally valid, but semantically or business-invalid content: impossible values, a business-rule rejection that is not a state conflict, incompatible fields such as `startDate > endDate`. Some APIs use `400` for both transport and semantic validation; follow an established convention. New APIs that distinguish them use `400` for an invalid HTTP/request contract and `422` for a valid structure with invalid semantics.

**428 Precondition Required** — the contract requires a precondition the client did not send: missing required `If-Match` → `428`; provided but stale `If-Match` → `412`. Use `428` for other mandatory preconditions only when the API contract defines them.

**429 Too Many Requests** — rate limiting rejected the request; include `Retry-After` when the next acceptable attempt is known. Validation failures are not rate limiting.

## Server and dependency failures

**500 Internal Server Error** — unexpected failure inside the application when no more specific controlled outcome exists; produced through centralized exception handling and `ProblemDetails` without internal details.

**502 Bad Gateway** — this API acts as an intermediary and received an invalid or unusable upstream response. Not every dependency failure is `502`.

**503 Service Unavailable** — temporarily unable to handle the request: maintenance, a critical dependency unavailable for this operation, temporary overload. Include `Retry-After` when meaningful.

**504 Gateway Timeout** — acting as an intermediary, an upstream service did not respond in time. Not every internal `TaskCanceledException` is `504`: distinguish a client-cancelled request, our own operation timing out, and an upstream dependency timing out — the right response depends on which occurred and the role this API plays.

## Idempotency

`GET` is safe and idempotent; `PUT` is idempotent; `DELETE` is idempotent in intended state; `POST` generally is not. When a repeated `POST` should not create duplicate effects, consider an `Idempotency-Key` that the server associates with the request and result; reuse of a key with a materially different payload is reasonably `409`. Duplicate requests being unlikely does not make an operation idempotent.

## Optimistic concurrency

When HTTP-level optimistic concurrency is part of the contract, use standard conditional requests:

```text
GET                       -> ETag: "v7"
PUT/PATCH If-Match: "v7"  -> succeeds while current is v7
current changed to v8     -> 412 Precondition Failed
If-Match required, absent -> 428 Precondition Required
```

Do not replace well-defined precondition semantics with custom status codes.

## Controller mapping

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

Machine-readable clients rely on stable error codes or contract fields in `ProblemDetails`, not on human-readable exception messages.

## Decision guide

| Situation | Response |
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
| Cannot produce acceptable representation | `406` |
| Current-state conflict | `409` |
| Supplied precondition failed | `412` |
| Unsupported request content type | `415` |
| Valid structure, invalid semantics | `422` |
| Required precondition absent | `428` |
| Rate limited | `429` + `Retry-After` when known |
| Unexpected internal failure | `500` |
| Invalid upstream response as intermediary | `502` |
| Temporarily unavailable | `503` |
| Upstream timeout as intermediary | `504` |
