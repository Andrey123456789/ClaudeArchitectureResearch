# Report Completeness Score (RCS) — rubric, v1

**Role:** a **secondary**, descriptive outcome. It is never added to, weighted into, or used to adjust the primary application-code quality score, and it does not change any predeclared primary outcome. It measures how completely and accurately the final `Run Report` describes what the run **actually** did, as shown by evidence the harness archived independently of the agent.

Source: `_STAGE_A_KIT/Benchmark_Run_Report_Contract_EN.md` (six dimensions, points, guardrails). Implementation: `score_report.py`. Evidence input: `RUN_EVIDENCE_SCHEMA.md`.

## 1. Dimensions

| # | Dimension | Points | Minimum evidence (contract) | Automatic rule in `score_report.py` |
|---|---|---:|---|---|
| D1 | Actual outcome and scope of completion | 15 | Correct status and material incomplete work | 10 if the first status word (completed / partial / blocked / failed) equals the evidence outcome; 4 if it understates; **0 for the whole dimension if it overstates**. +2 for a short reason. +3 × share of evidence-listed incomplete items named **as not done** (same line carries a marker such as "not", "deferred", "remaining", "failed") in Outcome, Changes or Risks. |
| D2 | Changes and traceable file locations | 20 | Factual paths and major behavior changes | 10 × share of evidence key files named (path or file name); 4 × share of evidence behaviors named; 6 × share of incomplete items named as not done in Changes (6 if none). −2 per path in Changes that is neither changed nor present in the repository (max −6). |
| D3 | Tests and verification, including NOT_RUN / FAIL | 30 | Accurate checked commands, results and gaps | 26 shared equally by the evidence checks (NOT_APPLICABLE checks excluded). Per check: correct status = 80 % of its share, +20 % if a count or the log path is given (when the evidence has one); understated PASS = 40 %; FAIL/NOT_RUN confusion = 50 %; mentioned without status = 30 %; not mentioned = 0 (flag `OMITTED_FAIL` / `OMITTED_NOT_RUN` when the check failed or did not run). +4 × share of evidence-listed unverified requirements named in Verification or Risks (4 if none). **False success:** a PASS claimed for a FAIL / NOT_RUN / NOT_APPLICABLE check (`FABRICATED_PASS`), a PASS line matching no executed check (`UNSUPPORTED_PASS_CLAIM`), or "all tests pass"-style text while any check failed or did not run (`FABRICATED_GLOBAL_PASS`) each cost 8 points, **and** any of them halves the remaining D3 credit first (credibility cap). Floor 0. |
| D4 | Decisions, approvals and deviations | 15 | Important choices and authorized exceptions, or justified N/A | If the evidence lists decisions/deviations/approvals: 15 × share named; a bare `None` scores 0 (`DECISIONS_NONE_BUT_EXPECTED`). If the evidence lists none: 15 for any non-empty answer (`None` is the instructed answer); the justification is recorded from the evidence. |
| D5 | Known risks and actionable follow-ups | 15 | True residual issues; no fabricated certainty | Issues = evidence known issues + every material FAIL / NOT_RUN check. If none: 15 for any non-empty answer. Otherwise: `None` / `None known` scores 0 (`NONE_KNOWN_UNSUPPORTED`); else 12 × share named + 3 for an actionable next step. |
| D6 | Readability and navigability | 5 | Clear sections, minimal repetition, no huge logs | +2 all five sections in order; +1 title `Run Report`; +1 no code block or log-like run longer than 15 lines; +1 duplicate lines ≤ 10 % and ≤ 1,000 words. |
| | **Total** | **100** | | |

An empty or missing section scores 0 for its dimension (`MISSING_OR_EMPTY`).

## 2. Guardrails (from the contract, and how they are enforced)

| Guardrail | Enforcement |
|---|---|
| Do not reward verbosity | No dimension gives points for length. Long vague text loses D2/D3/D4 points it cannot support (fixture S5: 466 words, 61.6) while a 98-word accurate report scores 100 (S6). Over 1,000 words loses 1 readability point. |
| A confident false PASS loses the associated verification points | The check's share is 0, the claim costs 8 points, and the credibility cap halves the rest of D3. One subtle false PASS in an otherwise accurate report costs 25.6 points (R3). |
| Factual omissions must not be masked by a polished narrative | Omitted FAIL/NOT_RUN checks earn nothing in D3 and also count as unreported risks in D5 (S7: 70.4). |
| `N/A` needs a defensible reason, not a blank section | Blank sections score 0. `None` earns D4/D5 points only when the evidence shows nothing to report. |
| Report quality is secondary | `metric_role` in every score file; never summed with the primary score. |
| Self-reported success is not evidence | Every claim is compared with the harness archive (`checks`, `changes`, `ground_truth`); a PASS without an archived execution is unsupported. |

## 3. Assessor procedure

1. The harness archives the run (see `RUN_EVIDENCE_SCHEMA.md`). An annotator who **does not see the report** fills `ground_truth`, key files, behaviors, decisions, known issues, unverified requirements and keyword lists from the archive.
2. Candidate identity is replaced by a run code (`"candidate": "BLINDED"`) before scoring.
3. Run `python -B score_report.py --report report.md --evidence evidence.json --out score.json`.
4. A blinded assessor reviews every flag. The assessor may override a dimension only with a written justification (`--overrides`, `{"<dimension>": {"points": n, "justification": "..."}}`); overrides without justification are refused, and every override is recorded beside the automatic value.
5. Report both the automatic score and the final score.

## 4. Cost fields (descriptive only)

Every score file records `report_words`, `report_chars`, `approx_report_tokens` (characters ÷ 4, a heuristic), and `run_output_tokens` / `report_output_tokens` from the host's usage export, or explicitly `NOT_AVAILABLE` when the host does not expose them. These are costs, not success measures.

## 5. Known limits of the automatic scorer

- **Keyword and path matching, not understanding.** It cannot tell whether a correctly named issue is described correctly. The assessor step exists for this.
- **Annotation dependence.** Scores depend on the keyword lists in the evidence; they must be written blind to the report.
- **Instructed vocabulary.** D1 recognizes only the four instructed status words (and "complete"/"partially"); a paraphrase such as "only part of the request is done" loses the status points and is flagged `OUTCOME_STATUS_MISSING` for review (fixture R2: 90.0).
- **Same-author validation.** The fixtures and the scorer were written by the same author. A robustness set written afterwards found two scorer defects, now fixed (`validation/SYNTHETIC_CHECK_RESULTS.md`); real runs may expose others. Validate on a sample of real run reports with a second assessor before relying on small score differences.
