---
name: caching
description: >
  Use when implementing, reviewing, or troubleshooting caching: choosing output
  caching vs. in-memory vs. HybridCache, designing cache keys and expiration,
  invalidation after mutations, cache abstractions, failure behavior, or cache
  tests.
---

> Owns: caching technique | Scope: backend | Loads: on demand (knowledge skill)

# Caching

Policy owners: when caching is justified, keys, expiration, invalidation →
`.claude/rules/performance.md` (Caching); cache technology placement →
`.claude/rules/architecture.md`. A distributed cache (Redis, HybridCache L2) is
Reserved infrastructure (`CLAUDE.md`). Measure before caching for performance.

## Choosing the Layer

| Need | Technique |
|---|---|
| Entire reusable HTTP response | ASP.NET Core output caching (Api layer) |
| Local application cache | `IMemoryCache` or `HybridCache` |
| Multi-instance shared cache | `HybridCache` with an approved distributed L2 |
| Expensive repeated remote read | Cache inside the Infrastructure adapter when the contract permits |
| Application-controlled invalidation | Application abstraction + Infrastructure implementation |

Keep caching an internal Infrastructure concern unless a use case genuinely needs
cache-aware behavior.

## HybridCache

Offers local caching, optional distributed L2, stampede protection, and
cache-aside behavior. Not mandatory.

```csharp
services.AddHybridCache();

public async Task<ProductSummary?> GetAsync(Guid id, CancellationToken ct) =>
    await cache.GetOrCreateAsync(
        $"product:{id}",
        async token => await repository.GetSummaryAsync(id, token),
        new HybridCacheEntryOptions { Expiration = TimeSpan.FromMinutes(5) },
        cancellationToken: ct);
```

## Application Abstraction Example

```csharp
public interface IProductCache
{
    Task<ProductSummary?> GetAsync(Guid id, CancellationToken cancellationToken);
    Task SetAsync(ProductSummary product, CancellationToken cancellationToken);
    Task RemoveAsync(Guid id, CancellationToken cancellationToken);
}
```

Infrastructure implements it (for example with `HybridCache`), keeping the cache
technology behind the abstraction (boundary: `architecture.md`).

## Keys

Required key dimensions: `performance.md` (Caching). Centralize key construction
once formats repeat:

```csharp
internal static class CacheKeys
{
    public static string Product(Guid tenantId, Guid id, string culture) =>
        $"product:{tenantId}:{id}:{culture}";
}
```

## Expiration and Invalidation

Choose expiration from change frequency, regeneration cost, acceptable
staleness, memory footprint, and behavior when the source is down — not from a
universal default. Invalidation options: remove affected keys after a successful
mutation, short TTL with tolerated staleness, tag/group invalidation, versioned
keys. Application Services keep their normal repository/UoW workflow and
coordinate invalidation through the abstraction after commit.

## Output Caching

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

For authenticated or user-specific responses, either vary the policy by the
user/authorization context (custom `IOutputCachePolicy`, `SetVaryByHeader`) so
the key rules in `performance.md` hold, or leave those responses uncached.

## Failure Behavior

Decide explicitly whether a cache failure falls back to the source, fails the
request, or serves stale data.

## Testing

Test cache behavior that affects observable correctness: invalidation after
successful mutation, tenant/user key isolation, miss fallback, outage policy.
Do not unit-test framework cache internals.

## Pitfalls

Caching EF tracked entities across Unit of Work boundaries; adding Redis merely
because the application caches; bypassing repositories/`IUnitOfWork` to make
invalidation convenient.
