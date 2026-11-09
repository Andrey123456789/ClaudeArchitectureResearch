> Level: 3 Project · Owns: per-layer investigation prompts for `security-scan` (private reference) · Scope: common · Loads: read by `security-scan` only · Depends on: .claude/skills/security-scan/SKILL.md

# Security Scan — Layer Reference

Investigation prompts, not automatic vulnerability declarations. The invariants being checked are owned by `.claude/rules/0-core/security-principles.md` and `logging-principles.md`.

## Layer 1: Dependencies and supply chain (A03)

- .NET: `dotnet package list --vulnerable --include-transitive`. Review vulnerable direct and transitive packages, advisory severity, whether the component is actually used, whether a patched compatible version exists, and unexpected or untrusted NuGet sources. Do not upgrade packages during a scan unless asked.
- npm: `npm audit`. Distinguish production from development/build dependencies and direct from transitive packages; a dev-only vulnerability still matters to the supply chain but has different runtime impact than a browser-shipped package. Review lockfiles when integrity or unexpected dependency changes matter.

## Layer 2: Secrets and configuration (A02, A04)

Search source-controlled `.cs`, `.ts`, `.json`, `.yml`/`.yaml`, `.xml`, `.config`, `.env*`, Dockerfiles, Compose files, CI workflows, and scripts.

- High-confidence indicators: private keys, real access/refresh tokens, cloud access keys, database passwords, API secrets, service-account credentials, production connection strings with credentials.
- Indicators that need context: `ApiKey = "..."`, `Secret = "..."`, `Token = "..."`, `Password = "..."`, long opaque strings, connection strings, certificate material.
- A real committed secret is a secret regardless of the file name; `appsettings.Development.json` is not exempt. Obviously fake values (`changeme`, `example-only`, `test-password`, `not-a-real-key`) may be ignored or reported as Info. `UserSecretsId` is not a secret.
- Preferred pattern: `builder.Configuration.GetConnectionString("Default")` with the real value from the chosen local or deployment secret mechanism.
- Also review production debug/development flags, certificate-validation bypass, insecure URLs carrying credentials, verbose production error configuration, and committed `.env` files.

## Layer 3: Injection and dangerous patterns (A04, A05, A08)

- **SQL injection:** SQL built from untrusted input, e.g. `$"SELECT * FROM Orders WHERE Name = '{search}'"`, or interpolated data passed to APIs that do not parameterize. Safe forms: EF Core LINQ, parameterized SQL, `FromSqlInterpolated` where appropriate, ADO.NET/Dapper parameters. Normal EF Core LINQ with user input in a predicate is not SQL injection.
- **Command injection:** `Process.Start`, shell/PowerShell/bash invocation, arguments built from user input. Prefer APIs that separate executable and arguments; constrain input when execution is genuinely needed.
- **Path traversal:** user-controlled file names, paths, archive extraction, download and upload destinations; look for `../`, absolute-path injection, escaping the intended root, unsafe extraction. Normalize and verify paths stay within the storage boundary.
- **SSRF:** outbound requests where users influence scheme, host, port, full URL, or redirect destination — especially when the server reaches internal networks, metadata endpoints, or privileged services. A user-supplied query parameter alone is not SSRF; host/control-plane influence matters.
- **XSS / unsafe HTML:** Angular sanitizer bypasses (`bypassSecurityTrustHtml`, `bypassSecurityTrustScript`, `bypassSecurityTrustResourceUrl`) and direct DOM manipulation with untrusted content. Ordinary Angular binding is escaped/sanitized and is not automatically XSS.
- **Unsafe deserialization:** polymorphic/type-driven mechanisms such as `BinaryFormatter` or unsafe Newtonsoft `TypeNameHandling`; never deserialize untrusted payloads into arbitrary runtime types.
- **Cryptography:** security-sensitive MD5, SHA1, ECB mode, hardcoded keys, custom password hashing, home-grown protocols. MD5/SHA1 as a non-security checksum is fine. Passwords use established hashing (ASP.NET Core Identity password hasher), never reversible encryption.

## Layer 4: Authentication and access control (A01, A07)

- **Effective authorization:** fallback/global policy, controller/action `[Authorize]`, `[AllowAnonymous]`, policy names, role/claim requirements, resource-based authorization. Identify the actual behavior before reporting.
- **Anonymous access:** confirm each deliberately public surface is intentional; a public endpoint is not automatically a vulnerability.
- **Resource authorization / IDOR:** operations such as `GET /orders/{id}`, `PUT /users/{id}`, `DELETE /documents/{id}` where possessing an identifier could expose another user's or tenant's data. Verify ownership, tenant, permission, or resource policy; client-side filtering is not authorization.
- **Authentication configuration:** for Bearer/OIDC check issuer, audience where applicable, signature/signing authority, lifetime. Do not require setting every `TokenValidationParameters` property when authority/metadata configuration already establishes secure validation, and do not impose an arbitrary universal `ClockSkew`. Flag intentionally disabled validation without a valid reason.
- **Passwords and accounts:** hashing, reset behavior, lockout/brute-force controls where appropriate, account enumeration, credential storage.
- **Angular:** route guards and hidden/disabled buttons are UX; verify the backend protects sensitive operations.

## Layer 5: Browser and HTTP/API security (A01, A02)

- **CORS:** origins versus the actual browser-client model; problems include unnecessarily broad origins, credentialed requests from untrusted origins, and environment-specific origins exposed in Production. `AllowAnyOrigin()` can be valid for a public non-credentialed API; CORS is not authorization.
- **CSRF:** when browser credentials (especially cookies) are sent automatically, review CSRF protection for state-changing operations; explicitly attached Bearer headers have different characteristics.
- **TLS:** disabled certificate validation, accept-all callbacks, plain HTTP for sensitive external communication. Account for termination at proxies, ingress, gateways, or platforms; missing HTTPS redirection in code is not automatically a vulnerability.
- **File uploads:** size limits, storage path safety, file-name handling, content/type assumptions (client MIME type treated as authoritative?), execution or public-serving risk, authorization.
- **Rate limiting:** consider it where abuse realistically matters (login/password reset, expensive anonymous endpoints, resource-intensive operations); not on every endpoint. `429` semantics: `http-api` skill.

## Layer 6: Sensitive data, logging, error exposure (A04, A09)

- **Logging:** check for the never-log categories in `logging-principles.md`, PII against project requirements, Debug/Trace treated as a safety boundary, and missing or duplicated security-relevant logging in context (no demand to log every successful request).
- **Error responses:** stack traces, SQL, connection strings, internal paths, secret values, internal exception details in public errors.
- **Response data:** entities returned directly, password hashes, internal security fields, unnecessary personal data, secret metadata. Inspect the serialized fields — returning an entity is not automatically a vulnerability.
- **Data at rest:** password → one-way hashing; verification-only token → often a hash; retrievable application secret → protected/encrypted storage; database/storage encryption → platform mechanism; temporary application payload → ASP.NET Core Data Protection may fit.

## Layer 7: Exceptional conditions (A06, A10)

- **Fail-open:** code that catches an exception and then allows a privileged operation — authorization service failed → allow; token validation failed → anonymous but privileged action; permission lookup failed → permitted.
- **Swallowed exceptions:** empty `catch (Exception) { }` and broad catches without a deliberate fallback; security-relevant failures must not silently become success.
- **Retry and idempotency:** retries of state-changing operations; a lost response plus retry can duplicate effects (`httpclient-factory` skill and its resilience reference); check caller-cancellation handling against `.claude/rules/0-core/runtime-principles.md`.
- **Timeouts and resource exhaustion:** unbounded time, memory, rows, file size, request body, retries, or parallel work; judge whether an attacker can actually exploit it.
- **Startup/configuration failure:** invalid auth configuration → authentication silently disabled; missing encryption key → plaintext mode; failed authorization provider → allow-all.
- **Unexpected error exposure:** unexpected exceptions follow centralized handling and reveal nothing sensitive.

## Cross-cutting design review

Static checks do not cover insecure design, tenant isolation, business-workflow abuse, privilege escalation through legitimate operations, financial/idempotency abuse, or multi-step authorization. Name such workflows as candidates for threat modeling or dedicated manual review instead of claiming the scan proves them secure.

## Severity examples

Do not map pattern → severity, CVSS → severity, or OWASP category → severity mechanically:

- real production private key committed publicly → potentially Critical;
- raw SQL containing only developer-controlled constant text → not SQL injection;
- missing `[Authorize]` under a secure fallback policy → not a finding;
- PII logged in a restricted internal diagnostic environment → contextual, not automatically High.

## Finding format

```markdown
### [HIGH] src/.../File.cs:42 — Resource authorization missing

OWASP: A01:2025 Broken Access Control

Evidence:
The endpoint loads an order solely by route ID and does not constrain it to the
authenticated customer.

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

Never invent exploitability that the code does not establish.
