# SINGLE-CIS-L0-U0033 (1 records)

## CIS-L0-U0033 (pass 3) L0 .claude/skills/aspnet-error-handling/SKILL.md:93-93  [MAY UNCERTAIN_NOVELTY]
CLAIM: A useful ProblemDetails contract may contain a stable machine-readable error code when clients need one.
TRIGGER: when clients need one | EXC: Technique-only skill; permission is not a presence requirement. Existing safe/stable error-contract rules and approved product contracts still apply. | POL: ['API-008']
CODEX WHY: Explicit permissive wording is source-verified. It may merely describe conventional contract contents rather than independently constrain admissible behavior; this normativity/subsumption ambiguity remains open.
```
  90  
  91  ## Error contract contents
  92  
  93> A useful ProblemDetails contract may contain the HTTP status, a stable machine-readable error code when clients need one, a human-readable title, a safe detail, and a correlation/trace identifier when appropriate.
  94  
  95  ## Request validation wiring
  96  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L0/constraints.jsonl/RULE-L0-0145 -> FG-L0-34172df011 [CANONICAL_ONLY] HTTP failures use a structured problem-details contract whose machine-readable parts stay stable and safe.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0180 -> FG-L0-2c9dd38e7b [CANONICAL_ONLY] ProblemDetails for non-validation failures and ValidationProblemDetails for request validation; stable safe machine-readable fields.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0089 -> FG-L0-34172df011 [CANONICAL_ONLY] HTTP failures use a structured problem-details contract whose machine-readable parts stay stable and safe.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0023 -> FG-L0-3f0ff267b6 [CANONICAL_PLUS_DELTA] Centralized unexpected-exception handling uses IExceptionHandler with AddProblemDetails()/UseExceptionHandler().
