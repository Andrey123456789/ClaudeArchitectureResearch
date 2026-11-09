---
name: caching
description: Use when adding or reviewing caching — cache layer choice, HybridCache, in-memory/distributed caches, output caching, keys, expiration, invalidation, failure behavior.
---

> Kind: KNW | Scope: backend | Owner: caching technique with examples | Loading: on demand (model-invoked knowledge)

# Caching

Rules: `rules/backend/caching.md` (need, boundaries, keys, lifetime, invalidation). Distributed caching is Reserved (CLAUDE.md § Decisions).

Define consistency semantics first — how stale data may become and how it is invalidated — and measure before adding caching purely for performance.

## Choosing the cache layer

- **HTTP response caching** — ASP.NET Core output caching when the whole response can safely be reused; it belongs in the API layer.
- **Application/data caching** — when a use case genuinely needs cache-aware behavior, define an Application abstraction and implement it in Infrastructure; skip the abstraction when caching can stay an internal Infrastructure concern.
- **Infrastructure caching** — adapters may cache expensive remote or persistence operations when the contract exposed to Application is preserved.

## HybridCache

A strong option for local in-memory caching with optional distributed L2, stampede protection and cache-aside behavior — not mandatory everywhere.

```csharp
public static IServiceCollection AddInfrastructure(
    this IServiceCollection services,
    IConfiguration configuration)
{
    services.AddHybridCache();

    return services;
}
```

A distributed backend such as Redis is added only when deployment requirements justify it.

## Application cache abstraction

When Application coordinates invalidation explicitly:

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

Infrastructure may implement it with `HybridCache`, which stays out of Application contracts (`rules/backend/caching.md`). Centralize key construction once duplicated key formats become hard to maintain.

## Expiration

Choose by data semantics, not a universal default: change frequency, regeneration cost, acceptable staleness, memory footprint, behavior when the source is unavailable.

## Invalidation strategies

Remove affected keys after a successful mutation; short TTL with tolerated staleness; tag/group invalidation; versioned keys.

No single order is correct by itself (`rules/backend/caching.md` owns the choice): evicting after commit leaves stale data if the process crashes between the two, or if a concurrent reader refills a value it read before the commit; evicting before the mutation lets a concurrent reader refill the old value before the commit, while a rollback only costs a miss. Bound these windows with a lifetime, versioned keys, or a retried invalidation, and document the staleness you accept.

## Output caching

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

For Controllers, apply the selected policy through controller/action metadata. Authenticated or user-specific responses are cached only when the key and policy isolate users and authorization context.

## Mutations and failures

Application Services keep their normal repository/Unit of Work flow (`rules/backend/architecture.md` § Unit of Work) and coordinate invalidation through an abstraction when it is part of the use-case semantics. Decide explicitly whether a cache failure falls back to the source, fails the request or returns stale data.

## Testing

Test cache behavior that affects observable correctness: stale entries invalidated after a successful mutation, tenant/user key isolation, cache-miss fallback, the intended outage policy. Framework cache internals need no tests.

## Common mistakes

Caching by default without a reason; global keys for tenant/user data; indefinitely cached mutable data; cache technology in Domain; Application depending directly on `HybridCache` without a deliberate decision; caching EF tracked entities across Unit of Work boundaries; cache as authoritative persistence; Redis added merely because caching exists.

## Decision guide

| Need | Consideration |
|---|---|
| Entire reusable HTTP response | ASP.NET Core output caching |
| Local application cache | In-memory or HybridCache |
| Multi-instance shared cache | Distributed cache / HybridCache L2 (Reserved) |
| Expensive repeated remote read | Cache in Infrastructure when the contract permits |
| Application-controlled invalidation | Application abstraction + Infrastructure implementation |
| Unknown performance problem | Measure first |
