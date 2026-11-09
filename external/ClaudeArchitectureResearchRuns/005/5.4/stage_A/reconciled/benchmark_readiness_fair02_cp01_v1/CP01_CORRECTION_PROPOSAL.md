# CP-01 — Potential correction for candidate M (proposal only, NOT applied)

Status: **for user authorization. Nothing was edited.** Evidence: `CP01_IDE0005_REPRODUCTION_REPORT.md`.

## Why a proposal at all

The experiment found **no functional defect**: M routes unused-using checks to its verify workflow, and the `dotnet format --verify-no-changes` route detects IDE0005 in M as is. It found a **minor documentation imprecision** in two M lines:

| File (v3 M template) | Current text | Observed |
|---|---|---|
| `Directory.Build.props:12` | `<!-- Surfaces .editorconfig code-style diagnostics (warning severity) during build. -->` | IDE0005 is warning severity in M and is not surfaced during build (case A). |
| `.claude/MAP.md:119` | Row for `.editorconfig`: purpose "Formatting, naming, unused-using diagnostics"; consumers "IDE, `dotnet format`, build" | Build does not report unused-using diagnostics in M (case A). |

## Options

| Option | Change | Effect on behavior | Effect on FAIR-01 / Step 3 | Recommendation |
|---|---|---|---|---|
| **0 — leave (recommended)** | None | None | Preserves the frozen v3/Step 3 bytes and the approved enforcement differences | **Recommended for the benchmark freeze.** The imprecise props comment is qualified by `.editorconfig:31-33` in the same repository, and M's verify skill (lines 163–168) tells the agent not to assume tooling removed every redundant import. Record the imprecision as a known note. |
| 1 — comment-only clarification | Props line 12 → `<!-- Surfaces warning-severity .editorconfig code-style diagnostics during build. IDE0005 (unused usings) is not reported at build because GenerateDocumentationFile is off; the verify workflow checks it. -->`. MAP row consumers → `IDE, dotnet format, build (unused usings: IDE and dotnet format only)` | None (comments and human map) | Changes two M file hashes, so v3/Step 3 fingerprints no longer describe M byte for byte; no label change | Only if the user wants M's text to be exact before measured runs. |
| 2 — add `GenerateDocumentationFile=true` and `NoWarn $(NoWarn);CS1591` to M's props | Two property lines | M's build would report IDE0005 (as case B2/B shows) and drop the hint warning | **Changes M's enforcement tier for RUN-010 D2 to L0's**, i.e. harmonizes an enforcement difference that FAIR-01 says to preserve | **Not recommended** unless the user explicitly reclassifies this as a defect rather than an architecture choice. |

## Option 1 — smallest change, side effects, test plan

- **Diff size:** one comment line in `Directory.Build.props`, one table cell in `.claude/MAP.md`.
- **Possible side effects:** M's `check-manifests.mjs` treats `Directory.Build.props` as a CPM chain file, so its hooks re-run the CPM proof on that edit (no setting changes). `check-instructions.mjs` requires `MAP.md` to list every file; the row stays. Step 2 v3 and Step 3 hashes (`UPSTREAM_V3_TREE_HASHES.json`, 448 template hashes) go stale for these two files; a new repair version folder is needed rather than an in-place edit.
- **Test plan:** (1) apply in a new repair folder, never in v3; (2) byte-diff shows only the two lines; (3) run M's `node .claude/scripts/check-instructions.mjs` and `node .claude/scripts/check-manifests.mjs` (expect the same results as v3); (4) replay the v3 suites that cover M; (5) re-run `_tools/cp01_evidence_harness.ps1` with the new props (expect identical build and format results: comments do not change behavior); (6) record the change in a change log with the user's authorization.

## Option 2 — side effects (if the user ever chooses it)

Every M project would generate an XML documentation file; public members without XML comments would warn CS1591 unless suppressed; malformed XML doc comments would start producing CS15xx warnings; build output and warning counts would change; the `EnableGenerateDocumentationFile` hint would disappear; RUN-010 D2 would move M into L0's tier, changing a Step 3 enforcement comparison. Test plan as for option 1, plus CP-01 cases A and C re-run and a regression check of warnings on a representative multi-project solution.
