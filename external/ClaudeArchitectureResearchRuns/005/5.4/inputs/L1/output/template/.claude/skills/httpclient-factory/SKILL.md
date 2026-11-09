---
name: httpclient-factory
description: Outbound HTTP technique with IHttpClientFactory. Use when implementing or reviewing calls to external HTTP APIs — typed, named, or keyed clients, adapters, DelegatingHandlers, timeouts, cancellation, response mapping, 429/Retry-After, retries — and resilience pipelines (circuit breaker, hedging, fallback) via its reference.
---

> Level: 2-technology · Owns: outbound HTTP technique; resilience depth in `references/resilience.md` · Loading: on demand

# HttpClient Factory

Rules: outbound-dependency rules (`.claude/rules/0-core/backend-code.md` § Outbound dependencies), the role rule that remote HTTP stays behind implementation-layer adapters, resilience package choices (`add-dependency`). Resilience technique: `references/resilience.md`.

## Adapter boundary

```csharp
public interface IPaymentGateway            // use-case layer abstraction
{
    Task<PaymentResult> ChargeAsync(PaymentRequest request, CancellationToken cancellationToken);
}

internal sealed class PaymentGateway(HttpClient httpClient) : IPaymentGateway   // implementation layer
{
    // ...
}
```

The use case does not need to know the remote service speaks HTTP.

## Choosing a client model

Named, typed, and keyed clients are all valid; choose the simplest one for the consumer and lifetime.

```csharp
services.AddHttpClient<PaymentGateway>(client => client.BaseAddress = new Uri(configuration["Payments:BaseUrl"]!));  // typed: one class owns one remote API
services.AddHttpClient("catalog", client => client.BaseAddress = new Uri(configuration["Catalog:BaseUrl"]!));      // named: factories, singletons creating clients per operation
```

Keyed clients fit when keyed DI makes consumption clearer — not automatically. Do not capture a transient typed client inside a singleton without understanding the lifetime consequences.

## Delegating handlers

Use a `DelegatingHandler` for genuine pipeline concerns — token acquisition, correlation propagation, request signing — never for business decisions:

```csharp
internal sealed class AccessTokenHandler(IAccessTokenProvider tokens) : DelegatingHandler
{
    protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
    {
        var token = await tokens.GetAsync(cancellationToken);
        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
        return await base.SendAsync(request, cancellationToken);
    }
}
```

## Cancellation and timeouts

Pass the caller's token (`await httpClient.SendAsync(request, cancellationToken)`); use `CancellationToken.None` only when the operation intentionally outlives the request. Choose timeouts from the remote operation and the latency budget; with resilience pipelines, distinguish per-attempt from total-operation timeouts.

## Response mapping

Translate remote responses into the abstraction's outcomes; do not call `EnsureSuccessStatusCode()` blindly when specific statuses carry meaning:

```csharp
if (response.StatusCode == HttpStatusCode.NotFound)
{
    return null;
}

response.EnsureSuccessStatusCode();
```

Do not forward every upstream status code to your own API; outbound retry behavior and the inbound response your API returns are separate decisions.

## Retries

Before enabling retry decide whether the failure is transient, whether repeating is safe, whether the remote API supports idempotency, and whether retry may duplicate side effects. `PUT`/`DELETE` are not operationally safe merely because HTTP defines them idempotent; POST/PATCH need idempotency keys, naturally idempotent semantics, or explicit deduplication.

## Headers and serialization

Configure stable headers (media types) on the client; apply per-request values such as dynamic tokens per request or through a handler — never mutate shared `DefaultRequestHeaders` concurrently. Prefer `System.Net.Http.Json` / `System.Text.Json`, with explicit options when the remote contract differs; do not reuse domain entities as remote contracts.

## Testing

A controlled `HttpMessageHandler` verifies method/path, headers, payload, response mapping, and cancellation/failure behavior. `new HttpClient(testHandler) { BaseAddress = new Uri("https://example.test/") }` is fine in a focused test — the lifetime rule concerns production code.

## Anti-patterns

Per-request `HttpClient`; mandating one client model everywhere; retries on unsafe operations without idempotency analysis; unbounded retries; leaking `HttpResponseMessage`; ignored cancellation; dynamic tokens in shared default headers; mapping every upstream failure to one status; resilience pipelines added without understanding their behavior.
