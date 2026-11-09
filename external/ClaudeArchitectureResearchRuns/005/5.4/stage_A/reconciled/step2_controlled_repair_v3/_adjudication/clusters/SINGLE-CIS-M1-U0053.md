# SINGLE-CIS-M1-U0053 (1 records)

## CIS-M1-U0053 (pass 3) M1 .claude/skills/swagger/SKILL.md:75-76  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: When a canonical resource URL exists, prefer CreatedAtAction or CreatedAtRoute for a creation response.
TRIGGER: Producing the runtime 201 Created contract with a canonical resource URL | EXC: Preference, not mandatory exclusive helper; URI condition retained. Must document actual runtime behavior. | POL: []
CODEX WHY: Source explicitly prefers helpers, but this could be explanatory implementation of the covered Location rule.
```
  72  
  73  ## Creation Responses
  74  
  75> Document `201 Created` when that is the runtime contract, and prefer
  76> `CreatedAtAction` / `CreatedAtRoute` when a canonical resource URL exists.
  77  
  78  ## Error Responses
  79  
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-M1-05089589ad [75, 76] CANONICAL_ONLY/MUST pol=['API-003'] rel=[]: Choose 200/201/202/204 by actual HTTP semantics; no blanket 200, no 201 for internal inserts, no 202 for completed work.
- V2 FG-M1-0d82a465e2 [75, 76] CANONICAL_ONLY/DEFAULT pol=['API-003'] rel=[]: A 201 response includes Location when a stable resource URI exists.
- V2 FG-M1-b77b89232d [75, 76] CANONICAL_ONLY/DEFAULT pol=['API-003'] rel=[]: A 201 response includes Location when a stable resource URI exists.
- V2 FG-M1-7b5693b4e3 [75, 76] CANONICAL_ONLY/MUST pol=['API-016'] rel=[]: Swagger/OpenAPI metadata describes the API that actually runs (routes, important statuses, schemas, authentication); no speculative responses.
- V2 FG-M1-e129044704 [75, 76] CANONICAL_ONLY/DEFAULT pol=['API-016', 'API-003'] rel=[]: Document 201 Created only when it is the runtime contract.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0071 -> FG-M1-b77b89232d [CANONICAL_ONLY] A 201 response includes Location when a stable resource URI exists.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0649 -> FG-M1-e129044704 [CANONICAL_ONLY] Document 201 Created only when it is the runtime contract.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0018 -> FG-M1-0d82a465e2 [CANONICAL_ONLY] A 201 response includes Location when a stable resource URI exists.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0026 -> FG-M1-7b5693b4e3 [CANONICAL_ONLY] Swagger/OpenAPI metadata describes the API that actually runs (routes, important statuses, schemas, authentication); no speculative responses.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0118 -> FG-M1-a876ee45ce [CANONICAL_PLUS_DELTA] When API behavior changes, open the Development Swagger UI and confirm it loads when the change alters API behavior and the project exposes the UI in Development, even when startup
