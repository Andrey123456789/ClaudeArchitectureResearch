# IDE0005 build-time reproduction — Experiment 005 / Stage A Step 3

This isolated experiment uses **unaltered** `.editorconfig` and `Directory.Build.props` copied directly from the final `step2_controlled_repair_v3(1).zip` candidate M and candidate L0 trees. It never edits the research repository.

## Requirements

Windows PowerShell 5.1 or PowerShell 7 and **.NET 10 SDK**, matching the templates' `net10.0` target. No NuGet downloads are intended; an empty local NuGet feed is used.

## Run

Extract this ZIP into any directory. In a PowerShell terminal in that extracted directory:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Test-IDE0005.ps1
```

Or in an existing PowerShell session: `./Test-IDE0005.ps1` (execution policy permitting).

The script makes three independent temporary projects from identical source (`Source.cs` contains an unused `using System.IO;`) and identical `Probe.csproj`:

- `A_M_as_is`: candidate M `.editorconfig` and `Directory.Build.props`; expect IDE0005 **absent**.
- `B_M_docs_override`: same candidate M files, with only the MSBuild CLI overrides `GenerateDocumentationFile=true` and `NoWarn=CS1591`; expect IDE0005 **present**.
- `C_L0_as_is`: candidate L0 files with its existing `GenerateDocumentationFile=true`; expect IDE0005 **present**.

For the as-is M case, the script also performs a separate `dotnet format style --verify-no-changes --diagnostics IDE0005` check and saves `format-style.log`. This tests the alternative `verify`-workflow route explicitly mentioned in M, rather than assuming the build is its only enforcement mechanism.

The script prints pass/fail and leaves `build.log`, `restore.log`, and `summary.json` in a uniquely named directory under the Windows temp directory; it reports the exact location. Provide those files if results disagree with expectations. A failure is not automatically evidence that the candidate is wrong; first check SDK version, restore and effective MSBuild properties.

## Why this matters

The M `.editorconfig` explicitly says `GenerateDocumentationFile` is needed for IDE0005 to appear during CLI builds, but M `Directory.Build.props` does not enable it; L0 does. Microsoft IDE0005 docs confirm that XML documentation generation is necessary for build-time reporting. A positive control with `-p:GenerateDocumentationFile=true` isolates the missing build property.

This test checks **build-time reporting of IDE0005**, not whether `dotnet format` can detect/fix the same style issue. Nor does it prove that the live Claude Code agent runs `dotnet build` on every relevant task.
