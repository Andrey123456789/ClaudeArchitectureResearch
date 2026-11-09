---
name: ef-core
description: Use when writing or reviewing EF Core code — AppDbContext and entity configuration, repository and Unit of Work implementations, LINQ queries, tracking, projections, pagination, bulk updates, transactions, compiled queries, interceptors, DbSeeder seeding, migrations, SQL Server specifics or query performance.
---
Kind: KNW | Scope: backend | Capability: persistence/ef-core | Loading: on invocation

# EF Core (SQL Server)

Technique for the persistence implementation. Rules: `.claude/rules/backend/persistence-technology.md` (EF Core boundary, seeder placement, development configuration), `.claude/rules/backend/persistence.md` (data access efficiency, seed data), `.claude/rules/backend/architecture-style.md` (repositories, Unit of Work). Procedures (setup, migrations, schema changes): the persistence workflow facet `.claude/capabilities/persistence/ef-core/workflow-facet.md`.

## Role in the architecture

Application defines persistence contracts (specific repository interfaces and `IUnitOfWork`); Infrastructure implements them with EF Core. `DbContext` already provides change tracking and unit-of-work behavior internally; `IUnitOfWork` is the Application-facing abstraction over the commit boundary, and its Infrastructure implementation delegates to the same scoped `DbContext`.

## DbContext configuration

Keep entity configuration separate with `IEntityTypeConfiguration<T>` and keep persistence-specific configuration out of Domain entities where practical.

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

String columns: SQL Server compares strings using the column or database collation (commonly case-insensitive). When product sources define comparison semantics, configure them explicitly (`UseCollation(...)` on the property or model); when they do not, the choice is a product decision (`CLAUDE.md` → Product behavior).

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

## Specific repositories

```csharp
internal sealed class OrderRepository(AppDbContext db) : IOrderRepository
{
    public Task<Order?> GetByIdAsync(Guid id, CancellationToken cancellationToken)
        => db.Orders.FirstOrDefaultAsync(x => x.Id == id, cancellationToken);

    public async Task AddAsync(Order order, CancellationToken cancellationToken)
        => await db.Orders.AddAsync(order, cancellationToken);
}
```

Repositories stage changes; the commit happens through `IUnitOfWork` (`architecture-style.md` → Unit of Work).

## Unit of Work implementation

```csharp
internal sealed class UnitOfWork(AppDbContext db) : IUnitOfWork
{
    public Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
        => db.SaveChangesAsync(cancellationToken);
}
```

Repositories participate in the same Unit of Work by sharing the same scoped `AppDbContext`.

## Infrastructure-only generic base

When a base class removes genuine duplication between concrete repositories:

```csharp
internal abstract class Repository<TEntity>(AppDbContext db) where TEntity : class
{
    protected DbSet<TEntity> Set => db.Set<TEntity>();
}
```

Complex queries stay in the concrete repositories, which may use the full EF Core API.

## Read queries and projections

Prefer database-side projection for read-only queries that need selected data; avoid loading a complete aggregate to return two scalar fields. Projection is not mandatory when the use case genuinely needs the entity.

```csharp
public Task<OrderSummary?> GetSummaryAsync(Guid id, CancellationToken cancellationToken)
    => db.Orders
        .Where(x => x.Id == id)
        .Select(x => new OrderSummary(x.Id, x.Total, x.CreatedAt))
        .FirstOrDefaultAsync(cancellationToken);
```

## Tracking

Use tracking queries when loaded entities will be modified and committed through the current Unit of Work. Use `AsNoTracking()` for read-only entity queries where change tracking adds nothing. Do not add `AsNoTracking()` mechanically to projections that already produce non-entity DTOs.

## Primary-key lookups

`FindAsync` fits when querying by primary key, an entity instance is required, and returning an already tracked entity is desirable. Use LINQ when predicates, projection, related data or query shaping are needed.

```csharp
var order = await db.Orders.FindAsync([orderId], cancellationToken);
```

## Related data

Prefer an explicit query shape: projection for selected related data, `Include`/`ThenInclude` when the entity graph itself is required. Avoid lazy loading by default because it hides database access and causes N+1 queries. For large collection includes, consider split queries and verify the generated SQL.

## Pagination

Filter, order and paginate in the database, always with deterministic ordering. For very large or frequently traversed datasets, consider keyset pagination instead of large `Skip` offsets.

```csharp
var query = db.Orders
    .Where(x => x.CustomerId == customerId)
    .OrderByDescending(x => x.CreatedAt)
    .ThenBy(x => x.Id);

var totalCount = await query.CountAsync(cancellationToken);

var items = await query
    .Skip((page - 1) * pageSize)
    .Take(pageSize)
    .Select(x => new OrderSummary(x.Id, x.Total, x.CreatedAt))
    .ToListAsync(cancellationToken);
```

## Bulk update and delete

`ExecuteUpdateAsync` and `ExecuteDeleteAsync` run set-based operations directly in the database and bypass change tracking. Do not mix them casually with tracked entities representing the same rows, and understand their transaction and consistency implications.

```csharp
await db.Orders
    .Where(x => x.Status == OrderStatus.Cancelled)
    .ExecuteDeleteAsync(cancellationToken);
```

## Transactions

A single `SaveChangesAsync` is normally the transaction boundary of one application operation. When a concrete use case needs several database operations or several `SaveChangesAsync` calls to succeed atomically, use `db.Database.BeginTransactionAsync(...)` (or an execution-strategy-aware transaction, see Transient failures). EF transaction APIs do not solve distributed transactions.

## Transient failures

For SQL Server transient faults, prefer the provider's execution strategy over generic application-level retry pipelines:

```csharp
options.UseSqlServer(connectionString, sql => sql.EnableRetryOnFailure());
```

With a retrying execution strategy, wrap user-initiated transactions in `db.Database.CreateExecutionStrategy().ExecuteAsync(...)`. Do not wrap normal EF Core operations in an HTTP-style resilience pipeline.

## Compiled queries

Normal LINQ is the default; EF Core already caches query compilation by query shape. `EF.CompileQuery`/`EF.CompileAsyncQuery` are for a measured hot path where profiling shows compilation or cache-lookup overhead is material (`performance.md`).

## Interceptors

Interceptors suit infrastructure-level cross-cutting behavior such as auditing. Do not hide business behavior in persistence interceptors.

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

## Development seeding

Rules: `persistence.md` → Development seed data and `persistence-technology.md` → Development seeding. Technique:

- Use one or more representative root or anchor entities to detect whether development data already exists, and return early if it does.
- Build the dataset with deterministic values (fixed identifiers and dates) so behavior stays predictable between database recreations; what the dataset must cover is defined in `persistence.md`.
- The concrete seed entities and states must match the current Domain and persistence model; review `DbSeeder` together with any migration that changes seeded entities.

```csharp
internal static class DbSeeder
{
    public static async Task SeedAsync(AppDbContext db, CancellationToken cancellationToken = default)
    {
        if (await db.Projects.AnyAsync(cancellationToken))
        {
            return;
        }

        await db.Projects.AddRangeAsync(CreateProjects(), cancellationToken);
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
        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        await DbSeeder.SeedAsync(db, cancellationToken);
    }
}
```

Startup (Api `Program.cs`):

```csharp
if (app.Environment.IsDevelopment())
{
    await app.Services.SeedDevelopmentDataAsync();
}
```

## Query performance

Start with clear LINQ and optimize after identifying a real problem. Before specialized optimization, inspect round trips, selected columns, N+1 behavior, indexes, the generated SQL (`ToQueryString()`, logging), the query plan where necessary, the amount of materialized data and tracking overhead.

To inspect generated SQL in Development, raise the `Microsoft.EntityFrameworkCore.Database.Command` logging category (for example through Serilog `MinimumLevel.Override`); keep it quiet in Production.

## Raw SQL

Use raw SQL only when EF Core cannot express the query effectively or measured performance justifies it. `FromSql`, `FromSqlInterpolated` and `ExecuteSql` with interpolated values create parameters; `FromSqlRaw` and `ExecuteSqlRaw` need explicit parameters and must never receive concatenated untrusted input (`.claude/rules/backend/security.md`).

## Testing implications

- Provider fidelity means SQL Server: use a real SQL Server instance (for example a Testcontainers SQL Server container or LocalDB) when constraints, transactions, locking, indexes, raw SQL, collations, provider mappings or migrations are what the test proves.
- EF Core InMemory is not relational and does not demonstrate SQL Server behavior; for true unit tests a fake repository is usually clearer.
- Persistence tests are worth writing for custom mappings, query filters, projections, non-trivial queries, relationships, concurrency and provider-specific behavior, not for every trivial `Add`/`Get`.

## Anti-patterns

Review checks; the named standard owns each rule:

- `DbContext`, `DbSet<T>`, `IQueryable<T>` or a generic CRUD contract visible to Application? (`architecture-style.md` → Repositories)
- A repository committing on its own? (`architecture-style.md` → Unit of Work)
- In-memory filtering of data the database could filter? (`persistence.md` → Data access efficiency)
- Lazy loading enabled by default, or fire-and-forget EF asynchronous operations (EF Core does not support concurrent operations on one context)?
- Compiled queries or raw SQL without evidence? (`performance.md`)
- A seeder that migrates, patches or overwrites a database, or runs outside Development? (`persistence.md`, `persistence-technology.md`)

## Technique quick reference

| Scenario | Technique |
|---|---|
| Read-only entity query | `AsNoTracking()` when useful |
| Read model | Database-side projection with `Select` |
| Primary-key entity lookup | `FindAsync` when its semantics fit |
| Complex entity graph | Explicit `Include` / `ThenInclude` or projection; split queries for large collections |
| Set-based mass update or delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` |
| Measured extremely hot query | `EF.CompileAsyncQuery` |
| Several commits that must be atomic | `BeginTransactionAsync` inside the execution strategy |
| Transient SQL Server faults | `EnableRetryOnFailure` |
| Inspect generated SQL | `ToQueryString()` or command logging in Development |
