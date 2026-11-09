---
name: httpclient-factory
description: >
  Use when implementing or reviewing calls to external HTTP APIs: typed, named,
  or keyed HttpClient registration, Infrastructure adapters, DelegatingHandlers,
  timeouts, response mapping, Retry-After, outbound testing, or resilience
  pipelines (retry, circuit breaker, hedging, fallback) via its reference.
---

> Owns: outbound HttpClient and resilience technique | Scope: backend | Loads: on demand (knowledge skill); private reference references/resilience.md

# HttpClient Factory

Policy owners: client lifetime → `.claude/rules/performance.md` (Outbound HTTP);
bounded time, retry safety, Retry-After, fallback, cancellation →
`.claude/rules/error-handling.md` (Outbound Dependency Calls); transport not
leaking into Application → `.claude/rules/architecture.md`; resilience packages →
`docs/technology-stack.md`. Resilience technique: `references/resilience.md`.

## Architectural Boundary

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
        using var response = await httpClient.PostAsJsonAsync("payments", request, cancellationToken);
        // translate the remote response into PaymentResult here
        ...
    }
}
```

## Choosing a Client Model

Named, typed, and keyed clients are all valid; pick whichever makes ownership and
lifetime easiest to understand.

```csharp
// Typed: one class owns communication with one remote API
services.AddHttpClient<IPaymentGateway, PaymentGateway>(client =>
    client.BaseAddress = new Uri(configuration["Payments:BaseUrl"]!));

// Named: factories, shared usage, or singletons creating clients per operation
services.AddHttpClient("catalog", client =>
    client.BaseAddress = new Uri(configuration["Catalog:BaseUrl"]!));
```

Do not capture a transient typed client inside a singleton without understanding
the lifetime implications; keyed clients only when keyed DI makes consumption
clearer.

## Delegating Handlers

For genuine HTTP pipeline concerns — auth header acquisition, correlation
propagation, request signing — not business decisions.

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

Stable headers (media types) may sit on the client; per-request values such as
dynamic tokens go on the request or a handler, never into shared
`DefaultRequestHeaders` mutated concurrently.

## Cancellation and Timeouts

Pass the caller's token (`await httpClient.SendAsync(request, cancellationToken)`);
use `CancellationToken.None` only when the operation intentionally outlives the
request. Choose timeouts from the remote operation and latency budget
(`HttpClient.Timeout`, or attempt/total timeouts in a resilience pipeline — not
both without understanding their interaction).

## Response Mapping

```csharp
if (response.StatusCode == HttpStatusCode.NotFound)
    return null;

response.EnsureSuccessStatusCode();
```

Avoid blind `EnsureSuccessStatusCode()` when specific statuses have contract
meaning; translate richer failures into explicit outcomes. Do not mirror every
upstream status into your own API — the outbound retry policy and the inbound
response you return are separate decisions (`http-api`).

## Retry Safety Checklist

Before enabling retry, determine whether the failure is transient, whether the
operation is safe to repeat, whether the remote API supports idempotency (keys,
naturally idempotent semantics, explicit deduplication), and whether a retry
could duplicate side effects. An HTTP method being "idempotent" by definition
does not make a specific `PUT`/`DELETE` implementation operationally safe.

## Serialization

Prefer `System.Net.Http.Json` / `System.Text.Json`; use explicit options when the
remote contract differs from defaults. Do not reuse Domain entities as remote API
contracts to avoid mapping.

## Testing Outbound Adapters

A controlled `HttpMessageHandler` verifies method/path, headers, serialized
payload, response mapping, and cancellation/failure behavior:

```csharp
var client = new HttpClient(testHandler) { BaseAddress = new Uri("https://example.test/") };
```

Constructing `HttpClient` directly in a focused test is fine; the lifetime rule
concerns production code.
