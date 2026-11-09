# DI-DECISION-GUIDE (18 records)

## CIS-M-U0043 (pass 3) M .claude/skills/dependency-injection/SKILL.md:155-160  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The shown Scrutor decorator-registration example applies when Scrutor is already used by the project.
TRIGGER: considering the shown services.Decorate example | EXC: Knowledge-skill technique, not mandatory installation or global ban on adopting Scrutor. Source conditions retained. General dependency approval and simplicity rules still apply. | POL: []
CODEX WHY: A distinct condition or named technique is present in rejected material. Preserve uncertain until recommendation strength and general-policy subsumption can be adjudicated.
```
 152  }
 153  ```
 154  
 155> If Scrutor is already used by the project:
 156> 
 157> ```csharp
 158> services.AddScoped<IOrderService, OrderService>();
 159> services.Decorate<IOrderService, LoggingOrderService>();
 160> ```
 161  
 162  Do not add Scrutor solely for one decoration when normal composition is simpler
 163  (adding it goes through `add-dependency`).
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/M/constraints.jsonl/RULE-M-0373 -> FG-M-82d9796c78 [CANONICAL_ONLY] Prefer explicit registration in small/medium apps; add convention scanning, keyed services, factories or decorators only when they solve an actual composition problem.
- NAMED primary/M/constraints.jsonl/RULE-M-0375 -> FG-M-d38d0c411e [CANONICAL_ONLY] Do not add Scrutor solely for one decoration when normal composition is simpler (adding it goes through add-dependency).
- NAMED primary/M/constraints.jsonl/EXTRA-M-0103 -> FG-M-01a562919a [EXTRA_PRODUCT] Use keyed services only when implementations are selected by a known key; decorators when the same cross-cutting behaviour wraps an abstraction; assembly scanning only for genuinel
- NAMED replica/M/constraints.jsonl/RULE-M-0057 -> FG-M-d0a19395e1 [CANONICAL_ONLY] Respect lifetimes; never capture a shorter-lived (e.g. scoped) dependency in a longer-lived service.
- NAMED replica/M/constraints.jsonl/RULE-M-0069 -> FG-M-2edfa95f6c [CANONICAL_ONLY] Add a dependency only for a concrete current requirement; no packages for hypothetical future use; 'approved' does not mean 'install by default'.
- NAMED replica/M/constraints.jsonl/RULE-M-0148 -> FG-M-f45c5ed5b1 [CANONICAL_ONLY] Prefer simple, maintainable solutions and avoid speculative abstractions (e.g. no custom abstraction around every UI-library component without a concrete reason).
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0062 -> FG-M-82d9796c78 [CANONICAL_ONLY] Prefer explicit registration in small/medium apps; add convention scanning, keyed services, factories or decorators only when they solve an actual composition problem.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0063 -> FG-M-372dc668d6 [CANONICAL_PLUS_DELTA] When a singleton/hosted service genuinely needs scoped work create a scope per operation and resolve a scoped orchestration service, not Infrastructure internals.

## CIS-M-U0010 (pass 2) M .claude/skills/dependency-injection/SKILL.md:257-257  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For an Application service using repositories or Unit of Work, the decision guide recommends scoped registration.
TRIGGER: Selecting the registration lifetime of an Application service with repository/UoW dependencies. | EXC: Parent explicitly owns technique and examples, no policy. The recommendation may be nonexclusive explanatory guidance; no unconditional API or lifetime mandate is established. | POL: ['ARC-022']
CODEX WHY: The table recommendation can affect an implementation choice independently of the broad rule. Its no-policy ownership and plausible explanatory reading prevent a verified novelty judgment.
```
 254  
 255  | Scenario | Recommendation |
 256  |----------|---------------|
 257> | Application service using repositories/UoW | Scoped |
 258  | Pure stateless helper with no scoped dependency | Transient or concrete registration |
 259  | Immutable/shared configuration | Singleton-compatible |
 260  | DbContext | Scoped (registered by `AddDbContext`) |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-d0a19395e1 [255, 265] CANONICAL_ONLY/MUST pol=['ARC-022'] rel=[]: Respect lifetimes; never capture a shorter-lived (e.g. scoped) dependency in a longer-lived service.
- V2 FG-M-bcc7afd10a [255, 265] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured service configuration, validate settings at startup when missing or invalid values prevent correct or secure operation, and avoid scattering string-based IConfiguration lookups through 
- V2 FG-M-f45c5ed5b1 [255, 265] CANONICAL_ONLY/DEFAULT pol=['GOV-012'] rel=[]: Prefer simple, maintainable solutions and avoid speculative abstractions (e.g. no custom abstraction around every UI-library component without a concrete reason).
- NAMED primary/M/constraints.jsonl/RULE-M-0052 -> FG-M-d0a19395e1 [CANONICAL_ONLY] Respect lifetimes; never capture a shorter-lived (e.g. scoped) dependency in a longer-lived service.
- NAMED primary/M/constraints.jsonl/RULE-M-0054 -> FG-M-24958494e5 [CANONICAL_PLUS_DELTA] Prefer strongly typed options, validate at startup when missing/invalid values prevent correct/secure operation, avoid scattered string IConfiguration lookups (direct IConfiguratio
- NAMED replica/M/constraints.jsonl/RULE-M-0057 -> FG-M-d0a19395e1 [CANONICAL_ONLY] Respect lifetimes; never capture a shorter-lived (e.g. scoped) dependency in a longer-lived service.
- NAMED replica/M/constraints.jsonl/RULE-M-0059 -> FG-M-bcc7afd10a [CANONICAL_ONLY] Prefer strongly typed options for structured service configuration, validate settings at startup when missing or invalid values prevent correct or secure operation, and avoid scatt
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0061 -> FG-M-f5162347fe [CANONICAL_PLUS_DELTA] Direct IConfiguration access belongs to the composition root, provider setup and infrastructure registration; ordinary application services receive typed options.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0062 -> FG-M-82d9796c78 [CANONICAL_ONLY] Prefer explicit registration in small/medium apps; add convention scanning, keyed services, factories or decorators only when they solve an actual composition problem.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0063 -> FG-M-372dc668d6 [CANONICAL_PLUS_DELTA] When a singleton/hosted service genuinely needs scoped work create a scope per operation and resolve a scoped orchestration service, not Infrastructure internals.

## CIS-M-U0011 (pass 2) M .claude/skills/dependency-injection/SKILL.md:258-258  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For a pure stateless helper without scoped dependencies, the decision guide recommends transient or concrete registration.
TRIGGER: Selecting registration for a pure stateless helper with no scoped dependency. | EXC: Parent explicitly owns technique and examples, no policy. The recommendation may be nonexclusive explanatory guidance; no unconditional API or lifetime mandate is established. | POL: ['ARC-022']
CODEX WHY: The table recommendation can affect an implementation choice independently of the broad rule. Its no-policy ownership and plausible explanatory reading prevent a verified novelty judgment.
```
 255  | Scenario | Recommendation |
 256  |----------|---------------|
 257  | Application service using repositories/UoW | Scoped |
 258> | Pure stateless helper with no scoped dependency | Transient or concrete registration |
 259  | Immutable/shared configuration | Singleton-compatible |
 260  | DbContext | Scoped (registered by `AddDbContext`) |
 261  | Multiple implementations selected by key | Keyed services |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-d0a19395e1 [255, 265] CANONICAL_ONLY/MUST pol=['ARC-022'] rel=[]: Respect lifetimes; never capture a shorter-lived (e.g. scoped) dependency in a longer-lived service.
- V2 FG-M-bcc7afd10a [255, 265] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured service configuration, validate settings at startup when missing or invalid values prevent correct or secure operation, and avoid scattering string-based IConfiguration lookups through 
- V2 FG-M-f45c5ed5b1 [255, 265] CANONICAL_ONLY/DEFAULT pol=['GOV-012'] rel=[]: Prefer simple, maintainable solutions and avoid speculative abstractions (e.g. no custom abstraction around every UI-library component without a concrete reason).
- NAMED primary/M/constraints.jsonl/RULE-M-0052 -> FG-M-d0a19395e1 [CANONICAL_ONLY] Respect lifetimes; never capture a shorter-lived (e.g. scoped) dependency in a longer-lived service.
- NAMED primary/M/constraints.jsonl/RULE-M-0054 -> FG-M-24958494e5 [CANONICAL_PLUS_DELTA] Prefer strongly typed options, validate at startup when missing/invalid values prevent correct/secure operation, avoid scattered string IConfiguration lookups (direct IConfiguratio
- NAMED replica/M/constraints.jsonl/RULE-M-0057 -> FG-M-d0a19395e1 [CANONICAL_ONLY] Respect lifetimes; never capture a shorter-lived (e.g. scoped) dependency in a longer-lived service.
- NAMED replica/M/constraints.jsonl/RULE-M-0059 -> FG-M-bcc7afd10a [CANONICAL_ONLY] Prefer strongly typed options for structured service configuration, validate settings at startup when missing or invalid values prevent correct or secure operation, and avoid scatt
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0061 -> FG-M-f5162347fe [CANONICAL_PLUS_DELTA] Direct IConfiguration access belongs to the composition root, provider setup and infrastructure registration; ordinary application services receive typed options.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0062 -> FG-M-82d9796c78 [CANONICAL_ONLY] Prefer explicit registration in small/medium apps; add convention scanning, keyed services, factories or decorators only when they solve an actual composition problem.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0063 -> FG-M-372dc668d6 [CANONICAL_PLUS_DELTA] When a singleton/hosted service genuinely needs scoped work create a scope per operation and resolve a scoped orchestration service, not Infrastructure internals.

## CIS-M-U0045 (pass 3) M .claude/skills/dependency-injection/SKILL.md:263-263  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For convention-based registration, the DI decision guide recommends Scrutor when already justified.
TRIGGER: choosing an implementation for already-justified convention registration | EXC: Knowledge-skill technique, not mandatory installation or global ban on adopting Scrutor. Source conditions retained. General dependency approval and simplicity rules still apply. | POL: []
CODEX WHY: A distinct condition or named technique is present in rejected material. Preserve uncertain until recommendation strength and general-policy subsumption can be adjudicated.
```
 260  | DbContext | Scoped (registered by `AddDbContext`) |
 261  | Multiple implementations selected by key | Keyed services |
 262  | Cross-cutting behavior | Decorator |
 263> | Convention-based registration | Scrutor, when already justified |
 264  | Runtime implementation selection | Factory delegate |
 265  | Strongly typed config | `AddOptions<T>().BindConfiguration()` |
 266  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-d0a19395e1 [255, 265] CANONICAL_ONLY/MUST pol=['ARC-022'] rel=[]: Respect lifetimes; never capture a shorter-lived (e.g. scoped) dependency in a longer-lived service.
- V2 FG-M-bcc7afd10a [255, 265] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured service configuration, validate settings at startup when missing or invalid values prevent correct or secure operation, and avoid scattering string-based IConfiguration lookups through 
- V2 FG-M-f45c5ed5b1 [255, 265] CANONICAL_ONLY/DEFAULT pol=['GOV-012'] rel=[]: Prefer simple, maintainable solutions and avoid speculative abstractions (e.g. no custom abstraction around every UI-library component without a concrete reason).
- NAMED primary/M/constraints.jsonl/RULE-M-0373 -> FG-M-82d9796c78 [CANONICAL_ONLY] Prefer explicit registration in small/medium apps; add convention scanning, keyed services, factories or decorators only when they solve an actual composition problem.
- NAMED primary/M/constraints.jsonl/RULE-M-0375 -> FG-M-d38d0c411e [CANONICAL_ONLY] Do not add Scrutor solely for one decoration when normal composition is simpler (adding it goes through add-dependency).
- NAMED primary/M/constraints.jsonl/EXTRA-M-0103 -> FG-M-01a562919a [EXTRA_PRODUCT] Use keyed services only when implementations are selected by a known key; decorators when the same cross-cutting behaviour wraps an abstraction; assembly scanning only for genuinel
- NAMED replica/M/constraints.jsonl/RULE-M-0057 -> FG-M-d0a19395e1 [CANONICAL_ONLY] Respect lifetimes; never capture a shorter-lived (e.g. scoped) dependency in a longer-lived service.
- NAMED replica/M/constraints.jsonl/RULE-M-0069 -> FG-M-2edfa95f6c [CANONICAL_ONLY] Add a dependency only for a concrete current requirement; no packages for hypothetical future use; 'approved' does not mean 'install by default'.
- NAMED replica/M/constraints.jsonl/RULE-M-0148 -> FG-M-f45c5ed5b1 [CANONICAL_ONLY] Prefer simple, maintainable solutions and avoid speculative abstractions (e.g. no custom abstraction around every UI-library component without a concrete reason).
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0062 -> FG-M-82d9796c78 [CANONICAL_ONLY] Prefer explicit registration in small/medium apps; add convention scanning, keyed services, factories or decorators only when they solve an actual composition problem.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0063 -> FG-M-372dc668d6 [CANONICAL_PLUS_DELTA] When a singleton/hosted service genuinely needs scoped work create a scope per operation and resolve a scoped orchestration service, not Infrastructure internals.

## CIS-M-U0044 (pass 3) M .claude/skills/dependency-injection/SKILL.md:264-264  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For runtime implementation selection, the DI decision guide recommends a factory delegate.
TRIGGER: choosing how DI selects an implementation at runtime | EXC: Knowledge-skill technique, not mandatory installation or global ban on adopting Scrutor. Source conditions retained. General dependency approval and simplicity rules still apply. | POL: []
CODEX WHY: A distinct condition or named technique is present in rejected material. Preserve uncertain until recommendation strength and general-policy subsumption can be adjudicated.
```
 261  | Multiple implementations selected by key | Keyed services |
 262  | Cross-cutting behavior | Decorator |
 263  | Convention-based registration | Scrutor, when already justified |
 264> | Runtime implementation selection | Factory delegate |
 265  | Strongly typed config | `AddOptions<T>().BindConfiguration()` |
 266  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-d0a19395e1 [255, 265] CANONICAL_ONLY/MUST pol=['ARC-022'] rel=[]: Respect lifetimes; never capture a shorter-lived (e.g. scoped) dependency in a longer-lived service.
- V2 FG-M-bcc7afd10a [255, 265] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured service configuration, validate settings at startup when missing or invalid values prevent correct or secure operation, and avoid scattering string-based IConfiguration lookups through 
- V2 FG-M-f45c5ed5b1 [255, 265] CANONICAL_ONLY/DEFAULT pol=['GOV-012'] rel=[]: Prefer simple, maintainable solutions and avoid speculative abstractions (e.g. no custom abstraction around every UI-library component without a concrete reason).
- NAMED primary/M/constraints.jsonl/RULE-M-0373 -> FG-M-82d9796c78 [CANONICAL_ONLY] Prefer explicit registration in small/medium apps; add convention scanning, keyed services, factories or decorators only when they solve an actual composition problem.
- NAMED primary/M/constraints.jsonl/RULE-M-0375 -> FG-M-d38d0c411e [CANONICAL_ONLY] Do not add Scrutor solely for one decoration when normal composition is simpler (adding it goes through add-dependency).
- NAMED primary/M/constraints.jsonl/EXTRA-M-0103 -> FG-M-01a562919a [EXTRA_PRODUCT] Use keyed services only when implementations are selected by a known key; decorators when the same cross-cutting behaviour wraps an abstraction; assembly scanning only for genuinel
- NAMED replica/M/constraints.jsonl/RULE-M-0057 -> FG-M-d0a19395e1 [CANONICAL_ONLY] Respect lifetimes; never capture a shorter-lived (e.g. scoped) dependency in a longer-lived service.
- NAMED replica/M/constraints.jsonl/RULE-M-0069 -> FG-M-2edfa95f6c [CANONICAL_ONLY] Add a dependency only for a concrete current requirement; no packages for hypothetical future use; 'approved' does not mean 'install by default'.
- NAMED replica/M/constraints.jsonl/RULE-M-0148 -> FG-M-f45c5ed5b1 [CANONICAL_ONLY] Prefer simple, maintainable solutions and avoid speculative abstractions (e.g. no custom abstraction around every UI-library component without a concrete reason).
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0062 -> FG-M-82d9796c78 [CANONICAL_ONLY] Prefer explicit registration in small/medium apps; add convention scanning, keyed services, factories or decorators only when they solve an actual composition problem.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0063 -> FG-M-372dc668d6 [CANONICAL_PLUS_DELTA] When a singleton/hosted service genuinely needs scoped work create a scope per operation and resolve a scoped orchestration service, not Infrastructure internals.

## CIS-M1-U0033 (pass 3) M1 .claude/skills/dependency-injection/SKILL.md:146-151  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The shown Scrutor decorator-registration example applies when Scrutor is already used by the project.
TRIGGER: considering the shown services.Decorate example | EXC: Nonexclusive knowledge-skill guidance; no mandatory package adoption or global ban inferred. Actual need, simplicity, approval and lifetime rules still apply. | POL: []
CODEX WHY: Separately falsifiable choice is present in rejected material, but technique-only and broad-subsumption readings remain plausible.
```
 143  }
 144  ```
 145  
 146> If Scrutor is already used by the project:
 147> 
 148> ```csharp
 149> services.AddScoped<IOrderService, OrderService>();
 150> services.Decorate<IOrderService, LoggingOrderService>();
 151> ```
 152  
 153  Do not add Scrutor solely for one decoration when normal composition is
 154  simpler.
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/M1/constraints.jsonl/RULE-M1-0153 -> FG-M1-2627bd9f2f [CANONICAL_PLUS_DELTA] Never capture a shorter-lived dependency in a longer-lived service; singletons/hosted services needing scoped work create a scope per operation and resolve a scoped orchestration s
- NAMED primary/M1/constraints.jsonl/RULE-M1-0417 -> FG-M1-89b535e162 [CANONICAL_ONLY] Prefer explicit registration in small/medium applications; add scanning, keyed services, factories or decorators only for actual composition problems.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0419 -> FG-M1-f62eb69189 [CANONICAL_ONLY] Do not add Scrutor solely for one decoration when normal composition is simpler.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0125 -> FG-M1-f36e94b1d8 [EXTRA_PRODUCT] Application services, repositories and external adapters use interface-to-implementation registration at boundaries; concrete registration for implementation-only helpers.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0126 -> FG-M1-78a9554489 [EXTRA_PRODUCT] Keyed services only for key-selected implementations; decorators for cross-cutting wrapping; assembly scanning only for genuinely repetitive registration and over the owning assemb
- NAMED replica/M1/constraints.jsonl/RULE-M1-0055 -> FG-M1-2627bd9f2f [CANONICAL_PLUS_DELTA] Never capture a shorter-lived dependency in a longer-lived service; singletons/hosted services needing scoped work create a scope per operation and resolve a scoped orchestration s
- NAMED replica/M1/constraints.jsonl/RULE-M1-0059 -> FG-M1-eaa632c4fe [CANONICAL_ONLY] Add a dependency only for a concrete current requirement; no hypothetical future use.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0148 -> FG-M1-a4ef0faadf [CANONICAL_ONLY] Prefer simple, maintainable solutions and avoid speculative abstractions (e.g. no custom abstraction around every UI-library component without a concrete reason).
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0027 -> FG-M1-60d5a43efd [CANONICAL_PLUS_DELTA] A singleton or hosted service that needs scoped work creates a scope per operation and resolves a scoped orchestration service.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0089 -> FG-M1-f36e94b1d8 [EXTRA_PRODUCT] Application services, repositories and external adapters use interface-to-implementation registration at boundaries; concrete registration for implementation-only helpers.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0090 -> FG-M1-89b535e162 [CANONICAL_ONLY] Prefer explicit registration in small/medium applications; add scanning, keyed services, factories or decorators only for actual composition problems.

## CIS-M1-U0031 (pass 3) M1 .claude/skills/dependency-injection/SKILL.md:253-253  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For an Application service using repositories or Unit of Work, prefer scoped registration.
TRIGGER: selecting the lifetime of an Application service using repositories/UoW | EXC: Nonexclusive knowledge-skill guidance; no mandatory package adoption or global ban inferred. Actual need, simplicity, approval and lifetime rules still apply. | POL: ['ARC-022']
CODEX WHY: Separately falsifiable choice is present in rejected material, but technique-only and broad-subsumption readings remain plausible.
```
 250  
 251  | Scenario | Recommendation |
 252  |---|---|
 253> | Application service using repositories/UoW | Scoped |
 254  | Pure stateless helper with no scoped dependency | Transient or concrete registration |
 255  | Immutable/shared configuration | Singleton-compatible |
 256  | Persistence session | Scoped (registered by the persistence technology) |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-2627bd9f2f [251, 261] CANONICAL_PLUS_DELTA/MUST pol=['ARC-022'] rel=[]: Never capture a shorter-lived dependency in a longer-lived service; singletons/hosted services needing scoped work create a scope per operation and resolve a scoped orchestration service.
- V2 FG-M1-9de8829dcf [251, 261] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured configuration consumed by services; direct IConfiguration access is appropriate in the composition root, provider setup and infrastructure registration.
- V2 FG-M1-4bed05f607 [251, 261] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Validate settings at startup when missing/invalid values prevent correct or secure operation.
- V2 FG-M1-a4ef0faadf [251, 261] CANONICAL_ONLY/DEFAULT pol=['GOV-012'] rel=[]: Prefer simple, maintainable solutions and avoid speculative abstractions (e.g. no custom abstraction around every UI-library component without a concrete reason).
- NAMED primary/M1/constraints.jsonl/RULE-M1-0153 -> FG-M1-2627bd9f2f [CANONICAL_PLUS_DELTA] Never capture a shorter-lived dependency in a longer-lived service; singletons/hosted services needing scoped work create a scope per operation and resolve a scoped orchestration s
- NAMED primary/M1/constraints.jsonl/RULE-M1-0417 -> FG-M1-89b535e162 [CANONICAL_ONLY] Prefer explicit registration in small/medium applications; add scanning, keyed services, factories or decorators only for actual composition problems.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0419 -> FG-M1-f62eb69189 [CANONICAL_ONLY] Do not add Scrutor solely for one decoration when normal composition is simpler.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0125 -> FG-M1-f36e94b1d8 [EXTRA_PRODUCT] Application services, repositories and external adapters use interface-to-implementation registration at boundaries; concrete registration for implementation-only helpers.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0126 -> FG-M1-78a9554489 [EXTRA_PRODUCT] Keyed services only for key-selected implementations; decorators for cross-cutting wrapping; assembly scanning only for genuinely repetitive registration and over the owning assemb
- NAMED replica/M1/constraints.jsonl/RULE-M1-0055 -> FG-M1-2627bd9f2f [CANONICAL_PLUS_DELTA] Never capture a shorter-lived dependency in a longer-lived service; singletons/hosted services needing scoped work create a scope per operation and resolve a scoped orchestration s
- NAMED replica/M1/constraints.jsonl/RULE-M1-0059 -> FG-M1-eaa632c4fe [CANONICAL_ONLY] Add a dependency only for a concrete current requirement; no hypothetical future use.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0148 -> FG-M1-a4ef0faadf [CANONICAL_ONLY] Prefer simple, maintainable solutions and avoid speculative abstractions (e.g. no custom abstraction around every UI-library component without a concrete reason).
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0027 -> FG-M1-60d5a43efd [CANONICAL_PLUS_DELTA] A singleton or hosted service that needs scoped work creates a scope per operation and resolves a scoped orchestration service.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0089 -> FG-M1-f36e94b1d8 [EXTRA_PRODUCT] Application services, repositories and external adapters use interface-to-implementation registration at boundaries; concrete registration for implementation-only helpers.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0090 -> FG-M1-89b535e162 [CANONICAL_ONLY] Prefer explicit registration in small/medium applications; add scanning, keyed services, factories or decorators only for actual composition problems.

## CIS-M1-U0032 (pass 3) M1 .claude/skills/dependency-injection/SKILL.md:254-254  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For a pure stateless helper with no scoped dependency, prefer transient or concrete registration.
TRIGGER: selecting registration for a pure stateless helper with no scoped dependency | EXC: Nonexclusive knowledge-skill guidance; no mandatory package adoption or global ban inferred. Actual need, simplicity, approval and lifetime rules still apply. | POL: ['ARC-022']
CODEX WHY: Separately falsifiable choice is present in rejected material, but technique-only and broad-subsumption readings remain plausible.
```
 251  | Scenario | Recommendation |
 252  |---|---|
 253  | Application service using repositories/UoW | Scoped |
 254> | Pure stateless helper with no scoped dependency | Transient or concrete registration |
 255  | Immutable/shared configuration | Singleton-compatible |
 256  | Persistence session | Scoped (registered by the persistence technology) |
 257  | Multiple implementations | Keyed services (strategy pattern) |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-2627bd9f2f [251, 261] CANONICAL_PLUS_DELTA/MUST pol=['ARC-022'] rel=[]: Never capture a shorter-lived dependency in a longer-lived service; singletons/hosted services needing scoped work create a scope per operation and resolve a scoped orchestration service.
- V2 FG-M1-9de8829dcf [251, 261] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured configuration consumed by services; direct IConfiguration access is appropriate in the composition root, provider setup and infrastructure registration.
- V2 FG-M1-4bed05f607 [251, 261] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Validate settings at startup when missing/invalid values prevent correct or secure operation.
- V2 FG-M1-a4ef0faadf [251, 261] CANONICAL_ONLY/DEFAULT pol=['GOV-012'] rel=[]: Prefer simple, maintainable solutions and avoid speculative abstractions (e.g. no custom abstraction around every UI-library component without a concrete reason).
- NAMED primary/M1/constraints.jsonl/RULE-M1-0153 -> FG-M1-2627bd9f2f [CANONICAL_PLUS_DELTA] Never capture a shorter-lived dependency in a longer-lived service; singletons/hosted services needing scoped work create a scope per operation and resolve a scoped orchestration s
- NAMED primary/M1/constraints.jsonl/RULE-M1-0417 -> FG-M1-89b535e162 [CANONICAL_ONLY] Prefer explicit registration in small/medium applications; add scanning, keyed services, factories or decorators only for actual composition problems.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0419 -> FG-M1-f62eb69189 [CANONICAL_ONLY] Do not add Scrutor solely for one decoration when normal composition is simpler.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0125 -> FG-M1-f36e94b1d8 [EXTRA_PRODUCT] Application services, repositories and external adapters use interface-to-implementation registration at boundaries; concrete registration for implementation-only helpers.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0126 -> FG-M1-78a9554489 [EXTRA_PRODUCT] Keyed services only for key-selected implementations; decorators for cross-cutting wrapping; assembly scanning only for genuinely repetitive registration and over the owning assemb
- NAMED replica/M1/constraints.jsonl/RULE-M1-0055 -> FG-M1-2627bd9f2f [CANONICAL_PLUS_DELTA] Never capture a shorter-lived dependency in a longer-lived service; singletons/hosted services needing scoped work create a scope per operation and resolve a scoped orchestration s
- NAMED replica/M1/constraints.jsonl/RULE-M1-0059 -> FG-M1-eaa632c4fe [CANONICAL_ONLY] Add a dependency only for a concrete current requirement; no hypothetical future use.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0148 -> FG-M1-a4ef0faadf [CANONICAL_ONLY] Prefer simple, maintainable solutions and avoid speculative abstractions (e.g. no custom abstraction around every UI-library component without a concrete reason).
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0027 -> FG-M1-60d5a43efd [CANONICAL_PLUS_DELTA] A singleton or hosted service that needs scoped work creates a scope per operation and resolves a scoped orchestration service.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0089 -> FG-M1-f36e94b1d8 [EXTRA_PRODUCT] Application services, repositories and external adapters use interface-to-implementation registration at boundaries; concrete registration for implementation-only helpers.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0090 -> FG-M1-89b535e162 [CANONICAL_ONLY] Prefer explicit registration in small/medium applications; add scanning, keyed services, factories or decorators only for actual composition problems.

## CIS-M1-U0034 (pass 3) M1 .claude/skills/dependency-injection/SKILL.md:259-259  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For justified convention-based registration, prefer Scrutor.
TRIGGER: choosing a mechanism for convention registration justified by repetitive boilerplate | EXC: Nonexclusive knowledge-skill guidance; no mandatory package adoption or global ban inferred. Actual need, simplicity, approval and lifetime rules still apply. | POL: []
CODEX WHY: Separately falsifiable choice is present in rejected material, but technique-only and broad-subsumption readings remain plausible.
```
 256  | Persistence session | Scoped (registered by the persistence technology) |
 257  | Multiple implementations | Keyed services (strategy pattern) |
 258  | Cross-cutting behavior | Decorator pattern |
 259> | Convention-based registration | Scrutor |
 260  | Runtime implementation selection | Factory delegate |
 261  | Strongly typed config | `AddOptions<T>().BindConfiguration()` |
 262  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-2627bd9f2f [251, 261] CANONICAL_PLUS_DELTA/MUST pol=['ARC-022'] rel=[]: Never capture a shorter-lived dependency in a longer-lived service; singletons/hosted services needing scoped work create a scope per operation and resolve a scoped orchestration service.
- V2 FG-M1-9de8829dcf [251, 261] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured configuration consumed by services; direct IConfiguration access is appropriate in the composition root, provider setup and infrastructure registration.
- V2 FG-M1-4bed05f607 [251, 261] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Validate settings at startup when missing/invalid values prevent correct or secure operation.
- V2 FG-M1-a4ef0faadf [251, 261] CANONICAL_ONLY/DEFAULT pol=['GOV-012'] rel=[]: Prefer simple, maintainable solutions and avoid speculative abstractions (e.g. no custom abstraction around every UI-library component without a concrete reason).
- NAMED primary/M1/constraints.jsonl/RULE-M1-0153 -> FG-M1-2627bd9f2f [CANONICAL_PLUS_DELTA] Never capture a shorter-lived dependency in a longer-lived service; singletons/hosted services needing scoped work create a scope per operation and resolve a scoped orchestration s
- NAMED primary/M1/constraints.jsonl/RULE-M1-0417 -> FG-M1-89b535e162 [CANONICAL_ONLY] Prefer explicit registration in small/medium applications; add scanning, keyed services, factories or decorators only for actual composition problems.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0419 -> FG-M1-f62eb69189 [CANONICAL_ONLY] Do not add Scrutor solely for one decoration when normal composition is simpler.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0125 -> FG-M1-f36e94b1d8 [EXTRA_PRODUCT] Application services, repositories and external adapters use interface-to-implementation registration at boundaries; concrete registration for implementation-only helpers.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0126 -> FG-M1-78a9554489 [EXTRA_PRODUCT] Keyed services only for key-selected implementations; decorators for cross-cutting wrapping; assembly scanning only for genuinely repetitive registration and over the owning assemb
- NAMED replica/M1/constraints.jsonl/RULE-M1-0055 -> FG-M1-2627bd9f2f [CANONICAL_PLUS_DELTA] Never capture a shorter-lived dependency in a longer-lived service; singletons/hosted services needing scoped work create a scope per operation and resolve a scoped orchestration s
- NAMED replica/M1/constraints.jsonl/RULE-M1-0059 -> FG-M1-eaa632c4fe [CANONICAL_ONLY] Add a dependency only for a concrete current requirement; no hypothetical future use.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0148 -> FG-M1-a4ef0faadf [CANONICAL_ONLY] Prefer simple, maintainable solutions and avoid speculative abstractions (e.g. no custom abstraction around every UI-library component without a concrete reason).
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0027 -> FG-M1-60d5a43efd [CANONICAL_PLUS_DELTA] A singleton or hosted service that needs scoped work creates a scope per operation and resolves a scoped orchestration service.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0089 -> FG-M1-f36e94b1d8 [EXTRA_PRODUCT] Application services, repositories and external adapters use interface-to-implementation registration at boundaries; concrete registration for implementation-only helpers.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0090 -> FG-M1-89b535e162 [CANONICAL_ONLY] Prefer explicit registration in small/medium applications; add scanning, keyed services, factories or decorators only for actual composition problems.

## CIS-M1-U0035 (pass 3) M1 .claude/skills/dependency-injection/SKILL.md:260-260  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For runtime implementation selection, prefer a factory delegate.
TRIGGER: choosing how DI selects an implementation at runtime | EXC: Nonexclusive knowledge-skill guidance; no mandatory package adoption or global ban inferred. Actual need, simplicity, approval and lifetime rules still apply. | POL: []
CODEX WHY: Separately falsifiable choice is present in rejected material, but technique-only and broad-subsumption readings remain plausible.
```
 257  | Multiple implementations | Keyed services (strategy pattern) |
 258  | Cross-cutting behavior | Decorator pattern |
 259  | Convention-based registration | Scrutor |
 260> | Runtime implementation selection | Factory delegate |
 261  | Strongly typed config | `AddOptions<T>().BindConfiguration()` |
 262  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-2627bd9f2f [251, 261] CANONICAL_PLUS_DELTA/MUST pol=['ARC-022'] rel=[]: Never capture a shorter-lived dependency in a longer-lived service; singletons/hosted services needing scoped work create a scope per operation and resolve a scoped orchestration service.
- V2 FG-M1-9de8829dcf [251, 261] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured configuration consumed by services; direct IConfiguration access is appropriate in the composition root, provider setup and infrastructure registration.
- V2 FG-M1-4bed05f607 [251, 261] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Validate settings at startup when missing/invalid values prevent correct or secure operation.
- V2 FG-M1-a4ef0faadf [251, 261] CANONICAL_ONLY/DEFAULT pol=['GOV-012'] rel=[]: Prefer simple, maintainable solutions and avoid speculative abstractions (e.g. no custom abstraction around every UI-library component without a concrete reason).
- NAMED primary/M1/constraints.jsonl/RULE-M1-0153 -> FG-M1-2627bd9f2f [CANONICAL_PLUS_DELTA] Never capture a shorter-lived dependency in a longer-lived service; singletons/hosted services needing scoped work create a scope per operation and resolve a scoped orchestration s
- NAMED primary/M1/constraints.jsonl/RULE-M1-0417 -> FG-M1-89b535e162 [CANONICAL_ONLY] Prefer explicit registration in small/medium applications; add scanning, keyed services, factories or decorators only for actual composition problems.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0419 -> FG-M1-f62eb69189 [CANONICAL_ONLY] Do not add Scrutor solely for one decoration when normal composition is simpler.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0125 -> FG-M1-f36e94b1d8 [EXTRA_PRODUCT] Application services, repositories and external adapters use interface-to-implementation registration at boundaries; concrete registration for implementation-only helpers.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0126 -> FG-M1-78a9554489 [EXTRA_PRODUCT] Keyed services only for key-selected implementations; decorators for cross-cutting wrapping; assembly scanning only for genuinely repetitive registration and over the owning assemb
- NAMED replica/M1/constraints.jsonl/RULE-M1-0055 -> FG-M1-2627bd9f2f [CANONICAL_PLUS_DELTA] Never capture a shorter-lived dependency in a longer-lived service; singletons/hosted services needing scoped work create a scope per operation and resolve a scoped orchestration s
- NAMED replica/M1/constraints.jsonl/RULE-M1-0059 -> FG-M1-eaa632c4fe [CANONICAL_ONLY] Add a dependency only for a concrete current requirement; no hypothetical future use.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0148 -> FG-M1-a4ef0faadf [CANONICAL_ONLY] Prefer simple, maintainable solutions and avoid speculative abstractions (e.g. no custom abstraction around every UI-library component without a concrete reason).
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0027 -> FG-M1-60d5a43efd [CANONICAL_PLUS_DELTA] A singleton or hosted service that needs scoped work creates a scope per operation and resolves a scoped orchestration service.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0089 -> FG-M1-f36e94b1d8 [EXTRA_PRODUCT] Application services, repositories and external adapters use interface-to-implementation registration at boundaries; concrete registration for implementation-only helpers.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0090 -> FG-M1-89b535e162 [CANONICAL_ONLY] Prefer explicit registration in small/medium applications; add scanning, keyed services, factories or decorators only for actual composition problems.

## CIS-L0-U0038 (pass 3) L0 .claude/skills/dependency-injection/SKILL.md:80-82  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: Use the displayed Scrutor decoration snippet only if Scrutor is already used by the project.
TRIGGER: Consulting or applying the example decoration snippet. | EXC: Technique-only source; not a universal ban on alternative valid lifetimes or future justified dependency adoption. Existing approval and proportionality rules still apply. | POL: []
CODEX WHY: Source and parent qualifications verified; semantic distinction plausible, but optional technique/example scope and subsumption prevent verified novelty.
```
  77      }
  78  }
  79  
  80> // Only if Scrutor is already used by the project:
  81> services.AddScoped<IOrderService, OrderService>();
  82> services.Decorate<IOrderService, LoggingOrderService>();
  83  ```
  84  
  85  Do not add Scrutor for one decoration when normal composition is simpler (`add-dependency`).
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L0/constraints.jsonl/EXTRA-L0-0082 -> FG-L0-5d67d8949f [EXTRA_PRODUCT] Use interface-to-implementation registration at architectural boundaries (Application services, repositories, adapters); concrete registration is fine for implementation-only helpe
- NAMED primary/L0/constraints.jsonl/RULE-L0-0374 -> FG-L0-627c8897f1 [CANONICAL_ONLY] Prefer explicit registration in small/medium applications; add scanning, keyed services, factories or decorators only when they solve an actual composition problem or genuine boile
- NAMED primary/L0/constraints.jsonl/RULE-L0-0375 -> FG-L0-43ad3b79cb [CANONICAL_ONLY] Do not add Scrutor for one decoration when normal composition is simpler.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0082 -> FG-L0-889fd798d1 [CANONICAL_ONLY] Never capture a shorter-lived dependency inside a longer-lived service.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0181 -> FG-L0-7a62ec9e6e [CANONICAL_ONLY] Do not introduce frameworks, libraries, infrastructure or architectural patterns without a concrete current need.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0075 -> FG-L0-5d67d8949f [EXTRA_PRODUCT] Use interface-to-implementation registration at architectural boundaries (Application services, repositories, adapters); concrete registration is fine for implementation-only helpe
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0076 -> FG-L0-5bcbbe1d62 [CANONICAL_PLUS_DELTA] A singleton or hosted service needing scoped work creates a scope per operation and resolves a scoped orchestration service, not Infrastructure internals.

## CIS-L0-U0037 (pass 3) L0 .claude/skills/dependency-injection/SKILL.md:137-137  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For a stateless helper without scoped dependencies, the decision guide recommends transient or concrete registration.
TRIGGER: Selecting registration for a stateless helper without scoped dependencies. | EXC: Technique-only source; not a universal ban on alternative valid lifetimes or future justified dependency adoption. Existing approval and proportionality rules still apply. | POL: []
CODEX WHY: Source and parent qualifications verified; semantic distinction plausible, but optional technique/example scope and subsumption prevent verified novelty.
```
 134  | Scenario | Technique |
 135  |---|---|
 136  | Application service using repositories/UoW | scoped |
 137> | Stateless helper without scoped dependencies | transient or concrete registration |
 138  | Immutable shared configuration | singleton-compatible |
 139  | `DbContext` | scoped (`AddDbContext`) |
 140  | Several implementations selected by key | keyed services |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L0-889fd798d1 [134, 144] CANONICAL_ONLY/MUST_NOT pol=['ARC-022'] rel=[]: Never capture a shorter-lived dependency inside a longer-lived service.
- V2 FG-L0-f4700105ff [134, 144] CANONICAL_ONLY/DEFAULT pol=['GOV-012'] rel=[]: Prefer simple maintainable solutions; complexity proportional to current requirements; avoid speculative abstractions.
- NAMED primary/L0/constraints.jsonl/EXTRA-L0-0082 -> FG-L0-5d67d8949f [EXTRA_PRODUCT] Use interface-to-implementation registration at architectural boundaries (Application services, repositories, adapters); concrete registration is fine for implementation-only helpe
- NAMED primary/L0/constraints.jsonl/RULE-L0-0374 -> FG-L0-627c8897f1 [CANONICAL_ONLY] Prefer explicit registration in small/medium applications; add scanning, keyed services, factories or decorators only when they solve an actual composition problem or genuine boile
- NAMED primary/L0/constraints.jsonl/RULE-L0-0375 -> FG-L0-43ad3b79cb [CANONICAL_ONLY] Do not add Scrutor for one decoration when normal composition is simpler.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0082 -> FG-L0-889fd798d1 [CANONICAL_ONLY] Never capture a shorter-lived dependency inside a longer-lived service.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0181 -> FG-L0-7a62ec9e6e [CANONICAL_ONLY] Do not introduce frameworks, libraries, infrastructure or architectural patterns without a concrete current need.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0075 -> FG-L0-5d67d8949f [EXTRA_PRODUCT] Use interface-to-implementation registration at architectural boundaries (Application services, repositories, adapters); concrete registration is fine for implementation-only helpe
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0076 -> FG-L0-5bcbbe1d62 [CANONICAL_PLUS_DELTA] A singleton or hosted service needing scoped work creates a scope per operation and resolves a scoped orchestration service, not Infrastructure internals.

## CIS-K0-U0034 (pass 3) K0 .claude/skills/dependency-injection/SKILL.md:174-174  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: The DI decision guide directs a stateless helper without scoped dependencies to Transient or concrete registration; potential selection guidance beyond general valid lifetimes and actual composition need.
TRIGGER: Registering services for a stateless helper without scoped dependencies under the DI skill | EXC: Explicit registration preferred for small/medium applications; specialized techniques solve actual composition problems. Table is not expressly exclusive. | POL: ['ARC-022']
CODEX WHY: Concrete helper registration and generic technique necessity already covered; possible additional recommendation remains unresolved rather than verified novelty.
```
 171  | Scenario | Registration |
 172  |---|---|
 173  | Application service using repositories/UoW | Scoped |
 174> | Stateless helper without scoped dependencies | Transient or concrete registration |
 175  | Immutable shared configuration | Singleton-compatible |
 176  | `DbContext` | Scoped (via `AddDbContext`) |
 177  | Several implementations chosen by key | Keyed services |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-3ee80273f7 [173, 181] CANONICAL_ONLY/MUST pol=['ARC-022'] rel=[]: Service lifetimes must be valid; never capture a shorter-lived dependency in a longer-lived service.
- V2 FG-K0-3ee80273f7 [171, 181] CANONICAL_ONLY/MUST pol=['ARC-022'] rel=[]: Service lifetimes must be valid; never capture a shorter-lived dependency in a longer-lived service.
- V2 FG-K0-f81797201d [173, 181] CANONICAL_PLUS_DELTA/DEFAULT pol=['RUN-022'] rel=[]: Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; direct IConfiguration access only in the composition root, provider setup and infrastructure registration.
- V2 FG-K0-6e94029c43 [171, 181] MIXED/MIXED pol=[] rel=[]: Use interface-to-implementation registration at architectural boundaries (concrete registration for implementation-only helpers); prefer explicit registration in small/medium applications; keyed services, factories, decorators, Sc
- V2 FG-K0-6ea7ff7c20 [173, 181] EXTRA_PRODUCT/DEFAULT pol=[] rel=['GOV-012', 'ARC-021']: Keyed services for several implementations of one abstraction selected by a known key, not when a single registration or simple factory is clearer.
- V2 FG-K0-c5bc2f0e7c [173, 181] EXTRA_PRODUCT/DEFAULT pol=[] rel=['GOV-012', 'ARC-023']: Use assembly scanning only when registration volume creates genuine repetitive boilerplate, scanning the assembly that owns the services.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0118 -> FG-K0-b2a42159f2 [MIXED] Interface-to-implementation registration at architectural boundaries, concrete registration for implementation-only helpers; prefer explicit registration in small and medium applic
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0120 -> FG-K0-9e13b040f1 [CANONICAL_ONLY] Scrutor is not added for a single decoration when normal composition is simpler.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0121 -> FG-K0-c5bc2f0e7c [EXTRA_PRODUCT] Use assembly scanning only when registration volume creates genuine repetitive boilerplate, scanning the assembly that owns the services.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0098 -> FG-K0-3ee80273f7 [CANONICAL_ONLY] Service lifetimes must be valid; never capture a shorter-lived dependency in a longer-lived service.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0228 -> FG-K0-6e94029c43 [MIXED] Use interface-to-implementation registration at architectural boundaries (concrete registration for implementation-only helpers); prefer explicit registration in small/medium appli
- NAMED replica/K0/constraints.jsonl/RULE-K0-0046 -> FG-K0-3ee80273f7 [CANONICAL_ONLY] Service lifetimes must be valid; never capture a shorter-lived dependency in a longer-lived service.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0017 -> FG-K0-60a5b8de95 [EXTRA_PRODUCT] Application services, repositories and external adapters use interface-to-implementation registration at architectural boundaries; implementation-only helpers can be registered con
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0018 -> FG-K0-10b20a5501 [CANONICAL_ONLY] An application service depending on scoped repositories or the Unit of Work is scoped; registering it as a singleton captures them.

## CIS-K0-U0035 (pass 3) K0 .claude/skills/dependency-injection/SKILL.md:178-178  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: The DI decision guide directs cross-cutting behavior to Decorator; potential selection guidance beyond general valid lifetimes and actual composition need.
TRIGGER: Registering services for cross-cutting behavior under the DI skill | EXC: Explicit registration preferred for small/medium applications; specialized techniques solve actual composition problems. Table is not expressly exclusive. | POL: []
CODEX WHY: Concrete helper registration and generic technique necessity already covered; possible additional recommendation remains unresolved rather than verified novelty.
```
 175  | Immutable shared configuration | Singleton-compatible |
 176  | `DbContext` | Scoped (via `AddDbContext`) |
 177  | Several implementations chosen by key | Keyed services |
 178> | Cross-cutting behavior | Decorator |
 179  | Convention-based registration | Scrutor |
 180  | Runtime implementation selection | Factory delegate |
 181  | Strongly typed configuration | `AddOptions<T>().BindConfiguration()` (`configuration`) |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-3ee80273f7 [173, 181] CANONICAL_ONLY/MUST pol=['ARC-022'] rel=[]: Service lifetimes must be valid; never capture a shorter-lived dependency in a longer-lived service.
- V2 FG-K0-3ee80273f7 [171, 181] CANONICAL_ONLY/MUST pol=['ARC-022'] rel=[]: Service lifetimes must be valid; never capture a shorter-lived dependency in a longer-lived service.
- V2 FG-K0-f81797201d [173, 181] CANONICAL_PLUS_DELTA/DEFAULT pol=['RUN-022'] rel=[]: Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; direct IConfiguration access only in the composition root, provider setup and infrastructure registration.
- V2 FG-K0-6e94029c43 [171, 181] MIXED/MIXED pol=[] rel=[]: Use interface-to-implementation registration at architectural boundaries (concrete registration for implementation-only helpers); prefer explicit registration in small/medium applications; keyed services, factories, decorators, Sc
- V2 FG-K0-6ea7ff7c20 [173, 181] EXTRA_PRODUCT/DEFAULT pol=[] rel=['GOV-012', 'ARC-021']: Keyed services for several implementations of one abstraction selected by a known key, not when a single registration or simple factory is clearer.
- V2 FG-K0-c5bc2f0e7c [173, 181] EXTRA_PRODUCT/DEFAULT pol=[] rel=['GOV-012', 'ARC-023']: Use assembly scanning only when registration volume creates genuine repetitive boilerplate, scanning the assembly that owns the services.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0118 -> FG-K0-b2a42159f2 [MIXED] Interface-to-implementation registration at architectural boundaries, concrete registration for implementation-only helpers; prefer explicit registration in small and medium applic
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0120 -> FG-K0-9e13b040f1 [CANONICAL_ONLY] Scrutor is not added for a single decoration when normal composition is simpler.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0121 -> FG-K0-c5bc2f0e7c [EXTRA_PRODUCT] Use assembly scanning only when registration volume creates genuine repetitive boilerplate, scanning the assembly that owns the services.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0098 -> FG-K0-3ee80273f7 [CANONICAL_ONLY] Service lifetimes must be valid; never capture a shorter-lived dependency in a longer-lived service.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0228 -> FG-K0-6e94029c43 [MIXED] Use interface-to-implementation registration at architectural boundaries (concrete registration for implementation-only helpers); prefer explicit registration in small/medium appli
- NAMED replica/K0/constraints.jsonl/RULE-K0-0046 -> FG-K0-3ee80273f7 [CANONICAL_ONLY] Service lifetimes must be valid; never capture a shorter-lived dependency in a longer-lived service.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0017 -> FG-K0-60a5b8de95 [EXTRA_PRODUCT] Application services, repositories and external adapters use interface-to-implementation registration at architectural boundaries; implementation-only helpers can be registered con
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0018 -> FG-K0-10b20a5501 [CANONICAL_ONLY] An application service depending on scoped repositories or the Unit of Work is scoped; registering it as a singleton captures them.

## CIS-K0-U0036 (pass 3) K0 .claude/skills/dependency-injection/SKILL.md:179-179  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: The DI decision guide directs convention-based registration to Scrutor; potential selection guidance beyond general valid lifetimes and actual composition need.
TRIGGER: Registering services for convention-based registration under the DI skill | EXC: Explicit registration preferred for small/medium applications; specialized techniques solve actual composition problems. Table is not expressly exclusive. | POL: []
CODEX WHY: Concrete helper registration and generic technique necessity already covered; possible additional recommendation remains unresolved rather than verified novelty.
```
 176  | `DbContext` | Scoped (via `AddDbContext`) |
 177  | Several implementations chosen by key | Keyed services |
 178  | Cross-cutting behavior | Decorator |
 179> | Convention-based registration | Scrutor |
 180  | Runtime implementation selection | Factory delegate |
 181  | Strongly typed configuration | `AddOptions<T>().BindConfiguration()` (`configuration`) |
 182  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-3ee80273f7 [173, 181] CANONICAL_ONLY/MUST pol=['ARC-022'] rel=[]: Service lifetimes must be valid; never capture a shorter-lived dependency in a longer-lived service.
- V2 FG-K0-3ee80273f7 [171, 181] CANONICAL_ONLY/MUST pol=['ARC-022'] rel=[]: Service lifetimes must be valid; never capture a shorter-lived dependency in a longer-lived service.
- V2 FG-K0-f81797201d [173, 181] CANONICAL_PLUS_DELTA/DEFAULT pol=['RUN-022'] rel=[]: Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; direct IConfiguration access only in the composition root, provider setup and infrastructure registration.
- V2 FG-K0-6e94029c43 [171, 181] MIXED/MIXED pol=[] rel=[]: Use interface-to-implementation registration at architectural boundaries (concrete registration for implementation-only helpers); prefer explicit registration in small/medium applications; keyed services, factories, decorators, Sc
- V2 FG-K0-6ea7ff7c20 [173, 181] EXTRA_PRODUCT/DEFAULT pol=[] rel=['GOV-012', 'ARC-021']: Keyed services for several implementations of one abstraction selected by a known key, not when a single registration or simple factory is clearer.
- V2 FG-K0-c5bc2f0e7c [173, 181] EXTRA_PRODUCT/DEFAULT pol=[] rel=['GOV-012', 'ARC-023']: Use assembly scanning only when registration volume creates genuine repetitive boilerplate, scanning the assembly that owns the services.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0118 -> FG-K0-b2a42159f2 [MIXED] Interface-to-implementation registration at architectural boundaries, concrete registration for implementation-only helpers; prefer explicit registration in small and medium applic
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0120 -> FG-K0-9e13b040f1 [CANONICAL_ONLY] Scrutor is not added for a single decoration when normal composition is simpler.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0121 -> FG-K0-c5bc2f0e7c [EXTRA_PRODUCT] Use assembly scanning only when registration volume creates genuine repetitive boilerplate, scanning the assembly that owns the services.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0098 -> FG-K0-3ee80273f7 [CANONICAL_ONLY] Service lifetimes must be valid; never capture a shorter-lived dependency in a longer-lived service.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0228 -> FG-K0-6e94029c43 [MIXED] Use interface-to-implementation registration at architectural boundaries (concrete registration for implementation-only helpers); prefer explicit registration in small/medium appli
- NAMED replica/K0/constraints.jsonl/RULE-K0-0046 -> FG-K0-3ee80273f7 [CANONICAL_ONLY] Service lifetimes must be valid; never capture a shorter-lived dependency in a longer-lived service.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0017 -> FG-K0-60a5b8de95 [EXTRA_PRODUCT] Application services, repositories and external adapters use interface-to-implementation registration at architectural boundaries; implementation-only helpers can be registered con
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0018 -> FG-K0-10b20a5501 [CANONICAL_ONLY] An application service depending on scoped repositories or the Unit of Work is scoped; registering it as a singleton captures them.

## CIS-K0-U0037 (pass 3) K0 .claude/skills/dependency-injection/SKILL.md:180-180  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: The DI decision guide directs runtime implementation selection to Factory delegate; potential selection guidance beyond general valid lifetimes and actual composition need.
TRIGGER: Registering services for runtime implementation selection under the DI skill | EXC: Explicit registration preferred for small/medium applications; specialized techniques solve actual composition problems. Table is not expressly exclusive. | POL: []
CODEX WHY: Concrete helper registration and generic technique necessity already covered; possible additional recommendation remains unresolved rather than verified novelty.
```
 177  | Several implementations chosen by key | Keyed services |
 178  | Cross-cutting behavior | Decorator |
 179  | Convention-based registration | Scrutor |
 180> | Runtime implementation selection | Factory delegate |
 181  | Strongly typed configuration | `AddOptions<T>().BindConfiguration()` (`configuration`) |
 182  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-3ee80273f7 [173, 181] CANONICAL_ONLY/MUST pol=['ARC-022'] rel=[]: Service lifetimes must be valid; never capture a shorter-lived dependency in a longer-lived service.
- V2 FG-K0-3ee80273f7 [171, 181] CANONICAL_ONLY/MUST pol=['ARC-022'] rel=[]: Service lifetimes must be valid; never capture a shorter-lived dependency in a longer-lived service.
- V2 FG-K0-f81797201d [173, 181] CANONICAL_PLUS_DELTA/DEFAULT pol=['RUN-022'] rel=[]: Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; direct IConfiguration access only in the composition root, provider setup and infrastructure registration.
- V2 FG-K0-6e94029c43 [171, 181] MIXED/MIXED pol=[] rel=[]: Use interface-to-implementation registration at architectural boundaries (concrete registration for implementation-only helpers); prefer explicit registration in small/medium applications; keyed services, factories, decorators, Sc
- V2 FG-K0-6ea7ff7c20 [173, 181] EXTRA_PRODUCT/DEFAULT pol=[] rel=['GOV-012', 'ARC-021']: Keyed services for several implementations of one abstraction selected by a known key, not when a single registration or simple factory is clearer.
- V2 FG-K0-c5bc2f0e7c [173, 181] EXTRA_PRODUCT/DEFAULT pol=[] rel=['GOV-012', 'ARC-023']: Use assembly scanning only when registration volume creates genuine repetitive boilerplate, scanning the assembly that owns the services.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0118 -> FG-K0-b2a42159f2 [MIXED] Interface-to-implementation registration at architectural boundaries, concrete registration for implementation-only helpers; prefer explicit registration in small and medium applic
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0120 -> FG-K0-9e13b040f1 [CANONICAL_ONLY] Scrutor is not added for a single decoration when normal composition is simpler.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0121 -> FG-K0-c5bc2f0e7c [EXTRA_PRODUCT] Use assembly scanning only when registration volume creates genuine repetitive boilerplate, scanning the assembly that owns the services.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0098 -> FG-K0-3ee80273f7 [CANONICAL_ONLY] Service lifetimes must be valid; never capture a shorter-lived dependency in a longer-lived service.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0228 -> FG-K0-6e94029c43 [MIXED] Use interface-to-implementation registration at architectural boundaries (concrete registration for implementation-only helpers); prefer explicit registration in small/medium appli
- NAMED replica/K0/constraints.jsonl/RULE-K0-0046 -> FG-K0-3ee80273f7 [CANONICAL_ONLY] Service lifetimes must be valid; never capture a shorter-lived dependency in a longer-lived service.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0017 -> FG-K0-60a5b8de95 [EXTRA_PRODUCT] Application services, repositories and external adapters use interface-to-implementation registration at architectural boundaries; implementation-only helpers can be registered con
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0018 -> FG-K0-10b20a5501 [CANONICAL_ONLY] An application service depending on scoped repositories or the Unit of Work is scoped; registering it as a singleton captures them.

## CIS-K1-U0020 (pass 3) K1 .claude/skills/dependency-injection/SKILL.md:56-56  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For a pure stateless helper without scoped dependencies, the lifetime table recommends Transient or concrete registration.
TRIGGER: Selecting DI lifetime for a pure stateless helper without scoped dependencies | EXC: Technique guidance, not universal lifetime restriction or global prohibition on adding Scrutor; actual composition need and normal simpler composition remain governing conditions. | POL: []
CODEX WHY: Same indexed passage can contain a separate technique qualifier; normativity and subsumption remain unresolved. Existing Application scoped claim BF0071 is not duplicated.
```
  53  | Scenario | Lifetime |
  54  |---|---|
  55  | Application service using repositories/Unit of Work | Scoped |
  56> | Pure stateless helper without scoped dependencies | Transient or concrete registration |
  57  | Immutable/shared configuration | Singleton-compatible |
  58  | Persistence context | Scoped (registered by the persistence facet) |
  59  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K1-93cd441f08 [55, 58] CANONICAL_ONLY/MUST pol=['ARC-022'] rel=[]: Dependency lifetimes are valid; never capture a shorter-lived dependency in a longer-lived service.
- V2 FG-K1-93cd441f08 [53, 58] CANONICAL_ONLY/MUST pol=['ARC-022'] rel=[]: Dependency lifetimes are valid; never capture a shorter-lived dependency in a longer-lived service.
- NAMED primary/K1/constraints.jsonl/EXTRA-K1-0123 -> FG-K1-ca274c8064 [EXTRA_PRODUCT] Use abstractions at architectural boundaries (Application services, repositories, external adapters); concrete registration is fine for implementation-only helpers.
- NAMED primary/K1/constraints.jsonl/EXTRA-K1-0124 -> FG-K1-0b33e75938 [CANONICAL_ONLY] Prefer explicit registration in small and medium applications; scanning, keyed services, factories or decorators only for actual composition problems.
- NAMED primary/K1/constraints.jsonl/EXTRA-K1-0126 -> FG-K1-b9090a95d9 [CANONICAL_ONLY] Do not add Scrutor for a single decoration when normal composition is simpler.
- NAMED replica/K1/constraints.jsonl/RULE-K1-0048 -> FG-K1-93cd441f08 [CANONICAL_ONLY] Dependency lifetimes are valid; never capture a shorter-lived dependency in a longer-lived service.
- NAMED replica/K1/constraints.jsonl/RULE-K1-0237 -> FG-K1-1b9a7a70dd [EXTRA_PRODUCT] Use assembly scanning only when registration volume creates genuine boilerplate, scanning the assembly that owns the services.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0070 -> FG-K1-ca274c8064 [EXTRA_PRODUCT] Use abstractions at architectural boundaries (Application services, repositories, external adapters); concrete registration is fine for implementation-only helpers.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0071 -> FG-K1-57a6b5dba0 [MIXED] Never register an Application service depending on scoped repositories as a singleton; a singleton/hosted service needing scoped work creates a scope per operation and resolves a s
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0072 -> FG-K1-1b9a7a70dd [EXTRA_PRODUCT] Use assembly scanning only when registration volume creates genuine boilerplate, scanning the assembly that owns the services.

## CIS-K1-U0021 (pass 3) K1 .claude/skills/dependency-injection/SKILL.md:106-106  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The shown Scrutor decorator registration is conditioned on Scrutor already being used.
TRIGGER: Following the specific decorator-registration example in the DI skill | EXC: Technique guidance, not universal lifetime restriction or global prohibition on adding Scrutor; actual composition need and normal simpler composition remain governing conditions. | POL: []
CODEX WHY: Same indexed passage can contain a separate technique qualifier; normativity and subsumption remain unresolved. Existing Application scoped claim BF0071 is not duplicated.
```
 103  }
 104  ```
 105  
 106> If Scrutor is already used: `services.AddScoped<IOrderService, OrderService>(); services.Decorate<IOrderService, LoggingOrderService>();`. Do not add Scrutor for a single decoration when normal composition is simpl
 107  
 108  ## Convention scanning (Scrutor)
 109  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K1-9be9561772 [106, 106] CANONICAL_ONLY/DEFAULT pol=['GOV-012', 'GOV-013'] rel=['ARC-021']: Prefer explicit DI registration in small and medium applications; add assembly scanning, keyed services, factories or decorators only when they solve an actual composition problem.
- V2 FG-K1-d8c34708a7 [106, 106] CANONICAL_ONLY/MUST_NOT pol=['DEP-001', 'GOV-013'] rel=[]: Do not add Scrutor for a single decoration when normal composition is simpler.
- V2 FG-K1-b9090a95d9 [106, 106] CANONICAL_ONLY/MUST_NOT pol=['DEP-001', 'GOV-013'] rel=[]: Do not add Scrutor for a single decoration when normal composition is simpler.
- V2 FG-K1-1b9a7a70dd [106, 106] EXTRA_PRODUCT/DEFAULT pol=[] rel=['GOV-012', 'ARC-023']: Use assembly scanning only when registration volume creates genuine boilerplate, scanning the assembly that owns the services.
- NAMED primary/K1/constraints.jsonl/EXTRA-K1-0123 -> FG-K1-ca274c8064 [EXTRA_PRODUCT] Use abstractions at architectural boundaries (Application services, repositories, external adapters); concrete registration is fine for implementation-only helpers.
- NAMED primary/K1/constraints.jsonl/EXTRA-K1-0124 -> FG-K1-0b33e75938 [CANONICAL_ONLY] Prefer explicit registration in small and medium applications; scanning, keyed services, factories or decorators only for actual composition problems.
- NAMED primary/K1/constraints.jsonl/EXTRA-K1-0126 -> FG-K1-b9090a95d9 [CANONICAL_ONLY] Do not add Scrutor for a single decoration when normal composition is simpler.
- NAMED replica/K1/constraints.jsonl/RULE-K1-0048 -> FG-K1-93cd441f08 [CANONICAL_ONLY] Dependency lifetimes are valid; never capture a shorter-lived dependency in a longer-lived service.
- NAMED replica/K1/constraints.jsonl/RULE-K1-0237 -> FG-K1-1b9a7a70dd [EXTRA_PRODUCT] Use assembly scanning only when registration volume creates genuine boilerplate, scanning the assembly that owns the services.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0070 -> FG-K1-ca274c8064 [EXTRA_PRODUCT] Use abstractions at architectural boundaries (Application services, repositories, external adapters); concrete registration is fine for implementation-only helpers.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0071 -> FG-K1-57a6b5dba0 [MIXED] Never register an Application service depending on scoped repositories as a singleton; a singleton/hosted service needing scoped work creates a scope per operation and resolves a s
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0072 -> FG-K1-1b9a7a70dd [EXTRA_PRODUCT] Use assembly scanning only when registration volume creates genuine boilerplate, scanning the assembly that owns the services.
