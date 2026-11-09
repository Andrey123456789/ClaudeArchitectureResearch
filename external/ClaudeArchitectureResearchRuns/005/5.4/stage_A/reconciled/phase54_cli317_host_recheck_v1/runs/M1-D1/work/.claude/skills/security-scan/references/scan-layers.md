> Private reference of `security-scan` · Investigation prompts per layer · Prompts are not automatic vulnerability declarations; the security invariants they check are owned by `.claude/rules/security.md`

# Security Scan — Layer Reference

# Layer 1: Dependencies and Supply Chain

OWASP: `A03:2025 Software Supply Chain Failures`

## .NET

When supported by the installed SDK:

```bash
dotnet package list --vulnerable --include-transitive
```

Review vulnerable direct and transitive dependencies, advisory severity,
whether the vulnerable component is actually used by the application, whether
a patched compatible version exists, and unexpected or untrusted NuGet sources.
Do not upgrade a package during a scan unless asked, and do not rate the
finding from CVSS alone — consider reachability and exposure.

## npm

When an npm frontend exists, inspect `npm audit`. Distinguish production from
development/build dependencies and direct from transitive packages. A
development-only vulnerability can still matter to the supply chain, but its
runtime impact differs from a browser-shipped dependency. Review lockfiles when
package integrity or unexpected dependency changes are relevant.

# Layer 2: Secrets and Configuration

OWASP: `A02:2025 Security Misconfiguration`, `A04:2025 Cryptographic Failures`

Search source-controlled `.cs`, `.ts`, `.json`, `.yml`, `.yaml`, `.xml`,
`.config`, `.env*`, Dockerfile, Compose, CI workflow, and script files for real
credentials and secret material.

High-confidence indicators: private keys, real access/refresh tokens, cloud
access keys, database passwords, API secrets, service-account credentials,
production connection strings containing credentials.

Indicators requiring context: `ApiKey = "..."`, `Secret = "..."`,
`Token = "..."`, `Password = "..."`, long opaque strings, connection strings,
certificate material.

Do not automatically ignore `appsettings.Development.json`; a real committed
secret remains a secret regardless of the file name. Obviously fake values
(`changeme`, `example-only`, `test-password`, `not-a-real-key`) may be ignored
or reported as Info when context makes them clearly non-sensitive.
`UserSecretsId` itself is not a secret.

Preferred pattern:

```csharp
var connectionString =
    builder.Configuration.GetConnectionString("Default");
```

with the real secret supplied through the chosen local or deployment secret
mechanism. Also review production debug/development flags, certificate
validation bypass, insecure URLs carrying credentials, overly verbose
production error configuration, and accidentally committed `.env` files.

# Layer 3: Injection and Dangerous Code Patterns

OWASP: `A04 Cryptographic Failures`, `A05 Injection`, `A08 Software or Data Integrity Failures`

## SQL Injection

Look for SQL constructed from untrusted input, or interpolated/concatenated
data passed to APIs that do not parameterize it:

```csharp
var sql =
    $"SELECT * FROM Orders WHERE Name = '{search}'";
```

Prefer ORM LINQ queries, parameterized SQL, interpolation-aware raw-SQL APIs
where appropriate (persistence knowledge skill), and ADO.NET/micro-ORM
parameters. Do not report ordinary ORM LINQ as SQL injection merely because
user input participates in a predicate.

## Command Injection

Inspect `Process.Start`, shell execution, PowerShell/bash invocation, and
command arguments built from user input. Prefer APIs that separate executable
and arguments; validate or constrain external input when command execution is
genuinely needed.

## Path Traversal

Review user-controlled file names, paths, archive extraction, download paths,
and upload destinations for `../`, absolute-path injection, escape from the
intended root, and unsafe archive extraction. Normalize and verify that paths
remain within the intended storage boundary.

## SSRF

Inspect outbound requests where users can influence the scheme, host, port,
full URL, or redirect destination, especially when the server can reach
internal networks, metadata endpoints, or privileged services. Host or
control-plane influence matters; do not report every user-supplied query
parameter in an outbound request as SSRF.

## XSS and Unsafe HTML

Investigate deliberate sanitizer bypasses and direct DOM manipulation with
untrusted content in the frontend (framework-specific bypass APIs are listed in
the frontend knowledge skill). Ordinary template binding benefits from
framework escaping/sanitization and is not automatically XSS. Review deliberate
raw HTML handling in any server-rendered UI as well.

## Unsafe Deserialization

Investigate dangerous polymorphic or type-driven deserialization, such as
`BinaryFormatter` or unsafe Newtonsoft `TypeNameHandling` configurations. Do
not deserialize untrusted payloads into arbitrary runtime types.

## Cryptography

Flag security-sensitive uses of MD5, SHA1, ECB mode, hardcoded encryption keys,
custom password hashing, or home-grown encryption protocols. Do not flag
MD5/SHA1 used as a non-security checksum where collision resistance is
irrelevant. For passwords, expect established password-hashing facilities such
as ASP.NET Core Identity password hashers rather than reversible encryption.

# Layer 4: Authentication and Access Control

OWASP: `A01:2025 Broken Access Control`, `A07:2025 Authentication Failures`

## Effective Authorization

Determine the effective access policy: fallback/global authorization policy,
controller and action `[Authorize]`, `[AllowAnonymous]`, policy names,
role/claim requirements, resource-based authorization. An endpoint without an
explicit `[Authorize]` is not automatically vulnerable when a secure fallback
policy protects it; bare `[Authorize]` is not automatically insufficient when
simple authentication is the intended requirement.

## Anonymous Access

Review `[AllowAnonymous]` and other public surfaces and confirm that public
access is intentional. Do not report every public endpoint as a vulnerability.

## Resource Authorization / IDOR

Look for operations such as `GET /orders/{id}`, `PUT /users/{id}`, or
`DELETE /documents/{id}` where possessing an identifier could be enough to
reach another user's or tenant's data. Verify ownership, tenant, permission, or
resource policy where required. Client-side filtering is not authorization.

## Authentication Configuration

When Bearer/OIDC authentication is used, check the token-validation
requirement in `security.md` § Authentication and Authorization. Do not require
manually setting every `TokenValidationParameters` property when the
provider's authority/metadata configuration already establishes secure
validation, and do not impose an arbitrary universal `ClockSkew` value. Flag
intentionally disabled validation that weakens the authentication contract
without a valid reason.

## Passwords and Accounts

When the application owns local accounts, review password hashing, password
reset behavior, lockout/brute-force controls where appropriate,
account-enumeration behavior, and credential storage. Do not recommend custom
password hashing.

## Frontend

Verify that sensitive operations are protected by the backend rather than only
by route guards or hidden controls (`security.md` § Authentication and
Authorization).

# Layer 5: Browser and HTTP/API Security

OWASP: `A01 Broken Access Control`, `A02 Security Misconfiguration`

## CORS

CORS is a browser-origin policy, not an authorization mechanism. Check whether
configured origins match the actual browser-client model: unnecessarily broad
trusted origins, credentialed requests from untrusted origins, environment
origins accidentally exposed in Production. `AllowAnyOrigin()` can be valid for
a genuinely public non-credentialed API; credentialed cross-origin access
requires restricted origins.

## CSRF

When browser credentials are sent automatically (especially cookies), review
CSRF protection for state-changing operations. Bearer tokens attached
explicitly through the `Authorization` header have different CSRF
characteristics.

## TLS

Review disabled certificate validation, accept-all certificate callbacks, and
plain HTTP for sensitive external communication. Account for TLS termination at
reverse proxies, ingress, gateways, or hosting platforms; absence of HTTPS
redirection in application code is not automatically a vulnerability.

## File Uploads

When uploads exist, inspect size limits, storage path safety, file-name
handling, content/type assumptions (`security.md` § Failure Handling),
execution or public-serving risks, and authorization.

## Rate Limiting

Consider rate limiting where abuse could realistically matter — login and
password reset, expensive anonymous endpoints, resource-intensive operations.
Do not require it on every endpoint; `429` semantics are in the `http-api`
skill.

# Layer 6: Sensitive Data, Logging, and Error Exposure

OWASP: `A04 Cryptographic Failures`, `A09 Security Logging & Alerting Failures`

## Logging

Check logs against `security.md` § Logging and Sensitive Data. Review PII
according to project requirements, and do not consider Debug/Trace level a
security boundary. Review duplicate or missing security-relevant logging in
context; do not demand logs for every successful request.

## Error Responses

Review public errors for stack traces, SQL, connection strings, internal
filesystem paths, secret values, and internal exception details
(`error-handling.md` § HTTP Error Contracts).

## Response Data

Look for database/domain entities returned directly, password hashes, internal
security fields, unnecessary personal information, and secret metadata. Prefer
explicit response contracts where needed; inspect the actual serialized fields
rather than assuming a returned entity is vulnerable.

## Data at Rest

Choose protection by requirement: passwords → one-way password hashing;
verification-only tokens → often hashing rather than reversible encryption;
retrievable application secrets → protected/encrypted storage;
database/storage encryption → platform or database mechanism when suitable;
temporary application payloads → ASP.NET Core Data Protection may be suitable.

# Layer 7: Exceptional Conditions and Failure Handling

OWASP: `A06:2025 Insecure Design`, `A10:2025 Mishandling of Exceptional Conditions`

## Fail-Open Behavior

Investigate code that catches an exception and then lets a privileged operation
continue — authorization service failed → allow; token validation failed →
continue as anonymous but perform a privileged action; permission lookup failed
→ permitted. Compare with `security.md` § Failure Handling.

## Swallowed Exceptions

Review empty `catch (Exception) { }` blocks and broad catches that continue
without a deliberate fallback. Not every swallowed exception is a
vulnerability, but security-relevant failures must not silently become success.

## Retry and Idempotency

Review retries of state-changing operations: a lost response followed by a
retry can duplicate effects (`performance.md` § Outbound Calls). Caller
cancellation is not a transient failure.

## Timeouts and Resource Exhaustion

Review external operations or public inputs that can consume unbounded time,
memory, database rows, file size, request body, retry attempts, or parallel
work. A theoretical lack of a limit is not automatically High severity;
evaluate whether an attacker can exploit it.

## Startup and Configuration Failure

Review security-sensitive startup configuration for dangerous fallback —
invalid auth configuration → authentication silently disabled; missing
encryption key → plaintext mode; failed authorization provider → allow-all.
Compare with `security.md` § Failure Handling.

## Unexpected Error Exposure

Confirm unexpected exceptions follow the centralized error-handling policy and
do not reveal sensitive information.

# Cross-Cutting Design Review

Static checks do not fully cover insecure design, tenant isolation, business
workflow abuse, privilege escalation through legitimate operations,
financial/idempotency abuse, or multi-step authorization problems. Identify
meaningful security-sensitive workflows as candidates for threat modeling or
dedicated manual review rather than claiming the static scan proves them secure.

# Severity Guidance

Do not map pattern → fixed severity, CVSS → application severity, or OWASP
category → severity mechanically. Examples:

```text
real production private key committed publicly         → potentially Critical
raw SQL string containing only developer-controlled text → not SQL injection
missing [Authorize] while a secure fallback policy exists → not a finding
PII logged in a restricted internal diagnostic environment → contextual, not automatically High
```

# Report Format

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
