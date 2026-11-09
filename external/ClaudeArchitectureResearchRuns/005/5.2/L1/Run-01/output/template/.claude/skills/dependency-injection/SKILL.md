---
name: dependency-injection
description: >
  Use for DI: AddScoped/AddTransient/AddSingleton lifetimes, captive
  dependencies, registration methods, keyed services, decorators, factories,
  Scrutor.
---
> Level: 2-technology | Owns: dependency-injection technique | Scope: backend | Loads: on demand (skill)

# Dependency Injection

Policy: `hosting.md` (constructor injection, valid lifetimes),
`role-boundaries.md` (registration close to the owning role, composition root).
Concrete registration method names per project: `architecture.layout`.

## Principles

- Use abstractions at architectural boundaries (use-case services, persistence
  contracts, external adapters); concrete registration is fine for
  implementation-only helpers that need no separate contract.
- Prefer explicit registration in small and medium applications; add
  convention scanning, keyed services, factories, or decorators when they solve
  an actual composition problem.

## Per-project registration

Each project exposes one registration extension for what it owns, and the host
composes them:

```csharp
public static class DependencyInjection
{
    public static IServiceCollection AddOrdering(this IServiceCollection services)
    {
        services.AddScoped<IOrderService, OrderService>();
        return services;
    }
}
```

## Lifetimes

| Service | Lifetime |
|---|---|
| Use-case service depending on repositories / unit of work | Scoped |
| Stateless helper without scoped dependencies | Transient or concrete |
| Immutable shared configuration | Singleton-compatible |
| Persistence context | Scoped (registered by its provider) |

A singleton or hosted service that needs scoped work creates a scope per
operation and resolves a scoped orchestration service, not adapter internals:

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

Do not register a service that depends on scoped repositories as a singleton.

## Keyed services

For several implementations of one abstraction selected by a known key —
otherwise a single registration or a small explicit factory is clearer.

```csharp
builder.Services.AddKeyedScoped<INotificationService, EmailNotificationService>("email");
builder.Services.AddKeyedScoped<INotificationService, SmsNotificationService>("sms");

internal sealed class EmailOrderNotifier(
    [FromKeyedServices("email")] INotificationService notifier) { }
```

## Decorators

Wrap an abstraction with the same cross-cutting behavior without changing the
implementation:

```csharp
internal sealed class LoggingOrderService(
    IOrderService inner,
    ILogger<LoggingOrderService> logger) : IOrderService
{
    public async Task<Guid> CreateAsync(CreateOrderRequest request, CancellationToken cancellationToken)
    {
        var id = await inner.CreateAsync(request, cancellationToken);
        logger.LogInformation("Order {OrderId} created", id);
        return id;
    }
}
```

If Scrutor is already used: `services.Decorate<IOrderService, LoggingOrderService>();`.
Do not add Scrutor for a single decoration when manual composition is simpler.

## Convention scanning

Use assembly scanning only when registration volume creates genuine
boilerplate, and scan the assembly that owns the services — not accidentally the
host assembly:

```csharp
builder.Services.Scan(scan => scan
    .FromAssemblyOf<IOrderService>()
    .AddClasses(c => c.AssignableTo<IScopedService>())
    .AsImplementedInterfaces()
    .WithScopedLifetime());
```

## Factories

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

## Validation

Enable `ValidateScopes` and `ValidateOnBuild` (on by default in Development) to
catch captive dependencies and missing registrations at startup.
