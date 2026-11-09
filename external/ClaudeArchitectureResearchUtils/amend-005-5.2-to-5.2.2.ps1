[CmdletBinding()]
param(
    [string]$Root = "C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.2"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$Root = [System.IO.Path]::GetFullPath($Root)
$Candidates = @("M", "L0", "L1", "K0", "K1")
$Runs = @("Run-01", "Run-02")

$Completed = @(
    "M\Run-01",
    "L0\Run-01"
)

$Remaining = @(
    "M\Run-02",
    "L0\Run-02",
    "L1\Run-01",
    "L1\Run-02",
    "K0\Run-01",
    "K0\Run-02",
    "K1\Run-01",
    "K1\Run-02"
)

$ProtocolDir = Join-Path $Root "protocol-amendments"
$EvidenceDir = Join-Path $ProtocolDir "evidence"
$AmendmentMd = Join-Path $ProtocolDir "5.2.2-bounded-convergence.md"
$AmendmentJson = Join-Path $ProtocolDir "5.2.2-manifest.json"
$ReadmePath = Join-Path $Root "README.md"
$GoalPath = Join-Path $Root "GOAL_PROMPT.txt"

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
    $lines = @(
        Get-ChildItem -LiteralPath $base -Recurse -File -Force |
        ForEach-Object {
            $relative = $_.FullName.Substring($base.Length).TrimStart('\','/').Replace('\','/')
            "$relative`t$(Get-Sha256 $_.FullName)"
        } |
        Sort-Object
    )
    $joined = $lines -join "`n"
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($joined)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace("-", "").ToLowerInvariant()
    }
    finally {
        $sha.Dispose()
    }
}

function Replace-Section(
    [string]$Text,
    [string]$StartHeadingRegex,
    [string]$NextHeadingRegex,
    [string]$Replacement,
    [string]$Label,
    [string]$Path
) {
    $pattern = "(?ms)^$StartHeadingRegex.*?(?=^$NextHeadingRegex)"
    $matches = [regex]::Matches($Text, $pattern)
    if ($matches.Count -ne 1) {
        throw "Expected exactly one section [$Label] in $Path, found $($matches.Count)."
    }
    return [regex]::Replace($Text, $pattern, ($Replacement.TrimEnd() + "`r`n`r`n"), 1)
}

function Replace-TailSection(
    [string]$Text,
    [string]$StartHeadingRegex,
    [string]$Replacement,
    [string]$Label,
    [string]$Path
) {
    $pattern = "(?ms)^$StartHeadingRegex.*\z"
    $matches = [regex]::Matches($Text, $pattern)
    if ($matches.Count -ne 1) {
        throw "Expected exactly one tail section [$Label] in $Path, found $($matches.Count)."
    }
    return [regex]::Replace($Text, $pattern, ($Replacement.TrimEnd() + "`r`n"), 1)
}

function RunPath([string]$Relative) {
    return Join-Path $Root $Relative
}

Write-Host ""
Write-Host "Iteration 005 / Protocol Amendment 5.2.2"
Write-Host "Root: $Root"
Write-Host ""

Assert-Directory $Root
Assert-File $GoalPath
Assert-File $ReadmePath

# ---------------------------------------------------------------------------
# CHECKLIST A — preflight / evidence protection
# ---------------------------------------------------------------------------

Write-Host "Checklist A: preflight and evidence protection"

$allRuns = @()
foreach ($candidate in $Candidates) {
    foreach ($run in $Runs) {
        $relative = "$candidate\$run"
        $allRuns += $relative
        $runRoot = RunPath $relative
        Assert-Directory $runRoot
        Assert-File (Join-Path $runRoot "TASK.md")
        Assert-File (Join-Path $runRoot "CANDIDATE.md")
        Assert-Directory (Join-Path $runRoot "source")
        Assert-File (Join-Path $runRoot "source\inventory.json")
        Assert-File (Join-Path $runRoot "source\shared-research-invariants.json")
        Assert-Directory (Join-Path $runRoot "source\v2-baseline")
        Assert-Directory (Join-Path $runRoot "output")
    }
}

if ($allRuns.Count -ne 10) {
    throw "Expected 10 runs, found $($allRuns.Count)."
}

# Completed runs must contain evidence; remaining runs must still be clean.
foreach ($relative in $Completed) {
    $output = Join-Path (RunPath $relative) "output"
    $items = @(Get-ChildItem -LiteralPath $output -Force)
    if ($items.Count -eq 0) {
        throw "Completed run has empty output: $relative"
    }
    Assert-File (Join-Path $output "GENERATION_REPORT.md")
}

foreach ($relative in $Remaining) {
    $output = Join-Path (RunPath $relative) "output"
    $items = @(Get-ChildItem -LiteralPath $output -Force)
    if ($items.Count -ne 0) {
        throw "Refusing to patch an already-executed remaining run: $relative"
    }
}

# Candidate definitions must remain pair-identical.
$candidateHashesBefore = [ordered]@{}
foreach ($candidate in $Candidates) {
    $p1 = Join-Path (RunPath "$candidate\Run-01") "CANDIDATE.md"
    $p2 = Join-Path (RunPath "$candidate\Run-02") "CANDIDATE.md"
    $h1 = Get-Sha256 $p1
    $h2 = Get-Sha256 $p2
    if ($h1 -ne $h2) {
        throw "CANDIDATE.md parity failure for ${candidate}."
    }
    $candidateHashesBefore[$candidate] = $h1
}

# Shared source must be identical across all ten runs.
$sourceReference = $null
foreach ($relative in $allRuns) {
    $sig = Get-TreeSignature (Join-Path (RunPath $relative) "source")
    if ($null -eq $sourceReference) {
        $sourceReference = $sig
    }
    elseif ($sig -ne $sourceReference) {
        throw "Source-tree parity failure at $relative."
    }
}

# Remaining eight TASK files must currently be identical.
$remainingOldTaskHashes = @(
    $Remaining |
    ForEach-Object { Get-Sha256 (Join-Path (RunPath $_) "TASK.md") } |
    Sort-Object -Unique
)
if ($remainingOldTaskHashes.Count -ne 1) {
    throw "Remaining TASK.md files are not identical before amendment."
}
$oldRemainingTaskHash = $remainingOldTaskHashes[0]

# Freeze completed raw evidence before touching anything.
$completedTaskHashesBefore = [ordered]@{}
$completedOutputHashesBefore = [ordered]@{}
foreach ($relative in $Completed) {
    $completedTaskHashesBefore[$relative] = Get-Sha256 (Join-Path (RunPath $relative) "TASK.md")
    $completedOutputHashesBefore[$relative] = Get-TreeSignature (Join-Path (RunPath $relative) "output")
}

$oldGoalHash = Get-Sha256 $GoalPath
$oldGoalText = [System.IO.File]::ReadAllText($GoalPath)

New-Item -ItemType Directory -Path $EvidenceDir -Force | Out-Null

$oldGoalEvidence = Join-Path $EvidenceDir "GOAL_PROMPT-used-by-M-R1-and-L0-R1.txt"
if (Test-Path -LiteralPath $oldGoalEvidence) {
    if ((Get-Sha256 $oldGoalEvidence) -ne $oldGoalHash) {
        throw "Existing preserved GOAL_PROMPT does not match the currently executed prompt."
    }
}
else {
    Copy-Item -LiteralPath $GoalPath -Destination $oldGoalEvidence
}

$l0TaskEvidence = Join-Path $EvidenceDir "L0-Run-01-TASK-executed.md"
if (-not (Test-Path -LiteralPath $l0TaskEvidence)) {
    Copy-Item -LiteralPath (Join-Path (RunPath "L0\Run-01") "TASK.md") -Destination $l0TaskEvidence
}

Write-Host "  PASS - completed runs protected; remaining 8 outputs empty"
Write-Host "  PASS - candidate pairs and source trees are identical"

# ---------------------------------------------------------------------------
# Amendment content
# ---------------------------------------------------------------------------

$Section2 = @'
## 2. Goal-execution contract

Treat this task as a **goal to be completed**, not as a one-pass generation request.

Work autonomously until the deliverables satisfy the binding requirements. Use the bounded verification protocol below. The purpose is to catch real template defects without spending additional cycles proving that prior verification was itself verified.

### Required execution protocol

1. Read all required inputs completely.
2. Design and generate the first complete candidate template.
3. Run one **primary substantive audit** against the actual generated files.
4. Repair every concrete binding defect found by that audit.
5. Run one **confirmation audit** against the repaired template.
6. If the confirmation audit finds a new concrete defect in `output/template/`, repair that defect and rerun the confirmation audit.
7. When a complete confirmation audit finds **zero concrete template defects**, update `GENERATION_REPORT.md`, remove `output/.work/`, and stop.

Do not declare PASS before the primary substantive audit has covered all of these high-value checks:

- explicit owner + trigger-role + minimum-scope mapping for every inventory policy and shared runtime invariant;
- semantic-fidelity review between each normalized policy and its authoritative owner text, including strength/condition preservation;
- systematic V2 preservation review across the complete baseline, using automation to identify unmatched files/sections/headings and manual review only where automation cannot establish preservation;
- duplicate/restatement sweep across rules, workflows, knowledge skills, imports, and decision summaries;
- candidate-specific structural constraints and dependency direction;
- internal reference resolution;
- deterministic enforcement/checker behavior, including Windows-compatible hook launching;
- research-metadata/language/output hygiene and the always-loaded budget.

The confirmation audit is the convergence proof. It may reuse deterministic tooling created during the primary audit. It must recheck all binding gates and must specifically recheck anything changed during repair.

### Stop rule

A **concrete template defect** is a specific generated-file condition that violates a binding item in this `TASK.md`, `CANDIDATE.md`, `source/inventory.json`, or `source/shared-research-invariants.json`.

The following are **not** reasons to start another audit cycle after a zero-defect confirmation audit:

- a request for more detailed prose or stronger narrative evidence;
- a request to prove that the previous audit was independently verified;
- a request to inspect platform/session logs or other data outside the workspace;
- a request for another convergence cycle when no generated file changed and no concrete binding defect was identified;
- corrections that affect only `GENERATION_REPORT.md` bookkeeping and do not reveal a template defect.

If a Goal/Stop evaluator raises a concrete failed binding item with evidence, fix it. If it only asks for stronger meta-verification without identifying a concrete template defect, do **not** reopen the audit. The task is complete once the confirmation audit reaches zero concrete template defects.

Do not repeatedly redesign compliant choices in search of subjective perfection.

Early termination is allowed only when the task's explicit contradiction/missing-source rule applies and proceeding would require inventing research material or violating a binding input.
'@

$Section5 = @'
## 5. Workspace boundary

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
- intentionally create construction artifacts, caches, reports, or helper files outside the current run workspace.

Write generated deliverables only under `output/`.

If temporary construction/audit material is needed, keep it under `output/.work/` and remove `output/.work/` before final completion.

Before reading or writing a path derived programmatically, ensure its resolved absolute path remains inside the current run workspace. Treat a path that escapes the workspace as invalid even if the operating system permits access.

When testing Git behavior in a scratch repository, cap upward discovery at the scratch/workspace boundary (for example with `GIT_CEILING_DIRECTORIES`) from the first test. When testing hooks or path handling, use in-workspace sandboxes and simulated inputs rather than deliberate probes of external paths.

### Workspace-event classification

Distinguish three classes during normal execution:

1. **Experimental isolation violation** — the run reads or depends on forbidden external information, including parent/sibling run content, another candidate's output or metadata, external repositories, network material, or intentionally excluded research material. These are validity failures and must be `0` for PASS.
2. **Recoverable workspace-process incident** — the model accidentally targets an outside path or temporarily writes allowed-input-derived scratch/audit data outside the workspace, obtains no forbidden external information, detects the mistake, and remediates it. Record the incident briefly; after remediation it does not by itself prevent PASS.
3. **Platform-managed persistence event** — Claude Desktop, the tool runtime, operating system, or another platform-managed component automatically stores session state, logs, command output, or tool results outside the workspace without the run choosing that storage location. Record only events surfaced directly during normal execution. Such an event is not an isolation violation and does not prevent PASS unless the run consumes forbidden external information from it or makes the result depend on it.

### Evidence ceiling for workspace events

Do **not** enumerate, open, parse, or cross-check Claude/session/transcript/tool-result storage outside the workspace for the purpose of proving isolation or completeness of the event ledger.

Do **not** use session-management tools to obtain an independent record of this run.

The event record in `GENERATION_REPORT.md` is based on events directly observed during normal execution. It is not required to be exhaustive with respect to hidden platform behavior. An uncertainty about unseen platform internals does not fail acceptance unless there is concrete evidence that forbidden information was consumed or the generated result depends on an external artifact.

A recoverable incident or report-count correction does not by itself require a new full audit cycle. Start another confirmation cycle only if the incident or correction reveals a concrete defect in `output/template/`.
'@

$Section10 = @'
## 10. Final acceptance and confirmation

The quality bar below is unchanged. Evaluate it against the generated files as part of the primary audit, repair concrete failures, then run the confirmation audit defined in Section 2.

Before finishing, verify that:

1. `output/template/` is standalone;
2. all applicable V2-derived policy semantics from `source/inventory.json` are preserved;
3. shared construction requirements from Section 7 and `source/shared-research-invariants.json` are preserved;
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
14. experimental isolation violations are `0`; all directly observed recoverable workspace-process incidents are remediated; directly observed platform-managed persistence events create no forbidden external dependency;
15. no concrete application or benchmark implementation was generated;
16. runtime artifacts contain no research-only metadata;
17. output does not depend on files outside `output/template/`;
18. the structure remains understandable to a human maintainer and does not contain gratuitous layers/files;
19. the always-loaded surface remains compact without changing frozen trigger roles merely to optimize token count;
20. **all technical and programming-related output is in English**.

### Required audit evidence

The primary audit must produce enough in-workspace evidence to support the checks above. Prefer compact machine-readable or scripted evidence under `output/.work/`, deleted before completion.

At minimum, establish:

- policy owner / trigger / scope coverage for the complete normalized policy set;
- semantic-fidelity review of policy owner text;
- systematic preservation coverage of the complete V2 baseline, with manual review of unmatched material;
- duplicate/restatement review;
- candidate-structure and dependency checks;
- internal-reference checks;
- deterministic checker/hook tests appropriate to the generated template;
- output/research-metadata/language checks;
- a directly observed workspace-event summary.

Do **not** turn evidence generation into a separate research project. The acceptance target is the generated template, not an exhaustive reconstruction of Claude Desktop internals.

### Confirmation and completion rule

After repairs, run one complete confirmation audit.

- If it finds a concrete template defect, repair it and rerun the confirmation audit.
- If it finds **zero concrete template defects**, convergence is established.
- Report-only wording/count corrections that reveal no template defect do not reset convergence.
- Do not hash and re-hash the full deliverable tree merely to prove that a zero-defect confirmation audit was a fixed point.
- Do not seek an external or "independent" record of the current session.
- Do not read platform session/transcript/tool-result files outside the workspace to strengthen item 14.
- Do not run another audit solely because a Goal/Stop evaluator requests stronger evidence without identifying a failed binding item.

Once the zero-defect confirmation audit completes, write/update `GENERATION_REPORT.md`, remove `output/.work/`, verify that `output/` contains only the required deliverables, and **stop immediately**.

Record in `GENERATION_REPORT.md`:

- final acceptance result: `PASS` or `BLOCKED`;
- trigger-role delta count (must be `0` for PASS);
- unresolved broken-reference count (must be `0` for PASS);
- known Windows-hook compatibility defects (must be `0` for PASS);
- directly observed experimental isolation violation count (must be `0` for PASS);
- directly observed recoverable workspace-process incidents and remediation status;
- directly observed platform-managed persistence events, if any;
- primary-audit repairs that materially changed the template;
- confirmation-audit result (`0` concrete template defects is the completion condition).

If a genuinely required source is missing or the binding inputs contain an irreconcilable contradiction, report `BLOCKED` with the exact reason and stop instead of fabricating a result.
'@

$NewGoal = @'
Read `TASK.md` completely and execute it as an autonomous goal.

Produce the complete required runtime instruction template. Follow the bounded verification protocol in `TASK.md`: perform the required primary substantive audit, repair every concrete binding defect it finds, then run the confirmation audit.

Do not declare PASS before the primary audit and confirmation audit are complete. Once a complete confirmation audit finds zero concrete template defects, update the report, clean the scratch area, and stop immediately.

Do not start extra audit cycles merely to obtain stronger narrative evidence, independent verification, platform/session-log proof, repeated hashes, or another convergence demonstration when no concrete failed binding item has been identified.

Do not ask for a follow-up prompt to fix a defect you can resolve from the provided inputs. Stop early only if `TASK.md` explicitly requires BLOCKED because of a genuine missing source or irreconcilable contradiction.
'@

# ---------------------------------------------------------------------------
# CHECKLIST B — patch only the 8 unexecuted runs
# ---------------------------------------------------------------------------

Write-Host ""
Write-Host "Checklist B: apply bounded-convergence protocol to remaining 8 runs"

foreach ($relative in $Remaining) {
    $taskPath = Join-Path (RunPath $relative) "TASK.md"
    $text = [System.IO.File]::ReadAllText($taskPath)

    $text = Replace-Section `
        -Text $text `
        -StartHeadingRegex '## 2\. Goal-execution contract\s*$' `
        -NextHeadingRegex '## 3\. Language requirement\s*$' `
        -Replacement $Section2 `
        -Label "Section 2" `
        -Path $taskPath

    $text = Replace-Section `
        -Text $text `
        -StartHeadingRegex '## 5\. Workspace boundary\s*$' `
        -NextHeadingRegex '## 6\. Contract and conflict handling\s*$' `
        -Replacement $Section5 `
        -Label "Section 5" `
        -Path $taskPath

    $text = Replace-TailSection `
        -Text $text `
        -StartHeadingRegex '## 10\. Final acceptance loop\s*$' `
        -Replacement $Section10 `
        -Label "Section 10" `
        -Path $taskPath

    Write-Utf8NoBom -Path $taskPath -Content $text
}

Write-Utf8NoBom -Path $GoalPath -Content ($NewGoal.TrimEnd() + "`r`n")

$newTaskHashes = @(
    $Remaining |
    ForEach-Object { Get-Sha256 (Join-Path (RunPath $_) "TASK.md") } |
    Sort-Object -Unique
)
if ($newTaskHashes.Count -ne 1) {
    throw "Patched TASK.md files are not byte-identical."
}
$newTaskHash = $newTaskHashes[0]
$newGoalHash = Get-Sha256 $GoalPath

if ($newTaskHash -eq $oldRemainingTaskHash) {
    throw "TASK amendment did not change the remaining task."
}
if ($newGoalHash -eq $oldGoalHash) {
    throw "GOAL_PROMPT amendment did not change the prompt."
}

Write-Host "  PASS - 8 TASK.md files patched identically"
Write-Host "  PASS - GOAL_PROMPT updated"

# ---------------------------------------------------------------------------
# Protocol documentation
# ---------------------------------------------------------------------------

$AmendmentText = @'
# Iteration 005 / Protocol Amendment 5.2.2 — bounded convergence

## Reason

`L0/Run-01` demonstrated two things simultaneously:

1. deeper post-draft auditing materially improved the template by finding real semantic-strength drift, duplicate policy restatements, and missing V2 technique;
2. after the template reached a zero-defect fixed point, the Goal/Stop loop continued consuming tokens on meta-evidence, session-log reconstruction, repeated convergence proof, and requests for independent verification that were not additional template-quality requirements.

The amendment preserves the useful audit depth while removing unbounded meta-verification.

## Quality-preserving change

The remaining unexecuted runs must perform a primary substantive audit before PASS. That audit explicitly includes policy semantic fidelity, trigger/scope ownership, systematic V2 preservation, duplicate review, candidate structure, references, Windows hooks/checkers, and hygiene.

After repairs, one complete confirmation audit is the convergence proof. If that audit finds a concrete template defect, the defect is repaired and the confirmation audit is repeated. A zero-defect confirmation audit ends the task.

## What no longer reopens the audit

The following do not trigger another full cycle unless they reveal a concrete defect in `output/template/`:

- report-only bookkeeping corrections;
- requests for stronger prose or independent verification;
- platform/session-log reconstruction;
- transcript/session storage inspection;
- repeated file hashing solely to prove convergence;
- another audit request with no specific failed binding item.

## Workspace evidence ceiling

Platform-managed events are recorded only when surfaced directly during normal execution. Runs must not read or enumerate external session/transcript/tool-result storage merely to prove isolation.

## Provenance

`M/Run-01` and `L0/Run-01` remain unchanged as raw evidence and keep the TASK/GOAL protocol actually used for those runs.

The remaining eight runs use the 5.2.2 bounded-convergence TASK and GOAL prompt.
'@

$AmendmentText = $AmendmentText.TrimEnd() + "`r`n"
Write-Utf8NoBom -Path $AmendmentMd -Content $AmendmentText

$manifest = [ordered]@{
    schema_version = "1.0"
    amendment = "5.2.2"
    created_utc = [DateTime]::UtcNow.ToString("o")
    reason = "Preserve substantive audit depth while preventing unbounded post-convergence meta-verification."
    completed_runs_preserved = @(
        [ordered]@{
            run = "M/Run-01"
            task_sha256 = $completedTaskHashesBefore["M\Run-01"]
            output_tree_sha256 = $completedOutputHashesBefore["M\Run-01"]
        },
        [ordered]@{
            run = "L0/Run-01"
            task_sha256 = $completedTaskHashesBefore["L0\Run-01"]
            output_tree_sha256 = $completedOutputHashesBefore["L0\Run-01"]
        }
    )
    executed_goal_prompt_sha256 = $oldGoalHash
    remaining_runs = [ordered]@{
        count = 8
        old_task_sha256 = $oldRemainingTaskHash
        amended_task_sha256 = $newTaskHash
        amended_goal_prompt_sha256 = $newGoalHash
    }
    quality_controls = @(
        "complete policy owner/trigger/scope mapping",
        "semantic-fidelity review",
        "systematic V2 preservation review",
        "duplicate/restatement review",
        "candidate structural validation",
        "internal reference validation",
        "Windows hook/checker validation",
        "zero-defect confirmation audit"
    )
    bounded_controls = @(
        "no external session-log reconstruction",
        "no independent-verification loop",
        "no repeated convergence hashing without a concrete defect",
        "report-only corrections do not reopen full audit"
    )
}

Write-Utf8NoBom -Path $AmendmentJson -Content (($manifest | ConvertTo-Json -Depth 12) + "`r`n")

# README: append one protocol note if not already present.
$readme = [System.IO.File]::ReadAllText($ReadmePath)
if (-not $readme.Contains("## Protocol amendment 5.2.2")) {
    $readmeAppend = @'

## Protocol amendment 5.2.2

After `L0/Run-01`, the protocol was refined to preserve the useful deep audit while preventing post-convergence token loops.

`M/Run-01` and `L0/Run-01` remain unchanged raw evidence. The remaining eight runs use a bounded verification protocol:

1. primary substantive audit with policy-semantic, V2-preservation, duplication, structure, reference, enforcement, and hygiene checks;
2. repair concrete template defects;
3. confirmation audit;
4. repeat confirmation only if it identifies a new concrete template defect;
5. stop immediately after a zero-defect confirmation audit.

Meta-evidence requests, external session-log reconstruction, repeated convergence hashing, and report-only corrections do not reopen the audit unless they reveal a concrete template defect.

See `protocol-amendments/5.2.2-bounded-convergence.md` and `protocol-amendments/5.2.2-manifest.json`.
'@
    Write-Utf8NoBom -Path $ReadmePath -Content ($readme.TrimEnd() + $readmeAppend + "`r`n")
}

# ---------------------------------------------------------------------------
# CHECKLIST C — prove quality controls are present and waste loops are absent
# ---------------------------------------------------------------------------

Write-Host ""
Write-Host "Checklist C: validate quality floor and stop conditions"

$requiredPhrases = @(
    "semantic-fidelity review",
    "systematic V2 preservation review",
    "duplicate/restatement",
    "zero trigger-role deltas",
    "Windows-compatible",
    "confirmation audit",
    "zero concrete template defects",
    "stop immediately",
    "Do not read platform session/transcript/tool-result files outside the workspace"
)

$forbiddenFuturePhrases = @(
    "repeat the audit-and-repair cycle until the result is PASS",
    "independently verified against the platform"
)

foreach ($relative in $Remaining) {
    $taskPath = Join-Path (RunPath $relative) "TASK.md"
    $text = [System.IO.File]::ReadAllText($taskPath)

    foreach ($phrase in $requiredPhrases) {
        if (-not $text.Contains($phrase)) {
            throw "Quality/stop requirement missing in ${relative}: $phrase"
        }
    }

    foreach ($phrase in $forbiddenFuturePhrases) {
        if ($text.Contains($phrase)) {
            throw "Unbounded-loop phrase still present in ${relative}: $phrase"
        }
    }

    $outputItems = @(Get-ChildItem -LiteralPath (Join-Path (RunPath $relative) "output") -Force)
    if ($outputItems.Count -ne 0) {
        throw "Remaining output became non-empty: $relative"
    }
}

$goalText = [System.IO.File]::ReadAllText($GoalPath)
foreach ($phrase in @(
    "primary substantive audit",
    "confirmation audit",
    "zero concrete template defects",
    "stop immediately",
    "Do not start extra audit cycles"
)) {
    if (-not $goalText.Contains($phrase)) {
        throw "GOAL_PROMPT missing bounded-quality phrase: $phrase"
    }
}

Write-Host "  PASS - deep semantic/V2/duplication/trigger/hook checks retained"
Write-Host "  PASS - zero-defect confirmation remains mandatory"
Write-Host "  PASS - meta-verification/session-log/repeated-convergence loops bounded"

# ---------------------------------------------------------------------------
# CHECKLIST D — prove no experimental evidence/input was corrupted
# ---------------------------------------------------------------------------

Write-Host ""
Write-Host "Checklist D: verify experimental integrity"

foreach ($relative in $Completed) {
    $taskHashNow = Get-Sha256 (Join-Path (RunPath $relative) "TASK.md")
    $outputHashNow = Get-TreeSignature (Join-Path (RunPath $relative) "output")

    if ($taskHashNow -ne $completedTaskHashesBefore[$relative]) {
        throw "Completed TASK.md changed: $relative"
    }
    if ($outputHashNow -ne $completedOutputHashesBefore[$relative]) {
        throw "Completed output changed: $relative"
    }
}

foreach ($candidate in $Candidates) {
    $p1 = Join-Path (RunPath "$candidate\Run-01") "CANDIDATE.md"
    $p2 = Join-Path (RunPath "$candidate\Run-02") "CANDIDATE.md"
    if ((Get-Sha256 $p1) -ne $candidateHashesBefore[$candidate] -or
        (Get-Sha256 $p2) -ne $candidateHashesBefore[$candidate]) {
        throw "CANDIDATE.md changed for ${candidate}."
    }
}

foreach ($relative in $allRuns) {
    if ((Get-TreeSignature (Join-Path (RunPath $relative) "source")) -ne $sourceReference) {
        throw "Source tree changed or diverged at $relative."
    }
}

# Final remaining TASK parity.
$finalTaskHashes = @(
    $Remaining |
    ForEach-Object { Get-Sha256 (Join-Path (RunPath $_) "TASK.md") } |
    Sort-Object -Unique
)
if ($finalTaskHashes.Count -ne 1 -or $finalTaskHashes[0] -ne $newTaskHash) {
    throw "Final remaining TASK parity failed."
}

Assert-File $AmendmentMd
Assert-File $AmendmentJson
Assert-File $oldGoalEvidence
Assert-File $l0TaskEvidence

Write-Host "  PASS - M/Run-01 and L0/Run-01 raw evidence unchanged"
Write-Host "  PASS - all CANDIDATE.md and source inputs unchanged"
Write-Host "  PASS - remaining 8 TASK.md files are byte-identical"
Write-Host "  PASS - remaining 8 outputs are empty"

Write-Host ""
Write-Host "Protocol amendment 5.2.2 applied successfully." -ForegroundColor Green
Write-Host ""
Write-Host "Completed runs preserved:"
Write-Host "  M/Run-01"
Write-Host "  L0/Run-01"
Write-Host ""
Write-Host "Remaining runs now use bounded convergence:"
foreach ($relative in $Remaining) {
    Write-Host "  $relative"
}
Write-Host ""
Write-Host "Old remaining TASK SHA256: $oldRemainingTaskHash"
Write-Host "New remaining TASK SHA256: $newTaskHash"
Write-Host "Old GOAL_PROMPT SHA256:    $oldGoalHash"
Write-Host "New GOAL_PROMPT SHA256:    $newGoalHash"
Write-Host ""
Write-Host "Ready for the next Goal run."
