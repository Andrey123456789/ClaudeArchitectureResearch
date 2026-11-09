---
paths:
  - "**/*"
---

> Level: 0-core · Owns: secrets, trust boundaries, data access safety, authentication/authorization, transport, CORS, sensitive data, fail-safe behavior · Scope: common (backend, frontend, configuration, delivery) · Loading: path

# Security Rules

## Secrets

- Never hardcode or commit real secrets, credentials, private keys, access/refresh tokens, or production connection strings — including in example or Development configuration files.
- Default: use a local secret mechanism (such as `dotnet user-secrets`) in development and environment-specific injection or a managed secret store in deployed environments; do not assume a cloud provider the project has not chosen.

## Input and data access

- Treat data crossing the trusted boundary — HTTP requests, uploads, external-service responses, message payloads, user-supplied identifiers and filters — as untrusted, and validate it at the owning layer where assumptions matter.
- Use parameterized database access; never build SQL by concatenating untrusted input.
- Do not trust client-provided file metadata such as MIME type as authoritative when upload handling or security decisions depend on actual content.

## Authentication and authorization

- Enforce authorization on the server; frontend route guards, hidden or disabled buttons, and client checks are UX, not a security boundary.
- Anonymous access must be deliberate and visible; avoid redundant authorization attributes when a secure global or fallback policy already expresses the intent.
- Do not implement custom token or password security, password hashing, or reset-token cryptography when the platform's established authentication and account-management facilities cover the requirement.
- For Bearer/OIDC authentication, validate what the actual issuer requires — issuer, audience where applicable, signature/signing authority, lifetime; never disable validation to make a token work.
- Do not expose authentication-failure detail that unnecessarily reveals secrets or account state; login behavior avoids account-enumeration leaks where relevant.
- When browser cookies carry authentication credentials automatically, include CSRF protection in the design; do not assume the frontend framework removes the risk.
- Do not claim any browser token-storage mechanism is universally secure; choose storage by the application's threat model (tokens are never logged — see Sensitive data and logs).

## Transport, browser, cryptography

- Production traffic carrying credentials or sensitive data must use TLS; respect the actual hosting topology (TLS may terminate at a proxy or platform) and never disable certificate validation to make an integration work.
- Default: configure CORS as the narrowest policy satisfying actual browser-client requirements; never combine credentialed cross-origin requests with unrestricted origins.
- Do not implement custom cryptography when a well-reviewed platform mechanism fits; do not treat the platform's data-protection mechanism for application payloads (protected cookies, temporary tokens) as universal database encryption.

## Sensitive data and logs

- Never log passwords, access/refresh tokens, private keys, authentication secrets, or full payment credentials; avoid PII without a concrete permitted operational need. Log level is not a privacy control.
- Do not serialize arbitrary request bodies, domain objects, or sensitive payloads into logs by default; log the minimum operationally useful non-sensitive context.

## Failure behavior

- Default: security-sensitive authorization, permission, and required-control checks fail safely; never silently convert a lookup or configuration failure into success.
- When a required security control cannot be configured correctly, prefer a visible startup/configuration failure over an insecure fallback.

Dependency vulnerability and license checks: `add-dependency`. Audits: `security-scan`.
