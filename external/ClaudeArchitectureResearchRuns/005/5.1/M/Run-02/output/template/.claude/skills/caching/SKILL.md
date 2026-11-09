---
name: caching
description: >
  Use when adding or reviewing caching: HybridCache, IMemoryCache, distributed
  cache or Redis, output caching, cache keys, expiration, invalidation after
  mutations, cache failure behavior, cache tests.
---

> Owner: caching technique and examples (normative policy lives in rules) | Scope: backend | Loads: on demand — knowledge | Enforced: none

# Caching

Policy: `.claude/rules/performance.md` § Caching (need, keys, lifetime,
invalidation) and `.claude/rules/architecture.md` § Application (cache
technology boundary). A distributed cache is a new infrastructure category and
therefore a Reserved decision (`CLAUDE.md` § Decision Control).

Define the consistency semantics first — how stale data may become and how it is
invalidated — and measure before adding a cache purely for performance.

## Choosing the Cache Layer

- **HTTP response caching** — ASP.NET Core output caching when the whole response
  can safely be reused; lives in the API layer.
- **Application/data caching** — when a use case genuinely needs cache-aware
  behavior, define an abstraction in Application and implement it in
  Infrastructure. If caching can stay an internal Infrastructure concern, no
  Application abstraction is needed.
- **Infrastructure caching** — adapters may cache expensive remote or
  persistence operations when the contract exposed to Application is preserved.

## HybridCache

A strong option when the application benefits from local in-memory caching,
optional distributed L2 caching, stampede protection, and common cache-aside
behavior; not mandatory for every project.

```csharp
public static IServiceCollection AddInfrastructure(
    this IServiceCollection services,
    IConfiguration configuration)
{
    services.AddHybridCache();

    return services;
}
```

```csharp
var summary = await cache.GetOrCreateAsync(
    $"product:{tenantId}:{productId}",
    async ct => await LoadSummaryAsync(productId, ct),
    new HybridCacheEntryOptions { Expiration = TimeSpan.FromMinutes(5) },
    cancellationToken: cancellationToken);
```

Add a distributed backend such as Redis only when deployment requirements
justify it.

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

Infrastructure may implement it with `HybridCache`; the Application contract
does not expose `HybridCache` itself.

## Cache Keys

Include every dimension that affects the result: entity identifier, tenant, user
when genuinely user-specific, locale, relevant query and filter parameters.
Centralize key construction once duplicated key formats become hard to maintain.

## Expiration

Choose expiration from data semantics rather than a universal default: how often
the data changes, regeneration cost, acceptable staleness, memory footprint, and
behavior when the source is unavailable.

## Invalidation Strategies

- remove the affected key after a successful mutation;
- a short TTL with tolerated staleness;
- tag/group invalidation;
- versioned keys.

Invalidate before the mutation is known to have succeeded only when the workflow
deliberately accepts that behavior.

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

```csharp
[HttpGet("{id:guid}")]
[OutputCache(PolicyName = "ProductById")]
public async Task<ActionResult<ProductResponse>> GetById(Guid id, CancellationToken cancellationToken)
```

Do not cache authenticated or user-specific responses unless the key and policy
isolate users and authorization context correctly.

## Mutations

Application Services keep their normal repository/Unit of Work workflow; when
invalidation is part of the use-case semantics, coordinate it through an
appropriate abstraction rather than bypassing repositories or `IUnitOfWork`.

## Failure Behavior

Decide whether a cache failure should fall back to the source, fail the request,
or return stale data, and make that choice explicit.

## Testing

Test caching when it affects observable correctness: stale entries invalidated
after a successful mutation, tenant/user key isolation, correct fallback on a
miss, the intended policy during a cache outage. Do not unit-test the framework's
cache implementation.

## Common Mistakes

- indefinitely cached mutable data;
- caching EF tracked entities across Unit of Work boundaries;
- adding Redis merely because the application has caching.

## Decision Guide

| Need | Consider |
|---|---|
| Entire reusable HTTP response | ASP.NET Core output caching |
| Local application cache | In-memory or HybridCache |
| Multi-instance shared cache | Distributed cache / HybridCache L2 (Reserved) |
| Expensive repeated remote read | Cache in Infrastructure when the contract permits |
| Application-controlled invalidation | Application abstraction + Infrastructure implementation |
| Unknown performance problem | Measure before caching |
