[CmdletBinding()]
param(
    [ValidateSet("Patch", "PrepareRuns")]
    [string]$Mode = "Patch",
    [string]$RepoRoot = (Get-Location).Path,
    [string]$DestinationRoot = "C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = [System.IO.Path]::GetFullPath($RepoRoot)
$DestinationRoot = [System.IO.Path]::GetFullPath($DestinationRoot)

$PromptPath = Join-Path $RepoRoot "prompts\005-template-generation.md"
$PreparePath = Join-Path $RepoRoot "research\tools\prepare-005-runs.ps1"
$ObservationPath = Join-Path $RepoRoot "research\observations\005-template-generation.md"
$InventoryPath = Join-Path $RepoRoot "research\policy\inventory.json"
$SharedInvariantsPath = Join-Path $RepoRoot "research\policy\shared-research-invariants.json"

function Write-Utf8NoBom {
    param([string]$Path, [string]$Content)
    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $encoding)
}

function Assert-File {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Required file is missing: $Path"
    }
}

function Get-NormalizedText {
    param([string]$Path)
    return ([System.IO.File]::ReadAllText($Path)).Replace("`r`n", "`n")
}

function Set-NormalizedText {
    param([string]$Path, [string]$Content)
    Write-Utf8NoBom -Path $Path -Content ($Content.Replace("`r`n", "`n"))
}

function Replace-ExactOnce {
    param([string]$Text, [string]$Old, [string]$New, [string]$Label)

    if ($Text.Contains($New)) {
        Write-Host "Already applied: $Label"
        return $Text
    }

    $first = $Text.IndexOf($Old, [System.StringComparison]::Ordinal)
    if ($first -lt 0) {
        throw "Could not find expected source block for: $Label"
    }

    $second = $Text.IndexOf($Old, $first + $Old.Length, [System.StringComparison]::Ordinal)
    if ($second -ge 0) {
        throw "Expected exactly one source block for '$Label', but found more than one."
    }

    Write-Host "Applying: $Label"
    return $Text.Substring(0, $first) + $New + $Text.Substring($first + $Old.Length)
}

function Get-RelativeSelfPath {
    $self = [System.IO.Path]::GetFullPath($PSCommandPath)
    $repo = $RepoRoot.TrimEnd("\", "/")

    if (-not $self.StartsWith($repo + "\", [System.StringComparison]::OrdinalIgnoreCase)) {
        return $null
    }

    return $self.Substring($repo.Length + 1).Replace("\", "/")
}

function Assert-RepositoryClean {
    $selfRelative = Get-RelativeSelfPath
    $dirty = @(& git -C $RepoRoot status --porcelain --untracked-files=all)

    $blocking = @(
        $dirty | Where-Object {
            if ([string]::IsNullOrWhiteSpace($_)) {
                return $false
            }

            $path = $_.Substring(3).Replace("\", "/")
            if ($path.Contains(" -> ")) {
                $path = ($path.Split(" -> ")[-1]).Trim()
            }

            if ($null -ne $selfRelative -and $path -eq $selfRelative) {
                return $false
            }

            return $true
        }
    )

    if ($blocking.Count -gt 0) {
        throw @"
The repository is not clean.

Commit, stash, or remove unrelated changes before using this script.
The script itself is ignored if it is stored inside the repository.

Blocking changes:
$($blocking -join "`n")
"@
    }
}

function Assert-PolicyInputs {
    Assert-File $InventoryPath
    Assert-File $SharedInvariantsPath

    try {
        $inventory = Get-Content -LiteralPath $InventoryPath -Raw | ConvertFrom-Json
    }
    catch {
        throw "research/policy/inventory.json is not valid JSON: $($_.Exception.Message)"
    }

    if ([string]$inventory.schema_version -ne "0.4") {
        throw "Expected inventory schema_version 0.4, got '$($inventory.schema_version)'."
    }

    if ([int]$inventory.policy_count -ne 194) {
        throw "Expected inventory policy_count 194, got '$($inventory.policy_count)'."
    }

    $actualPolicyCount = 0
    foreach ($group in $inventory.policygroups) {
        $actualPolicyCount += @($group.policies).Count
    }

    if ($actualPolicyCount -ne 194) {
        throw "Inventory declares 194 policies but stores $actualPolicyCount."
    }

    if ([string]$inventory.coverage_policy.candidate_visibility -ne "allowed") {
        throw "Inventory must allow candidate-construction visibility."
    }

    if ([string]$inventory.coverage_policy.benchmark_execution_visibility -ne "forbidden") {
        throw "Inventory must forbid benchmark-execution visibility."
    }

    try {
        $shared = Get-Content -LiteralPath $SharedInvariantsPath -Raw | ConvertFrom-Json
    }
    catch {
        throw "shared-research-invariants.json is not valid JSON: $($_.Exception.Message)"
    }

    $sharedIds = @($shared.invariants | ForEach-Object { [string]$_.id })
    if ($sharedIds.Count -ne 2 -or
        -not ($sharedIds -contains "GOV-017") -or
        -not ($sharedIds -contains "GOV-018")) {
        throw "Expected shared research invariants GOV-017 and GOV-018 only."
    }

    foreach ($invariant in $shared.invariants) {
        if ([string]$invariant.status -ne "shared_construction_constraint") {
            throw "Shared invariant $($invariant.id) has unexpected status '$($invariant.status)'."
        }
    }
}

function Assert-RestartPatchPresent {
    $prompt = Get-NormalizedText $PromptPath
    $prepare = Get-NormalizedText $PreparePath
    $observation = Get-NormalizedText $ObservationPath

    $requiredPromptMarkers = @(
        "research/policy/shared-research-invariants.json",
        "## Language requirement",
        "All programming-related and AI-instruction artifacts must be written in English.",
        "The V2 inventory is the normative oracle for V2-derived policy.",
        "verify that all generated technical/programming artifacts are English-only;"
    )

    foreach ($marker in $requiredPromptMarkers) {
        if (-not $prompt.Contains($marker)) {
            throw "Prompt validation failed. Missing marker: $marker"
        }
    }

    if (-not $prepare.Contains('"research\policy\shared-research-invariants.json"')) {
        throw "prepare-005-runs.ps1 does not copy shared-research-invariants.json."
    }

    if (-not $observation.Contains("## Restart provenance")) {
        throw "Observation does not record restart provenance."
    }

    if (-not $observation.Contains("research/policy/shared-research-invariants.json")) {
        throw "Observation allowlist does not include shared-research-invariants.json."
    }

    if ($observation.Contains("| 01 | 01-M-R1 | | Opus 5.5 | xhigh | **STARTED** |")) {
        throw "Observation still marks 01-M-R1 as STARTED."
    }

    $runRows = @(
        $observation -split "`n" |
        Where-Object { $_ -match '^\|\s*(0[1-9]|10)\s*\|' }
    )

    if ($runRows.Count -ne 10) {
        throw "Expected 10 run rows in the Iteration-005 observation; found $($runRows.Count)."
    }

    foreach ($row in $runRows) {
        if ($row -notmatch '\|\s*Pending\s*\|\s*$') {
            throw "Every restarted run must be Pending before execution. Unexpected row: $row"
        }
    }
}

function Apply-Patch {
    Assert-RepositoryClean

    Assert-File $PromptPath
    Assert-File $PreparePath
    Assert-File $ObservationPath
    Assert-PolicyInputs

    $prompt = Get-NormalizedText $PromptPath

    $oldInputs = @'
Shared inputs:

1. `research/observations/001-v3-design-proposal.md`
2. `research/observations/002-candidate-space-analysis.md`
3. `research/policy/inventory.json`
4. `research/candidates/<assigned>/CORE_FEATURES.md`
5. `research/candidates/<assigned>/DESIGN.md`
6. the complete `templates/v2-baseline/` tree
'@

    $newInputs = @'
Shared inputs:

1. `research/observations/001-v3-design-proposal.md`
2. `research/observations/002-candidate-space-analysis.md`
3. `research/policy/inventory.json`
4. `research/policy/shared-research-invariants.json`
5. `research/candidates/<assigned>/CORE_FEATURES.md`
6. `research/candidates/<assigned>/DESIGN.md`
7. the complete `templates/v2-baseline/` tree
'@

    $prompt = Replace-ExactOnce -Text $prompt -Old $oldInputs -New $newInputs -Label "add shared research invariants to required inputs"

    $oldLanguageAnchor = @'
Do **not** inspect files outside the workspace root. Do not use the network or external repositories to recover excluded material.

## Established E0 mechanics
'@

    $newLanguageAnchor = @'
Do **not** inspect files outside the workspace root. Do not use the network or external repositories to recover excluded material.

## Language requirement

All programming-related and AI-instruction artifacts must be written in English.

This includes:

- all generated Markdown;
- Claude / AI instruction files;
- code and code comments;
- configuration files;
- scripts;
- technical documentation;
- `GENERATION_REPORT.md`.

Do not generate Russian text in technical artifacts.

The only exception is explicit end-user UI text when a product specification requires a non-English UI. This template-generation task has no such requirement.

## Established E0 mechanics
'@

    $prompt = Replace-ExactOnce -Text $prompt -Old $oldLanguageAnchor -New $newLanguageAnchor -Label "add English-only technical-artifact requirement"

    $oldRule2 = @'
2. **The inventory is the normative oracle.**
   Do not independently strengthen, weaken, add, or remove policy. Organizational rewrites and technology-neutral wording are allowed only where the assigned candidate design requires them.
'@

    $newRule2 = @'
2. **The V2 inventory is the normative oracle for V2-derived policy.**
   Do not independently strengthen, weaken, add, or remove V2 policy. Organizational rewrites and technology-neutral wording are allowed only where the assigned candidate design requires them.
   `research/policy/shared-research-invariants.json` contains experiment-wide construction constraints that apply equally to every candidate. Preserve those constraints without treating them as V2-derived policy.
'@

    $prompt = Replace-ExactOnce -Text $prompt -Old $oldRule2 -New $newRule2 -Label "separate V2 policy oracle from research-shared construction constraints"

    $oldSelfCheck = @'
5. check for accidental normative duplication;
6. check that no concrete application code or benchmark material was generated;
7. correct clear construction defects you find;
8. leave unresolved design ambiguities documented in `GENERATION_REPORT.md` rather than silently inventing a new architecture.
'@

    $newSelfCheck = @'
5. check for accidental normative duplication;
6. check that no concrete application code or benchmark material was generated;
7. verify that all generated technical/programming artifacts are English-only;
8. correct clear construction defects you find;
9. leave unresolved design ambiguities documented in `GENERATION_REPORT.md` rather than silently inventing a new architecture.
'@

    $prompt = Replace-ExactOnce -Text $prompt -Old $oldSelfCheck -New $newSelfCheck -Label "add English-only final self-check"
    Set-NormalizedText -Path $PromptPath -Content $prompt

    $prepare = Get-NormalizedText $PreparePath

    $oldSharedFiles = @'
$sharedFiles = @(
    "prompts\005-template-generation.md",
    "research\observations\001-v3-design-proposal.md",
    "research\observations\002-candidate-space-analysis.md",
    "research\policy\inventory.json"
)
'@

    $newSharedFiles = @'
$sharedFiles = @(
    "prompts\005-template-generation.md",
    "research\observations\001-v3-design-proposal.md",
    "research\observations\002-candidate-space-analysis.md",
    "research\policy\inventory.json",
    "research\policy\shared-research-invariants.json"
)
'@

    $prepare = Replace-ExactOnce -Text $prepare -Old $oldSharedFiles -New $newSharedFiles -Label "copy shared research invariants into every Iteration-005 workspace"
    Set-NormalizedText -Path $PreparePath -Content $prepare

    $observation = Get-NormalizedText $ObservationPath

    $observation = Replace-ExactOnce `
        -Text $observation `
        -Old '| 01 | 01-M-R1 | | Opus 5.5 | xhigh | **STARTED** |' `
        -New '| 01 | 01-M-R1 | | Opus 5.5 | xhigh | Pending |' `
        -Label "reset 01-M-R1 to Pending"

    $purposeTail = @'
Template generation and code generation are deliberately separated. The two generations of each candidate are **replicates of the same candidate definition, not separate candidate variants**. After all ten raw generation results are audited, at most one canonical runtime template per candidate architecture is carried forward to any later code-generation experiment.

## Run order
'@

    $restartSection = @'
Template generation and code generation are deliberately separated. The two generations of each candidate are **replicates of the same candidate definition, not separate candidate variants**. After all ten raw generation results are audited, at most one canonical runtime template per candidate architecture is carried forward to any later code-generation experiment.

## Restart provenance

Two earlier Iteration-005 attempts are explicitly annulled and are **not experimental evidence** for this restarted 5×2 series:

- an earlier automated/opaque M generation was completed but annulled before comparative audit because the workflow did not meet the experiment's human-inspectability requirement;
- a later restarted M generation was stopped after technical Markdown was produced in Russian, violating the English-only technical-artifact requirement.

No output from either attempt may be used as a replicate, baseline, recovery input, candidate-quality result, or comparative evidence for the restarted series.

## Run order
'@

    $observation = Replace-ExactOnce -Text $observation -Old $purposeTail -New $restartSection -Label "record annulled Iteration-005 attempts"

    $oldAllowlist = @'
research/observations/001-v3-design-proposal.md
research/observations/002-candidate-space-analysis.md
research/policy/inventory.json

research/candidates/<assigned>/DESIGN.md
'@

    $newAllowlist = @'
research/observations/001-v3-design-proposal.md
research/observations/002-candidate-space-analysis.md
research/policy/inventory.json
research/policy/shared-research-invariants.json

research/candidates/<assigned>/DESIGN.md
'@

    $observation = Replace-ExactOnce -Text $observation -Old $oldAllowlist -New $newAllowlist -Label "document shared research invariants in the workspace allowlist"
    Set-NormalizedText -Path $ObservationPath -Content $observation

    Assert-RestartPatchPresent

    & git -C $RepoRoot diff --check
    if ($LASTEXITCODE -ne 0) {
        throw "git diff --check failed."
    }

    Write-Host ""
    Write-Host "Iteration-005 restart patch applied successfully."
    Write-Host ""
    Write-Host "Changed files:"
    Write-Host "  prompts/005-template-generation.md"
    Write-Host "  research/tools/prepare-005-runs.ps1"
    Write-Host "  research/observations/005-template-generation.md"
    Write-Host ""
    Write-Host "Review:"
    Write-Host "  git -C `"$RepoRoot`" diff -- prompts/005-template-generation.md research/tools/prepare-005-runs.ps1 research/observations/005-template-generation.md"
    Write-Host ""
    Write-Host "Commit/push the reviewed changes."
    Write-Host "Then rerun this same script with: -Mode PrepareRuns"
}

function Prepare-Runs {
    Assert-RepositoryClean
    Assert-File $PromptPath
    Assert-File $PreparePath
    Assert-File $ObservationPath
    Assert-PolicyInputs
    Assert-RestartPatchPresent

    & $PreparePath -DestinationRoot $DestinationRoot -Recreate
    if ($LASTEXITCODE -ne 0) {
        throw "prepare-005-runs.ps1 failed with exit code $LASTEXITCODE."
    }

    $runFolders = @(
        "01-M-R1",
        "02-L0-R1",
        "03-L1-R1",
        "04-K0-R1",
        "05-K1-R1",
        "06-M-R2",
        "07-L0-R2",
        "08-L1-R2",
        "09-K0-R2",
        "10-K1-R2"
    )

    $sourcePromptHash = (Get-FileHash -LiteralPath $PromptPath -Algorithm SHA256).Hash
    $sourceInventoryHash = (Get-FileHash -LiteralPath $InventoryPath -Algorithm SHA256).Hash
    $sourceSharedHash = (Get-FileHash -LiteralPath $SharedInvariantsPath -Algorithm SHA256).Hash

    foreach ($folder in $runFolders) {
        $root = Join-Path $DestinationRoot $folder
        if (-not (Test-Path -LiteralPath $root -PathType Container)) {
            throw "Expected run workspace is missing: $root"
        }

        $runPrompt = Join-Path $root "prompts\005-template-generation.md"
        $runInventory = Join-Path $root "research\policy\inventory.json"
        $runShared = Join-Path $root "research\policy\shared-research-invariants.json"
        $runOutput = Join-Path $root "output"

        foreach ($required in @($runPrompt, $runInventory, $runShared, $runOutput)) {
            if (-not (Test-Path -LiteralPath $required)) {
                throw "Prepared workspace is missing required input: $required"
            }
        }

        if ((Get-FileHash -LiteralPath $runPrompt -Algorithm SHA256).Hash -ne $sourcePromptHash) {
            throw "Prompt copy hash mismatch in $folder."
        }
        if ((Get-FileHash -LiteralPath $runInventory -Algorithm SHA256).Hash -ne $sourceInventoryHash) {
            throw "Inventory copy hash mismatch in $folder."
        }
        if ((Get-FileHash -LiteralPath $runShared -Algorithm SHA256).Hash -ne $sourceSharedHash) {
            throw "Shared-invariants copy hash mismatch in $folder."
        }

        if (@(Get-ChildItem -LiteralPath $runOutput -Force).Count -ne 0) {
            throw "Output directory is not empty in $folder."
        }

        foreach ($forbidden in @("research\metrics", "research\benchmark", "research\e0", ".git")) {
            if (Test-Path -LiteralPath (Join-Path $root $forbidden)) {
                throw "Forbidden path exists in '$folder': $forbidden"
            }
        }
    }

    $head = (& git -C $RepoRoot rev-parse HEAD).Trim()

    Write-Host ""
    Write-Host "Iteration-005 run workspaces are ready."
    Write-Host "Source commit: $head"
    Write-Host "Destination:   $DestinationRoot"
    Write-Host ""
    Write-Host "Start with:"
    Write-Host "  $DestinationRoot\01-M-R1"
    Write-Host ""
    Write-Host "Use a fresh Claude Desktop Code session, Claude Opus 5.5 / xhigh,"
    Write-Host "and execute prompts\005-template-generation.md."
}

if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot ".git") -PathType Container)) {
    throw "RepoRoot does not look like the ClaudeArchitectureResearch repository: $RepoRoot"
}

switch ($Mode) {
    "Patch" { Apply-Patch }
    "PrepareRuns" { Prepare-Runs }
}
