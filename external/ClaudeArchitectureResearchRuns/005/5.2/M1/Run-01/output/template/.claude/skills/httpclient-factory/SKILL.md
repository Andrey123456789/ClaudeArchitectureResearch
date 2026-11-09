---
name: httpclient-factory
description: >
  Outbound HTTP: IHttpClientFactory typed/named/keyed clients,
  DelegatingHandlers, timeouts, cancellation, response mapping, 429, resilience
  handlers, retries, circuit breakers.
---

> **Knowledge skill** · Owns: outbound HTTP client technique and examples (resilience depth in `references/resilience.md`) · Scope: backend · Loading: on demand

# HttpClient Factory

## Rules

Rules: `performance.md` → HTTP (managed `HttpClient` lifetime) and
`backend-runtime.md` → Outbound Calls (Application-facing translation, bounded
execution time, safe retries, `Retry-After`, fallback, caller cancellation).

1. Named, typed, and keyed clients are all valid; choose the simplest model for
   the consumer and lifetime.
2. Outbound API clients normally belong in Infrastructure.
3. Propagate `CancellationToken` to every outbound call.

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

Infrastructure implements it with `HttpClient`.

```csharp
internal sealed class PaymentGateway(HttpClient httpClient)
    : IPaymentGateway
{
    ...
}
```

Application does not need to know the external service uses HTTP.

## Typed Clients

Typed clients are useful when one class owns communication with one remote API.

```csharp
services.AddHttpClient<PaymentGateway>(client =>
{
    client.BaseAddress = new Uri(configuration["Payments:BaseUrl"]!);
});
```

Do not capture a transient typed client inside a singleton without understanding
its lifetime implications.

## Named Clients

Named clients are useful when:

- a factory creates clients dynamically;
- several clients share one usage model;
- a singleton needs to create clients per operation.

```csharp
services.AddHttpClient("catalog", client =>
{
    client.BaseAddress = new Uri(configuration["Catalog:BaseUrl"]!);
});
```

## Keyed Clients

Keyed clients are useful when keyed DI makes consumption clearer.

Do not choose keyed clients automatically simply because the framework supports
them.

Prefer whichever model makes ownership and lifetime easiest to understand.

## Delegating Handlers

Use `DelegatingHandler` for genuine HTTP pipeline concerns such as:

- authorization header acquisition;
- correlation/context propagation;
- specialized request signing.

Do not hide business decisions inside handlers.

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

```csharp
await httpClient.SendAsync(
    request,
    cancellationToken);
```

Do not replace request cancellation with arbitrary `CancellationToken.None`
unless the operation intentionally must outlive the incoming request.

## Timeouts

Choose timeouts according to the remote operation and the application's latency
budget (`backend-runtime.md` → Outbound Calls).

When using resilience pipelines, understand the difference between:

- per-attempt timeout;
- total-operation timeout.

## Response Mapping

Infrastructure should translate remote HTTP responses into the abstraction
consumed by Application.

Do not blindly use `EnsureSuccessStatusCode()` when specific remote statuses
have meaningful contract semantics.

Example:

```csharp
if (response.StatusCode == HttpStatusCode.NotFound)
{
    return null;
}

response.EnsureSuccessStatusCode();
```

For richer failure semantics, translate responses into explicit Infrastructure /
Application outcomes.

Do not simply expose every upstream status code to your own API.

## 429 and Retry-After

The standard resilience handler honors `Retry-After` for `429` responses. The
outbound client's retry behavior and the inbound HTTP response your own API
returns are separate decisions.

## Resilience

Read `references/resilience.md` when configuring retries, circuit breakers,
hedging, fallback, or resilience pipelines. Retry and circuit breaker are not
mandatory for every external call.

Before enabling retry, determine:

- whether the failure is transient;
- whether the operation is safe to repeat;
- whether the remote API supports idempotency;
- whether retry may duplicate side effects.

## Unsafe HTTP Methods

State-changing operations become safe to retry through mechanisms such as
(`backend-runtime.md` → Outbound Calls):

- API-defined idempotency keys;
- naturally idempotent operation semantics;
- explicit deduplication.

Do not assume every PUT or DELETE implementation is operationally safe merely
because the HTTP method is defined as idempotent.

## Headers

Stable headers such as media types may be configured on the client.

Per-request values such as dynamic access tokens should normally be applied to
the specific request or through an appropriate handler.

Do not mutate shared default headers concurrently for request-specific values.

## Serialization

Prefer `System.Net.Http.Json` / `System.Text.Json` where sufficient.

Use explicit serialization options when the external API contract differs from
the application's defaults.

Do not reuse internal Domain entities as remote API contracts merely to avoid
mapping.

## Testing

For an outbound adapter, a controlled `HttpMessageHandler` can verify:

- request method/path;
- headers;
- serialized payload;
- response mapping;
- cancellation/failure behavior.

```csharp
var client = new HttpClient(testHandler)
{
    BaseAddress = new Uri("https://example.test/")
};
```

Using `new HttpClient(testHandler)` in a focused test is fine; the prohibition on
per-request construction concerns production lifetime management.

## Anti-Patterns

Avoid:

- making typed/keyed/named clients mandatory universally;
- dynamic auth tokens in shared `DefaultRequestHeaders`;
- blind `EnsureSuccessStatusCode()` where remote statuses carry meaning;
- mapping every upstream failure mechanically to the same status in your own API;
- adding resilience pipelines without understanding their behavior.
