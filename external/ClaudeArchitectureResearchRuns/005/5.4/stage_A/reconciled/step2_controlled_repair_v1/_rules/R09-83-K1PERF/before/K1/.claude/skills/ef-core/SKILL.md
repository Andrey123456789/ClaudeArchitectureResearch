---
name: ef-core
description: >
  Use when writing or reviewing EF Core code: DbContext, entity configurations,
  LINQ queries, tracking, includes, pagination, transactions, migrations,
  seeding code, raw SQL, SQL Server provider, EF Core tests.
---

> Kind: KNW | Scope: backend | Capability: persistence/ef-core | Loading: on-demand knowledge

# Entity Framework Core

Policy: `.claude/rules/backend/persistence.md`, `.claude/rules/backend/persistence-technology.md`, `.claude/rules/backend/runtime.md`. Procedure for model, migration, and seed changes: `persistence-change`.

## Role in the architecture

Application defines the persistence contracts (specific repository interfaces and `IUnitOfWork`); Infrastructure implements them with EF Core. `DbContext` already provides change tracking and unit-of-work behavior internally; `IUnitOfWork` is the Application-facing abstraction over that commit boundary, and its implementation delegates to the same scoped `DbContext`.

## DbContext configuration

Keep entity configuration in separate `IEntityTypeConfiguration<T>` classes and keep persistence-specific configuration out of Domain entities where practical.

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

`AddDbContext` registers the context as scoped, so repositories and the Unit of Work in one request share it. Use the provider the project actually selected; never add a provider because an example shows it.

## Repositories and Unit of Work

```csharp
internal sealed class OrderRepository(AppDbContext db) : IOrderRepository
{
    public Task<Order?> GetByIdAsync(Guid id, CancellationToken cancellationToken) =>
        db.Orders.FirstOrDefaultAsync(x => x.Id == id, cancellationToken);

    public async Task AddAsync(Order order, CancellationToken cancellationToken) =>
        await db.Orders.AddAsync(order, cancellationToken);
}

internal sealed class UnitOfWork(AppDbContext db) : IUnitOfWork
{
    public Task<int> SaveChangesAsync(CancellationToken cancellationToken = default) =>
        db.SaveChangesAsync(cancellationToken);
}
```

Repositories stage changes; the Application Service calls `IUnitOfWork.SaveChangesAsync` once the operation is ready. An Infrastructure-only base class can remove genuine duplication without becoming a generic CRUD contract; concrete repositories keep the full EF Core API for use-case-specific queries:

```csharp
internal abstract class Repository<TEntity>(AppDbContext db) where TEntity : class
{
    protected DbSet<TEntity> Set => db.Set<TEntity>();
}
```

## Queries

- **Projection:** for read-only queries that need selected data, project in the database; projection is not mandatory when the use case needs the entity. Avoid loading a complete aggregate to return two scalar fields.

  ```csharp
  db.Orders.Where(x => x.Id == id)
      .Select(x => new OrderSummary(x.Id, x.Total, x.CreatedAt))
      .FirstOrDefaultAsync(cancellationToken);
  ```

- **Tracking:** use tracking queries when loaded entities will be modified and committed through the current Unit of Work; `AsNoTracking()` for read-only entity queries where tracking adds nothing. Do not add `AsNoTracking()` mechanically to projections that already produce non-entity DTOs.
- **Primary-key lookups:** `FindAsync([orderId], cancellationToken)` fits a key lookup that needs an entity instance and may return an already tracked one; use LINQ for extra predicates, projection, related data, or shaping.
- **Related data:** prefer an explicit query shape — projection for selected related data, `Include`/`ThenInclude` when the entity graph itself is needed. Avoid lazy loading by default (it hides database access and causes N+1 queries). For large collection includes consider split queries and verify the generated SQL.
- **Pagination:** filter, order, and page in the database, always with deterministic ordering; consider keyset pagination for very large or frequently traversed datasets.

  ```csharp
  var query = db.Orders.Where(x => x.CustomerId == customerId).OrderByDescending(x => x.CreatedAt);
  var totalCount = await query.CountAsync(cancellationToken);
  var items = await query.Skip((page - 1) * pageSize).Take(pageSize)
      .Select(x => new OrderSummary(x.Id, x.Total, x.CreatedAt))
      .ToListAsync(cancellationToken);
  ```

- **Bulk update/delete:** `ExecuteUpdateAsync`/`ExecuteDeleteAsync` run directly against the database and bypass change tracking; do not mix them casually with tracked entities for the same rows, and understand their transaction and consistency implications.
- **Never fire-and-forget** EF Core asynchronous operations; a `DbContext` is not thread-safe.

## Transactions

One `SaveChangesAsync` is normally the transaction boundary of an application operation. Use an explicit transaction (`db.Database.BeginTransactionAsync`) only when a concrete use case needs several database operations or `SaveChangesAsync` calls to succeed atomically; EF transaction APIs do not solve distributed transactions.

## Compiled queries and performance

EF Core already caches query compilation by query shape. `EF.CompileQuery`/`EF.CompileAsyncQuery` fit only a measured hot path where compilation/cache lookup overhead is material. Before specialized optimization inspect round trips, selected columns, N+1 behavior, indexes, generated SQL, the query plan where necessary, materialized data volume, and tracking overhead.

## Interceptors

Use interceptors for infrastructure-level cross-cutting behavior with a clear benefit, such as auditing; never hide business behavior in them.

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

## Development seeding code

Use one or more representative root/anchor entities to detect existing data; keep the seeder internal and expose a narrow extension that creates the scope.

```csharp
internal static class DbSeeder
{
    public static async Task SeedAsync(AppDbContext db, CancellationToken cancellationToken = default)
    {
        if (await db.Projects.AnyAsync(cancellationToken))
            return;

        await db.Projects.AddRangeAsync(CreateProjects(), cancellationToken);
        await db.SaveChangesAsync(cancellationToken);
    }

    private static IReadOnlyCollection<Project> CreateProjects()
    {
        // Deterministic, representative development scenarios matching the current model.
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

// Program.cs
if (app.Environment.IsDevelopment())
{
    await app.Services.SeedDevelopmentDataAsync();
}
```

Representative states to consider: newly created, active/in progress, completed, inactive/archived, with and without optional values and relationships, representative status values, meaningful boundary states. When the required graph is complex, the task should describe the dataset explicitly instead of inventing a large generic graph.

## Migrations

Create migrations from the Infrastructure project with the Api project as startup project:

```bash
dotnet ef migrations add AddOrderIndex --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api
dotnet ef migrations script --idempotent --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api
```

For controlled production deployment, generated (idempotent) migration scripts are often preferable; production migration is an explicit deployment step (`delivery-change`).

## Raw SQL

Use raw SQL only when EF Core cannot express the query effectively or measured performance justifies it, and keep values parameterized: `FromSql`/`FromSqlInterpolated` and `ExecuteSql`/`ExecuteSqlInterpolated` parameterize interpolated values, whereas `FromSqlRaw`/`ExecuteSqlRaw` with concatenated input do not.

## SQL Server provider (variant: sqlserver)

- String comparison in queries follows the column/database collation; SQL Server's default collations are case-insensitive. Choosing case sensitivity or a collation is a product decision when observable — make an approved choice explicit with `UseCollation(...)` or a column-level collation in configuration.
- Transient faults: prefer provider execution strategies (`options.UseSqlServer(cs, sql => sql.EnableRetryOnFailure())`) over generic application-level retry pipelines; with an execution strategy, wrap explicit transactions in `db.Database.CreateExecutionStrategy().ExecuteAsync(...)`. Do not apply HTTP retry policies to database operations.

## Testing with EF Core

- The EF Core InMemory provider is not a relational database: never use it to claim relational behavior (constraints, transactions, collation, SQL translation). A fake repository is often clearer for a true unit test.
- Provider fidelity: run provider-sensitive tests against SQL Server (for example a Testcontainers `MsSql` container or an isolated LocalDB/SQL Server database); a lighter isolated relational database may suffice when provider specifics are irrelevant — state the trade-off.
- Integration tests replace the registered `DbContextOptions<AppDbContext>` in `WebApplicationFactory` with an isolated test database and create the schema from migrations (or `EnsureCreated` for disposable test databases only).
- Test repository implementations and mappings when there is meaningful persistence behavior: custom mappings, query filters, projections, non-trivial queries, relationships, concurrency, provider-specific behavior — not every trivial `Add`/`Get`.

## Decision guide

| Scenario | Default technique |
|---|---|
| Application persistence dependency | Specific repository interface |
| Commit application changes | `IUnitOfWork.SaveChangesAsync` |
| Read-only entity query | `AsNoTracking()` when useful |
| Read model | Database-side projection |
| Primary-key entity lookup | `FindAsync` when its semantics fit |
| Complex entity graph | Explicit `Include` / projection |
| Set-based mass update/delete | `ExecuteUpdateAsync` / `ExecuteDeleteAsync` when appropriate |
| Measured extremely hot query | Consider a compiled query |
| Multiple commits requiring atomicity | Explicit transaction (inside the execution strategy) |
| Production schema change | Reviewed migration, scripted deployment |
| Fresh local seed dataset | Developer drops and recreates the local database |
