[CmdletBinding()]
param(
    [string]$Root = "C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.2"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = [System.IO.Path]::GetFullPath($Root)
$Candidates = @("M", "L0", "L1", "K0", "K1")
$Runs = @("Run-01", "Run-02")

function Assert-File([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Required file not found: $Path"
    }
}

function Assert-Directory([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        throw "Required directory not found: $Path"
    }
}

function Get-Sha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Write-Utf8NoBom([string]$Path, [string]$Content) {
    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $encoding)
}

function Get-AllRunRoots {
    $roots = @()
    foreach ($candidate in $Candidates) {
        foreach ($run in $Runs) {
            $roots += (Join-Path (Join-Path $Root $candidate) $run)
        }
    }
    return $roots
}

Write-Host ""
Write-Host "Iteration 005 / 5.2 repair"
Write-Host "Root: $Root"
Write-Host ""

Assert-Directory $Root

$GoalPromptPath = Join-Path $Root "GOAL_PROMPT.txt"
$ManifestPath = Join-Path $Root "INPUT_HASHES.json"
$ReadmePath = Join-Path $Root "README.md"
$LegacyReadmePath = Join-Path $Root "README-5.2.md"

Assert-File $GoalPromptPath
Assert-File $ManifestPath

$runRoots = Get-AllRunRoots

# ---------------------------------------------------------------------------
# 1. Preflight: validate structure and protect existing experimental output.
# ---------------------------------------------------------------------------

foreach ($runRoot in $runRoots) {
    Assert-Directory $runRoot
    Assert-File (Join-Path $runRoot "TASK.md")
    Assert-File (Join-Path $runRoot "CANDIDATE.md")
    Assert-File (Join-Path $runRoot "source\inventory.json")
    Assert-File (Join-Path $runRoot "source\shared-research-invariants.json")
    Assert-Directory (Join-Path $runRoot "source\v2-baseline")
    Assert-Directory (Join-Path $runRoot "output")

    $outputItems = @(Get-ChildItem -LiteralPath (Join-Path $runRoot "output") -Force)
    if ($outputItems.Count -ne 0) {
        throw "Refusing to repair because output is not empty: $(Join-Path $runRoot 'output'). Preserve/relocate experimental evidence first."
    }
}

# Candidate files must already be identical inside each replicate pair.
foreach ($candidate in $Candidates) {
    $c1 = Join-Path (Join-Path (Join-Path $Root $candidate) "Run-01") "CANDIDATE.md"
    $c2 = Join-Path (Join-Path (Join-Path $Root $candidate) "Run-02") "CANDIDATE.md"

    if ((Get-Sha256 $c1) -ne (Get-Sha256 $c2)) {
        throw "Candidate parity failure for ${candidate}: Run-01 and Run-02 CANDIDATE.md differ."
    }
}

# ---------------------------------------------------------------------------
# 2. Patch the common TASK.md in every run.
#    Only repair the known stale section reference.
# ---------------------------------------------------------------------------

$oldText = "shared construction requirements from Section 6 and ``source/shared-research-invariants.json`` are preserved;"
$newText = "shared construction requirements from Section 7 and ``source/shared-research-invariants.json`` are preserved;"

$taskTexts = @()

foreach ($runRoot in $runRoots) {
    $taskPath = Join-Path $runRoot "TASK.md"
    $text = [System.IO.File]::ReadAllText($taskPath)

    if ($text.Contains($oldText)) {
        $count = ([regex]::Matches($text, [regex]::Escape($oldText))).Count
        if ($count -ne 1) {
            throw "Expected exactly one stale Section-6 reference in $taskPath, found $count."
        }
        $text = $text.Replace($oldText, $newText)
        Write-Utf8NoBom -Path $taskPath -Content $text
    }
    elseif (-not $text.Contains($newText)) {
        throw "TASK.md contains neither the expected old nor corrected acceptance text: $taskPath"
    }

    $taskTexts += $text
}

# All ten TASK.md files must now be byte-identical.
$taskHashes = @($runRoots | ForEach-Object {
    Get-Sha256 (Join-Path $_ "TASK.md")
} | Sort-Object -Unique)

if ($taskHashes.Count -ne 1) {
    throw "TASK parity failure after repair: the ten TASK.md files are not byte-identical."
}

$taskHash = $taskHashes[0]

# ---------------------------------------------------------------------------
# 3. Canonicalize operator documentation.
#    Keep one README only; GOAL_PROMPT.txt is authoritative for launch text.
# ---------------------------------------------------------------------------

$readme = @'
# Iteration 005 / 5.2

This directory is the corrected second template-generation series.

`5.1` preserves the earlier generation state and diagnostic evidence.
`5.2` is the clean rerun series created from the same candidate/source inputs
with corrected shared experimental controls.

## Run structure

```text
5.2/
├── M/
│   ├── Run-01/
│   └── Run-02/
├── L0/
│   ├── Run-01/
│   └── Run-02/
├── L1/
│   ├── Run-01/
│   └── Run-02/
├── K0/
│   ├── Run-01/
│   └── Run-02/
├── K1/
│   ├── Run-01/
│   └── Run-02/
├── GOAL_PROMPT.txt
├── INPUT_HASHES.json
├── SOURCE_COMMIT.txt
└── README.md
```

Each run contains:

```text
Run-XX/
├── TASK.md
├── CANDIDATE.md
├── source/
│   ├── inventory.json
│   ├── shared-research-invariants.json
│   └── v2-baseline/
└── output/
```

## What changed from 5.1

The shared construction contract was tightened equally for all candidates:

- every frozen inventory `trigger_class` must be preserved exactly;
- path/workflow policy must not be promoted to always-loaded merely for convenience;
- multi-step procedures belong to workflow owners rather than `CLAUDE.md`;
- deterministic hooks/scripts must be compatible with the Windows Claude Desktop environment;
- parent/sibling workspace inspection is explicitly forbidden;
- generation runs as an autonomous Goal with repeated audit-and-repair until objective acceptance gates pass.

`CANDIDATE.md` files were not changed for these corrections.

## Execution

Use a fresh Claude Desktop Code session for every run and keep model/effort settings identical.

For every run, use **exactly the contents of `GOAL_PROMPT.txt`** as the Goal prompt.

Do not replace it with the older one-shot instruction.

The Goal must continue through draft -> audit -> repair -> audit cycles until all binding
acceptance gates in `TASK.md` pass. Once all gates pass, it must stop rather than perform
unbounded aesthetic refactoring.

Do not add candidate-specific hints and do not expose another run's output.

## Evidence rule

Do not manually repair generated output before comparative audit.
Preserve raw run output as evidence.

The construction Claude may see the run's `inventory.json`.
A later benchmark-execution Claude must not see research/evaluation material.
'@

Write-Utf8NoBom -Path $ReadmePath -Content $readme

if (Test-Path -LiteralPath $LegacyReadmePath) {
    Remove-Item -LiteralPath $LegacyReadmePath -Force
}

# ---------------------------------------------------------------------------
# 4. Recompute common hashes from the actual 5.2 files.
#    Preserve manifest fields whose derivation belongs to the earlier
#    preparation tooling (notably v2_baseline_manifest_sha256), but verify
#    all source trees are byte-identical across the ten runs.
# ---------------------------------------------------------------------------

$inventoryHashes = @($runRoots | ForEach-Object {
    Get-Sha256 (Join-Path $_ "source\inventory.json")
} | Sort-Object -Unique)

if ($inventoryHashes.Count -ne 1) {
    throw "Source parity failure: inventory.json differs across runs."
}

$sharedHashes = @($runRoots | ForEach-Object {
    Get-Sha256 (Join-Path $_ "source\shared-research-invariants.json")
} | Sort-Object -Unique)

if ($sharedHashes.Count -ne 1) {
    throw "Source parity failure: shared-research-invariants.json differs across runs."
}

# Compare V2 baseline trees by relative path + file hash.
function Get-TreeSignature([string]$Directory) {
    $base = [System.IO.Path]::GetFullPath($Directory).TrimEnd('\','/')
    $entries = @(
        Get-ChildItem -LiteralPath $base -Recurse -File -Force |
        ForEach-Object {
            $relative = $_.FullName.Substring($base.Length).TrimStart('\','/').Replace('\','/')
            $hash = Get-Sha256 $_.FullName
            "$relative`t$hash"
        } |
        Sort-Object
    )

    return ($entries -join "`n")
}

$baselineReference = $null
foreach ($runRoot in $runRoots) {
    $signature = Get-TreeSignature (Join-Path $runRoot "source\v2-baseline")
    if ($null -eq $baselineReference) {
        $baselineReference = $signature
    }
    elseif ($signature -cne $baselineReference) {
        throw "Source parity failure: v2-baseline tree differs across runs."
    }
}

$manifestRaw = [System.IO.File]::ReadAllText($ManifestPath)
$manifest = $manifestRaw | ConvertFrom-Json

if ($null -eq $manifest.hashes) {
    throw "INPUT_HASHES.json does not contain a hashes object."
}

$manifest.hashes.task_sha256 = $taskHash
$manifest.hashes.inventory_sha256 = $inventoryHashes[0]
$manifest.hashes.shared_research_invariants_sha256 = $sharedHashes[0]

# Recompute candidate hashes from Run-01 after pair-parity validation.
foreach ($candidate in $Candidates) {
    $candidatePath = Join-Path (Join-Path (Join-Path $Root $candidate) "Run-01") "CANDIDATE.md"
    $manifest.hashes.candidate_sha256.$candidate = Get-Sha256 $candidatePath
}

# Keep source_commit and v2_baseline_manifest_sha256 unchanged: their canonical
# derivation belongs to the preparation tooling. We verified baseline byte parity
# independently above.
$manifest.created_utc = [DateTime]::UtcNow.ToString("o")
$manifest.structure = "5.2 candidate/Run-01|Run-02 with TASK.md + CANDIDATE.md + source + output; Goal launch via GOAL_PROMPT.txt"

$json = $manifest | ConvertTo-Json -Depth 12
Write-Utf8NoBom -Path $ManifestPath -Content ($json + "`n")

# ---------------------------------------------------------------------------
# 5. Final validation.
# ---------------------------------------------------------------------------

# TASK parity.
$finalTaskHashes = @($runRoots | ForEach-Object {
    Get-Sha256 (Join-Path $_ "TASK.md")
} | Sort-Object -Unique)

if ($finalTaskHashes.Count -ne 1) {
    throw "Final validation failed: TASK.md parity."
}

# Candidate pair parity.
foreach ($candidate in $Candidates) {
    $c1 = Join-Path (Join-Path (Join-Path $Root $candidate) "Run-01") "CANDIDATE.md"
    $c2 = Join-Path (Join-Path (Join-Path $Root $candidate) "Run-02") "CANDIDATE.md"
    if ((Get-Sha256 $c1) -ne (Get-Sha256 $c2)) {
        throw "Final validation failed: CANDIDATE.md parity for ${candidate}."
    }
}

# Outputs must still be empty.
foreach ($runRoot in $runRoots) {
    $items = @(Get-ChildItem -LiteralPath (Join-Path $runRoot "output") -Force)
    if ($items.Count -ne 0) {
        throw "Final validation failed: non-empty output in $runRoot."
    }
}

# Manifest must now match actual common input hashes.
$finalManifest = ([System.IO.File]::ReadAllText($ManifestPath) | ConvertFrom-Json)

if ($finalManifest.hashes.task_sha256 -ne $finalTaskHashes[0]) {
    throw "Final validation failed: task_sha256 mismatch."
}
if ($finalManifest.hashes.inventory_sha256 -ne $inventoryHashes[0]) {
    throw "Final validation failed: inventory_sha256 mismatch."
}
if ($finalManifest.hashes.shared_research_invariants_sha256 -ne $sharedHashes[0]) {
    throw "Final validation failed: shared_research_invariants_sha256 mismatch."
}

Write-Host ""
Write-Host "5.2 repair completed successfully." -ForegroundColor Green
Write-Host ""
Write-Host "TASK SHA256:"
Write-Host "  $($finalTaskHashes[0])"
Write-Host ""
Write-Host "Validated:"
Write-Host "  - 10/10 TASK.md files are byte-identical"
Write-Host "  - all 5 candidate replicate pairs are identical"
Write-Host "  - inventory.json is identical across all runs"
Write-Host "  - shared-research-invariants.json is identical across all runs"
Write-Host "  - v2-baseline trees are identical across all runs"
Write-Host "  - all 10 output directories are empty"
Write-Host "  - INPUT_HASHES.json matches the repaired common inputs"
Write-Host "  - README.md is canonical for 5.2"
Write-Host "  - README-5.2.md was removed if present"
Write-Host ""
Write-Host "5.2 is ready for the first Goal run."
