---
name: security-scan
description: >
  Use for a security scan or audit, OWASP or vulnerability review, secret scan,
  auth or CORS review, or pre-release security check of the .NET/Angular
  repository.
---

> Owns: security review procedure, evidence and severity discipline, scan report format | Scope: common | Loads: workflow (routed from CLAUDE.md and code-review); private reference references/scan-layers.md

# Security Scan

## Purpose

Perform an evidence-based static security review of the repository. This is
not a penetration test: static review cannot prove the application is secure and
may miss runtime-only vulnerabilities, infrastructure configuration outside the
repository, complex business-logic abuse, sophisticated authorization bypasses,
deployment-specific weaknesses, and vulnerabilities that need dynamic
exploitation. State that limitation in the report.

The security invariants themselves live in `.claude/rules/security.md`; read it
before scanning.

## Principles

1. Report concrete security risks, not generic security advice.
2. Evaluate findings in the context of actual exposure and application
   behavior.
3. Distinguish confirmed findings from items that need verification.
4. Assign severity from exploitability, reachability, impact, and application
   context — never from a suspicious pattern or a raw CVSS score alone.
5. Do not suppress a real secret merely because it appears in a Development
   file.
6. Do not require security mechanisms the project does not need.
7. Evaluate effective authorization behavior, including global/fallback
   policies.
8. Use the project's security, authentication, configuration, logging,
   error-handling, HTTP, and resilience guidance.
9. The scan must work without any specific MCP server, agent, analyzer,
   commercial scanner, or other external tool: use available tooling as
   evidence, never as the sole authority.

## OWASP Mapping

Use OWASP Top 10:2025 as an awareness taxonomy when it genuinely fits:

```text
A01 Broken Access Control
A02 Security Misconfiguration
A03 Software Supply Chain Failures
A04 Cryptographic Failures
A05 Injection
A06 Insecure Design
A07 Authentication Failures
A08 Software or Data Integrity Failures
A09 Security Logging & Alerting Failures
A10 Mishandling of Exceptional Conditions
```

Not every issue needs a category; do not force an inaccurate mapping.

## Scan Scope

Inspect the repository first and determine which surfaces exist: .NET backend,
Angular frontend, authentication/authorization, database access, external HTTP
integrations, file upload/download, Docker/container configuration, CI/CD,
production configuration, logging, caching, background processing. Skip
irrelevant checks rather than reporting them as failures.

## Security Layers

Read `references/scan-layers.md` for the detailed investigation prompts of each
layer:

| # | Layer | Typical OWASP mapping |
|---|---|---|
| 1 | Dependencies and supply chain | A03 |
| 2 | Secrets and configuration | A02, A04 |
| 3 | Injection and dangerous code patterns | A04, A05, A08 |
| 4 | Authentication and access control | A01, A07 |
| 5 | Browser and HTTP/API security | A01, A02 |
| 6 | Sensitive data, logging, and error exposure | A04, A09 |
| 7 | Exceptional conditions and failure handling | A06, A10 |

## Selecting Scope

For a full pre-release or explicitly requested audit, review all applicable
layers. For targeted changes, start with the affected layers and expand when the
change crosses security boundaries:

| Change | Priority areas |
|---|---|
| Dependency update | Dependencies / supply chain |
| Authentication change | Authentication / access control |
| New Controller endpoint | Access control, input handling, HTTP security |
| Database/query change | Injection, access control, sensitive data |
| Configuration change | Secrets / configuration |
| Logging change | Sensitive data / logging |
| HttpClient integration | Configuration, SSRF/input handling, failure handling |
| File upload | Input handling, path safety, resource limits |
| Angular auth/UI change | Browser security + server authorization assumptions |

## Tooling

Use repository search, compiler/tooling output, package-audit commands, and
static analyzers when available. When a scanner reports a possible issue:

1. inspect the actual code;
2. determine whether the pattern is reachable and relevant;
3. report it only with appropriate confidence.

## Severity

Rate severity from actual risk: exploitability, external exposure, required
privileges, affected data or capability, blast radius, reliability of
exploitation, and existing compensating controls.

- **Critical** — use sparingly for immediately exploitable, high-impact
  conditions: exposed real production credentials, reachable authentication
  bypass, straightforward remote code execution, exploitable injection with
  major data/system impact.
- **High** — a serious vulnerability that is realistically exploitable or can
  substantially compromise data, authorization, or system behavior.
- **Medium** — a meaningful weakness requiring realistic conditions, limited
  access, or additional exploitation steps.
- **Low** — a genuine but limited weakness with low practical impact.
- **Info** — a useful observation or hardening opportunity that is not itself a
  demonstrated vulnerability.

Do not convert advisory CVSS scores directly into application severity without
considering whether the affected dependency or code path is relevant.

## False Positives and Context

Do not automatically report as vulnerabilities: an endpoint without
`[Authorize]` protected by a secure fallback/global policy; bare `[Authorize]`
when authentication alone is the intended policy; `AllowAnyOrigin()` for a
genuinely public non-credentialed API; MD5/SHA1 used as a non-security checksum;
data not encrypted at application level when platform/storage encryption
satisfies the requirement; obviously fake test credentials; framework defaults
that are secure in the actual hosting configuration.

Conversely, do not automatically treat as safe: secrets in
`appsettings.Development.json`, sensitive values logged only at Debug level,
client-side Angular route guards, hidden UI buttons, or CORS configuration used
as a substitute for authorization.

## Cross-Skill Guidance

For deeper guidance use `.claude/rules/security.md` and the `authentication`,
`configuration`, `logging`, `aspnet-error-handling`, `http-api`,
`httpclient-factory`, `ef-core`, and `angular` skills. Do not duplicate their
implementation guidance in the scan.

## Reporting

Every confirmed finding includes: severity, file and location, title,
evidence, why it is a security risk, likely impact, the smallest reasonable
remediation, and the OWASP category when applicable. Label uncertain findings
`NEEDS VERIFICATION` instead of presenting them as confirmed.

## Report Shape

```markdown
# Security Scan Report

Scope:
- ...

Limitations:
Static analysis only. This does not replace penetration testing,
dynamic testing, threat modeling, or infrastructure review.

## Summary

| Severity | Count |
|---|---:|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |
| Info | 0 |

## Findings

### [HIGH] File:Line — Finding title

OWASP: A01:2025 Broken Access Control

Evidence:
...

Impact:
...

Remediation:
...

## Layer Results

| Layer | Status | Findings |
|---|---|---:|
| Dependencies and supply chain | PASS | 0 |
| Secrets and configuration | PASS | 0 |
| Injection and dangerous patterns | PASS | 0 |
| Authentication and access control | PASS | 0 |
| Browser and HTTP/API security | PASS | 0 |
| Sensitive data/logging/error exposure | PASS | 0 |
| Exceptional conditions | PASS | 0 |
```

Use `PASS`, `FINDINGS`, `NOT APPLICABLE`, or `NOT CHECKED`; never mark an
uninspected layer as passed.

## Remediation Discipline

Prefer the smallest secure change consistent with the project architecture. Do
not recommend a new authentication system unnecessarily, custom cryptography,
blanket encryption of all database fields, `[Authorize]` on every action when a
global policy already provides the protection, security libraries merely to
satisfy the scan, or disabling functionality solely because a static scanner
cannot understand it.

## Completion

A security scan is complete when all applicable layers were inspected, findings
have evidence, uncertain findings are labeled, severity reflects actual risk,
limitations are stated, and no layer is marked PASS without being checked.
