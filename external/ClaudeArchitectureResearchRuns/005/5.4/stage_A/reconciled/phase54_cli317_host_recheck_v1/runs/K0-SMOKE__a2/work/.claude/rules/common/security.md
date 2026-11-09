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

> Kind: STD | Scope: common | Owner: cross-cutting security — secrets, input trust, authorization authority, transport, sensitive logging, fail-safe behavior | Loading: path-scoped

# Security Standard — Common

See also: `rules/backend/security.md` (backend-specific security), `rules/frontend/angular.md` (browser tokens and CSRF).

## Secrets

- Never hardcode or commit real secrets, credentials, private keys, access or refresh tokens, or production connection strings in source-controlled files, example configuration files included.
- Default: a local secret mechanism such as `dotnet user-secrets` for development, and environment-specific secret injection or a managed secret store appropriate to the hosting platform for deployed environments. Do not assume a cloud provider the project has not chosen.

## Input boundaries

- Treat data crossing the trusted application boundary as untrusted — HTTP requests, uploaded files, external-service responses when assumptions matter, message or event payloads, user-provided identifiers and filters — and validate it at the layer that owns the assumption. Backend validation ownership: `rules/backend/error-handling.md`.

## Authorization authority

- Authorization must be enforced on the server. Frontend route guards, hidden or disabled buttons and other client-side checks are UX, not a security boundary.

## Transport security

- Production traffic carrying credentials or sensitive data must use TLS. Respect the actual hosting topology: TLS may terminate in the application, a reverse proxy, ingress controller, gateway or hosting platform, and in-app HTTP-to-HTTPS redirection is not required when the deployment already provides the secure transport boundary.
- Never disable certificate validation to make an integration work.

## Logging and sensitive data

- Never log passwords, access or refresh tokens, private keys, authentication secrets or full payment credentials. Avoid logging PII unless a concrete operational need exists and the project's privacy policy permits it; prefer stable technical identifiers. Changing the log level does not make sensitive data safe.
- Do not serialize arbitrary request bodies, domain objects or sensitive payloads into logs by default; log the minimum operationally useful, non-sensitive context.

## Failure behavior

- Default: security-sensitive authorization, permission and required-control checks fail safely — a lookup or configuration failure does not silently turn into success.
- A required security control that cannot be configured correctly must not fall back to an insecure mode; prefer visible startup or configuration failure.
