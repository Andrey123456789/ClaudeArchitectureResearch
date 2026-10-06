# Security

> Shared normalized content pool. Research artifact, not a runtime candidate file.
> Each policy ID must map to exactly one runtime normative owner in every experimental candidate.

Secrets, trust boundaries, SQL safety, authorization, transport security, CORS and sensitive data.

## SEC-001 — Never commit real secrets

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** path
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/rules/security.md#Secrets`

Never hardcode or commit real secrets, credentials, private keys, access/refresh tokens, or production connection strings.

## SEC-002 — Use appropriate secret mechanisms

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/rules/security.md#Secrets`

Use appropriate local secret mechanisms for development and environment-specific injection/managed secret storage for deployed environments; do not assume a cloud provider.

## SEC-003 — Treat external data as untrusted

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/rules/security.md#Input Boundaries`

Treat data crossing the trusted boundary as untrusted and validate it at the owning layer when assumptions matter.

## SEC-004 — Parameterize database access

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/security.md#SQL and Persistence`

Use parameterized database access; never build SQL by concatenating untrusted input.

## SEC-005 — Server authorization is authoritative

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/rules/security.md#Authentication and Authorization`, `templates/v2-baseline/.claude/skills/angular/SKILL.md#Authentication`

Enforce authorization on the server; frontend route guards, hidden buttons and client checks are UX, not a security boundary.

## SEC-006 — Anonymous access is deliberate

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/security.md#Authentication and Authorization`

Anonymous access must be deliberate and visible; avoid redundant authorization attributes when a secure global policy already expresses intent.

## SEC-007 — Protect sensitive transport

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/rules/security.md#HTTPS and Transport Security`

Production traffic carrying credentials or sensitive data must use TLS; respect actual hosting topology and never disable certificate validation to make integration work.

## SEC-008 — Use reviewed cryptography/platform mechanisms

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/security.md#Data Protection and Encryption`

Do not implement custom cryptography when a well-reviewed platform mechanism is appropriate; do not treat ASP.NET Core Data Protection as universal database encryption.

## SEC-009 — CORS is least-permissive for requirements

- **Origin:** v2
- **Strength:** DEFAULT
- **Trigger class:** path
- **Scope:** backend
- **Source:** `templates/v2-baseline/.claude/rules/security.md#CORS`

Configure CORS to the narrowest policy that satisfies actual browser-client requirements; never combine credentialed cross-origin requests with unrestricted origins.

## SEC-010 — Do not log sensitive secrets

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** path
- **Scope:** common
- **Source:** `templates/v2-baseline/.claude/rules/security.md#Logging and Sensitive Data`

Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without a concrete permitted operational need.

## SEC-011 — Cookie auth requires CSRF consideration

- **Origin:** v2
- **Strength:** MUST
- **Trigger class:** path
- **Scope:** frontend
- **Source:** `templates/v2-baseline/.claude/skills/authentication/SKILL.md#Cookie Authentication and CSRF`

When browser cookies automatically carry authentication credentials, include CSRF protection in the design; do not assume an Angular frontend removes the risk.

## SEC-012 — Token storage is threat-model dependent

- **Origin:** v2
- **Strength:** MUST_NOT
- **Trigger class:** path
- **Scope:** frontend
- **Source:** `templates/v2-baseline/.claude/skills/authentication/SKILL.md#Token Storage`

Do not claim one browser token-storage mechanism is universally secure; choose storage according to the application's threat model and never log tokens.
