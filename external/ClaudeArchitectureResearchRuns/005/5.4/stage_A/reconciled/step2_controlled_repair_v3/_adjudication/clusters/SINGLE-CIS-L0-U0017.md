# SINGLE-CIS-L0-U0017 (1 records)

## CIS-L0-U0017 (pass 2) L0 .claude/skills/ef-core/SKILL.md:225-225  [DEFAULT UNCERTAIN_NOVELTY]
CLAIM: For controlled production deployment, generated idempotent scripts or migration bundles are presented as often preferable migration artifacts.
TRIGGER: Choosing an artifact for controlled production deployment. | EXC: Hedged often preferable wording supplies no universal selection rule; the parent skill is technique only, and scripts versus bundles remain alternatives. | POL: ['WF-019']
CODEX WHY: Not a discovery of an unseen location: explicit prior rejection is challenged. Controlled deployment and artifact selection are partly covered; the residual idempotent-script qualification and hedged preference may or may not carry independent normative content. Preserve unresolved.
```
 222  dotnet ef migrations script --idempotent --project backend/MyApp.Infrastructure --startup-project backend/MyApp.Api
 223  ```
 224  
 225> Generated idempotent scripts or migration bundles are often preferable for controlled production deployment.
 226  
 227  ## Query performance checklist
 228  
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- NAMED primary/L0/constraints.jsonl/RULE-L0-0331 -> FG-L0-886a174d5e [CANONICAL_PLUS_DELTA] Generate migration scripts or bundles in CI and execute them as an explicit visible deployment step.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0371 -> FG-L0-d4af2076af [CANONICAL_ONLY] Production migration is an explicit deployment operation using approved credentials; scripts/bundles may be generated earlier in CI.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0183 -> FG-L0-e6cfdca837 [CANONICAL_ONLY] Deployment never runs Development seeding in Production.
