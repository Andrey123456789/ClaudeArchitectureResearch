---
name: dependency-injection
description: >
  Use when registering services or fixing DI problems: lifetimes, captive
  dependencies, AddApplication/AddInfrastructure extensions, keyed services,
  decorators, factories, scopes inside singletons, Scrutor scanning.
---

> Owner: dependency-injection technique and examples (normative policy lives in rules) | Scope: backend | Loads: on demand — knowledge | Enforced: none

# Dependency Injection

Policy: `.claude/rules/architecture.md` § Dependency Injection (constructor
injection, valid lifetimes, registration per layer).

Application services, repositories, and external adapters normally use
interface-to-implementation registration at architectural boundaries; concrete
registration is fine for implementation-only helpers without a separate contract.
Prefer explicit registration in small and medium applications; add scanning,
keyed services, factories, or decorators when they solve an actual composition
problem.

## Layer Registration

Application:

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

Infrastructure:

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

API composition:

```csharp
builder.Services
    .AddApplication()
    .AddInfrastructure(builder.Configuration);
```

## Keyed Services

For several implementations of one abstraction selected by a known key; a single
registration or a simple explicit factory is often clearer.

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

Wrap an abstraction with the same cross-cutting behavior without changing its
implementation:

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

Without Scrutor, register the decorator manually:

```csharp
services.AddScoped<OrderService>();
services.AddScoped<IOrderService>(sp =>
    new LoggingOrderService(
        sp.GetRequiredService<OrderService>(),
        sp.GetRequiredService<ILogger<LoggingOrderService>>()));
```

If the project already uses Scrutor:

```csharp
services.AddScoped<IOrderService, OrderService>();
services.Decorate<IOrderService, LoggingOrderService>();
```

Adding Scrutor for a single decoration is rarely worth a new dependency.

## Registration by Convention (Scrutor)

Use assembly scanning when registration volume creates genuinely repetitive
boilerplate, and scan the assembly that actually owns the services (not only the
API assembly):

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

Marker interfaces such as `IScopedService` are a project-wide convention
(Reserved) — agree on them before introducing them.

## Factory Registration

When runtime logic selects the implementation:

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

public sealed class TokenService(IOptions<JwtOptions> options)
{
    private readonly JwtOptions _jwt = options.Value;
}
```

More in the `configuration` skill.

## Scoped Work from Singletons

A singleton or hosted service that needs scoped work creates a scope per
operation and resolves a scoped orchestration service, not Infrastructure
internals:

```csharp
// Captive dependency: the singleton holds a scoped service forever
public sealed class BackgroundWorker(IOrderProcessor processor)
{
}
```

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

Enable scope validation to catch captive dependencies early (on by default in
Development):

```csharp
builder.Host.UseDefaultServiceProvider(options =>
{
    options.ValidateScopes = true;
    options.ValidateOnBuild = true;
});
```

## Singleton Misuse

```csharp
// Wrong lifetime — the service depends on scoped repositories/UoW
services.AddSingleton<IOrderService, OrderService>();

// Matches its dependencies
services.AddScoped<IOrderService, OrderService>();
```

## Decision Guide

| Scenario | Technique |
|---|---|
| Application service using repositories/UoW | Scoped |
| Stateless helper without scoped dependencies | Transient or concrete registration |
| Immutable/shared configuration | Singleton-compatible |
| DbContext | Scoped (`AddDbContext`) |
| Multiple implementations selected by key | Keyed services |
| Cross-cutting behavior | Decorator |
| High-volume repetitive registration | Scrutor scanning |
| Runtime implementation selection | Factory delegate |
| Strongly typed config | `AddOptions<T>().BindConfiguration()` |
