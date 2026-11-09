# CP-01 — IDE0005 controlled reproduction (M and L0)

**Result in one line:** on the active .NET SDK 10.0.403, M's unmodified configuration does **not** report IDE0005 during `dotnet build`, the documentation-file positive control does, and L0 as is does; M's `dotnet format` routes (the kit's narrow one and M's own verify command) **do** detect IDE0005 without `GenerateDocumentationFile`. The supplied script itself could run only case A on this host; all cases were then run with the same commands by a replica harness, twice, with identical results.

Nothing in M, L0, any other candidate, Step 2 v3 or Step 3 was edited. This was not a benchmark execution.

## 1. Environment and provenance

| Item | Value | Evidence |
|---|---|---|
| Active SDK (muxer, `dotnet --version` in every case folder) | 10.0.403 | `cp01/replica_harness_run2/<case>/00_dotnet_version.stdout.log` |
| SDK used by MSBuild per case (`NETCoreSdkVersion`) | 10.0.403 in all six cases | `…/<case>/02_properties.stdout.log` |
| MSBuild / Roslyn | MSBuild 18.9.15; `C:\Program Files\dotnet\sdk\10.0.403\Roslyn\bincore\csc.exe`; targeting pack Microsoft.NETCore.App.Ref 10.0.14 | build logs |
| OS / shell | Windows 11 Pro 10.0.26200; Windows PowerShell 5.1.26100 (no PowerShell 7 installed) | `EVIDENCE_SUMMARY.json` |
| Other SDKs installed (not used) | 2.2 – 9.0 | `cp01/supplied_script_run/console.stdout.log` |
| `%TEMP%` parent chain | No `global.json`, `Directory.Build.*`, `Directory.Packages.props`, `.editorconfig` or NuGet config | checked before the run (`cp01/SCRIPT_REVIEW.md` E1) |
| Package feeds | Restore used only an empty local folder feed (`<clear />`); all restores exit 0; nothing installed | `…/01_restore.*.log` |
| Process-only environment | `DOTNET_CLI_TELEMETRY_OPTOUT`, `DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE`, `DOTNET_NOLOGO`, `DOTNET_SKIP_FIRST_TIME_EXPERIENCE`, `MSBUILDDISABLENODEREUSE` = 1 | `RUN_METADATA.json`, `EVIDENCE_SUMMARY.json` |
| Config provenance | All four kit configs = `CONFIG_PROVENANCE_SHA256.json` = v3 candidate files (**MATCH_ALL_4**) | `cp01/CONFIG_PROVENANCE_CHECK.json` |
| Case inputs | In every case `Probe.csproj`, `Source.cs`, `.editorconfig`, `Directory.Build.props` matched the kit hashes before the run and were unchanged after it (including both `--verify-no-changes` format runs) | `inputs_match_kit`, `inputs_unchanged_after` in `EVIDENCE_SUMMARY.json` |

Input hashes (SHA-256): M `.editorconfig` `6f93a112…7315`, M `Directory.Build.props` `ea04f6e3…80be`, L0 `.editorconfig` `224af498…244f`, L0 `Directory.Build.props` `4c1226fa…e31f`, `Probe.csproj` `a34e10a8…e89c`, `Source.cs` `5ad12ecd…a7d3`, `Test-IDE0005.ps1` `9c2853db…415a` (full values in `CONFIG_PROVENANCE_CHECK.json`).

## 2. The supplied script (`Test-IDE0005.ps1`, run unmodified)

Run by `_tools/cp01_run_supplied.ps1` from a hash-verified copy in `%TEMP%`, working directory `%TEMP%`, as its README instructs. Archive: `cp01/supplied_script_run/` (console stdout/stderr, `RUN_METADATA.json`, the script's own `restore.log`/`build.log` and inputs).

| Observation | Detail |
|---|---|
| Exit code | **1** |
| Cases reached | Only `A_M_as_is` (restore, build, then the format route) |
| Why it stopped | The M format route wrote its IDE0005 diagnostic to **stderr**; under Windows PowerShell 5.1 with `$ErrorActionPreference = 'Stop'` and `2>&1`, that became a terminating `NativeCommandError` (script line 78). B and C never ran; no `format-style.log` or `summary.json` was written. (Review item E2.) |
| Script verdict for A | `Build exit: 0; IDE0005 present: True; expected: False; PASS: False` — **a detector false positive**. The A build log contains no IDE0005 diagnostic. `\bIDE0005\b` matched (a) the script's own temp folder name `IDE0005-Probe-<guid>` in every path line and (b) the text "to enable IDE0005" inside the SDK hint below. (Review item E3.) |
| Real diagnostics in A's build log | One: `CSC : warning EnableGenerateDocumentationFile: Set MSBuild property 'GenerateDocumentationFile' to 'true' in project file to enable IDE0005 (Remove unnecessary usings/imports) on build` |
| Real diagnostic captured from the format route | `Source.cs(1,1): warning IDE0005: Using directive is unnecessary.` (in the error record, console stderr) |

The script's partial run agrees with the replica on everything it reached. Its own pass/fail line for A must not be used as evidence.

## 3. Replica harness (same commands, full capture)

`_tools/cp01_evidence_harness.ps1` re-creates each case in a new `%TEMP%\CP01-Evidence-<guid>` folder (name avoids the string "IDE0005") with the supplied script's **exact** restore, build and format arguments, captures stdout and stderr separately, queries effective MSBuild properties with the case's own global properties, and hashes inputs before and after. Two supplementary cases are labeled as such. Runs: `cp01/replica_harness_run1/` (harness `45e7cb63…`; its summary JSON collapses one-element arrays, a PowerShell 5.1 serialization quirk; logs unaffected) and `cp01/replica_harness_run2/` (harness `a2d32f22…`, the current file). **Both runs gave identical exit codes and diagnostics.** An independent Python parser (`_tools/cp01_tabulate.py`) re-read every raw log and agreed with the harness parser on every case (`cp01/OBSERVED_VS_EXPECTED.json`: `replicates_identical`, `all_parsers_agree`, `all_predeclared_expectations_met` = true).

Commands (`<p>` = the case's `Probe.csproj`):

- restore (all): `dotnet restore <p> --configfile <root>\NuGet.Config --ignore-failed-sources --nologo`
- build A, C: `dotnet build <p> --no-restore --nologo --verbosity normal`
- build B: same + `-p:GenerateDocumentationFile=true -p:NoWarn=CS1591`
- build B2 (supplementary): same + `-p:GenerateDocumentationFile=true` only
- format F (the kit's M route): `dotnet format style <p> --verify-no-changes --diagnostics IDE0005 --severity warn --no-restore --verbosity normal`
- format V (supplementary, M's verify-skill command `dotnet format --verify-no-changes`, run in the case folder with `--no-restore` as in M's ci-cd skill): `dotnet format --verify-no-changes --no-restore --verbosity normal`
- properties (all): `dotnet msbuild <p> -nologo -getProperty:…` (+ the case's `-p:` overrides)

### Observed versus expected

| Case | Origin | `EnforceCodeStyleInBuild` | `GenerateDocumentationFile` | csc `/doc:` | Effective `NoWarn` | Exit | IDE0005 diagnostics emitted | Other diagnostics | Expected | Match |
|---|---|---|---|---|---|---|---|---|---|---|
| A — M as is, build | kit | true | false | absent | `1701;1702` | 0 | **0** | `CSC : warning EnableGenerateDocumentationFile` (hint) | absent | **yes** |
| B — M + docs override, build | kit | true | true (CLI) | present | `CS1591` | 0 | **1** — `Source.cs(1,1): warning IDE0005: Using directive is unnecessary.` | none | present | **yes** |
| B2 — M + `GenerateDocumentationFile` only, build | supplementary | true | true (CLI) | present | `1701;1702` | 0 | **1** (same) | CS1591 × 2 (`Sample`, `Sample.Answer`) | present | **yes** |
| C — L0 as is, build | kit | true | true (props) | present | `;CS1591` | 0 | **1** (same) | none | present | **yes** |
| F — M `dotnet format style … --diagnostics IDE0005` | kit | (true) | (false) | n/a | n/a | **2** | **1** — `Source.cs(1,1): warning IDE0005` on stderr | none | not predeclared ("nonzero can indicate IDE0005") | detected |
| V — M `dotnet format --verify-no-changes` | supplementary | (true) | (false) | n/a | n/a | **2** | **1** (same, stderr) | none | not predeclared | detected |

`TreatWarningsAsErrors` = false, `AnalysisLevel` = latest, `TargetFramework` = net10.0 in every case. In F and V the formatter printed "Formatted code file …Source.cs" but, as `--verify-no-changes` requires, the file hash is unchanged.

## 4. What is confirmed, and what is not

| Question | Status | Basis |
|---|---|---|
| Does M's command-line build report IDE0005? | **No — experiment-confirmed** (this SDK, this fixture) | A, two replicates plus the supplied script's A |
| Is the missing `GenerateDocumentationFile` the cause? | **Yes — experiment-confirmed** | B and B2 add only that property (B2 without the `NoWarn` override) and IDE0005 appears; csc gets `/doc:` only then |
| Does L0's build report IDE0005 as is? | **Yes — experiment-confirmed** | C |
| Is M's build silent about unused usings? | **No, but it does not name them.** Every M build prints the SDK hint `EnableGenerateDocumentationFile` (no file, no line) | A |
| Does M's verify workflow have a working tool route? | **Yes — experiment-confirmed for the tool.** Both `dotnet format` commands exit 2 and name `Source.cs(1,1)` IDE0005 without `GenerateDocumentationFile` | F, V |
| Does a live agent run `dotnet build` or `dotnet format`, read the output, and remove the using? | **NOT_RUN.** Agent compliance is untested. M's verify skill makes formatting conditional ("If the repository configures formatting or analyzers, run them", `verify/SKILL.md` section 6) and separately requires removing unused usings from changed files (lines 163–168). | no host run |
| M1, L1, K0, K1 | **Not tested** (outside the required cases); Step 3's static reading stands for them | — |
| Larger solutions, other SDK patch levels, IDE behavior | **Not tested** | — |

## 5. Bug in M's claim, or valid alternative enforcement?

What M's files say, checked against the observations:

| M statement | Observed | Assessment |
|---|---|---|
| `.editorconfig:31` "Unused or redundant usings (verified for changed files by the verify workflow)." | `dotnet format` detects IDE0005 in M as is (F, V) | **Accurate.** This is M's declared route. |
| `.editorconfig:32-33` "reporting IDE0005 during command-line builds also requires `<GenerateDocumentationFile>true</GenerateDocumentationFile>`." | A vs B2 | **Accurate.** It is a conditional note, not a claim that M's build reports IDE0005. |
| `Directory.Build.props:12` "Surfaces .editorconfig code-style diagnostics (warning severity) during build." | IDE0005 is warning severity in M and is **not** surfaced (A) | **Over-general for IDE0005.** Other warning-severity rules were not tested. |
| `.claude/MAP.md:119` `.editorconfig` — "Formatting, naming, unused-using diagnostics" — consumers "IDE, `dotnet format`, build" | Build does not report unused-using diagnostics in M | **Imprecise.** A human map; Step 3 (`METRIC_LINEAGE_AND_LIMITS.md` section 5) records that human maps are not loaded for study tasks. |

**Conclusion.** There is **no functional defect** in M's IDE0005 enforcement as M itself describes it: M routes unused-using checks to the verify workflow, and that tool route works. The build-time difference from L0 is real and is an **enforcement-design difference**, which falls under the approved FAIR-01 disposition (preserve). There is a **minor documentation imprecision** in two M lines (props comment, human map). Step 3's phrasing "M's configuration contradicts its own comment" is stronger than the evidence supports: the comment correctly states a requirement that M does not adopt.

## 6. Bearing on Step 3 (recorded here; Step 3 files unchanged)

- RUN-010 D2 (root RC-ENF-IDE0005-BUILD): L0's top tier and M's position below it are now **execution-confirmed** for these two candidates (Step 3 basis was "source-read, no build"). The positions of M1, L1, K0, K1 remain source-read.
- Step 3's counterexample says M "print[s] nothing" on `dotnet build`. Refinement: M prints the `EnableGenerateDocumentationFile` hint, not an IDE0005 diagnostic.
- Step 3's counterexample says "only the verify step's manual check catches it". Refinement for M: M's verify step also has a tool route (`dotnet format --verify-no-changes`), confirmed to detect IDE0005 — **if** the agent runs it.
- Gate C limit "IDE0005: build not run" is resolved for M and L0.

None of these changes a Step 3 label: RUN-010 stays MEANINGFUL_DIVERGENCE on the enforcement axis (build-time visibility differs).

## 7. Correction proposal

A separate, **not applied** proposal is in `CP01_CORRECTION_PROPOSAL.md`. It recommends **no change** to M for the benchmark freeze; it documents an optional comment-only correction and explains why adding `GenerateDocumentationFile` to M is not recommended under FAIR-01.

## 8. Practical note for later benchmarks

- In M every build carries one SDK hint warning (`EnableGenerateDocumentationFile`). An agent aiming at a warning-free build may edit `Directory.Build.props` to silence it, which would change M's configuration during a run. Benchmarks should log edits to `Directory.Build.props` and `.editorconfig` per candidate.
- `dotnet format` writes IDE0005 to stderr. Harnesses that treat stderr as failure (as the supplied script did under PowerShell 5.1) can abort; capture streams separately.

## 9. Deviations and side effects of this experiment

- The supplied script could not complete on this host (PowerShell 5.1 only); results come from the replica harness with identical commands. The script was not edited.
- Besides the supplied probe's own `%TEMP%\IDE0005-Probe-7eaa635019bb471c98d5c185d5af14fa`, this task created `%TEMP%\CP01-KitCopy-48cffc95b82745c3a15c59cc8aa63fa7` (hash-verified kit copy) and `%TEMP%\CP01-Evidence-b2ca7eefc8f24adc97b206aba9d2a8ee` and `%TEMP%\CP01-Evidence-9f1c6aecf5ea46518641553e6ecb7393` (replica runs, with `bin/obj`). They were left in place as evidence; they can be deleted without affecting this folder, which holds all logs.
- The dotnet runs may have left the Roslyn compiler server process running until its idle timeout; no configuration was changed.

## 10. Files

| File | Content |
|---|---|
| `cp01/CONFIG_PROVENANCE_CHECK.json` | Kit / provenance / v3 hash comparison, all kit file hashes |
| `cp01/SCRIPT_REVIEW.md` | Pre-run safety and assumption review (E1–E8) |
| `cp01/supplied_script_run/` | Supplied script console output, metadata, its own logs and inputs |
| `cp01/replica_harness_run1/`, `cp01/replica_harness_run2/` | Per case: `00_dotnet_version`, `01_restore`, `02_properties`, `03_build` or `03_format_*` stdout/stderr logs; `EVIDENCE_SUMMARY.json` |
| `cp01/OBSERVED_VS_EXPECTED.json` | Machine-readable table, second-parser cross-check |
| `_tools/cp01_run_supplied.ps1`, `_tools/cp01_evidence_harness.ps1`, `_tools/cp01_tabulate.py` | Reproduction tools |

Reproduce (from this folder; writes only to `%TEMP%` and the given output folder):

```
powershell -NoProfile -ExecutionPolicy Bypass -File _tools\cp01_evidence_harness.ps1 -KitDir ..\..\..\_STAGE_A_KIT\ide0005_probe_en -OutDir cp01\replica_harness_run3
```
