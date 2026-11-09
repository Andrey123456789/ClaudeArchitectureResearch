# LOGGING-SCOPE-GUIDE (4 records)

## CIS-L0-U0041 (pass 3) L0 .claude/skills/logging/SKILL.md:86-86  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For context shared across log entries, the decision guide selects BeginScope.
TRIGGER: Choosing a technique for context shared across log entries. | EXC: Optional technique; no mandatory audit subsystem, sink adoption or exclusive context API inferred. Audit use requires adopted design; runtime library semantics are described by the source, not indepen | POL: ['RUN-013']
CODEX WHY: Source-grounded optional recommendation/permission could guide an independent choice, but may be only implementation technique or already implicit in broad logging policy.
```
  83  | Scenario | Technique |
  84  |---|---|
  85  | Application logging API | `ILogger<T>` |
  86> | Context shared across entries | `BeginScope` |
  87  | Unexpected handled exception | `logger.LogError(exception, template, ...)` in the handler that owns it |
  88  | Expected business rejection | usually no Error entry |
  89  | Serilog setup, sinks, enrichers | `references/serilog.md` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L0-bd296dc96b [83, 90] CANONICAL_ONLY/MUST pol=['API-012'] rel=[]: Log an unexpected exception once at the handling boundary, not in every layer.
- V2 FG-L0-932544f0c6 [83, 90] CANONICAL_ONLY/DEFAULT pol=['API-009'] rel=[]: Represent common expected outcomes explicitly when useful (null, bool, typed outcome, deliberately adopted Result) using the simplest contract.
- V2 FG-L0-e511038b58 [83, 90] CANONICAL_ONLY/MUST_NOT pol=['API-009'] rel=[]: Do not force a generic Result<T> pattern; no HTTP-named outcome categories in Application; describe Application semantics and map them to HTTP in Api.
- V2 FG-L0-b81cf21323 [83, 90] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=[]: ILogger<T> with structured templates and stable property names; avoid interpolation that flattens values.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0471 -> FG-L0-c65b6e6c48 [CANONICAL_ONLY] Keep log property names stable so logs remain queryable.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0479 -> FG-L0-8c9ca73b13 [CANONICAL_ONLY] Keep Log.Logger and LogContext at composition/provider-specific boundaries (application code on ILogger<T>).
- NAMED primary/L0/constraints.jsonl/EXTRA-L0-0146 -> FG-L0-dbc44960e4 [EXTRA_PRODUCT] Do not use logs as an audit database without an adopted audit design.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0143 -> FG-L0-b81cf21323 [CANONICAL_ONLY] ILogger<T> with structured templates and stable property names; avoid interpolation that flattens values.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0144 -> FG-L0-9f57cdb5cf [CANONICAL_ONLY] With Serilog use builder.Services.AddSerilog(...) (not UseSerilog()); levels/sinks/overrides in environment-aware configuration; application code depends on ILogger<T>.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0094 -> FG-L0-78c1bb0108 [CANONICAL_ONLY] Normal structured logging suffices; use source-generated logging only on a measured high-volume path, not everywhere to avoid theoretical allocations.

## CIS-L1-U0027 (pass 3) L1 .claude/skills/logging/SKILL.md:67-67  [DEFAULT UNCERTAIN_NOVELTY]
CLAIM: Use BeginScope by default for context shared across log entries (LogContext at Serilog-specific boundaries).
TRIGGER: Applicable logging scenario and selected provider; no automatic infrastructure adoption | EXC: Table header Option (except skill Default); only needed sinks/enrichers; direct Serilog at provider boundaries. AuditTo parenthetical describes synchronous/exception propagation but no runtime proof a | POL: []
CODEX WHY: Specific scenario/API choice differs from generic logging policy, existing U0015 prerequisite, and adoption permission. Whether available options create normative constraints remains open.
```
  64  | Scenario | Default |
  65  | --- | --- |
  66  | Logging API | `ILogger<T>` |
  67> | Shared context across entries | `BeginScope` (Serilog: `LogContext`) |
  68  | Unexpected handled exception | log once at the handling boundary |
  69  | Expected business rejection | usually no Error log |
  70  | Provider setup | `references/serilog.md` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L1-02ac25b097 [64, 71] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=[]: Log through the injected abstraction with structured templates and stable property names; avoid interpolation.
- V2 FG-L1-7858f9b1fa [64, 71] CANONICAL_ONLY/MUST pol=['API-012'] rel=[]: Log an unexpected exception once at the handling boundary.
- V2 FG-L1-ecd48b7caf [64, 71] CANONICAL_ONLY/DEFAULT pol=['API-009'] rel=[]: Represent common expected outcomes explicitly when useful (null, bool, typed outcome); no forced generic result wrapper; no HTTP-named outcome categories; the entry point maps outcomes to HTTP.
- NAMED primary/L1/constraints.jsonl/RULE-L1-0498 -> FG-L1-e6779ead4c [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries (application code on ILogger<T>).
- NAMED primary/L1/constraints.jsonl/RULE-L1-0499 -> FG-L1-d8a716f67f [CANONICAL_ONLY] Configure only sinks and enrichers the project needs; Console is enough locally; File/Seq/OpenTelemetry/Elasticsearch are options, not baseline dependencies.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0181 -> FG-L1-c936a0d93d [EXTRA_PRODUCT] Do not use logs as an audit database without an adopted audit design.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0184 -> FG-L1-148957dd5b [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0143 -> FG-L1-36e12d0f5b [CANONICAL_ONLY] With Serilog use DI-integrated AddSerilog with environment-aware configuration; application code depends on ILogger<T>.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0127 -> FG-L1-d6ccf61e2f [NON_NORMATIVE] The Serilog bootstrap example logs a fatal startup failure without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0128 -> FG-L1-148957dd5b [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0129 -> FG-L1-6a59d2372c [CANONICAL_ONLY] Validate or normalize correlation ids accepted from clients.

## CIS-K0-U0040 (pass 3) K0 .claude/skills/logging/SKILL.md:99-99  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: For context shared across log entries the logging guide directs the author to BeginScope.
TRIGGER: Sharing context across log entries under the logging skill or its private reference | EXC: Only for the concrete logging need; sinks are optional. Provider-specific APIs stay at composition/provider boundaries. No global or exclusive requirement inferred. | POL: ['RUN-013', 'DEP-010']
CODEX WHY: Potential independent technique guidance, with uncertainty about descriptive modality and whether the broad independent finding already encompasses it.
```
  96  | Scenario | Technique |
  97  |---|---|
  98  | Application logging API | `ILogger<T>` |
  99> | Context shared across log entries | `BeginScope` |
 100  | Unexpected handled exception | Log once at the handling boundary |
 101  | Expected business rejection | No Error log |
 102  | Serilog setup, sinks, enrichers | `references/serilog.md` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-374804eff0 [98, 103] CANONICAL_ONLY/MUST pol=['API-012'] rel=[]: Unexpected exceptions are logged once, by default at the handling boundary, never repeatedly across layers and the global handler.
- V2 FG-K0-374804eff0 [96, 103] CANONICAL_ONLY/MUST pol=['API-012'] rel=[]: Unexpected exceptions are logged once, by default at the handling boundary, never repeatedly across layers and the global handler.
- V2 FG-K0-22a95f7e7f [96, 103] CANONICAL_ONLY/DEFAULT pol=['API-009'] rel=['ARC-020']: Represent expected outcomes explicitly when useful (null, bool, typed outcome) without forcing Result<T> or HTTP-named categories in Application.
- V2 FG-K0-84d69f4114 [96, 103] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=['DEP-010']: ILogger<T> with structured message templates and stable property names; avoid interpolation that makes structured values opaque.
- V2 FG-K0-fb31028a10 [98, 103] CANONICAL_ONLY/DEFAULT pol=['API-009'] rel=['API-012', 'RUN-013']: Expected outcomes such as NotFound, validation failures or rejected business operations are not logged as application errors.
- V2 FG-K0-ae4e861431 [98, 103] CANONICAL_ONLY/DEFAULT pol=['RUN-008'] rel=[]: Normal structured ILogger calls suffice; source-generated LoggerMessage only for measured high-volume hot paths, not everywhere by default.
- V2 FG-K0-bea0f704fb [98, 103] CANONICAL_ONLY/DECIDED pol=['DEP-010', 'DEP-021'] rel=['RUN-013', 'DEP-001']: ILogger<T> in application code with Serilog as provider (Serilog.AspNetCore; sinks only as required).
- NAMED primary/K0/constraints.jsonl/RULE-K0-0450 -> FG-K0-458a5e6617 [CANONICAL_ONLY] Application code keeps using ILogger<T>; direct Serilog APIs (Log.Logger, LogContext) stay at composition or provider-specific boundaries.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0452 -> FG-K0-ea63ebf1dc [CANONICAL_ONLY] Keep levels, sinks and overrides in configuration so they can differ per environment.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0190 -> FG-K0-17e2f22e6a [CANONICAL_ONLY] File, Seq and other sinks are not baseline dependencies; a Console sink suffices for a simple local Development baseline; example limits and retention values are illustrative.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0071 -> FG-K0-84d69f4114 [CANONICAL_ONLY] ILogger<T> with structured message templates and stable property names; avoid interpolation that makes structured values opaque.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0072 -> FG-K0-a89cc47d55 [CANONICAL_ONLY] When Serilog is configured use DI-integrated AddSerilog with environment-aware provider configuration; application code depends on ILogger<T>.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0042 -> FG-K0-b967417c39 [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.

## CIS-K1-U0024 (pass 3) K1 .claude/skills/logging/SKILL.md:76-76  [DEFAULT UNCERTAIN_NOVELTY]
CLAIM: For context shared across log entries, the logging decision guide gives BeginScope as the default.
TRIGGER: Shared context across multiple log entries while using the applicable knowledge reference | EXC: Recommendation or optional integration, not mandatory adoption or exclusive list. Sinks require actual need; Serilog APIs remain at provider/composition edges; examples do not authorize hardcoded oper | POL: []
CODEX WHY: Generic option coverage may subsume these conventional techniques; semantic independence remains unresolved. Existing U0010 Enrich.FromLogContext prerequisite is not duplicated, and AuditTo adoption gate is already EXTRA0203/BF0040.
```
  73  | Scenario | Default |
  74  |---|---|
  75  | Application logging API | `ILogger<T>` |
  76> | Context shared across entries | `BeginScope` |
  77  | Unexpected handled exception | Log once at the handling boundary |
  78  | Expected business rejection | Usually no Error log |
  79  | Serilog provider setup | `references/serilog.md` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K1-c919198c86 [73, 80] CANONICAL_ONLY/MUST pol=['API-012'] rel=[]: Log an unexpected exception once at the handling boundary; never again across repository, Application, controller and global handler.
- V2 FG-K1-c919198c86 [75, 80] CANONICAL_ONLY/MUST pol=['API-012'] rel=[]: Log an unexpected exception once at the handling boundary; never again across repository, Application, controller and global handler.
- V2 FG-K1-307a12b5d5 [73, 80] CANONICAL_ONLY/DEFAULT pol=['API-009'] rel=[]: Represent expected outcomes explicitly when useful (null, bool, typed outcome); no forced Result<T>; no HTTP-named outcome categories in Application.
- V2 FG-K1-505943657f [73, 80] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=['DEP-010']: ILogger<T> with structured templates and stable property names; avoid interpolation that makes structured values opaque.
- V2 FG-K1-493b0ae5c9 [73, 80] CANONICAL_ONLY/DEFAULT pol=['RUN-008'] rel=[]: Compiled queries, ValueTask, pooling, custom serialization, aggressive caching and raw SQL for performance only for a measured or clearly demonstrated need.
- V2 FG-K1-7698e04e21 [75, 80] CANONICAL_ONLY/DEFAULT pol=['API-009'] rel=[]: Expected outcomes (not found, validation failures, rejected operations) are normally not logged as application errors.
- V2 FG-K1-c00d0b681d [75, 80] CANONICAL_ONLY/DEFAULT pol=['RUN-008'] rel=[]: Normal structured ILogger calls suffice; source-generated LoggerMessage only for measured high-volume hot paths, not everywhere to avoid theoretical allocations.
- V2 FG-K1-aad27ece18 [75, 80] CANONICAL_ONLY/DECIDED pol=['DEP-010', 'DEP-021'] rel=[]: Application code logs through ILogger<T>; Serilog is the provider.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0454 -> FG-K1-38e289cf30 [CANONICAL_ONLY] Levels, sinks and overrides live in appsettings so they change per environment without redeployment.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0455 -> FG-K1-4e5dcc868a [CANONICAL_ONLY] Serilog APIs (Log.Logger, LogContext) stay at composition and provider-specific boundaries.
- NAMED primary/K1/constraints.jsonl/EXTRA-K1-0197 -> FG-K1-33200fed57 [CANONICAL_ONLY] Serilog.AspNetCore is the baseline integration package.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0456 -> FG-K1-1d4be1ff67 [CANONICAL_ONLY] Add sinks and enrichers only when the project requires them, through add-dependency.
- NAMED replica/K1/constraints.jsonl/RULE-K1-0058 -> FG-K1-505943657f [CANONICAL_ONLY] ILogger<T> with structured templates and stable property names; avoid interpolation that makes structured values opaque.
- NAMED replica/K1/constraints.jsonl/RULE-K1-0059 -> FG-K1-3b8ba4aabd [CANONICAL_ONLY] When Serilog is configured use DI-integrated AddSerilog with environment-aware provider configuration; application code depends on ILogger<T>.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0038 -> FG-K1-4e5dcc868a [CANONICAL_ONLY] Serilog APIs (Log.Logger, LogContext) stay at composition and provider-specific boundaries.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0039 -> FG-K1-33200fed57 [CANONICAL_ONLY] Serilog.AspNetCore is the baseline integration package.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0040 -> FG-K1-7d2487d180 [EXTRA_PRODUCT] When the static/bootstrap Log.Logger is used flush it on shutdown (CloseAndFlushAsync) so asynchronous sinks keep buffered events.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0041 -> FG-K1-6a33dca936 [CANONICAL_ONLY] Validate or normalize a correlation identifier accepted from an external client.
