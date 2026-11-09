---
name: dependency-injection
description: >
  Use when registering services or fixing lifetime or captive-dependency errors:
  layer registration methods, Scoped/Transient/Singleton, scopes in singletons,
  keyed services, decorators, factories.
---

> Level: 2 Technology · Owns: DI registration technique · Scope: backend · Loads: on demand (knowledge skill)

# Dependency Injection

Policy owners: `.claude/rules/1-architecture/backend-layers.md` (constructor injection, lifetimes, registration near the owning layer, composition root). Interface-to-implementation registration suits architectural boundaries (Application services, repositories, external adapters); concrete registration is fine for implementation-only helpers. Prefer explicit registration in small applications.

## Layer registration

```csharp
// Application/DependencyInjection.cs
public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddScoped<IOrderService, OrderService>();
        return services;
    }
}

// Infrastructure/DependencyInjection.cs
public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.AddDbContext<AppDbContext>(options => { /* selected provider */ });
        services.AddScoped<IOrderRepository, OrderRepository>();
        services.AddScoped<IUnitOfWork, UnitOfWork>();
        return services;
    }
}

// Api/Program.cs
builder.Services
    .AddApplication()
    .AddInfrastructure(builder.Configuration);
```

## Lifetimes

| Service | Typical lifetime |
|---|---|
| Application service using repositories/unit of work | Scoped |
| `DbContext` | Scoped (`AddDbContext`) |
| Stateless helper without scoped dependencies | Transient or singleton-compatible |
| Immutable shared configuration | Singleton-compatible |

A singleton or hosted service that needs scoped work creates a scope per operation and resolves a scoped orchestration service — not Infrastructure internals:

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

`builder.Host.UseDefaultServiceProvider(o => { o.ValidateScopes = true; o.ValidateOnBuild = true; })` surfaces captive dependencies early (both are on by default in Development).

## Keyed services

For several implementations selected by a known key — not when one registration or a simple factory is clearer:

```csharp
builder.Services.AddKeyedScoped<INotificationService, EmailNotificationService>("email");
builder.Services.AddKeyedScoped<INotificationService, SmsNotificationService>("sms");

internal sealed class EmailOrderNotifier([FromKeyedServices("email")] INotificationService notifier)
{
}
```

## Decorators

Wrap an abstraction with cross-cutting behavior without changing the implementation:

```csharp
internal sealed class LoggingOrderService(IOrderService inner, ILogger<LoggingOrderService> logger)
    : IOrderService
{
    public async Task<Guid> CreateAsync(CreateOrderRequest request, CancellationToken cancellationToken)
    {
        logger.LogInformation("Creating order");
        var id = await inner.CreateAsync(request, cancellationToken);
        logger.LogInformation("Order {OrderId} created", id);
        return id;
    }
}
```

Without a library, register the inner type concretely and compose in a factory delegate. If the project already uses Scrutor: `services.Decorate<IOrderService, LoggingOrderService>();` — do not add Scrutor for a single decoration.

## Factories

Runtime selection of an implementation:

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

## Convention scanning

Use assembly scanning only when registration volume creates real boilerplate, and scan the assembly that owns the services (not only the Api assembly). With Scrutor (already adopted):

```csharp
builder.Services.Scan(scan => scan
    .FromAssemblyOf<IOrderService>()
    .AddClasses(c => c.AssignableTo<IScopedService>())
    .AsImplementedInterfaces()
    .WithScopedLifetime());
```

## Review cues

Singleton application services depending on scoped repositories, `IServiceProvider` injected into business classes, property injection, Infrastructure implementations registered from Application, scanning libraries added for a handful of services.
