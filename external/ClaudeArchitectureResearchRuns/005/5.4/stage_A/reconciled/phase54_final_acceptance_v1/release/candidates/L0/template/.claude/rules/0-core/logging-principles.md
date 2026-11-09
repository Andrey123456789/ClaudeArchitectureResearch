---
paths:
  - "backend/**/*"
  - "frontend/**/*"
---

> Level: 0 Core · Owns: technology-neutral logging principles (sensitive data, payloads, exception logging) · Scope: common · Loads: path rule · Depends on: CLAUDE.md

# Logging Principles

Logging API and provider bindings: `2-technology/logging.md`. Technique: the `logging` skill.

- Never log passwords, access or refresh tokens, private keys, authentication secrets, or full payment credentials. Avoid personal data unless there is a concrete operational need that the project's privacy and security policy permits; prefer stable technical identifiers. A lower log level does not make sensitive data safe.
- Do not serialize arbitrary request bodies, domain objects, or sensitive payloads into logs by default; log the minimum operationally useful, non-sensitive context.
- Log an unexpected exception once, at the boundary that handles it; do not log the same exception again in every layer it passes through (repository, service, entry point, global handler).
