---
name: httpclient-factory
description: >
  Use for outbound HTTP: IHttpClientFactory typed, named, keyed clients,
  handlers, timeouts, response mapping, Retry-After; resilience, retries,
  circuit breakers.
---
> Level: 2-technology | Owns: outbound HTTP client technique; resilience depth in a private reference | Scope: backend | Loads: on demand (skill)

# HttpClient Factory

Policy: `outbound-calls.md` (client lifetime, timeouts, retry safety, fallback,
cancellation), `role-boundaries.md` (remote transport stays in adapters).
Resilience depth: `references/resilience.md`.

## Adapter boundary

The use-case side defines a contract; an adapter implements it with
`HttpClient`, so use-case code does not know the dependency uses HTTP.

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

Named, typed, and keyed clients are all valid; choose the simplest model for
the consumer and its lifetime.

```csharp
services.AddHttpClient<PaymentGateway>(client =>
{
    client.BaseAddress = new Uri(configuration["Payments:BaseUrl"]!);
});

services.AddHttpClient("catalog", client =>
{
    client.BaseAddress = new Uri(configuration["Catalog:BaseUrl"]!);
});
```

- Typed clients fit one class owning communication with one API; do not capture
  a transient typed client in a singleton without understanding the lifetime.
- Named clients fit factories, several clients sharing one usage model, or a
  singleton creating clients per operation.
- Keyed clients fit when keyed DI makes consumption clearer — not by default.

## Delegating handlers

For genuine HTTP pipeline concerns — token acquisition, correlation
propagation, request signing — never business decisions.

```csharp
internal sealed class AccessTokenHandler(IAccessTokenProvider tokens)
    : DelegatingHandler
{
    protected override async Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request,
        CancellationToken cancellationToken)
    {
        var token = await tokens.GetAsync(cancellationToken);
        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
        return await base.SendAsync(request, cancellationToken);
    }
}
```

## Cancellation and timeouts

Pass the caller's token to `SendAsync`; use `CancellationToken.None` only when
the operation intentionally outlives the request. Choose timeouts from the
remote operation and latency budget; with resilience pipelines distinguish
per-attempt from total-operation timeouts.

## Response mapping

Translate remote responses into the contract's result:

```csharp
if (response.StatusCode == HttpStatusCode.NotFound)
{
    return null;
}

response.EnsureSuccessStatusCode();
```

Do not blindly call `EnsureSuccessStatusCode()` when specific statuses carry
contract meaning, and do not expose every upstream status through your own API.
Outbound retry behavior and your API's inbound response are separate decisions.

## Retry preconditions

Before enabling retry: is the failure transient, is the operation safe to
repeat, does the remote API support idempotency, could retry duplicate side
effects? `POST`/`PATCH` need an idempotency key, naturally idempotent
semantics, or explicit deduplication; do not assume every `PUT`/`DELETE`
implementation is safe merely because the method is idempotent by definition.

## Headers and serialization

Configure stable headers (media types) on the client; apply per-request values
(dynamic tokens) to the request or through a handler — never mutate shared
`DefaultRequestHeaders` concurrently. Prefer `System.Net.Http.Json` /
`System.Text.Json`, with explicit options when the remote contract differs; do
not reuse domain entities as remote contracts.

## Testing

```csharp
var client = new HttpClient(testHandler) { BaseAddress = new Uri("https://example.test/") };
```

A controlled `HttpMessageHandler` verifies method/path, headers, payload,
response mapping, and cancellation/failure behavior. Constructing `HttpClient`
in a focused test is fine; the lifetime rule concerns production code.

## Anti-patterns

Per-request `HttpClient`; mandatory typed/keyed/named clients everywhere;
retries on unsafe operations without idempotency analysis; unbounded retries;
`HttpResponseMessage` across boundaries; ignored cancellation; dynamic tokens in
`DefaultRequestHeaders`; mapping every upstream failure to one status; resilience
pipelines whose behavior is not understood.
