---
name: caching
description: >
  Use for caching: HybridCache, IMemoryCache, distributed caches and Redis,
  output caching, cache keys, expiration, invalidation after mutations, stale
  data, cache failure behavior.
---

> Knowledge skill · Caching technique · Policy: `.claude/rules/performance.md` § Caching, `.claude/rules/architecture.md` § Layer Placement

# Caching

Define consistency semantics first — how stale data may become and how it is
invalidated — and measure before adding caching solely for performance.

## Choosing the Cache Layer

- **HTTP response caching** — ASP.NET Core output caching when the entire HTTP
  response can safely be reused; it belongs in the API layer.
- **Application/data caching** — when a use case genuinely needs cache-aware
  behavior, define an abstraction in Application and implement it in
  Infrastructure; do not introduce one if caching can stay an internal
  Infrastructure concern.
- **Infrastructure caching** — adapters may cache expensive remote or
  persistence operations when doing so preserves the contract exposed to
  Application.

## HybridCache

A strong option when the application benefits from local in-memory caching,
optional distributed L2 caching, stampede protection, and common cache-aside
behavior. Not mandatory.

```csharp
public static IServiceCollection AddInfrastructure(
    this IServiceCollection services,
    IConfiguration configuration)
{
    services.AddHybridCache();

    return services;
}
```

Add a distributed backend such as Redis only when deployment requirements
justify it (distributed caching is Reserved).

## Cache Abstraction Example

When Application must coordinate invalidation explicitly:

```csharp
public interface IProductCache
{
    Task<ProductSummary?> GetAsync(
        Guid id,
        CancellationToken cancellationToken);

    Task SetAsync(
        ProductSummary product,
        CancellationToken cancellationToken);

    Task RemoveAsync(
        Guid id,
        CancellationToken cancellationToken);
}
```

Infrastructure may implement this contract with `HybridCache`; do not expose
`HybridCache` itself from Application contracts.

## Cache Keys

Centralize key construction when duplicated key formats become hard to
maintain.

## Expiration

Choose expiration from data semantics rather than arbitrary universal defaults:
change frequency, regeneration cost, acceptable staleness, memory footprint,
and failure behavior when the source is unavailable. Avoid unbounded entries.

## Invalidation Strategies

Typical strategies: remove the affected key after a successful mutation, short
TTL with tolerated staleness, tag/group invalidation, versioned keys.

No single order is correct by itself (`.claude/rules/performance.md` § Caching
owns the choice): evicting after commit leaves stale data if the process crashes
between the two, or if a concurrent reader refills a value it read before the
commit; evicting before the mutation lets a concurrent reader refill the old
value before the commit, while a rollback only costs a miss. Bound these windows
with a lifetime, versioned keys, or a retried invalidation, and document the
staleness you accept.

## Output Caching

```csharp
builder.Services.AddOutputCache(options =>
{
    options.AddPolicy(
        "ProductById",
        policy => policy
            .Expire(TimeSpan.FromMinutes(5))
            .SetVaryByRouteValue("id"));
});

app.UseOutputCache();
```

For Controllers, apply the selected output-cache policy through controller or
action metadata. Do not cache authenticated or user-specific responses unless
the cache key and policy correctly isolate users and authorization context.

## Mutations

Application Services perform their normal repository/Unit of Work workflow; if
cache invalidation is part of the use-case semantics, coordinate it through an
abstraction. Do not bypass repositories or `IUnitOfWork` to make invalidation
convenient.

## Failure Behavior

Decide whether a cache failure falls back to the source, fails the request, or
returns stale data.

## Testing

Test cache behavior when it affects observable correctness: stale entries are
invalidated after a successful mutation, tenant/user keys are isolated, a miss
falls back correctly, an outage follows the intended failure policy. Do not
unit-test framework cache internals.

## Review Checks

Check-by-reference against `performance.md` § Caching and `architecture.md`
§ Layer Placement: caching by default without a reason; global keys for
tenant/user data; mutable data cached indefinitely without invalidation; cache
technology in Domain; Application depending directly on `HybridCache` without a
deliberate decision; tracked persistence entities cached across Unit of Work
boundaries; cache used as authoritative persistence; Redis added merely because
the application caches.

## Decision Guide

| Need | Default consideration |
|---|---|
| Entire reusable HTTP response | ASP.NET Core output caching |
| Local application cache | In-memory or HybridCache |
| Multi-instance shared cache | Distributed cache / HybridCache L2 |
| Expensive repeated remote read | Cache in Infrastructure when the contract permits |
| Application-controlled invalidation | Application abstraction + Infrastructure implementation |
| Unknown performance problem | Measure before adding caching |
