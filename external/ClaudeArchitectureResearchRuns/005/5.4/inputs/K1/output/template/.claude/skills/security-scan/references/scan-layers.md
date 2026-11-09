> Kind: WF | Scope: common | Capability: — | Loading: read by `security-scan` during a scan

# Security Scan — Layer Reference

Investigation prompts for the `security-scan` workflow, not automatic vulnerability declarations.

# Layer 1: Dependencies and Supply Chain (A03)

## .NET

When supported by the installed SDK:

```bash
dotnet package list --vulnerable --include-transitive
```

Review vulnerable direct and transitive dependencies, advisory severity, whether the vulnerable component is actually used, whether a patched compatible version exists, and unexpected or untrusted NuGet sources. Do not upgrade packages during a scan unless asked, and do not rate the finding from CVSS alone — consider reachability and exposure.

## npm

When a frontend workspace exists, run `npm audit`. Distinguish production from development/build dependencies and direct from transitive packages: a development-only vulnerability can still matter to the supply chain, but its runtime impact differs from a browser-shipped dependency. Review lockfiles when package integrity or unexpected dependency changes are relevant.

# Layer 2: Secrets and Configuration (A02, A04)

Search source-controlled files for real credentials: `.cs`, `.ts`, `.json`, `.yml`, `.yaml`, `.xml`, `.config`, `.env*`, Dockerfiles, Compose files, CI workflow files, scripts.

High-confidence indicators: private keys, real access/refresh tokens, cloud access keys, database passwords, API secrets, service-account credentials, production connection strings containing credentials.

Indicators requiring context: `ApiKey = "..."`, `Secret = "..."`, `Token = "..."`, `Password = "..."`, long opaque strings, connection strings, certificate material.

Do not automatically ignore `appsettings.Development.json`; a real committed secret remains a secret regardless of file name. Obviously fake values (`changeme`, `example-only`, `test-password`, `not-a-real-key`) may be ignored or reported as Info when context makes them clearly non-sensitive. `UserSecretsId` itself is not a secret.

Preferred pattern — configuration structure in files, the real secret from the chosen local/deployment secret mechanism:

```csharp
var connectionString = builder.Configuration.GetConnectionString("Default");
```

Also review production debug/development flags, certificate-validation bypasses, insecure URLs carrying credentials, overly verbose production error configuration, and accidentally committed `.env` files.

# Layer 3: Injection and Dangerous Code Patterns (A04, A05, A08)

## SQL injection

Look for SQL constructed from untrusted input, e.g.

```csharp
var sql = $"SELECT * FROM Orders WHERE Name = '{search}'";
```

or interpolated/concatenated data passed to APIs that do not parameterize it. Safe forms: ORM LINQ queries, parameterized SQL, the persistence technology's interpolation-parameterizing APIs (persistence knowledge facet), ADO.NET/Dapper parameters. Do not report ordinary ORM LINQ as SQL injection merely because user input participates in a predicate.

## Command injection

Inspect `Process.Start`, shell execution, PowerShell/bash invocation, and command arguments built from user input. Prefer APIs that separate executable and arguments; validate or constrain input when command execution is genuinely needed.

## Path traversal

Review user-controlled file names, paths, archive extraction, download paths, and upload destinations for `../`, absolute-path injection, escapes from the intended root, and unsafe archive extraction. Normalize and verify that paths remain within the intended storage boundary.

## SSRF

Inspect outbound requests where users influence scheme, host, port, full URL, or redirect destination, especially when the server can reach internal networks, metadata endpoints, or privileged services. Host/control-plane influence matters; not every user-supplied query parameter in an outbound request is SSRF.

## XSS and unsafe HTML

In the frontend, investigate deliberate sanitizer bypasses and direct DOM manipulation with untrusted content (the frontend knowledge facet names the framework's bypass APIs). Ordinary template binding benefits from framework escaping/sanitization and is not automatically XSS. Review deliberate raw HTML handling in any server-rendered UI as well.

## Unsafe deserialization

Investigate polymorphic/type-driven deserialization (legacy examples: `BinaryFormatter`, unsafe Newtonsoft `TypeNameHandling`). Untrusted payloads must not deserialize into arbitrary runtime types.

## Cryptography

Flag security-sensitive uses of MD5, SHA1, ECB mode, hardcoded encryption keys, custom password hashing, and home-grown encryption protocols — but not MD5/SHA1 used as a non-security checksum where collision resistance is irrelevant. Passwords use established password-hashing facilities such as ASP.NET Core Identity password hashers, not reversible encryption. Never recommend custom cryptography.

# Layer 4: Authentication and Access Control (A01, A07)

## Effective authorization

Determine the effective policy from fallback/global policies, controller and action `[Authorize]`, `[AllowAnonymous]`, policy names, role/claim requirements, and resource-based authorization. An endpoint without explicit `[Authorize]` is not automatically vulnerable under a secure fallback policy, and bare `[Authorize]` is not automatically insufficient when simple authentication is intended.

## Anonymous access

Review `[AllowAnonymous]` and other deliberately public surfaces and confirm public access is intentional; do not report every public endpoint as a vulnerability.

## Resource authorization / IDOR

Look for operations such as `GET /orders/{id}`, `PUT /users/{id}`, `DELETE /documents/{id}` where possessing an identifier could expose another user's or tenant's data; verify ownership, tenant, permission, or resource policy where required. Client-side filtering is not authorization.

## Authentication configuration

For Bearer/OIDC, inspect whether issuer, audience where applicable, signature/signing authority, and lifetime are validated. Do not require manually setting every `TokenValidationParameters` property when the provider's authority/metadata configuration already establishes secure validation, and do not impose an arbitrary universal `ClockSkew` value. Flag intentionally disabled validation that weakens the authentication contract without a valid reason.

## Passwords and accounts

When the application owns local accounts, review password hashing, reset behavior, lockout/brute-force controls where appropriate, account-enumeration behavior, and credential storage. Never recommend custom password hashing.

## Frontend

Route guards and hidden/disabled buttons are UX mechanisms; verify that sensitive operations are protected by the backend.

# Layer 5: Browser and HTTP/API Security (A01, A02)

## CORS

CORS is a browser-origin policy, not an authorization mechanism. Review whether configured origins match the actual browser-client model; potential problems are unnecessarily broad trusted origins, credentialed requests from untrusted origins, and environment-specific origins exposed in Production. `AllowAnyOrigin()` can be valid for a genuinely public non-credentialed API; do not report a wildcard origin without considering intended exposure. Credentialed cross-origin access requires restricted origins.

## CSRF

When browser credentials are sent automatically, especially cookies, review CSRF protection for state-changing operations. Bearer tokens attached explicitly through the `Authorization` header have different CSRF characteristics; do not assume the frontend framework provides server-side CSRF protection for every authentication model.

## TLS

Review disabled certificate validation, accept-all certificate callbacks, and plain HTTP for sensitive external communication. Account for TLS termination at proxies, ingress, gateways, or hosting platforms; missing HTTPS redirection in application code is not automatically a vulnerability when the topology enforces TLS.

## File uploads

Inspect size limits, storage path safety, file-name handling, content/type assumptions, execution/public-serving risks, and authorization. Client-provided MIME types are not authoritative.

## Rate limiting

Consider rate limiting where abuse realistically matters (login/password reset, expensive anonymous endpoints, resource-intensive operations); do not require it on every endpoint. `http-api` covers 429 semantics.

# Layer 6: Sensitive Data, Logging, and Error Exposure (A04, A09)

## Logging

Check for passwords, access/refresh tokens, private keys, authentication secrets, and full payment credentials in logs; review PII against project requirements; prefer technical identifiers over identity data. Debug/Trace level is not a security boundary. Review duplicate or missing security-relevant logging in context; do not demand logs for every successful request.

## Error responses

Review public errors for stack traces, SQL, connection strings, internal filesystem paths, secret values, and internal exception details; the centralized error-handling policy applies.

## Response data

Look for database/domain entities returned directly, password hashes, internal security fields, unnecessary personal information, and secret metadata. Prefer explicit response contracts where needed, but inspect the actual serialized fields before calling a returned entity a vulnerability.

## Data at rest

Choose protection from the requirement: password → one-way password hashing; verification-only token → often a hash rather than reversible encryption; retrievable application secret → protected/encrypted storage; database/storage encryption → platform or database mechanism when suitable; temporary application payload → ASP.NET Core Data Protection may fit. Data Protection is not a universal database-encryption solution, and custom cryptography is never the answer.

# Layer 7: Exceptional Conditions and Failure Handling (A06, A10)

## Fail-open behavior

Investigate code that catches an exception and then lets a privileged operation continue: authorization service failed → allow; token validation failed → continue as anonymous but perform a privileged action; permission lookup failed → default to permitted. Security-sensitive checks fail safely.

## Swallowed exceptions

Review empty `catch (Exception) { }` blocks and broad catches that continue without a deliberate fallback. Not every swallowed exception is a vulnerability, but security-relevant failures must not silently turn into success.

## Retry and idempotency

Review retries of state-changing operations: a lost response followed by a retry can duplicate effects; check that caller cancellation is never retried (`.claude/rules/backend/runtime.md`). Technique: `httpclient-factory` (including its resilience reference).

## Timeouts and resource exhaustion

Review external operations or public inputs that can consume unbounded time, memory, database rows, file size, request body, retry attempts, or parallel work. A theoretical missing limit is not automatically High; evaluate whether an attacker can exploit it.

## Startup and configuration failure

Review security-sensitive startup configuration for dangerous fallback: invalid auth configuration → authentication silently disabled; missing encryption key → plaintext mode; failed authorization provider → allow-all. Prefer visible failure over insecure fallback.

## Unexpected error exposure

Confirm unexpected exceptions follow the centralized error-handling policy and reveal no sensitive information.

# Cross-cutting design review

Static pattern checks do not cover insecure design, tenant isolation, business workflow abuse, privilege escalation through legitimate operations, financial/idempotency abuse, or multi-step authorization problems. When meaningful security-sensitive workflows exist, flag them for threat modeling or dedicated manual review instead of claiming the scan proves them secure.

# Severity guidance

Never map mechanically pattern → severity, CVSS → application severity, or OWASP category → severity. Examples: a real production private key committed publicly → potentially Critical; raw SQL with only developer-controlled constant text → not SQL injection; missing `[Authorize]` under a secure fallback policy → not a finding; PII logged in a restricted internal diagnostic environment → contextual finding, not automatically High.

# Finding format

```markdown
### [HIGH] src/.../File.cs:42 — Resource authorization missing

OWASP: A01:2025 Broken Access Control

Evidence:
The endpoint loads an order solely by route ID and does not constrain it to the authenticated customer.

Impact:
An authenticated user who learns another order ID may access that customer's order.

Remediation:
Apply resource/ownership authorization before returning the order.
```

When evidence is incomplete:

```markdown
### [NEEDS VERIFICATION] ...

The static code suggests ..., but effective behavior depends on ...
```

Never invent exploitability the code does not establish.
