---
paths:
  - "backend/**/*"
  - "frontend/**/*"
  - "**/*.json"
  - "**/*.yml"
  - "**/*.yaml"
  - "**/*.csproj"
  - "**/*.props"
  - "**/*.targets"
  - "**/*.config"
  - "**/.env*"
  - "Dockerfile*"
  - "**/Dockerfile*"
---

> Owns: secrets, trust boundaries, SQL safety, authentication/authorization, browser credential handling, transport security, cryptography, CORS, sensitive logging, fail-safe security behavior, uploads | Scope: common (backend, frontend, configuration, delivery files) | Loads: path

# Security Rules

Public error/health response exposure: `api.md`. Dependency vulnerability and
license checks: `add-dependency` workflow. Audits: `security-scan` workflow.

## Secrets

- Never hardcode or commit real secrets, credentials, private keys,
  access/refresh tokens, or production connection strings — including in example
  or Development configuration files.
- By default, use a local secret mechanism such as `dotnet user-secrets` for
  development and environment-specific secret injection or a managed secret
  store for deployed environments. Do not assume a cloud provider the project
  has not chosen.

## Input Boundaries

Treat data crossing the trusted boundary (HTTP requests, uploaded files,
external-service responses when assumptions matter, message payloads,
user-provided identifiers and filters) as untrusted and validate it at the
owning layer (validation ownership: `error-handling.md`). Do not trust
client-provided file metadata such as MIME type as authoritative when upload
handling or security decisions depend on actual content.

## SQL and Persistence

Use parameterized database access. For raw SQL, Dapper, or ADO.NET use the
supported parameterization mechanisms; never build SQL by concatenating
untrusted input.

## Authentication and Authorization

- Enforce authorization on the server. Frontend route guards, hidden or
  disabled buttons, and client checks are UX, not a security boundary.
- Anonymous access must be deliberate and visible. Do not require redundant
  `[Authorize]` attributes when a secure global/fallback policy already
  expresses the intent.
- Do not implement custom token/password security, password hashing, or
  reset-token cryptography when established ASP.NET Core authentication/Identity
  facilities cover the requirement.
- For Bearer/OIDC authentication, validate what the actual issuer/provider
  requires — issuer, audience where applicable, signature/signing authority, and
  lifetime. Never disable validation merely to make a token work.
- Do not expose authentication-failure detail that unnecessarily reveals
  secrets or account state; login behavior avoids account-enumeration leaks
  where relevant.

## Browser Credentials

- When browser cookies automatically carry authentication credentials, the
  design must include CSRF protection; an Angular frontend does not remove the
  risk.
- Do not claim any browser token-storage mechanism is universally secure; choose
  storage from the application's threat model, and never log tokens.

## Transport Security

Production traffic carrying credentials or sensitive data must use TLS. Respect
the actual hosting topology (TLS may terminate at a proxy, ingress, gateway, or
platform), and never disable certificate validation to make an integration
work.

## Cryptography

Do not implement custom cryptography when a well-reviewed platform mechanism is
appropriate. ASP.NET Core Data Protection suits application-generated protected
payloads (cookies, temporary protected values); it is not a universal database
encryption solution.

## CORS

By default, configure CORS to the narrowest policy that satisfies the actual
browser-client requirements. Never combine credentialed cross-origin requests
with unrestricted origins.

## Logging and Sensitive Data

- Never log passwords, access/refresh tokens, private keys, authentication
  secrets, or full payment credentials. Avoid PII unless there is a concrete
  operational need permitted by the project's privacy policy. Log level does
  not make sensitive data safe.
- Do not serialize arbitrary request bodies, domain objects, or sensitive
  payloads into logs by default; log the minimum operationally useful,
  non-sensitive context, preferring stable technical identifiers.

## Failure Safety

- Security-sensitive authorization, permission, or required-control checks fail
  safely by default; never silently convert a lookup or configuration failure
  into success.
- When a required security control cannot be configured correctly, fail visibly
  at startup/configuration rather than falling back to insecure behavior.
