from jdsl import C, D, P  # noqa: F401

P("RUN-001",
  dims=["D1 clear correct code first; no specialized optimization without a concrete reason; measurement/profiling for non-trivial optimization (default)"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each backend runtime rule: M rules/performance.md:14-16, M1 performance.md:15-17, L0 rules/0-core/runtime-principles.md:14, L1 rules/0-core/backend-code.md:12, K0 rules/backend/csharp.md:35, K1 rules/backend/runtime.md:12. Angular and ef-core skills in all six repeat 'optimize after identifying a real problem'.")

P("RUN-002",
  dims=["D1 async APIs for asynchronous I/O; never block with .Result/.Wait()/sync-over-async"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each rule: M performance.md:20-21, M1 performance.md:21-22, L0 rules/2-technology/csharp.md:20, L1 backend-code.md:18 ('synchronous waits', with the .NET names in backend-platform.md:26), K0 csharp.md:26, K1 runtime.md:17. No candidate checks it mechanically.")

P("RUN-003",
  dims=["D1 propagate CancellationToken through asynchronous operations when cancellation is meaningful; no cancellation parameters on purely synchronous code without a use case"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST with the same exception in each rule: M performance.md:22-24, M1 performance.md:23-25, L0 csharp.md:21, L1 backend-code.md:19, K0 csharp.md:27, K1 runtime.md:18. httpclient-factory skills in all six pass the caller's token outbound and treat CancellationToken.None as a deliberate exception.")

P("RUN-004",
  dims=["D1 TimeProvider for clock-dependent logic that needs deterministic tests; stored/explicit timestamps are not replaced mechanically (default)"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each rule: M performance.md:28-31, M1 performance.md:29-32, L0 csharp.md:25, L1 backend-code.md:20 ('injectable time abstraction', TimeProvider in backend-platform.md:28), K0 csharp.md:31, K1 runtime.md:19.")

P("RUN-005",
  dims=["D1 never create and dispose a new HttpClient per request; use IHttpClientFactory or another long-lived strategy"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each rule: M performance.md:35-36, M1 performance.md:36-37, L0 csharp.md:29, L1 backend-code.md:24 (factory-managed client; .NET name in backend-platform.md:29), K0 rules/backend/integrations.md:12, K1 runtime.md:27.")

P("RUN-006",
  dims=["D1 filter/project in the database when practical; avoid unnecessary round trips, over-fetching and N+1; paginate potentially large results (default)"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each rule: M performance.md:42-45, M1 performance.md:53-56 ('watch for N+1'), L0 runtime-principles.md:16, L1 backend-code.md:14, K0 rules/backend/persistence.md:17, K1 runtime.md:23. ef-core skills in all six give the same technique (projection, deterministic ordering for paging, no lazy loading by default).")

P("RUN-007",
  dims=["D1 caching is not a default requirement; only for a clear measured or reasoned need, implementation chosen by deployment, consistency and staleness"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each rule: M performance.md:49-53, M1 performance.md:60-65, L0 runtime-principles.md:20, L1 backend-code.md:33, K0 rules/backend/caching.md:12, K1 runtime.md:36. caching skills in all six add 'define consistency semantics first'; a distributed cache is Reserved in all six (Reserved item 5).")

P("RUN-008",
  dims=["D1 compiled queries, ValueTask, pooling, custom serialization, aggressive caching and raw SQL for performance only for a measured or clearly demonstrated need (default)"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default with the same technique list in each rule: M performance.md:70-74, M1 performance.md:83-87, L0 runtime-principles.md:15, L1 backend-code.md:13, K0 csharp.md:36, K1 runtime.md:13. v2's C02 review (approved register item 8.3: 'measured or clearly demonstrated' basis) holds in all six; raw-SQL lines in all six ef-core skills use the same wording.")
