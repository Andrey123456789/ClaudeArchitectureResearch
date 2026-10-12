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

Iteration 003 was **not executed as a Claude Code run**; it was human-directed methodology work with ChatGPT assistance and manual review/commit. It froze the V2-derived policy oracle (**180 policies**), metric/evidence contract (**59 metrics** after the final pre-candidate amendment), benchmark isolation protocol, benchmark shape, capability framework, recovery accounting, and the E0 mechanics plan.
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

### 2026-10-12 — MILESTONE — Iteration 005 execution started

Ten controlled template-generation workspaces were prepared outside the research repository under `C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\`: two independent generation replicates for each of **M, L0, L1, K0 and K1**. Workspace names encode both execution order and replicate identity (`01-M-R1` … `10-K1-R2`), and **Run 01 / M-R1** was started in a fresh Claude Desktop / Code session using `prompts/005-template-generation.md`; no generated-template result is recorded yet.

---

## Current state

- Baseline: `templates/v2-baseline/`.
- Candidate designs defined: V2 / M / L0 / L1 / K0 / K1.
- Normative oracle frozen: 180 policies.
- Metrics manifest frozen: 59 metrics.
- E0 closed partial: R1 PASS, I1 PASS; R2/S1/S2/A1/T1/W1 remain deferred rather than assumed.
- Research direction: **simplify**, avoid unnecessary harness/methodology expansion, and use Claude Desktop with version verification after every experimental prompt/run.
- Iteration 005 execution is **in progress**: ten controlled external workspaces are prepared for `01-M-R1` through `10-K1-R2`, and Run 01 / M-R1 has started.
- Next checkpoint: complete the 5×2 template-generation set, record the Desktop version after every run, then audit the generated templates before any code generation.
