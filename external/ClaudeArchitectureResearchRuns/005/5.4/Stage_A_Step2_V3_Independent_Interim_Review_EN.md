# Independent Interim Review — Stage A / Step 2 v3 (2026-11-06)

**Scope:** Independent archive-level inspection of the uploaded `step2_controlled_repair_v3.zip` against the supplied v1 and v2 archives and frozen `5.4(2).zip`. This is a **partial, static independent review**, not a fresh execution of Claude's full test suite or a live-host experiment.

## Status

**INCOMPLETE — do not freeze templates or claim Step 3 readiness yet.** `STATE.json` is at `P3_CHANGES`; the `V3-D02-MODALITY86` full gate, final cold audit, final reports and completed status are outstanding. The latest successful gate was `V3-D01-PASS23-OVERLAY`: **3,028 PASS / 0 FAIL / 29 NOT_RUN**. This is NOT a final-v3 audit result.

## Verified lineage and conservation

- Pass 1 remains integrated through `step1_union_augmented_pass1`: **152 dispositions = 26 proposals + 29 facets + 71 non-independent + 25 covered + 1 unresolved**. Do not integrate Pass 1 a second time.
- Pass 2 and Pass 3: **63 + 148 = 211 unique Codex finding IDs**. All 211 recorded original source quotes were independently matched **exactly at their cited line ranges** in frozen `5.4(2).zip` candidate inputs.
- v3 adjudication: **211 records, 30 issue clusters**; verdicts **160 NON_NORMATIVE, 4 ALREADY_COVERED, 18 FACET_OF_EXISTING, 29 CANDIDATE_UNREPRESENTED_DUTY**. The claim that these create **zero study-wide new independent obligations** is the v3 author's semantic judgment, NOT independently proven by this archive-level review.
- Classification identity retention: **6,448 v1 → 6,472 v2 → 6,498 v3**. Zero original `source_key` IDs were lost at either transition. v3 adds **26** records over v2; 17 existing claim texts changed and 1 existing modality changed (M NgModules `DEFAULT`→`MUST_NOT`). No existing record changed classification. The three previously inactive source-removed records remain represented.
- All **448** candidate-relative paths remain identical between v2 and v3. Exactly **24** changed bytes (M 6, M1 5, L0 3, L1 3, K0 3, K1 4). No candidate files added or deleted.
- All **1,176** `(candidate, policy_id)` coverage cells remain present. No `computed_status`, `normative_strength`, `baseline_status` or `baseline_strength_status` changed versus v2. Six cells acquired extra partial witness links, consistent with the approved changes. These unchanged labels **do not prove semantic parity**.
- All **26** new v3 classification records have valid source paths and source quotes: **23 exact strings, 3 strings matching after whitespace normalization** because the Markdown source line wraps them; all 26 quotes match the recorded source line ranges.
- `DATASET_MANIFEST.json` hashes match the actual `REPAIRED_CLASSIFICATIONS.jsonl`, `REPAIRED_POLICY_COVERAGE.jsonl`, `ORIGINAL_TO_REPAIRED_CLAIMS.jsonl` and `V2_TO_V3_CROSSWALK.jsonl` bytes.
- The six completed gates (baseline replay, PV2-01 through PV2-04, D01) each have passing checkpoints. All 41 cumulative suites (previous and v3) are represented in the latest gate. Failed attempts are retained; do not erase them.
- The v1 convenience ZIP missing from the user's source tree explains a known v2 verifier error; v3 preflight checked the underlying **1,626-file v1 directory** against the previously recorded fingerprint with **zero differences**. Treat this as a documented environmental warning, not evidence of lost v1 work.

## Limitations of the current metrics

- Of the **1,176** coverage cells, the latest gate marks **173 SOURCE_REVIEWED**, with the other **1,003** mechanically checked (touched-file or unchanged-witness). Most data labels are not independently reread.
- The 86 `never`/`must not` softer-modality records were individually reviewed: **84 UPHELD, 1 QUALIFIED, 1 CORRECTED**. The corrected M NgModules row is already reflected in the dataset, but its independent full **V3-D02 gate is not yet run**. Do not compare architecture strictness via raw `MUST_NOT` counts.
- The dataset has **6,498 total rows / 6,495 active rows**, **1,176** coverage cells and four retained proposals. The new security-scan records reflect **uneven extraction of existing scan instructions**, not necessarily actual template differences. `CL15` explicitly records a real candidate-specific omission: L0 lacks the separate server-rendered raw-HTML scan sentence present in the other five. Do not silently add it to L0 without authority.
- No live Claude host, real application, registry, database, cache, Swagger UI, or CI is verified; passing hook-script fixtures do not establish live-host `ask`/`deny` behavior. The final cold audit is still missing.

## Two concrete issues to resolve or explicitly carry forward

### 1. K0 central-file location may still be too restrictive (NEW external observation)

`candidates/K0/template/.claude/scripts/check-dependencies.cjs`, lines **385–405**, retains a mandatory `centralFileAbove()` check limited to a project's own directory or ancestor **inside the repository**. It errors if no such file is found. However the approved PV2-03 semantics and the current K0 D-17 text allow **any legitimate Directory.Packages.props location explicitly imported by MSBuild** into the project with effective central package management. The PV2-03 tests cover root and nested **ancestor** files, not a file at another in-repository location imported explicitly from the project.

**Requested adversarial test:** a project `backend/App/App.csproj` explicitly imports `config/Directory.Packages.props`, the latter contains a valid central package version, and MSBuild reports the effective CPM property and central import as enabled. Compare all six candidate checkers. If the example is genuinely valid MSBuild CPM and K0 alone rejects it due to the ancestor-path heuristic, remove/soften that hard error in a **single separate gated logical change**, retaining effective per-project MSBuild validation and all prior regressions. If it is invalid, document the exact MSBuild result and rationale instead. A source-level discrepancy is evident; a real MSBuild counterexample has NOT been run independently here.

### 2. M1 and K0 admit a missing central package version (KNOWN v3 discovery)

`candidates/M1/template/.claude/scripts/check-manifests.js` lines **154–168** only validates a version **when `version !== null`**, and `candidates/K0/template/.claude/scripts/check-dependencies.cjs` lines **307–320** skips an entry when `Version` is undefined. The existing PV2-03 fixture records `M1=OK` and `K0=OK` for `<PackageVersion Include="A.B" />`, versus ERROR in the other four candidates. This is **pre-existing**, not introduced by v3. It is the not-yet-written decision queue's Q-10. Resolve whether this is already prohibited by the agreed dependency/version policy, then apply an explicitly authorized, separately gated correction or document it as outstanding. Do not silently change the normative contract.

## Required continuation

1. Preserve the current v3 output and checkpoints. Execute the pending `V3-D02-MODALITY86` full gate **before** claiming the 86-row review complete.
2. Address or explicitly retain both issues above; if any additional template or data changes are made, use a separate one-rule gate and full cumulative v1+v2+v3 regression.
3. Complete the v3 evidence-limit addendum; run the separate final cold audit; generate all prescribed regression, implementation, crosswalk, metric-impact and decision-queue reports; write `FINAL_PASS2_PASS3_INTEGRATION_AND_PARITY_REPORT.md` and only then mark state COMPLETE.
4. State what changed in data-label counts separately from policy-cell/strength statuses and from independently verified live behavior. Preserve audit limitations and no-Step-3 condition.
