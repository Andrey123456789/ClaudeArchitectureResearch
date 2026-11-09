---
name: dependency-injection
description: >
  Use when registering services or fixing DI problems:
  AddScoped/AddTransient/AddSingleton, captive dependencies, scopes in
  singletons, keyed services, decorators, Scrutor scanning, factory
  registration.
---

> Kind: KNW | Scope: backend | Capability: — | Loading: on-demand knowledge

# Dependency Injection

Policy: `.claude/rules/backend/architecture.md` (constructor injection, valid lifetimes) and the frame's registration rules in `.claude/rules/backend/architecture-style.md`.

## Layer registration

Use abstractions at architectural boundaries (Application services, repositories, external adapters); concrete registration is fine for implementation-only helpers without a separate contract.

```csharp
// Application
public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddScoped<IOrderService, OrderService>();
        return services;
    }
}

// Infrastructure
public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration configuration)
    {
        // Persistence registration: the persistence knowledge facet named in the decision register.
        services.AddScoped<IOrderRepository, OrderRepository>();
        services.AddScoped<IUnitOfWork, UnitOfWork>();
        return services;
    }
}

// Api (composition root)
builder.Services
    .AddApplication()
    .AddInfrastructure(builder.Configuration);
```

Prefer explicit registration in small and medium applications; add scanning, keyed services, factories, or decorators when they solve an actual composition problem.

## Lifetimes

| Scenario | Lifetime |
|---|---|
| Application service using repositories/Unit of Work | Scoped |
| Pure stateless helper without scoped dependencies | Transient or concrete registration |
| Immutable/shared configuration | Singleton-compatible |
| Persistence context | Scoped (registered by the persistence facet) |

Never register an Application service that depends on scoped repositories as a singleton. A singleton or hosted service that needs scoped work creates a scope per operation and resolves a scoped orchestration service, not Infrastructure internals:

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

## Keyed services

For several implementations of one abstraction selected by a known key; not when a single registration or a simple explicit factory is clearer.

```csharp
builder.Services.AddKeyedScoped<INotificationService, EmailNotificationService>("email");
builder.Services.AddKeyedScoped<INotificationService, SmsNotificationService>("sms");

internal sealed class EmailOrderNotifier([FromKeyedServices("email")] INotificationService notifier)
{
    public Task NotifyAsync(Notification notification, CancellationToken cancellationToken) =>
        notifier.SendAsync(notification, cancellationToken);
}
```

## Decorators

Wrap an abstraction with cross-cutting behavior without changing its implementation:

```csharp
internal sealed class LoggingOrderService(IOrderService inner, ILogger<LoggingOrderService> logger) : IOrderService
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

If Scrutor is already used: `services.AddScoped<IOrderService, OrderService>(); services.Decorate<IOrderService, LoggingOrderService>();`. Do not add Scrutor for a single decoration when normal composition is simpler.

## Convention scanning (Scrutor)

Use assembly scanning only when registration volume creates genuine boilerplate, and scan the assembly that owns the services (not accidentally only the Api assembly):

```csharp
builder.Services.Scan(scan => scan
    .FromAssemblyOf<IOrderService>()
    .AddClasses(classes => classes.AssignableTo<IScopedService>())
    .AsImplementedInterfaces()
    .WithScopedLifetime());
```

## Factory registration

For runtime implementation selection:

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

Options registration: `configuration`.
