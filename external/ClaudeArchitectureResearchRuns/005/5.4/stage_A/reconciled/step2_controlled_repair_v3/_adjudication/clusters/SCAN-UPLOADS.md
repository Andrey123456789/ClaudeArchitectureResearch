# SCAN-UPLOADS (8 records)

## CIS-M1-U0049 (pass 3) M1 .claude/skills/security-scan/references/scan-layers.md:205-207  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When uploads exist, inspect risks that uploaded content can execute.
TRIGGER: Applicable security review of file uploads | EXC: Investigation prompts, not automatic vulnerabilities or mandates to add product controls. Review only applicable surfaces; do not demand logs for every successful request; actual exposure and context  | POL: ['WF-020']
CODEX WHY: Positive review action may be separately falsifiable beyond broad security invariants, but the all-applicable-layers duty could already incorporate it.
```
 202  
 203  ## File Uploads
 204  
 205> When uploads exist, inspect size limits, storage path safety, file-name
 206> handling, content/type assumptions (`security.md` § Failure Handling),
 207> execution or public-serving risks, and authorization.
 208  
 209  ## Rate Limiting
 210  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-374c3093b8 [205, 207] CANONICAL_ONLY/MUST_NOT pol=['SEC-015'] rel=[]: Do not trust client file metadata such as MIME type as authoritative.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0613 -> FG-M1-9856d9cf83 [CANONICAL_ONLY] Do not report suspicious patterns as findings without context (ordinary LINQ predicates, every user-influenced query parameter as SSRF, ordinary template binding as XSS, non-securi
- NAMED primary/M1/constraints.jsonl/RULE-M1-0624 -> FG-M1-7c88da0f41 [CANONICAL_ONLY] Check logs against security.md; review PII per project requirements; Debug/Trace level is not a security boundary; do not demand logs for every successful request.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0641 -> FG-M1-77a9a56e68 [CANONICAL_ONLY] Full pre-release or requested audits review all applicable layers; targeted changes start with affected layers and expand when the change crosses security boundaries.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0646 -> FG-M1-a581882787 [CANONICAL_ONLY] A scan is complete when applicable layers were inspected, findings have evidence, uncertain findings are labelled, severity reflects actual risk and no layer is PASS unchecked.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0096 -> FG-M1-a0cf4e40d9 [EXTRA_WORKFLOW] In security review investigate deliberate sanitizer bypasses (bypassSecurityTrustHtml/Script/ResourceUrl) and direct DOM manipulation with untrusted content; ordinary Angular bindi
- NAMED replica/M1/constraints.jsonl/RULE-M1-0196 -> FG-M1-be1a8db21a [CANONICAL_ONLY] Severity from reachability, exposure and exploitability, not CVSS, pattern or OWASP category alone; a theoretical missing limit is not automatically High.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0128 -> FG-M1-374c3093b8 [CANONICAL_ONLY] Do not trust client file metadata such as MIME type as authoritative.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0124 -> FG-M1-064c990ec0 [CANONICAL_ONLY] Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without permitted need; log level does not make data safe.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0125 -> FG-M1-805f4b7b04 [CANONICAL_ONLY] No arbitrary request bodies, domain objects or sensitive payloads in logs by default; minimum useful non-sensitive context.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0117 -> FG-M1-5579fdfb09 [EXTRA_WORKFLOW] Use OWASP Top 10:2025 as an awareness taxonomy when it genuinely fits; not every issue needs a category; do not force an inaccurate mapping.

## CIS-M1-U0050 (pass 3) M1 .claude/skills/security-scan/references/scan-layers.md:205-207  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When uploads exist, inspect risks from public serving of uploaded content.
TRIGGER: Applicable security review of file uploads | EXC: Investigation prompts, not automatic vulnerabilities or mandates to add product controls. Review only applicable surfaces; do not demand logs for every successful request; actual exposure and context  | POL: ['WF-020']
CODEX WHY: Positive review action may be separately falsifiable beyond broad security invariants, but the all-applicable-layers duty could already incorporate it.
```
 202  
 203  ## File Uploads
 204  
 205> When uploads exist, inspect size limits, storage path safety, file-name
 206> handling, content/type assumptions (`security.md` § Failure Handling),
 207> execution or public-serving risks, and authorization.
 208  
 209  ## Rate Limiting
 210  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-374c3093b8 [205, 207] CANONICAL_ONLY/MUST_NOT pol=['SEC-015'] rel=[]: Do not trust client file metadata such as MIME type as authoritative.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0613 -> FG-M1-9856d9cf83 [CANONICAL_ONLY] Do not report suspicious patterns as findings without context (ordinary LINQ predicates, every user-influenced query parameter as SSRF, ordinary template binding as XSS, non-securi
- NAMED primary/M1/constraints.jsonl/RULE-M1-0624 -> FG-M1-7c88da0f41 [CANONICAL_ONLY] Check logs against security.md; review PII per project requirements; Debug/Trace level is not a security boundary; do not demand logs for every successful request.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0641 -> FG-M1-77a9a56e68 [CANONICAL_ONLY] Full pre-release or requested audits review all applicable layers; targeted changes start with affected layers and expand when the change crosses security boundaries.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0646 -> FG-M1-a581882787 [CANONICAL_ONLY] A scan is complete when applicable layers were inspected, findings have evidence, uncertain findings are labelled, severity reflects actual risk and no layer is PASS unchecked.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0096 -> FG-M1-a0cf4e40d9 [EXTRA_WORKFLOW] In security review investigate deliberate sanitizer bypasses (bypassSecurityTrustHtml/Script/ResourceUrl) and direct DOM manipulation with untrusted content; ordinary Angular bindi
- NAMED replica/M1/constraints.jsonl/RULE-M1-0196 -> FG-M1-be1a8db21a [CANONICAL_ONLY] Severity from reachability, exposure and exploitability, not CVSS, pattern or OWASP category alone; a theoretical missing limit is not automatically High.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0128 -> FG-M1-374c3093b8 [CANONICAL_ONLY] Do not trust client file metadata such as MIME type as authoritative.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0124 -> FG-M1-064c990ec0 [CANONICAL_ONLY] Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without permitted need; log level does not make data safe.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0125 -> FG-M1-805f4b7b04 [CANONICAL_ONLY] No arbitrary request bodies, domain objects or sensitive payloads in logs by default; minimum useful non-sensitive context.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0117 -> FG-M1-5579fdfb09 [EXTRA_WORKFLOW] Use OWASP Top 10:2025 as an awareness taxonomy when it genuinely fits; not every issue needs a category; do not force an inaccurate mapping.

## CIS-L0-U0045 (pass 3) L0 .claude/skills/security-scan/references/scan-layers.md:46-46  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During applicable file-upload security review, investigate whether uploaded files can execute.
TRIGGER: applicable file-upload security review when that surface exists; full audits cover applicable layers and targeted reviews expand with security boundaries. | EXC: Investigation prompt, not automatic vulnerability declaration, required code change, ban on every configuration value or mandate to add upload controls. Severity and applicability remain contextual. | POL: ['WF-020']
CODEX WHY: Exact source instruction/list item is plausible independently checkable review content, yet general full-layer coverage and incorporation by reference provide serious equivalence counterevidence. Preserve uncertain.
```
  43  - **CORS:** origins versus the actual browser-client model; problems include unnecessarily broad origins, credentialed requests from untrusted origins, and environment-specific origins exposed in Production. `Allow
  44  - **CSRF:** when browser credentials (especially cookies) are sent automatically, review CSRF protection for state-changing operations; explicitly attached Bearer headers have different characteristics.
  45  - **TLS:** disabled certificate validation, accept-all callbacks, plain HTTP for sensitive external communication. Account for termination at proxies, ingress, gateways, or platforms; missing HTTPS redirection in c
  46> - **File uploads:** size limits, storage path safety, file-name handling, content/type assumptions (client MIME type treated as authoritative?), execution or public-serving risk, authorization.
  47  - **Rate limiting:** consider it where abuse realistically matters (login/password reset, expensive anonymous endpoints, resource-intensive operations); not on every endpoint. `429` semantics: `http-api` skill.
  48  
  49  ## Layer 6: Sensitive data, logging, error exposure (A04, A09)
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L0/constraints.jsonl/RULE-L0-0529 -> FG-L0-f7f7986ea8 [CANONICAL_ONLY] Inspect which surfaces exist and skip irrelevant checks rather than reporting failures; full audits review all applicable layers; targeted changes start with affected layers and ex
- NAMED primary/L0/constraints.jsonl/RULE-L0-0540 -> FG-L0-5106f13e4b [CANONICAL_ONLY] A committed real secret is a secret regardless of file name (appsettings.Development.json not exempt); obviously fake values may be ignored or Info; UserSecretsId is not a secret.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0552 -> FG-L0-131120755c [CANONICAL_ONLY] Review disabled certificate validation, accept-all callbacks and plain HTTP; account for TLS termination; missing HTTPS redirection is not automatically a vulnerability.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0558 -> FG-L0-f35ced143f [CANONICAL_ONLY] Do not map pattern, CVSS or OWASP category to severity mechanically; judge whether an attacker can actually exploit unbounded resources.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0559 -> FG-L0-e6cdfa2340 [CANONICAL_ONLY] Review startup/configuration failure for dangerous fallback (auth disabled, plaintext mode, allow-all).
- NAMED replica/L0/constraints.jsonl/RULE-L0-0045 -> FG-L0-fc7ca2f4bb [CANONICAL_ONLY] Treat data crossing the trusted boundary (requests, uploads, external responses, messages, user identifiers/filters) as untrusted and validate it at the owning layer when assumptio
- NAMED replica/L0/constraints.jsonl/RULE-L0-0046 -> FG-L0-a9aba1bf8a [CANONICAL_ONLY] Do not trust client-provided file metadata such as MIME type as authoritative when handling or security decisions depend on content.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0208 -> FG-L0-e9e021edc5 [CANONICAL_ONLY] Never invent exploitability that the code does not establish.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0103 -> FG-L0-d2ce44cdf5 [EXTRA_WORKFLOW] Security review uses seven layers (dependencies, secrets/configuration, injection, authentication/access control, browser/HTTP, sensitive data/logging/errors, exceptional condition

## CIS-L0-U0046 (pass 3) L0 .claude/skills/security-scan/references/scan-layers.md:46-46  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During applicable file-upload security review, investigate risks from publicly serving uploaded files.
TRIGGER: applicable file-upload security review when that surface exists; full audits cover applicable layers and targeted reviews expand with security boundaries. | EXC: Investigation prompt, not automatic vulnerability declaration, required code change, ban on every configuration value or mandate to add upload controls. Severity and applicability remain contextual. | POL: ['WF-020']
CODEX WHY: Exact source instruction/list item is plausible independently checkable review content, yet general full-layer coverage and incorporation by reference provide serious equivalence counterevidence. Preserve uncertain.
```
  43  - **CORS:** origins versus the actual browser-client model; problems include unnecessarily broad origins, credentialed requests from untrusted origins, and environment-specific origins exposed in Production. `Allow
  44  - **CSRF:** when browser credentials (especially cookies) are sent automatically, review CSRF protection for state-changing operations; explicitly attached Bearer headers have different characteristics.
  45  - **TLS:** disabled certificate validation, accept-all callbacks, plain HTTP for sensitive external communication. Account for termination at proxies, ingress, gateways, or platforms; missing HTTPS redirection in c
  46> - **File uploads:** size limits, storage path safety, file-name handling, content/type assumptions (client MIME type treated as authoritative?), execution or public-serving risk, authorization.
  47  - **Rate limiting:** consider it where abuse realistically matters (login/password reset, expensive anonymous endpoints, resource-intensive operations); not on every endpoint. `429` semantics: `http-api` skill.
  48  
  49  ## Layer 6: Sensitive data, logging, error exposure (A04, A09)
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L0/constraints.jsonl/RULE-L0-0529 -> FG-L0-f7f7986ea8 [CANONICAL_ONLY] Inspect which surfaces exist and skip irrelevant checks rather than reporting failures; full audits review all applicable layers; targeted changes start with affected layers and ex
- NAMED primary/L0/constraints.jsonl/RULE-L0-0540 -> FG-L0-5106f13e4b [CANONICAL_ONLY] A committed real secret is a secret regardless of file name (appsettings.Development.json not exempt); obviously fake values may be ignored or Info; UserSecretsId is not a secret.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0552 -> FG-L0-131120755c [CANONICAL_ONLY] Review disabled certificate validation, accept-all callbacks and plain HTTP; account for TLS termination; missing HTTPS redirection is not automatically a vulnerability.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0558 -> FG-L0-f35ced143f [CANONICAL_ONLY] Do not map pattern, CVSS or OWASP category to severity mechanically; judge whether an attacker can actually exploit unbounded resources.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0559 -> FG-L0-e6cdfa2340 [CANONICAL_ONLY] Review startup/configuration failure for dangerous fallback (auth disabled, plaintext mode, allow-all).
- NAMED replica/L0/constraints.jsonl/RULE-L0-0045 -> FG-L0-fc7ca2f4bb [CANONICAL_ONLY] Treat data crossing the trusted boundary (requests, uploads, external responses, messages, user identifiers/filters) as untrusted and validate it at the owning layer when assumptio
- NAMED replica/L0/constraints.jsonl/RULE-L0-0046 -> FG-L0-a9aba1bf8a [CANONICAL_ONLY] Do not trust client-provided file metadata such as MIME type as authoritative when handling or security decisions depend on content.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0208 -> FG-L0-e9e021edc5 [CANONICAL_ONLY] Never invent exploitability that the code does not establish.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0103 -> FG-L0-d2ce44cdf5 [EXTRA_WORKFLOW] Security review uses seven layers (dependencies, secrets/configuration, injection, authentication/access control, browser/HTTP, sensitive data/logging/errors, exceptional condition

## CIS-L1-U0041 (pass 3) L1 .claude/skills/security-scan/references/scan-layers.md:45-45  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During an applicable security scan, review file-upload execution risks.
TRIGGER: The corresponding surface exists and the scan covers that layer | EXC: Investigation prompts, not automatic vulnerability declarations; assess actual behavior and contextual risk. No requirement to add controls or logs everywhere. | POL: ['WF-020']
CODEX WHY: Concrete review activity can be omitted while complying with general security invariants. Distinct from own source/lock/debug findings; investigation-prompt force remains uncertain.
```
  42  - **CORS** — a browser-origin policy, not authorization. Look for unnecessarily broad trusted origins, credentialed requests from untrusted origins, and environment-specific origins leaking into Production. A wildc
  43  - **CSRF** — when browser credentials (especially cookies) are sent automatically, review CSRF protection for state-changing operations; explicitly attached Bearer headers have different characteristics.
  44  - **TLS** — disabled certificate validation, accept-all callbacks, plain HTTP for sensitive external calls. Account for termination at proxies, ingress, gateways, or platforms; missing HTTPS redirection in code is 
  45> - **File uploads** — size limits, storage path safety, file-name handling, content/type assumptions, execution or public-serving risks, authorization.
  46  - **Rate limiting** — consider it where abuse realistically matters (login, password reset, expensive anonymous or resource-intensive endpoints); not required everywhere. 429 semantics: `http-api`.
  47  
  48  ## Layer 6: Sensitive data, logging, and error exposure (A04, A09)
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L1/constraints.jsonl/RULE-L1-0551 -> FG-L1-e52b9bf6fd [CANONICAL_ONLY] Full pre-release or requested audits review all applicable layers; targeted changes start with affected layers and expand across security boundaries.
- NAMED primary/L1/constraints.jsonl/RULE-L1-0564 -> FG-L1-844366a741 [CANONICAL_ONLY] Do not report patterns without context (LINQ predicates with user input, query parameters as SSRF without host influence, ordinary template binding as XSS, returned entities withou
- NAMED primary/L1/constraints.jsonl/RULE-L1-0574 -> FG-L1-5821a256da [CANONICAL_ONLY] Check logs for never-log data, PII per requirements; Debug/Trace is not a boundary; no demand to log every successful request.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0108 -> FG-L1-15d9f150d9 [CANONICAL_ONLY] Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without permitted need; log level is not a privacy control.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0109 -> FG-L1-c4e1401ee1 [CANONICAL_ONLY] Do not serialize arbitrary request bodies, domain objects or sensitive payloads into logs by default; log the minimum operationally useful non-sensitive context.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0135 -> FG-L1-d6ab123b1f [CANONICAL_ONLY] Review for unsafe deserialization: BinaryFormatter, unsafe TypeNameHandling, deserializing untrusted payloads into arbitrary runtime types (reported as possibly illustrative).
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0137 -> FG-L1-accce90761 [CANONICAL_ONLY] Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED.

## CIS-L1-U0042 (pass 3) L1 .claude/skills/security-scan/references/scan-layers.md:45-45  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During an applicable security scan, review file-upload public-serving risks.
TRIGGER: The corresponding surface exists and the scan covers that layer | EXC: Investigation prompts, not automatic vulnerability declarations; assess actual behavior and contextual risk. No requirement to add controls or logs everywhere. | POL: ['WF-020']
CODEX WHY: Concrete review activity can be omitted while complying with general security invariants. Distinct from own source/lock/debug findings; investigation-prompt force remains uncertain.
```
  42  - **CORS** — a browser-origin policy, not authorization. Look for unnecessarily broad trusted origins, credentialed requests from untrusted origins, and environment-specific origins leaking into Production. A wildc
  43  - **CSRF** — when browser credentials (especially cookies) are sent automatically, review CSRF protection for state-changing operations; explicitly attached Bearer headers have different characteristics.
  44  - **TLS** — disabled certificate validation, accept-all callbacks, plain HTTP for sensitive external calls. Account for termination at proxies, ingress, gateways, or platforms; missing HTTPS redirection in code is 
  45> - **File uploads** — size limits, storage path safety, file-name handling, content/type assumptions, execution or public-serving risks, authorization.
  46  - **Rate limiting** — consider it where abuse realistically matters (login, password reset, expensive anonymous or resource-intensive endpoints); not required everywhere. 429 semantics: `http-api`.
  47  
  48  ## Layer 6: Sensitive data, logging, and error exposure (A04, A09)
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L1/constraints.jsonl/RULE-L1-0551 -> FG-L1-e52b9bf6fd [CANONICAL_ONLY] Full pre-release or requested audits review all applicable layers; targeted changes start with affected layers and expand across security boundaries.
- NAMED primary/L1/constraints.jsonl/RULE-L1-0564 -> FG-L1-844366a741 [CANONICAL_ONLY] Do not report patterns without context (LINQ predicates with user input, query parameters as SSRF without host influence, ordinary template binding as XSS, returned entities withou
- NAMED primary/L1/constraints.jsonl/RULE-L1-0574 -> FG-L1-5821a256da [CANONICAL_ONLY] Check logs for never-log data, PII per requirements; Debug/Trace is not a boundary; no demand to log every successful request.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0108 -> FG-L1-15d9f150d9 [CANONICAL_ONLY] Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without permitted need; log level is not a privacy control.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0109 -> FG-L1-c4e1401ee1 [CANONICAL_ONLY] Do not serialize arbitrary request bodies, domain objects or sensitive payloads into logs by default; log the minimum operationally useful non-sensitive context.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0135 -> FG-L1-d6ab123b1f [CANONICAL_ONLY] Review for unsafe deserialization: BinaryFormatter, unsafe TypeNameHandling, deserializing untrusted payloads into arbitrary runtime types (reported as possibly illustrative).
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0137 -> FG-L1-accce90761 [CANONICAL_ONLY] Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED.

## CIS-K0-U0050 (pass 3) K0 .claude/skills/security-scan/references/scan-layers.md:129-129  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When file-upload surfaces exist, the security-scan procedure calls for reviewing file-upload execution risks.
TRIGGER: An invoked security scan in which file-upload surfaces exist | EXC: Inspect applicable surfaces only; context and actual exposure determine whether any finding exists. Investigation prompts are not automatic vulnerabilities. | POL: ['WF-020']
CODEX WHY: Upload metadata trust does not separately instruct review of execution risks. Source is procedural, but general full-layer review may semantically include it; retain uncertainty.
```
 126  
 127  ## File uploads
 128  
 129> Rules: `rules/backend/security.md` § Uploads. Inspect size limits, storage path safety, file-name handling, content/type assumptions, execution or public-serving risks and authorization.
 130  
 131  ## Rate limiting
 132  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-0f0308785f [129, 129] CANONICAL_ONLY/MUST_NOT pol=['SEC-015'] rel=[]: Do not treat client-provided file metadata such as MIME type as authoritative when handling or security depends on actual content.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0211 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0280 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0281 -> FG-K0-16b58514ed [CANONICAL_PLUS_DELTA] The scan completes only when applicable layers were inspected, findings carry evidence, uncertain findings are labelled and limitations stated.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0007 -> FG-K0-0ef1e5ed3d [EXTRA_WORKFLOW] A security scan investigates polymorphic or type-driven deserialization such as BinaryFormatter or unsafe TypeNameHandling; its audit criterion is that untrusted payloads are not d
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0009 -> FG-K0-0282fdad6d [CANONICAL_ONLY] Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED; never PASS for a layer that was not inspected.

## CIS-K0-U0051 (pass 3) K0 .claude/skills/security-scan/references/scan-layers.md:129-129  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When file-upload surfaces exist, the security-scan procedure calls for reviewing file-upload public-serving risks.
TRIGGER: An invoked security scan in which file-upload surfaces exist | EXC: Inspect applicable surfaces only; context and actual exposure determine whether any finding exists. Investigation prompts are not automatic vulnerabilities. | POL: ['WF-020']
CODEX WHY: Upload metadata trust does not separately instruct review of public-serving risks. Source is procedural, but general full-layer review may semantically include it; retain uncertainty.
```
 126  
 127  ## File uploads
 128  
 129> Rules: `rules/backend/security.md` § Uploads. Inspect size limits, storage path safety, file-name handling, content/type assumptions, execution or public-serving risks and authorization.
 130  
 131  ## Rate limiting
 132  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-0f0308785f [129, 129] CANONICAL_ONLY/MUST_NOT pol=['SEC-015'] rel=[]: Do not treat client-provided file metadata such as MIME type as authoritative when handling or security depends on actual content.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0211 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0280 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0281 -> FG-K0-16b58514ed [CANONICAL_PLUS_DELTA] The scan completes only when applicable layers were inspected, findings carry evidence, uncertain findings are labelled and limitations stated.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0007 -> FG-K0-0ef1e5ed3d [EXTRA_WORKFLOW] A security scan investigates polymorphic or type-driven deserialization such as BinaryFormatter or unsafe TypeNameHandling; its audit criterion is that untrusted payloads are not d
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0009 -> FG-K0-0282fdad6d [CANONICAL_ONLY] Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED; never PASS for a layer that was not inspected.
