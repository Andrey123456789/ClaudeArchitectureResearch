---
name: security-scan
description: >
  Use for a security scan, audit, OWASP or vulnerability review, secret scan,
  auth/CORS review, or pre-release security check: evidence-based seven-layer review.
---

> Level: 3 Project · Owns: security review procedure, evidence and severity discipline, report shape (workflow) · Scope: common · Loads: on invocation · Depends on: CLAUDE.md, .claude/rules/** (owner reads)

# Security Scan

Perform an evidence-based static security review. This is not a penetration test: static review cannot prove the application is secure and may miss runtime-only vulnerabilities, infrastructure outside the repository, complex business-logic abuse, sophisticated authorization bypasses, deployment-specific weaknesses, and issues that need dynamic exploitation. State that limitation in every report.

The security invariants being checked are owned by `.claude/rules/0-core/security-principles.md` and `logging-principles.md` (with bindings in `2-technology/aspnet-core.md`); read them first.

## Principles

1. Report concrete risks, not generic advice; evaluate them in the context of actual exposure and behavior.
2. Distinguish confirmed findings from items that need verification, and assign severity from exploitability, reachability, impact, and application context — never from a suspicious pattern or raw CVSS alone.
3. Do not suppress a real secret because it sits in a Development file, and do not require security mechanisms the project does not need.
4. Evaluate effective authorization, including global/fallback policies.
5. Do not require a specific MCP server, agent, analyzer, commercial scanner, or other external tool; use available tooling as evidence, not as the sole authority.

## Scope

Inspect which surfaces exist — .NET backend, Angular frontend, authentication/authorization, database access, external HTTP integrations, file upload/download, Docker, CI/CD, production configuration, logging, caching, background processing — and skip irrelevant checks rather than reporting them as failures. For a full audit review every applicable layer; for a targeted change start with the affected layers and expand when the change crosses security boundaries:

| Change | Priority layers |
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

## Layers

Use `references/scan-layers.md` for the investigation prompts of each layer.

| # | Layer | Typical OWASP 2025 |
|---|---|---|
| 1 | Dependencies and supply chain | A03 |
| 2 | Secrets and configuration | A02, A04 |
| 3 | Injection and dangerous code patterns | A04, A05, A08 |
| 4 | Authentication and access control | A01, A07 |
| 5 | Browser and HTTP/API security | A01, A02 |
| 6 | Sensitive data, logging, and error exposure | A04, A09 |
| 7 | Exceptional conditions and failure handling | A06, A10 |

OWASP Top 10:2025: A01 Broken Access Control · A02 Security Misconfiguration · A03 Software Supply Chain Failures · A04 Cryptographic Failures · A05 Injection · A06 Insecure Design · A07 Authentication Failures · A08 Software or Data Integrity Failures · A09 Security Logging & Alerting Failures · A10 Mishandling of Exceptional Conditions. Map only when the category genuinely fits.

## Tool findings

When a scanner or analyzer reports a possible issue: inspect the actual code, decide whether the pattern is reachable and relevant, and report it only with appropriate confidence.

## Severity

Consider exploitability, external exposure, required privileges, affected data or capability, blast radius, reliability of exploitation, and compensating controls.

- **Critical** (sparingly) — exposed real production credentials, reachable authentication bypass, straightforward remote code execution, exploitable injection with major impact.
- **High** — realistically exploitable or substantially compromises data, authorization, or system behavior.
- **Medium** — meaningful weakness needing realistic conditions, limited access, or extra steps.
- **Low** — genuine but limited weakness.
- **Info** — useful observation or hardening opportunity, not a demonstrated vulnerability.

## False positives and false comfort

Not automatically vulnerabilities: an endpoint without `[Authorize]` under a secure fallback policy; bare `[Authorize]` when authentication alone is intended; `AllowAnyOrigin()` on a genuinely public non-credentialed API; MD5/SHA1 as a non-security checksum; no application-level encryption when platform/storage encryption satisfies the requirement; obviously fake test credentials; framework defaults that are secure in the actual hosting.

Not automatically safe: secrets in `appsettings.Development.json`; sensitive values logged only at Debug; Angular route guards; hidden UI buttons; CORS used as a substitute for authorization.

## Report

Each confirmed finding: severity · file and location · title · evidence · why it is a risk · likely impact · smallest remediation · OWASP category when applicable. Label uncertain items `NEEDS VERIFICATION`.

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

Layer status is `PASS`, `FINDINGS`, `NOT APPLICABLE`, or `NOT CHECKED`; never mark a layer PASS without checking it.

## Remediation discipline

Prefer the smallest secure change consistent with the architecture. Do not recommend a new authentication system without need, custom cryptography, blanket encryption of all database fields, `[Authorize]` on every action when a global policy already protects them, security libraries merely to satisfy the scan, or disabling functionality because a static scanner cannot understand it.

## Completion

Complete when all applicable layers were inspected, findings have evidence, uncertain findings are labeled, severity reflects actual risk, limitations are stated, and no layer is marked PASS unchecked.
