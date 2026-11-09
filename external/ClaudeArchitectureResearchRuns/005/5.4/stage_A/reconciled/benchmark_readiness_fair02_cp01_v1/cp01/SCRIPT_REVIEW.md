# CP-01 — Review of the supplied `Test-IDE0005.ps1` before execution

Reviewed file: `_STAGE_A_KIT/ide0005_probe_en/Test-IDE0005.ps1`, SHA-256 `9c2853db1edd38602fb5c6cf0192b4649c0eb070df141eaf144d5d8c3de8415a` (all kit hashes: `CONFIG_PROVENANCE_CHECK.json`). The script was **not edited**. It is run from a hash-verified copy in a new Windows temporary directory.

## 1. Safety

| Question | Finding |
|---|---|
| Where does it write? | Only under `[System.IO.Path]::GetTempPath()\IDE0005-Probe-<guid>` (case folders, `NuGet.Config`, empty `emptyfeed`, logs, `summary.json`). It copies from its own folder and never writes there. |
| Does it delete or overwrite anything? | No `Remove-Item`, no `-Force` overwrite outside the new GUID folder. |
| Does it install packages, tools, workloads or SDKs? | No. Only `dotnet --list-sdks`, `--version`, `restore`, `build`, `format style`. |
| Does it change machine configuration? | No registry access, no `Set-ExecutionPolicy`, no environment changes, no global NuGet or SDK configuration. `-ExecutionPolicy Bypass` applies to the launched process only. |
| Does it contact package feeds? | Restore uses `--configfile` pointing at a `NuGet.Config` with `<clear />` and a single empty local folder feed, plus `--ignore-failed-sources`. The probe project has no package references; the `net10.0` targeting pack and the code-style analyzers ship with the SDK. |
| Residual network contact outside the script's control | The .NET CLI can send telemetry and run a background workload-update check. Mitigation: the wrapper sets **process-scoped** variables `DOTNET_CLI_TELEMETRY_OPTOUT=1`, `DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE=1`, `DOTNET_NOLOGO=1`, `DOTNET_SKIP_FIRST_TIME_EXPERIENCE=1`, `MSBUILDDISABLENODEREUSE=1`. None affects compilation or analyzers; none persists after the process ends. |

Verdict: **safe to run** in an isolated temporary directory.

## 2. Environment assumptions and weaknesses (affecting interpretation, not safety)

| # | Assumption or weakness | Consequence | Mitigation in this task |
|---|---|---|---|
| E1 | `dotnet --version` is evaluated in the caller's working directory, not in the probe folder. The muxer picks the SDK by the caller's `global.json`; MSBuild's SDK resolver uses the project folder's chain. | The printed "Selected SDK" might differ from the SDK that built a case if a `global.json` existed on one path only. | No `global.json`, `Directory.Build.*`, `Directory.Packages.props`, `.editorconfig` or NuGet config exists anywhere on the `%TEMP%` parent chain (checked before the run). The wrapper starts the script with the working directory set to `%TEMP%`. The supplementary harness queries `NETCoreSdkVersion` **per case** through MSBuild. |
| E2 | Windows PowerShell 5.1 is the only PowerShell on this host (no `pwsh`). With `$ErrorActionPreference = 'Stop'`, a native command whose stderr is merged by `2>&1` raises a terminating `NativeCommandError` in 5.1. | If `dotnet` writes to stderr the script may stop before finishing all cases. | Run as is and record the exit code and console transcript. The supplementary harness captures stdout and stderr separately through `System.Diagnostics.Process`, so it does not depend on this behavior. |
| E3 | IDE0005 detection is `$text -match '\bIDE0005\b'` over **all** normal-verbosity output. | Could match non-diagnostic text (property dumps, command lines, file paths); it also cannot count diagnostics. | Supplementary harness counts only compiler-format diagnostics `file(line,col): warning|error IDE0005: … [project]`, deduplicated by file, position and id. A warning is treated as confirmed only if such a line was emitted. |
| E4 | Case B passes `-p:NoWarn=CS1591` as a **global** property. A global property replaces the whole `NoWarn` value (the SDK's own `1701;1702` append is ignored). | B differs from A in `NoWarn` as well as `GenerateDocumentationFile`. Harmless for IDE0005 (not in either list) but a second variable. | Supplementary case **B2** sets only `-p:GenerateDocumentationFile=true`, isolating the documentation property. Effective `NoWarn` is recorded per case. |
| E5 | Pass criterion requires build exit code 0. | Correct here: neither props file sets `TreatWarningsAsErrors`, so an IDE0005 warning does not fail the build. | Effective `TreatWarningsAsErrors` recorded. |
| E6 | The `dotnet format style` result is reported only as an exit code; the log is not parsed. | A nonzero exit could come from a load or restore error, not IDE0005. | Supplementary harness parses the format log for IDE0005 diagnostics and checks that `Source.cs` is unchanged (`--verify-no-changes`). |
| E7 | No file hashes, no MSBuild property queries in the script. | Cannot show from the script alone that configurations were unmodified or what properties were effective. | Supplementary harness hashes all case inputs before and after, and queries `EnforceCodeStyleInBuild`, `GenerateDocumentationFile`, `DocumentationFile`, `NoWarn`, `TreatWarningsAsErrors`, `AnalysisLevel`, `TargetFramework`, `NETCoreSdkVersion` per case. |
| E8 | `$args` (an automatic variable) is reassigned for the build arguments. | Works in 5.1 (array splatting); a style issue only. | None needed. |

## 3. What the run can and cannot show

- It shows whether a **command-line build** of a minimal project with M's or L0's unmodified files emits IDE0005, and whether M's `dotnet format style` route detects it.
- It does **not** show whether a live agent runs `dotnet build` or `dotnet format`, whether it reads or acts on warnings, or how a full application with many projects behaves. It is not a benchmark execution.
