[CmdletBinding()]
param(
    [string]$Root = "C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.2",
    [switch]$RecreateM1
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = [System.IO.Path]::GetFullPath($Root)
$CandidateSource = Join-Path $PSScriptRoot "M1-CANDIDATE.md"
$GoalPrompt = Join-Path $Root "GOAL_PROMPT.txt"
$Readme = Join-Path $Root "README.md"
$ProtocolDir = Join-Path $Root "protocol-amendments"
$AmendmentMd = Join-Path $ProtocolDir "5.2.3-m1-extension.md"
$AmendmentJson = Join-Path $ProtocolDir "5.2.3-manifest.json"
$M1Root = Join-Path $Root "M1"

$ExistingCandidates = @("M", "L0", "L1", "K0", "K1")
$ExistingRuns = @("Run-01", "Run-02")
$SecondRoundCandidates = @("M", "L0", "L1", "K0", "K1")

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

function Get-TreeSignature([string]$Directory) {
    $base = [System.IO.Path]::GetFullPath($Directory).TrimEnd('\','/')
    $entries = @(
        Get-ChildItem -LiteralPath $base -Recurse -File -Force |
        ForEach-Object {
            $relative = $_.FullName.Substring($base.Length).TrimStart('\','/').Replace('\','/')
            "$relative`t$(Get-Sha256 $_.FullName)"
        } |
        Sort-Object
    )

    $joined = $entries -join "`n"
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($joined)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace("-", "").ToLowerInvariant()
    }
    finally {
        $sha.Dispose()
    }
}

function Get-RunRoot([string]$Candidate, [string]$Run) {
    return Join-Path -Path (Join-Path -Path $Root -ChildPath $Candidate) -ChildPath $Run
}

Write-Host ""
Write-Host "Iteration 005 / Protocol Amendment 5.2.3 - add M1"
Write-Host "Root: $Root"
Write-Host ""

Assert-Directory $Root
Assert-File $CandidateSource
Assert-File $GoalPrompt
Assert-File $Readme

# ---------------------------------------------------------------------------
# A. Validate and freeze the original 10-run experiment.
# ---------------------------------------------------------------------------

Write-Host "Checklist A: validate the completed original 10 runs"

$existingRunRoots = @()
$existingOutputSignatures = @{}
$sourceReference = $null

foreach ($candidate in $ExistingCandidates) {
    foreach ($run in $ExistingRuns) {
        $runRoot = Get-RunRoot $candidate $run
        $existingRunRoots += $runRoot

        Assert-Directory $runRoot
        Assert-File (Join-Path $runRoot "TASK.md")
        Assert-File (Join-Path $runRoot "CANDIDATE.md")
        Assert-Directory (Join-Path $runRoot "source")
        Assert-Directory (Join-Path $runRoot "output")
        Assert-File (Join-Path $runRoot "output\GENERATION_REPORT.md")

        $existingOutputSignatures[$runRoot] = Get-TreeSignature (Join-Path $runRoot "output")

        $sourceSig = Get-TreeSignature (Join-Path $runRoot "source")
        if ($null -eq $sourceReference) {
            $sourceReference = $sourceSig
        }
        elseif ($sourceSig -ne $sourceReference) {
            throw "Source-tree parity failure in existing run: $runRoot"
        }
    }
}

if (@($existingRunRoots).Count -ne 10) {
    throw "Expected 10 existing runs, found $(@($existingRunRoots).Count)."
}

Write-Host "  PASS - all 10 existing runs have generation reports"
Write-Host "  PASS - source corpus is identical across all 10 existing runs"

# Use the completed second round as the canonical current protocol.
$secondRoundTaskHashes = @(
    @(
        foreach ($candidate in $SecondRoundCandidates) {
            Get-Sha256 (Join-Path (Get-RunRoot $candidate "Run-02") "TASK.md")
        }
    ) | Sort-Object -Unique
)

if (@($secondRoundTaskHashes).Count -ne 1) {
    throw "Second-round TASK.md files are not byte-identical. Refusing to create M1."
}

$canonicalTask = Join-Path (Get-RunRoot "M" "Run-02") "TASK.md"
$canonicalSource = Join-Path (Get-RunRoot "M" "Run-02") "source"
$canonicalTaskHash = $secondRoundTaskHashes[0]
$canonicalTaskText = [System.IO.File]::ReadAllText($canonicalTask)

foreach ($phrase in @(
    "bounded verification protocol",
    "primary substantive audit",
    "confirmation audit",
    "zero concrete template defects"
)) {
    if (-not $canonicalTaskText.Contains($phrase)) {
        throw "Canonical TASK.md is not the expected 5.2.2 task. Missing: $phrase"
    }
}

$goalText = [System.IO.File]::ReadAllText($GoalPrompt)
foreach ($phrase in @(
    "bounded verification protocol",
    "primary substantive audit",
    "confirmation audit",
    "zero concrete template defects",
    "Do not start extra audit cycles"
)) {
    if (-not $goalText.Contains($phrase)) {
        throw "GOAL_PROMPT.txt is not the expected bounded prompt. Missing: $phrase"
    }
}

Write-Host "  PASS - second-round TASK.md is the shared 5.2.2 protocol"
Write-Host "  PASS - current GOAL_PROMPT.txt is the bounded-convergence prompt"

# ---------------------------------------------------------------------------
# B. Protect existing M1 evidence if present.
# ---------------------------------------------------------------------------

if (Test-Path -LiteralPath $M1Root) {
    $existingM1OutputFiles = @(
        Get-ChildItem -LiteralPath $M1Root -Recurse -File -Force -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -match '[\\/]output[\\/]' }
    )

    if (@($existingM1OutputFiles).Count -gt 0) {
        throw "M1 already contains generated output/evidence. Refusing to overwrite it."
    }

    if (-not $RecreateM1) {
        throw "M1 already exists. Use -RecreateM1 only if it has no generated output and you intentionally want to rebuild it."
    }

    Remove-Item -LiteralPath $M1Root -Recurse -Force
}

# ---------------------------------------------------------------------------
# C. Create M1 Run-01 and Run-02.
# ---------------------------------------------------------------------------

Write-Host ""
Write-Host "Checklist B: create M1 workspaces"

$candidateText = [System.IO.File]::ReadAllText($CandidateSource)

foreach ($run in $ExistingRuns) {
    $runRoot = Get-RunRoot "M1" $run
    New-Item -ItemType Directory -Path $runRoot -Force | Out-Null

    Copy-Item -LiteralPath $canonicalTask -Destination (Join-Path $runRoot "TASK.md")
    Write-Utf8NoBom -Path (Join-Path $runRoot "CANDIDATE.md") -Content ($candidateText.TrimEnd() + "`r`n")
    Copy-Item -LiteralPath $canonicalSource -Destination (Join-Path $runRoot "source") -Recurse
    New-Item -ItemType Directory -Path (Join-Path $runRoot "output") -Force | Out-Null
}

Write-Host "  PASS - M1/Run-01 created"
Write-Host "  PASS - M1/Run-02 created"

# ---------------------------------------------------------------------------
# D. Validate M1 parity and candidate identity.
# ---------------------------------------------------------------------------

Write-Host ""
Write-Host "Checklist C: validate M1 inputs"

$m1Run01 = Get-RunRoot "M1" "Run-01"
$m1Run02 = Get-RunRoot "M1" "Run-02"
$m1Task01 = Join-Path $m1Run01 "TASK.md"
$m1Task02 = Join-Path $m1Run02 "TASK.md"
$m1Candidate01 = Join-Path $m1Run01 "CANDIDATE.md"
$m1Candidate02 = Join-Path $m1Run02 "CANDIDATE.md"
$m1CandidateHash = Get-Sha256 $m1Candidate01

if ((Get-Sha256 $m1Task01) -ne $canonicalTaskHash -or (Get-Sha256 $m1Task02) -ne $canonicalTaskHash) {
    throw "M1 TASK.md does not match the current 5.2.2 protocol."
}

if ((Get-Sha256 $m1Candidate02) -ne $m1CandidateHash) {
    throw "M1 Run-01 and Run-02 CANDIDATE.md files differ."
}

if ((Get-TreeSignature (Join-Path $m1Run01 "source")) -ne $sourceReference -or
    (Get-TreeSignature (Join-Path $m1Run02 "source")) -ne $sourceReference) {
    throw "M1 source corpus does not match the frozen source corpus."
}

foreach ($runRoot in @($m1Run01, $m1Run02)) {
    $items = @(Get-ChildItem -LiteralPath (Join-Path $runRoot "output") -Force)
    if (@($items).Count -ne 0) {
        throw "M1 output directory is not empty: $runRoot"
    }
}

$m1CandidateText = [System.IO.File]::ReadAllText($m1Candidate01)
foreach ($phrase in @(
    "M1 = **M + the same four replaceable capability slots used by L1/K1**",
    "architecture",
    "persistence",
    "backend-testing",
    "frontend",
    "stability levels",
    "Kinds × Scopes",
    "Composition is static",
    "Placement belongs to the frame; technique belongs to the leaf",
    "recognizable, well-refactored M/V2 system"
)) {
    if (-not $m1CandidateText.Contains($phrase)) {
        throw "M1 candidate definition is missing required design marker: $phrase"
    }
}

Write-Host "  PASS - both M1 TASK.md files match the current protocol"
Write-Host "  PASS - both M1 CANDIDATE.md files are byte-identical"
Write-Host "  PASS - both M1 source trees match the frozen corpus"
Write-Host "  PASS - both M1 output directories are empty"
Write-Host "  PASS - M1 defining properties are present"

# ---------------------------------------------------------------------------
# E. Record the 5.2.3 extension without rewriting old manifests.
# ---------------------------------------------------------------------------

Write-Host ""
Write-Host "Checklist D: record 5.2.3 provenance"

New-Item -ItemType Directory -Path $ProtocolDir -Force | Out-Null

$amendmentText = @'
# Iteration 005 / Protocol Amendment 5.2.3 — add Candidate M1

Iteration 5.2 is extended from 5 generated candidates × 2 independent runs (10 runs) to 6 × 2 (12 runs) by adding `M1/Run-01` and `M1/Run-02`.

M1 fills the missing matrix cell: **Minimal Modular + replaceable capabilities**.

The controlled comparison is:

- M ↔ M1 — capability value without Stability-first or Kinds × Scopes;
- L0 ↔ L1 — capability value inside Stability-first;
- K0 ↔ K1 — capability value inside Kinds × Scopes;
- M1 ↔ L1 ↔ K1 — whether the additional L/K meta-architecture adds value beyond the capability mechanism itself.

M1 uses the same four slots as L1/K1: architecture/clean-architecture, persistence/ef-core(sqlserver), backend-testing/nunit, and optional frontend/angular. It uses contracts, MODULE manifests, static selection/composition, runtime facets, leak checking, and frame/leaf separation while preserving M/V2-style organization outside those slots.

Both M1 runs use the current 5.2.2 TASK.md, the same frozen source corpus, the current bounded GOAL_PROMPT.txt, fresh independent Claude Desktop Code sessions, identical model/effort settings, and empty output directories.

The original 10 runs remain unchanged.
'@

Write-Utf8NoBom -Path $AmendmentMd -Content ($amendmentText.TrimEnd() + "`r`n")

$manifest = [ordered]@{
    schema_version = "1.0"
    amendment = "5.2.3"
    created_utc = [DateTime]::UtcNow.ToString("o")
    purpose = "Extend iteration 5.2 with Candidate M1 (Minimal Modular + replaceable capabilities)."
    experiment = [ordered]@{
        generated_candidates = @("M", "M1", "L0", "L1", "K0", "K1")
        generated_candidate_count = 6
        replicates_per_candidate = 2
        total_generated_runs = 12
        baseline = "V2"
    }
    hypothesis = [ordered]@{
        primary_comparison = "M vs M1"
        secondary_comparison = "M1 vs L1 vs K1"
        controlled_difference = "Add the same four replaceable capability slots/contracts/manifests/static composition used by L1/K1 while retaining M organization outside the slots."
    }
    m1 = [ordered]@{
        runs = @("M1/Run-01", "M1/Run-02")
        candidate_sha256 = $m1CandidateHash
        task_sha256 = $canonicalTaskHash
        source_tree_sha256 = $sourceReference
        goal_prompt_sha256 = Get-Sha256 $GoalPrompt
        output_initial_state = "empty"
        slots = @(
            "architecture:clean-architecture",
            "persistence:ef-core(sqlserver)",
            "backend-testing:nunit",
            "frontend:angular(optional)"
        )
    }
    provenance = [ordered]@{
        canonical_task_from = "M/Run-02/TASK.md"
        canonical_source_from = "M/Run-02/source"
        original_10_runs_modified = $false
        old_manifests_modified = $false
    }
}

Write-Utf8NoBom -Path $AmendmentJson -Content (($manifest | ConvertTo-Json -Depth 12) + "`r`n")

$readmeText = [System.IO.File]::ReadAllText($Readme)
$marker = "## Protocol amendment 5.2.3 — M1 extension"

if (-not $readmeText.Contains($marker)) {
    $append = @'

## Protocol amendment 5.2.3 — M1 extension

Iteration 5.2 was extended after the original 5×2 series with `M1/Run-01` and `M1/Run-02`.

M1 is **Minimal Modular + replaceable capabilities**: M/V2-style organization outside the capability subsystem, plus the same four static capability slots used by L1/K1.

The generated-candidate experiment is now **6 candidates × 2 independent replicates = 12 runs**: `M / M1 / L0 / L1 / K0 / K1`.

The original ten runs remain unchanged. M1 uses the current bounded-convergence TASK.md, the same frozen source corpus, and the current shared GOAL_PROMPT.txt.

See `protocol-amendments/5.2.3-m1-extension.md` and `protocol-amendments/5.2.3-manifest.json`.
'@

    Write-Utf8NoBom -Path $Readme -Content ($readmeText.TrimEnd() + $append + "`r`n")
}

Write-Host "  PASS - 5.2.3 amendment document created"
Write-Host "  PASS - 5.2.3 manifest created"
Write-Host "  PASS - README current-state note added"

# ---------------------------------------------------------------------------
# F. Verify that the original 10 run outputs and sources were not changed.
# ---------------------------------------------------------------------------

Write-Host ""
Write-Host "Checklist E: final integrity verification"

foreach ($runRoot in $existingRunRoots) {
    if ((Get-TreeSignature (Join-Path $runRoot "output")) -ne $existingOutputSignatures[$runRoot]) {
        throw "Existing experimental output changed unexpectedly: $runRoot"
    }

    if ((Get-TreeSignature (Join-Path $runRoot "source")) -ne $sourceReference) {
        throw "Existing source corpus changed unexpectedly: $runRoot"
    }
}

Write-Host "  PASS - original 10 outputs unchanged"
Write-Host "  PASS - original source inputs unchanged"
Write-Host "  PASS - M1 replicate inputs are identical"
Write-Host "  PASS - M1 outputs remain empty"

Write-Host ""
Write-Host "Protocol amendment 5.2.3 applied successfully." -ForegroundColor Green
Write-Host ""
Write-Host "Added:"
Write-Host "  M1\Run-01"
Write-Host "  M1\Run-02"
Write-Host ""
Write-Host "Experiment now contains 6 generated candidates x 2 replicates = 12 runs."
Write-Host ""
Write-Host "M1 TASK SHA256:        $canonicalTaskHash"
Write-Host "M1 CANDIDATE SHA256:   $m1CandidateHash"
Write-Host "M1 SOURCE TREE SHA256: $sourceReference"
Write-Host ""
Write-Host "Run M1/Run-01 and M1/Run-02 in fresh Claude Desktop Code sessions"
Write-Host "using the exact current root GOAL_PROMPT.txt."
