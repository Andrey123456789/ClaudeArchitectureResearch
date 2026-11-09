> Level: 3 Project | Owns: security investigation prompts per layer (private to `security-scan`) | Scope: common | Loads: on demand by `security-scan` | Depends on: 0-core/*, 2-technology/*

# Security Scan — Layer Reference

Investigation prompts, not automatic vulnerability declarations. The invariants
being checked are owned by the Core security principles and their bindings;
this file only says where and how to look.

## Layer 1 — Dependencies and Supply Chain (A03)

- .NET: `dotnet package list --vulnerable --include-transitive`. Review direct
  and transitive vulnerabilities, advisory details, whether the vulnerable
  component is actually used, whether a patched compatible version exists, and
  unexpected or untrusted NuGet sources.
- npm: `npm audit`. Distinguish production vs. development/build dependencies
  and direct vs. transitive packages; a dev-only issue still matters to the
  supply chain but has different runtime impact. Review lockfiles when
  integrity or unexpected dependency changes matter.
- Do not upgrade packages during a scan unless asked.

## Layer 2 — Secrets and Configuration (A02, A04)

Search `.cs`, `.ts`, `.json`, `.yml`, `.yaml`, `.xml`, `.config`, `.env*`,
Dockerfiles, Compose files, CI workflows, and scripts.

- High-confidence indicators: private keys, real access/refresh tokens, cloud
  access keys, database passwords, API secrets, service-account credentials,
  production connection strings with credentials.
- Context-dependent indicators: `ApiKey = "..."`, `Secret = "..."`,
  `Token = "..."`, `Password = "..."`, long opaque strings, connection strings,
  certificate material.
- `appsettings.Development.json` is not exempt; obviously fake values
  (`changeme`, `example-only`, `not-a-real-key`) may be ignored or reported as
  Info; `UserSecretsId` is not a secret.
- Also review production debug flags, certificate-validation bypasses,
  credential-bearing URLs, verbose production error settings, and committed
  `.env` files.

## Layer 3 — Injection and Dangerous Code Patterns (A04, A05, A08)

- **SQL:** SQL built from untrusted input, e.g.
  `$"SELECT * FROM Orders WHERE Name = '{search}'"`, or interpolated data passed
  to APIs that do not parameterize. Normal EF Core LINQ with user input in a
  predicate is not SQL injection; `FromSqlInterpolated` and ADO.NET/Dapper
  parameters are the safe forms.
- **Command injection:** `Process.Start`, shell/PowerShell invocation, arguments
  built from user input; prefer APIs that separate executable and arguments.
- **Path traversal:** user-controlled file names, paths, archive extraction,
  download or upload destinations; look for `../`, absolute-path injection, and
  unsafe extraction; normalize and verify paths stay inside the storage root.
- **SSRF:** user influence over scheme, host, port, full URL, or redirect
  target, especially where the server reaches internal networks or metadata
  endpoints; a user-supplied query parameter alone is not SSRF.
- **XSS:** Angular sanitizer bypasses (`bypassSecurityTrustHtml`,
  `bypassSecurityTrustScript`, `bypassSecurityTrustResourceUrl`) and direct DOM
  manipulation with untrusted content; ordinary Angular binding is escaped.
- **Deserialization:** `BinaryFormatter`, unsafe Newtonsoft `TypeNameHandling`,
  untrusted payloads deserialized into arbitrary runtime types.
- **Cryptography:** security-sensitive MD5/SHA1, ECB mode, hardcoded keys,
  custom password hashing, home-grown protocols. MD5/SHA1 as non-security
  checksums are not findings.

## Layer 4 — Authentication and Access Control (A01, A07)

- **Effective authorization:** fallback/global policy, controller and action
  `[Authorize]`, `[AllowAnonymous]`, policy names, role/claim requirements,
  resource-based authorization. A missing `[Authorize]` under a secure fallback
  policy is not a finding; bare `[Authorize]` can be the intended policy.
- **Anonymous surfaces:** confirm each `[AllowAnonymous]` endpoint is
  intentionally public.
- **IDOR:** `GET /orders/{id}`, `PUT /users/{id}`, `DELETE /documents/{id}` —
  verify ownership, tenant, or permission checks; client-side filtering is not
  authorization.
- **Token validation:** issuer, audience, signature/signing authority, lifetime.
  Do not demand manual `TokenValidationParameters` when authority metadata
  already establishes validation, and do not impose a universal `ClockSkew`.
- **Local accounts:** password hashing, reset behavior, lockout/brute-force
  controls, account-enumeration behavior, credential storage.
- **Angular:** route guards and hidden buttons are UX; verify the backend
  protects sensitive operations.

## Layer 5 — Browser and HTTP/API Security (A01, A02)

- **CORS:** compare origins with the browser-client model; look for broad
  trusted origins, credentialed requests from untrusted origins, and
  Development origins exposed in Production. `AllowAnyOrigin()` can be valid
  for a public non-credentialed API. CORS is not authorization.
- **CSRF:** with automatically sent cookie credentials, review state-changing
  operations; Bearer tokens in the `Authorization` header behave differently.
- **TLS:** disabled certificate validation, accept-all callbacks, plain HTTP for
  sensitive external calls; account for TLS termination at proxies or platforms.
- **Uploads:** size limits, storage path safety, file-name handling,
  content/type assumptions, execution or public-serving risk, authorization.
- **Rate limiting:** login, password reset, expensive anonymous or
  resource-intensive endpoints; not required everywhere (`429` semantics:
  `http-api` skill).

## Layer 6 — Sensitive Data, Logging, Error Exposure (A04, A09)

- Logs: secrets and tokens, PII without permitted need, Debug/Trace treated as
  a safe level, duplicate or missing security-relevant logging in context.
- Public errors: stack traces, SQL, connection strings, internal paths, secret
  values, internal exception details.
- Response data: entities returned directly, password hashes, internal security
  fields, unnecessary personal data, secret metadata — inspect the actual
  serialized fields before reporting.
- Data at rest: password → one-way hashing; verification-only token → often
  hash; retrievable secret → protected storage; database/storage encryption →
  platform mechanism; temporary payload → Data Protection may fit.

## Layer 7 — Exceptional Conditions (A06, A10)

- **Fail-open:** exceptions caught and a privileged operation continues
  (authorization service failed → allow; permission lookup failed → permitted).
- **Swallowed exceptions:** empty `catch (Exception) { }` or broad catches that
  continue without a deliberate fallback.
- **Retry and idempotency:** retried state-changing operations, lost-response
  duplicates, retried caller cancellation.
- **Resource exhaustion:** unbounded time, memory, rows, file or body size,
  retries, or parallel work reachable from public input; a theoretical missing
  limit is not automatically High.
- **Startup fallback:** invalid auth configuration silently disabling
  authentication, missing key → plaintext mode, failed provider → allow-all.
- **Unexpected errors:** centralized handling without sensitive detail.

## Severity Examples

- Real production private key committed publicly → potentially Critical.
- Raw SQL with only developer-controlled constant text → not SQL injection.
- Missing `[Authorize]` with a secure fallback policy → not a finding.
- PII logged in a restricted internal diagnostic environment → contextual, not
  automatically High.

## Finding Templates

```markdown
### [HIGH] src/.../File.cs:42 — Resource authorization missing
OWASP: A01:2025 Broken Access Control
Evidence: The endpoint loads an order by route ID without constraining it to the
authenticated customer.
Impact: An authenticated user who learns another order ID can read it.
Remediation: Apply resource/ownership authorization before returning the order.
```

```markdown
### [NEEDS VERIFICATION] ...
The static code suggests ..., but effective behavior depends on ...
```
