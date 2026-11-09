---
paths:
  - "backend/**"
  - "frontend/**"
  - "**/*.json"
  - "**/*.yml"
  - "**/*.yaml"
  - "**/*.props"
  - "**/*.targets"
  - "**/*.config"
  - "**/.env*"
  - "**/Dockerfile*"
---

> Level: 0 Core · Owns: technology-neutral security principles and security-review discipline · Scope: common · Loads: path; read explicitly by `security-scan`

# Security Principles

## Secrets

- **Must not** hardcode or commit real secrets, credentials, private keys, access or refresh tokens, or production connection strings — including in example configuration files.
- **Default:** supply development secrets through a local secret store and deployed-environment secrets through environment-specific injection or a managed secret store suited to the hosting platform. Do not assume a cloud provider the project has not chosen.

## Untrusted input

- **Must** treat data crossing the trusted application boundary — requests, uploaded files, external-service responses, message payloads, user-provided identifiers and filters — as untrusted and validate it at the owning layer when assumptions matter.
- **Must not** treat client-provided file metadata such as MIME type or file name as authoritative when upload handling or a security decision depends on the actual content.
- **Must** use parameterized database access; never build SQL by concatenating untrusted input.

## Authentication and authorization

- **Must** enforce authorization on the server. Frontend route guards, hidden or disabled buttons and client checks are user experience, not a security boundary.
- **Must** make anonymous access deliberate and visible; avoid redundant per-endpoint authorization declarations when a secure global policy already expresses the intent.
- **Default:** security-sensitive authorization, permission and required-control checks fail safely; a lookup or configuration failure never silently becomes success.
- **Must not** implement custom token or password security, password hashing or reset-token cryptography when established platform authentication facilities cover the requirement.
- **Must** keep effective token validation for bearer-token or OpenID Connect authentication: validate what the actual issuer requires — issuer, audience where applicable, signature/signing authority, lifetime — and never disable validation merely to make a token work.
- **Must not** expose authentication-failure detail that unnecessarily reveals secrets or account state; login flows avoid account-enumeration leaks where relevant.
- **Must** include CSRF protection in the design whenever browser cookies carry authentication credentials automatically; a single-page frontend does not remove that risk.
- **Must not** claim that one browser token-storage mechanism is universally secure; choose storage from the application's threat model.

## Transport, cryptography and CORS

- **Must** use TLS for production traffic that carries credentials or sensitive data, respecting the actual hosting topology (TLS may terminate at a proxy, ingress, gateway or platform). Never disable certificate validation to make an integration work.
- **Must not** implement custom cryptography when a well-reviewed platform mechanism is appropriate; choose protection per requirement (one-way hashing for passwords, platform or database encryption for data at rest).
- **Default:** configure CORS with the narrowest policy that satisfies the actual browser clients; **never** combine credentialed cross-origin requests with unrestricted origins.

## Failure and error exposure

- **Must** fail visibly at startup or configuration time when a required security control cannot be configured correctly, rather than falling back to an insecure mode.
- **Must not** expose stack traces, SQL, connection strings, internal paths, secret values or sensitive exception details in public error responses.

## Security review discipline (procedure: `security-scan`)

- **Must** distinguish confirmed findings from items that need verification, and assign severity from exploitability, reachability, impact and application context — not from suspicious patterns or raw advisory scores alone.
- **Must not** make a security review depend on one specific scanner, analyzer, service or external tool; available tool output is evidence, not authority.
