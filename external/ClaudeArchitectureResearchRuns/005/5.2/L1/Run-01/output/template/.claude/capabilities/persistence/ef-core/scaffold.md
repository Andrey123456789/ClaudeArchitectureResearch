> Level: 3-project | Capability: persistence/ef-core (persistence.scaffold) | Owns: initial EF Core + SQL Server setup inside the persistence implementation | Scope: backend | Loads: read when project-structure names persistence.scaffold

# Persistence Scaffold — EF Core with SQL Server

Paths use the current frame: the named location `persistence implementation`
is `backend/<Name>.Infrastructure/Persistence/`.

## Packages (through `add-dependency`)

- `Microsoft.EntityFrameworkCore.SqlServer` — adapter project.
- `Microsoft.EntityFrameworkCore.Design` — composition-root host, as a
  development-only asset (`PrivateAssets="all"`).
- `dotnet-ef` — local .NET tool (`dotnet new tool-manifest`, then
  `dotnet tool install dotnet-ef --version <verified version>`).

## Internal structure

```text
Persistence/
├── AppDbContext.cs
├── UnitOfWork.cs
├── Configurations/        # IEntityTypeConfiguration<T> mappings
├── Repositories/          # repository implementations (optional internal Repository<TEntity> base)
├── Migrations/            # generated EF Core migrations
└── Seeding/
    ├── DbSeeder.cs                          # internal
    └── DatabaseInitializationExtensions.cs  # public SeedDevelopmentDataAsync()
```

## Registration (adapter `DependencyInjection.cs`)

```csharp
services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(
        configuration.GetConnectionString("DefaultConnection")));

services.AddScoped<IOrderRepository, OrderRepository>();
services.AddScoped<IUnitOfWork, UnitOfWork>();
```

## Development configuration

`appsettings.Development.json` in the host (adapt the database name):

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\MSSQLLocalDB;Database=ProjectName;Trusted_Connection=True;TrustServerCertificate=True;"
  }
}
```

Do not add Production credentials or production migration automation.

## Startup seeding wiring (host `Program.cs`)

```csharp
if (app.Environment.IsDevelopment())
{
    await app.Services.SeedDevelopmentDataAsync();
}
```

The extension creates a scope and delegates to the internal `DbSeeder`; it does
not run migrations. Apply the initial migration with `persistence.workflow`.
