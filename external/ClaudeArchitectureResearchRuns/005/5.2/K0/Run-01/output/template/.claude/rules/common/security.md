---
paths:
  - "backend/**"
  - "frontend/**"
  - "*.slnx"
  - "*.props"
  - "global.json"
  - "**/*.yml"
  - "**/*.yaml"
  - "**/Dockerfile*"
  - "**/.env*"
---
<!-- Kind: STD | Scope: common | Owns: secrets, input trust, server authority, transport security, sensitive logging, fail-safe security controls | Loads: path-scoped (common globs) -->
# Common Security Standards

Server-side authentication, cryptography, CORS and uploads: `rules/backend/security.md`. Browser-side authentication: `rules/frontend/security.md`.

## Secrets

- **Never** hardcode or commit real secrets, credentials, private keys, access or refresh tokens, or production connection strings in source-controlled files, including example configuration.
- **Default:** a local secret mechanism such as `dotnet user-secrets` for development, and environment-specific secret injection or a managed secret store for deployed environments. Do not assume a cloud provider the project has not chosen.

## Input Trust

- Data crossing the trusted application boundary **must** be treated as untrusted and validated at the owning layer when assumptions matter: HTTP requests, uploaded files, external-service responses, message/event payloads, user-provided identifiers and filters. Validation placement: `rules/backend/error-handling.md` § Validation Boundaries.

## Server Authority

- Authorization **must** be enforced on the server. Frontend route guards, hidden or disabled buttons and other client checks are UX, not a security boundary.

## Transport Security

- Production traffic carrying credentials or sensitive data **must** use TLS. Respect the actual hosting topology — TLS may terminate in the application, a reverse proxy, ingress, gateway or hosting platform — and **never** disable certificate validation to make an integration work.
- HTTP-to-HTTPS redirection in the application is not required when the deployment already provides the secure transport boundary and redirection is not wanted.

## Logging and Sensitive Data

- **Never** log passwords, access or refresh tokens, private keys, authentication secrets or full payment credentials. Avoid logging PII unless there is a concrete operational need the project's privacy/security policy permits. A log level does not make sensitive data safe; prefer stable technical identifiers over personal data.
- **Must not** serialize arbitrary request bodies, domain objects or sensitive payloads into logs by default; log the minimum operationally useful, non-sensitive context.

## Failure Behavior

- **Default:** security-sensitive authorization, permission and required-control checks fail safely rather than silently converting lookup or configuration failures into success.
- When a required security control cannot be configured correctly, visible startup/configuration failure **must** be preferred over an insecure fallback.

Workflow: dependency security checks — `add-dependency`; security audits — `security-scan`.
