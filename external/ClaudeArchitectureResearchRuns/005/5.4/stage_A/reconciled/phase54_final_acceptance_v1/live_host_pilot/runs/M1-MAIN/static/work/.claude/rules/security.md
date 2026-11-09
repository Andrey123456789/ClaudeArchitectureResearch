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

> Path rule · Scope: common · Owns secrets, trust boundaries, SQL safety, authentication and authorization, transport, data protection, CORS, sensitive logging, fail-safe behavior, uploads, and container hardening

# Security Rules

Public error responses: `.claude/rules/error-handling.md`. Dependency
security: `add-dependency` workflow. Audit procedure: `security-scan` workflow.

## Secrets

- Never hardcode or commit real secrets, credentials, private keys, access or
  refresh tokens, or production connection strings in source-controlled files,
  including example configuration files.
- By default use an appropriate local secret mechanism such as
  `dotnet user-secrets` for development, and environment-specific secret
  injection or a managed secret store for deployed environments. Do not assume a
  specific cloud provider unless the project has chosen one.

## Input Boundaries

Treat data from outside the trusted application boundary as untrusted — HTTP
requests, uploaded files, external-service responses when assumptions matter,
message/event payloads, user-provided identifiers and filters — and validate it
at the owning layer (`error-handling.md` § Validation Boundaries) when
assumptions matter.

## SQL and Persistence

Use parameterized database access. Never build SQL by concatenating untrusted
input; for raw SQL, micro-ORMs, or ADO.NET use the supported parameterization
mechanisms.

## Authentication and Authorization

- Enforce authorization on the server. Frontend route guards, hidden or disabled
  buttons, and client-side checks are UX, not a security boundary.
- Anonymous access must be deliberate and visible. A project may secure
  endpoints with global/fallback policies, controller or action attributes, or
  endpoint configuration; avoid redundant `[Authorize]` attributes when a secure
  global policy already expresses the intent.
- Do not implement custom token or password security, password hashing, or
  reset-token cryptography when established ASP.NET Core authentication or
  Identity facilities cover the requirement.
- For Bearer/OIDC authentication, validate the properties required by the
  actual issuer or provider — issuer, audience where applicable, signature or
  signing authority, and lifetime. Do not disable validation merely to make a
  token work.
- Do not expose authentication-failure detail that unnecessarily reveals
  secrets or account state; login behavior avoids account-enumeration leaks
  where relevant.
- When browser cookies carry authentication credentials automatically, include
  CSRF protection in the design; do not assume the frontend framework removes
  that risk.
- Do not claim that one browser token-storage mechanism is universally secure;
  choose token storage according to the application's threat model.

## HTTPS and Transport Security

Production traffic carrying credentials or sensitive data must use TLS. Respect
the actual hosting topology — TLS may terminate in the application, a reverse
proxy, an ingress controller, a gateway, or the hosting platform — and do not
require HTTP-to-HTTPS redirection when the deployment already provides an
appropriate secure transport boundary. Never disable certificate validation to
make an integration work.

## Data Protection and Encryption

Do not implement custom cryptography when a well-reviewed platform mechanism is
appropriate. ASP.NET Core Data Protection suits application-generated protected
payloads such as cookies or temporary protected values; do not treat it as a
universal database encryption solution. Use storage, database, or platform
encryption according to the actual data-protection requirement.

## CORS

By default configure CORS to the narrowest policy that satisfies the actual
browser-client requirements; a public unauthenticated API may legitimately
differ from a private browser application. Never combine credentialed
cross-origin requests with an unrestricted origin policy.

## Logging and Sensitive Data

- Never log passwords, access or refresh tokens, private keys, authentication
  secrets, or full payment credentials. Avoid logging PII unless there is a
  concrete operational requirement and the project's privacy/security policy
  permits it; prefer stable technical identifiers. Changing the log level does
  not make sensitive data safe.
- Do not serialize arbitrary request bodies, domain objects, or sensitive
  payloads into logs by default; log the minimum operationally useful,
  non-sensitive context.

## Failure Handling

- By default, security-sensitive authorization, permission, or required-control
  checks fail safely; they do not silently convert lookup or configuration
  failures into success.
- When a required security control cannot be configured correctly, prefer a
  visible startup or configuration failure over an insecure fallback.
- Do not trust client-provided file metadata such as MIME type as authoritative
  when upload handling or security decisions depend on actual content.

## Containers

For production containers, by default use an appropriate runtime image rather
than the SDK image solely for convenience, and do not switch to root merely to
bypass filesystem permission problems.
