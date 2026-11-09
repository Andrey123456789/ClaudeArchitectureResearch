---
paths:
  - "frontend/**/*"
---

> Capability: frontend/angular · Path rule · Scope: frontend · Owns Angular-specific frontend rules and the bindings for the framework-independent frontend rule

# Frontend Framework Rules: Angular

Framework-independent frontend policy: `.claude/rules/frontend.md`.

- Use modern standalone Angular APIs for new code, organized primarily by
  feature. Do not introduce NgModules for ordinary new feature development
  unless an integration or legacy dependency genuinely requires them.
- Use Signals for naturally synchronous, local UI state and RxJS when
  asynchronous streams, HTTP composition, cancellation, or event pipelines are
  the clearer model; avoid mechanical conversions between the two.
- Prefer functional interceptors for new code and keep interceptor
  responsibilities cross-cutting; do not put feature business logic in an
  interceptor.
- Avoid manual nested RxJS subscriptions; prefer composition operators when
  stream composition expresses the behavior clearly.
- When manually subscribing from Angular framework-managed code, tie the
  subscription lifetime to the component or service lifecycle using the
  project's current Angular facilities.

## Bindings for `frontend.md`

| Role in `frontend.md` | Angular binding |
|---|---|
| feature data-access service (HTTP boundary) | `@Injectable` feature service using `HttpClient` |
| explicit form model | Reactive Forms |
