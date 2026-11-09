> Level: 3 Project · Owns: per-layer investigation prompts (private reference of `security-scan`) · Scope: common · Loads: read by `security-scan` only

# Security Scan — Layer Reference

Investigation prompts, not automatic vulnerability declarations. The invariants behind them are in `.claude/rules/0-core/security-principles.md` and `logging-principles.md`.

## Layer 1 — Dependencies and supply chain (A03)

.NET:

```bash
dotnet package list --vulnerable --include-transitive
```

Review vulnerable direct and transitive packages, advisory severity, whether the vulnerable component is actually used, whether a patched compatible version exists, and unexpected or untrusted NuGet sources. NuGet audit also runs during restore on modern SDKs.

Angular/npm:

```bash
npm audit
```

Distinguish production from development/build dependencies and direct from transitive packages. A development-only vulnerability still matters to the supply chain, but its runtime impact differs from a browser-shipped dependency. Review lockfile changes when integrity or unexpected dependency changes are relevant.

## Layer 2 — Secrets and configuration (A02, A04)

Search source-controlled `.cs`, `.ts`, `.json`, `.yml`/`.yaml`, `.xml`, `.config`, `.env*`, Dockerfiles, Compose files, CI workflows and scripts.

- High-confidence indicators: private keys, real access/refresh tokens, cloud access keys, database passwords, API secrets, service-account credentials, production connection strings with credentials.
- Context-dependent: `ApiKey = "..."`, `Secret = "..."`, `Token = "..."`, `Password = "..."`, long opaque strings, connection strings, certificate material.
- `appsettings.Development.json` is not exempt — a real committed secret is a secret regardless of the file name. Obviously fake values (`changeme`, `example-only`, `test-password`, `not-a-real-key`) may be ignored or reported as Info. `UserSecretsId` is not a secret.

Preferred shape: read the value through configuration (`builder.Configuration.GetConnectionString("Default")`) and supply it through the chosen local or deployment secret mechanism.

Also review: production debug/development flags, certificate-validation bypass, credentials in URLs, verbose production error configuration, committed `.env` files.

## Layer 3 — Injection and dangerous patterns (A04, A05, A08)

- **SQL injection** — SQL built from untrusted input, e.g. `$"SELECT * FROM Orders WHERE Name = '{search}'"` passed to an API that does not parameterize. Safe shapes: EF Core LINQ, `FromSql`/`FromSqlInterpolated`/`ExecuteSql` with interpolated parameters, ADO.NET or Dapper parameters. Normal EF Core LINQ with user values in predicates is not SQL injection.
- **Command injection** — `Process.Start`, shell or PowerShell invocation with arguments built from user input. Prefer APIs that separate the executable from arguments; constrain input when execution is genuinely needed.
- **Path traversal** — user-controlled file names, paths, archive extraction, download paths, upload destinations (`../`, absolute-path injection, escaping the intended root). Normalize and verify the path stays inside the storage boundary.
- **SSRF** — outbound requests where users influence scheme, host, port, full URL or redirect destination, especially when the server can reach internal networks or metadata endpoints. A user-supplied query parameter alone is not SSRF; host/control-plane influence matters.
- **XSS / unsafe HTML** — Angular sanitizer bypasses (`bypassSecurityTrustHtml`, `bypassSecurityTrustScript`, `bypassSecurityTrustResourceUrl`) and direct DOM manipulation with untrusted content. Ordinary Angular binding is escaped/sanitized by the framework.
- **Unsafe deserialization** — type-driven polymorphic deserialization of untrusted payloads (`BinaryFormatter`, unsafe Newtonsoft `TypeNameHandling`).
- **Cryptography** — security-sensitive MD5, SHA1, ECB mode, hardcoded keys, custom password hashing, home-grown protocols. MD5/SHA1 used purely as a non-security checksum is not a finding. Passwords belong to ASP.NET Core Identity/password hashers, never reversible encryption.

## Layer 4 — Authentication and access control (A01, A07)

- **Effective authorization** — fallback/global policy, controller and action `[Authorize]`, `[AllowAnonymous]`, policy names, role/claim requirements, resource-based authorization. Determine the actual behavior before reporting.
- **Anonymous surfaces** — confirm each public endpoint is intentional; public is not automatically vulnerable.
- **Resource authorization / IDOR** — operations such as `GET /orders/{id}`, `PUT /users/{id}`, `DELETE /documents/{id}` where possessing an identifier could expose another user's or tenant's data. Look for ownership, tenant or permission checks. Client-side filtering is not authorization.
- **Token validation** — for Bearer/OIDC, check issuer, audience where applicable, signature/signing authority and lifetime. Framework/provider metadata configuration may already establish secure validation; do not demand every `TokenValidationParameters` property be set manually, and do not impose an arbitrary universal `ClockSkew`. Intentionally disabled validation without a valid reason is a finding.
- **Local accounts** — password hashing, reset behavior, lockout/brute-force controls where appropriate, account-enumeration behavior, credential storage.
- **Angular** — guards and hidden buttons are UX; confirm the backend protects sensitive operations.

## Layer 5 — Browser and HTTP/API security (A01, A02)

- **CORS** — origins versus the actual browser-client model; unnecessarily broad trusted origins; credentialed requests from untrusted origins; environment-specific origins leaking into Production. Wildcard origin alone is not a finding without considering intended exposure.
- **CSRF** — when browser credentials (especially cookies) are sent automatically, check protection of state-changing operations. Bearer tokens attached explicitly through the `Authorization` header have different characteristics; Angular does not provide server-side CSRF protection for every model.
- **TLS** — disabled certificate validation, accept-all certificate callbacks, plain HTTP for sensitive external communication. Missing HTTPS redirection is not a finding when the hosting topology enforces TLS.
- **File uploads** — size limits, storage path safety, file-name handling, content/type assumptions (client MIME used as authoritative), execution or public-serving risks, authorization.
- **Rate limiting** — consider where abuse realistically matters (login, password reset, expensive anonymous or resource-intensive endpoints); not required everywhere. `429` semantics: `http-api` skill.

## Layer 6 — Sensitive data, logging and error exposure (A04, A09)

- **Logging** — credentials, tokens, keys, payment data or PII in logs; Debug/Trace treated as safe; duplicate or missing security-relevant logging in context (logs for every successful request are not required).
- **Error responses** — stack traces, SQL, connection strings, internal paths, secret values or internal exception details in public errors.
- **Response data** — Domain/database entities returned directly, password hashes, internal security fields, unnecessary personal data, secret metadata. Inspect the serialized fields; returning an entity is not automatically a vulnerability.
- **Data at rest** — choose protection per need: password → one-way hashing; verification-only token → often a hash; retrievable application secret → protected/encrypted storage; database/storage encryption → platform mechanism; temporary application payload → ASP.NET Core Data Protection may fit. No custom cryptography.

## Layer 7 — Exceptional conditions and failure handling (A06, A10)

- **Fail-open** — an exception caught and a privileged operation continuing: authorization service failed → allow; token validation failed → anonymous but privileged action; permission lookup failed → permitted.
- **Swallowed exceptions** — `catch (Exception) { }` and broad catches that continue without a deliberate fallback; security-relevant failures must not turn into success.
- **Retry and idempotency** — retries of state-changing operations (a lost response plus retry duplicates effects); caller cancellation retried as transient (`httpclient-factory` skill).
- **Resource exhaustion** — unbounded time, memory, rows, file size, request body, retry attempts or parallel work reachable from public input. A theoretical missing limit is not automatically High.
- **Startup and configuration** — invalid auth configuration silently disabling authentication; missing key → plaintext mode; failed authorization provider → allow-all.
- **Unexpected error exposure** — unexpected exceptions follow centralized handling without revealing internals.

## Cross-cutting design review

Static checks do not cover insecure design, tenant isolation, business-workflow abuse, privilege escalation through legitimate operations, financial/idempotency abuse or multi-step authorization problems. Name such workflows as candidates for threat modeling or dedicated manual review instead of claiming the scan proves them secure.

## Severity examples

```text
real production private key committed publicly            → potentially Critical
raw SQL containing only developer-controlled constants    → not SQL injection
missing [Authorize] while a secure fallback policy exists → not a finding
PII logged in a restricted internal diagnostic environment → contextual, not automatically High
```

Never map pattern → fixed severity, CVSS → application severity, or OWASP category → severity mechanically.

## Finding format

```markdown
### [HIGH] src/.../OrdersController.cs:42 — Resource authorization missing

OWASP: A01:2025 Broken Access Control

Evidence:
The endpoint loads an order solely by route ID and does not constrain it to the
authenticated customer.

Impact:
An authenticated user who learns another order ID can read that customer's order.

Remediation:
Apply resource/ownership authorization before returning the order.
```

When evidence is incomplete:

```markdown
### [NEEDS VERIFICATION] ...

The static code suggests ..., but effective behavior depends on ...
```
