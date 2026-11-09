---
paths:
  - "frontend/**"
---
<!-- Kind: STD | Scope: frontend | Owns: browser-side authentication security (CSRF, token storage) | Loads: path-scoped (frontend/**) -->
# Frontend Security Standards

Server authority over authorization, secrets and sensitive logging: `rules/common/security.md`.

- When browser cookies automatically carry authentication credentials, the design **must** include CSRF protection; do not assume an Angular frontend removes the risk. Bearer tokens sent explicitly in the `Authorization` header have different CSRF characteristics.
- **Must not** claim that any browser token-storage mechanism is universally secure: choose token storage by the application's threat model. Token logging is prohibited by `rules/common/security.md` § Logging and Sensitive Data.

Technique: `authentication`, `angular` knowledge skills.
