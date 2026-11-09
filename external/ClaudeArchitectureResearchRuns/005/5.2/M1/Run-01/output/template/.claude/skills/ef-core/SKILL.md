---
name: ef-core
description: >
  EF Core technique: DbContext and mappings, repositories and Unit of Work,
  LINQ, AsNoTracking, Include, pagination, ExecuteUpdate, transactions, dotnet
  ef migrations, DbSeeder, SQL Server.
---

> **Knowledge skill** · Capability: persistence/ef-core · Owns: EF Core and SQL Server technique and examples · Scope: backend · Loading: on demand

# Entity Framework Core

## Role in the Architecture

Rules: the frame's boundary rules (`architecture-style.md`) and this capability's
rule facet (`persistence-technology.md`). This skill shows how to implement them
with EF Core.

Application defines persistence contracts such as specific repository interfaces
and `IUnitOfWork`; Infrastructure implements them using EF Core.

EF Core's `DbContext` already provides change tracking and unit-of-work behavior
internally. `IUnitOfWork` is the Application-facing abstraction over the commit
boundary; its Infrastructure implementation delegates to the same `DbContext`.

## Packages and Tooling

```text
Microsoft.EntityFrameworkCore.SqlServer   adapter-layer project
Microsoft.EntityFrameworkCore.Design      composition-root project (design-time services for dotnet ef)
dotnet-ef                                 local or global .NET tool
```

Resolve versions through `add-dependency`.

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

Use the provider variant recorded in `docs/capability-selection.md`. Do not add a
provider merely because it appears in an example.

## Specific Repositories

Implement Application repository interfaces in Infrastructure.

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

Repositories stage changes; the commit happens through the Unit of Work
(`architecture-style.md` → Unit of Work).

## Unit of Work Implementation

The Unit of Work normally represents the Application-facing commit boundary.

Repositories are injected independently and participate in the same Unit of Work
by sharing the same scoped `AppDbContext`.

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

## Generic Repository

A generic repository may be used internally in Infrastructure to remove genuine
implementation duplication.

```csharp
internal abstract class Repository<TEntity>(AppDbContext db)
    where TEntity : class
{
    protected DbSet<TEntity> Set => db.Set<TEntity>();
}
```

Concrete repositories may use the full EF Core API internally rather than forcing
complex queries through a generic CRUD abstraction.

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

Projection is not mandatory when the use case genuinely needs the entity.

Avoid loading a complete aggregate only to return two scalar fields.

## Tracking

Use tracking intentionally.

Use normal tracking queries when loaded entities will be modified and committed
through the current Unit of Work.

Use `AsNoTracking()` for read-only entity queries where change tracking provides
no value.

Do not add `AsNoTracking()` mechanically to projections that already produce
non-entity DTOs.

## Primary-Key Lookups

`FindAsync` is appropriate when:

- querying by primary key;
- an entity instance is required;
- returning an already tracked entity is desirable.

```csharp
var order = await db.Orders.FindAsync(
    [orderId],
    cancellationToken);
```

Use LINQ when additional predicates, projection, related data, or query shaping
are required.

## Related Data

Prefer explicit query shape.

Use projection when only selected related data is needed.

Use `Include` / `ThenInclude` when an entity graph itself is required.

Avoid lazy loading by default because it hides database access and can cause
N+1 queries.

For large collection includes, consider split queries when appropriate and
verify the generated SQL and performance characteristics.

## Pagination

Apply filtering, ordering, and pagination in the database.

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

Always use deterministic ordering for paged queries.

For very large or frequently traversed datasets, consider keyset pagination
instead of large `Skip` offsets when justified.

## Bulk Update and Delete

`ExecuteUpdateAsync` and `ExecuteDeleteAsync` can be useful for set-based
operations.

```csharp
await db.Orders
    .Where(x => x.Status == OrderStatus.Cancelled)
    .ExecuteDeleteAsync(cancellationToken);
```

These operations execute directly against the database and bypass normal change
tracking.

Do not mix them casually with tracked entities representing the same rows.
Understand their transaction and consistency implications before using them.

## Transactions

A single `SaveChangesAsync` is normally sufficient as the transaction boundary
for one application operation.

When a concrete use case requires multiple database operations or multiple
`SaveChangesAsync` calls to succeed atomically, use an explicit transaction:

```csharp
await using var transaction =
    await db.Database.BeginTransactionAsync(cancellationToken);

// ... several SaveChangesAsync calls ...

await transaction.CommitAsync(cancellationToken);
```

With SQL Server retrying execution strategies, wrap the transaction in
`db.Database.CreateExecutionStrategy().ExecuteAsync(...)`.

Do not attempt to solve distributed transactions with EF transaction APIs.

## Compiled Queries

Normal EF Core LINQ is the default.

EF Core already caches query compilation based on query shape.

Use `EF.CompileQuery` or `EF.CompileAsyncQuery` only for a measured hot path
where profiling demonstrates that query compilation/cache lookup overhead is
material.

Do not introduce compiled queries merely because a query executes frequently.

## Interceptors

Use EF Core interceptors for infrastructure-level cross-cutting behavior when
they provide a clear benefit, for example auditing.

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

## Development Data Seeding

Rules: `persistence-technology.md` → Development Seeding. Keeping the seeder in
step with model changes: `development-workflow` → Change-Specific Obligations.

Keep development seeding in a dedicated file:

```text
Persistence/
  Seeding/
    DbSeeder.cs
    DatabaseInitializationExtensions.cs
```

For a new local database, the developer first applies the current migrations;
application startup then populates the empty schema with Development seed data.
When a developer needs the latest seed dataset in an existing local database, the
database is dropped and recreated explicitly.

Detect existing development data through one or more representative root/anchor
entities:

```csharp
if (await db.Projects.AnyAsync(cancellationToken))
{
    return;
}
```

Representative states usually worth covering: newly created; active or in
progress; completed; inactive or archived; with and without optional values;
with and without optional relationships; representative status values; meaningful
boundary states.

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

The concrete seed entities and states must match the actual current Domain and
persistence model.

### Startup

Invoke the seeder from the composition root inside the Development check, through
the narrow Infrastructure initialization extension:

```csharp
if (app.Environment.IsDevelopment())
{
    await app.Services.SeedDevelopmentDataAsync();
}
```

The Infrastructure extension creates the required scope and delegates to the
internal `DbSeeder`. Migration strategy is separate from development data
seeding.

## Migrations

Create migrations from the Infrastructure project using the API project as the
startup project:

```bash
dotnet ef migrations add AddOrderIndex --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api
```

Apply them to a local database with:

```bash
dotnet ef database update --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api
```

Reviewing generated migrations and updating the seeder in the same change are
`development-workflow` obligations. After the change, recreating an empty
development database should produce seed data valid for the migrated schema and
current Domain model.

For controlled production deployment, generated idempotent migration scripts are
often preferable:

```bash
dotnet ef migrations script --idempotent --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api --output artifacts/migrations.sql
```

Production migration as a deployment step: `development-workflow` →
Change-Specific Obligations.

## Database Resilience

Do not wrap normal EF Core operations in a generic application-level retry or
resilience pipeline. When transient retry is needed, prefer the provider's EF
Core execution strategy (`options.UseSqlServer(connectionString, sql =>
sql.EnableRetryOnFailure())`) and handle transaction/retry interaction according
to the provider's EF Core guidance. An HTTP retry policy is not appropriate for
database operations.

## Testing Against the Provider

The InMemory provider does not reproduce relational behavior (constraints,
transactions, collation, SQL translation). For provider-fidelity tests use SQL
Server — LocalDB for local runs or the Testcontainers MsSql module when isolated
real-provider tests are justified — and recreate or reset the test database per
suite.

## Logging

EF Core logs under the `Microsoft.EntityFrameworkCore` category; raise its minimum
level (for example `Warning`) in provider configuration to reduce noise.

## Query Performance

Start with clear normal LINQ.

Optimize after identifying a real problem.

Before introducing specialized optimization, inspect:

- number of database round trips;
- selected columns;
- N+1 behavior;
- indexes;
- generated SQL;
- query plan where necessary;
- amount of data materialized;
- tracking overhead.

Measured-optimization policy: `performance.md`.

## Raw SQL

Use raw SQL only when EF Core cannot express the query effectively or measured
performance justifies it.

EF Core LINQ parameterizes values automatically. For raw SQL, prefer
`FromSql`/`FromSqlInterpolated`/`ExecuteSql` with interpolated parameters, which
preserve parameterization (`security.md` → SQL and Persistence).

## Anti-Patterns

Avoid:

- loading all rows and filtering in memory when the database can filter;
- lazy loading by default;
- fire-and-forget EF asynchronous operations;
- adding `AsNoTracking()` mechanically to non-entity projections;
- mixing `ExecuteUpdateAsync`/`ExecuteDeleteAsync` with tracked entities for the
  same rows;
- introducing raw SQL merely to appear more performant.

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
| Measured extremely hot query | Consider compiled query |
| Multiple commits requiring atomicity | Explicit transaction |
| Transient database faults | Provider execution strategy |
| Production schema change | Reviewed migration / idempotent script in a controlled deployment |
| Need fresh local seed dataset | Developer explicitly recreates the local database |
