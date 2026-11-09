<!-- Kind: WF | Scope: common | Owns: security-scan layer investigation prompts (private to security-scan) | Loads: read by security-scan -->
# Security Scan — Layer Reference

Investigation prompts for the `security-scan` workflow. They locate candidates; they are not automatic vulnerability declarations. The invariants behind them live in the standards named in `SKILL.md`.

# Layer 1: Dependencies and Supply Chain

OWASP: A03:2025 Software Supply Chain Failures

## .NET

When supported by the installed SDK:

```bash
dotnet package list --vulnerable --include-transitive
```

Review vulnerable direct and transitive dependencies, severity/advisory information, whether the vulnerable component is actually used by the application, whether a patched compatible version exists, and unexpected or untrusted NuGet sources. Rate the application finding from reachability and exposure, not from CVSS alone.

## Angular / npm

When an npm frontend exists:

```bash
npm audit
```

Distinguish production vs development/build dependencies and direct vs transitive packages. A development-only vulnerability still matters to the supply chain, but its runtime impact differs from a browser-shipped dependency. Review lockfiles when package integrity or unexpected dependency changes are relevant.

# Layer 2: Secrets and Configuration

OWASP: A02:2025 Security Misconfiguration, A04:2025 Cryptographic Failures

Search source-controlled `.cs`, `.ts`, `.json`, `.yml`, `.yaml`, `.xml`, `.config`, `.env*`, Dockerfiles, Compose files, CI workflow files and scripts.

High-confidence indicators: private keys, real access/refresh tokens, cloud access keys, database passwords, API secrets, service-account credentials, production connection strings containing credentials.

Indicators requiring context: `ApiKey = "..."`, `Secret = "..."`, `Token = "..."`, `Password = "..."`, long opaque strings, connection strings, certificate material.

Do not skip `appsettings.Development.json` — a committed real secret is a secret regardless of the file name. Obviously fake values (`changeme`, `example-only`, `test-password`, `not-a-real-key`) may be ignored or reported as Info when context makes them clearly non-sensitive. `UserSecretsId` itself is not a secret. The expected pattern reads configuration (for example `builder.Configuration.GetConnectionString("Default")`) with the real value supplied by the chosen secret mechanism.

Also review production debug/development flags, certificate-validation bypasses, URLs carrying credentials, overly verbose production error configuration and accidentally committed `.env` files.

# Layer 3: Injection and Dangerous Code Patterns

OWASP: A04 Cryptographic Failures, A05 Injection, A08 Software or Data Integrity Failures

## SQL Injection

Look for SQL constructed from untrusted input, such as

```csharp
var sql =
    $"SELECT * FROM Orders WHERE Name = '{search}'";
```

or interpolated/concatenated data passed to APIs that do not parameterize it. Expected forms: EF Core LINQ, parameterized SQL, `FromSqlInterpolated` where appropriate, ADO.NET/Dapper parameters. Normal EF Core LINQ is not SQL injection merely because user input participates in a predicate.

## Command Injection

Inspect `Process.Start`, shell execution, PowerShell/bash invocation and command arguments built from user input. Expected: APIs that separate executable and arguments, with external input validated or constrained.

## Path Traversal

Review user-controlled file names, paths, archive extraction, download paths and upload destinations for `../`, absolute-path injection, escape from the intended root and unsafe archive extraction. Expected: normalized paths verified to stay within the storage boundary.

## SSRF

Inspect outbound requests where users influence scheme, host, port, full URL or redirect destination — especially when the server can reach internal networks, metadata endpoints or privileged services. A user-supplied query parameter inside an outbound request is not SSRF by itself; host/control-plane influence matters.

## XSS / Unsafe HTML

For Angular, investigate deliberate sanitizer bypasses (`bypassSecurityTrustHtml`, `bypassSecurityTrustScript`, `bypassSecurityTrustResourceUrl`) and direct DOM manipulation with untrusted content. Ordinary Angular binding benefits from framework escaping/sanitization. Review deliberate raw HTML handling in any server-rendered UI as well.

## Unsafe Deserialization

Investigate polymorphic/type-driven deserialization of untrusted payloads into arbitrary runtime types (legacy examples: `BinaryFormatter`, unsafe Newtonsoft `TypeNameHandling`).

## Cryptography

Flag security-sensitive uses of MD5, SHA1, ECB mode, hardcoded encryption keys, custom password hashing and home-grown encryption protocols (`rules/backend/security.md` § Cryptography and Data Protection). MD5/SHA1 used only as a non-security checksum, where collision resistance is irrelevant, is not a finding. For passwords, the expected mechanism is an established password hasher such as ASP.NET Core Identity's, not reversible encryption.

# Layer 4: Authentication and Access Control

OWASP: A01:2025 Broken Access Control, A07:2025 Authentication Failures

## Effective Authorization

Determine the effective access policy from the fallback/global authorization policy, controller and action `[Authorize]`, `[AllowAnonymous]`, policy names, role/claim requirements and resource-based authorization. An endpoint without explicit `[Authorize]` is not automatically vulnerable under a secure fallback/global policy; bare `[Authorize]` is not automatically insufficient when simple authentication is the intended requirement.

## Anonymous Access

Review `[AllowAnonymous]` and other deliberately public surfaces and confirm the public access is intentional. Not every public endpoint is a vulnerability.

## Resource Authorization / IDOR

Look for operations such as `GET /orders/{id}`, `PUT /users/{id}`, `DELETE /documents/{id}` where possessing an identifier could expose another user's or tenant's data. Verify ownership, tenant, permission or resource policy where required. Client-side filtering is not authorization.

## Authentication Configuration

For Bearer/OIDC, check that the configured mechanism validates issuer, audience where applicable, signature/signing authority and lifetime (`rules/backend/security.md`). Do not require manually setting every `TokenValidationParameters` property when the framework/provider already establishes secure validation through authority metadata, and do not impose an arbitrary universal `ClockSkew` as a vulnerability rule. Flag intentionally disabled validation that weakens the actual authentication contract.

## Passwords and Accounts

When the application owns local accounts, review password hashing, password reset behavior, lockout/brute-force controls where appropriate, account-enumeration behavior and credential storage.

## Angular

Route guards and hidden or disabled buttons are UX mechanisms; verify that sensitive operations are protected by the backend.

# Layer 5: Browser and HTTP/API Security

OWASP: A01 Broken Access Control, A02 Security Misconfiguration

## CORS

CORS is a browser-origin policy, not authorization. Check whether configured origins match the actual browser-client model; look for unnecessarily broad trusted origins, credentialed requests from untrusted origins, and environment-specific origins exposed in Production. `AllowAnyOrigin()` can be valid for a genuinely public non-credentialed API; credentialed cross-origin access needs restricted origins.

## CSRF

When browsers send credentials automatically (especially cookies), review CSRF protection of state-changing operations (`rules/frontend/security.md`). Bearer tokens explicitly attached in the `Authorization` header have different CSRF characteristics.

## TLS

Look for disabled certificate validation, accept-all certificate callbacks and plain HTTP for sensitive external communication. Account for TLS termination at reverse proxies, ingress, gateways or hosting platforms; missing HTTPS redirection in application code is not automatically a vulnerability when the hosting topology enforces TLS.

## File Uploads

Inspect size limits, storage path safety, file-name handling, content/type assumptions (client MIME type treated as authoritative?), execution/public-serving risks and authorization.

## Rate Limiting

Consider rate limiting where abuse realistically matters — login/password reset, expensive anonymous endpoints, resource-intensive operations — not on every endpoint. `429` semantics: `http-api` skill.

# Layer 6: Sensitive Data, Logging and Error Exposure

OWASP: A04 Cryptographic Failures, A09 Security Logging & Alerting Failures

## Logging

Look for passwords, access/refresh tokens, private keys, authentication secrets or full payment credentials in log statements, and review PII against project requirements (`rules/common/security.md` § Logging and Sensitive Data). Debug/Trace level is not a security boundary. Review duplicate or missing security-relevant logging in context; do not demand logs for every successful request.

## Error Responses

Review public errors for stack traces, SQL, connection strings, internal filesystem paths, secret values and internal exception details (`rules/backend/error-handling.md`).

## Response Data

Look for database/domain entities returned directly, password hashes, internal security fields, unnecessary personal information and secret metadata. Returning a Domain entity is not automatically vulnerable — inspect the serialized fields; explicit response contracts are the usual remedy.

## Data at Rest

Match protection to the requirement:

    password                          -> one-way password hashing
    verification-only token           -> often hash rather than reversible encryption
    retrievable application secret    -> appropriate protected/encrypted storage
    database/storage encryption       -> platform/database mechanism when suitable
    temporary application payload     -> ASP.NET Core Data Protection may be suitable

# Layer 7: Exceptional Conditions and Failure Handling

OWASP: A06:2025 Insecure Design, A10:2025 Mishandling of Exceptional Conditions

## Fail-Open Behavior

Investigate code that catches an exception and then lets a privileged operation continue (`rules/common/security.md` § Failure Behavior):

    authorization service failed      -> allow
    token validation failed           -> continue as anonymous but perform privileged action
    permission lookup failed          -> default to permitted

## Swallowed Exceptions

Review empty `catch (Exception) { }` blocks and broad catches that continue without a deliberate fallback. Not every swallowed exception is a vulnerability, but a security-relevant failure silently converted into success is.

## Retry and Idempotency

Review retries of state-changing operations — a lost response followed by a retry can duplicate effects — and caller cancellation treated as a transient failure (`rules/backend/outbound-http.md`).

## Timeouts and Resource Exhaustion

Review external operations or public inputs that can consume unbounded time, memory, database rows, file size, request body, retry attempts or parallel work. A theoretical missing limit is not automatically High; evaluate whether an attacker can actually exploit it.

## Startup and Configuration Failure

Review security-sensitive startup configuration for dangerous fallback:

    invalid auth configuration        -> authentication silently disabled
    missing encryption key            -> plaintext mode
    failed authorization provider     -> allow-all fallback

## Unexpected Error Exposure

Confirm unexpected exceptions go through the centralized error handling and reveal no sensitive information.

# Cross-Cutting Design Review

Static pattern checks do not fully cover A06 Insecure Design, tenant isolation, business-workflow abuse, privilege escalation through legitimate operations, financial/idempotency abuse or multi-step authorization problems. When the application has meaningful security-sensitive workflows, name them as candidates for threat modeling or dedicated manual review rather than claiming the static scan proves them secure.

# Severity Examples

Do not map mechanically from pattern, CVSS or OWASP category to severity.

    real production private key committed publicly          -> potentially Critical
    raw SQL string with only developer-controlled constants -> not SQL injection
    missing [Authorize] while a secure fallback policy exists -> not a finding
    PII logged in a restricted internal diagnostic environment -> contextual, not automatically High

# Finding Examples

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

Do not invent exploitability that the code does not establish.
