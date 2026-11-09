# Benchmark protocol addendum FAIR-02 — prompted run report (to adopt before the first measured run)

1. **Condition.** Every measured run of M, M1, L0, L1, K0 and K1 receives the same reporting instruction (`fair02/RUN_REPORT_INSTRUCTION.txt`, SHA-256 `bb17a883e947b6d259afa683d26a5cbd23343e6a02e26bf93fd239918ffe6710`), appended byte-identically to the end of the first user message, at user-message priority, before any work.

2. **What is measured.** This condition measures **compliance with an identical, prompted report request** under six architectures. It does **not** measure spontaneous or unprompted reporting quality. An unprompted-reporting experiment, if ever wanted, is a separate, explicitly identified condition with its own runs.

3. **Secondary outcome.** The Report Completeness Score (0–100, `fair02/REPORT_COMPLETENESS_RUBRIC.md`) is a secondary, descriptive outcome. It is never added to the primary application-code quality score and does not change any predeclared primary outcome. Report words and output tokens (or `NOT_AVAILABLE`) are recorded as costs, not success measures.

4. **Evidence.** Reports are scored only against evidence the harness archives independently (`fair02/RUN_EVIDENCE_SCHEMA.md`). A report is not evidence that a check happened.

5. **Unchanged design.** The candidate templates, their own report instructions and their enforcement mechanisms are unchanged (FAIR-01 approved: preserve). The baseline experimental design and all Stage A Step 3 findings stand as recorded; the seven architecture-specific report-content extras remain descriptive evidence and are not edited out.
