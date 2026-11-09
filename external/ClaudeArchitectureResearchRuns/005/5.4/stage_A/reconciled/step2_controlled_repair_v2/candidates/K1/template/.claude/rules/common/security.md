---
paths:
  - "**/*"
---

> Kind: STD | Scope: common | Capability: — | Loading: path-scoped (frontmatter paths)

# Security Standard (all code and configuration)

## Secrets

- Never hardcode or commit real secrets, credentials, private keys, access/refresh tokens, or production connection strings, including in example configuration files.
- Default: a local secret mechanism such as `dotnet user-secrets` for development, and environment-specific secret injection or a managed secret store for deployed environments. Do not assume a cloud provider the project has not chosen.

## Trust boundaries

- Data crossing the trusted application boundary is untrusted: HTTP requests, uploaded files, external-service responses, message/event payloads, user-provided identifiers and filters. Validate it at the owning layer when assumptions matter.
- Authorization must be enforced on the server. Frontend route guards, hidden or disabled UI actions, and client-side checks are UX, not a security boundary.

## Transport

- Production traffic carrying credentials or sensitive data must use TLS. Respect the actual hosting topology: TLS may terminate in the application, a reverse proxy, ingress, gateway, or hosting platform, so application-level HTTP-to-HTTPS redirection is not required where the deployment already provides a secure transport boundary and redirection is not desired.
- Never disable certificate validation to make an integration work.

## Logging and sensitive data

- Never log passwords, access or refresh tokens, private keys, authentication secrets, or full payment credentials. Avoid logging PII unless a concrete operational requirement exists and the project's privacy/security policy permits it. A lower log level does not make sensitive data safe; prefer stable technical identifiers.
- Do not serialize arbitrary request bodies, domain objects, or sensitive payloads into logs by default; log the minimum operationally useful, non-sensitive context.

## Failure behavior

- Default: security-sensitive authorization, permission, and required-control checks fail safely; never silently convert a lookup or configuration failure into success.
- A required security control that cannot be configured correctly must fail visibly at startup/configuration time instead of falling back to an insecure mode.

Related: dependency security checks — `add-dependency`; security audits — `security-scan`.
