# SINGLE-CIS-M1-U0014 (1 records)

## CIS-M1-U0014 (pass 2) M1 .claude/rules/security.md:98-105  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: Prefer stable technical identifiers when selecting operational logging context.
TRIGGER: Choosing identifying context for logs under the security rule, including cases where limited personal data is operationally needed and permitted. | EXC: A preference, not an absolute prohibition on permitted PII or a requirement to invent identifiers; required operational context and privacy/security policy still apply. | POL: ['SEC-010', 'RUN-014']
CODEX WHY: Potential independent preference omitted during atomization, not a proven EXTRA. Normative phrasing is explicit but whether it adds a separate constraint beyond minimum non-sensitive context remains open.
```
  95  
  96  ## Logging and Sensitive Data
  97  
  98> - Never log passwords, access or refresh tokens, private keys, authentication
  99>   secrets, or full payment credentials. Avoid logging PII unless there is a
 100>   concrete operational requirement and the project's privacy/security policy
 101>   permits it; prefer stable technical identifiers. Changing the log level does
 102>   not make sensitive data safe.
 103> - Do not serialize arbitrary request bodies, domain objects, or sensitive
 104>   payloads into logs by default; log the minimum operationally useful,
 105>   non-sensitive context.
 106  
 107  ## Failure Handling
 108  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-064c990ec0 [98, 102] CANONICAL_ONLY/MUST_NOT pol=['SEC-010'] rel=['SEC-012']: Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without permitted need; log level does not make data safe.
- V2 FG-M1-805f4b7b04 [103, 105] CANONICAL_ONLY/MUST_NOT pol=['RUN-014'] rel=[]: No arbitrary request bodies, domain objects or sensitive payloads in logs by default; minimum useful non-sensitive context.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0241 -> FG-M1-064c990ec0 [CANONICAL_ONLY] Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without permitted need; log level does not make data safe.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0124 -> FG-M1-064c990ec0 [CANONICAL_ONLY] Never log passwords, tokens, private keys, auth secrets or full payment credentials; avoid PII without permitted need; log level does not make data safe.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0242 -> FG-M1-805f4b7b04 [CANONICAL_ONLY] No arbitrary request bodies, domain objects or sensitive payloads in logs by default; minimum useful non-sensitive context.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0531 -> FG-M1-6e1d604324 [CANONICAL_ONLY] Avoid logging authorization headers and full sensitive bodies; log specific needed properties.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0125 -> FG-M1-805f4b7b04 [CANONICAL_ONLY] No arbitrary request bodies, domain objects or sensitive payloads in logs by default; minimum useful non-sensitive context.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0111 -> FG-M1-f4d4f40a5e [MIXED] Prefer platform trace identifiers; add an explicit correlation identifier only when required; validate or normalize an externally accepted identifier before propagating it; propaga
- NAMED primary/M1/constraints.jsonl/RULE-M1-0156 -> FG-M1-b9dabc85e3 [CANONICAL_ONLY] Use ILogger<T> with structured templates and stable property names; avoid interpolation.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0057 -> FG-M1-b9dabc85e3 [CANONICAL_ONLY] Use ILogger<T> with structured templates and stable property names; avoid interpolation.
