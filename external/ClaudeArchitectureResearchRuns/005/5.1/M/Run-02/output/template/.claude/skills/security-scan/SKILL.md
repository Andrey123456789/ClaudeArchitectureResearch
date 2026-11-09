---
name: security-scan
description: >
  Use for a security scan or audit, an OWASP, secret, auth, or CORS review, a
  pre-release security check, or a materially security-sensitive change.
  Evidence-based seven-layer static review with a severity-ranked report.
---

> Owner: static security review procedure — evidence and severity discipline, tool independence, layer coverage, report shape | Scope: common | Loads: on demand — workflow (routed by `CLAUDE.md` § Development Workflow) | Enforced: none (review procedure)

# Security Scan

## Purpose

An evidence-based static security review of the repository. It is not a
penetration test: it cannot detect runtime-only vulnerabilities, infrastructure
configuration outside the repository, complex business-logic abuse,
sophisticated authorization bypasses, deployment-specific weaknesses, or
vulnerabilities that need dynamic exploitation. State that limitation in the
report.

## Read First

`.claude/rules/security.md` defines the security invariants the scan checks.
Read it, plus `.claude/rules/error-handling.md` (error exposure, outbound
failures) and `.claude/rules/angular.md` when the frontend is in scope.

## Principles

- Report concrete risks, not generic security advice, evaluated in the context
  of actual exposure and application behavior.
- Distinguish confirmed findings from items that need verification, and assign
  severity from exploitability, reachability, impact, and application context —
  never from a suspicious pattern or a raw CVSS score alone.
- Do not suppress a real secret because it sits in a Development file.
- Do not require security mechanisms the project does not need.
- Evaluate effective authorization behavior, including global and fallback
  policies.
- Do not require a specific MCP server, agent, analyzer, or commercial scanner;
  available tools provide evidence, not the sole authority.

## OWASP Mapping

Use OWASP Top 10:2025 as an awareness taxonomy where it genuinely fits:

```text
A01 Broken Access Control
A02 Security Misconfiguration
A03 Software Supply Chain Failures
A04 Cryptographic Failures
A05 Injection
A06 Insecure Design
A07 Authentication Failures
A08 Software or Data Integrity Failures
A09 Security Logging & Alerting Failures
A10 Mishandling of Exceptional Conditions
```

Not every finding needs a category; never force an inaccurate mapping.

## Scan Scope

First determine which surfaces exist: .NET backend, Angular frontend,
authentication/authorization, database access, external HTTP integrations, file
upload/download, Docker/container configuration, CI/CD, production
configuration, logging, caching, background processing. Mark irrelevant checks
NOT APPLICABLE instead of reporting them as failures.

## Security Layers

Investigation prompts for each layer: `references/scan-layers.md`.

| # | Layer | Typical OWASP mapping |
|---|---|---|
| 1 | Dependencies and supply chain | A03 |
| 2 | Secrets and configuration | A02, A04 |
| 3 | Injection and dangerous code patterns | A04, A05, A08 |
| 4 | Authentication and access control | A01, A07 |
| 5 | Browser and HTTP/API security | A01, A02 |
| 6 | Sensitive data, logging, and error exposure | A04, A09 |
| 7 | Exceptional conditions and failure handling | A06, A10 |

## Selecting Scope

A full pre-release or explicitly requested audit covers every applicable layer.
For a targeted change, start with the affected layers and expand when the change
crosses security boundaries:

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

## Tooling

Use repository search, compiler and tooling output, package-audit commands
(`dotnet package list --vulnerable --include-transitive`, `npm audit`),
`node .claude/scripts/check-dependencies.mjs`, and static analyzers when
available. When a tool reports a possible issue: inspect the actual code, decide
whether the pattern is reachable and relevant, and report it only with
appropriate confidence. Do not upgrade packages during a scan unless asked.

## Severity

Consider exploitability, external exposure, required privileges, affected data
or capability, blast radius, reliability of exploitation, and compensating
controls.

- **Critical** — use sparingly: exposed real production credentials, reachable
  authentication bypass, straightforward remote code execution, exploitable
  injection with major impact.
- **High** — realistically exploitable, or able to substantially compromise data,
  authorization, or system behavior.
- **Medium** — meaningful weakness that needs realistic conditions, limited
  access, or extra exploitation steps.
- **Low** — genuine but limited weakness.
- **Info** — useful observation or hardening opportunity, not a demonstrated
  vulnerability.

## False Positives and Context

Not automatically vulnerabilities: an endpoint without `[Authorize]` under a
secure fallback policy; bare `[Authorize]` when authentication alone is the
intended policy; `AllowAnyOrigin()` on a genuinely public non-credentialed API;
MD5/SHA1 as a non-security checksum; no application-level encryption where
platform or storage encryption satisfies the requirement; obviously fake test
credentials; framework defaults that are secure in the actual hosting
configuration.

Not automatically safe: secrets in `appsettings.Development.json`, sensitive
values logged only at Debug level, Angular route guards, hidden UI buttons, CORS
used as a substitute for authorization.

## Deeper Guidance

Knowledge skills for remediation detail: `authentication`, `configuration`,
`logging`, `aspnet-error-handling`, `http-api`, `httpclient-factory`, `ef-core`,
`angular`.

## Reporting

Every confirmed finding includes severity, file and location, title, evidence,
why it is a risk, likely impact, smallest reasonable remediation, and the OWASP
category when applicable. Label uncertain findings `NEEDS VERIFICATION` instead of
presenting them as confirmed.

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

Layer status is `PASS`, `FINDINGS`, `NOT APPLICABLE`, or `NOT CHECKED`; never mark
an uninspected layer PASS.

## Remediation Discipline

Prefer the smallest secure change consistent with project architecture. Do not
recommend a new authentication system without need, custom cryptography, blanket
encryption of all database fields, `[Authorize]` on every action when a global
policy already protects them, security libraries merely to satisfy the scan, or
disabling functionality because a static scanner cannot understand it.

## Completion

The scan is complete when every applicable layer was inspected, findings have
evidence, uncertain findings are labeled, severity reflects actual risk, and
limitations are stated.
