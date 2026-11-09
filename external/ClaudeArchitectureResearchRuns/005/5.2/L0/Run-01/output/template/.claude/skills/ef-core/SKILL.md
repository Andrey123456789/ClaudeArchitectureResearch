---
name: ef-core
description: >
  Use for EF Core code: DbContext and mappings, repository/UoW implementations, LINQ, tracking, pagination, transactions, migrations, seeder code, query performance.
---

> Level: 2 Technology | Owns: EF Core implementation technique | Scope: backend | Loads: knowledge skill (on demand) | Depends on: 2-technology/ef-core.md

# EF Core Technique

Policy owners (routing): repository and Unit of Work rules →
`1-architecture/persistence-boundary.md`; EF Core placement and bindings →
`2-technology/ef-core.md`; seeding lifecycle → `3-project/data-lifecycle.md`;
migration review → `develop`; data-access efficiency and raw-SQL evidence →
`0-core/performance-principles.md`; SQL parameterization →
`0-core/security-principles.md`.

`DbContext` already provides change tracking and unit-of-work behavior;
`IUnitOfWork` is the Application-facing commit abstraction and its
implementation delegates to the same scoped context.

## DbContext and Configuration

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

## Repository and Unit of Work Implementations

```csharp
internal sealed class OrderRepository(AppDbContext db) : IOrderRepository
{
    public Task<Order?> GetByIdAsync(Guid id, CancellationToken cancellationToken) =>
        db.Orders.FirstOrDefaultAsync(x => x.Id == id, cancellationToken);

    public async Task AddAsync(Order order, CancellationToken cancellationToken) =>
        await db.Orders.AddAsync(order, cancellationToken);   // staged; no SaveChanges here
}

internal sealed class UnitOfWork(AppDbContext db) : IUnitOfWork
{
    public Task<int> SaveChangesAsync(CancellationToken cancellationToken = default) =>
        db.SaveChangesAsync(cancellationToken);
}

// Optional Infrastructure-only base that removes real duplication.
internal abstract class Repository<TEntity>(AppDbContext db) where TEntity : class
{
    protected DbSet<TEntity> Set => db.Set<TEntity>();
}
```

Concrete repositories may use the full EF Core API internally; use-case-specific
queries belong in them, not in the base class.

## Reads

- **Projection:** for read models, project in the database instead of loading a
  whole aggregate to return two fields; projection is optional when the use case
  needs the entity.

```csharp
public Task<OrderSummary?> GetSummaryAsync(Guid id, CancellationToken ct) =>
    db.Orders.Where(x => x.Id == id)
        .Select(x => new OrderSummary(x.Id, x.Total, x.CreatedAt))
        .FirstOrDefaultAsync(ct);
```

- **Tracking:** track entities you will modify and commit; use `AsNoTracking()`
  for read-only entity queries; projections to non-entity DTOs do not need it.
- **Primary key:** `FindAsync([id], ct)` fits a key lookup that needs an entity
  instance and may return an already tracked one; use LINQ for extra
  predicates, projection, or related data.
- **Related data:** prefer an explicit query shape — projection for selected
  data, `Include`/`ThenInclude` when the graph itself is needed. Avoid lazy
  loading (hidden queries, N+1). For large collection includes consider split
  queries and check the generated SQL.
- **Pagination:** filter, order deterministically, and page in the database;
  consider keyset pagination for very large or frequently traversed sets.

```csharp
var query = db.Orders.Where(x => x.CustomerId == customerId)
    .OrderByDescending(x => x.CreatedAt).ThenBy(x => x.Id);
var total = await query.CountAsync(ct);
var items = await query.Skip((page - 1) * pageSize).Take(pageSize)
    .Select(x => new OrderSummary(x.Id, x.Total, x.CreatedAt))
    .ToListAsync(ct);
```

## Writes

- **Bulk:** `ExecuteUpdateAsync`/`ExecuteDeleteAsync` run set-based statements
  directly and bypass change tracking; do not mix them casually with tracked
  entities for the same rows, and understand their transaction implications.
- **Transactions:** one `SaveChangesAsync` is normally the transaction. Use an
  explicit transaction only when several operations or several `SaveChangesAsync`
  calls must be atomic. EF transactions do not solve distributed transactions.
- **Interceptors:** use `SaveChangesInterceptor` for infrastructure
  cross-cutting behavior such as auditing timestamps (with `TimeProvider`);
  never hide business behavior in them.
- Avoid fire-and-forget EF asynchronous operations; the context is not
  thread-safe and failures are lost.

## Development Seeder Shape

```csharp
internal static class DbSeeder
{
    public static async Task SeedAsync(AppDbContext db, CancellationToken ct = default)
    {
        if (await db.Projects.AnyAsync(ct))   // representative anchor entity
            return;

        await db.Projects.AddRangeAsync(CreateProjects(), ct);
        await db.SaveChangesAsync(ct);
    }

    private static IReadOnlyCollection<Project> CreateProjects()
    {
        // Deterministic, representative development scenarios for the current model.
        throw new NotImplementedException();
    }
}

public static class DatabaseInitializationExtensions
{
    public static async Task SeedDevelopmentDataAsync(
        this IServiceProvider services, CancellationToken ct = default)
    {
        await using var scope = services.CreateAsyncScope();
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        await DbSeeder.SeedAsync(db, ct);
    }
}

// Program.cs
if (app.Environment.IsDevelopment())
{
    await app.Services.SeedDevelopmentDataAsync();
}
```

When the required scenarios are complex, the task should describe the dataset
explicitly rather than having a large generic graph invented.

## Migrations

```bash
dotnet ef migrations add AddOrderIndex --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api
dotnet ef migrations script --idempotent --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api
```

For controlled production deployment, generated (idempotent) migration scripts
are often preferable to applying migrations from code.

## Query Performance

Start with clear LINQ. Before optimizing, inspect round trips, selected columns,
N+1 behavior, indexes, generated SQL, the query plan when needed, materialized
volume, and tracking overhead. EF Core already caches query compilation by
shape; `EF.CompileAsyncQuery` helps only a measured hot path.

## Raw SQL

Raw SQL fits queries LINQ cannot express well or a measured performance need;
use parameter-preserving APIs:

```csharp
var rows = await db.Orders
    .FromSqlInterpolated($"SELECT * FROM Orders WHERE CustomerId = {customerId}")
    .ToListAsync(ct);
```

## Decision Guide

| Scenario | Technique |
|---|---|
| Read-only entity query | `AsNoTracking()` when useful |
| Read model | Database-side projection |
| Key lookup needing an entity | `FindAsync` |
| Entity graph | Explicit `Include` or projection |
| Set-based mass update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` |
| Measured very hot query | Compiled query |
| Several commits that must be atomic | Explicit transaction |
| Production schema change | Reviewed migration via controlled deployment |
| Fresh local seed dataset | Recreate the local database explicitly |
