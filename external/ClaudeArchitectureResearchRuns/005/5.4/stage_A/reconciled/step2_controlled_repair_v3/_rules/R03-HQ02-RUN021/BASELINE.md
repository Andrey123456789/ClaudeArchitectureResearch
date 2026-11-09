# R03 HQ-02 / RUN-021: baseline and impact

**Target.** Cache invalidation or refresh is coherent with the successful canonical mutation. The strategy accounts for isolation level, concurrent read and refill, commit and rollback order, crash between commit and invalidation, retries, and documented tolerated staleness. Pre-mutation invalidation is not categorically prohibited when correctness for the chosen semantics is established. Commit-then-evict is not claimed to be atomic across database and cache.

**Original quotes.** RUN-021: "Invalidate/update cache entries only in a way consistent with successful underlying mutations; do not make cache state a second source of truth." Skills: M `caching:92` "Invalidating before the underlying mutation is known to have succeeded is acceptable only when the workflow deliberately accepts that behavior"; M1:86, K1:56 same sense; L1:49 "must be a deliberate choice"; L0 and K0 have no such sentence, and K0 points to its standard for timing.

**Files.** Owner rule and `caching` skill in all six. Related: RUN-007, RUN-020, ARC-016, and logging and transaction rules (no change).

**Shared semantics versus mechanism.** The same sentence goes into each candidate's existing owner: flat rule in M and M1, Level 0 principle in L0 and L1 (technology-neutral: it says database and cache, no product name), scope-first standard in K0 and K1. Technique stays in the knowledge skill.

**Regression risks.** A rule sentence could name a technology in L0 or L1 Level 0: the invariant check covers it. "Do not cache tracked entities across Unit of Work" stays. L0 `caching:43` keeps "remove or update the affected entry after the commit succeeded" as the usual flow; the new paragraph qualifies it without deleting it.

**Pre-change controls.** Suite before patch: text checks and mutations FAIL; timeline checks PASS because they are logic only (`suite_pre.jsonl`).
