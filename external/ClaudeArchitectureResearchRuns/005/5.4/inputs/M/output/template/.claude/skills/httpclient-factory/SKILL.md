---
name: httpclient-factory
description: >
  Use when calling external HTTP APIs: IHttpClientFactory clients, adapters,
  handlers, timeouts, cancellation, response mapping, Retry-After, and
  resilience pipelines (retry, circuit breaker, fallback, hedging).
---

> Owns: outbound HTTP client technique and examples (no policy); private reference references/resilience.md | Scope: backend | Loads: on demand (knowledge skill)

# HttpClient Factory

Policy owners: `HttpClient` lifetime — `.claude/rules/performance.md`; bounded
execution time, retry safety, Retry-After, fallback, and caller cancellation —
`.claude/rules/error-handling.md`; transport not leaking into Application —
`.claude/rules/architecture.md`; resilience package choice — `add-dependency`.
For retries, circuit breakers, fallback, hedging, and pipelines read
`references/resilience.md`.

## Choosing a Client Model

Named, typed, and keyed clients are all valid; choose the simplest model for the
consumer and its lifetime. Outbound API clients normally live in
Infrastructure.

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

Application does not need to know the external service uses HTTP.

## Typed Clients

Useful when one class owns communication with one remote API:

```csharp
services.AddHttpClient<PaymentGateway>(client =>
{
    client.BaseAddress = new Uri(configuration["Payments:BaseUrl"]!);
});
```

Do not capture a transient typed client inside a singleton without
understanding the lifetime implications.

## Named Clients

Useful when a factory creates clients dynamically, several clients share one
usage model, or a singleton needs to create clients per operation:

```csharp
services.AddHttpClient("catalog", client =>
{
    client.BaseAddress = new Uri(configuration["Catalog:BaseUrl"]!);
});
```

## Keyed Clients

Useful when keyed DI makes consumption clearer. Do not choose them
automatically because the framework supports them; prefer the model whose
ownership and lifetime are easiest to understand.

## Delegating Handlers

Use a `DelegatingHandler` for genuine HTTP pipeline concerns — authorization
header acquisition, correlation/context propagation, specialized request
signing — never for business decisions.

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

Do not replace request cancellation with `CancellationToken.None` unless the
operation intentionally must outlive the incoming request.

## Timeouts

Choose timeouts from the remote operation and the application's latency budget.
With resilience pipelines, understand the difference between a per-attempt
timeout and a total-operation timeout (`references/resilience.md`).

## Response Mapping

Infrastructure translates remote responses into the abstraction consumed by
Application. Do not blindly call `EnsureSuccessStatusCode()` when specific
remote statuses carry contract meaning:

```csharp
if (response.StatusCode == HttpStatusCode.NotFound)
{
    return null;
}

response.EnsureSuccessStatusCode();
```

For richer failure semantics, translate responses into explicit Infrastructure
or Application outcomes. Do not simply expose every upstream status code through
your own API, and do not map every upstream failure mechanically to the same
status.

## 429 and Retry-After

When a remote service returns `429 Too Many Requests`, honor `Retry-After` if
the selected retry policy supports it. The outbound client's retry behavior and
the inbound response your own API returns are separate decisions.

## Before Enabling Retry

A timeout is normally required for external I/O; retry and circuit breaker are
not mandatory for every call. Before enabling retry, determine whether the
failure is transient, whether the operation is safe to repeat, whether the
remote API supports idempotency, and whether a retry may duplicate side effects.
Safety mechanisms for state-changing calls include API-defined idempotency keys,
naturally idempotent semantics, and explicit deduplication. Do not assume every
PUT or DELETE implementation is operationally safe merely because the HTTP
method is defined as idempotent.

## Headers

Stable headers such as media types may be configured on the client. Apply
per-request values such as dynamic access tokens to the specific request or
through a handler; do not mutate shared `DefaultRequestHeaders` concurrently for
request-specific values.

## Serialization

Prefer `System.Net.Http.Json` / `System.Text.Json` where sufficient. Use
explicit serialization options when the external contract differs from the
application's defaults, and do not reuse internal Domain entities as remote API
contracts merely to avoid mapping.

## Testing

A controlled `HttpMessageHandler` can verify request method/path, headers,
serialized payload, response mapping, and cancellation/failure behavior:

```csharp
var client = new HttpClient(testHandler)
{
    BaseAddress = new Uri("https://example.test/")
};
```

Constructing `new HttpClient(testHandler)` in a focused test is fine; the
lifetime rule concerns production code.

## Anti-Patterns

Avoid making typed, keyed, or named clients mandatory universally, ignoring
cancellation, putting dynamic auth tokens in shared `DefaultRequestHeaders`, and
adding resilience pipelines without understanding their behavior.
