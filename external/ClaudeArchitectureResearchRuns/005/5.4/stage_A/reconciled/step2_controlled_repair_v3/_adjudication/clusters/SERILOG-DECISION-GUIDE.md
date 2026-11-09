# SERILOG-DECISION-GUIDE (44 records)

## CIS-M-U0026 (pass 2) M .claude/skills/logging/references/serilog.md:198-198  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: The scoped LogContext example requires Enrich.FromLogContext() on the logger configuration.
TRIGGER: Using LogContext.PushProperty to attach properties to logged events. | EXC: Reference owns technique and examples, no policy. Lines76-81 explicitly make sinks/enrichers optional and Console sufficient locally. No mandatory adoption, exclusive backend list or independently ver | POL: ['RUN-013', 'DEP-021']
CODEX WHY: The exact source can guide a different implementation choice, but optional technique ownership and broad-policy subsumption remain credible. Preserve as unresolved, not a proven extra requirement or cross-candidate difference.
```
 195  }
 196  ```
 197  
 198> Requires `.Enrich.FromLogContext()` on the logger configuration.
 199  
 200  ## OpenTelemetry Sink (OTLP Export)
 201  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/M/constraints.jsonl/RULE-M-0189 -> FG-M-fe9089370b [CANONICAL_ONLY] Add Serilog sinks only when required; a Console sink suffices for local Development.
- NAMED primary/M/constraints.jsonl/RULE-M-0504 -> FG-M-4b5b28eca6 [CANONICAL_ONLY] Keep log levels, sinks and overrides in configuration so they change per environment without redeployment.
- NAMED primary/M/constraints.jsonl/RULE-M-0505 -> FG-M-a9131f9b4d [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries.
- NAMED replica/M/constraints.jsonl/RULE-M-0060 -> FG-M-2cebfa2b6d [CANONICAL_ONLY] When Serilog is configured use builder.Services.AddSerilog(...) rather than UseSerilog; keep provider configuration in environment-aware configuration; application code depends on 
- NAMED replica/M/constraints.jsonl/RULE-M-0067 -> FG-M-23a0768623 [CANONICAL_ONLY] Use ILogger<T> with structured message templates and stable property names; avoid string interpolation in log calls.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0089 -> FG-M-5095798628 [EXTRA_PRODUCT] When using Serilog's static/bootstrap Log.Logger flush it on shutdown; for purely host-managed logging follow the provider lifetime instead of static lifecycle code.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0090 -> FG-M-ade51003dd [EXTRA_PRODUCT] Use the official Elastic.Serilog.Sinks package instead of the deprecated Serilog.Sinks.Elasticsearch when writing to Elasticsearch.

## CIS-M-U0018 (pass 2) M .claude/skills/logging/references/serilog.md:290-290  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For development log storage, the Serilog guide recommends Seq or Aspire Dashboard.
TRIGGER: Choosing a development log-storage backend when storage is needed. | EXC: Reference owns technique and examples, no policy. Lines76-81 explicitly make sinks/enrichers optional and Console sufficient locally. No mandatory adoption, exclusive backend list or independently ver | POL: ['RUN-013', 'DEP-021']
CODEX WHY: The exact source can guide a different implementation choice, but optional technique ownership and broad-policy subsumption remain credible. Preserve as unresolved, not a proven extra requirement or cross-candidate difference.
```
 287  | Scenario | Recommendation |
 288  |----------|---------------|
 289  | Project uses Serilog as provider | `AddSerilog()` + configuration |
 290> | Log storage (development) | Seq (free single-user) or Aspire Dashboard |
 291  | Log storage (production) | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 292  | Request logging | `UseSerilogRequestLogging()` |
 293  | Scoped properties | `LogContext.PushProperty()` in middleware |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-2cebfa2b6d [287, 298] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: When Serilog is configured use builder.Services.AddSerilog(...) rather than UseSerilog; keep provider configuration in environment-aware configuration; application code depends on ILogger<T>.
- V2 FG-M-23a0768623 [287, 298] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=[]: Use ILogger<T> with structured message templates and stable property names; avoid string interpolation in log calls.
- NAMED primary/M/constraints.jsonl/RULE-M-0189 -> FG-M-fe9089370b [CANONICAL_ONLY] Add Serilog sinks only when required; a Console sink suffices for local Development.
- NAMED primary/M/constraints.jsonl/RULE-M-0504 -> FG-M-4b5b28eca6 [CANONICAL_ONLY] Keep log levels, sinks and overrides in configuration so they change per environment without redeployment.
- NAMED primary/M/constraints.jsonl/RULE-M-0505 -> FG-M-a9131f9b4d [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries.
- NAMED replica/M/constraints.jsonl/RULE-M-0060 -> FG-M-2cebfa2b6d [CANONICAL_ONLY] When Serilog is configured use builder.Services.AddSerilog(...) rather than UseSerilog; keep provider configuration in environment-aware configuration; application code depends on 
- NAMED replica/M/constraints.jsonl/RULE-M-0067 -> FG-M-23a0768623 [CANONICAL_ONLY] Use ILogger<T> with structured message templates and stable property names; avoid string interpolation in log calls.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0089 -> FG-M-5095798628 [EXTRA_PRODUCT] When using Serilog's static/bootstrap Log.Logger flush it on shutdown; for purely host-managed logging follow the provider lifetime instead of static lifecycle code.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0090 -> FG-M-ade51003dd [EXTRA_PRODUCT] Use the official Elastic.Serilog.Sinks package instead of the deprecated Serilog.Sinks.Elasticsearch when writing to Elasticsearch.

## CIS-M-U0019 (pass 2) M .claude/skills/logging/references/serilog.md:291-291  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For production log storage, the guide recommends Seq, Elasticsearch through the Elastic sink, or an OTLP backend.
TRIGGER: Choosing production log storage when required. | EXC: Reference owns technique and examples, no policy. Lines76-81 explicitly make sinks/enrichers optional and Console sufficient locally. No mandatory adoption, exclusive backend list or independently ver | POL: ['RUN-013', 'DEP-021']
CODEX WHY: The exact source can guide a different implementation choice, but optional technique ownership and broad-policy subsumption remain credible. Preserve as unresolved, not a proven extra requirement or cross-candidate difference.
```
 288  |----------|---------------|
 289  | Project uses Serilog as provider | `AddSerilog()` + configuration |
 290  | Log storage (development) | Seq (free single-user) or Aspire Dashboard |
 291> | Log storage (production) | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 292  | Request logging | `UseSerilogRequestLogging()` |
 293  | Scoped properties | `LogContext.PushProperty()` in middleware |
 294  | Log filtering | `Serilog.Expressions` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-2cebfa2b6d [287, 298] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: When Serilog is configured use builder.Services.AddSerilog(...) rather than UseSerilog; keep provider configuration in environment-aware configuration; application code depends on ILogger<T>.
- V2 FG-M-23a0768623 [287, 298] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=[]: Use ILogger<T> with structured message templates and stable property names; avoid string interpolation in log calls.
- NAMED primary/M/constraints.jsonl/RULE-M-0189 -> FG-M-fe9089370b [CANONICAL_ONLY] Add Serilog sinks only when required; a Console sink suffices for local Development.
- NAMED primary/M/constraints.jsonl/RULE-M-0504 -> FG-M-4b5b28eca6 [CANONICAL_ONLY] Keep log levels, sinks and overrides in configuration so they change per environment without redeployment.
- NAMED primary/M/constraints.jsonl/RULE-M-0505 -> FG-M-a9131f9b4d [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries.
- NAMED replica/M/constraints.jsonl/RULE-M-0060 -> FG-M-2cebfa2b6d [CANONICAL_ONLY] When Serilog is configured use builder.Services.AddSerilog(...) rather than UseSerilog; keep provider configuration in environment-aware configuration; application code depends on 
- NAMED replica/M/constraints.jsonl/RULE-M-0067 -> FG-M-23a0768623 [CANONICAL_ONLY] Use ILogger<T> with structured message templates and stable property names; avoid string interpolation in log calls.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0089 -> FG-M-5095798628 [EXTRA_PRODUCT] When using Serilog's static/bootstrap Log.Logger flush it on shutdown; for purely host-managed logging follow the provider lifetime instead of static lifecycle code.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0090 -> FG-M-ade51003dd [EXTRA_PRODUCT] Use the official Elastic.Serilog.Sinks package instead of the deprecated Serilog.Sinks.Elasticsearch when writing to Elasticsearch.

## CIS-M-U0020 (pass 2) M .claude/skills/logging/references/serilog.md:292-292  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For request logging, the guide recommends UseSerilogRequestLogging().
TRIGGER: Choosing request-logging technique with Serilog. | EXC: Reference owns technique and examples, no policy. Lines76-81 explicitly make sinks/enrichers optional and Console sufficient locally. No mandatory adoption, exclusive backend list or independently ver | POL: ['RUN-013', 'DEP-021']
CODEX WHY: The exact source can guide a different implementation choice, but optional technique ownership and broad-policy subsumption remain credible. Preserve as unresolved, not a proven extra requirement or cross-candidate difference.
```
 289  | Project uses Serilog as provider | `AddSerilog()` + configuration |
 290  | Log storage (development) | Seq (free single-user) or Aspire Dashboard |
 291  | Log storage (production) | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 292> | Request logging | `UseSerilogRequestLogging()` |
 293  | Scoped properties | `LogContext.PushProperty()` in middleware |
 294  | Log filtering | `Serilog.Expressions` |
 295  | High-performance paths | `[LoggerMessage]` source generator |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-2cebfa2b6d [287, 298] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: When Serilog is configured use builder.Services.AddSerilog(...) rather than UseSerilog; keep provider configuration in environment-aware configuration; application code depends on ILogger<T>.
- V2 FG-M-23a0768623 [287, 298] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=[]: Use ILogger<T> with structured message templates and stable property names; avoid string interpolation in log calls.
- NAMED primary/M/constraints.jsonl/RULE-M-0189 -> FG-M-fe9089370b [CANONICAL_ONLY] Add Serilog sinks only when required; a Console sink suffices for local Development.
- NAMED primary/M/constraints.jsonl/RULE-M-0504 -> FG-M-4b5b28eca6 [CANONICAL_ONLY] Keep log levels, sinks and overrides in configuration so they change per environment without redeployment.
- NAMED primary/M/constraints.jsonl/RULE-M-0505 -> FG-M-a9131f9b4d [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries.
- NAMED replica/M/constraints.jsonl/RULE-M-0060 -> FG-M-2cebfa2b6d [CANONICAL_ONLY] When Serilog is configured use builder.Services.AddSerilog(...) rather than UseSerilog; keep provider configuration in environment-aware configuration; application code depends on 
- NAMED replica/M/constraints.jsonl/RULE-M-0067 -> FG-M-23a0768623 [CANONICAL_ONLY] Use ILogger<T> with structured message templates and stable property names; avoid string interpolation in log calls.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0089 -> FG-M-5095798628 [EXTRA_PRODUCT] When using Serilog's static/bootstrap Log.Logger flush it on shutdown; for purely host-managed logging follow the provider lifetime instead of static lifecycle code.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0090 -> FG-M-ade51003dd [EXTRA_PRODUCT] Use the official Elastic.Serilog.Sinks package instead of the deprecated Serilog.Sinks.Elasticsearch when writing to Elasticsearch.

## CIS-M-U0021 (pass 2) M .claude/skills/logging/references/serilog.md:293-293  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For scoped properties, the guide recommends LogContext.PushProperty() in middleware.
TRIGGER: Adding scoped properties through a Serilog provider boundary. | EXC: Reference owns technique and examples, no policy. Lines76-81 explicitly make sinks/enrichers optional and Console sufficient locally. No mandatory adoption, exclusive backend list or independently ver | POL: ['RUN-013', 'DEP-021']
CODEX WHY: The exact source can guide a different implementation choice, but optional technique ownership and broad-policy subsumption remain credible. Preserve as unresolved, not a proven extra requirement or cross-candidate difference.
```
 290  | Log storage (development) | Seq (free single-user) or Aspire Dashboard |
 291  | Log storage (production) | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 292  | Request logging | `UseSerilogRequestLogging()` |
 293> | Scoped properties | `LogContext.PushProperty()` in middleware |
 294  | Log filtering | `Serilog.Expressions` |
 295  | High-performance paths | `[LoggerMessage]` source generator |
 296  | Audit trails | `AuditTo` (synchronous, exceptions propagate) |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-2cebfa2b6d [287, 298] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: When Serilog is configured use builder.Services.AddSerilog(...) rather than UseSerilog; keep provider configuration in environment-aware configuration; application code depends on ILogger<T>.
- V2 FG-M-23a0768623 [287, 298] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=[]: Use ILogger<T> with structured message templates and stable property names; avoid string interpolation in log calls.
- NAMED primary/M/constraints.jsonl/RULE-M-0189 -> FG-M-fe9089370b [CANONICAL_ONLY] Add Serilog sinks only when required; a Console sink suffices for local Development.
- NAMED primary/M/constraints.jsonl/RULE-M-0504 -> FG-M-4b5b28eca6 [CANONICAL_ONLY] Keep log levels, sinks and overrides in configuration so they change per environment without redeployment.
- NAMED primary/M/constraints.jsonl/RULE-M-0505 -> FG-M-a9131f9b4d [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries.
- NAMED replica/M/constraints.jsonl/RULE-M-0060 -> FG-M-2cebfa2b6d [CANONICAL_ONLY] When Serilog is configured use builder.Services.AddSerilog(...) rather than UseSerilog; keep provider configuration in environment-aware configuration; application code depends on 
- NAMED replica/M/constraints.jsonl/RULE-M-0067 -> FG-M-23a0768623 [CANONICAL_ONLY] Use ILogger<T> with structured message templates and stable property names; avoid string interpolation in log calls.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0089 -> FG-M-5095798628 [EXTRA_PRODUCT] When using Serilog's static/bootstrap Log.Logger flush it on shutdown; for purely host-managed logging follow the provider lifetime instead of static lifecycle code.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0090 -> FG-M-ade51003dd [EXTRA_PRODUCT] Use the official Elastic.Serilog.Sinks package instead of the deprecated Serilog.Sinks.Elasticsearch when writing to Elasticsearch.

## CIS-M-U0022 (pass 2) M .claude/skills/logging/references/serilog.md:294-294  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For log filtering, the guide recommends Serilog.Expressions.
TRIGGER: Choosing a log-filtering technique. | EXC: Reference owns technique and examples, no policy. Lines76-81 explicitly make sinks/enrichers optional and Console sufficient locally. No mandatory adoption, exclusive backend list or independently ver | POL: ['RUN-013', 'DEP-021']
CODEX WHY: The exact source can guide a different implementation choice, but optional technique ownership and broad-policy subsumption remain credible. Preserve as unresolved, not a proven extra requirement or cross-candidate difference.
```
 291  | Log storage (production) | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 292  | Request logging | `UseSerilogRequestLogging()` |
 293  | Scoped properties | `LogContext.PushProperty()` in middleware |
 294> | Log filtering | `Serilog.Expressions` |
 295  | High-performance paths | `[LoggerMessage]` source generator |
 296  | Audit trails | `AuditTo` (synchronous, exceptions propagate) |
 297  | Log levels by environment | `MinimumLevel.Override` per namespace in appsettings |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-2cebfa2b6d [287, 298] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: When Serilog is configured use builder.Services.AddSerilog(...) rather than UseSerilog; keep provider configuration in environment-aware configuration; application code depends on ILogger<T>.
- V2 FG-M-23a0768623 [287, 298] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=[]: Use ILogger<T> with structured message templates and stable property names; avoid string interpolation in log calls.
- NAMED primary/M/constraints.jsonl/RULE-M-0189 -> FG-M-fe9089370b [CANONICAL_ONLY] Add Serilog sinks only when required; a Console sink suffices for local Development.
- NAMED primary/M/constraints.jsonl/RULE-M-0504 -> FG-M-4b5b28eca6 [CANONICAL_ONLY] Keep log levels, sinks and overrides in configuration so they change per environment without redeployment.
- NAMED primary/M/constraints.jsonl/RULE-M-0505 -> FG-M-a9131f9b4d [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries.
- NAMED replica/M/constraints.jsonl/RULE-M-0060 -> FG-M-2cebfa2b6d [CANONICAL_ONLY] When Serilog is configured use builder.Services.AddSerilog(...) rather than UseSerilog; keep provider configuration in environment-aware configuration; application code depends on 
- NAMED replica/M/constraints.jsonl/RULE-M-0067 -> FG-M-23a0768623 [CANONICAL_ONLY] Use ILogger<T> with structured message templates and stable property names; avoid string interpolation in log calls.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0089 -> FG-M-5095798628 [EXTRA_PRODUCT] When using Serilog's static/bootstrap Log.Logger flush it on shutdown; for purely host-managed logging follow the provider lifetime instead of static lifecycle code.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0090 -> FG-M-ade51003dd [EXTRA_PRODUCT] Use the official Elastic.Serilog.Sinks package instead of the deprecated Serilog.Sinks.Elasticsearch when writing to Elasticsearch.

## CIS-M-U0023 (pass 2) M .claude/skills/logging/references/serilog.md:296-296  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For audit trails, the guide recommends AuditTo, describing synchronous operation and exception propagation.
TRIGGER: Selecting a Serilog technique after a dedicated audit design is adopted. | EXC: Reference owns technique and examples, no policy. Lines76-81 explicitly make sinks/enrichers optional and Console sufficient locally. No mandatory adoption, exclusive backend list or independently ver | POL: ['RUN-013', 'DEP-021']
CODEX WHY: The exact source can guide a different implementation choice, but optional technique ownership and broad-policy subsumption remain credible. Preserve as unresolved, not a proven extra requirement or cross-candidate difference.
```
 293  | Scoped properties | `LogContext.PushProperty()` in middleware |
 294  | Log filtering | `Serilog.Expressions` |
 295  | High-performance paths | `[LoggerMessage]` source generator |
 296> | Audit trails | `AuditTo` (synchronous, exceptions propagate) |
 297  | Log levels by environment | `MinimumLevel.Override` per namespace in appsettings |
 298  | OpenTelemetry integration | `Serilog.Sinks.OpenTelemetry` (no SDK dependency) |
 299  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-2cebfa2b6d [287, 298] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: When Serilog is configured use builder.Services.AddSerilog(...) rather than UseSerilog; keep provider configuration in environment-aware configuration; application code depends on ILogger<T>.
- V2 FG-M-23a0768623 [287, 298] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=[]: Use ILogger<T> with structured message templates and stable property names; avoid string interpolation in log calls.
- NAMED primary/M/constraints.jsonl/RULE-M-0189 -> FG-M-fe9089370b [CANONICAL_ONLY] Add Serilog sinks only when required; a Console sink suffices for local Development.
- NAMED primary/M/constraints.jsonl/RULE-M-0504 -> FG-M-4b5b28eca6 [CANONICAL_ONLY] Keep log levels, sinks and overrides in configuration so they change per environment without redeployment.
- NAMED primary/M/constraints.jsonl/RULE-M-0505 -> FG-M-a9131f9b4d [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries.
- NAMED replica/M/constraints.jsonl/RULE-M-0060 -> FG-M-2cebfa2b6d [CANONICAL_ONLY] When Serilog is configured use builder.Services.AddSerilog(...) rather than UseSerilog; keep provider configuration in environment-aware configuration; application code depends on 
- NAMED replica/M/constraints.jsonl/RULE-M-0067 -> FG-M-23a0768623 [CANONICAL_ONLY] Use ILogger<T> with structured message templates and stable property names; avoid string interpolation in log calls.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0089 -> FG-M-5095798628 [EXTRA_PRODUCT] When using Serilog's static/bootstrap Log.Logger flush it on shutdown; for purely host-managed logging follow the provider lifetime instead of static lifecycle code.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0090 -> FG-M-ade51003dd [EXTRA_PRODUCT] Use the official Elastic.Serilog.Sinks package instead of the deprecated Serilog.Sinks.Elasticsearch when writing to Elasticsearch.

## CIS-M-U0024 (pass 2) M .claude/skills/logging/references/serilog.md:297-297  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For log levels by environment, the guide recommends MinimumLevel.Override per namespace in appsettings.
TRIGGER: Configuring environment-specific log levels. | EXC: Reference owns technique and examples, no policy. Lines76-81 explicitly make sinks/enrichers optional and Console sufficient locally. No mandatory adoption, exclusive backend list or independently ver | POL: ['RUN-013', 'DEP-021']
CODEX WHY: The exact source can guide a different implementation choice, but optional technique ownership and broad-policy subsumption remain credible. Preserve as unresolved, not a proven extra requirement or cross-candidate difference.
```
 294  | Log filtering | `Serilog.Expressions` |
 295  | High-performance paths | `[LoggerMessage]` source generator |
 296  | Audit trails | `AuditTo` (synchronous, exceptions propagate) |
 297> | Log levels by environment | `MinimumLevel.Override` per namespace in appsettings |
 298  | OpenTelemetry integration | `Serilog.Sinks.OpenTelemetry` (no SDK dependency) |
 299  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-2cebfa2b6d [287, 298] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: When Serilog is configured use builder.Services.AddSerilog(...) rather than UseSerilog; keep provider configuration in environment-aware configuration; application code depends on ILogger<T>.
- V2 FG-M-23a0768623 [287, 298] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=[]: Use ILogger<T> with structured message templates and stable property names; avoid string interpolation in log calls.
- NAMED primary/M/constraints.jsonl/RULE-M-0189 -> FG-M-fe9089370b [CANONICAL_ONLY] Add Serilog sinks only when required; a Console sink suffices for local Development.
- NAMED primary/M/constraints.jsonl/RULE-M-0504 -> FG-M-4b5b28eca6 [CANONICAL_ONLY] Keep log levels, sinks and overrides in configuration so they change per environment without redeployment.
- NAMED primary/M/constraints.jsonl/RULE-M-0505 -> FG-M-a9131f9b4d [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries.
- NAMED replica/M/constraints.jsonl/RULE-M-0060 -> FG-M-2cebfa2b6d [CANONICAL_ONLY] When Serilog is configured use builder.Services.AddSerilog(...) rather than UseSerilog; keep provider configuration in environment-aware configuration; application code depends on 
- NAMED replica/M/constraints.jsonl/RULE-M-0067 -> FG-M-23a0768623 [CANONICAL_ONLY] Use ILogger<T> with structured message templates and stable property names; avoid string interpolation in log calls.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0089 -> FG-M-5095798628 [EXTRA_PRODUCT] When using Serilog's static/bootstrap Log.Logger flush it on shutdown; for purely host-managed logging follow the provider lifetime instead of static lifecycle code.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0090 -> FG-M-ade51003dd [EXTRA_PRODUCT] Use the official Elastic.Serilog.Sinks package instead of the deprecated Serilog.Sinks.Elasticsearch when writing to Elasticsearch.

## CIS-M-U0025 (pass 2) M .claude/skills/logging/references/serilog.md:298-298  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For OpenTelemetry integration, the guide recommends Serilog.Sinks.OpenTelemetry without an SDK dependency.
TRIGGER: Selecting a Serilog-to-OpenTelemetry integration. | EXC: Reference owns technique and examples, no policy. Lines76-81 explicitly make sinks/enrichers optional and Console sufficient locally. No mandatory adoption, exclusive backend list or independently ver | POL: ['RUN-013', 'DEP-021']
CODEX WHY: The exact source can guide a different implementation choice, but optional technique ownership and broad-policy subsumption remain credible. Preserve as unresolved, not a proven extra requirement or cross-candidate difference.
```
 295  | High-performance paths | `[LoggerMessage]` source generator |
 296  | Audit trails | `AuditTo` (synchronous, exceptions propagate) |
 297  | Log levels by environment | `MinimumLevel.Override` per namespace in appsettings |
 298> | OpenTelemetry integration | `Serilog.Sinks.OpenTelemetry` (no SDK dependency) |
 299  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-2cebfa2b6d [287, 298] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: When Serilog is configured use builder.Services.AddSerilog(...) rather than UseSerilog; keep provider configuration in environment-aware configuration; application code depends on ILogger<T>.
- V2 FG-M-23a0768623 [287, 298] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=[]: Use ILogger<T> with structured message templates and stable property names; avoid string interpolation in log calls.
- NAMED primary/M/constraints.jsonl/RULE-M-0189 -> FG-M-fe9089370b [CANONICAL_ONLY] Add Serilog sinks only when required; a Console sink suffices for local Development.
- NAMED primary/M/constraints.jsonl/RULE-M-0504 -> FG-M-4b5b28eca6 [CANONICAL_ONLY] Keep log levels, sinks and overrides in configuration so they change per environment without redeployment.
- NAMED primary/M/constraints.jsonl/RULE-M-0505 -> FG-M-a9131f9b4d [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries.
- NAMED replica/M/constraints.jsonl/RULE-M-0060 -> FG-M-2cebfa2b6d [CANONICAL_ONLY] When Serilog is configured use builder.Services.AddSerilog(...) rather than UseSerilog; keep provider configuration in environment-aware configuration; application code depends on 
- NAMED replica/M/constraints.jsonl/RULE-M-0067 -> FG-M-23a0768623 [CANONICAL_ONLY] Use ILogger<T> with structured message templates and stable property names; avoid string interpolation in log calls.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0089 -> FG-M-5095798628 [EXTRA_PRODUCT] When using Serilog's static/bootstrap Log.Logger flush it on shutdown; for purely host-managed logging follow the provider lifetime instead of static lifecycle code.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0090 -> FG-M-ade51003dd [EXTRA_PRODUCT] Use the official Elastic.Serilog.Sinks package instead of the deprecated Serilog.Sinks.Elasticsearch when writing to Elasticsearch.

## CIS-M1-U0020 (pass 2) M1 .claude/skills/logging/references/serilog.md:200-211  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: When using the Serilog.Expressions filtering technique, include the Serilog.Expressions package prerequisite.
TRIGGER: Applying string-expression filtering shown in the Serilog.Expressions section after the private reference is consulted. | EXC: Does not require adopting expression filtering, nor approve installation outside add-dependency; may be a descriptive API prerequisite rather than an independent normative choice. | POL: ['DEP-001', 'DEP-004', 'DEP-021']
CODEX WHY: Exact requires wording states a conditional dependency of a technique. It could constrain implementation when selected, but framework feasibility may be explanatory rather than independently normative. Kept uncertain rather than automatically reclassifying technical prose. Existing U0013 concerns logger enrichment configuration for scoped properties, a different prerequisite.
```
 197  })
 198  ```
 199  
 200> ## Serilog.Expressions Filtering
 201> 
 202> Requires the `Serilog.Expressions` package:
 203> 
 204> ```csharp
 205> // Exclude health check noise
 206> .Filter.ByExcluding("RequestPath like '/health%'")
 207> 
 208> // Route errors to a separate file
 209> .WriteTo.Conditional("@l = 'Error'",
 210>     wt => wt.File("logs/errors-.log", rollingInterval: RollingInterval.Day))
 211> ```
 212  
 213  ## [LoggerMessage] Source Generator for Hot Paths
 214  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/M1/constraints.jsonl/RULE-M1-0537 -> FG-M1-b45e946d3f [CANONICAL_ONLY] Sinks/enrichers beyond Console are not baseline; configure only what the project needs.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0264 -> FG-M1-71aa469282 [CANONICAL_ONLY] Before installing check deprecation, known vulnerabilities and the exact version's license (registry, upstream when needed); free download does not imply acceptability.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0144 -> FG-M1-3d0b8d6ee8 [CANONICAL_ONLY] Before installing check whether the selected package/version is deprecated, known vulnerability information and the license of the exact version from official registry metadata (an

## CIS-M1-U0039 (pass 3) M1 .claude/skills/logging/references/serilog.md:272-272  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For development log storage, prefer Seq or Aspire Dashboard.
TRIGGER: choosing development log storage | EXC: Nonexclusive recommendation; sinks and tooling not baseline dependencies, configure only project needs. No mandatory audit adoption, SDK ban or independently verified library runtime behavior inferred | POL: []
CODEX WHY: Optional tooling may still express a separately registrable preference; technique-only ownership and broad policy subsumption leave normativity unresolved.
```
 269  |---|---|
 270  | Serilog as provider | `AddSerilog()` + configuration |
 271  | General application logging API | `ILogger<T>` (logging skill) |
 272> | Log storage (development) | Seq (free single-user) or Aspire Dashboard |
 273  | Log storage (production) | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 274  | Request logging | `UseSerilogRequestLogging()` |
 275  | Scoped properties | `LogContext.PushProperty()` in middleware |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-b9dabc85e3 [268, 280] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=[]: Use ILogger<T> with structured templates and stable property names; avoid interpolation.
- V2 FG-M1-412a5270d6 [268, 280] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=['DEP-010']: When Serilog is configured use DI-integrated AddSerilog() with environment-aware provider configuration; application code depends on ILogger<T>, not Serilog APIs.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0535 -> FG-M1-5445dc5fa4 [CANONICAL_ONLY] Keep levels, sinks and overrides in appsettings to vary per environment.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0536 -> FG-M1-d73120b7f9 [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0537 -> FG-M1-b45e946d3f [CANONICAL_ONLY] Sinks/enrichers beyond Console are not baseline; configure only what the project needs.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0194 -> FG-M1-19794a2bcd [EXTRA_PRODUCT] Do not use logs as an audit database without a dedicated audit design.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0058 -> FG-M1-412a5270d6 [CANONICAL_ONLY] When Serilog is configured use DI-integrated AddSerilog() with environment-aware provider configuration; application code depends on ILogger<T>, not Serilog APIs.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0059 -> FG-M1-eaa632c4fe [CANONICAL_ONLY] Add a dependency only for a concrete current requirement; no hypothetical future use.
- NAMED replica/M1/constraints.jsonl/EXTRA-M1-0028 -> FG-M1-9069e49693 [EXTRA_PRODUCT] Logs are not used as an audit database without a dedicated audit design.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0109 -> FG-M1-6ac2f1cab7 [NON_NORMATIVE] The Serilog bootstrap sample logs a fatal startup exception without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0110 -> FG-M1-b225d90bca [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks for Elasticsearch.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0111 -> FG-M1-f4d4f40a5e [MIXED] Prefer platform trace identifiers; add an explicit correlation identifier only when required; validate or normalize an externally accepted identifier before propagating it; propaga

## CIS-M1-U0040 (pass 3) M1 .claude/skills/logging/references/serilog.md:273-273  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For production log storage, prefer Seq, Elasticsearch with the Elastic sink, or an OTLP backend.
TRIGGER: choosing production log storage | EXC: Nonexclusive recommendation; sinks and tooling not baseline dependencies, configure only project needs. No mandatory audit adoption, SDK ban or independently verified library runtime behavior inferred | POL: []
CODEX WHY: Optional tooling may still express a separately registrable preference; technique-only ownership and broad policy subsumption leave normativity unresolved.
```
 270  | Serilog as provider | `AddSerilog()` + configuration |
 271  | General application logging API | `ILogger<T>` (logging skill) |
 272  | Log storage (development) | Seq (free single-user) or Aspire Dashboard |
 273> | Log storage (production) | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 274  | Request logging | `UseSerilogRequestLogging()` |
 275  | Scoped properties | `LogContext.PushProperty()` in middleware |
 276  | Log filtering | `Serilog.Expressions` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-b9dabc85e3 [268, 280] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=[]: Use ILogger<T> with structured templates and stable property names; avoid interpolation.
- V2 FG-M1-412a5270d6 [268, 280] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=['DEP-010']: When Serilog is configured use DI-integrated AddSerilog() with environment-aware provider configuration; application code depends on ILogger<T>, not Serilog APIs.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0535 -> FG-M1-5445dc5fa4 [CANONICAL_ONLY] Keep levels, sinks and overrides in appsettings to vary per environment.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0536 -> FG-M1-d73120b7f9 [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0537 -> FG-M1-b45e946d3f [CANONICAL_ONLY] Sinks/enrichers beyond Console are not baseline; configure only what the project needs.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0194 -> FG-M1-19794a2bcd [EXTRA_PRODUCT] Do not use logs as an audit database without a dedicated audit design.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0058 -> FG-M1-412a5270d6 [CANONICAL_ONLY] When Serilog is configured use DI-integrated AddSerilog() with environment-aware provider configuration; application code depends on ILogger<T>, not Serilog APIs.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0059 -> FG-M1-eaa632c4fe [CANONICAL_ONLY] Add a dependency only for a concrete current requirement; no hypothetical future use.
- NAMED replica/M1/constraints.jsonl/EXTRA-M1-0028 -> FG-M1-9069e49693 [EXTRA_PRODUCT] Logs are not used as an audit database without a dedicated audit design.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0109 -> FG-M1-6ac2f1cab7 [NON_NORMATIVE] The Serilog bootstrap sample logs a fatal startup exception without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0110 -> FG-M1-b225d90bca [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks for Elasticsearch.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0111 -> FG-M1-f4d4f40a5e [MIXED] Prefer platform trace identifiers; add an explicit correlation identifier only when required; validate or normalize an externally accepted identifier before propagating it; propaga

## CIS-M1-U0041 (pass 3) M1 .claude/skills/logging/references/serilog.md:274-274  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For Serilog request logging, prefer UseSerilogRequestLogging().
TRIGGER: implementing request logging with Serilog | EXC: Nonexclusive recommendation; sinks and tooling not baseline dependencies, configure only project needs. No mandatory audit adoption, SDK ban or independently verified library runtime behavior inferred | POL: []
CODEX WHY: Optional tooling may still express a separately registrable preference; technique-only ownership and broad policy subsumption leave normativity unresolved.
```
 271  | General application logging API | `ILogger<T>` (logging skill) |
 272  | Log storage (development) | Seq (free single-user) or Aspire Dashboard |
 273  | Log storage (production) | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 274> | Request logging | `UseSerilogRequestLogging()` |
 275  | Scoped properties | `LogContext.PushProperty()` in middleware |
 276  | Log filtering | `Serilog.Expressions` |
 277  | High-performance paths | `[LoggerMessage]` source generator |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-b9dabc85e3 [268, 280] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=[]: Use ILogger<T> with structured templates and stable property names; avoid interpolation.
- V2 FG-M1-412a5270d6 [268, 280] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=['DEP-010']: When Serilog is configured use DI-integrated AddSerilog() with environment-aware provider configuration; application code depends on ILogger<T>, not Serilog APIs.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0535 -> FG-M1-5445dc5fa4 [CANONICAL_ONLY] Keep levels, sinks and overrides in appsettings to vary per environment.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0536 -> FG-M1-d73120b7f9 [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0537 -> FG-M1-b45e946d3f [CANONICAL_ONLY] Sinks/enrichers beyond Console are not baseline; configure only what the project needs.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0194 -> FG-M1-19794a2bcd [EXTRA_PRODUCT] Do not use logs as an audit database without a dedicated audit design.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0058 -> FG-M1-412a5270d6 [CANONICAL_ONLY] When Serilog is configured use DI-integrated AddSerilog() with environment-aware provider configuration; application code depends on ILogger<T>, not Serilog APIs.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0059 -> FG-M1-eaa632c4fe [CANONICAL_ONLY] Add a dependency only for a concrete current requirement; no hypothetical future use.
- NAMED replica/M1/constraints.jsonl/EXTRA-M1-0028 -> FG-M1-9069e49693 [EXTRA_PRODUCT] Logs are not used as an audit database without a dedicated audit design.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0109 -> FG-M1-6ac2f1cab7 [NON_NORMATIVE] The Serilog bootstrap sample logs a fatal startup exception without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0110 -> FG-M1-b225d90bca [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks for Elasticsearch.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0111 -> FG-M1-f4d4f40a5e [MIXED] Prefer platform trace identifiers; add an explicit correlation identifier only when required; validate or normalize an externally accepted identifier before propagating it; propaga

## CIS-M1-U0042 (pass 3) M1 .claude/skills/logging/references/serilog.md:275-275  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For scoped Serilog properties, prefer LogContext.PushProperty() in middleware.
TRIGGER: adding provider-specific scoped properties | EXC: Nonexclusive recommendation; sinks and tooling not baseline dependencies, configure only project needs. No mandatory audit adoption, SDK ban or independently verified library runtime behavior inferred | POL: []
CODEX WHY: Optional tooling may still express a separately registrable preference; technique-only ownership and broad policy subsumption leave normativity unresolved.
```
 272  | Log storage (development) | Seq (free single-user) or Aspire Dashboard |
 273  | Log storage (production) | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 274  | Request logging | `UseSerilogRequestLogging()` |
 275> | Scoped properties | `LogContext.PushProperty()` in middleware |
 276  | Log filtering | `Serilog.Expressions` |
 277  | High-performance paths | `[LoggerMessage]` source generator |
 278  | Audit trails | `AuditTo` (synchronous, exceptions propagate) |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-b9dabc85e3 [268, 280] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=[]: Use ILogger<T> with structured templates and stable property names; avoid interpolation.
- V2 FG-M1-412a5270d6 [268, 280] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=['DEP-010']: When Serilog is configured use DI-integrated AddSerilog() with environment-aware provider configuration; application code depends on ILogger<T>, not Serilog APIs.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0535 -> FG-M1-5445dc5fa4 [CANONICAL_ONLY] Keep levels, sinks and overrides in appsettings to vary per environment.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0536 -> FG-M1-d73120b7f9 [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0537 -> FG-M1-b45e946d3f [CANONICAL_ONLY] Sinks/enrichers beyond Console are not baseline; configure only what the project needs.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0194 -> FG-M1-19794a2bcd [EXTRA_PRODUCT] Do not use logs as an audit database without a dedicated audit design.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0058 -> FG-M1-412a5270d6 [CANONICAL_ONLY] When Serilog is configured use DI-integrated AddSerilog() with environment-aware provider configuration; application code depends on ILogger<T>, not Serilog APIs.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0059 -> FG-M1-eaa632c4fe [CANONICAL_ONLY] Add a dependency only for a concrete current requirement; no hypothetical future use.
- NAMED replica/M1/constraints.jsonl/EXTRA-M1-0028 -> FG-M1-9069e49693 [EXTRA_PRODUCT] Logs are not used as an audit database without a dedicated audit design.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0109 -> FG-M1-6ac2f1cab7 [NON_NORMATIVE] The Serilog bootstrap sample logs a fatal startup exception without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0110 -> FG-M1-b225d90bca [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks for Elasticsearch.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0111 -> FG-M1-f4d4f40a5e [MIXED] Prefer platform trace identifiers; add an explicit correlation identifier only when required; validate or normalize an externally accepted identifier before propagating it; propaga

## CIS-M1-U0043 (pass 3) M1 .claude/skills/logging/references/serilog.md:276-276  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For Serilog log filtering, prefer Serilog.Expressions.
TRIGGER: choosing a log-filtering mechanism | EXC: Nonexclusive recommendation; sinks and tooling not baseline dependencies, configure only project needs. No mandatory audit adoption, SDK ban or independently verified library runtime behavior inferred | POL: []
CODEX WHY: Optional tooling may still express a separately registrable preference; technique-only ownership and broad policy subsumption leave normativity unresolved.
```
 273  | Log storage (production) | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 274  | Request logging | `UseSerilogRequestLogging()` |
 275  | Scoped properties | `LogContext.PushProperty()` in middleware |
 276> | Log filtering | `Serilog.Expressions` |
 277  | High-performance paths | `[LoggerMessage]` source generator |
 278  | Audit trails | `AuditTo` (synchronous, exceptions propagate) |
 279  | Log levels by environment | `MinimumLevel.Override` per namespace in appsettings |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-b9dabc85e3 [268, 280] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=[]: Use ILogger<T> with structured templates and stable property names; avoid interpolation.
- V2 FG-M1-412a5270d6 [268, 280] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=['DEP-010']: When Serilog is configured use DI-integrated AddSerilog() with environment-aware provider configuration; application code depends on ILogger<T>, not Serilog APIs.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0535 -> FG-M1-5445dc5fa4 [CANONICAL_ONLY] Keep levels, sinks and overrides in appsettings to vary per environment.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0536 -> FG-M1-d73120b7f9 [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0537 -> FG-M1-b45e946d3f [CANONICAL_ONLY] Sinks/enrichers beyond Console are not baseline; configure only what the project needs.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0194 -> FG-M1-19794a2bcd [EXTRA_PRODUCT] Do not use logs as an audit database without a dedicated audit design.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0058 -> FG-M1-412a5270d6 [CANONICAL_ONLY] When Serilog is configured use DI-integrated AddSerilog() with environment-aware provider configuration; application code depends on ILogger<T>, not Serilog APIs.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0059 -> FG-M1-eaa632c4fe [CANONICAL_ONLY] Add a dependency only for a concrete current requirement; no hypothetical future use.
- NAMED replica/M1/constraints.jsonl/EXTRA-M1-0028 -> FG-M1-9069e49693 [EXTRA_PRODUCT] Logs are not used as an audit database without a dedicated audit design.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0109 -> FG-M1-6ac2f1cab7 [NON_NORMATIVE] The Serilog bootstrap sample logs a fatal startup exception without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0110 -> FG-M1-b225d90bca [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks for Elasticsearch.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0111 -> FG-M1-f4d4f40a5e [MIXED] Prefer platform trace identifiers; add an explicit correlation identifier only when required; validate or normalize an externally accepted identifier before propagating it; propaga

## CIS-M1-U0044 (pass 3) M1 .claude/skills/logging/references/serilog.md:278-278  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For an adopted audit-trail need, consider AuditTo, described as synchronous with propagated exceptions.
TRIGGER: choosing a mechanism within a dedicated audit design | EXC: Nonexclusive recommendation; sinks and tooling not baseline dependencies, configure only project needs. No mandatory audit adoption, SDK ban or independently verified library runtime behavior inferred | POL: []
CODEX WHY: Optional tooling may still express a separately registrable preference; technique-only ownership and broad policy subsumption leave normativity unresolved.
```
 275  | Scoped properties | `LogContext.PushProperty()` in middleware |
 276  | Log filtering | `Serilog.Expressions` |
 277  | High-performance paths | `[LoggerMessage]` source generator |
 278> | Audit trails | `AuditTo` (synchronous, exceptions propagate) |
 279  | Log levels by environment | `MinimumLevel.Override` per namespace in appsettings |
 280  | OpenTelemetry integration | `Serilog.Sinks.OpenTelemetry` (no SDK dependency) |
 281  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-b9dabc85e3 [268, 280] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=[]: Use ILogger<T> with structured templates and stable property names; avoid interpolation.
- V2 FG-M1-412a5270d6 [268, 280] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=['DEP-010']: When Serilog is configured use DI-integrated AddSerilog() with environment-aware provider configuration; application code depends on ILogger<T>, not Serilog APIs.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0535 -> FG-M1-5445dc5fa4 [CANONICAL_ONLY] Keep levels, sinks and overrides in appsettings to vary per environment.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0536 -> FG-M1-d73120b7f9 [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0537 -> FG-M1-b45e946d3f [CANONICAL_ONLY] Sinks/enrichers beyond Console are not baseline; configure only what the project needs.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0194 -> FG-M1-19794a2bcd [EXTRA_PRODUCT] Do not use logs as an audit database without a dedicated audit design.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0058 -> FG-M1-412a5270d6 [CANONICAL_ONLY] When Serilog is configured use DI-integrated AddSerilog() with environment-aware provider configuration; application code depends on ILogger<T>, not Serilog APIs.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0059 -> FG-M1-eaa632c4fe [CANONICAL_ONLY] Add a dependency only for a concrete current requirement; no hypothetical future use.
- NAMED replica/M1/constraints.jsonl/EXTRA-M1-0028 -> FG-M1-9069e49693 [EXTRA_PRODUCT] Logs are not used as an audit database without a dedicated audit design.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0109 -> FG-M1-6ac2f1cab7 [NON_NORMATIVE] The Serilog bootstrap sample logs a fatal startup exception without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0110 -> FG-M1-b225d90bca [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks for Elasticsearch.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0111 -> FG-M1-f4d4f40a5e [MIXED] Prefer platform trace identifiers; add an explicit correlation identifier only when required; validate or normalize an externally accepted identifier before propagating it; propaga

## CIS-M1-U0045 (pass 3) M1 .claude/skills/logging/references/serilog.md:279-279  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For log levels by environment, prefer MinimumLevel.Override per namespace in appsettings.
TRIGGER: configuring environment-specific logging levels | EXC: Nonexclusive recommendation; sinks and tooling not baseline dependencies, configure only project needs. No mandatory audit adoption, SDK ban or independently verified library runtime behavior inferred | POL: []
CODEX WHY: Optional tooling may still express a separately registrable preference; technique-only ownership and broad policy subsumption leave normativity unresolved.
```
 276  | Log filtering | `Serilog.Expressions` |
 277  | High-performance paths | `[LoggerMessage]` source generator |
 278  | Audit trails | `AuditTo` (synchronous, exceptions propagate) |
 279> | Log levels by environment | `MinimumLevel.Override` per namespace in appsettings |
 280  | OpenTelemetry integration | `Serilog.Sinks.OpenTelemetry` (no SDK dependency) |
 281  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-b9dabc85e3 [268, 280] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=[]: Use ILogger<T> with structured templates and stable property names; avoid interpolation.
- V2 FG-M1-412a5270d6 [268, 280] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=['DEP-010']: When Serilog is configured use DI-integrated AddSerilog() with environment-aware provider configuration; application code depends on ILogger<T>, not Serilog APIs.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0535 -> FG-M1-5445dc5fa4 [CANONICAL_ONLY] Keep levels, sinks and overrides in appsettings to vary per environment.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0536 -> FG-M1-d73120b7f9 [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0537 -> FG-M1-b45e946d3f [CANONICAL_ONLY] Sinks/enrichers beyond Console are not baseline; configure only what the project needs.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0194 -> FG-M1-19794a2bcd [EXTRA_PRODUCT] Do not use logs as an audit database without a dedicated audit design.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0058 -> FG-M1-412a5270d6 [CANONICAL_ONLY] When Serilog is configured use DI-integrated AddSerilog() with environment-aware provider configuration; application code depends on ILogger<T>, not Serilog APIs.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0059 -> FG-M1-eaa632c4fe [CANONICAL_ONLY] Add a dependency only for a concrete current requirement; no hypothetical future use.
- NAMED replica/M1/constraints.jsonl/EXTRA-M1-0028 -> FG-M1-9069e49693 [EXTRA_PRODUCT] Logs are not used as an audit database without a dedicated audit design.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0109 -> FG-M1-6ac2f1cab7 [NON_NORMATIVE] The Serilog bootstrap sample logs a fatal startup exception without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0110 -> FG-M1-b225d90bca [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks for Elasticsearch.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0111 -> FG-M1-f4d4f40a5e [MIXED] Prefer platform trace identifiers; add an explicit correlation identifier only when required; validate or normalize an externally accepted identifier before propagating it; propaga

## CIS-M1-U0046 (pass 3) M1 .claude/skills/logging/references/serilog.md:280-280  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For Serilog OpenTelemetry integration, prefer Serilog.Sinks.OpenTelemetry without an SDK dependency.
TRIGGER: choosing an already-needed OpenTelemetry logging integration | EXC: Nonexclusive recommendation; sinks and tooling not baseline dependencies, configure only project needs. No mandatory audit adoption, SDK ban or independently verified library runtime behavior inferred | POL: []
CODEX WHY: Optional tooling may still express a separately registrable preference; technique-only ownership and broad policy subsumption leave normativity unresolved.
```
 277  | High-performance paths | `[LoggerMessage]` source generator |
 278  | Audit trails | `AuditTo` (synchronous, exceptions propagate) |
 279  | Log levels by environment | `MinimumLevel.Override` per namespace in appsettings |
 280> | OpenTelemetry integration | `Serilog.Sinks.OpenTelemetry` (no SDK dependency) |
 281  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-b9dabc85e3 [268, 280] CANONICAL_ONLY/DEFAULT pol=['RUN-013'] rel=[]: Use ILogger<T> with structured templates and stable property names; avoid interpolation.
- V2 FG-M1-412a5270d6 [268, 280] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=['DEP-010']: When Serilog is configured use DI-integrated AddSerilog() with environment-aware provider configuration; application code depends on ILogger<T>, not Serilog APIs.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0535 -> FG-M1-5445dc5fa4 [CANONICAL_ONLY] Keep levels, sinks and overrides in appsettings to vary per environment.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0536 -> FG-M1-d73120b7f9 [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0537 -> FG-M1-b45e946d3f [CANONICAL_ONLY] Sinks/enrichers beyond Console are not baseline; configure only what the project needs.
- NAMED primary/M1/constraints.jsonl/EXTRA-M1-0194 -> FG-M1-19794a2bcd [EXTRA_PRODUCT] Do not use logs as an audit database without a dedicated audit design.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0058 -> FG-M1-412a5270d6 [CANONICAL_ONLY] When Serilog is configured use DI-integrated AddSerilog() with environment-aware provider configuration; application code depends on ILogger<T>, not Serilog APIs.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0059 -> FG-M1-eaa632c4fe [CANONICAL_ONLY] Add a dependency only for a concrete current requirement; no hypothetical future use.
- NAMED replica/M1/constraints.jsonl/EXTRA-M1-0028 -> FG-M1-9069e49693 [EXTRA_PRODUCT] Logs are not used as an audit database without a dedicated audit design.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0109 -> FG-M1-6ac2f1cab7 [NON_NORMATIVE] The Serilog bootstrap sample logs a fatal startup exception without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0110 -> FG-M1-b225d90bca [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks for Elasticsearch.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0111 -> FG-M1-f4d4f40a5e [MIXED] Prefer platform trace identifiers; add an explicit correlation identifier only when required; validate or normalize an externally accepted identifier before propagating it; propaga

## CIS-L0-U0040 (pass 3) L0 .claude/skills/logging/references/serilog.md:149-149  [MAY UNCERTAIN_NOVELTY]
CLAIM: Audit trails that must not lose events may use AuditTo; the source describes it as synchronous with propagating exceptions.
TRIGGER: Choosing delivery for an adopted audit design requiring event retention. | EXC: Optional technique; no mandatory audit subsystem, sink adoption or exclusive context API inferred. Audit use requires adopted design; runtime library semantics are described by the source, not indepen | POL: ['RUN-013']
CODEX WHY: Source-grounded optional recommendation/permission could guide an independent choice, but may be only implementation technique or already implicit in broad logging policy.
```
 146      opts.DataStream = new DataStreamName("logs", "myapp"))
 147  ```
 148  
 149> Audit trails that must not lose events can use `AuditTo` (synchronous; exceptions propagate).
 150  
 151  ## Decision guide
 152  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L0/constraints.jsonl/RULE-L0-0471 -> FG-L0-c65b6e6c48 [CANONICAL_ONLY] Keep log property names stable so logs remain queryable.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0479 -> FG-L0-8c9ca73b13 [CANONICAL_ONLY] Keep Log.Logger and LogContext at composition/provider-specific boundaries (application code on ILogger<T>).
- NAMED primary/L0/constraints.jsonl/EXTRA-L0-0146 -> FG-L0-dbc44960e4 [EXTRA_PRODUCT] Do not use logs as an audit database without an adopted audit design.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0143 -> FG-L0-b81cf21323 [CANONICAL_ONLY] ILogger<T> with structured templates and stable property names; avoid interpolation that flattens values.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0144 -> FG-L0-9f57cdb5cf [CANONICAL_ONLY] With Serilog use builder.Services.AddSerilog(...) (not UseSerilog()); levels/sinks/overrides in environment-aware configuration; application code depends on ILogger<T>.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0094 -> FG-L0-78c1bb0108 [CANONICAL_ONLY] Normal structured logging suffices; use source-generated logging only on a measured high-volume path, not everywhere to avoid theoretical allocations.

## CIS-L0-U0023 (pass 2) L0 .claude/skills/logging/references/serilog.md:156-156  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For Development log storage, the Serilog decision guide lists Seq or the Aspire Dashboard.
TRIGGER: Selecting Development log storage. | EXC: The reference calls itself technique; additional sinks are optional and require need. Listed alternatives are not proven exhaustive or mandatory; application code remains on ILogger. | POL: ['DEP-021']
CODEX WHY: A named scenario choice can affect implementation independently of the generic provider policy. The technique-only parent and explicitly optional sinks strongly support a nonexclusive illustrative reading. Preserve for adjudication rather than treating a table as automatically normative. Scoped-property selection is distinct from existing U0009 enrichment prerequisite.
```
 153  | Scenario | Technique |
 154  |---|---|
 155  | Serilog as provider | `AddSerilog()` + configuration |
 156> | Development log storage | Seq or the Aspire Dashboard |
 157  | Production log storage | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 158  | Request logging | `UseSerilogRequestLogging()` |
 159  | Scoped properties | `LogContext.PushProperty()` in middleware |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L0/constraints.jsonl/RULE-L0-0202 -> FG-L0-9f57cdb5cf [CANONICAL_ONLY] With Serilog use builder.Services.AddSerilog(...) (not UseSerilog()); levels/sinks/overrides in environment-aware configuration; application code depends on ILogger<T>.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0478 -> FG-L0-29f3ddfea3 [CANONICAL_ONLY] File, Seq, OpenTelemetry and Elasticsearch sinks are optional, not baseline dependencies.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0479 -> FG-L0-8c9ca73b13 [CANONICAL_ONLY] Keep Log.Logger and LogContext at composition/provider-specific boundaries (application code on ILogger<T>).
- NAMED primary/L0/constraints.jsonl/RULE-L0-0053 -> FG-L0-a98496bce4 [CANONICAL_ONLY] Add Serilog sinks only when required (Console is enough locally).
- NAMED replica/L0/constraints.jsonl/RULE-L0-0144 -> FG-L0-9f57cdb5cf [CANONICAL_ONLY] With Serilog use builder.Services.AddSerilog(...) (not UseSerilog()); levels/sinks/overrides in environment-aware configuration; application code depends on ILogger<T>.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0092 -> FG-L0-293fcb0abe [NON_NORMATIVE] The Serilog bootstrap example logs a fatal startup failure without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0093 -> FG-L0-e8e7ecedc4 [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.

## CIS-L0-U0024 (pass 2) L0 .claude/skills/logging/references/serilog.md:157-157  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For Production log storage, the Serilog decision guide lists Seq, Elasticsearch with the Elastic sink, or an OTLP backend.
TRIGGER: Selecting Production log storage. | EXC: The reference calls itself technique; additional sinks are optional and require need. Listed alternatives are not proven exhaustive or mandatory; application code remains on ILogger. | POL: ['DEP-021']
CODEX WHY: A named scenario choice can affect implementation independently of the generic provider policy. The technique-only parent and explicitly optional sinks strongly support a nonexclusive illustrative reading. Preserve for adjudication rather than treating a table as automatically normative. Scoped-property selection is distinct from existing U0009 enrichment prerequisite.
```
 154  |---|---|
 155  | Serilog as provider | `AddSerilog()` + configuration |
 156  | Development log storage | Seq or the Aspire Dashboard |
 157> | Production log storage | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 158  | Request logging | `UseSerilogRequestLogging()` |
 159  | Scoped properties | `LogContext.PushProperty()` in middleware |
 160  | Level per environment | `MinimumLevel.Override` in appsettings |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L0/constraints.jsonl/RULE-L0-0202 -> FG-L0-9f57cdb5cf [CANONICAL_ONLY] With Serilog use builder.Services.AddSerilog(...) (not UseSerilog()); levels/sinks/overrides in environment-aware configuration; application code depends on ILogger<T>.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0478 -> FG-L0-29f3ddfea3 [CANONICAL_ONLY] File, Seq, OpenTelemetry and Elasticsearch sinks are optional, not baseline dependencies.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0479 -> FG-L0-8c9ca73b13 [CANONICAL_ONLY] Keep Log.Logger and LogContext at composition/provider-specific boundaries (application code on ILogger<T>).
- NAMED primary/L0/constraints.jsonl/RULE-L0-0053 -> FG-L0-a98496bce4 [CANONICAL_ONLY] Add Serilog sinks only when required (Console is enough locally).
- NAMED replica/L0/constraints.jsonl/RULE-L0-0144 -> FG-L0-9f57cdb5cf [CANONICAL_ONLY] With Serilog use builder.Services.AddSerilog(...) (not UseSerilog()); levels/sinks/overrides in environment-aware configuration; application code depends on ILogger<T>.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0092 -> FG-L0-293fcb0abe [NON_NORMATIVE] The Serilog bootstrap example logs a fatal startup failure without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0093 -> FG-L0-e8e7ecedc4 [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.

## CIS-L0-U0025 (pass 2) L0 .claude/skills/logging/references/serilog.md:158-158  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For request logging, the Serilog decision guide selects UseSerilogRequestLogging().
TRIGGER: Choosing a Serilog request-logging technique. | EXC: The reference calls itself technique; additional sinks are optional and require need. Listed alternatives are not proven exhaustive or mandatory; application code remains on ILogger. | POL: ['DEP-021']
CODEX WHY: A named scenario choice can affect implementation independently of the generic provider policy. The technique-only parent and explicitly optional sinks strongly support a nonexclusive illustrative reading. Preserve for adjudication rather than treating a table as automatically normative. Scoped-property selection is distinct from existing U0009 enrichment prerequisite.
```
 155  | Serilog as provider | `AddSerilog()` + configuration |
 156  | Development log storage | Seq or the Aspire Dashboard |
 157  | Production log storage | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 158> | Request logging | `UseSerilogRequestLogging()` |
 159  | Scoped properties | `LogContext.PushProperty()` in middleware |
 160  | Level per environment | `MinimumLevel.Override` in appsettings |
 161  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L0/constraints.jsonl/RULE-L0-0202 -> FG-L0-9f57cdb5cf [CANONICAL_ONLY] With Serilog use builder.Services.AddSerilog(...) (not UseSerilog()); levels/sinks/overrides in environment-aware configuration; application code depends on ILogger<T>.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0478 -> FG-L0-29f3ddfea3 [CANONICAL_ONLY] File, Seq, OpenTelemetry and Elasticsearch sinks are optional, not baseline dependencies.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0479 -> FG-L0-8c9ca73b13 [CANONICAL_ONLY] Keep Log.Logger and LogContext at composition/provider-specific boundaries (application code on ILogger<T>).
- NAMED primary/L0/constraints.jsonl/RULE-L0-0053 -> FG-L0-a98496bce4 [CANONICAL_ONLY] Add Serilog sinks only when required (Console is enough locally).
- NAMED replica/L0/constraints.jsonl/RULE-L0-0144 -> FG-L0-9f57cdb5cf [CANONICAL_ONLY] With Serilog use builder.Services.AddSerilog(...) (not UseSerilog()); levels/sinks/overrides in environment-aware configuration; application code depends on ILogger<T>.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0092 -> FG-L0-293fcb0abe [NON_NORMATIVE] The Serilog bootstrap example logs a fatal startup failure without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0093 -> FG-L0-e8e7ecedc4 [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.

## CIS-L0-U0026 (pass 2) L0 .claude/skills/logging/references/serilog.md:159-159  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For scoped properties, the Serilog decision guide selects LogContext.PushProperty() in middleware.
TRIGGER: Adding scoped properties at a Serilog provider boundary. | EXC: The reference calls itself technique; additional sinks are optional and require need. Listed alternatives are not proven exhaustive or mandatory; application code remains on ILogger. | POL: ['DEP-021']
CODEX WHY: A named scenario choice can affect implementation independently of the generic provider policy. The technique-only parent and explicitly optional sinks strongly support a nonexclusive illustrative reading. Preserve for adjudication rather than treating a table as automatically normative. Scoped-property selection is distinct from existing U0009 enrichment prerequisite.
```
 156  | Development log storage | Seq or the Aspire Dashboard |
 157  | Production log storage | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 158  | Request logging | `UseSerilogRequestLogging()` |
 159> | Scoped properties | `LogContext.PushProperty()` in middleware |
 160  | Level per environment | `MinimumLevel.Override` in appsettings |
 161  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L0/constraints.jsonl/RULE-L0-0202 -> FG-L0-9f57cdb5cf [CANONICAL_ONLY] With Serilog use builder.Services.AddSerilog(...) (not UseSerilog()); levels/sinks/overrides in environment-aware configuration; application code depends on ILogger<T>.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0478 -> FG-L0-29f3ddfea3 [CANONICAL_ONLY] File, Seq, OpenTelemetry and Elasticsearch sinks are optional, not baseline dependencies.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0479 -> FG-L0-8c9ca73b13 [CANONICAL_ONLY] Keep Log.Logger and LogContext at composition/provider-specific boundaries (application code on ILogger<T>).
- NAMED primary/L0/constraints.jsonl/RULE-L0-0053 -> FG-L0-a98496bce4 [CANONICAL_ONLY] Add Serilog sinks only when required (Console is enough locally).
- NAMED replica/L0/constraints.jsonl/RULE-L0-0144 -> FG-L0-9f57cdb5cf [CANONICAL_ONLY] With Serilog use builder.Services.AddSerilog(...) (not UseSerilog()); levels/sinks/overrides in environment-aware configuration; application code depends on ILogger<T>.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0092 -> FG-L0-293fcb0abe [NON_NORMATIVE] The Serilog bootstrap example logs a fatal startup failure without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0093 -> FG-L0-e8e7ecedc4 [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.

## CIS-L0-U0027 (pass 2) L0 .claude/skills/logging/references/serilog.md:160-160  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For per-environment levels, the Serilog decision guide selects MinimumLevel.Override in appsettings.
TRIGGER: Configuring per-environment Serilog log levels. | EXC: The reference calls itself technique; additional sinks are optional and require need. Listed alternatives are not proven exhaustive or mandatory; application code remains on ILogger. | POL: ['DEP-021']
CODEX WHY: A named scenario choice can affect implementation independently of the generic provider policy. The technique-only parent and explicitly optional sinks strongly support a nonexclusive illustrative reading. Preserve for adjudication rather than treating a table as automatically normative. Scoped-property selection is distinct from existing U0009 enrichment prerequisite.
```
 157  | Production log storage | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 158  | Request logging | `UseSerilogRequestLogging()` |
 159  | Scoped properties | `LogContext.PushProperty()` in middleware |
 160> | Level per environment | `MinimumLevel.Override` in appsettings |
 161  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L0/constraints.jsonl/RULE-L0-0202 -> FG-L0-9f57cdb5cf [CANONICAL_ONLY] With Serilog use builder.Services.AddSerilog(...) (not UseSerilog()); levels/sinks/overrides in environment-aware configuration; application code depends on ILogger<T>.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0478 -> FG-L0-29f3ddfea3 [CANONICAL_ONLY] File, Seq, OpenTelemetry and Elasticsearch sinks are optional, not baseline dependencies.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0479 -> FG-L0-8c9ca73b13 [CANONICAL_ONLY] Keep Log.Logger and LogContext at composition/provider-specific boundaries (application code on ILogger<T>).
- NAMED primary/L0/constraints.jsonl/RULE-L0-0053 -> FG-L0-a98496bce4 [CANONICAL_ONLY] Add Serilog sinks only when required (Console is enough locally).
- NAMED replica/L0/constraints.jsonl/RULE-L0-0144 -> FG-L0-9f57cdb5cf [CANONICAL_ONLY] With Serilog use builder.Services.AddSerilog(...) (not UseSerilog()); levels/sinks/overrides in environment-aware configuration; application code depends on ILogger<T>.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0092 -> FG-L0-293fcb0abe [NON_NORMATIVE] The Serilog bootstrap example logs a fatal startup failure without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0093 -> FG-L0-e8e7ecedc4 [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.

## CIS-L1-U0035 (pass 3) L1 .claude/skills/logging/references/serilog.md:95-95  [MAY UNCERTAIN_NOVELTY]
CLAIM: OTLP export may use Serilog.Sinks.OpenTelemetry without the OpenTelemetry SDK.
TRIGGER: Applicable logging scenario and selected provider; no automatic infrastructure adoption | EXC: Table header Option (except skill Default); only needed sinks/enrichers; direct Serilog at provider boundaries. AuditTo parenthetical describes synchronous/exception propagation but no runtime proof a | POL: []
CODEX WHY: Specific scenario/API choice differs from generic logging policy, existing U0015 prerequisite, and adoption permission. Whether available options create normative constraints remains open.
```
  92  
  93  ## Sinks to avoid
  94  
  95> The `Serilog.Sinks.Elasticsearch` package is deprecated; use `Elastic.Serilog.Sinks` when Elasticsearch is the chosen log store. OTLP export is available through `Serilog.Sinks.OpenTelemetry` without the OpenTeleme
  96  
  97  ## Decision guide
  98  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L1-2773711466 [95, 95] CANONICAL_PLUS_DELTA/MUST_NOT pol=['DEP-020', 'DEP-004', 'DEP-010'] rel=[]: Packages Microsoft.Extensions.Http.Polly, Polly.Extensions.Http (deprecated resilience integrations), FluentValidation.AspNetCore (deprecated automatic-validation integration) and Serilog.Sinks.Elasticsearch (deprecated sink) must
- V2 FG-L1-148957dd5b [95, 95] CANONICAL_PLUS_DELTA/DEFAULT pol=['DEP-004'] rel=['DEP-021']: Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED primary/L1/constraints.jsonl/RULE-L1-0498 -> FG-L1-e6779ead4c [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries (application code on ILogger<T>).
- NAMED primary/L1/constraints.jsonl/RULE-L1-0499 -> FG-L1-d8a716f67f [CANONICAL_ONLY] Configure only sinks and enrichers the project needs; Console is enough locally; File/Seq/OpenTelemetry/Elasticsearch are options, not baseline dependencies.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0181 -> FG-L1-c936a0d93d [EXTRA_PRODUCT] Do not use logs as an audit database without an adopted audit design.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0184 -> FG-L1-148957dd5b [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0143 -> FG-L1-36e12d0f5b [CANONICAL_ONLY] With Serilog use DI-integrated AddSerilog with environment-aware configuration; application code depends on ILogger<T>.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0127 -> FG-L1-d6ccf61e2f [NON_NORMATIVE] The Serilog bootstrap example logs a fatal startup failure without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0128 -> FG-L1-148957dd5b [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0129 -> FG-L1-6a59d2372c [CANONICAL_ONLY] Validate or normalize correlation ids accepted from clients.

## CIS-L1-U0028 (pass 3) L1 .claude/skills/logging/references/serilog.md:102-102  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: Consider Seq or the Aspire Dashboard for local log storage when needed.
TRIGGER: Applicable logging scenario and selected provider; no automatic infrastructure adoption | EXC: Table header Option (except skill Default); only needed sinks/enrichers; direct Serilog at provider boundaries. AuditTo parenthetical describes synchronous/exception propagation but no runtime proof a | POL: []
CODEX WHY: Specific scenario/API choice differs from generic logging policy, existing U0015 prerequisite, and adoption permission. Whether available options create normative constraints remains open.
```
  99  | Scenario | Option |
 100  | --- | --- |
 101  | Provider setup | `AddSerilog()` + configuration |
 102> | Local log storage when needed | Seq (free single-user) or the Aspire Dashboard |
 103  | Production log storage | Seq, Elasticsearch (`Elastic.Serilog.Sinks`), or an OTLP backend |
 104  | Request logging | `UseSerilogRequestLogging()` |
 105  | Scoped properties | `LogContext.PushProperty()` in middleware |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L1/constraints.jsonl/RULE-L1-0498 -> FG-L1-e6779ead4c [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries (application code on ILogger<T>).
- NAMED primary/L1/constraints.jsonl/RULE-L1-0499 -> FG-L1-d8a716f67f [CANONICAL_ONLY] Configure only sinks and enrichers the project needs; Console is enough locally; File/Seq/OpenTelemetry/Elasticsearch are options, not baseline dependencies.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0181 -> FG-L1-c936a0d93d [EXTRA_PRODUCT] Do not use logs as an audit database without an adopted audit design.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0184 -> FG-L1-148957dd5b [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0143 -> FG-L1-36e12d0f5b [CANONICAL_ONLY] With Serilog use DI-integrated AddSerilog with environment-aware configuration; application code depends on ILogger<T>.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0127 -> FG-L1-d6ccf61e2f [NON_NORMATIVE] The Serilog bootstrap example logs a fatal startup failure without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0128 -> FG-L1-148957dd5b [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0129 -> FG-L1-6a59d2372c [CANONICAL_ONLY] Validate or normalize correlation ids accepted from clients.

## CIS-L1-U0029 (pass 3) L1 .claude/skills/logging/references/serilog.md:103-103  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: Consider Seq, Elasticsearch via Elastic.Serilog.Sinks, or an OTLP backend for production log storage.
TRIGGER: Applicable logging scenario and selected provider; no automatic infrastructure adoption | EXC: Table header Option (except skill Default); only needed sinks/enrichers; direct Serilog at provider boundaries. AuditTo parenthetical describes synchronous/exception propagation but no runtime proof a | POL: []
CODEX WHY: Specific scenario/API choice differs from generic logging policy, existing U0015 prerequisite, and adoption permission. Whether available options create normative constraints remains open.
```
 100  | --- | --- |
 101  | Provider setup | `AddSerilog()` + configuration |
 102  | Local log storage when needed | Seq (free single-user) or the Aspire Dashboard |
 103> | Production log storage | Seq, Elasticsearch (`Elastic.Serilog.Sinks`), or an OTLP backend |
 104  | Request logging | `UseSerilogRequestLogging()` |
 105  | Scoped properties | `LogContext.PushProperty()` in middleware |
 106  | Filtering | `Serilog.Expressions` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L1/constraints.jsonl/RULE-L1-0498 -> FG-L1-e6779ead4c [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries (application code on ILogger<T>).
- NAMED primary/L1/constraints.jsonl/RULE-L1-0499 -> FG-L1-d8a716f67f [CANONICAL_ONLY] Configure only sinks and enrichers the project needs; Console is enough locally; File/Seq/OpenTelemetry/Elasticsearch are options, not baseline dependencies.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0181 -> FG-L1-c936a0d93d [EXTRA_PRODUCT] Do not use logs as an audit database without an adopted audit design.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0184 -> FG-L1-148957dd5b [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0143 -> FG-L1-36e12d0f5b [CANONICAL_ONLY] With Serilog use DI-integrated AddSerilog with environment-aware configuration; application code depends on ILogger<T>.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0127 -> FG-L1-d6ccf61e2f [NON_NORMATIVE] The Serilog bootstrap example logs a fatal startup failure without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0128 -> FG-L1-148957dd5b [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0129 -> FG-L1-6a59d2372c [CANONICAL_ONLY] Validate or normalize correlation ids accepted from clients.

## CIS-L1-U0030 (pass 3) L1 .claude/skills/logging/references/serilog.md:104-104  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: Consider UseSerilogRequestLogging for request logging.
TRIGGER: Applicable logging scenario and selected provider; no automatic infrastructure adoption | EXC: Table header Option (except skill Default); only needed sinks/enrichers; direct Serilog at provider boundaries. AuditTo parenthetical describes synchronous/exception propagation but no runtime proof a | POL: []
CODEX WHY: Specific scenario/API choice differs from generic logging policy, existing U0015 prerequisite, and adoption permission. Whether available options create normative constraints remains open.
```
 101  | Provider setup | `AddSerilog()` + configuration |
 102  | Local log storage when needed | Seq (free single-user) or the Aspire Dashboard |
 103  | Production log storage | Seq, Elasticsearch (`Elastic.Serilog.Sinks`), or an OTLP backend |
 104> | Request logging | `UseSerilogRequestLogging()` |
 105  | Scoped properties | `LogContext.PushProperty()` in middleware |
 106  | Filtering | `Serilog.Expressions` |
 107  | Audit trails (only with an adopted audit design) | `AuditTo` (synchronous; exceptions propagate) |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L1/constraints.jsonl/RULE-L1-0498 -> FG-L1-e6779ead4c [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries (application code on ILogger<T>).
- NAMED primary/L1/constraints.jsonl/RULE-L1-0499 -> FG-L1-d8a716f67f [CANONICAL_ONLY] Configure only sinks and enrichers the project needs; Console is enough locally; File/Seq/OpenTelemetry/Elasticsearch are options, not baseline dependencies.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0181 -> FG-L1-c936a0d93d [EXTRA_PRODUCT] Do not use logs as an audit database without an adopted audit design.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0184 -> FG-L1-148957dd5b [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0143 -> FG-L1-36e12d0f5b [CANONICAL_ONLY] With Serilog use DI-integrated AddSerilog with environment-aware configuration; application code depends on ILogger<T>.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0127 -> FG-L1-d6ccf61e2f [NON_NORMATIVE] The Serilog bootstrap example logs a fatal startup failure without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0128 -> FG-L1-148957dd5b [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0129 -> FG-L1-6a59d2372c [CANONICAL_ONLY] Validate or normalize correlation ids accepted from clients.

## CIS-L1-U0031 (pass 3) L1 .claude/skills/logging/references/serilog.md:105-105  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: Consider LogContext.PushProperty in middleware for scoped Serilog properties.
TRIGGER: Applicable logging scenario and selected provider; no automatic infrastructure adoption | EXC: Table header Option (except skill Default); only needed sinks/enrichers; direct Serilog at provider boundaries. AuditTo parenthetical describes synchronous/exception propagation but no runtime proof a | POL: []
CODEX WHY: Specific scenario/API choice differs from generic logging policy, existing U0015 prerequisite, and adoption permission. Whether available options create normative constraints remains open.
```
 102  | Local log storage when needed | Seq (free single-user) or the Aspire Dashboard |
 103  | Production log storage | Seq, Elasticsearch (`Elastic.Serilog.Sinks`), or an OTLP backend |
 104  | Request logging | `UseSerilogRequestLogging()` |
 105> | Scoped properties | `LogContext.PushProperty()` in middleware |
 106  | Filtering | `Serilog.Expressions` |
 107  | Audit trails (only with an adopted audit design) | `AuditTo` (synchronous; exceptions propagate) |
 108  | Levels per environment | `MinimumLevel.Override` per namespace in configuration |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L1/constraints.jsonl/RULE-L1-0498 -> FG-L1-e6779ead4c [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries (application code on ILogger<T>).
- NAMED primary/L1/constraints.jsonl/RULE-L1-0499 -> FG-L1-d8a716f67f [CANONICAL_ONLY] Configure only sinks and enrichers the project needs; Console is enough locally; File/Seq/OpenTelemetry/Elasticsearch are options, not baseline dependencies.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0181 -> FG-L1-c936a0d93d [EXTRA_PRODUCT] Do not use logs as an audit database without an adopted audit design.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0184 -> FG-L1-148957dd5b [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0143 -> FG-L1-36e12d0f5b [CANONICAL_ONLY] With Serilog use DI-integrated AddSerilog with environment-aware configuration; application code depends on ILogger<T>.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0127 -> FG-L1-d6ccf61e2f [NON_NORMATIVE] The Serilog bootstrap example logs a fatal startup failure without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0128 -> FG-L1-148957dd5b [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0129 -> FG-L1-6a59d2372c [CANONICAL_ONLY] Validate or normalize correlation ids accepted from clients.

## CIS-L1-U0032 (pass 3) L1 .claude/skills/logging/references/serilog.md:106-106  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: Consider Serilog.Expressions for filtering.
TRIGGER: Applicable logging scenario and selected provider; no automatic infrastructure adoption | EXC: Table header Option (except skill Default); only needed sinks/enrichers; direct Serilog at provider boundaries. AuditTo parenthetical describes synchronous/exception propagation but no runtime proof a | POL: []
CODEX WHY: Specific scenario/API choice differs from generic logging policy, existing U0015 prerequisite, and adoption permission. Whether available options create normative constraints remains open.
```
 103  | Production log storage | Seq, Elasticsearch (`Elastic.Serilog.Sinks`), or an OTLP backend |
 104  | Request logging | `UseSerilogRequestLogging()` |
 105  | Scoped properties | `LogContext.PushProperty()` in middleware |
 106> | Filtering | `Serilog.Expressions` |
 107  | Audit trails (only with an adopted audit design) | `AuditTo` (synchronous; exceptions propagate) |
 108  | Levels per environment | `MinimumLevel.Override` per namespace in configuration |
 109  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L1/constraints.jsonl/RULE-L1-0498 -> FG-L1-e6779ead4c [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries (application code on ILogger<T>).
- NAMED primary/L1/constraints.jsonl/RULE-L1-0499 -> FG-L1-d8a716f67f [CANONICAL_ONLY] Configure only sinks and enrichers the project needs; Console is enough locally; File/Seq/OpenTelemetry/Elasticsearch are options, not baseline dependencies.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0181 -> FG-L1-c936a0d93d [EXTRA_PRODUCT] Do not use logs as an audit database without an adopted audit design.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0184 -> FG-L1-148957dd5b [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0143 -> FG-L1-36e12d0f5b [CANONICAL_ONLY] With Serilog use DI-integrated AddSerilog with environment-aware configuration; application code depends on ILogger<T>.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0127 -> FG-L1-d6ccf61e2f [NON_NORMATIVE] The Serilog bootstrap example logs a fatal startup failure without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0128 -> FG-L1-148957dd5b [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0129 -> FG-L1-6a59d2372c [CANONICAL_ONLY] Validate or normalize correlation ids accepted from clients.

## CIS-L1-U0033 (pass 3) L1 .claude/skills/logging/references/serilog.md:107-107  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: Consider AuditTo for audit trails only with an adopted audit design.
TRIGGER: Applicable logging scenario and selected provider; no automatic infrastructure adoption | EXC: Table header Option (except skill Default); only needed sinks/enrichers; direct Serilog at provider boundaries. AuditTo parenthetical describes synchronous/exception propagation but no runtime proof a | POL: []
CODEX WHY: Specific scenario/API choice differs from generic logging policy, existing U0015 prerequisite, and adoption permission. Whether available options create normative constraints remains open.
```
 104  | Request logging | `UseSerilogRequestLogging()` |
 105  | Scoped properties | `LogContext.PushProperty()` in middleware |
 106  | Filtering | `Serilog.Expressions` |
 107> | Audit trails (only with an adopted audit design) | `AuditTo` (synchronous; exceptions propagate) |
 108  | Levels per environment | `MinimumLevel.Override` per namespace in configuration |
 109  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L1/constraints.jsonl/RULE-L1-0498 -> FG-L1-e6779ead4c [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries (application code on ILogger<T>).
- NAMED primary/L1/constraints.jsonl/RULE-L1-0499 -> FG-L1-d8a716f67f [CANONICAL_ONLY] Configure only sinks and enrichers the project needs; Console is enough locally; File/Seq/OpenTelemetry/Elasticsearch are options, not baseline dependencies.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0181 -> FG-L1-c936a0d93d [EXTRA_PRODUCT] Do not use logs as an audit database without an adopted audit design.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0184 -> FG-L1-148957dd5b [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0143 -> FG-L1-36e12d0f5b [CANONICAL_ONLY] With Serilog use DI-integrated AddSerilog with environment-aware configuration; application code depends on ILogger<T>.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0127 -> FG-L1-d6ccf61e2f [NON_NORMATIVE] The Serilog bootstrap example logs a fatal startup failure without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0128 -> FG-L1-148957dd5b [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0129 -> FG-L1-6a59d2372c [CANONICAL_ONLY] Validate or normalize correlation ids accepted from clients.

## CIS-L1-U0034 (pass 3) L1 .claude/skills/logging/references/serilog.md:108-108  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: Consider MinimumLevel.Override per namespace in configuration for levels per environment.
TRIGGER: Applicable logging scenario and selected provider; no automatic infrastructure adoption | EXC: Table header Option (except skill Default); only needed sinks/enrichers; direct Serilog at provider boundaries. AuditTo parenthetical describes synchronous/exception propagation but no runtime proof a | POL: []
CODEX WHY: Specific scenario/API choice differs from generic logging policy, existing U0015 prerequisite, and adoption permission. Whether available options create normative constraints remains open.
```
 105  | Scoped properties | `LogContext.PushProperty()` in middleware |
 106  | Filtering | `Serilog.Expressions` |
 107  | Audit trails (only with an adopted audit design) | `AuditTo` (synchronous; exceptions propagate) |
 108> | Levels per environment | `MinimumLevel.Override` per namespace in configuration |
 109  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L1/constraints.jsonl/RULE-L1-0498 -> FG-L1-e6779ead4c [CANONICAL_ONLY] Keep direct Serilog APIs (Log.Logger, LogContext) at composition or provider-specific boundaries (application code on ILogger<T>).
- NAMED primary/L1/constraints.jsonl/RULE-L1-0499 -> FG-L1-d8a716f67f [CANONICAL_ONLY] Configure only sinks and enrichers the project needs; Console is enough locally; File/Seq/OpenTelemetry/Elasticsearch are options, not baseline dependencies.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0181 -> FG-L1-c936a0d93d [EXTRA_PRODUCT] Do not use logs as an audit database without an adopted audit design.
- NAMED primary/L1/constraints.jsonl/EXTRA-L1-0184 -> FG-L1-148957dd5b [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED replica/L1/constraints.jsonl/RULE-L1-0143 -> FG-L1-36e12d0f5b [CANONICAL_ONLY] With Serilog use DI-integrated AddSerilog with environment-aware configuration; application code depends on ILogger<T>.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0127 -> FG-L1-d6ccf61e2f [NON_NORMATIVE] The Serilog bootstrap example logs a fatal startup failure without rethrowing or setting a failure exit status (reported failure-visibility uncertainty).
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0128 -> FG-L1-148957dd5b [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use Elastic.Serilog.Sinks when Elasticsearch is the chosen store.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0129 -> FG-L1-6a59d2372c [CANONICAL_ONLY] Validate or normalize correlation ids accepted from clients.

## CIS-K0-U0045 (pass 3) K0 .claude/skills/logging/references/serilog.md:174-174  [MAY UNCERTAIN_NOVELTY]
CLAIM: Serilog.Sinks.OpenTelemetry is presented as an OTLP export path without requiring the OpenTelemetry SDK.
TRIGGER: Exporting Serilog events to an OTLP backend under the logging skill or its private reference | EXC: Only for the concrete logging need; sinks are optional. Provider-specific APIs stay at composition/provider boundaries. No global or exclusive requirement inferred. | POL: ['RUN-013', 'DEP-010']
CODEX WHY: Potential independent technique guidance, with uncertainty about descriptive modality and whether the broad independent finding already encompasses it.
```
 171  
 172  ## OpenTelemetry export
 173  
 174> `Serilog.Sinks.OpenTelemetry` exports to any OTLP backend without the OpenTelemetry SDK:
 175  
 176  ```csharp
 177  .WriteTo.OpenTelemetry(options =>
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/K0/constraints.jsonl/RULE-K0-0450 -> FG-K0-458a5e6617 [CANONICAL_ONLY] Application code keeps using ILogger<T>; direct Serilog APIs (Log.Logger, LogContext) stay at composition or provider-specific boundaries.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0452 -> FG-K0-ea63ebf1dc [CANONICAL_ONLY] Keep levels, sinks and overrides in configuration so they can differ per environment.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0190 -> FG-K0-17e2f22e6a [CANONICAL_ONLY] File, Seq and other sinks are not baseline dependencies; a Console sink suffices for a simple local Development baseline; example limits and retention values are illustrative.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0071 -> FG-K0-84d69f4114 [CANONICAL_ONLY] ILogger<T> with structured message templates and stable property names; avoid interpolation that makes structured values opaque.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0072 -> FG-K0-a89cc47d55 [CANONICAL_ONLY] When Serilog is configured use DI-integrated AddSerilog with environment-aware provider configuration; application code depends on ILogger<T>.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0042 -> FG-K0-b967417c39 [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.

## CIS-K0-U0041 (pass 3) K0 .claude/skills/logging/references/serilog.md:214-214  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: For request logging the Serilog guide directs the author to UseSerilogRequestLogging().
TRIGGER: Implementing Serilog request logging under the logging skill or its private reference | EXC: Only for the concrete logging need; sinks are optional. Provider-specific APIs stay at composition/provider boundaries. No global or exclusive requirement inferred. | POL: ['RUN-013', 'DEP-010']
CODEX WHY: Potential independent technique guidance, with uncertainty about descriptive modality and whether the broad independent finding already encompasses it.
```
 211  | Serilog as provider | `AddSerilog()` + configuration |
 212  | Development log storage | Seq (free single-user) or Aspire Dashboard |
 213  | Production log storage | Seq, Elasticsearch (Elastic sink) or an OTLP backend |
 214> | Request logging | `UseSerilogRequestLogging()` |
 215  | Scoped properties | `LogContext.PushProperty()` in middleware |
 216  | Expression-based filtering | `Serilog.Expressions` |
 217  | Audit trail | `AuditTo` (synchronous, exceptions propagate) |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-a89cc47d55 [209, 219] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: When Serilog is configured use DI-integrated AddSerilog with environment-aware provider configuration; application code depends on ILogger<T>.
- V2 FG-K0-c00f054503 [211, 219] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: AddSerilog() integrates with DI (ReadFrom.Services), replacing the older builder.Host.UseSerilog().
- V2 FG-K0-ea63ebf1dc [211, 219] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: Keep levels, sinks and overrides in configuration so they can differ per environment.
- V2 FG-K0-b967417c39 [211, 219] CANONICAL_PLUS_DELTA/DEFAULT pol=['DEP-004'] rel=['DEP-001']: Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.
- V2 FG-K0-b967417c39 [200, 217] CANONICAL_PLUS_DELTA/DEFAULT pol=['DEP-004'] rel=['DEP-001']: Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0450 -> FG-K0-458a5e6617 [CANONICAL_ONLY] Application code keeps using ILogger<T>; direct Serilog APIs (Log.Logger, LogContext) stay at composition or provider-specific boundaries.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0452 -> FG-K0-ea63ebf1dc [CANONICAL_ONLY] Keep levels, sinks and overrides in configuration so they can differ per environment.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0190 -> FG-K0-17e2f22e6a [CANONICAL_ONLY] File, Seq and other sinks are not baseline dependencies; a Console sink suffices for a simple local Development baseline; example limits and retention values are illustrative.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0071 -> FG-K0-84d69f4114 [CANONICAL_ONLY] ILogger<T> with structured message templates and stable property names; avoid interpolation that makes structured values opaque.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0072 -> FG-K0-a89cc47d55 [CANONICAL_ONLY] When Serilog is configured use DI-integrated AddSerilog with environment-aware provider configuration; application code depends on ILogger<T>.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0042 -> FG-K0-b967417c39 [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.

## CIS-K0-U0042 (pass 3) K0 .claude/skills/logging/references/serilog.md:215-215  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: For scoped properties the Serilog guide directs LogContext.PushProperty() in middleware.
TRIGGER: Implementing Serilog scoped properties under the logging skill or its private reference | EXC: Only for the concrete logging need; sinks are optional. Provider-specific APIs stay at composition/provider boundaries. No global or exclusive requirement inferred. | POL: ['RUN-013', 'DEP-010']
CODEX WHY: Potential independent technique guidance, with uncertainty about descriptive modality and whether the broad independent finding already encompasses it.
```
 212  | Development log storage | Seq (free single-user) or Aspire Dashboard |
 213  | Production log storage | Seq, Elasticsearch (Elastic sink) or an OTLP backend |
 214  | Request logging | `UseSerilogRequestLogging()` |
 215> | Scoped properties | `LogContext.PushProperty()` in middleware |
 216  | Expression-based filtering | `Serilog.Expressions` |
 217  | Audit trail | `AuditTo` (synchronous, exceptions propagate) |
 218  | Levels per environment | `MinimumLevel.Override` in appsettings |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-a89cc47d55 [209, 219] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: When Serilog is configured use DI-integrated AddSerilog with environment-aware provider configuration; application code depends on ILogger<T>.
- V2 FG-K0-c00f054503 [211, 219] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: AddSerilog() integrates with DI (ReadFrom.Services), replacing the older builder.Host.UseSerilog().
- V2 FG-K0-ea63ebf1dc [211, 219] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: Keep levels, sinks and overrides in configuration so they can differ per environment.
- V2 FG-K0-b967417c39 [211, 219] CANONICAL_PLUS_DELTA/DEFAULT pol=['DEP-004'] rel=['DEP-001']: Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.
- V2 FG-K0-b967417c39 [200, 217] CANONICAL_PLUS_DELTA/DEFAULT pol=['DEP-004'] rel=['DEP-001']: Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0450 -> FG-K0-458a5e6617 [CANONICAL_ONLY] Application code keeps using ILogger<T>; direct Serilog APIs (Log.Logger, LogContext) stay at composition or provider-specific boundaries.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0452 -> FG-K0-ea63ebf1dc [CANONICAL_ONLY] Keep levels, sinks and overrides in configuration so they can differ per environment.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0190 -> FG-K0-17e2f22e6a [CANONICAL_ONLY] File, Seq and other sinks are not baseline dependencies; a Console sink suffices for a simple local Development baseline; example limits and retention values are illustrative.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0071 -> FG-K0-84d69f4114 [CANONICAL_ONLY] ILogger<T> with structured message templates and stable property names; avoid interpolation that makes structured values opaque.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0072 -> FG-K0-a89cc47d55 [CANONICAL_ONLY] When Serilog is configured use DI-integrated AddSerilog with environment-aware provider configuration; application code depends on ILogger<T>.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0042 -> FG-K0-b967417c39 [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.

## CIS-K0-U0043 (pass 3) K0 .claude/skills/logging/references/serilog.md:216-216  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: For expression-based filtering the Serilog guide directs the author to Serilog.Expressions.
TRIGGER: Implementing expression-based Serilog filtering under the logging skill or its private reference | EXC: Only for the concrete logging need; sinks are optional. Provider-specific APIs stay at composition/provider boundaries. No global or exclusive requirement inferred. | POL: ['RUN-013', 'DEP-010']
CODEX WHY: Potential independent technique guidance, with uncertainty about descriptive modality and whether the broad independent finding already encompasses it.
```
 213  | Production log storage | Seq, Elasticsearch (Elastic sink) or an OTLP backend |
 214  | Request logging | `UseSerilogRequestLogging()` |
 215  | Scoped properties | `LogContext.PushProperty()` in middleware |
 216> | Expression-based filtering | `Serilog.Expressions` |
 217  | Audit trail | `AuditTo` (synchronous, exceptions propagate) |
 218  | Levels per environment | `MinimumLevel.Override` in appsettings |
 219  | OpenTelemetry integration | `Serilog.Sinks.OpenTelemetry` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-a89cc47d55 [209, 219] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: When Serilog is configured use DI-integrated AddSerilog with environment-aware provider configuration; application code depends on ILogger<T>.
- V2 FG-K0-c00f054503 [211, 219] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: AddSerilog() integrates with DI (ReadFrom.Services), replacing the older builder.Host.UseSerilog().
- V2 FG-K0-ea63ebf1dc [211, 219] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: Keep levels, sinks and overrides in configuration so they can differ per environment.
- V2 FG-K0-b967417c39 [211, 219] CANONICAL_PLUS_DELTA/DEFAULT pol=['DEP-004'] rel=['DEP-001']: Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.
- V2 FG-K0-b967417c39 [200, 217] CANONICAL_PLUS_DELTA/DEFAULT pol=['DEP-004'] rel=['DEP-001']: Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0450 -> FG-K0-458a5e6617 [CANONICAL_ONLY] Application code keeps using ILogger<T>; direct Serilog APIs (Log.Logger, LogContext) stay at composition or provider-specific boundaries.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0452 -> FG-K0-ea63ebf1dc [CANONICAL_ONLY] Keep levels, sinks and overrides in configuration so they can differ per environment.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0190 -> FG-K0-17e2f22e6a [CANONICAL_ONLY] File, Seq and other sinks are not baseline dependencies; a Console sink suffices for a simple local Development baseline; example limits and retention values are illustrative.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0071 -> FG-K0-84d69f4114 [CANONICAL_ONLY] ILogger<T> with structured message templates and stable property names; avoid interpolation that makes structured values opaque.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0072 -> FG-K0-a89cc47d55 [CANONICAL_ONLY] When Serilog is configured use DI-integrated AddSerilog with environment-aware provider configuration; application code depends on ILogger<T>.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0042 -> FG-K0-b967417c39 [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.

## CIS-K0-U0044 (pass 3) K0 .claude/skills/logging/references/serilog.md:218-218  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: For levels per environment the Serilog guide selects MinimumLevel.Override in appsettings.
TRIGGER: Configuring Serilog levels per environment under the logging skill or its private reference | EXC: Only for the concrete logging need; sinks are optional. Provider-specific APIs stay at composition/provider boundaries. No global or exclusive requirement inferred. | POL: ['RUN-013', 'DEP-010']
CODEX WHY: Potential independent technique guidance, with uncertainty about descriptive modality and whether the broad independent finding already encompasses it.
```
 215  | Scoped properties | `LogContext.PushProperty()` in middleware |
 216  | Expression-based filtering | `Serilog.Expressions` |
 217  | Audit trail | `AuditTo` (synchronous, exceptions propagate) |
 218> | Levels per environment | `MinimumLevel.Override` in appsettings |
 219  | OpenTelemetry integration | `Serilog.Sinks.OpenTelemetry` |
 220  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-a89cc47d55 [209, 219] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: When Serilog is configured use DI-integrated AddSerilog with environment-aware provider configuration; application code depends on ILogger<T>.
- V2 FG-K0-c00f054503 [211, 219] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: AddSerilog() integrates with DI (ReadFrom.Services), replacing the older builder.Host.UseSerilog().
- V2 FG-K0-ea63ebf1dc [211, 219] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: Keep levels, sinks and overrides in configuration so they can differ per environment.
- V2 FG-K0-b967417c39 [211, 219] CANONICAL_PLUS_DELTA/DEFAULT pol=['DEP-004'] rel=['DEP-001']: Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0450 -> FG-K0-458a5e6617 [CANONICAL_ONLY] Application code keeps using ILogger<T>; direct Serilog APIs (Log.Logger, LogContext) stay at composition or provider-specific boundaries.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0452 -> FG-K0-ea63ebf1dc [CANONICAL_ONLY] Keep levels, sinks and overrides in configuration so they can differ per environment.
- NAMED primary/K0/constraints.jsonl/EXTRA-K0-0190 -> FG-K0-17e2f22e6a [CANONICAL_ONLY] File, Seq and other sinks are not baseline dependencies; a Console sink suffices for a simple local Development baseline; example limits and retention values are illustrative.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0071 -> FG-K0-84d69f4114 [CANONICAL_ONLY] ILogger<T> with structured message templates and stable property names; avoid interpolation that makes structured values opaque.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0072 -> FG-K0-a89cc47d55 [CANONICAL_ONLY] When Serilog is configured use DI-integrated AddSerilog with environment-aware provider configuration; application code depends on ILogger<T>.
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0042 -> FG-K0-b967417c39 [CANONICAL_PLUS_DELTA] Serilog.Sinks.Elasticsearch is deprecated; use the official Elastic.Serilog.Sinks package.

## CIS-K1-U0030 (pass 3) K1 .claude/skills/logging/references/serilog.md:125-125  [MAY UNCERTAIN_NOVELTY]
CLAIM: Optional OTLP export may use Serilog.Sinks.OpenTelemetry without the OpenTelemetry SDK.
TRIGGER: Selecting optional OTLP logging export while using the applicable knowledge reference | EXC: Recommendation or optional integration, not mandatory adoption or exclusive list. Sinks require actual need; Serilog APIs remain at provider/composition edges; examples do not authorize hardcoded oper | POL: []
CODEX WHY: Generic option coverage may subsume these conventional techniques; semantic independence remains unresolved. Existing U0010 Enrich.FromLogContext prerequisite is not duplicated, and AuditTo adoption gate is already EXTRA0203/BF0040.
```
 122  
 123  ## Optional integrations
 124  
 125> - OTLP export without the OpenTelemetry SDK: `Serilog.Sinks.OpenTelemetry` (`.WriteTo.OpenTelemetry(o => { o.Endpoint = "http://localhost:4317"; o.Protocol = OtlpProtocol.Grpc; })`).
 126  - Expression filtering (`Serilog.Expressions`): `.Filter.ByExcluding("RequestPath like '/health%'")`, `.WriteTo.Conditional("@l = 'Error'", wt => wt.File("logs/errors-.log", rollingInterval: RollingInterval.Day))`.
 127  - Elasticsearch: the `Serilog.Sinks.Elasticsearch` package is deprecated; use `Elastic.Serilog.Sinks` (`.WriteTo.Elasticsearch([new Uri("https://elastic.example.com:9200")], opts => opts.DataStream = new DataStream
 128  - Audit trails: `AuditTo` (synchronous; exceptions propagate) — only with an adopted audit design.
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
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

## CIS-K1-U0031 (pass 3) K1 .claude/skills/logging/references/serilog.md:126-126  [MAY UNCERTAIN_NOVELTY]
CLAIM: Optional expression filtering is presented through Serilog.Expressions.
TRIGGER: Selecting optional Serilog expression filtering while using the applicable knowledge reference | EXC: Recommendation or optional integration, not mandatory adoption or exclusive list. Sinks require actual need; Serilog APIs remain at provider/composition edges; examples do not authorize hardcoded oper | POL: []
CODEX WHY: Generic option coverage may subsume these conventional techniques; semantic independence remains unresolved. Existing U0010 Enrich.FromLogContext prerequisite is not duplicated, and AuditTo adoption gate is already EXTRA0203/BF0040.
```
 123  ## Optional integrations
 124  
 125  - OTLP export without the OpenTelemetry SDK: `Serilog.Sinks.OpenTelemetry` (`.WriteTo.OpenTelemetry(o => { o.Endpoint = "http://localhost:4317"; o.Protocol = OtlpProtocol.Grpc; })`).
 126> - Expression filtering (`Serilog.Expressions`): `.Filter.ByExcluding("RequestPath like '/health%'")`, `.WriteTo.Conditional("@l = 'Error'", wt => wt.File("logs/errors-.log", rollingInterval: RollingInterval.Day))`.
 127  - Elasticsearch: the `Serilog.Sinks.Elasticsearch` package is deprecated; use `Elastic.Serilog.Sinks` (`.WriteTo.Elasticsearch([new Uri("https://elastic.example.com:9200")], opts => opts.DataStream = new DataStream
 128  - Audit trails: `AuditTo` (synchronous; exceptions propagate) — only with an adopted audit design.
 129  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
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

## CIS-K1-U0025 (pass 3) K1 .claude/skills/logging/references/serilog.md:139-139  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For Development log storage, the guide recommends Console, with Seq or Aspire Dashboard when useful.
TRIGGER: Choosing Development log storage while using the applicable knowledge reference | EXC: Recommendation or optional integration, not mandatory adoption or exclusive list. Sinks require actual need; Serilog APIs remain at provider/composition edges; examples do not authorize hardcoded oper | POL: []
CODEX WHY: Generic option coverage may subsume these conventional techniques; semantic independence remains unresolved. Existing U0010 Enrich.FromLogContext prerequisite is not duplicated, and AuditTo adoption gate is already EXTRA0203/BF0040.
```
 136  | Scenario | Recommendation |
 137  |---|---|
 138  | Provider setup | `AddSerilog()` + configuration |
 139> | Development log storage | Console; Seq or Aspire Dashboard when useful |
 140  | Production log storage | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 141  | Request logging | `UseSerilogRequestLogging()` |
 142  | Scoped properties | `LogContext.PushProperty()` in middleware |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K1-3b8ba4aabd [136, 143] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: When Serilog is configured use DI-integrated AddSerilog with environment-aware provider configuration; application code depends on ILogger<T>.
- V2 FG-K1-edc43043be [136, 143] CANONICAL_ONLY/MUST pol=['DEP-001'] rel=['DEP-011', 'GOV-013']: Add a dependency only for a concrete current requirement, never for hypothetical future use; an approved technology is not a reason to install it by default.
- V2 FG-K1-57b33b9f67 [138, 143] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: builder.Services.AddSerilog(), not builder.Host.UseSerilog(), integrating with DI via ReadFrom.Services.
- V2 FG-K1-38e289cf30 [138, 143] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: Levels, sinks and overrides live in appsettings so they change per environment without redeployment.
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

## CIS-K1-U0026 (pass 3) K1 .claude/skills/logging/references/serilog.md:140-140  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For Production log storage, the guide recommends Seq, Elasticsearch with the Elastic sink, or an OTLP backend.
TRIGGER: Choosing Production log storage while using the applicable knowledge reference | EXC: Recommendation or optional integration, not mandatory adoption or exclusive list. Sinks require actual need; Serilog APIs remain at provider/composition edges; examples do not authorize hardcoded oper | POL: []
CODEX WHY: Generic option coverage may subsume these conventional techniques; semantic independence remains unresolved. Existing U0010 Enrich.FromLogContext prerequisite is not duplicated, and AuditTo adoption gate is already EXTRA0203/BF0040.
```
 137  |---|---|
 138  | Provider setup | `AddSerilog()` + configuration |
 139  | Development log storage | Console; Seq or Aspire Dashboard when useful |
 140> | Production log storage | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 141  | Request logging | `UseSerilogRequestLogging()` |
 142  | Scoped properties | `LogContext.PushProperty()` in middleware |
 143  | Level per environment | `MinimumLevel.Override` in appsettings |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K1-3b8ba4aabd [136, 143] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: When Serilog is configured use DI-integrated AddSerilog with environment-aware provider configuration; application code depends on ILogger<T>.
- V2 FG-K1-edc43043be [136, 143] CANONICAL_ONLY/MUST pol=['DEP-001'] rel=['DEP-011', 'GOV-013']: Add a dependency only for a concrete current requirement, never for hypothetical future use; an approved technology is not a reason to install it by default.
- V2 FG-K1-57b33b9f67 [138, 143] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: builder.Services.AddSerilog(), not builder.Host.UseSerilog(), integrating with DI via ReadFrom.Services.
- V2 FG-K1-38e289cf30 [138, 143] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: Levels, sinks and overrides live in appsettings so they change per environment without redeployment.
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

## CIS-K1-U0027 (pass 3) K1 .claude/skills/logging/references/serilog.md:141-141  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For request logging, the Serilog guide recommends UseSerilogRequestLogging().
TRIGGER: Configuring Serilog request logging while using the applicable knowledge reference | EXC: Recommendation or optional integration, not mandatory adoption or exclusive list. Sinks require actual need; Serilog APIs remain at provider/composition edges; examples do not authorize hardcoded oper | POL: []
CODEX WHY: Generic option coverage may subsume these conventional techniques; semantic independence remains unresolved. Existing U0010 Enrich.FromLogContext prerequisite is not duplicated, and AuditTo adoption gate is already EXTRA0203/BF0040.
```
 138  | Provider setup | `AddSerilog()` + configuration |
 139  | Development log storage | Console; Seq or Aspire Dashboard when useful |
 140  | Production log storage | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 141> | Request logging | `UseSerilogRequestLogging()` |
 142  | Scoped properties | `LogContext.PushProperty()` in middleware |
 143  | Level per environment | `MinimumLevel.Override` in appsettings |
 144  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K1-3b8ba4aabd [136, 143] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: When Serilog is configured use DI-integrated AddSerilog with environment-aware provider configuration; application code depends on ILogger<T>.
- V2 FG-K1-edc43043be [136, 143] CANONICAL_ONLY/MUST pol=['DEP-001'] rel=['DEP-011', 'GOV-013']: Add a dependency only for a concrete current requirement, never for hypothetical future use; an approved technology is not a reason to install it by default.
- V2 FG-K1-57b33b9f67 [138, 143] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: builder.Services.AddSerilog(), not builder.Host.UseSerilog(), integrating with DI via ReadFrom.Services.
- V2 FG-K1-38e289cf30 [138, 143] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: Levels, sinks and overrides live in appsettings so they change per environment without redeployment.
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

## CIS-K1-U0028 (pass 3) K1 .claude/skills/logging/references/serilog.md:142-142  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For scoped Serilog properties, the guide recommends LogContext.PushProperty in middleware.
TRIGGER: Adding scoped properties through Serilog while using the applicable knowledge reference | EXC: Recommendation or optional integration, not mandatory adoption or exclusive list. Sinks require actual need; Serilog APIs remain at provider/composition edges; examples do not authorize hardcoded oper | POL: []
CODEX WHY: Generic option coverage may subsume these conventional techniques; semantic independence remains unresolved. Existing U0010 Enrich.FromLogContext prerequisite is not duplicated, and AuditTo adoption gate is already EXTRA0203/BF0040.
```
 139  | Development log storage | Console; Seq or Aspire Dashboard when useful |
 140  | Production log storage | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 141  | Request logging | `UseSerilogRequestLogging()` |
 142> | Scoped properties | `LogContext.PushProperty()` in middleware |
 143  | Level per environment | `MinimumLevel.Override` in appsettings |
 144  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K1-3b8ba4aabd [136, 143] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: When Serilog is configured use DI-integrated AddSerilog with environment-aware provider configuration; application code depends on ILogger<T>.
- V2 FG-K1-edc43043be [136, 143] CANONICAL_ONLY/MUST pol=['DEP-001'] rel=['DEP-011', 'GOV-013']: Add a dependency only for a concrete current requirement, never for hypothetical future use; an approved technology is not a reason to install it by default.
- V2 FG-K1-57b33b9f67 [138, 143] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: builder.Services.AddSerilog(), not builder.Host.UseSerilog(), integrating with DI via ReadFrom.Services.
- V2 FG-K1-38e289cf30 [138, 143] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: Levels, sinks and overrides live in appsettings so they change per environment without redeployment.
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

## CIS-K1-U0029 (pass 3) K1 .claude/skills/logging/references/serilog.md:143-143  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For log levels per environment, the guide recommends MinimumLevel.Override in appsettings.
TRIGGER: Varying log levels by environment while using the applicable knowledge reference | EXC: Recommendation or optional integration, not mandatory adoption or exclusive list. Sinks require actual need; Serilog APIs remain at provider/composition edges; examples do not authorize hardcoded oper | POL: []
CODEX WHY: Generic option coverage may subsume these conventional techniques; semantic independence remains unresolved. Existing U0010 Enrich.FromLogContext prerequisite is not duplicated, and AuditTo adoption gate is already EXTRA0203/BF0040.
```
 140  | Production log storage | Seq, Elasticsearch (Elastic sink), or an OTLP backend |
 141  | Request logging | `UseSerilogRequestLogging()` |
 142  | Scoped properties | `LogContext.PushProperty()` in middleware |
 143> | Level per environment | `MinimumLevel.Override` in appsettings |
 144  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K1-3b8ba4aabd [136, 143] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: When Serilog is configured use DI-integrated AddSerilog with environment-aware provider configuration; application code depends on ILogger<T>.
- V2 FG-K1-edc43043be [136, 143] CANONICAL_ONLY/MUST pol=['DEP-001'] rel=['DEP-011', 'GOV-013']: Add a dependency only for a concrete current requirement, never for hypothetical future use; an approved technology is not a reason to install it by default.
- V2 FG-K1-57b33b9f67 [138, 143] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: builder.Services.AddSerilog(), not builder.Host.UseSerilog(), integrating with DI via ReadFrom.Services.
- V2 FG-K1-38e289cf30 [138, 143] CANONICAL_ONLY/DEFAULT pol=['DEP-021'] rel=[]: Levels, sinks and overrides live in appsettings so they change per environment without redeployment.
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
