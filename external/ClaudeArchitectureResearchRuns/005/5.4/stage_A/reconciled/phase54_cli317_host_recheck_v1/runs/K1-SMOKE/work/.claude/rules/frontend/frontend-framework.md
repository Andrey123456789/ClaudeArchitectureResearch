---
paths:
  - "frontend/**/*"
---

> Kind: STD | Scope: frontend | Capability: frontend/angular | Loading: path-scoped (frontmatter paths)

# Frontend Framework — Angular

- Default: modern standalone Angular APIs for new code (no new NgModules for ordinary feature development), with application code organized primarily by feature.
- Default: Signals for naturally synchronous, local UI state; RxJS when asynchronous streams, HTTP composition, cancellation, or event pipelines are clearer. Avoid mechanical conversions between the two.
- Default: functional HTTP interceptors for new code. Interceptors stay cross-cutting and never contain feature business logic.
- Use reactive forms for non-trivial forms when explicit state, validation, and testability are useful. Frontend validation is UX and must never replace backend validation or data-integrity/security enforcement.
- Default: avoid manual nested RxJS subscriptions; prefer composition operators when stream composition expresses the behavior clearly.
- A manual RxJS subscription made from Angular framework-managed code must be tied to the component/service lifecycle using the project's current Angular facilities (for example `takeUntilDestroyed`).

Technique: `angular`. Enforced by: `.claude/scripts/facets/frontend-framework.cjs` (library and tooling checks on `package.json`).
