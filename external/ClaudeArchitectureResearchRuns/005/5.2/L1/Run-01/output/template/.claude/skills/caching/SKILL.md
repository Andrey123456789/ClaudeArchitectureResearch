---
name: caching
description: >
  Use for caching: HybridCache, IMemoryCache, distributed cache, output caching,
  cache keys, expiration, invalidation after mutations, failure behavior.
---
> Level: 2-technology | Owns: caching technique | Scope: backend | Loads: on demand (skill)

# Caching

Policy: `performance.md` (need, lifetime, keys, invalidation),
`role-boundaries.md` (cache technology stays out of the domain model and
use-case units without a deliberate abstraction). Adding a distributed cache is
a Reserved infrastructure decision.

## Choosing the cache layer

- **HTTP response caching** — ASP.NET Core output caching when the entire
  response can safely be reused; configured at the entry point/host.
- **Use-case-controlled caching** — when a use case genuinely needs cache-aware
  behavior (explicit invalidation), define a contract on the use-case side and
  implement it in an adapter. Skip the abstraction when caching can stay an
  internal adapter concern.
- **Adapter caching** — adapters may cache expensive remote or persistence
  operations when the contract exposed to use-case units is preserved.

## HybridCache

A strong option for local in-memory caching with optional distributed L2,
stampede protection, and cache-aside behavior — not mandatory.

```csharp
services.AddHybridCache();
```

Add a distributed backend such as Redis only when deployment requirements
justify it (multiple instances needing shared state).

## Contract example

```csharp
public interface IProductCache
{
    Task<ProductSummary?> GetAsync(Guid id, CancellationToken cancellationToken);
    Task SetAsync(ProductSummary product, CancellationToken cancellationToken);
    Task RemoveAsync(Guid id, CancellationToken cancellationToken);
}
```

The adapter may implement it with `HybridCache`; never expose `HybridCache`
itself through use-case contracts.

## Keys

Include every dimension that affects the result — entity identifier, tenant,
user when genuinely user-specific, locale, relevant query/filter parameters.
Centralize key construction when duplicated formats become hard to maintain.

## Expiration

Choose expiration from data semantics: change frequency, regeneration cost,
acceptable staleness, memory footprint, behavior while the source is
unavailable — not an arbitrary universal default.

## Invalidation

Typical strategies: remove the affected key after a successful mutation; a
short TTL with tolerated staleness; tag/group invalidation; versioned keys.
Invalidate before the mutation succeeded only when the workflow deliberately
accepts it. Mutations keep their normal persistence-access/commit workflow; do
not bypass it to make invalidation convenient.

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

Apply the policy to Controllers through action metadata
(`[OutputCache(PolicyName = "ProductById")]`). Do not cache authenticated or
user-specific responses unless the key and policy isolate users and
authorization context.

## Failure behavior

Decide whether a cache failure falls back to the source, fails the request, or
returns stale data.

## Testing

Test cache behavior when it affects correctness: invalidation after a
successful mutation, tenant/user key isolation, miss fallback, the intended
outage policy. Do not unit-test framework cache internals.

## Anti-patterns

Caching without a demonstrated reason; global keys for tenant/user data;
indefinitely cached mutable data; cache technology in the domain model;
use-case code depending directly on `HybridCache`; caching tracked persistence
entities across units of work; cache as authoritative storage; Redis merely
because caching exists.

## Decision guide

| Need | Default consideration |
|---|---|
| Entire reusable HTTP response | Output caching |
| Local application cache | In-memory or HybridCache |
| Multi-instance shared cache | Distributed cache / HybridCache L2 (Reserved) |
| Expensive repeated remote read | Cache in the adapter when the contract permits |
| Use-case-controlled invalidation | Use-case contract + adapter implementation |
| Unknown performance problem | Measure first |
