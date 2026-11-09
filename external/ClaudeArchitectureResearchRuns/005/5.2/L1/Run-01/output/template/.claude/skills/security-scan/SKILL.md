---
name: security-scan
description: >
  Run for a security scan or audit, OWASP, vulnerability, secret, auth, or CORS
  review, or a pre-release check: evidence-based static review, contextual
  severity.
---
> Level: 2-technology | Owns: security-scan procedure, finding evidence and severity discipline, report shape | Scope: common | Loads: on demand (skill)

# Security Scan

An evidence-based **static** review of the repository. It is not a penetration
test and cannot prove the application secure: runtime-only vulnerabilities,
infrastructure outside the repository, complex business-logic abuse,
sophisticated authorization bypasses, deployment-specific weaknesses, and
issues needing dynamic exploitation may stay undetected. State this limitation
in every report.

## Principles

1. Report concrete risks, not generic advice; evaluate each finding in the
   context of actual exposure and application behavior.
2. Distinguish confirmed findings from items that need verification, and assign
   severity from exploitability, reachability, impact, and application
   context — never from a suspicious pattern or a raw CVSS score alone.
3. Do not suppress a real secret because it sits in a Development file; do not
   require security mechanisms the project does not need.
4. Evaluate effective authorization, including global and fallback policies.
5. Security review must not depend on one tool: do not require a specific MCP
   server, analyzer, commercial scanner, or external tool. Use available
   tooling as evidence, not as the authority — inspect the code, confirm
   reachability and relevance, and report only with appropriate confidence.

The security invariants themselves are owned by `security.md` and the related
rules; this skill finds violations of them.

## Scope

Inspect which surfaces exist — .NET backend, frontend (if selected),
authentication/authorization, database access, external HTTP integrations, file
upload/download, container configuration, CI/CD, production configuration,
logging, caching, background processing — and mark irrelevant layers
`NOT APPLICABLE` rather than failing them.

For a full or pre-release audit review every applicable layer. For a targeted
change start with the affected layers and expand when the change crosses a
security boundary:

| Change | Priority layers |
|---|---|
| Dependency update | 1 |
| Authentication change | 4 |
| New Controller endpoint | 4, 5, input handling in 3 |
| Database/query change | 3, 4, 6 |
| Configuration change | 2 |
| Logging change | 6 |
| Outbound HTTP integration | 2, 3 (SSRF), 7 |
| File upload | 3 (paths), 5, 7 |
| Frontend auth/UI change | 5 and server-side authorization in 4 |

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

Use the OWASP categories (A01 Broken Access Control, A02 Security
Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic
Failures, A05 Injection, A06 Insecure Design, A07 Authentication Failures, A08
Software or Data Integrity Failures, A09 Security Logging & Alerting Failures,
A10 Mishandling of Exceptional Conditions) only where they genuinely fit.

## Severity

Consider exploitability, external exposure, required privileges, affected data
or capability, blast radius, reliability of exploitation, and compensating
controls.

- **Critical** — sparingly: exposed real production credentials, reachable
  authentication bypass, straightforward remote code execution, exploitable
  injection with major impact.
- **High** — realistically exploitable, substantial compromise of data,
  authorization, or behavior.
- **Medium** — meaningful weakness needing realistic conditions or extra steps.
- **Low** — genuine but limited weakness.
- **Info** — hardening opportunity, not a demonstrated vulnerability.

## Context and false positives

Not automatically vulnerabilities: an endpoint without `[Authorize]` under a
secure fallback policy; bare `[Authorize]` where authentication alone is the
intent; `AllowAnyOrigin()` on a genuinely public non-credentialed API; MD5/SHA1
as a non-security checksum; platform/storage encryption that satisfies the
requirement; obviously fake test credentials; framework defaults that are secure
in the actual hosting configuration.

Not automatically safe: secrets in `appsettings.Development.json`; sensitive
values logged only at Debug level; client-side route guards; hidden UI buttons;
CORS used as a substitute for authorization.

## Reporting

Each confirmed finding: severity, file and location, title, evidence, why it is
a risk, likely impact, smallest reasonable remediation, OWASP category when
applicable. Label uncertain items `NEEDS VERIFICATION`.

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
Evidence: ...
Impact: ...
Remediation: ...

## Layer Results
| Layer | Status | Findings |
|---|---|---:|
| Dependencies and supply chain | PASS | 0 |
| ... | ... | ... |
```

Layer status values: `PASS`, `FINDINGS`, `NOT APPLICABLE`, `NOT CHECKED` — never
mark an uninspected layer `PASS`.

## Remediation discipline

Recommend the smallest secure change consistent with the project architecture.
Do not recommend a new authentication system unnecessarily, custom
cryptography, blanket encryption of all database fields, `[Authorize]` on every
action when a global policy already protects them, security libraries merely to
satisfy the scan, or disabling functionality because a scanner cannot
understand it. Do not upgrade packages during a scan unless asked.

## Completion

Complete when every applicable layer was inspected, findings have evidence,
uncertain findings are labeled, severity reflects actual risk, limitations are
stated, and no layer is marked `PASS` without being checked. Deeper guidance:
`authentication`, `configuration`, `logging`, `aspnet-error-handling`,
`http-api`, `httpclient-factory`, `persistence.knowledge`, `frontend.knowledge`.
