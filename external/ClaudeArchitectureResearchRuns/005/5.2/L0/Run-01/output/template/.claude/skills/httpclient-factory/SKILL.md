---
name: httpclient-factory
description: >
  Use for outbound HTTP calls: typed/named clients, gateway adapters, timeouts, handlers, response mapping, retries and resilience pipelines.
---

> Level: 2 Technology | Owns: outbound HttpClient and resilience technique | Scope: backend | Loads: knowledge skill (on demand) | Depends on: 0-core/integration-principles.md, 2-technology/dotnet-runtime.md

# HttpClient Factory Technique

Policy owners (routing): client lifetime → `2-technology/dotnet-runtime.md`;
time bounds, retry safety, `Retry-After`, fallback, cancellation →
`0-core/integration-principles.md`; transport not leaking into Application →
`1-architecture/backend-layers.md`; resilience package choice →
`add-dependency`. Resilience depth: read `references/resilience.md`.

## Gateway Boundary

```csharp
// Application
public interface IPaymentGateway
{
    Task<PaymentResult> ChargeAsync(PaymentRequest request, CancellationToken cancellationToken);
}

// Infrastructure
internal sealed class PaymentGateway(HttpClient httpClient) : IPaymentGateway
{
    public async Task<PaymentResult> ChargeAsync(PaymentRequest request, CancellationToken cancellationToken)
    {
        using var response = await httpClient.PostAsJsonAsync("charges", request, cancellationToken);
        // translate the remote contract into PaymentResult here
        ...
    }
}
```

Application does not need to know the dependency uses HTTP.

## Client Styles

- **Typed** — one class owns communication with one remote API:
  `services.AddHttpClient<PaymentGateway>(c => c.BaseAddress = new Uri(options.BaseUrl));`
  Do not capture a transient typed client in a singleton without understanding
  the lifetime.
- **Named** — a factory creates clients dynamically, several consumers share a
  usage model, or a singleton creates clients per operation:
  `services.AddHttpClient("catalog", c => ...)` + `IHttpClientFactory.CreateClient("catalog")`.
- **Keyed** — when keyed DI makes consumption clearer; not by default.

Choose the simplest model whose ownership and lifetime are easy to understand.

## Handlers and Headers

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

Use handlers for genuine pipeline concerns (token acquisition, correlation
propagation, request signing), never for business decisions. Configure stable
headers (media types) on the client; apply per-request values per request or in
a handler — never by mutating shared `DefaultRequestHeaders` concurrently.

## Cancellation and Timeouts

Pass the caller's `CancellationToken` to `SendAsync`/`GetAsync`; use
`CancellationToken.None` only when the operation must deliberately outlive the
request. Choose timeouts from the remote operation and the latency budget; with
resilience pipelines distinguish per-attempt and total timeouts.

## Response Mapping

```csharp
if (response.StatusCode == HttpStatusCode.NotFound)
    return null;
response.EnsureSuccessStatusCode();
```

Do not call `EnsureSuccessStatusCode()` blindly when specific statuses carry
contract meaning; translate richer failures into explicit outcomes, and do not
pass every upstream status through to your own API. The outbound retry policy
and your API's inbound response are separate decisions.

## Serialization

Prefer `System.Net.Http.Json` / `System.Text.Json`; set explicit serializer
options when the remote contract differs from application defaults; do not reuse
Domain entities as remote contracts to avoid mapping.

## Testing

```csharp
var client = new HttpClient(stubHandler) { BaseAddress = new Uri("https://example.test/") };
```

A controlled `HttpMessageHandler` verifies method, path, headers, payload,
response mapping, and cancellation/failure behavior. Constructing `HttpClient`
directly in a focused test is fine; the lifetime rule concerns production code.
