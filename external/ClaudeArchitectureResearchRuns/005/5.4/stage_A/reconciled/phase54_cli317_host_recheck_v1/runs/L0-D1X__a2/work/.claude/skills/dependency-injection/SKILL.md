---
name: dependency-injection
description: >
  Use when registering services or fixing DI issues: lifetimes, captive dependencies,
  layer registration, keyed services, decorators, Scrutor, factories.
---

> Level: 2 Technology · Owns: .NET dependency-injection technique and examples (knowledge) · Scope: backend · Loads: on invocation · Depends on: .claude/rules/1-architecture/backend-layers.md

# Dependency Injection

Policy owners: constructor injection, lifetimes, registration near the owning layer, composition root → `.claude/rules/1-architecture/backend-layers.md` → Composition and dependency injection. This skill is technique only.

Use interface-to-implementation registration at architectural boundaries (Application services, repositories, external adapters); concrete registration is fine for implementation-only helpers. Prefer explicit registration in small applications; add scanning, keyed services, factories, or decorators when they solve an actual composition problem.

## Layer registration

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
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services, IConfiguration configuration)
    {
        services.AddDbContext<AppDbContext>(options => { /* provider selected by the project */ });
        services.AddScoped<IOrderRepository, OrderRepository>();
        services.AddScoped<IUnitOfWork, UnitOfWork>();
        return services;
    }
}

// Api — composition root
builder.Services
    .AddApplication()
    .AddInfrastructure(builder.Configuration);
```

## Keyed services

Use when several implementations of one abstraction are selected by a known key and a single registration or a simple factory is not clearer:

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

// Only if Scrutor is already used by the project:
services.AddScoped<IOrderService, OrderService>();
services.Decorate<IOrderService, LoggingOrderService>();
```

Do not add Scrutor for one decoration when normal composition is simpler (`add-dependency`).

## Convention scanning

Prefer explicit registrations in small and medium projects; scan when registration volume creates genuine boilerplate, and scan the assembly that owns the services (not accidentally only the Api assembly):

```csharp
builder.Services.Scan(scan => scan
    .FromAssemblyOf<IOrderService>()
    .AddClasses(c => c.AssignableTo<IScopedService>())
    .AsImplementedInterfaces()
    .WithScopedLifetime());
```

## Factory delegates

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

## Scoped work from singletons

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

Registering an Application service that uses repositories/Unit of Work as a singleton is a captive-dependency bug: register it scoped.

## Decision guide

| Scenario | Technique |
|---|---|
| Application service using repositories/UoW | scoped |
| Stateless helper without scoped dependencies | transient or concrete registration |
| Immutable shared configuration | singleton-compatible |
| `DbContext` | scoped (`AddDbContext`) |
| Several implementations selected by key | keyed services |
| Cross-cutting wrapper | decorator |
| Many repetitive registrations | Scrutor scanning |
| Runtime implementation selection | factory delegate |
| Strongly typed configuration | `AddOptions<T>().BindConfiguration()` (`configuration` skill) |
