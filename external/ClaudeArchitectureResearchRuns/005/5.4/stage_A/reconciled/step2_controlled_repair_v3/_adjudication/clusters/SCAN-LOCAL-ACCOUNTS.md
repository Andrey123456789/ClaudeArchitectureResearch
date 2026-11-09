# SCAN-LOCAL-ACCOUNTS (12 records)

## CIS-L0-U0018 (pass 2) L0 .claude/skills/security-scan/references/scan-layers.md:38-38  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When the passwords/accounts investigation prompts apply, examine password hashing during the security scan.
TRIGGER: Applicable account-security surface during a full audit, or relevant targeted authentication review under the parent workflow. | EXC: Irrelevant surfaces are skipped; lockout/brute-force controls are qualified where appropriate. The prompt does not prove a missing control is a vulnerability or mandate an implementation. | POL: ['WF-020']
CODEX WHY: Implementation duties, generic account-layer coverage and actually examining each named concern are related but not identical. The frozen parent instruction may make each list item a review duty, or the list may be illustrative and subsumed. Preserve uncertain; do not infer novelty from same-line label alone.
```
  35  - **Anonymous access:** confirm each deliberately public surface is intentional; a public endpoint is not automatically a vulnerability.
  36  - **Resource authorization / IDOR:** operations such as `GET /orders/{id}`, `PUT /users/{id}`, `DELETE /documents/{id}` where possessing an identifier could expose another user's or tenant's data. Verify ownership,
  37  - **Authentication configuration:** for Bearer/OIDC check issuer, audience where applicable, signature/signing authority, lifetime. Do not require setting every `TokenValidationParameters` property when authority/m
  38> - **Passwords and accounts:** hashing, reset behavior, lockout/brute-force controls where appropriate, account enumeration, credential storage.
  39  - **Angular:** route guards and hidden/disabled buttons are UX; verify the backend protects sensitive operations.
  40  
  41  ## Layer 5: Browser and HTTP/API security (A01, A02)
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L0/constraints.jsonl/RULE-L0-0529 -> FG-L0-f7f7986ea8 [CANONICAL_ONLY] Inspect which surfaces exist and skip irrelevant checks rather than reporting failures; full audits review all applicable layers; targeted changes start with affected layers and ex
- NAMED primary/L0/constraints.jsonl/RULE-L0-0283 -> FG-L0-8761263b08 [CANONICAL_ONLY] With ASP.NET Core Identity use its password hashing, lockout and reset-token features.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0544 -> FG-L0-bd2c887b48 [CANONICAL_ONLY] Flag security-sensitive MD5/SHA1/ECB, hardcoded keys, custom password hashing and home-grown protocols (non-security checksums are fine); passwords use established hashing, never r
- NAMED replica/L0/constraints.jsonl/RULE-L0-0208 -> FG-L0-e9e021edc5 [CANONICAL_ONLY] Never invent exploitability that the code does not establish.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0103 -> FG-L0-d2ce44cdf5 [EXTRA_WORKFLOW] Security review uses seven layers (dependencies, secrets/configuration, injection, authentication/access control, browser/HTTP, sensitive data/logging/errors, exceptional condition
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0101 -> FG-L0-009161dd35 [CANONICAL_ONLY] Never deserialize untrusted payloads into arbitrary runtime types (BinaryFormatter, unsafe TypeNameHandling).

## CIS-L0-U0019 (pass 2) L0 .claude/skills/security-scan/references/scan-layers.md:38-38  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When the passwords/accounts investigation prompts apply, examine password reset behavior during the security scan.
TRIGGER: Applicable account-security surface during a full audit, or relevant targeted authentication review under the parent workflow. | EXC: Irrelevant surfaces are skipped; lockout/brute-force controls are qualified where appropriate. The prompt does not prove a missing control is a vulnerability or mandate an implementation. | POL: ['WF-020']
CODEX WHY: Implementation duties, generic account-layer coverage and actually examining each named concern are related but not identical. The frozen parent instruction may make each list item a review duty, or the list may be illustrative and subsumed. Preserve uncertain; do not infer novelty from same-line label alone.
```
  35  - **Anonymous access:** confirm each deliberately public surface is intentional; a public endpoint is not automatically a vulnerability.
  36  - **Resource authorization / IDOR:** operations such as `GET /orders/{id}`, `PUT /users/{id}`, `DELETE /documents/{id}` where possessing an identifier could expose another user's or tenant's data. Verify ownership,
  37  - **Authentication configuration:** for Bearer/OIDC check issuer, audience where applicable, signature/signing authority, lifetime. Do not require setting every `TokenValidationParameters` property when authority/m
  38> - **Passwords and accounts:** hashing, reset behavior, lockout/brute-force controls where appropriate, account enumeration, credential storage.
  39  - **Angular:** route guards and hidden/disabled buttons are UX; verify the backend protects sensitive operations.
  40  
  41  ## Layer 5: Browser and HTTP/API security (A01, A02)
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L0/constraints.jsonl/RULE-L0-0529 -> FG-L0-f7f7986ea8 [CANONICAL_ONLY] Inspect which surfaces exist and skip irrelevant checks rather than reporting failures; full audits review all applicable layers; targeted changes start with affected layers and ex
- NAMED primary/L0/constraints.jsonl/RULE-L0-0283 -> FG-L0-8761263b08 [CANONICAL_ONLY] With ASP.NET Core Identity use its password hashing, lockout and reset-token features.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0208 -> FG-L0-e9e021edc5 [CANONICAL_ONLY] Never invent exploitability that the code does not establish.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0103 -> FG-L0-d2ce44cdf5 [EXTRA_WORKFLOW] Security review uses seven layers (dependencies, secrets/configuration, injection, authentication/access control, browser/HTTP, sensitive data/logging/errors, exceptional condition
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0101 -> FG-L0-009161dd35 [CANONICAL_ONLY] Never deserialize untrusted payloads into arbitrary runtime types (BinaryFormatter, unsafe TypeNameHandling).

## CIS-L0-U0020 (pass 2) L0 .claude/skills/security-scan/references/scan-layers.md:38-38  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When the passwords/accounts investigation prompts apply, examine lockout/brute-force controls where appropriate during the security scan.
TRIGGER: Applicable account-security surface during a full audit, or relevant targeted authentication review under the parent workflow. | EXC: Irrelevant surfaces are skipped; lockout/brute-force controls are qualified where appropriate. The prompt does not prove a missing control is a vulnerability or mandate an implementation. | POL: ['WF-020']
CODEX WHY: Implementation duties, generic account-layer coverage and actually examining each named concern are related but not identical. The frozen parent instruction may make each list item a review duty, or the list may be illustrative and subsumed. Preserve uncertain; do not infer novelty from same-line label alone.
```
  35  - **Anonymous access:** confirm each deliberately public surface is intentional; a public endpoint is not automatically a vulnerability.
  36  - **Resource authorization / IDOR:** operations such as `GET /orders/{id}`, `PUT /users/{id}`, `DELETE /documents/{id}` where possessing an identifier could expose another user's or tenant's data. Verify ownership,
  37  - **Authentication configuration:** for Bearer/OIDC check issuer, audience where applicable, signature/signing authority, lifetime. Do not require setting every `TokenValidationParameters` property when authority/m
  38> - **Passwords and accounts:** hashing, reset behavior, lockout/brute-force controls where appropriate, account enumeration, credential storage.
  39  - **Angular:** route guards and hidden/disabled buttons are UX; verify the backend protects sensitive operations.
  40  
  41  ## Layer 5: Browser and HTTP/API security (A01, A02)
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L0/constraints.jsonl/RULE-L0-0529 -> FG-L0-f7f7986ea8 [CANONICAL_ONLY] Inspect which surfaces exist and skip irrelevant checks rather than reporting failures; full audits review all applicable layers; targeted changes start with affected layers and ex
- NAMED primary/L0/constraints.jsonl/RULE-L0-0283 -> FG-L0-8761263b08 [CANONICAL_ONLY] With ASP.NET Core Identity use its password hashing, lockout and reset-token features.
- NAMED primary/L0/constraints.jsonl/EXTRA-L0-0176 -> FG-L0-184b815400 [EXTRA_WORKFLOW] Consider rate limiting where abuse realistically matters (login/reset, expensive anonymous or resource-intensive endpoints), not on every endpoint.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0208 -> FG-L0-e9e021edc5 [CANONICAL_ONLY] Never invent exploitability that the code does not establish.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0103 -> FG-L0-d2ce44cdf5 [EXTRA_WORKFLOW] Security review uses seven layers (dependencies, secrets/configuration, injection, authentication/access control, browser/HTTP, sensitive data/logging/errors, exceptional condition
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0101 -> FG-L0-009161dd35 [CANONICAL_ONLY] Never deserialize untrusted payloads into arbitrary runtime types (BinaryFormatter, unsafe TypeNameHandling).

## CIS-L0-U0021 (pass 2) L0 .claude/skills/security-scan/references/scan-layers.md:38-38  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When the passwords/accounts investigation prompts apply, examine account enumeration during the security scan.
TRIGGER: Applicable account-security surface during a full audit, or relevant targeted authentication review under the parent workflow. | EXC: Irrelevant surfaces are skipped; lockout/brute-force controls are qualified where appropriate. The prompt does not prove a missing control is a vulnerability or mandate an implementation. | POL: ['WF-020']
CODEX WHY: Implementation duties, generic account-layer coverage and actually examining each named concern are related but not identical. The frozen parent instruction may make each list item a review duty, or the list may be illustrative and subsumed. Preserve uncertain; do not infer novelty from same-line label alone.
```
  35  - **Anonymous access:** confirm each deliberately public surface is intentional; a public endpoint is not automatically a vulnerability.
  36  - **Resource authorization / IDOR:** operations such as `GET /orders/{id}`, `PUT /users/{id}`, `DELETE /documents/{id}` where possessing an identifier could expose another user's or tenant's data. Verify ownership,
  37  - **Authentication configuration:** for Bearer/OIDC check issuer, audience where applicable, signature/signing authority, lifetime. Do not require setting every `TokenValidationParameters` property when authority/m
  38> - **Passwords and accounts:** hashing, reset behavior, lockout/brute-force controls where appropriate, account enumeration, credential storage.
  39  - **Angular:** route guards and hidden/disabled buttons are UX; verify the backend protects sensitive operations.
  40  
  41  ## Layer 5: Browser and HTTP/API security (A01, A02)
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L0/constraints.jsonl/RULE-L0-0529 -> FG-L0-f7f7986ea8 [CANONICAL_ONLY] Inspect which surfaces exist and skip irrelevant checks rather than reporting failures; full audits review all applicable layers; targeted changes start with affected layers and ex
- NAMED primary/L0/constraints.jsonl/RULE-L0-0076 -> FG-L0-97502ad9f6 [CANONICAL_ONLY] Do not expose authentication-failure detail revealing secrets or account state; avoid account-enumeration leaks.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0208 -> FG-L0-e9e021edc5 [CANONICAL_ONLY] Never invent exploitability that the code does not establish.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0103 -> FG-L0-d2ce44cdf5 [EXTRA_WORKFLOW] Security review uses seven layers (dependencies, secrets/configuration, injection, authentication/access control, browser/HTTP, sensitive data/logging/errors, exceptional condition
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0101 -> FG-L0-009161dd35 [CANONICAL_ONLY] Never deserialize untrusted payloads into arbitrary runtime types (BinaryFormatter, unsafe TypeNameHandling).

## CIS-L0-U0022 (pass 2) L0 .claude/skills/security-scan/references/scan-layers.md:38-38  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When the passwords/accounts investigation prompts apply, examine credential storage during the security scan.
TRIGGER: Applicable account-security surface during a full audit, or relevant targeted authentication review under the parent workflow. | EXC: Irrelevant surfaces are skipped; lockout/brute-force controls are qualified where appropriate. The prompt does not prove a missing control is a vulnerability or mandate an implementation. | POL: ['WF-020']
CODEX WHY: Implementation duties, generic account-layer coverage and actually examining each named concern are related but not identical. The frozen parent instruction may make each list item a review duty, or the list may be illustrative and subsumed. Preserve uncertain; do not infer novelty from same-line label alone.
```
  35  - **Anonymous access:** confirm each deliberately public surface is intentional; a public endpoint is not automatically a vulnerability.
  36  - **Resource authorization / IDOR:** operations such as `GET /orders/{id}`, `PUT /users/{id}`, `DELETE /documents/{id}` where possessing an identifier could expose another user's or tenant's data. Verify ownership,
  37  - **Authentication configuration:** for Bearer/OIDC check issuer, audience where applicable, signature/signing authority, lifetime. Do not require setting every `TokenValidationParameters` property when authority/m
  38> - **Passwords and accounts:** hashing, reset behavior, lockout/brute-force controls where appropriate, account enumeration, credential storage.
  39  - **Angular:** route guards and hidden/disabled buttons are UX; verify the backend protects sensitive operations.
  40  
  41  ## Layer 5: Browser and HTTP/API security (A01, A02)
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L0/constraints.jsonl/RULE-L0-0529 -> FG-L0-f7f7986ea8 [CANONICAL_ONLY] Inspect which surfaces exist and skip irrelevant checks rather than reporting failures; full audits review all applicable layers; targeted changes start with affected layers and ex
- NAMED primary/L0/constraints.jsonl/RULE-L0-0554 -> FG-L0-e99ede61e8 [CANONICAL_ONLY] Data at rest by requirement: one-way password hashing, hashes for verification tokens, protected storage for retrievable secrets, platform storage encryption, Data Protection for t
- NAMED primary/L0/constraints.jsonl/RULE-L0-0086 -> FG-L0-831bd62c59 [CANONICAL_ONLY] Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid personal data without a permitted operational need, prefer stable technical identifiers; 
- NAMED replica/L0/constraints.jsonl/RULE-L0-0208 -> FG-L0-e9e021edc5 [CANONICAL_ONLY] Never invent exploitability that the code does not establish.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0103 -> FG-L0-d2ce44cdf5 [EXTRA_WORKFLOW] Security review uses seven layers (dependencies, secrets/configuration, injection, authentication/access control, browser/HTTP, sensitive data/logging/errors, exceptional condition
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0101 -> FG-L0-009161dd35 [CANONICAL_ONLY] Never deserialize untrusted payloads into arbitrary runtime types (BinaryFormatter, unsafe TypeNameHandling).

## CIS-L1-U0040 (pass 3) L1 .claude/skills/security-scan/references/scan-layers.md:37-37  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During an applicable security scan, review credential storage in local-account implementations.
TRIGGER: The corresponding surface exists and the scan covers that layer | EXC: Investigation prompts, not automatic vulnerability declarations; assess actual behavior and contextual risk. No requirement to add controls or logs everywhere. | POL: ['WF-020']
CODEX WHY: Concrete review activity can be omitted while complying with general security invariants. Distinct from own source/lock/debug findings; investigation-prompt force remains uncertain.
```
  34  - **Anonymous access** — confirm public surfaces are intentional; a public endpoint is not automatically a vulnerability.
  35  - **Resource authorization / IDOR** — `GET /orders/{id}`, `PUT /users/{id}`, `DELETE /documents/{id}` where possessing an identifier could expose another user's or tenant's data; verify ownership, tenant, or permis
  36  - **Authentication configuration** — for Bearer/OIDC, check issuer, audience where applicable, signature/signing authority, lifetime. Do not demand every `TokenValidationParameters` property when authority metadata
  37> - **Local accounts** — password hashing, reset behavior, lockout/brute-force controls where appropriate, account enumeration, credential storage.
  38  - **Frontend** — route guards and hidden/disabled buttons are UX; verify the backend protects sensitive operations.
  39  
  40  ## Layer 5: Browser and HTTP/API security (A01, A02)
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L1/constraints.jsonl/RULE-L1-0551 -> FG-L1-e52b9bf6fd [CANONICAL_ONLY] Full pre-release or requested audits review all applicable layers; targeted changes start with affected layers and expand across security boundaries.
- NAMED primary/L1/constraints.jsonl/RULE-L1-0564 -> FG-L1-844366a741 [CANONICAL_ONLY] Do not report patterns without context (LINQ predicates with user input, query parameters as SSRF without host influence, ordinary template binding as XSS, returned entities withou
- NAMED primary/L1/constraints.jsonl/RULE-L1-0574 -> FG-L1-5821a256da [CANONICAL_ONLY] Check logs for never-log data, PII per requirements; Debug/Trace is not a boundary; no demand to log every successful request.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0108 -> FG-L1-15d9f150d9 [CANONICAL_ONLY] Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without permitted need; log level is not a privacy control.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0109 -> FG-L1-c4e1401ee1 [CANONICAL_ONLY] Do not serialize arbitrary request bodies, domain objects or sensitive payloads into logs by default; log the minimum operationally useful non-sensitive context.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0135 -> FG-L1-d6ab123b1f [CANONICAL_ONLY] Review for unsafe deserialization: BinaryFormatter, unsafe TypeNameHandling, deserializing untrusted payloads into arbitrary runtime types (reported as possibly illustrative).
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0137 -> FG-L1-accce90761 [CANONICAL_ONLY] Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED.

## CIS-K0-U0022 (pass 2) K0 .claude/skills/security-scan/references/scan-layers.md:107-107  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When a security scan includes an application that owns local accounts, review password hashing.
TRIGGER: Applying the authentication/account layer of security-scan to an application owning local accounts; targeted versus full-scan applicability follows the parent workflow. | EXC: Lockout/brute-force review is qualified by where appropriate; the prompt does not mandate a particular mechanism or assert that its absence proves a vulnerability. | POL: ['SEC-016', 'WF-020']
CODEX WHY: The five targets in one sentence can be reviewed or omitted independently. Same-line generic account-review labels do not settle separate registration or normative force. Implementation correctness and actually reviewing it are different actions, but general inspect-applicable-layers coverage might subsume the procedural detail. Preserved uncertain instead of declaring five verified discoveries.
```
 104  
 105  ## Passwords and accounts
 106  
 107> When the application owns local accounts, review password hashing, password reset behavior, lockout/brute-force controls where appropriate, account-enumeration behavior and credential storage.
 108  
 109  ## Angular
 110  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/K0/constraints.jsonl/RULE-K0-0263 -> FG-K0-ab8cd7097b [CANONICAL_ONLY] When the application owns passwords rely on Identity's password hashing, lockout, reset tokens and related features.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0526 -> FG-K0-1413440458 [CANONICAL_ONLY] Security-sensitive MD5/SHA1/ECB, hardcoded keys, custom hashing and home-grown protocols are flagged (not non-security checksums); passwords use established password-hashing facili
- NAMED primary/K0/constraints.jsonl/RULE-K0-0535 -> FG-K0-dc460058ce [CANONICAL_ONLY] Match data-at-rest protection to the requirement: one-way hashing for passwords, usually hashing for verification-only tokens, protected storage for retrievable secrets, platform/d
- NAMED replica/K0/constraints.jsonl/RULE-K0-0280 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0096 -> FG-K0-c71ea3954c [CANONICAL_ONLY] No custom token/password security, password hashing or reset-token cryptography when ASP.NET Core authentication or Identity covers the requirement.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0007 -> FG-K0-0ef1e5ed3d [EXTRA_WORKFLOW] A security scan investigates polymorphic or type-driven deserialization such as BinaryFormatter or unsafe TypeNameHandling; its audit criterion is that untrusted payloads are not d
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0057 -> FG-K0-ab8cd7097b [CANONICAL_ONLY] When the application owns passwords rely on Identity's password hashing, lockout, reset tokens and related features.

## CIS-K0-U0023 (pass 2) K0 .claude/skills/security-scan/references/scan-layers.md:107-107  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When a security scan includes an application that owns local accounts, review password reset behavior.
TRIGGER: Applying the authentication/account layer of security-scan to an application owning local accounts; targeted versus full-scan applicability follows the parent workflow. | EXC: Lockout/brute-force review is qualified by where appropriate; the prompt does not mandate a particular mechanism or assert that its absence proves a vulnerability. | POL: ['SEC-016', 'WF-020']
CODEX WHY: The five targets in one sentence can be reviewed or omitted independently. Same-line generic account-review labels do not settle separate registration or normative force. Implementation correctness and actually reviewing it are different actions, but general inspect-applicable-layers coverage might subsume the procedural detail. Preserved uncertain instead of declaring five verified discoveries.
```
 104  
 105  ## Passwords and accounts
 106  
 107> When the application owns local accounts, review password hashing, password reset behavior, lockout/brute-force controls where appropriate, account-enumeration behavior and credential storage.
 108  
 109  ## Angular
 110  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/K0/constraints.jsonl/RULE-K0-0263 -> FG-K0-ab8cd7097b [CANONICAL_ONLY] When the application owns passwords rely on Identity's password hashing, lockout, reset tokens and related features.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0221 -> FG-K0-ed347bd7d1 [EXTRA_WORKFLOW] Consider rate limiting where abuse realistically matters (login, password reset, expensive anonymous or resource-intensive endpoints), not on every endpoint.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0280 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0096 -> FG-K0-c71ea3954c [CANONICAL_ONLY] No custom token/password security, password hashing or reset-token cryptography when ASP.NET Core authentication or Identity covers the requirement.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0007 -> FG-K0-0ef1e5ed3d [EXTRA_WORKFLOW] A security scan investigates polymorphic or type-driven deserialization such as BinaryFormatter or unsafe TypeNameHandling; its audit criterion is that untrusted payloads are not d
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0057 -> FG-K0-ab8cd7097b [CANONICAL_ONLY] When the application owns passwords rely on Identity's password hashing, lockout, reset tokens and related features.

## CIS-K0-U0024 (pass 2) K0 .claude/skills/security-scan/references/scan-layers.md:107-107  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When a security scan includes an application that owns local accounts, review lockout/brute-force controls where appropriate.
TRIGGER: Applying the authentication/account layer of security-scan to an application owning local accounts; targeted versus full-scan applicability follows the parent workflow. | EXC: Lockout/brute-force review is qualified by where appropriate; the prompt does not mandate a particular mechanism or assert that its absence proves a vulnerability. | POL: ['WF-020']
CODEX WHY: The five targets in one sentence can be reviewed or omitted independently. Same-line generic account-review labels do not settle separate registration or normative force. Implementation correctness and actually reviewing it are different actions, but general inspect-applicable-layers coverage might subsume the procedural detail. Preserved uncertain instead of declaring five verified discoveries.
```
 104  
 105  ## Passwords and accounts
 106  
 107> When the application owns local accounts, review password hashing, password reset behavior, lockout/brute-force controls where appropriate, account-enumeration behavior and credential storage.
 108  
 109  ## Angular
 110  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/K0/constraints.jsonl/RULE-K0-0263 -> FG-K0-ab8cd7097b [CANONICAL_ONLY] When the application owns passwords rely on Identity's password hashing, lockout, reset tokens and related features.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0221 -> FG-K0-ed347bd7d1 [EXTRA_WORKFLOW] Consider rate limiting where abuse realistically matters (login, password reset, expensive anonymous or resource-intensive endpoints), not on every endpoint.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0280 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0096 -> FG-K0-c71ea3954c [CANONICAL_ONLY] No custom token/password security, password hashing or reset-token cryptography when ASP.NET Core authentication or Identity covers the requirement.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0007 -> FG-K0-0ef1e5ed3d [EXTRA_WORKFLOW] A security scan investigates polymorphic or type-driven deserialization such as BinaryFormatter or unsafe TypeNameHandling; its audit criterion is that untrusted payloads are not d
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0057 -> FG-K0-ab8cd7097b [CANONICAL_ONLY] When the application owns passwords rely on Identity's password hashing, lockout, reset tokens and related features.

## CIS-K0-U0025 (pass 2) K0 .claude/skills/security-scan/references/scan-layers.md:107-107  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When a security scan includes an application that owns local accounts, review account-enumeration behavior.
TRIGGER: Applying the authentication/account layer of security-scan to an application owning local accounts; targeted versus full-scan applicability follows the parent workflow. | EXC: Lockout/brute-force review is qualified by where appropriate; the prompt does not mandate a particular mechanism or assert that its absence proves a vulnerability. | POL: ['WF-020']
CODEX WHY: The five targets in one sentence can be reviewed or omitted independently. Same-line generic account-review labels do not settle separate registration or normative force. Implementation correctness and actually reviewing it are different actions, but general inspect-applicable-layers coverage might subsume the procedural detail. Preserved uncertain instead of declaring five verified discoveries.
```
 104  
 105  ## Passwords and accounts
 106  
 107> When the application owns local accounts, review password hashing, password reset behavior, lockout/brute-force controls where appropriate, account-enumeration behavior and credential storage.
 108  
 109  ## Angular
 110  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/K0/constraints.jsonl/RULE-K0-0159 -> FG-K0-b1d048d2b9 [CANONICAL_ONLY] Authentication failures never expose detail that reveals secrets or account state; login avoids account-enumeration leaks where relevant.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0280 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0098 -> FG-K0-b1d048d2b9 [CANONICAL_ONLY] Authentication failures never expose detail that reveals secrets or account state; login avoids account-enumeration leaks where relevant.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0007 -> FG-K0-0ef1e5ed3d [EXTRA_WORKFLOW] A security scan investigates polymorphic or type-driven deserialization such as BinaryFormatter or unsafe TypeNameHandling; its audit criterion is that untrusted payloads are not d
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0057 -> FG-K0-ab8cd7097b [CANONICAL_ONLY] When the application owns passwords rely on Identity's password hashing, lockout, reset tokens and related features.

## CIS-K0-U0026 (pass 2) K0 .claude/skills/security-scan/references/scan-layers.md:107-107  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When a security scan includes an application that owns local accounts, review credential storage.
TRIGGER: Applying the authentication/account layer of security-scan to an application owning local accounts; targeted versus full-scan applicability follows the parent workflow. | EXC: Lockout/brute-force review is qualified by where appropriate; the prompt does not mandate a particular mechanism or assert that its absence proves a vulnerability. | POL: ['SEC-001', 'WF-020']
CODEX WHY: The five targets in one sentence can be reviewed or omitted independently. Same-line generic account-review labels do not settle separate registration or normative force. Implementation correctness and actually reviewing it are different actions, but general inspect-applicable-layers coverage might subsume the procedural detail. Preserved uncertain instead of declaring five verified discoveries.
```
 104  
 105  ## Passwords and accounts
 106  
 107> When the application owns local accounts, review password hashing, password reset behavior, lockout/brute-force controls where appropriate, account-enumeration behavior and credential storage.
 108  
 109  ## Angular
 110  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/K0/constraints.jsonl/RULE-K0-0059 -> FG-K0-8194fcc423 [CANONICAL_ONLY] Never hardcode or commit real secrets, credentials, private keys, access/refresh tokens or production connection strings in source-controlled files, example configuration included.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0535 -> FG-K0-dc460058ce [CANONICAL_ONLY] Match data-at-rest protection to the requirement: one-way hashing for passwords, usually hashing for verification-only tokens, protected storage for retrievable secrets, platform/d
- NAMED replica/K0/constraints.jsonl/RULE-K0-0280 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0120 -> FG-K0-8194fcc423 [CANONICAL_ONLY] Never hardcode or commit real secrets, credentials, private keys, access/refresh tokens or production connection strings in source-controlled files, example configuration included.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0007 -> FG-K0-0ef1e5ed3d [EXTRA_WORKFLOW] A security scan investigates polymorphic or type-driven deserialization such as BinaryFormatter or unsafe TypeNameHandling; its audit criterion is that untrusted payloads are not d
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0057 -> FG-K0-ab8cd7097b [CANONICAL_ONLY] When the application owns passwords rely on Identity's password hashing, lockout, reset tokens and related features.

## CIS-K1-U0036 (pass 3) K1 .claude/skills/security-scan/references/scan-layers.md:97-97  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During applicable authentication/account review when the application owns local accounts, review credential storage.
TRIGGER: authentication/account review when the application owns local accounts within a requested scan; full audits cover applicable layers, targeted scans focus affected surfaces. | EXC: Investigation only, not an automatic vulnerability declaration or mandatory product change. Severity depends on actual exposure; ordinary query parameters do not automatically imply SSRF, and successf | POL: ['WF-020']
CODEX WHY: A specific investigation can be omitted while other items in the same layer are reviewed. Whether the baseline general review obligation incorporates every prompt remains unresolved. Prior rejected labels are not accepted as normative truth.
```
  94  
  95  ## Passwords and accounts
  96  
  97> When the application owns local accounts, review password hashing, reset behavior, lockout/brute-force controls where appropriate, account-enumeration behavior, and credential storage. Never recommend custom passwo
  98  
  99  ## Frontend
 100  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K1-cc23871b3f [97, 97] CANONICAL_ONLY/MUST_NOT pol=['SEC-016'] rel=[]: No custom token/password security, password hashing or reset-token cryptography when ASP.NET Core authentication/Identity covers the requirement.
- V2 FG-K1-8e0b256c02 [97, 97] CANONICAL_ONLY/MUST pol=['SEC-016', 'SEC-018'] rel=[]: Review local-account hashing, reset, lockout and enumeration behaviour; never recommend custom password hashing.
- V2 FG-K1-bd7c36ea22 [97, 97] EXTRA_WORKFLOW/DEFAULT pol=[] rel=['SEC-018', 'WF-020']: Account brute-force controls are inspected.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0541 -> FG-K1-8e0b256c02 [CANONICAL_ONLY] Review local-account hashing, reset, lockout and enumeration behaviour; never recommend custom password hashing.
- NAMED replica/K1/constraints.jsonl/RULE-K1-0317 -> FG-K1-f0aca49ccf [CANONICAL_PLUS_DELTA] The scan is complete only when applicable layers were inspected, findings have evidence, uncertain findings are labelled and limitations are stated.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0003 -> FG-K1-045154787f [EXTRA_WORKFLOW] Consider rate limiting where abuse realistically matters (login/password reset, expensive anonymous endpoints, resource-intensive operations); do not require it on every endpoint.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0006 -> FG-K1-ba3da08dba [CANONICAL_ONLY] A full pre-release or requested audit reviews all applicable layers; a targeted change focuses on affected layers and expands when it crosses security boundaries.
