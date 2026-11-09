---
name: httpclient-factory
description: >
  Use for calls to external HTTP APIs: IHttpClientFactory, typed/named clients,
  handlers, timeouts, cancellation, response mapping, retries and resilience.
---

> Level: 2 Technology · Owns: outbound HTTP client technique and examples (knowledge) · Scope: backend · Loads: on invocation · Depends on: .claude/rules/0-core/runtime-principles.md, .claude/rules/2-technology/csharp.md

# HttpClient Factory

Policy owners: client lifetime → `.claude/rules/2-technology/csharp.md`; bounded time, retry safety, Retry-After, fallback, cancellation → `0-core/runtime-principles.md`; transport not leaking into Application → `1-architecture/backend-layers.md`; resilience package choice → `add-dependency`. Resilience depth: `references/resilience.md`. This skill is technique only.

## Architectural shape

Application defines the abstraction; Infrastructure implements it with `HttpClient`:

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

Application does not need to know the external service uses HTTP.

## Client styles

Named, typed, and keyed clients are all valid; choose the simplest for the consumer and lifetime.

```csharp
// Typed: one class owns communication with one remote API
services.AddHttpClient<PaymentGateway>(client =>
    client.BaseAddress = new Uri(configuration["Payments:BaseUrl"]!));

// Named: factories, shared usage models, or singletons creating clients per operation
services.AddHttpClient("catalog", client =>
    client.BaseAddress = new Uri(configuration["Catalog:BaseUrl"]!));
```

Do not capture a transient typed client inside a singleton without understanding the lifetime implications. Choose keyed clients only when keyed DI makes consumption clearer.

## Delegating handlers

Use `DelegatingHandler` for genuine HTTP pipeline concerns — access-token acquisition, correlation propagation, request signing — never for business decisions:

```csharp
internal sealed class AccessTokenHandler(IAccessTokenProvider tokens) : DelegatingHandler
{
    protected override async Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request, CancellationToken cancellationToken)
    {
        var token = await tokens.GetAsync(cancellationToken);
        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
        return await base.SendAsync(request, cancellationToken);
    }
}
```

## Cancellation and timeouts

Pass the caller's token to every outbound call (`await httpClient.SendAsync(request, cancellationToken)`); use `CancellationToken.None` only when the operation intentionally must outlive the incoming request. Choose timeouts from the remote operation and the latency budget; with resilience pipelines distinguish per-attempt from total-operation timeouts.

## Response mapping

Translate remote responses into the abstraction Application consumes. Do not call `EnsureSuccessStatusCode()` blindly when specific statuses carry contract meaning:

```csharp
if (response.StatusCode == HttpStatusCode.NotFound)
    return null;

response.EnsureSuccessStatusCode();
```

For richer failure semantics translate into explicit Infrastructure/Application outcomes; do not pass every upstream status through to your own API. The outbound retry behavior and the inbound response your API returns are separate decisions.

## Retries and unsafe methods

Retry and circuit breaker are not mandatory for every call. Before enabling retry, determine whether the failure is transient, whether the operation is safe to repeat, whether the remote API supports idempotency, and whether a retry may duplicate side effects. POST/PATCH and other state-changing operations are not retried automatically unless an idempotency key, naturally idempotent semantics, or explicit deduplication makes it safe; do not assume every PUT/DELETE implementation is operationally safe. Configuration: `references/resilience.md`.

## Headers and serialization

Configure stable headers (media types) on the client; apply per-request values such as dynamic tokens per request or through a handler — never mutate shared `DefaultRequestHeaders` concurrently. Prefer `System.Net.Http.Json` / `System.Text.Json`, with explicit options when the remote contract differs; do not reuse Domain entities as remote contracts to avoid mapping.

## Testing adapters

A controlled `HttpMessageHandler` verifies method/path, headers, payload, response mapping, and cancellation/failure behavior:

```csharp
var client = new HttpClient(testHandler) { BaseAddress = new Uri("https://example.test/") };
```

Constructing `HttpClient` directly in a focused test is fine; the lifetime rule concerns production code.

## Anti-patterns

Making one client style mandatory everywhere; dynamic tokens in shared default headers; mapping every upstream failure to the same status; resilience pipelines added without understanding their behavior.
