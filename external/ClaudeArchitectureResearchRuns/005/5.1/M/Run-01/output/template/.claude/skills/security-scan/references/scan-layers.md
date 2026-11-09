> Owns: per-layer security investigation prompts and false-positive context | Scope: common | Loads: private reference of security-scan (read on demand by that workflow only)

# Security Scan — Layer Reference

Investigation prompts for `security-scan`. They are prompts, not automatic
vulnerability declarations. The invariants being checked are in
`.claude/rules/security.md`.

# Layer 1: Dependencies and Supply Chain (A03)

- .NET: `dotnet package list --vulnerable --include-transitive` (when the SDK
  supports it). Review vulnerable direct and transitive packages, whether the
  vulnerable component is actually used, whether a patched compatible version
  exists, and unexpected or untrusted NuGet sources.
- npm: `npm audit`. Distinguish production vs. development/build dependencies
  and direct vs. transitive packages; a dev-only vulnerability still matters to
  the supply chain but has different runtime impact. Review lockfiles when
  integrity or unexpected dependency changes are relevant.
- Do not upgrade packages during a scan unless asked.

# Layer 2: Secrets and Configuration (A02, A04)

Search source-controlled `.cs`, `.ts`, `.json`, `.yml`/`.yaml`, `.xml`,
`.config`, `.env*`, Dockerfiles, Compose files, CI workflows, and scripts.

- High-confidence indicators: private keys, real access/refresh tokens, cloud
  access keys, database passwords, API secrets, service-account credentials,
  production connection strings with credentials.
- Context-dependent indicators: `ApiKey = "..."`, `Secret = "..."`,
  `Token = "..."`, `Password = "..."`, long opaque strings, connection strings,
  certificate material.
- `appsettings.Development.json` is not exempt. Obviously fake values
  (`changeme`, `example-only`, `test-password`, `not-a-real-key`) may be ignored
  or reported as Info. `UserSecretsId` is not a secret.
- Also review production debug/development flags, certificate-validation
  bypasses, insecure URLs carrying credentials, verbose production error
  configuration, and committed `.env` files.

# Layer 3: Injection and Dangerous Code Patterns (A04, A05, A08)

- **SQL**: SQL built from untrusted input, for example
  `$"SELECT * FROM Orders WHERE Name = '{search}'"`, or interpolated data passed
  to APIs that do not parameterize it. Safe forms: EF Core LINQ, parameterized
  SQL, `FromSqlInterpolated` where appropriate, ADO.NET/Dapper parameters.
  Normal EF Core LINQ with user input in a predicate is not SQL injection.
- **Command injection**: `Process.Start`, shell/PowerShell invocation, arguments
  built from user input. Prefer APIs separating executable and arguments.
- **Path traversal**: user-controlled file names, paths, archive extraction,
  download/upload destinations; look for `../`, absolute-path injection, unsafe
  extraction. Normalize and verify paths stay inside the intended root.
- **SSRF**: user influence over scheme, host, port, full URL, or redirect target,
  especially where the server reaches internal networks or metadata endpoints.
  Ordinary query parameters in an outbound request are not SSRF by themselves.
- **XSS**: Angular sanitizer bypasses (`bypassSecurityTrustHtml`,
  `bypassSecurityTrustScript`, `bypassSecurityTrustResourceUrl`) and direct DOM
  manipulation with untrusted content. Ordinary Angular binding is escaped.
- **Unsafe deserialization**: `BinaryFormatter`, unsafe Newtonsoft
  `TypeNameHandling`, deserializing untrusted payloads into arbitrary types.
- **Cryptography**: security-sensitive MD5/SHA1, ECB mode, hardcoded keys,
  custom password hashing, home-grown protocols. MD5/SHA1 as a non-security
  checksum is not a finding.

# Layer 4: Authentication and Access Control (A01, A07)

- **Effective authorization**: inspect fallback/global policies, controller and
  action `[Authorize]`, `[AllowAnonymous]`, policy names, role/claim
  requirements, resource-based authorization. A missing `[Authorize]` under a
  secure fallback policy, or bare `[Authorize]` where authentication alone is
  intended, is not a finding.
- **Anonymous access**: confirm each public surface is intentional.
- **Resource authorization / IDOR**: operations like `GET /orders/{id}`,
  `PUT /users/{id}`, `DELETE /documents/{id}` where knowing an identifier could
  expose another user's or tenant's data; verify ownership/tenant/permission
  checks. Client-side filtering is not authorization.
- **Bearer/OIDC configuration**: check issuer, audience, signing authority, and
  lifetime validation against the actual provider. Do not demand that every
  `TokenValidationParameters` property be set manually when authority/metadata
  configuration already secures validation, and do not impose an arbitrary
  universal `ClockSkew`. Flag deliberately disabled validation.
- **Local accounts**: password hashing, reset behavior, lockout/brute-force
  controls where appropriate, account-enumeration behavior, credential storage.
- **Angular**: route guards and hidden/disabled buttons are UX; verify the
  backend protects sensitive operations.

# Layer 5: Browser and HTTP/API Security (A01, A02)

- **CORS** is a browser-origin policy, not authorization. Look for broader than
  necessary origins, credentialed requests from untrusted origins, and
  environment-specific origins leaking into Production. `AllowAnyOrigin()` can
  be valid for a genuinely public, non-credentialed API.
- **CSRF**: when browsers send credentials automatically (cookies), review
  protection of state-changing operations. Bearer tokens attached explicitly
  through the `Authorization` header have different characteristics.
- **TLS**: disabled certificate validation, accept-all callbacks, plain HTTP for
  sensitive external calls. Missing in-app HTTPS redirection is not a finding
  when the hosting topology enforces TLS.
- **File uploads**: size limits, storage path safety, file-name handling,
  content/type assumptions, execution/public-serving risk, authorization.
- **Rate limiting**: consider it where abuse realistically matters (login,
  password reset, expensive anonymous or resource-intensive endpoints), not on
  every endpoint. `429` semantics: `http-api`.

# Layer 6: Sensitive Data, Logging, and Error Exposure (A04, A09)

- **Logging**: credentials, tokens, keys, payment data, PII, and full payloads in
  logs. Debug/Trace level is not a security boundary. Do not demand logs for
  every successful request.
- **Error responses**: stack traces, SQL, connection strings, internal paths,
  secret values, exception details in public responses.
- **Response data**: entities returned directly, password hashes, internal
  security fields, unnecessary personal information. Returning a Domain entity is
  not automatically a vulnerability; inspect the serialized fields.
- **Data at rest**: match protection to the requirement — passwords → one-way
  password hashing; verification-only tokens → often hashed; retrievable secrets
  → protected/encrypted storage; database/storage encryption → platform
  mechanism; temporary application payloads → ASP.NET Core Data Protection may
  fit.

# Layer 7: Exceptional Conditions and Failure Handling (A06, A10)

- **Fail-open**: exceptions caught and then allowing a privileged operation
  (authorization service failed → allow; token validation failed → continue as
  anonymous but act privileged; permission lookup failed → permitted).
- **Swallowed exceptions**: empty `catch (Exception)` blocks and broad catches
  continuing without a deliberate fallback; security-relevant failures must not
  turn into success.
- **Retry and idempotency**: retries of state-changing operations that can
  duplicate effects; caller cancellation treated as transient.
- **Resource exhaustion**: unbounded time, memory, rows, file or body size,
  retries, or parallel work on public inputs — rate by actual exploitability.
- **Startup configuration**: invalid auth configuration silently disabling
  authentication, missing keys enabling plaintext mode, failed authorization
  providers falling back to allow-all.

# Cross-Cutting Design Review

Static checks do not cover A06 insecure design, tenant isolation, workflow abuse,
privilege escalation through legitimate operations, financial/idempotency abuse,
or multi-step authorization flaws. Identify such workflows as candidates for
threat modeling or manual review instead of claiming the scan proves them
secure.

# Severity Calibration Examples

- Real production private key committed publicly → potentially Critical.
- Raw SQL containing only developer-controlled constant text → not injection.
- Missing `[Authorize]` while a secure fallback policy exists → not a finding.
- PII logged in a restricted internal diagnostic environment → contextual, not
  automatically High.

# Finding Examples

```markdown
### [HIGH] src/.../OrdersController.cs:42 — Resource authorization missing
OWASP: A01:2025 Broken Access Control
Evidence: The endpoint loads an order solely by route ID and does not constrain
it to the authenticated customer.
Impact: An authenticated user who learns another order ID can read that order.
Remediation: Apply resource/ownership authorization before returning the order.
```

```markdown
### [NEEDS VERIFICATION] ...
The static code suggests ..., but effective behavior depends on ...
```
