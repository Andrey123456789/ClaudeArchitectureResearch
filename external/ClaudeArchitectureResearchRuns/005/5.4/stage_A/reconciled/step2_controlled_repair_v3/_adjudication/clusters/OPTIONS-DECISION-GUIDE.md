# OPTIONS-DECISION-GUIDE (24 records)

## CIS-M-U0013 (pass 2) M .claude/skills/configuration/SKILL.md:204-204  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For simple immutable configuration, the decision guide selects IOptions<T>.
TRIGGER: Choosing an accessor for simple immutable service configuration. | EXC: The parent skill explicitly calls itself technique only; this is a possible scenario-conditioned preference, not a proven mandate to forbid equivalent APIs. Illustrative numbers are not approved defau | POL: ['RUN-022']
CODEX WHY: Exact scenario/technique row can change a choice independently of the broad typed-options norm. However the parent labels itself technique only and other APIs may fulfill the same behavior. Preserve separately for adjudication without promoting a table example to a proven normative constraint.
```
 201  | Scenario | Recommendation |
 202  |----------|---------------|
 203  | Binding config to a class | Options pattern with `BindConfiguration` |
 204> | Simple, immutable config | `IOptions<T>` |
 205  | Config that changes per request | `IOptionsSnapshot<T>` |
 206  | Background service watching config | `IOptionsMonitor<T>` |
 207  | Development secrets | `dotnet user-secrets` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-bcc7afd10a [201, 210] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured service configuration, validate settings at startup when missing or invalid values prevent correct or secure operation, and avoid scattering string-based IConfiguration lookups through 
- V2 FG-M-61c7219967 [201, 210] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Use a local secret mechanism (dotnet user-secrets) in development and environment secret injection/managed secret store when deployed; do not assume a cloud provider unless chosen.
- NAMED primary/M/constraints.jsonl/RULE-M-0054 -> FG-M-24958494e5 [CANONICAL_PLUS_DELTA] Prefer strongly typed options, validate at startup when missing/invalid values prevent correct/secure operation, avoid scattered string IConfiguration lookups (direct IConfiguratio
- NAMED primary/M/constraints.jsonl/RULE-M-0371 -> FG-M-f5162347fe [CANONICAL_PLUS_DELTA] Direct IConfiguration access belongs to the composition root, provider setup and infrastructure registration; ordinary application services receive typed options.
- NAMED replica/M/constraints.jsonl/RULE-M-0059 -> FG-M-bcc7afd10a [CANONICAL_ONLY] Prefer strongly typed options for structured service configuration, validate settings at startup when missing or invalid values prevent correct or secure operation, and avoid scatt
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0036 -> FG-M-1fe20a0d8a [CANONICAL_PLUS_DELTA] Direct IConfiguration access is confined to composition and registration code (reported as a restriction stronger than discouraging scattered lookups).
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0061 -> FG-M-f5162347fe [CANONICAL_PLUS_DELTA] Direct IConfiguration access belongs to the composition root, provider setup and infrastructure registration; ordinary application services receive typed options.

## CIS-M-U0014 (pass 2) M .claude/skills/configuration/SKILL.md:205-205  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For a value that may change per request, the decision guide selects IOptionsSnapshot<T>.
TRIGGER: Choosing an options accessor for values that may change per request. | EXC: The parent skill explicitly calls itself technique only; this is a possible scenario-conditioned preference, not a proven mandate to forbid equivalent APIs. Illustrative numbers are not approved defau | POL: ['RUN-022']
CODEX WHY: Exact scenario/technique row can change a choice independently of the broad typed-options norm. However the parent labels itself technique only and other APIs may fulfill the same behavior. Preserve separately for adjudication without promoting a table example to a proven normative constraint.
```
 202  |----------|---------------|
 203  | Binding config to a class | Options pattern with `BindConfiguration` |
 204  | Simple, immutable config | `IOptions<T>` |
 205> | Config that changes per request | `IOptionsSnapshot<T>` |
 206  | Background service watching config | `IOptionsMonitor<T>` |
 207  | Development secrets | `dotnet user-secrets` |
 208  | Production secrets | Environment/platform secret injection or chosen managed store |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-bcc7afd10a [201, 210] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured service configuration, validate settings at startup when missing or invalid values prevent correct or secure operation, and avoid scattering string-based IConfiguration lookups through 
- V2 FG-M-61c7219967 [201, 210] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Use a local secret mechanism (dotnet user-secrets) in development and environment secret injection/managed secret store when deployed; do not assume a cloud provider unless chosen.
- NAMED primary/M/constraints.jsonl/RULE-M-0054 -> FG-M-24958494e5 [CANONICAL_PLUS_DELTA] Prefer strongly typed options, validate at startup when missing/invalid values prevent correct/secure operation, avoid scattered string IConfiguration lookups (direct IConfiguratio
- NAMED primary/M/constraints.jsonl/RULE-M-0371 -> FG-M-f5162347fe [CANONICAL_PLUS_DELTA] Direct IConfiguration access belongs to the composition root, provider setup and infrastructure registration; ordinary application services receive typed options.
- NAMED replica/M/constraints.jsonl/RULE-M-0059 -> FG-M-bcc7afd10a [CANONICAL_ONLY] Prefer strongly typed options for structured service configuration, validate settings at startup when missing or invalid values prevent correct or secure operation, and avoid scatt
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0036 -> FG-M-1fe20a0d8a [CANONICAL_PLUS_DELTA] Direct IConfiguration access is confined to composition and registration code (reported as a restriction stronger than discouraging scattered lookups).
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0061 -> FG-M-f5162347fe [CANONICAL_PLUS_DELTA] Direct IConfiguration access belongs to the composition root, provider setup and infrastructure registration; ordinary application services receive typed options.

## CIS-M-U0015 (pass 2) M .claude/skills/configuration/SKILL.md:206-206  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For a background service watching changes, the decision guide selects IOptionsMonitor<T>.
TRIGGER: Choosing an accessor for a background service observing configuration changes. | EXC: The parent skill explicitly calls itself technique only; this is a possible scenario-conditioned preference, not a proven mandate to forbid equivalent APIs. Illustrative numbers are not approved defau | POL: ['RUN-022']
CODEX WHY: Exact scenario/technique row can change a choice independently of the broad typed-options norm. However the parent labels itself technique only and other APIs may fulfill the same behavior. Preserve separately for adjudication without promoting a table example to a proven normative constraint.
```
 203  | Binding config to a class | Options pattern with `BindConfiguration` |
 204  | Simple, immutable config | `IOptions<T>` |
 205  | Config that changes per request | `IOptionsSnapshot<T>` |
 206> | Background service watching config | `IOptionsMonitor<T>` |
 207  | Development secrets | `dotnet user-secrets` |
 208  | Production secrets | Environment/platform secret injection or chosen managed store |
 209  | Validating config | `ValidateDataAnnotations()` + `ValidateOnStart()` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-bcc7afd10a [201, 210] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured service configuration, validate settings at startup when missing or invalid values prevent correct or secure operation, and avoid scattering string-based IConfiguration lookups through 
- V2 FG-M-61c7219967 [201, 210] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Use a local secret mechanism (dotnet user-secrets) in development and environment secret injection/managed secret store when deployed; do not assume a cloud provider unless chosen.
- NAMED primary/M/constraints.jsonl/RULE-M-0054 -> FG-M-24958494e5 [CANONICAL_PLUS_DELTA] Prefer strongly typed options, validate at startup when missing/invalid values prevent correct/secure operation, avoid scattered string IConfiguration lookups (direct IConfiguratio
- NAMED primary/M/constraints.jsonl/RULE-M-0371 -> FG-M-f5162347fe [CANONICAL_PLUS_DELTA] Direct IConfiguration access belongs to the composition root, provider setup and infrastructure registration; ordinary application services receive typed options.
- NAMED replica/M/constraints.jsonl/RULE-M-0059 -> FG-M-bcc7afd10a [CANONICAL_ONLY] Prefer strongly typed options for structured service configuration, validate settings at startup when missing or invalid values prevent correct or secure operation, and avoid scatt
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0036 -> FG-M-1fe20a0d8a [CANONICAL_PLUS_DELTA] Direct IConfiguration access is confined to composition and registration code (reported as a restriction stronger than discouraging scattered lookups).
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0061 -> FG-M-f5162347fe [CANONICAL_PLUS_DELTA] Direct IConfiguration access belongs to the composition root, provider setup and infrastructure registration; ordinary application services receive typed options.

## CIS-M-U0016 (pass 2) M .claude/skills/configuration/SKILL.md:209-209  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For validation, the decision guide selects ValidateDataAnnotations() together with ValidateOnStart().
TRIGGER: Choosing validation technique in the configuration decision guide; broad owner restricts startup validation to correctness/security-relevant invalidity. | EXC: The parent skill explicitly calls itself technique only; this is a possible scenario-conditioned preference, not a proven mandate to forbid equivalent APIs. Illustrative numbers are not approved defau | POL: ['RUN-022']
CODEX WHY: Exact scenario/technique row can change a choice independently of the broad typed-options norm. However the parent labels itself technique only and other APIs may fulfill the same behavior. Preserve separately for adjudication without promoting a table example to a proven normative constraint.
```
 206  | Background service watching config | `IOptionsMonitor<T>` |
 207  | Development secrets | `dotnet user-secrets` |
 208  | Production secrets | Environment/platform secret injection or chosen managed store |
 209> | Validating config | `ValidateDataAnnotations()` + `ValidateOnStart()` |
 210  | Multiple configs of the same type | Named options with `IOptionsSnapshot<T>.Get(name)` |
 211  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-bcc7afd10a [201, 210] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured service configuration, validate settings at startup when missing or invalid values prevent correct or secure operation, and avoid scattering string-based IConfiguration lookups through 
- V2 FG-M-61c7219967 [201, 210] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Use a local secret mechanism (dotnet user-secrets) in development and environment secret injection/managed secret store when deployed; do not assume a cloud provider unless chosen.
- NAMED primary/M/constraints.jsonl/RULE-M-0054 -> FG-M-24958494e5 [CANONICAL_PLUS_DELTA] Prefer strongly typed options, validate at startup when missing/invalid values prevent correct/secure operation, avoid scattered string IConfiguration lookups (direct IConfiguratio
- NAMED primary/M/constraints.jsonl/RULE-M-0371 -> FG-M-f5162347fe [CANONICAL_PLUS_DELTA] Direct IConfiguration access belongs to the composition root, provider setup and infrastructure registration; ordinary application services receive typed options.
- NAMED replica/M/constraints.jsonl/RULE-M-0059 -> FG-M-bcc7afd10a [CANONICAL_ONLY] Prefer strongly typed options for structured service configuration, validate settings at startup when missing or invalid values prevent correct or secure operation, and avoid scatt
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0036 -> FG-M-1fe20a0d8a [CANONICAL_PLUS_DELTA] Direct IConfiguration access is confined to composition and registration code (reported as a restriction stronger than discouraging scattered lookups).
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0061 -> FG-M-f5162347fe [CANONICAL_PLUS_DELTA] Direct IConfiguration access belongs to the composition root, provider setup and infrastructure registration; ordinary application services receive typed options.

## CIS-M-U0017 (pass 2) M .claude/skills/configuration/SKILL.md:210-210  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For several configurations of one type, the decision guide selects named options and IOptionsSnapshot<T>.Get(name).
TRIGGER: Retrieving several configurations of a single options type. | EXC: The parent skill explicitly calls itself technique only; this is a possible scenario-conditioned preference, not a proven mandate to forbid equivalent APIs. Illustrative numbers are not approved defau | POL: ['RUN-022']
CODEX WHY: Exact scenario/technique row can change a choice independently of the broad typed-options norm. However the parent labels itself technique only and other APIs may fulfill the same behavior. Preserve separately for adjudication without promoting a table example to a proven normative constraint.
```
 207  | Development secrets | `dotnet user-secrets` |
 208  | Production secrets | Environment/platform secret injection or chosen managed store |
 209  | Validating config | `ValidateDataAnnotations()` + `ValidateOnStart()` |
 210> | Multiple configs of the same type | Named options with `IOptionsSnapshot<T>.Get(name)` |
 211  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-bcc7afd10a [201, 210] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured service configuration, validate settings at startup when missing or invalid values prevent correct or secure operation, and avoid scattering string-based IConfiguration lookups through 
- V2 FG-M-61c7219967 [201, 210] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Use a local secret mechanism (dotnet user-secrets) in development and environment secret injection/managed secret store when deployed; do not assume a cloud provider unless chosen.
- NAMED primary/M/constraints.jsonl/RULE-M-0054 -> FG-M-24958494e5 [CANONICAL_PLUS_DELTA] Prefer strongly typed options, validate at startup when missing/invalid values prevent correct/secure operation, avoid scattered string IConfiguration lookups (direct IConfiguratio
- NAMED primary/M/constraints.jsonl/RULE-M-0371 -> FG-M-f5162347fe [CANONICAL_PLUS_DELTA] Direct IConfiguration access belongs to the composition root, provider setup and infrastructure registration; ordinary application services receive typed options.
- NAMED replica/M/constraints.jsonl/RULE-M-0059 -> FG-M-bcc7afd10a [CANONICAL_ONLY] Prefer strongly typed options for structured service configuration, validate settings at startup when missing or invalid values prevent correct or secure operation, and avoid scatt
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0036 -> FG-M-1fe20a0d8a [CANONICAL_PLUS_DELTA] Direct IConfiguration access is confined to composition and registration code (reported as a restriction stronger than discouraging scattered lookups).
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0061 -> FG-M-f5162347fe [CANONICAL_PLUS_DELTA] Direct IConfiguration access belongs to the composition root, provider setup and infrastructure registration; ordinary application services receive typed options.

## CIS-M-U0012 (pass 2) M .claude/skills/dependency-injection/SKILL.md:265-265  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For strongly typed configuration, the DI decision guide selects AddOptions<T>().BindConfiguration().
TRIGGER: Choosing the binding mechanism for strongly typed configuration. | EXC: Parent explicitly owns technique and examples, no policy. The recommendation may be nonexclusive explanatory guidance; no unconditional API or lifetime mandate is established. | POL: ['RUN-022']
CODEX WHY: The table recommendation can affect an implementation choice independently of the broad rule. Its no-policy ownership and plausible explanatory reading prevent a verified novelty judgment.
```
 262  | Cross-cutting behavior | Decorator |
 263  | Convention-based registration | Scrutor, when already justified |
 264  | Runtime implementation selection | Factory delegate |
 265> | Strongly typed config | `AddOptions<T>().BindConfiguration()` |
 266  
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

## CIS-M1-U0015 (pass 2) M1 .claude/skills/configuration/SKILL.md:190-190  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: Prefer the Options pattern with BindConfiguration when binding configuration to a class.
TRIGGER: Binding configuration to a class while this knowledge skill is applicable and consulted. | EXC: Recommendation, not an established mandatory or exclusive API choice. Knowledge-skill technique framing and template-maintenance placement guidance may make this explanatory rather than an independent | POL: ['RUN-022']
CODEX WHY: The Recommendation column may express a weak independent selection preference absent from registered actions, or merely describe idiomatic framework technique. Header calls this Configuration technique; template-maintenance 25..38 assigns techniques/examples to knowledge skills and prohibits hiding must/must-not rules there. No stronger obligation inferred. Each row has a different independently s
```
 187  
 188  | Scenario | Recommendation |
 189  |---|---|
 190> | Binding config to a class | Options pattern with `BindConfiguration` |
 191  | Simple, immutable config | `IOptions<T>` |
 192  | Config that changes per request | `IOptionsSnapshot<T>` |
 193  | Background service watching config | `IOptionsMonitor<T>` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-9de8829dcf [188, 197] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured configuration consumed by services; direct IConfiguration access is appropriate in the composition root, provider setup and infrastructure registration.
- V2 FG-M1-4bed05f607 [188, 197] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Validate settings at startup when missing/invalid values prevent correct or secure operation.
- V2 FG-M1-00864db450 [188, 197] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: By default local secret mechanism (dotnet user-secrets) in development; environment injection/managed store when deployed; no cloud-provider assumption.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0056 -> FG-M1-4bed05f607 [CANONICAL_ONLY] Validate settings at startup when missing/invalid values prevent correct or secure operation.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0154 -> FG-M1-045e52a944 [CANONICAL_ONLY] Prefer strongly typed options for structured configuration; avoid scattered string IConfiguration lookups in services; direct IConfiguration belongs to composition/provider setup/i
- NAMED primary/M1/constraints.jsonl/RULE-M1-0155 -> FG-M1-4bed05f607 [CANONICAL_ONLY] Validate settings at startup when missing/invalid values prevent correct or secure operation.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0088 -> FG-M1-580fecfcce [NON_NORMATIVE] The JWT-validation example includes a minimum key length and an expiration bound (reported copy risk despite the numeric-example disclaimer).

## CIS-M1-U0016 (pass 2) M1 .claude/skills/configuration/SKILL.md:191-191  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: Prefer IOptions<T> for simple immutable configuration.
TRIGGER: Consuming simple immutable configuration while this knowledge skill is applicable and consulted. | EXC: Recommendation, not an established mandatory or exclusive API choice. Knowledge-skill technique framing and template-maintenance placement guidance may make this explanatory rather than an independent | POL: ['RUN-022']
CODEX WHY: The Recommendation column may express a weak independent selection preference absent from registered actions, or merely describe idiomatic framework technique. Header calls this Configuration technique; template-maintenance 25..38 assigns techniques/examples to knowledge skills and prohibits hiding must/must-not rules there. No stronger obligation inferred. Each row has a different independently s
```
 188  | Scenario | Recommendation |
 189  |---|---|
 190  | Binding config to a class | Options pattern with `BindConfiguration` |
 191> | Simple, immutable config | `IOptions<T>` |
 192  | Config that changes per request | `IOptionsSnapshot<T>` |
 193  | Background service watching config | `IOptionsMonitor<T>` |
 194  | Development secrets | `dotnet user-secrets` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-9de8829dcf [188, 197] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured configuration consumed by services; direct IConfiguration access is appropriate in the composition root, provider setup and infrastructure registration.
- V2 FG-M1-4bed05f607 [188, 197] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Validate settings at startup when missing/invalid values prevent correct or secure operation.
- V2 FG-M1-00864db450 [188, 197] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: By default local secret mechanism (dotnet user-secrets) in development; environment injection/managed store when deployed; no cloud-provider assumption.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0056 -> FG-M1-4bed05f607 [CANONICAL_ONLY] Validate settings at startup when missing/invalid values prevent correct or secure operation.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0154 -> FG-M1-045e52a944 [CANONICAL_ONLY] Prefer strongly typed options for structured configuration; avoid scattered string IConfiguration lookups in services; direct IConfiguration belongs to composition/provider setup/i
- NAMED primary/M1/constraints.jsonl/RULE-M1-0155 -> FG-M1-4bed05f607 [CANONICAL_ONLY] Validate settings at startup when missing/invalid values prevent correct or secure operation.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0088 -> FG-M1-580fecfcce [NON_NORMATIVE] The JWT-validation example includes a minimum key length and an expiration bound (reported copy risk despite the numeric-example disclaimer).

## CIS-M1-U0017 (pass 2) M1 .claude/skills/configuration/SKILL.md:192-192  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: Prefer IOptionsSnapshot<T> for configuration that changes per request.
TRIGGER: Consuming per-request changing configuration while this knowledge skill is applicable and consulted. | EXC: Recommendation, not an established mandatory or exclusive API choice. Knowledge-skill technique framing and template-maintenance placement guidance may make this explanatory rather than an independent | POL: ['RUN-022']
CODEX WHY: The Recommendation column may express a weak independent selection preference absent from registered actions, or merely describe idiomatic framework technique. Header calls this Configuration technique; template-maintenance 25..38 assigns techniques/examples to knowledge skills and prohibits hiding must/must-not rules there. No stronger obligation inferred. Each row has a different independently s
```
 189  |---|---|
 190  | Binding config to a class | Options pattern with `BindConfiguration` |
 191  | Simple, immutable config | `IOptions<T>` |
 192> | Config that changes per request | `IOptionsSnapshot<T>` |
 193  | Background service watching config | `IOptionsMonitor<T>` |
 194  | Development secrets | `dotnet user-secrets` |
 195  | Production secrets | Environment/platform secret injection or the chosen managed secret store |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-9de8829dcf [188, 197] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured configuration consumed by services; direct IConfiguration access is appropriate in the composition root, provider setup and infrastructure registration.
- V2 FG-M1-4bed05f607 [188, 197] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Validate settings at startup when missing/invalid values prevent correct or secure operation.
- V2 FG-M1-00864db450 [188, 197] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: By default local secret mechanism (dotnet user-secrets) in development; environment injection/managed store when deployed; no cloud-provider assumption.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0056 -> FG-M1-4bed05f607 [CANONICAL_ONLY] Validate settings at startup when missing/invalid values prevent correct or secure operation.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0154 -> FG-M1-045e52a944 [CANONICAL_ONLY] Prefer strongly typed options for structured configuration; avoid scattered string IConfiguration lookups in services; direct IConfiguration belongs to composition/provider setup/i
- NAMED primary/M1/constraints.jsonl/RULE-M1-0155 -> FG-M1-4bed05f607 [CANONICAL_ONLY] Validate settings at startup when missing/invalid values prevent correct or secure operation.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0088 -> FG-M1-580fecfcce [NON_NORMATIVE] The JWT-validation example includes a minimum key length and an expiration bound (reported copy risk despite the numeric-example disclaimer).

## CIS-M1-U0018 (pass 2) M1 .claude/skills/configuration/SKILL.md:193-193  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: Prefer IOptionsMonitor<T> for a background service watching configuration.
TRIGGER: Background service observing configuration updates while this knowledge skill is applicable and consulted. | EXC: Recommendation, not an established mandatory or exclusive API choice. Knowledge-skill technique framing and template-maintenance placement guidance may make this explanatory rather than an independent | POL: ['RUN-022']
CODEX WHY: The Recommendation column may express a weak independent selection preference absent from registered actions, or merely describe idiomatic framework technique. Header calls this Configuration technique; template-maintenance 25..38 assigns techniques/examples to knowledge skills and prohibits hiding must/must-not rules there. No stronger obligation inferred. Each row has a different independently s
```
 190  | Binding config to a class | Options pattern with `BindConfiguration` |
 191  | Simple, immutable config | `IOptions<T>` |
 192  | Config that changes per request | `IOptionsSnapshot<T>` |
 193> | Background service watching config | `IOptionsMonitor<T>` |
 194  | Development secrets | `dotnet user-secrets` |
 195  | Production secrets | Environment/platform secret injection or the chosen managed secret store |
 196  | Validating config | `ValidateDataAnnotations()` + `ValidateOnStart()` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-9de8829dcf [188, 197] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured configuration consumed by services; direct IConfiguration access is appropriate in the composition root, provider setup and infrastructure registration.
- V2 FG-M1-4bed05f607 [188, 197] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Validate settings at startup when missing/invalid values prevent correct or secure operation.
- V2 FG-M1-00864db450 [188, 197] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: By default local secret mechanism (dotnet user-secrets) in development; environment injection/managed store when deployed; no cloud-provider assumption.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0056 -> FG-M1-4bed05f607 [CANONICAL_ONLY] Validate settings at startup when missing/invalid values prevent correct or secure operation.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0154 -> FG-M1-045e52a944 [CANONICAL_ONLY] Prefer strongly typed options for structured configuration; avoid scattered string IConfiguration lookups in services; direct IConfiguration belongs to composition/provider setup/i
- NAMED primary/M1/constraints.jsonl/RULE-M1-0155 -> FG-M1-4bed05f607 [CANONICAL_ONLY] Validate settings at startup when missing/invalid values prevent correct or secure operation.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0088 -> FG-M1-580fecfcce [NON_NORMATIVE] The JWT-validation example includes a minimum key length and an expiration bound (reported copy risk despite the numeric-example disclaimer).

## CIS-M1-U0030 (pass 3) M1 .claude/skills/configuration/SKILL.md:196-196  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: When validating configuration, prefer ValidateDataAnnotations() together with ValidateOnStart().
TRIGGER: Choosing a configuration-validation technique while applying the configuration skill | EXC: Recommendation, not exclusive required mechanism; custom validation examples remain permitted. Does not impose numeric example bounds. | POL: ['RUN-022']
CODEX WHY: Source recommendation is explicit; uncertainty remains whether mechanism guidance counts as independently normative or is subsumed by startup-validation duty.
```
 193  | Background service watching config | `IOptionsMonitor<T>` |
 194  | Development secrets | `dotnet user-secrets` |
 195  | Production secrets | Environment/platform secret injection or the chosen managed secret store |
 196> | Validating config | `ValidateDataAnnotations()` + `ValidateOnStart()` |
 197  | Multiple configs of the same type | Named options with `IOptionsSnapshot<T>.Get(name)` |
 198  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-9de8829dcf [188, 197] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured configuration consumed by services; direct IConfiguration access is appropriate in the composition root, provider setup and infrastructure registration.
- V2 FG-M1-4bed05f607 [188, 197] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Validate settings at startup when missing/invalid values prevent correct or secure operation.
- V2 FG-M1-00864db450 [188, 197] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: By default local secret mechanism (dotnet user-secrets) in development; environment injection/managed store when deployed; no cloud-provider assumption.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0155 -> FG-M1-4bed05f607 [CANONICAL_ONLY] Validate settings at startup when missing/invalid values prevent correct or secure operation.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0056 -> FG-M1-4bed05f607 [CANONICAL_ONLY] Validate settings at startup when missing/invalid values prevent correct or secure operation.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0088 -> FG-M1-580fecfcce [NON_NORMATIVE] The JWT-validation example includes a minimum key length and an expiration bound (reported copy risk despite the numeric-example disclaimer).

## CIS-M1-U0019 (pass 2) M1 .claude/skills/configuration/SKILL.md:197-197  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: Prefer named options with IOptionsSnapshot<T>.Get(name) for multiple configurations of the same type.
TRIGGER: Several configurations of a single options type while this knowledge skill is applicable and consulted. | EXC: Recommendation, not an established mandatory or exclusive API choice. Knowledge-skill technique framing and template-maintenance placement guidance may make this explanatory rather than an independent | POL: ['RUN-022']
CODEX WHY: The Recommendation column may express a weak independent selection preference absent from registered actions, or merely describe idiomatic framework technique. Header calls this Configuration technique; template-maintenance 25..38 assigns techniques/examples to knowledge skills and prohibits hiding must/must-not rules there. No stronger obligation inferred. Each row has a different independently s
```
 194  | Development secrets | `dotnet user-secrets` |
 195  | Production secrets | Environment/platform secret injection or the chosen managed secret store |
 196  | Validating config | `ValidateDataAnnotations()` + `ValidateOnStart()` |
 197> | Multiple configs of the same type | Named options with `IOptionsSnapshot<T>.Get(name)` |
 198  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-9de8829dcf [188, 197] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options for structured configuration consumed by services; direct IConfiguration access is appropriate in the composition root, provider setup and infrastructure registration.
- V2 FG-M1-4bed05f607 [188, 197] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Validate settings at startup when missing/invalid values prevent correct or secure operation.
- V2 FG-M1-00864db450 [188, 197] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: By default local secret mechanism (dotnet user-secrets) in development; environment injection/managed store when deployed; no cloud-provider assumption.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0056 -> FG-M1-4bed05f607 [CANONICAL_ONLY] Validate settings at startup when missing/invalid values prevent correct or secure operation.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0154 -> FG-M1-045e52a944 [CANONICAL_ONLY] Prefer strongly typed options for structured configuration; avoid scattered string IConfiguration lookups in services; direct IConfiguration belongs to composition/provider setup/i
- NAMED primary/M1/constraints.jsonl/RULE-M1-0155 -> FG-M1-4bed05f607 [CANONICAL_ONLY] Validate settings at startup when missing/invalid values prevent correct or secure operation.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0088 -> FG-M1-580fecfcce [NON_NORMATIVE] The JWT-validation example includes a minimum key length and an expiration bound (reported copy risk despite the numeric-example disclaimer).

## CIS-L0-U0011 (pass 2) L0 .claude/skills/configuration/SKILL.md:122-122  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For binding a configuration section to a class, the decision guide selects AddOptions<T>().BindConfiguration().
TRIGGER: Binding a section to an options class. | EXC: The parent skill explicitly calls itself technique only; this is a possible scenario-conditioned preference, not a proven mandate to forbid equivalent APIs. Illustrative numbers are not approved defau | POL: ['RUN-022']
CODEX WHY: Exact scenario/technique row can change a choice independently of the broad typed-options norm. However the parent labels itself technique only and other APIs may fulfill the same behavior. Preserve separately for adjudication without promoting a table example to a proven normative constraint.
```
 119  
 120  | Scenario | Technique |
 121  |---|---|
 122> | Bind a section to a class | `AddOptions<T>().BindConfiguration()` |
 123  | Simple immutable configuration | `IOptions<T>` |
 124  | Value that may change per request | `IOptionsSnapshot<T>` |
 125  | Background service watching changes | `IOptionsMonitor<T>` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L0-884e4ad952 [120, 129] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Local secret mechanism for development; environment-specific injection or managed secret store for deployments; do not assume an unchosen cloud provider.
- V2 FG-L0-2b28ecaa76 [120, 129] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options and validate at startup when invalid values prevent correct/secure operation; avoid scattered string IConfiguration lookups.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0177 -> FG-L0-2b28ecaa76 [CANONICAL_ONLY] Prefer strongly typed options and validate at startup when invalid values prevent correct/secure operation; avoid scattered string IConfiguration lookups.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0351 -> FG-L0-ffb2b22b51 [CANONICAL_ONLY] Direct IConfiguration access is normal in Program.cs, provider setup and infrastructure registration; ordinary services must not parse configuration keys.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0138 -> FG-L0-2b28ecaa76 [CANONICAL_ONLY] Prefer strongly typed options and validate at startup when invalid values prevent correct/secure operation; avoid scattered string IConfiguration lookups.

## CIS-L0-U0012 (pass 2) L0 .claude/skills/configuration/SKILL.md:123-123  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For simple immutable configuration, the decision guide selects IOptions<T>.
TRIGGER: Choosing an accessor for simple immutable service configuration. | EXC: The parent skill explicitly calls itself technique only; this is a possible scenario-conditioned preference, not a proven mandate to forbid equivalent APIs. Illustrative numbers are not approved defau | POL: ['RUN-022']
CODEX WHY: Exact scenario/technique row can change a choice independently of the broad typed-options norm. However the parent labels itself technique only and other APIs may fulfill the same behavior. Preserve separately for adjudication without promoting a table example to a proven normative constraint.
```
 120  | Scenario | Technique |
 121  |---|---|
 122  | Bind a section to a class | `AddOptions<T>().BindConfiguration()` |
 123> | Simple immutable configuration | `IOptions<T>` |
 124  | Value that may change per request | `IOptionsSnapshot<T>` |
 125  | Background service watching changes | `IOptionsMonitor<T>` |
 126  | Development secrets | `dotnet user-secrets` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L0-884e4ad952 [120, 129] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Local secret mechanism for development; environment-specific injection or managed secret store for deployments; do not assume an unchosen cloud provider.
- V2 FG-L0-2b28ecaa76 [120, 129] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options and validate at startup when invalid values prevent correct/secure operation; avoid scattered string IConfiguration lookups.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0177 -> FG-L0-2b28ecaa76 [CANONICAL_ONLY] Prefer strongly typed options and validate at startup when invalid values prevent correct/secure operation; avoid scattered string IConfiguration lookups.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0351 -> FG-L0-ffb2b22b51 [CANONICAL_ONLY] Direct IConfiguration access is normal in Program.cs, provider setup and infrastructure registration; ordinary services must not parse configuration keys.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0138 -> FG-L0-2b28ecaa76 [CANONICAL_ONLY] Prefer strongly typed options and validate at startup when invalid values prevent correct/secure operation; avoid scattered string IConfiguration lookups.

## CIS-L0-U0013 (pass 2) L0 .claude/skills/configuration/SKILL.md:124-124  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For a value that may change per request, the decision guide selects IOptionsSnapshot<T>.
TRIGGER: Choosing an options accessor for values that may change per request. | EXC: The parent skill explicitly calls itself technique only; this is a possible scenario-conditioned preference, not a proven mandate to forbid equivalent APIs. Illustrative numbers are not approved defau | POL: ['RUN-022']
CODEX WHY: Exact scenario/technique row can change a choice independently of the broad typed-options norm. However the parent labels itself technique only and other APIs may fulfill the same behavior. Preserve separately for adjudication without promoting a table example to a proven normative constraint.
```
 121  |---|---|
 122  | Bind a section to a class | `AddOptions<T>().BindConfiguration()` |
 123  | Simple immutable configuration | `IOptions<T>` |
 124> | Value that may change per request | `IOptionsSnapshot<T>` |
 125  | Background service watching changes | `IOptionsMonitor<T>` |
 126  | Development secrets | `dotnet user-secrets` |
 127  | Production secrets | environment/platform injection or the chosen managed store |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L0-884e4ad952 [120, 129] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Local secret mechanism for development; environment-specific injection or managed secret store for deployments; do not assume an unchosen cloud provider.
- V2 FG-L0-2b28ecaa76 [120, 129] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options and validate at startup when invalid values prevent correct/secure operation; avoid scattered string IConfiguration lookups.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0177 -> FG-L0-2b28ecaa76 [CANONICAL_ONLY] Prefer strongly typed options and validate at startup when invalid values prevent correct/secure operation; avoid scattered string IConfiguration lookups.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0351 -> FG-L0-ffb2b22b51 [CANONICAL_ONLY] Direct IConfiguration access is normal in Program.cs, provider setup and infrastructure registration; ordinary services must not parse configuration keys.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0138 -> FG-L0-2b28ecaa76 [CANONICAL_ONLY] Prefer strongly typed options and validate at startup when invalid values prevent correct/secure operation; avoid scattered string IConfiguration lookups.

## CIS-L0-U0014 (pass 2) L0 .claude/skills/configuration/SKILL.md:125-125  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For a background service watching changes, the decision guide selects IOptionsMonitor<T>.
TRIGGER: Choosing an accessor for a background service observing configuration changes. | EXC: The parent skill explicitly calls itself technique only; this is a possible scenario-conditioned preference, not a proven mandate to forbid equivalent APIs. Illustrative numbers are not approved defau | POL: ['RUN-022']
CODEX WHY: Exact scenario/technique row can change a choice independently of the broad typed-options norm. However the parent labels itself technique only and other APIs may fulfill the same behavior. Preserve separately for adjudication without promoting a table example to a proven normative constraint.
```
 122  | Bind a section to a class | `AddOptions<T>().BindConfiguration()` |
 123  | Simple immutable configuration | `IOptions<T>` |
 124  | Value that may change per request | `IOptionsSnapshot<T>` |
 125> | Background service watching changes | `IOptionsMonitor<T>` |
 126  | Development secrets | `dotnet user-secrets` |
 127  | Production secrets | environment/platform injection or the chosen managed store |
 128  | Validation | `ValidateDataAnnotations()` + `ValidateOnStart()` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L0-884e4ad952 [120, 129] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Local secret mechanism for development; environment-specific injection or managed secret store for deployments; do not assume an unchosen cloud provider.
- V2 FG-L0-2b28ecaa76 [120, 129] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options and validate at startup when invalid values prevent correct/secure operation; avoid scattered string IConfiguration lookups.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0177 -> FG-L0-2b28ecaa76 [CANONICAL_ONLY] Prefer strongly typed options and validate at startup when invalid values prevent correct/secure operation; avoid scattered string IConfiguration lookups.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0351 -> FG-L0-ffb2b22b51 [CANONICAL_ONLY] Direct IConfiguration access is normal in Program.cs, provider setup and infrastructure registration; ordinary services must not parse configuration keys.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0138 -> FG-L0-2b28ecaa76 [CANONICAL_ONLY] Prefer strongly typed options and validate at startup when invalid values prevent correct/secure operation; avoid scattered string IConfiguration lookups.

## CIS-L0-U0015 (pass 2) L0 .claude/skills/configuration/SKILL.md:128-128  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For validation, the decision guide selects ValidateDataAnnotations() together with ValidateOnStart().
TRIGGER: Choosing validation technique in the configuration decision guide; broad owner restricts startup validation to correctness/security-relevant invalidity. | EXC: The parent skill explicitly calls itself technique only; this is a possible scenario-conditioned preference, not a proven mandate to forbid equivalent APIs. Illustrative numbers are not approved defau | POL: ['RUN-022']
CODEX WHY: Exact scenario/technique row can change a choice independently of the broad typed-options norm. However the parent labels itself technique only and other APIs may fulfill the same behavior. Preserve separately for adjudication without promoting a table example to a proven normative constraint.
```
 125  | Background service watching changes | `IOptionsMonitor<T>` |
 126  | Development secrets | `dotnet user-secrets` |
 127  | Production secrets | environment/platform injection or the chosen managed store |
 128> | Validation | `ValidateDataAnnotations()` + `ValidateOnStart()` |
 129  | Several configurations of one type | named options + `IOptionsSnapshot<T>.Get(name)` |
 130  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L0-884e4ad952 [120, 129] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Local secret mechanism for development; environment-specific injection or managed secret store for deployments; do not assume an unchosen cloud provider.
- V2 FG-L0-2b28ecaa76 [120, 129] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options and validate at startup when invalid values prevent correct/secure operation; avoid scattered string IConfiguration lookups.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0177 -> FG-L0-2b28ecaa76 [CANONICAL_ONLY] Prefer strongly typed options and validate at startup when invalid values prevent correct/secure operation; avoid scattered string IConfiguration lookups.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0351 -> FG-L0-ffb2b22b51 [CANONICAL_ONLY] Direct IConfiguration access is normal in Program.cs, provider setup and infrastructure registration; ordinary services must not parse configuration keys.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0138 -> FG-L0-2b28ecaa76 [CANONICAL_ONLY] Prefer strongly typed options and validate at startup when invalid values prevent correct/secure operation; avoid scattered string IConfiguration lookups.

## CIS-L0-U0016 (pass 2) L0 .claude/skills/configuration/SKILL.md:129-129  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For several configurations of one type, the decision guide selects named options and IOptionsSnapshot<T>.Get(name).
TRIGGER: Retrieving several configurations of a single options type. | EXC: The parent skill explicitly calls itself technique only; this is a possible scenario-conditioned preference, not a proven mandate to forbid equivalent APIs. Illustrative numbers are not approved defau | POL: ['RUN-022']
CODEX WHY: Exact scenario/technique row can change a choice independently of the broad typed-options norm. However the parent labels itself technique only and other APIs may fulfill the same behavior. Preserve separately for adjudication without promoting a table example to a proven normative constraint.
```
 126  | Development secrets | `dotnet user-secrets` |
 127  | Production secrets | environment/platform injection or the chosen managed store |
 128  | Validation | `ValidateDataAnnotations()` + `ValidateOnStart()` |
 129> | Several configurations of one type | named options + `IOptionsSnapshot<T>.Get(name)` |
 130  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-L0-884e4ad952 [120, 129] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Local secret mechanism for development; environment-specific injection or managed secret store for deployments; do not assume an unchosen cloud provider.
- V2 FG-L0-2b28ecaa76 [120, 129] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Prefer strongly typed options and validate at startup when invalid values prevent correct/secure operation; avoid scattered string IConfiguration lookups.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0177 -> FG-L0-2b28ecaa76 [CANONICAL_ONLY] Prefer strongly typed options and validate at startup when invalid values prevent correct/secure operation; avoid scattered string IConfiguration lookups.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0351 -> FG-L0-ffb2b22b51 [CANONICAL_ONLY] Direct IConfiguration access is normal in Program.cs, provider setup and infrastructure registration; ordinary services must not parse configuration keys.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0138 -> FG-L0-2b28ecaa76 [CANONICAL_ONLY] Prefer strongly typed options and validate at startup when invalid values prevent correct/secure operation; avoid scattered string IConfiguration lookups.

## CIS-L1-U0024 (pass 3) L1 .claude/skills/configuration/SKILL.md:51-51  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: Use IOptions<T> for a stable configuration value.
TRIGGER: On-demand configuration skill; value does not require refresh | EXC: Other table rows choose interfaces for refreshed, changing or named configuration; no ban on these interfaces generally. | POL: ['RUN-022']
CODEX WHY: Possible conditional binding distinct from existing U0008..0010; generic IOptions representation makes novelty genuinely uncertain.
```
  48  
  49  | Need | Use |
  50  | --- | --- |
  51> | stable value | `IOptions<T>` |
  52  | refreshed per scope/request | `IOptionsSnapshot<T>` |
  53  | observe changes over time (background services) | `IOptionsMonitor<T>.CurrentValue` |
  54  | several configurations of one type | named options: `AddOptions<SmtpOptions>("internal").BindConfiguration("Smtp:Internal")`, then `IOptionsSnapshot<T>.Get("internal")` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L1/constraints.jsonl/RULE-L1-0168 -> FG-L1-8af5c9583e [CANONICAL_ONLY] Typed options: IOptions<T> via AddOptions<T>().Bind(...), validated with ValidateDataAnnotations()/Validate(...) and ValidateOnStart(); scattered lookups mean IConfiguration["..."]
- NAMED replica/L1/constraints.jsonl/RULE-L1-0062 -> FG-L1-60b660abb4 [CANONICAL_ONLY] Strongly typed options validated at startup when invalid values prevent correct/secure operation; avoid scattered string lookups.
- NAMED independent/L1/BLIND_FINDINGS.jsonl/BF-L1-0103 -> FG-L1-5cb81d6c69 [CANONICAL_ONLY] Avoid services reading string keys, secrets in committed settings and Configure<T>(section) without validation for settings the app cannot run without.
- PASS1 CIS-L1-U0008 NOT_AN_INDEPENDENT_CONSTRAINT [52, 52]: Use IOptionsSnapshot<T> for values refreshed per scope or request.
- PASS1 CIS-L1-U0009 NOT_AN_INDEPENDENT_CONSTRAINT [53, 53]: Use IOptionsMonitor<T>.CurrentValue when observing configuration changes over time, such as in background services.

## CIS-K0-U0019 (pass 2) K0 .claude/skills/configuration/SKILL.md:164-164  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: Binding configuration to a class is directed to the Options pattern with BindConfiguration.
TRIGGER: Binding structured configuration into a class. Applying the on-demand configuration knowledge guide. | EXC: No mandatory or exclusive API choice established. Skill identifies itself as knowledge technique with examples; local prose and approved conventions may support alternatives. | POL: ['RUN-022']
CODEX WHY: Plausible independently applicable technique recommendation not separately expressed by three raw runs. Normative force is uncertain under KNW technique ownership; descriptive classification is preserved as contrary evidence. Existing CIS-K0-U0009/U0010/U0011 concern different lifecycle/multiple-instance choices and are not duplicated.
```
 161  
 162  | Scenario | Technique |
 163  |---|---|
 164> | Binding configuration to a class | Options pattern with `BindConfiguration` |
 165  | Simple immutable configuration | `IOptions<T>` |
 166  | Configuration that changes per request | `IOptionsSnapshot<T>` |
 167  | Background service watching configuration | `IOptionsMonitor<T>` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-f81797201d [162, 171] CANONICAL_PLUS_DELTA/DEFAULT pol=['RUN-022'] rel=[]: Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; direct IConfiguration access only in the composition root, provider setup and infrastructure registration.
- V2 FG-K0-f81797201d [164, 171] CANONICAL_PLUS_DELTA/DEFAULT pol=['RUN-022'] rel=[]: Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; direct IConfiguration access only in the composition root, provider setup and infrastructure registration.
- V2 FG-K0-37b0a794ed [162, 171] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Local secret mechanism (dotnet user-secrets) for development; environment-specific injection or a managed secret store for deployed environments; do not assume an unchosen cloud provider.
- V2 FG-K0-37b0a794ed [164, 171] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Local secret mechanism (dotnet user-secrets) for development; environment-specific injection or a managed secret store for deployed environments; do not assume an unchosen cloud provider.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0148 -> FG-K0-f81797201d [CANONICAL_PLUS_DELTA] Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; direct IConfiguration access only in the composition root, provider set
- NAMED primary/K0/constraints.jsonl/RULE-K0-0326 -> FG-K0-4bad74cf41 [CANONICAL_ONLY] Configure<T> without validation finds misconfiguration only at runtime; AddOptions<T>().BindConfiguration(...).ValidateOnStart() fails fast.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0327 -> FG-K0-f9895bc72d [CANONICAL_ONLY] Typed options access instead of string-based IConfiguration lookups.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0070 -> FG-K0-f81797201d [CANONICAL_PLUS_DELTA] Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; direct IConfiguration access only in the composition root, provider set
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0067 -> FG-K0-4bad74cf41 [CANONICAL_ONLY] Configure<T> without validation finds misconfiguration only at runtime; AddOptions<T>().BindConfiguration(...).ValidateOnStart() fails fast.
- PASS1 CIS-K0-U0009 NOT_AN_INDEPENDENT_CONSTRAINT [166, 166]: Configuration that changes per request is directed to IOptionsSnapshot<T> by the configuration decision guide.

## CIS-K0-U0020 (pass 2) K0 .claude/skills/configuration/SKILL.md:165-165  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: Simple immutable configuration is directed to IOptions<T>.
TRIGGER: Selecting access to simple immutable configuration. Applying the on-demand configuration knowledge guide. | EXC: No mandatory or exclusive API choice established. Skill identifies itself as knowledge technique with examples; local prose and approved conventions may support alternatives. | POL: ['RUN-022']
CODEX WHY: Plausible independently applicable technique recommendation not separately expressed by three raw runs. Normative force is uncertain under KNW technique ownership; descriptive classification is preserved as contrary evidence. Existing CIS-K0-U0009/U0010/U0011 concern different lifecycle/multiple-instance choices and are not duplicated.
```
 162  | Scenario | Technique |
 163  |---|---|
 164  | Binding configuration to a class | Options pattern with `BindConfiguration` |
 165> | Simple immutable configuration | `IOptions<T>` |
 166  | Configuration that changes per request | `IOptionsSnapshot<T>` |
 167  | Background service watching configuration | `IOptionsMonitor<T>` |
 168  | Development secrets | `dotnet user-secrets` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-f81797201d [162, 171] CANONICAL_PLUS_DELTA/DEFAULT pol=['RUN-022'] rel=[]: Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; direct IConfiguration access only in the composition root, provider setup and infrastructure registration.
- V2 FG-K0-f81797201d [164, 171] CANONICAL_PLUS_DELTA/DEFAULT pol=['RUN-022'] rel=[]: Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; direct IConfiguration access only in the composition root, provider setup and infrastructure registration.
- V2 FG-K0-37b0a794ed [162, 171] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Local secret mechanism (dotnet user-secrets) for development; environment-specific injection or a managed secret store for deployed environments; do not assume an unchosen cloud provider.
- V2 FG-K0-37b0a794ed [164, 171] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Local secret mechanism (dotnet user-secrets) for development; environment-specific injection or a managed secret store for deployed environments; do not assume an unchosen cloud provider.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0148 -> FG-K0-f81797201d [CANONICAL_PLUS_DELTA] Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; direct IConfiguration access only in the composition root, provider set
- NAMED primary/K0/constraints.jsonl/RULE-K0-0326 -> FG-K0-4bad74cf41 [CANONICAL_ONLY] Configure<T> without validation finds misconfiguration only at runtime; AddOptions<T>().BindConfiguration(...).ValidateOnStart() fails fast.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0327 -> FG-K0-f9895bc72d [CANONICAL_ONLY] Typed options access instead of string-based IConfiguration lookups.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0070 -> FG-K0-f81797201d [CANONICAL_PLUS_DELTA] Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; direct IConfiguration access only in the composition root, provider set
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0067 -> FG-K0-4bad74cf41 [CANONICAL_ONLY] Configure<T> without validation finds misconfiguration only at runtime; AddOptions<T>().BindConfiguration(...).ValidateOnStart() fails fast.
- PASS1 CIS-K0-U0009 NOT_AN_INDEPENDENT_CONSTRAINT [166, 166]: Configuration that changes per request is directed to IOptionsSnapshot<T> by the configuration decision guide.
- PASS1 CIS-K0-U0010 NOT_AN_INDEPENDENT_CONSTRAINT [167, 167]: A background service watching configuration is directed to IOptionsMonitor<T> by the configuration decision guide.

## CIS-K0-U0021 (pass 2) K0 .claude/skills/configuration/SKILL.md:170-170  [UNCERTAIN UNCERTAIN_NOVELTY]
CLAIM: Configuration validation is directed to the combination ValidateDataAnnotations() and ValidateOnStart().
TRIGGER: Selecting validation of structured configuration. Applying the on-demand configuration knowledge guide. | EXC: No mandatory or exclusive API choice established. Skill identifies itself as knowledge technique with examples; local prose and approved conventions may support alternatives. | POL: ['RUN-022']
CODEX WHY: Plausible independently applicable technique recommendation not separately expressed by three raw runs. Normative force is uncertain under KNW technique ownership; descriptive classification is preserved as contrary evidence. Existing CIS-K0-U0009/U0010/U0011 concern different lifecycle/multiple-instance choices and are not duplicated.
```
 167  | Background service watching configuration | `IOptionsMonitor<T>` |
 168  | Development secrets | `dotnet user-secrets` |
 169  | Deployed secrets | Environment/platform injection or chosen managed store |
 170> | Validating configuration | `ValidateDataAnnotations()` + `ValidateOnStart()` |
 171  | Several configurations of one type | Named options with `IOptionsSnapshot<T>.Get(name)` |
 172  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K0-f81797201d [162, 171] CANONICAL_PLUS_DELTA/DEFAULT pol=['RUN-022'] rel=[]: Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; direct IConfiguration access only in the composition root, provider setup and infrastructure registration.
- V2 FG-K0-f81797201d [164, 171] CANONICAL_PLUS_DELTA/DEFAULT pol=['RUN-022'] rel=[]: Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; direct IConfiguration access only in the composition root, provider setup and infrastructure registration.
- V2 FG-K0-37b0a794ed [162, 171] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Local secret mechanism (dotnet user-secrets) for development; environment-specific injection or a managed secret store for deployed environments; do not assume an unchosen cloud provider.
- V2 FG-K0-37b0a794ed [164, 171] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Local secret mechanism (dotnet user-secrets) for development; environment-specific injection or a managed secret store for deployed environments; do not assume an unchosen cloud provider.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0148 -> FG-K0-f81797201d [CANONICAL_PLUS_DELTA] Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; direct IConfiguration access only in the composition root, provider set
- NAMED primary/K0/constraints.jsonl/RULE-K0-0326 -> FG-K0-4bad74cf41 [CANONICAL_ONLY] Configure<T> without validation finds misconfiguration only at runtime; AddOptions<T>().BindConfiguration(...).ValidateOnStart() fails fast.
- NAMED primary/K0/constraints.jsonl/RULE-K0-0327 -> FG-K0-f9895bc72d [CANONICAL_ONLY] Typed options access instead of string-based IConfiguration lookups.
- NAMED replica/K0/constraints.jsonl/RULE-K0-0070 -> FG-K0-f81797201d [CANONICAL_PLUS_DELTA] Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; direct IConfiguration access only in the composition root, provider set
- NAMED independent/K0/BLIND_FINDINGS.jsonl/BF-K0-0067 -> FG-K0-4bad74cf41 [CANONICAL_ONLY] Configure<T> without validation finds misconfiguration only at runtime; AddOptions<T>().BindConfiguration(...).ValidateOnStart() fails fast.
- PASS1 CIS-K0-U0011 NOT_AN_INDEPENDENT_CONSTRAINT [171, 171]: Several configurations of one type are directed to named options with IOptionsSnapshot<T>.Get(name) by the configuration decision guide.

## CIS-K1-U0018 (pass 3) K1 .claude/skills/configuration/SKILL.md:92-92  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For simple immutable configuration, the decision guide recommends IOptions<T>.
TRIGGER: Using the configuration knowledge skill for the scenario named by its decision guide | EXC: Recommendation, not universal mandate; complex validation delegate is explicitly shown at43..50 and example numeric values are not approved defaults. | POL: []
CODEX WHY: Same table contains previously queued U0005..0007; these are different independent recommendations. Open whether normative choices or illustrative technique under owning policy.
```
  89  | Scenario | Recommendation |
  90  |---|---|
  91  | Binding config to a class | Options pattern with `BindConfiguration` |
  92> | Simple, immutable config | `IOptions<T>` |
  93  | Config that changes per request | `IOptionsSnapshot<T>` |
  94  | Background service watching config | `IOptionsMonitor<T>` |
  95  | Development secrets | `dotnet user-secrets` |
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K1-cef95d7aaa [89, 98] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; avoid scattered string-based IConfiguration lookups.
- V2 FG-K1-cef95d7aaa [91, 98] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; avoid scattered string-based IConfiguration lookups.
- V2 FG-K1-48221bfd54 [89, 98] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Local secret mechanism (dotnet user-secrets) for development and environment-specific injection or a managed secret store when deployed; do not assume an unchosen cloud provider.
- V2 FG-K1-48221bfd54 [91, 98] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Local secret mechanism (dotnet user-secrets) for development and environment-specific injection or a managed secret store when deployed; do not assume an unchosen cloud provider.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0139 -> FG-K1-cef95d7aaa [CANONICAL_ONLY] Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; avoid scattered string-based IConfiguration lookups.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0334 -> FG-K1-87dd6783e8 [CANONICAL_ONLY] Prefer AddOptions<T>().BindConfiguration(...).ValidateOnStart() over Configure<T>(section), which defers misconfiguration to runtime.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0064 -> FG-K1-1ae0708bed [CANONICAL_ONLY] Direct IConfiguration access belongs in the composition root, provider setup and infrastructure registration; ordinary services consume typed options instead of keys and parsing.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0065 -> FG-K1-87dd6783e8 [CANONICAL_ONLY] Prefer AddOptions<T>().BindConfiguration(...).ValidateOnStart() over Configure<T>(section), which defers misconfiguration to runtime.
- PASS1 CIS-K1-U0005 NOT_AN_INDEPENDENT_CONSTRAINT [93, 93]: For configuration that changes per request, the decision guide recommends IOptionsSnapshot<T>.
- PASS1 CIS-K1-U0006 NOT_AN_INDEPENDENT_CONSTRAINT [94, 94]: For a background service watching configuration, the decision guide recommends IOptionsMonitor<T>.

## CIS-K1-U0019 (pass 3) K1 .claude/skills/configuration/SKILL.md:97-97  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For validating configuration, the decision guide recommends ValidateDataAnnotations() together with ValidateOnStart().
TRIGGER: Using the configuration knowledge skill for the scenario named by its decision guide | EXC: Recommendation, not universal mandate; complex validation delegate is explicitly shown at43..50 and example numeric values are not approved defaults. | POL: []
CODEX WHY: Same table contains previously queued U0005..0007; these are different independent recommendations. Open whether normative choices or illustrative technique under owning policy.
```
  94  | Background service watching config | `IOptionsMonitor<T>` |
  95  | Development secrets | `dotnet user-secrets` |
  96  | Production secrets | Environment/platform injection or chosen managed store |
  97> | Validating config | `ValidateDataAnnotations()` + `ValidateOnStart()` |
  98  | Multiple configs of one type | Named options |
  99  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-K1-cef95d7aaa [89, 98] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; avoid scattered string-based IConfiguration lookups.
- V2 FG-K1-cef95d7aaa [91, 98] CANONICAL_ONLY/DEFAULT pol=['RUN-022'] rel=[]: Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; avoid scattered string-based IConfiguration lookups.
- V2 FG-K1-48221bfd54 [89, 98] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Local secret mechanism (dotnet user-secrets) for development and environment-specific injection or a managed secret store when deployed; do not assume an unchosen cloud provider.
- V2 FG-K1-48221bfd54 [91, 98] CANONICAL_ONLY/DEFAULT pol=['SEC-002'] rel=[]: Local secret mechanism (dotnet user-secrets) for development and environment-specific injection or a managed secret store when deployed; do not assume an unchosen cloud provider.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0139 -> FG-K1-cef95d7aaa [CANONICAL_ONLY] Strongly typed options validated at startup when missing/invalid values prevent correct or secure operation; avoid scattered string-based IConfiguration lookups.
- NAMED primary/K1/constraints.jsonl/RULE-K1-0334 -> FG-K1-87dd6783e8 [CANONICAL_ONLY] Prefer AddOptions<T>().BindConfiguration(...).ValidateOnStart() over Configure<T>(section), which defers misconfiguration to runtime.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0064 -> FG-K1-1ae0708bed [CANONICAL_ONLY] Direct IConfiguration access belongs in the composition root, provider setup and infrastructure registration; ordinary services consume typed options instead of keys and parsing.
- NAMED independent/K1/BLIND_FINDINGS.jsonl/BF-K1-0065 -> FG-K1-87dd6783e8 [CANONICAL_ONLY] Prefer AddOptions<T>().BindConfiguration(...).ValidateOnStart() over Configure<T>(section), which defers misconfiguration to runtime.
- PASS1 CIS-K1-U0007 NOT_AN_INDEPENDENT_CONSTRAINT [98, 98]: For multiple configurations of one type, the decision guide recommends named options.
