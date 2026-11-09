> Level: 2-technology | Owns: per-layer investigation prompts for security-scan (skill-private reference) | Scope: common | Loads: read by security-scan only

# Security Scan — Layer Reference

Investigation prompts, not automatic vulnerability declarations.

# Layer 1: Dependencies and supply chain (A03)

.NET, when the installed SDK supports it:

```bash
dotnet package list --vulnerable --include-transitive
```

Review vulnerable direct and transitive packages, advisory severity, whether
the vulnerable component is actually used, whether a patched compatible version
exists, and unexpected or untrusted package sources. Rate the application
finding by reachability and exposure, not CVSS alone.

Frontend (when selected): run the audit command from `frontend.commands`.
Distinguish production from development/build dependencies and direct from
transitive packages; a development-only vulnerability still matters to the
supply chain but has different runtime impact. Review lockfiles when package
integrity or unexpected dependency changes matter.

# Layer 2: Secrets and configuration (A02, A04)

Search source-controlled files — `.cs`, `.ts`, `.json`, `.yml`/`.yaml`,
`.xml`, `.config`, `.env*`, container and Compose files, CI workflows, scripts —
for real credentials.

High-confidence indicators: private keys, real access/refresh tokens, cloud
access keys, database passwords, API secrets, service-account credentials,
production connection strings with credentials.

Indicators needing context: `ApiKey = "..."`, `Secret = "..."`,
`Token = "..."`, `Password = "..."`, long opaque strings, connection strings,
certificate material.

Do not ignore `appsettings.Development.json`: a real committed secret is a
secret regardless of the file name. Obviously fake values (`changeme`,
`example-only`, `test-password`, `not-a-real-key`) may be ignored or reported as
Info. `UserSecretsId` is not a secret. Preferred pattern:
`builder.Configuration.GetConnectionString("Default")` with the value supplied
by the chosen secret mechanism.

Also review production debug/development flags, certificate-validation
bypasses, insecure URLs carrying credentials, overly verbose production error
configuration, and accidentally committed `.env` files.

# Layer 3: Injection and dangerous code patterns (A04, A05, A08)

## SQL injection

Look for SQL built from untrusted input, for example
`$"SELECT * FROM Orders WHERE Name = '{search}'"`, or interpolated/concatenated
data passed to APIs that do not parameterize it. Safe forms: the persistence
implementation's LINQ/query API and its interpolation-safe raw SQL APIs
(`persistence.knowledge`), parameterized ADO.NET or micro-ORM parameters. Do not
report ordinary LINQ as injection merely because user input participates in a
predicate.

## Command injection

Inspect `Process.Start`, shell/PowerShell invocation, and arguments built from
user input. Prefer APIs that separate executable and arguments; constrain input
when command execution is genuinely needed.

## Path traversal

Review user-controlled file names, paths, archive extraction, download paths,
and upload destinations for `../`, absolute-path injection, escaping the
intended root, and unsafe extraction. Normalize and verify paths stay inside the
intended storage boundary.

## SSRF

Inspect outbound requests where users influence scheme, host, port, full URL,
or redirect destination — especially when the server reaches internal networks,
metadata endpoints, or privileged services. A user-supplied query parameter in
an outbound request is not SSRF by itself; host/control-plane influence
matters.

## XSS and unsafe HTML

Investigate deliberate sanitizer bypasses in the frontend framework (listed in
`frontend.knowledge`) and direct DOM manipulation with untrusted content.
Ordinary template binding benefits from framework escaping and is not
automatically XSS. Review deliberate raw HTML handling in any server-rendered UI.

## Unsafe deserialization

Investigate polymorphic/type-driven deserialization (legacy `BinaryFormatter`,
unsafe Newtonsoft `TypeNameHandling` settings). Never deserialize untrusted
payloads into arbitrary runtime types.

## Cryptography

Flag security-sensitive MD5, SHA1, ECB mode, hardcoded encryption keys, custom
password hashing, home-grown protocols. MD5/SHA1 as a non-security checksum is
not a finding. Passwords use established password-hashing facilities (ASP.NET
Core Identity password hashers), never reversible encryption.

# Layer 4: Authentication and access control (A01, A07)

## Effective authorization

Inspect fallback/global policies, controller and action `[Authorize]`,
`[AllowAnonymous]`, policy names, role/claim requirements, and resource-based
authorization, and determine the actual behavior. A missing `[Authorize]` under
a secure fallback policy is not a finding; bare `[Authorize]` is not
insufficient when authentication alone is intended.

## Anonymous access

Confirm every `[AllowAnonymous]` or public surface is intentional; do not report
every public endpoint.

## Resource authorization / IDOR

For operations such as `GET /orders/{id}`, `PUT /users/{id}`,
`DELETE /documents/{id}`, check whether possession of an identifier is enough
to reach another user's or tenant's data; verify ownership, tenant, permission,
or resource policy. Client-side filtering is not authorization.

## Authentication configuration

For Bearer/OIDC, check token validation against `security.md` (Authentication
and authorization). Do not require manually
setting every `TokenValidationParameters` property when the provider's
authority/metadata already establishes secure validation, and do not impose an
arbitrary universal `ClockSkew`. Flag validation disabled without a valid
reason.

## Passwords and accounts

When the application owns local accounts, review password hashing, reset
behavior, lockout/brute-force controls where appropriate, account-enumeration
behavior, and credential storage.

## Frontend

Route guards and hidden/disabled buttons are UX; verify sensitive operations
are protected by the backend.

# Layer 5: Browser and HTTP/API security (A01, A02)

- **CORS** is a browser-origin policy, not authorization. Check that origins
  match the actual client model; look for unnecessarily broad origins,
  credentialed requests from untrusted origins, and development origins exposed
  in Production. `AllowAnyOrigin()` can be valid for a genuinely public,
  non-credentialed API.
- **CSRF** — when browser credentials are sent automatically (cookies), review
  CSRF protection for state-changing operations; explicit `Authorization`
  header tokens differ.
- **TLS** — disabled certificate validation, accept-all certificate callbacks,
  plain HTTP for sensitive external calls. Missing HTTPS redirection in code is
  not a finding when the hosting topology enforces TLS.
- **File uploads** — size limits, storage path safety, file-name handling,
  content/type assumptions (client MIME type is not authoritative),
  execution/public-serving risks, authorization.
- **Rate limiting** — consider it where abuse realistically matters (login,
  password reset, expensive anonymous or resource-intensive endpoints); not on
  every endpoint. `429` semantics: `http-api`.

# Layer 6: Sensitive data, logging, and error exposure (A04, A09)

- **Logging** — passwords, access/refresh tokens, private keys, authentication
  secrets, full payment credentials; PII per project requirements. Debug/Trace
  level is not a security boundary. Do not demand logs for every successful
  request.
- **Error responses** — stack traces, SQL, connection strings, internal paths,
  secret values, internal exception details.
- **Response data** — entities returned directly, password hashes, internal
  security fields, unnecessary personal data, secret metadata. Returning a
  domain entity is not automatically vulnerable; inspect the serialized fields.
- **Data at rest** — choose protection by requirement: passwords → one-way
  hashing; verification-only tokens → often hashed; retrievable secrets →
  protected/encrypted storage; database/storage encryption → platform
  mechanisms; temporary application payloads → ASP.NET Core Data Protection may
  fit. Never roll custom cryptography.

# Layer 7: Exceptional conditions and failure handling (A06, A10)

- **Fail-open** — code that catches an exception and then allows a privileged
  operation: authorization service failed → allow; token validation failed →
  continue anonymously but act privileged; permission lookup failed → permitted.
- **Swallowed exceptions** — `catch (Exception) { }` and broad catches without
  a deliberate fallback; security-relevant failures must not become success.
- **Retry and idempotency** — retries of state-changing operations can duplicate
  effects after a lost response; caller cancellation is not transient.
- **Timeouts and resource exhaustion** — unbounded time, memory, rows, file
  size, request body, retries, or parallel work; rate severity by real
  exploitability.
- **Startup and configuration failure** — invalid auth configuration silently
  disabling authentication, a missing key falling back to plaintext, a failed
  authorization provider falling back to allow-all.
- **Unexpected error exposure** — confirm centralized error handling hides
  sensitive details.

# Cross-cutting design review

Static checks do not cover insecure design, tenant isolation, business-workflow
abuse, privilege escalation through legitimate operations, financial or
idempotency abuse, or multi-step authorization problems. Recommend such
workflows for threat modeling or manual review instead of claiming the scan
proves them secure.

# Severity examples

- Real production private key committed publicly → potentially Critical.
- Raw SQL containing only developer-controlled constant text → not SQL injection.
- Missing `[Authorize]` while a secure fallback policy exists → not a finding.
- PII logged in a restricted internal diagnostic environment → contextual, not
  automatically High.

Never map pattern → severity, CVSS → application severity, or OWASP category →
severity mechanically, and never invent exploitability the code does not
establish.

```markdown
### [NEEDS VERIFICATION] ...

The static code suggests ..., but effective behavior depends on ...
```
