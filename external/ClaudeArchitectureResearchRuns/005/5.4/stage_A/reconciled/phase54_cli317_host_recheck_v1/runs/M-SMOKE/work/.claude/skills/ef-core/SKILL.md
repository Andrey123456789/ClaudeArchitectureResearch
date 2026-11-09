---
name: ef-core
description: >
  Use when writing or reviewing EF Core code: DbContext and entity
  configuration, repository and Unit of Work implementations, LINQ, tracking,
  projections, pagination, transactions, migrations, DbSeeder.
---

> Owns: EF Core implementation technique and examples (no policy) | Scope: backend | Loads: on demand (knowledge skill)

# Entity Framework Core

Policy owners: repository, Unit of Work, and EF Core boundary rules —
`.claude/rules/architecture.md`; seeding and Development database configuration
— `.claude/rules/persistence.md`; database efficiency and measured
optimizations — `.claude/rules/performance.md`; SQL parameterization —
`.claude/rules/security.md`; migration review and seed co-change —
`development-workflow`.

## How the Boundary Is Implemented

Application defines persistence contracts such as specific repository
interfaces and `IUnitOfWork`; Infrastructure implements them with EF Core.

EF Core's `DbContext` already provides change tracking and unit-of-work behavior
internally. `IUnitOfWork` is the Application-facing abstraction over the commit
boundary, and its Infrastructure implementation delegates to the same
`DbContext`.

## DbContext Configuration

Keep entity configuration separate with `IEntityTypeConfiguration<T>`.

```csharp
internal sealed class AppDbContext(
    DbContextOptions<AppDbContext> options)
    : DbContext(options)
{
    public DbSet<Order> Orders => Set<Order>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(
            typeof(AppDbContext).Assembly);
    }
}
```

```csharp
internal sealed class OrderConfiguration
    : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.HasKey(x => x.Id);

        builder.Property(x => x.Total)
            .HasPrecision(18, 2);

        builder.HasIndex(x => x.CreatedAt);
    }
}
```

Keep persistence-specific configuration out of Domain entities where practical.

## Registration

Register EF Core and persistence implementations in Infrastructure.

```csharp
public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.AddDbContext<AppDbContext>(options =>
            options.UseSqlServer(
                configuration.GetConnectionString("DefaultConnection")));

        services.AddScoped<IOrderRepository, OrderRepository>();
        services.AddScoped<IUnitOfWork, UnitOfWork>();

        return services;
    }
}
```

Use the database provider selected by the actual project; do not add a provider
merely because it appears in an example.

## Specific Repositories

```csharp
internal sealed class OrderRepository(AppDbContext db)
    : IOrderRepository
{
    public Task<Order?> GetByIdAsync(
        Guid id,
        CancellationToken cancellationToken)
    {
        return db.Orders
            .FirstOrDefaultAsync(
                x => x.Id == id,
                cancellationToken);
    }

    public async Task AddAsync(
        Order order,
        CancellationToken cancellationToken)
    {
        await db.Orders.AddAsync(order, cancellationToken);
    }
}
```

The repository stages the change; the Application Service commits through
`IUnitOfWork`.

## Unit of Work Implementation

Repositories are injected independently and participate in the same Unit of
Work by sharing the same scoped `AppDbContext`.

```csharp
internal sealed class UnitOfWork(AppDbContext db)
    : IUnitOfWork
{
    public Task<int> SaveChangesAsync(
        CancellationToken cancellationToken = default)
    {
        return db.SaveChangesAsync(cancellationToken);
    }
}
```

## Generic Repository Base

When an Infrastructure-only base class removes genuine duplication:

```csharp
internal abstract class Repository<TEntity>(AppDbContext db)
    where TEntity : class
{
    protected DbSet<TEntity> Set => db.Set<TEntity>();
}
```

Concrete repositories may still use the full EF Core API internally; do not
force complex queries through a generic CRUD abstraction.

## Read Queries and Projections

For read-only queries that need only selected data, prefer database-side
projection.

```csharp
public Task<OrderSummary?> GetSummaryAsync(
    Guid id,
    CancellationToken cancellationToken)
{
    return db.Orders
        .Where(x => x.Id == id)
        .Select(x => new OrderSummary(
            x.Id,
            x.Total,
            x.CreatedAt))
        .FirstOrDefaultAsync(cancellationToken);
}
```

Projection is not mandatory when the use case genuinely needs the entity, but
avoid loading a complete aggregate only to return two scalar fields.

## Tracking

Use tracking intentionally: normal tracking queries when loaded entities will be
modified and committed through the current Unit of Work; `AsNoTracking()` for
read-only entity queries where change tracking provides no value. Do not add
`AsNoTracking()` mechanically to projections that already produce non-entity
DTOs.

## Primary-Key Lookups

`FindAsync` fits when querying by primary key, an entity instance is required,
and returning an already tracked entity is desirable:

```csharp
var order = await db.Orders.FindAsync(
    [orderId],
    cancellationToken);
```

Use LINQ when additional predicates, projection, related data, or query shaping
are required.

## Related Data

Prefer an explicit query shape: projection when only selected related data is
needed; `Include`/`ThenInclude` when the entity graph itself is required. Avoid
lazy loading by default because it hides database access and causes N+1
queries. For large collection includes, consider split queries and verify the
generated SQL and performance.

## Pagination

Apply filtering, ordering, and pagination in the database, and always use
deterministic ordering for paged queries:

```csharp
var query = db.Orders
    .Where(x => x.CustomerId == customerId)
    .OrderByDescending(x => x.CreatedAt);

var totalCount = await query.CountAsync(cancellationToken);

var items = await query
    .Skip((page - 1) * pageSize)
    .Take(pageSize)
    .Select(x => new OrderSummary(
        x.Id,
        x.Total,
        x.CreatedAt))
    .ToListAsync(cancellationToken);
```

For very large or frequently traversed datasets, consider keyset pagination
instead of large `Skip` offsets when justified.

## Bulk Update and Delete

`ExecuteUpdateAsync` and `ExecuteDeleteAsync` are useful for set-based
operations:

```csharp
await db.Orders
    .Where(x => x.Status == OrderStatus.Cancelled)
    .ExecuteDeleteAsync(cancellationToken);
```

They execute directly against the database and bypass change tracking. Do not
mix them casually with tracked entities representing the same rows, and
understand their transaction and consistency implications.

## Transactions

A single `SaveChangesAsync` is normally the transaction boundary for one
application operation. Use an explicit transaction when a concrete use case
needs several database operations or several `SaveChangesAsync` calls to succeed
atomically. Do not attempt distributed transactions with EF transaction APIs.

## Compiled Queries

Normal LINQ is the default; EF Core already caches query compilation by query
shape. `EF.CompileQuery`/`EF.CompileAsyncQuery` pay off only where compilation or cache
lookup overhead is measured, or clearly demonstrated, to be material — not merely
because a query runs frequently; do not add them speculatively
(`.claude/rules/performance.md`).

## Interceptors

Use EF Core interceptors for infrastructure-level cross-cutting behavior such as
auditing:

```csharp
internal sealed class AuditInterceptor(TimeProvider clock)
    : SaveChangesInterceptor
{
    public override ValueTask<InterceptionResult<int>> SavingChangesAsync(
        DbContextEventData eventData,
        InterceptionResult<int> result,
        CancellationToken cancellationToken = default)
    {
        var context = eventData.Context;

        if (context is null)
            return ValueTask.FromResult(result);

        var now = clock.GetUtcNow();

        foreach (var entry in context.ChangeTracker.Entries<IAuditable>())
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

Do not hide business behavior in persistence interceptors.

## Development Seeder Implementation

The seeder assumes the Development schema was already migrated to the current
revision. For a new local database the developer applies the current
migrations first; application startup then populates the empty schema.

### Dataset shape

Cover the main meaningful states and relationships, for example where
applicable: newly created; active or in progress; completed; inactive or
archived; entities with and without optional values; with and without optional
relationships; representative status values; meaningful boundary states. Do not
attempt every combination. When the required entity graph or scenarios are
complex, the task requirements should describe the dataset explicitly rather
than leaving Claude to invent a large generic object graph.

### Seeder example

Use one or more representative root/anchor entities to detect existing data.

```csharp
internal static class DbSeeder
{
    public static async Task SeedAsync(
        AppDbContext db,
        CancellationToken cancellationToken = default)
    {
        if (await db.Projects.AnyAsync(cancellationToken))
        {
            return;
        }

        var projects = CreateProjects();

        await db.Projects.AddRangeAsync(
            projects,
            cancellationToken);

        await db.SaveChangesAsync(cancellationToken);
    }

    private static IReadOnlyCollection<Project> CreateProjects()
    {
        // Create deterministic, representative development scenarios.
        throw new NotImplementedException();
    }
}

public static class DatabaseInitializationExtensions
{
    public static async Task SeedDevelopmentDataAsync(
        this IServiceProvider services,
        CancellationToken cancellationToken = default)
    {
        await using var scope = services.CreateAsyncScope();

        var db = scope.ServiceProvider
            .GetRequiredService<AppDbContext>();

        await DbSeeder.SeedAsync(
            db,
            cancellationToken);
    }
}
```

The concrete seed entities and states must match the current Domain and
persistence model.

### Startup wiring

```csharp
if (app.Environment.IsDevelopment())
{
    await app.Services.SeedDevelopmentDataAsync();
}
```

The Infrastructure extension creates the scope and delegates to the internal
`DbSeeder`. Database migration strategy is separate from development seeding.

## Migrations

Create migrations from the Infrastructure project, using the API project as the
startup project when required:

```bash
dotnet ef migrations add AddOrderIndex --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api
```

After a model change, recreating an empty Development database must produce
seed data that is valid for the migrated schema. For controlled production
deployment, generated migration scripts are often preferable:

```bash
dotnet ef migrations script --idempotent --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api
```

## Query Performance

Start with clear LINQ and optimize after identifying a real problem. Before
specialized optimization, inspect the number of round trips, selected columns,
N+1 behavior, indexes, generated SQL, the query plan where necessary, the amount
of data materialized, and tracking overhead.

## Raw SQL

Use raw SQL only when EF Core cannot express the query effectively or a measured
or clearly demonstrated performance need justifies it, and prefer EF APIs that preserve parameterization
(`FromSql`, `FromSqlInterpolated`, `SqlQuery`) over string-built SQL.

## Anti-Patterns

Avoid loading all rows and filtering in memory when the database can filter,
lazy loading by default, fire-and-forget EF asynchronous operations, and raw SQL
introduced merely to appear more performant.

## Decision Guide

| Scenario | Default technique |
|---|---|
| Read-only entity query | `AsNoTracking()` when useful |
| Read model | Database-side projection |
| Primary-key entity lookup | `FindAsync` when its semantics fit |
| Complex entity graph | Explicit `Include` / projection |
| Set-based mass update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` when appropriate |
| Normal query | Ordinary LINQ |
| Measured or clearly demonstrated hot query | Consider a compiled query |
| Multiple commits requiring atomicity | Explicit transaction |
| Production schema change | Reviewed migration script, controlled deployment |
| Empty Development database | Run the maintained development seeder |
| Need a fresh local seed dataset | Recreate the local database explicitly |
