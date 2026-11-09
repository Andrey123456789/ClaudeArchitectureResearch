> Private reference of the security-scan workflow. Owns: per-layer investigation prompts and examples · Scope: common · Loads: read by security-scan for the layers in scope · Depends on: .claude/skills/security-scan/SKILL.md

# Security Scan — Layer Reference

Investigation prompts, not automatic vulnerability declarations. The security
invariants these prompts probe are owned by `.claude/rules/security.md`.

# Layer 1: Dependencies and Supply Chain

OWASP: A03:2025 Software Supply Chain Failures.

## .NET

When supported by the installed SDK:

```bash
dotnet package list --vulnerable --include-transitive
```

Review vulnerable direct and transitive dependencies, advisory severity,
whether the vulnerable component is actually used, whether a patched compatible
version exists, and unexpected or untrusted NuGet sources. Do not upgrade
packages during a scan unless asked, and do not rate the application finding
solely from CVSS: consider reachability and exposure.

## Angular / npm

When an npm frontend exists, inspect `npm audit`. Distinguish production from
development/build dependencies and direct from transitive packages. A
development-only vulnerability can still matter to the supply chain, but its
runtime impact differs from a browser-shipped dependency. Review lockfiles when
package integrity or unexpected dependency changes are relevant.

# Layer 2: Secrets and Configuration

OWASP: A02:2025 Security Misconfiguration, A04:2025 Cryptographic Failures.

Search source-controlled files for real credentials and secret material:
`.cs`, `.ts`, `.json`, `.yml`, `.yaml`, `.xml`, `.config`, `.env*`, Dockerfiles,
Compose files, CI workflow files, scripts.

High-confidence indicators: private keys, real access/refresh tokens, cloud
access keys, database passwords, API secrets, service-account credentials,
production connection strings containing credentials.

Indicators requiring context: `ApiKey = "..."`, `Secret = "..."`,
`Token = "..."`, `Password = "..."`, long opaque strings, connection strings,
certificate material.

Do not automatically ignore `appsettings.Development.json`: a real committed
secret remains a secret regardless of the filename. Obviously fake values such
as `changeme`, `example-only`, `test-password`, or `not-a-real-key` may be
ignored or reported as Info when context makes them clearly non-sensitive.
`UserSecretsId` itself is not a secret.

Preferred pattern:

```csharp
var connectionString =
    builder.Configuration.GetConnectionString("Default");
```

with the real secret supplied through the project's chosen local or deployment
secret mechanism.

Also review production debug/development flags, certificate-validation bypass,
insecure URLs carrying credentials, overly verbose production error
configuration, and accidentally committed `.env` files.

# Layer 3: Injection and Dangerous Code Patterns

OWASP: A04 Cryptographic Failures, A05 Injection, A08 Software or Data
Integrity Failures.

## SQL Injection

Look for SQL constructed from untrusted input:

```csharp
var sql =
    $"SELECT * FROM Orders WHERE Name = '{search}'";
```

or interpolated/concatenated data passed to APIs that do not parameterize it.
Safe alternatives: EF Core LINQ, parameterized SQL, `FromSqlInterpolated` where
appropriate, ADO.NET/Dapper parameters. Do not report normal EF Core LINQ as SQL
injection merely because user input participates in a predicate.

## Command Injection

Inspect `Process.Start`, shell execution, PowerShell/bash invocation, and
command arguments built from user input. Prefer APIs that separate the
executable from its arguments, and validate or constrain external input when
command execution is genuinely needed.

## Path Traversal

Review user-controlled file names, paths, archive extraction, download paths,
and upload destinations for `../`, absolute-path injection, escaping the
intended root, and unsafe archive extraction. Check that paths are normalized
and verified to stay within the intended storage boundary.

## SSRF

Inspect outbound requests where users can influence the scheme, host, port,
full URL, or redirect destination, especially when the server can reach
internal networks, metadata endpoints, or privileged services. Host and
control-plane influence matters; not every user-supplied query parameter in an
outbound request is SSRF.

## XSS / Unsafe HTML

For Angular, investigate deliberate sanitizer bypasses such as
`bypassSecurityTrustHtml`, `bypassSecurityTrustScript`,
`bypassSecurityTrustResourceUrl`, and direct DOM manipulation with untrusted
content. Ordinary Angular binding benefits from framework escaping and
sanitization and is not automatically XSS. Review deliberate raw HTML handling
in any server-rendered UI as well.

## Unsafe Deserialization

Investigate dangerous polymorphic or type-driven deserialization, for example
`BinaryFormatter` or unsafe Newtonsoft `TypeNameHandling` configurations, and
flag untrusted payloads deserialized into arbitrary runtime types.

## Cryptography

Flag security-sensitive uses of MD5, SHA1, ECB mode, hardcoded encryption keys,
custom password hashing, and home-grown encryption protocols. Do not flag MD5 or
SHA1 used only as a non-security checksum where collision resistance is
irrelevant. Expect passwords to be handled by established password-hashing
facilities such as ASP.NET Core Identity password hashers, not reversible
encryption (`security.md`, Authentication and Authorization).

# Layer 4: Authentication and Access Control

OWASP: A01:2025 Broken Access Control, A07:2025 Authentication Failures.

## Effective Authorization

Determine the effective access policy: fallback/global authorization policy,
controller and action `[Authorize]`, `[AllowAnonymous]`, policy names,
role/claim requirements, resource-based authorization. An endpoint without an
explicit `[Authorize]` is not automatically vulnerable when a secure fallback
policy protects it, and bare `[Authorize]` is not automatically insufficient
when simple authentication is the intended requirement.

## Anonymous Access

Review `[AllowAnonymous]` and other deliberately public surfaces and confirm
that public access is intentional. Do not report every public endpoint as a
vulnerability.

## Resource Authorization / IDOR

Look for operations such as `GET /orders/{id}`, `PUT /users/{id}`, or
`DELETE /documents/{id}` where possessing an identifier could be enough to
access another user's or tenant's data. Verify ownership, tenant, permission, or
resource policy where required; client-side filtering is not authorization.

## Authentication Configuration

When Bearer/OIDC authentication is used, inspect whether the configured
mechanism validates issuer, audience where applicable, signature/signing
authority, and lifetime. Do not require manually setting every
`TokenValidationParameters` property when the provider's authority/metadata
configuration already establishes secure validation, and do not impose an
arbitrary universal `ClockSkew` value. Flag intentionally disabled validation
that weakens the actual authentication contract without a valid reason.

## Passwords and Accounts

When the application owns local accounts, review password hashing, password
reset behavior, lockout/brute-force controls where appropriate,
account-enumeration behavior, and credential storage.

## Angular

Route guards and hidden or disabled buttons are UX mechanisms; verify that
sensitive operations are protected by the backend.

# Layer 5: Browser and HTTP/API Security

OWASP: A01 Broken Access Control, A02 Security Misconfiguration.

## CORS

CORS is a browser-origin policy, not an authorization mechanism. Check whether
the configured origins match the actual browser-client model. Potential
problems: unnecessarily broad trusted origins, credentialed requests from
untrusted origins, environment-specific origins accidentally exposed in
Production. `AllowAnyOrigin()` can be valid for a genuinely public
non-credentialed API, so a wildcard origin alone is not a finding without
considering the intended exposure.

## CSRF

When browser credentials are sent automatically, especially cookies, review
CSRF protection for state-changing operations. Bearer tokens explicitly attached
through the `Authorization` header have different CSRF characteristics. Do not
assume Angular itself provides server-side CSRF protection for every
authentication model.

## TLS

Review disabled certificate validation, accept-all certificate callbacks, and
plain HTTP for sensitive external communication. Account for TLS termination at
reverse proxies, ingress, gateways, or hosting platforms: missing HTTPS
redirection in application code is not automatically a vulnerability when the
hosting topology enforces TLS.

## File Uploads

When uploads exist, inspect size limits, storage path safety, file-name
handling, content/type assumptions (the client-provided MIME type is not
authoritative), execution or public-serving risks, and authorization.

## Rate Limiting

Consider rate limiting where abuse could realistically matter — login and
password reset, expensive anonymous endpoints, resource-intensive operations —
without requiring it on every endpoint. `429` semantics: `http-api` skill.

# Layer 6: Sensitive Data, Logging, and Error Exposure

OWASP: A04 Cryptographic Failures, A09 Security Logging & Alerting Failures.

## Logging

Look for passwords, access/refresh tokens, private keys, authentication
secrets, and full payment credentials in log statements; review PII against
project requirements, preferring technical identifiers. Debug/Trace level is not
a security boundary. Review duplicate or missing security-relevant logging in
context; do not demand logs for every successful request.

## Error Responses

Review public errors for stack traces, SQL, connection strings, internal
filesystem paths, secret values, and internal exception details, and check that
the centralized error-handling policy is used.

## Response Data

Look for database/domain entities returned directly, password hashes, internal
security fields, unnecessary personal information, and secret metadata. Prefer
explicit response contracts where needed; returning a Domain entity is not
automatically vulnerable — inspect the serialized fields.

## Data at Rest

Choose protection by requirement:

```text
password -> one-way password hashing
verification-only token -> often hash rather than reversible encryption
retrievable application secret -> appropriate protected/encrypted storage
database/storage encryption -> platform/database mechanism when suitable
temporary application payload -> ASP.NET Core Data Protection may be suitable
```

# Layer 7: Exceptional Conditions and Failure Handling

OWASP: A06:2025 Insecure Design, A10:2025 Mishandling of Exceptional
Conditions.

## Fail-Open Behavior

Investigate code that catches an exception and then lets a privileged
operation continue:

```text
authorization service failed -> allow
token validation failed -> continue as anonymous but perform privileged action
permission lookup failed -> default to permitted
```

## Swallowed Exceptions

Review empty `catch (Exception) { }` blocks and broad catches that continue
without a deliberate fallback. Not every swallowed exception is a vulnerability;
flag security-relevant failures that silently turn into success (`security.md`,
Failure Behavior).

## Retry and Idempotency

Review retries of state-changing operations: a lost response followed by a
retry can create duplicate effects. Caller cancellation is not a transient
failure. Technique: `httpclient-factory` skill.

## Timeouts and Resource Exhaustion

Review external operations or public inputs that can consume unbounded time,
memory, database rows, file size, request body, retry attempts, or parallel
work. A theoretical missing limit is not automatically High severity; evaluate
whether an attacker can actually exploit it.

## Startup and Configuration Failure

Review security-sensitive startup configuration for dangerous fallback:

```text
invalid auth configuration -> authentication silently disabled
missing encryption key -> plaintext mode
failed authorization provider -> allow-all fallback
```

## Unexpected Error Exposure

Confirm unexpected exceptions follow the centralized error-handling policy and
do not reveal sensitive information.

# Cross-Cutting Design Review

Static pattern checks do not fully cover insecure design, tenant isolation,
business workflow abuse, privilege escalation through legitimate operations,
financial or idempotency abuse, or multi-step authorization problems. When the
application has meaningful security-sensitive workflows, name them as
candidates for threat modeling or dedicated manual review instead of claiming
the static scan proves them secure.

# Severity Examples

Do not map pattern, CVSS, or OWASP category mechanically to severity:

```text
real production private key committed publicly
-> potentially Critical

raw SQL string containing only developer-controlled constant text
-> not SQL injection

missing [Authorize] while secure fallback policy exists
-> not a finding

PII logged in a restricted internal diagnostic environment
-> contextual finding, not automatically High
```

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
