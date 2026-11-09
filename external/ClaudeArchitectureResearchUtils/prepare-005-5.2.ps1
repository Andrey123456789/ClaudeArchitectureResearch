[CmdletBinding()]
param(
    [string]$Root = "C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005",
    [switch]$Recreate52
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = [System.IO.Path]::GetFullPath($Root)
$SourceRoot = Join-Path $Root "5.1"
$TargetRoot = Join-Path $Root "5.2"

$Candidates = @("M", "L0", "L1", "K0", "K1")
$Runs = @("Run-01", "Run-02")

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Content
    )

    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $encoding)
}

function Get-NormalizedText {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Required file not found: $Path"
    }

    return ([System.IO.File]::ReadAllText($Path) -replace "`r`n", "`n")
}

function Replace-ExactOnce {
    param(
        [Parameter(Mandatory = $true)][string]$Text,
        [Parameter(Mandatory = $true)][string]$Old,
        [Parameter(Mandatory = $true)][string]$New,
        [Parameter(Mandatory = $true)][string]$Label
    )

    $count = ([regex]::Matches($Text, [regex]::Escape($Old))).Count
    if ($count -ne 1) {
        throw "Patch '$Label' expected exactly one match, found $count."
    }

    return $Text.Replace($Old, $New)
}

function Clear-DirectoryContents {
    param([Parameter(Mandatory = $true)][string]$Path)

    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        return
    }

    Get-ChildItem -LiteralPath $Path -Force | Remove-Item -Recurse -Force
}

function Assert-RunLayout {
    param([Parameter(Mandatory = $true)][string]$SeriesRoot)

    foreach ($candidate in $Candidates) {
        foreach ($run in $Runs) {
            $runRoot = Join-Path (Join-Path $SeriesRoot $candidate) $run
            $task = Join-Path $runRoot "TASK.md"
            $candidateFile = Join-Path $runRoot "CANDIDATE.md"
            $source = Join-Path $runRoot "source"
            $output = Join-Path $runRoot "output"

            foreach ($required in @($task, $candidateFile, $source, $output)) {
                if (-not (Test-Path -LiteralPath $required)) {
                    throw "Invalid 5.x layout. Missing: $required"
                }
            }
        }
    }
}

if (-not (Test-Path -LiteralPath $SourceRoot -PathType Container)) {
    throw @"
5.1 was not found:
$SourceRoot

Create 005\5.1 first and place the current candidate run tree there.
This script intentionally does not mutate or relocate the current evidence automatically.
"@
}

Assert-RunLayout -SeriesRoot $SourceRoot

if (Test-Path -LiteralPath $TargetRoot) {
    if (-not $Recreate52) {
        throw @"
5.2 already exists:
$TargetRoot

Refusing to overwrite it.
Run again with -Recreate52 only if you intentionally want to rebuild 5.2 from 5.1.
"@
    }

    Remove-Item -LiteralPath $TargetRoot -Recurse -Force
}

# ---------------------------------------------------------------------------
# 1. Clone 5.1 -> 5.2 exactly, then remove all experimental outputs.
# ---------------------------------------------------------------------------

Copy-Item -LiteralPath $SourceRoot -Destination $TargetRoot -Recurse -Force
Assert-RunLayout -SeriesRoot $TargetRoot

foreach ($candidate in $Candidates) {
    foreach ($run in $Runs) {
        $output = Join-Path (Join-Path (Join-Path $TargetRoot $candidate) $run) "output"
        Clear-DirectoryContents -Path $output
    }
}

# ---------------------------------------------------------------------------
# 2. Strengthen the shared TASK.md only.
#    CANDIDATE.md files are intentionally untouched.
# ---------------------------------------------------------------------------

$goalExecutionSection = @'
## 2. Goal-execution contract

Treat this task as a **goal to be completed**, not as a one-pass generation request.

Work autonomously until the deliverables satisfy all binding requirements and every final acceptance check that can be evaluated from the provided inputs.

Required execution loop:

1. read all required inputs completely;
2. design and generate the first complete candidate template;
3. perform the full self-check from Section 10 against the actual generated files;
4. fix every clear defect found;
5. repeat the audit-and-repair cycle until no known binding defect remains;
6. finish only when the final self-check passes.

Do not stop merely because a first complete draft exists.
Do not leave a clear, locally repairable defect for the user to fix in a follow-up prompt.
Do not repeatedly redesign compliant choices merely in search of subjective perfection: once all binding requirements pass, stop.

Early termination is allowed only when the task's explicit contradiction/missing-source rule applies and proceeding would require inventing research material or violating a binding input.

'@

$workspaceStrengthening = @'
## 4. Workspace boundary

The current run directory is the experimental workspace boundary.

Work only inside the current run workspace.

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

`output/` must be empty at the start. If it already contains a previous generated template or report, stop and report the problem.
'@

$separationStrengthening = @'
### 6.3 Separation of concerns

Do not mix these responsibilities in one artifact without a concrete reason:

- normative policy;
- multi-step procedure;
- technique/examples;
- product input;
- deterministic enforcement.

Use the following responsibility model:

- workflow skill = procedure;
- knowledge skill = technique/depth;
- rule / standard / always-loaded policy artifact = normative constraint;
- product files = inputs;
- hook / script / configuration / scaffold asset = deterministic enforcement or delivery.

A multi-step development/review/verification procedure must live in its workflow owner. Always-loaded policy may contain a short routing pointer to that workflow, but must not carry a second copy of the procedure merely for convenience.

In particular, do not place the full Development Workflow or an equivalent multi-step operating procedure in `CLAUDE.md`. `CLAUDE.md` may expose the governing policy, stop/approval boundary, and a concise pointer telling the model which workflow to run.

Pointers and check-by-reference items may cross these boundaries without becoming duplicate owners.
'@

$triggerStrengthening = @'
### 6.5 Trigger assignment and reliable loading

`trigger_class` is part of the frozen experimental input, not an advisory hint.

Preserve the `trigger_class` of **every** inventory policy across candidates. A policy classified as `always`, `path`, or `workflow` must remain in that trigger role after generation; moving it to another trigger role is a construction defect even when the policy wording itself is preserved.

Use these trigger roles:

- `always` → available at planning time through the always-loaded surface;
- `path` → path-scoped rule for at least the policy's declared scope;
- `workflow` → explicit workflow step/procedure with any required owner reads;
- on-demand technique → knowledge skill/reference where applicable;
- mechanically checkable or co-change obligations → deterministic enforcement where appropriate, while keeping critical generation-time boundaries in concise runtime policy.

Do not promote `path` or `workflow` policy into the always-loaded surface merely to make loading easier.
Do not demote `always` policy to a path/workflow/on-demand location merely to reduce token cost.

Critical `must` / `must not` policy must not exist only inside a model-invoked skill or a skill-private reference.

Always-loaded policy must be reachable from `CLAUDE.md`, including through explicit `@` imports where used.

Every rule file must declare `paths`.

Path granularity may vary only where the candidate architecture permits it; minimum scope coverage must not be reduced.

Workflows that depend on policy not guaranteed to have loaded must explicitly read the relevant owner.

Do not solve reliability by loading the whole corpus all the time.

During the final audit, construct an explicit internal mapping from every inventory policy to its generated authoritative owner and trigger role. The audit passes only if the trigger-role delta count is **zero**.
'@

$enforcementStrengthening = @'
### 6.13 Deterministic enforcement

Include a small common enforcement layer where the associated policy makes enforcement meaningful:

- `.editorconfig`;
- `Directory.Build.props`;
- `Directory.Packages.props`;
- `.claude/settings.json`;
- fast cross-platform hooks/scripts;
- an instruction-structure checker;
- architecture/dependency checks or scaffold assets where required by policy.

The experimental host is Windows. Every generated hook entry point and enforcement command must therefore be directly usable from Windows Claude Desktop and must not rely on POSIX-only shell expansion.

In particular:

- do not depend on shell syntax such as `$CLAUDE_PROJECT_DIR/...` inside a hook command;
- if environment variables are needed, resolve them inside the invoked script (for example through `process.env` in Node or the platform-appropriate PowerShell API), rather than relying on POSIX command-line expansion;
- prefer shell-neutral hook commands and cross-platform implementation scripts where practical;
- generated deterministic tooling must fail clearly rather than silently skipping enforcement when a path/environment assumption is not met.

At minimum, support these hook intentions:

- dependency command/change → route to `add-dependency`;
- package/project manifest change → check central package management, versions, deny-list, and project references;
- `SPECIFICATION.md` / `CUSTOM_SETTINGS.md` change → synchronization reminder;
- stop/co-change checks → seed/migration/test reminders where applicable, without creating an execution loop.

Hook messages point to the authoritative owner/workflow and do not restate policy.

Mechanical rules should be checked mechanically where practical, while critical generation-time boundaries remain concise runtime policy as well.

The instruction-structure checker must validate the structural predicates of the assigned candidate, not another candidate's architecture.
'@

$finalSelfCheck = @'
## 10. Final acceptance loop

Do not treat this section as a report-only checklist. Execute it against the generated files, repair failures, and rerun the checks until all applicable items pass.

Before finishing, verify that:

1. `output/template/` is standalone;
2. all applicable V2-derived policy semantics from `source/inventory.json` are preserved;
3. shared construction requirements from Section 6 and `source/shared-research-invariants.json` are preserved;
4. the structure satisfies every binding rule in `CANDIDATE.md`;
5. each normative policy has one authoritative owner and there is no accidental semantic duplication;
6. every internal import/reference resolves;
7. all inventory `trigger_class` assignments are preserved with **zero trigger-role deltas**;
8. all inventory minimum scope requirements are preserved;
9. critical must-rules are not hidden only in model-invoked/on-demand material;
10. multi-step procedures are owned by workflow artifacts rather than duplicated into always-loaded policy;
11. product inputs remain inputs and do not become instruction layers;
12. required workflows, knowledge surfaces, deterministic enforcement, and the human map are present;
13. generated hook/enforcement commands are Windows-compatible and do not rely on POSIX-only environment-variable expansion;
14. no generated or temporary file exists outside `output/`, and no construction artifact depends on a parent/sibling workspace;
15. no concrete application or benchmark implementation was generated;
16. runtime artifacts contain no research-only metadata;
17. output does not depend on files outside `output/template/`;
18. the structure remains understandable to a human maintainer and does not contain gratuitous layers/files;
19. the always-loaded surface remains compact without changing frozen trigger roles merely to optimize token count;
20. **all technical and programming-related output is in English**.

Also record in `GENERATION_REPORT.md`:

- final acceptance result: `PASS` or `BLOCKED`;
- trigger-role delta count (must be `0` for PASS);
- unresolved broken-reference count (must be `0` for PASS);
- known workspace-boundary violations (must be `0` for PASS);
- known Windows-hook compatibility defects (must be `0` for PASS).

If any locally repairable item fails, continue working and repair it before completion.

If a genuinely required source is missing or the binding inputs contain an irreconcilable contradiction, report `BLOCKED` with the exact reason and stop instead of fabricating a result.
'@

$taskHashesBefore = @{}
$taskHashesAfter = @{}

foreach ($candidate in $Candidates) {
    foreach ($run in $Runs) {
        $runRoot = Join-Path (Join-Path $TargetRoot $candidate) $run
        $taskPath = Join-Path $runRoot "TASK.md"
        $candidatePath = Join-Path $runRoot "CANDIDATE.md"

        $taskHashesBefore["$candidate/$run"] = (Get-FileHash -LiteralPath $taskPath -Algorithm SHA256).Hash
        $candidateHashBefore = (Get-FileHash -LiteralPath $candidatePath -Algorithm SHA256).Hash

        $task = Get-NormalizedText -Path $taskPath

        $oldGoalBoundary = @'
## 2. Language requirement
'@
        $task = Replace-ExactOnce -Text $task -Old $oldGoalBoundary -New ($goalExecutionSection + "## 3. Language requirement`n") -Label "insert goal-execution contract"

        # Renumber the original sections following the new Goal-execution section.
        $task = $task.Replace("## 3. Required inputs", "## 4. Required inputs")
        $task = $task.Replace("## 4. Workspace boundary", "## 5. Workspace boundary")
        $task = $task.Replace("## 5. Contract and conflict handling", "## 6. Contract and conflict handling")
        $task = $task.Replace("## 6. Shared mandatory properties", "## 7. Shared mandatory properties")
        $task = $task.Replace("### 6.", "### 7.")
        $task = $task.Replace("Section 6", "Section 7")
        $task = $task.Replace("## 7. Candidate binding and design freedom", "## 8. Candidate binding and design freedom")
        $task = $task.Replace("## 8. Deliverables", "## 9. Deliverables")
        $task = $task.Replace("## 9. Final self-check", "## 10. Final self-check")

        # Replace strengthened sections after renumbering.
        $workspaceOldStart = @'
## 5. Workspace boundary

Work only inside the current run workspace.

Do not:

- read files above the workspace root;
- use the network;
- use external repositories;
- inspect another run;
- inspect outputs from another run;
- attempt to reconstruct intentionally excluded benchmark, metrics, ranking, or other research material.

Write only under `output/`.

`output/` must be empty at the start. If it already contains a previous generated template or report, stop and report the problem.
'@
        $task = Replace-ExactOnce -Text $task -Old $workspaceOldStart -New $workspaceStrengthening.Replace("## 4.", "## 5.") -Label "strengthen workspace boundary"

        $separationOld = @'
### 7.3 Separation of concerns

Do not mix these responsibilities in one artifact without a concrete reason:

- normative policy;
- multi-step procedure;
- technique/examples;
- product input;
- deterministic enforcement.

Use the following responsibility model:

- workflow skill = procedure;
- knowledge skill = technique/depth;
- rule / standard / always-loaded policy artifact = normative constraint;
- product files = inputs;
- hook / script / configuration / scaffold asset = deterministic enforcement or delivery.

Pointers and check-by-reference items may cross these boundaries without becoming duplicate owners.
'@
        $task = Replace-ExactOnce -Text $task -Old $separationOld -New $separationStrengthening.Replace("### 6.3", "### 7.3") -Label "strengthen procedure/policy separation"

        $triggerOldStart = @'
### 7.5 Trigger assignment and reliable loading

Preserve the `trigger_class` of every inventory policy across candidates.

Use these trigger roles:

- `always` → available at planning time through the always-loaded surface;
- `path` → path-scoped rule for at least the policy's declared scope;
- `workflow` → explicit workflow step/procedure with any required owner reads;
- on-demand technique → knowledge skill/reference where applicable;
- mechanically checkable or co-change obligations → deterministic enforcement where appropriate, while keeping critical generation-time boundaries in concise runtime policy.

Critical `must` / `must not` policy must not exist only inside a model-invoked skill or a skill-private reference.

Always-loaded policy must be reachable from `CLAUDE.md`, including through explicit `@` imports where used.

Every rule file must declare `paths`.

Path granularity may vary only where the candidate architecture permits it; minimum scope coverage must not be reduced.

Workflows that depend on policy not guaranteed to have loaded must explicitly read the relevant owner.

Do not solve reliability by loading the whole corpus all the time.
'@
        $task = Replace-ExactOnce -Text $task -Old $triggerOldStart -New $triggerStrengthening.Replace("### 6.5", "### 7.5") -Label "freeze trigger-class assignment"

        $enforcementOld = @'
### 7.13 Deterministic enforcement

Include a small common enforcement layer where the associated policy makes enforcement meaningful:

- `.editorconfig`;
- `Directory.Build.props`;
- `Directory.Packages.props`;
- `.claude/settings.json`;
- fast cross-platform hooks/scripts;
- an instruction-structure checker;
- architecture/dependency checks or scaffold assets where required by policy.

At minimum, support these hook intentions:

- dependency command/change → route to `add-dependency`;
- package/project manifest change → check central package management, versions, deny-list, and project references;
- `SPECIFICATION.md` / `CUSTOM_SETTINGS.md` change → synchronization reminder;
- stop/co-change checks → seed/migration/test reminders where applicable, without creating an execution loop.

Hook messages point to the authoritative owner/workflow and do not restate policy.

Mechanical rules should be checked mechanically where practical, while critical generation-time boundaries remain concise runtime policy as well.

The instruction-structure checker must validate the structural predicates of the assigned candidate, not another candidate's architecture.
'@
        $task = Replace-ExactOnce -Text $task -Old $enforcementOld -New $enforcementStrengthening.Replace("### 6.13", "### 7.13") -Label "require Windows-compatible enforcement"

        $finalOldStart = $task.Substring($task.IndexOf("## 10. Final self-check"))
        if (-not $finalOldStart.StartsWith("## 10. Final self-check")) {
            throw "Could not locate final self-check in $taskPath"
        }
        $task = $task.Substring(0, $task.IndexOf("## 10. Final self-check")) + $finalSelfCheck

        # Normalize final LF content back to Windows CRLF for local readability.
        $taskWindows = $task -replace "(?<!`r)`n", "`r`n"
        Write-Utf8NoBom -Path $taskPath -Content $taskWindows

        $candidateHashAfter = (Get-FileHash -LiteralPath $candidatePath -Algorithm SHA256).Hash
        if ($candidateHashBefore -ne $candidateHashAfter) {
            throw "CANDIDATE.md changed unexpectedly: $candidatePath"
        }

        $taskHashesAfter["$candidate/$run"] = (Get-FileHash -LiteralPath $taskPath -Algorithm SHA256).Hash
    }
}

# ---------------------------------------------------------------------------
# 3. Verify TASK parity across all ten runs.
# ---------------------------------------------------------------------------

$distinctTaskHashes = @($taskHashesAfter.Values | Sort-Object -Unique)
if ($distinctTaskHashes.Count -ne 1) {
    throw "TASK.md parity failure: 5.2 does not contain one byte-identical shared TASK across all ten runs."
}

foreach ($candidate in $Candidates) {
    $c1 = Join-Path (Join-Path (Join-Path $TargetRoot $candidate) "Run-01") "CANDIDATE.md"
    $c2 = Join-Path (Join-Path (Join-Path $TargetRoot $candidate) "Run-02") "CANDIDATE.md"
    if ((Get-FileHash $c1 -Algorithm SHA256).Hash -ne (Get-FileHash $c2 -Algorithm SHA256).Hash) {
        throw "Candidate parity failure for ${candidate}: Run-01 and Run-02 CANDIDATE.md differ."
    }
}

# ---------------------------------------------------------------------------
# 4. Write one shared Goal prompt OUTSIDE run workspaces.
#    The human pastes this into Claude Desktop Goal mode for every run.
# ---------------------------------------------------------------------------

$goalPrompt = @'
Read `TASK.md` completely and execute it as an autonomous goal.

Produce the complete required runtime instruction template and keep working until every binding requirement and final acceptance check in `TASK.md` passes. Do not stop after the first complete draft: audit the actual generated files, repair every clear defect, and repeat the audit-and-repair cycle until the result is PASS.

Do not ask for a follow-up prompt to fix a defect you can resolve from the provided inputs. Stop early only if `TASK.md` explicitly requires BLOCKED because of a genuine missing source or irreconcilable contradiction.
'@
Write-Utf8NoBom -Path (Join-Path $TargetRoot "GOAL_PROMPT.txt") -Content (($goalPrompt.TrimEnd()) -replace "(?<!`r)`n", "`r`n")

# ---------------------------------------------------------------------------
# 5. Record local 5.2 provenance without placing research metadata in runs.
# ---------------------------------------------------------------------------

$readme = @"
# Iteration 005 / 5.2

5.2 was cloned from 5.1 and all run `output/` directories were cleared before execution.

Purpose of 5.2:

- preserve every frozen inventory `trigger_class` exactly;
- strengthen procedure/policy separation;
- require Windows-compatible deterministic enforcement;
- strengthen parent/sibling workspace isolation;
- execute generation as an autonomous Goal with repeated self-audit and repair until objective acceptance gates pass.

`CANDIDATE.md` files were not modified by the 5.2 preparation script.
The shared `TASK.md` is byte-identical across all ten runs.

Use the exact prompt in `GOAL_PROMPT.txt` for every Claude Desktop Goal run.
"@
Write-Utf8NoBom -Path (Join-Path $TargetRoot "README-5.2.md") -Content (($readme.TrimEnd()) -replace "(?<!`r)`n", "`r`n")

# ---------------------------------------------------------------------------
# 6. Final validation.
# ---------------------------------------------------------------------------

foreach ($candidate in $Candidates) {
    foreach ($run in $Runs) {
        $runRoot = Join-Path (Join-Path $TargetRoot $candidate) $run
        $output = Join-Path $runRoot "output"
        $items = @(Get-ChildItem -LiteralPath $output -Force)
        if ($items.Count -ne 0) {
            throw "Output cleanup failed: $output is not empty."
        }
    }
}

Write-Host ""
Write-Host "Iteration 005 / 5.2 prepared successfully."
Write-Host ""
Write-Host "Source evidence preserved at:"
Write-Host "  $SourceRoot"
Write-Host ""
Write-Host "New clean series:"
Write-Host "  $TargetRoot"
Write-Host ""
Write-Host "Shared TASK SHA256:"
Write-Host "  $($distinctTaskHashes[0])"
Write-Host ""
Write-Host "Goal prompt:"
Write-Host "  $(Join-Path $TargetRoot 'GOAL_PROMPT.txt')"
Write-Host ""
Write-Host "All ten output directories are empty."
Write-Host "CANDIDATE.md files were not modified."
