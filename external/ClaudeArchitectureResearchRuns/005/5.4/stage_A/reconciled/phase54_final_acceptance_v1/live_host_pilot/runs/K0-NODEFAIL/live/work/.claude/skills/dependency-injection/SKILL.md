---
name: dependency-injection
description: Use when registering services or fixing DI issues — lifetimes, captive dependencies, layer registration, keyed services, decorators, factories, Scrutor scanning.
---

> Kind: KNW | Scope: backend | Owner: dependency-injection technique with examples | Loading: on demand (model-invoked knowledge)

# Dependency Injection

Rules: `rules/backend/architecture.md` § Composition and dependency injection. Architecture: D-01.

## Registration shape

Application services, repositories and external adapters use interface-to-implementation registration at architectural boundaries; implementation-only helpers can be registered concretely. Prefer explicit registration in small and medium applications — keyed services, factories, decorators and convention scanning solve actual composition problems.

```csharp
// Application
public static class DependencyInjection
{
    public static IServiceCollection AddApplication(
        this IServiceCollection services)
    {
        services.AddScoped<IOrderService, OrderService>();

        return services;
    }
}

// Infrastructure
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

// Api composition root
builder.Services
    .AddApplication()
    .AddInfrastructure(builder.Configuration);
```

## Keyed services

For several implementations of one abstraction selected by a known key — not when a single registration or simple factory is clearer:

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

## Decorators

Wrap an abstraction with the same cross-cutting behavior without changing its implementation:

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

If Scrutor is already in use:

```csharp
services.AddScoped<IOrderService, OrderService>();
services.Decorate<IOrderService, LoggingOrderService>();
```

Scrutor is not worth adding for a single decoration when normal composition is simpler.

## Convention scanning

Use assembly scanning when registration volume creates genuine repetitive boilerplate, and scan the assembly that owns the services (not accidentally only the API assembly):

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

## Captive dependencies

A singleton or hosted service that needs scoped work creates a scope per operation and resolves a scoped orchestration service — not Infrastructure internals:

```csharp
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

An application service depending on scoped repositories or the Unit of Work is itself scoped; registering it as a singleton captures them (`rules/backend/architecture.md` § Composition and dependency injection).

## Decision guide

| Scenario | Registration |
|---|---|
| Application service using repositories/UoW | Scoped |
| Stateless helper without scoped dependencies | Transient or concrete registration |
| Immutable shared configuration | Singleton-compatible |
| `DbContext` | Scoped (via `AddDbContext`) |
| Several implementations chosen by key | Keyed services |
| Cross-cutting behavior | Decorator |
| Convention-based registration | Scrutor |
| Runtime implementation selection | Factory delegate |
| Strongly typed configuration | `AddOptions<T>().BindConfiguration()` (`configuration`) |
