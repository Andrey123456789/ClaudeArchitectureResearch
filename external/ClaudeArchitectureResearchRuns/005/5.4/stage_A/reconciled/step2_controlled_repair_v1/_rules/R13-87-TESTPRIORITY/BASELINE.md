# R13 item 8.7 test priority: comparison

**Type.** CLASSIFICATION_ONLY. No template change, because no required obligation is missing.

**Six-way source.** `prioritize meaningful behavior, important edge cases and risky integrations` stands in `dotnet-testing` of M, K0, K1. M1, L0, L1 have no such sentence; they carry `Do not generate low-value tests merely to ... coverage`, which is TST-011, and "Choose the narrowest test level that meaningfully verifies the behavior" and the `code-review` priority "missing meaningful tests".

**Canonical baseline.** TST-011 forbids low-value tests for coverage. No policy states a priority order. The sentence is therefore a DEFAULT extra in M, K0, K1. Its absence in M1, L0, L1 is a real but small source difference on an extra, not a missing duty.

**Register note.** The register says the priority «уже представлены». That is true through `code-review` in all six and through the sentence in three. Recorded rather than harmonized, as the contract says: preserve intentionally different wording, change templates only for a demonstrated missing or weaker required obligation. Step 3 should compare the extra fragment and not count it as a difference in required behavior.

**Classification.** `FG-K0-9146b82c8d` and `FG-K1-8a61b0db25` follow M to `MIXED` through the audit proposals, adjudicated in R25.
