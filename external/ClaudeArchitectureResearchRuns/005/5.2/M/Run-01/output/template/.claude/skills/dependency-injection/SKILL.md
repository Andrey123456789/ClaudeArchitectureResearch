---
name: dependency-injection
description: >
  Use for service registration and DI problems: lifetimes, captive
  dependencies, layer registration, keyed services, decorators, Scrutor,
  factories, scopes inside singletons.
---

> Knowledge skill. Owns: dependency-injection technique and examples · Scope: backend · Loads: on demand · Depends on: CLAUDE.md, .claude/rules/architecture.md

# Dependency Injection

Rules: `architecture.md` (Composition and Configuration — constructor
injection, valid lifetimes, registration near the owning layer).

## Abstractions and Registration Style

Application services, repositories, and external adapters typically use
interface-to-implementation registration; concrete registration is fine for
implementation-only helpers that need no separate contract. Prefer explicit
registration in small and medium applications; add convention scanning, keyed
services, factories, or decorators when they solve an actual composition
problem.

## Layer Registration

```csharp
public static class DependencyInjection
{
    public static IServiceCollection AddApplication(
        this IServiceCollection services)
    {
        services.AddScoped<IOrderService, OrderService>();

        return services;
    }
}
```

```csharp
public static class DependencyInjection
{
    public static IServiceCollection AddInfrastructure(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.AddDbContext<AppDbContext>(options =>
        {
            // Configure the provider selected by the project.
        });

        services.AddScoped<IOrderRepository, OrderRepository>();
        services.AddScoped<IUnitOfWork, UnitOfWork>();

        return services;
    }
}
```

```csharp
builder.Services
    .AddApplication()
    .AddInfrastructure(builder.Configuration);
```

## Keyed Services

Use keyed services when several implementations of one abstraction are selected
by a known key; a single registration or a simple explicit factory is often
clearer.

```csharp
builder.Services.AddKeyedScoped<INotificationService, EmailNotificationService>("email");
builder.Services.AddKeyedScoped<INotificationService, SmsNotificationService>("sms");

internal sealed class EmailOrderNotifier(
    [FromKeyedServices("email")] INotificationService notifier)
{
    public Task NotifyAsync(
        Notification notification,
        CancellationToken cancellationToken)
    {
        return notifier.SendAsync(notification, cancellationToken);
    }
}
```

## Decorator Pattern

Decorators wrap an abstraction with cross-cutting behavior without changing the
implementation:

```csharp
internal sealed class LoggingOrderService(
    IOrderService inner,
    ILogger<LoggingOrderService> logger)
    : IOrderService
{
    public async Task<Guid> CreateAsync(
        CreateOrderRequest request,
        CancellationToken cancellationToken)
    {
        logger.LogInformation("Creating order");

        var id = await inner.CreateAsync(
            request,
            cancellationToken);

        logger.LogInformation(
            "Order {OrderId} created",
            id);

        return id;
    }
}
```

If Scrutor is already used by the project:

```csharp
services.AddScoped<IOrderService, OrderService>();
services.Decorate<IOrderService, LoggingOrderService>();
```

Adding Scrutor for a single decoration goes through `add-dependency`; plain
composition is often simpler.

## Registration by Convention

Use assembly scanning when registration volume creates genuine boilerplate, and
scan the assembly that actually owns the services (not only the Api assembly):

```csharp
builder.Services.Scan(scan => scan
    .FromAssemblyOf<IOrderService>()
    .AddClasses(classes => classes.AssignableTo<ITransientService>())
    .AsImplementedInterfaces()
    .WithTransientLifetime()
    .AddClasses(classes => classes.AssignableTo<IScopedService>())
    .AsImplementedInterfaces()
    .WithScopedLifetime());
```

## Factory Registration

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

## Scoped Work from Singletons

A singleton or hosted service that must perform scoped work creates a scope per
operation and resolves a scoped orchestration service, not Infrastructure
internals:

```csharp
// BAD — singleton captures a scoped application service
public sealed class BackgroundWorker(IOrderProcessor processor)
{
}

// GOOD
public sealed class BackgroundWorker(
    IServiceScopeFactory scopeFactory)
{
    public async Task ProcessAsync(
        CancellationToken cancellationToken)
    {
        await using var scope =
            scopeFactory.CreateAsyncScope();

        var processor =
            scope.ServiceProvider
                .GetRequiredService<IOrderProcessor>();

        await processor.ProcessAsync(cancellationToken);
    }
}
```

```csharp
// BAD — application service depends on scoped repositories/UoW
services.AddSingleton<IOrderService, OrderService>();

// GOOD
services.AddScoped<IOrderService, OrderService>();
```

## Decision Guide

| Scenario | Recommendation |
|---|---|
| Application service using repositories/UoW | Scoped |
| Stateless helper with no scoped dependency | Transient or concrete registration |
| Immutable/shared configuration | Singleton-compatible |
| `DbContext` | Scoped (registered by `AddDbContext`) |
| Several implementations selected by key | Keyed services |
| Cross-cutting behavior | Decorator |
| Convention-based registration | Scrutor, when already justified |
| Runtime implementation selection | Factory delegate |
| Strongly typed config | `AddOptions<T>().BindConfiguration()` |
