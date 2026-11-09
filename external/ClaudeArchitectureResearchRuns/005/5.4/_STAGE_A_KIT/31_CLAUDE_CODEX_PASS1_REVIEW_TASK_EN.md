# Experiment 005 — Phase 5.4 — Stage A: Codex Pass 0001 Independent Adjudication and Non-Destructive Union Augmentation

## 0. Mission and limits

You are performing **one bounded review**, NOT another discovery sweep. Evaluate all findings from the **completed first full pass** of Codex Iterative Search against the **completed three-run Step 1 union**, verify evidence and novelty, and produce an independently reviewable *augmentation* of that union. Your goal is reliability, not maximizing the count of additions.

Do **not** finalize whether a finding is `EXTRA` versus one of the 196 canonical policies, determine cross-candidate stricter/weaker relationships, harmonize requirements, modify architecture templates, or execute Stage 2–4. An assertion in a source is not necessarily an applicable engineering rule: distinguish product behavior, workflow enforcement, architecture-internal rules, examples, and conditional loading, while leaving unresolved cases open.

Working root: `C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.4`.

## 1. Authoritative read-only sources

- `inputs/` — immutable candidate snapshots for `M`, `M1`, `L0`, `L1`, `K0`, `K1`, including the 196-policy oracle. Use these to verify **exact citations and full surrounding context**.
- `stage_A/reconciled/step1_union/` — completed initial union. Its authoritative `MERGED_FINDINGS.jsonl` contains 6,347 groups. Also consult `SOURCE_CLAUSES.jsonl`, `SOURCE_OCCURRENCES.jsonl`, `MERGE_DECISIONS.jsonl`, `MERGE_REVIEW_QUEUE.jsonl`, `RECORD_ACCOUNTING.jsonl`, per-candidate files, `MERGE_PROTOCOL.md`, `STEP1_UNION_REPORT.md`, and `VALIDATE_STAGE1_UNION.py` when necessary. The original union is **immutable**.
- `stage_A/codex_iterative_search/PASSES/pass_0001/` — **completed** first pass, especially `PASS_VALIDATION.json`, `PASS_REPORT.md`, `CANDIDATE_CLAIMS.jsonl`, `NOVELTY_COMPARISONS.jsonl`, checkpoints/receipts.
- `stage_A/codex_iterative_search/NOVEL_FINDINGS.jsonl`, `UNRESOLVED_FINDINGS.jsonl`, and relevant `REVISIONS/` — include findings belonging to `discovery_pass == 1` only. These are evidence and annotations, not ground truth.
- `stage_A/codex_iterative_search/BASELINE_RECORD_INDEX.jsonl` and `BASELINE_LOCATION_MAP.jsonl` — use when reviewing Codex's references to the earlier raw audits. Check the actual source when the extracted baseline wording is incomplete.

**Strict exclusion:** do not read, import or adjudicate `PASSES/pass_0002/**` or any later pass, and do not treat mutable `STATE.json`, `FINAL_REPORT.md` or ongoing-search status as proof of first-pass counts. `PASS_VALIDATION.json` and first-pass receipt/checkpoint data take precedence. Do not read `stage_A/reconciled/step1_union_augmented_pass1` as an input unless resuming your own interrupted review.

The expected first-pass effective accounting is **152** claims: **15** `NOVEL_CLAUSE`, **44** `RECLASSIFICATION_CANDIDATE`, **72** `UNCERTAIN_NOVELTY`, and **21** `ALREADY_COVERED`. The original novel queue has 60 entries, of which `CIS-M1-0004` has an auditable revision to `ALREADY_COVERED`; three L1 uncertain records have corrected `RUN-022` policy links. Recompute all counts from authoritative data instead of blindly assuming these totals. Do not mistake the 20 original already-covered claims for 21 effective already-covered claims, and do not double-count entries appearing in multiple indexes.

## 2. Non-destructive output and concurrency

Write **exclusively** under:
`stage_A/reconciled/step1_union_augmented_pass1/`

Create it if absent; never overwrite any original source, original audit, initial union, or ongoing Codex output. The iterative Codex search may resume separately; your review MUST remain pinned to completed Pass 0001 and its documented revisions. Snapshot the exact first-pass input/union file hashes at the start (hash manifest under your output directory). If a relevant first-pass file changes during execution, STOP with an integrity error rather than silently combining versions.

Use stable file names, append-only or atomic checkpoint writes where practical, and support resuming after an interruption. Do not discard verified results from completed candidates. Do not create an alternate source of truth by casually editing union group IDs or changing original source records.

## 3. Preflight: mechanical indexing, not semantic guessing

1. Read original Step 1 merge protocol and verify its output invariants.
2. Confirm all six candidates and `PASS_VALIDATION.json` status `COMPLETE`, `source_files: 448`. Read the first-pass records and effective revisions. Build a canonical **one-record-per-pass1-claim** review queue. Preserve the original finding ID, original/effective status, evidence pointer, candidate, source location, quote, baseline references and revision ID if any.
3. Verify unique claim IDs; confirm that all **152** first-pass candidate claims are accounted for exactly once. The original 60-row `NOVEL_FINDINGS` and 72-row `UNRESOLVED_FINDINGS` are supplementary views of this same set, **not 132 extra records to append**.
4. Index original `MERGED_FINDINGS.jsonl` **per candidate** and supporting source occurrences; never declare equivalence merely because two claims cite overlapping lines, share a technology name or have the same policy ID.
5. Report any missing or corrupt inputs as a blocker. Do not fabricate evidence or silently drop a claim.

## 4. Review protocol — every effective first-pass claim

Process `M -> M1 -> L0 -> L1 -> K0 -> K1` with a concise in-chat checkpoint after each candidate and continue without user confirmation. Give the 131 effectively novel/reclassification/uncertain records close scrutiny; also account for and verify the 21 effectively already-covered cases, including the withdrawn `CIS-M1-0004`.

For EACH claim:

A. **Source truth.** Verify the exact quotation, file and line range against `inputs/<candidate>/output/template/...`; read sufficient surrounding context. Record whether the text actually imposes an obligation, recommendation, prohibition, default, exception, checker's acceptance gate, workflow behavior, or is only a descriptive example/implementation detail. Do not promote a technical parser fact to an unconditional agent-facing instruction. For code/configuration, distinguish statically verified branch behavior from behavior actually tested at runtime.

B. **Effective applicability.** Identify actor, action, object, trigger, modality, scope, exception, sequencing/timing, severity and applicable instruction-loading conditions. Preserve differences among product engineering, workflow enforcement and instruction architecture. A rule in a conditionally invoked skill is not automatically global. Keep uncertainty explicit when the actual host/loading semantics are not verified.

C. **Semantic same-candidate comparison.** Identify the strongest candidate matching groups in the existing union. Compare independent behavioral obligations, not line overlap. Inspect the full group and its evidence; where relevant consult the original raw baseline records. Test equivalence using a concrete *distinguishing scenario*: would one formulation allow an implementation/action that the other forbids under the same trigger, scope and exceptions? Do not call a requirement novel merely because Codex split a compound requirement into more atoms when the prior union already preserved that component.

D. **Disposition (exactly one primary disposition per source claim):**
- `ALREADY_REPRESENTED`: behavior fully present in one or more original groups (including compound claims). Cite exact group ID(s) and supporting clauses.
- `EXISTING_GROUP_NEEDS_EXPLICIT_FACET`: a valid separately testable obligation is implicit or under-specified in a group. Propose a **non-destructive overlay** specifying the missing facet. Distinguish newly recorded granularity from truly new allowed/forbidden behavior; use a distinguishing scenario.
- `DISTINCT_UNREPRESENTED_CLAUSE`: a real normative restriction or enforceable behavioral gate not covered by any same-candidate group, with evidence and a distinguishing scenario. This **does not** yet mean `EXTRA` or cross-architecture divergence.
- `NOT_AN_INDEPENDENT_CONSTRAINT`: descriptive text, a mere implementation step already reflected by a behavior, or an example without enforceable/normative additional content. Explain; do not dismiss executable enforcement blindly.
- `UNRESOLVED`: evidence incomplete or applicability/equivalence genuinely unclear. Specify what evidence is missing, rather than guessing.

E. **Provenance.** Preserve `CIS-*` ID, original Codex status, the effective revision, exact evidence, candidate, matching `FG-*` ID(s), reasoning and any counterexample. If one source finding contains multiple truly independent obligations, represent its subfacets by stable suffixes but **count the original claim once in the 152-claim ledger**; enumerate subfacets separately in proposed additions. Never merge groups from different candidates in Stage A.

F. **Do not adjudicate the 196-policy mapping yet.** You may record suspected policy links and domain, but no final `ORACLE_LINKED` / `EXTRA` ruling or strictness comparison is authorized in this task.

## 5. Required outputs

Create at least:

1. `INPUT_HASHES.json` — exact hashes of authoritative source/union and completed first-pass evidence used; indicate which directories are immutable and the effective revisions applied.
2. `PASS1_REVIEW_LEDGER.jsonl` — exactly one row per source claim (152 expected), with original/effective statuses, final reviewer disposition, matching original group IDs, source evidence, reproducible rationale, distinguishing scenario or reason one is inapplicable, reviewer confidence and unresolved question if any. The original `CIS-*` ID is a required key.
3. `NEW_CLAUSE_PROPOSALS.jsonl` — **only** `DISTINCT_UNREPRESENTED_CLAUSE` proposals, with stable new IDs, same-candidate evidence, exact source location, and trace to reviewer ledger IDs. They are *proposals*, not confirmed `EXTRA`.
4. `EXISTING_GROUP_FACETS.jsonl` — proposed non-destructive enrichments for under-specified existing `FG-*` groups; preserve their original fields, IDs and provenance. No silent reclassification or destructive overwrite.
5. `UNRESOLVED_REVIEW_QUEUE.jsonl` — all unresolved review issues, evidence gaps and next checks. Original 72 uncertain records should be resolved or explicitly retained with an auditable reason; do not force a low-confidence outcome to make counts look better.
6. `UNION_AUGMENTATION_MANIFEST.json` — identify immutable base union, reviewer-ledger coverage, proposed new clauses, proposed facet additions and deterministic identifiers. Permit Stage 2 to assemble an augmented view without losing or changing any original group.
7. `REVIEW_REPORT.md` — exact per-candidate table and totals; counts by original Codex class, effective class and final disposition; how many of the 15 NOVEL survived as distinct clauses versus refinements/duplicates, how many of the 44 RECLASSIFICATION and 72 UNCERTAIN cases resolved, examples of each, limitations, whether additional full search is justified by the **verified** findings rather than raw discovery count.
8. `VALIDATE_PASS1_AUGMENTATION.py` (or equivalent local validator) and the saved actual validation result — verify JSONL validity, 152 distinct ledger IDs exactly equal the pass1 claim IDs, applied revisions, unique proposal IDs, `FG-*` references present and from same candidate, no invented candidate paths, complete evidence/provenance, no duplicate incorporation, unchanged base hashes, and every addition justified by a reviewed source claim.
9. `PROGRESS.json` and/or per-candidate checkpoints for robust continuation.

Optionally generate `AUGMENTED_UNION_VIEW.jsonl` as a **derived** view of all original groups plus explicit proposal records and facet overlays. If generated, prove that all 6,347 original group IDs and claims are retained, and **label additions provisional**. Do not present this as a final classification result.

## 6. Explicit exclusions

- No Phase 5.3 modifications; no changes to `inputs/`, `stage_A/primary/`, `stage_A/replica/`, `stage_A/independent/`, `stage_A/codex_iterative_search/`, or `stage_A/reconciled/step1_union/`.
- No ingestion of incomplete `pass_0002` or later results.
- No fresh global 448-file extraction or another full macro pass; follow citations of first-pass findings only, with enough source context to verify them.
- No treating `NOVEL_CLAUSE` as proven new, `UNCERTAIN_NOVELTY` as false, or pre-existing location overlap as semantic duplication.
- No comparisons of relative strictness among M, M1, L0, L1, K0, K1; no requirement unification, no edits to hooks/skills/checkers, no Stage 2–4 conclusions.
- No artificial convergence claim: this is an adjudication of a completed first pass, **not** completion of Codex's original six-strategy search.

## 7. Done criteria and reporting

You are done only when all 152 first-pass claim IDs are reviewed and accounted for exactly once (including effective revisions), every proposed addition/overlay has verified source evidence and a same-candidate union comparison, the new outputs pass the validator, and no original research artifact was modified. Report a concise candidate-level summary after each candidate; then a final report with counts, unresolved questions, source-integrity status and actual validator output. **Stop after this task**; do not proceed to Stage 2 or restart Codex iterative search.

If interrupted, save atomic checkpoints and update `PROGRESS.json`. On the next continuation, re-read this document and resume after the last validated candidate or claim without redoing valid work.
