> Level: 2-technology · Owns: layer-by-layer investigation technique for .NET/ASP.NET Core backends and browser frontends (private reference of `security-scan`) · Loading: read by `security-scan`

# Security Scan — Layer Reference

Investigation prompts, not automatic vulnerability declarations.

## Layer 1: Dependencies and supply chain (A03)

- .NET: `dotnet package list --vulnerable --include-transitive` when supported. Review vulnerable direct and transitive packages, advisory severity, whether the component is actually used, whether a patched compatible version exists, and unexpected or untrusted NuGet sources. Do not upgrade packages during a scan unless asked.
- Frontend: the audit command in `frontend.commands`. Distinguish production from development/build dependencies and direct from transitive packages; a development-only vulnerability still matters for the supply chain but has different runtime impact. Review lockfiles when integrity or unexpected dependency changes matter.

## Layer 2: Secrets and configuration (A02, A04)

Search source-controlled `.cs`, `.ts`, `.json`, `.yml`/`.yaml`, `.xml`, `.config`, `.env*`, Dockerfiles, Compose files, CI workflows, and scripts.

- High-confidence indicators: private keys, real access/refresh tokens, cloud access keys, database passwords, API secrets, service-account credentials, production connection strings with credentials.
- Context-dependent: `ApiKey = "..."`, `Secret = "..."`, `Token = "..."`, `Password = "..."`, long opaque strings, connection strings, certificate material.
- Do not ignore `appsettings.Development.json` automatically; obviously fake values (`changeme`, `example-only`, `test-password`, `not-a-real-key`) may be ignored or reported as Info. `UserSecretsId` is not a secret. Preferred: `builder.Configuration.GetConnectionString("Default")` with the value supplied by the chosen secret mechanism.
- Also review production debug/development flags, certificate-validation bypasses, URLs carrying credentials, verbose production error configuration, committed `.env` files.

## Layer 3: Injection and dangerous code patterns (A04, A05, A08)

- **SQL injection** — SQL built from untrusted input (`$"SELECT ... WHERE Name = '{search}'"`) or interpolated data passed to APIs that do not parameterize. Prefer ORM LINQ, parameterized SQL, interpolation-aware raw-SQL APIs, ADO.NET or micro-ORM parameters. Ordinary ORM LINQ predicates with user input are not SQL injection.
- **Command injection** — `Process.Start`, shell/PowerShell invocation, arguments built from user input; prefer APIs separating executable and arguments; constrain input.
- **Path traversal** — user-controlled file names, paths, archive extraction, download/upload destinations; look for `../`, absolute-path injection, unsafe extraction; normalize and verify paths stay inside the intended root.
- **SSRF** — user influence over scheme, host, port, full URL, or redirects, especially with access to internal networks or metadata endpoints. A user-supplied query parameter alone is not SSRF; host/control-plane influence matters.
- **XSS / unsafe HTML** — deliberate sanitizer bypasses and direct DOM manipulation with untrusted content in the frontend (framework-specific APIs: frontend knowledge skill); ordinary template binding benefits from framework escaping. Review raw HTML handling in any server-rendered UI.
- **Unsafe deserialization** — `BinaryFormatter`, unsafe `TypeNameHandling`, deserializing untrusted payloads into arbitrary runtime types.
- **Cryptography** — security-sensitive MD5, SHA1, ECB mode, hardcoded keys, custom password hashing, home-grown protocols. MD5/SHA1 as non-security checksums are fine. Passwords use established hashers such as ASP.NET Core Identity's, never reversible encryption.

## Layer 4: Authentication and access control (A01, A07)

- **Effective authorization** — fallback/global policy, controller and action `[Authorize]`, `[AllowAnonymous]`, policy names, role/claim requirements, resource-based authorization. Determine actual behavior before reporting.
- **Anonymous access** — confirm public surfaces are intentional; a public endpoint is not automatically a vulnerability.
- **Resource authorization / IDOR** — `GET /orders/{id}`, `PUT /users/{id}`, `DELETE /documents/{id}` where possessing an identifier could expose another user's or tenant's data; verify ownership, tenant, or permission checks. Client-side filtering is not authorization.
- **Authentication configuration** — for Bearer/OIDC, check issuer, audience where applicable, signature/signing authority, lifetime. Do not demand every `TokenValidationParameters` property when authority metadata already establishes secure validation, and do not impose a universal `ClockSkew`. Flag intentionally disabled validation without a valid reason.
- **Local accounts** — password hashing, reset behavior, lockout/brute-force controls where appropriate, account enumeration, credential storage.
- **Frontend** — route guards and hidden/disabled buttons are UX; verify the backend protects sensitive operations.

## Layer 5: Browser and HTTP/API security (A01, A02)

- **CORS** — a browser-origin policy, not authorization. Look for unnecessarily broad trusted origins, credentialed requests from untrusted origins, and environment-specific origins leaking into Production. A wildcard alone is not a finding for a genuinely public non-credentialed API.
- **CSRF** — when browser credentials (especially cookies) are sent automatically, review CSRF protection for state-changing operations; explicitly attached Bearer headers have different characteristics.
- **TLS** — disabled certificate validation, accept-all callbacks, plain HTTP for sensitive external calls. Account for termination at proxies, ingress, gateways, or platforms; missing HTTPS redirection in code is not automatically a vulnerability.
- **File uploads** — size limits, storage path safety, file-name handling, content/type assumptions, execution or public-serving risks, authorization.
- **Rate limiting** — consider it where abuse realistically matters (login, password reset, expensive anonymous or resource-intensive endpoints); not required everywhere. 429 semantics: `http-api`.

## Layer 6: Sensitive data, logging, and error exposure (A04, A09)

- **Logging** — passwords, tokens, private keys, authentication secrets, payment credentials; PII per project requirements; Debug/Trace is not a security boundary. Review missing or duplicated security-relevant logging in context; do not demand logs for every successful request.
- **Error responses** — compare public error payloads against the failure rules in `.claude/rules/0-core/http-api.md`.
- **Response data** — domain/persistence entities returned directly, password hashes, internal security fields, unnecessary personal data, secret metadata; inspect the actual serialized fields before reporting.
- **Data at rest** — choose protection by requirement: one-way hashing for passwords; hashing for verification-only tokens; protected storage for retrievable secrets; platform/database encryption where suitable; ASP.NET Core Data Protection for temporary application payloads — not as universal database encryption.

## Layer 7: Exceptional conditions and failure handling (A06, A10)

- **Fail-open** — catch blocks that let privileged operations continue (authorization service failed → allow; token validation failed → continue anonymous but act privileged; permission lookup failed → permitted).
- **Swallowed exceptions** — empty `catch (Exception) { }` or broad catches without deliberate fallback; security-relevant failures must not silently become success.
- **Retry and idempotency** — retried state-changing operations can duplicate effects; caller cancellation is never a transient failure. Technique: `httpclient-factory`.
- **Timeouts and resource exhaustion** — unbounded time, memory, rows, file size, request body, retries, parallel work; judge real exploitability before rating.
- **Startup and configuration failure** — invalid auth config silently disabling authentication, missing encryption key falling back to plaintext, failed authorization provider allowing everything.
- **Unexpected error exposure** — unexpected exceptions follow centralized handling and reveal nothing sensitive.

## Cross-cutting design review

Static checks do not cover insecure design, tenant isolation, business workflow abuse, privilege escalation through legitimate operations, financial/idempotency abuse, or multi-step authorization problems. Name meaningful security-sensitive workflows as candidates for threat modeling or dedicated manual review instead of claiming the scan proves them secure.

## Severity examples

- Real production private key committed publicly → potentially Critical.
- Raw SQL containing only developer-controlled constant text → not SQL injection.
- Missing `[Authorize]` while a secure fallback policy exists → not a finding.
- PII logged in a restricted internal diagnostic environment → contextual, not automatically High.

## Finding examples

```markdown
### [HIGH] src/.../File.cs:42 — Resource authorization missing
OWASP: A01:2025 Broken Access Control
Evidence: The endpoint loads an order solely by route ID and does not constrain it to the authenticated customer.
Impact: An authenticated user who learns another order ID may access that customer's order.
Remediation: Apply resource/ownership authorization before returning the order.
```

```markdown
### [NEEDS VERIFICATION] ...
The static code suggests ..., but effective behavior depends on ...
```

Never invent exploitability the code does not establish.
