# 005 — Candidate template generation

| | |
|---|---|
| Status | **PLANNED / READY TO EXECUTE** |
| Scope | Template generation only; no application/code generation |
| Subjects | M, L0, L1, K0, K1 |
| Replicates | 2 independent generation replicates per candidate (5×2 = 10 runs) |
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

Template generation and code generation are deliberately separated. The two generations of each candidate are **replicates of the same candidate definition, not separate candidate variants**. After all ten raw generation results are audited, at most one canonical runtime template per candidate architecture is carried forward to any later code-generation experiment.

## Run order

Use two rounds rather than generating each pair back-to-back.

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

Do not eliminate a candidate between its first and second replicate merely because the first output looks weak. Iteration 005 is the planned 5×2 generation set. Replicate 1 and replicate 2 use the same candidate specification; neither is a preferred variant. A run may be stopped only for a genuine technical/input failure, which must be recorded.

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
```

Only the contents of each `template/` directory are runtime candidate artifacts. `GENERATION_REPORT.md` remains research evidence and must not later be copied into a code-generation benchmark workspace.

## Audit after generation

Stop after all ten template generations. Do not generate TaskBoard yet.

The post-generation audit will examine, at minimum:

1. structural conformance to the assigned candidate;
2. preservation of the frozen normative policy corpus;
3. accidental semantic duplication or added policy;
4. broken references / unusable runtime structure;
5. within-candidate consistency between replicate 1 and replicate 2;
6. meaningful convergence or divergence between candidate architectures.

The replicate outputs remain research evidence. After the audit, at most one canonical runtime template per candidate architecture is selected or derived for any later code-generation stage; the experiment does not carry ten competing runtime candidates forward.

The next experiment is chosen **after** this audit. It is intentionally not fixed in advance.

## Relation to Iteration 004

Iteration 004 is closed as a partial mechanics study after the scope reduction.

Established results remain evidence:

- R1 — nested `.claude/rules/**` discovery: PASS;
- I1 — direct/nested `CLAUDE.md` imports: PASS.

R2, S1, S2, A1, T1 and W1 remain explicitly unverified/deferred. They are not silently treated as PASS. A deferred probe should be revisited only if a later surviving candidate or code-generation decision materially depends on it.