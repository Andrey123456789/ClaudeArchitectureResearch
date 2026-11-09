> Kind: WF | Scope: common | Owner: security-scan layer investigation prompts (private to security-scan) | Loading: read by security-scan only

# Security Scan — Layer Reference

Investigation prompts for `security-scan`, not automatic vulnerability declarations. The rules each layer checks against are named in the layer heading notes.

# Layer 1: Dependencies and supply chain (A03)

## .NET

```bash
dotnet package list --vulnerable --include-transitive
```

Review vulnerable direct and transitive dependencies, advisory severity, whether the vulnerable component is actually used, whether a patched compatible version exists, and unexpected or untrusted NuGet sources. Do not upgrade packages during a scan unless asked; rate the application finding from reachability and exposure, not CVSS alone.

## Angular / npm

```bash
npm audit
```

Distinguish production from development/build dependencies and direct from transitive packages. A development-only vulnerability still matters to the supply chain, but its runtime impact differs from a browser-shipped dependency. Review lockfiles when package integrity or unexpected dependency changes are relevant.

# Layer 2: Secrets and configuration (A02, A04)

Rules: `rules/common/security.md` § Secrets.

Search source-controlled `.cs`, `.ts`, `.json`, `.yml`, `.yaml`, `.xml`, `.config`, `.env*`, Dockerfiles, Compose files, CI workflows and scripts.

High-confidence indicators: private keys, real access/refresh tokens, cloud access keys, database passwords, API secrets, service-account credentials, production connection strings containing credentials.

Indicators that need context: `ApiKey = "..."`, `Secret = "..."`, `Token = "..."`, `Password = "..."`, long opaque strings, connection strings, certificate material.

`appsettings.Development.json` is not exempt — a real committed secret remains a secret regardless of the filename. Obviously fake values (`changeme`, `example-only`, `test-password`, `not-a-real-key`) may be ignored or reported as Info when context makes them clearly non-sensitive. `UserSecretsId` itself is not a secret.

Preferred pattern — structure in configuration, secret supplied by the chosen local or deployment mechanism:

```csharp
var connectionString =
    builder.Configuration.GetConnectionString("Default");
```

Also review production debug/development flags, certificate-validation bypass, insecure URLs carrying credentials, overly verbose production error configuration and accidentally committed `.env` files.

# Layer 3: Injection and dangerous code patterns (A04, A05, A08)

## SQL injection

Rules: `rules/backend/security.md` § SQL and persistence.

```csharp
var sql =
    $"SELECT * FROM Orders WHERE Name = '{search}'";
```

Look for SQL built from untrusted input, or interpolated/concatenated data passed to APIs that do not parameterize it. Safe forms: EF Core LINQ, parameterized SQL, `FromSqlInterpolated` where appropriate, ADO.NET/Dapper parameters. Normal EF Core LINQ is not SQL injection merely because user input participates in a predicate.

## Command injection

Inspect `Process.Start`, shell execution, PowerShell/bash invocation and command arguments built from user input. Prefer APIs that separate the executable from its arguments; validate or constrain external input when command execution is genuinely needed.

## Path traversal

Review user-controlled file names, paths, archive extraction, download paths and upload destinations for `../`, absolute-path injection, escaping the intended root and unsafe archive extraction. Normalize and verify that paths remain inside the intended storage boundary.

## SSRF

Inspect outbound requests where users influence scheme, host, port, full URL or redirect destination — especially when the server can reach internal networks, metadata endpoints or privileged services. A user-supplied query parameter alone is not SSRF; host/control-plane influence matters.

## XSS and unsafe HTML

For Angular, investigate deliberate sanitizer bypasses — `bypassSecurityTrustHtml`, `bypassSecurityTrustScript`, `bypassSecurityTrustResourceUrl` — and direct DOM manipulation with untrusted content. Ordinary Angular binding benefits from framework escaping and is not automatically XSS. Review deliberate raw HTML handling in any server-rendered UI as well.

## Unsafe deserialization

Investigate polymorphic or type-driven deserialization such as `BinaryFormatter` or unsafe Newtonsoft `TypeNameHandling` settings. Untrusted payloads are not deserialized into arbitrary runtime types.

## Cryptography

Rules: `rules/backend/security.md` § Cryptography and data protection.

Flag security-sensitive use of MD5, SHA1, ECB mode, hardcoded encryption keys, custom password hashing and home-grown encryption protocols — but not MD5/SHA1 used as non-security checksums. Passwords use established password-hashing facilities (ASP.NET Core Identity password hashers), not reversible encryption.

# Layer 4: Authentication and access control (A01, A07)

Rules: `rules/common/security.md` § Authorization authority, `rules/backend/security.md` § Authentication and authorization.

## Effective authorization

Determine the effective policy: fallback/global authorization policy, controller and action `[Authorize]`, `[AllowAnonymous]`, policy names, role/claim requirements, resource-based authorization. An endpoint without an explicit `[Authorize]` is not automatically vulnerable when a secure fallback protects it; bare `[Authorize]` is not automatically insufficient when simple authentication is the intended requirement.

## Anonymous access

Review `[AllowAnonymous]` and other deliberately public surfaces and confirm the public access is intentional. Not every public endpoint is a vulnerability.

## Resource authorization / IDOR

Look for operations such as `GET /orders/{id}`, `PUT /users/{id}`, `DELETE /documents/{id}` where possessing an identifier could expose another user's or tenant's data. Verify ownership, tenant, permission or resource policy where required. Client-side filtering is not authorization.

## Authentication configuration

For Bearer/OIDC, check that the configured mechanism validates issuer, audience where applicable, signature/signing authority and lifetime. Do not demand manually setting every `TokenValidationParameters` property when the provider's authority/metadata configuration already establishes secure validation, and do not impose an arbitrary universal `ClockSkew`. Flag intentionally disabled validation that weakens the actual authentication contract.

## Passwords and accounts

When the application owns local accounts, review password hashing, password reset behavior, lockout/brute-force controls where appropriate, account-enumeration behavior and credential storage.

## Angular

Route guards and hidden or disabled buttons are UX; verify that sensitive operations are protected by the backend.

# Layer 5: Browser and HTTP/API security (A01, A02)

## CORS

Rules: `rules/backend/security.md` § CORS. CORS is a browser-origin policy, not authorization. Look for unnecessarily broad trusted origins, credentialed requests from untrusted origins and environment-specific origins exposed in Production. `AllowAnyOrigin()` can be valid for a genuinely public, non-credentialed API; consider intended exposure before reporting a wildcard.

## CSRF

Rules: `rules/frontend/angular.md` § Browser authentication security. When browser credentials (especially cookies) are sent automatically, review CSRF protection for state-changing operations. Bearer tokens attached explicitly through the `Authorization` header have different CSRF characteristics.

## TLS

Rules: `rules/common/security.md` § Transport security. Review disabled certificate validation, accept-all certificate callbacks and plain HTTP for sensitive external communication, accounting for TLS termination at proxies, ingress, gateways or the hosting platform. Missing in-app HTTPS redirection is not automatically a vulnerability.

## File uploads

Rules: `rules/backend/security.md` § Uploads. Inspect size limits, storage path safety, file-name handling, content/type assumptions, execution or public-serving risks and authorization.

## Rate limiting

Consider rate limiting where abuse realistically matters — login and password reset, expensive anonymous endpoints, resource-intensive operations — not on every endpoint. `429` semantics: `http-api`.

# Layer 6: Sensitive data, logging and error exposure (A04, A09)

## Logging

Rules: `rules/common/security.md` § Logging and sensitive data. Review logs for credentials, tokens, keys and payment data, PII against project requirements, Debug/Trace treated as a safe level, and duplicate or missing security-relevant logging in context — not logs for every successful request.

## Error responses

Rules: `rules/backend/error-handling.md`. Review public errors for stack traces, SQL, connection strings, internal filesystem paths, secret values and internal exception details.

## Response data

Look for database/domain entities returned directly, password hashes, internal security fields, unnecessary personal information and secret metadata. Returning a Domain entity is not automatically vulnerable — inspect the serialized fields — but explicit response contracts are preferable where needed.

## Data at rest

Match protection to the requirement: passwords → one-way password hashing; verification-only tokens → often hashed rather than reversibly encrypted; retrievable application secrets → protected/encrypted storage; database/storage encryption → platform or database mechanism when suitable; temporary application payloads → ASP.NET Core Data Protection may fit.

# Layer 7: Exceptional conditions and failure handling (A06, A10)

Rules: `rules/common/security.md` § Failure behavior, `rules/backend/integrations.md`.

## Fail-open behavior

Investigate code that catches an exception and then lets a privileged operation continue:

```text
authorization service failed -> allow
token validation failed -> continue as anonymous but perform privileged action
permission lookup failed -> default to permitted
```

## Swallowed exceptions

```csharp
catch (Exception)
{
}
```

Review broad catch blocks that continue without a deliberate fallback. Not every swallowed exception is a vulnerability, but a security-relevant failure silently turning into success is.

## Retry and idempotency

Review retries of state-changing operations — a lost response followed by a retry can duplicate effects — and retries triggered by caller cancellation. Technique: `httpclient-factory`.

## Timeouts and resource exhaustion

Review external operations and public inputs that can consume unbounded time, memory, database rows, file size, request body, retry attempts or parallel work. A theoretical missing limit is not automatically High; evaluate whether an attacker can actually exploit it.

## Startup and configuration failure

Look for dangerous fallbacks such as invalid auth configuration silently disabling authentication, a missing encryption key switching to plaintext, or a failed authorization provider falling back to allow-all.

## Unexpected error exposure

Confirm unexpected exceptions follow the centralized error-handling path and reveal nothing sensitive.

# Cross-cutting design review

Static checks do not fully cover A06 Insecure Design, tenant isolation, business-workflow abuse, privilege escalation through legitimate operations, financial/idempotency abuse or multi-step authorization problems. When meaningful security-sensitive workflows exist, name them as candidates for threat modeling or dedicated manual review rather than claiming the static scan proves them secure.

# Severity examples

```text
real production private key committed publicly
-> potentially Critical

raw SQL string containing only developer-controlled constant text
-> not SQL injection

missing [Authorize] while a secure fallback policy exists
-> not a finding

PII logged in a restricted internal diagnostic environment
-> contextual finding, not automatically High
```

Do not map pattern → fixed severity, CVSS → application severity or OWASP category → severity mechanically.

# Finding format

```markdown
### [HIGH] src/.../File.cs:42 — Resource authorization missing

OWASP: A01:2025 Broken Access Control

Evidence:
The endpoint loads an order solely by route ID and does not constrain it to the
authenticated customer.

Impact:
An authenticated user who learns another order ID may access that customer's
order.

Remediation:
Apply resource/ownership authorization before returning the order.
```

When evidence is incomplete:

```markdown
### [NEEDS VERIFICATION] ...

The static code suggests ..., but effective behavior depends on ...
```
