---
paths:
  - "backend/**"
  - "frontend/**"
  - "docs/**"
  - ".github/**"
  - "**/*.json"
  - "**/*.yml"
  - "**/*.yaml"
  - "**/*.props"
  - "**/*.targets"
  - "**/*.config"
  - "**/*.csproj"
  - "**/*.slnx"
  - "**/.env*"
  - "**/Dockerfile*"
  - "**/*.ps1"
  - "**/*.sh"
---

> Level: 0 Core | Owns: technology-neutral security principles (secrets, trust boundaries, data access, authorization, transport, cryptography, browser security, fail-safe behavior) | Scope: common, backend, frontend | Loads: path | Depends on: none

# Security Principles

## Secrets

- Never hardcode or commit real secrets, credentials, private keys, access or
  refresh tokens, or production connection strings — including in example or
  Development configuration files.
- Default: use a local secret mechanism for development and environment-specific
  secret injection or a managed secret store for deployed environments; do not
  assume a cloud provider the project has not chosen.

## Trust Boundaries

- Treat data crossing the trusted application boundary as untrusted (HTTP
  requests, uploaded files, external-service responses, message payloads,
  user-provided identifiers and filters) and validate it at the owning layer
  when assumptions matter.
- Do not trust client-provided file metadata such as the MIME type as
  authoritative when upload handling or a security decision depends on the
  actual content.

## Data Access

- Use parameterized database access; never build SQL by concatenating
  untrusted input.

## Authentication and Authorization

- Enforce authorization on the server. Frontend route guards, hidden or
  disabled buttons, and other client checks are UX, not a security boundary.
- Anonymous access must be deliberate and visible; avoid redundant
  authorization annotations when a secure global policy already expresses the
  intent.
- For Bearer/OIDC authentication, validate the properties the actual issuer
  requires — issuer, audience where applicable, signature or signing authority,
  and lifetime; do not disable validation merely to make a token work.
- Do not expose authentication-failure detail that unnecessarily reveals secrets
  or account state; login behavior avoids account-enumeration leaks where
  relevant.

## Transport and Cryptography

- Production traffic carrying credentials or sensitive data must use TLS;
  respect the actual hosting topology (TLS may terminate at a proxy, ingress,
  gateway, or platform, so application-level HTTPS redirection is not required
  when the deployment already provides that boundary) and never disable
  certificate validation to make an integration work.
- Do not implement custom cryptography when a well-reviewed platform mechanism
  is appropriate; choose storage, database, or platform encryption according to
  the actual data-protection requirement.

## Browser Security

- Default: configure CORS to the narrowest policy that satisfies the actual
  browser-client requirements; never combine credentialed cross-origin requests
  with unrestricted origins.
- When browser cookies carry authentication credentials automatically, include
  CSRF protection in the design; do not assume the frontend framework removes
  the risk.
- Do not claim that one browser token-storage mechanism is universally secure;
  choose storage according to the application's threat model and never log
  tokens.

## Fail-Safe Behavior

- Default: security-sensitive authorization, permission, or required-control
  checks fail safely; do not silently convert lookup or configuration failures
  into success.
- When a required security control cannot be configured correctly, prefer a
  visible startup or configuration failure over an insecure fallback.

Dependency selection, versioning, and vulnerability checks: → `add-dependency`.
