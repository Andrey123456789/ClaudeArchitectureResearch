---
name: caching
description: >
  Use when adding or reviewing caching: output caching, HybridCache, in-memory
  or distributed cache, key design, expiration, invalidation after mutations,
  cache failure behavior.
---

> Level: 2 Technology · Owns: caching technique · Scope: backend · Loads: on demand (knowledge skill)

# Caching

Policy owners: `.claude/rules/0-core/runtime-principles.md` (need, lifetime, keys, invalidation), `.claude/rules/1-architecture/backend-layers.md` (cache technology stays out of Domain and Application). Distributed caching is a Reserved infrastructure category (decision control). Define consistency semantics — tolerated staleness and invalidation — before writing code, and measure before caching for performance.

## Choosing the layer

| Need | Typical choice | Where |
|---|---|---|
| Whole HTTP response reusable | ASP.NET Core output caching | Api |
| Expensive repeated remote or persistence read | Cache inside the Infrastructure adapter when the contract permits | Infrastructure |
| Use case must coordinate invalidation | Application abstraction implemented in Infrastructure | Application + Infrastructure |
| Local cache with stampede protection, optional L2 | `HybridCache` | Infrastructure |
| Shared cache across instances | Distributed cache / `HybridCache` L2 (approval required) | Infrastructure |

Do not create an Application cache abstraction when caching can stay an Infrastructure detail.

## HybridCache

```csharp
services.AddHybridCache();                         // in AddInfrastructure

var summary = await cache.GetOrCreateAsync(
    $"product:{tenantId}:{id}",
    async ct => await LoadSummaryAsync(id, ct),
    new HybridCacheEntryOptions { Expiration = TimeSpan.FromMinutes(5) },
    cancellationToken: cancellationToken);
```

Add a Redis (or other) L2 backend only when deployment requirements justify it.

## Application-coordinated invalidation

```csharp
public interface IProductCache                     // Application
{
    Task<ProductSummary?> GetAsync(Guid id, CancellationToken cancellationToken);
    Task SetAsync(ProductSummary product, CancellationToken cancellationToken);
    Task RemoveAsync(Guid id, CancellationToken cancellationToken);
}
```

Infrastructure implements it (for example with `HybridCache`), which keeps the cache technology behind the Application abstraction (`backend-layers.md`). Application Services keep their normal repository/unit-of-work flow and remove or refresh entries after the commit succeeds — never bypass repositories to make invalidation convenient.

## Keys

Include every dimension that changes the result: entity id, tenant, user when genuinely user-specific, locale, relevant query/filter parameters. Centralize key construction once formats repeat (`ProductCacheKeys.Summary(tenantId, id)`).

## Expiration

Derive lifetimes from data semantics: change frequency, regeneration cost, acceptable staleness, memory footprint, behavior when the source is unavailable. Avoid unbounded entries.

## Invalidation strategies

Remove the affected key after a successful mutation; short TTL with tolerated staleness; tag/group invalidation (`HybridCache.RemoveByTagAsync`); versioned keys.

## Output caching

```csharp
builder.Services.AddOutputCache(options =>
    options.AddPolicy("ProductById", policy => policy
        .Expire(TimeSpan.FromMinutes(5))
        .SetVaryByRouteValue("id")));

app.UseOutputCache();

[OutputCache(PolicyName = "ProductById")]
[HttpGet("{id:guid}")]
public async Task<ActionResult<ProductResponse>> GetById(Guid id, CancellationToken ct) { ... }
```

Authenticated or user-specific responses are cached only when the key and policy isolate users and authorization context.

## Failure behavior

Decide explicitly whether a cache failure falls back to the source, fails the request, or serves stale data.

## Testing

Test cache behavior that affects observable correctness: invalidation after successful mutation, tenant/user key isolation, miss fallback, outage behavior. Do not unit-test framework cache internals.

## Review cues

Caching added without a reason, global keys for tenant/user data, mutable data cached without invalidation, cache types in Domain, `HybridCache` in Application contracts without a decision, EF tracked entities cached across unit-of-work boundaries, cache used as authoritative storage, Redis added merely because caching exists.
