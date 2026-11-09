# Final report: Codex Pass 2+3 integration and post-v2 parity closure (Stage A, Step 2 v3)

- **Run folder:** `stage_A/reconciled/step2_controlled_repair_v3/`.
- **Contract:** `_STAGE_A_KIT/74_CLAUDE_STAGE_A_STEP2_PASS23_INTEGRATION_TASK_EN.md`.
- **Resumed on 2026-11-06** under the user's instruction to:
  - finish the V3-D02 gate;
  - test the two residual NuGet/CPM checker-parity issues from the interim review;
  - run the cold audit and write the reports.

**Status: COMPLETE, PASS_WITH_DOCUMENTED_NOT_RUN.**
- All nine v3 changes hold PASS checkpoints.
- The separate cold audit (attempt 3, final) gives 263 PASS, **0 FAIL**, 35 NOT_RUN and 9 FINDING. It re-ran all 44 suites on the final bytes: 3,416 PASS, 0 FAIL, 32 NOT_RUN.
- Step 3 was not started.
- **Recommendation for Step 3: CONDITIONAL_GO**, with the conditions in section 10.

This is a self-audit by the same model family that produced the data. It is not independent validation.

## 1. Executive findings

1. **Codex Pass 2 and Pass 3 add no new study-level obligation.**
   - The 211 records (63 + 148) fall into 30 unique semantic issue clusters, and 11 of them have a normative effect.
   - What they add:
     - 18 records for security-scan prompts that the extraction runs missed in some candidates although the text is there. This is uneven extraction, not a template difference.
     - 14 facet rewordings of existing records.
   - One real candidate text difference was found: L0 lacks the server-rendered raw-HTML scan sentence. It is left as it is, for your decision (Q-01).
2. **The four approved corrections are implemented**, each in its own gate with full cumulative regression:
   - PV2-01: Git `ask` in M, M1, L0, L1 and K1;
   - PV2-02: fail-closed hook input in M and M1;
   - PV2-03: no root mandate for the K0 central file;
   - PV2-04: the M frontend-test ban.
3. **Both residual checker-parity issues were confirmed with real MSBuild and NuGet, and corrected under already-approved semantics**, each as its own gated change with full regression. Details in section 5.
   - **PV2-03B.** K0 and M rejected a valid central file that MSBuild imports from outside the project's ancestor folders (`DirectoryPackagesPropsPath`). M's post-edit hook even blocked the edit.
     - The interim review's exact example, a project file that `<Import>`s `config/Directory.Packages.props`, is **not** effective CPM. The SDK does not mark it imported, and NuGet ignores CPM (NU1015). All six already reject it, and that is unchanged.
   - **V3-Q10.** M1 and K0 accepted a `PackageVersion` with no version; NuGet warns NU1604, no lower bound. The same rule fixed two more related defects:
     - K0 accepted empty and floating `Version` child elements;
     - M rejected a valid child-element version.
4. **The 86 flagged records** were each read at source: 84 upheld, 1 qualified and 1 corrected (the M NgModules ban, DEFAULT to MUST_NOT). The correction passed the full V3-D02 gate.
5. **No coverage or strength status moved** in any of the 1,176 policy cells against v2. Six cells gained witness links with the same statuses. Same labels do not prove semantic parity; see the check levels in section 7.
6. **External events.**
   - Outside this session, the v2 convenience archive was removed, and two files were added: your v3 archive and the interim review.
   - All three are recorded in `EXTERNAL_EVENTS.json` (ENV-01 to ENV-03).
   - The fence and R27 tolerate exactly those bytes. The v2 tree is verified unchanged, file by file.

## 2. Provenance and preflight

- **Pass 1** stays integrated through `step1_union_augmented_pass1` and v2. It was not integrated again.
  - Pass 2/3 ids overlap Pass 1 ids nowhere.
  - 23 Pass 2/3 records overlap Pass 1 content, and those are deduplicated in the adjudication.
- **Pass 2:** COMPLETE.
  - 63 records; 448 of 448 files; 211 checkpoint files; 205 completed units.
  - Revisions CIS-K0-U0025 and CIS-M1-U0014 applied.
  - Three records lack a three-run reference: CIS-M1-U0020, CIS-M1-U0021 and CIS-L0-U0010.
- **Pass 3:** COMPLETE.
  - 148 records; 448 files; 99 checkpoint files; 95 units.
  - Twelve K0 revisions applied (U0034 to U0045).
- **Integrity:** every quote matches its source, and no baseline reference is broken.
  - The baseline fingerprint `90a4dd94…` was recomputed: 933 files, 33,987 records.
  - The Codex validator says PASS_STRUCTURAL_ONLY. Codex is PAUSED_BY_USER after Pass 3.
  - Pass 0004 and later were never entered. The cold audit proves the prune behaviorally.
- **Preflight warning PRE-W01:** the v1 convenience zip was absent at the start; the v1 tree matches its fingerprint byte for byte.
- **ENV-01 to ENV-03 (found at V3-D02 gate attempt 1):**
  - the v2 zip was removed (preflight SHA-256 `e1e293ea…`);
  - `step2_controlled_repair_v3.zip` and `Stage_A_Step2_V3_Independent_Interim_Review_EN.md` were added.
  - The interim review was read as data. Your chat message was the instruction.

## 3. Codex Pass 2+3 adjudication (against Pass 1, the three raw runs and v2)

| Count | Value |
|---|---:|
| (a) Codex finding records (Pass 2 + Pass 3) | 211 (63 + 148) |
| (b) Unique semantic issue clusters | 30 (11 with normative effect) |
| (c) Truly new independent study-level obligations | **0** |
| (d) Facets of existing obligations | 18 records → 14 existing records reworded (13 appended plus a second K1 record of the same line) |
| (d') Candidate-level scan prompts present in the text but not extracted | 29 records → 18 added records (`V3A-*`), backed by an 8-item census |
| (e) Already covered | 4 |
| (f) Non-normative (technique and decision tables, examples, configuration values, permissive guidance) | 160 |
| (g) Open hypotheses / items needing your decision | 0 open hypotheses; 3 observations (Q-01 L0 raw HTML, Q-05 M1 section-reference heuristic, hook time budgets) |

**Unique new semantic discrepancies, compared with Pass 1 and prior audits:**
- **From Codex:**
  - one real candidate text difference (L0 raw HTML, Q-01);
  - one checker heuristic (M1, Q-05);
  - 6 clusters of unevenly extracted security-scan prompts (local accounts, uploads, SSRF, raw HTML, security logging, secrets and configuration);
  - 5 facet clusters (2 qualifiers, 2 dropped atoms, 1 loading restriction).
- **From v3 testing after the interim review:**
  - the rejection of a non-ancestor central file (K0, M);
  - the `PackageVersion` version-metadata defects (M1, K0, M).

  Both are corrected.

Files: `PASS2_PASS3_ADJUDICATION.jsonl`, `UNIQUE_ISSUE_CLUSTERS.jsonl`, `ADJUDICATION_COUNTS.json`, `ADJUDICATION_CHECKPOINTS/`.

## 4. Changes implemented (one logical change per gate)

| # | Change | Authority | Candidates | Gate (attempts; cumulative tally at the passing gate) |
|---:|---|---|---|---|
| 1 | V3-0-BASELINE-REPLAY | replay of v2, no change | — | PASS_WITH_DOCUMENTED_NOT_RUN after 3 (2,242 pass, 20 not run) |
| 2 | PV2-02-FAILCLOSED-INPUT | kit 74 PV2-02 (approved) | M, M1 | PASS_WITH_DOCUMENTED_NOT_RUN after 2 (2,323 pass, 22 not run) |
| 3 | PV2-01-GIT-GATING | kit 74 PV2-01 (approved) | M, M1, L0, L1, K1 | PASS_WITH_DOCUMENTED_NOT_RUN after 2 (2,801 pass, 25 not run) |
| 4 | PV2-03-K0-CPM-ROOT | kit 74 PV2-03 (approved) | K0 | PASS_WITH_DOCUMENTED_NOT_RUN after 1 (2,886 pass, 26 not run) |
| 5 | PV2-04-M-FRONTEND-TESTS | kit 74 PV2-04 (approved) | M | PASS_WITH_DOCUMENTED_NOT_RUN after 3 (2,934 pass, 28 not run) |
| 6 | V3-D01-PASS23-OVERLAY | Pass 2+3 adjudication (data only) | data | PASS_WITH_DOCUMENTED_NOT_RUN after 1 (3,028 pass, 29 not run) |
| 7 | V3-D02-MODALITY86 | review of the 86 records (data only) | data: M | PASS_WITH_DOCUMENTED_NOT_RUN after 2 (3,127 pass, 30 not run) |
| 8 | PV2-03B-CPM-IMPORT-PROVEN | PV2-03 semantics; kit 74 Part C; your instruction of 2026-11-06 | K0, M | PASS_WITH_DOCUMENTED_NOT_RUN after 1 (3,256 pass, 31 not run) |
| 9 | V3-Q10-PACKAGEVERSION-VERSION | DEP-006 and DEP-003 (frozen oracle, MUST); PV2-03 invalid metadata; kit 74 Part C; your instruction of 2026-11-06 | M1, K0, M | PASS_WITH_DOCUMENTED_NOT_RUN after 1 (3,416 pass, 32 not run) |

**Template files changed against v2: 26.** By candidate: M 7, M1 6, L0 3, L1 3, K0 3, K1 4. No file was added or removed.
- Against the frozen inputs, cumulative with v1 and v2: M 18, M1 16, L0 16, L1 16, K0 17, K1 21.
- Per-file SHA-256: `V3_FINAL_MANIFEST.json`. Crosswalk: `V2_TO_V3_FILE_CROSSWALK.jsonl` (448 rows).

**Records against v2** (`V2_TO_V3_CROSSWALK.jsonl`): 6,498 in v3, 6,472 in v2.
- 6,046 unchanged and 404 with only an anchor shift.
- 21 claims reworded: 14 by D01, 3 by PV2-03, 1 more by PV2-03B (which also rewords two of PV2-03's records again), and 3 by V3-Q10.
- 1 modality changed (FG-M-8b2c02178e, DEFAULT to MUST_NOT, V3-D02).
- 26 added: 18 by D01, 5 by PV2-01, 2 by PV2-02 and 1 by PV2-04.
- No label changed on an existing record.

**Behavior** (details in `APPROVED_DECISION_IMPLEMENTATION_MATRIX.md` and `V3_METRIC_IMPACT.md`):
- **PV2-01:** M, M1, L0, L1 and K1 return `ask` for repository-changing Git, using K0's table placed byte-identical in each hook.
  - Read-only Git runs without a prompt.
  - An existing non-Git deny still wins.
  - The ask reason says that a prompt is not authorization (HQ-01/GOV-015 preserved).
- **PV2-02:** M and M1 refuse malformed, empty or non-object shell PreToolUse input in the script. They also refuse a missing, blank or non-string command.
- **PV2-03 and PV2-03B:**
  - K0 no longer mandates a root central file.
  - K0 and M no longer reject a central file that MSBuild proves imported from elsewhere.
  - Per-project effective CPM is still proven by MSBuild in all six.
- **PV2-04:** M bans frontend tests under `backend/` in its normative owner (record V3A-M-030, MUST_NOT, as M1 and K0 store it).
- **V3-Q10:** all six read a `PackageVersion` version from the attribute or from a child element. A missing, empty or floating version errors in all six.
- **V3-D01 and V3-D02:** data only; no template byte changed.

## 5. The two residual checker-parity issues (your instruction of 2026-11-06)

Probe: `_tools/cpm_residual_probe.py`. Results: `_investigation/cpm_residual_probe_before.json`. Real MSBuild 10.0.403 evaluation and an offline NuGet restore against an empty local feed. The "→" shows the outcome after the correction.

**Issue 1: a central file outside the project's ancestor folders.**

| Fixture | MSBuild: CPM / file imported | NuGet | M | M1 | L0 | L1 | K0 | K1 |
|---|---|---|---|---|---|---|---|---|
| `DirectoryPackagesPropsPath` → `config/Directory.Packages.props` (also: two projects, a renamed file, the path set in a nested `Directory.Build.props`) | true / true | NU1008 for a version pinned in the project (CPM enforced) | ERROR → **OK** | OK | OK | OK | ERROR → **OK** | OK |
| The project file `<Import>`s `config/Directory.Packages.props` (the review's example), or a plain `<Import>` from `Directory.Build.props` | true / **empty** | NU1015 (CPM not applied) | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR |
| Path to a missing file; CPM off in the imported file; version pinned in the project; a project outside the covered path | — | — | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR |

Why the `DirectoryPackagesPropsPath` layout is valid:
- The SDK's `NuGet.props` imports `$(DirectoryPackagesPropsPath)` and only then sets `CentralPackageVersionsFileImported`.
- `NuGet.targets` enables CPM only when both that property and `ManagePackageVersionsCentrally` are true.

Authority for the correction:
- Kit 74 PV2-03: "Allow valid nested/otherwise legitimately effective central package configurations, validated using per-project effective MSBuild properties".
- K0 D-17 already said "any location MSBuild imports for each project is valid".
- M's own NuGet rule names no location.

What PV2-03B changed:
- In K0 (repository check) and M (command and post-edit hook), the static ancestor check now stands only when MSBuild did not prove CPM on and a central file imported.
- Nothing was relaxed:
  - the no-SDK static fallback stays (Q-11);
  - the error messages are unchanged;
  - the shared evaluator is unchanged.
- Three claims were reworded to the conditional form: FG-K0-36395ffe06, FG-K0-73dd5d1170 and FG-M-7f012a0fe2.

This also completes PV2-03. Its ancestor check, written in v3, still rejected such a file although D-17 allowed it.

**Issue 2: a `PackageVersion` with no version.**

| Fixture | MSBuild `Version` | NuGet | M | M1 | L0 | L1 | K0 | K1 |
|---|---|---|---|---|---|---|---|---|
| `<PackageVersion Include="A.B" />` (root and nested) | empty | NU1604 | ERROR | OK → **ERROR** | ERROR | ERROR | OK → **ERROR** | ERROR |
| `<Version></Version>` or `<Version />` child | empty | NU1604 | ERROR | ERROR | ERROR | ERROR | OK → **ERROR** | ERROR |
| `<Version>1.*</Version>` child | 1.* | — | ERROR | ERROR | ERROR | ERROR | OK, notice only → **ERROR** | ERROR |
| `<Version>1.2.3</Version>` child (valid) | 1.2.3 | valid | ERROR → **OK** | OK | OK | OK | OK | OK |

Recheck against the approved rules:
- DEP-006 (frozen oracle, MUST: versions belong in `Directory.Packages.props`) and DEP-003 (MUST: latest stable compatible version) both forbid a missing version.
- Every candidate's NuGet text says so as well.
- PV2-03 requires negative fixtures for invalid package metadata.

What V3-Q10 changed:
- Checker enforcement only; no rule text changed.
- Three K0 claims were reworded to add "missing".
- The v3 PV2-03 suite row that documented the old M1/K0 difference now requires ERROR in all six. That makes it stricter; the negative test is V3-Q10's mutations.
- Q-10 in the queue is now RESOLVED.

## 6. The 86 flagged records

Each was read at source (`MARKED_NEVER_86_REVIEW.jsonl`):
- 84 upheld;
- 1 qualified (FG-L1-5f5febf5c6, Q-09);
- 1 corrected (FG-M-8b2c02178e).

Reason codes:

| Reason code | Count |
|---|---:|
| COMPOUND_TECHNIQUE | 26 |
| DEFAULT_MARKED | 24 |
| UNMARKED_SOURCE | 10 |
| COMPOUND_POLICY | 8 |
| RESULT_CLAUSE | 5 |
| TRIGGER_WORDING | 4 |
| DESCRIPTIVE | 3 |
| CHECK_BY_REFERENCE | 2 |
| MARKED_BAN_ONLY | 1 |
| DUPLICATE_MARKED | 1 |
| CATALOGUE_BORDERLINE | 1 |
| OWNER_MARKED_DEFAULT | 1 |

Records that say "do not" were outside the class and were not reviewed (Q-06). Raw MUST_NOT counts are still not a strictness metric.

## 7. Test outcomes

**Gates** (`GATE_LOG.jsonl`, `REGRESSION_MATRIX.md`, logs in `GATE_ATTEMPTS/`):
- 16 attempts across the 9 changes; every change ends PASS_WITH_DOCUMENTED_NOT_RUN.
- Seven attempts failed:
  - two crashes in the gate tooling: V3-0 (bootstrap had not copied the v2 rule snapshots) and PV2-04 (quoting in `adaptations.py`);
  - one tooling-port failure at V3-0: a missing adaptations row, and R27 still using v2's start time;
  - three real issues caught by the gates:
    - PV2-01: L1's own neutrality checker rejected the word "PreToolUse" in its technology-neutral text;
    - PV2-02: claims added in v3 had no review rows;
    - PV2-04: a new phrase in an added claim's trigger had not been read in the census;
  - one failure from the external file events (V3-D02).
- Each failure was repaired or rolled back, and the whole gate was re-run. No failure was waived.
- The last gate ran all 27 v1 suites, all 9 v2 suites and all 9 v3 suites: 3,416 PASS, 0 FAIL, 32 NOT_RUN.

**Cold audit** (`FINAL_AUDIT_RESULTS.jsonl`, attempt 3, run from the final bytes; it reads no gate result as evidence):

| Section | Scope | Pass | Fail | Not run | Finding |
|---|---|---:|---:|---:|---:|
| A | Isolation: fence, external events, Codex pass pruning, no Git tree, no Step 3 | 8 | 0 | 0 | 2 |
| B | Bytes: the last logged hash of each file across v1, v2 and v3; the final manifest | 18 | 0 | 0 | 0 |
| C | Architecture invariants, own checkers, `node --check` | 25 | 0 | 0 | 0 |
| D | Adversarial: one Git table, stale wording, change scope, declarations | 30 | 0 | 0 | 0 |
| E | Same task across six: Git, bad input, nested CPM and imported central file, `PackageVersion`, frontend tests | 96 | 0 | 3 | 5 |
| F | Interactions: PV2-01 with DEP-025, PV2-02, R02, HQ-01 and C04; PV2-03, PV2-03B and V3-Q10 with DEP-003; coverage | 30 | 0 | 0 | 0 |
| G | Dataset: replay, crosswalk, identities, graph, reviews, adjudication | 9 | 0 | 0 | 0 |
| H | 1,176 policy cells: witnesses, check levels, counterexamples | 3 | 0 | 0 | 2 |
| I | All 44 suites re-run on the final bytes | 44 | 0 | 32 | 0 |
| **Total** | | **263** | **0** | **35** | **9** |

Earlier audit attempts (`AUDIT_ATTEMPTS/`):
- **Attempt 1:** one FAIL, a false positive in the audit's own scan for Codex pass names. It matched prose lines that state the pruning.
- **Attempt 2:** stopped after section E, because a new test in the audit itself wrote a later pass name literally.
- Neither attempt changed any candidate or data file.

The nine FINDING rows are:
- the v2 archive warning (ENV-01);
- the tolerated external files (ENV-02, ENV-03);
- the no-SDK CPM difference (Q-11);
- the unchecked central-file name (Q-12);
- the K0 Git over-approximation (Q-04);
- bad-input differences outside PV2-02 (Q-02, Q-03);
- different hook time budgets;
- the two check-level rows below.

**Policy cells** (`POLICY_PARITY_MATRIX.jsonl`):
- **Cold audit count:** 97 of 1,176 cells were read side by side: 13 in v3, 54 in v2, and 30 v2 clause reviews. The other 1,079 rest on the Step 2 classification plus a witness at a current line.
- **Gate count (broader, it includes v1 rule reviews):** 173 cells source-reviewed, 581 mechanically checked in touched files, and 422 with an unchanged witness.
- Either way, a mechanical witness shows traceability, not semantic parity.
- Same-task matrices: `SAME_TASK_MATRIX_V3.json`. Interaction matrix: `INTERACTION_MATRIX_V3.json`.

**NOT_RUN** (35 audit rows; never counted as PASS):
- A live Claude Code host:
  - how `ask` is displayed and answered;
  - how `deny`, exit 2 and `onFailure` are applied;
  - what a headless run does when it meets `ask`.
- A live agent doing one task end to end, including stopping on a dirty tree and a headless decision log.
- A real application, database, cache, Swagger UI, registry or CI.
- A NuGet restore against a real registry, for every CPM fixture.
- Checker enforcement of text-only duties (PV2-04).
- Git run indirectly by a script or program.
- A blind second reader (a fresh session or a human) for the adjudication, the 86 readings and the PI-012 records.
- A hand reading of every condition in all 1,176 cells.

## 8. Metrics

See `V3_METRIC_IMPACT.md` and `V3_METRIC_CROSSWALK.json`. It keeps three layers apart:
- **Data labels:** 26 added records, 21 reworded claims, 1 modality change and 404 anchor-only shifts.
  - Per candidate: M +4, M1 +5, L0 +4, L1 +5, K0 +5, K1 +3 records.
- **Policy cells:** 0 status or strength moves. Strength is 1,171 EQUIVALENT_EVIDENCE_PRESENT and 5 STRONGER_AND_WEAKER_EVIDENCE, as in v2.
- **Template behavior:** one row per v3 change, with its own suite's result on the old and the new bytes.

v2's reported results are not overwritten. Comparative enforcement or strictness metrics must use the v3 behavior layer and must not use raw MUST_NOT or label counts.

## 9. Remaining uncertainties and the decision queue

Full text: `UNRESOLVED_AND_USER_DECISION_QUEUE.jsonl` (Q-01 to Q-13).

| Id | Kind | Item |
|---|---|---|
| Q-01 | USER_DECISION | L0 lacks the raw-HTML scan sentence the other five have |
| Q-02 | USER_DECISION | A blank PreToolUse command is allowed in L0, K0 and K1 |
| Q-03 | USER_DECISION | Event/tool mismatch handling differs |
| Q-04 | OBSERVATION | K0 asks for `echo git commit` |
| Q-05 | OBSERVATION | M1 section-reference heuristic |
| Q-06 | OPEN_CLASS | "do not" records at a soft modality not reviewed |
| Q-07 | OPEN_HYPOTHESIS_RESIDUE | Codex not saturated (3 of 6 strategy families) |
| Q-08 | NOT_RUN | Live host behavior |
| Q-09 | QUALIFIED | L1 304 catalogue line kept DEFAULT |
| Q-10 | RESOLVED | Missing `PackageVersion` version (V3-Q10) |
| Q-11 | OBSERVATION | Without the SDK, K0 and M error statically where four report NOT_RUN |
| Q-12 | USER_DECISION | No candidate checks the name of a central file imported through `DirectoryPackagesPropsPath` |
| Q-13 | ENVIRONMENT | v2 convenience archive removed outside the session; restore it from your copy if it should stay beside the tree |

The v2-known limit stands: a version taken from an MSBuild property is read differently by the static checkers. Detail: `EVIDENCE_LIMITS.md` (v3 section).

## 10. Residual risk and the Step 3 recommendation

**Self-audit caveat.**
- The same model family that wrote the Step 2 labels, v1 and v2 also adjudicated, corrected and audited v3. Agreement is weak evidence.
- Your interim review was static, and it still found two real issues. That shows the value of an independent reader. A second model family or a human is still the next step.

**CONDITIONAL_GO for Step 3**, on these conditions:
1. Observe live-host behavior in a pilot before any metric relies on it: the `ask` display and answer, `deny`, exit 2 and `onFailure`. Above all, see what a headless run does when it meets a Git `ask`.
2. Run every benchmark from a clean Git tree, with the .NET SDK on PATH. Without the SDK, the CPM checks report NOT_RUN in four candidates and a static error in K0 and M.
3. Use no raw MUST_NOT or label counts as strictness metrics (Q-06); use the v3 behavior layer.
4. Exclude CI, registries and live services, or record them as NOT_RUN.
5. Decide Q-01, Q-02, Q-03 and Q-12 first, or record them as known differences in the Step 3 protocol.
6. Have someone independent review the adjudication and a sample of the mechanically witnessed cells: another model family or a human.

## 11. Deliverables in this folder

- **Adjudication:** `PASS2_PASS3_ADJUDICATION.jsonl`, `UNIQUE_ISSUE_CLUSTERS.jsonl`, `ADJUDICATION_COUNTS.json`, `ADJUDICATION_CHECKPOINTS/`.
- **Changes and gates:** `APPROVED_DECISION_IMPLEMENTATION_MATRIX.md`, `CHANGE_LOG.jsonl`, `GATE_LOG.jsonl`, `REGRESSION_MATRIX.md`, `CHECKPOINTS/`, `GATE_ATTEMPTS/`, `_rules/<change>/` (declaration, patches, dispositions, updates, review, suite runs before and after).
- **Cold audit:** `FINAL_AUDIT_RESULTS.jsonl`, `FINAL_SUITE_TALLY.json`, `POLICY_PARITY_MATRIX.jsonl`, `SAME_TASK_MATRIX_V3.json`, `INTERACTION_MATRIX_V3.json`, `AUDIT_ATTEMPTS/`.
- **Manifest:** `V3_FINAL_MANIFEST.json` (SHA-256 per file, with v2 and frozen hashes).
- **Crosswalks and metrics:** `V2_TO_V3_FILE_CROSSWALK.jsonl`, `V2_TO_V3_CROSSWALK.jsonl` (claims), `V3_METRIC_CROSSWALK.json`, `V3_METRIC_IMPACT.md`.
- **Final classifications and overlays:** `REPAIRED_CLASSIFICATIONS.jsonl`, `REPAIRED_POLICY_COVERAGE.jsonl`, `ORIGINAL_TO_REPAIRED_CLAIMS.jsonl`, `DATASET_MANIFEST.json`, `V3_NEW_CLAIMS_REVIEW.jsonl`, `MARKED_NEVER_86_REVIEW.jsonl`.
- **Queue, limits and environment:** `UNRESOLVED_AND_USER_DECISION_QUEUE.jsonl`, `EVIDENCE_LIMITS.md`, `EXTERNAL_EVENTS.json`.
- **Investigation:** `_investigation/cpm_residual_probe_before.json`.
- **State:** `STATE.json`, `RESUME.md`.
