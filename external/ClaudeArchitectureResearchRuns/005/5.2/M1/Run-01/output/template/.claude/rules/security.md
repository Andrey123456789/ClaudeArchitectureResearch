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

> **Policy rule** · Owns: secrets, untrusted input, SQL parameterization, server-side authorization, authentication mechanisms, transport security, cryptography, CORS, browser credentials, fail-safe security checks, uploads, sensitive logging, production containers · Scope: common, backend, frontend · Loading: path (application code, configuration, manifests, container files)

# Security Rules

## Secrets

Never hardcode real secrets, credentials, private keys, access tokens, or
production connection strings in source-controlled files.

For local development, use an appropriate local secret mechanism such as
`dotnet user-secrets`.

For deployed environments, use environment-specific secret injection or a
managed secret store appropriate to the hosting platform.

Do not assume a specific cloud provider unless the project has chosen one.

Never commit real secrets to example configuration files.

## Input Boundaries

Treat data from outside the trusted application boundary as untrusted.

Validate inputs where appropriate, including:

- HTTP requests;
- uploaded files;
- external-service responses when assumptions matter;
- message/event payloads;
- user-provided identifiers and filters.

Validate at the owning layer according to `error-handling.md` → Validation
Boundaries.

## SQL and Persistence

Use parameterized database access. For raw SQL, Dapper, or ADO.NET, use the
supported parameterization mechanisms. Never construct SQL by concatenating
untrusted input.

## Authentication and Authorization

Default to explicit, reviewable authorization behavior.

A project may secure endpoints using:

- global/fallback authorization policies;
- controller/action authorization attributes;
- endpoint authorization configuration.

Do not require redundant `[Authorize]` attributes when a secure global policy
already defines the intended behavior.

Anonymous access must be deliberate and visible.

Authorization must be enforced on the server. Frontend route guards, hidden or
disabled buttons, and other client-side checks are UX, not a security boundary.

Do not implement custom token or password security, password hashing, or
reset-token cryptography when established ASP.NET Core authentication / ASP.NET
Core Identity facilities cover the requirement.

For Bearer/OIDC authentication, validate the properties required by the actual
issuer/provider — issuer, audience where applicable, signature/signing authority,
and lifetime. Do not disable validation merely to make a token work.

Do not expose authentication-failure detail that unnecessarily reveals secrets or
account state; login behavior avoids account-enumeration leaks where relevant.

## Browser Credentials and Tokens

When browser cookies automatically carry authentication credentials, include CSRF
protection in the design; do not assume the frontend framework removes the risk.
Bearer tokens attached explicitly through the `Authorization` header have
different CSRF characteristics.

Do not claim that one browser token-storage mechanism is universally secure;
choose token storage according to the application's threat model, and never log
tokens.

## HTTPS and Transport Security

Production traffic carrying credentials or sensitive data must use TLS.

Respect the actual hosting topology. TLS may terminate in the application, a
reverse proxy, ingress controller, gateway, or hosting platform.

Do not disable certificate validation to make an integration work.

Do not require HTTP-to-HTTPS redirection when the deployment architecture
already provides an appropriate secure transport boundary and redirection is not
desired.

## Data Protection and Encryption

Do not implement custom cryptography when a well-reviewed platform mechanism is
appropriate.

ASP.NET Core Data Protection is suitable for application-generated protected
payloads such as cookies or temporary protected values.

Do not treat ASP.NET Core Data Protection as a universal database encryption
solution.

Use storage/database/platform encryption mechanisms according to the actual data
protection requirement.

## Fail-Safe Security Checks

Default: security-sensitive authorization, permission, or required-control checks
fail safely; do not silently convert a lookup or configuration failure into
success.

When a required security control cannot be configured correctly, fail visibly at
startup/configuration instead of falling back insecurely (for example
authentication silently disabled, plaintext mode, allow-all authorization).

## File Uploads

Do not trust client-provided file metadata, such as the MIME type, as
authoritative when upload handling or security decisions depend on the actual
content.

## CORS

Default: configure CORS to the narrowest policy that satisfies the actual
browser-client requirements.

Do not combine credentialed cross-origin requests with an unrestricted origin
policy.

A public unauthenticated API may legitimately have different CORS requirements
from a private browser application.

## Logging and Sensitive Data

Never log:

- passwords;
- access or refresh tokens;
- private keys;
- authentication secrets;
- full payment credentials.

Avoid logging PII unless there is a concrete operational requirement and the
project's privacy/security policy permits it.

Changing the log level does not make sensitive data safe.

Prefer stable technical identifiers over personal data in operational logs.

Do not serialize arbitrary request bodies, domain objects, or sensitive payloads
into logs by default; log the minimum operationally useful, non-sensitive context.

## Error Responses

Public error-response content is governed by `error-handling.md` → HTTP Errors.

## Containers

Default: production containers use an appropriate runtime image (for example the
ASP.NET Core runtime image) rather than the SDK image solely for convenience, run
as a non-root user where supported, and do not switch to root merely to bypass a
filesystem permission problem. Never bake real secrets into images, Dockerfiles,
committed Compose files, or build arguments.

## Dependencies

Dependency selection, versioning, licensing, and vulnerability checks are owned
by `.claude/rules/dependencies.md` and the `add-dependency` workflow.

Security-sensitive dependency changes must not bypass that policy.
