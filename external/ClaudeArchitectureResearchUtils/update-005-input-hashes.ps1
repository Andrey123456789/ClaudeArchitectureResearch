[CmdletBinding()]
param(
    [string]$Root = "C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = [System.IO.Path]::GetFullPath($Root)
$ManifestPath = Join-Path $Root "INPUT_HASHES.json"

$RunPlan = @(
    [pscustomobject]@{ Candidate = "M";  Run = "Run-01" },
    [pscustomobject]@{ Candidate = "M";  Run = "Run-02" },
    [pscustomobject]@{ Candidate = "L0"; Run = "Run-01" },
    [pscustomobject]@{ Candidate = "L0"; Run = "Run-02" },
    [pscustomobject]@{ Candidate = "L1"; Run = "Run-01" },
    [pscustomobject]@{ Candidate = "L1"; Run = "Run-02" },
    [pscustomobject]@{ Candidate = "K0"; Run = "Run-01" },
    [pscustomobject]@{ Candidate = "K0"; Run = "Run-02" },
    [pscustomobject]@{ Candidate = "K1"; Run = "Run-01" },
    [pscustomobject]@{ Candidate = "K1"; Run = "Run-02" }
)

function Assert-File {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Required file is missing: $Path"
    }
}

function Assert-Directory {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        throw "Required directory is missing: $Path"
    }
}

function Get-FileSha256 {
    param([string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-DirectoryManifestHash {
    param([string]$Directory)

    $fullRoot = [System.IO.Path]::GetFullPath($Directory).TrimEnd("\", "/")
    $lines = New-Object System.Collections.Generic.List[string]

    Get-ChildItem -LiteralPath $fullRoot -Recurse -Force -File |
        Sort-Object FullName |
        ForEach-Object {
            $relative = $_.FullName.Substring($fullRoot.Length + 1).Replace("\", "/")
            $hash = Get-FileSha256 $_.FullName
            $lines.Add("$relative`t$hash")
        }

    $payload = [string]::Join("`n", $lines)
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($payload)

    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace("-", "").ToLowerInvariant()
    }
    finally {
        $sha.Dispose()
    }
}

function Write-Utf8NoBom {
    param(
        [string]$Path,
        [string]$Content
    )

    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $encoding)
}

Assert-Directory $Root
Assert-File (Join-Path $Root "SOURCE_COMMIT.txt")

$sourceCommit = (Get-Content -LiteralPath (Join-Path $Root "SOURCE_COMMIT.txt") -Raw).Trim()
if ([string]::IsNullOrWhiteSpace($sourceCommit)) {
    throw "SOURCE_COMMIT.txt is empty."
}

$expectedTaskHash = $null
$expectedInventoryHash = $null
$expectedSharedHash = $null
$expectedBaselineHash = $null
$candidateHashes = @{}

foreach ($item in $RunPlan) {
    $runRoot = Join-Path (Join-Path $Root $item.Candidate) $item.Run

    $taskPath = Join-Path $runRoot "TASK.md"
    $candidatePath = Join-Path $runRoot "CANDIDATE.md"
    $inventoryPath = Join-Path $runRoot "source\inventory.json"
    $sharedPath = Join-Path $runRoot "source\shared-research-invariants.json"
    $baselinePath = Join-Path $runRoot "source\v2-baseline"
    $outputPath = Join-Path $runRoot "output"

    Assert-File $taskPath
    Assert-File $candidatePath
    Assert-File $inventoryPath
    Assert-File $sharedPath
    Assert-Directory $baselinePath
    Assert-Directory $outputPath

    $assignedCandidatePath = Join-Path $runRoot "ASSIGNED_CANDIDATE.txt"
    if (Test-Path -LiteralPath $assignedCandidatePath) {
        throw "Legacy ASSIGNED_CANDIDATE.txt must not exist: $assignedCandidatePath"
    }

    $taskHash = Get-FileSha256 $taskPath
    if ($null -eq $expectedTaskHash) {
        $expectedTaskHash = $taskHash
    }
    elseif ($taskHash -ne $expectedTaskHash) {
        throw "TASK.md differs between runs. First mismatch: $taskPath"
    }

    $candidateHash = Get-FileSha256 $candidatePath
    if (-not $candidateHashes.ContainsKey($item.Candidate)) {
        $candidateHashes[$item.Candidate] = $candidateHash
    }
    elseif ($candidateHash -ne $candidateHashes[$item.Candidate]) {
        throw "CANDIDATE.md differs between replicates for $($item.Candidate)."
    }

    $inventoryHash = Get-FileSha256 $inventoryPath
    if ($null -eq $expectedInventoryHash) {
        $expectedInventoryHash = $inventoryHash
    }
    elseif ($inventoryHash -ne $expectedInventoryHash) {
        throw "inventory.json differs between runs. First mismatch: $inventoryPath"
    }

    $sharedHash = Get-FileSha256 $sharedPath
    if ($null -eq $expectedSharedHash) {
        $expectedSharedHash = $sharedHash
    }
    elseif ($sharedHash -ne $expectedSharedHash) {
        throw "shared-research-invariants.json differs between runs. First mismatch: $sharedPath"
    }

    $baselineHash = Get-DirectoryManifestHash $baselinePath
    if ($null -eq $expectedBaselineHash) {
        $expectedBaselineHash = $baselineHash
    }
    elseif ($baselineHash -ne $expectedBaselineHash) {
        throw "v2-baseline differs between runs. First mismatch: $baselinePath"
    }
}

# Validate the expected final TASK.md hash discussed for the corrected contract.
$ExpectedCorrectedTaskHash = "37e3dcda7c41a51dac81782e0a7319dec62dc97efe8c7334f9e85b5e10c0d029"

if ($expectedTaskHash -ne $ExpectedCorrectedTaskHash) {
    throw @"
TASK.md is internally consistent across all ten runs, but it is not the corrected TASK.md version expected by this repair script.

Actual:
$expectedTaskHash

Expected:
$ExpectedCorrectedTaskHash

Nothing was changed.
"@
}

$manifest = [ordered]@{
    schema_version = "1.0"
    source_commit = $sourceCommit
    created_utc = [DateTime]::UtcNow.ToString("o")
    structure = "candidate/Run-01|Run-02 with TASK.md + CANDIDATE.md + source + output"
    run_count = 10
    hashes = [ordered]@{
        task_sha256 = $expectedTaskHash
        inventory_sha256 = $expectedInventoryHash
        shared_research_invariants_sha256 = $expectedSharedHash
        v2_baseline_manifest_sha256 = $expectedBaselineHash
        candidate_sha256 = [ordered]@{
            M  = $candidateHashes["M"]
            L0 = $candidateHashes["L0"]
            L1 = $candidateHashes["L1"]
            K0 = $candidateHashes["K0"]
            K1 = $candidateHashes["K1"]
        }
    }
}

$json = $manifest | ConvertTo-Json -Depth 8
Write-Utf8NoBom -Path $ManifestPath -Content ($json + "`n")

Write-Host ""
Write-Host "INPUT_HASHES.json updated successfully."
Write-Host ""
Write-Host "Root:       $Root"
Write-Host "Manifest:   $ManifestPath"
Write-Host "Created UTC: $($manifest.created_utc)"
Write-Host ""
Write-Host "TASK SHA256:"
Write-Host "  $expectedTaskHash"
Write-Host ""
Write-Host "All ten TASK.md files are identical."
Write-Host "All candidate replicate pairs are identical."
Write-Host "All source inputs are identical across all ten runs."
Write-Host ""
