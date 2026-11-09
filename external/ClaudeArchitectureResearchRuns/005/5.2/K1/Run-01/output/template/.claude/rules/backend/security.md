---
paths:
  - "backend/**"
---
Kind: STD | Scope: backend | Capability: — | Loading: path-scoped (backend/**)

# Backend Security Standards

General security standards: `.claude/rules/common/security.md`. Technique: `authentication` knowledge skill. Review procedure: `security-scan`.

## Data access

- Use parameterized database access. Never build SQL by concatenating untrusted input, including in raw SQL, Dapper or ADO.NET code.

## Authentication and authorization

- Anonymous access must be deliberate and visible (for example `[AllowAnonymous]` against a secure global or fallback policy). Avoid redundant authorization attributes when a secure global policy already expresses the intended behavior.
- Do not implement custom token or password security, password hashing or reset-token cryptography when established ASP.NET Core authentication or Identity facilities cover the requirement.
- For Bearer/OIDC authentication, validate the properties the actual issuer or provider requires, including issuer, audience where applicable, signature or signing authority, and lifetime. Never disable validation merely to make a token work.
- Do not expose authentication-failure detail that unnecessarily reveals secrets or account state. Login behavior avoids account-enumeration leaks where relevant.

## Cryptography and data protection

- Do not implement custom cryptography when a well-reviewed platform mechanism is appropriate. Do not treat ASP.NET Core Data Protection as a universal database encryption solution; choose storage, database or platform encryption according to the actual data-protection requirement.

## Browser-facing configuration

- Default: configure CORS to the narrowest policy that satisfies the actual browser-client requirements. Never combine credentialed cross-origin requests with an unrestricted origin policy.

## Uploads

- Do not trust client-provided file metadata, such as the MIME type, as authoritative when upload handling or a security decision depends on the actual content.
