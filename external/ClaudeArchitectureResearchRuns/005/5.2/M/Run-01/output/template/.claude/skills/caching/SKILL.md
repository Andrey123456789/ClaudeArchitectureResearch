---
name: caching
description: >
  Use for caching: HybridCache, in-memory or distributed caches, output
  caching, cache keys, expiration, invalidation after mutations, cache tests.
---

> Knowledge skill. Owns: caching technique and examples · Scope: backend · Loads: on demand · Depends on: CLAUDE.md, .claude/rules/performance.md, .claude/rules/architecture.md

# Caching

Rules: `performance.md` (when to cache, keys, lifetimes, invalidation
consistency) and `architecture.md` (cache technology stays out of Domain and
behind a deliberate abstraction in Application). A distributed cache is a new
infrastructure category (CLAUDE.md, Decision Control). Define the consistency
semantics — how stale data may become and how it is invalidated — before
choosing an implementation, and measure before caching for performance alone.

## Choosing the Cache Layer

- **HTTP response caching** — ASP.NET Core output caching when the entire HTTP
  response can safely be reused; belongs in the Api layer.
- **Application/data caching** — when a use case genuinely needs cache-aware
  behavior, define an abstraction in Application and implement it in
  Infrastructure. Skip the abstraction when caching can stay an internal
  Infrastructure concern.
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

A distributed backend such as Redis is added only when deployment requirements
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

Infrastructure may implement it with `HybridCache`; `HybridCache` itself does
not appear in Application contracts.

## Key Construction

Centralize key construction once duplicated key formats become hard to
maintain, and include every dimension that affects the value (identifier,
tenant, user when user-specific, locale, relevant query/filter parameters).

## Expiration

Choose expiration from data semantics rather than a universal default: change
frequency, regeneration cost, acceptable staleness, memory footprint, behavior
when the source is unavailable.

## Invalidation Strategies

- remove the affected key after a successful mutation;
- a short TTL with tolerated staleness;
- tag/group invalidation;
- versioned keys.

Invalidating before the mutation is known to have succeeded is acceptable only
when the workflow deliberately accepts that behavior.

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

For Controllers, apply the selected output-cache policy through controller or
action metadata. Cache authenticated or user-specific responses only when the
key and policy correctly isolate users and authorization context.

## Mutations

Application Services perform their usual repository and Unit of Work
workflow; when invalidation is part of the use-case semantics, coordinate it
through an abstraction instead of bypassing repositories or `IUnitOfWork`.

## Failure Behavior

Decide whether a cache failure falls back to the source, fails the request, or
returns stale data.

## Testing

Test cache behavior when it affects observable correctness: stale entries are
invalidated after a successful mutation, tenant/user keys are isolated, a miss
falls back correctly, an outage follows the intended failure policy. Do not
unit-test framework cache internals.

## Anti-Patterns

- caching by default without a demonstrated reason;
- indefinitely cached mutable data without an invalidation strategy;
- caching EF-tracked entities across Unit of Work boundaries;
- using the cache as authoritative persistence;
- adding Redis merely because the application has caching.

## Decision Guide

| Need | Default consideration |
|---|---|
| Entire reusable HTTP response | ASP.NET Core output caching |
| Local application cache | In-memory or HybridCache |
| Multi-instance shared cache | Distributed cache / HybridCache L2 (Reserved) |
| Expensive repeated remote read | Cache in Infrastructure when the contract permits |
| Application-controlled invalidation | Application abstraction + Infrastructure implementation |
| Unknown performance problem | Measure before adding caching |
