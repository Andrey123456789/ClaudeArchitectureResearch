---
name: dependency-injection
description: >
  Use when registering services or fixing DI problems: lifetimes, captive
  dependencies, layer registration methods, keyed services, decorators, Scrutor,
  factory registrations.
---

> Owns: dependency-injection technique and examples (no policy) | Scope: backend | Loads: on demand (knowledge skill)

# Dependency Injection

Policy owners: constructor injection, lifetime validity, registration placement,
and the composition root — `.claude/rules/architecture.md` § Composition and
Dependency Injection.

## Registration Style

- Use interface-to-implementation registration for Application services,
  repositories, and external adapters at architectural boundaries; concrete
  registration is fine for implementation-only helpers that need no separate
  contract.
- Prefer explicit registration in small and medium applications. Add convention
  scanning, keyed services, factories, or decorators when they solve an actual
  composition problem.

## Layer Registration

Application exposes its own registration method:

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

Infrastructure registers technical implementations:

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

The API composes the application:

```csharp
builder.Services
    .AddApplication()
    .AddInfrastructure(builder.Configuration);
```

## Keyed Services

Use keyed services when multiple implementations of the same abstraction are
selected by a known key, not when a normal single registration or a simple
explicit factory is clearer.

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

Use a decorator when the same cross-cutting behavior should wrap an abstraction
without changing its implementation.

```csharp
public interface IOrderService
{
    Task<Guid> CreateAsync(
        CreateOrderRequest request,
        CancellationToken cancellationToken);
}

internal sealed class OrderService(
    IOrderRepository orders,
    IUnitOfWork unitOfWork,
    TimeProvider clock)
    : IOrderService
{
    public async Task<Guid> CreateAsync(
        CreateOrderRequest request,
        CancellationToken cancellationToken)
    {
        var order = new Order(
            Guid.NewGuid(),
            request.CustomerId,
            clock.GetUtcNow());

        await orders.AddAsync(order, cancellationToken);
        await unitOfWork.SaveChangesAsync(cancellationToken);

        return order.Id;
    }
}

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

Do not add Scrutor solely for one decoration when normal composition is simpler
(adding it goes through `add-dependency`).

## Registration by Convention (Scrutor)

Use assembly scanning when registration volume creates genuinely repetitive
boilerplate, and scan the assembly that actually owns the services — not only the
API assembly by accident.

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

## Factory Pattern

When runtime logic selects an implementation:

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

## Options Registration

```csharp
builder.Services.AddOptions<JwtOptions>()
    .BindConfiguration("Jwt")
    .ValidateDataAnnotations()
    .ValidateOnStart();

public class TokenService(IOptions<JwtOptions> options)
{
    private readonly JwtOptions _jwt = options.Value;
}
```

## Captive Dependencies

```csharp
// BAD - singleton captures a scoped application service
public sealed class BackgroundWorker(IOrderProcessor processor)
{
}
```

When a singleton or hosted service genuinely needs scoped work, create a scope
per operation and resolve a scoped orchestration service, not Infrastructure
internals:

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

```csharp
// BAD - application service depends on scoped repositories/UoW
services.AddSingleton<IOrderService, OrderService>();

// GOOD
services.AddScoped<IOrderService, OrderService>();
```

## Decision Guide

| Scenario | Recommendation |
|----------|---------------|
| Application service using repositories/UoW | Scoped |
| Pure stateless helper with no scoped dependency | Transient or concrete registration |
| Immutable/shared configuration | Singleton-compatible |
| DbContext | Scoped (registered by `AddDbContext`) |
| Multiple implementations selected by key | Keyed services |
| Cross-cutting behavior | Decorator |
| Convention-based registration | Scrutor, when already justified |
| Runtime implementation selection | Factory delegate |
| Strongly typed config | `AddOptions<T>().BindConfiguration()` |
