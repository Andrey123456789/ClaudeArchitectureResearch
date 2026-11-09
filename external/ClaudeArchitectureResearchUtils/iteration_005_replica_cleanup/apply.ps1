$ErrorActionPreference = "Stop"

$ExpectedHead = "9b781dd711f5f63ce701cc4ae154a1c180b4f2a6"

function Normalize-Lf([string]$s) {
    return $s.Replace("`r`n", "`n").Replace("`r", "`n")
}

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Read-Lf([string]$RelativePath) {
    $full = Join-Path $Repo $RelativePath
    if (-not (Test-Path -LiteralPath $full)) { throw "Missing expected file: $RelativePath" }
    return Normalize-Lf([System.IO.File]::ReadAllText($full))
}

function Write-Lf([string]$RelativePath, [string]$Text) {
    $full = Join-Path $Repo $RelativePath
    [System.IO.File]::WriteAllText($full, (Normalize-Lf $Text), $Utf8NoBom)
}

function Replace-Exact([string]$RelativePath, [string]$Old, [string]$New) {
    $text = Read-Lf $RelativePath
    $oldLf = Normalize-Lf $Old
    $newLf = Normalize-Lf $New
    if (-not $text.Contains($oldLf)) {
        throw "Expected text not found in $RelativePath. Repository may not match the intended base."
    }
    Write-Lf $RelativePath ($text.Replace($oldLf, $newLf))
}

$Repo = (git rev-parse --show-toplevel).Trim()
if (-not $Repo) { throw "Run this script inside the ClaudeArchitectureResearch Git repository." }
Set-Location $Repo

$Head = (git rev-parse HEAD).Trim()
if ($Head -ne $ExpectedHead) {
    throw "Unexpected HEAD: $Head`nExpected: $ExpectedHead"
}

$Dirty = git status --porcelain
if ($Dirty) {
    throw "Working tree is not clean. Commit/stash local changes first."
}

Replace-Exact "research/observations/005-template-generation.md" @'
| Repetitions | 2 independent generations per candidate (5×2 = 10 runs) |
'@ @'
| Replicates | 2 independent generation replicates per candidate (5×2 = 10 runs) |
'@

Replace-Exact "research/observations/005-template-generation.md" @'
Template generation and code generation are deliberately separated. After all ten templates are generated, they are audited before any decision about the next experiment.
'@ @'
Template generation and code generation are deliberately separated. The two generations of each candidate are **replicates of the same candidate definition, not separate candidate variants**. After all ten raw generation results are audited, at most one canonical runtime template per candidate architecture is carried forward to any later code-generation experiment.
'@

Replace-Exact "research/observations/005-template-generation.md" @'
| Run | Candidate instance | Desktop version after run | Model | Effort | Status / notes |
|---:|---|---|---|---|---|
| 01 | M-1 | | Opus 5.5 | xhigh | |
| 02 | L0-1 | | Opus 5.5 | xhigh | |
| 03 | L1-1 | | Opus 5.5 | xhigh | |
| 04 | K0-1 | | Opus 5.5 | xhigh | |
| 05 | K1-1 | | Opus 5.5 | xhigh | |
| 06 | M-2 | | Opus 5.5 | xhigh | |
| 07 | L0-2 | | Opus 5.5 | xhigh | |
| 08 | L1-2 | | Opus 5.5 | xhigh | |
| 09 | K0-2 | | Opus 5.5 | xhigh | |
| 10 | K1-2 | | Opus 5.5 | xhigh | |
'@ @'
| Run | Generation replicate | Desktop version after run | Model | Effort | Status / notes |
|---:|---|---|---|---|---|
| 01 | M-r1 | | Opus 5.5 | xhigh | |
| 02 | L0-r1 | | Opus 5.5 | xhigh | |
| 03 | L1-r1 | | Opus 5.5 | xhigh | |
| 04 | K0-r1 | | Opus 5.5 | xhigh | |
| 05 | K1-r1 | | Opus 5.5 | xhigh | |
| 06 | M-r2 | | Opus 5.5 | xhigh | |
| 07 | L0-r2 | | Opus 5.5 | xhigh | |
| 08 | L1-r2 | | Opus 5.5 | xhigh | |
| 09 | K0-r2 | | Opus 5.5 | xhigh | |
| 10 | K1-r2 | | Opus 5.5 | xhigh | |
'@

Replace-Exact "research/observations/005-template-generation.md" @'
Do not eliminate a candidate between its first and second generation merely because the first output looks weak. Iteration 005 is the planned 5×2 generation set. A run may be stopped only for a genuine technical/input failure, which must be recorded.
'@ @'
Do not eliminate a candidate between its first and second replicate merely because the first output looks weak. Iteration 005 is the planned 5×2 generation set. Replicate 1 and replicate 2 use the same candidate specification; neither is a preferred variant. A run may be stopped only for a genuine technical/input failure, which must be recorded.
'@

Replace-Exact "research/observations/005-template-generation.md" @'
research/generation/005/runs/
  M-1/
    template/
    GENERATION_REPORT.md
  L0-1/
  L1-1/
  K0-1/
  K1-1/
  M-2/
  L0-2/
  L1-2/
  K0-2/
  K1-2/
'@ @'
research/generation/005/runs/
  M-r1/
    template/
    GENERATION_REPORT.md
  L0-r1/
  L1-r1/
  K0-r1/
  K1-r1/
  M-r2/
  L0-r2/
  L1-r2/
  K0-r2/
  K1-r2/
'@

Replace-Exact "research/observations/005-template-generation.md" @'
5. within-candidate consistency between run 1 and run 2;
6. meaningful convergence or divergence between candidate architectures.

The next experiment is chosen **after** this audit. It is intentionally not fixed in advance.
'@ @'
5. within-candidate consistency between replicate 1 and replicate 2;
6. meaningful convergence or divergence between candidate architectures.

The replicate outputs remain research evidence. After the audit, at most one canonical runtime template per candidate architecture is selected or derived for any later code-generation stage; the experiment does not carry ten competing runtime candidates forward.

The next experiment is chosen **after** this audit. It is intentionally not fixed in advance.
'@

Replace-Exact "research/e0/README.md" @'
## Required probes
'@ @'
## Original required probes
'@

Replace-Exact "research/observations/004-e0-mechanics-validation.md" @'
## 8. Decisions needed before candidate generation
'@ @'
## 8. Decisions originally required before candidate generation
'@

Write-Host ""
Write-Host "Replica terminology cleanup applied."
Write-Host "Review with:"
Write-Host "  git diff --check"
Write-Host "  git diff"
Write-Host ""
Write-Host "No commit was created."
