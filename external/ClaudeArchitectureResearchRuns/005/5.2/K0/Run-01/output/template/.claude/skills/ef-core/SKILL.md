---
name: ef-core
description: Use when writing or reviewing EF Core code — DbContext and entity configuration, repository or Unit of Work implementations, LINQ queries, tracking, projections, pagination, bulk updates, transactions, migrations, development seeding code or query performance.
---
<!-- Kind: KNW | Scope: backend | Owns: EF Core implementation technique and examples | Loads: on demand (model-invoked) -->
# Entity Framework Core

Standards: `rules/backend/persistence.md` (repositories, Unit of Work, EF Core boundary, database access, development seeding) and `rules/backend/architecture.md`. This skill shows how to implement them.

## Role in the Architecture

Application owns persistence contracts — specific repository interfaces and `IUnitOfWork` — and Infrastructure implements them with EF Core. `DbContext` already provides change tracking and unit-of-work behavior internally; `IUnitOfWork` is the Application-facing abstraction over the commit boundary, and its Infrastructure implementation normally delegates to the same `DbContext`.

Application contracts:

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
public interface IUnitOfWork
{
    Task<int> SaveChangesAsync(
        CancellationToken cancellationToken = default);
}
```

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

Use the provider the project selected (DEC-DATA-01); avoid adding a provider merely because it appears in an example.

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

Repositories stage changes; the Application Service commits through `IUnitOfWork`.

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

Repositories join the same Unit of Work simply by receiving the same scoped `AppDbContext` from DI; no repository properties on the Unit of Work.

## Generic Repository

When an Infrastructure-internal base class removes genuine duplication:

```csharp
internal abstract class Repository<TEntity>(AppDbContext db)
    where TEntity : class
{
    protected DbSet<TEntity> Set => db.Set<TEntity>();
}
```

Concrete repositories keep full access to the EF Core API for complex queries rather than forcing them through generic CRUD helpers.

## Read Queries and Projections

For read-only queries that need only selected data, prefer database-side projection:

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

Projection is not mandatory when the use case genuinely needs the entity; avoid loading a complete aggregate only to return two scalar fields.

## Tracking

Use normal tracking queries when loaded entities will be modified and committed through the current Unit of Work. Use `AsNoTracking()` for read-only entity queries where change tracking provides no value; it adds nothing to projections that already produce non-entity DTOs.

## Primary-Key Lookups

`FindAsync` fits when querying by primary key, an entity instance is required, and returning an already tracked entity is desirable:

```csharp
var order = await db.Orders.FindAsync(
    [orderId],
    cancellationToken);
```

Use LINQ when additional predicates, projection, related data or query shaping are required.

## Related Data

Prefer an explicit query shape: projection when only selected related data is needed, `Include` / `ThenInclude` when the entity graph itself is required. Avoid lazy loading by default — it hides database access and invites N+1 queries. For large collection includes, consider split queries and verify the generated SQL and performance characteristics.

## Pagination

Apply filtering, ordering and pagination in the database, always with deterministic ordering:

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

For very large or frequently traversed datasets, consider keyset pagination instead of large `Skip` offsets when justified.

## Bulk Update and Delete

`ExecuteUpdateAsync` and `ExecuteDeleteAsync` suit set-based operations:

```csharp
await db.Orders
    .Where(x => x.Status == OrderStatus.Cancelled)
    .ExecuteDeleteAsync(cancellationToken);
```

They execute directly against the database and bypass change tracking: avoid mixing them casually with tracked entities for the same rows, and understand their transaction and consistency implications first.

## Transactions

A single `SaveChangesAsync` is normally sufficient as the transaction boundary of one application operation. Use an explicit transaction when a concrete use case requires several database operations or several `SaveChangesAsync` calls to succeed atomically. EF transaction APIs do not solve distributed transactions.

## Compiled Queries

Normal LINQ is the default, and EF Core already caches query compilation by query shape. `EF.CompileQuery` / `EF.CompileAsyncQuery` pay off only on a measured hot path where profiling shows compilation/cache lookup overhead is material — frequent execution alone is not a reason (`rules/backend/csharp.md` § Optimization Discipline).

## Interceptors

Interceptors suit infrastructure-level cross-cutting behavior with a clear benefit, such as auditing:

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

Avoid hiding business behavior in persistence interceptors.

## Development Data Seeding

Rules: `rules/backend/persistence.md` § Development Seeding. Co-change with model changes: `development-workflow` § Co-change Obligations.

### Location

```text
Persistence/
  Seeding/
    DbSeeder.cs
    DatabaseInitializationExtensions.cs
```

### Empty Database Behavior

The seeder assumes the Development schema has already been migrated to the current revision; for a new local database the developer applies the migrations first, then application startup populates the empty schema. Use one or more representative root/anchor entities to detect existing data:

```csharp
if (await db.Projects.AnyAsync(cancellationToken))
{
    return;
}
```

When a developer needs the latest seed dataset in an existing local database, they drop and recreate it explicitly.

### Seed Dataset

Cover the main meaningful states and relationships needed during development, where applicable: newly created; active or in progress; completed; inactive or archived; with and without optional values; with and without optional relationships; representative status values; meaningful boundary states. Do not try to generate every combination; a small, readable, deterministic dataset keeps development behavior predictable between recreations. When the required entity graph or scenarios are complex, the task requirements should describe the dataset explicitly rather than leaving a large generic object graph to be invented.

### Seeder Example

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

The concrete seed entities and states match the actual current Domain and persistence model.

### Startup

Keep `DbSeeder` internal to Infrastructure and expose the narrow initialization extension; invoke it only for the Development environment:

```csharp
if (app.Environment.IsDevelopment())
{
    await app.Services.SeedDevelopmentDataAsync();
}
```

Migration strategy stays separate from development seeding.

## Migrations

Create migrations from the Infrastructure project with the Api project as startup project when required:

```bash
dotnet ef migrations add AddOrderIndex --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api
```

Review obligations: `development-workflow` § Co-change Obligations. Production application: `delivery-pipeline` — for controlled production deployment, generated migration scripts (`dotnet ef migrations script --idempotent`) are often preferable.

## Query Performance

Start with clear normal LINQ and optimize after identifying a real problem. Before specialized optimization, inspect the number of round trips, selected columns, N+1 behavior, indexes, generated SQL, the query plan where necessary, the amount of data materialized, and tracking overhead.

## Raw SQL

Raw SQL is for queries EF Core cannot express effectively or a measured performance need. Prefer EF APIs that preserve parameterization (`FromSql`, `FromSqlInterpolated`, `ExecuteSql`) over string-built SQL (`rules/backend/persistence.md` § Database Access).

## Anti-Patterns

Avoid loading all rows and filtering in memory when the database can filter, lazy loading by default, fire-and-forget EF asynchronous operations, compiled queries without evidence, raw SQL merely to appear more performant, and changing the seeded entity model without updating the seed dataset. Boundary violations are listed in `rules/backend/persistence.md`.

## Decision Guide

| Scenario | Default technique |
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
| Production schema change | Reviewed migration, controlled deployment |
| Empty development database | Run the maintained development seeder |
| Existing development database | Leave seed data unchanged |
| Need a fresh local seed dataset | Recreate the local database explicitly |
| Test data | Dedicated test setup, not development seeding |
