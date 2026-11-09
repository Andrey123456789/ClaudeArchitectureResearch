---
name: httpclient-factory
description: >
  Use for outbound HTTP calls: IHttpClientFactory, typed/named/keyed clients,
  DelegatingHandlers, timeouts, cancellation, response mapping, Retry-After,
  resilience pipelines.
---

> Knowledge skill · Outbound HTTP technique · Policy: `.claude/rules/performance.md` § Outbound Calls, `.claude/rules/architecture.md` § Layer Placement · Resilience depth: `references/resilience.md`

# HttpClient Factory

Named, typed, and keyed clients are all valid; choose the simplest model for
the consumer and its lifetime. Outbound API clients belong in Infrastructure.
Retry and circuit-breaker behavior is added only when its semantics fit.

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

Do not capture a transient typed client inside a singleton without
understanding its lifetime implications.

## Named Clients

Useful when a factory creates clients dynamically, several clients share one
usage model, or a singleton creates clients per operation:

```csharp
services.AddHttpClient("catalog", client =>
{
    client.BaseAddress = new Uri(configuration["Catalog:BaseUrl"]!);
});
```

## Keyed Clients

Useful when keyed DI makes consumption clearer; do not choose them
automatically because the framework supports them.

## Delegating Handlers

Use a `DelegatingHandler` for genuine HTTP pipeline concerns — authorization
header acquisition, correlation/context propagation, specialized request
signing — and never for business decisions.

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

Do not replace request cancellation with `CancellationToken.None` unless the
operation intentionally must outlive the incoming request.

## Timeouts

Choose timeouts from the remote operation and the application's latency
budget. With resilience pipelines, distinguish the per-attempt timeout from the
total-operation timeout.

## Response Mapping

Translate remote responses into the abstraction Application consumes. Do not
blindly call `EnsureSuccessStatusCode()` when specific remote statuses carry
contract meaning:

```csharp
if (response.StatusCode == HttpStatusCode.NotFound)
{
    return null;
}

response.EnsureSuccessStatusCode();
```

For richer failure semantics, translate responses into explicit Infrastructure
or Application outcomes, and do not expose every upstream status code through
your own API.

## 429 and Retry-After

When a remote service returns `429 Too Many Requests`, honor `Retry-After` when
the selected retry policy supports it. The outbound client's retry behavior and
the inbound response your own API returns are separate decisions.

## Resilience

Configure retries, circuit breakers, hedging, fallback, or pipelines with
`references/resilience.md`. Before enabling retry, determine whether the
failure is transient, whether the operation is safe to repeat, whether the
remote API supports idempotency, and whether a retry may duplicate side effects.
For POST/PATCH and other state-changing operations, retry safety comes from
API-defined idempotency keys, naturally idempotent semantics, or explicit
deduplication; do not assume every PUT or DELETE implementation is
operationally safe merely because the method is defined as idempotent.

## Headers

Stable headers such as media types may be configured on the client. Apply
per-request values such as dynamic access tokens to the specific request or
through a handler; do not mutate shared default headers concurrently.

## Serialization

Prefer `System.Net.Http.Json` / `System.Text.Json` where sufficient, with
explicit serialization options when the external contract differs from the
application's defaults. Do not reuse internal Domain entities as remote API
contracts to avoid mapping.

## Testing

A controlled `HttpMessageHandler` can verify request method/path, headers,
serialized payload, response mapping, and cancellation/failure behavior:

```csharp
var client = new HttpClient(testHandler)
{
    BaseAddress = new Uri("https://example.test/")
};
```

Constructing `HttpClient` directly in a focused test is fine; the lifetime rule
concerns production code.

## Review Checks

Check-by-reference against `performance.md` § Outbound Calls and
`architecture.md` § Layer Placement: a new `HttpClient` per request; typed,
keyed, or named clients made mandatory universally; retries on unsafe
operations without idempotency analysis; infinite or poorly bounded retries;
`HttpResponseMessage` leaking across boundaries; ignored cancellation; dynamic
tokens in shared `DefaultRequestHeaders`; every upstream failure mapped to the
same status; resilience pipelines added without understanding their behavior.
