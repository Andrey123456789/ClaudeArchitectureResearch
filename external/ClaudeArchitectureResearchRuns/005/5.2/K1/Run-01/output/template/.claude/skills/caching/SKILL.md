---
name: caching
description: Use when implementing, reviewing or troubleshooting caching in .NET — HybridCache, in-memory and distributed caches, output caching, cache keys, expiration, invalidation after mutations, cache failure behavior and cache tests.
---
Kind: KNW | Scope: backend | Capability: — | Loading: on invocation

# Caching

Rules: `.claude/rules/backend/performance.md` → Caching (when to cache, keys, expiration, invalidation) and `.claude/rules/backend/architecture.md` (cache technology stays out of inner layers). A distributed cache is a new infrastructure category and is Reserved (`CLAUDE.md` → Decision control). Define the consistency semantics (acceptable staleness, invalidation) before choosing a cache.

## Choosing the cache layer

- **HTTP response caching**: ASP.NET Core output caching when the entire response can safely be reused; it lives in the Api layer.
- **Application/data caching**: when a use case genuinely needs cache-aware behavior, define an Application abstraction and implement it in Infrastructure. Do not introduce an Application-level cache abstraction when caching can stay an internal Infrastructure concern.
- **Infrastructure caching**: adapters may cache expensive remote or persistence operations when that preserves the contract exposed to Application.

## HybridCache

`HybridCache` fits when the application benefits from local in-memory caching, optional distributed L2 caching, stampede protection and common cache-aside behavior. It is not mandatory.

```csharp
public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration configuration)
{
    services.AddHybridCache();
    return services;
}
```

Add a distributed backend such as Redis only when deployment requirements justify it.

## Cache abstraction example

When Application must coordinate invalidation explicitly:

```csharp
public interface IProductCache
{
    Task<ProductSummary?> GetAsync(Guid id, CancellationToken cancellationToken);
    Task SetAsync(ProductSummary product, CancellationToken cancellationToken);
    Task RemoveAsync(Guid id, CancellationToken cancellationToken);
}
```

Infrastructure may implement it with `HybridCache`; the Application contract does not expose `HybridCache`.

## Keys

Key rules: `performance.md` → Caching. Centralize key construction (for example a small key-builder per cached type) when duplicated key formats become hard to maintain.

## Expiration

Choose expiration from data semantics rather than universal defaults: how often the data changes, regeneration cost, acceptable staleness, memory footprint, and behavior when the source is unavailable.

## Invalidation strategies

Remove the affected key after a successful mutation; a short TTL with tolerated staleness; tag or group invalidation; versioned keys. Invalidating before the underlying mutation is known to have succeeded is acceptable only when the workflow deliberately accepts it.

## Output caching

```csharp
builder.Services.AddOutputCache(options =>
{
    options.AddPolicy("ProductById", policy => policy
        .Expire(TimeSpan.FromMinutes(5))
        .SetVaryByRouteValue("id"));
});

app.UseOutputCache();
```

For controllers, apply the selected policy through controller or action metadata (`[OutputCache(PolicyName = "ProductById")]`). Do not cache authenticated or user-specific responses unless the key and policy isolate users and authorization context.

## Mutations

Application Services keep their normal repository and Unit of Work workflow. When invalidation is part of the use-case semantics, coordinate it through an abstraction; do not bypass repositories or the Unit of Work to make invalidation convenient.

## Failure behavior

Decide whether a cache failure falls back to the source, fails the request or returns stale data.

## Testing

Test cache behavior when it affects observable correctness: stale entries invalidated after a successful mutation, tenant and user keys isolated, a miss falling back correctly, an outage following the intended failure policy. Do not unit-test framework cache internals.

## Anti-patterns

Review checks; the named standard owns each rule:

- Caching by default without a demonstrated reason, or unbounded entries? (`performance.md`)
- Global keys for tenant- or user-specific data? (`performance.md`)
- Cache technology in Domain, or `HybridCache` in Application contracts without a deliberate decision? (`architecture.md`)
- Tracked persistence entities cached across Unit of Work boundaries?
- The cache used as authoritative persistence? (`performance.md`)
- Redis added merely because the application caches? (`CLAUDE.md` → Decision control)

## Quick reference

| Need | Consider |
|---|---|
| Entire reusable HTTP response | ASP.NET Core output caching |
| Local application cache | In-memory cache or HybridCache |
| Multi-instance shared cache | Distributed cache / HybridCache L2 (Reserved decision) |
| Expensive repeated remote read | Cache in Infrastructure when the contract permits |
| Application-controlled invalidation | Application abstraction + Infrastructure implementation |
| Unknown performance problem | Measure before caching |
