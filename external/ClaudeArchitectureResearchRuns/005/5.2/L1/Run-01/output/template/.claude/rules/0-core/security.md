---
paths:
  - "**/*"
---
> Level: 0-core | Owns: security invariants for code, configuration, and secrets | Scope: common, backend, frontend | Loads: path (all files)

# Security Rules

## Secrets

- Never hardcode or commit real secrets, credentials, private keys, access or
  refresh tokens, or production connection strings — including in example
  configuration files.
- Default: use a local secret mechanism such as `dotnet user-secrets` for
  development, and environment-specific secret injection or a managed secret
  store appropriate to the hosting platform for deployed environments. Do not
  assume a specific cloud provider unless the project has chosen one.

## Input boundaries

Treat data from outside the trusted application boundary as untrusted and
validate it at the layer that owns the assumption when the assumption matters:
HTTP requests, uploaded files, external-service responses, message/event
payloads, and user-provided identifiers and filters.

## Data access

Use parameterized database access. The persistence technology's query API
parameterizes values for ordinary queries; for raw SQL or lower-level data
access use the supported parameterization mechanism. Never build SQL by
concatenating untrusted input.

## Authentication and authorization

- Enforce authorization on the server. Frontend route guards, hidden or disabled
  buttons, and client-side checks are UX, not a security boundary.
- Anonymous access must be deliberate and visible. Default to explicit,
  reviewable authorization (global/fallback policy, controller/action
  attributes, or endpoint configuration); avoid redundant `[Authorize]`
  attributes when a secure global policy already expresses the intent.
- Do not implement custom token or password security, password hashing, or
  reset-token cryptography when established ASP.NET Core authentication or
  ASP.NET Core Identity facilities cover the requirement.
- For Bearer/OIDC authentication, validate what the actual issuer/provider
  requires — issuer, audience where applicable, signature/signing authority,
  and lifetime. Do not disable validation merely to make a token work.
- Do not expose authentication-failure detail that unnecessarily reveals secrets
  or account state; login and recovery behavior must avoid account-enumeration
  leaks where relevant.

## Browser clients

- When browser cookies carry authentication credentials automatically, include
  CSRF protection in the design; do not assume the frontend framework removes
  the risk. Bearer tokens sent explicitly in the `Authorization` header have
  different CSRF characteristics.
- Do not claim that one browser token-storage mechanism is universally secure;
  choose storage according to the application's threat model, and never log
  tokens (see Logging and sensitive data).
- Default CORS to the narrowest policy that satisfies actual browser-client
  requirements. Never combine credentialed cross-origin requests with an
  unrestricted origin policy. CORS is not authorization.

## Transport

Production traffic carrying credentials or sensitive data must use TLS. Respect
the actual hosting topology (TLS may terminate at the application, a reverse
proxy, an ingress, a gateway, or the platform). Never disable certificate
validation to make an integration work.

## Cryptography and data protection

Do not implement custom cryptography when a well-reviewed platform mechanism is
appropriate. ASP.NET Core Data Protection suits application-generated protected
payloads (cookies, temporary protected values); do not treat it as universal
database encryption — use storage, database, or platform encryption according
to the actual requirement.

## Failure behavior

- Default: security-sensitive authorization, permission, and required-control
  checks fail safely; never silently convert a lookup or configuration failure
  into success.
- When a required security control cannot be configured correctly, fail
  visibly at startup or configuration time instead of falling back to an
  insecure mode.

## Uploads

Do not treat client-provided file metadata, such as the declared MIME type, as
authoritative when upload handling or a security decision depends on the
actual content.

## Logging and sensitive data

- Never log passwords, access or refresh tokens, private keys, authentication
  secrets, or full payment credentials. Avoid logging PII unless a concrete
  operational need exists and the project's privacy policy permits it. A log
  level is not a privacy control; prefer stable technical identifiers.
- Do not serialize arbitrary request bodies, domain objects, or sensitive
  payloads into logs by default; log the minimum operationally useful,
  non-sensitive context.

Public error-response content: `error-handling.md`. Dependency security checks:
`add-dependency`.
