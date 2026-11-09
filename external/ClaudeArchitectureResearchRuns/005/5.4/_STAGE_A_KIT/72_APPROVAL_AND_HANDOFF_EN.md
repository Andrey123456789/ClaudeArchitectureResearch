# Approved Decisions and Handoff for the Step 2 Corrective Iteration

Date: November 3, 2026. Research: Experiment 005 / Phase 5.4 / Stage A / Step 2.

## User's latest approval

**YES: align ALL SIX architectures to verify the effective MSBuild-evaluated `ManagePackageVersionsCentrally` setting, rather than reverting K0 to a simplistic literal XML-text check.** This is already approved; do not request confirmation again.

## Other previously approved decisions

- **Git (HQ-01):** If pre-existing uncommitted changes are found before a modifying task, offer either (a) an expressly authorized commit of clearly scoped changes or (b) pausing the entire task so the user can resolve them manually. Never discard or reset changes without authorization. In headless mode, stop if no standing choice was granted. An explicit user instruction can authorize rewriting `main` unless another applicable policy forbids it. Approval of an abstract workflow is not blanket authorization for dangerous Git operations. Do not over-engineer Git outside this C#-focused research.
- **Caching (HQ-02):** Ensure correct invalidation considering transaction isolation level, concurrency, commit/rollback, failures, and coherence between the cache and authoritative store. Pre-commit invalidation is permitted only if correctness is demonstrated for the relevant failure and concurrency model.
- **Versions (HQ-03):** Prefer pinned stable versions. Floating versions and prereleases are permitted only through explicit, scoped authorization; checkers must not silently reject a legitimately approved exception.
- **Headless (HQ-04):** An explicitly pre-approved Reserved change may be implemented; a new Reserved decision must not be made autonomously.
- **npm (HQ-05):** A generic `ask` confirmation or a magic command comment does not override the prohibition on bypassing incompatible peer dependencies.
- **PI-012 (HQ-06):** Classify actual normative strength using semantics, conditions, and the authority of the source, not the mere presence of `not` or `never`. Review the additional 230 cases and the 21 residual candidates. Do not automatically elevate specialized security-audit criteria into universal MUST_NOT obligations.
- **Swagger UI:** After a relevant API behavior change, open Swagger UI in Development and verify that it loads; a real runtime trial may legitimately remain NOT_RUN during this Step 2 task.
- **CPM:** The required rigor corresponds to actual effective Central Package Management behavior. The user's latest explicit approval mandates effective checking in ALL SIX candidates.
- **Compiled queries:** Shared policy `RUN-008` permits an optimization justified by measurements **or** compelling evidence. Preserve that across all candidates without artificially strengthening it.
- **Production migrations:** Preserve the general default under `WF-019`. Do not make explicitly authorized exceptions impossible by adding unconditional `never`; retain credential controls and the Production seeding prohibition.
- **CUSTOM_SETTINGS.md:** Preserve the same requirement to read it for substantial planning across all six candidates.
- **HTTP timeouts, security scans, fast/slow tests:** Their principal semantics have already been found in all six candidates. Do not rewrite them without evidence of a real gap.
- **CI/CD:** Out of scope for practical execution benchmarks; do not expand CI infrastructure for this study. Preserve existing common policy unless a concrete inconsistency requires correction.
- **Four extra claims:** Remain candidate-specific proposals; do not automatically convert them into new common policies among the 194 V2-derived policies.
- **Every edit:** One logical rule change, then verify the entire affected architecture and all related inventory policies, then rerun all preceding regressions; only then move on. After ALL edits, execute a separate full cross-candidate final audit.

## Predecessor and immutability boundaries

Work exclusively on COPIES of the final predecessor trees at `step2_controlled_repair_v1/candidates/<C>/template/`. Do not modify v1 or `inputs/`. Reuse the preceding 27 stages as regression baseline; record new stages under `step2_controlled_repair_v2/`. Do not start Step 3. Do not inspect or modify the concurrently running Codex area.

## Required final deliverables

Produce only evidence-supported corrections, a detailed per-change gate ledger, revised classification with current file/line citations, review of the six residual reviewer readings, 21 additional PI-012 cases, 62 review flags, 38 qualified policy witnesses, and 42 new claims. Conclude with explicit remaining limitations and live-environment tests required before Step 3.
