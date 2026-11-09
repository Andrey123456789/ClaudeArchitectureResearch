---
paths:
  - "backend/**"
---
<!-- Kind: STD | Scope: backend | Owns: server-side authentication and authorization, cryptography, CORS, upload trust | Loads: path-scoped (backend/**) -->
# Backend Security Standards

Secrets, input trust, server authority, TLS, sensitive logging and fail-safe checks: `rules/common/security.md`.

## Authentication and Authorization

- Anonymous access **must** be deliberate and visible (for example `[AllowAnonymous]` where the project otherwise defaults to authenticated access); avoid redundant `[Authorize]` attributes when a secure global or fallback policy already expresses the intent.
- **Must not** implement custom token or password security, password hashing or reset-token cryptography when established ASP.NET Core authentication or Identity facilities cover the requirement.
- Bearer/OIDC authentication **must** validate the properties required by the actual issuer or provider — issuer, audience where applicable, signature/signing authority and lifetime — and **must not** disable validation merely to make a token work.
- Authentication failures **must not** expose detail that unnecessarily reveals secrets or account state; login behavior avoids account-enumeration leaks where relevant.

## Cryptography and Data Protection

- **Must not** implement custom cryptography when a well-reviewed platform mechanism is appropriate, and **must not** treat ASP.NET Core Data Protection as universal database encryption: it suits application-generated protected payloads such as cookies or temporary protected values; choose storage, database or platform encryption by the actual protection requirement.

## CORS

- **Default:** the narrowest CORS policy that satisfies the actual browser-client requirements; **never** combine credentialed cross-origin requests with unrestricted origins. A public unauthenticated API may legitimately differ from a private browser application.

## Uploads

- Client-provided file metadata such as the MIME type **must not** be treated as authoritative when upload handling or security decisions depend on actual content.

Technique: `authentication` knowledge skill. Workflow: audits — `security-scan`.
