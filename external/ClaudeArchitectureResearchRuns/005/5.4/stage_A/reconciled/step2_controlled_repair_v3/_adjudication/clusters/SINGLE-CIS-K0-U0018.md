# SINGLE-CIS-K0-U0018 (1 records)

## CIS-K0-U0018 (pass 2) K0 .claude/skills/dotnet-testing/SKILL.md:117-117  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: If top-level statements make Program inaccessible for host integration testing, expose it; a public partial Program declaration is an example mechanism.
TRIGGER: Applying dotnet-testing host-integration technique and top-level Program is inaccessible. | EXC: Source gives public partial class only as an example, not an exclusive required syntax. Applicability/normative strength of on-demand knowledge remains open. | POL: ['TST-006']
CODEX WHY: Specific all-three Program/accessibility/host and exact-location record review found no equivalent conditional remedy claim. The imperative is plausible procedural guidance, but could be only an optional technique prerequisite; no mandatory public-class syntax inferred.
```
 114  }
 115  ```
 116  
 117> Configure the `Testing` environment with isolated test resources so an integration test cannot reach a development or production database by accident (`rules/backend-tests/testing.md` § Isolation and data). If top-
 118  
 119  ## Test database strategy
 120  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-6354036f6d [117, 117] CANONICAL_ONLY/MUST pol=['TST-004', 'RUN-004'] rel=[]: Tests are deterministic, order-independent and isolated from Production/Development data, uncontrolled external systems and shared mutable state; no wall-clock reliance when TimeProvider can make time deterministic; never Producti
- V2 FG-K0-04cda0563e [117, 117] CANONICAL_ONLY/DEFAULT pol=['TST-004'] rel=[]: Configure the Testing environment with isolated test resources so integration tests cannot reach a development or production database by accident.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0371 -> FG-K0-04cda0563e [CANONICAL_ONLY] Configure the Testing environment with isolated test resources so integration tests cannot reach a development or production database by accident.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0505 -> FG-K0-78ecdac255 [CANONICAL_ONLY] Integration tests may reference the API project for WebApplicationFactory<Program>.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0109 -> FG-K0-6354036f6d [CANONICAL_ONLY] Tests are deterministic, order-independent and isolated from Production/Development data, uncontrolled external systems and shared mutable state; no wall-clock reliance when TimePr
- NAMED replica/K0/constraints.jsonl/RULE-K0-0104 -> FG-K0-e17c5497d1 [CANONICAL_ONLY] WebApplicationFactory-based integration tests when routing, binding, middleware, authentication, DI, repositories, EF Core or persistence must be proven.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0024 -> FG-K0-04cda0563e [CANONICAL_ONLY] Configure the Testing environment with isolated test resources so integration tests cannot reach a development or production database by accident.
