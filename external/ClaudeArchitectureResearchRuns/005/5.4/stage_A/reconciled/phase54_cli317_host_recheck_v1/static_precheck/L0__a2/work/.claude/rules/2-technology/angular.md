---
paths:
  - "frontend/**/*"
---

> Level: 2 Technology · Owns: Angular bindings — standalone APIs, Signals vs RxJS, subscriptions, interceptors, reactive forms · Scope: frontend · Loads: path rule · Depends on: CLAUDE.md, .claude/rules/1-architecture/frontend-structure.md

# Angular Bindings

Structural rules (feature organization, HTTP boundary, state, errors, validation role): `1-architecture/frontend-structure.md`. Technique: the `angular` skill.

- Use modern standalone Angular APIs for new code, organized by feature as `frontend-structure.md` requires; do not introduce NgModules for ordinary new feature work unless an integration or legacy dependency genuinely requires them (default).
- Use Signals for naturally synchronous, local UI state and RxJS when asynchronous streams, HTTP composition, cancellation, or event pipelines are clearer; avoid mechanical conversions between them (default).
- Avoid manual nested RxJS subscriptions; prefer composition operators when stream composition expresses the behavior clearly (default).
- When manually subscribing from Angular framework-managed code, tie the subscription's lifetime to the component or service lifecycle using the project's current Angular facilities.
- Prefer functional HTTP interceptors for new code and keep interceptor responsibilities cross-cutting; never put feature business logic in an interceptor (default).
- Use reactive forms for non-trivial forms when explicit state, validation, and testability are useful (default).
- Unit and component tests run with the workspace's configured runner; inspect `package.json` instead of assuming a command (the baseline runner for new workspaces is recorded in `3-project/decisions.md`).
