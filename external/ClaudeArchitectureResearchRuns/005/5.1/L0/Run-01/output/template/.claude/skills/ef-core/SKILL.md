---
name: ef-core
description: >
  Use when writing or reviewing EF Core persistence: DbContext and
  configurations, repositories, UnitOfWork, LINQ queries, tracking, pagination,
  transactions, raw SQL, migrations, development seeder.
---

> Level: 2 Technology · Owns: EF Core implementation technique · Scope: backend · Loads: on demand (knowledge skill)

# EF Core

Policy owners: `.claude/rules/1-architecture/persistence-boundary.md` (repositories, unit of work, boundary), `.claude/rules/2-technology/ef-core.md` (bindings, migration review), `.claude/rules/0-core/runtime-principles.md` (data-access efficiency, measured optimization), `.claude/rules/0-core/security-principles.md` (parameterization). Seeding and production-migration policy are project rules (see `.claude/INSTRUCTION-MAP.md`); this skill shows the mechanics.

## DbContext configuration

Keep entity configuration in `IEntityTypeConfiguration<T>` classes, out of Domain entities where practical.

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

Use the provider the project selected; do not add a provider because it appears in an example.

## Repositories and Unit of Work

```csharp
internal sealed class OrderRepository(AppDbContext db) : IOrderRepository
{
    public Task<Order?> GetByIdAsync(Guid id, CancellationToken cancellationToken) =>
        db.Orders.FirstOrDefaultAsync(x => x.Id == id, cancellationToken);

    public async Task AddAsync(Order order, CancellationToken cancellationToken) =>
        await db.Orders.AddAsync(order, cancellationToken);   // staged; committed by IUnitOfWork
}

internal sealed class UnitOfWork(AppDbContext db) : IUnitOfWork
{
    public Task<int> SaveChangesAsync(CancellationToken cancellationToken = default) =>
        db.SaveChangesAsync(cancellationToken);
}
```

`DbContext` already tracks changes and acts as a unit of work; `IUnitOfWork` is the Application-facing commit abstraction over the same scoped context. An Infrastructure-only base class may remove real duplication:

```csharp
internal abstract class Repository<TEntity>(AppDbContext db) where TEntity : class
{
    protected DbSet<TEntity> Set => db.Set<TEntity>();
}
```

Concrete repositories may use the full EF Core API internally; do not force complex queries through a generic CRUD abstraction.

## Read queries and projections

Prefer database-side projection when a read needs only selected data:

```csharp
public Task<OrderSummary?> GetSummaryAsync(Guid id, CancellationToken cancellationToken) =>
    db.Orders
        .Where(x => x.Id == id)
        .Select(x => new OrderSummary(x.Id, x.Total, x.CreatedAt))
        .FirstOrDefaultAsync(cancellationToken);
```

Projection is not mandatory when the use case genuinely needs the entity; avoid loading a full aggregate to return two scalars.

## Tracking

- Tracking queries when loaded entities will be modified and committed through the current unit of work.
- `AsNoTracking()` for read-only entity queries where tracking adds nothing; not needed on projections to non-entity DTOs.
- `FindAsync([id], cancellationToken)` fits primary-key lookups where an entity instance is needed and an already-tracked instance is acceptable; use LINQ when predicates, projection or related data are required.

## Related data

Prefer an explicit query shape: projection for selected related data, `Include`/`ThenInclude` when the entity graph itself is needed. Avoid lazy loading by default — it hides database access and causes N+1 queries. For large collection includes, consider `AsSplitQuery()` and check the generated SQL.

## Pagination

```csharp
var query = db.Orders
    .Where(x => x.CustomerId == customerId)
    .OrderByDescending(x => x.CreatedAt)
    .ThenBy(x => x.Id);                       // deterministic ordering

var totalCount = await query.CountAsync(cancellationToken);

var items = await query
    .Skip((page - 1) * pageSize)
    .Take(pageSize)
    .Select(x => new OrderSummary(x.Id, x.Total, x.CreatedAt))
    .ToListAsync(cancellationToken);
```

For very large or frequently traversed sets, consider keyset pagination instead of large `Skip` offsets.

## Bulk update and delete

```csharp
await db.Orders
    .Where(x => x.Status == OrderStatus.Cancelled)
    .ExecuteDeleteAsync(cancellationToken);
```

`ExecuteUpdateAsync`/`ExecuteDeleteAsync` run directly against the database and bypass change tracking — do not mix them casually with tracked entities for the same rows, and understand their transaction implications.

## Transactions

One `SaveChangesAsync` is the transaction for a normal operation. When a concrete use case needs several commits to succeed atomically:

```csharp
await using var transaction = await db.Database.BeginTransactionAsync(cancellationToken);
// ... multiple SaveChangesAsync calls ...
await transaction.CommitAsync(cancellationToken);
```

With a retrying execution strategy, wrap the transaction in `db.Database.CreateExecutionStrategy().ExecuteAsync(...)`. EF transactions do not solve distributed transactions.

## Compiled queries

EF Core caches query compilation by shape. `EF.CompileAsyncQuery` helps only on a measured hot path where compilation or cache lookup is material.

## Interceptors

Interceptors suit infrastructure cross-cutting behavior such as auditing — never business behavior.

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

## Raw SQL

Use raw SQL only when LINQ cannot express the query well or measurement justifies it, through parameter-preserving APIs:

```csharp
var orders = await db.Orders
    .FromSql($"SELECT * FROM Orders WHERE CustomerId = {customerId}")   // interpolation becomes a parameter
    .ToListAsync(cancellationToken);
```

`FromSqlRaw`/`ExecuteSqlRaw` do not parameterize a concatenated or pre-formatted string — pass values as separate parameters (`DbParameter` or positional `{0}` arguments).

## Development seeding mechanics

Dedicated internal seeder plus a narrow initialization extension; the anchor-entity check keeps existing data untouched:

```csharp
internal static class DbSeeder
{
    public static async Task SeedAsync(AppDbContext db, CancellationToken cancellationToken = default)
    {
        if (await db.Projects.AnyAsync(cancellationToken))
            return;                                   // existing data stays unchanged

        await db.Projects.AddRangeAsync(CreateProjects(), cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
    }

    private static IReadOnlyCollection<Project> CreateProjects()
    {
        // Deterministic, representative scenarios that match the current Domain model.
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

Startup call (Api):

```csharp
if (app.Environment.IsDevelopment())
{
    await app.Services.SeedDevelopmentDataAsync();
}
```

Typical local flow: `dotnet ef database update` brings the schema to the current migration, then a Development startup seeds the empty database. For a fresh dataset: `dotnet ef database drop`, then `dotnet ef database update`, then start the application.

## Migrations

```bash
dotnet ef migrations add AddOrderIndex --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api
dotnet ef database update --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api      # local Development
dotnet ef migrations script --idempotent --project backend/<Name>.Infrastructure --startup-project backend/<Name>.Api -o artifacts/migrate.sql
```

`dotnet ef` needs the `dotnet-ef` tool (install through `add-dependency`, preferably as a local tool) and `Microsoft.EntityFrameworkCore.Design` in the startup project. Review technique: read the generated `Up`/`Down` code and the model-snapshot diff, look for `DropColumn`/`AddColumn` pairs that should be renames, check `onDelete` behavior and index changes, and inspect `migrationBuilder.Sql(...)` data steps. When the migration touches seeded entities, the project's data-lifecycle rule applies. Idempotent scripts suit controlled production deployment.

## Query performance checklist

Before optimizing, inspect: round trips, selected columns, N+1 behavior, indexes, generated SQL (`ToQueryString()`, logging), query plans where needed, materialized row counts, tracking overhead.

## Decision guide

| Scenario | Typical choice |
|---|---|
| Read-only entity query | `AsNoTracking()` when useful |
| Read model | Database-side projection |
| Primary-key entity lookup | `FindAsync` when its semantics fit |
| Complex entity graph | Explicit `Include` or projection; split query for large collections |
| Set-based mass update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` |
| Several commits that must be atomic | Explicit transaction (inside the execution strategy when retrying) |
| Measured extremely hot query | Compiled query |
| Production schema change | Reviewed migration, idempotent script, controlled deployment |
| Fresh local seed dataset | Drop and recreate the local database |
