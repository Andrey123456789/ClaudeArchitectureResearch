---
name: security-scan
description: Use for a security scan, security audit, vulnerability or OWASP review, secret scan, auth or CORS review, pre-release security check, or penetration-test preparation of the backend and frontend. Evidence-based static review across seven layers with contextual severity.
---

> Level: 0-core · Owns: security review procedure — evidence and severity discipline, tool independence, scan scope, report shape · Loading: on invocation

# Security Scan

Evidence-based static review of the repository. It is not a penetration test and cannot prove the application secure: it may miss runtime-only vulnerabilities, infrastructure outside the repository, complex business-logic abuse, sophisticated authorization bypasses, deployment-specific weaknesses, and anything requiring dynamic exploitation. State that limitation in every report. Security invariants themselves live in `.claude/rules/0-core/security.md`.

## Principles

1. Report concrete risks in the context of actual exposure, not generic advice.
2. Distinguish confirmed findings from items that need verification (`NEEDS VERIFICATION`).
3. Assign severity from exploitability, reachability, impact, and application context — never from a suspicious pattern, an OWASP category, or a raw CVSS score alone.
4. Do not suppress a real secret because it sits in a Development file.
5. Do not require security mechanisms the project does not need.
6. Evaluate effective authorization, including global and fallback policies.
7. The scan must work without any specific MCP server, analyzer, agent, or commercial scanner: available tools are evidence, not the sole authority — inspect the code, confirm reachability and relevance, then report with appropriate confidence.

## Scope

Inspect which surfaces exist — backend, frontend, authentication/authorization, database access, external HTTP integrations, file upload/download, container configuration, CI/CD, production configuration, logging, caching, background processing — and skip irrelevant checks rather than reporting them as failures.

For a full pre-release or requested audit, review all applicable layers. For targeted changes, start with the affected layers and expand when the change crosses security boundaries:

| Change | Priority areas |
| --- | --- |
| Dependency update | Dependencies / supply chain |
| Authentication change | Authentication / access control |
| New controller endpoint | Access control, input handling, HTTP security |
| Database/query change | Injection, access control, sensitive data |
| Configuration change | Secrets / configuration |
| Logging change | Sensitive data / logging |
| Outbound HTTP integration | Configuration, SSRF/input handling, failure handling |
| File upload | Input handling, path safety, resource limits |
| Frontend auth/UI change | Browser security + server authorization assumptions |

## Layers

Detailed investigation prompts: `references/scan-layers.md`.

| # | Layer | Typical OWASP Top 10:2025 mapping |
| --- | --- | --- |
| 1 | Dependencies and supply chain | A03 |
| 2 | Secrets and configuration | A02, A04 |
| 3 | Injection and dangerous code patterns | A04, A05, A08 |
| 4 | Authentication and access control | A01, A07 |
| 5 | Browser and HTTP/API security | A01, A02 |
| 6 | Sensitive data, logging, and error exposure | A04, A09 |
| 7 | Exceptional conditions and failure handling | A06, A10 |

OWASP categories (A01 Broken Access Control, A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging & Alerting Failures, A10 Mishandling of Exceptional Conditions) are an awareness taxonomy: map only when it genuinely fits.

Deeper technique: `authentication`, `configuration`, `logging`, `aspnet-error-handling`, `http-api`, `httpclient-factory`, and the persistence and frontend knowledge skills named in the capability selection. Do not copy their guidance into the report.

## Severity

Weigh exploitability, external exposure, required privileges, affected data or capability, blast radius, reliability of exploitation, and existing compensating controls.

- **Critical** — use sparingly: exposed real production credentials, reachable authentication bypass, straightforward remote code execution, exploitable injection with major impact.
- **High** — realistically exploitable or substantially compromises data, authorization, or system behavior.
- **Medium** — meaningful weakness needing realistic conditions, limited access, or extra steps.
- **Low** — genuine but limited practical impact.
- **Info** — hardening observation, not a demonstrated vulnerability.

Not automatically findings: an endpoint without `[Authorize]` under a secure fallback policy; bare `[Authorize]` when authentication alone is intended; `AllowAnyOrigin()` on a genuinely public non-credentialed API; MD5/SHA1 as a non-security checksum; no application-level encryption when platform encryption satisfies the requirement; obviously fake test credentials; framework defaults secure in the actual hosting. Not automatically safe: secrets in `appsettings.Development.json`; sensitive values logged only at Debug; client-side route guards; hidden UI buttons; CORS used as a substitute for authorization.

## Report shape

Each confirmed finding: severity, file and location, title, evidence, why it is a risk, likely impact, smallest reasonable remediation, OWASP category when applicable. Label uncertain items `NEEDS VERIFICATION`.

```markdown
# Security Scan Report

Scope: ...
Limitations: Static analysis only. This does not replace penetration testing, dynamic testing, threat modeling, or infrastructure review.

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
| ... | ... | ... |
```

Layer status is `PASS`, `FINDINGS`, `NOT APPLICABLE`, or `NOT CHECKED` — never `PASS` for an uninspected layer.

## Remediation discipline

Recommend the smallest secure change consistent with the architecture. Do not recommend a new authentication system without need, custom cryptography, blanket field encryption, `[Authorize]` on every action when a global policy already protects them, security libraries just to satisfy the scan, or disabling functionality because a scanner cannot understand it.

## Completion

All applicable layers inspected, findings carry evidence, uncertain items are labeled, severity reflects actual risk, limitations are stated, and no layer is marked `PASS` without being checked.
