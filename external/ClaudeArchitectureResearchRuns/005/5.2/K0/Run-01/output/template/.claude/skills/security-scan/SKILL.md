---
name: security-scan
description: Use for a security scan or audit, vulnerability or OWASP review, secret scan, authentication/authorization or CORS review, pre-release security check, or penetration-test preparation of the .NET/Angular repository.
---
<!-- Kind: WF | Scope: common | Owns: static security review procedure, evidence and severity discipline, tool independence, report shape | Loads: workflow invocation -->
# Security Scan

## Purpose

Perform an evidence-based static security review of the repository. This is not a penetration test: static review finds many code, dependency, configuration and access-control problems but cannot prove the application secure and may miss runtime-only vulnerabilities, infrastructure configured outside the repository, complex business-logic abuse, sophisticated authorization bypasses, deployment-specific weaknesses and issues that need dynamic exploitation. State that limitation in the report.

## Principles

- Findings **must** distinguish confirmed issues from items needing verification, and severity **must** come from exploitability, reachability, impact and application context — not from a suspicious pattern or a raw CVSS score alone.
- The review **must not** depend on a specific MCP server, agent, analyzer, commercial scanner or other external tool; available tooling is evidence, not the sole authority.
- Report concrete risks, not generic advice; evaluate effective authorization, including global and fallback policies; do not suppress a real secret because it sits in a Development file; do not require security mechanisms the project does not need.

## Standards to Read First

The security invariants checked here are owned by `rules/common/security.md`, `rules/backend/security.md`, `rules/frontend/security.md`, `rules/backend/error-handling.md` (error exposure) and `rules/backend/operations.md` (health responses). Read them before scanning. Deeper technique: `authentication`, `configuration`, `logging`, `aspnet-error-handling`, `http-api`, `httpclient-factory`, `ef-core`, `angular` skills — do not duplicate their guidance in the report.

## OWASP Mapping

Use OWASP Top 10:2025 as an awareness taxonomy when it genuinely fits; do not force an inaccurate mapping.

    A01 Broken Access Control            A06 Insecure Design
    A02 Security Misconfiguration        A07 Authentication Failures
    A03 Software Supply Chain Failures   A08 Software or Data Integrity Failures
    A04 Cryptographic Failures           A09 Security Logging & Alerting Failures
    A05 Injection                        A10 Mishandling of Exceptional Conditions

## 1. Determine Scan Scope

Inspect which surfaces exist: .NET backend, Angular frontend, authentication/authorization, database access, external HTTP integrations, file upload/download, Docker/container configuration, CI/CD, production configuration, logging, caching, background processing. Skip irrelevant checks rather than reporting them as failures.

For a full pre-release or explicitly requested audit, review all applicable layers. For targeted changes, start with the affected layers and expand when the change crosses security boundaries:

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

## 2. Inspect the Layers

Work through the applicable layers using `references/scan-layers.md`:

| # | Layer | Typical OWASP mapping |
|---|---|---|
| 1 | Dependencies and supply chain | A03 |
| 2 | Secrets and configuration | A02, A04 |
| 3 | Injection and dangerous code patterns | A04, A05, A08 |
| 4 | Authentication and access control | A01, A07 |
| 5 | Browser and HTTP/API security | A01, A02 |
| 6 | Sensitive data, logging and error exposure | A04, A09 |
| 7 | Exceptional conditions and failure handling | A06, A10 |

## 3. Use Tooling as Evidence

Use repository search, compiler/tooling output, package-audit commands and static analyzers when available. When a tool reports a possible issue: inspect the actual code, determine whether the pattern is reachable and relevant, and report it only with appropriate confidence.

## 4. Rate Severity

Consider exploitability, external exposure, required privileges, affected data or capability, blast radius, reliability of exploitation and compensating controls.

- **Critical** — use sparingly: exposed real production credentials, reachable authentication bypass, straightforward remote code execution, exploitable injection with major data/system impact.
- **High** — realistically exploitable, or able to substantially compromise data, authorization or system behavior.
- **Medium** — meaningful weakness that needs realistic conditions, limited access or additional steps.
- **Low** — genuine but limited weakness with low practical impact.
- **Info** — useful observation or hardening opportunity, not a demonstrated vulnerability.

Do not convert advisory CVSS scores into application severity without considering whether the affected dependency or code path is relevant.

## 5. Weigh Context and False Positives

Not automatically vulnerabilities: an endpoint without `[Authorize]` under a secure fallback/global policy; bare `[Authorize]` when authentication alone is the intended policy; `AllowAnyOrigin()` for a genuinely public non-credentialed API; MD5/SHA1 as a non-security checksum; data without application-level encryption when platform/storage encryption satisfies the requirement; obviously fake test credentials; framework defaults that are secure in the actual hosting configuration.

Not automatically safe: secrets in `appsettings.Development.json`; sensitive values logged only at Debug level; client-side Angular route guards; hidden UI buttons; CORS used as a substitute for authorization.

## 6. Report

Every confirmed finding includes severity, file and location, title, evidence, why it is a security risk, likely impact, smallest reasonable remediation, and the OWASP category when applicable. Label uncertain findings `NEEDS VERIFICATION` instead of presenting them as confirmed.

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

Layer status is `PASS`, `FINDINGS`, `NOT APPLICABLE` or `NOT CHECKED` — never mark an uninspected layer PASS.

## Remediation Discipline

Prefer the smallest secure change consistent with the project architecture. Do not recommend a new authentication system unnecessarily, custom cryptography, blanket encryption of all database fields, `[Authorize]` on every action when a global policy already protects them, security libraries merely to satisfy the scan, or disabling functionality because a static scanner cannot understand it. Do not upgrade packages during a scan unless asked.

## Completion

The scan is complete when all applicable layers were inspected, findings have evidence, uncertain findings are labeled, severity reflects actual risk, limitations are stated, and no layer is marked PASS without being checked.
