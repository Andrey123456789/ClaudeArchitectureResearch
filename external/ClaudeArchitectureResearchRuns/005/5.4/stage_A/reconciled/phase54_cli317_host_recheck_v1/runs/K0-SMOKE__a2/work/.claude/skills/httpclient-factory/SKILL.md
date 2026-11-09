---
name: httpclient-factory
description: Use when calling external HTTP APIs — IHttpClientFactory clients, adapters, timeouts, handlers, cancellation, response mapping, Retry-After, resilience pipelines (retry, circuit breaker, fallback, hedging).
---

> Kind: KNW | Scope: backend | Owner: outbound HTTP client technique; resilience depth in references/resilience.md | Loading: on demand (model-invoked knowledge)

# HttpClient Factory

Rules: `rules/backend/integrations.md` (client lifetime, transport boundary, time limits, retry, fallback, cancellation). Resilience packages: D-12. Resilience pipelines: `references/resilience.md`.

## Architectural boundary

Application may define an abstraction that Infrastructure implements with `HttpClient`; Application does not need to know the service uses HTTP.

```csharp
public interface IPaymentGateway
{
    Task<PaymentResult> ChargeAsync(
        PaymentRequest request,
        CancellationToken cancellationToken);
}

internal sealed class PaymentGateway(HttpClient httpClient)
    : IPaymentGateway
{
    ...
}
```

## Client models

Named, typed and keyed clients are all valid; choose the simplest model for the consumer and lifetime.

Typed clients — one class owns communication with one remote API:

```csharp
services.AddHttpClient<PaymentGateway>(client =>
{
    client.BaseAddress = new Uri(configuration["Payments:BaseUrl"]!);
});
```

Capturing a transient typed client inside a singleton has lifetime implications — understand them first.

Named clients — a factory creates clients dynamically, several clients share one usage model, or a singleton creates clients per operation:

```csharp
services.AddHttpClient("catalog", client =>
{
    client.BaseAddress = new Uri(configuration["Catalog:BaseUrl"]!);
});
```

Keyed clients — when keyed DI makes consumption clearer; not automatically because the framework supports them.

## Delegating handlers

For genuine HTTP pipeline concerns — authorization header acquisition, correlation/context propagation, request signing — not business decisions:

```csharp
internal sealed class AccessTokenHandler(
    IAccessTokenProvider tokens)
    : DelegatingHandler
{
    protected override async Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request,
        CancellationToken cancellationToken)
    {
        var token = await tokens.GetAsync(cancellationToken);

        request.Headers.Authorization =
            new AuthenticationHeaderValue("Bearer", token);

        return await base.SendAsync(request, cancellationToken);
    }
}
```

## Cancellation and timeouts

```csharp
await httpClient.SendAsync(
    request,
    cancellationToken);
```

Replace request cancellation with `CancellationToken.None` only when the operation intentionally outlives the incoming request. Choose timeouts from the remote operation and the application's latency budget; with resilience pipelines, distinguish per-attempt from total-operation timeout.

## Response mapping

Response translation boundary: `rules/backend/integrations.md`. `EnsureSuccessStatusCode()` is too blunt when specific remote statuses carry contract meaning:

```csharp
if (response.StatusCode == HttpStatusCode.NotFound)
{
    return null;
}

response.EnsureSuccessStatusCode();
```

For richer failure semantics, translate into explicit Infrastructure/Application outcomes rather than exposing every upstream status code through your own API.

## 429 and Retry-After

When a remote service returns `429 Too Many Requests`, honor `Retry-After` when the selected retry policy supports it. Outbound retry behavior and the inbound response your own API returns are separate decisions.

## Retry safety

Every external I/O call needs a bounded execution time (`rules/backend/integrations.md`); retry and circuit breakers are not mandatory for every call. Before enabling retry, establish whether the failure is transient, whether the operation is safe to repeat, whether the remote API supports idempotency, and whether a retry may duplicate side effects. Mechanisms that make state-changing calls retry-safe: API-defined idempotency keys, naturally idempotent semantics, explicit deduplication. A PUT or DELETE implementation is not operationally safe merely because the HTTP method is defined as idempotent.

## Headers and serialization

Stable headers (media types) can be configured on the client; per-request values such as dynamic access tokens go on the request or through a handler — mutating shared `DefaultRequestHeaders` concurrently for request-specific values is a race. Prefer `System.Net.Http.Json`/`System.Text.Json`, with explicit serializer options when the remote contract differs from the application's defaults. Internal Domain entities are not remote API contracts.

## Testing outbound adapters

A controlled `HttpMessageHandler` verifies request method/path, headers, serialized payload, response mapping and cancellation/failure behavior:

```csharp
var client = new HttpClient(testHandler)
{
    BaseAddress = new Uri("https://example.test/")
};
```

`new HttpClient(testHandler)` in a focused test is fine; the lifetime rule concerns production code.

## Common mistakes

New `HttpClient` per request; mandating one client model everywhere; retrying unsafe operations without idempotency analysis; unbounded retries; leaking `HttpResponseMessage` across boundaries; ignoring cancellation; dynamic tokens in shared default headers; mapping every upstream failure to the same status; resilience pipelines added without understanding them.
