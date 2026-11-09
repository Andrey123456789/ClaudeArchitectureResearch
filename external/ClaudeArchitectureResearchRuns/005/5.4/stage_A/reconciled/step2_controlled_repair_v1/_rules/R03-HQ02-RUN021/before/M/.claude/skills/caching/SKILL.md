---
name: caching
description: >
  Use when adding or reviewing caching: HybridCache, in-memory or distributed
  caches, output caching, cache keys, expiration, invalidation after mutations,
  cache failure behavior and tests.
---

> Owns: caching technique and examples (no policy) | Scope: backend | Loads: on demand (knowledge skill)

# Caching

Policy owners: when to cache, key, invalidation, and expiration rules —
`.claude/rules/performance.md` § Caching; cache technology at boundaries —
`.claude/rules/architecture.md` § Boundary Contracts; distributed caching as a
new infrastructure category — CLAUDE.md § Decision Control.

Define consistency semantics first: know how stale data may become and how it is
invalidated. Measure before adding caching solely for performance.

## Choosing the Cache Layer

- **HTTP response caching** — ASP.NET Core output caching, in the API layer, when
  the entire response can safely be reused.
- **Application/data caching** — when a use case genuinely needs cache-aware
  behavior, define an abstraction in Application and implement it in
  Infrastructure. Do not introduce an application-level cache abstraction if
  caching can stay an internal Infrastructure concern.
- **Infrastructure caching** — adapters may cache expensive remote or
  persistence operations when that preserves the contract exposed to
  Application.

## HybridCache

`HybridCache` is a strong option for local in-memory caching, optional
distributed L2 caching, stampede protection, and common cache-aside behavior. It
is not mandatory.

```csharp
public static IServiceCollection AddInfrastructure(
    this IServiceCollection services,
    IConfiguration configuration)
{
    services.AddHybridCache();

    return services;
}
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

Infrastructure may implement this contract with `HybridCache`; `HybridCache`
itself does not appear in Application contracts.

## Cache Keys

Dimensions that commonly affect the result: entity identifier, tenant, user when
genuinely user-specific, locale, relevant query/filter parameters. Centralize key
construction when duplicated key formats become hard to maintain.

## Expiration

Choose expiration from data semantics rather than a universal default: how often
the data changes, regeneration cost, acceptable staleness, memory footprint, and
failure behavior when the source is unavailable.

## Invalidation Strategies

Remove the affected key after a successful mutation; short TTL with tolerated
staleness; tag/group invalidation; versioned keys. Invalidating before the
underlying mutation is known to have succeeded is acceptable only when the
workflow deliberately accepts that behavior.

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
action metadata. Do not cache authenticated or user-specific responses unless
the key and policy correctly isolate users and authorization context.

## Mutations

Application Services perform their normal repository/Unit of Work workflow; if
invalidation is part of the use-case semantics, coordinate it through an
appropriate abstraction. Do not bypass repositories or `IUnitOfWork` to make
invalidation convenient.

## Failure Behavior

Decide whether a cache failure falls back to the source, fails the request, or
returns stale data.

## Testing

Test cache behavior when it affects observable correctness: stale entries are
invalidated after a successful mutation; tenant/user keys are isolated; a miss
falls back correctly; an outage follows the intended failure policy. Do not
unit-test framework cache internals.

## Anti-Patterns

Avoid caching EF tracked entities across Unit of Work boundaries, using a cache
as authoritative persistence, and adding Redis merely because the application
has caching.

## Decision Guide

| Need | Default consideration |
|---|---|
| Entire reusable HTTP response | ASP.NET Core output caching |
| Local application cache | In-memory or HybridCache |
| Multi-instance shared cache | Distributed cache / HybridCache L2 (Reserved: new infrastructure) |
| Expensive repeated remote read | Cache in Infrastructure when the contract permits |
| Application-controlled invalidation | Application abstraction + Infrastructure implementation |
| Unknown performance problem | Measure before adding caching |
