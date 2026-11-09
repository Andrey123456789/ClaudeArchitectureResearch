---
name: ef-core
description: >
  Use when writing or reviewing EF Core code in Infrastructure: DbContext and
  entity configuration, repository and Unit of Work implementations, LINQ
  queries, tracking, projections, pagination, bulk operations, transactions,
  interceptors, migrations commands, and the Development seeder implementation.
---

> Owns: EF Core implementation technique and examples | Scope: backend | Loads: on demand (knowledge skill)

# Entity Framework Core

Policy owners: repository/UoW/EF boundary → `.claude/rules/architecture.md`;
seeding and migrations → `.claude/rules/persistence.md`; query efficiency and
measured optimizations → `.claude/rules/performance.md`; SQL parameterization →
`.claude/rules/security.md`. This skill shows how.

`DbContext` already provides change tracking and unit-of-work behavior;
`IUnitOfWork` is the Application-facing abstraction over the commit boundary and
its implementation delegates to the same scoped `DbContext`.

## DbContext and Entity Configuration

```csharp
internal sealed class AppDbContext(DbContextOptions<AppDbContext> options)
    : DbContext(options)
{
    public DbSet<Order> Orders => Set<Order>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);
    }
}

internal sealed class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.HasKey(x => x.Id);
        builder.Property(x => x.Total).HasPrecision(18, 2);
        builder.HasIndex(x => x.CreatedAt);
    }
}
```

Keep persistence configuration in `IEntityTypeConfiguration<T>` classes rather
than on Domain entities where practical.

## Registration

```csharp
public static IServiceCollection AddInfrastructure(
    this IServiceCollection services, IConfiguration configuration)
{
    services.AddDbContext<AppDbContext>(options =>
        options.UseSqlServer(configuration.GetConnectionString("DefaultConnection")));

    services.AddScoped<IOrderRepository, OrderRepository>();
    services.AddScoped<IUnitOfWork, UnitOfWork>();
    return services;
}
```

## Repository and Unit of Work

```csharp
internal sealed class OrderRepository(AppDbContext db) : IOrderRepository
{
    public Task<Order?> GetByIdAsync(Guid id, CancellationToken cancellationToken) =>
        db.Orders.FirstOrDefaultAsync(x => x.Id == id, cancellationToken);

    public async Task AddAsync(Order order, CancellationToken cancellationToken) =>
        await db.Orders.AddAsync(order, cancellationToken);   // stages only
}

internal sealed class UnitOfWork(AppDbContext db) : IUnitOfWork
{
    public Task<int> SaveChangesAsync(CancellationToken cancellationToken = default) =>
        db.SaveChangesAsync(cancellationToken);
}

// Optional Infrastructure-only base removing real duplication
internal abstract class Repository<TEntity>(AppDbContext db) where TEntity : class
{
    protected DbSet<TEntity> Set => db.Set<TEntity>();
}
```

## Read Queries and Projections

```csharp
public Task<OrderSummary?> GetSummaryAsync(Guid id, CancellationToken cancellationToken) =>
    db.Orders
        .Where(x => x.Id == id)
        .Select(x => new OrderSummary(x.Id, x.Total, x.CreatedAt))
        .FirstOrDefaultAsync(cancellationToken);
```

Projection is not mandatory when the use case needs the entity; avoid loading a
whole aggregate to return two scalars.

## Tracking and Lookups

- Use tracking queries when loaded entities will be modified and committed in
  the current Unit of Work; use `AsNoTracking()` for read-only entity queries.
  Do not add `AsNoTracking()` to projections that already produce DTOs.
- `FindAsync([orderId], cancellationToken)` fits primary-key lookups where an
  entity instance (possibly already tracked) is wanted; use LINQ when you need
  predicates, projection, related data, or shaping.

## Related Data

Prefer an explicit query shape: projection for selected related data,
`Include`/`ThenInclude` when the graph itself is needed. Avoid lazy loading by
default (hidden queries, N+1). For large collection includes consider split
queries and verify the generated SQL.

## Pagination

```csharp
var query = db.Orders
    .Where(x => x.CustomerId == customerId)
    .OrderByDescending(x => x.CreatedAt)
    .ThenBy(x => x.Id);                       // deterministic ordering

var totalCount = await query.CountAsync(cancellationToken);
var items = await query
    .Skip((page - 1) * pageSize)
    .Take(pageSize)
    .Select(x => new OrderSummary(x.Id, x.Total, x.CreatedAt))
    .ToListAsync(cancellationToken);
```

Always order paged queries deterministically; consider keyset pagination for
very large or frequently traversed datasets.

## Bulk Update and Delete

```csharp
await db.Orders
    .Where(x => x.Status == OrderStatus.Cancelled)
    .ExecuteDeleteAsync(cancellationToken);
```

`ExecuteUpdateAsync`/`ExecuteDeleteAsync` bypass change tracking; do not mix them
casually with tracked entities for the same rows, and understand their
transaction implications.

## Transactions

One `SaveChangesAsync` is normally the transaction for an operation. Use an
explicit transaction (`await using var tx = await db.Database.BeginTransactionAsync(ct);`)
only when several database operations or `SaveChangesAsync` calls must succeed
atomically. EF transactions do not solve distributed transactions.

## Interceptors

Interceptors suit infrastructure cross-cutting behavior such as auditing; never
hide business behavior in them.

```csharp
internal sealed class AuditInterceptor(TimeProvider clock) : SaveChangesInterceptor
{
    public override ValueTask<InterceptionResult<int>> SavingChangesAsync(
        DbContextEventData eventData, InterceptionResult<int> result,
        CancellationToken cancellationToken = default)
    {
        if (eventData.Context is { } context)
        {
            var now = clock.GetUtcNow();
            foreach (var entry in context.ChangeTracker.Entries<IAuditable>())
            {
                if (entry.State == EntityState.Added) entry.Entity.CreatedAt = now;
                if (entry.State is EntityState.Added or EntityState.Modified) entry.Entity.UpdatedAt = now;
            }
        }
        return ValueTask.FromResult(result);
    }
}
```

## Compiled Queries and Raw SQL

EF Core already caches query compilation by shape; `EF.CompileAsyncQuery` is for
measured hot paths only. Use raw SQL only when LINQ cannot express the query
effectively or measurement justifies it, with parameterizing APIs
(`FromSqlInterpolated`, `SqlQuery` with interpolation, ADO.NET parameters).

## Migrations

```bash
dotnet ef migrations add AddOrderIndex --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api
dotnet ef migrations script --idempotent --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api
```

Generated idempotent scripts are often preferable for controlled production
deployment. Review checklist: `persistence.md`.

## Development Seeder Implementation

```csharp
internal static class DbSeeder
{
    public static async Task SeedAsync(AppDbContext db, CancellationToken cancellationToken = default)
    {
        if (await db.Projects.AnyAsync(cancellationToken))   // anchor entity check
            return;

        await db.Projects.AddRangeAsync(CreateProjects(), cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
    }

    private static IReadOnlyCollection<Project> CreateProjects()
    {
        // Deterministic, representative scenarios: new, active/in progress,
        // completed, archived; with/without optional values and relationships;
        // representative status values and meaningful boundary states.
        throw new NotImplementedException();
    }
}

public static class DatabaseInitializationExtensions
{
    public static async Task SeedDevelopmentDataAsync(
        this IServiceProvider services, CancellationToken cancellationToken = default)
    {
        await using var scope = services.CreateAsyncScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        await DbSeeder.SeedAsync(db, cancellationToken);
    }
}

// Program.cs — after migrations were applied separately
if (app.Environment.IsDevelopment())
{
    await app.Services.SeedDevelopmentDataAsync();
}
```

Seeder changes typically follow new required properties, renamed/removed
properties, changed relationships, new required related entities, changed
enum/status values, new meaningful states, or changed invariants.

## Query Performance Investigation

Start with clear LINQ. When a real problem appears, inspect round trips,
selected columns, N+1 behavior, indexes, generated SQL (`ToQueryString()`,
logging), query plans, materialized volume, and tracking overhead before any
specialized optimization.

## Decision Guide

| Scenario | Technique |
|---|---|
| Read-only entity query | `AsNoTracking()` when useful |
| Read model | Database-side `Select` projection |
| Primary-key entity lookup | `FindAsync` when its semantics fit |
| Complex entity graph | Explicit `Include` or projection; split query if large |
| Set-based mass update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` |
| Multiple commits requiring atomicity | Explicit transaction |
| Measured extremely hot query | Consider compiled query |
| Production schema change | Reviewed migration, idempotent script |
| Need fresh local seed data | Drop and recreate the local database explicitly |
