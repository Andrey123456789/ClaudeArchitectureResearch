# FAIR-02 — Shared benchmark reporting contract: implementation report

**Result:** the shared reporting instruction is implemented as one external, user-level text, identical for all six candidates, with a prompt-assembly tool, an evidence schema, a 0–100 secondary Report Completeness Score and synthetic validation (final attempt 103/103 checks). Integration status is **PREPARED, not executable**: experiment 005 has no benchmark-execution runner, so nothing has been run against a real agent. No candidate instruction, hook or template was changed.

## 1. Requirement-by-requirement status

| # | Task requirement | Status | Where |
|---|---|---|---|
| 1 | Inspect the harness read-only; identical insertion point at equal priority and timing; identical engineering tasks | **Done.** Precedent: 5.2 `GOAL_PROMPT.txt` (one shared user prompt per fresh session). Insertion: final block of the first user message, `task.rstrip() + "\n\n" + instruction`. Candidates' own instructions untouched. | `fair02/INTEGRATION_CONTRACT.md` §1–3 |
| 2 | Ready-to-use instruction text and integration contract; say whether integration is possible now | **Done.** Instruction verbatim from the contract (176 words, SHA-256 `bb17a883…6710`). Integration is **prepared only**: runner dependencies R1–R9 listed. | `fair02/RUN_REPORT_INSTRUCTION.txt`, `…provenance.json`, `fair02/assemble_prompt.py`, `INTEGRATION_CONTRACT.md` §5 |
| 3 | Headings Outcome, Changes, Verification, Decisions and deviations, Risks and follow-ups; 250–500 words preferred, never hide failures | **Done** (in the verbatim instruction). The scorer checks order and presence; it gives no points for length. | instruction; rubric D6 |
| 4 | Verifiable paths, actual commands/results, PASS/FAIL/NOT_RUN, no fabricated success; archive evidence independently | **Done.** Archive layout and `evidence.json` fields defined; every report claim is scored against archived evidence, never against itself. | `fair02/RUN_EVIDENCE_SCHEMA.md` |
| 5 | Separate 0–100 score with the six-dimension rubric; validate against archived evidence; `N/A` needs justification; reward accuracy not length | **Done.** Deterministic scorer + blinded assessor overrides that require a written justification. `None` earns points only when the evidence has nothing to report. | `fair02/REPORT_COMPLETENESS_RUBRIC.md`, `fair02/score_report.py` |
| 6 | Secondary and distinct from primary metrics; record words and approximate output tokens, else `NOT_AVAILABLE` | **Done.** Every score file carries `metric_role: SECONDARY`, `report_words`, `approx_report_tokens` (chars ÷ 4) and host token counts or `NOT_AVAILABLE`. | scorer output; rubric §4 |
| 7 | Synthetic checks for completed, partial, failed and misleading reports; fabricated PASS penalized; store cases and actual outcomes | **Done.** 13 fixtures, 103 checks, three recorded attempts. | `fair02/validation/` |
| 8 | Protocol states that this measures compliance with an identical **prompted** request, not spontaneous reporting; baseline design and Step 3 unchanged | **Done** (addendum to adopt before the first measured run). | `fair02/BENCHMARK_PROTOCOL_ADDENDUM_FAIR02.md` |

## 2. Validation evidence (actual outcomes)

Synthetic fixtures (fictional task: an order-lookup endpoint, tests and an Angular page) pair a report with independently "archived" evidence. Expectations were declared before each attempt that used them. Full table: `fair02/validation/SYNTHETIC_CHECK_RESULTS.md`.

| Fixture | What it represents | Final score |
|---|---|---:|
| S1 | Genuinely completed, accurate | 100 |
| S2 | Partially completed (1 failing test, page not built), accurate | 100 |
| S3 | Failed run (build error), accurate | 100 |
| S4 | **Misleading**: claims completion and PASS on the S2 evidence | **17.0** |
| S8 | **Misleading**: claims completion and PASS on the S3 evidence | **14.0** |
| S7 | No false PASS, but silently omits the failing test and NOT_RUN checks | 70.4 |
| S5 | 466-word polished, vague report of a true run | 61.6 |
| S6 | 98-word accurate report of the same run | 100 |
| S9 | Accurate, plus two invented file paths | 96.0 |
| R1 | Accurate, tables and emoji statuses | 100 |
| R2 | Accurate, paraphrased outcome and lowercase statuses | 90.0 |
| R3 | Accurate except one false PASS | 74.4 |
| R4 | Accurate plus a PASS for a check never executed | 77.0 |

Fabricated PASS claims are penalized in every misleading case (S4, S8, R3, R4: Verification 0, 0, 4.4, 7.0 of 30). An honest failure scores as high as an honest success (S3 = S1), so the metric rewards accuracy, not run success.

**Attempt history.** Attempt 1 (core fixtures S1–S9): 79/79. Attempt 2 added a robustness set written afterwards (R1–R4) with pre-declared expectations, and failed 4/103. It exposed two real scorer defects: (a) the honest line "47 passed, 1 failed" was read as PASS, so an honest report was **falsely accused of fabrication**; (b) one subtle false PASS cost only 13.2 points. Attempt 3, after fixing both (a nonzero failed count means FAIL; a credibility cap halves verification credit after any false success claim), passed 103/103 with unchanged fixtures and expectations. All attempts are kept in `fair02/validation/results/`.

Prompt assembly: on a placeholder task, `assemble_prompt.py` produced six byte-identical prompts ending in the instruction (`fair02/validation/prompt_assembly_check/`).

## 3. Interpretation limits

- **Prompted compliance only.** The results will describe how each architecture complies with the same report request, not how it reports unprompted.
- **Architecture-specific report extras remain.** Step 3's seven report-content extras and the force vocabulary (M1 and L1 do not require reporting deviations) can raise some candidates' D4 and section content. Report RCS per dimension and per candidate with this caveat; do not edit the extras out.
- **Heuristic scorer.** Keyword and path matching cannot judge whether a named issue is described correctly; a blinded assessor reviews the flags. The instructed status vocabulary is required for full D1 credit (R2).
- **Same-author validation.** Fixtures, expectations and scorer were written in one session by one author; the robustness set reduced but did not remove this bias. Calibrate on real run reports with a second assessor before interpreting small differences.
- **Not run against an agent.** No live run, token count or real report was measured; costs are `NOT_AVAILABLE` until a runner exists.

## 4. Files

| File | Purpose |
|---|---|
| `fair02/RUN_REPORT_INSTRUCTION.txt` (+ `.provenance.json`) | The exact shared instruction and its derivation from the contract |
| `fair02/assemble_prompt.py` | Appends it identically per candidate; refuses on hash drift or non-identical output |
| `fair02/INTEGRATION_CONTRACT.md` | Insertion point, rejected alternatives, candidate interactions, visibility, runner dependencies R1–R9 |
| `fair02/BENCHMARK_PROTOCOL_ADDENDUM_FAIR02.md` | Protocol text to adopt before the first measured run |
| `fair02/REPORT_COMPLETENESS_RUBRIC.md`, `fair02/score_report.py` | Rubric and scorer (SHA-256 `29a845d5…828c`) |
| `fair02/RUN_EVIDENCE_SCHEMA.md` | Independent archive layout and `evidence.json` fields |
| `fair02/validation/` | `build_fixtures.py`, `fixtures/` (13), `run_synthetic_checks.py`, `results/attempt_001..003/`, `SYNTHETIC_CHECK_RESULTS.md`, `prompt_assembly_check/` |

Reproduce (from `fair02/validation`): `python -B build_fixtures.py`, `python -B run_synthetic_checks.py`, `python -B summarize_results.py`.
