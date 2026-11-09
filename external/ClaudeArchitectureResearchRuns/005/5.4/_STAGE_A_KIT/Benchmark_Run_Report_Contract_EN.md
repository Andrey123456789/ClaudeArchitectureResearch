# Experiment 005 — Benchmark run reporting contract (proposed, FAIR-02)

**Purpose:** Produce readable, complete run reports for each of M, M1, L0, L1, K0 and K1, while treating report quality as a secondary outcome. This is an **identical external benchmark task instruction**, not an edit to any architecture's Markdown template. Apply it to all runs at the same user-instruction priority and record that decision in the benchmark protocol before executing the first measured run.

## Report instruction to append identically to every benchmark run

> At the end of this run, produce a final report titled `Run Report` with the following sections in order. Use specific, verifiable evidence and actual file paths; do not guess results or claim unexecuted checks passed.
>
> 1. **Outcome:** State the outcome (completed, partial, blocked, or failed) and briefly explain why.
> 2. **Changes:** Describe implemented behavior and the important code/configuration files changed. Distinguish work requested from work actually completed.
> 3. **Verification:** List the important commands/checks actually executed and their results (PASS, FAIL, NOT_RUN), with counts and paths to logs when available. Identify unverified requirements.
> 4. **Decisions and deviations:** Record significant technical decisions, deviations from the request, necessary approvals and their status. Say `None` when applicable.
> 5. **Risks and follow-ups:** Identify unresolved defects, limitations, remaining work and what should be checked next. Say `None known` only if supported by your verification.
>
> Prefer a concise, clear summary (typically 250–500 words), but do not omit a material issue to meet a length target. Do not reprint large test logs. Reference their saved paths. State facts rather than unsupported confidence claims.

**Important:** The research harness must archive the generated report, terminal output, commit/worktree diff where permitted, test logs and run metadata independently. A report is not evidence that the described check happened.

## Secondary metric (reporting completeness, 0–100)

Each dimension is scored independently against the archived run evidence. `N/A` requires a defensible reason, not a blank section. Use a blinded assessor when possible.

| Dimension | Points | Minimum evidence |
|---|---:|---|
| Actual outcome and scope of completion | 15 | Correct status and material incomplete work |
| Changes and traceable file locations | 20 | Factual paths and major behavior changes |
| Tests and verification, including NOT_RUN/FAIL | 30 | Accurate checked commands, results, and gaps |
| Decisions, approvals, and deviations | 15 | Important choices and authorized exceptions, or justified N/A |
| Known risks and actionable follow-ups | 15 | True residual issues; no fabricated certainty |
| Readability and navigability | 5 | Clear sections, minimal repetition, no huge logs |
| **Total** | **100** | |

**Scoring guardrails:** Do not reward verbosity. A confident false claim that a test passed must lose the associated verification points; factual omissions should not be masked by a polished narrative. Do not add this score to the primary application-code quality score or retroactively change the predeclared primary outcome. Log report token/word count as a descriptive cost metric, not a success metric.

## Experimental interpretation

By supplying an identical reporting contract to all six candidates, the experiment measures **compliance with a common reporting request under six architectures**, not their unprompted natural reporting behavior. The seven architecture-specific report extras from Step 3 remain available as descriptive evidence; preserve them rather than editing them out. If an unprompted reporting experiment is ever wanted, it must be a separate, explicitly identified condition.
