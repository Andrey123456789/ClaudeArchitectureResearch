---
paths:
  - "frontend/**/*"
---

> Kind: STD | Scope: frontend | Capability: — | Loading: path-scoped (frontmatter paths)

# Frontend Security Standard

- When browser cookies automatically carry authentication credentials, CSRF protection must be part of the design; never assume the SPA framework removes that risk. Bearer tokens attached explicitly through the `Authorization` header have different CSRF characteristics.
- Never claim that one browser token-storage mechanism is universally secure: choose token storage according to the application's threat model, and never log tokens.

Technique: `authentication`.
