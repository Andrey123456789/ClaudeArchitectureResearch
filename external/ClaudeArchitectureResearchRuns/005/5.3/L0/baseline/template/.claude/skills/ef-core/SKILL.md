---
name: ef-core
description: >
  Use for EF Core work: DbContext and entity configuration, repositories, Unit of
  Work, LINQ queries, projections, tracking, pagination, migrations, raw SQL,
  DbSeeder.
---

> Level: 2 Technology · Owns: EF Core implementation technique and examples (knowledge) · Scope: backend · Loads: on invocation · Depends on: .claude/rules/1-architecture/persistence-boundary.md, .claude/rules/2-technology/ef-core.md

# Entity Framework Core

Policy owners: repository/Unit of Work/framework boundary → `.claude/rules/1-architecture/persistence-boundary.md` (EF bindings in `2-technology/ef-core.md`); data-access efficiency and measured optimization → `0-core/runtime-principles.md`; seeding and local database → `3-project/data-lifecycle.md`; migration creation/review and seed co-changes → `development-workflow`; production migrations → `delivery-pipeline`; SQL parameterization → `0-core/security-principles.md`. This skill is technique only.

EF Core's `DbContext` already provides change tracking and unit-of-work behavior; `IUnitOfWork` is the Application-facing abstraction over that commit boundary.

## DbContext and entity configuration

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

## Registration

```csharp
public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.AddDbContext<AppDbContext>(options =>
            options.UseSqlServer(configuration.GetConnectionString("DefaultConnection")));

        services.AddScoped<IOrderRepository, OrderRepository>();
        services.AddScoped<IUnitOfWork, UnitOfWork>();

        return services;
    }
}
```

Use the provider the project selected; do not add a provider because it appears in an example.

## Repository and Unit of Work implementations

```csharp
internal sealed class OrderRepository(AppDbContext db) : IOrderRepository
{
    public Task<Order?> GetByIdAsync(Guid id, CancellationToken cancellationToken) =>
        db.Orders.FirstOrDefaultAsync(x => x.Id == id, cancellationToken);

    public async Task AddAsync(Order order, CancellationToken cancellationToken) =>
        await db.Orders.AddAsync(order, cancellationToken);   // stages only; no SaveChanges here
}

internal sealed class UnitOfWork(AppDbContext db) : IUnitOfWork
{
    public Task<int> SaveChangesAsync(CancellationToken cancellationToken = default) =>
        db.SaveChangesAsync(cancellationToken);
}

// Optional Infrastructure-only base that removes real duplication
internal abstract class Repository<TEntity>(AppDbContext db) where TEntity : class
{
    protected DbSet<TEntity> Set => db.Set<TEntity>();
}
```

Repositories share the scoped `AppDbContext` because it is registered scoped and injected into each of them.

## Read queries and projections

```csharp
public Task<OrderSummary?> GetSummaryAsync(Guid id, CancellationToken cancellationToken) =>
    db.Orders
        .Where(x => x.Id == id)
        .Select(x => new OrderSummary(x.Id, x.Total, x.CreatedAt))
        .FirstOrDefaultAsync(cancellationToken);
```

Projection is not mandatory when the use case genuinely needs the entity; avoid loading a whole aggregate to return two scalars.

## Tracking and lookups

- Use tracking queries when loaded entities will be modified and committed through the current Unit of Work; use `AsNoTracking()` for read-only entity queries where tracking adds nothing. Projections to non-entity DTOs do not need `AsNoTracking()`.
- `FindAsync([orderId], cancellationToken)` fits primary-key lookups where an entity instance is needed and an already tracked instance is acceptable; use LINQ for extra predicates, projection, related data, or shaping.

## Related data

Prefer an explicit query shape: projection for selected related data, `Include`/`ThenInclude` when the graph itself is needed. Avoid lazy loading by default — it hides database access and invites N+1 queries. For large collection includes consider split queries and verify the generated SQL.

## Pagination

```csharp
var query = db.Orders
    .Where(x => x.CustomerId == customerId)
    .OrderByDescending(x => x.CreatedAt);       // paged queries need a deterministic order

var totalCount = await query.CountAsync(cancellationToken);

var items = await query
    .Skip((page - 1) * pageSize)
    .Take(pageSize)
    .Select(x => new OrderSummary(x.Id, x.Total, x.CreatedAt))
    .ToListAsync(cancellationToken);
```

For very large or frequently traversed datasets consider keyset pagination instead of large `Skip` offsets.

## Bulk update and delete

```csharp
await db.Orders
    .Where(x => x.Status == OrderStatus.Cancelled)
    .ExecuteDeleteAsync(cancellationToken);
```

`ExecuteUpdateAsync`/`ExecuteDeleteAsync` run directly against the database and bypass change tracking; do not mix them casually with tracked entities for the same rows, and understand their transaction implications.

## Transactions

A single `SaveChangesAsync` is the normal transaction boundary for one operation. When a concrete use case needs several operations or several saves to succeed atomically, use `await using var tx = await db.Database.BeginTransactionAsync(cancellationToken);` … `await tx.CommitAsync(cancellationToken);` inside Infrastructure. EF transactions do not solve distributed transactions.

## Compiled queries and interceptors

EF Core already caches query compilation by shape; `EF.CompileAsyncQuery` helps only on a measured hot path where compilation/cache lookup is material.

Interceptors suit infrastructure cross-cutting behavior such as auditing, not hidden business behavior:

```csharp
internal sealed class AuditInterceptor(TimeProvider clock) : SaveChangesInterceptor
{
    public override ValueTask<InterceptionResult<int>> SavingChangesAsync(
        DbContextEventData eventData,
        InterceptionResult<int> result,
        CancellationToken cancellationToken = default)
    {
        if (eventData.Context is null)
            return ValueTask.FromResult(result);

        var now = clock.GetUtcNow();
        foreach (var entry in eventData.Context.ChangeTracker.Entries<IAuditable>())
        {
            if (entry.State == EntityState.Added)
                entry.Entity.CreatedAt = now;
            if (entry.State is EntityState.Added or EntityState.Modified)
                entry.Entity.UpdatedAt = now;
        }

        return ValueTask.FromResult(result);
    }
}
```

## Development seeder technique

The seeder detects existing data through one or more representative root entities and populates an already migrated, empty schema:

```csharp
internal static class DbSeeder
{
    public static async Task SeedAsync(AppDbContext db, CancellationToken cancellationToken = default)
    {
        if (await db.Projects.AnyAsync(cancellationToken))
            return;

        await db.Projects.AddRangeAsync(CreateProjects(), cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
    }

    private static IReadOnlyCollection<Project> CreateProjects()
    {
        // Deterministic, representative development scenarios matching the current model.
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

// Program.cs
if (app.Environment.IsDevelopment())
{
    await app.Services.SeedDevelopmentDataAsync();
}
```

A representative dataset typically includes, where applicable: newly created, active/in-progress, completed, inactive/archived entities; entities with and without optional values and relationships; representative status values; meaningful boundary states. When the required graph is complex, ask the task to describe the dataset instead of inventing a large generic graph. Which model changes require a seeder update: `development-workflow` → Co-changes. Migrating an existing Development database does not require the seeder to patch rows already seeded.

## Migrations

```bash
dotnet ef migrations add AddOrderIndex --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api
dotnet ef migrations script --idempotent --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api
```

Generated idempotent scripts or migration bundles are often preferable for controlled production deployment.

## Query performance checklist

Start with clear LINQ; optimize after identifying a real problem. Inspect round trips, selected columns, N+1 behavior, indexes, generated SQL (`ToQueryString()`, logging), the query plan when necessary, the amount of data materialized, and tracking overhead.

## Raw SQL

Use raw SQL only when EF Core cannot express the query effectively or measured performance justifies it. Prefer APIs that keep parameterization, such as `FromSql($"... {value}")` / `FromSqlInterpolated` or explicit `SqlParameter`s, over string concatenation.

## Anti-patterns

Lazy loading by default; fire-and-forget EF async calls.
