---
name: httpclient-factory
description: >
  Use for outbound HTTP calls: typed/named/keyed HttpClient,
  DelegatingHandlers, timeouts, response mapping, Retry-After, test handlers,
  and resilience (retry, circuit breaker, fallback, hedging).
---

> Knowledge skill. Owns: outbound HTTP client technique; resilience depth through its private reference · Scope: backend · Loads: on demand · Depends on: CLAUDE.md, .claude/rules/architecture.md, .claude/rules/performance.md, .claude/rules/error-handling.md

# HttpClient Factory

Rules: `performance.md` (managed `HttpClient` lifetime), `error-handling.md`
(bounded execution time, retry safety, `Retry-After`, fallback, cancellation),
`architecture.md` (remote transport stays out of Application). Resilience
package choice: `add-dependency`. Resilience pipelines, retry, circuit
breakers, fallback, hedging, database and messaging retries: read
`references/resilience.md`.

## Choosing a Client Model

Named, typed, and keyed clients are all valid; choose the simplest model for the
consumer and its lifetime. Outbound API clients belong in Infrastructure.

## Architectural Boundary

```csharp
public interface IPaymentGateway
{
    Task<PaymentResult> ChargeAsync(
        PaymentRequest request,
        CancellationToken cancellationToken);
}
```

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

Capturing a transient typed client inside a singleton runs into the lifetime
rule (`architecture.md`, Composition and Configuration); resolve per operation
or use a named client instead.

## Named Clients

Useful when a factory creates clients dynamically, several clients share one
usage model, or a singleton needs a client per operation:

```csharp
services.AddHttpClient("catalog", client =>
{
    client.BaseAddress = new Uri(configuration["Catalog:BaseUrl"]!);
});
```

## Keyed Clients

Useful when keyed DI makes consumption clearer; do not choose them only because
the framework supports them.

## Delegating Handlers

Use a `DelegatingHandler` for genuine HTTP pipeline concerns — authorization
header acquisition, correlation/context propagation, request signing — not for
business decisions:

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

Pass the caller's token rather than `CancellationToken.None`, unless the
operation intentionally must outlive the incoming request (`performance.md`,
Async and Cancellation).

## Timeouts

Choose timeouts from the remote operation and the application's latency
budget. With resilience pipelines, distinguish the per-attempt timeout from the
total-operation timeout.

## Response Mapping

Infrastructure translates remote responses into the abstraction Application
consumes. Do not blindly call `EnsureSuccessStatusCode()` when specific remote
statuses have contract meaning:

```csharp
if (response.StatusCode == HttpStatusCode.NotFound)
{
    return null;
}

response.EnsureSuccessStatusCode();
```

For richer failure semantics, translate responses into explicit outcomes, and
do not simply expose every upstream status through your own API.

## 429 and Retry-After

The rule for rate-limit guidance is in `error-handling.md`. The standard
resilience handler's retry strategy can read `Retry-After`; the outbound retry
behavior and the inbound response your own API returns are separate
decisions.

## Before Enabling Retry

Retry and circuit breaker are optional, unlike the bounded execution time
required by `error-handling.md` (Outbound Dependencies). Questions to answer
first: is the failure transient, is the operation safe to repeat, does the
remote API support idempotency, can a retry duplicate side effects? Mechanisms
that can make a state-changing call repeatable: an API-defined idempotency key,
naturally idempotent operation semantics, or explicit deduplication. A PUT or
DELETE implementation is not operationally safe merely because the HTTP method
is defined as idempotent.

## Headers

Stable headers such as media types may be configured on the client;
per-request values such as dynamic access tokens go on the specific request or
through a handler. Do not mutate shared default headers concurrently.

## Serialization

Prefer `System.Net.Http.Json` / `System.Text.Json` where sufficient, use explicit
serialization options when the external contract differs from the
application's defaults, and do not reuse Domain entities as remote API
contracts merely to avoid mapping.

## Testing

A controlled `HttpMessageHandler` can verify the request method and path,
headers, serialized payload, response mapping, and cancellation/failure
behavior:

```csharp
var client = new HttpClient(testHandler)
{
    BaseAddress = new Uri("https://example.test/")
};
```

Constructing `new HttpClient(testHandler)` in a focused test is fine; the
lifetime rule concerns production code.

## Anti-Patterns

- making typed, keyed, or named clients mandatory universally;
- retries on unsafe operations without idempotency analysis;
- leaking `HttpResponseMessage` across architectural boundaries;
- dynamic auth tokens in shared `DefaultRequestHeaders`;
- mapping every upstream failure mechanically to the same status;
- adding resilience pipelines without understanding their behavior.
