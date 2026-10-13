[CmdletBinding()]
param(
    [string]$DestinationRoot = "C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005",
    [switch]$Recreate
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Intended location:
#   <repo>\research\tools\prepare-005-runs.ps1
#
# The repository root is derived from the script location, so this script can
# be launched from any current working directory.
$RepoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\.."))
$DestinationRoot = [System.IO.Path]::GetFullPath($DestinationRoot)

function Assert-File([string]$RelativePath) {
    $full = Join-Path $RepoRoot $RelativePath
    if (-not (Test-Path -LiteralPath $full -PathType Leaf)) {
        throw "Required source file is missing: $RelativePath"
    }
}

function Assert-Directory([string]$RelativePath) {
    $full = Join-Path $RepoRoot $RelativePath
    if (-not (Test-Path -LiteralPath $full -PathType Container)) {
        throw "Required source directory is missing: $RelativePath"
    }
}

function Copy-RelativeFile(
    [string]$RunRoot,
    [string]$RelativePath
) {
    $source = Join-Path $RepoRoot $RelativePath
    $target = Join-Path $RunRoot $RelativePath
    $targetDir = Split-Path -Parent $target

    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    Copy-Item -LiteralPath $source -Destination $target -Force
}

function Copy-RelativeDirectory(
    [string]$RunRoot,
    [string]$RelativePath
) {
    $source = Join-Path $RepoRoot $RelativePath
    $target = Join-Path $RunRoot $RelativePath

    New-Item -ItemType Directory -Path $target -Force | Out-Null

    # Copy contents including dot-prefixed items such as .claude.
    Get-ChildItem -LiteralPath $source -Force | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $target -Recurse -Force
    }
}

function Write-Utf8NoBom(
    [string]$Path,
    [string]$Content
) {
    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $encoding)
}

function Assert-NoForbiddenInputs([string]$RunRoot) {
    $forbidden = @(
        "research\metrics",
        "research\benchmark",
        "research\e0",
        ".git"
    )

    foreach ($relative in $forbidden) {
        $full = Join-Path $RunRoot $relative
        if (Test-Path -LiteralPath $full) {
            throw "Isolation validation failed. Forbidden path exists in run workspace: $relative"
        }
    }
}

function Assert-OutputEmpty([string]$RunRoot) {
    $output = Join-Path $RunRoot "output"
    $items = @(Get-ChildItem -LiteralPath $output -Force)
    if ($items.Count -ne 0) {
        throw "Fresh-output validation failed: $output is not empty."
    }
}

function Assert-DestinationOutsideRepository {
    $repo = $RepoRoot.TrimEnd("\", "/")
    $dest = $DestinationRoot.TrimEnd("\", "/")

    if ($dest.Equals($repo, [System.StringComparison]::OrdinalIgnoreCase) -or
        $dest.StartsWith($repo + "\", [System.StringComparison]::OrdinalIgnoreCase)) {
        throw @"
Destination must be outside the research repository.

Repository:
$RepoRoot

Destination:
$DestinationRoot

Iteration 005 uses controlled workspace isolation, so run workspaces must not be
created inside ClaudeArchitectureResearch.
"@
    }
}

# ---------------------------------------------------------------------------
# Run plan
#
# Folder names contain BOTH execution order and human-readable candidate/
# replicate identity. This avoids opaque run-01/run-02 directories while still
# preserving the intended execution order.
#
# Two independent replicates are generated for each candidate. They are NOT
# separate candidate variants.
# ---------------------------------------------------------------------------

$runs = @(
    [pscustomobject]@{ Number = 1;  Folder = "01-M-R1";  Replicate = "M-R1";  Candidate = "M"  },
    [pscustomobject]@{ Number = 2;  Folder = "02-L0-R1"; Replicate = "L0-R1"; Candidate = "L0" },
    [pscustomobject]@{ Number = 3;  Folder = "03-L1-R1"; Replicate = "L1-R1"; Candidate = "L1" },
    [pscustomobject]@{ Number = 4;  Folder = "04-K0-R1"; Replicate = "K0-R1"; Candidate = "K0" },
    [pscustomobject]@{ Number = 5;  Folder = "05-K1-R1"; Replicate = "K1-R1"; Candidate = "K1" },
    [pscustomobject]@{ Number = 6;  Folder = "06-M-R2";  Replicate = "M-R2";  Candidate = "M"  },
    [pscustomobject]@{ Number = 7;  Folder = "07-L0-R2"; Replicate = "L0-R2"; Candidate = "L0" },
    [pscustomobject]@{ Number = 8;  Folder = "08-L1-R2"; Replicate = "L1-R2"; Candidate = "L1" },
    [pscustomobject]@{ Number = 9;  Folder = "09-K0-R2"; Replicate = "K0-R2"; Candidate = "K0" },
    [pscustomobject]@{ Number = 10; Folder = "10-K1-R2"; Replicate = "K1-R2"; Candidate = "K1" }
)

# Legacy folders created by the earlier version of this utility.
$legacyFolders = 1..10 | ForEach-Object { "run-{0:D2}" -f $_ }

# ---------------------------------------------------------------------------
# Preflight
# ---------------------------------------------------------------------------

if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot ".git"))) {
    throw "Could not identify repository root from script location: $RepoRoot"
}

Assert-DestinationOutsideRepository

$gitHead = (& git -C $RepoRoot rev-parse HEAD).Trim()
if (-not $gitHead) {
    throw "Unable to read Git HEAD from $RepoRoot"
}

# The preparation script itself is allowed to be untracked/modified because it
# is tooling only and is NOT copied into experiment workspaces.
# Any other dirty repository state still blocks workspace generation.
$selfRelative = "research/tools/" + (Split-Path -Leaf $PSCommandPath)
$selfRelativeNormalized = $selfRelative.Replace("\", "/")

$statusLines = @(& git -C $RepoRoot status --porcelain --untracked-files=all)

$relevantDirty = @(
    $statusLines | Where-Object {
        if ([string]::IsNullOrWhiteSpace($_)) {
            return $false
        }

        # Porcelain v1 path starts after two status columns plus one space.
        $path = $_.Substring(3).Replace("\", "/")

        # Handle rename syntax "old -> new" conservatively.
        if ($path.Contains(" -> ")) {
            $path = ($path.Split(" -> ")[-1]).Trim()
        }

        return $path -ne $selfRelativeNormalized
    }
)

if ($relevantDirty.Count -gt 0) {
    $details = ($relevantDirty -join "`n")
    throw @"
Source repository contains changes that affect experiment reproducibility.

The preparation script itself is allowed to be uncommitted, but all other
changes must be committed or stashed before preparing Iteration 005 workspaces.

Repository:
$RepoRoot

Blocking changes:
$details
"@
}

$sharedFiles = @(
    "prompts\005-template-generation.md",
    "research\observations\001-v3-design-proposal.md",
    "research\observations\002-candidate-space-analysis.md",
    "research\policy\inventory.json",
    "research\policy\shared-research-invariants.json"
)

foreach ($file in $sharedFiles) {
    Assert-File $file
}

Assert-Directory "templates\v2-baseline"

foreach ($candidate in @("M", "L0", "L1", "K0", "K1")) {
    Assert-File "research\candidates\$candidate\DESIGN.md"
    Assert-File "research\candidates\$candidate\CORE_FEATURES.md"
}

Assert-File "research\capabilities\capability-framework.md"

# Detect old opaque folders and/or already-created new folders before changing
# anything. If they exist, require an explicit -Recreate.
$existingKnownFolders = @()

if (Test-Path -LiteralPath $DestinationRoot -PathType Container) {
    foreach ($name in $legacyFolders) {
        $full = Join-Path $DestinationRoot $name
        if (Test-Path -LiteralPath $full -PathType Container) {
            $existingKnownFolders += $full
        }
    }

    foreach ($run in $runs) {
        $full = Join-Path $DestinationRoot $run.Folder
        if (Test-Path -LiteralPath $full -PathType Container) {
            $existingKnownFolders += $full
        }
    }
}

if ($existingKnownFolders.Count -gt 0 -and -not $Recreate) {
    $details = ($existingKnownFolders -join "`n")
    throw @"
Iteration 005 workspace folders already exist:

$details

Nothing was changed.

The earlier utility created opaque run-01 ... run-10 folders. This version uses
explicit names such as 01-M-R1 and 02-L0-R1.

If these existing folders contain no results you need, rerun with -Recreate.
-Recreate removes ONLY the known Iteration 005 workspace folder names listed
above; it does not delete unrelated files from the destination root.
"@
}

# ---------------------------------------------------------------------------
# Recreate known old/new run directories when explicitly requested.
# ---------------------------------------------------------------------------

if ($Recreate -and (Test-Path -LiteralPath $DestinationRoot -PathType Container)) {
    $knownFolderNames = @($legacyFolders) + @($runs | ForEach-Object { $_.Folder })

    foreach ($name in $knownFolderNames | Select-Object -Unique) {
        $full = Join-Path $DestinationRoot $name
        if (Test-Path -LiteralPath $full) {
            Remove-Item -LiteralPath $full -Recurse -Force
        }
    }
}

# ---------------------------------------------------------------------------
# Create all ten workspaces.
# ---------------------------------------------------------------------------

New-Item -ItemType Directory -Path $DestinationRoot -Force | Out-Null

$results = @()

foreach ($run in $runs) {
    $runRoot = Join-Path $DestinationRoot $run.Folder

    New-Item -ItemType Directory -Path $runRoot -Force | Out-Null
    New-Item -ItemType Directory -Path (Join-Path $runRoot "output") -Force | Out-Null

    # This tiny selector is intentional: the generation prompt is byte-for-byte
    # identical across all runs, while this file tells it which candidate design
    # is assigned to the current isolated workspace.
    Write-Utf8NoBom `
        -Path (Join-Path $runRoot "ASSIGNED_CANDIDATE.txt") `
        -Content ($run.Candidate + "`n")

    # Shared allowlist.
    foreach ($file in $sharedFiles) {
        Copy-RelativeFile -RunRoot $runRoot -RelativePath $file
    }

    Copy-RelativeDirectory `
        -RunRoot $runRoot `
        -RelativePath "templates\v2-baseline"

    # Assigned candidate only.
    Copy-RelativeFile `
        -RunRoot $runRoot `
        -RelativePath "research\candidates\$($run.Candidate)\DESIGN.md"

    Copy-RelativeFile `
        -RunRoot $runRoot `
        -RelativePath "research\candidates\$($run.Candidate)\CORE_FEATURES.md"

    # L1 is defined as an extension/transformation of L0.
    if ($run.Candidate -eq "L1") {
        Copy-RelativeFile `
            -RunRoot $runRoot `
            -RelativePath "research\candidates\L0\DESIGN.md"

        Copy-RelativeFile `
            -RunRoot $runRoot `
            -RelativePath "research\capabilities\capability-framework.md"
    }

    # K1 is defined as an extension/transformation of K0.
    if ($run.Candidate -eq "K1") {
        Copy-RelativeFile `
            -RunRoot $runRoot `
            -RelativePath "research\candidates\K0\DESIGN.md"

        Copy-RelativeFile `
            -RunRoot $runRoot `
            -RelativePath "research\capabilities\capability-framework.md"
    }

    Assert-NoForbiddenInputs $runRoot
    Assert-OutputEmpty $runRoot

    $fileCount = @(
        Get-ChildItem -LiteralPath $runRoot -Recurse -Force -File
    ).Count

    $results += [pscustomobject]@{
        Order     = $run.Number
        Workspace = $run.Folder
        Replicate = $run.Replicate
        Candidate = $run.Candidate
        Files     = $fileCount
        Path      = $runRoot
    }
}

# ---------------------------------------------------------------------------
# Result
# ---------------------------------------------------------------------------

Write-Host ""
Write-Host "Iteration 005 workspaces created successfully."
Write-Host ""
Write-Host "Source repository: $RepoRoot"
Write-Host "Source commit:     $gitHead"
Write-Host "Destination:       $DestinationRoot"
Write-Host ""

$results | Format-Table Order, Workspace, Candidate, Files, Path -AutoSize

Write-Host ""
Write-Host "Execution order:"
foreach ($run in $runs) {
    Write-Host ("  {0,2}. {1}" -f $run.Number, $run.Folder)
}

Write-Host ""
Write-Host "Next:"
Write-Host "  1. Open 01-M-R1 as the Claude Desktop Code root."
Write-Host "  2. Use Claude Opus 5.5 / xhigh."
Write-Host "  3. Run prompts\005-template-generation.md."
Write-Host "  4. After the run, verify Desktop version:"
Write-Host "     Get-AppxPackage -Name Claude | Select-Object Name, Version, PackageFullName"
Write-Host "  5. Continue in the printed order through 10-K1-R2."
Write-Host ""
Write-Host "Expected Claude Desktop version: 2.26454.2.0"
Write-Host ""
