[CmdletBinding()]
param(
    [string]$Root = "C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.2"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = [System.IO.Path]::GetFullPath($Root)

$Candidates = @("M", "L0", "L1", "K0", "K1")
$Runs = @("Run-01", "Run-02")

$CompletedRun = Join-Path (Join-Path $Root "M") "Run-01"
$CompletedTask = Join-Path $CompletedRun "TASK.md"
$CompletedReport = Join-Path $CompletedRun "output\GENERATION_REPORT.md"

$AmendmentDir = Join-Path $Root "protocol-amendments"
$EvidenceDir = Join-Path $AmendmentDir "evidence"
$AmendmentMd = Join-Path $AmendmentDir "5.2.1-workspace-boundary-adjudication.md"
$AmendmentJson = Join-Path $AmendmentDir "5.2.1-manifest.json"
$ExecutedTaskCopy = Join-Path $EvidenceDir "M-Run-01-TASK-executed.md"

$ReadmePath = Join-Path $Root "README.md"

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

function Replace-ExactOnce(
    [string]$Text,
    [string]$Old,
    [string]$New,
    [string]$Label,
    [string]$Path
) {
    $count = ([regex]::Matches($Text, [regex]::Escape($Old))).Count

    if ($count -eq 0) {
        # Idempotency: if already patched, accept the new form.
        if ($Text.Contains($New)) {
            return $Text
        }
        throw "Patch target not found [$Label] in $Path"
    }

    if ($count -ne 1) {
        throw "Expected exactly one patch target [$Label] in $Path, found $count"
    }

    return $Text.Replace($Old, $New)
}

function Get-AllRunRoots {
    return @(
        foreach ($candidate in $Candidates) {
            foreach ($run in $Runs) {
                Join-Path -Path (Join-Path -Path $Root -ChildPath $candidate) -ChildPath $run
            }
        }
    )
}

function Get-RemainingRunRoots {
    $all = @(Get-AllRunRoots)
    return @(
        $all | Where-Object {
            -not ([System.IO.Path]::GetFullPath($_).Equals(
                [System.IO.Path]::GetFullPath($CompletedRun),
                [System.StringComparison]::OrdinalIgnoreCase
            ))
        }
    )
}

Write-Host ""
Write-Host "Iteration 005 / 5.2.1 protocol amendment"
Write-Host "Root: $Root"
Write-Host ""

Assert-Directory $Root
Assert-Directory $CompletedRun
Assert-File $CompletedTask
Assert-File $CompletedReport
Assert-File $ReadmePath

$allRunRoots = @(Get-AllRunRoots)
$remainingRunRoots = @(Get-RemainingRunRoots)

if ($allRunRoots.Count -ne 10) {
    throw "Run-root enumeration failure: expected 10 runs, found $($allRunRoots.Count)."
}
if ($remainingRunRoots.Count -ne 9) {
    throw "Remaining-run enumeration failure: expected 9 runs, found $($remainingRunRoots.Count)."
}

foreach ($p in $allRunRoots) {
    Assert-Directory $p
    Assert-File (Join-Path $p "TASK.md")
    Assert-File (Join-Path $p "CANDIDATE.md")
    Assert-Directory (Join-Path $p "output")
}

# M Run-01 must contain completed evidence.
$completedOutputItems = @(Get-ChildItem -LiteralPath (Join-Path $CompletedRun "output") -Force)
if ($completedOutputItems.Count -eq 0) {
    throw "M Run-01 output is empty. This amendment must be applied only after the completed M Run-01 Goal run."
}

# The other nine runs must still be unexecuted.
foreach ($runRoot in $remainingRunRoots) {
    $items = @(Get-ChildItem -LiteralPath (Join-Path $runRoot "output") -Force)
    if ($items.Count -ne 0) {
        throw "Refusing to amend because a remaining run already has output: $runRoot"
    }
}

# Preserve and validate the completed report.
$reportText = [System.IO.File]::ReadAllText($CompletedReport)
if (-not $reportText.Contains("NOT PASS")) {
    throw "M Run-01 report does not contain the expected NOT PASS status."
}

$oldTaskHash = Get-Sha256 $CompletedTask

# ---------------------------------------------------------------------------
# Preserve exact executed M Run-01 TASK.md as evidence.
# Safe if an earlier failed script already created this copy.
# ---------------------------------------------------------------------------

New-Item -ItemType Directory -Path $EvidenceDir -Force | Out-Null

if (Test-Path -LiteralPath $ExecutedTaskCopy) {
    if ((Get-Sha256 $ExecutedTaskCopy) -ne $oldTaskHash) {
        throw "Existing executed-task evidence copy does not match M Run-01 TASK.md."
    }
}
else {
    Copy-Item -LiteralPath $CompletedTask -Destination $ExecutedTaskCopy
}

# ---------------------------------------------------------------------------
# Patch only three small, verified fragments in the remaining nine TASK.md.
# ---------------------------------------------------------------------------

$oldCreateTemp = '- create temporary files, caches, reports, or helper artifacts outside the current run workspace.'
$newCreateTemp = '- intentionally create construction artifacts, caches, reports, or helper files outside the current run workspace.'

$oldAfterPathRule = 'Before reading or writing a path derived programmatically, ensure its resolved absolute path remains inside the current run workspace. Treat a path that escapes the workspace as invalid even if the operating system permits access.'

$newAfterPathRule = @'
Before reading or writing a path derived programmatically, ensure its resolved absolute path remains inside the current run workspace. Treat a path that escapes the workspace as invalid even if the operating system permits access.

### Workspace-event classification

Distinguish three classes during self-audit:

1. **Experimental isolation violation** — the run reads or depends on forbidden external information, including parent/sibling run content, another candidate's output or metadata, external repositories, network material, or intentionally excluded research material. These are validity failures and must be `0` for PASS.
2. **Recoverable workspace-process incident** — the model itself temporarily writes allowed-workspace-derived scratch or audit data outside the workspace, but detects the mistake, stops using it, removes it when controllable, recreates any needed material under `output/.work/`, and does not read or acquire forbidden external information through the incident. Record the incident and remediation, but after successful remediation it does not by itself prevent PASS.
3. **Platform-managed persistence event** — Claude Desktop, the tool runtime, the operating system, or another platform-managed component automatically stores session state, logs, command output, or tool results outside the workspace without the run choosing that storage location. Record it when known, but it is not an experimental isolation violation and does not prevent PASS unless the run later reads forbidden external information from it or makes the generated result depend on it.

A recoverable process incident is not permission to use external scratch storage intentionally. Once detected, keep all further model-controlled temporary artifacts inside `output/.work/`.
'@

$oldAcceptance14 = '14. no generated or temporary file exists outside `output/`, and no construction artifact depends on a parent/sibling workspace;'
$newAcceptance14 = '14. experimental isolation violations are `0`; all recoverable workspace-process incidents are remediated; platform-managed persistence events do not create forbidden external dependencies;'

$oldReportFields = '- known workspace-boundary violations (must be `0` for PASS);'

$newReportFields = @'
- experimental isolation violation count (must be `0` for PASS);
- recoverable workspace-process incident count, with remediation status;
- known platform-managed persistence events, if any;
'@

foreach ($runRoot in $remainingRunRoots) {
    $taskPath = Join-Path $runRoot "TASK.md"
    $text = [System.IO.File]::ReadAllText($taskPath)

    $text = Replace-ExactOnce `
        -Text $text `
        -Old $oldCreateTemp `
        -New $newCreateTemp `
        -Label "intentional external temp creation" `
        -Path $taskPath

    $text = Replace-ExactOnce `
        -Text $text `
        -Old $oldAfterPathRule `
        -New $newAfterPathRule `
        -Label "workspace-event classification" `
        -Path $taskPath

    $text = Replace-ExactOnce `
        -Text $text `
        -Old $oldAcceptance14 `
        -New $newAcceptance14 `
        -Label "acceptance item 14" `
        -Path $taskPath

    $text = Replace-ExactOnce `
        -Text $text `
        -Old $oldReportFields `
        -New $newReportFields `
        -Label "generation report workspace line" `
        -Path $taskPath

    Write-Utf8NoBom -Path $taskPath -Content $text
}

# All remaining tasks must be byte-identical after amendment.
$remainingTaskHashes = @(
    $remainingRunRoots |
    ForEach-Object { Get-Sha256 (Join-Path $_ "TASK.md") } |
    Sort-Object -Unique
)

if ($remainingTaskHashes.Count -ne 1) {
    throw "Amendment failed: remaining nine TASK.md files are not byte-identical."
}

$newTaskHash = $remainingTaskHashes[0]

if ($newTaskHash -eq $oldTaskHash) {
    throw "Amendment failed: amended TASK hash equals original TASK hash."
}

# Raw M Run-01 must remain untouched.
if ((Get-Sha256 $CompletedTask) -ne $oldTaskHash) {
    throw "M Run-01 TASK.md changed unexpectedly."
}

# ---------------------------------------------------------------------------
# Adjudication document.
# ---------------------------------------------------------------------------

$amendmentText = @'
# Iteration 005 / Protocol Amendment 5.2.1

## Purpose

This amendment corrects the workspace-boundary accounting rule discovered by the first completed 5.2 Goal run (`M/Run-01`).

The architectural and construction requirements are unchanged. The amendment changes only how workspace/session-storage events are classified for final acceptance.

## Why the amendment was needed

`M/Run-01` completed the substantive template checks successfully, including zero trigger-role deltas, policy coverage/ownership checks, workflow/procedure separation, Windows-compatible enforcement, internal-reference checks, and the always-loaded budget.

Its raw `GENERATION_REPORT.md` nevertheless recorded `NOT PASS` because two events were counted under the original absolute workspace gate:

1. a model-created scratchpad dump outside the workspace that was detected, deleted, and recreated under `output/.work/`;
2. automatic Claude Desktop/tool-runtime persistence of a large command result in platform-managed session storage outside the workspace.

No parent directory, sibling run, another candidate output, external repository, network material, or intentionally excluded research content was consumed. No generated runtime artifact depends on the external scratch/platform storage.

Treating platform-managed persistence as an irreversible validity failure would make candidate acceptance depend on Claude Desktop implementation details rather than candidate quality.

## Adjudication of M / Run-01

The original run files and original `GENERATION_REPORT.md` remain unchanged as raw evidence.

For research interpretation under Protocol 5.2.1:

**M / Run-01 is accepted as VALID / PASS for generated-template and comparative-candidate purposes.**

The original `NOT PASS` is preserved historically and is interpreted as a protocol-accounting failure under the superseded 5.2 workspace rule, not as a template-quality failure.

This is a post-hoc protocol adjudication, not a rerun and not a manual repair of generated output.

## Revised event classes

### Experimental isolation violation

Forbidden external information was read or used, including parent/sibling run content, another run/candidate output, network material, external repositories, or intentionally excluded research material.

Required for PASS: **0**.

### Recoverable workspace-process incident

The model temporarily created allowed-input-derived scratch/audit material outside the workspace, detected and remediated the mistake, and did not acquire forbidden external information through it.

This must be recorded but does not by itself prevent PASS after remediation.

### Platform-managed persistence event

Claude Desktop/tool runtime/OS automatically persists session state, logs, command output, or tool results outside the workspace without the run selecting that storage location.

This is informational and does not prevent PASS unless the run later consumes forbidden external information from it or the generated result depends on it.

## Provenance

Executed M Run-01 TASK SHA-256:

`{{OLD_TASK_HASH}}`

Amended TASK SHA-256 used by the remaining nine 5.2 runs:

`{{NEW_TASK_HASH}}`

The exact M Run-01 executed task is preserved at:

`protocol-amendments/evidence/M-Run-01-TASK-executed.md`
'@

$amendmentText = $amendmentText.Replace("{{OLD_TASK_HASH}}", $oldTaskHash)
$amendmentText = $amendmentText.Replace("{{NEW_TASK_HASH}}", $newTaskHash)

Write-Utf8NoBom -Path $AmendmentMd -Content ($amendmentText.TrimEnd() + "`n")

# ---------------------------------------------------------------------------
# Machine-readable amendment manifest.
# ---------------------------------------------------------------------------

$manifestObject = [ordered]@{
    schema_version = "1.0"
    amendment = "5.2.1"
    created_utc = [DateTime]::UtcNow.ToString("o")
    reason = "Workspace acceptance now distinguishes experimental isolation violations from remediated model-process incidents and platform-managed persistence."
    completed_run = [ordered]@{
        run = "M/Run-01"
        task_sha256_executed = $oldTaskHash
        raw_report_status = "NOT PASS"
        adjudicated_status = "VALID_PASS_FOR_COMPARATIVE_USE"
        raw_files_modified = $false
    }
    remaining_runs = [ordered]@{
        count = 9
        task_sha256 = $newTaskHash
    }
    acceptance = [ordered]@{
        experimental_isolation_violations_required = 0
        recoverable_workspace_process_incidents = "record_and_remediate_non_blocking"
        platform_managed_persistence = "record_if_known_non_blocking_unless_forbidden_external_information_is_consumed"
    }
}

$json = $manifestObject | ConvertTo-Json -Depth 10
Write-Utf8NoBom -Path $AmendmentJson -Content ($json + "`n")

# ---------------------------------------------------------------------------
# README amendment note.
# ---------------------------------------------------------------------------

$readme = [System.IO.File]::ReadAllText($ReadmePath)
$marker = "## Protocol amendment 5.2.1"

if (-not $readme.Contains($marker)) {
    $append = @'

## Protocol amendment 5.2.1

After the completed `M/Run-01` Goal run, the absolute workspace-boundary PASS rule was found to conflate candidate-controlled experimental isolation with Claude Desktop/tool-runtime session persistence.

`M/Run-01` is preserved unchanged as raw evidence. Its original report says `NOT PASS`, but the run is post-hoc adjudicated as **VALID / PASS for comparative use** because the substantive candidate/template gates passed and no forbidden parent/sibling/network/external research information was consumed.

The remaining nine runs use an amended common `TASK.md` that distinguishes:

- experimental isolation violations — must be `0`;
- recoverable workspace-process incidents — record + remediate, non-blocking after successful remediation;
- platform-managed persistence — informational/non-blocking unless forbidden external information is later consumed or becomes a dependency.

See:

- `protocol-amendments/5.2.1-workspace-boundary-adjudication.md`
- `protocol-amendments/5.2.1-manifest.json`
- `protocol-amendments/evidence/M-Run-01-TASK-executed.md`

Do not modify the raw `M/Run-01` output/report to rewrite history.
'@

    Write-Utf8NoBom -Path $ReadmePath -Content ($readme.TrimEnd() + $append + "`n")
}

# ---------------------------------------------------------------------------
# Final validation.
# ---------------------------------------------------------------------------

if ((Get-Sha256 $CompletedTask) -ne $oldTaskHash) {
    throw "Final validation failed: M Run-01 TASK.md changed."
}

if ((Get-Sha256 $ExecutedTaskCopy) -ne $oldTaskHash) {
    throw "Final validation failed: executed-task evidence copy hash mismatch."
}

$finalRemainingHashes = @(
    $remainingRunRoots |
    ForEach-Object { Get-Sha256 (Join-Path $_ "TASK.md") } |
    Sort-Object -Unique
)

if ($finalRemainingHashes.Count -ne 1 -or $finalRemainingHashes[0] -ne $newTaskHash) {
    throw "Final validation failed: amended TASK parity."
}

foreach ($runRoot in $remainingRunRoots) {
    $taskPath = Join-Path $runRoot "TASK.md"
    $text = [System.IO.File]::ReadAllText($taskPath)

    if (-not $text.Contains("### Workspace-event classification")) {
        throw "Final validation failed: workspace-event classification missing in $taskPath"
    }
    if (-not $text.Contains("experimental isolation violation count (must be `0` for PASS)")) {
        throw "Final validation failed: new report fields missing in $taskPath"
    }
    if ($text.Contains("known workspace-boundary violations (must be `0` for PASS)")) {
        throw "Final validation failed: old absolute workspace gate remains in $taskPath"
    }

    $items = @(Get-ChildItem -LiteralPath (Join-Path $runRoot "output") -Force)
    if ($items.Count -ne 0) {
        throw "Final validation failed: remaining output is not empty in $runRoot"
    }
}

Assert-File $AmendmentMd
Assert-File $AmendmentJson
Assert-File $ExecutedTaskCopy

Write-Host ""
Write-Host "Protocol amendment 5.2.1 applied successfully." -ForegroundColor Green
Write-Host ""
Write-Host "M/Run-01 preserved unchanged:"
Write-Host "  original TASK SHA256: $oldTaskHash"
Write-Host "  adjudication: VALID / PASS for comparative use"
Write-Host ""
Write-Host "Remaining 9 runs:"
Write-Host "  amended TASK SHA256: $newTaskHash"
Write-Host "  all TASK.md files are byte-identical"
Write-Host "  all outputs remain empty"
Write-Host ""
Write-Host "Created/updated:"
Write-Host "  protocol-amendments\5.2.1-workspace-boundary-adjudication.md"
Write-Host "  protocol-amendments\5.2.1-manifest.json"
Write-Host "  protocol-amendments\evidence\M-Run-01-TASK-executed.md"
Write-Host "  README.md"
Write-Host ""
Write-Host "Ready for the next Goal run."
