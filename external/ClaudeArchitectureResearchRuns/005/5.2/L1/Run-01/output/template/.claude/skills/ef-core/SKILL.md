---
name: ef-core
description: >
  Use for EF Core code: AppDbContext, DbSet, entity configurations, LINQ,
  tracking, projections, paging, repository and Unit of Work implementation,
  DbSeeder, migrations, raw SQL.
---
> Level: 2-technology | Capability: persistence/ef-core (persistence.knowledge) | Owns: EF Core implementation technique and examples | Scope: backend | Loads: on demand (skill)

# Entity Framework Core

Rules: role binding, seeding, and Development configuration in
`data-access.md`; boundaries in `role-boundaries.md`. Procedures:
`persistence.workflow` (model, migration, seed changes) and
`persistence.scaffold` (initial setup). Examples use the current frame's names
(`IUnitOfWork`, `I<Entity>Repository`, the persistence implementation folder).

## DbContext and Unit of Work

`DbContext` already provides change tracking and unit-of-work behavior;
`IUnitOfWork` is the use-case-facing abstraction over the commit, and its
implementation delegates to the same scoped context.

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

internal sealed class UnitOfWork(AppDbContext db) : IUnitOfWork
{
    public Task<int> SaveChangesAsync(
        CancellationToken cancellationToken = default)
        => db.SaveChangesAsync(cancellationToken);
}
```

Keep persistence-specific configuration in `IEntityTypeConfiguration<T>`
classes rather than in entities where practical.

## Repositories

```csharp
internal sealed class OrderRepository(AppDbContext db) : IOrderRepository
{
    public Task<Order?> GetByIdAsync(Guid id, CancellationToken cancellationToken)
        => db.Orders.FirstOrDefaultAsync(x => x.Id == id, cancellationToken);

    public async Task AddAsync(Order order, CancellationToken cancellationToken)
        => await db.Orders.AddAsync(order, cancellationToken);
}
```

Repositories stage changes; the use-case unit commits through `IUnitOfWork`.
An internal base class can remove genuine duplication while concrete
repositories keep the full EF Core API:

```csharp
internal abstract class Repository<TEntity>(AppDbContext db)
    where TEntity : class
{
    protected DbSet<TEntity> Set => db.Set<TEntity>();
}
```

## Read queries and projections

Project in the database when only selected data is needed; projection is not
mandatory when the use case genuinely needs the entity. Avoid loading a whole
aggregate to return two scalar fields.

```csharp
public Task<OrderSummary?> GetSummaryAsync(Guid id, CancellationToken cancellationToken)
    => db.Orders
        .Where(x => x.Id == id)
        .Select(x => new OrderSummary(x.Id, x.Total, x.CreatedAt))
        .FirstOrDefaultAsync(cancellationToken);
```

## Tracking

Use tracking queries when loaded entities will be modified and committed in the
current unit of work; use `AsNoTracking()` for read-only entity queries where
change tracking adds nothing. Do not add `AsNoTracking()` mechanically to
projections that already produce non-entity DTOs.

## Primary-key lookups

`FindAsync` fits a primary-key lookup that needs the entity and benefits from
returning an already tracked instance:

```csharp
var order = await db.Orders.FindAsync([orderId], cancellationToken);
```

Use LINQ when predicates, projection, related data, or shaping are needed.

## Related data

Prefer an explicit query shape: projection for selected related data,
`Include`/`ThenInclude` when the graph itself is required. Avoid lazy loading by
default — it hides database access and invites N+1 queries. For large
collection includes, consider split queries and check the generated SQL.

## Pagination

Filter, order, and page in the database, always with deterministic ordering:

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

For very large or frequently traversed sets consider keyset pagination instead
of large `Skip` offsets.

## Bulk update and delete

`ExecuteUpdateAsync` / `ExecuteDeleteAsync` run set-based statements directly
against the database and bypass change tracking:

```csharp
await db.Orders
    .Where(x => x.Status == OrderStatus.Cancelled)
    .ExecuteDeleteAsync(cancellationToken);
```

Do not mix them casually with tracked entities for the same rows; understand
their transaction and consistency implications.

## Transactions

One `SaveChangesAsync` is the transaction for one operation. When a concrete
use case needs several operations or several `SaveChangesAsync` calls to succeed
atomically, use `db.Database.BeginTransactionAsync`. EF transactions do not
solve distributed transactions. With an execution strategy (transient-fault
retry), wrap the transaction in `db.Database.CreateExecutionStrategy()`.

## Compiled queries

EF Core already caches query compilation by query shape. Reserve
`EF.CompileQuery`/`EF.CompileAsyncQuery` for a measured hot path where
compilation or cache lookup overhead is material.

## Interceptors

Interceptors suit infrastructure-level cross-cutting behavior such as auditing;
never hide business behavior in them.

```csharp
internal sealed class AuditInterceptor(TimeProvider clock)
    : SaveChangesInterceptor
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

## Development seeder implementation

```csharp
internal static class DbSeeder
{
    public static async Task SeedAsync(
        AppDbContext db,
        CancellationToken cancellationToken = default)
    {
        if (await db.Projects.AnyAsync(cancellationToken))
        {
            return; // anchor entity present: leave existing data unchanged
        }

        await db.Projects.AddRangeAsync(CreateProjects(), cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
    }

    private static IReadOnlyCollection<Project> CreateProjects()
    {
        // Deterministic, representative development scenarios that match the
        // current domain and persistence model.
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

Startup wiring: `persistence.scaffold`.

## Query performance

Start with clear LINQ and optimize after identifying a real problem. Inspect
round trips, selected columns, N+1 behavior, indexes, the generated SQL
(`ToQueryString()`, logging), the query plan when needed, materialized volume,
and tracking overhead.

## Raw SQL

Use raw SQL only when EF Core cannot express the query effectively or measured
performance justifies it, and keep it parameterized:
`FromSql($"... WHERE Name = {name}")` / `FromSqlInterpolated` /
`ExecuteSql($"...")` parameterize interpolated values; never build SQL with
string concatenation (`FromSqlRaw` only with explicit parameters).

## Anti-patterns

- loading all rows and filtering in memory;
- lazy loading by default;
- fire-and-forget EF asynchronous operations or concurrent use of one context;
- caching tracked entities across units of work;
- compiled queries or raw SQL without evidence.

## Decision guide

| Scenario | Default technique |
|---|---|
| Read-only entity query | `AsNoTracking()` when useful |
| Read model | Database-side projection |
| Primary-key entity lookup | `FindAsync` when its semantics fit |
| Complex entity graph | Explicit `Include` or projection |
| Set-based mass update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` when appropriate |
| Measured extremely hot query | Consider a compiled query |
| Multiple commits requiring atomicity | Explicit transaction |
| Empty Development database | Maintained seeder (`data-access.md`) |
| Model change affecting seeded entities | `persistence.workflow` |
