# Codex Pass 0001: Adjudication and Non-Destructive Union Augmentation

Experiment 005, phase 5.4, Stage A. Task: `_STAGE_A_KIT/31_CLAUDE_CODEX_PASS1_REVIEW_TASK_EN.md`. Augmentation version `step1-union-augmented-pass1/v1`. Review date 2026-11-02.

This review adjudicates the completed first pass of the Codex iterative search against the completed Step 1 union. It does not decide EXTRA versus the 196 oracle policies. It does not compare strictness across candidates, change any original group, or start Stage 2. Every addition below is **provisional**.

## 1. Inputs, scope and integrity

| Item | Value |
| --- | --- |
| Base union | `stage_A/reconciled/step1_union/MERGED_FINDINGS.jsonl`, 6,347 groups (M 995, M1 1,101, L0 965, L1 1,028, K0 1,062, K1 1,196). Base validator re-run at preflight: `PASS_WITH_OPEN_ISSUES`, 0 errors, 0 warnings, 484 input files verified |
| Codex evidence | `PASSES/pass_0001/` only. `PASS_VALIDATION.json`: `COMPLETE`, `source_files` 448, checkpoint hashes verified |
| Revisions applied | Only the four named in `PASS_VALIDATION.applied_revisions`: `CIS-M1-0004-R1` (RECLASSIFICATION to ALREADY_COVERED), and `CIS-L1-U0008-R1`, `U0009-R1`, `U0010-R1` (closest policy corrected to RUN-022) |
| Excluded | `PASSES/pass_0002/**` and later (not read). `STATE.json`, `FINAL_REPORT.md` and the handoff file were not used as count evidence |
| Hash pin | `INPUT_HASHES.json`, written before any decision, pins 266 files: the whole Step 1 union tree (160), the pass_0001 tree (98), the three Codex baseline index/map/manifest files, the four revisions and the inputs manifest. All 484 manifest-listed input files are verified against that manifest, and the three rolling Codex files are pinned by a digest of their pass-1 subset. Integrity was re-verified at each of the six candidate checkpoints and at finalisation: **PASS** every time |
| Concurrency note | The Codex search was running while this review ran: `UNRESOLVED_FINDINGS.jsonl` grew with later-pass rows. Its pass-1 subset never changed. This is logged as a warning, and no later-pass row was imported |

**Recomputed accounting (from `CANDIDATE_CLAIMS.jsonl` and the revisions):**

- **Claims:** 152 distinct claim IDs.
  - 60 are in `NOVEL_FINDINGS`, 72 in `UNRESOLVED_FINDINGS` and 20 in `ALREADY_COVERED_SAMPLES`. Each claim is in exactly one of these files and in `NOVELTY_COMPARISONS`, and each rollup row is identical to its source row.
  - These are views of the same 152 claims, not 132 extra records.
- **Original status:** NOVEL 15, RECLASSIFICATION 45, UNCERTAIN 72, ALREADY_COVERED 20.
- **Effective status:** NOVEL 15, RECLASSIFICATION 44, UNCERTAIN 72, ALREADY_COVERED 21.
- **Per candidate:** the effective counts equal `PASS_VALIDATION.effective_counts_by_candidate`.
- **Quotes:** all 152 quotes match their cited line ranges exactly, after newline normalisation only.

## 2. Method

For every claim the reviewer did the following:

1. Read the cited lines with surrounding context (`_tools/show.py`).
2. Mapped every Codex baseline key to its union record and group, including coverage segments and orphans.
3. Inspected the co-located groups and grepped the candidate's union for semantically related groups.
4. Wrote one decision block in `_review/<C>.rev`. Each block records the source nature, actor, action, trigger, modality, scope, exceptions, timing, enforcement and loading. It also names the matched or compared groups, gives a rationale, a distinguishing scenario and a confidence.

For code, only static control flow was read. Nothing was executed, and the Codex probe results were not re-run.

Decisions were compiled deterministically by `_tools/build.py` and frozen per candidate by `CHECKPOINTS/<C>.checkpoint.json`.

**Conventions applied identically to all six candidates:**

- **Facet versus new clause.**
  - **Facet:** use when an existing group cites the same passage or mechanism but drops a condition, an exception or an acceptance boundary. Protocol rule F6 applies: text cited by the group but not stated in it. A facet uses `NEW_GRANULARITY` when it makes something already implied explicit, and `NEW_BEHAVIOR_BOUNDARY` when the allowed or forbidden behaviour actually changes.
  - **New clause (`DISTINCT_UNREPRESENTED_CLAUSE`):** use only when no same-candidate group covers the actor, action and trigger at all.
- **Hooks and checkers.**
  - Designed trigger or acceptance predicates that a group states too broadly become facets. Examples: lexical dispatch checks, single-group registration, the inline-`paths` parser, marker regexes, the `PostToolUseFailure` channel.
  - Incidental edge effects of helpers and silent failure modes are recorded as `NOT_AN_INDEPENDENT_CONSTRAINT`, with an enforcement observation. Examples: the `'..'`-prefix containment test, rename-source parsing, `git status` failure, unreadable directories.
- **Normativity.**
  - Every candidate's ownership headers mark knowledge skills as technique holders: "(no policy)", "Technique only", "Kind: KNW".
  - Declarative or permissive wording ("may contain", "a useful structure", "consider ... when justified"), technique contrasts (FindAsync vs LINQ), API decision tables (`IOptions*`) and library prerequisites (`Enrich.FromLogContext`) were not promoted to rules, unless an existing group already registered them.
  - Imperatives in workflow skills and their private references, such as scan-layer prompts and reference-loading restrictions, were treated as procedural duties.
- **Loading routes.**
  - Plain "read reference X for topic Y" pointers are a loading mechanism. Their content is already represented through the reference's own groups, so they are `NOT_AN_INDEPENDENT_CONSTRAINT`.
  - An explicit negative default ("not all of them by default") is an independent instruction-architecture restriction.

## 3. Results per candidate

AR = ALREADY_REPRESENTED, FX = EXISTING_GROUP_NEEDS_EXPLICIT_FACET, DC = DISTINCT_UNREPRESENTED_CLAUSE, NI = NOT_AN_INDEPENDENT_CONSTRAINT, UR = UNRESOLVED.

| Candidate | Claims (N/R/U/AC effective) | AR | FX | DC | NI | UR | Proposals | Facets | Queue items |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| M | 34 (3/9/9/13) | 13 | 7 | 1 | 13 | 0 | 1 | 7 | 2 |
| M1 | 31 (6/8/13/4) | 6 | 7 | 5 | 12 | 1 | 5 | 7 | 3 |
| L0 | 17 (2/5/9/1) | 1 | 4 | 3 | 9 | 0 | 3 | 4 | 3 |
| L1 | 25 (3/6/15/1) | 3 | 4 | 5 | 13 | 0 | 5 | 4 | 2 |
| K0 | 30 (1/11/16/2) | 2 | 7 | 8 | 13 | 0 | 8 | 7 | 4 |
| K1 | 15 (0/5/10/0) | 0 | 0 | 4 | 11 | 0 | 4 | 0 | 3 |
| **Total** | **152 (15/44/72/21)** | **25** | **29** | **26** | **71** | **1** | **26** | **29** | **17** |

### Effective Codex status by final disposition

| Effective status | AR | FX | DC | NI | UR | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| NOVEL_CLAUSE | 0 | 10 | 5 | 0 | 0 | 15 |
| RECLASSIFICATION_CANDIDATE | 0 | 11 | 21 | 12 | 0 | 44 |
| UNCERTAIN_NOVELTY | 5 | 7 | 0 | 59 | 1 | 72 |
| ALREADY_COVERED | 20 | 1 | 0 | 0 | 0 | 21 |

By original status, the only difference is CIS-M1-0004. It is originally RECLASSIFICATION (45) and was finally ALREADY_REPRESENTED, as its revision states.

Reviewer confidence: HIGH 59, MEDIUM 92, LOW 1. The single LOW is the unresolved claim. 25 of the 26 distinct clauses are MEDIUM.

## 4. What survived

### The 15 NOVEL claims

- **5 survived as distinct clauses:**
  - CIS-M1-0007: binds entry needs a reason (checker ERROR).
  - CIS-M1-0008: unused frame binding (checker WARN).
  - CIS-L0-0006 and CIS-L1-0007: review untrusted NuGet sources.
  - CIS-L1-0002: run frontend commands from the workspace directory.
- **10 are refinements of existing groups (facets), not new rules:**
  - Checker gates: CIS-M-0004 (lexical event dispatch), CIS-M-0005 and CIS-L0-0004 (one registration must cover all tools), CIS-L1-0003 (inline `paths` rejected).
  - Hook triggers: CIS-M1-0002 (no notes on the initial snapshot), CIS-M1-0003 (token predicate on new text only).
  - Product guidance whose existing group dropped half of the cited sentence: CIS-M-0009 and CIS-M1-0011 (keyed services "not when a simpler option is clearer"), CIS-M1-0012 and CIS-K0-0009 (304 "carries no representation").
- **None was a plain duplicate.**

### The 44 effective RECLASSIFICATION claims

All 44 were resolved: 21 distinct, 11 facets, 12 not independent.

- **Distinct clauses:**
  - project-structure selective reference loading (M, M1, L0, L1, K0)
  - scan-layer review steps: NuGet sources (M1, K0), lockfiles (M1, L0, L1, K0, K1), production debug flags (L1, K0, K1)
  - manifest-checker fail-closed errors: K0 malformed XML and undecodable files, K1 invalid JSON and unreadable files
  - K0 code-fence errors (an unclosed fence, and a closing fence that is not exactly three backticks)
- **Facets:**
  - the failed-command `additionalContext` channel (M, K0)
  - the snapshot silence (M)
  - inline `paths` and quoted skill names (M, M1, L0, L1)
  - the commit-body "do not narrate the obvious diff" clause (L1)
  - the repository-wide scope of the empty-directory error (K0)
- **Not independent:**
  - all six EditorConfig `root = true` claims
  - three plain loading routes in M
  - the caching attach-mechanism technique (M, M1)
  - the Serilog override remedy (M1)

### The 72 UNCERTAIN claims

71 were resolved with stated evidence; 1 was retained.

- **5 already represented:**
  - CIS-M1-U0001 and U0002: silent EditorConfig style settings, present as part of Codex group FG-M1-50ce19e2ed.
  - CIS-L1-U0007: provider-based HttpClient setup, covered by the standalone/NgModule rules.
  - CIS-L1-U0014 and CIS-K0-U0015: the hedging decision-table rows, covered by the hedging-safety and measurement-preference groups.
- **7 facets:** the headless "do not wait" (M), the record-semantics exception (M1), the 304 body (L0), the retry-key whitespace normalisation (L1), the two K0 marker regexes, and K0 inline `paths`.
- **59 not independent:** technique/descriptive/permissive text, API tables, library prerequisites, and incidental hook/checker edge effects. Each carries its evidence: ownership header, wording, the Claude runs' explicit rejections, and the registered rule that governs the outcome.
- **1 retained as UNRESOLVED (`AUG1-UR-CIS-M1-U0011`):** whether "Arrange / Act / Assert is a useful **default** structure" is a registrable PREFER-strength recommendation. Evidence points both ways, and forcing it would create an artificial representation difference.

### The 21 effective ALREADY_COVERED claims

- **20 confirmed.** This includes the revised CIS-M1-0004. The split replica part `EXTRA-M1-0012#b` in FG-M1-90ed13d72d states "post-tool and Stop hooks report failures visibly without blocking", and the code (hook-output.js lines 5-7 and 49-52) agrees.
- **1 refined to a facet: CIS-K0-C0002.** The "a test may construct `new HttpClient(testHandler)`" permission appears only as a cited evidence quote. The group text and the member scope fields (which include `backend/**/*.cs`) do not state it.

## 5. Examples per disposition

| Disposition | Example | Why |
| --- | --- | --- |
| ALREADY_REPRESENTED | CIS-P0001-M-C0004, the 30 s fail-closed PreToolUse guard | FG-M-d05bc59108 and FG-M-f268d4b313 state the timeout, the shell-wide trigger and the block on failure |
| FACET (new behaviour boundary) | CIS-M-0002 → FG-M-89479fb15b | `postToolBlock` exits after emitting `additionalContext` for `PostToolUseFailure`, so a failed command never receives `decision:block`. The group says violations are "returned as a blocking reason" |
| FACET (new granularity) | CIS-M-U0004 → FG-M-2b1be76983 | "do not wait" sits in text the group cites (architecture-decision lines 37-39) but is only implied by "proceed only ... and report" |
| DISTINCT | CIS-M1-0007 → AUG1-NC-CIS-M1-0007-a | check-instructions.js line 387 errors on any binds entry without a reason. No M1 group or instruction text mentions the requirement |
| NOT INDEPENDENT | CIS-M-U0008 (FindAsync vs LINQ) | The line closes a FindAsync section of a skill that declares itself "(no policy)". LINQ as default and the raw-SQL gate are already registered |
| UNRESOLVED | CIS-M1-U0011 | See section 4 |

## 6. Unresolved issues and observations (`UNRESOLVED_REVIEW_QUEUE.jsonl`, 17 items)

- **1 unresolved disposition:** CIS-M1-U0011, as above.
- **7 methodology items, revisit together:**
  - six of them: `root = true`, one per candidate, to revisit if Stage 2 counts configuration-inheritance boundaries as constraints;
  - one: the loading-route claims CIS-M-0010/0011/0012, to revisit if Stage 2 treats them as process duties.
- **7 "same line, other items":** scan-layer lines (M1, L0, L1, K0 ×3, K1) whose other listed review items also appear unregistered. They were not extracted, because extraction beyond the cited claims is out of scope.
- **1 attribution check:** primary group FG-L0-69195df14f says an unknown hook event "exits 2". The code exits 1, because only `pre-bash` fails closed.
- **1 possible enforcement bypass:** K1 `npm install -- <pkg>` skips the exact-version classifier. This is from static reading only.

## 7. Limitations

- **Static review only.** Every code and configuration claim was verified by reading source and control flow, not by running it. Host semantics are not verified, for example whether `PostToolUseFailure` honours `decision:block`, how quoted YAML is read, and the Git porcelain field order (taken from Git documentation).
- **Judgement calls.** Normativity and facet-versus-clause decisions are reviewer judgements, made under the conventions in section 2. 92 of them are MEDIUM confidence.
- **Same-candidate coverage only.** Union coverage was established within the same candidate, by co-location and targeted grep. A group expressing the same rule from a non-co-located file could have been missed. The base union protocol accepts the same limitation, and it errs towards proposing.
- **No other mappings.** No EXTRA/ORACLE mapping, strictness or cross-candidate parity was decided. The `policy_hint` fields are non-binding.
- **Cross-candidate reads.** Other candidates were consulted only to keep conventions consistent, for example how the base union treats scan-layer prompts. No groups were merged across candidates.

## 8. Is another full search justified?

The verified yield is narrow:

- **Distinct clauses:** 26 of 152 hypotheses (17 %). They fall into four recurring clusters:
  - scan-layer investigation prompts (12)
  - project-structure selective reference loading (5)
  - manifest and instruction checker acceptance errors (8)
  - one working-directory instruction
- **Product rules:** none is a new product-engineering rule. The product-level hits (keyed services, the 304 body, record semantics, the commit-body narration) are omitted halves of sentences that existing groups already cite. They became facets.
- **Facets:** the 29 facets are mostly enforcement-layer boundaries of registered hooks and checkers.

On this evidence, a further *full* multi-strategy sweep is not justified by product-rule yield. Two **targeted** checks are justified by verified gaps:

1. A complete pass over each candidate's security-scan investigation reference. Several items on already-cited lines are visibly unregistered (queue items of type "same line"), and the base runs treated these prompts inconsistently across candidates.
2. A focused review of checker and hook acceptance predicates (parsers, marker and identity tests, fail-closed or fail-open error paths). The base union records these gates at coarse granularity.

Whether to run either check is the user's decision. This recommendation is not a convergence claim for Codex's six-strategy search.

## 9. Validation

Validator: `VALIDATE_PASS1_AUGMENTATION.py`, run as `python -B VALIDATE_PASS1_AUGMENTATION.py`. It re-implements its checks independently and imports nothing from `_tools/`. Its saved result is in `VALIDATION_RESULT.json`.

Actual result of the final run (exit code 0):

```text
RESULT: PASS   errors: 0   warnings: 1
warning: C02: rolling file has later-pass changes (pass-1 subset unchanged, not imported): stage_A/codex_iterative_search/UNRESOLVED_FINDINGS.jsonl
immutable files verified: 266   inputs manifest files verified: 484
ledger: 152 rows = 152 pass-1 claim ids; revisions applied: CIS-L1-U0008, CIS-L1-U0009, CIS-L1-U0010, CIS-M1-0004
original totals: {"ALREADY_COVERED": 20, "NOVEL_CLAUSE": 15, "RECLASSIFICATION_CANDIDATE": 45, "UNCERTAIN_NOVELTY": 72}
effective totals: {"ALREADY_COVERED": 21, "NOVEL_CLAUSE": 15, "RECLASSIFICATION_CANDIDATE": 44, "UNCERTAIN_NOVELTY": 72}
dispositions: {"ALREADY_REPRESENTED": 25, "DISTINCT_UNREPRESENTED_CLAUSE": 26, "EXISTING_GROUP_NEEDS_EXPLICIT_FACET": 29, "NOT_AN_INDEPENDENT_CONSTRAINT": 71, "UNRESOLVED": 1}
UNCERTAIN resolved: 71 / retained UNRESOLVED: 1
proposals: 26   facets: 29   unresolved queue items: 17   augmented view rows: 6402 (6,347 original + 55 provisional)
```

Checks C01-C14: the outputs parse; pinned hashes are unchanged and no file was added to the immutable directories; there is exactly one ledger row per claim; statuses and revisions match; the evidence and quotes match their source files; every FG reference exists and belongs to the same candidate; dispositions and additions are consistent; proposal and facet IDs are deterministic and traced to a reviewed claim, with no duplicates; facet targets are byte-identical to the base groups; checkpoints match their files; the augmented view retains all 6,347 original groups unchanged; the manifest counts and hashes are consistent.

## 10. Files

- **Main outputs:** `INPUT_HASHES.json`, `PREFLIGHT_REPORT.json`, `REVIEW_QUEUE.jsonl` (canonical 152-claim queue), `PASS1_REVIEW_LEDGER.jsonl`, `NEW_CLAUSE_PROPOSALS.jsonl`, `EXISTING_GROUP_FACETS.jsonl`, `UNRESOLVED_REVIEW_QUEUE.jsonl`, `UNION_AUGMENTATION_MANIFEST.json`, `AUGMENTED_UNION_VIEW.jsonl` (6,347 original groups unchanged, plus 26 provisional clauses and 29 provisional overlays), `STATS.json`, `PROGRESS.json`, `VALIDATION_RESULT.json`.
- **Per candidate:** `per_candidate/<C>/*` and `CHECKPOINTS/<C>.checkpoint.json`.
- **Reviewer decisions:** `_review/<C>.rev`, plain text, one block per claim.
- **Tools:** `_tools/` (`preflight.py`, `show.py`, `build.py`, `finalize.py`, `aug_lib.py`).
