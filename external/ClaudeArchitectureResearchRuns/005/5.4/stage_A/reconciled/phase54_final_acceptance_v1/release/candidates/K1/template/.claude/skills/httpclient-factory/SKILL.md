---
name: httpclient-factory
description: >
  Use when calling external HTTP APIs: IHttpClientFactory typed/named/keyed
  clients, DelegatingHandler, timeouts, cancellation, response mapping,
  429/Retry-After, retries, circuit breakers, fallback, resilience pipelines.
---

> Kind: KNW | Scope: backend | Capability: — | Loading: on-demand knowledge

# HttpClient Factory

Policy: `.claude/rules/backend/runtime.md` (client lifetime, timeouts, retries, fallback, cancellation), `.claude/rules/backend/architecture.md` (transport does not leak into Application). Retries, circuit breakers, hedging, and pipelines: `references/resilience.md`.

## Architectural boundary

Application may define an abstraction; Infrastructure implements it with `HttpClient`, so Application does not know the service uses HTTP:

```csharp
public interface IPaymentGateway
{
    Task<PaymentResult> ChargeAsync(PaymentRequest request, CancellationToken cancellationToken);
}

internal sealed class PaymentGateway(HttpClient httpClient) : IPaymentGateway
{
    // ...
}
```

## Client models

Named, typed, and keyed clients are all valid; choose the model that makes ownership and lifetime easiest to understand.

- **Typed** — one class owns communication with one remote API. Do not capture a transient typed client inside a singleton without understanding the lifetime implications.

  ```csharp
  services.AddHttpClient<PaymentGateway>(client => client.BaseAddress = new Uri(configuration["Payments:BaseUrl"]!));
  ```

- **Named** — a factory creates clients dynamically, several clients share a usage model, or a singleton creates clients per operation (`services.AddHttpClient("catalog", ...)`).
- **Keyed** — when keyed DI makes consumption clearer; not automatically because the framework supports it.

## Delegating handlers

Use a `DelegatingHandler` for genuine HTTP pipeline concerns — authorization header acquisition, correlation/context propagation, request signing — never for business decisions.

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

Pass the caller's token (`await httpClient.SendAsync(request, cancellationToken)`); use `CancellationToken.None` only when the operation intentionally must outlive the incoming request. Choose time limits from the remote operation and the application's latency budget; with resilience pipelines distinguish per-attempt timeout from total-operation timeout.

## Response mapping

Translate remote responses into the abstraction Application consumes. Do not blindly call `EnsureSuccessStatusCode()` when specific statuses carry contract meaning:

```csharp
if (response.StatusCode == HttpStatusCode.NotFound)
{
    return null;
}

response.EnsureSuccessStatusCode();
```

Translate richer failures into explicit Infrastructure/Application outcomes, and do not expose every upstream status code through your own API; the outbound retry behavior and the inbound response your API returns are separate decisions.

## Retry safety

Before enabling retry determine whether the failure is transient, whether the operation is safe to repeat, whether the remote API supports idempotency, and whether retry may duplicate side effects. POST/PATCH and other state-changing operations need API-defined idempotency keys, naturally idempotent semantics, or explicit deduplication; do not assume a PUT or DELETE implementation is operationally safe merely because the method is defined as idempotent. A timeout is normally required; retry and circuit breaker are not mandatory for every call.

## Headers and serialization

Configure stable headers (media types) on the client; apply per-request values such as dynamic access tokens to the specific request or through a handler, never by mutating shared `DefaultRequestHeaders` concurrently. Prefer `System.Net.Http.Json`/`System.Text.Json`, with explicit serializer options when the external contract differs from application defaults; never reuse Domain entities as remote API contracts to avoid mapping.

## Testing

A controlled `HttpMessageHandler` verifies method/path, headers, serialized payload, response mapping, and cancellation/failure behavior:

```csharp
var client = new HttpClient(testHandler) { BaseAddress = new Uri("https://example.test/") };
```

Constructing `HttpClient` directly in a focused test is fine; the lifetime rule concerns production code.

## Anti-patterns

Making typed/keyed/named clients mandatory universally, infinite or poorly bounded retries, ignoring cancellation, dynamic auth tokens in shared `DefaultRequestHeaders`, mapping every upstream failure to the same status, and adding resilience pipelines without understanding their behavior.
