---
name: security-scan
description: Use when asked for a security scan, security audit, vulnerability review, OWASP review, secret scan, auth review, CORS review, pre-release security check or penetration-test preparation of the .NET backend and frontend.
---
Kind: WF | Scope: common | Capability: — | Loading: on invocation (routed from CLAUDE.md and code-review)

# Security Scan

Evidence-based static security review of the repository. Security standards: `.claude/rules/common/security.md`, `.claude/rules/backend/security.md`, `.claude/rules/frontend/frontend.md` (Browser security). Detailed layer checks: `references/scan-layers.md` (read it during the scan).

This is not a penetration test. Static review cannot prove that the application is secure and may miss runtime-only vulnerabilities, infrastructure configuration outside the repository, complex business-logic abuse, sophisticated authorization bypasses, deployment-specific weaknesses and vulnerabilities that require dynamic exploitation. State this limitation in the report.

## Principles

- Report concrete security risks, not generic security advice, evaluated in the context of actual exposure and application behavior.
- Distinguish confirmed findings from items that need verification, and assign severity from exploitability, reachability, impact and application context, not from suspicious patterns or raw CVSS scores alone.
- Do not suppress a real secret because it appears in a Development file.
- Do not require security mechanisms the project does not need. Evaluate effective authorization, including global and fallback policies.
- Do not require a specific MCP server, agent, analyzer, commercial scanner or other external tool for the review to work. Use available repository search, compiler output, package-audit commands and analyzers as evidence, not as the sole authority. When a tool reports a possible issue, inspect the code, decide whether it is reachable and relevant, and report it only with appropriate confidence.

## 1. Determine the scope

Inspect which surfaces exist: .NET backend, frontend, authentication and authorization, database access, external HTTP integrations, file upload or download, container configuration, CI/CD, production configuration, logging, caching, background processing. Skip irrelevant checks instead of reporting them as failures.

For a full or pre-release audit, review all applicable layers. For a targeted change, start with the affected layers and expand when the change crosses security boundaries:

| Change | Priority areas |
|---|---|
| Dependency update | Dependencies and supply chain |
| Authentication change | Authentication and access control |
| New controller endpoint | Access control, input handling, HTTP security |
| Database or query change | Injection, access control, sensitive data |
| Configuration change | Secrets and configuration |
| Logging change | Sensitive data and logging |
| `HttpClient` integration | Configuration, SSRF and input handling, failure handling |
| File upload | Input handling, path safety, resource limits |
| Frontend auth or UI change | Browser security and server authorization assumptions |

## 2. Review the layers

Use `references/scan-layers.md`:

| # | Layer | Typical OWASP Top 10:2025 mapping |
|---|---|---|
| 1 | Dependencies and supply chain | A03 |
| 2 | Secrets and configuration | A02, A04 |
| 3 | Injection and dangerous code patterns | A04, A05, A08 |
| 4 | Authentication and access control | A01, A07 |
| 5 | Browser and HTTP/API security | A01, A02 |
| 6 | Sensitive data, logging and error exposure | A04, A09 |
| 7 | Exceptional conditions and failure handling | A06, A10 |

Implementation-specific checks come from the selected modules' workflow facets (decision register → Capability selection): the persistence facet for raw-query APIs and the frontend facet for browser-side sanitization bypasses. Deeper technique: `authentication`, `configuration`, `logging`, `aspnet-error-handling`, `http-api`, `httpclient-factory` and the persistence and frontend knowledge facets; do not duplicate their guidance here.

Use OWASP Top 10:2025 (A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging & Alerting Failures, A10 Mishandling of Exceptional Conditions) as an awareness taxonomy only where it genuinely fits; do not force a mapping.

## 3. Rate severity

Consider exploitability, external exposure, required privileges, affected data or capability, blast radius, reliability of exploitation and compensating controls.

- **Critical** (use sparingly): exposed real production credentials, a reachable authentication bypass, straightforward remote code execution, exploitable injection with major data or system impact.
- **High**: a serious, realistically exploitable vulnerability that can substantially compromise data, authorization or system behavior.
- **Medium**: a meaningful weakness that requires realistic conditions, limited access or additional exploitation steps.
- **Low**: a genuine but limited weakness with low practical impact.
- **Info**: a useful observation or hardening opportunity that is not a demonstrated vulnerability.

Do not convert advisory CVSS scores into application severity without considering whether the affected dependency or code path is relevant.

## 4. Context and false positives

Not automatically vulnerabilities: an endpoint without `[Authorize]` under a secure fallback policy; bare `[Authorize]` when authentication alone is the intended policy; `AllowAnyOrigin()` for a genuinely public, non-credentialed API; MD5 or SHA1 as non-security checksums; data without application-level encryption when platform or storage encryption satisfies the requirement; obviously fake test credentials; framework defaults that are secure in the actual hosting configuration.

Not automatically safe: secrets in `appsettings.Development.json`; sensitive values logged only at Debug level; client-side route guards; hidden UI buttons; CORS used as a substitute for authorization.

## 5. Report

Every confirmed finding includes severity, file and location, title, evidence, why it is a risk, likely impact, the smallest reasonable remediation, and the OWASP category when applicable. Label uncertain findings `NEEDS VERIFICATION`.

```markdown
# Security Scan Report

Scope:
- ...

Limitations:
Static analysis only. This does not replace penetration testing, dynamic testing, threat modeling or infrastructure review.

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

Evidence: ...
Impact: ...
Remediation: ...

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

Use PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED; never mark a layer PASS without checking it.

## Remediation discipline

Prefer the smallest secure change consistent with the project architecture. Do not recommend a new authentication system without need, custom cryptography, blanket encryption of all database fields, `[Authorize]` on every action when a global policy already protects them, security libraries merely to satisfy the scan, or disabling functionality because a static scanner cannot understand it.

## Completion

The scan is complete when all applicable layers were inspected, findings have evidence, uncertain findings are labeled, severity reflects actual risk, limitations are stated, and no layer is marked PASS without being checked.
