---
name: httpclient-factory
description: Use when implementing or reviewing calls to external HTTP APIs — IHttpClientFactory typed, named or keyed clients, Infrastructure adapters, DelegatingHandlers, timeouts, cancellation, response mapping, headers, serialization, adapter tests; includes the resilience reference (retries, circuit breakers, fallback, hedging).
---
<!-- Kind: KNW | Scope: backend | Owns: outbound HTTP client technique; resilience reference | Loads: on demand (model-invoked) -->
# HttpClient Factory

Standards: `rules/backend/outbound-http.md` (client lifetime, timeouts, retry safety, Retry-After, fallback, caller cancellation) and `rules/backend/architecture.md` § Boundary Leaks. Resilience technique: `references/resilience.md`.

Named, typed and keyed clients are all valid — choose the simplest model for the consumer and lifetime. Outbound API clients normally live in Infrastructure.

## Architectural Boundary

Application may define an abstraction:

```csharp
public interface IPaymentGateway
{
    Task<PaymentResult> ChargeAsync(
        PaymentRequest request,
        CancellationToken cancellationToken);
}
```

Infrastructure implements it with `HttpClient`:

```csharp
internal sealed class PaymentGateway(HttpClient httpClient)
    : IPaymentGateway
{
    ...
}
```

Application does not need to know that the external service uses HTTP.

## Typed Clients

Useful when one class owns communication with one remote API:

```csharp
services.AddHttpClient<PaymentGateway>(client =>
{
    client.BaseAddress = new Uri(configuration["Payments:BaseUrl"]!);
});
```

Avoid capturing a transient typed client inside a singleton without understanding the lifetime implications.

## Named Clients

Useful when a factory creates clients dynamically, several clients share one usage model, or a singleton needs a client per operation:

```csharp
services.AddHttpClient("catalog", client =>
{
    client.BaseAddress = new Uri(configuration["Catalog:BaseUrl"]!);
});
```

## Keyed Clients

Useful when keyed DI makes consumption clearer — not automatically because the framework supports them. Prefer whichever model makes ownership and lifetime easiest to understand.

## Delegating Handlers

`DelegatingHandler` suits genuine HTTP pipeline concerns — authorization header acquisition, correlation/context propagation, request signing — not business decisions:

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

## Cancellation

Pass the caller's token to outbound calls:

```csharp
await httpClient.SendAsync(
    request,
    cancellationToken);
```

Use `CancellationToken.None` only when the operation intentionally outlives the incoming request.

## Timeouts

Choose timeouts from the remote operation and the application's latency budget. With resilience pipelines, distinguish per-attempt timeout from total-operation timeout (`references/resilience.md`).

## Response Mapping

Infrastructure translates remote responses into the abstraction Application consumes. Avoid blind `EnsureSuccessStatusCode()` when specific remote statuses carry contract meaning:

```csharp
if (response.StatusCode == HttpStatusCode.NotFound)
{
    return null;
}

response.EnsureSuccessStatusCode();
```

For richer failure semantics, translate responses into explicit Infrastructure/Application outcomes; avoid exposing every upstream status code through your own API.

## 429 and Retry-After

When a remote service returns `429 Too Many Requests`, honor `Retry-After` through a retry policy that supports it. The outbound client's retry behavior and the response your own API returns are separate decisions.

## Resilience

Configure retries, circuit breakers, hedging, fallback and pipelines with `references/resilience.md`. A timeout is normally required for external I/O; retry and circuit breaker are not mandatory for every call. Before enabling retry, establish whether the failure is transient, whether the operation is safe to repeat, whether the remote API supports idempotency, and whether a retry may duplicate side effects.

## Unsafe HTTP Methods

POST, PATCH and other state-changing operations become safe to retry only through API-defined idempotency keys, naturally idempotent semantics or explicit deduplication. A PUT or DELETE implementation is not operationally safe merely because the HTTP method is defined as idempotent.

## Headers

Stable headers such as media types may live on the client. Per-request values such as dynamic access tokens go on the specific request or through a handler; avoid mutating shared default headers concurrently for request-specific values.

## Serialization

Prefer `System.Net.Http.Json` / `System.Text.Json` where sufficient, with explicit serialization options when the external contract differs from the application's defaults. Avoid reusing internal Domain entities as remote API contracts merely to skip mapping.

## Testing

For an outbound adapter, a controlled `HttpMessageHandler` can verify request method and path, headers, serialized payload, response mapping, and cancellation/failure behavior:

```csharp
var client = new HttpClient(testHandler)
{
    BaseAddress = new Uri("https://example.test/")
};
```

`new HttpClient(testHandler)` in a focused test is fine; the lifetime standard concerns production per-request construction.

## Anti-Patterns

Avoid creating/disposing `HttpClient` per request, making typed/keyed/named clients mandatory universally, retrying unsafe operations without idempotency analysis, infinite or poorly bounded retries, leaking `HttpResponseMessage` across boundaries, ignoring cancellation, dynamic auth tokens in shared `DefaultRequestHeaders`, mapping every upstream failure to the same status in your own API, and resilience pipelines added without understanding their behavior.
