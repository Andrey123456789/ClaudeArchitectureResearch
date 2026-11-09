# SCAN-TARGETED-PRIORITY (2 records)

## CIS-L1-U0016 (pass 2) L1 .claude/skills/security-scan/SKILL.md:24-38  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: For a targeted security scan of a database/query change, treat access control as a priority review area.
TRIGGER: A targeted security review whose change is classified as database/query work. | EXC: Priority is not exclusive scope; skip irrelevant surfaces and expand across security boundaries. No authentication infrastructure or finding is required merely by this table. | POL: ['WF-007', 'WF-020']
CODEX WHY: The residual is whether the table independently changes review priority rather than merely illustrates already-recorded affected-surface scoping. No novelty asserted from NON_NORMATIVE label or row location alone. Similar K1 question is a separate candidate record, not evidence of cross-candidate difference.
```
  21  
  22  ## Scope
  23  
  24> Inspect which surfaces exist — backend, frontend, authentication/authorization, database access, external HTTP integrations, file upload/download, container configuration, CI/CD, production configuration, logging, 
  25> 
  26> For a full pre-release or requested audit, review all applicable layers. For targeted changes, start with the affected layers and expand when the change crosses security boundaries:
  27> 
  28> | Change | Priority areas |
  29> | --- | --- |
  30> | Dependency update | Dependencies / supply chain |
  31> | Authentication change | Authentication / access control |
  32> | New HTTP endpoint | Access control, input handling, HTTP security |
  33> | Database/query change | Injection, access control, sensitive data |
  34> | Configuration change | Secrets / configuration |
  35> | Logging change | Sensitive data / logging |
  36> | Outbound HTTP integration | Configuration, SSRF/input handling, failure handling |
  37> | File upload | Input handling, path safety, resource limits |
  38> | Frontend auth/UI change | Browser security + server authorization assumptions |
  39  
  40  ## Layers
  41  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L1-8611d59073 [24, 24] CANONICAL_ONLY/MUST pol=['WF-007'] rel=[]: Run architecture, formatting/analyzer, dependency and security checks when relevant to the change rather than indiscriminately (e.g. the architecture check when project references or packages changed).
- V2 FG-L1-8611d59073 [26, 26] CANONICAL_ONLY/MUST pol=['WF-007'] rel=[]: Run architecture, formatting/analyzer, dependency and security checks when relevant to the change rather than indiscriminately (e.g. the architecture check when project references or packages changed).
- V2 FG-L1-b8e7f36df1 [24, 24] CANONICAL_ONLY/MUST pol=['WF-007', 'WF-009'] rel=[]: Inspect which surfaces exist and skip irrelevant checks rather than reporting them as failures.
- V2 FG-L1-e52b9bf6fd [26, 26] CANONICAL_ONLY/MUST pol=['WF-007'] rel=[]: Full pre-release or requested audits review all applicable layers; targeted changes start with affected layers and expand across security boundaries.
- NAMED primary/L1/constraints.jsonl/RULE-L1-0551 -> FG-L1-e52b9bf6fd [CANONICAL_ONLY] Full pre-release or requested audits review all applicable layers; targeted changes start with affected layers and expand across security boundaries.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0210 -> FG-L1-943ebee4b6 [CANONICAL_ONLY] Never invent exploitability the code does not establish.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0135 -> FG-L1-d6ab123b1f [CANONICAL_ONLY] Review for unsafe deserialization: BinaryFormatter, unsafe TypeNameHandling, deserializing untrusted payloads into arbitrary runtime types (reported as possibly illustrative).
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0137 -> FG-L1-accce90761 [CANONICAL_ONLY] Layer status is PASS, FINDINGS, NOT APPLICABLE or NOT CHECKED.
- NAMED primary/L1/constraints.jsonl/RULE-L1-0371 -> FG-L1-636029a8f4 [CANONICAL_ONLY] When relevant check commits, destructive changes, raw SQL parameterization, authorization, trust boundaries, secrets, sensitive logging, concurrency, migrations incl. seed co-chang
- NAMED primary/L1/constraints.jsonl/RULE-L1-0568 -> FG-L1-70229c9e88 [CANONICAL_ONLY] Verify ownership, tenant or permission checks where identifiers could expose others' data; client-side filtering is not authorization.
- NAMED primary/L1/constraints.jsonl/RULE-L1-0550 -> FG-L1-b8e7f36df1 [CANONICAL_ONLY] Inspect which surfaces exist and skip irrelevant checks rather than reporting them as failures.

## CIS-K1-U0013 (pass 2) K1 .claude/skills/security-scan/SKILL.md:32-55  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: For a targeted security scan of a database/query change, treat authentication and access control (layer 4) as a priority review area.
TRIGGER: A targeted security review whose change is classified as database/query work. | EXC: Table concerns priority, not exclusive scope; irrelevant checks are skipped and scope expands across security boundaries. It does not require authentication infrastructure to exist or require a findin | POL: ['WF-007', 'WF-020']
CODEX WHY: Canonical contextual scoping and broad security review may subsume the table. The precise residual question is whether the table independently changes priority for a database/query change without an obvious altered authorization surface; it is not novelty merely from an unregistered row or different quotation.
```
  29  
  30  ## Scope
  31  
  32> Inspect which surfaces exist — .NET backend, frontend, authentication/authorization, database access, external HTTP integrations, file upload/download, container configuration, CI/CD, production configuration, logg
  33> 
  34> | Change | Priority layers |
  35> |---|---|
  36> | Dependency update | 1 |
  37> | Authentication change | 4 |
  38> | New controller endpoint | 4, 5, input handling |
  39> | Database/query change | 3, 4, 6 |
  40> | Configuration change | 2 |
  41> | Logging change | 6 |
  42> | HttpClient integration | 2, 3 (SSRF), 7 |
  43> | File upload | 3 (path safety), 5, resource limits |
  44> | Frontend auth/UI change | 5 + server authorization assumptions |
  45> 
  46> ## Layers
  47> 
  48> Detailed investigation prompts: `references/scan-layers.md`.
  49> 
  50> | # | Layer | Typical OWASP Top 10:2025 mapping |
  51> |---|---|---|
  52> | 1 | Dependencies and supply chain | A03 |
  53> | 2 | Secrets and configuration | A02, A04 |
  54> | 3 | Injection and dangerous code patterns | A04, A05, A08 |
  55> | 4 | Authentication and access control | A01, A07 |
  56  | 5 | Browser and HTTP/API security | A01, A02 |
  57  | 6 | Sensitive data, logging, and error exposure | A04, A09 |
  58  | 7 | Exceptional conditions and failure handling | A06, A10 |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K1-1e25829d2e [32, 32] CANONICAL_ONLY/MUST pol=['WF-007', 'WF-009'] rel=[]: Inspect which surfaces exist and skip irrelevant checks instead of reporting them as failures.
- V2 FG-K1-ba3da08dba [32, 32] CANONICAL_ONLY/MUST pol=['WF-007'] rel=['WF-020']: A full pre-release or requested audit reviews all applicable layers; a targeted change focuses on affected layers and expands when it crosses security boundaries.
- V2 FG-K1-ba3da08dba [36, 44] CANONICAL_ONLY/MUST pol=['WF-007'] rel=['WF-020']: A full pre-release or requested audit reviews all applicable layers; a targeted change focuses on affected layers and expands when it crosses security boundaries.
- V2 FG-K1-ac27bb9d33 [50, 58] EXTRA_WORKFLOW/DEFAULT pol=[] rel=['WF-020']: A seven-layer OWASP Top 10:2025 mapping is supplied.
- NAMED primary/K1/constraints.jsonl/EXTRA-K1-0238 -> FG-K1-ba3da08dba [CANONICAL_ONLY] A full pre-release or requested audit reviews all applicable layers; a targeted change focuses on affected layers and expands when it crosses security boundaries.
- NAMED replica/K1/constraints.jsonl/RULE-K1-0316 -> FG-K1-ba3da08dba [CANONICAL_ONLY] A full pre-release or requested audit reviews all applicable layers; a targeted change focuses on affected layers and expands when it crosses security boundaries.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0006 -> FG-K1-ba3da08dba [CANONICAL_ONLY] A full pre-release or requested audit reviews all applicable layers; a targeted change focuses on affected layers and expands when it crosses security boundaries.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0007 -> FG-K1-5566f6a31f [EXTRA_WORKFLOW] Map OWASP Top 10:2025 categories only when they genuinely fit.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0327 -> FG-K1-68fd6bf762 [CANONICAL_ONLY] Review transactions/commits, destructive data changes, raw SQL parameterization, authorization, trust boundaries, secrets, sensitive logging, concurrency, migrations and cache cons
- NAMED replica/K1/constraints.jsonl/RULE-K1-0213 -> FG-K1-68fd6bf762 [CANONICAL_ONLY] Review transactions/commits, destructive data changes, raw SQL parameterization, authorization, trust boundaries, secrets, sensitive logging, concurrency, migrations and cache cons
- NAMED primary/K1/constraints.jsonl/RULE-K1-0539 -> FG-K1-5cf38cddbd [CANONICAL_ONLY] Client-side filtering is not authorization.
