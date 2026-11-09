---
name: dependency-injection
description: .NET dependency-injection technique. Use for service registration, AddScoped/AddTransient/AddSingleton lifetimes, captive dependencies, per-layer registration methods, keyed services, decorators, Scrutor scanning, factory delegates, or IServiceScopeFactory in hosted services.
---

> Level: 2-technology · Owns: DI composition technique · Loading: on demand

# Dependency Injection

Rules: constructor injection and lifetime rules (`.claude/rules/0-core/backend-code.md`); where registration lives (frame boundaries). Interface-to-implementation registration suits use-case units, repositories, and adapters; concrete registration is fine for implementation-only helpers. Prefer explicit registration in small and medium projects; add scanning, keyed services, factories, or decorators for an actual composition problem.

## Per-layer registration

```csharp
public static class DependencyInjection   // use-case project
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        services.AddScoped<IOrderService, OrderService>();
        return services;
    }
}

public static class DependencyInjection   // implementation project
{
    public static IServiceCollection AddInfrastructure(this IServiceCollection services, IConfiguration configuration)
    {
        // persistence registration: persistence commands facet
        services.AddScoped<IOrderRepository, OrderRepository>();
        services.AddScoped<IUnitOfWork, UnitOfWork>();
        return services;
    }
}

// composition root
builder.Services.AddApplication().AddInfrastructure(builder.Configuration);
```

## Lifetimes

| Service | Lifetime |
| --- | --- |
| use-case unit using repositories/commit boundary | scoped |
| stateless helper without scoped dependencies | transient or concrete |
| immutable shared configuration | singleton-compatible |
| persistence context | scoped (registered by the persistence implementation) |

A singleton or hosted service that needs scoped work creates a scope per operation and resolves a scoped orchestration service, not implementation internals:

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

Never register a service that depends on scoped repositories as a singleton.

## Optional patterns

- **Keyed services** — several implementations selected by a known key: `AddKeyedScoped<INotificationService, EmailNotificationService>("email")` and `[FromKeyedServices("email")] INotificationService notifier`. Prefer a single registration or simple factory when clearer.
- **Decorator** — wraps an abstraction with cross-cutting behavior (`LoggingOrderService(IOrderService inner, ILogger<LoggingOrderService> logger)`). With Scrutor already present: `services.Decorate<IOrderService, LoggingOrderService>();` — do not add Scrutor for one decoration.
- **Convention scanning** — only when registration volume creates real boilerplate; scan the assembly that owns the services (`scan.FromAssemblyOf<IOrderService>()`), not just the entry-point assembly.
- **Factory delegate** — runtime selection: `services.AddScoped<IPaymentProcessor>(sp => ... ActivatorUtilities.CreateInstance<StripeProcessor>(sp) ...)`, throwing for unknown configuration values.
- **Options** — `AddOptions<T>().BindConfiguration(...).ValidateDataAnnotations().ValidateOnStart()` (see `configuration`).
