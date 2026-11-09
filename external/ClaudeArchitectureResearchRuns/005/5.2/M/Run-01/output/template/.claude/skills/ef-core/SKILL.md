---
name: ef-core
description: >
  Use for EF Core code: DbContext and entity configuration, repository and
  UnitOfWork implementations, LINQ queries, tracking, pagination, migrations,
  the development seeder, query performance.
---

> Knowledge skill. Owns: EF Core implementation technique and examples · Scope: backend · Loads: on demand · Depends on: CLAUDE.md, .claude/rules/persistence.md, .claude/rules/architecture.md, .claude/rules/performance.md

# Entity Framework Core

Rules this technique serves: `persistence.md` (repositories, Unit of Work, EF
Core boundary, seeding), `architecture.md` (layers), `performance.md` (database
access, measured optimizations), `security.md` (parameterized SQL). Migration
review, seed co-change, and production migration: `development-workflow`.

## Role in the Architecture

Application defines persistence contracts — specific repository interfaces and
`IUnitOfWork`; Infrastructure implements them with EF Core. `DbContext` already
provides change tracking and unit-of-work behavior internally; `IUnitOfWork` is
the Application-facing abstraction over the commit boundary, and its
implementation delegates to the same scoped `DbContext`.

## DbContext Configuration

Keep entity configuration separate with `IEntityTypeConfiguration<T>`:

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

Keep persistence-specific configuration out of Domain entities where
practical.

## Registration

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

Use the provider the project actually selected; do not add a provider because
it appears in an example.

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

The repository stages changes; the Application Service commits through
`IUnitOfWork`.

## Unit of Work Implementation

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

Repositories are injected independently and participate in the same Unit of
Work by sharing the scoped `AppDbContext`.

## Infrastructure-Only Generic Base

```csharp
internal abstract class Repository<TEntity>(AppDbContext db)
    where TEntity : class
{
    protected DbSet<TEntity> Set => db.Set<TEntity>();
}
```

Concrete repositories may use the full EF Core API internally; complex queries
do not have to pass through a generic CRUD abstraction.

## Read Queries and Projections

For read-only queries that need selected data, prefer database-side
projection:

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

Use tracking queries when loaded entities will be modified and committed
through the current Unit of Work. Use `AsNoTracking()` for read-only entity
queries where change tracking provides no value; do not add it mechanically to
projections that already produce non-entity DTOs.

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
needed, `Include` / `ThenInclude` when the entity graph itself is required.
Avoid lazy loading by default — it hides database access and invites N+1
queries. For large collection includes consider split queries, and verify the
generated SQL and performance.

## Pagination

Apply filtering, ordering, and pagination in the database, always with a
deterministic order:

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

For very large or frequently traversed datasets consider keyset pagination
instead of large `Skip` offsets when justified.

## Bulk Update and Delete

```csharp
await db.Orders
    .Where(x => x.Status == OrderStatus.Cancelled)
    .ExecuteDeleteAsync(cancellationToken);
```

`ExecuteUpdateAsync` / `ExecuteDeleteAsync` run directly against the database
and bypass change tracking. Do not mix them casually with tracked entities for
the same rows, and understand their transaction and consistency implications.

## Transactions

A single `SaveChangesAsync` is the transaction boundary for one application
operation. Use an explicit transaction when a concrete use case needs several
database operations or several `SaveChangesAsync` calls to succeed atomically.
EF transaction APIs do not solve distributed transactions.

## Compiled Queries

Ordinary LINQ comes first; EF Core already caches query compilation by query
shape. `EF.CompileQuery` / `EF.CompileAsyncQuery` pay off only on a measured hot
path where compilation or cache-lookup overhead is material — frequent
execution alone is not a reason.

## Interceptors

Interceptors suit infrastructure-level cross-cutting behavior such as auditing:

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

## Development Seeding Technique

The seeding rules are in `persistence.md`. Typical shape:

```text
Persistence/
  Seeding/
    DbSeeder.cs
    DatabaseInitializationExtensions.cs
```

Use one or more representative root/anchor entities to detect existing data:

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

Startup invokes the extension only in Development:

```csharp
if (app.Environment.IsDevelopment())
{
    await app.Services.SeedDevelopmentDataAsync();
}
```

A representative dataset typically includes, where applicable: newly created,
active or in-progress, completed, and inactive or archived entities; entities
with and without optional values and optional relationships; representative
status values; meaningful boundary states. Do not try to generate every
combination; use deterministic values so behavior is predictable across
database recreations. When the required entity graph is complex, the task
should describe the desired dataset explicitly rather than leaving a large
generic graph to be invented. Take the concrete entities and states from the
current Domain and persistence model (`persistence.md`, Development Seeding).

## Migrations Technique

Create migrations from the Infrastructure project with the Api project as the
startup project when required:

```bash
dotnet ef migrations add AddOrderIndex --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api
```

For controlled production deployment, generated migration scripts are often
preferable to applying migrations from code.

## Query Performance

Start with clear LINQ and optimize after identifying a real problem. Before a
specialized optimization, inspect the number of round trips, selected columns,
N+1 behavior, indexes, generated SQL, the query plan where necessary, the
amount of data materialized, and tracking overhead.

## Raw SQL

Use raw SQL only when EF Core cannot express the query effectively or measured
performance justifies it; prefer EF APIs that preserve parameterization, such
as `FromSqlInterpolated`, over string construction.

## Anti-Patterns

- exposing `DbContext`, `DbSet<T>`, or `IQueryable<T>` from Infrastructure;
- calling `SaveChangesAsync` from every repository operation;
- loading all rows and filtering in memory when the database can filter;
- lazy loading by default;
- fire-and-forget EF asynchronous operations;
- compiled queries or raw SQL without evidence;
- using the development seeder as a patch/overwrite tool for an existing local
  database, or as test setup.

## Decision Guide

| Scenario | Default |
|---|---|
| Application persistence dependency | Specific repository interface |
| Commit application changes | `IUnitOfWork.SaveChangesAsync` |
| Repository implementation | EF Core inside Infrastructure |
| Read-only entity query | `AsNoTracking()` when useful |
| Read model | Database-side projection |
| Primary-key entity lookup | `FindAsync` when its semantics fit |
| Complex entity graph | Explicit `Include` / projection |
| Set-based mass update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` when appropriate |
| Normal query | Ordinary LINQ |
| Measured extremely hot query | Consider a compiled query |
| Multiple commits requiring atomicity | Explicit transaction |
| Production schema change | Reviewed migration / controlled deployment |
| Empty development database | Maintained development seeder |
| Existing development database | Leave seed data unchanged |
| Model/migration affects seeded entities | Update `DbSeeder` in the same change |
| Fresh local seed dataset needed | Developer recreates the local database |
| Test data | Dedicated test setup, not development seeding |
