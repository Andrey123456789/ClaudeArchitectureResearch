---
paths:
  - "backend/**"
  - "frontend/**"
---

> Level: 0 Core · Owns: what may be logged and where failures are logged · Scope: common · Loads: path

# Logging Principles

- **Must not** log passwords, access or refresh tokens, private keys, authentication secrets, authorization headers or full payment credentials. Avoid personal data unless a concrete operational need exists and the project's privacy policy permits it. A log level is not a privacy control; prefer stable technical identifiers over personal data.
- **Must not** serialize arbitrary request bodies, domain objects or sensitive payloads into logs by default; log the specific, non-sensitive properties needed to operate and diagnose the system.
- **Must** log an unexpected exception once, at the boundary that handles it; do not log the same exception again in every layer it passes through.

Technique (levels, scopes, correlation, provider setup): `logging` skill.
