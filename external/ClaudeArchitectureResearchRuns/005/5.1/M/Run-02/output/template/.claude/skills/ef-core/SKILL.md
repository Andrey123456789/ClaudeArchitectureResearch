---
name: ef-core
description: >
  Use when writing or reviewing EF Core code: DbContext, entity
  configurations, repository and UnitOfWork implementations, LINQ queries,
  tracking, Include/projection, pagination, bulk updates, transactions,
  interceptors, raw SQL, migrations, DbSeeder.
---

> Owner: EF Core implementation technique and examples (normative policy lives in rules) | Scope: backend | Loads: on demand — knowledge | Enforced: none

# Entity Framework Core

Policy: `.claude/rules/persistence.md` (Unit of Work, EF Core boundary, seeding,
migrations), `.claude/rules/architecture.md` § Repositories (contracts),
`.claude/rules/performance.md` § Database Access (efficiency),
`.claude/rules/security.md` § SQL and Persistence (parameterization).

`DbContext` already provides change tracking and unit-of-work behavior.
`IUnitOfWork` is the Application-facing abstraction over the commit boundary, and
its Infrastructure implementation delegates to the same `DbContext`.

## DbContext Configuration

Keep entity configuration in separate `IEntityTypeConfiguration<T>` classes and
persistence-specific configuration out of Domain entities where practical.

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

Use the provider the project actually selected; do not add a provider because it
appears in an example.

## Specific Repositories

An Application contract and its Infrastructure implementation:

```csharp
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(
        Guid id,
        CancellationToken cancellationToken);

    Task AddAsync(
        Order order,
        CancellationToken cancellationToken);
}
```

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

`AddAsync` stages the entity; the commit happens through `IUnitOfWork`.

## Unit of Work Implementation

```csharp
public interface IUnitOfWork
{
    Task<int> SaveChangesAsync(
        CancellationToken cancellationToken = default);
}
```

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

Repositories and `UnitOfWork` share one scoped `AppDbContext` because
`AddDbContext` registers it as scoped.

## Generic Repository Base

An Infrastructure-only base can remove genuine implementation duplication while
concrete repositories keep the full EF Core API:

```csharp
internal abstract class Repository<TEntity>(AppDbContext db)
    where TEntity : class
{
    protected DbSet<TEntity> Set => db.Set<TEntity>();
}
```

Do not force complex queries through a generic CRUD abstraction.

## Read Queries and Projections

For read-only queries that need selected data, prefer database-side projection:

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

Projection is not mandatory when the use case genuinely needs the entity; avoid
loading a complete aggregate only to return two scalar fields.

## Tracking

- Use normal tracking queries when loaded entities will be modified and committed
  through the current Unit of Work.
- Use `AsNoTracking()` for read-only entity queries where change tracking adds no
  value.
- Do not add `AsNoTracking()` mechanically to projections that already produce
  non-entity DTOs.

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

- Prefer an explicit query shape: projection when only selected related data is
  needed, `Include` / `ThenInclude` when the entity graph itself is required.
- Avoid lazy loading by default; it hides database access and invites N+1
  queries.
- For large collection includes, consider split queries and verify the generated
  SQL and performance characteristics.

## Pagination

Apply filtering, ordering, and pagination in the database, always with a
deterministic order:

```csharp
var query = db.Orders
    .Where(x => x.CustomerId == customerId)
    .OrderByDescending(x => x.CreatedAt)
    .ThenBy(x => x.Id);

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

Page-size defaults and maximums are product values (`CUSTOM_SETTINGS.md`). For
very large or frequently traversed datasets, consider keyset pagination instead
of large `Skip` offsets when justified.

## Bulk Update and Delete

`ExecuteUpdateAsync` and `ExecuteDeleteAsync` suit set-based operations:

```csharp
await db.Orders
    .Where(x => x.Status == OrderStatus.Cancelled)
    .ExecuteDeleteAsync(cancellationToken);
```

They execute directly against the database and bypass change tracking. Do not mix
them casually with tracked entities for the same rows, and understand their
transaction and consistency implications first.

## Transactions

A single `SaveChangesAsync` is the transaction boundary for one application
operation. When a concrete use case needs several database operations or several
`SaveChangesAsync` calls to succeed atomically:

```csharp
await using var transaction =
    await db.Database.BeginTransactionAsync(cancellationToken);

// ... several operations / SaveChangesAsync calls ...

await transaction.CommitAsync(cancellationToken);
```

With a retrying execution strategy enabled, wrap the transaction in
`db.Database.CreateExecutionStrategy().ExecuteAsync(...)`. Do not attempt
distributed transactions with EF transaction APIs.

## Compiled Queries

EF Core already caches query compilation by query shape. `EF.CompileQuery` /
`EF.CompileAsyncQuery` only pays off on a measured hot path where profiling shows
compilation or cache lookup overhead is material (`.claude/rules/performance.md`
§ General Principle).

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

Keep business behavior out of persistence interceptors.

## Development Seeding Pattern

Implements `.claude/rules/persistence.md` § Development Seeding.

```text
Persistence/
  Seeding/
    DbSeeder.cs
    DatabaseInitializationExtensions.cs
```

Use one or more representative root entities to detect existing data, and keep
the seeder internal behind a narrow extension that creates the scope:

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

Startup:

```csharp
if (app.Environment.IsDevelopment())
{
    await app.Services.SeedDevelopmentDataAsync();
}
```

Useful scenario coverage, where applicable: newly created, active or in
progress, completed, inactive or archived; entities with and without optional
values and optional relationships; representative status values; meaningful
boundary states. When the required graph is complex, ask the task to describe
the dataset instead of inventing a large generic object graph.

Seed-affecting changes to watch for: new required properties, removed or renamed
properties, changed relationships, new required related entities, changed
enum/status values, new meaningful states, changed invariants. A migration of an
existing Development database does not require the seeder to patch rows that are
already seeded.

## Migrations

Create migrations from the Infrastructure project with the API project as the
startup project:

```bash
dotnet ef migrations add AddOrderIndex --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api
dotnet ef database update --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api
```

Review checklist: `.claude/rules/persistence.md` § Migrations. For controlled
production deployment, generated idempotent scripts are often preferable:

```bash
dotnet ef migrations script --idempotent --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api --output artifacts/migrations.sql
```

## Query Performance

Start with clear LINQ and optimize after identifying a real problem. Inspect:
round trips, selected columns, N+1 behavior, indexes, generated SQL
(`ToQueryString()`, logging), the query plan when necessary, the amount of data
materialized, and tracking overhead.

## Raw SQL

Use raw SQL only when EF Core cannot express the query effectively or measured
performance justifies it, and keep values parameterized:

```csharp
var orders = await db.Orders
    .FromSqlInterpolated($"SELECT * FROM Orders WHERE CustomerId = {customerId}")
    .ToListAsync(cancellationToken);
```

`FromSqlInterpolated` / `SqlQuery` convert interpolated values into parameters,
which is what `.claude/rules/security.md` § SQL and Persistence requires.

## Common Mistakes

- calling `SaveChangesAsync` from every repository method;
- loading all rows and filtering in memory when the database can filter;
- fire-and-forget EF asynchronous operations;
- caching tracked entities across Unit of Work boundaries;
- lazy loading enabled by default.

## Decision Guide

| Scenario | Technique |
|---|---|
| Read-only entity query | `AsNoTracking()` when useful |
| Read model | Database-side projection |
| Primary-key entity lookup | `FindAsync` when its semantics fit |
| Complex entity graph | Explicit `Include` / projection |
| Set-based mass update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` |
| Measured extremely hot query | Consider a compiled query |
| Multiple commits requiring atomicity | Explicit transaction |
| Production schema change | Reviewed migration, scripted deployment |
| Fresh local seed dataset | Drop and recreate the local database explicitly |
