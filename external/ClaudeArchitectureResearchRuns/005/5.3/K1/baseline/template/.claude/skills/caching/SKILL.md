---
name: caching
description: >
  Use when adding or reviewing caching: HybridCache, IMemoryCache, distributed
  cache, output caching, cache keys, expiration, invalidation after writes,
  stale data, cache failure behavior.
---

> Kind: KNW | Scope: backend | Capability: — | Loading: on-demand knowledge

# Caching

Policy: `.claude/rules/backend/runtime.md` (need, keys, lifetimes, invalidation), `.claude/rules/backend/architecture.md` (cache technology boundaries). Adding a distributed cache is a Reserved infrastructure decision (`CLAUDE.md`). Clear reasons to cache: measured expensive repeated work, high read volume, expensive remote calls — with acceptable staleness semantics; a value being read frequently is not by itself a reason. Define consistency semantics — acceptable staleness and invalidation — before writing cache code, and measure before caching solely for performance.

## Choosing the layer

- **HTTP response caching** — ASP.NET Core output caching when the entire response can safely be reused; lives in the Api layer.
- **Application/data caching** — when a use case genuinely needs cache-aware behavior, define an Application abstraction and implement it in Infrastructure; do not introduce one if caching can stay an internal Infrastructure concern.
- **Infrastructure caching** — adapters may cache expensive remote or persistence operations when the contract exposed to Application is preserved.

## HybridCache

A strong option for local in-memory caching with optional distributed L2, stampede protection, and cache-aside behavior; not mandatory. Add a distributed backend such as Redis only when deployment requirements justify it.

```csharp
public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration configuration)
{
    services.AddHybridCache();
    return services;
}
```

## Application cache abstraction

When Application coordinates invalidation explicitly, expose a narrow contract and keep `HybridCache` itself out of Application contracts:

```csharp
public interface IProductCache
{
    Task<ProductSummary?> GetAsync(Guid id, CancellationToken cancellationToken);
    Task SetAsync(ProductSummary product, CancellationToken cancellationToken);
    Task RemoveAsync(Guid id, CancellationToken cancellationToken);
}
```

## Keys

Include every dimension that affects the result: entity identifier, tenant, user when genuinely user-specific, locale, relevant query/filter parameters. Centralize key construction once duplicated key formats become hard to maintain.

## Expiration

Choose expiration from data semantics, not universal defaults: change frequency, regeneration cost, acceptable staleness, memory footprint, behavior when the source is unavailable. Avoid unbounded entries.

## Invalidation strategies

Remove the affected key after a successful mutation; short TTL with tolerated staleness; tag/group invalidation; versioned keys. Invalidate before the mutation succeeds only when the workflow deliberately accepts that behavior.

## Output caching

```csharp
builder.Services.AddOutputCache(options =>
{
    options.AddPolicy("ProductById", policy => policy.Expire(TimeSpan.FromMinutes(5)).SetVaryByRouteValue("id"));
});

app.UseOutputCache();
```

Apply the policy through controller/action metadata. Never cache authenticated or user-specific responses unless the key and policy isolate users and authorization context.

## Mutations and failures

Application Services keep their normal repository/Unit of Work workflow; coordinate required invalidation through an abstraction instead of bypassing repositories or `IUnitOfWork`. Decide whether a cache failure falls back to the source, fails the request, or returns stale data. Never cache tracked persistence entities across Unit of Work boundaries.

## Testing

Test caching when it affects observable correctness: stale entries invalidated after successful mutation, tenant/user key isolation, cache-miss fallback, outage behavior per the intended failure policy. Do not unit-test framework cache internals.

## Decision guide

| Need | Default consideration |
|---|---|
| Entire reusable HTTP response | Output caching |
| Local application cache | In-memory or HybridCache |
| Multi-instance shared cache | Distributed cache / HybridCache L2 (Reserved decision) |
| Expensive repeated remote read | Cache in Infrastructure when the contract permits |
| Application-controlled invalidation | Application abstraction + Infrastructure implementation |
| Unknown performance problem | Measure before caching |
