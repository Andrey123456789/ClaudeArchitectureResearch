---
name: caching
description: >
  Use for caching: HybridCache, memory/distributed caches, output caching, key design, expiration, invalidation, cache tests.
---

> Level: 2 Technology | Owns: .NET caching technique | Scope: backend | Loads: knowledge skill (on demand) | Depends on: 0-core/caching-principles.md, 1-architecture/backend-layers.md

# Caching Technique

Policy owners (routing): need, keys, invalidation, expiration →
`0-core/caching-principles.md`; cache technology kept out of Domain and
Application → `1-architecture/backend-layers.md`; distributed caching is
Reserved → `1-architecture/overview.md`.

## Choosing the Layer

| Need | Technique |
|---|---|
| Whole HTTP response reusable | ASP.NET Core output caching (Api layer) |
| Local application cache | `IMemoryCache` or `HybridCache` |
| Multi-instance shared cache | Distributed cache / `HybridCache` L2 (Reserved) |
| Expensive repeated remote read | Cache inside the Infrastructure adapter when the contract allows |
| Application-controlled invalidation | Application abstraction + Infrastructure implementation |
| Unknown performance problem | Measure first |

When caching can stay inside Infrastructure, do not create an Application cache
abstraction.

## HybridCache

```csharp
services.AddHybridCache();   // local cache, optional L2, stampede protection
```

Add a distributed backend such as Redis only when deployment needs it.

## Application Cache Abstraction

```csharp
public interface IProductCache
{
    Task<ProductSummary?> GetAsync(Guid id, CancellationToken cancellationToken);
    Task SetAsync(ProductSummary product, CancellationToken cancellationToken);
    Task RemoveAsync(Guid id, CancellationToken cancellationToken);
}
```

Infrastructure implements it with `HybridCache`, which stays behind the
abstraction.

## Keys and Expiration

Build keys from every dimension that affects the value — entity id, tenant,
user (when user-specific), locale, query/filter parameters — and centralize key
construction when formats repeat. Choose expiration from change frequency,
regeneration cost, tolerated staleness, memory footprint, and behavior when the
source is unavailable.

## Invalidation Strategies

Remove the affected key after a successful mutation, use a short TTL with
tolerated staleness, tag/group invalidation, or versioned keys. Mutations still
follow the normal repository and Unit of Work flow; coordinate required
invalidation through an abstraction, never by bypassing them.

## Output Caching

```csharp
builder.Services.AddOutputCache(options =>
    options.AddPolicy("ProductById", policy => policy
        .Expire(TimeSpan.FromMinutes(5))
        .SetVaryByRouteValue("id")));

app.UseOutputCache();
// Controller action: [OutputCache(PolicyName = "ProductById")]
```

Cache authenticated or user-specific responses only when key and policy isolate
users and authorization context.

## Failure Behavior

Decide per use case whether a cache failure falls back to the source, fails the
request, or serves stale data.

## Testing

Test caching where it affects observable correctness: invalidation after a
successful mutation, tenant/user key isolation, miss fallback, outage behavior.
Do not test framework cache internals.

## Avoid

Caching EF tracked entities across Unit of Work boundaries, and adding Redis
merely because the application caches.
