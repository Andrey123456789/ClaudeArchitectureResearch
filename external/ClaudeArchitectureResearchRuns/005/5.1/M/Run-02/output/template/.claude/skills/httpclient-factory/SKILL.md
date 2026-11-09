---
name: httpclient-factory
description: >
  Use when calling external HTTP APIs: typed/named/keyed HttpClient
  registration, DelegatingHandlers, timeouts, response mapping, Retry-After,
  stub-handler tests, and resilience (AddStandardResilienceHandler, retries,
  circuit breakers, hedging, fallback).
---

> Owner: outbound HTTP client technique; resilience depth in a private reference (normative policy lives in rules) | Scope: backend | Loads: on demand — knowledge | Enforced: none

# HttpClient Factory

Policy: `.claude/rules/performance.md` § Outbound HTTP (client lifetime),
`.claude/rules/architecture.md` § Application (no HTTP transport in Application),
`.claude/rules/error-handling.md` § External Dependency Failures (timeouts,
retries, `Retry-After`, fallback, cancellation). Resilience pipelines:
`references/resilience.md`. Packages: `docs/technology-stack.md`
§ Conditional Technologies.

Named, typed, and keyed clients are all valid; choose the simplest model for the
consumer and its lifetime. Outbound API clients normally live in Infrastructure.

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

Infrastructure implements it with `HttpClient`, so Application never needs to
know the service uses HTTP:

```csharp
internal sealed class PaymentGateway(HttpClient httpClient)
    : IPaymentGateway
{
    ...
}
```

## Typed Clients

One class owns communication with one remote API:

```csharp
services.AddHttpClient<IPaymentGateway, PaymentGateway>(client =>
{
    client.BaseAddress = new Uri(configuration["Payments:BaseUrl"]!);
});
```

Prefer typed options for the base URL and timeouts in real code (`configuration`
skill). Do not capture a transient typed client inside a singleton without
understanding its lifetime.

## Named Clients

Useful when a factory creates clients dynamically, several clients share one
usage model, or a singleton must create clients per operation:

```csharp
services.AddHttpClient("catalog", client =>
{
    client.BaseAddress = new Uri(configuration["Catalog:BaseUrl"]!);
});
```

## Keyed Clients

Useful when keyed DI makes consumption clearer; do not choose them just because
the framework supports them.

## Delegating Handlers

For genuine HTTP pipeline concerns — authorization header acquisition,
correlation/context propagation, request signing — not business decisions:

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

Replace it with `CancellationToken.None` only when the operation intentionally
must outlive the incoming request.

## Timeouts

Choose timeouts from the remote operation and the application's latency budget.
`HttpClient.Timeout` is a total-request limit; with resilience pipelines,
distinguish the per-attempt timeout from the total-operation timeout
(`references/resilience.md`).

## Response Mapping

Translate remote responses into the abstraction Application consumes, and do not
use `EnsureSuccessStatusCode()` blindly when specific remote statuses carry
contract meaning:

```csharp
if (response.StatusCode == HttpStatusCode.NotFound)
{
    return null;
}

response.EnsureSuccessStatusCode();
```

For richer failure semantics, translate into explicit Infrastructure or
Application outcomes. Your own API's response is a separate decision from the
upstream status; do not pass every upstream status through mechanically.

## 429 and Retry-After

When a remote service returns `429 Too Many Requests`, the retry policy can honor
`Retry-After` (the standard resilience handler does). The outbound retry behavior
and the inbound response your API returns are separate decisions.

## Before Enabling Retry

Determine whether the failure is transient, whether the operation is safe to
repeat, whether the remote API supports idempotency (for example
`Idempotency-Key`), and whether a retry may duplicate side effects. Do not assume
a `PUT` or `DELETE` implementation is operationally safe merely because the
method is defined as idempotent. Retry and circuit breakers are not mandatory for
every call.

## Headers

Configure stable headers (media types) on the client; apply per-request values
such as dynamic access tokens on the request or in a handler. Mutating shared
`DefaultRequestHeaders` concurrently for request-specific values is not
thread-safe.

## Serialization

Prefer `System.Net.Http.Json` / `System.Text.Json`. Use explicit serializer
options when the external contract differs from application defaults, and map to
dedicated remote contracts rather than reusing Domain entities.

## Testing

A controlled `HttpMessageHandler` verifies method and path, headers, serialized
payload, response mapping, and cancellation/failure behavior:

```csharp
var client = new HttpClient(testHandler)
{
    BaseAddress = new Uri("https://example.test/")
};
```

Constructing `new HttpClient(testHandler)` in a focused test is fine; the
lifetime rule concerns production code.

## Common Mistakes

- making typed, keyed, or named clients mandatory everywhere;
- dynamic auth tokens in shared `DefaultRequestHeaders`;
- ignoring cancellation;
- adding resilience pipelines without understanding their behavior.
