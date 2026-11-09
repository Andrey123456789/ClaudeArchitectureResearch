---
name: security-scan
description: >
  Use for a security scan, audit, OWASP, secret, auth or CORS review, or a pre-
  release security check: seven-layer, evidence-based static review with
  severity-rated findings.
---

> Level: 3 Project · Owns: security-scan procedure, severity scale and report shape · Scope: common · Loads: on demand (model- or user-invoked)

# Security Scan

Static review of code, dependencies and configuration in the repository. It is not a penetration test and cannot prove the application secure: runtime-only issues, infrastructure outside the repository, business-logic abuse, complex authorization bypasses and deployment-specific weaknesses can remain undetected. State that limitation in the report.

## Read first

- `.claude/rules/0-core/security-principles.md` — the security invariants and the review discipline (evidence, contextual severity, tool independence).
- `.claude/rules/0-core/logging-principles.md` — sensitive-data logging.
- Private reference `references/scan-layers.md` — investigation prompts per layer.

## 1. Determine scope

Inspect which surfaces exist: .NET backend, Angular frontend, authentication/authorization, database access, external HTTP integrations, file upload/download, container configuration, CI/CD, production configuration, logging, caching, background processing. Skip checks for absent surfaces (NOT APPLICABLE) instead of reporting them as failures.

- Full pre-release or explicitly requested audit → all applicable layers.
- Targeted change → affected layers first, expanding when the change crosses security boundaries:

| Change | Priority layers |
|---|---|
| Dependency update | 1 |
| Authentication change | 4 |
| New controller endpoint | 4, 3, 5 |
| Database/query change | 3, 4, 6 |
| Configuration change | 2 |
| Logging change | 6 |
| HttpClient integration | 2, 3 (SSRF), 7 |
| File upload | 3, 5, 7 |
| Angular auth/UI change | 5 + server authorization assumptions (4) |

## 2. Inspect the layers

| # | Layer | Typical OWASP Top 10:2025 mapping |
|---|---|---|
| 1 | Dependencies and supply chain | A03 |
| 2 | Secrets and configuration | A02, A04 |
| 3 | Injection and dangerous code patterns | A04, A05, A08 |
| 4 | Authentication and access control | A01, A07 |
| 5 | Browser and HTTP/API security | A01, A02 |
| 6 | Sensitive data, logging and error exposure | A04, A09 |
| 7 | Exceptional conditions and failure handling | A06, A10 |

OWASP categories: A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging & Alerting Failures, A10 Mishandling of Exceptional Conditions. Map a finding only when a category genuinely fits.

Use available tooling — repository search, compiler and analyzer output, `dotnet package list --vulnerable --include-transitive`, `npm audit` — then inspect the code to decide reachability before reporting. Evaluate effective authorization including global and fallback policies.

## 3. Rate severity

Consider exploitability, external exposure, required privileges, affected data or capability, blast radius, reliability of exploitation and compensating controls. Advisory CVSS scores are not application severity.

- **Critical** — immediately exploitable, high impact (exposed real production credentials, reachable authentication bypass, straightforward RCE, exploitable injection with major impact). Use sparingly.
- **High** — realistically exploitable; can substantially compromise data, authorization or behavior.
- **Medium** — meaningful weakness that needs realistic conditions, limited access or extra steps.
- **Low** — genuine but limited weakness.
- **Info** — hardening opportunity, not a demonstrated vulnerability.

Label uncertain items `NEEDS VERIFICATION` instead of presenting them as confirmed.

## 4. Context checks

Usually not findings: an endpoint without `[Authorize]` under a secure fallback policy; bare `[Authorize]` when authentication alone is the intent; `AllowAnyOrigin()` on a genuinely public non-credentialed API; MD5/SHA1 as a non-security checksum; data protected by adequate platform/storage encryption; obviously fake test credentials; framework defaults that are secure in the actual hosting setup.

Not automatically safe: secrets in `appsettings.Development.json`; sensitive values logged only at Debug; client-side route guards; hidden UI buttons; CORS used as a substitute for authorization.

## Report

```markdown
# Security Scan Report

Scope:
- ...

Limitations:
Static analysis only. It does not replace penetration testing, dynamic testing,
threat modeling or infrastructure review.

## Summary

| Severity | Count |
|---|---:|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |
| Info | 0 |

## Findings

### [HIGH] path/File.cs:42 — Finding title

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
| Dependencies and supply chain | PASS / FINDINGS / NOT APPLICABLE / NOT CHECKED | 0 |
| Secrets and configuration | ... | 0 |
| Injection and dangerous patterns | ... | 0 |
| Authentication and access control | ... | 0 |
| Browser and HTTP/API security | ... | 0 |
| Sensitive data/logging/error exposure | ... | 0 |
| Exceptional conditions | ... | 0 |
```

Every confirmed finding includes severity, file and location, title, evidence, why it is a risk, likely impact, smallest reasonable remediation and OWASP category when applicable. Never mark a layer PASS without inspecting it.

## Remediation discipline

Prefer the smallest secure change consistent with the architecture. Do not recommend a new authentication system without need, custom cryptography, blanket encryption of all database fields, `[Authorize]` on every action when a global policy already protects them, security libraries merely to satisfy the scan, or disabling functionality because a static tool cannot understand it. Do not upgrade packages during a scan unless asked; dependency changes go through `add-dependency`.

## Completion

All applicable layers inspected; findings carry evidence; uncertain items labelled; severity reflects actual risk; limitations stated; no unchecked layer marked PASS.
