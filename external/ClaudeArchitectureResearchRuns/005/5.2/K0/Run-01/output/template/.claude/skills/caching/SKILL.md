---
name: caching
description: Use when implementing, reviewing or troubleshooting application or HTTP caching — HybridCache, in-memory and distributed caches, output caching, cache abstractions, key design, expiration, invalidation, failure behavior, cache tests.
---
<!-- Kind: KNW | Scope: backend | Owns: caching technique and examples | Loads: on demand (model-invoked) -->
# Caching

Standards: `rules/backend/caching.md` (need, keys, expiration, invalidation) and `rules/backend/architecture.md` § Boundary Leaks (cache technology placement). Define consistency semantics first — how stale data may become and how it is invalidated — and measure before adding a cache solely for performance.

## Choosing the Cache Layer

### HTTP Response Caching

ASP.NET Core output caching, in the Api layer, when the entire HTTP response can safely be reused.

### Application/Data Caching

When an Application use case genuinely needs cache-aware behavior, define an appropriate abstraction in Application and implement it in Infrastructure. Skip the Application-level abstraction when caching can stay an internal Infrastructure concern.

### Infrastructure Caching

Infrastructure adapters may cache expensive remote or persistence operations when the contract exposed to Application is preserved.

## HybridCache

A strong option when the application benefits from local in-memory caching, an optional distributed L2, stampede protection and common cache-aside behavior — not mandatory for every project.

```csharp
public static IServiceCollection AddInfrastructure(
    this IServiceCollection services,
    IConfiguration configuration)
{
    services.AddHybridCache();

    return services;
}
```

A distributed backend such as Redis comes only with a deployment requirement (distributed cache adoption: CLAUDE.md § Decisions).

## Cache Abstraction Example

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

Infrastructure may implement it with `HybridCache`; the Application contract does not expose `HybridCache` itself.

## Cache Keys

Centralize key construction when duplicated key formats become hard to maintain; a single key builder per cached concept keeps the required dimensions (`rules/backend/caching.md`) from drifting between call sites.

## Expiration

Choose expiration from data semantics rather than arbitrary universal defaults — change frequency, regeneration cost, acceptable staleness, memory footprint, behavior when the source is unavailable.

## Invalidation

Typical strategies: remove the affected key after a successful mutation; short TTL with tolerated staleness; tag/group invalidation; versioned keys.

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

For Controllers, apply the selected output-cache policy through controller/action metadata. Avoid caching authenticated or user-specific responses unless the key and policy isolate users and authorization context.

## Mutations

Application Services keep their normal repository/Unit of Work workflow; when invalidation is part of the use-case semantics, coordinate it through an appropriate abstraction rather than bypassing repositories or `IUnitOfWork` for convenience.

## Failure Behavior

Decide whether a cache failure falls back to the source, fails the request, or returns stale data.

## Testing

Test cache behavior when it affects observable correctness: stale entries invalidated after a successful mutation, tenant/user key isolation, cache-miss fallback, cache-outage behavior per the intended failure policy. Framework cache implementations need no unit tests.

## Anti-Patterns

Avoid caching by default without a demonstrated reason, global keys for tenant- or user-specific data, indefinitely cached mutable data, cache technology in Domain, Application depending directly on `HybridCache` without a deliberate decision, caching EF tracked entities across Unit of Work boundaries, the cache as authoritative persistence, and adding Redis merely because the application caches.

## Decision Guide

| Need | Default consideration |
|---|---|
| Entire reusable HTTP response | ASP.NET Core output caching |
| Local application cache | In-memory or HybridCache |
| Multi-instance shared cache | Distributed cache / HybridCache L2 |
| Expensive repeated remote read | Cache in Infrastructure when the contract permits |
| Application-controlled invalidation | Application abstraction + Infrastructure implementation |
| Unknown performance problem | Measure before adding caching |
