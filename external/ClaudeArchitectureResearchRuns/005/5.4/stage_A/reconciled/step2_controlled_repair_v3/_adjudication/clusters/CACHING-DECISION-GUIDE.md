# CACHING-DECISION-GUIDE (10 records)

## CIS-M-U0040 (pass 3) M .claude/skills/caching/SKILL.md:144-144  [DEFAULT UNCERTAIN_NOVELTY]
CLAIM: For an entire reusable HTTP response, the caching decision guide gives ASP.NET Core output caching as the default consideration.
TRIGGER: Using the caching skill for an entire reusable HTTP response after a concrete caching need exists | EXC: Default consideration, not mandatory installation or exclusive list; HybridCache explicitly not mandatory (35-37). Distributed infrastructure remains Reserved and deployment requirements must justify  | POL: []
CODEX WHY: Specific technology-to-need mapping was called a duplicate of broad placement/need policies. Whether it changes an independently falsifiable decision rather than documenting options is unresolved.
```
 141  
 142  | Need | Default consideration |
 143  |---|---|
 144> | Entire reusable HTTP response | ASP.NET Core output caching |
 145  | Local application cache | In-memory or HybridCache |
 146  | Multi-instance shared cache | Distributed cache / HybridCache L2 (Reserved: new infrastructure) |
 147  | Expensive repeated remote read | Cache in Infrastructure when the contract permits |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-M-e4ebf7038a [142, 149] CANONICAL_ONLY/MUST pol=['ARC-024'] rel=[]: Keep cache technology out of Domain; do not leak infrastructure cache APIs into Application without a deliberate boundary abstraction.
- V2 FG-M-2f8f82443b [142, 149] CANONICAL_ONLY/DEFAULT pol=['RUN-007'] rel=[]: Caching is an optimization, introduced only for a clear measured/reasoned need; implementation chosen from deployment, consistency and staleness requirements.
- V2 FG-M-4ba9006a5a [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['GOV-017', 'ARC-020'] rel=[]: Reserved decisions require explicit approval, including changing an accepted project or architecture decision.
- V2 FG-M-513c353770 [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'ARC-004', 'ARC-009'] rel=[]: A new architectural style/pattern (Rich Domain/DDD tactical, CQRS/MediatR/VSA, event sourcing, microservices) is Reserved.
- V2 FG-M-749161ab42 [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: A new production project, layer or assembly, or an additional DbContext/persistence boundary, is Reserved.
- V2 FG-M-61e26b5432 [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'DEP-002'] rel=[]: Changed persistence boundaries or persistence technology are Reserved.
- V2 FG-M-4b2e39b049 [142, 149] CANONICAL_PLUS_DELTA/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: Introducing search, external storage or external identity infrastructure is Reserved.
- V2 FG-M-809acdb398 [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: New infrastructure category (messaging, background processing, distributed caching) is Reserved.
- V2 FG-M-61cc55669d [142, 149] EXTRA_PRODUCT/REQUIRES_APPROVAL pol=[] rel=['ARC-020', 'DEP-001', 'DEP-005']: Adding any major library or framework is Reserved (requires approval).
- V2 FG-M-86387ea16c [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'DEP-002'] rel=[]: Replacing an approved baseline technology is Reserved.
- V2 FG-M-7244e1d057 [142, 149] EXTRA_PRODUCT/REQUIRES_APPROVAL pol=[] rel=['ARC-020', 'GOV-012']: Any project-wide convention or abstraction other code must follow is Reserved.
- V2 FG-M-566af20434 [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: A new or changed authentication/authorization architecture is Reserved.
- V2 FG-M-21cbfa88b3 [142, 149] CANONICAL_PLUS_DELTA/REQUIRES_APPROVAL pol=['API-014'] rel=[]: A breaking public API change is Reserved (requires approval).
- NAMED primary/M/constraints.jsonl/RULE-M-0321 -> FG-M-c3b4ac323e [CANONICAL_ONLY] When a use case genuinely needs cache-aware behaviour define the abstraction in Application and implement it in Infrastructure; do not introduce an Application cache abstraction if
- NAMED primary/M/constraints.jsonl/RULE-M-0323 -> FG-M-9050e41bb6 [CANONICAL_ONLY] HybridCache may implement an Infrastructure cache contract but does not appear in Application contracts.
- NAMED replica/M/constraints.jsonl/RULE-M-0061 -> FG-M-e4ebf7038a [CANONICAL_ONLY] Keep cache technology out of Domain; do not leak infrastructure cache APIs into Application without a deliberate boundary abstraction.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0056 -> FG-M-8ac0f2b686 [CANONICAL_PLUS_DELTA] Adding caching solely for performance requires a measurement first (reported as stronger than 'measured or reasoned need').
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0057 -> FG-M-2a5d78e63e [EXTRA_PRODUCT] Avoid caching EF tracked entities across Unit of Work boundaries.

## CIS-M-U0041 (pass 3) M .claude/skills/caching/SKILL.md:145-145  [DEFAULT UNCERTAIN_NOVELTY]
CLAIM: For a local application cache, the caching decision guide gives in-memory caching or HybridCache as the default consideration.
TRIGGER: Using the caching skill for a local application cache after a concrete caching need exists | EXC: Default consideration, not mandatory installation or exclusive list; HybridCache explicitly not mandatory (35-37). Distributed infrastructure remains Reserved and deployment requirements must justify  | POL: []
CODEX WHY: Specific technology-to-need mapping was called a duplicate of broad placement/need policies. Whether it changes an independently falsifiable decision rather than documenting options is unresolved.
```
 142  | Need | Default consideration |
 143  |---|---|
 144  | Entire reusable HTTP response | ASP.NET Core output caching |
 145> | Local application cache | In-memory or HybridCache |
 146  | Multi-instance shared cache | Distributed cache / HybridCache L2 (Reserved: new infrastructure) |
 147  | Expensive repeated remote read | Cache in Infrastructure when the contract permits |
 148  | Application-controlled invalidation | Application abstraction + Infrastructure implementation |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-M-e4ebf7038a [142, 149] CANONICAL_ONLY/MUST pol=['ARC-024'] rel=[]: Keep cache technology out of Domain; do not leak infrastructure cache APIs into Application without a deliberate boundary abstraction.
- V2 FG-M-2f8f82443b [142, 149] CANONICAL_ONLY/DEFAULT pol=['RUN-007'] rel=[]: Caching is an optimization, introduced only for a clear measured/reasoned need; implementation chosen from deployment, consistency and staleness requirements.
- V2 FG-M-4ba9006a5a [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['GOV-017', 'ARC-020'] rel=[]: Reserved decisions require explicit approval, including changing an accepted project or architecture decision.
- V2 FG-M-513c353770 [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'ARC-004', 'ARC-009'] rel=[]: A new architectural style/pattern (Rich Domain/DDD tactical, CQRS/MediatR/VSA, event sourcing, microservices) is Reserved.
- V2 FG-M-749161ab42 [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: A new production project, layer or assembly, or an additional DbContext/persistence boundary, is Reserved.
- V2 FG-M-61e26b5432 [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'DEP-002'] rel=[]: Changed persistence boundaries or persistence technology are Reserved.
- V2 FG-M-4b2e39b049 [142, 149] CANONICAL_PLUS_DELTA/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: Introducing search, external storage or external identity infrastructure is Reserved.
- V2 FG-M-809acdb398 [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: New infrastructure category (messaging, background processing, distributed caching) is Reserved.
- V2 FG-M-61cc55669d [142, 149] EXTRA_PRODUCT/REQUIRES_APPROVAL pol=[] rel=['ARC-020', 'DEP-001', 'DEP-005']: Adding any major library or framework is Reserved (requires approval).
- V2 FG-M-86387ea16c [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'DEP-002'] rel=[]: Replacing an approved baseline technology is Reserved.
- V2 FG-M-7244e1d057 [142, 149] EXTRA_PRODUCT/REQUIRES_APPROVAL pol=[] rel=['ARC-020', 'GOV-012']: Any project-wide convention or abstraction other code must follow is Reserved.
- V2 FG-M-566af20434 [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: A new or changed authentication/authorization architecture is Reserved.
- V2 FG-M-21cbfa88b3 [142, 149] CANONICAL_PLUS_DELTA/REQUIRES_APPROVAL pol=['API-014'] rel=[]: A breaking public API change is Reserved (requires approval).
- NAMED primary/M/constraints.jsonl/RULE-M-0321 -> FG-M-c3b4ac323e [CANONICAL_ONLY] When a use case genuinely needs cache-aware behaviour define the abstraction in Application and implement it in Infrastructure; do not introduce an Application cache abstraction if
- NAMED primary/M/constraints.jsonl/RULE-M-0323 -> FG-M-9050e41bb6 [CANONICAL_ONLY] HybridCache may implement an Infrastructure cache contract but does not appear in Application contracts.
- NAMED replica/M/constraints.jsonl/RULE-M-0061 -> FG-M-e4ebf7038a [CANONICAL_ONLY] Keep cache technology out of Domain; do not leak infrastructure cache APIs into Application without a deliberate boundary abstraction.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0056 -> FG-M-8ac0f2b686 [CANONICAL_PLUS_DELTA] Adding caching solely for performance requires a measurement first (reported as stronger than 'measured or reasoned need').
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0057 -> FG-M-2a5d78e63e [EXTRA_PRODUCT] Avoid caching EF tracked entities across Unit of Work boundaries.

## CIS-M-U0042 (pass 3) M .claude/skills/caching/SKILL.md:146-146  [DEFAULT UNCERTAIN_NOVELTY]
CLAIM: For a multi-instance shared cache, the caching decision guide gives a distributed cache or HybridCache L2 as the default consideration.
TRIGGER: Using the caching skill for a multi-instance shared cache after a concrete caching need exists | EXC: Default consideration, not mandatory installation or exclusive list; HybridCache explicitly not mandatory (35-37). Distributed infrastructure remains Reserved and deployment requirements must justify  | POL: []
CODEX WHY: Specific technology-to-need mapping was called a duplicate of broad placement/need policies. Whether it changes an independently falsifiable decision rather than documenting options is unresolved.
```
 143  |---|---|
 144  | Entire reusable HTTP response | ASP.NET Core output caching |
 145  | Local application cache | In-memory or HybridCache |
 146> | Multi-instance shared cache | Distributed cache / HybridCache L2 (Reserved: new infrastructure) |
 147  | Expensive repeated remote read | Cache in Infrastructure when the contract permits |
 148  | Application-controlled invalidation | Application abstraction + Infrastructure implementation |
 149  | Unknown performance problem | Measure before adding caching |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-M-e4ebf7038a [142, 149] CANONICAL_ONLY/MUST pol=['ARC-024'] rel=[]: Keep cache technology out of Domain; do not leak infrastructure cache APIs into Application without a deliberate boundary abstraction.
- V2 FG-M-2f8f82443b [142, 149] CANONICAL_ONLY/DEFAULT pol=['RUN-007'] rel=[]: Caching is an optimization, introduced only for a clear measured/reasoned need; implementation chosen from deployment, consistency and staleness requirements.
- V2 FG-M-4ba9006a5a [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['GOV-017', 'ARC-020'] rel=[]: Reserved decisions require explicit approval, including changing an accepted project or architecture decision.
- V2 FG-M-513c353770 [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'ARC-004', 'ARC-009'] rel=[]: A new architectural style/pattern (Rich Domain/DDD tactical, CQRS/MediatR/VSA, event sourcing, microservices) is Reserved.
- V2 FG-M-749161ab42 [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: A new production project, layer or assembly, or an additional DbContext/persistence boundary, is Reserved.
- V2 FG-M-61e26b5432 [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'DEP-002'] rel=[]: Changed persistence boundaries or persistence technology are Reserved.
- V2 FG-M-4b2e39b049 [142, 149] CANONICAL_PLUS_DELTA/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: Introducing search, external storage or external identity infrastructure is Reserved.
- V2 FG-M-809acdb398 [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: New infrastructure category (messaging, background processing, distributed caching) is Reserved.
- V2 FG-M-61cc55669d [142, 149] EXTRA_PRODUCT/REQUIRES_APPROVAL pol=[] rel=['ARC-020', 'DEP-001', 'DEP-005']: Adding any major library or framework is Reserved (requires approval).
- V2 FG-M-86387ea16c [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'DEP-002'] rel=[]: Replacing an approved baseline technology is Reserved.
- V2 FG-M-7244e1d057 [142, 149] EXTRA_PRODUCT/REQUIRES_APPROVAL pol=[] rel=['ARC-020', 'GOV-012']: Any project-wide convention or abstraction other code must follow is Reserved.
- V2 FG-M-566af20434 [142, 149] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: A new or changed authentication/authorization architecture is Reserved.
- V2 FG-M-21cbfa88b3 [142, 149] CANONICAL_PLUS_DELTA/REQUIRES_APPROVAL pol=['API-014'] rel=[]: A breaking public API change is Reserved (requires approval).
- NAMED primary/M/constraints.jsonl/RULE-M-0321 -> FG-M-c3b4ac323e [CANONICAL_ONLY] When a use case genuinely needs cache-aware behaviour define the abstraction in Application and implement it in Infrastructure; do not introduce an Application cache abstraction if
- NAMED primary/M/constraints.jsonl/RULE-M-0323 -> FG-M-9050e41bb6 [CANONICAL_ONLY] HybridCache may implement an Infrastructure cache contract but does not appear in Application contracts.
- NAMED replica/M/constraints.jsonl/RULE-M-0061 -> FG-M-e4ebf7038a [CANONICAL_ONLY] Keep cache technology out of Domain; do not leak infrastructure cache APIs into Application without a deliberate boundary abstraction.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0056 -> FG-M-8ac0f2b686 [CANONICAL_PLUS_DELTA] Adding caching solely for performance requires a measurement first (reported as stronger than 'measured or reasoned need').
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0057 -> FG-M-2a5d78e63e [EXTRA_PRODUCT] Avoid caching EF tracked entities across Unit of Work boundaries.

## CIS-M1-U0028 (pass 3) M1 .claude/skills/caching/SKILL.md:143-143  [DEFAULT UNCERTAIN_NOVELTY]
CLAIM: For a local application cache, consider in-memory caching or HybridCache by default.
TRIGGER: Choosing technology after a justified need for a local application cache is established | EXC: Nonexclusive default consideration, not mandatory adoption. HybridCache explicitly not mandatory. Deployment justification, acceptable consistency/staleness and Reserved distributed-cache approval rem | POL: ['RUN-022']
CODEX WHY: A conditional technique recommendation is plausible distinct content; broad implementation-selection policy and optionality keep normativity/equivalence unsettled.
```
 140  | Need | Default consideration |
 141  |---|---|
 142  | Entire reusable HTTP response | ASP.NET Core output caching |
 143> | Local application cache | In-memory or HybridCache |
 144  | Multi-instance shared cache | Distributed cache / HybridCache L2 |
 145  | Expensive repeated remote read | Cache in Infrastructure when the contract permits |
 146  | Application-controlled invalidation | Application abstraction + Infrastructure implementation |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-M1-60bc8ca680 [140, 147] CANONICAL_ONLY/MUST pol=['ARC-024'] rel=[]: Keep cache technology out of Domain; no infrastructure cache APIs in Application without a deliberate boundary abstraction.
- V2 FG-M1-83187b4219 [140, 147] CANONICAL_ONLY/DEFAULT pol=['RUN-007'] rel=[]: Caching only for clear measured/reasoned need with acceptable staleness; implementation per deployment/consistency/staleness; not merely because read frequently.
- V2 FG-M1-aa1d48d81a [140, 147] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['GOV-017', 'ARC-020'] rel=[]: Reserved decisions require explicit approval.
- V2 FG-M1-a1120dca8a [140, 147] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['GOV-017', 'ARC-020', 'DEP-002'] rel=[]: Changing an accepted project or architecture decision, including a capability selection, is Reserved.
- V2 FG-M1-a678e1dd48 [140, 147] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'ARC-004', 'ARC-009'] rel=[]: Adopting a new architectural style/pattern (CQRS, mediator, VSA, event sourcing, microservices, Rich Domain/DDD tactical patterns, project-wide Result) is Reserved.
- V2 FG-M1-ec0bf7c599 [140, 147] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: Adding a production project, layer or assembly is Reserved.
- V2 FG-M1-f5fb596e81 [140, 147] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'DEP-002'] rel=[]: Changing persistence boundaries (incl. multiple persistence contexts) or persistence technology is Reserved.
- V2 FG-M1-6e49bc1b6a [140, 147] CANONICAL_PLUS_DELTA/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: Adding search, external storage or external identity infrastructure is Reserved.
- V2 FG-M1-b67c6601d0 [140, 147] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: Adding messaging, background processing or distributed caching infrastructure is Reserved.
- V2 FG-M1-a69b03fc1f [140, 147] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'DEP-002'] rel=[]: Replacing an approved baseline technology is Reserved.
- V2 FG-M1-fadcf75ee6 [140, 147] EXTRA_PRODUCT/REQUIRES_APPROVAL pol=[] rel=['ARC-020', 'DEP-001', 'GOV-013']: Adding a major library or framework is Reserved.
- V2 FG-M1-b9dca5c65e [140, 147] EXTRA_PRODUCT/REQUIRES_APPROVAL pol=[] rel=['ARC-020']: Introducing any project-wide convention or abstraction other code must follow is Reserved.
- V2 FG-M1-9bc9dc17e1 [140, 147] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: Changing the authentication/authorization architecture is Reserved.
- V2 FG-M1-97651b7a0d [140, 147] CANONICAL_PLUS_DELTA/REQUIRES_APPROVAL pol=['API-014'] rel=[]: A breaking public API change is Reserved.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0360 -> FG-M1-ae19d24e58 [CANONICAL_ONLY] Add a distributed backend such as Redis only when deployment requirements justify it (distributed caching is Reserved).
- NAMED primary/M1/constraints.jsonl/RULE-M1-0361 -> FG-M1-7390ef4e06 [CANONICAL_ONLY] Do not expose HybridCache itself from Application contracts (Infrastructure may implement the contract with it).
- NAMED replica/M1/constraints.jsonl/RULE-M1-0093 -> FG-M1-83187b4219 [CANONICAL_ONLY] Caching only for clear measured/reasoned need with acceptable staleness; implementation per deployment/consistency/staleness; not merely because read frequently.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0085 -> FG-M1-ae19d24e58 [CANONICAL_ONLY] Add a distributed backend such as Redis only when deployment requirements justify it (distributed caching is Reserved).

## CIS-M1-U0029 (pass 3) M1 .claude/skills/caching/SKILL.md:144-144  [DEFAULT UNCERTAIN_NOVELTY]
CLAIM: For a multi-instance shared cache, consider distributed caching or HybridCache L2 by default.
TRIGGER: Choosing technology after a justified need for a multi-instance shared cache is established | EXC: Nonexclusive default consideration, not mandatory adoption. HybridCache explicitly not mandatory. Deployment justification, acceptable consistency/staleness and Reserved distributed-cache approval rem | POL: ['RUN-022']
CODEX WHY: A conditional technique recommendation is plausible distinct content; broad implementation-selection policy and optionality keep normativity/equivalence unsettled.
```
 141  |---|---|
 142  | Entire reusable HTTP response | ASP.NET Core output caching |
 143  | Local application cache | In-memory or HybridCache |
 144> | Multi-instance shared cache | Distributed cache / HybridCache L2 |
 145  | Expensive repeated remote read | Cache in Infrastructure when the contract permits |
 146  | Application-controlled invalidation | Application abstraction + Infrastructure implementation |
 147  | Unknown performance problem | Measure before adding caching |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-M1-60bc8ca680 [140, 147] CANONICAL_ONLY/MUST pol=['ARC-024'] rel=[]: Keep cache technology out of Domain; no infrastructure cache APIs in Application without a deliberate boundary abstraction.
- V2 FG-M1-83187b4219 [140, 147] CANONICAL_ONLY/DEFAULT pol=['RUN-007'] rel=[]: Caching only for clear measured/reasoned need with acceptable staleness; implementation per deployment/consistency/staleness; not merely because read frequently.
- V2 FG-M1-aa1d48d81a [140, 147] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['GOV-017', 'ARC-020'] rel=[]: Reserved decisions require explicit approval.
- V2 FG-M1-a1120dca8a [140, 147] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['GOV-017', 'ARC-020', 'DEP-002'] rel=[]: Changing an accepted project or architecture decision, including a capability selection, is Reserved.
- V2 FG-M1-a678e1dd48 [140, 147] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'ARC-004', 'ARC-009'] rel=[]: Adopting a new architectural style/pattern (CQRS, mediator, VSA, event sourcing, microservices, Rich Domain/DDD tactical patterns, project-wide Result) is Reserved.
- V2 FG-M1-ec0bf7c599 [140, 147] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: Adding a production project, layer or assembly is Reserved.
- V2 FG-M1-f5fb596e81 [140, 147] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'DEP-002'] rel=[]: Changing persistence boundaries (incl. multiple persistence contexts) or persistence technology is Reserved.
- V2 FG-M1-6e49bc1b6a [140, 147] CANONICAL_PLUS_DELTA/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: Adding search, external storage or external identity infrastructure is Reserved.
- V2 FG-M1-b67c6601d0 [140, 147] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: Adding messaging, background processing or distributed caching infrastructure is Reserved.
- V2 FG-M1-a69b03fc1f [140, 147] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'DEP-002'] rel=[]: Replacing an approved baseline technology is Reserved.
- V2 FG-M1-fadcf75ee6 [140, 147] EXTRA_PRODUCT/REQUIRES_APPROVAL pol=[] rel=['ARC-020', 'DEP-001', 'GOV-013']: Adding a major library or framework is Reserved.
- V2 FG-M1-b9dca5c65e [140, 147] EXTRA_PRODUCT/REQUIRES_APPROVAL pol=[] rel=['ARC-020']: Introducing any project-wide convention or abstraction other code must follow is Reserved.
- V2 FG-M1-9bc9dc17e1 [140, 147] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: Changing the authentication/authorization architecture is Reserved.
- V2 FG-M1-97651b7a0d [140, 147] CANONICAL_PLUS_DELTA/REQUIRES_APPROVAL pol=['API-014'] rel=[]: A breaking public API change is Reserved.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0360 -> FG-M1-ae19d24e58 [CANONICAL_ONLY] Add a distributed backend such as Redis only when deployment requirements justify it (distributed caching is Reserved).
- NAMED primary/M1/constraints.jsonl/RULE-M1-0361 -> FG-M1-7390ef4e06 [CANONICAL_ONLY] Do not expose HybridCache itself from Application contracts (Infrastructure may implement the contract with it).
- NAMED replica/M1/constraints.jsonl/RULE-M1-0093 -> FG-M1-83187b4219 [CANONICAL_ONLY] Caching only for clear measured/reasoned need with acceptable staleness; implementation per deployment/consistency/staleness; not merely because read frequently.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0085 -> FG-M1-ae19d24e58 [CANONICAL_ONLY] Add a distributed backend such as Redis only when deployment requirements justify it (distributed caching is Reserved).

## CIS-L1-U0022 (pass 3) L1 .claude/skills/caching/SKILL.md:79-79  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For a local application cache, consider in-memory caching or HybridCache.
TRIGGER: Selecting a solution for a local application cache | EXC: Consider recommendation, not mandatory adoption; distributed infrastructure remains Reserved; HybridCache explicitly not mandatory. | POL: []
CODEX WHY: Permission/approval and anti-default caching constraints can be satisfied without following this recommendation. Table may still be nonbinding advice.
```
  76  | Need | Consider |
  77  | --- | --- |
  78  | Entire reusable HTTP response | output caching |
  79> | Local application cache | in-memory or HybridCache |
  80  | Multi-instance shared cache | distributed cache / HybridCache L2 (Reserved) |
  81  | Expensive repeated remote read | cache inside the adapter |
  82  | Use-case-controlled invalidation | use-case abstraction + adapter implementation |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- NAMED primary/L1/constraints.jsonl/RULE-L1-0340 -> FG-L1-7b96317821 [CANONICAL_ONLY] Add a distributed backend such as Redis only when deployment requirements justify it.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0170 -> FG-L1-f4b94cab92 [CANONICAL_ONLY] Adding new production projects/layers is Reserved.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0097 -> FG-L1-b671db9dfd [MIXED] Cache keys include entity id, tenant, user when genuinely user-specific, locale and relevant query parameters; centralize key construction once formats repeat.

## CIS-L1-U0023 (pass 3) L1 .claude/skills/caching/SKILL.md:80-80  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For a multi-instance shared cache, consider distributed caching or HybridCache L2.
TRIGGER: Selecting a solution for a multi-instance shared cache | EXC: Consider recommendation, not mandatory adoption; distributed infrastructure remains Reserved; HybridCache explicitly not mandatory. | POL: []
CODEX WHY: Permission/approval and anti-default caching constraints can be satisfied without following this recommendation. Table may still be nonbinding advice.
```
  77  | --- | --- |
  78  | Entire reusable HTTP response | output caching |
  79  | Local application cache | in-memory or HybridCache |
  80> | Multi-instance shared cache | distributed cache / HybridCache L2 (Reserved) |
  81  | Expensive repeated remote read | cache inside the adapter |
  82  | Use-case-controlled invalidation | use-case abstraction + adapter implementation |
  83  | Unknown performance problem | measure first |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-L1-399f7fe97a [80, 80] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['GOV-017', 'ARC-020'] rel=[]: Reserved choices require approval.
- V2 FG-L1-3b6bdaa5f8 [80, 80] CANONICAL_PLUS_DELTA/REQUIRES_APPROVAL pol=['API-014'] rel=['ARC-020']: A breaking public API change requires approval.
- V2 FG-L1-4eb377d522 [80, 80] EXTRA_PRODUCT/REQUIRES_APPROVAL pol=[] rel=['DEP-001', 'GOV-013']: Adding a major library/framework is Reserved.
- V2 FG-L1-5eddccea01 [80, 80] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'DEP-002'] rel=[]: Replacing baseline technology is Reserved.
- V2 FG-L1-65898726d4 [80, 80] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: Adding messaging, background processing or distributed cache infrastructure is Reserved.
- V2 FG-L1-6b0ca91c65 [80, 80] EXTRA_PRODUCT/REQUIRES_APPROVAL pol=[] rel=['ARC-020']: Introducing any project-wide convention or abstraction is Reserved.
- V2 FG-L1-7bebdf74c9 [80, 80] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'ARC-004', 'ARC-009'] rel=[]: Adopting new architectural styles/patterns (Rich Domain/DDD, CQRS, mediator, VSA, event sourcing, project-wide Result, microservices) is Reserved.
- V2 FG-L1-dcda9be79a [80, 80] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['GOV-017', 'ARC-020'] rel=[]: Changing accepted decisions is Reserved.
- V2 FG-L1-e95e3c3b4e [80, 80] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'DEP-002'] rel=[]: Persistence boundary or technology changes are Reserved.
- V2 FG-L1-efe0f6abe1 [80, 80] CANONICAL_PLUS_DELTA/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: Adding search, external storage or external identity infrastructure is Reserved.
- V2 FG-L1-f1fc3d4d2b [80, 80] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: Changing the authentication architecture is Reserved.
- V2 FG-L1-f4b94cab92 [80, 80] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: Adding new production projects/layers is Reserved.
- NAMED primary/L1/constraints.jsonl/RULE-L1-0340 -> FG-L1-7b96317821 [CANONICAL_ONLY] Add a distributed backend such as Redis only when deployment requirements justify it.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0170 -> FG-L1-f4b94cab92 [CANONICAL_ONLY] Adding new production projects/layers is Reserved.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0097 -> FG-L1-b671db9dfd [MIXED] Cache keys include entity id, tenant, user when genuinely user-specific, locale and relevant query parameters; centralize key construction once formats repeat.

## CIS-K0-U0032 (pass 3) K0 .claude/skills/caching/SKILL.md:102-102  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: The decision guide associates local application cache with in-memory or HybridCache as a consideration, potentially narrower selection guidance than deployment-based cache choice.
TRIGGER: An established need for local application cache under the caching skill | EXC: Table heading is Consideration; not exclusive or mandatory. Distributed infrastructure remains Reserved. | POL: ['RUN-007', 'ARC-024']
CODEX WHY: Potential selection recommendation absent as an independent proposition; weak table modality and general baseline coverage prevent verified novelty.
```
  99  | Need | Consideration |
 100  |---|---|
 101  | Entire reusable HTTP response | ASP.NET Core output caching |
 102> | Local application cache | In-memory or HybridCache |
 103  | Multi-instance shared cache | Distributed cache / HybridCache L2 (Reserved) |
 104  | Expensive repeated remote read | Cache in Infrastructure when the contract permits |
 105  | Application-controlled invalidation | Application abstraction + Infrastructure implementation |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-K0-debf9372df [99, 106] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: Distributed caching is Reserved.
- V2 FG-K0-f9aafcfecc [101, 106] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: New messaging, background-processing or distributed-cache infrastructure is Reserved.
- V2 FG-K0-0b760dcf90 [99, 106] CANONICAL_ONLY/DEFAULT pol=['RUN-007'] rel=[]: Caching is an optimization, not an architecture requirement; introduce it only for a clear measured or reasoned need and choose the implementation by deployment, consistency and staleness requirements, never merely because a value
- V2 FG-K0-0b760dcf90 [101, 106] CANONICAL_ONLY/DEFAULT pol=['RUN-007'] rel=[]: Caching is an optimization, not an architecture requirement; introduce it only for a clear measured or reasoned need and choose the implementation by deployment, consistency and staleness requirements, never merely because a value
- V2 FG-K0-24c5c9b14b [99, 106] CANONICAL_ONLY/MUST pol=['ARC-024'] rel=[]: Cache technology stays out of Domain; infrastructure cache APIs never leak into Application without a deliberate boundary abstraction.
- V2 FG-K0-24c5c9b14b [101, 106] CANONICAL_ONLY/MUST pol=['ARC-024'] rel=[]: Cache technology stays out of Domain; infrastructure cache APIs never leak into Application without a deliberate boundary abstraction.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0143 -> FG-K0-0b760dcf90 [CANONICAL_ONLY] Caching is an optimization, not an architecture requirement; introduce it only for a clear measured or reasoned need and choose the implementation by deployment, consistency and st
- NAMED primary/K0/constraints.jsonl/RULE-K0-0299 -> FG-K0-3aa34979c8 [CANONICAL_ONLY] Infrastructure may implement the cache abstraction with HybridCache, which stays out of Application contracts.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0049 -> FG-K0-0b760dcf90 [CANONICAL_ONLY] Caching is an optimization, not an architecture requirement; introduce it only for a clear measured or reasoned need and choose the implementation by deployment, consistency and st
- NAMED replica/K0/constraints.jsonl/RULE-K0-0048 -> FG-K0-debf9372df [CANONICAL_ONLY] Distributed caching is Reserved.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0062 -> FG-K0-f5cd026e7f [CANONICAL_PLUS_DELTA] Measure before adding caching purely for performance.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0063 -> FG-K0-1e498959c9 [NON_NORMATIVE] The output-cache example embeds a five-minute TTL without a local illustrative-value caveat (reported copy risk).

## CIS-K0-U0033 (pass 3) K0 .claude/skills/caching/SKILL.md:103-103  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: The decision guide associates multi-instance shared cache with distributed cache or HybridCache L2 as a consideration, potentially narrower selection guidance than deployment-based cache choice.
TRIGGER: An established need for multi-instance shared cache under the caching skill | EXC: Table heading is Consideration; not exclusive or mandatory. Distributed infrastructure remains Reserved. | POL: ['RUN-007', 'ARC-024']
CODEX WHY: Potential selection recommendation absent as an independent proposition; weak table modality and general baseline coverage prevent verified novelty.
```
 100  |---|---|
 101  | Entire reusable HTTP response | ASP.NET Core output caching |
 102  | Local application cache | In-memory or HybridCache |
 103> | Multi-instance shared cache | Distributed cache / HybridCache L2 (Reserved) |
 104  | Expensive repeated remote read | Cache in Infrastructure when the contract permits |
 105  | Application-controlled invalidation | Application abstraction + Infrastructure implementation |
 106  | Unknown performance problem | Measure first |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-K0-debf9372df [99, 106] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: Distributed caching is Reserved.
- V2 FG-K0-f9aafcfecc [101, 106] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: New messaging, background-processing or distributed-cache infrastructure is Reserved.
- V2 FG-K0-0b760dcf90 [99, 106] CANONICAL_ONLY/DEFAULT pol=['RUN-007'] rel=[]: Caching is an optimization, not an architecture requirement; introduce it only for a clear measured or reasoned need and choose the implementation by deployment, consistency and staleness requirements, never merely because a value
- V2 FG-K0-0b760dcf90 [101, 106] CANONICAL_ONLY/DEFAULT pol=['RUN-007'] rel=[]: Caching is an optimization, not an architecture requirement; introduce it only for a clear measured or reasoned need and choose the implementation by deployment, consistency and staleness requirements, never merely because a value
- V2 FG-K0-24c5c9b14b [99, 106] CANONICAL_ONLY/MUST pol=['ARC-024'] rel=[]: Cache technology stays out of Domain; infrastructure cache APIs never leak into Application without a deliberate boundary abstraction.
- V2 FG-K0-24c5c9b14b [101, 106] CANONICAL_ONLY/MUST pol=['ARC-024'] rel=[]: Cache technology stays out of Domain; infrastructure cache APIs never leak into Application without a deliberate boundary abstraction.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0143 -> FG-K0-0b760dcf90 [CANONICAL_ONLY] Caching is an optimization, not an architecture requirement; introduce it only for a clear measured or reasoned need and choose the implementation by deployment, consistency and st
- NAMED primary/K0/constraints.jsonl/RULE-K0-0299 -> FG-K0-3aa34979c8 [CANONICAL_ONLY] Infrastructure may implement the cache abstraction with HybridCache, which stays out of Application contracts.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0049 -> FG-K0-0b760dcf90 [CANONICAL_ONLY] Caching is an optimization, not an architecture requirement; introduce it only for a clear measured or reasoned need and choose the implementation by deployment, consistency and st
- NAMED replica/K0/constraints.jsonl/RULE-K0-0048 -> FG-K0-debf9372df [CANONICAL_ONLY] Distributed caching is Reserved.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0062 -> FG-K0-f5cd026e7f [CANONICAL_PLUS_DELTA] Measure before adding caching purely for performance.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0063 -> FG-K0-1e498959c9 [NON_NORMATIVE] The output-cache example embeds a five-minute TTL without a local illustrative-value caveat (reported copy risk).

## CIS-K1-U0017 (pass 3) K1 .claude/skills/caching/SKILL.md:84-84  [DEFAULT UNCERTAIN_NOVELTY]
CLAIM: For a local application cache, the decision guide gives in-memory caching or HybridCache as the default consideration.
TRIGGER: Using the caching skill for a justified local application cache | EXC: Default consideration, not required installation or exhaustive technology list; HybridCache explicitly not mandatory at line23. | POL: []
CODEX WHY: A need-to-choice default may add to general cache-placement policies, but optional strong-option text may already convey the same advice. Preserved as uncertain, not verified novelty.
```
  81  | Need | Default consideration |
  82  |---|---|
  83  | Entire reusable HTTP response | Output caching |
  84> | Local application cache | In-memory or HybridCache |
  85  | Multi-instance shared cache | Distributed cache / HybridCache L2 (Reserved decision) |
  86  | Expensive repeated remote read | Cache in Infrastructure when the contract permits |
  87  | Application-controlled invalidation | Application abstraction + Infrastructure implementation |
```
v3 bytes: file changed in v1/v2=True, cited text still present=True
- V2 FG-K1-2cbf448166 [83, 88] CANONICAL_ONLY/MUST pol=['ARC-024'] rel=[]: Cache technology stays out of Domain; infrastructure cache APIs do not leak into Application without a deliberate boundary abstraction.
- V2 FG-K1-2cbf448166 [81, 88] CANONICAL_ONLY/MUST pol=['ARC-024'] rel=[]: Cache technology stays out of Domain; infrastructure cache APIs do not leak into Application without a deliberate boundary abstraction.
- V2 FG-K1-1a623ecdbc [83, 88] CANONICAL_ONLY/DEFAULT pol=['RUN-007'] rel=[]: No caching without a clear measured or reasoned need; choose the implementation by deployment, consistency and staleness requirements.
- V2 FG-K1-1a623ecdbc [81, 88] CANONICAL_ONLY/DEFAULT pol=['RUN-007'] rel=[]: No caching without a clear measured or reasoned need; choose the implementation by deployment, consistency and staleness requirements.
- V2 FG-K1-750f5a1748 [81, 88] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020', 'RUN-007'] rel=[]: Adding a distributed cache (multi-instance shared cache, HybridCache L2, Redis) is a Reserved infrastructure decision, added only when deployment requirements justify it.
- V2 FG-K1-29997bfd9c [83, 88] CANONICAL_ONLY/REQUIRES_APPROVAL pol=['ARC-020'] rel=[]: Adding messaging, background-processing or distributed-cache infrastructure is Reserved.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0307 -> FG-K1-f485f3c2e3 [CANONICAL_ONLY] HybridCache is a strong but not mandatory option; add a distributed backend such as Redis only when deployment requirements justify it.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0308 -> FG-K1-64e9c9e171 [CANONICAL_ONLY] When Application coordinates invalidation expose a narrow contract and keep HybridCache itself out of Application contracts.
- NAMED replica/K1/constraints.jsonl/RULE-K1-0089 -> FG-K1-1a623ecdbc [CANONICAL_ONLY] No caching without a clear measured or reasoned need; choose the implementation by deployment, consistency and staleness requirements.
- NAMED replica/K1/constraints.jsonl/RULE-K1-0201 -> FG-K1-750f5a1748 [CANONICAL_ONLY] Adding a distributed cache (multi-instance shared cache, HybridCache L2, Redis) is a Reserved infrastructure decision, added only when deployment requirements justify it.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0116 -> FG-K1-9acca8ff5f [CANONICAL_ONLY] Output caching belongs to the Api layer; cache abstractions are avoided when internal Infrastructure caching suffices.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0117 -> FG-K1-a2b893ac20 [CANONICAL_ONLY] Invalidating before the mutation is not ruled out when correctness for the chosen semantics is shown; no single order is correct by itself.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0118 -> FG-K1-81e53820f4 [EXTRA_PRODUCT] Test caching when it affects observable correctness (invalidation after mutation, key isolation, miss fallback, outage policy); do not unit-test framework cache internals.
