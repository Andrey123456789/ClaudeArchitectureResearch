---
paths:
  - "backend/**/*.cs"
  - "backend/**/appsettings*.json"
---

> Kind: STD | Scope: backend | Owner: backend security — SQL safety, authentication and authorization configuration, cryptography, CORS, uploads | Loading: path-scoped

# Security Standard — Backend

See also: `rules/common/security.md` (secrets, input trust, server-side authorization, transport, sensitive logging, fail-safe behavior).

Authentication architecture changes are Reserved (CLAUDE.md § Decisions).

## SQL and persistence

- Use parameterized database access: EF Core LINQ, or the supported parameterization of raw SQL, Dapper or ADO.NET. Never build SQL by concatenating untrusted input.

## Authentication and authorization

- Default to explicit, reviewable authorization (global or fallback policies, controller or action attributes, endpoint configuration). Anonymous access must be deliberate and visible; avoid redundant `[Authorize]` attributes when a secure global policy already expresses the intent.
- Do not implement custom token or password security, password hashing or reset-token cryptography when established ASP.NET Core authentication or Identity facilities cover the requirement.
- For Bearer/OIDC authentication, validate what the actual issuer requires — issuer, audience where applicable, signature/signing authority and lifetime; never disable validation to make a token work.
- Authentication failures must not expose detail that unnecessarily reveals secrets or account state; login behavior avoids account-enumeration leaks where relevant.

## Cryptography and data protection

- Do not implement custom cryptography when a well-reviewed platform mechanism is appropriate. ASP.NET Core Data Protection suits application-generated protected payloads (cookies, temporary protected values); do not treat it as universal database encryption — use storage, database or platform encryption according to the actual requirement.

## CORS

- Default: the narrowest CORS policy that satisfies the actual browser-client requirements. Never combine credentialed cross-origin requests with an unrestricted origin policy.

## Uploads

- Do not treat client-provided file metadata such as the MIME type as authoritative when upload handling or a security decision depends on the actual content.
