# C02-RUN008-EVIDENCE: declaration (contract section 2, step A)

Written before the first edit of this change.

**Change.** EF Core technique text in all six stops narrowing `RUN-008` to measurement alone. Compiled queries and raw SQL for performance are justified by a measured **or clearly demonstrated** need, with no speculative use.

**Authority.** `RUN-008` (DEFAULT): "Compiled queries, ValueTask, pooling, custom serialization, aggressive caching and raw SQL should normally be introduced only for a measured or clearly demonstrated need." Kit 72: preserve that across all candidates without artificially strengthening it. The owner lines are already correct in all six.

**Affected candidates.** M, M1, L0, L1, K0 for compiled queries. All six for the raw SQL line.

## Line-by-line reading, on current v2 bytes

| Candidate | Line | Reading | Decision |
|---|---|---|---|
| M | `ef-core` compiled queries: "pay off only on a measured hot path where profiling shows" | "only" plus "profiling shows" excludes demonstrated need. Contradicts the owner | Change |
| M1 | `ef-core`: "fit only a measured hot path where profiling shows" | Same | Change |
| L0 | `ef-core`: "helps only on a measured hot path" | Same | Change |
| L1 | `ef-core`: "helps only when profiling shows" | Same | Change |
| K0 | `ef-core`: "belong to measured hot paths where profiling shows" | Same in effect. The line states where they belong | Change |
| K1 | `ef-core`: "measured, or clearly demonstrated, to be material" | Already aligned by v1 R09 | No change |
| M, M1, L1, K0 | Decision table "Measured extremely hot query → Consider a compiled query" | A sufficient condition, not exclusive. But it summarizes the section beside it and K1's row was aligned. Left alone, the table is narrower than the corrected section, so a reader using only the table gets a different answer | Change the row to K1's wording |
| M, M1, L0, K1 | `ef-core` Raw SQL: "or measured performance justifies it"; K0 "a measured performance need"; L1 "or measurement justifies it" | `RUN-008` names raw SQL. "only when ... or measured" excludes demonstrated need. The first branch (EF Core cannot express the query) is unrelated and stays | Change the performance branch only |

## No change, with reason

- `performance.md` and equivalent owner lines in all six: already state the policy.
- `code-review` in all six: "demonstrated hot path" and "do not recommend ... speculatively" agree with `RUN-008`.
- `modern-csharp` (M1 "profiling or a clearly hot path", L0 the same; L1, K0, K1 "demonstrated"): admit evidence other than a profile.
- `logging` "measured high-volume hot paths": `[LoggerMessage]` is not in the `RUN-008` list, and the lines say "consider" for a named situation. A conditional example, not a narrowing. Parity holds across six.
- `RUN-007` caching lines ("measured or reasoned"): a different policy, already stated in its own words.

## Kept on purpose

Measurement stays preferred where a line recommends profiling. No candidate loses a performance check. "Not merely because a query runs frequently" stays where present: frequency alone is not evidence. No owner moves.

## Same hypothetical task, all six

A query known to be hot from a documented throughput requirement, with no profile yet: `RUN-008` allows a compiled query. Before this change the technique text refused it in five candidates and allowed it in K1. A frequently run query with no evidence: refused by all six, before and after.

## Negative cases

Removing "clearly demonstrated" from any candidate's line must fail. Allowing speculative use must fail. The old "only on a measured hot path" wording must fail.
