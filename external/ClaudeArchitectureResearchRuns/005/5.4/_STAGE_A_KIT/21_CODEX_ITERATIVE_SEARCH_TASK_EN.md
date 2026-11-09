# Experiment 005 / Phase 5.4 / Stage A — Codex Iterative Residual Search

## 0. Research question and boundary

Find **previously unregistered, independently falsifiable, effective normative clauses** in the frozen six candidate instruction architectures, especially cases that three prior passes overlooked or classified as mere examples, implementation details, or already-covered policy text. Preserve evidence for later human/Claude adjudication. A novel claim need not be *truly EXTRA* or experimentally important: those classifications belong to later steps.

Work root: `C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.4`.

**Six names, exactly:** `M`, `M1`, `L0`, `L1`, `K0`, `K1`. `L1-Restart` is only a historical name in 5.3; do not use it in 5.4 output identifiers.

**Immutable factual sources:**
- `inputs/<candidate>/output/template/**`: active candidate source, including rules, skills, capabilities, agents, docs, workflows, hooks, scripts, and enforceable configuration. Do not infer that the location of an instruction makes it automatically binding or irrelevant; check trigger and load conditions.
- `inputs/<candidate>/source/inventory.json` and `inputs/<candidate>/source/shared-research-invariants.json` where provided: 194 canonical policies plus 2 shared invariants, totaling 196. Inspect actual location/schema, rather than assuming a particular JSON representation.
- `inputs/INPUT_MANIFEST_SHA256.csv`: frozen source snapshot manifest.

**Three existing, completed reference sets — READ ONLY:**
- `stage_A/primary/<candidate>/`: Claude run 1, including `constraints.jsonl`, `coverage_ranges.jsonl`, `policies.jsonl`, `ORPHAN_CANDIDATES.jsonl`.
- `stage_A/replica/<candidate>/`: Claude run 2, same main formats.
- `stage_A/independent/<candidate>/blind/`: prior Codex run, including `BLIND_FINDINGS.jsonl`, `FILE_REVIEW_LEDGER.jsonl`, completion/validation reports.

These runs are **baseline claims**, not a truth oracle. Include **all** `ORACLE_LINKED`, `EXTRA`, `LINK_UNCERTAIN`, prior orphan resolutions (including `NON_NORMATIVE`), and Codex potential/uncertain findings. A finding linked to one of 196 policies is still meaningful prior coverage, even if it was not called EXTRA. Do not compare only the 1427/211/813 previously reported headline counts.

**Live concurrent task:** Claude is building `stage_A/reconciled/step1_union/**`. This directory is absolutely out of scope until your task is finished; do not read it, depend on it, modify it, or attempt to resolve concurrent write conflicts by accessing it. You must deliver independent new evidence that Claude can inspect *afterward*.

**Only writable subtree:** `stage_A/codex_iterative_search/**`. All inputs, existing runs, historical phases, and `_STAGE_A_KIT/**` are immutable for this task. Use local, read-only scans. Never run mutating candidate hooks, install dependencies, or generate app code.

## 1. Initialize immediately for reliable phone resume

Before a lengthy scan:

1. Create output root, `RESUME.md`, `STATE.json`, `BASELINE_MANIFEST.json`, and an initial `SEARCH_PROTOCOL.md` in the allowed subtree. `RESUME.md` must be self-contained: objective, authoritative task path, input paths, prohibited paths, current candidate/file/pass pointer, accepted output schemas, validation commands, and the next **one** action. `STATE.json` is its machine-readable source of checkpoint truth.
2. Inventory/hash frozen source files and the three completed result sets; check candidate completeness and readable JSONL. Build a deterministic `BASELINE_RECORD_INDEX.jsonl`, including record kind/run/original key, claimed normative action, labels, source path/range/quote/segments, scope/modality/exceptions, and policy references. Resolve Claude `evidence_segment_ids` through the **same run's** `coverage_ranges.jsonl`. Retain ambiguities; don't invent locations.
3. Make a normalized source-location map and a conservative semantic baseline lookup (candidate + actor/action/object + trigger + modality + scope + exception + lifecycle). Text search/embeddings/scripts may propose matches; no similarity threshold alone may declare equivalence.
4. Validate sources and baseline counts from the filesystem. If an expected input is absent or unexpectedly modified, STOP with a clear blocking report rather than quietly dropping it. The actual run counts are authoritative, not historical chat numbers.
5. Record a frozen `baseline_fingerprint` derived from SHA-256 of every source and baseline input; check it again at each pass boundary. Do not incorporate newly changing `step1_union` results.

Write checkpoints **before** token-intensive reasoning, then after each meaningful unit (e.g., a candidate/file or small file batch). Avoid multi-hour work existing only in conversation memory. Write temporary files then atomically replace finalized checkpoints when practical. On resume, inspect the last committed checkpoint and any incomplete output; never assume the final console message means files were saved.

`STATE.json` should contain: task/protocol version; baseline fingerprint; current pass ID; current strategy; candidate and next file/batch; completed units with output hash; current candidate findings and status; counts; convergence history; last completed pass; final status (`IN_PROGRESS`, `LIMIT_INTERRUPTED` if known, `BLOCKED`, `CONVERGED`). Do not overwrite a completed pass in order to improve its reported totals.

## 2. Freeze a comparable unit of discovery

A **candidate claim** is the smallest independently falsifiable normative proposition, consisting of:
- actor/owner; required, preferred, permitted, disallowed, or default action; target/artifact;
- precise trigger and applicability (e.g., only during a workflow, only if a frontend workspace exists, only when a hook fires);
- modality (`MUST`, `MUST_NOT`, `SHOULD`, `DEFAULT`, `MAY`, `CONDITIONAL`, or `UNCERTAIN`);
- exceptions, approval gates, fallback conditions, ordering/timing, and enforcement severity (advisory/warning/blocking) where relevant.

Split compound source text ONLY if one part could be satisfied while another is independently violated under the same applicable scenario. Merge two occurrences ONLY if they express equivalent normative behavior across all these dimensions. A narrower scope, exception, timing difference, or mandatory-vs-advisory difference is **not** a duplicate, even if the same source lines or policy ID appear.

Distinguish domains without prematurely excluding any: `PRODUCT_ENGINEERING`, `WORKFLOW_ENFORCEMENT`, `INSTRUCTION_ARCHITECTURE`, `EXAMPLE_ONLY`, `UNCERTAIN`. Executable guards and hooks may enforce real behavior; not all implementation code is normative, and not all imperative documentation is always loaded. Distinguish an observed branch from a hypothesized runtime effect.

Your discovery is **new relative to the union of THREE prior raw runs** only when a credible, independently falsifiable *source-grounded* clause is not already represented at equivalent scope, strength, exception, and trigger in any of them. An overlooked sub-clause in the **same source passage** is new. A fresh quotation of an already-recorded same clause is not new. A previous `NON_NORMATIVE` attribution is not dispositive: flag it as a `RECLASSIFICATION_CANDIDATE` with original attribution preserved.

For each claim, choose a comparison status:
- `ALREADY_COVERED`: cite one or more **specific prior record keys** and explain equivalence, including conditions/strength.
- `NOVEL_CLAUSE`: traceable new claim missing from all prior baseline claims; provide a concise counter-scenario or independently falsifiable test to show it is distinct.
- `RECLASSIFICATION_CANDIDATE`: the same source material was previously dismissed as non-normative/implementation, but evidence suggests a normative effect that was not represented as a constraint.
- `UNCERTAIN_NOVELTY`: insufficient evidence to decide prior equivalence, normativity, scope or loading. Keep in the unresolved queue; **do not** count it as proven new or discard it.
- `DUPLICATE_IN_THIS_SEARCH`: link to an earlier finding from this iterative search.

**Crucial:** `NOVEL_CLAUSE` means novel relative to previous extraction, **not** proven `EXTRA`, not proven violating the 196 requirements, not a cross-candidate difference, and not a mandate to change an architecture.

## 3. Finite, long-running diversified repeat-until-converged loop

Repeat source-first discovery, candidate by candidate, over all six, with **different search questions**, not repetitive paraphrases of one scan. A completed pass must include all six candidates and a file-coverage ledger for every active source file, even when only specific portions require deep rereading. Reuse a complete, verified source index to reduce token cost, but do not substitute a broad keyword grep for inspecting relevant code branches and prose contexts.

**Pass families (minimum diversity before claiming convergence):**

1. **Reverse normative-clause sweep:** read active source files by structure; extract explicit and conditional obligations, prohibitions, defaults, exception gates, permissions, action sequences, and approval requirements. Look for multiple constraints within one sentence or code block. Do this source-first before comparing candidates against baseline claims to avoid anchoring.
2. **Canonical-policy boundary sweep:** for each of the 196 policies, inspect implementation wording across six candidates. Search for additional restrictions not entailed by the canonical wording: narrower approvals, stronger `never`, changed `by default`, broader domains, mandatory technology choices, stricter tests, and non-obvious exceptions. Preserve canonical linkage as evidence, not a verdict.
3. **Orphan / non-normative challenge:** independently revisit ranges previously labeled `NON_NORMATIVE`, `IMPLEMENTATION`, `ORACLE_LINKED`, or unregistered by both Claude passes; search for overlooked imperative subclauses or real procedural obligations in skill references, examples, decision documents and capability descriptions.
4. **Executable-enforcement and actual-trigger sweep:** analyze hooks, guards, checkers, YAML/frontmatter, JSON/build config, pattern matching, skip lists, exit codes, warning versus block, default toggles, loading/routing and timing. Do not execute hooks with side effects. Distinguish aspirational prose from enforced behavior.
5. **Modality, exception and scope adversarial sweep:** use falsifiable counterexamples to hunt mismatches in `must/should/default/only/unless`, permission gates, lifecycle, frontend-vs-backend domains, test fixtures and migration/dependency exceptions. Split multi-part statements where independently testable. Prefer likely rare clauses rather than simple reiterated baselines.
6. **Cross-artifact consistency and negative-space sweep:** seek conditions present only in subordinate docs, reference skills, scripts, or configuration; compare that candidate's root rules versus leaf procedures. Look for controls present in one file but absent or contradicted in another. Do NOT turn this into Stage B six-way strictness ranking; record only source-grounded candidate claims absent from prior runs.

Run these **six distinct families at least once each** before concluding the search has converged. After that, use your recorded misses and hotspot ledger to formulate additional source-based, adversarial strategies as needed. If new findings remain, keep iterating. Change the order of candidate/file exploration across passes to reduce order-related bias, but preserve full coverage and traceability. The research task intentionally spans multiple five-hour quota windows if necessary; do not rush to an early conclusion.

At the end of every pass, generate validated artifacts before publishing any completion message:
- all six candidates have been covered; every active source file has a file-level accounting entry with read/index status, potential normative hotspots, inspected relevant line ranges, and reason for any deferred deeper reread;
- each new hypothesis has exact, verified source path/range and quotation, with trigger, modality, domain, and why an earlier claim does not already express it;
- candidate-specific `NOVEL_CLAUSE` and `RECLASSIFICATION_CANDIDATE` entries are added with stable IDs to append-only `NOVEL_FINDINGS.jsonl` (or upserted by stable ID with an auditable revision log); uncertain cases remain in `UNRESOLVED_FINDINGS.jsonl`;
- each claim has a recorded semantic baseline comparison, including prior candidate records considered and why they are or are not equivalent;
- write `PASSES/pass_NNNN/` reports and checkpoint, validate, give a short in-session report, then immediately start the next pass.

**Convergence / termination contract (FINITE `REPEAT ... UNTIL`):**

Run one complete six-candidate pass, validate and persist its evidence, then test the stopping condition. Repeat only while the stopping condition is false and execution resources permit. A pass finding zero new claims is a real, valid result; do not manufacture novelty to keep working. There is no fixed upper bound on the number of passes, but this is **not an infinite loop**. The minimum six strategy families and the two qualifying zero-discovery passes are necessary; unresolved, genuinely plausible issues have the separate qualified stopping path below. The count of five-hour quota resets is not a stopping condition.
- Never stop after a partial pass, a single empty pass, or because the token window is low; save a checkpoint and allow manual resume.
- Before declaring `CONVERGED`, finish **at least all six distinct pass families**, with **two consecutive FULL six-candidate passes** that each find **zero newly verified distinct claims** and **zero newly surfaced plausible unresolved claims needing investigation**. The two zero-discovery passes must use different search methods. Repeated rewordings of existing findings do not count as discoveries; do not inflate counts to force continued work.
- An unresolved plausible new claim that needs adjudication prevents a strong `NO_MORE_PLAUSIBLE_FINDINGS` closure; revisit it using another evidence strategy, or report `SEARCH_SATURATED_WITH_OPEN_ISSUES` instead of claiming convergence. If the ambiguity cannot be resolved from frozen evidence, do not loop forever merely to generate empty guesses: record the blocker precisely and stop with that qualified terminal status once all mandatory searches were done.
- Perform a final **unattributed-normative-clause review** over the complete source/index ledger: every plausible normative clause must be either linked to a baseline finding, linked to a new finding, or explicitly categorized with evidence and an open question where appropriate. A category is not proof of correct interpretation.
- Stopping means **search saturation under these strategies**, NOT mathematical proof that all possible hidden constraints have been found. State this explicitly.

## 4. Outputs and exact schemas (English only)

Create outputs in `stage_A/codex_iterative_search/` ONLY:

- `RESUME.md` — concise, self-contained recovery runbook with stable restart wording and current first incomplete unit.
- `STATE.json` — durable progress and convergence state.
- `SEARCH_PROTOCOL.md` — frozen atomization, novelty, deduplication and pass/stop rules; document revisions and why, without changing already completed pass records.
- `BASELINE_MANIFEST.json` and `BASELINE_RECORD_INDEX.jsonl` — frozen exact input hashes and indexed prior findings/orphans/canonical cross-links, without altering their classifications.
- `SOURCE_FILE_INDEX.jsonl` — all active candidate files, line counts and hashes, paths relative to candidate input root; mark binary/non-text explicitly.
- `NOVEL_FINDINGS.jsonl` — stable ID, candidate, exact path/line/quote, atomic candidate claim and domain, trigger, modality, exceptions, enforcement effect, closest canonical policy IDs (possibly empty), baseline comparisons (specific old record IDs or reason a match does not exist), discovery strategy/pass, concrete distinguishing behavioral scenario, `NOVEL_CLAUSE` or `RECLASSIFICATION_CANDIDATE`, evidence verification status and current confidence. Do not call these proven EXTRA.
- `UNRESOLVED_FINDINGS.jsonl` — plausible new clauses where evidence, normativity or novelty is not yet established; preserve exact question and candidate source. Include reproducible suspect cases even if no confident classification is possible.
- `ALREADY_COVERED_SAMPLES.jsonl` — selected positive and negative baseline-matching examples, including hard cases with same location but distinct clauses. This is an audit trail of the novelty decision rather than a complete duplication of all already known claims.
- `PASSES/pass_NNNN/`: `PASS_PLAN.md`, `FILE_COVERAGE.jsonl`, `CANDIDATE_CLAIMS.jsonl`, `NOVELTY_COMPARISONS.jsonl`, `PASS_VALIDATION.json`, `PASS_REPORT.md`, and checkpoint hashes. The first three file types can be produced incrementally; final pass report must record counts per candidate and be immutable after the pass closes.
- `SEARCH_DECISION_LOG.md` — contentious merges, rejected candidates, previously dismissed clauses, methodology cautions and actual verification activities (no invented command results).
- `VALIDATE_ITERATIVE_SEARCH.py` — local read-only validator verifying all expected input file hashes, per-pass candidate/file coverage, record/schema/id uniqueness, referential integrity, exact quotation matches, monotonic durable pass IDs and append-only/revision history, plus the mechanically checkable convergence gates. This validator **must explicitly not claim to prove semantic completeness**.
- `HANDOFF_TO_CLAUDE.md` — when done or interrupted, a reviewer-friendly account of new candidates and unresolved items **only**, with evidence paths, likely overlaps, risk, and how a fresh Claude can independently verify and import valid discoveries into its Stage 1 union later. Do not edit `step1_union` yourself.
- `FINAL_REPORT.md` — complete search passes, changed strategies, counts of credible new and reclassification candidates, unresolved, validation results and limits. Mark unfinished work accurately if interrupted.

Simple JSONL conventions: UTF-8, one JSON object per line; source paths relative to `inputs/<candidate>/`; candidate names exact; immutable source quotes byte-accurate (allow newline normalization only when documented); stable IDs across resume. Source segment IDs from different runs must never be conflated. Findings can be confirmed as **source-verified** while still **not normatively adjudicated**.

Persist at file/batch granularity and at each candidate and pass boundary. You may implement local helper scripts for indexes and validation, but do not modify scripts or outputs created by other agents.

## 5. Strict mobile resume and quota interruption protocol

**Primary and preferred user resume message in the SAME Codex session:**

`Continue 5.4`

Treat this exact short English command as an instruction to resume the saved task; do not require a longer prompt.

On receiving it, without requesting a longer prompt:
1. Read this task (`_STAGE_A_KIT/21_CODEX_ITERATIVE_SEARCH_TASK_EN.md`), `stage_A/codex_iterative_search/RESUME.md`, and `STATE.json`.
2. Verify source/baseline fingerprint; do not consume or follow newly produced Claude reconciliation files.
3. Check the last committed candidate/file unit and whether a partially written file needs to be retried; do not trust progress claims without saved output and validation.
4. Continue the **same iterative search**, at the first incomplete unit or next pass, using the original frozen protocol and six-pass diversity requirement.
5. Do not redo verified earlier batches, reinitialize outputs, reset pass counter, discard ambiguous items, or end early merely because an earlier pass yielded no new candidate.
6. Send one short progress sentence, then immediately work. Do not wait for approval between files, candidates or passes.

**If the original conversation history is lost or a NEW Codex session is required**, a phone-sized recovery message is:

`Read stage_A/codex_iterative_search/RESUME.md and continue.`

A single word cannot guarantee a NEW session will find the correct task. Thus `RESUME.md` is required from the first action and must remain self-contained and current.

A usage-limit error may terminate the current Codex execution. **Do not claim you can operate in the background, wait for reset, or automatically restart the session.** Save frequent checkpoints while execution is available; user can manually send the short resume message after quota availability returns. Never represent a scheduled or automatic action as configured.

## 6. Independent evidence and handoff boundary

- This search is a fourth *research method*, not a majority-vote final arbiter. Previous baselines and new candidates are all hypotheses pending source-grounded review.
- Do not label a new record as a confirmed 5.3 blocker, confirmed `EXTRA`, or proven six-way parity defect. Do not edit any of the 196 policies.
- No Stage 1 union import, Stage 2 classification, Stage 3 parity matrix, Stage 4 unification, or code generation in this task.
- Do not read `stage_A/reconciled/step1_union/**` at any time, even if it completes during your search; this prevents feedback contamination and file contention. Claude will reconcile **your frozen findings afterward** in a separate task.
- Do not mistake test or exemplar snippets for active project obligations without considering their loading/trigger semantics; conversely, do not dismiss conditional procedures simply for living in skills or scripts.
- Structural `PASS` is evidence of accounting, not proof that no unreported normative clauses remain.

Start by writing `RESUME.md` and `STATE.json`, then checking that all six inputs and three completed research baselines exist. Once validated, begin Pass 0001 and keep going until the convergence contract is satisfied or an actual resource/tool block interrupts execution.
