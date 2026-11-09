---
paths:
  - "frontend/**/*"
---

> Level: 2-technology · Capability: frontend/angular · Facet: frontend.framework · Owns: Angular-specific framework rules — standalone APIs, Signals vs RxJS, interceptors, subscriptions · Scope: frontend · Loading: path

# Angular Framework Rules

- Default: use modern standalone Angular APIs for new code and organize application code primarily by feature.
- Default: use Signals for naturally synchronous, local UI state and RxJS when asynchronous streams, HTTP composition, cancellation, or event pipelines make it clearer; avoid mechanical conversions between them.
- Default: prefer functional interceptors for new code; keep interceptor responsibilities cross-cutting and never put feature business logic in an interceptor.
- Default: avoid manual nested RxJS subscriptions; prefer composition operators when stream composition expresses the behavior clearly.
- When manually subscribing from framework-managed code, tie the subscription lifetime to the component or service lifecycle using the project's current Angular facilities.

Technique: `angular`. Commands: `frontend.commands`.
