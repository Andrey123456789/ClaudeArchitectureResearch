---
name: security-scan
description: >
  Evidence-based static security review of the .NET backend and frontend:
  dependencies, secrets/configuration, injection, authentication/authorization,
  browser/API security, sensitive data and logging, exceptional conditions,
  OWASP Top 10:2025 mapping. Use for security scans, audits, OWASP, secret,
  auth, or CORS reviews, and pre-release security checks.
---

> Kind: WF | Scope: common | Capability: — | Loading: on-demand workflow

# Security Scan

## Purpose and limits

Perform an evidence-based static security review. This is not a penetration test: static review cannot prove the application secure and may miss runtime-only vulnerabilities, infrastructure outside the repository, complex business-logic abuse, sophisticated authorization bypasses, deployment-specific weaknesses, and vulnerabilities that need dynamic exploitation. State that limitation in the report.

## Principles

1. Report concrete risks, not generic security advice.
2. Evaluate findings in the context of actual exposure and application behavior.
3. Every finding must distinguish confirmed evidence from items needing verification, and severity must come from exploitability, reachability, impact, and application context — never from a suspicious pattern or a raw CVSS score alone.
4. Do not suppress a real secret because it sits in a Development file.
5. Do not require security mechanisms the project does not need.
6. Evaluate effective authorization behavior, including global/fallback policies.
7. Apply the project's standards and knowledge (below) instead of duplicating their guidance.
8. The review must not depend on a specific MCP server, agent, analyzer, commercial scanner, or other external tool; available tooling is evidence, not the sole authority.

## Scope

Inspect which surfaces exist — .NET backend, frontend, authentication/authorization, database access, external HTTP integrations, file upload/download, container configuration, CI/CD, production configuration, logging, caching, background processing — and skip irrelevant checks instead of reporting them as failures. A full pre-release or explicitly requested audit reviews all applicable layers; a targeted change focuses on the affected layers and expands when it crosses security boundaries:

| Change | Priority layers |
|---|---|
| Dependency update | 1 |
| Authentication change | 4 |
| New controller endpoint | 4, 5, input handling |
| Database/query change | 3, 4, 6 |
| Configuration change | 2 |
| Logging change | 6 |
| HttpClient integration | 2, 3 (SSRF), 7 |
| File upload | 3 (path safety), 5, resource limits |
| Frontend auth/UI change | 5 + server authorization assumptions |

## Layers

Detailed investigation prompts: `references/scan-layers.md`.

| # | Layer | Typical OWASP Top 10:2025 mapping |
|---|---|---|
| 1 | Dependencies and supply chain | A03 |
| 2 | Secrets and configuration | A02, A04 |
| 3 | Injection and dangerous code patterns | A04, A05, A08 |
| 4 | Authentication and access control | A01, A07 |
| 5 | Browser and HTTP/API security | A01, A02 |
| 6 | Sensitive data, logging, and error exposure | A04, A09 |
| 7 | Exceptional conditions and failure handling | A06, A10 |

OWASP categories: A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging & Alerting Failures, A10 Mishandling of Exceptional Conditions. Map only when a category genuinely fits.

Read the governing standards for the surfaces in scope (`.claude/rules/common/security.md`, `.claude/rules/backend/security.md`, `.claude/rules/frontend/security.md`, `.claude/rules/backend/api.md`) and use knowledge where depth is needed: `authentication`, `configuration`, `logging`, `aspnet-error-handling`, `http-api`, `httpclient-factory`, and the persistence and frontend knowledge facets named in the decision register.

## Tooling

Use repository search, compiler/tooling output, package-audit commands, and analyzers when available. When a scanner reports a possible issue: inspect the actual code, decide whether the pattern is reachable and relevant, and report it only with appropriate confidence.

## Severity

Consider exploitability, external exposure, required privileges, affected data or capability, blast radius, reliability of exploitation, and compensating controls.

- **Critical** — sparingly: exposed real production credentials, reachable authentication bypass, straightforward remote code execution, exploitable injection with major impact.
- **High** — realistically exploitable or substantially compromises data, authorization, or system behavior.
- **Medium** — meaningful weakness needing realistic conditions, limited access, or extra steps.
- **Low** — genuine but limited weakness.
- **Info** — useful observation or hardening opportunity, not a demonstrated vulnerability.

## False positives and context

Not automatically vulnerabilities: an endpoint without `[Authorize]` under a secure fallback policy; bare `[Authorize]` when authentication alone is intended; `AllowAnyOrigin()` for a genuinely public non-credentialed API; MD5/SHA1 as a non-security checksum; no application-level encryption when platform/storage encryption satisfies the requirement; obviously fake test credentials; framework defaults that are secure in the actual hosting configuration.

Not automatically safe: secrets in `appsettings.Development.json`; sensitive values logged only at Debug level; client-side route guards; hidden UI buttons; CORS used as a substitute for authorization.

## Reporting

Every confirmed finding includes: severity, file and location, title, evidence, why it is a risk, likely impact, smallest reasonable remediation, and an OWASP category when applicable. Label uncertain items `NEEDS VERIFICATION` instead of presenting them as confirmed.

```markdown
# Security Scan Report

Scope:
- ...

Limitations:
Static analysis only. This does not replace penetration testing, dynamic testing, threat modeling, or infrastructure review.

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

Layer status is PASS, FINDINGS, NOT APPLICABLE, or NOT CHECKED — never PASS for an uninspected layer.

## Remediation discipline

Prefer the smallest secure change consistent with the architecture. Do not recommend a new authentication system unnecessarily, custom cryptography, blanket encryption of all database fields, `[Authorize]` on every action when a global policy already protects it, security libraries merely to satisfy the scan, or disabling functionality because a static scanner cannot understand it.

## Completion

The scan is complete when all applicable layers were inspected, findings have evidence, uncertain findings are labeled, severity reflects actual risk, limitations are stated, and no layer is marked PASS without being checked.
