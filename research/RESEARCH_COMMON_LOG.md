# Research Log

> Intended repository path: `research/RESEARCH_COMMON_LOG.md`

## Purpose

A concise, append-only chronology of the research. This file is the **human-readable spine** of the project: what was tried, what was learned, and what decision changed the next step.

Detailed evidence belongs in `research/observations/`, benchmark artifacts, prompts, commits, and raw results. This log should stay short.

### Entry rule

Add an entry only when at least one of these happens:

- an experiment produces a material result;
- a design/research decision changes the plan;
- a previously assumed fact is disproved;
- the frozen environment/protocol changes;
- an iteration starts, closes, or is explicitly abandoned.

Prefer 1–3 concise sentences. Link to the detailed artifact instead of copying it.

Labels:

- **MILESTONE** — project/iteration transition;
- **RESULT** — empirical or benchmark finding;
- **DECISION** — human research/design decision;
- **ENV** — frozen execution environment;
- **CORRECTION** — correction to an earlier entry or assumption.

---

## Pre-repository history

These entries reconstruct the work that preceded `ClaudeArchitectureResearch`. They come from the original V1/V2 TaskBoard experiments and research notes, not from commits in this repository.

### 2026-09-20 — MILESTONE — CleanArchitectureTemplate V1 ready

CleanArchitectureTemplate V1 was committed/pushed and treated as the first usable prototype. The next experiment was defined as two TaskBoard implementations from the same starting point: **Goal** (one-shot goal-driven generation) versus **Step** (incremental prompting).

### 2026-09-21 — RESULT — TaskBoard Goal V1 exposed over-engineering

Goal V1 completed a working implementation in roughly **1h06** including SDK installation; the Step run reached only the foundation in roughly **25 min**, while the shared 5-hour token allowance was already heavily consumed. More importantly, Goal V1 chose a behavior-rich / Rich Domain Model approach for a comparatively simple CRUD/workflow domain, which was judged unnecessarily complex for the intended template.

### 2026-09-21 — DECISION — Freeze Goal V1 as diagnostic evidence

Do not “repair” Goal V1 in place. Preserve it as evidence of what V1 instructions naturally produced, audit the failure modes, improve the template, and then rerun from a clean start. The Step V1 branch was not considered valuable enough to finish before correcting the template.

### 2026-09-28 — RESULT — TaskBoard Goal V2 materially improved architecture

TaskBoard-Goal-V2 kept the non-trivial task state workflow (`Created → InProgress → Completed → Closed`) but moved workflow/use-case logic into Application while keeping Domain simple. The architectural approval gate also worked: Claude asked before inventing product-significant text limits instead of silently choosing them.

### 2026-09-28 — RESULT — V2 verification and remaining gaps

The V2 run completed broad verification (52 Application tests, 110 integration tests, 28 frontend tests, plus runtime checks). Remaining template gaps were identified around test readability, organization/naming of supporting types, and unspecified string/case-sensitivity semantics; those rules were subsequently tightened in the template.

### 2026-09-29 — DECISION — Move from “fix V2” to instruction-architecture research

The research question expanded from improving individual rules to comparing **instruction architectures**: modularity, Stable Dependencies, separation of concerns, single normative ownership, selective/reliable loading, decision control, policy vs enforcement, and maintainability. V2 became the baseline rather than the target to keep patching.

---

## ClaudeArchitectureResearch repository

### 2026-09-30 — MILESTONE — Research repository initialized

Repository created with a frozen `templates/v2-baseline/` and an initially identical `templates/v3/`.
Initial commit: `0da9ed908b1494504c5bf7a91c670b31dc6f5027`.

### 2026-09-30 — RESULT — Iteration 001: V2 analyzed before redesign

`prompts/001-v3-design-goal.md` was executed in Claude Code. Claude read the V2 corpus and produced `research/observations/001-v3-design-proposal.md` without changing the template. Core diagnosis: **V2 has strong content but weak structure**—critical policy can hide behind uncertain triggers, duplication compensates for loading uncertainty, decisions lack a single register, and deterministic enforcement is largely absent.
Commit: `6f2f816e039c87b432a3d712f95a1c9544bc909b`.

### 2026-10-02 — RESULT — Iteration 002: six candidate architectures defined

Instead of prematurely selecting the Iteration-001 proposal, the experiment retained six candidates: **V2, M, L0, L1, K0, K1**. This separates two main axes: decomposition strategy (Minimal / Stability-first / Kinds×Scopes) and embedded vs replaceable capabilities.
Detailed artifact: `research/observations/002-candidate-space-analysis.md`.
Commit: `03243d080ad31b37073db6c4b6ecd5ae177e0d6a`.

### 2026-10-06…07 — MILESTONE — Iteration 003: methodology/foundation frozen

Iteration 003 was **not executed as a Claude Code run**; it was human-directed methodology work with ChatGPT assistance and manual review/commit. It froze the V2-derived policy oracle, metric/evidence contract (**59 metrics** after the final pre-candidate amendment), benchmark isolation protocol, benchmark shape, capability framework, recovery accounting, and the E0 mechanics plan.
Detailed artifact: `research/observations/003-pre-generation-foundation.md`.
Final foundation commit: `a9e83fec5f462b23863f0e17e86028636040cf81`.

### 2026-10-08 — RESULT — Iteration 004.1: E0 mechanics harness built; execution partial

Claude built a reproducible E0 harness with tiny fixtures and raw evidence capture. Empirically established without a model call: nested `.claude/rules/**` discovery works (**R1 PASS**) and direct/nested `CLAUDE.md` imports work (**I1 PASS**). Path-scoped loading, skill triggering, private references, subagent preload, telemetry values, and root-boundary behavior remained incomplete because fresh child CLI processes were not authenticated.
Detailed artifact: `research/observations/004-e0-mechanics-validation.md`.
Commit: `776cb92803cf3e8706bf20e76ffea51e1c4995f7`.

### 2026-10-08 — RESULT — Desktop/CLI environment is not stable by default

During E0, Claude Desktop silently changed its bundled Claude Code from **2.1.289 to 2.1.293** after restart. This proved that version parity must be explicitly controlled if the experiment spans multiple days/sessions.

### 2026-10-12 — DECISION — Simplify the remaining experiment and stay on Claude Desktop

The research scope was intentionally reduced to avoid turning the methodology itself into the project. The chosen execution surface for the remaining practical experiment is **Claude Desktop / Code tab**, rather than rebuilding the study around authenticated headless CLI runs.

### 2026-10-12 — ENV — Claude Desktop version controlled per experimental run

Windows Claude Desktop version recorded as **2.26454.2.0** (`Claude_2.26454.2.0_x64__pzs8sxrjxfjjc`) and the auto-update policy was applied. The shortened experiment does not wait for a multi-day freeze observation: after every experimental Claude prompt/run, the installed Desktop version is checked with `Get-AppxPackage -Name Claude | Select-Object Name, Version, PackageFullName`. A changed version makes that run suspect until an explicit repeat/accept decision is made.

### 2026-10-12 — DECISION — Iteration 004 closed partial after scope reduction

The full E0 behavioral matrix will not be completed before candidate generation. R1 and I1 remain established results; R2, S1, S2, A1, T1 and W1 remain explicitly deferred and will be revisited only if a later surviving candidate or code-generation decision materially depends on them.

### 2026-10-12 — DECISION — Iteration 005 will separate template generation from code generation

Five non-baseline candidates will each be generated twice (5×2); V2 remains frozen. The two generations are independent replicates of the same candidate definition, not separate candidate variants. The resulting templates will be audited before deciding the next experiment; further stages remain evidence-driven rather than fixed in advance.

### 2026-10-12 — MILESTONE — Initial Iteration 005 execution started

Ten controlled template-generation workspaces were initially prepared outside the research repository under `C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\`, using numbered workspace names such as `01-M-R1` and `06-M-R2`. This execution layout was later superseded by the clean Iteration-005 restart described below.

### 2026-10-13 — CORRECTION — Early Iteration 005 attempts annulled

Two early Iteration-005 attempts were explicitly annulled and are **not experimental evidence** for the final 5×2 series. One M generation used an automated/opaque workflow that did not satisfy the experiment's human-inspectability requirement; a subsequent restarted M attempt was stopped after technical Markdown was generated in Russian, violating the English-only technical-artifact requirement.

Outputs from those attempts must not be used as replicates, recovery inputs, baselines, candidate-quality results, or comparative evidence.

### 2026-10-13 — DECISION — Iteration 005 rebuilt as a clean human-readable 5×2 experiment

The temporary workspace structure was simplified to:

```text
005/
├── M/
│   ├── Run-01/
│   └── Run-02/
├── L0/
│   ├── Run-01/
│   └── Run-02/
├── L1/
│   ├── Run-01/
│   └── Run-02/
├── K0/
│   ├── Run-01/
│   └── Run-02/
└── K1/
    ├── Run-01/
    └── Run-02/
```

Each run receives only `TASK.md`, `CANDIDATE.md`, the common `source/` corpus, and an initially empty `output/`. `TASK.md` is identical across all candidates, `CANDIDATE.md` is identical within each candidate pair, and the common source corpus is identical across all ten runs. `ASSIGNED_CANDIDATE.txt` was removed.

### 2026-10-13 — ENV — Clean Iteration 005 package validated

The restarted 5×2 package passed pre-run validation: all ten workspaces were present, outputs were empty, common inputs matched, and the normalized policy inventory contained **194/194 policies**. The common source corpus includes the frozen V2 baseline, `inventory.json`, and the separate `shared-research-invariants.json`.

This supersedes the earlier **180-policy** count recorded during the pre-generation foundation stage; **194 policies** is the current frozen inventory used by Iteration 005.

### 2026-10-13 — DECISION — Shared construction contract separated from candidate design

Iteration 005 now distinguishes three roles explicitly: `inventory.json` defines the accepted V2-derived policy semantics that must survive; shared research constraints apply equally to all candidates through the common construction contract / `shared-research-invariants.json`; and `CANDIDATE.md` controls only the candidate-specific organization, ownership, dependency, loading, and composition model.

This prevents candidate generation from treating research-wide controls as candidate-specific architectural choices.

### 2026-10-14 — RESULT — First clean Iteration 005 generation results produced

Clean raw generations were completed for **M Run-01**, **L0 Run-01**, and **M Run-02**. Each run remained an independent construction replicate and its raw output was preserved without manual repair before audit.

The execution order temporarily deviated from the nominal round-by-round sequence because of available Claude usage quota; the runs remained fresh-session executions with isolated workspaces and identical candidate-independent inputs.

### 2026-10-14 — RESULT — M replicates exposed a shared trigger-preservation defect

Audit of the two clean M generations found that both changed the frozen `trigger_class` assignment of inventory policies: **M Run-01 changed 20 policies and M Run-02 changed 17**. Because `trigger_class` determines when a policy becomes available to the runtime model, this is not merely a file-placement difference: it changes the loading profile being compared across candidate architectures.

The result demonstrated that preserving policy semantics alone is insufficient for this experiment; trigger assignment is part of the controlled input and must remain invariant across candidates.

### 2026-10-14 — RESULT — M audit found additional construction defects

Both M replicates also kept substantial multi-step `Development Workflow` procedure in always-loaded `CLAUDE.md` instead of separating procedure into a workflow skill. Their generated hooks additionally used command forms whose environment-variable expansion is potentially unsafe on the Windows execution platform, so nominal deterministic enforcement may not actually execute as intended.

M Run-01 also violated the intended workspace boundary during construction by writing temporary material outside its allowed output area and observing a sibling run-directory name. No sibling output was established as having been read, but the event confirmed that the workspace rule must be treated as an experimental control rather than assumed filesystem sandboxing.

The approximately **5.3k-token** always-loaded M surface was slightly above the roughly **5k** design target, but this was treated as a secondary optimization issue rather than a validity failure.

### 2026-10-14 — DECISION — Do not advance the current M pair to code generation

Neither current M replicate will be promoted to downstream code-generation testing. **M Run-02 is structurally preferable to M Run-01**, but selecting it would still carry forward a generation that violated the controlled trigger assignment.

The two current M outputs remain useful **diagnostic evidence**, but they are not accepted as the final comparative M replicate pair.

### 2026-10-14 — DECISION — Strengthen the shared task and regenerate M

The corrective action must be made in the **shared Iteration-005 construction contract**, not as an M-specific hint. At minimum, the task must make the following controls unambiguous for every candidate:

- preserve every inventory policy's `trigger_class`;
- keep normative policy, multi-step procedure, technique, product input, and deterministic enforcement separated by responsibility;
- use Windows-compatible hook/enforcement invocation;
- obey the workspace/output boundary strictly and do not inspect sibling runs or parent-workspace material;
- preserve reliable loading without solving it by moving conditional material into the always-loaded surface.

After the common contract is corrected, **both M Run-01 and M Run-02 are to be regenerated from clean workspaces**. This is cheaper and methodologically safer than carrying the flawed M pair into application/code-generation testing and discovering the comparability problem later.

---

## Current state

- Baseline: `templates/v2-baseline/`.
- Candidate designs: **V2 / M / L0 / L1 / K0 / K1**.
- Current frozen V2-derived policy inventory: **194 policies**.
- Metrics manifest: **59 metrics**.
- Shared research-added constraints are separated from the V2-derived policy oracle.
- E0 is closed partial: **R1 PASS, I1 PASS**; R2/S1/S2/A1/T1/W1 remain deferred rather than assumed.
- Remaining experimental execution uses **Claude Desktop / Code tab** with version verification after experimental runs.
- Iteration 005 uses a clean human-readable **5 candidates × 2 independent replicates** structure: `M/L0/L1/K0/K1 × Run-01/Run-02`.
- Early opaque/Russian-output Iteration-005 attempts are annulled and are not experimental evidence.
- Clean raw generations have been produced for **M Run-01, L0 Run-01, and M Run-02**.
- Audit of the current M pair found material construction/control violations, most importantly `trigger_class` drift (**20 policies in Run-01; 17 in Run-02**).
- The current M pair is retained as diagnostic evidence but **will not advance to code generation or serve as the final comparative M pair**.
- Immediate next step: strengthen the **shared** `TASK.md` controls, then regenerate **both M replicates** from clean workspaces.
- After M is clean, continue/complete candidate generation and comparative audit before deciding which architectures, if any, advance to code-generation benchmarks.