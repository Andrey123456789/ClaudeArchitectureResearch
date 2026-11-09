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

> Path-scoped rule. Owns: secrets, trust boundaries, SQL safety, authentication and authorization, browser credentials, transport security, cryptography, CORS, sensitive data in logs, fail-safe security behavior, container hardening · Scope: common, backend, frontend, delivery · Loads: when application code, configuration, manifests, or container files are in context · Depends on: CLAUDE.md

# Security Rules

Dependency selection, versions, licenses, and vulnerability checks:
`dependencies.md` and the `add-dependency` workflow. Public error exposure:
`error-handling.md`. Technique: `authentication`, `configuration`, and `logging`
skills. Audits: `security-scan` workflow.

## Secrets

- Never hardcode or commit real secrets, credentials, private keys, access or
  refresh tokens, or production connection strings in source-controlled files,
  including example configuration files.
- Default: use a local secret mechanism such as `dotnet user-secrets` for
  development and environment-specific secret injection or a managed secret
  store appropriate to the hosting platform for deployed environments. Do not
  assume a cloud provider the project has not chosen.

## Input Boundaries

- Treat data crossing the trusted application boundary as untrusted — HTTP
  requests, uploaded files, external-service responses when assumptions
  matter, message/event payloads, user-provided identifiers and filters — and
  validate it at its owning boundary (`error-handling.md`, Validation
  Boundaries).
- Do not treat client-provided file metadata such as the MIME type as
  authoritative when upload handling or security decisions depend on the actual
  content.

## SQL and Persistence

- Use parameterized database access; never build SQL by concatenating untrusted
  input. EF Core LINQ parameterizes values automatically; for raw SQL, Dapper,
  or ADO.NET use the supported parameterization mechanisms.

## Authentication and Authorization

- Enforce authorization on the server. Frontend route guards, hidden or
  disabled buttons, and other client checks are UX, not a security boundary.
- Anonymous access must be deliberate and visible. Do not require redundant
  `[Authorize]` attributes when a secure global or fallback policy already
  expresses the intended behavior.
- Do not implement custom token or password security, password hashing, or
  reset-token cryptography when established ASP.NET Core authentication and
  Identity facilities cover the requirement.
- For Bearer/OIDC authentication, validate what the actual issuer or provider
  requires — issuer, audience where applicable, signature/signing authority,
  and lifetime. Never disable validation merely to make a token work.
- Do not expose authentication-failure detail that unnecessarily reveals
  secrets or account state; login behavior avoids account-enumeration leaks
  where relevant.

## Browser Credentials

- When browser cookies carry authentication credentials automatically, CSRF
  protection must be part of the design; an Angular frontend does not remove the
  risk.
- Do not claim that any browser token-storage mechanism is universally secure;
  choose token storage from the application's threat model, and never log
  tokens.

## Transport Security

- Production traffic carrying credentials or sensitive data must use TLS,
  respecting the actual hosting topology: TLS may terminate in the application,
  a reverse proxy, an ingress controller, a gateway, or the hosting platform.
- Never disable certificate validation to make an integration work.
- Do not require HTTP-to-HTTPS redirection when the deployment architecture
  already provides an appropriate secure transport boundary and redirection is
  not desired.

## Cryptography and Data Protection

- Do not implement custom cryptography when a well-reviewed platform mechanism
  is appropriate.
- ASP.NET Core Data Protection suits application-generated protected payloads
  such as cookies or temporary protected values; do not treat it as universal
  database encryption. Use storage, database, or platform encryption according
  to the actual data-protection requirement.

## CORS

- Default: configure CORS to the narrowest policy that satisfies the actual
  browser-client requirements. Never combine credentialed cross-origin requests
  with an unrestricted origin policy. A public unauthenticated API may
  legitimately need a different policy than a private browser application.

## Logging and Sensitive Data

- Never log passwords, access or refresh tokens, private keys, authentication
  secrets, or full payment credentials. Avoid logging PII unless there is a
  concrete operational requirement and the project's privacy/security policy
  permits it. Changing the log level does not make sensitive data safe; prefer
  stable technical identifiers over personal data in operational logs.
- Do not serialize arbitrary request bodies, domain objects, or sensitive
  payloads into logs by default; log the minimum operationally useful,
  non-sensitive context.

## Failure Behavior

- Default: security-sensitive authorization, permission, and required-control
  checks fail safely rather than silently converting lookup or configuration
  failures into success.
- When a required security control cannot be configured correctly, fail
  visibly at startup or configuration time instead of falling back to insecure
  behavior.

## Containers

- Default: production containers use an appropriate runtime image (for example
  the ASP.NET Core runtime image for an API), not the SDK image for convenience,
  and do not switch to root merely to bypass a filesystem permission problem.
