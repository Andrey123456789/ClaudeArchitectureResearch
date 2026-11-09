---
name: dependency-injection
description: Use when registering services or designing composition — AddScoped/AddTransient/AddSingleton lifetimes, captive dependencies, layer registration methods, keyed services, decorators, Scrutor scanning, factory registrations, options registration.
---
<!-- Kind: KNW | Scope: backend | Owns: dependency-injection technique and examples | Loads: on demand (model-invoked) -->
# Dependency Injection

Standards: `rules/backend/architecture.md` § Composition and Dependency Injection (constructor injection, valid lifetimes, registration near the owning layer).

Application services, repositories and external adapters normally use interface-to-implementation registration at architectural boundaries; concrete registration is fine for implementation-only helpers without a separate contract. Small applications are easiest to follow with explicit registration; convention scanning, keyed services, factories and decorators earn their place when they solve an actual composition problem.

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

Api composes the application:

```csharp
builder.Services
    .AddApplication()
    .AddInfrastructure(builder.Configuration);
```

## Keyed Services (.NET 8+)

For several implementations of one abstraction selected by a known key — not when a single registration or a simple explicit factory is clearer:

```csharp
// Registration
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

For the same cross-cutting behavior wrapped around an abstraction without changing its implementation:

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

Adding Scrutor solely for one decoration is rarely worth it when normal composition is simpler.

## Registration by Convention (Scrutor)

Explicit registrations are easier to discover and debug in small and medium projects. Assembly scanning pays off when registration volume creates genuinely repetitive boilerplate; scan the assembly that actually owns the services, not accidentally only the Api assembly.

```csharp
// Auto-register all services matching a convention
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
// Bind configuration section to a strongly typed options class
builder.Services.AddOptions<JwtOptions>()
    .BindConfiguration("Jwt")
    .ValidateDataAnnotations()
    .ValidateOnStart();

// Inject as IOptions<T>
public class TokenService(IOptions<JwtOptions> options)
{
    private readonly JwtOptions _jwt = options.Value;
}
```

## Anti-Patterns

### Scoped Services Captured in Singletons

```csharp
// BAD — singleton captures a scoped application service
public sealed class BackgroundWorker(IOrderProcessor processor)
{
}
```

When a singleton or hosted service genuinely needs scoped work, create a scope per operation and resolve a scoped orchestration service, not Infrastructure internals:

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

### Everything Registered as Singleton

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
| Pure stateless helper with no scoped dependency | Transient or concrete registration |
| Immutable/shared configuration | Singleton-compatible |
| DbContext | Scoped (registered by `AddDbContext`) |
| Multiple implementations | Keyed services (strategy pattern) |
| Cross-cutting behavior | Decorator pattern |
| Convention-based registration | Scrutor |
| Runtime implementation selection | Factory delegate |
| Strongly typed configuration | `AddOptions<T>().BindConfiguration()` |
