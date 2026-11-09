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

> Owner: secrets, trust boundaries, SQL safety, authentication and authorization, browser credentials, transport, cryptography, CORS, sensitive logging, fail-safe security behavior | Scope: common | Loads: path (application code, configuration, dependency and delivery files); read explicitly by `security-scan`, `code-review`, `verify` | Enforced: `security-scan` workflow, `verify` security check

# Security Rules

Technique: `authentication` and `configuration` skills; structured review:
`security-scan` workflow.

## Secrets

- Never hardcode or commit real secrets, credentials, private keys, access or
  refresh tokens, or production connection strings in source-controlled files,
  including example and Development configuration.
- Default: use a local secret mechanism such as `dotnet user-secrets` for
  development and environment-specific secret injection or a managed secret
  store for deployed environments; do not assume a cloud provider the project has
  not chosen.

## Input Boundaries

- Treat data from outside the trusted boundary — HTTP requests, uploaded files,
  external-service responses when assumptions matter, message payloads,
  user-provided identifiers and filters — as untrusted, and validate it at the
  owning layer (`.claude/rules/error-handling.md` § Validation Boundaries).
- Do not treat client-provided file metadata such as the MIME type as
  authoritative when upload handling or security decisions depend on the actual
  content.

## SQL and Persistence

- Use parameterized database access and never build SQL by concatenating
  untrusted input. EF Core LINQ parameterizes values; raw SQL, Dapper, and
  ADO.NET must use their supported parameter mechanisms.

## Authentication and Authorization

- Enforce authorization on the server; frontend route guards, hidden or disabled
  buttons, and other client checks are UX, not a security boundary.
- Anonymous access must be deliberate and visible; avoid redundant `[Authorize]`
  attributes when a secure global or fallback policy already expresses the
  intent.
- Do not implement custom token or password security, password hashing, or
  reset-token cryptography when established ASP.NET Core authentication or
  Identity facilities cover the requirement.
- For Bearer/OIDC authentication, validate the properties the actual issuer
  requires — issuer, audience where applicable, signature/signing authority, and
  lifetime; do not disable validation merely to make a token work.
- Do not expose authentication-failure detail that unnecessarily reveals secrets
  or account state; login flows avoid account-enumeration leaks where relevant.

## Browser Credentials

- When browser cookies carry authentication credentials automatically, include
  CSRF protection in the design; do not assume an Angular frontend removes the
  risk.
- Do not claim that one browser token-storage mechanism is universally secure;
  choose storage according to the application's threat model.

## Transport and Cryptography

- Production traffic carrying credentials or sensitive data must use TLS. Respect
  the actual hosting topology (TLS may terminate at a reverse proxy, ingress,
  gateway, or platform, so application-level HTTPS redirection is not always
  required), and never disable certificate validation to make an integration
  work.
- Do not implement custom cryptography when a well-reviewed platform mechanism is
  appropriate. ASP.NET Core Data Protection suits application-generated protected
  payloads; it is not a universal database-encryption solution.

## CORS

- Default: configure CORS to the narrowest policy that satisfies the actual
  browser-client requirements, and never combine credentialed cross-origin
  requests with an unrestricted origin policy.

## Logging and Sensitive Data

- Never log passwords, access or refresh tokens, private keys, authentication
  secrets, or full payment credentials; avoid logging PII without a concrete
  operational need the project's privacy policy permits. Changing the log level
  does not make sensitive data safe.
- Do not serialize arbitrary request bodies, domain objects, or sensitive
  payloads into logs by default; log the minimum operationally useful,
  non-sensitive context.

## Failure Behavior

- Default: security-sensitive authorization, permission, and required-control
  checks fail safely rather than silently converting lookup or configuration
  failures into success.
- When a required security control cannot be configured correctly, fail visibly
  at startup or configuration time instead of falling back insecurely.

Error-response exposure: `.claude/rules/error-handling.md` § Error Contracts.
Dependency selection and vulnerability checks: `add-dependency` workflow.
