---
name: ef-core
description: >
  Use for EF Core code: AppDbContext and mappings, repository and Unit of Work
  implementations, LINQ, tracking, projections, pagination, bulk updates,
  transactions, raw SQL, DbSeeder, SQL Server setup.
---

> Capability: persistence/ef-core · Knowledge skill · Technique only · Policy: `.claude/rules/persistence-technology.md`, `.claude/rules/architecture.md`, `.claude/rules/performance.md` · Procedure: `persistence-change`

# Entity Framework Core

## Role in the Architecture

EF Core lives in the adapter layer. The use-case layer defines persistence
contracts — specific repository interfaces and `IUnitOfWork` — and the adapter
layer implements them with EF Core.

`DbContext` already provides change tracking and unit-of-work behavior.
`IUnitOfWork` is the use-case-facing abstraction over the commit boundary; its
adapter-layer implementation delegates to the same scoped `AppDbContext`.

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

Keep persistence-specific configuration out of core-model entities where
practical.

## Registration (provider variant: SQL Server)

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

Use the provider recorded in `docs/capability-selection.md`; do not add another
provider merely because it appears in an example.

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

Repositories stage changes; committing is the Unit of Work's job
(`architecture.md` § Unit of Work).

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

The Unit of Work and the repositories of one use case work on the same scoped
`AppDbContext` (`persistence-technology.md` § Technology Boundary).

## Persistence Layout

```text
<adapter-layer project>/
  Persistence/
    AppDbContext.cs
    UnitOfWork.cs
    Configurations/
    Repositories/
    Migrations/
    Seeding/
      DbSeeder.cs
      DatabaseInitializationExtensions.cs
```

## Generic Repository Base

```csharp
internal abstract class Repository<TEntity>(AppDbContext db)
    where TEntity : class
{
    protected DbSet<TEntity> Set => db.Set<TEntity>();
}
```

Concrete repositories may use the full EF Core API internally; do not force
complex queries through a generic CRUD abstraction.

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

Projection is not mandatory when the use case genuinely needs the entity; avoid
loading a complete aggregate only to return two scalar fields.

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
needed, `Include`/`ThenInclude` when the entity graph itself is required. Avoid
lazy loading by default because it hides database access and causes N+1
queries. For large collection includes, consider split queries and verify the
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

For very large or frequently traversed datasets, consider keyset pagination
instead of large `Skip` offsets when justified.

## Bulk Update and Delete

`ExecuteUpdateAsync` and `ExecuteDeleteAsync` suit set-based operations:

```csharp
await db.Orders
    .Where(x => x.Status == OrderStatus.Cancelled)
    .ExecuteDeleteAsync(cancellationToken);
```

They execute directly against the database and bypass change tracking; do not
mix them casually with tracked entities representing the same rows, and
understand their transaction and consistency implications.

## Transactions

An explicit transaction fits when a concrete use case needs multiple database
operations or multiple `SaveChangesAsync` calls to succeed atomically
(`persistence-technology.md` § Transactions). Do not attempt to solve
distributed transactions with EF Core transaction APIs.

## Compiled Queries

Normal LINQ is the default; EF Core already caches query compilation by query
shape. `EF.CompileQuery` / `EF.CompileAsyncQuery` fit only a measured hot path
where profiling shows compilation or cache-lookup overhead is material.

## Interceptors

Interceptors suit infrastructure-level cross-cutting behavior such as
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

## Development Seeding Technique

Seeding policy: `persistence-technology.md` § Development Seeding. Location:
`Persistence/Seeding/` (Persistence Layout above).

Use one or more representative root/anchor entities to detect existing data.
Representative scenarios, where applicable: newly created, active or in
progress, completed, inactive or archived, with and without optional values or
relationships, representative status values, meaningful boundary states. When
the required graph is complex, the task requirements should describe the
dataset explicitly rather than inventing a large generic object graph.

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

Startup wiring in the composition root:

```csharp
if (app.Environment.IsDevelopment())
{
    await app.Services.SeedDevelopmentDataAsync();
}
```

The concrete seed entities and states must match the current Domain and
persistence model. For a new local database the developer applies the current
migrations first; application startup then populates the empty schema.

## Migrations

Commands and the review checklist: `persistence-change` § Migrations; seed
co-change: `persistence-change` § Seed Data. For controlled production deployment, generated migration scripts
(`dotnet ef migrations script --idempotent`) are often preferable; production
migration runs as an explicit deployment step.

## Query Performance

Start with clear LINQ and optimize after identifying a real problem. Inspect
database round trips, selected columns, N+1 behavior, indexes, generated SQL,
the query plan where necessary, materialized data volume, and tracking
overhead before introducing specialized optimization.

## Raw SQL

Use raw SQL only when EF Core cannot express the query effectively or measured
performance justifies it. EF Core LINQ parameterizes values automatically; for
raw SQL prefer `FromSql`/`FromSqlInterpolated`/`ExecuteSql` forms that
preserve parameterization over string concatenation.

## Project Setup

- Packages (through `add-dependency`): `Microsoft.EntityFrameworkCore.SqlServer`
  in the adapter-layer project; `Microsoft.EntityFrameworkCore.Design` in the
  startup project when migrations are created from the CLI; the `dotnet-ef`
  tool.
- Local Development connection string in `appsettings.Development.json` (adapt
  the database name):

  ```json
  {
    "ConnectionStrings": {
      "DefaultConnection": "Server=(localdb)\\MSSQLLocalDB;Database=ProjectName;Trusted_Connection=True;TrustServerCertificate=True;"
    }
  }
  ```

- Keep `appsettings.json` free of secrets; credential-bearing values go to
  user-secrets.

## Review Checks

Check-by-reference against `persistence-technology.md` and `architecture.md`:
`DbContext`, `DbSet<T>`, or EF-backed `IQueryable<T>` exposed outside the
adapter layer; the use-case layer depending on EF Core; a generic CRUD contract
exposed to the use-case layer; `SaveChangesAsync` called from every repository
operation; all rows loaded and filtered in memory; lazy loading by default;
fire-and-forget EF asynchronous operations; compiled queries or raw SQL without
evidence; development seeding outside Development, silently patching an
existing database, or left stale after a model change.

## Decision Guide

| Scenario | Default |
|---|---|
| Use-case persistence dependency | Specific repository interface |
| Commit application changes | `IUnitOfWork.SaveChangesAsync` |
| Repository implementation | EF Core inside the adapter layer |
| Read-only entity query | `AsNoTracking()` when useful |
| Read model | Database-side projection |
| Primary-key entity lookup | `FindAsync` when its semantics fit |
| Complex entity graph | Explicit `Include` / projection |
| Set-based mass update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` when appropriate |
| Measured extremely hot query | Consider a compiled query |
| Multiple commits requiring atomicity | Explicit transaction |
| Production schema change | Reviewed migration / controlled deployment |
| Empty development database | Run the maintained development seeder |
| Existing development database | Leave seed data unchanged |
| Need a fresh local seed dataset | Recreate the local database explicitly |
| Test data | Dedicated test setup, not development seeding |
