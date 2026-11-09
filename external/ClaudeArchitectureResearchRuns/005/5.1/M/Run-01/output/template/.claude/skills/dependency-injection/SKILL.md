---
name: dependency-injection
description: >
  Use when registering services, choosing AddScoped/AddTransient/AddSingleton,
  diagnosing captive dependencies, writing AddApplication/AddInfrastructure
  extensions, or considering keyed services, decorators, factories, or Scrutor
  assembly scanning.
---

> Owns: .NET dependency-injection technique | Scope: backend | Loads: on demand (knowledge skill)

# Dependency Injection

Policy owners: constructor injection, valid lifetimes, registration per layer →
`.claude/rules/architecture.md` (Dependency Injection and Configuration). Adding a
library such as Scrutor goes through `add-dependency`.

Application services, repositories, and external adapters normally use
interface-to-implementation registration; implementation-only helpers can be
registered concretely. Prefer explicit registration in small and medium
applications.

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
    services.AddDbContext<AppDbContext>(options => { /* provider selected by the project */ });
    services.AddScoped<IOrderRepository, OrderRepository>();
    services.AddScoped<IUnitOfWork, UnitOfWork>();
    return services;
}

// Api (composition root)
builder.Services
    .AddApplication()
    .AddInfrastructure(builder.Configuration);
```

## Lifetimes

| Service | Lifetime |
|---|---|
| Application service using repositories/UoW | Scoped |
| `DbContext` | Scoped (via `AddDbContext`) |
| Stateless helper without scoped dependencies | Transient or concrete |
| Immutable shared configuration | Singleton-compatible |

Scoped work from a singleton or hosted service: create a scope per operation and
resolve a scoped orchestration service, not Infrastructure internals.

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

Enable `ValidateScopes`/`ValidateOnBuild` (on by default in Development) to catch
captive dependencies early.

## Keyed Services

When several implementations are selected by a known key:

```csharp
builder.Services.AddKeyedScoped<INotificationService, EmailNotificationService>("email");
builder.Services.AddKeyedScoped<INotificationService, SmsNotificationService>("sms");

internal sealed class EmailOrderNotifier([FromKeyedServices("email")] INotificationService notifier) { }
```

Prefer a normal registration or a simple factory when that is clearer.

## Decorators

For cross-cutting behavior around an abstraction:

```csharp
internal sealed class LoggingOrderService(IOrderService inner, ILogger<LoggingOrderService> logger)
    : IOrderService
{
    public async Task<Guid> CreateAsync(CreateOrderRequest request, CancellationToken cancellationToken)
    {
        var id = await inner.CreateAsync(request, cancellationToken);
        logger.LogInformation("Order {OrderId} created", id);
        return id;
    }
}

// Without a library
services.AddScoped<OrderService>();
services.AddScoped<IOrderService>(sp =>
    new LoggingOrderService(sp.GetRequiredService<OrderService>(),
        sp.GetRequiredService<ILogger<LoggingOrderService>>()));

// If Scrutor is already used
services.AddScoped<IOrderService, OrderService>();
services.Decorate<IOrderService, LoggingOrderService>();
```

## Factory Selection

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

## Convention Scanning

Only when registration volume creates real boilerplate, and scan the assembly
that owns the services (not just the Api assembly):

```csharp
builder.Services.Scan(scan => scan
    .FromAssemblyOf<IOrderService>()
    .AddClasses(c => c.AssignableTo<IScopedService>())
    .AsImplementedInterfaces()
    .WithScopedLifetime());
```
