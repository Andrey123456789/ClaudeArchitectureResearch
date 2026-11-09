# Experiment 005 / Phase 5.4 — Stage A, Step 1: Evidence-Preserving Union

## Scope and purpose

Produce **one traceable, candidate-aware union of findings from three independent research runs**. This is a **data reconciliation and deduplication task**, not a fresh audit and not a normative adjudication task.

The three completed runs previously disagreed strongly on what was labeled `EXTRA`. The immediate objective is **not** to make their counts converge. It is to ensure that every distinct *claimed constraint* survives once in a reconciled registry, with every original observation and disagreement retained. A group's existence is **not** evidence that the claim is correct, mandatory, extra, applicable, or experimentally significant.

### Explicitly out of scope

- No edits to the six architectures, their policies, skills, scripts, hooks, or configuration.
- No addition, deletion, or rewriting of the 196 canonical policies.
- No decisions about `ORACLE_LINKED` versus truly `EXTRA`, `INTERNAL`, `NON_NORMATIVE`, etc. Preserve previous labels as **attributed claims**, not validated labels.
- No cross-architecture parity verdict (`SAME`, `STRICTER`, `WEAKER`, `DIFFERENT`) or behavioral equivalence decision.
- No decisions on which restrictions to enforce or remove; no 5.4 unification.
- No additional generation of a full independent findings inventory, and no new fourth full source sweep.

## 0. Environment, inputs, and safeguards

Use working root:

`C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.4`

Exactly six candidate names in 5.4: `M`, `M1`, `L0`, `L1`, `K0`, `K1`. **Do not reintroduce `L1-Restart`**. The 5.3 snapshot is historical and is not a working input for this task.

Authoritative immutable sources and canonical policies: `inputs/<candidate>/` and `inputs/INPUT_MANIFEST_SHA256.csv`.

For each candidate, the three **read-only** finding sources are:

1. `stage_A/primary/<candidate>/constraints.jsonl`, `policies.jsonl`, `ORPHAN_CANDIDATES.jsonl`, `coverage_ranges.jsonl`, and `files.jsonl` (plus progress/reports for context only).
2. `stage_A/replica/<candidate>/constraints.jsonl`, `policies.jsonl`, `ORPHAN_CANDIDATES.jsonl`, `coverage_ranges.jsonl`, and `files.jsonl`.
3. `stage_A/independent/<candidate>/blind/BLIND_FINDINGS.jsonl`, `FILE_REVIEW_LEDGER.jsonl`, `BLIND_COMPLETE.json`, and associated evidence/validation files.

Read both Claude runs **including** all `ORACLE_LINKED` and `LINK_UNCERTAIN` records, not only `EXTRA`. An independently found constraint may already be covered by a canonical policy according to one extractor and labeled additional by another. Dropping `ORACLE_LINKED` records destroys precisely this evidence.

Read Codex `BLIND_FINDINGS.jsonl` as **hypotheses**; a `POTENTIAL_EXTRA` label is not a confirmed finding. Some Codex records quote a *long paragraph containing multiple independent claims*; do not merge the paragraph as though it represented only one constraint.

The policy files provide cross-references to the 196 original policies. The orphan records provide candidate passages and original dispositions; a linked `EXTRA_REGISTERED` orphan and its constraint do **not** become two new rules. Orphan records labeled `NON_NORMATIVE` or `DUPLICATE` still require accounting, but do **not** automatically become claimed constraints.

Never modify `inputs/**`, `stage_A/primary/**`, `stage_A/replica/**`, `stage_A/independent/**`, or other historical research results. Write ONLY to `stage_A/reconciled/step1_union/**`. Create that directory if absent. If it already contains files, inspect and resume without deleting or rewriting valid work.

Preflight: inventory the actual records and their schemas, record the source file SHA-256 hashes, confirm all six completed independent runs are present, and verify the input snapshot manifest using existing read-only tools. For the archived completed run previously inspected, expected raw counts were **5,131 primary constraints; 1,765 replica constraints; 813 Codex findings; 1,176 policy rows in each Claude run; 1,626 primary orphan rows; and 396 replica orphan rows (12,083 indexed source records total)**. Recompute these from the actual current files; investigate any discrepancy rather than silently treating the figures as authoritative. If source files are missing or mutable, stop and report rather than fabricate data.

## 1. Define a consistent unit of comparison BEFORE merging

A **candidate constraint claim** is the smallest independently falsifiable normative proposition, expressed as:

- actor / subject;
- action or prohibition;
- target / artifact;
- trigger and applicability scope;
- strength / modality (must, must not, default, should, conditional, etc.);
- exceptions / approvals / escape conditions;
- lifecycle or sequencing, if behaviorally material.

Split a source passage into two claims **only when one could be satisfied while the other is violated under an otherwise identical scenario**. Do not split a mere list of synonyms or illustrations into new obligations. A sentence may contain several independently falsifiable claims. Conversely, duplicate quotations of the same obligation in several files do not create several distinct requirements, although every occurrence must be retained.

A Codex finding may yield several clauses; a Claude constraint may cover multiple clauses. **Input-to-output links are many-to-many.** Retain source-record references for every split and join.

Do not atomize mechanically by punctuation, line breaks, `and`, or `must`. Use the substantive behavior and applicability. When in doubt, preserve separate claims and an `UNRESOLVED_MERGE` note rather than merge destructively.

For tracking, distinguish:

- **source occurrence:** exact file path, line range, quotation;
- **source clause:** one independent claimed obligation in that occurrence;
- **finding group:** one hypothesized effective obligation **for one candidate**, supported by one or more source clauses / run records.

Do **not** merge across candidate boundaries into a single record. Cross-candidate conceptual similarities may be noted as nonbinding candidate links for future steps, but each candidate's evidence must remain independently inspectable.

Before large-scale clustering, produce `MERGE_PROTOCOL.md` with the frozen unit-of-account definition, merge predicates, negative examples, stable ID scheme, and handling of compound/ambiguous findings. Test it on a small mixed pilot from all three runs (including one identical-looking but differently scoped pair). Record the pilot decisions and failure modes. Apply the protocol consistently across all six candidates. Do not silently rewrite the protocol to make later totals look closer; record any necessary correction and the scope of re-validation.

## 2. Merge criteria (strict and conservative)

Two claims for the **same candidate** may be `EXACT_DUPLICATE` if their effective normative propositions and conditions are textually identical after harmless normalization (whitespace, case, typographic punctuation).

They may be `SEMANTIC_DUPLICATE` only if both are equivalent with respect to **all** normatively relevant dimensions above, including scope, strength, exception, and timing. Record a short explanation and traceable supporting citations.

**Never merge solely because** of the same policy ID, source line range, shared keywords, source file, similar descriptions, or a third model's opinion.

Distinguish and **preserve separately**:

- `RELATED_BUT_DISTINCT`: overlap, example-versus-general rule, or a broader/narrower obligation;
- `APPARENT_CONFLICT`: possible incompatible instructions;
- `UNRESOLVED`: insufficient evidence for equivalence, modality, source attribution, or scope.

These are *merge-review relations*, not Stage 2 verdicts. A broader rule and a narrower rule are not semantic duplicates. A `MUST` and a `SHOULD` are not semantic duplicates. A procedural hook reminder and an unconditional product requirement are not automatically duplicates. A permission/exception is a distinct substantive claim when it changes allowable behavior.

Do not throw away the weaker, broader, narrower, or ambiguous formulation. Do not vote among the three agents. Include every original agent classification as `reported_by_run`, with no adjudicated `origin` or `correctness` label.

If a record provides no sufficiently precise evidence, keep a `NEEDS_EVIDENCE` unresolved item rather than invent a source location.

## 3. Evidence and source handling

- Preserve each source record's original run, candidate, record type, original ID, original label, original text, and source-file relative path / record number (or raw-record hash). Use stable keys such as `PRIMARY:M:CONSTRAINT:EXTRA-M-0001` (plus row ordinal if any IDs collide).
- For primary/replica constraints, resolve `evidence_segment_ids` through the **matching run's** `coverage_ranges.jsonl`. The same segment ID in another run does not constitute the same evidence. Use `inputs/<candidate>/output/template/...` for source text. Resolve paths relative to the candidate root, not project root.
- For Codex, use `path`, `start_line`, `end_line`, and `quote`; a multi-line quotation may contain more than one atomic claim.
- Do not copy a fabricated or paraphrased fragment into a field marked `exact_quote`. Quote exact source text. Store normalized meaning separately.
- Do not use the byte hash of the model-generated summary as the sole semantic identity. Generate deterministic persistent clause IDs based on candidate, verified source location, and exact excerpt (with a suffix for two distinct clauses sharing a source span); maintain an explicit mapping ledger. Never use `EXTRA-...` IDs as semantic keys across runs.
- Keep different documents or different source occurrences linked to the same finding group, but preserve every location individually.
- If a prior extractor assigned a possibly wrong policy ID, **retain that assignment as a claim**; Stage 2 will decide applicability.
- Where exact source/quote verification cannot be established, mark `SOURCE_UNVERIFIED` and explain the reason. It is not permissible to mark the group `VERIFIED` by inference.

## 4. Work sequence — all six candidates in one session

Process candidates sequentially: `M`, `M1`, `L0`, `L1`, `K0`, `K1`.

For each candidate:

A. Mechanically index **all** original constraints from both Claude runs, all Codex blind findings, all policies cross-reference rows, and all orphan entries. Preserve raw records or hashes and their original filenames and line numbers.

B. Resolve source evidence locations. Extract **source-grounded candidate clauses** from overlapping source quotations and split compound findings conservatively. A broad Codex quote must not swallow smaller independent claims.

C. Assign the clauses to conservative per-candidate finding groups. Retain precise `EXACT_DUPLICATE`, `SEMANTIC_DUPLICATE`, `RELATED_BUT_DISTINCT`, `APPARENT_CONFLICT`, and `UNRESOLVED` relations with reasons.

D. Preserve `ORACLE_LINKED`/`EXTRA`/`LINK_UNCERTAIN` and Codex `POTENTIAL_*` labels as *source claims*, and preserve their closest-policy IDs; do not decide the correct category.

E. Cross-reference `ORPHAN_CANDIDATES.jsonl` with the findings via its original constraint IDs, paths and quotes. Preserve even excluded/originally non-normative orphan records in the input ledger for Stage 2 re-examination; do not silently discard them or count them as new rules.

F. Run structural and provenance validation. Save an immutable candidate completion checkpoint, send a short progress message **in the session** with record counts, candidate groups, unresolved merges, and verification gaps, then immediately continue to the next candidate. No approval pauses.

Use ordinary local Python/scripts for indexing, stable identifiers, deterministic source hashing, and validation; reserve model reasoning for real semantic equivalence decisions. Batch by files or source clauses to stay within context. Never infer matching from a numeric similarity score alone. Keep resumable intermediate outputs inside the allowed Step 1 directory. Do not rewrite earlier verified candidates merely because a later candidate uses different terminology.

## 5. Deliverables (all in English)

Output root: `stage_A/reconciled/step1_union/`.

Provide at least:

1. `MERGE_PROTOCOL.md` — fixed grouping/atomization rules and documented pilot, written before full-scale merging.
2. `SOURCE_RECORD_INDEX.jsonl` — **lossless** index for every primary, replica and Codex input record, including policy mappings and orphan candidates. Contains run, candidate, type, original ID, original label, input filename, ordinal, raw-record hash, and the original content or an unchanged exact pointer to it. Different input record types must remain distinguishable.
3. `SOURCE_CLAUSES.jsonl` — candidate/source-path/line/quote-level clauses, deterministic clause ID, normalized *claimed* action, modal/scope/exceptions **as reported or explicitly marked unknown**, and links to original input record keys. A record supporting multiple clauses must link to all of them.
4. `MERGED_FINDINGS.jsonl` — per-candidate groups: stable group ID, neutral claim text, linked source clause IDs, source record keys, supporting run set, original labels, original claimed policy IDs, and explicit merge rationale. Group IDs must not silently change on resume.
5. `RECORD_ACCOUNTING.jsonl` — disposition for **every** source record (`LINKED_TO_FINDING`, `POLICY_CROSS_REFERENCE`, `ORPHAN_CONTEXT_LINKED`, `ORPHAN_PENDING_REVIEW`, or `UNRESOLVED`) and zero, one, or many destination group/clauses as appropriate. All primary/replica `constraints.jsonl` records and all Codex findings must map to at least one finding group **or** be explicitly unresolved; none may be silently dropped. All orphan/policy rows must also be accounted for.
6. `MERGE_REVIEW_QUEUE.jsonl` — linked records/groups that cannot confidently be merged, broader/narrower relations, apparent conflicts, nontrivial source disagreement, and missing evidence. Include exact sources and the specific open question. A singleton confidently retained as unique is not automatically a defect.
7. `SOURCE_VERIFICATION_ISSUES.jsonl` — quote mismatches, ambiguous segment mapping, incomplete citations, and other source verification failures; may be empty.
8. `VALIDATE_STAGE1_UNION.py` — **executable deterministic validator**. Check required files/fields, six-candidate coverage, unique IDs, input-record accounting against the current original JSONL files, referential integrity across all ledgers, no orphaned source-record key, no deleted or modified source input, and whether declared evidence locations and exact excerpts really match the immutable files. Report false-success cases as errors, never suppress them. The validator checks structural completeness, **not** correctness of semantic equivalence; state this plainly.
9. `STEP1_UNION_REPORT.md` — per-candidate and total input records by run/type, merged finding groups, exact versus semantic deduplications, all singleton/unique claims, uncertain cases, provenance quality, validation results, methodological limitations, and instructions for Step 2. Explain that different agent counts are not comparable without a stable unit of account.
10. `CHECKPOINTS/` — per-candidate validated progress and SHA-256 of relevant inputs and completed output files.

JSONL files must contain parseable UTF-8 JSON objects, one per line, with valid unique IDs where applicable. Prefer stable names and well-defined schemas over narrative-only reports. A human-readable examples section in the report should demonstrate one valid deduplication, one intentionally non-merged broader/narrower pair, and one suspicious Codex finding retained rather than validated.

## 6. Mandatory acceptance checks

**Fail/uncertain rather than claim success** if any of the following applies:

- A candidate or a run is absent, incomplete, or corrupted.
- A primary/replica constraint or Codex finding is missing from accounting.
- An orphan record was silently omitted because it was originally labeled non-normative.
- Policies or orphans were accidentally counted twice as independently confirmed rules.
- A many-to-many mapping was collapsed into an unsupported one-to-one link.
- A source quote was asserted exact but not supported by immutable file contents.
- Duplicate decisions omit the relevant scope, modality, exceptions or timeframe.
- Any original input or original analysis output was changed.
- Provenance was erased or original `ORACLE_LINKED`/`EXTRA`/`POTENTIAL_*` classifications were silently rewritten.
- Stage 2–4 conclusions (true EXTRA, strictness, canonical policy changes, repair) appear as accepted decisions.

At the end, run the validator. Include its actual result (PASS / PASS_WITH_OPEN_ISSUES / FAIL), counts of unresolved items, source verification issues, and input hashes in `STEP1_UNION_REPORT.md`. Do not invent completeness metrics. State precisely what has and has not been verified.

The proper Step 1 success criterion is **traceable union + conservative, defensible deduplication + no lost evidence**, not identical agent counts or zero unresolved disagreements. Maintain the ability to adjudicate every original finding during Step 2.
