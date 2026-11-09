---
name: dependency-injection
description: Use when registering services or fixing DI problems in .NET — AddScoped/AddTransient/AddSingleton lifetimes, captive dependencies, layer registration methods, keyed services, decorators, factory registration, Scrutor scanning or options registration.
---
Kind: KNW | Scope: backend | Capability: — | Loading: on invocation

# Dependency Injection

Rules: `.claude/rules/backend/architecture.md` → Composition and dependency injection (constructor injection, valid lifetimes, registration next to the owning layer, composition root).

## Principles

- Use abstractions at architectural boundaries: Application services, repositories and external adapters use interface-to-implementation registration. Concrete registration is fine for implementation-only helpers that need no separate contract.
- Prefer explicit registration in small and medium applications; add convention scanning, keyed services, factories or decorators when they solve an actual composition problem.

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
        this IServiceCollection services,
        IConfiguration configuration)
    {
        // Persistence registration (context, repositories, IUnitOfWork):
        // see the persistence knowledge facet named in the decision register.
        services.AddScoped<IEmailSender, EmailSender>();
        return services;
    }
}

// Api composition root
builder.Services
    .AddApplication()
    .AddInfrastructure(builder.Configuration);
```

## Keyed services

Use keyed services when several implementations of one abstraction are selected by a known key; a single registration or a simple explicit factory is often clearer.

```csharp
builder.Services.AddKeyedScoped<INotificationService, EmailNotificationService>("email");
builder.Services.AddKeyedScoped<INotificationService, SmsNotificationService>("sms");

internal sealed class EmailOrderNotifier(
    [FromKeyedServices("email")] INotificationService notifier)
{
    public Task NotifyAsync(Notification notification, CancellationToken cancellationToken)
        => notifier.SendAsync(notification, cancellationToken);
}
```

## Decorators

Use a decorator when the same cross-cutting behavior should wrap an abstraction without changing its implementation:

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

If Scrutor is already used: `services.AddScoped<IOrderService, OrderService>(); services.Decorate<IOrderService, LoggingOrderService>();`. Do not add Scrutor for a single decoration when normal composition is simpler.

## Convention scanning (Scrutor)

Use assembly scanning when registration volume creates genuinely repetitive boilerplate, and scan the assembly that owns the services, not accidentally only the Api assembly:

```csharp
builder.Services.Scan(scan => scan
    .FromAssemblyOf<IOrderService>()
    .AddClasses(classes => classes.AssignableTo<IScopedService>())
    .AsImplementedInterfaces()
    .WithScopedLifetime());
```

## Factory registration

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

## Scoped work from singletons

A singleton or hosted service that needs scoped work creates a scope per operation and resolves a scoped orchestration service, not Infrastructure internals:

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

An Application service that depends on scoped repositories or the Unit of Work is itself scoped, never a singleton.

## Quick reference

| Scenario | Registration |
|---|---|
| Application service using repositories or the Unit of Work | Scoped |
| Stateless helper without scoped dependencies | Transient or concrete registration |
| Immutable shared configuration | Singleton-compatible |
| Persistence context | Scoped (registered by the persistence technology) |
| Several implementations selected by key | Keyed services |
| Cross-cutting wrapper | Decorator |
| Repetitive registrations | Scrutor scanning |
| Runtime implementation selection | Factory delegate |
| Strongly typed configuration | `AddOptions<T>().BindConfiguration()` (`configuration` skill) |
