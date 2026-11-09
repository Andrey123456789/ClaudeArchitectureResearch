---
name: dependency-injection
description: >
  Use for DI registration and lifetime problems: scoped/singleton, captive dependencies, keyed services, decorators, factories, Scrutor.
---

> Level: 2 Technology | Owns: .NET dependency-injection technique | Scope: backend | Loads: knowledge skill (on demand) | Depends on: 2-technology/dotnet-runtime.md, 1-architecture/backend-layers.md

# Dependency Injection Technique

Policy owners (routing): constructor injection and valid lifetimes →
`2-technology/dotnet-runtime.md`; registration ownership per layer →
`1-architecture/backend-layers.md`.

Architectural boundaries (Application services, repositories, external
adapters) normally use interface-to-implementation registration; concrete
registration is fine for implementation-only helpers. Prefer explicit
registration in small and medium projects.

## Layer Registration

```csharp
// Application
public static IServiceCollection AddApplication(this IServiceCollection services)
{
    services.AddScoped<IOrderService, OrderService>();
    return services;
}

// Infrastructure
public static IServiceCollection AddInfrastructure(
    this IServiceCollection services, IConfiguration configuration)
{
    services.AddDbContext<AppDbContext>(options => { /* project's provider */ });
    services.AddScoped<IOrderRepository, OrderRepository>();
    services.AddScoped<IUnitOfWork, UnitOfWork>();
    return services;
}

// Api (composition root)
builder.Services.AddApplication().AddInfrastructure(builder.Configuration);
```

## Lifetimes

| Service | Lifetime |
|---|---|
| Application service using repositories/UoW | Scoped |
| `DbContext` | Scoped (via `AddDbContext`) |
| Stateless helper without scoped dependencies | Transient or concrete |
| Immutable shared configuration | Singleton-compatible |

A singleton or hosted service that needs scoped work creates a scope per
operation and resolves a scoped orchestration service, not Infrastructure
internals:

```csharp
public sealed class BackgroundWorker(IServiceScopeFactory scopeFactory)
{
    public async Task ProcessAsync(CancellationToken cancellationToken)
    {
        await using var scope = scopeFactory.CreateAsyncScope();
        var processor = scope.ServiceProvider.GetRequiredService<IOrderProcessor>();
        await processor.ProcessAsync(cancellationToken);
    }
}
```

## Keyed Services

```csharp
builder.Services.AddKeyedScoped<INotificationService, EmailNotificationService>("email");
builder.Services.AddKeyedScoped<INotificationService, SmsNotificationService>("sms");

internal sealed class EmailOrderNotifier(
    [FromKeyedServices("email")] INotificationService notifier) { /* ... */ }
```

Use keys when several implementations are selected by a known key; a single
registration or a small factory is often clearer.

## Decorators

```csharp
internal sealed class LoggingOrderService(IOrderService inner, ILogger<LoggingOrderService> logger)
    : IOrderService
{
    public async Task<Guid> CreateAsync(CreateOrderRequest request, CancellationToken ct)
    {
        logger.LogInformation("Creating order");
        var id = await inner.CreateAsync(request, ct);
        logger.LogInformation("Order {OrderId} created", id);
        return id;
    }
}

// If the project already uses Scrutor:
services.AddScoped<IOrderService, OrderService>();
services.Decorate<IOrderService, LoggingOrderService>();
```

Do not add Scrutor (a new library) for one decoration when manual composition is
simpler.

## Convention Scanning (Scrutor)

Use scanning only when registration volume creates real boilerplate, and scan
the assembly that owns the services:

```csharp
builder.Services.Scan(scan => scan
    .FromAssemblyOf<IOrderService>()
    .AddClasses(c => c.AssignableTo<IScopedService>())
    .AsImplementedInterfaces()
    .WithScopedLifetime());
```

## Factory Registration

```csharp
builder.Services.AddScoped<IPaymentProcessor>(sp =>
{
    var config = sp.GetRequiredService<IOptions<PaymentOptions>>().Value;
    return config.Provider switch
    {
        "stripe" => ActivatorUtilities.CreateInstance<StripeProcessor>(sp),
        "paypal" => ActivatorUtilities.CreateInstance<PayPalProcessor>(sp),
        _ => throw new InvalidOperationException($"Unknown payment provider: {config.Provider}")
    };
});
```

## Avoid

```csharp
services.AddSingleton<IOrderService, OrderService>();     // captures scoped repositories/UoW
public sealed class BackgroundWorker(IOrderProcessor p);  // singleton capturing a scoped service
```
