# SCAN-SECRETS-CONFIG (9 records)

## CIS-L0-U0042 (pass 3) L0 .claude/skills/security-scan/references/scan-layers.md:20-20  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During applicable secrets/configuration review, investigate production debug/development flags.
TRIGGER: applicable secrets/configuration review when that surface exists; full audits cover applicable layers and targeted reviews expand with security boundaries. | EXC: Investigation prompt, not automatic vulnerability declaration, required code change, ban on every configuration value or mandate to add upload controls. Severity and applicability remain contextual. | POL: ['WF-020']
CODEX WHY: Exact source instruction/list item is plausible independently checkable review content, yet general full-layer coverage and incorporation by reference provide serious equivalence counterevidence. Preserve uncertain.
```
  17  - Indicators that need context: `ApiKey = "..."`, `Secret = "..."`, `Token = "..."`, `Password = "..."`, long opaque strings, connection strings, certificate material.
  18  - A real committed secret is a secret regardless of the file name; `appsettings.Development.json` is not exempt. Obviously fake values (`changeme`, `example-only`, `test-password`, `not-a-real-key`) may be ignored 
  19  - Preferred pattern: `builder.Configuration.GetConnectionString("Default")` with the real value from the chosen local or deployment secret mechanism.
  20> - Also review production debug/development flags, certificate-validation bypass, insecure URLs carrying credentials, verbose production error configuration, and committed `.env` files.
  21  
  22  ## Layer 3: Injection and dangerous patterns (A04, A05, A08)
  23  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 NCP-L0-0001 [20, 20] EXTRA_WORKFLOW/DEFAULT pol=[] rel=['SEC-001', 'SEC-007', 'API-008']: During a security scan also review production debug or development flags, certificate-validation bypass, insecure URLs carrying credentials, verbose production error configuration, and committed .env files.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0529 -> FG-L0-f7f7986ea8 [CANONICAL_ONLY] Inspect which surfaces exist and skip irrelevant checks rather than reporting failures; full audits review all applicable layers; targeted changes start with affected layers and ex
- NAMED primary/L0/constraints.jsonl/RULE-L0-0540 -> FG-L0-5106f13e4b [CANONICAL_ONLY] A committed real secret is a secret regardless of file name (appsettings.Development.json not exempt); obviously fake values may be ignored or Info; UserSecretsId is not a secret.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0552 -> FG-L0-131120755c [CANONICAL_ONLY] Review disabled certificate validation, accept-all callbacks and plain HTTP; account for TLS termination; missing HTTPS redirection is not automatically a vulnerability.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0558 -> FG-L0-f35ced143f [CANONICAL_ONLY] Do not map pattern, CVSS or OWASP category to severity mechanically; judge whether an attacker can actually exploit unbounded resources.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0559 -> FG-L0-e6cdfa2340 [CANONICAL_ONLY] Review startup/configuration failure for dangerous fallback (auth disabled, plaintext mode, allow-all).
- NAMED replica/L0/constraints.jsonl/RULE-L0-0045 -> FG-L0-fc7ca2f4bb [CANONICAL_ONLY] Treat data crossing the trusted boundary (requests, uploads, external responses, messages, user identifiers/filters) as untrusted and validate it at the owning layer when assumptio
- NAMED replica/L0/constraints.jsonl/RULE-L0-0046 -> FG-L0-a9aba1bf8a [CANONICAL_ONLY] Do not trust client-provided file metadata such as MIME type as authoritative when handling or security decisions depend on content.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0208 -> FG-L0-e9e021edc5 [CANONICAL_ONLY] Never invent exploitability that the code does not establish.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0103 -> FG-L0-d2ce44cdf5 [EXTRA_WORKFLOW] Security review uses seven layers (dependencies, secrets/configuration, injection, authentication/access control, browser/HTTP, sensitive data/logging/errors, exceptional condition

## CIS-L0-U0043 (pass 3) L0 .claude/skills/security-scan/references/scan-layers.md:20-20  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During applicable secrets/configuration review, investigate verbose production error configuration.
TRIGGER: applicable secrets/configuration review when that surface exists; full audits cover applicable layers and targeted reviews expand with security boundaries. | EXC: Investigation prompt, not automatic vulnerability declaration, required code change, ban on every configuration value or mandate to add upload controls. Severity and applicability remain contextual. | POL: ['WF-020']
CODEX WHY: Exact source instruction/list item is plausible independently checkable review content, yet general full-layer coverage and incorporation by reference provide serious equivalence counterevidence. Preserve uncertain.
```
  17  - Indicators that need context: `ApiKey = "..."`, `Secret = "..."`, `Token = "..."`, `Password = "..."`, long opaque strings, connection strings, certificate material.
  18  - A real committed secret is a secret regardless of the file name; `appsettings.Development.json` is not exempt. Obviously fake values (`changeme`, `example-only`, `test-password`, `not-a-real-key`) may be ignored 
  19  - Preferred pattern: `builder.Configuration.GetConnectionString("Default")` with the real value from the chosen local or deployment secret mechanism.
  20> - Also review production debug/development flags, certificate-validation bypass, insecure URLs carrying credentials, verbose production error configuration, and committed `.env` files.
  21  
  22  ## Layer 3: Injection and dangerous patterns (A04, A05, A08)
  23  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 NCP-L0-0001 [20, 20] EXTRA_WORKFLOW/DEFAULT pol=[] rel=['SEC-001', 'SEC-007', 'API-008']: During a security scan also review production debug or development flags, certificate-validation bypass, insecure URLs carrying credentials, verbose production error configuration, and committed .env files.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0529 -> FG-L0-f7f7986ea8 [CANONICAL_ONLY] Inspect which surfaces exist and skip irrelevant checks rather than reporting failures; full audits review all applicable layers; targeted changes start with affected layers and ex
- NAMED primary/L0/constraints.jsonl/RULE-L0-0540 -> FG-L0-5106f13e4b [CANONICAL_ONLY] A committed real secret is a secret regardless of file name (appsettings.Development.json not exempt); obviously fake values may be ignored or Info; UserSecretsId is not a secret.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0552 -> FG-L0-131120755c [CANONICAL_ONLY] Review disabled certificate validation, accept-all callbacks and plain HTTP; account for TLS termination; missing HTTPS redirection is not automatically a vulnerability.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0558 -> FG-L0-f35ced143f [CANONICAL_ONLY] Do not map pattern, CVSS or OWASP category to severity mechanically; judge whether an attacker can actually exploit unbounded resources.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0559 -> FG-L0-e6cdfa2340 [CANONICAL_ONLY] Review startup/configuration failure for dangerous fallback (auth disabled, plaintext mode, allow-all).
- NAMED replica/L0/constraints.jsonl/RULE-L0-0045 -> FG-L0-fc7ca2f4bb [CANONICAL_ONLY] Treat data crossing the trusted boundary (requests, uploads, external responses, messages, user identifiers/filters) as untrusted and validate it at the owning layer when assumptio
- NAMED replica/L0/constraints.jsonl/RULE-L0-0046 -> FG-L0-a9aba1bf8a [CANONICAL_ONLY] Do not trust client-provided file metadata such as MIME type as authoritative when handling or security decisions depend on content.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0208 -> FG-L0-e9e021edc5 [CANONICAL_ONLY] Never invent exploitability that the code does not establish.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0103 -> FG-L0-d2ce44cdf5 [EXTRA_WORKFLOW] Security review uses seven layers (dependencies, secrets/configuration, injection, authentication/access control, browser/HTTP, sensitive data/logging/errors, exceptional condition

## CIS-L0-U0044 (pass 3) L0 .claude/skills/security-scan/references/scan-layers.md:20-20  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During applicable secrets/configuration review, investigate committed .env files.
TRIGGER: applicable secrets/configuration review when that surface exists; full audits cover applicable layers and targeted reviews expand with security boundaries. | EXC: Investigation prompt, not automatic vulnerability declaration, required code change, ban on every configuration value or mandate to add upload controls. Severity and applicability remain contextual. | POL: ['WF-020']
CODEX WHY: Exact source instruction/list item is plausible independently checkable review content, yet general full-layer coverage and incorporation by reference provide serious equivalence counterevidence. Preserve uncertain.
```
  17  - Indicators that need context: `ApiKey = "..."`, `Secret = "..."`, `Token = "..."`, `Password = "..."`, long opaque strings, connection strings, certificate material.
  18  - A real committed secret is a secret regardless of the file name; `appsettings.Development.json` is not exempt. Obviously fake values (`changeme`, `example-only`, `test-password`, `not-a-real-key`) may be ignored 
  19  - Preferred pattern: `builder.Configuration.GetConnectionString("Default")` with the real value from the chosen local or deployment secret mechanism.
  20> - Also review production debug/development flags, certificate-validation bypass, insecure URLs carrying credentials, verbose production error configuration, and committed `.env` files.
  21  
  22  ## Layer 3: Injection and dangerous patterns (A04, A05, A08)
  23  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 NCP-L0-0001 [20, 20] EXTRA_WORKFLOW/DEFAULT pol=[] rel=['SEC-001', 'SEC-007', 'API-008']: During a security scan also review production debug or development flags, certificate-validation bypass, insecure URLs carrying credentials, verbose production error configuration, and committed .env files.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0529 -> FG-L0-f7f7986ea8 [CANONICAL_ONLY] Inspect which surfaces exist and skip irrelevant checks rather than reporting failures; full audits review all applicable layers; targeted changes start with affected layers and ex
- NAMED primary/L0/constraints.jsonl/RULE-L0-0540 -> FG-L0-5106f13e4b [CANONICAL_ONLY] A committed real secret is a secret regardless of file name (appsettings.Development.json not exempt); obviously fake values may be ignored or Info; UserSecretsId is not a secret.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0552 -> FG-L0-131120755c [CANONICAL_ONLY] Review disabled certificate validation, accept-all callbacks and plain HTTP; account for TLS termination; missing HTTPS redirection is not automatically a vulnerability.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0558 -> FG-L0-f35ced143f [CANONICAL_ONLY] Do not map pattern, CVSS or OWASP category to severity mechanically; judge whether an attacker can actually exploit unbounded resources.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0559 -> FG-L0-e6cdfa2340 [CANONICAL_ONLY] Review startup/configuration failure for dangerous fallback (auth disabled, plaintext mode, allow-all).
- NAMED replica/L0/constraints.jsonl/RULE-L0-0045 -> FG-L0-fc7ca2f4bb [CANONICAL_ONLY] Treat data crossing the trusted boundary (requests, uploads, external responses, messages, user identifiers/filters) as untrusted and validate it at the owning layer when assumptio
- NAMED replica/L0/constraints.jsonl/RULE-L0-0046 -> FG-L0-a9aba1bf8a [CANONICAL_ONLY] Do not trust client-provided file metadata such as MIME type as authoritative when handling or security decisions depend on content.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0208 -> FG-L0-e9e021edc5 [CANONICAL_ONLY] Never invent exploitability that the code does not establish.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0103 -> FG-L0-d2ce44cdf5 [EXTRA_WORKFLOW] Security review uses seven layers (dependencies, secrets/configuration, injection, authentication/access control, browser/HTTP, sensitive data/logging/errors, exceptional condition

## CIS-L1-U0036 (pass 3) L1 .claude/skills/security-scan/references/scan-layers.md:19-19  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During an applicable security scan, review verbose production error configuration.
TRIGGER: The corresponding surface exists and the scan covers that layer | EXC: Investigation prompts, not automatic vulnerability declarations; assess actual behavior and contextual risk. No requirement to add controls or logs everywhere. | POL: ['WF-020']
CODEX WHY: Concrete review activity can be omitted while complying with general security invariants. Distinct from own source/lock/debug findings; investigation-prompt force remains uncertain.
```
  16  - High-confidence indicators: private keys, real access/refresh tokens, cloud access keys, database passwords, API secrets, service-account credentials, production connection strings with credentials.
  17  - Context-dependent: `ApiKey = "..."`, `Secret = "..."`, `Token = "..."`, `Password = "..."`, long opaque strings, connection strings, certificate material.
  18  - Do not ignore `appsettings.Development.json` automatically; obviously fake values (`changeme`, `example-only`, `test-password`, `not-a-real-key`) may be ignored or reported as Info. `UserSecretsId` is not a secre
  19> - Also review production debug/development flags, certificate-validation bypasses, URLs carrying credentials, verbose production error configuration, committed `.env` files.
  20  
  21  ## Layer 3: Injection and dangerous code patterns (A04, A05, A08)
  22  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 AUG1-NC-CIS-L1-0009-a [19, 19] EXTRA_WORKFLOW/DEFAULT pol=[] rel=['WF-020']: Review production debug/development flags as part of the secrets and configuration layer of a security scan.
- NAMED primary/L1/constraints.jsonl/RULE-L1-0551 -> FG-L1-e52b9bf6fd [CANONICAL_ONLY] Full pre-release or requested audits review all applicable layers; targeted changes start with affected layers and expand across security boundaries.
- NAMED primary/L1/constraints.jsonl/RULE-L1-0564 -> FG-L1-844366a741 [CANONICAL_ONLY] Do not report patterns without context (LINQ predicates with user input, query parameters as SSRF without host influence, ordinary template binding as XSS, returned entities withou
- NAMED primary/L1/constraints.jsonl/RULE-L1-0574 -> FG-L1-5821a256da [CANONICAL_ONLY] Check logs for never-log data, PII per requirements; Debug/Trace is not a boundary; no demand to log every successful request.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0108 -> FG-L1-15d9f150d9 [CANONICAL_ONLY] Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without permitted need; log level is not a privacy control.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0109 -> FG-L1-c4e1401ee1 [CANONICAL_ONLY] Do not serialize arbitrary request bodies, domain objects or sensitive payloads into logs by default; log the minimum operationally useful non-sensitive context.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0135 -> FG-L1-d6ab123b1f [CANONICAL_ONLY] Review for unsafe deserialization: BinaryFormatter, unsafe TypeNameHandling, deserializing untrusted payloads into arbitrary runtime types (reported as possibly illustrative).
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0137 -> FG-L1-accce90761 [CANONICAL_ONLY] Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED.
- PASS1 CIS-L1-0009 DISTINCT_UNREPRESENTED_CLAUSE [19, 19]: Review production debug or development flags in the secrets and configuration layer of a security scan.

## CIS-L1-U0037 (pass 3) L1 .claude/skills/security-scan/references/scan-layers.md:19-19  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During an applicable security scan, review committed .env files.
TRIGGER: The corresponding surface exists and the scan covers that layer | EXC: Investigation prompts, not automatic vulnerability declarations; assess actual behavior and contextual risk. No requirement to add controls or logs everywhere. | POL: ['WF-020']
CODEX WHY: Concrete review activity can be omitted while complying with general security invariants. Distinct from own source/lock/debug findings; investigation-prompt force remains uncertain.
```
  16  - High-confidence indicators: private keys, real access/refresh tokens, cloud access keys, database passwords, API secrets, service-account credentials, production connection strings with credentials.
  17  - Context-dependent: `ApiKey = "..."`, `Secret = "..."`, `Token = "..."`, `Password = "..."`, long opaque strings, connection strings, certificate material.
  18  - Do not ignore `appsettings.Development.json` automatically; obviously fake values (`changeme`, `example-only`, `test-password`, `not-a-real-key`) may be ignored or reported as Info. `UserSecretsId` is not a secre
  19> - Also review production debug/development flags, certificate-validation bypasses, URLs carrying credentials, verbose production error configuration, committed `.env` files.
  20  
  21  ## Layer 3: Injection and dangerous code patterns (A04, A05, A08)
  22  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 AUG1-NC-CIS-L1-0009-a [19, 19] EXTRA_WORKFLOW/DEFAULT pol=[] rel=['WF-020']: Review production debug/development flags as part of the secrets and configuration layer of a security scan.
- NAMED primary/L1/constraints.jsonl/RULE-L1-0551 -> FG-L1-e52b9bf6fd [CANONICAL_ONLY] Full pre-release or requested audits review all applicable layers; targeted changes start with affected layers and expand across security boundaries.
- NAMED primary/L1/constraints.jsonl/RULE-L1-0564 -> FG-L1-844366a741 [CANONICAL_ONLY] Do not report patterns without context (LINQ predicates with user input, query parameters as SSRF without host influence, ordinary template binding as XSS, returned entities withou
- NAMED primary/L1/constraints.jsonl/RULE-L1-0574 -> FG-L1-5821a256da [CANONICAL_ONLY] Check logs for never-log data, PII per requirements; Debug/Trace is not a boundary; no demand to log every successful request.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0108 -> FG-L1-15d9f150d9 [CANONICAL_ONLY] Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without permitted need; log level is not a privacy control.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0109 -> FG-L1-c4e1401ee1 [CANONICAL_ONLY] Do not serialize arbitrary request bodies, domain objects or sensitive payloads into logs by default; log the minimum operationally useful non-sensitive context.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0135 -> FG-L1-d6ab123b1f [CANONICAL_ONLY] Review for unsafe deserialization: BinaryFormatter, unsafe TypeNameHandling, deserializing untrusted payloads into arbitrary runtime types (reported as possibly illustrative).
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0137 -> FG-L1-accce90761 [CANONICAL_ONLY] Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED.
- PASS1 CIS-L1-0009 DISTINCT_UNREPRESENTED_CLAUSE [19, 19]: Review production debug or development flags in the secrets and configuration layer of a security scan.

## CIS-K0-U0046 (pass 3) K0 .claude/skills/security-scan/references/scan-layers.md:44-44  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When the secrets/configuration layer applies, the security-scan procedure calls for reviewing overly verbose production error configuration.
TRIGGER: An invoked security scan in which the secrets/configuration layer applies | EXC: Inspect applicable surfaces only; context and actual exposure determine whether any finding exists. Investigation prompts are not automatic vulnerabilities. | POL: ['WF-020']
CODEX WHY: Generic public-error secrecy does not itself record a review of production configuration. Source is procedural, but general full-layer review may semantically include it; retain uncertainty.
```
  41      builder.Configuration.GetConnectionString("Default");
  42  ```
  43  
  44> Also review production debug/development flags, certificate-validation bypass, insecure URLs carrying credentials, overly verbose production error configuration and accidentally committed `.env` files.
  45  
  46  # Layer 3: Injection and dangerous code patterns (A04, A05, A08)
  47  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 AUG1-NC-CIS-K0-0012-a [44, 44] EXTRA_WORKFLOW/DEFAULT pol=[] rel=[]: Review production debug/development flags as part of the secrets and configuration layer of a security scan.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0211 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0280 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0281 -> FG-K0-16b58514ed [CANONICAL_PLUS_DELTA] The scan completes only when applicable layers were inspected, findings carry evidence, uncertain findings are labelled and limitations stated.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0007 -> FG-K0-0ef1e5ed3d [EXTRA_WORKFLOW] A security scan investigates polymorphic or type-driven deserialization such as BinaryFormatter or unsafe TypeNameHandling; its audit criterion is that untrusted payloads are not d
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0009 -> FG-K0-0282fdad6d [CANONICAL_ONLY] Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED; never PASS for a layer that was not inspected.
- PASS1 CIS-K0-0012 DISTINCT_UNREPRESENTED_CLAUSE [44, 44]: During the applicable secrets/configuration scan, review production debug/development flags.

## CIS-K0-U0047 (pass 3) K0 .claude/skills/security-scan/references/scan-layers.md:44-44  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When the secrets/configuration layer applies, the security-scan procedure calls for reviewing accidentally committed .env files.
TRIGGER: An invoked security scan in which the secrets/configuration layer applies | EXC: Inspect applicable surfaces only; context and actual exposure determine whether any finding exists. Investigation prompts are not automatic vulnerabilities. | POL: ['WF-020']
CODEX WHY: Real-secret prohibition and broad file search may entail this; .env review remains a separate procedural target, not proof all .env files are unsafe. Source is procedural, but general full-layer review may semantically include it; retain uncertainty.
```
  41      builder.Configuration.GetConnectionString("Default");
  42  ```
  43  
  44> Also review production debug/development flags, certificate-validation bypass, insecure URLs carrying credentials, overly verbose production error configuration and accidentally committed `.env` files.
  45  
  46  # Layer 3: Injection and dangerous code patterns (A04, A05, A08)
  47  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 AUG1-NC-CIS-K0-0012-a [44, 44] EXTRA_WORKFLOW/DEFAULT pol=[] rel=[]: Review production debug/development flags as part of the secrets and configuration layer of a security scan.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0211 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0280 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0281 -> FG-K0-16b58514ed [CANONICAL_PLUS_DELTA] The scan completes only when applicable layers were inspected, findings carry evidence, uncertain findings are labelled and limitations stated.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0007 -> FG-K0-0ef1e5ed3d [EXTRA_WORKFLOW] A security scan investigates polymorphic or type-driven deserialization such as BinaryFormatter or unsafe TypeNameHandling; its audit criterion is that untrusted payloads are not d
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0009 -> FG-K0-0282fdad6d [CANONICAL_ONLY] Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED; never PASS for a layer that was not inspected.
- PASS1 CIS-K0-0012 DISTINCT_UNREPRESENTED_CLAUSE [44, 44]: During the applicable secrets/configuration scan, review production debug/development flags.

## CIS-K1-U0032 (pass 3) K1 .claude/skills/security-scan/references/scan-layers.md:39-39  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During applicable secrets/configuration review, investigate overly verbose production error configuration.
TRIGGER: secrets/configuration review within a requested scan; full audits cover applicable layers, targeted scans focus affected surfaces. | EXC: Investigation only, not an automatic vulnerability declaration or mandatory product change. Severity depends on actual exposure; ordinary query parameters do not automatically imply SSRF, and successf | POL: ['WF-020']
CODEX WHY: A specific investigation can be omitted while other items in the same layer are reviewed. Whether the baseline general review obligation incorporates every prompt remains unresolved. Prior rejected labels are not accepted as normative truth.
```
  36  var connectionString = builder.Configuration.GetConnectionString("Default");
  37  ```
  38  
  39> Also review production debug/development flags, certificate-validation bypasses, insecure URLs carrying credentials, overly verbose production error configuration, and accidentally committed `.env` files.
  40  
  41  # Layer 3: Injection and Dangerous Code Patterns (A04, A05, A08)
  42  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 AUG1-NC-CIS-K1-0005-a [39, 39] EXTRA_WORKFLOW/DEFAULT pol=[] rel=[]: Review production debug/development flags as part of the secrets and configuration layer of a security scan.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0534 -> FG-K1-cb3247e43d [CANONICAL_ONLY] appsettings.Development.json is not automatically ignored: a real committed secret remains a secret; obviously fake values may be ignored or reported as Info; UserSecretsId is not 
- NAMED primary/K1/constraints.jsonl/EXTRA-K1-0238 -> FG-K1-ba3da08dba [CANONICAL_ONLY] A full pre-release or requested audit reviews all applicable layers; a targeted change focuses on affected layers and expands when it crosses security boundaries.
- NAMED replica/K1/constraints.jsonl/RULE-K1-0317 -> FG-K1-f0aca49ccf [CANONICAL_PLUS_DELTA] The scan is complete only when applicable layers were inspected, findings have evidence, uncertain findings are labelled and limitations are stated.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0001 -> FG-K1-cb3247e43d [CANONICAL_ONLY] appsettings.Development.json is not automatically ignored: a real committed secret remains a secret; obviously fake values may be ignored or reported as Info; UserSecretsId is not 
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0006 -> FG-K1-ba3da08dba [CANONICAL_ONLY] A full pre-release or requested audit reviews all applicable layers; a targeted change focuses on affected layers and expands when it crosses security boundaries.
- PASS1 CIS-K1-0005 DISTINCT_UNREPRESENTED_CLAUSE [39, 39]: During applicable security configuration review, inspect production debug/development flags.

## CIS-K1-U0033 (pass 3) K1 .claude/skills/security-scan/references/scan-layers.md:39-39  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During applicable secrets/configuration review, investigate accidentally committed .env files.
TRIGGER: secrets/configuration review within a requested scan; full audits cover applicable layers, targeted scans focus affected surfaces. | EXC: Investigation only, not an automatic vulnerability declaration or mandatory product change. Severity depends on actual exposure; ordinary query parameters do not automatically imply SSRF, and successf | POL: ['WF-020']
CODEX WHY: A specific investigation can be omitted while other items in the same layer are reviewed. Whether the baseline general review obligation incorporates every prompt remains unresolved. Prior rejected labels are not accepted as normative truth.
```
  36  var connectionString = builder.Configuration.GetConnectionString("Default");
  37  ```
  38  
  39> Also review production debug/development flags, certificate-validation bypasses, insecure URLs carrying credentials, overly verbose production error configuration, and accidentally committed `.env` files.
  40  
  41  # Layer 3: Injection and Dangerous Code Patterns (A04, A05, A08)
  42  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 AUG1-NC-CIS-K1-0005-a [39, 39] EXTRA_WORKFLOW/DEFAULT pol=[] rel=[]: Review production debug/development flags as part of the secrets and configuration layer of a security scan.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0370 -> FG-K1-f598482bc8 [CANONICAL_ONLY] Keep local passwords in an ignored .env or similar mechanism.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0534 -> FG-K1-cb3247e43d [CANONICAL_ONLY] appsettings.Development.json is not automatically ignored: a real committed secret remains a secret; obviously fake values may be ignored or reported as Info; UserSecretsId is not 
- NAMED replica/K1/constraints.jsonl/RULE-K1-0317 -> FG-K1-f0aca49ccf [CANONICAL_PLUS_DELTA] The scan is complete only when applicable layers were inspected, findings have evidence, uncertain findings are labelled and limitations are stated.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0001 -> FG-K1-cb3247e43d [CANONICAL_ONLY] appsettings.Development.json is not automatically ignored: a real committed secret remains a secret; obviously fake values may be ignored or reported as Info; UserSecretsId is not 
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0006 -> FG-K1-ba3da08dba [CANONICAL_ONLY] A full pre-release or requested audit reviews all applicable layers; a targeted change focuses on affected layers and expands when it crosses security boundaries.
- PASS1 CIS-K1-0005 DISTINCT_UNREPRESENTED_CLAUSE [39, 39]: During applicable security configuration review, inspect production debug/development flags.
