$ErrorActionPreference = "Stop"

$ExpectedHead = "949d4758396865ae12e2f071ca3ef058d8366091"

function Normalize-Lf([string]$s) {
    return $s.Replace("`r`n", "`n").Replace("`r", "`n")
}

$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Read-Lf([string]$RelativePath) {
    $full = Join-Path $Repo $RelativePath
    if (-not (Test-Path -LiteralPath $full)) {
        throw "Missing expected file: $RelativePath"
    }
    return Normalize-Lf([System.IO.File]::ReadAllText($full))
}

function Write-Lf([string]$RelativePath, [string]$Text) {
    $full = Join-Path $Repo $RelativePath
    $dir = [System.IO.Path]::GetDirectoryName($full)
    if ($dir -and -not (Test-Path -LiteralPath $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
    [System.IO.File]::WriteAllText($full, (Normalize-Lf $Text), $Utf8NoBom)
}

function Replace-Exact([string]$RelativePath, [string]$Old, [string]$New) {
    $text = Read-Lf $RelativePath
    $oldLf = Normalize-Lf $Old
    $newLf = Normalize-Lf $New
    if (-not $text.Contains($oldLf)) {
        throw "Expected text not found in $RelativePath. Repository may not match the intended base."
    }
    $text = $text.Replace($oldLf, $newLf)
    Write-Lf $RelativePath $text
}

function Append-Once([string]$RelativePath, [string]$Marker, [string]$Block) {
    $text = Read-Lf $RelativePath
    if ($text.Contains($Marker)) {
        return
    }
    $text = $text.TrimEnd("`n") + "`n`n" + (Normalize-Lf $Block).TrimStart("`n") + "`n"
    Write-Lf $RelativePath $text
}

$Repo = (git rev-parse --show-toplevel).Trim()
if (-not $Repo) { throw "Run this script inside the ClaudeArchitectureResearch Git repository." }
Set-Location $Repo

$Head = (git rev-parse HEAD).Trim()
if ($Head -ne $ExpectedHead) {
    throw "Unexpected HEAD: $Head`nExpected: $ExpectedHead`nRefresh/rebuild the patch instead of applying it blindly."
}

$Dirty = git status --porcelain
if ($Dirty) {
    throw "Working tree is not clean. Commit/stash local changes before applying this preparation patch."
}

# README: clarify legacy V3 and broaden prompt description.
Replace-Exact "README.md" @'
- `templates/v3` — experimental version.
'@ @'
- `templates/v3` — legacy scaffold from the original single-V3 phase; not an Iteration 005 candidate.
'@

Replace-Exact "README.md" @'
- `prompts/` — prompts used to generate and modify V3.
'@ @'
- `prompts/` — executed and planned prompts for research iterations and candidate generation.
'@

# .gitignore + remove accidentally committed Python bytecode.
$gitignore = Read-Lf ".gitignore"
if (-not $gitignore.Contains("**/__pycache__/")) {
    $gitignore = $gitignore.TrimEnd("`n") + @'

# Python generated files
**/__pycache__/
*.pyc
'@
    Write-Lf ".gitignore" $gitignore
}

$Pycache = Join-Path $Repo "research/e0/probes/harness/__pycache__"
if (Test-Path -LiteralPath $Pycache) {
    Remove-Item -LiteralPath $Pycache -Recurse -Force
}

# Common log: replace wait-for-48h wording with per-run version verification.
Replace-Exact "research/RESEARCH_COMMON_LOG.md" @'
### 2026-10-12 — ENV — Claude Desktop version freeze attempted

Windows Claude Desktop version recorded as **2.26454.2.0** (`Claude_2.26454.2.0_x64__pzs8sxrjxfjjc`). Auto-update policy was applied and the version remained unchanged immediately after restart/check. Treat the freeze as **pending confirmation** until the same version survives normal 24–48 hour observation; once confirmed, use this as the frozen Desktop environment for the shortened experiment.
'@ @'
### 2026-10-12 — ENV — Claude Desktop version controlled per experimental run

Windows Claude Desktop version recorded as **2.26454.2.0** (`Claude_2.26454.2.0_x64__pzs8sxrjxfjjc`) and the auto-update policy was applied. The shortened experiment does not wait for a multi-day freeze observation: after every experimental Claude prompt/run, the installed Desktop version is checked with `Get-AppxPackage -Name Claude | Select-Object Name, Version, PackageFullName`. A changed version makes that run suspect until an explicit repeat/accept decision is made.
'@

Replace-Exact "research/RESEARCH_COMMON_LOG.md" @'
### 2026-10-12 — DECISION — Iteration 005 will separate template generation from code generation.
Five non-baseline candidates will each be generated twice (5×2); V2 remains frozen. The resulting templates will be audited before deciding the next experiment. Further stages remain evidence-driven rather than fixed in advance.
'@ @'
### 2026-10-12 — DECISION — Iteration 004 closed partial after scope reduction

The full E0 behavioral matrix will not be completed before candidate generation. R1 and I1 remain established results; R2, S1, S2, A1, T1 and W1 remain explicitly deferred and will be revisited only if a later surviving candidate or code-generation decision materially depends on them.

### 2026-10-12 — DECISION — Iteration 005 will separate template generation from code generation

Five non-baseline candidates will each be generated twice (5×2); V2 remains frozen. The resulting templates will be audited before deciding the next experiment. Further stages remain evidence-driven rather than fixed in advance.
'@

Replace-Exact "research/RESEARCH_COMMON_LOG.md" @'
- E0 result so far: R1 PASS, I1 PASS; several behavioral mechanics remain unverified.
- Research direction: **simplify**, avoid unnecessary harness/methodology expansion, continue through frozen Claude Desktop when the version freeze is confirmed.
- Next journal entry should record either:
  - confirmation/failure of the Desktop version freeze; or
  - the next consciously simplified experimental step.
'@ @'
- E0 closed partial: R1 PASS, I1 PASS; R2/S1/S2/A1/T1/W1 remain deferred rather than assumed.
- Research direction: **simplify**, avoid unnecessary harness/methodology expansion, and use Claude Desktop with version verification after every experimental prompt/run.
- Next stage: Iteration 005 generates M/L0/L1/K0/K1 twice each, then stops for template audit before any code generation.
'@

# E0 README: close partial and supersede the old mandatory full gate.
Replace-Exact "research/e0/README.md" @'
**ITERATION 004 — PARTIALLY EXECUTED. The gate to candidate generation is NOT passed.**

A fresh headless child of the desktop-bundled Claude Code CLI cannot authenticate (`Not logged in`), so no probe that needs model behavior was executed. Loading and discovery were verified with startup-only runs: fresh processes with no model call, using the harness's own context records as evidence. Details, affected assumptions and open decisions: `research/observations/004-e0-mechanics-validation.md`.
'@ @'
**ITERATION 004 — CLOSED PARTIAL AFTER SCOPE REDUCTION.**

R1 and I1 are established results. R2, S1, S2, A1, T1 and W1 remain explicitly unverified/deferred; they are not treated as PASS. The research scope was reduced on 2026-10-12, so completion of the original headless behavioral matrix is no longer a prerequisite for Iteration 005 template generation. Details and historical evidence remain in `research/observations/004-e0-mechanics-validation.md`.
'@

Replace-Exact "research/e0/README.md" @'
- Next step: sign in the pinned CLI (`claude auth login`), then `python research/e0/probes/harness/e0.py --expect-version 2.1.293 run all`.
'@ @'
- Next step: no full E0 rerun before Iteration 005. A deferred probe is revisited only if a later surviving candidate or code-generation decision materially depends on it.
'@

Replace-Exact "research/e0/README.md" @'
## Exit criterion

Candidate generation is not allowed to rely on an unverified mechanic.

Iteration 004 is complete when each required mechanic is:

- empirically `PASS` / supported as expected; or
- explicitly characterized as unsupported/limited and a consistent candidate-design adaptation is proposed for approval.

Raw failures are retained.
'@ @'
## Historical exit criterion and 2026-10-12 amendment

The original protocol required every listed mechanic to be characterized before candidate generation. That criterion was intentionally superseded when the research was shortened.

Iteration 004 therefore closes **partial**, not PASS:

- R1 and I1 remain established evidence;
- R2, S1, S2, A1, T1 and W1 remain deferred/unverified;
- raw evidence and harness artifacts are retained;
- Iteration 005 may generate templates using controlled workspace isolation;
- no deferred mechanic may later be described as empirically validated unless it is actually tested.

Before code generation, revisit only those deferred mechanics that materially affect the candidates and experiment design that survive the Iteration-005 audit.
'@

# Observation 004: status + closeout.
Replace-Exact "research/observations/004-e0-mechanics-validation.md" @'
| Status | **PARTIAL — gate to candidate generation NOT passed.** R1 and I1 are characterized; S1, S2, A1 and R2 are characterized only on their loading half; T1 is characterized statically; W1 is not executed. |
'@ @'
| Status | **CLOSED PARTIAL AFTER SCOPE REDUCTION.** R1 and I1 remain established; R2, S1, S2, A1, T1 and W1 remain explicitly deferred/unverified. |
'@

Replace-Exact "research/observations/004-e0-mechanics-validation.md" @'
## 10. Gate to the next iteration

Iteration 004 is **not complete**. Candidate generation must not rely on:
- path-triggered must-rules (R2);
- description-triggered skills (S1);
- reachability of skill references (S2);
- `skills:` preload (A1);
- telemetry values (T1);
- workspace isolation (W1).

**Next step (top-level, outside any Claude session):**

```bash
"C:/Users/atonkonog/AppData/Roaming/Claude/claude-code/2.1.293/83cb0bd7fed4/claude.exe" auth login
python research/e0/probes/harness/e0.py --expect-version 2.1.293 preflight
python research/e0/probes/harness/e0.py --expect-version 2.1.293 run all
python research/e0/probes/harness/e0.py summarize
```

`run all` runs 23 fresh sessions (21 behavioral run definitions; `S1-pos` repeats 3 times) on `claude-opus-5-5` at effort `xhigh`, with a $3 per-run budget cap. `W1-bypass` runs one session with `bypassPermissions`; its prompt touches only the generated canaries. Alternatively, run `auth login` and then ask Claude to continue Iteration 004: the harness strips parent-session variables, so it also works from inside a Claude session.

After the run:
1. interpret `summary.json`;
2. complete §5.3–§5.8;
3. take decisions D-E0-1…D-E0-6;
4. only then freeze benchmark scenarios and generate candidates.
'@ @'
## 10. Closeout after research-scope reduction — 2026-10-12

The original E0 plan required the full behavioral matrix before candidate generation. The project subsequently adopted a shorter, adaptive experiment so that methodology work would not dominate the research itself.

Iteration 004 therefore closes **partial**, not PASS.

Established evidence remains unchanged:

- **R1 PASS** — nested `.claude/rules/**` discovery works to the tested depth;
- **I1 PASS** — direct and nested `CLAUDE.md` imports work in the tested shape.

The following remain explicitly **deferred/unverified**:

- R2 — path-scoped behavior on Read/Edit/new Write;
- S1 — description-triggered skill invocation;
- S2 — reachability of skill-private references;
- A1 — `skills:` preload into a spawned subagent;
- T1 — behavioral telemetry values/cross-checks;
- W1 — launch-root access boundary.

No deferred item is converted to PASS by this closeout.

Iteration 005 may proceed to **template generation only** using controlled allowlisted workspaces. Because W1 was not proven, this is described as controlled workspace isolation rather than a verified security sandbox.

Before later code generation, a deferred E0 probe should be revisited only if the candidates and experiment design that survive the Iteration-005 audit materially depend on that mechanic.
'@

# Benchmark plan: preserve old plan, but supersede mandatory sequencing.
Replace-Exact "research/benchmark/plan.md" @'
**Protocol accepted at Iteration 003 close.**

This file freezes the benchmark shape before E0 results and before candidate generation.
Exact task wording, starting fixtures, response scripts, and hidden Scenario Oracles are still to be authored and frozen in a dedicated pre-candidate iteration. Candidate-construction Claude must not see those hidden benchmark materials.
'@ @'
**Protocol accepted at Iteration 003 close.**

### Sequencing amendment — 2026-10-12

The scenario definitions below are retained as the original benchmark design and as a menu for later code-generation experiments, but the mandatory sequencing was intentionally shortened before any M/L/K runtime template or benchmark result existed.

Iteration 005 now generates and audits the five non-baseline candidate templates twice each **before** deciding the scope of code-generation benchmarking. Exact TaskBoard scenarios, fixtures, response scripts and hidden oracles therefore no longer have to be frozen before template generation.

The information boundary is unchanged: candidate-construction Claude must not see benchmark tasks, hidden oracles, metrics, prior results or competing-candidate results. Any later code-generation benchmark must freeze its own inputs before those benchmark runs begin.

The next experiment after Iteration 005 is evidence-driven rather than precommitted.

---

This file originally froze the benchmark shape before E0 results and before candidate generation.
'@

# Isolation protocol: Phase A remains, add explicit 005 controlled-workspace note.
Replace-Exact "research/benchmark/isolation-protocol.md" @'
Run candidate construction in a temporary allowlisted workspace rather than exposing the whole research repository.
'@ @'
Run candidate construction in a temporary allowlisted workspace rather than exposing the whole research repository.

**Iteration 005 note (2026-10-12).** This Phase-A rule remains active for the shortened 5×2 template-generation experiment. Because E0-W1 did not prove the Desktop launch root to be a hard sandbox, call this **controlled workspace isolation**, not a verified security boundary. Each run uses a fresh neutral workspace containing only the explicit construction allowlist and no prior generation output.
'@

# Observation 003: append a transparent sequencing amendment without rewriting history.
Append-Once "research/observations/003-pre-generation-foundation.md" "## Adaptive sequencing amendment — 2026-10-12" @'
## Adaptive sequencing amendment — 2026-10-12

The pre-candidate ordering above records the protocol as accepted at Iteration 003 close. Before any M/L/K runtime template or benchmark result existed, the project deliberately shortened the research plan.

The revised sequence permits Iteration 005 to generate and audit candidate **templates** before detailed TaskBoard scenarios/oracles are frozen. Template generation remains isolated from metrics, benchmark tasks, hidden oracles and prior results.

This amendment does not alter the frozen 180-policy oracle or the existing metrics definitions. It changes which parts of the methodology are mandatory for the next step. Code-generation experiments are selected and frozen only after the Iteration-005 template audit.
'@

# New Iteration 005 files.
$Prompt005 = @'
# 005 — Generate one candidate runtime template

## Goal

Generate a **complete, standalone runtime instruction template** for the single assigned candidate in this isolated workspace.

This iteration is **template generation only**. Do not generate TaskBoard or any other application code, do not run a benchmark, and do not compare candidates.

## Assigned candidate

Read `ASSIGNED_CANDIDATE.txt` first.

It must contain exactly one candidate ID:

- `M`
- `L0`
- `L1`
- `K0`
- `K1`

If the file is missing or contains anything else, stop and report the problem. Do not guess the candidate.

## Required inputs

Read the relevant inputs before constructing the template.

Shared inputs:

1. `research/observations/001-v3-design-proposal.md`
2. `research/observations/002-candidate-space-analysis.md`
3. `research/policy/inventory.json`
4. `research/candidates/<assigned>/CORE_FEATURES.md`
5. `research/candidates/<assigned>/DESIGN.md`
6. the complete `templates/v2-baseline/` tree

Additional inputs:

- for `L1`, read `research/candidates/L0/DESIGN.md` before `research/candidates/L1/DESIGN.md`;
- for `K1`, read `research/candidates/K0/DESIGN.md` before `research/candidates/K1/DESIGN.md`;
- for `L1` and `K1`, also read `research/capabilities/capability-framework.md`.

The workspace is intentionally allowlisted. Missing benchmark, metrics, other-candidate, TaskBoard, result, or oracle material is intentional.

Do **not** inspect files outside the workspace root. Do not use the network or external repositories to recover excluded material.

## Established E0 mechanics

You may rely on these established Iteration-004 facts:

- nested directories under `.claude/rules/` are discovered recursively to at least two levels;
- direct and nested `@` imports work;
- a rule file explicitly loaded through `@` is effectively always-loaded; a `paths:` field on that imported copy does not make it conditional.

Do not treat unresolved E0 probes as established facts. Do not redesign the candidate merely to make an unresolved mechanic look proven.

## Construction rules

1. **V2 is the behavioral baseline, not the target layout.**
   Preserve the accepted normative intent represented by `research/policy/inventory.json`.

2. **The inventory is the normative oracle.**
   Do not independently strengthen, weaken, add, or remove policy. Organizational rewrites and technology-neutral wording are allowed only where the assigned candidate design requires them.

3. **The assigned design controls structure.**
   Implement the candidate described by its `DESIGN.md`, `CORE_FEATURES.md`, and the shared invariants/predicates in Iteration 002. Do not drift toward another candidate because it seems cleaner.

4. **Illustrative trees are not literal file-generation scripts.**
   Use engineering judgment where the design explicitly leaves implementation freedom, but choose the smallest solution that satisfies the assigned candidate.

5. **One normative owner.**
   Avoid semantic duplication of policy. Pointers, routing text, summaries that contain no independent normative content, and deterministic checks are allowed where the design permits them.

6. **No research metadata in the runtime template.**
   The generated template must not contain candidate labels (`M`, `L0`, `L1`, `K0`, `K1`) as research labels, experiment commentary, metric definitions, benchmark material, policy-inventory IDs used only for research bookkeeping, or references to the research repository.

7. **No product implementation.**
   `SPECIFICATION.md` and other input placeholders may exist as template artifacts, but do not fill them with TaskBoard or another concrete application.

8. **Do not modify inputs.**
   Write only under `output/`.

9. **Fresh-output requirement.**
   `output/` must be empty or absent at the start. If it already contains a prior generated template or report, stop rather than overwrite or learn from it.

10. **No candidate comparison or winner selection.**
    Generate the assigned template only. Do not score it against V2 or other candidates.

11. **Do not commit or push.**

## Deliverables

Create:

### `output/template/`

A complete standalone template ready to be copied into a future code-generation workspace. It must include all runtime instruction/configuration/reference/enforcement artifacts required by the assigned candidate.

It must not require the research repository to function.

### `output/GENERATION_REPORT.md`

Keep this concise. Record:

- assigned candidate;
- total generated runtime file count;
- major structural choices where the design allowed more than one valid implementation;
- any candidate-design ambiguity and the minimal interpretation chosen;
- any policy-preservation concern or unresolved item;
- any intentionally permitted wording/placement delta that is important for later audit;
- whether the final self-check found any broken internal references or known missing required artifact.

Do not include a quality score or comparison with another candidate.

## Final self-check

Before finishing:

1. verify that `output/template/` is standalone and contains no research-only files;
2. check the output against the assigned candidate's distinguishing predicates and shared invariants;
3. check that accepted V2 policy intent from `inventory.json` has not been silently lost or materially changed;
4. check internal file references/imports for broken paths;
5. check for accidental normative duplication;
6. check that no concrete application code or benchmark material was generated;
7. correct clear construction defects you find;
8. leave unresolved design ambiguities documented in `GENERATION_REPORT.md` rather than silently inventing a new architecture.

If a genuinely required input is missing and the candidate cannot be generated without inventing research material, stop and report the missing input rather than fabricating it.
'@
Write-Lf "prompts/005-template-generation.md" $Prompt005

$Obs005 = @'
# 005 — Candidate template generation

| | |
|---|---|
| Status | **PLANNED / READY TO EXECUTE** |
| Scope | Template generation only; no application/code generation |
| Subjects | M, L0, L1, K0, K1 |
| Repetitions | 2 independent generations per candidate (5×2 = 10 runs) |
| Baseline | V2 remains frozen and is **not regenerated** |
| Prompt | `prompts/005-template-generation.md` |
| Execution surface | Claude Desktop / Code tab |
| Intended Desktop version | `2.26454.2.0` |
| Model | Claude Opus 5.5 |
| Effort | `xhigh` |
| Decision after 005 | Evidence-driven; not precommitted |

## Purpose

Iteration 005 answers a narrower question than the future code-generation experiment:

> Given the same frozen V2 policy corpus and one candidate design, what concrete runtime template does Claude construct, and how reproducible is that construction across two independent runs?

Template generation and code generation are deliberately separated. After all ten templates are generated, they are audited before any decision about the next experiment.

## Run order

Use two rounds rather than generating each pair back-to-back.

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

Do not eliminate a candidate between its first and second generation merely because the first output looks weak. Iteration 005 is the planned 5×2 generation set. A run may be stopped only for a genuine technical/input failure, which must be recorded.

## Desktop version control

The experiment does not wait for a multi-day freeze observation.

After **every** experimental Claude prompt/run, execute:

```powershell
Get-AppxPackage -Name Claude | Select-Object Name, Version, PackageFullName
```

Expected Desktop version:

```text
2.26454.2.0
```

Record the observed version in the run table.

If the version changes, mark that run `VERSION_CHANGED / SUSPECT`. Do not silently mix it with the other runs; decide explicitly whether it must be repeated before comparative audit.

## Fresh-session rule

Each run uses:

- a fresh Claude Desktop Code session;
- a fresh isolated workspace;
- the same prompt file;
- the same model and effort;
- an empty `output/` directory;
- no prior run output in the workspace.

Avoid corrective/follow-up prompts during construction. If Claude can resolve a non-material ambiguity with the prompt's "smallest compliant interpretation" rule, let it do so and record it in the report. If a required input is genuinely missing, preserve the failure instead of coaching the run into success.

## Controlled workspace isolation

Iteration 005 uses **controlled workspace isolation**, not a claimed security boundary. E0-W1 did not prove that the Desktop root is a hard sandbox.

Use neutral roots such as:

```text
C:\ResearchRuns\005\run-01\
...
C:\ResearchRuns\005\run-10\
```

The Code-tab root for a run is that run directory, not the full research repository.

### Shared allowlist for every run

Copy only:

```text
ASSIGNED_CANDIDATE.txt
prompts/005-template-generation.md

templates/v2-baseline/**

research/observations/001-v3-design-proposal.md
research/observations/002-candidate-space-analysis.md
research/policy/inventory.json

research/candidates/<assigned>/DESIGN.md
research/candidates/<assigned>/CORE_FEATURES.md
```

`ASSIGNED_CANDIDATE.txt` contains only one line: `M`, `L0`, `L1`, `K0`, or `K1`.

Additional allowed inputs:

```text
L1:
  research/candidates/L0/DESIGN.md
  research/capabilities/capability-framework.md

K1:
  research/candidates/K0/DESIGN.md
  research/capabilities/capability-framework.md
```

Do **not** copy:

```text
research/metrics/**
research/benchmark/**
research/e0/**
other candidate DESIGN/CORE_FEATURES files
TaskBoard specifications or fixtures
hidden oracles / acceptance criteria
prior generation outputs or reports
candidate rankings / comparisons
.git history from the research repository
```

The prompt also instructs Claude not to inspect outside the workspace root. This is an experimental-control rule, not proof of filesystem sandboxing.

## Output collection

During the ten runs, keep each run's output only in its own isolated workspace.

After all ten runs are finished, collect for audit under:

```text
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
```

Only the contents of each `template/` directory are runtime candidate artifacts. `GENERATION_REPORT.md` remains research evidence and must not later be copied into a code-generation benchmark workspace.

## Audit after generation

Stop after all ten template generations. Do not generate TaskBoard yet.

The post-generation audit will examine, at minimum:

1. structural conformance to the assigned candidate;
2. preservation of the frozen normative policy corpus;
3. accidental semantic duplication or added policy;
4. broken references / unusable runtime structure;
5. within-candidate consistency between run 1 and run 2;
6. meaningful convergence or divergence between candidate architectures.

The next experiment is chosen **after** this audit. It is intentionally not fixed in advance.

## Relation to Iteration 004

Iteration 004 is closed as a partial mechanics study after the scope reduction.

Established results remain evidence:

- R1 — nested `.claude/rules/**` discovery: PASS;
- I1 — direct/nested `CLAUDE.md` imports: PASS.

R2, S1, S2, A1, T1 and W1 remain explicitly unverified/deferred. They are not silently treated as PASS. A deferred probe should be revisited only if a later surviving candidate or code-generation decision materially depends on it.
'@
Write-Lf "research/observations/005-template-generation.md" $Obs005

Write-Host ""
Write-Host "Iteration 005 preparation applied."
Write-Host "Review with:"
Write-Host "  git status --short"
Write-Host "  git diff --check"
Write-Host "  git diff --stat"
Write-Host ""
Write-Host "No commit was created."
