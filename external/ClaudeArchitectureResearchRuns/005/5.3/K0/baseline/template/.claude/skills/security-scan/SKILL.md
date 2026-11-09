---
name: security-scan
description: Use for a security scan or audit, vulnerability/OWASP review, secret scan, auth or CORS review, pre-release security check, or a materially security-sensitive change.
---

> Kind: WF | Scope: common | Owner: security scan procedure — scope, layers, evidence and severity discipline, report | Loading: workflow (model- or user-invoked)

# Security Scan

Security rules the scan checks against: `rules/common/security.md`, `rules/backend/security.md`, `rules/frontend/angular.md` § Browser authentication security, plus the error-handling, hosting and integration standards in `rules/backend/`. Detailed layer prompts: `references/scan-layers.md`.

## Purpose and limits

Perform an evidence-based static review of the repository. It is not a penetration test and cannot prove the application secure; it may miss runtime-only vulnerabilities, infrastructure outside the repository, complex business-logic abuse, sophisticated authorization bypasses, deployment-specific weaknesses and issues that need dynamic exploitation. State that limitation in the report.

## Principles

1. Report concrete security risks, not generic security advice.
2. Evaluate findings in the context of actual exposure and application behavior.
3. Distinguish confirmed findings from items that need verification, and assign severity from exploitability, reachability, impact and application context — never from a suspicious pattern or a raw CVSS score alone.
4. Do not suppress a real secret because it sits in a Development file.
5. Do not require security mechanisms the project does not need.
6. Evaluate effective authorization behavior, including global and fallback policies.
7. Do not make the review depend on a specific MCP server, agent, analyzer, commercial scanner or other external tool; use whatever tooling is available as evidence, not as the sole authority.

## 1. Determine scope

Inspect which surfaces exist — .NET backend, Angular frontend, authentication/authorization, database access, external HTTP integrations, file upload/download, Docker/container configuration, CI/CD, production configuration, logging, caching, background processing — and skip irrelevant checks instead of reporting them as failures.

For a full pre-release or explicitly requested audit, review every applicable layer. For targeted changes, start with the affected layers and expand when the change crosses security boundaries:

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

## 2. Scan the layers

Work through `references/scan-layers.md`:

| # | Layer | Typical OWASP mapping |
|---|---|---|
| 1 | Dependencies and supply chain | A03 |
| 2 | Secrets and configuration | A02, A04 |
| 3 | Injection and dangerous code patterns | A04, A05, A08 |
| 4 | Authentication and access control | A01, A07 |
| 5 | Browser and HTTP/API security | A01, A02 |
| 6 | Sensitive data, logging and error exposure | A04, A09 |
| 7 | Exceptional conditions and failure handling | A06, A10 |

OWASP Top 10:2025 is an awareness taxonomy — A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging & Alerting Failures, A10 Mishandling of Exceptional Conditions. Map a finding only when the category genuinely fits.

When a scanner reports a possible issue: inspect the actual code, decide whether the pattern is reachable and relevant, and report it only with appropriate confidence.

## 3. Rate severity

Consider exploitability, external exposure, required privileges, affected data or capability, blast radius, reliability of exploitation and existing compensating controls. Do not convert advisory CVSS scores directly into application severity without checking that the affected dependency or code path is relevant.

- **Critical** (use sparingly) — immediately exploitable, high-impact: exposed real production credentials, reachable authentication bypass, straightforward remote code execution, exploitable injection with major impact.
- **High** — serious, realistically exploitable, or able to substantially compromise data, authorization or system behavior.
- **Medium** — meaningful weakness needing realistic conditions, limited access or extra steps.
- **Low** — genuine but limited weakness.
- **Info** — useful observation or hardening opportunity, not a demonstrated vulnerability.

### Context and false positives

Not automatically vulnerabilities: an endpoint without `[Authorize]` protected by a secure fallback policy; bare `[Authorize]` when authentication alone is intended; `AllowAnyOrigin()` on a genuinely public, non-credentialed API; MD5/SHA1 as a non-security checksum; no application-level encryption when platform or storage encryption satisfies the requirement; obviously fake test credentials; framework defaults that are secure in the actual hosting configuration.

Not automatically safe: secrets in `appsettings.Development.json`; sensitive values logged only at Debug level; Angular route guards; hidden UI buttons; CORS used as a substitute for authorization.

## 4. Report

Every confirmed finding includes severity, file and location, title, evidence, why it is a risk, likely impact, smallest reasonable remediation and OWASP category when applicable. Label uncertain findings `NEEDS VERIFICATION` instead of presenting them as confirmed, and never invent exploitability the code does not establish.

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

Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED — never PASS for a layer that was not inspected.

## Remediation discipline

Recommend the smallest secure change consistent with the project architecture. Do not recommend a new authentication system unnecessarily, custom cryptography, blanket encryption of all database fields, `[Authorize]` on every action when a global policy already protects them, security libraries merely to satisfy the scan, or disabling functionality because a static scanner cannot understand it.

## Completion

The scan is complete when every applicable layer was inspected, findings carry evidence, uncertain findings are labeled, severity reflects actual risk, limitations are stated and no layer is marked PASS without being checked.
