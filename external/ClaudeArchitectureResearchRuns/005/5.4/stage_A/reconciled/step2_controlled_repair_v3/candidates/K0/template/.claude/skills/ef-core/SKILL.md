---
name: ef-core
description: Use when writing or reviewing EF Core code — DbContext/entity configuration, repositories and Unit of Work, LINQ, tracking, projections, pagination, transactions, migrations, seeding, query performance.
---

> Kind: KNW | Scope: backend | Owner: EF Core implementation technique and examples | Loading: on demand (model-invoked knowledge)

# Entity Framework Core

Rules: `rules/backend/architecture.md` (repositories, Unit of Work, EF Core boundary), `rules/backend/persistence.md` (database access, seeding), `rules/backend/security.md` (SQL safety). Stack: D-04. Workflow: `development-workflow` § Persistence or model change (migration review, seeder co-change).

## Unit of Work over DbContext

`DbContext` already tracks changes and behaves as a unit of work internally; `IUnitOfWork` is the Application-facing abstraction over the commit boundary, and its Infrastructure implementation delegates to the same scoped `DbContext` the repositories use.

## DbContext configuration

Keep entity configuration in `IEntityTypeConfiguration<T>` classes and persistence-specific configuration out of Domain entities where practical.

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

Register EF Core and persistence implementations in Infrastructure, with the provider the project actually uses — not one that merely appears in an example.

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

## Repository and Unit of Work implementations

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

public interface IUnitOfWork
{
    Task<int> SaveChangesAsync(
        CancellationToken cancellationToken = default);
}
```

Infrastructure implementations:

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

An Infrastructure-only base class can remove genuine duplication while concrete repositories keep the full EF Core API:

```csharp
internal abstract class Repository<TEntity>(AppDbContext db)
    where TEntity : class
{
    protected DbSet<TEntity> Set => db.Set<TEntity>();
}
```

## Read queries and projections

For read-only queries that need selected data, project in the database:

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

Projection is not mandatory when the use case genuinely needs the entity, but avoid loading a whole aggregate to return two scalar fields.

## Tracking

Use tracking queries when loaded entities will be modified and committed through the current Unit of Work, and `AsNoTracking()` for read-only entity queries where tracking adds nothing. Projections to non-entity DTOs do not need `AsNoTracking()`.

## Primary-key lookups

`FindAsync` fits a primary-key lookup that needs an entity instance and may return an already tracked one:

```csharp
var order = await db.Orders.FindAsync(
    [orderId],
    cancellationToken);
```

Use LINQ when extra predicates, projection, related data or query shaping are needed.

## Related data

Make the query shape explicit: projection for selected related data, `Include`/`ThenInclude` when the entity graph itself is required. Avoid lazy loading by default — it hides database access and invites N+1 queries. For large collection includes consider split queries and check the generated SQL and performance.

## Pagination

Filter, order and paginate in the database, with deterministic ordering:

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

For very large or frequently traversed datasets, consider keyset pagination instead of large `Skip` offsets.

## Bulk update and delete

```csharp
await db.Orders
    .Where(x => x.Status == OrderStatus.Cancelled)
    .ExecuteDeleteAsync(cancellationToken);
```

`ExecuteUpdateAsync`/`ExecuteDeleteAsync` run directly against the database and bypass change tracking: do not mix them casually with tracked entities for the same rows, and understand their transaction and consistency implications.

## Transactions

One `SaveChangesAsync` is the transaction boundary for one application operation. An explicit transaction fits a concrete use case where several database operations or several `SaveChangesAsync` calls succeed or fail together. EF transaction APIs do not solve distributed transactions.

## Compiled queries

Normal LINQ is the default; EF Core already caches query compilation by query shape. `EF.CompileQuery`/`EF.CompileAsyncQuery` belong where compilation or cache-lookup overhead is measured, or clearly demonstrated, to matter — not to queries that merely run often; do not add them speculatively (`rules/backend/csharp.md`).

## Interceptors

Interceptors fit infrastructure-level cross-cutting behavior with a clear benefit, such as auditing; business behavior does not belong in them.

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

## Development seeding

Seeding rules: `rules/backend/persistence.md` § Development seeding.

Layout:

```text
Persistence/
  Seeding/
    DbSeeder.cs
    DatabaseInitializationExtensions.cs
```

Detect existing data with one or more representative root/anchor entities. The seeder assumes the schema is already migrated to the current revision; for a new local database the developer applies migrations first, then application startup seeds the empty schema.

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

Startup — the internal seeder stays behind the narrow Infrastructure extension, and migrations are not run here:

```csharp
if (app.Environment.IsDevelopment())
{
    await app.Services.SeedDevelopmentDataAsync();
}
```

Representative states to cover where applicable: newly created; active or in progress; completed; inactive or archived; with and without optional values; with and without optional relationships; representative status values; meaningful boundary states. Do not attempt every combination. When the required entity graph or scenarios are complex, ask for the desired dataset in the task requirements instead of inventing a large generic object graph. The concrete entities and states follow the current Domain and persistence model; when a developer needs the latest seed dataset locally, they drop and recreate the local database explicitly.

## Migrations

Create migrations from the Infrastructure project with the API project as startup project:

```bash
dotnet ef migrations add AddOrderIndex --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api
```

For controlled production deployment, generated migration scripts are often preferable (see also: `delivery-pipeline` § 3).

## Query performance

Start with clear LINQ and optimize after identifying a real problem. Before specialized optimization inspect round trips, selected columns, N+1 behavior, indexes, generated SQL, the query plan where necessary, the amount of data materialized and tracking overhead.

## Raw SQL

Raw SQL fits queries EF Core cannot express effectively or a measured or clearly demonstrated performance need. Prefer APIs that keep parameterization (`FromSql`, `FromSqlInterpolated`, `ExecuteSql`) over building SQL strings.

## Common mistakes

Loading all rows and filtering in memory; lazy loading by default; fire-and-forget EF asynchronous operations; compiled queries or raw SQL without evidence; caching tracked entities across Unit of Work boundaries.

## Decision guide

| Scenario | Technique |
|---|---|
| Read-only entity query | `AsNoTracking()` when useful |
| Read model | Database-side projection |
| Primary-key entity lookup | `FindAsync` when its semantics fit |
| Complex entity graph | Explicit `Include` / projection |
| Set-based mass update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` when appropriate |
| Normal query | Ordinary LINQ |
| Measured or clearly demonstrated hot query | Consider a compiled query |
| Several commits that succeed or fail together | Explicit transaction |
| Production schema change | Reviewed migration, controlled deployment step |
| Empty development database | Run the maintained development seeder |
| Fresh local seed dataset needed | Recreate the local database explicitly |
| Test data | Dedicated test setup (`dotnet-testing`) |
