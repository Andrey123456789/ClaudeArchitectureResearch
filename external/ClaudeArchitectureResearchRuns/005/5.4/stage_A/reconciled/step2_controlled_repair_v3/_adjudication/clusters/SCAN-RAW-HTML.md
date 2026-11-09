# SCAN-RAW-HTML (4 records)

## CIS-M1-U0048 (pass 3) M1 .claude/skills/security-scan/references/scan-layers.md:111-112  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: Review deliberate raw HTML handling in server-rendered UI.
TRIGGER: Applicable security review where server-rendered raw HTML exists | EXC: Investigation prompts, not automatic vulnerabilities or mandates to add product controls. Review only applicable surfaces; do not demand logs for every successful request; actual exposure and context  | POL: ['WF-020']
CODEX WHY: Positive review action may be separately falsifiable beyond broad security invariants, but the all-applicable-layers duty could already incorporate it.
```
 108  Investigate deliberate sanitizer bypasses and direct DOM manipulation with
 109  untrusted content in the frontend (framework-specific bypass APIs are listed in
 110  the frontend knowledge skill). Ordinary template binding benefits from
 111> framework escaping/sanitization and is not automatically XSS. Review deliberate
 112> raw HTML handling in any server-rendered UI as well.
 113  
 114  ## Unsafe Deserialization
 115  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-9856d9cf83 [108, 112] CANONICAL_ONLY/MUST_NOT pol=['WF-020', 'WF-012'] rel=[]: Do not report suspicious patterns as findings without context (ordinary LINQ predicates, every user-influenced query parameter as SSRF, ordinary template binding as XSS, non-security MD5/SHA1 checksums, entities assumed vulnerable
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

## CIS-L1-U0039 (pass 3) L1 .claude/skills/security-scan/references/scan-layers.md:27-27  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During an applicable security scan, review raw HTML handling in any server-rendered UI.
TRIGGER: The corresponding surface exists and the scan covers that layer | EXC: Investigation prompts, not automatic vulnerability declarations; assess actual behavior and contextual risk. No requirement to add controls or logs everywhere. | POL: ['WF-020']
CODEX WHY: Concrete review activity can be omitted while complying with general security invariants. Distinct from own source/lock/debug findings; investigation-prompt force remains uncertain.
```
  24  - **Command injection** — `Process.Start`, shell/PowerShell invocation, arguments built from user input; prefer APIs separating executable and arguments; constrain input.
  25  - **Path traversal** — user-controlled file names, paths, archive extraction, download/upload destinations; look for `../`, absolute-path injection, unsafe extraction; normalize and verify paths stay inside the int
  26  - **SSRF** — user influence over scheme, host, port, full URL, or redirects, especially with access to internal networks or metadata endpoints. A user-supplied query parameter alone is not SSRF; host/control-plane 
  27> - **XSS / unsafe HTML** — deliberate sanitizer bypasses and direct DOM manipulation with untrusted content in the frontend (framework-specific APIs: frontend knowledge skill); ordinary template binding benefits fro
  28  - **Unsafe deserialization** — `BinaryFormatter`, unsafe `TypeNameHandling`, deserializing untrusted payloads into arbitrary runtime types.
  29  - **Cryptography** — security-sensitive MD5, SHA1, ECB mode, hardcoded keys, custom password hashing, home-grown protocols. MD5/SHA1 as non-security checksums are fine. Passwords use established hashers such as ASP
  30  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L1-844366a741 [27, 27] CANONICAL_ONLY/DEFAULT pol=['WF-020', 'WF-012'] rel=[]: Do not report patterns without context (LINQ predicates with user input, query parameters as SSRF without host influence, ordinary template binding as XSS, returned entities without inspecting serialized fields).
- NAMED primary/L1/constraints.jsonl/RULE-L1-0551 -> FG-L1-e52b9bf6fd [CANONICAL_ONLY] Full pre-release or requested audits review all applicable layers; targeted changes start with affected layers and expand across security boundaries.
- NAMED primary/L1/constraints.jsonl/RULE-L1-0564 -> FG-L1-844366a741 [CANONICAL_ONLY] Do not report patterns without context (LINQ predicates with user input, query parameters as SSRF without host influence, ordinary template binding as XSS, returned entities withou
- NAMED primary/L1/constraints.jsonl/RULE-L1-0574 -> FG-L1-5821a256da [CANONICAL_ONLY] Check logs for never-log data, PII per requirements; Debug/Trace is not a boundary; no demand to log every successful request.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0108 -> FG-L1-15d9f150d9 [CANONICAL_ONLY] Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without permitted need; log level is not a privacy control.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0109 -> FG-L1-c4e1401ee1 [CANONICAL_ONLY] Do not serialize arbitrary request bodies, domain objects or sensitive payloads into logs by default; log the minimum operationally useful non-sensitive context.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0135 -> FG-L1-d6ab123b1f [CANONICAL_ONLY] Review for unsafe deserialization: BinaryFormatter, unsafe TypeNameHandling, deserializing untrusted payloads into arbitrary runtime types (reported as possibly illustrative).
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0137 -> FG-L1-accce90761 [CANONICAL_ONLY] Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED.

## CIS-K0-U0049 (pass 3) K0 .claude/skills/security-scan/references/scan-layers.md:73-73  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: When a server-rendered UI exists, the security-scan procedure calls for reviewing deliberate raw HTML handling in server-rendered UI.
TRIGGER: An invoked security scan in which a server-rendered UI exists | EXC: Inspect applicable surfaces only; context and actual exposure determine whether any finding exists. Investigation prompts are not automatic vulnerabilities. | POL: ['WF-020']
CODEX WHY: Angular sanitizer and general trust-boundary guidance do not independently express server-rendered HTML review. Source is procedural, but general full-layer review may semantically include it; retain uncertainty.
```
  70  
  71  ## XSS and unsafe HTML
  72  
  73> For Angular, investigate deliberate sanitizer bypasses — `bypassSecurityTrustHtml`, `bypassSecurityTrustScript`, `bypassSecurityTrustResourceUrl` — and direct DOM manipulation with untrusted content. Ordinary Angul
  74  
  75  ## Unsafe deserialization
  76  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0211 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0280 -> FG-K0-bf877ace97 [CANONICAL_ONLY] A full pre-release or requested audit reviews every applicable layer; targeted changes start with the affected layers and expand when the change crosses security boundaries.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0281 -> FG-K0-16b58514ed [CANONICAL_PLUS_DELTA] The scan completes only when applicable layers were inspected, findings carry evidence, uncertain findings are labelled and limitations stated.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0007 -> FG-K0-0ef1e5ed3d [EXTRA_WORKFLOW] A security scan investigates polymorphic or type-driven deserialization such as BinaryFormatter or unsafe TypeNameHandling; its audit criterion is that untrusted payloads are not d
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0009 -> FG-K0-0282fdad6d [CANONICAL_ONLY] Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED; never PASS for a layer that was not inspected.

## CIS-K1-U0035 (pass 3) K1 .claude/skills/security-scan/references/scan-layers.md:67-67  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: During applicable XSS review when a server-rendered UI exists, review deliberate raw HTML handling in server-rendered UI.
TRIGGER: XSS review when a server-rendered UI exists within a requested scan; full audits cover applicable layers, targeted scans focus affected surfaces. | EXC: Investigation only, not an automatic vulnerability declaration or mandatory product change. Severity depends on actual exposure; ordinary query parameters do not automatically imply SSRF, and successf | POL: ['WF-020']
CODEX WHY: A specific investigation can be omitted while other items in the same layer are reviewed. Whether the baseline general review obligation incorporates every prompt remains unresolved. Prior rejected labels are not accepted as normative truth.
```
  64  
  65  ## XSS and unsafe HTML
  66  
  67> In the frontend, investigate deliberate sanitizer bypasses and direct DOM manipulation with untrusted content (the frontend knowledge facet names the framework's bypass APIs). Ordinary template binding benefits fro
  68  
  69  ## Unsafe deserialization
  70  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/K1/constraints.jsonl/EXTRA-K1-0238 -> FG-K1-ba3da08dba [CANONICAL_ONLY] A full pre-release or requested audit reviews all applicable layers; a targeted change focuses on affected layers and expands when it crosses security boundaries.
- NAMED replica/K1/constraints.jsonl/RULE-K1-0317 -> FG-K1-f0aca49ccf [CANONICAL_PLUS_DELTA] The scan is complete only when applicable layers were inspected, findings have evidence, uncertain findings are labelled and limitations are stated.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0099 -> FG-K1-c902d1daf1 [MIXED] Angular guidance: investigate sanitization bypasses, match server XSRF validation, specific behavioral test targets and a small default E2E suite; NgModules must not work around st
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0006 -> FG-K1-ba3da08dba [CANONICAL_ONLY] A full pre-release or requested audit reviews all applicable layers; a targeted change focuses on affected layers and expands when it crosses security boundaries.
