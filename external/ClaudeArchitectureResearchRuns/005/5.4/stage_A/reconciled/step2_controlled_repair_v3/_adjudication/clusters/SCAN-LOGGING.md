# SCAN-LOGGING (8 records)

## CIS-M1-U0051 (pass 3) M1 .claude/skills/security-scan/references/scan-layers.md:222-225  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: Review duplicate security-relevant logging in context.
TRIGGER: Applicable security review of logging | EXC: Investigation prompts, not automatic vulnerabilities or mandates to add product controls. Review only applicable surfaces; do not demand logs for every successful request; actual exposure and context  | POL: ['WF-020']
CODEX WHY: Positive review action may be separately falsifiable beyond broad security invariants, but the all-applicable-layers duty could already incorporate it.
```
 219  
 220  ## Logging
 221  
 222> Check logs against `security.md` § Logging and Sensitive Data. Review PII
 223> according to project requirements, and do not consider Debug/Trace level a
 224> security boundary. Review duplicate or missing security-relevant logging in
 225> context; do not demand logs for every successful request.
 226  
 227  ## Error Responses
 228  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-064c990ec0 [222, 225] CANONICAL_ONLY/MUST_NOT pol=['SEC-010'] rel=['SEC-012']: Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without permitted need; log level does not make data safe.
- V2 FG-M1-805f4b7b04 [222, 225] CANONICAL_ONLY/MUST_NOT pol=['RUN-014'] rel=[]: No arbitrary request bodies, domain objects or sensitive payloads in logs by default; minimum useful non-sensitive context.
- V2 FG-M1-7c88da0f41 [222, 225] CANONICAL_ONLY/MUST pol=['SEC-010', 'WF-012'] rel=[]: Check logs against security.md; review PII per project requirements; Debug/Trace level is not a security boundary; do not demand logs for every successful request.
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

## CIS-M1-U0052 (pass 3) M1 .claude/skills/security-scan/references/scan-layers.md:222-225  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: Review missing security-relevant logging in context.
TRIGGER: Applicable security review of logging | EXC: Investigation prompts, not automatic vulnerabilities or mandates to add product controls. Review only applicable surfaces; do not demand logs for every successful request; actual exposure and context  | POL: ['WF-020']
CODEX WHY: Positive review action may be separately falsifiable beyond broad security invariants, but the all-applicable-layers duty could already incorporate it.
```
 219  
 220  ## Logging
 221  
 222> Check logs against `security.md` § Logging and Sensitive Data. Review PII
 223> according to project requirements, and do not consider Debug/Trace level a
 224> security boundary. Review duplicate or missing security-relevant logging in
 225> context; do not demand logs for every successful request.
 226  
 227  ## Error Responses
 228  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-064c990ec0 [222, 225] CANONICAL_ONLY/MUST_NOT pol=['SEC-010'] rel=['SEC-012']: Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without permitted need; log level does not make data safe.
- V2 FG-M1-805f4b7b04 [222, 225] CANONICAL_ONLY/MUST_NOT pol=['RUN-014'] rel=[]: No arbitrary request bodies, domain objects or sensitive payloads in logs by default; minimum useful non-sensitive context.
- V2 FG-M1-7c88da0f41 [222, 225] CANONICAL_ONLY/MUST pol=['SEC-010', 'WF-012'] rel=[]: Check logs against security.md; review PII per project requirements; Debug/Trace level is not a security boundary; do not demand logs for every successful request.
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

## CIS-L1-U0043 (pass 3) L1 .claude/skills/security-scan/references/scan-layers.md:50-50  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During an applicable security scan, review missing security-relevant logging in context.
TRIGGER: The corresponding surface exists and the scan covers that layer | EXC: Investigation prompts, not automatic vulnerability declarations; assess actual behavior and contextual risk. No requirement to add controls or logs everywhere. | POL: ['WF-020']
CODEX WHY: Concrete review activity can be omitted while complying with general security invariants. Distinct from own source/lock/debug findings; investigation-prompt force remains uncertain.
```
  47  
  48  ## Layer 6: Sensitive data, logging, and error exposure (A04, A09)
  49  
  50> - **Logging** — passwords, tokens, private keys, authentication secrets, payment credentials; PII per project requirements; Debug/Trace is not a security boundary. Review missing or duplicated security-relevant log
  51  - **Error responses** — compare public error payloads against the failure rules in `.claude/rules/0-core/http-api.md`.
  52  - **Response data** — domain/persistence entities returned directly, password hashes, internal security fields, unnecessary personal data, secret metadata; inspect the actual serialized fields before reporting.
  53  - **Data at rest** — choose protection by requirement: one-way hashing for passwords; hashing for verification-only tokens; protected storage for retrievable secrets; platform/database encryption where suitable; AS
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L1-15d9f150d9 [50, 50] CANONICAL_ONLY/MUST_NOT pol=['SEC-010'] rel=[]: Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without permitted need; log level is not a privacy control.
- V2 FG-L1-c4e1401ee1 [50, 50] CANONICAL_ONLY/MUST_NOT pol=['RUN-014'] rel=[]: Do not serialize arbitrary request bodies, domain objects or sensitive payloads into logs by default; log the minimum operationally useful non-sensitive context.
- V2 FG-L1-5821a256da [50, 50] CANONICAL_ONLY/MUST pol=['SEC-010', 'WF-012'] rel=[]: Check logs for never-log data, PII per requirements; Debug/Trace is not a boundary; no demand to log every successful request.
- NAMED primary/L1/constraints.jsonl/RULE-L1-0551 -> FG-L1-e52b9bf6fd [CANONICAL_ONLY] Full pre-release or requested audits review all applicable layers; targeted changes start with affected layers and expand across security boundaries.
- NAMED primary/L1/constraints.jsonl/RULE-L1-0564 -> FG-L1-844366a741 [CANONICAL_ONLY] Do not report patterns without context (LINQ predicates with user input, query parameters as SSRF without host influence, ordinary template binding as XSS, returned entities withou
- NAMED primary/L1/constraints.jsonl/RULE-L1-0574 -> FG-L1-5821a256da [CANONICAL_ONLY] Check logs for never-log data, PII per requirements; Debug/Trace is not a boundary; no demand to log every successful request.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0108 -> FG-L1-15d9f150d9 [CANONICAL_ONLY] Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without permitted need; log level is not a privacy control.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0109 -> FG-L1-c4e1401ee1 [CANONICAL_ONLY] Do not serialize arbitrary request bodies, domain objects or sensitive payloads into logs by default; log the minimum operationally useful non-sensitive context.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0135 -> FG-L1-d6ab123b1f [CANONICAL_ONLY] Review for unsafe deserialization: BinaryFormatter, unsafe TypeNameHandling, deserializing untrusted payloads into arbitrary runtime types (reported as possibly illustrative).
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0137 -> FG-L1-accce90761 [CANONICAL_ONLY] Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED.

## CIS-L1-U0044 (pass 3) L1 .claude/skills/security-scan/references/scan-layers.md:50-50  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During an applicable security scan, review duplicated security-relevant logging in context.
TRIGGER: The corresponding surface exists and the scan covers that layer | EXC: Investigation prompts, not automatic vulnerability declarations; assess actual behavior and contextual risk. No requirement to add controls or logs everywhere. | POL: ['WF-020']
CODEX WHY: Concrete review activity can be omitted while complying with general security invariants. Distinct from own source/lock/debug findings; investigation-prompt force remains uncertain.
```
  47  
  48  ## Layer 6: Sensitive data, logging, and error exposure (A04, A09)
  49  
  50> - **Logging** — passwords, tokens, private keys, authentication secrets, payment credentials; PII per project requirements; Debug/Trace is not a security boundary. Review missing or duplicated security-relevant log
  51  - **Error responses** — compare public error payloads against the failure rules in `.claude/rules/0-core/http-api.md`.
  52  - **Response data** — domain/persistence entities returned directly, password hashes, internal security fields, unnecessary personal data, secret metadata; inspect the actual serialized fields before reporting.
  53  - **Data at rest** — choose protection by requirement: one-way hashing for passwords; hashing for verification-only tokens; protected storage for retrievable secrets; platform/database encryption where suitable; AS
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L1-15d9f150d9 [50, 50] CANONICAL_ONLY/MUST_NOT pol=['SEC-010'] rel=[]: Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without permitted need; log level is not a privacy control.
- V2 FG-L1-c4e1401ee1 [50, 50] CANONICAL_ONLY/MUST_NOT pol=['RUN-014'] rel=[]: Do not serialize arbitrary request bodies, domain objects or sensitive payloads into logs by default; log the minimum operationally useful non-sensitive context.
- V2 FG-L1-5821a256da [50, 50] CANONICAL_ONLY/MUST pol=['SEC-010', 'WF-012'] rel=[]: Check logs for never-log data, PII per requirements; Debug/Trace is not a boundary; no demand to log every successful request.
- NAMED primary/L1/constraints.jsonl/RULE-L1-0551 -> FG-L1-e52b9bf6fd [CANONICAL_ONLY] Full pre-release or requested audits review all applicable layers; targeted changes start with affected layers and expand across security boundaries.
- NAMED primary/L1/constraints.jsonl/RULE-L1-0564 -> FG-L1-844366a741 [CANONICAL_ONLY] Do not report patterns without context (LINQ predicates with user input, query parameters as SSRF without host influence, ordinary template binding as XSS, returned entities withou
- NAMED primary/L1/constraints.jsonl/RULE-L1-0574 -> FG-L1-5821a256da [CANONICAL_ONLY] Check logs for never-log data, PII per requirements; Debug/Trace is not a boundary; no demand to log every successful request.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0108 -> FG-L1-15d9f150d9 [CANONICAL_ONLY] Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without permitted need; log level is not a privacy control.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0109 -> FG-L1-c4e1401ee1 [CANONICAL_ONLY] Do not serialize arbitrary request bodies, domain objects or sensitive payloads into logs by default; log the minimum operationally useful non-sensitive context.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0135 -> FG-L1-d6ab123b1f [CANONICAL_ONLY] Review for unsafe deserialization: BinaryFormatter, unsafe TypeNameHandling, deserializing untrusted payloads into arbitrary runtime types (reported as possibly illustrative).
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0137 -> FG-L1-accce90761 [CANONICAL_ONLY] Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED.

## CIS-K0-U0052 (pass 3) K0 .claude/skills/security-scan/references/scan-layers.md:139-139  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When the logging layer applies, the security-scan procedure calls for reviewing missing security-relevant logging in context.
TRIGGER: An invoked security scan in which the logging layer applies | EXC: Inspect applicable surfaces only; context and actual exposure determine whether any finding exists. Investigation prompts are not automatic vulnerabilities. | POL: ['WF-020']
CODEX WHY: Sensitive-data exclusion does not represent missing-event inspection; not a mandate to log every request. Source is procedural, but general full-layer review may semantically include it; retain uncertainty.
```
 136  
 137  ## Logging
 138  
 139> Rules: `rules/common/security.md` § Logging and sensitive data. Review logs for credentials, tokens, keys and payment data, PII against project requirements, Debug/Trace treated as a safe level, and duplicate or mi
 140  
 141  ## Error responses
 142  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-46d3dca2e7 [139, 139] CANONICAL_ONLY/MUST_NOT pol=['SEC-010'] rel=[]: Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without a concrete operational need permitted by privacy policy; prefer stable technical identifiers; log level does not make sensitive
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0211 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0280 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0281 -> FG-K0-16b58514ed [CANONICAL_PLUS_DELTA] The scan completes only when applicable layers were inspected, findings carry evidence, uncertain findings are labelled and limitations stated.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0007 -> FG-K0-0ef1e5ed3d [EXTRA_WORKFLOW] A security scan investigates polymorphic or type-driven deserialization such as BinaryFormatter or unsafe TypeNameHandling; its audit criterion is that untrusted payloads are not d
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0009 -> FG-K0-0282fdad6d [CANONICAL_ONLY] Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED; never PASS for a layer that was not inspected.

## CIS-K0-U0053 (pass 3) K0 .claude/skills/security-scan/references/scan-layers.md:139-139  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When the logging layer applies, the security-scan procedure calls for reviewing duplicate security-relevant logging in context.
TRIGGER: An invoked security scan in which the logging layer applies | EXC: Inspect applicable surfaces only; context and actual exposure determine whether any finding exists. Investigation prompts are not automatic vulnerabilities. | POL: ['WF-020']
CODEX WHY: Unexpected-exception once-only logging differs from reviewing duplicated security-event logging; not every security event is an exception. Source is procedural, but general full-layer review may semantically include it; retain uncertainty.
```
 136  
 137  ## Logging
 138  
 139> Rules: `rules/common/security.md` § Logging and sensitive data. Review logs for credentials, tokens, keys and payment data, PII against project requirements, Debug/Trace treated as a safe level, and duplicate or mi
 140  
 141  ## Error responses
 142  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-46d3dca2e7 [139, 139] CANONICAL_ONLY/MUST_NOT pol=['SEC-010'] rel=[]: Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without a concrete operational need permitted by privacy policy; prefer stable technical identifiers; log level does not make sensitive
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0211 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0280 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0281 -> FG-K0-16b58514ed [CANONICAL_PLUS_DELTA] The scan completes only when applicable layers were inspected, findings carry evidence, uncertain findings are labelled and limitations stated.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0007 -> FG-K0-0ef1e5ed3d [EXTRA_WORKFLOW] A security scan investigates polymorphic or type-driven deserialization such as BinaryFormatter or unsafe TypeNameHandling; its audit criterion is that untrusted payloads are not d
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0009 -> FG-K0-0282fdad6d [CANONICAL_ONLY] Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED; never PASS for a layer that was not inspected.

## CIS-K1-U0037 (pass 3) K1 .claude/skills/security-scan/references/scan-layers.md:129-129  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During applicable logging security review, review duplicate security-relevant logging in context.
TRIGGER: logging security review within a requested scan; full audits cover applicable layers, targeted scans focus affected surfaces. | EXC: Investigation only, not an automatic vulnerability declaration or mandatory product change. Severity depends on actual exposure; ordinary query parameters do not automatically imply SSRF, and successf | POL: ['WF-020']
CODEX WHY: A specific investigation can be omitted while other items in the same layer are reviewed. Whether the baseline general review obligation incorporates every prompt remains unresolved. Prior rejected labels are not accepted as normative truth.
```
 126  
 127  ## Logging
 128  
 129> Check for passwords, access/refresh tokens, private keys, authentication secrets, and full payment credentials in logs; review PII against project requirements; prefer technical identifiers over identity data. Debu
 130  
 131  ## Error responses
 132  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K1-12d7f81bf6 [129, 129] CANONICAL_ONLY/MUST_NOT pol=['SEC-010'] rel=[]: Never log passwords, tokens, private keys, authentication secrets or full payment credentials; avoid PII without a concrete permitted operational need; a lower log level does not make sensitive data safe; prefer stable technical i
- V2 FG-K1-112ed0f2b3 [129, 129] CANONICAL_ONLY/DEFAULT pol=['SEC-010', 'RUN-014'] rel=[]: Logs must not contain passwords, tokens, keys, auth secrets or full payment credentials; PII per project requirements; prefer technical identifiers; Debug/Trace is not a security boundary.
- V2 FG-K1-208cef42a1 [129, 133] CANONICAL_ONLY/MUST_NOT pol=['WF-012'] rel=['SEC-010']: Success logging is not mandatory.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0547 -> FG-K1-112ed0f2b3 [CANONICAL_ONLY] Logs must not contain passwords, tokens, keys, auth secrets or full payment credentials; PII per project requirements; prefer technical identifiers; Debug/Trace is not a security b
- NAMED primary/K1/constraints.jsonl/RULE-K1-0459 -> FG-K1-565f397580 [CANONICAL_ONLY] Log an exception at the boundary that handles or terminates the failure; when rethrowing without meaningful handling add no duplicate log.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0589 -> FG-K1-2ba1ddb032 [CANONICAL_ONLY] For dependency or security-sensitive changes inspect vulnerabilities and changed secrets, authorization, raw SQL, CORS/TLS, sensitive logging and certificate validation.
- NAMED replica/K1/constraints.jsonl/RULE-K1-0317 -> FG-K1-f0aca49ccf [CANONICAL_PLUS_DELTA] The scan is complete only when applicable layers were inspected, findings have evidence, uncertain findings are labelled and limitations are stated.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0004 -> FG-K1-de49663227 [CANONICAL_ONLY] Choose data-at-rest protection from the requirement (password hashing; hashed verification tokens; protected storage for retrievable secrets; platform/database encryption; Data Pro
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0006 -> FG-K1-ba3da08dba [CANONICAL_ONLY] A full pre-release or requested audit reviews all applicable layers; a targeted change focuses on affected layers and expands when it crosses security boundaries.

## CIS-K1-U0038 (pass 3) K1 .claude/skills/security-scan/references/scan-layers.md:129-129  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During applicable logging security review, review missing security-relevant logging in context.
TRIGGER: logging security review within a requested scan; full audits cover applicable layers, targeted scans focus affected surfaces. | EXC: Investigation only, not an automatic vulnerability declaration or mandatory product change. Severity depends on actual exposure; ordinary query parameters do not automatically imply SSRF, and successf | POL: ['WF-020']
CODEX WHY: A specific investigation can be omitted while other items in the same layer are reviewed. Whether the baseline general review obligation incorporates every prompt remains unresolved. Prior rejected labels are not accepted as normative truth.
```
 126  
 127  ## Logging
 128  
 129> Check for passwords, access/refresh tokens, private keys, authentication secrets, and full payment credentials in logs; review PII against project requirements; prefer technical identifiers over identity data. Debu
 130  
 131  ## Error responses
 132  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K1-12d7f81bf6 [129, 129] CANONICAL_ONLY/MUST_NOT pol=['SEC-010'] rel=[]: Never log passwords, tokens, private keys, authentication secrets or full payment credentials; avoid PII without a concrete permitted operational need; a lower log level does not make sensitive data safe; prefer stable technical i
- V2 FG-K1-112ed0f2b3 [129, 129] CANONICAL_ONLY/DEFAULT pol=['SEC-010', 'RUN-014'] rel=[]: Logs must not contain passwords, tokens, keys, auth secrets or full payment credentials; PII per project requirements; prefer technical identifiers; Debug/Trace is not a security boundary.
- V2 FG-K1-208cef42a1 [129, 133] CANONICAL_ONLY/MUST_NOT pol=['WF-012'] rel=['SEC-010']: Success logging is not mandatory.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0547 -> FG-K1-112ed0f2b3 [CANONICAL_ONLY] Logs must not contain passwords, tokens, keys, auth secrets or full payment credentials; PII per project requirements; prefer technical identifiers; Debug/Trace is not a security b
- NAMED primary/K1/constraints.jsonl/RULE-K1-0589 -> FG-K1-2ba1ddb032 [CANONICAL_ONLY] For dependency or security-sensitive changes inspect vulnerabilities and changed secrets, authorization, raw SQL, CORS/TLS, sensitive logging and certificate validation.
- NAMED replica/K1/constraints.jsonl/RULE-K1-0317 -> FG-K1-f0aca49ccf [CANONICAL_PLUS_DELTA] The scan is complete only when applicable layers were inspected, findings have evidence, uncertain findings are labelled and limitations are stated.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0004 -> FG-K1-de49663227 [CANONICAL_ONLY] Choose data-at-rest protection from the requirement (password hashing; hashed verification tokens; protected storage for retrievable secrets; platform/database encryption; Data Pro
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0006 -> FG-K1-ba3da08dba [CANONICAL_ONLY] A full pre-release or requested audit reviews all applicable layers; a targeted change focuses on affected layers and expands when it crosses security boundaries.
