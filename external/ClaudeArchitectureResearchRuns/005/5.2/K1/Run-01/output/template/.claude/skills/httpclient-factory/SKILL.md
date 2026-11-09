---
name: httpclient-factory
description: Use when implementing or reviewing calls to external HTTP APIs — IHttpClientFactory typed, named and keyed clients, Infrastructure adapters, DelegatingHandlers, timeouts, cancellation, response mapping, 429/Retry-After, retries, circuit breakers and resilience pipelines, and adapter tests.
---
Kind: KNW | Scope: backend | Capability: — | Loading: on invocation

# HttpClient Factory

Rules: `.claude/rules/backend/integrations.md` (client lifetime, timeouts, safe retries, Retry-After, fallback, cancellation) and `.claude/rules/backend/architecture.md` (remote transport stays out of Application). Resilience depth: `references/resilience.md` (read it when configuring retries, circuit breakers, hedging or resilience pipelines). Resilience package choice: `add-dependency`.

## Architectural boundary

Application may define an abstraction; Infrastructure implements it with `HttpClient`, and Application does not need to know the service uses HTTP:

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

## Choosing a client model

Typed, named and keyed clients are all valid; choose the simplest model for the consumer and its lifetime.

- **Typed client**: one class owns communication with one remote API.

  ```csharp
  services.AddHttpClient<PaymentGateway>(client =>
  {
      client.BaseAddress = new Uri(configuration["Payments:BaseUrl"]!);
  });
  ```

  Do not capture a transient typed client inside a singleton without understanding the lifetime implications.
- **Named client**: a factory creates clients dynamically, several consumers share one usage model, or a singleton creates clients per operation.

  ```csharp
  services.AddHttpClient("catalog", client =>
  {
      client.BaseAddress = new Uri(configuration["Catalog:BaseUrl"]!);
  });
  ```
- **Keyed client**: when keyed DI makes consumption clearer; not automatically because the framework supports it.

## Delegating handlers

Use a `DelegatingHandler` for genuine HTTP pipeline concerns (authorization header acquisition, correlation propagation, request signing), never for business decisions:

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
```

## Cancellation and timeouts

Pass the incoming `CancellationToken` to `SendAsync`/`GetAsync`; replace it with `CancellationToken.None` only when the operation intentionally must outlive the incoming request. Choose timeouts from the remote operation and the application's latency budget, and when resilience pipelines are used, distinguish the per-attempt timeout from the total-operation timeout (`HttpClient.Timeout` versus pipeline timeouts).

## Response mapping

Translate remote responses into the abstraction Application consumes. Do not call `EnsureSuccessStatusCode()` blindly when specific remote statuses carry contract meaning:

```csharp
if (response.StatusCode == HttpStatusCode.NotFound)
{
    return null;
}

response.EnsureSuccessStatusCode();
```

For richer failure semantics, translate into explicit Infrastructure or Application outcomes. The status your own API returns is a separate decision (`http-api` skill); do not pass every upstream status through mechanically.

## 429 and Retry-After

When the remote service returns `429 Too Many Requests` with `Retry-After`, use a retry strategy that honors it (the standard resilience handler does). The outbound retry behavior and the inbound response your API returns are separate decisions.

## Resilience

A bounded execution time is required for external I/O; retry and circuit breakers are not mandatory for every call. Before enabling retry, determine whether the failure is transient, whether the operation is safe to repeat, whether the remote API supports idempotency, and whether a retry may duplicate side effects. POST, PATCH and other state-changing calls need API-defined idempotency keys, naturally idempotent semantics or explicit deduplication before automatic retry; do not assume every PUT or DELETE implementation is operationally safe because the HTTP method is defined as idempotent. Details: `references/resilience.md`.

## Headers and serialization

Configure stable headers such as media types on the client; apply per-request values such as dynamic access tokens to the request or through a handler, never by mutating shared `DefaultRequestHeaders` concurrently. Prefer `System.Net.Http.Json` and `System.Text.Json`, with explicit serializer options when the remote contract differs from the application's defaults. Do not reuse Domain entities as remote API contracts to avoid mapping.

## Testing

A controlled `HttpMessageHandler` verifies the request method and path, headers, serialized payload, response mapping, and cancellation or failure behavior of an outbound adapter:

```csharp
var client = new HttpClient(testHandler) { BaseAddress = new Uri("https://example.test/") };
```

Constructing `HttpClient` directly in a focused test is fine; the lifetime rule concerns production code.

## Anti-patterns

Review checks; `integrations.md` owns each rule unless noted:

- A new `HttpClient` per request, or a typed/keyed/named model made mandatory everywhere?
- Retries on unsafe operations without idempotency analysis, or infinite or poorly bounded retries?
- `HttpResponseMessage` crossing into Application? (`architecture.md`)
- Ignored cancellation, or dynamic auth tokens in shared default headers?
- Every upstream failure mapped mechanically to the same status of your own API?
- Resilience pipelines added without understanding their behavior?
