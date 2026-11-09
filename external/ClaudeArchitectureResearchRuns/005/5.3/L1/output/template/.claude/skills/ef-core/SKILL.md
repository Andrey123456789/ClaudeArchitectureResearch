---
name: ef-core
description: EF Core technique for the persistence implementation. Use when writing or reviewing DbContext configuration, entity mappings, repositories, Unit of Work, LINQ queries, projections, tracking, pagination, bulk updates, transactions, interceptors, raw SQL, DbSeeder, or migrations.
---

> Level: 2-technology · Capability: persistence/ef-core · Facet: persistence.knowledge · Owns: EF Core implementation technique and examples · Loading: on demand

# EF Core

Rules: `persistence.access`, `persistence.seeding` (and the frame boundaries for placement). Procedures: `persistence.workflow`; commands: `persistence.commands`. This skill adds technique only.

## DbContext and mappings

Keep entity configuration in `IEntityTypeConfiguration<T>` classes and persistence-specific configuration out of domain-model entities where practical.

```csharp
internal sealed class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<Order> Orders => Set<Order>();

    protected override void OnModelCreating(ModelBuilder modelBuilder) =>
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);
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

Registration happens in the implementation project's `AddInfrastructure` (`persistence.commands`); do not add a provider merely because an example shows it.

## Repositories and Unit of Work

```csharp
internal sealed class OrderRepository(AppDbContext db) : IOrderRepository
{
    public Task<Order?> GetByIdAsync(Guid id, CancellationToken cancellationToken) =>
        db.Orders.FirstOrDefaultAsync(x => x.Id == id, cancellationToken);

    public async Task AddAsync(Order order, CancellationToken cancellationToken) =>
        await db.Orders.AddAsync(order, cancellationToken);
}

internal sealed class UnitOfWork(AppDbContext db) : IUnitOfWork
{
    public Task<int> SaveChangesAsync(CancellationToken cancellationToken = default) =>
        db.SaveChangesAsync(cancellationToken);
}
```

`DbContext` already tracks changes; `IUnitOfWork` is the use-case-facing abstraction over the same scoped context. An internal generic base may share helpers:

```csharp
internal abstract class Repository<TEntity>(AppDbContext db) where TEntity : class
{
    protected DbSet<TEntity> Set => db.Set<TEntity>();
}
```

Use-case-specific queries stay in concrete repositories, which may use the full EF Core API.

## Queries

- **Projection** — for read-only queries that need selected data, project in the database; projection is not mandatory when the use case needs the entity. Avoid loading a whole aggregate to return two scalars.

  ```csharp
  db.Orders.Where(x => x.Id == id)
      .Select(x => new OrderSummary(x.Id, x.Total, x.CreatedAt))
      .FirstOrDefaultAsync(cancellationToken);
  ```

- **Tracking** — tracking queries for entities that will be modified and committed; `AsNoTracking()` for read-only entity queries; not needed on projections to non-entity DTOs.
- **Primary-key lookup** — `FindAsync([orderId], cancellationToken)` when querying by key, needing the entity, and an already tracked instance is acceptable; LINQ when predicates, projection, or related data are involved.
- **Related data** — explicit query shape: projection for selected related data, `Include`/`ThenInclude` when the graph itself is needed; avoid lazy loading by default (hidden queries, N+1); consider split queries for large collection includes and verify the SQL.
- **Pagination** — filter, order deterministically, and page in the database; consider keyset pagination for very large or frequently traversed sets.

  ```csharp
  var query = db.Orders.Where(x => x.CustomerId == customerId).OrderByDescending(x => x.CreatedAt).ThenBy(x => x.Id);
  var total = await query.CountAsync(cancellationToken);
  var items = await query.Skip((page - 1) * pageSize).Take(pageSize)
      .Select(x => new OrderSummary(x.Id, x.Total, x.CreatedAt)).ToListAsync(cancellationToken);
  ```

- **Bulk operations** — `ExecuteUpdateAsync`/`ExecuteDeleteAsync` run directly against the database and bypass change tracking; do not mix them casually with tracked entities for the same rows; understand their transaction semantics.
- **Transactions** — when the frame's Unit of Work rule allows an explicit transaction (several operations or commits that must be atomic), use `await using var tx = await db.Database.BeginTransactionAsync(cancellationToken);` … `await tx.CommitAsync(cancellationToken);`. EF transaction APIs do not solve distributed transactions.
- **Compiled queries** — `EF.CompileAsyncQuery` is a measured-optimization tool (backend code rule); EF Core already caches query compilation by shape, so it helps only when profiling shows compilation or cache lookup is material.
- **Raw SQL** — when LINQ cannot express the query effectively or measurement justifies it, `FromSql`, `FromSqlInterpolated`, and `ExecuteSql` turn interpolated values into parameters (parameterization rule: security rules).
- **Query performance** — start with clear LINQ; before optimizing, inspect round trips, selected columns, N+1, indexes, generated SQL, query plans, materialized volume, and tracking overhead.
- **Concurrency on one context** — a `DbContext` is not thread-safe: always `await` each operation; never fire-and-forget EF Core async calls or run parallel queries (`Task.WhenAll`) on the same scoped context; use separate scopes when parallel database work is genuinely needed.

## Interceptors

Use interceptors for infrastructure cross-cutting behavior such as auditing; never hide business behavior in them.

```csharp
internal sealed class AuditInterceptor(TimeProvider clock) : SaveChangesInterceptor
{
    public override ValueTask<InterceptionResult<int>> SavingChangesAsync(
        DbContextEventData eventData, InterceptionResult<int> result, CancellationToken cancellationToken = default)
    {
        if (eventData.Context is null) return ValueTask.FromResult(result);
        var now = clock.GetUtcNow();
        foreach (var entry in eventData.Context.ChangeTracker.Entries<IAuditable>())
        {
            if (entry.State == EntityState.Added) entry.Entity.CreatedAt = now;
            if (entry.State is EntityState.Added or EntityState.Modified) entry.Entity.UpdatedAt = now;
        }
        return ValueTask.FromResult(result);
    }
}
```

## Development seeder

Placement: `Persistence/Seeding/` in the implementation project. The concrete entities and states must match the current model; when the required graph is complex, ask for the desired dataset instead of inventing a large generic one.

```csharp
internal static class DbSeeder
{
    public static async Task SeedAsync(AppDbContext db, CancellationToken cancellationToken = default)
    {
        if (await db.Projects.AnyAsync(cancellationToken)) return;   // anchor entity: data exists
        await db.Projects.AddRangeAsync(CreateProjects(), cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
    }

    private static IReadOnlyCollection<Project> CreateProjects() =>
        throw new NotImplementedException(); // deterministic, representative development scenarios
}

public static class DatabaseInitializationExtensions
{
    public static async Task SeedDevelopmentDataAsync(this IServiceProvider services, CancellationToken cancellationToken = default)
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

## Decision guide

| Scenario | Default |
| --- | --- |
| Use-case persistence dependency | specific repository interface |
| Commit | `IUnitOfWork.SaveChangesAsync` |
| Read-only entity query | `AsNoTracking()` when useful |
| Read model | database-side projection |
| Primary-key entity lookup | `FindAsync` when its semantics fit |
| Complex graph | explicit `Include` or projection |
| Set-based update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` when appropriate |
| Measured extremely hot query | consider a compiled query |
| Several commits that must be atomic | explicit transaction |
| Production schema change | reviewed migration, controlled deployment |
| Empty Development database | run the seeder |
| Fresh local seed data | explicitly recreate the local database |
| Test data | dedicated test setup, never the seeder |
