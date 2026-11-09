from jdsl import C, D, P  # noqa: F401

P("RUN-017",
  dims=["D1 respect Retry-After or equivalent rate-limit guidance where appropriate; never retry indefinitely or aggressively (default)"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each rule: M rules/error-handling.md:75-76, M1 rules/performance.md:44-45, L0 rules/0-core/runtime-principles.md:29, L1 rules/0-core/backend-code.md:27, K0 rules/backend/integrations.md:16, K1 rules/backend/runtime.md:30.")

P("RUN-018",
  dims=["D1 fallback only when its result is semantically acceptable; never hide correctness failures behind convenient defaults"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each rule: M error-handling.md:77-78, M1 performance.md:46-47, L0 runtime-principles.md:30, L1 backend-code.md:28, K0 integrations.md:17, K1 runtime.md:31. Resilience references give the same acceptable/unacceptable examples (stale read vs 'pretend payment succeeded').")

P("RUN-019",
  dims=["D1 caller cancellation is not a transient dependency failure and is not turned into repeated outbound attempts"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each rule: M error-handling.md:79-80, M1 performance.md:48-49, L0 runtime-principles.md:34, L1 backend-code.md:29, K0 integrations.md:18, K1 runtime.md:32.")

P("RUN-020",
  dims=["D1 cache keys uniquely represent the cached value with every relevant dimension (identifier, tenant, user, locale, query); no global keys for user/tenant data"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each rule: M performance.md:54-56, M1 performance.md:68-71, L0 runtime-principles.md:21, L1 backend-code.md:34, K0 rules/backend/caching.md:14, K1 runtime.md:37. Output-cache technique for user-specific responses is the same in all six caching skills.")

P("RUN-021",
  dims=["D1 invalidate/update cache entries only consistently with successful mutations; the cache is never a second source of truth",
        "D2 the strategy accounts for isolation level, concurrent reads/refills, commit/rollback order, crash between commit and invalidation, retries and documented staleness; pre-mutation invalidation allowed when correctness is shown (HQ-02)"],
  label="FULL_SEMANTIC_PARITY",
  same="Both parts, with the approved HQ-02 wording, in each rule (read in full): M performance.md:57-64, M1 performance.md:72-79, L0 runtime-principles.md:22, L1 backend-code.md:36, K0 caching.md:16, K1 runtime.md:39. The caching skills of all six carry the same 'no single order is correct by itself' technique paragraph.")

P("RUN-022",
  dims=["D1 strongly typed options for structured configuration, validated at startup when missing/invalid values prevent correct or secure operation; no scattered string IConfiguration lookups in services"],
  label="FULL_SEMANTIC_PARITY",
  cells={"M1": C(owners=["FG-M1-045e52a944", "FG-M1-4bed05f607"], note="Step 2 override: no direct owner; rules/composition.md:25-31 states the full rule (read).")},
  same="Same default in each rule: M rules/architecture.md:144-148, M1 rules/composition.md:25-31, L0 rules/2-technology/csharp.md:33, L1 backend-code.md:40, K0 rules/backend/hosting.md:19, K1 rules/backend/operations.md:24. M, M1 and K0 name where direct IConfiguration access belongs (composition root, provider setup, infrastructure registration); the other three's configuration skills say the same.")

P("RUN-023",
  dims=["D1 every cache entry has a lifetime or another explicit invalidation strategy"],
  label="FULL_SEMANTIC_PARITY",
  same="Verbatim the same MUST in each rule: M performance.md:65-66, M1 performance.md:66-67, L0 runtime-principles.md:23, L1 backend-code.md:35, K0 caching.md:15, K1 runtime.md:38.")

P("RUN-024",
  dims=["D1 for new C# code: file-scoped namespaces when consistent, one primary top-level type per matching file, Async suffix for Task/ValueTask methods unless a contract makes it inappropriate (default)"],
  label="FULL_SEMANTIC_PARITY",
  cells={"M1": C(owners=["FG-M1-489a9096c7", "FG-M1-486661695c", "FG-M1-97180b7a82"], note="Step 2 override: no direct owner; rules/coding-style.md:17-32 states all three parts (read).")},
  same="Same three-part default in each rule: M coding-style.md:22-28, M1 coding-style.md:17-32, L0 rules/2-technology/csharp.md:16, L1 backend-code.md:48, K0 rules/backend/csharp.md:18, K1 rules/backend/coding-style.md:11. .editorconfig in all six sets the matching style preferences at suggestion level.")
