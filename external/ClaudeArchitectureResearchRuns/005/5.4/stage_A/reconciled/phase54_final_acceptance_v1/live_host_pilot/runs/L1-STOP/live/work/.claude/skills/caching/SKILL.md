---
name: caching
description: .NET caching technique. Use when implementing, reviewing, or troubleshooting caching — HybridCache, IMemoryCache, distributed cache/Redis, output caching, cache keys, expiration, invalidation, stampede protection, cache failure behavior, cache tests.
---

> Level: 2-technology · Owns: caching technique · Loading: on demand

# Caching

Rules: caching need, keys, lifetime, and invalidation (`.claude/rules/0-core/backend-code.md` § Caching); cache technology stays out of the domain model and behind deliberate abstractions (`.claude/rules/1-architecture/roles.md`); a distributed cache is a Reserved infrastructure category. Define consistency first: how stale may data become, and how is it invalidated?

## Choosing the layer

- **HTTP response caching** — ASP.NET Core output caching when the whole response is safely reusable; lives at the entry point.
- **Use-case caching** — when a use case genuinely needs cache-aware behavior, define an abstraction in the use-case layer and implement it in the implementation layer. Skip the abstraction when caching can stay internal to an adapter.
- **Adapter caching** — an implementation-layer adapter may cache expensive remote or persistence calls when the contract it exposes stays intact.

## HybridCache

Strong option for local in-memory caching with optional distributed L2, stampede protection, and cache-aside; not mandatory.

```csharp
public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration configuration)
{
    services.AddHybridCache();
    return services;
}
```

Add a distributed backend such as Redis only when deployment requirements justify it.

## Use-case cache abstraction

```csharp
public interface IProductCache
{
    Task<ProductSummary?> GetAsync(Guid id, CancellationToken cancellationToken);
    Task SetAsync(ProductSummary product, CancellationToken cancellationToken);
    Task RemoveAsync(Guid id, CancellationToken cancellationToken);
}
```

The implementation may use `HybridCache`; never expose `HybridCache` itself from use-case contracts.

## Keys, expiration, invalidation

- Key dimensions: entity id, tenant, user (when genuinely user-specific), locale, relevant query/filter parameters. Centralize key construction once formats repeat.
- Expiration from data semantics: change frequency, regeneration cost, acceptable staleness, memory footprint, behavior when the source is unavailable — not a universal default.
- Invalidation strategies: remove affected keys after a successful mutation, short TTL with tolerated staleness, tag/group invalidation, versioned keys.
- No single order is correct by itself (`.claude/rules/0-core/backend-code.md` § Caching owns the choice): evicting after commit leaves stale data if the process crashes between the two, or if a concurrent reader refills a value it read before the commit; evicting before the mutation lets a concurrent reader refill the old value before the commit, while a rollback only costs a miss. Bound these windows with a lifetime, versioned keys, or a retried invalidation, and document the staleness you accept.

## Output caching

```csharp
builder.Services.AddOutputCache(options =>
    options.AddPolicy("ProductById", policy => policy.Expire(TimeSpan.FromMinutes(5)).SetVaryByRouteValue("id")));

app.UseOutputCache();
```

Apply the policy through controller/action metadata. Cache authenticated or user-specific responses only when the key and policy isolate users and authorization context.

## Mutations and failures

Use cases keep their normal repository/commit-boundary flow; coordinate invalidation through an abstraction when it is part of the use-case semantics instead of bypassing repositories. Decide whether a cache failure falls back to the source, fails the request, or serves stale data.

## Testing

Test caching where it affects observable correctness: invalidation after successful mutation, tenant/user key isolation, correct miss fallback, intended outage behavior. Do not unit-test framework cache internals.

## Anti-patterns

Caching by default; global keys for tenant/user data; mutable data cached indefinitely; cache technology in the domain model; use-case code depending on `HybridCache` without a deliberate decision; caching tracked ORM entities across commit boundaries; cache as authoritative persistence; Redis merely because caching exists.

## Decision guide

| Need | Consider |
| --- | --- |
| Entire reusable HTTP response | output caching |
| Local application cache | in-memory or HybridCache |
| Multi-instance shared cache | distributed cache / HybridCache L2 (Reserved) |
| Expensive repeated remote read | cache inside the adapter |
| Use-case-controlled invalidation | use-case abstraction + adapter implementation |
| Unknown performance problem | measure first |
