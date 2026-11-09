# R09 item 8.3 K1 compiled queries: baseline and impact

**Target.** Compiled-query optimization is justified by measurement or clearly demonstrated need, with no unjustified speculative use. Other performance policies stay.

**Original.** RUN-008: "should normally be introduced only for a measured or clearly demonstrated need." K1 `ef-core:128`: "fit only a measured hot path where compilation/cache lookup overhead is material". K1 `ef-core:241`: "Measured extremely hot query". K1's own owner line `rules/backend/runtime.md:13` already matches RUN-008.

**Files.** K1 `skills/ef-core/SKILL.md` only.

**Parity lead, not edited.** M (`ef-core:253-258`), M1, L0 (`ef-core:144`), L1 (`ef-core:92`) and K0 (`ef-core:218`) have similar measured-hot-path technique lines. The register approves K1 only; K1 was the one the audit corrected, and its proposal found the rest by no sweep. All six owner lines say measured or clearly demonstrated. Recorded in `UNRESOLVED_DECISIONS.jsonl`.
