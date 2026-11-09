---
name: httpclient-factory
description: >
  Use when calling external HTTP APIs or adding transient-failure handling:
  IHttpClientFactory clients, handlers, timeouts, cancellation, response
  mapping, retries, circuit breakers, fallback.
---

> Level: 2 Technology · Owns: outbound HTTP technique (private reference: resilience) · Scope: backend · Loads: on demand (knowledge skill)

# HttpClient Factory

Policy owners: `.claude/rules/2-technology/csharp.md` (client lifetime, cancellation), `.claude/rules/0-core/runtime-principles.md` (bounded time, retry safety, Retry-After, fallback, cancellation is not transient), `.claude/rules/1-architecture/backend-layers.md` (remote transport stays out of Application). Resilience pipelines: `references/resilience.md`; package selection is in the project decisions.

## Architectural shape

Application defines what it needs; Infrastructure implements it with `HttpClient`:

```csharp
public interface IPaymentGateway                                   // Application
{
    Task<PaymentResult> ChargeAsync(PaymentRequest request, CancellationToken cancellationToken);
}

internal sealed class PaymentGateway(HttpClient httpClient) : IPaymentGateway   // Infrastructure
{
    // ...
}
```

Application does not need to know the remote service speaks HTTP.

## Client models

| Model | Fits when | Registration |
|---|---|---|
| Typed | one class owns communication with one remote API | `services.AddHttpClient<PaymentGateway>(c => c.BaseAddress = new Uri(configuration["Payments:BaseUrl"]!));` |
| Named | a factory creates clients dynamically, several consumers share one usage model, or a singleton creates clients per operation | `services.AddHttpClient("catalog", c => ...)` + `IHttpClientFactory.CreateClient("catalog")` |
| Keyed | keyed DI makes consumption clearer | `services.AddHttpClient("catalog").AddAsKeyed()` + `[FromKeyedServices("catalog")] HttpClient` |

Pick the model whose ownership and lifetime are easiest to understand. Typed clients are transient — do not capture one inside a singleton.

## Delegating handlers

For genuine HTTP pipeline concerns (token acquisition, correlation propagation, request signing) — never business decisions:

```csharp
internal sealed class AccessTokenHandler(IAccessTokenProvider tokens) : DelegatingHandler
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

services.AddTransient<AccessTokenHandler>();
services.AddHttpClient<PaymentGateway>(...).AddHttpMessageHandler<AccessTokenHandler>();
```

## Cancellation and timeouts

Pass the caller's token to every call (`httpClient.SendAsync(request, cancellationToken)`); use `CancellationToken.None` only when the operation must deliberately outlive the incoming request. Configure a finite time budget per remote operation — `HttpClient.Timeout`, or attempt and total timeouts in a resilience pipeline (not both stacked without understanding the combination).

## Response mapping

Translate remote responses into the abstraction Application consumes:

```csharp
if (response.StatusCode == HttpStatusCode.NotFound)
    return null;

response.EnsureSuccessStatusCode();
return await response.Content.ReadFromJsonAsync<PaymentResult>(cancellationToken);
```

Do not call `EnsureSuccessStatusCode()` blindly when specific remote statuses carry contract meaning, and do not forward every upstream status to your own API — the inbound response is a separate decision (`http-api`).

## 429 and Retry-After

The standard HTTP retry strategy reads `Retry-After` (`references/resilience.md`). The outbound retry behavior and the status your own API returns are independent decisions.

## Before enabling retries

Ask: is the failure transient; is the operation safe to repeat; does the remote API support idempotency; could a retry duplicate side effects? `POST`/`PATCH` and other state-changing calls need an API-defined idempotency key, naturally idempotent semantics or explicit deduplication; a `PUT` or `DELETE` implementation is not automatically safe just because the method is idempotent in principle. A timeout is normally needed; retries and circuit breakers are not mandatory for every call.

## Headers and serialization

Configure stable headers (media types) on the client; apply per-request values (dynamic tokens) on the request or through a handler — never by mutating shared `DefaultRequestHeaders` concurrently. Prefer `System.Net.Http.Json`/`System.Text.Json`; use explicit serializer options when the remote contract differs from the application's defaults; never reuse Domain entities as remote API contracts.

## Testing adapters

```csharp
var client = new HttpClient(stubHandler) { BaseAddress = new Uri("https://example.test/") };
```

A controlled `HttpMessageHandler` verifies method, path, headers, payload, response mapping and cancellation/failure behavior. Constructing `HttpClient` directly in a focused test is fine — the lifetime rule concerns production code.

## Review cues

Per-request `HttpClient` construction, mandatory typed/keyed clients everywhere, retries on unsafe operations without idempotency analysis, unbounded retries, leaking `HttpResponseMessage`, ignored cancellation, dynamic tokens in shared default headers, every upstream failure mapped to one status, resilience handlers added without understanding their behavior.
