---
paths:
  - "backend/**/*"
  - "frontend/**/*"
  - "**/*.json"
  - "**/*.yml"
  - "**/*.yaml"
  - "**/.*.yml"
  - "**/.*.yaml"
  - ".github/**"
  - "**/*.csproj"
  - "**/*.props"
  - "**/*.targets"
  - "**/*.config"
  - "**/*.ps1"
  - "**/*.sh"
  - "**/.env*"
  - "Dockerfile*"
  - "**/Dockerfile*"
---

> Owns: secrets, trust boundaries, SQL safety, authentication and authorization, transport, cryptography, CORS, sensitive logging, fail-safe security behavior, container runtime images | Scope: common | Loads: path-scoped (application code, configuration, manifests, scripts, delivery files)

# Security Rules

Security review procedure: `security-scan`. Authentication technique:
`authentication` skill.

## Secrets

- Never hardcode or commit real secrets, credentials, private keys, access or
  refresh tokens, or production connection strings in source-controlled files,
  including example configuration files.
- Use an appropriate local secret mechanism such as `dotnet user-secrets` for
  development, and environment-specific secret injection or a managed secret
  store for deployed environments. Do not assume a specific cloud provider
  unless the project has chosen one.

## Input Boundaries

- Treat data crossing the trusted application boundary as untrusted — HTTP
  requests, uploaded files, external-service responses when assumptions matter,
  message/event payloads, user-provided identifiers and filters — and validate
  it at the owning layer when assumptions matter.
- Do not trust client-provided file metadata such as the MIME type as
  authoritative when upload handling or security decisions depend on the actual
  content.

## SQL and Persistence

Use parameterized database access. EF Core LINQ parameterizes values; for raw
SQL, Dapper, or ADO.NET use the supported parameterization mechanisms. Never
build SQL by concatenating untrusted input.

## Authentication and Authorization

- Enforce authorization on the server. Frontend route guards, hidden or
  disabled buttons, and client-side checks are UX, not a security boundary.
- Anonymous access must be deliberate and visible; do not require redundant
  `[Authorize]` attributes when a secure global or fallback policy already
  expresses the intended behavior.
- Do not implement custom token or password security, password hashing, or
  reset-token cryptography when established ASP.NET Core authentication or
  Identity facilities cover the requirement.
- For Bearer/OIDC authentication, validate the properties required by the
  actual issuer or provider — issuer, audience where applicable,
  signature/signing authority, and lifetime. Do not disable validation merely to
  make a token work.
- Do not expose authentication-failure detail that unnecessarily reveals
  secrets or account state; login behavior avoids account-enumeration leaks
  where relevant.
- When browser cookies automatically carry authentication credentials, include
  CSRF protection in the design; an Angular frontend does not remove that risk.
- Do not claim that one browser token-storage mechanism is universally secure;
  choose token storage according to the application's threat model, and never
  log tokens.

## Transport Security

Production traffic carrying credentials or sensitive data must use TLS. Respect
the actual hosting topology — TLS may terminate in the application, a reverse
proxy, ingress controller, gateway, or hosting platform, and in-app HTTPS
redirection is not required when that boundary already provides secure
transport. Never disable certificate validation to make an integration work.

## Cryptography and Data Protection

Do not implement custom cryptography when a well-reviewed platform mechanism is
appropriate. ASP.NET Core Data Protection suits application-generated protected
payloads such as cookies or temporary protected values; do not treat it as a
universal database encryption solution — use storage, database, or platform
encryption according to the actual requirement.

## CORS

Configure CORS to the narrowest policy that satisfies the actual browser-client
requirements by default. Never combine credentialed cross-origin requests with
an unrestricted origin policy. A public unauthenticated API may legitimately
need a different policy than a private browser application.

## Logging and Sensitive Data

- Never log passwords, access or refresh tokens, private keys, authentication
  secrets, or full payment credentials. Avoid logging PII unless there is a
  concrete operational need that the project's privacy and security policy
  permits. Changing the log level does not make sensitive data safe; prefer
  stable technical identifiers.
- Do not serialize arbitrary request bodies, domain objects, or sensitive
  payloads into logs by default; log the minimum operationally useful,
  non-sensitive context.

## Failure Behavior

- By default, security-sensitive authorization, permission, or required-control
  checks fail safely rather than silently converting lookup or configuration
  failures into success.
- When a required security control cannot be configured correctly, prefer a
  visible startup or configuration failure over an insecure fallback.
- Public error responses: `error-handling.md`.

## Containers

By default, production containers use an appropriate runtime image (the ASP.NET
runtime image for ASP.NET Core) rather than the SDK image for convenience, and do
not switch to root merely to bypass filesystem permission problems.

## Dependencies

Dependency selection, versioning, licensing, and vulnerability checks are owned
by `dependencies.md` and `add-dependency`; security-sensitive dependency changes
must not bypass them.
