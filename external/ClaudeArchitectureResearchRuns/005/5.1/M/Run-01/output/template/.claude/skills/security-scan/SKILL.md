---
name: security-scan
description: >
  Use when asked for a security scan, security audit, vulnerability or OWASP
  review, secret scan, auth or CORS review, pre-release security check, or
  penetration-test preparation, or when a change is materially
  security-sensitive. Evidence-based static review of .NET and Angular code
  across seven layers.
---

> Owns: security review procedure, finding evidence and severity discipline, tool independence, security report shape | Scope: common | Loads: workflow (CLAUDE.md routing); private reference references/scan-layers.md

# Security Scan

Perform an evidence-based static security review. Security invariants are owned
by `.claude/rules/security.md` (read it first; also `api.md` for error/health
exposure and `dependencies.md` for manifests). This workflow finds violations
and real risks; it does not redefine them.

This is not a penetration test. Static review cannot prove security and may miss
runtime-only issues, infrastructure outside the repository, business-logic
abuse, sophisticated authorization bypasses, deployment-specific weaknesses, or
vulnerabilities requiring dynamic exploitation. State this limitation in the
report.

## Principles

1. Report concrete risks, not generic advice; evaluate each in the context of
   actual exposure and application behavior.
2. Distinguish confirmed findings from items that need verification
   (`NEEDS VERIFICATION`).
3. Assign severity from exploitability, reachability, impact, required
   privileges, blast radius, and compensating controls — never from a
   suspicious pattern, OWASP category, or raw CVSS score alone.
4. Do not suppress a real secret because it sits in a Development file; do not
   require security mechanisms the project does not need.
5. Evaluate effective authorization, including global/fallback policies.
6. No specific MCP server, agent, analyzer, commercial scanner, or external tool
   is required. Use available tooling as evidence, never as the sole
   authority: inspect the actual code, decide whether the pattern is reachable
   and relevant, and report with appropriate confidence.

## 1. Determine Scope

Inventory which surfaces exist: .NET backend, Angular frontend,
authentication/authorization, database access, external HTTP integrations, file
upload/download, Docker, CI/CD, production configuration, logging, caching,
background processing. Skip irrelevant checks instead of reporting them as
failures.

For a full or pre-release audit, review all applicable layers. For a targeted
change, start with the affected layers and expand when the change crosses
security boundaries:

| Change | Priority layers |
|---|---|
| Dependency update | 1 |
| Configuration change | 2 |
| Database/query change | 3, 4, 6 |
| Authentication change, Angular auth/UI change | 4, 5 |
| New Controller endpoint | 4, 5, 3 |
| Logging change | 6 |
| HttpClient integration | 2, 3 (SSRF), 7 |
| File upload | 3 (paths), 5 (uploads), 7 (limits) |

## 2. Inspect the Layers

Use `references/scan-layers.md` for the investigation prompts of each layer:

| # | Layer | Typical OWASP Top 10:2025 mapping |
|---|---|---|
| 1 | Dependencies and supply chain | A03 |
| 2 | Secrets and configuration | A02, A04 |
| 3 | Injection and dangerous code patterns | A04, A05, A08 |
| 4 | Authentication and access control | A01, A07 |
| 5 | Browser and HTTP/API security | A01, A02 |
| 6 | Sensitive data, logging, and error exposure | A04, A09 |
| 7 | Exceptional conditions and failure handling | A06, A10 |

Use an OWASP category only when it genuinely fits; do not force a mapping.
Load `authentication`, `configuration`, `logging`, `aspnet-error-handling`,
`http-api`, `httpclient-factory`, `ef-core`, or `angular` only for depth.

## 3. Severity

- **Critical** — use sparingly: exposed real production credentials, reachable
  authentication bypass, straightforward remote code execution, exploitable
  injection with major impact.
- **High** — realistically exploitable or substantially compromising data,
  authorization, or system behavior.
- **Medium** — meaningful weakness requiring realistic conditions or extra steps.
- **Low** — genuine but limited weakness.
- **Info** — hardening opportunity, not a demonstrated vulnerability.

## 4. Remediation Discipline

Recommend the smallest secure change consistent with the project architecture.
Do not recommend a new authentication system unnecessarily, custom
cryptography, blanket field encryption, redundant `[Authorize]` attributes under
a secure global policy, security libraries merely to satisfy the scan, or
disabling functionality a static scanner cannot understand.

## 5. Report

```markdown
# Security Scan Report

Scope: ...
Limitations: Static analysis only. This does not replace penetration testing,
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
### [HIGH] path/File.cs:42 — Finding title
OWASP: A01:2025 Broken Access Control (when applicable)
Evidence: ...
Impact: ...
Remediation: ...

## Layer Results
| Layer | Status | Findings |
|---|---|---:|
| Dependencies and supply chain | PASS | 0 |
| ... | ... | ... |
```

Layer status is `PASS`, `FINDINGS`, `NOT APPLICABLE`, or `NOT CHECKED`; never
mark an uninspected layer `PASS`. Uncertain items use `[NEEDS VERIFICATION]`.

## Completion

Complete when every applicable layer was inspected, findings have evidence,
uncertain findings are labeled, severity reflects actual risk, and limitations
are stated.
