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
    throw "Remaining-run enumeration failure: expected 9 runs after excluding M/Run-01, found $($remainingRunRoots.Count)."
}

foreach ($p in $allRunRoots) {
    if (-not (Test-Path -LiteralPath $p -PathType Container)) {
        throw "Enumerated run root does not exist: $p"
    }
}

if ($remainingRunRoots -contains $CompletedRun) {
    throw "Remaining-run enumeration failure: completed M/Run-01 was not excluded."
}

# ---------------------------------------------------------------------------
# 1. Preflight
# ---------------------------------------------------------------------------

foreach ($runRoot in $allRunRoots) {
    Assert-File (Join-Path $runRoot "TASK.md")
    Assert-File (Join-Path $runRoot "CANDIDATE.md")
    Assert-Directory (Join-Path $runRoot "output")
}

# M Run-01 must already contain evidence.
$completedOutputItems = @(Get-ChildItem -LiteralPath (Join-Path $CompletedRun "output") -Force)
if ($completedOutputItems.Count -eq 0) {
    throw "M Run-01 output is empty. This amendment is intended only after the completed M Run-01 Goal run."
}

# All remaining outputs must still be empty.
foreach ($runRoot in $remainingRunRoots) {
    $items = @(Get-ChildItem -LiteralPath (Join-Path $runRoot "output") -Force)
    if ($items.Count -ne 0) {
        throw "Refusing to amend because a remaining run already has output: $runRoot"
    }
}

# Confirm the completed report has the expected protocol-only NOT PASS.
$reportText = [System.IO.File]::ReadAllText($CompletedReport)
if (-not $reportText.Contains("NOT PASS")) {
    throw "M Run-01 report does not contain the expected NOT PASS status."
}
if (-not $reportText.Contains("workspace-boundary violations")) {
    throw "M Run-01 report does not contain the expected workspace-boundary reason."
}
if (-not $reportText.Contains("Zero trigger-role deltas") -and
    -not $reportText.Contains("trigger-role delta")) {
    throw "M Run-01 report does not appear to contain the expected trigger-role audit."
}

$oldTaskHash = Get-Sha256 $CompletedTask

# ---------------------------------------------------------------------------
# 2. Preserve exact executed M Run-01 task as protocol evidence.
#    Do NOT modify M/Run-01/TASK.md or its report/output.
# ---------------------------------------------------------------------------

New-Item -ItemType Directory -Path $EvidenceDir -Force | Out-Null

Copy-Item -LiteralPath $CompletedTask -Destination $ExecutedTaskCopy -Force

if ((Get-Sha256 $ExecutedTaskCopy) -ne $oldTaskHash) {
    throw "Failed to preserve an exact copy of the executed M Run-01 TASK.md."
}

# ---------------------------------------------------------------------------
# 3. Patch TASK.md only for the remaining 9 runs.
# ---------------------------------------------------------------------------

$oldWorkspaceBlock = @'
Do not:

- read files above the workspace root;
- enumerate or inspect the parent directory;
- enumerate, inspect, infer from, or open sibling candidate/run directories;
- use another run's output or metadata;
- use the network;
- use external repositories;
- attempt to reconstruct intentionally excluded benchmark, metrics, ranking, or other research material;
- create temporary files, caches, reports, or helper artifacts outside the current run workspace.

Write generated deliverables only under `output/`.

If you need temporary construction/audit material, keep it under `output/.work/` and remove `output/.work/` before final completion.

Before reading or writing a path derived programmatically, ensure its resolved absolute path remains inside the current run workspace. Treat a path that escapes the workspace as invalid even if the operating system permits access.
'@

$newWorkspaceBlock = @'
Do not:

- read files above the workspace root;
- enumerate or inspect the parent directory;
- enumerate, inspect, infer from, or open sibling candidate/run directories;
- use another run's output or metadata;
- use the network;
- use external repositories;
- attempt to reconstruct intentionally excluded benchmark, metrics, ranking, or other research material;
- intentionally create construction artifacts, caches, reports, or helper files outside the current run workspace.

Write generated deliverables only under `output/`.

If you need temporary construction/audit material, keep it under `output/.work/` and remove `output/.work/` before final completion.

Before reading or writing a path derived programmatically, ensure its resolved absolute path remains inside the current run workspace. Treat a path that escapes the workspace as invalid even if the operating system permits access.

### Workspace-event classification

Distinguish three classes during self-audit:

1. **Experimental isolation violation** — the run reads or depends on forbidden external information, including parent/sibling run content, another candidate's output/metadata, external repositories, network material, or intentionally excluded research material. These are validity failures and must be `0` for PASS.
2. **Recoverable workspace-process incident** — the model itself temporarily writes allowed-workspace-derived scratch/audit data outside the workspace, but detects the mistake, stops using it, removes it when controllable, recreates any needed material under `output/.work/`, and does not read or acquire forbidden external information through the incident. Record the incident, but after successful remediation it does not by itself prevent PASS.
3. **Platform-managed persistence event** — Claude Desktop, the tool runtime, operating system, or another platform-managed component automatically stores session state, logs, command output, or tool results outside the workspace without the run choosing that storage location. Record it when known, but it is not an experimental isolation violation and does not prevent PASS unless the run later reads forbidden external information from it or makes the generated template depend on it.

A recoverable process incident is not permission to use external scratch storage intentionally. Once detected, keep all further model-controlled temporary artifacts inside `output/.work/`.
'@

$oldAcceptance14 = '14. no generated or temporary file exists outside `output/`, and no construction artifact depends on a parent/sibling workspace;'
$newAcceptance14 = '14. experimental isolation violations are `0`; all recoverable workspace-process incidents are remediated; platform-managed persistence events do not create forbidden external dependencies;'

$oldReportFields = @'
- final acceptance result: `PASS` or `BLOCKED`;
- trigger-role delta count (must be `0` for PASS);
- unresolved broken-reference count (must be `0` for PASS);
- known workspace-boundary violations (must be `0` for PASS);
- known Windows-hook compatibility defects (must be `0` for PASS).
'@

$newReportFields = @'
- final acceptance result: `PASS` or `BLOCKED`;
- trigger-role delta count (must be `0` for PASS);
- unresolved broken-reference count (must be `0` for PASS);
- experimental isolation violation count (must be `0` for PASS);
- recoverable workspace-process incident count, with remediation status;
- known platform-managed persistence events, if any;
- known Windows-hook compatibility defects (must be `0` for PASS).
'@

foreach ($runRoot in $remainingRunRoots) {
    $taskPath = Join-Path $runRoot "TASK.md"
    $text = [System.IO.File]::ReadAllText($taskPath)

    if (-not $text.Contains($oldWorkspaceBlock)) {
        throw "Expected original workspace block not found in $taskPath"
    }
    if (-not $text.Contains($oldAcceptance14)) {
        throw "Expected acceptance item 14 not found in $taskPath"
    }
    if (-not $text.Contains($oldReportFields)) {
        throw "Expected report field block not found in $taskPath"
    }

    $text = $text.Replace($oldWorkspaceBlock, $newWorkspaceBlock)
    $text = $text.Replace($oldAcceptance14, $newAcceptance14)
    $text = $text.Replace($oldReportFields, $newReportFields)

    Write-Utf8NoBom -Path $taskPath -Content $text
}

# All remaining nine tasks must now be identical.
$remainingTaskHashes = @(
    $remainingRunRoots |
    ForEach-Object { Get-Sha256 (Join-Path $_ "TASK.md") } |
    Sort-Object -Unique
)

if ($remainingTaskHashes.Count -ne 1) {
    throw "Protocol amendment failed: the remaining nine TASK.md files are not identical."
}

$newTaskHash = $remainingTaskHashes[0]

if ($newTaskHash -eq $oldTaskHash) {
    throw "Protocol amendment failed: amended TASK hash is unchanged."
}

# Completed M Run-01 must still have the exact executed task.
if ((Get-Sha256 $CompletedTask) -ne $oldTaskHash) {
    throw "M Run-01 TASK.md changed unexpectedly. Raw evidence must remain untouched."
}

# ---------------------------------------------------------------------------
# 4. Create explicit adjudication note for M Run-01.
# ---------------------------------------------------------------------------

$amendmentText = @'
# Iteration 005 / Protocol Amendment 5.2.1

## Purpose

This amendment corrects the workspace-boundary accounting rule discovered by the first completed 5.2 Goal run (`M/Run-01`).

The architectural/construction requirements are unchanged. The amendment changes only how workspace/session-storage events are classified for final acceptance.

## Why the amendment was needed

`M/Run-01` completed all substantive template checks successfully, including:

- zero trigger-role deltas;
- preserved policy ownership/coverage;
- workflow/procedure separation;
- Windows-compatible hook/enforcement behavior;
- zero unresolved internal-reference defects;
- compact always-loaded surface.

Its raw `GENERATION_REPORT.md` nevertheless recorded `NOT PASS` solely because two events were counted under the original absolute workspace gate:

1. a model-created scratchpad dump outside the workspace that was detected, deleted, and recreated under `output/.work/`;
2. automatic Claude Desktop/tool-runtime persistence of a large command result in platform-managed session storage outside the workspace.

No parent directory, sibling run, another candidate output, external repository, network material, or intentionally excluded research content was used. No generated runtime artifact depends on the external scratch/platform storage.

The second event is not controlled by the candidate/template generation logic. Treating such platform-managed persistence as an irreversible validity failure would make the Goal acceptance criterion depend on Claude Desktop implementation details rather than candidate quality.

## Adjudication of M / Run-01

The original run files and original `GENERATION_REPORT.md` remain unchanged as raw evidence.

For research interpretation under Protocol 5.2.1:

**M / Run-01 is accepted as VALID / PASS for generated-template and comparative-candidate purposes.**

The original `NOT PASS` status is preserved historically and is interpreted as a **protocol-accounting failure under the superseded 5.2 workspace rule**, not as a template-quality failure.

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

Write-Utf8NoBom -Path $AmendmentMd -Content ($amendmentText + "`n")

# ---------------------------------------------------------------------------
# 5. Create machine-readable amendment manifest.
# ---------------------------------------------------------------------------

$manifestObject = [ordered]@{
    schema_version = "1.0"
    amendment = "5.2.1"
    created_utc = [DateTime]::UtcNow.ToString("o")
    reason = "Workspace-boundary acceptance accounting distinguished experimental isolation violations from remediated process incidents and platform-managed persistence."
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
# 6. Update README with protocol provenance, without replacing prior history.
# ---------------------------------------------------------------------------

$readme = [System.IO.File]::ReadAllText($ReadmePath)

$marker = "## Protocol amendment 5.2.1"

if (-not $readme.Contains($marker)) {
    $append = @'

## Protocol amendment 5.2.1

After the completed `M/Run-01` Goal run, the absolute workspace-boundary PASS rule was found to conflate candidate-controlled experimental isolation with Claude Desktop/tool-runtime session persistence.

`M/Run-01` is preserved unchanged as raw evidence. Its original report says `NOT PASS`, but the run is post-hoc adjudicated as **VALID / PASS for comparative use** because all substantive candidate/template gates passed and no forbidden parent/sibling/network/external research information was consumed.

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
# 7. Final validation
# ---------------------------------------------------------------------------

# M Run-01 raw task still unchanged.
if ((Get-Sha256 $CompletedTask) -ne $oldTaskHash) {
    throw "Final validation failed: completed M Run-01 TASK.md was modified."
}

# Exact task evidence copy.
if ((Get-Sha256 $ExecutedTaskCopy) -ne $oldTaskHash) {
    throw "Final validation failed: executed-task evidence hash mismatch."
}

# Remaining tasks all identical and amended.
$finalRemainingHashes = @(
    $remainingRunRoots |
    ForEach-Object { Get-Sha256 (Join-Path $_ "TASK.md") } |
    Sort-Object -Unique
)

if ($finalRemainingHashes.Count -ne 1 -or $finalRemainingHashes[0] -ne $newTaskHash) {
    throw "Final validation failed: amended TASK parity."
}

foreach ($runRoot in $remainingRunRoots) {
    $text = [System.IO.File]::ReadAllText((Join-Path $runRoot "TASK.md"))

    if (-not $text.Contains("Experimental isolation violation")) {
        throw "Final validation failed: amended workspace classification missing in $runRoot"
    }
    if (-not $text.Contains("recoverable workspace-process incident count")) {
        throw "Final validation failed: amended report fields missing in $runRoot"
    }
    if ($text.Contains("known workspace-boundary violations (must be `0` for PASS)")) {
        throw "Final validation failed: superseded absolute workspace gate still present in $runRoot"
    }
}

# Remaining outputs must still be empty.
foreach ($runRoot in $remainingRunRoots) {
    $items = @(Get-ChildItem -LiteralPath (Join-Path $runRoot "output") -Force)
    if ($items.Count -ne 0) {
        throw "Final validation failed: non-empty output in remaining run $runRoot"
    }
}

Assert-File $AmendmentMd
Assert-File $AmendmentJson
Assert-File $ExecutedTaskCopy

Write-Host ""
Write-Host "Protocol amendment 5.2.1 applied successfully." -ForegroundColor Green
Write-Host ""
Write-Host "M/Run-01:"
Write-Host "  raw TASK preserved"
Write-Host "  raw output/report preserved"
Write-Host "  original TASK SHA256: $oldTaskHash"
Write-Host "  adjudication: VALID / PASS for comparative use"
Write-Host ""
Write-Host "Remaining 9 runs:"
Write-Host "  amended TASK SHA256: $newTaskHash"
Write-Host "  outputs remain empty"
Write-Host ""
Write-Host "Created:"
Write-Host "  protocol-amendments\5.2.1-workspace-boundary-adjudication.md"
Write-Host "  protocol-amendments\5.2.1-manifest.json"
Write-Host "  protocol-amendments\evidence\M-Run-01-TASK-executed.md"
Write-Host ""
Write-Host "Ready for the next Goal run."
