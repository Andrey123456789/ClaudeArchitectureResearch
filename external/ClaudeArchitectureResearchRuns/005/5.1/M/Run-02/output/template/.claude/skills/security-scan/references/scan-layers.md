> Owner: private reference of the `security-scan` workflow — per-layer investigation prompts and false-positive heuristics | Scope: common | Loads: read by `security-scan` only | Enforced: none

# Security Scan — Layer Reference

Investigation prompts, not automatic vulnerability declarations. The invariants
being checked are owned by `.claude/rules/security.md`; each layer names the
section to compare against.

# Layer 1: Dependencies and Supply Chain

OWASP: `A03:2025 Software Supply Chain Failures`

## .NET

When supported by the installed SDK:

```bash
dotnet package list --vulnerable --include-transitive
```

Review vulnerable direct and transitive dependencies, advisory severity, whether
the vulnerable component is actually used by the affected application, whether a
patched compatible version exists, and unexpected or untrusted NuGet sources.
Rate the finding from reachability and exposure, not CVSS alone. Upgrades go
through the `add-dependency` workflow, not the scan.

## Angular / npm

```bash
npm audit
```

Distinguish production from development/build dependencies and direct from
transitive packages. A development-only vulnerability still matters to the supply
chain but has a different runtime impact than a browser-shipped dependency.
Review lockfiles when package integrity or unexpected dependency changes matter.

# Layer 2: Secrets and Configuration

OWASP: `A02:2025 Security Misconfiguration`, `A04:2025 Cryptographic Failures`
Compare against: `.claude/rules/security.md` § Secrets.

Search source-controlled `.cs`, `.ts`, `.json`, `.yml`, `.yaml`, `.xml`,
`.config`, `.env*`, Dockerfiles, Compose files, CI workflows, and scripts.

High-confidence indicators: private keys, real access/refresh tokens, cloud
access keys, database passwords, API secrets, service-account credentials,
production connection strings with credentials.

Indicators that need context: `ApiKey = "..."`, `Secret = "..."`,
`Token = "..."`, `Password = "..."`, long opaque strings, connection strings,
certificate material.

- Do not skip `appsettings.Development.json`; a real committed secret is a secret
  regardless of the file name.
- Obviously fake values (`changeme`, `example-only`, `test-password`,
  `not-a-real-key`) may be ignored or reported as Info when context makes them
  clearly non-sensitive.
- `UserSecretsId` is not a secret.

Preferred pattern, with the real value supplied by the chosen secret mechanism:

```csharp
var connectionString =
    builder.Configuration.GetConnectionString("Default");
```

Also review production debug/development flags, certificate-validation bypass,
insecure URLs carrying credentials, overly verbose production error
configuration, and accidentally committed `.env` files.

# Layer 3: Injection and Dangerous Code Patterns

OWASP: `A04 Cryptographic Failures`, `A05 Injection`,
`A08 Software or Data Integrity Failures`
Compare against: `.claude/rules/security.md` § SQL and Persistence and
§ Transport and Cryptography.

## SQL Injection

Look for SQL constructed from untrusted input:

```csharp
var sql =
    $"SELECT * FROM Orders WHERE Name = '{search}'";
```

or interpolated/concatenated data passed to APIs that do not parameterize it.
Safe forms: EF Core LINQ, parameterized SQL, `FromSqlInterpolated` where
appropriate, ADO.NET/Dapper parameters. Normal EF Core LINQ with user input in a
predicate is not SQL injection.

## Command Injection

Inspect `Process.Start`, shell execution, PowerShell/bash invocation, and command
arguments built from user input. Prefer APIs that separate executable and
arguments; constrain external input when command execution is genuinely needed.

## Path Traversal

Review user-controlled file names, paths, archive extraction, download paths,
and upload destinations for `../`, absolute-path injection, escapes from the
intended root, and unsafe archive extraction. Paths should be normalized and
verified to stay inside the intended storage boundary.

## SSRF

Inspect outbound requests where users can influence scheme, host, port, full URL,
or redirect destination — especially when the server can reach internal
networks, metadata endpoints, or privileged services. A user-supplied query
parameter in an outbound request is not SSRF by itself; host/control-plane
influence matters.

## XSS / Unsafe HTML

In Angular, investigate deliberate sanitizer bypasses
(`bypassSecurityTrustHtml`, `bypassSecurityTrustScript`,
`bypassSecurityTrustResourceUrl`) and direct DOM manipulation with untrusted
content. Ordinary Angular binding is escaped/sanitized by the framework and is
not automatically XSS. Review deliberate raw HTML handling in any server-rendered
UI too.

## Unsafe Deserialization

Investigate dangerous polymorphic or type-driven deserialization, such as
`BinaryFormatter` or unsafe Newtonsoft `TypeNameHandling` configurations, and any
deserialization of untrusted payloads into arbitrary runtime types.

## Cryptography

Flag security-sensitive use of MD5, SHA1, ECB mode, hardcoded encryption keys,
custom password hashing, or home-grown encryption protocols. MD5/SHA1 as a
non-security checksum, where collision resistance is irrelevant, is not a
finding. Passwords belong in established password hashers (ASP.NET Core
Identity), not reversible encryption.

# Layer 4: Authentication and Access Control

OWASP: `A01:2025 Broken Access Control`, `A07:2025 Authentication Failures`
Compare against: `.claude/rules/security.md` § Authentication and Authorization.

## Effective Authorization

Determine the effective access policy from the fallback/global authorization
policy, controller and action `[Authorize]`, `[AllowAnonymous]`, policy names,
role/claim requirements, and resource-based authorization. An endpoint without
explicit `[Authorize]` is not automatically vulnerable under a secure fallback
policy, and bare `[Authorize]` is not automatically insufficient when simple
authentication is the intended requirement.

## Anonymous Access

Review `[AllowAnonymous]` and other deliberately public surfaces and confirm the
public access is intentional; a public endpoint is not a vulnerability by itself.

## Resource Authorization / IDOR

Look for operations such as `GET /orders/{id}`, `PUT /users/{id}`,
`DELETE /documents/{id}` where possessing an identifier could be enough to reach
another user's or tenant's data. Verify ownership, tenant, permission, or
resource policy where required; client-side filtering is not authorization.

## Authentication Configuration

For Bearer/OIDC, check whether the configured mechanism validates issuer,
audience where applicable, signature/signing authority, and lifetime. Do not
require manually setting every `TokenValidationParameters` property when the
framework or provider already establishes secure validation through
authority/metadata configuration, and do not impose an arbitrary universal
`ClockSkew`. Flag validation that was intentionally disabled without a valid
reason.

## Passwords and Accounts

When the application owns local accounts, review password hashing, password
reset, lockout/brute-force controls where appropriate, account-enumeration
behavior, and credential storage.

## Angular

Route guards and hidden or disabled buttons are UX; verify that sensitive
operations are protected by the backend.

# Layer 5: Browser and HTTP/API Security

OWASP: `A01 Broken Access Control`, `A02 Security Misconfiguration`
Compare against: `.claude/rules/security.md` § CORS, § Browser Credentials,
§ Transport and Cryptography, § Input Boundaries.

## CORS

CORS is a browser-origin policy, not an authorization mechanism. Check whether
the configured origins match the actual browser-client model. Problems include
unnecessarily broad trusted origins, credentialed requests from untrusted
origins, and environment-specific origins exposed in Production. A wildcard
origin alone is not a finding without considering the API's intended exposure.

## CSRF

When browser credentials — especially cookies — are sent automatically, review
CSRF protection for state-changing operations. Bearer tokens attached explicitly
through the `Authorization` header have different CSRF characteristics.

## TLS

Review disabled certificate validation, accept-all certificate callbacks, and
plain HTTP for sensitive external communication. Account for TLS termination at
proxies, ingress, gateways, or platforms; missing HTTPS redirection in
application code is not automatically a vulnerability.

## File Uploads

When uploads exist, inspect size limits, storage path safety, file-name handling,
content/type assumptions, execution or public-serving risks, and authorization —
in particular whether the client-provided MIME type is treated as authoritative.

## Rate Limiting

Consider rate limiting where abuse could realistically matter — login, password
reset, expensive anonymous endpoints, resource-intensive operations — not on
every endpoint. `429` semantics: `http-api` skill.

# Layer 6: Sensitive Data, Logging, and Error Exposure

OWASP: `A04 Cryptographic Failures`, `A09 Security Logging & Alerting Failures`
Compare against: `.claude/rules/security.md` § Logging and Sensitive Data,
`.claude/rules/error-handling.md` § Error Contracts.

## Logging

Search log statements for passwords, tokens, private keys, authentication
secrets, full payment credentials, and PII beyond what project requirements
permit; technical identifiers are preferable to identity data. Debug/Trace level
is not a security boundary. Review duplicate or missing security-relevant logging
in context; do not demand logs for every successful request.

## Error Responses

Review public errors for stack traces, SQL, connection strings, internal
filesystem paths, secret values, and internal exception details.

## Response Data

Look for database/domain entities returned directly, password hashes, internal
security fields, unnecessary personal information, and secret metadata. Inspect
the actual serialized fields; returning a Domain entity is not automatically
vulnerable.

## Data at Rest

Match protection to the requirement:

```text
password                         -> one-way password hashing
verification-only token          -> often hash rather than reversible encryption
retrievable application secret   -> appropriate protected/encrypted storage
database/storage encryption      -> platform/database mechanism when suitable
temporary application payload    -> ASP.NET Core Data Protection may be suitable
```

# Layer 7: Exceptional Conditions and Failure Handling

OWASP: `A06:2025 Insecure Design`, `A10:2025 Mishandling of Exceptional Conditions`
Compare against: `.claude/rules/security.md` § Failure Behavior,
`.claude/rules/error-handling.md` § External Dependency Failures.

## Fail-Open Behavior

Investigate code that catches an exception and then lets a privileged operation
continue, for example:

```text
authorization service failed -> allow
token validation failed -> continue as anonymous but perform privileged action
permission lookup failed -> default to permitted
```

## Swallowed Exceptions

Review empty `catch (Exception) { }` blocks and broad catches that continue
without a deliberate fallback. Not every swallowed exception is a vulnerability,
but a security-relevant failure that silently becomes success is.

## Retry and Idempotency

Review retries of state-changing operations: a lost response followed by a retry
can duplicate effects. Caller cancellation treated as a transient failure is a
finding.

## Timeouts and Resource Exhaustion

Review external operations or public inputs that can consume unbounded time,
memory, database rows, file size, request body, retry attempts, or parallel
work. A theoretical missing limit is not automatically High; evaluate whether an
attacker can actually exploit it.

## Startup and Configuration Failure

Look for dangerous fallbacks when a required control cannot initialize:

```text
invalid auth configuration -> authentication silently disabled
missing encryption key -> plaintext mode
failed authorization provider -> allow-all fallback
```

## Unexpected Error Exposure

Confirm unexpected exceptions go through centralized handling and do not reveal
sensitive information.

# Cross-Cutting Design Review

Static pattern checks do not cover A06 Insecure Design, tenant isolation,
business workflow abuse, privilege escalation through legitimate operations,
financial/idempotency abuse, or multi-step authorization problems. When the
application has meaningful security-sensitive workflows, list them as candidates
for threat modeling or dedicated manual review rather than claiming the static
scan proves them secure.

# Severity Examples

Do not map pattern → fixed severity, CVSS → application severity, or OWASP
category → severity mechanically.

```text
real production private key committed publicly
→ potentially Critical

raw SQL string containing only developer-controlled constant text
→ not SQL injection

missing [Authorize] while secure fallback policy exists
→ not a finding

PII logged in a restricted internal diagnostic environment
→ contextual finding, not automatically High
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
