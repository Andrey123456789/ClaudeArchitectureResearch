---
name: security-scan
description: >
  Use for a security scan or audit, OWASP, secret, auth, or CORS review, or a pre-release security check.
---

> Level: 3 Project | Owns: security-review procedure, evidence and severity discipline, tool independence, report shape | Scope: common | Loads: workflow skill (model-invoked) | Depends on: CLAUDE.md, 0-core/*, 1-architecture/*, 2-technology/*, 3-project/*

# Security Scan

A static review identifies code, dependency, configuration, and access-control
problems; it is not a penetration test and cannot prove the application secure
(runtime-only issues, external infrastructure, complex business-logic abuse,
deployment-specific weaknesses). State that limitation in the report.

## Principles

1. Report concrete risks in the context of actual exposure, not generic advice.
2. Distinguish confirmed findings from items that need verification
   (`NEEDS VERIFICATION`).
3. Assign severity from exploitability, reachability, external exposure,
   required privileges, impact, blast radius, reliability of exploitation, and
   compensating controls — not from a suspicious pattern, an OWASP category, or
   a raw CVSS score alone.
4. Do not suppress a real secret because it is in a Development file; do not
   require security mechanisms the project does not need.
5. Evaluate effective authorization, including global and fallback policies.
6. Do not require a specific MCP server, agent, analyzer, commercial scanner, or
   other external tool; use available tooling as evidence, never as the sole
   authority. When a tool reports something, inspect the code, confirm
   reachability and relevance, then report with appropriate confidence.

The security invariants being checked are the Core security, logging,
error-exposure, health, and integration principles (`.claude/rules/0-core/`)
and their technology bindings.

## 1. Scope

Determine which surfaces exist: .NET backend, Angular frontend,
authentication/authorization, database access, outbound HTTP, file
upload/download, containers, CI/CD, production configuration, logging, caching,
background processing. Skip irrelevant layers instead of reporting them as
failures.

For a full or pre-release audit, review every applicable layer. For a targeted
change, start with the affected layers and expand when the change crosses a
security boundary:

| Change | Priority layers |
|---|---|
| Dependency update | 1 |
| Authentication change | 4 |
| New Controller endpoint | 3, 4, 5 |
| Database/query change | 3, 4, 6 |
| Configuration change | 2 |
| Logging change | 6 |
| HttpClient integration | 2, 3 (SSRF), 7 |
| File upload | 3, 5 |
| Angular auth/UI change | 4, 5 |

## 2. Layers

Investigate each applicable layer with `references/scan-layers.md`:

| # | Layer | Typical OWASP |
|---|---|---|
| 1 | Dependencies and supply chain | A03 |
| 2 | Secrets and configuration | A02, A04 |
| 3 | Injection and dangerous code patterns | A04, A05, A08 |
| 4 | Authentication and access control | A01, A07 |
| 5 | Browser and HTTP/API security | A01, A02 |
| 6 | Sensitive data, logging, error exposure | A04, A09 |
| 7 | Exceptional conditions and failure handling | A06, A10 |

Use an OWASP Top 10:2025 category only when it genuinely fits.

## False Positives and Context

Not automatically findings: an endpoint without `[Authorize]` under a secure
fallback policy; bare `[Authorize]` when authentication alone is the intended
policy; `AllowAnyOrigin()` for a genuinely public non-credentialed API; MD5/SHA1
as non-security checksums; no application-level encryption when platform or
storage encryption satisfies the requirement; obviously fake test credentials;
framework defaults that are secure in the actual hosting configuration.

Not automatically safe: secrets in `appsettings.Development.json`, sensitive
values logged only at Debug level, Angular route guards, hidden UI buttons, and
CORS used as a substitute for authorization.

For depth, consult `authentication`, `configuration`, `logging`,
`aspnet-error-handling`, `http-api`, `httpclient-factory`, `ef-core`, and
`angular` rather than duplicating their guidance in the report.

## 3. Severity

- **Critical** — immediately exploitable, high impact: exposed real production
  credentials, reachable authentication bypass, straightforward RCE, injection
  with major impact.
- **High** — realistically exploitable; can substantially compromise data,
  authorization, or behavior.
- **Medium** — meaningful weakness needing realistic conditions or extra steps.
- **Low** — genuine but limited weakness.
- **Info** — hardening opportunity, not a demonstrated vulnerability.

## 4. Remediation Discipline

Prefer the smallest secure change consistent with the architecture. Do not
recommend a new authentication system without need, custom cryptography,
blanket field encryption, `[Authorize]` on every action when a global policy
already protects them, security libraries merely to satisfy the scan, or
disabling functionality because a scanner cannot understand it.

## 5. Report

Each confirmed finding: severity, file and location, title, evidence, why it is
a risk, likely impact, smallest reasonable remediation, OWASP category when
applicable. Label uncertain items `NEEDS VERIFICATION`.

```markdown
# Security Scan Report

Scope: ...
Limitations: Static analysis only; does not replace penetration testing,
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
| Dependencies and supply chain | PASS / FINDINGS / NOT APPLICABLE / NOT CHECKED | 0 |
```

The scan is complete when every applicable layer was inspected, findings have
evidence, uncertain findings are labeled, severity reflects actual risk,
limitations are stated, and no layer is marked PASS without being checked.
Workflows with meaningful security-sensitive design (tenant isolation,
multi-step authorization, financial or idempotency abuse) are named as
candidates for threat modeling rather than claimed secure.
