Kind: WF | Scope: common | Capability: — | Loading: private reference of `security-scan`, read during a scan

# Security Scan: Layer Checks

Investigation prompts for the `security-scan` workflow, not automatic vulnerability declarations. Where a check corresponds to a standard, the standard is named in parentheses; the standard owns the rule.

## Layer 1: Dependencies and supply chain (A03)

.NET, when supported by the installed SDK:

```bash
dotnet package list --vulnerable --include-transitive
```

Review vulnerable direct and transitive dependencies, advisory severity, whether the vulnerable component is actually used, whether a patched compatible version exists, and unexpected or untrusted NuGet sources. Do not upgrade packages during a scan unless asked. Rate from reachability and exposure, not CVSS alone.

npm, when a frontend workspace exists: `npm audit`. Distinguish production from development/build dependencies and direct from transitive packages. A development-only vulnerability still matters to the supply chain, but its runtime impact differs from a browser-shipped dependency. Review lockfiles when package integrity or unexpected dependency changes are relevant.

`node .claude/scripts/check-manifests.mjs` reports deprecated packages, prerelease or floating versions and Central Package Management violations.

## Layer 2: Secrets and configuration (A02, A04)

Search source-controlled files (`.cs`, `.ts`, `.json`, `.yml`, `.yaml`, `.xml`, `.config`, `.env*`, Dockerfiles, Compose files, CI workflows, scripts) for real credentials (standard: `.claude/rules/common/security.md` → Secrets).

- High-confidence indicators: private keys, real access or refresh tokens, cloud access keys, database passwords, API secrets, service-account credentials, production connection strings with credentials.
- Indicators that need context: `ApiKey = "..."`, `Secret = "..."`, `Token = "..."`, `Password = "..."`, long opaque strings, connection strings, certificate material.
- Do not ignore `appsettings.Development.json`; a real committed secret is a secret regardless of the file name. Obviously fake values (`changeme`, `example-only`, `test-password`, `not-a-real-key`) may be ignored or reported as Info. `UserSecretsId` is not a secret.
- Preferred pattern: `builder.Configuration.GetConnectionString("Default")` with the real secret supplied by the chosen local or deployment secret mechanism.
- Also review production debug or development flags, certificate-validation bypasses, insecure URLs carrying credentials, overly verbose production error configuration and accidentally committed `.env` files.

## Layer 3: Injection and dangerous code patterns (A04, A05, A08)

### SQL injection (standard: `.claude/rules/backend/security.md` → Data access)

Look for SQL built from untrusted input:

```csharp
var sql = $"SELECT * FROM Orders WHERE Name = '{search}'";
```

or interpolated or concatenated data passed to APIs that do not parameterize it. Safe forms: LINQ through the persistence technology, parameterized SQL, ADO.NET or Dapper parameters. Raw-query API specifics: persistence workflow facet → Security review cues. Do not report ordinary LINQ as SQL injection merely because user input participates in a predicate.

### Command injection

Inspect `Process.Start`, shell execution, PowerShell or bash invocation, and command arguments built from user input. Prefer APIs that separate the executable from its arguments, and validate or constrain external input when command execution is genuinely needed.

### Path traversal

Review user-controlled file names, paths, archive extraction, download paths and upload destinations for `../`, absolute-path injection, escapes from the intended root and unsafe archive extraction. Normalize and verify that paths stay inside the intended storage boundary.

### SSRF

Inspect outbound requests where users influence the scheme, host, port, full URL or redirect destination, especially when the server can reach internal networks, metadata endpoints or privileged services. Host or control-plane influence matters; a user-supplied query parameter alone is not SSRF.

### XSS and unsafe HTML

Frontend: the frontend workflow facet → Security review cues lists the framework's sanitizer-bypass APIs; also investigate direct DOM manipulation with untrusted content. Ordinary framework template binding that escapes output is not automatically XSS. Review deliberate raw HTML handling in any server-rendered UI as well.

### Unsafe deserialization

Investigate dangerous polymorphic or type-driven deserialization (legacy examples: `BinaryFormatter`, unsafe Newtonsoft `TypeNameHandling` settings). Untrusted payloads must not be deserialized into arbitrary runtime types.

### Cryptography (standard: `.claude/rules/backend/security.md` → Cryptography and data protection)

Flag security-sensitive use of MD5, SHA1, ECB mode, hardcoded encryption keys, custom password hashing and home-grown encryption protocols. MD5 or SHA1 as a non-security checksum is not a finding. Passwords use established password-hashing facilities such as ASP.NET Core Identity password hashers.

## Layer 4: Authentication and access control (A01, A07)

### Effective authorization

Determine the effective access policy: fallback or global policy, controller and action `[Authorize]`, `[AllowAnonymous]`, policy names, role or claim requirements, resource-based authorization. An endpoint without `[Authorize]` is not vulnerable when a secure fallback policy protects it, and a bare `[Authorize]` is not insufficient when authentication alone is intended.

### Anonymous access (standard: `.claude/rules/backend/security.md` → Authentication and authorization)

Review `[AllowAnonymous]` and other deliberately public surfaces and confirm that public access is intentional. Not every public endpoint is a vulnerability.

### Resource authorization and IDOR

For operations such as `GET /orders/{id}`, `PUT /users/{id}` or `DELETE /documents/{id}`, check whether possession of an identifier is enough to access another user's or tenant's data, and verify ownership, tenant, permission or resource policy where required. Client-side filtering is not authorization.

### Authentication configuration (standard: `.claude/rules/backend/security.md`)

For Bearer/OIDC, check that the configured mechanism validates issuer, audience where applicable, signature or signing authority, and lifetime. Do not require every `TokenValidationParameters` property to be set manually when the provider's authority or metadata configuration already establishes secure validation, and do not impose an arbitrary universal `ClockSkew`. Flag intentionally disabled validation that weakens the authentication contract without a valid reason.

### Passwords and accounts

When the application owns local accounts, review password hashing, reset behavior, lockout and brute-force controls where appropriate, account-enumeration behavior and credential storage.

### Frontend

Route guards and hidden or disabled buttons are UX mechanisms (standard: `.claude/rules/common/security.md` → Trust boundaries). Verify that sensitive operations are protected by the backend.

## Layer 5: Browser and HTTP/API security (A01, A02)

- **CORS** (standard: `.claude/rules/backend/security.md`): CORS is a browser-origin policy, not authorization. Review whether configured origins match the actual browser-client model: unnecessarily broad trusted origins, credentialed requests from untrusted origins, development origins exposed in Production. `AllowAnyOrigin()` can be valid for a genuinely public, non-credentialed API.
- **CSRF** (standard: `.claude/rules/frontend/frontend.md` → Browser security): when browser credentials, especially cookies, are sent automatically, review CSRF protection for state-changing operations. Bearer tokens attached explicitly through the `Authorization` header have different CSRF characteristics.
- **TLS** (standard: `.claude/rules/common/security.md` → Transport): review disabled certificate validation, accept-all certificate callbacks and plain HTTP for sensitive external communication, accounting for TLS termination at proxies, ingress, gateways or the hosting platform.
- **File uploads** (standard: `.claude/rules/backend/security.md` → Uploads): review size limits, storage path safety, file-name handling, content and type assumptions, execution or public-serving risks, and authorization.
- **Rate limiting**: consider it where abuse realistically matters (login and password reset, expensive anonymous endpoints, resource-intensive operations), not on every endpoint. `429` semantics: `http-api` skill.

## Layer 6: Sensitive data, logging and error exposure (A04, A09)

- **Logging** (standard: `.claude/rules/common/security.md` → Sensitive data in logs): look for logged passwords, tokens, private keys, authentication secrets, payment credentials and unjustified PII. Debug or Trace level is not a security boundary. Review duplicate or missing security-relevant logging in context; do not demand logs for every successful request.
- **Error responses** (standard: `.claude/rules/backend/error-handling.md` → Error contracts): look for stack traces, SQL, connection strings, internal file-system paths, secret values and internal exception details in public errors.
- **Response data**: look for Domain or database entities returned directly, password hashes, internal security fields, unnecessary personal information and secret metadata. Inspect the actual serialized fields; returning an entity is not automatically vulnerable.
- **Data at rest**: password → one-way password hashing; verification-only token → often a hash rather than reversible encryption; retrievable application secret → appropriate protected or encrypted storage; database or storage encryption → platform or database mechanism when suitable; temporary application payload → ASP.NET Core Data Protection may be suitable.

## Layer 7: Exceptional conditions and failure handling (A06, A10)

- **Fail-open behavior** (standard: `.claude/rules/common/security.md` → Failure behavior of security controls): look for code that catches an exception and then lets a privileged operation continue, for example authorization service failed → allow, token validation failed → continue as anonymous but perform a privileged action, permission lookup failed → default to permitted.
- **Swallowed exceptions**: review empty `catch (Exception) { }` blocks and broad catches that continue without a deliberate fallback. Not every swallowed exception is a vulnerability, but security-relevant failures must not turn into success.
- **Retry and idempotency** (standard: `.claude/rules/backend/integrations.md`): review retries of state-changing operations; a lost response followed by a retry can duplicate effects. Technique: `httpclient-factory` skill.
- **Timeouts and resource exhaustion**: review operations or public inputs that can consume unbounded time, memory, database rows, file size, request body, retry attempts or parallel work. A theoretical lack of a limit is not automatically High; evaluate whether an attacker can exploit it.
- **Startup and configuration failure** (standard: `.claude/rules/common/security.md` → Failure behavior of security controls): review security-sensitive startup for dangerous fallbacks, such as invalid auth configuration → authentication silently disabled, missing encryption key → plaintext mode, failed authorization provider → allow-all.
- **Unexpected error exposure**: confirm that unexpected exceptions follow the centralized error-handling standard.

## Cross-cutting design review

Static checks do not fully cover insecure design, tenant isolation, business-workflow abuse, privilege escalation through legitimate operations, financial or idempotency abuse, or multi-step authorization problems. When the application has meaningful security-sensitive workflows, name them as candidates for threat modeling or dedicated manual review instead of claiming that the static scan proves them secure.

## Severity examples

Do not map pattern → fixed severity, CVSS → application severity or OWASP category → severity mechanically.

```text
real production private key committed publicly            → potentially Critical
raw SQL containing only developer-controlled constant text → not SQL injection
missing [Authorize] while a secure fallback policy exists  → not a finding
PII logged in a restricted internal diagnostic environment → contextual, not automatically High
```

## Finding format

```markdown
### [HIGH] src/.../File.cs:42 — Resource authorization missing

OWASP: A01:2025 Broken Access Control

Evidence:
The endpoint loads an order solely by route ID and does not constrain it to the authenticated customer.

Impact:
An authenticated user who learns another order ID may access that customer's order.

Remediation:
Apply resource or ownership authorization before returning the order.
```

When evidence is incomplete:

```markdown
### [NEEDS VERIFICATION] ...

The static code suggests ..., but effective behavior depends on ...
```

Do not invent exploitability that the code does not establish.
