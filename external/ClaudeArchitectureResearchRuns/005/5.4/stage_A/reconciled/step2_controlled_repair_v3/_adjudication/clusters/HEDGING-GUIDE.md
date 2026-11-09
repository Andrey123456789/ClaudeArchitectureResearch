# HEDGING-GUIDE (3 records)

## CIS-M-U0048 (pass 3) M .claude/skills/httpclient-factory/references/resilience.md:148-148  [CONDITIONAL UNCERTAIN_NOVELTY]
CLAIM: For a latency-sensitive idempotent read, the resilience guide says to consider hedging after measurement.
TRIGGER: latency-sensitive idempotent read when consulting the private resilience decision guide | EXC: Consideration after measurement, not mandatory hedging; duplicate execution must be safe and ordinary need/lifetime constraints remain. No runtime measurement or API behavior observed. | POL: ['RUN-001']
CODEX WHY: Same-location table is a possible stronger temporal condition than general evidence preference; normativity and semantic subsumption remain open.
```
 145  | `429` from dependency | Respect `Retry-After` where appropriate |
 146  | Repeated dependency outage | Consider circuit breaker |
 147  | Optional data unavailable | Consider explicit fallback |
 148> | Latency-sensitive idempotent read | Consider hedging after measurement |
 149  | EF transient faults | Provider/EF execution strategy |
 150  | Incoming request rate limiting | ASP.NET Core rate limiter |
 151  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M-da648ec4e0 [140, 150] CANONICAL_ONLY/MUST pol=['RUN-015'] rel=[]: External I/O calls have bounded execution time; distinguish per-attempt from total-operation timeouts; avoid overlapping unclear timeout mechanisms.
- V2 FG-M-0151ea0125 [140, 150] CANONICAL_ONLY/MUST pol=['RUN-016'] rel=[]: Retry only when repeating is safe; never auto-retry state-changing operations (e.g. POST/PATCH) without idempotency key, idempotent semantics or concrete deduplication.
- V2 FG-M-bbbb9e05dc [140, 150] CANONICAL_ONLY/DEFAULT pol=['RUN-017'] rel=[]: Respect Retry-After or rate-limit guidance where appropriate; no indefinite/aggressive retries.
- V2 FG-M-74cdba4a65 [140, 150] CANONICAL_ONLY/MUST pol=['RUN-018'] rel=[]: Use fallback only when semantically acceptable; do not hide correctness failures behind default values.
- V2 FG-M-bee768d2fd [140, 150] EXTRA_PRODUCT/DEFAULT pol=[] rel=['RUN-016']: Do not wrap normal EF Core operations in a generic application-level retry pipeline by default; prefer the provider's EF Core execution strategy for transient faults and handle transaction/retry interaction per the provider's guid
- NAMED primary/M/constraints.jsonl/RULE-M-0469 -> FG-M-52fc01d357 [CANONICAL_ONLY] Use hedging only for operations safe to execute multiple times (idempotent reads on interchangeable endpoints), never for state-changing operations by default.
- NAMED primary/M/constraints.jsonl/RULE-M-0084 -> FG-M-51a35c0c8b [CANONICAL_ONLY] Prefer clear correct code first; no specialized optimizations without a concrete reason; prefer measurement/profiling evidence for non-trivial optimizations.
- NAMED primary/M/constraints.jsonl/RULE-M-0094 -> FG-M-e2650d5362 [CANONICAL_ONLY] Introduce compiled queries, ValueTask<T>, ArrayPool/MemoryPool, manual pooling, custom serialization optimizations, aggressive caching and raw SQL for performance only for measured
- NAMED replica/M/constraints.jsonl/RULE-M-0085 -> FG-M-51a35c0c8b [CANONICAL_ONLY] Prefer clear correct code first; no specialized optimizations without a concrete reason; prefer measurement/profiling evidence for non-trivial optimizations.
- NAMED independent/M/BLIND_FINDINGS.jsonl/BF-M-0086 -> FG-M-3041e6df68 [CANONICAL_ONLY] Retrying publication can duplicate delivery; use idempotent consumers, broker deduplication or outbox when required; retry does not give exactly-once delivery.

## CIS-M1-U0038 (pass 3) M1 .claude/skills/httpclient-factory/references/resilience.md:139-139  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For a latency-sensitive idempotent read, consider hedging after measurement.
TRIGGER: Evaluating hedging for a latency-sensitive idempotent read | EXC: Consideration only; no mandatory hedging. Repeat-safety and no state-changing hedging rules remain. | POL: []
CODEX WHY: The timing phrase is explicit but could be an instance of already-covered evidence-based optimization rather than a new constraint.
```
 136  | `429` from dependency | Respect `Retry-After` where appropriate |
 137  | Repeated dependency outage | Consider circuit breaker |
 138  | Optional data unavailable | Consider explicit fallback |
 139> | Latency-sensitive idempotent read | Consider hedging after measurement |
 140  | Persistence transient faults | Prefer the provider's execution strategy |
 141  | Incoming request rate limiting | ASP.NET Core rate limiter |
 142  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- V2 FG-M1-5774798743 [131, 141] CANONICAL_PLUS_DELTA/MUST_NOT pol=['API-007', 'RUN-018'] rel=[]: Never swallow exceptions to continue execution.
- V2 FG-M1-ad0f236790 [131, 141] CANONICAL_ONLY/MUST pol=['RUN-015'] rel=[]: External I/O has bounded execution time; avoid overlapping unclear timeout mechanisms.
- V2 FG-M1-5076fe5e7a [131, 141] CANONICAL_ONLY/MUST pol=['RUN-016'] rel=[]: Retry only when safe; no automatic retries of state-changing operations without idempotency or duplicate prevention.
- V2 FG-M1-eab271e6a5 [131, 141] CANONICAL_ONLY/DEFAULT pol=['RUN-017'] rel=[]: Respect Retry-After/rate-limit guidance where appropriate; no indefinite/aggressive retries.
- V2 FG-M1-016862ff18 [131, 141] CANONICAL_ONLY/MUST pol=['RUN-018'] rel=[]: Fallback only when semantically acceptable; never hide correctness failures behind defaults.
- V2 FG-M1-8c3c83a37a [131, 141] EXTRA_PRODUCT/MUST_NOT pol=[] rel=['RUN-016']: Do not wrap persistence in a generic application retry pipeline; prefer the provider's execution strategy and its transaction/retry guidance; HTTP retry policies are not automatically appropriate for databases.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0487 -> FG-M1-0b529e0fdd [CANONICAL_ONLY] Resilience policies match failure and operation semantics.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0495 -> FG-M1-2f8cc6ebc2 [CANONICAL_ONLY] Hedge only operations safe to execute multiple times; never state-changing operations.
- NAMED primary/M1/constraints.jsonl/RULE-M1-0413 -> FG-M1-49ed558265 [CANONICAL_ONLY] Performance-motivated changes: identify the bottleneck, preserve behaviour, prefer the simplest optimization, add/preserve tests, benchmark/profile non-obvious or complex changes.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0089 -> FG-M1-5076fe5e7a [CANONICAL_ONLY] Retry only when safe; no automatic retries of state-changing operations without idempotency or duplicate prevention.
- NAMED replica/M1/constraints.jsonl/RULE-M1-0182 -> FG-M1-49ed558265 [CANONICAL_ONLY] Performance-motivated changes: identify the bottleneck, preserve behaviour, prefer the simplest optimization, add/preserve tests, benchmark/profile non-obvious or complex changes.
- NAMED independent/M1/BLIND_FINDINGS.jsonl/BF-M1-0107 -> FG-M1-8c3c83a37a [EXTRA_PRODUCT] Do not wrap persistence in a generic application retry pipeline; prefer the provider's execution strategy and its transaction/retry guidance; HTTP retry policies are not automatica

## CIS-L0-U0039 (pass 3) L0 .claude/skills/httpclient-factory/references/resilience.md:68-68  [SHOULD UNCERTAIN_NOVELTY]
CLAIM: For a latency-sensitive idempotent read, consider hedging after measurement.
TRIGGER: Latency-sensitive idempotent read considered for hedging | EXC: Consideration guidance, not a mandate to adopt hedging. Parent source calls techniques optional and requires operation safety; no mandatory particular measurement method. | POL: ['RUN-001']
CODEX WHY: Earlier pass treated general measurement guidance as coverage. This adversarial read questions whether a scenario-specific temporal qualifier differs; retain uncertainty instead of asserting a verified missing rule.
```
  65  | `429` from dependency | a retry strategy that reads `Retry-After` |
  66  | Repeated dependency outage | consider circuit breaker |
  67  | Optional data unavailable | consider explicit fallback |
  68> | Latency-sensitive idempotent read | consider hedging after measurement |
  69  | EF transient faults | provider/EF execution strategy |
  70  
```
v3 bytes: file changed in v1/v2=False, cited text still present=True
- NAMED primary/L0/constraints.jsonl/RULE-L0-0092 -> FG-L0-1a248c8798 [CANONICAL_ONLY] Prefer clear correct code first; no specialized optimizations without a concrete reason; prefer measurement for non-trivial optimization.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0093 -> FG-L0-da89c1d301 [CANONICAL_ONLY] Advanced techniques (precompiled queries, specialized async return types, pooling, custom serialization, aggressive caching, raw SQL for performance) only for a measured or demonst
- NAMED primary/L0/constraints.jsonl/RULE-L0-0385 -> FG-L0-34bd8157bc [CANONICAL_ONLY] Performance changes identify the bottleneck, preserve behaviour, use the simplest effective optimization, keep/add tests and benchmark/profile non-obvious complex optimizations.
- NAMED primary/L0/constraints.jsonl/RULE-L0-0467 -> FG-L0-4e834da231 [CANONICAL_ONLY] Hedge only operations safe to execute several times; never hedge state-changing operations.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0028 -> FG-L0-1a248c8798 [CANONICAL_ONLY] Prefer clear correct code first; no specialized optimizations without a concrete reason; prefer measurement for non-trivial optimization.
- NAMED replica/L0/constraints.jsonl/RULE-L0-0029 -> FG-L0-da89c1d301 [CANONICAL_ONLY] Advanced techniques (precompiled queries, specialized async return types, pooling, custom serialization, aggressive caching, raw SQL for performance) only for a measured or demonst
- NAMED replica/L0/constraints.jsonl/RULE-L0-0198 -> FG-L0-34bd8157bc [CANONICAL_ONLY] Performance changes identify the bottleneck, preserve behaviour, use the simplest effective optimization, keep/add tests and benchmark/profile non-obvious complex optimizations.
- NAMED independent/L0/BLIND_FINDINGS.jsonl/BF-L0-0089 -> FG-L0-f5695d48af [EXTRA_PRODUCT] Do not wrap EF Core operations in a generic application retry pipeline; prefer the provider execution strategy (EnableRetryOnFailure) and its transaction guidance; an HTTP retry po
