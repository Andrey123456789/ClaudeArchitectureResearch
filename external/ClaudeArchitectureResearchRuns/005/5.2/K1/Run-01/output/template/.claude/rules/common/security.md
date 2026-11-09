---
paths:
  - "**/*"
---
Kind: STD | Scope: common | Capability: — | Loading: path-scoped (all files)

# Security Standards

Backend-specific security: `.claude/rules/backend/security.md`. Browser security: `.claude/rules/frontend/frontend.md`. Review procedure: `security-scan`. Dependency selection, versions, licenses and vulnerability checks, including for security-sensitive dependency changes: `.claude/rules/common/dependencies.md` and `add-dependency`.

## Secrets

- Never hardcode or commit real secrets, credentials, private keys, access or refresh tokens, or production connection strings in source-controlled files, including example configuration and Development settings files.
- Default: use an appropriate local secret mechanism for development (for example `dotnet user-secrets`) and environment-specific secret injection or a managed secret store for deployed environments. Do not assume a cloud provider the project has not chosen.

## Trust boundaries

- Treat data crossing the trusted application boundary as untrusted (HTTP requests, uploaded files, external-service responses, message payloads, user-provided identifiers and filters) and validate it at the layer that owns it when assumptions matter.
- Authorization must be enforced on the server. Frontend route guards, hidden or disabled UI actions and client-side checks are UX, not a security boundary.

## Transport

- Production traffic carrying credentials or sensitive data must use TLS. Respect the actual hosting topology: TLS may terminate in the application, a reverse proxy, ingress, gateway or hosting platform, and application-level HTTPS redirection is not required when that boundary already secures transport. Never disable certificate validation to make an integration work.

## Sensitive data in logs

- Never log passwords, access or refresh tokens, private keys, authentication secrets or full payment credentials. Avoid logging PII unless there is a concrete operational need and the project's privacy policy permits it. A log level does not make sensitive data safe; prefer stable technical identifiers.
- Do not serialize arbitrary request bodies, domain objects or sensitive payloads into logs by default. Log the minimum non-sensitive context that operation and diagnosis need.

## Failure behavior of security controls

- Default: security-sensitive authorization, permission and required-control checks fail safely. A lookup or configuration failure must not silently turn into success.
- When a required security control cannot be configured correctly, it must fail visibly at startup or configuration time instead of falling back to an insecure mode (authentication disabled, plaintext mode, allow-all).
