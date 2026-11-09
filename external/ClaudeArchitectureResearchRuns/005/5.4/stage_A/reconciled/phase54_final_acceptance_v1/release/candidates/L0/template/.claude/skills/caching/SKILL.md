---
name: caching
description: >
  Use when adding or reviewing caching: output caching, in-memory, distributed,
  HybridCache, cache keys, expiration, invalidation after mutations, cache tests.
---

> Level: 2 Technology · Owns: caching technique and examples (knowledge) · Scope: backend · Loads: on invocation · Depends on: .claude/rules/0-core/runtime-principles.md, .claude/rules/1-architecture/backend-layers.md

# Caching

Policy owners: when caching is justified, key uniqueness, invalidation consistency, mandatory lifetime → `.claude/rules/0-core/runtime-principles.md` → Caching; cache technology out of Domain and Application → `1-architecture/backend-layers.md`; distributed cache as new infrastructure → Reserved (CLAUDE.md). Define consistency semantics — how stale data may become and how it is invalidated — before choosing a technology. This skill is technique only.

## Choosing the layer

- **HTTP response caching** — ASP.NET Core output caching when the entire response can safely be reused; it belongs in Api.
- **Application/data caching** — when a use case genuinely needs cache-aware behavior, define an abstraction in Application and implement it in Infrastructure; skip the abstraction when caching can stay an Infrastructure detail.
- **Infrastructure caching** — adapters may cache expensive remote or persistence operations when the contract to Application is preserved.

## HybridCache

A strong option for local in-memory caching with optional distributed L2, stampede protection, and cache-aside behavior; not mandatory for every project. Add a distributed backend such as Redis only when deployment requires it.

```csharp
public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration configuration)
{
    services.AddHybridCache();
    return services;
}
```

## Application-coordinated invalidation

```csharp
public interface IProductCache
{
    Task<ProductSummary?> GetAsync(Guid id, CancellationToken cancellationToken);
    Task SetAsync(ProductSummary product, CancellationToken cancellationToken);
    Task RemoveAsync(Guid id, CancellationToken cancellationToken);
}
```

Infrastructure may implement it with `HybridCache`, which stays behind the abstraction (`backend-layers.md`). Mutations still follow the normal repository/Unit of Work flow; remove or update the affected entry after the commit succeeded.

## Keys

Include every dimension that affects the result: entity identifier, tenant, user when genuinely user-specific, locale, relevant query/filter parameters. Centralize key construction when duplicated formats become hard to maintain.

## Expiration and invalidation

Choose expiration from data semantics: change frequency, regeneration cost, acceptable staleness, memory footprint, behavior when the source is unavailable. Invalidation strategies: remove the affected key after a successful mutation; short TTL with tolerated staleness; tag/group invalidation; versioned keys.

No single order is correct by itself (`.claude/rules/0-core/runtime-principles.md` → Caching owns the choice): evicting after commit leaves stale data if the process crashes between the two, or if a concurrent reader refills a value it read before the commit; evicting before the mutation lets a concurrent reader refill the old value before the commit, while a rollback only costs a miss. Bound these windows with a lifetime, versioned keys, or a retried invalidation, and document the staleness you accept.

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

Apply the policy through controller/action metadata (`[OutputCache(PolicyName = "ProductById")]`). Do not cache authenticated or user-specific responses unless the key and policy isolate users and authorization context.

## Failure behavior

Decide explicitly whether a cache failure falls back to the source, fails the request, or returns stale data.

## Testing

Test caching when it affects observable correctness: stale entries invalidated after a successful mutation, tenant/user keys isolated, a miss falls back correctly, an outage follows the intended failure policy. Do not unit-test framework cache internals.

## Anti-patterns

Caching EF tracked entities across Unit of Work boundaries; Redis added merely because the application caches.

## Decision guide

| Need | Consideration |
|---|---|
| Entire reusable HTTP response | output caching |
| Local application cache | in-memory or HybridCache |
| Shared cache across instances | distributed cache / HybridCache L2 (Reserved infrastructure) |
| Expensive repeated remote read | cache inside the Infrastructure adapter |
| Application-controlled invalidation | Application abstraction + Infrastructure implementation |
