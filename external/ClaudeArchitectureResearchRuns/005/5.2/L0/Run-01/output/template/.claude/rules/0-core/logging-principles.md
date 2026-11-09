---
paths:
  - "backend/**"
  - "frontend/**"
  - "docs/**"
  - ".github/**"
  - "**/*.json"
  - "**/*.yml"
  - "**/*.yaml"
  - "**/*.props"
  - "**/*.targets"
  - "**/*.config"
  - "**/*.csproj"
  - "**/*.slnx"
  - "**/.env*"
  - "**/Dockerfile*"
  - "**/*.ps1"
  - "**/*.sh"
---

> Level: 0 Core | Owns: technology-neutral logging content rules (sensitive data, payloads) | Scope: common | Loads: path | Depends on: none

# Logging Principles

- Never log passwords, access or refresh tokens, private keys, authentication
  secrets, or full payment credentials. Avoid logging PII unless there is a
  concrete operational need that the project's privacy and security policy
  permits. A lower log level does not make sensitive data safe; prefer stable
  technical identifiers over personal data.
- Do not serialize arbitrary request bodies, domain objects, or sensitive
  payloads into logs by default; log the minimum operationally useful,
  non-sensitive context.

Logging API and provider bindings: → `2-technology/logging.md`.
