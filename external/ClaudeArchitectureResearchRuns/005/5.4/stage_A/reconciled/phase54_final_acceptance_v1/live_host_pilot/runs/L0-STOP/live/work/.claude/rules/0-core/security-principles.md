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

> Level: 0 Core · Owns: technology-neutral security principles and error/diagnostic exposure · Scope: common · Loads: path rule · Depends on: CLAUDE.md

# Security Principles

Technology bindings live in `.claude/rules/2-technology/`; depth lives in the `authentication` and `security-scan` skills.

## Secrets

- Never hardcode or commit real secrets, credentials, private keys, access/refresh tokens, or production connection strings — including in example configuration files.
- Use an appropriate local secret mechanism for development and environment-specific secret injection or a managed secret store for deployed environments; do not assume a cloud provider the project has not chosen (default).

## Trust boundaries

- Treat data crossing the trusted application boundary as untrusted — HTTP requests, uploaded files, external-service responses, message payloads, user-provided identifiers and filters — and validate it at the owning layer when assumptions matter.
- Do not trust client-provided file metadata such as the MIME type as authoritative when upload handling or a security decision depends on the actual content.
- Use parameterized database access; never build SQL by concatenating untrusted input.

## Authentication and authorization

- Enforce authorization on the server. Frontend route guards, hidden buttons, and client checks are user experience, not a security boundary.
- Anonymous access must be deliberate and visible; avoid redundant authorization markers when a secure global or fallback policy already expresses the intent.
- Do not implement custom token or password security, password hashing, or reset-token cryptography when the platform's established authentication and identity facilities cover the requirement.
- For Bearer/OIDC authentication, validate what the actual issuer/provider requires — issuer, audience where applicable, signature/signing authority, and lifetime. Never disable validation merely to make a token work.
- Do not expose authentication-failure detail that unnecessarily reveals secrets or account state; login behavior avoids account-enumeration leaks where relevant.
- When browser cookies automatically carry authentication credentials, include CSRF protection in the design; a single-page frontend does not remove that risk.
- Do not claim that one browser token-storage mechanism is universally secure; choose storage according to the application's threat model, and never log tokens.

## Transport and cryptography

- Production traffic carrying credentials or sensitive data must use TLS. Respect the actual hosting topology (TLS may terminate at a proxy, ingress, gateway, or platform) and never disable certificate validation to make an integration work.
- Do not implement custom cryptography when a well-reviewed platform mechanism is appropriate.
- Configure CORS to the narrowest policy that satisfies the actual browser-client requirements; never combine credentialed cross-origin requests with unrestricted origins (default).

## Failing safely

- Security-sensitive authorization, permission, or required-control checks fail safely; do not silently convert lookup or configuration failures into success (default).
- When a required security control cannot be configured correctly, prefer a visible startup or configuration failure over an insecure fallback.

## Error and diagnostic exposure

- Do not expose stack traces, SQL details, connection strings, internal paths, secret values, or sensitive exception details in public API errors.
- Do not expose secrets, credentials, connection details, stack traces, or unnecessary internal diagnostics through publicly reachable health responses.

Logging of sensitive data: `logging-principles.md`. Dependency vulnerability and license checks: `add-dependency`.
