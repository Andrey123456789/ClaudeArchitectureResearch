---
paths:
  - "frontend/**"
---
Kind: STD | Scope: frontend | Capability: frontend/angular | Loading: path-scoped (frontend/**)

# Frontend Framework Standards: Angular

## Role bindings

- Data-access service: an injectable feature service that uses `HttpClient`, for example under `features/<feature>/data-access/`.
- Structured form mechanism: Angular reactive forms.
- HTTP pipeline configuration: `provideHttpClient(withInterceptors([...]))`.
- Route-level lazy loading: `loadChildren` and `loadComponent` route entries.

## Standards

- Default: new code uses modern standalone Angular APIs (standalone components, and no new NgModules unless an integration or legacy dependency genuinely requires one), and application code is organized primarily by feature.
- Default: use Signals, with `computed` for derived state, for naturally synchronous local UI state, and RxJS where asynchronous streams, HTTP composition, cancellation or switching, or event pipelines are the clearer model. Avoid unnecessary `effect()` and mechanical conversions between Observables and Signals.
- Default: use functional interceptors for new code. Interceptors stay cross-cutting and never contain feature business logic.
- Default: avoid manual nested RxJS subscriptions and prefer composition operators when they express the behavior clearly.
- A manual subscription made from Angular framework-managed code must have its lifetime tied to the component or service lifecycle through the project's current Angular facilities (for example `takeUntilDestroyed` or `DestroyRef`).
