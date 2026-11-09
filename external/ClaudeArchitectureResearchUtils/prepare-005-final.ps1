[CmdletBinding()]
param(
    [string]$RepoRoot = "C:\Projects\AI Learning\ClaudeArchitectureResearch",
    [string]$DestinationRoot = "C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005",
    [ValidateSet("Archive", "Fail", "Delete")]
    [string]$ExistingDestination = "Archive"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = [System.IO.Path]::GetFullPath($RepoRoot)
$DestinationRoot = [System.IO.Path]::GetFullPath($DestinationRoot)
$DestinationParent = Split-Path -Parent $DestinationRoot
$ArchiveRoot = Join-Path $DestinationParent "005-aborted"
$StagingRoot = Join-Path $DestinationParent ("005.__staging__." + [Guid]::NewGuid().ToString("N"))

$TaskContent = @'
# Task: generate one runtime instruction template

## Goal

Generate a complete, standalone runtime instruction template that implements the architecture defined in `CANDIDATE.md`.

This iteration is template generation only.

Do not generate application code, run a benchmark, compare candidates, or select a winner.

## Language requirement

All programming-related and AI-instruction artifacts must be written in English.

This includes generated Markdown, Claude / AI instruction files, code, code comments, configuration files, scripts, technical documentation, and `GENERATION_REPORT.md`.

Do not generate Russian text in technical artifacts.

The only allowed exception is explicit end-user UI text when a product specification requires a non-English UI. No such requirement exists in this task.

## Required inputs

Read completely:

1. `CANDIDATE.md`;
2. `source/inventory.json`;
3. `source/shared-research-invariants.json`;
4. the entire `source/v2-baseline/` tree.

Use the inputs as follows:

- `source/inventory.json` is the normalized V2 policy oracle. Preserve its accepted policy semantics.
- `source/shared-research-invariants.json` contains experiment-wide construction constraints that apply equally to every candidate.
- `CANDIDATE.md` defines the candidate's organization, dependency model, ownership model, and distinguishing constraints.
- `source/v2-baseline/` is the concrete behavioral/content baseline and the source of useful wording, examples, workflows, and technique.

The V2 layout is not a constraint when `CANDIDATE.md` requires another layout.

## Workspace boundary

Work only inside the current run workspace.

Do not read files above the workspace root, use the network, inspect another run, or recover excluded benchmark/metrics/research material.

Write only under `output/`.

`output/` must be empty at the start. If it is not empty, stop and report the problem.

## Construction requirements

- Preserve the semantics of all applicable V2 policies from `source/inventory.json`.
- Preserve the shared construction constraints from `source/shared-research-invariants.json`.
- Follow every binding rule in `CANDIDATE.md`.
- Keep exactly one authoritative normative owner for each policy. Pointers and check-by-reference items may route to the owner, but must not create a second independent restatement.
- Keep procedures, normative policy, technique/examples, product inputs, and deterministic enforcement separated when they have different responsibilities.
- Use reliable loading for critical policy; do not hide a critical must-rule only in model-invoked/private material.
- Preserve useful V2 detail unless it conflicts with the candidate architecture or creates duplication.
- Do not add, weaken, strengthen, or remove normative policy merely because another design seems preferable.
- Do not expose research labels, experiment commentary, policy IDs used only for research bookkeeping, benchmark material, metrics, or references to this run workspace inside the runtime template.
- Do not modify source inputs.
- Do not commit or push.

When several implementations are equally compliant, choose the simplest one that remains reliable and understandable to a human maintainer.

## Deliverables

Create only:

```text
output/
├── template/
└── GENERATION_REPORT.md
```

### `output/template/`

A complete standalone runtime instruction template.

It must work after being copied into a future project without access to `TASK.md`, `CANDIDATE.md`, `source/`, or this research workspace.

### `output/GENERATION_REPORT.md`

Keep it concise and in English.

Record:

- implemented candidate model;
- total runtime file count;
- final tree;
- meaningful structural choices where `CANDIDATE.md` allowed freedom;
- policy-preservation concerns, if any;
- intentionally permitted wording/placement deltas;
- unresolved ambiguity, if any;
- broken references found/fixed;
- final self-check result.

Do not assign a quality score and do not compare against another candidate.

## Final self-check

Before finishing, verify that:

1. the template is standalone;
2. accepted V2 policy semantics are preserved;
3. shared construction constraints are preserved;
4. the structure satisfies `CANDIDATE.md`;
5. there is no accidental semantic duplication;
6. all internal imports/references resolve;
7. critical must-rules are not hidden only in unreliable/on-demand locations;
8. no application or benchmark implementation was generated;
9. runtime artifacts contain no research-only metadata;
10. output does not depend on files outside `output/template/`;
11. the structure remains reasonably navigable for a human;
12. all technical/programming-related output is in English.

Fix clear construction defects before completion.

If a genuinely required source is missing and proceeding would require inventing research material, stop and report the missing input instead of fabricating it.
'@
$ReadmeContent = @'
# Iteration 005 — clean final restart

This directory is the clean 5×2 template-generation series.

The previous mixed/aborted Iteration-005 directory is archived outside this directory and is not experimental evidence for this series.

## Run structure

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

Every run contains only:

```text
Run-XX/
├── TASK.md
├── CANDIDATE.md
├── source/
│   ├── inventory.json
│   ├── shared-research-invariants.json
│   └── v2-baseline/
└── output/
```

There is no `ASSIGNED_CANDIDATE.txt`.

`TASK.md` is byte-identical across all ten runs.
`CANDIDATE.md` is byte-identical inside each candidate pair.
All `source/` inputs are byte-identical across all ten runs.

## Execution order

Run two rounds:

```text
M/Run-01
L0/Run-01
L1/Run-01
K0/Run-01
K1/Run-01

M/Run-02
L0/Run-02
L1/Run-02
K0/Run-02
K1/Run-02
```

Use a fresh Claude Desktop Code session for every run and keep model/effort settings identical.

Start every run with exactly:

```text
Read `TASK.md` completely and execute the task to completion, including all required inputs, deliverables, and final self-checks.
```

Do not add candidate-specific hints and do not expose another run's output.

## Evidence rule

Do not manually repair a generated run before comparative audit.
Preserve raw output as evidence.

The construction Claude may see `inventory.json`.
A later benchmark-execution Claude must not see research/evaluation material.
'@

$CandidateDocs = @{}
$CandidateDocs['M'] = @'
# Candidate M — Minimal Modular

## 1. Core idea

M tests the conservative hypothesis:

> A new instruction meta-architecture may not be necessary.
> Preserving V2's mental model and fixing its real defects may be enough.

M = **V2 + the frozen V2 policy oracle + the shared construction constraints + defect-driven refactoring**.

Do not reorganize the corpus merely for architectural elegance.

## 2. Binding rule: V2 lineage

Every runtime artifact must be explainable through V2 lineage.

Allowed change types:

- **Keep** — keep the V2 artifact, removing semantic restatements where needed;
- **Fix in place** — same owner, corrected defect;
- **Split** — one V2 artifact becomes several because it mixes owners, triggers, or responsibilities;
- **Merge** — competing artifacts become one;
- **Move** — content moves to a location with a more reliable trigger;
- **New** — only when a shared requirement genuinely requires a new owner, enforcement artifact, or human map.

Do not rename or move a file without a functional reason.

## 3. What M intentionally does not introduce

Do not introduce:

- stability levels;
- `Level:` classification;
- Kinds × Scopes as a meta-architecture;
- `Kind:` classification;
- capability slots/contracts/manifests/selection records;
- a formal replacement mechanism;
- rule directories organized by level/kind/capability;
- technology-neutral rewriting purely for future replaceability.

Scope must still be explicit through headers and `paths`,
but scope is not a primary architectural axis.

## 4. Ownership

Default heuristic:

> Keep policy with its V2 owner unless a concrete defect requires a move, split, or merge.

If V2 contains several copies of the same rule:

1. choose the owner with the most reliable trigger;
2. the owner must match the moment when the rule is actually needed;
3. replace other copies with pointers or check-by-reference entries.

`.claude/MAP.md` must give a human a simple answer to:

- what each file owns;
- its scope;
- how it loads;
- how it is enforced.

## 5. Decisions

Keep the V2-lineage two-part planning-time decision model:

- architecture defaults, approval gate, and patterns not adopted → always-loaded `CLAUDE.md`;
- approved technology stack and conditional technologies → imported `docs/technology-stack.md`.

Both must be available during planning.

Do not create:

- a K-style single decision register;
- an L-style decision hierarchy by stability level.

ADR history may live under `docs/decisions/`.

## 6. Rules

Expect a **flat** `.claude/rules/` directory.

A reasonable result after defect-driven splitting may resemble:

```text
.claude/rules/
├── architecture.md
├── persistence.md
├── coding-style.md
├── performance.md
├── error-handling.md
├── security.md
├── testing.md
├── dependencies.md
└── angular.md
```

This is illustrative, not a requirement to produce exactly nine files.

Binding properties:

- flat rule directory;
- recognizable V2 topical organization;
- `persistence.md` is allowed as a split from architecture/EF responsibilities;
- `angular.md` provides reliable path-loaded frontend policy;
- every runtime rule has explicit `paths`;
- procedures/technique are separated into skills/references.

## 7. Loading

Use the shared minimal mechanism model:

- always-loaded: `CLAUDE.md` plus imported `docs/technology-stack.md`;
- path-loaded: flat rules;
- hook: process/co-change enforcement;
- explicit workflow read: greenfield/review/verify cases where path loading may not have happened;
- on-demand: knowledge skills.

M may keep broader V2-like path globs when narrowing is not required by a real defect.

Do not turn M into K merely to optimize scope precision.

## 8. Skills and references

Preserve the familiar V2 skill model while fixing responsibility conflicts:

- workflow skill = procedure;
- knowledge skill = technique;
- a private reference is consumed only by its owning skill;
- shared policy must not live only in a private reference;
- `code-reviewer` is a thin wrapper;
- `serilog` does not compete with `logging`;
- `resilience` does not compete with `httpclient-factory`;
- a rule and a skill must not be independent owners of the same policy.

M does not need a formal workflow/knowledge taxonomy as a primary architecture.
The separation may be expressed through responsibility and naming.

## 9. Enforcement

Use deterministic enforcement where it materially improves reliability of mechanically checkable rules.

M must not avoid hooks/settings/checkers merely because V2 did not contain them when the candidate design or shared construction constraints require reliable enforcement.

However, every new artifact must have a clear purpose:
reliability, deterministic enforcement, or human navigation.

## 10. Illustrative top-level shape

```text
template/
├── CLAUDE.md
├── SPECIFICATION.md
├── CUSTOM_SETTINGS.md
├── .editorconfig
├── Directory.Build.props
├── Directory.Packages.props
├── docs/
│   ├── technology-stack.md
│   └── decisions/
└── .claude/
    ├── MAP.md
    ├── settings.json
    ├── hooks/
    ├── scripts/
    ├── rules/                 # flat topical rules
    ├── skills/
    └── agents/
```

Do not create a file merely because it appears in this illustrative tree.

## 11. Leakage checks

The result is no longer M if it introduces:

- `rules/0-core`, `rules/1-architecture`, or `Level:` → leakage toward L;
- a `Kind:` taxonomy or K-style scope-first organization plus a single decision register → leakage toward K;
- capability contracts/manifests/slot selection → leakage toward B1;
- broad reorganization that cannot be justified by a V2 defect or shared requirement;
- technology-neutral rewriting introduced only for replaceability.

## 12. Success criterion

M should look like a **recognizable, well-refactored V2**,
not like a new theory of instruction architecture.

If M physically converges with parts of K0 after fixing the same defects,
that is an acceptable research result.
Do not force artificial differences.
'@
$CandidateDocs['L0'] = @'
# Candidate L0 — Stability-first, Embedded Capabilities

## 1. Core idea

L0 organizes the instruction system **by stability**.

Primary axis:

```text
0 Core → 1 Architecture → 2 Technology → 3 Project
```

Product, feature, and task inputs are **outside** this hierarchy.

Technologies remain embedded:
NUnit, EF Core, Angular, and other concrete choices may be named directly where the level model allows them.

There are no capability contracts, slots, or selection mechanism.

## 2. Four levels

### 0 Core

Most stable concerns:

- precedence;
- product governance;
- decision-control protocol;
- completion contract;
- challenge obligation;
- Git safety;
- simplicity/proportional complexity;
- technology-neutral principles for testing, security, logging, dependency hygiene, and error exposure.

### 1 Architecture

Adopted architecture and role/boundary policy:

- Clean Architecture;
- reference direction;
- Domain/Application/Infrastructure/Api responsibilities;
- use-case orchestration;
- persistence boundary;
- composition root;
- code organization and naming by role;
- entry-point responsibilities;
- outcomes vs exceptions;
- frontend structural boundary;
- patterns not adopted.

Level 1 may use fixed platform vocabulary (.NET/C#/TypeScript)
but must not depend on EF Core, NUnit, Angular, Serilog, or other concrete technologies.

### 2 Technology

Concrete technique and bindings:

- C#/.NET conventions;
- ASP.NET Core;
- EF Core + SQL Server;
- FluentValidation;
- NUnit;
- Angular;
- logging provider;
- Docker/CI;
- other technology-specific policy/knowledge.

### 3 Project

Project-specific selection/defaults:

- approved stack;
- conditional technologies;
- repository/project layout;
- naming;
- test-project placement;
- development data lifecycle;
- project-specific rules;
- workflows that depend on concrete commands/layout/stack.

## 3. Level assignment rule

For each statement, apply these tests in order:

1. Depends on project-specific selection/layout/defaults? → **3 Project**
2. Names a technology other than the fixed platform? → **2 Technology**
3. Presupposes the adopted architecture/role/boundary? → **1 Architecture**
4. Otherwise → **0 Core**

Binding rule:

> A statement's level is determined by the most volatile thing it depends on.

Split mixed statements instead of forcing them into one level.

Example:

- Architecture: "Domain does not depend on a persistence framework."
- Technology/EF: "`DbContext`, `DbSet<T>`, and EF attributes are persistence-framework types."

## 4. Dependency direction

A conformance dependency may point only:

- to the same level;
- or to a **more stable** level.

```text
Project → Technology → Architecture → Core
```

Reverse conformance dependency is forbidden.

A routing pointer such as "run verify" or "see skill X" is not a conformance dependency.

### Technology neutrality

Levels 0 and 1 must not name concrete technologies
other than the fixed platform (.NET/C#/TypeScript).

This is a binding property of L0.

## 5. Runtime organization

Rules are **level-first**:

```text
.claude/rules/
├── 0-core/
├── 1-architecture/
├── 2-technology/
└── 3-project/
```

Every instruction artifact declares `Level:` in its classification header.

Do not create one file per level.
Each level contains cohesive modules with their own owner/trigger.

An illustrative split:

```text
0-core/
├── testing-principles.md
├── security-principles.md
├── logging-principles.md
└── dependency-hygiene.md

1-architecture/
├── overview.md
├── backend-layers.md
├── persistence-boundary.md
├── entry-points.md
├── outcomes.md
└── frontend-structure.md

2-technology/
├── csharp.md
├── aspnet-core.md
├── ef-core.md
├── fluentvalidation.md
├── nunit.md
├── angular.md
└── containers-ci.md

3-project/
├── decisions.md
├── layout.md
└── data-lifecycle.md
```

Names are illustrative.
The level model, neutrality rule, and dependency direction are mandatory.

## 6. Always-loaded decisions

L0 uses **stratified decisions**, not a single cross-level register:

- adopted architecture and patterns not adopted → Level 1;
- project stack/defaults/conditional technologies → Level 3.

Both summaries are always-loaded through imports from `CLAUDE.md`.

Do not merge them into a K-style single decision register.

## 7. Embedded technologies

L0 has no generic replacement mechanism.

Example for NUnit:

- framework-neutral testing principles → Level 0;
- NUnit-specific rules → Level 2;
- selection of NUnit → Level 3;
- workflows may name NUnit commands directly.

Replacing NUnit with xUnit therefore requires edits to the technology module,
project selection, workflows/assets where the choice is embedded.
That is an expected property of L0, not a defect.

## 8. Loading

Level does **not** determine loading mechanism.

A level may contain different trigger types:

- Core: `CLAUDE.md` plus path-scoped principle rules;
- Architecture: imported overview plus path rules;
- Technology: path rules plus knowledge skills;
- Project: imported decisions plus path rules plus workflows/hooks.

Do not make every Core file always-loaded merely because it is Core.

Greenfield workflows must explicitly read required Architecture/Project owners
when path triggers may not have fired yet.

## 9. Skills

Preserve useful V2 workflow and knowledge coverage, but refactor responsibilities to fit the level model. Workflows own procedures; knowledge skills own technique; neither is the sole owner of must-policy.

Skills may declare `Level:`.

Typical placement:

- technology knowledge → Level 2;
- `project-structure`, `verify`, `code-review`, `build-fix` → Level 3 when they depend on concrete layout/commands;
- `architecture-decision`, `custom-settings`, `template-maintenance` may sit closer to Core by responsibility.

A skill is not the sole owner of must-policy.

## 10. Human map

Organize the map **by level first, then module**.

Show:

- dependency direction;
- owners;
- loading;
- split-statement relationships.

## 11. What L0 intentionally does not contain

Do not introduce:

- `Kind:` taxonomy;
- K-style Kind × Scope grid as primary organization;
- a single K decision register;
- capability contracts;
- module manifests;
- slot selection;
- generic facet lookup;
- Feature/Task instruction levels.

## 12. Leakage checks

The result is no longer L0 if:

- levels exist only as labels and the dependency rule is not enforced;
- Core/Architecture directly name EF Core/NUnit/Angular/etc.;
- contracts/slots/manifests appear → leakage toward L1;
- `Kind:` plus scope-first standards appear → leakage toward K;
- decisions are collapsed into one cross-level register.

## 13. Success criterion

A human should understand placement by asking:

> "How fundamental and stable is this rule?"

More volatile content depends on more stable content,
and concrete technology bindings appear only at Technology/Project levels.
'@
$CandidateDocs['L1'] = @'
# Candidate L1 — Stability-first + Replaceable Capabilities

## 1. Core idea

L1 is the **full L0 stability-first model plus first-class replaceable capabilities**.

The primary hierarchy remains:

```text
0 Core → 1 Architecture → 2 Technology → 3 Project
```

Inputs remain outside the hierarchy.

A replacement boundary is added only for the agreed slot set.

L1 is not a different level model.
If the capability transformation were removed, the result should reduce to L0.

## 2. Stability-first model

Use the same binding level rules as L0.

### 0 Core

Operating policy and technology-neutral engineering principles.

### 1 Architecture

Role vocabulary, architecture-level invariants, and boundaries.

### 2 Technology

Concrete implementation technique and bindings.

### 3 Project

Selection, defaults, layout, and project decisions.

### Assignment rule

1. project-specific selection/layout/default → Project;
2. concrete non-platform technology → Technology;
3. adopted architecture/role/boundary → Architecture;
4. otherwise → Core.

Conformance dependencies may point only to the same or a more stable level.

Core/Architecture must not name concrete technology implementations
except for the fixed platform vocabulary.

Rules remain level-first:

```text
.claude/rules/0-core/
.claude/rules/1-architecture/
.claude/rules/2-technology/
.claude/rules/3-project/
```

Instruction artifacts declare `Level:`.

## 3. Capability model

Add exactly four experimental slots:

1. `architecture` — required **frame**, initial implementation `clean-architecture`;
2. `persistence` — required leaf, initial implementation `ef-core`, provider variant `sqlserver`;
3. `backend-testing` — required leaf, initial implementation `nunit`;
4. `frontend` — optional leaf, initial implementation `angular`.

Do not turn logging, validation, Swagger, caching, or other concerns into slots.
They remain embedded.

## 4. Capability structure

Each slot has:

- maintainer-facing `CONTRACT.md`;
- selected implementation;
- implementation manifest `MODULE.md`;
- runtime facets;
- an always-loaded selection record;
- structural leak/conformance checking.

Composition is **static**:

- each required slot has exactly one selected implementation;
- each optional slot has zero or one;
- unselected implementations do not appear in runtime context;
- dynamic runtime implementation selection is forbidden.

Contracts/manifests are maintainer metadata and are not auto-loaded in normal code-generation sessions.

## 5. Stable vocabulary and leak rule

Outside an implementation module, artifacts may refer to:

- slot name;
- facet role;
- stable role vocabulary;
- selection/declared properties in the designated decision summary.

Outside the module, do not hardcode the implementation name
except where explicitly allowed in selection/decision metadata.

Example:

- an external workflow refers to `backend-testing.commands`;
- the selected module knows that this means NUnit;
- replacing NUnit with xUnit should not require rewriting the external workflow merely because of the framework name.

A module-owned knowledge skill description may contain concrete trigger cues such as `NUnit` or `[TestCase]`.

Facet file names are based on **roles**, not implementations:
`test-framework.md`, not `nunit.md`.

## 6. Architecture is a frame capability

Architecture is not an ordinary leaf.

Level 1 contains stable **role vocabulary**, for example:

- use-case unit;
- persistence-access contract;
- commit boundary;
- entry point;
- composition root;
- test-project role.

The `architecture/clean-architecture` frame implementation:

- maps roles to Domain/Application/Infrastructure/Api;
- owns placement;
- owns Clean Architecture-specific layout and patterns-not-adopted;
- supplies the architecture-check specification.

Leaf capabilities depend on role vocabulary rather than frame implementation terms whenever possible.

## 7. Frame/leaf binding rule

Use this rule:

> Placement belongs to the frame; technique belongs to the leaf.

Examples:

- "the commit boundary lives in Application" → architecture frame;
- "`SaveChangesAsync` on the scoped DbContext implements the commit boundary" → persistence/ef-core;
- test-project placement → architecture frame;
- NUnit test adapter → backend-testing/nunit.

If a binding cannot be expressed through stable roles,
the dependent slot explicitly declares `binds:` coupling.

## 8. Persistence contract

The persistence capability covers more than the ORM name.

The contract requires explicit facets/properties for:

- persistence access / commit-boundary binding;
- migration mechanism;
- seeding mechanism;
- provider variant;
- default string-comparison / case-sensitivity semantics when observable;
- relational testing expectations;
- implementation-specific workflow/enforcement facets.

EF Core → Dapper must not silently lose migration or seeding semantics.
A missing required facet is a conformance failure / Decision Request.

SQL Server → PostgreSQL is a provider variation/change inside persistence,
not a separate capability.

## 9. Backend-testing contract

Implementation-independent test policy stays outside the module:

- test levels;
- determinism;
- isolation;
- probe-to-test;
- relational fidelity;
- framework-neutral naming policy.

`backend-testing/nunit` supplies:

- framework-specific rules;
- knowledge/technique;
- commands;
- scaffold assets;
- adapter for neutral architecture checks.

NUnit → xUnit should replace the module rather than require template-wide hunting.

## 10. Frontend contract

`frontend` is optional.

Neutral frontend structural policy stays outside the Angular implementation.

`frontend/angular` supplies Angular-specific:

- framework rule facet;
- knowledge;
- scaffold/verify commands;
- selected technology decision content.

Removing the frontend should be possible by clearing the optional selection
without manually hunting unrelated artifacts.

## 11. Placement by levels

Capability does **not** replace the level model.

Each facet remains at the level determined by its content.
One module may contribute facets at several levels.

Example:

- neutral test principles → Core, outside the module;
- frame-owned test placement → Architecture;
- `test-framework.md` and `dotnet-testing` → Technology facets;
- selected implementation → Project selection record.

Implementation-owned artifacts declare `Capability:` in addition to `Level:`.

## 12. Decisions and selection

Architecture/project decisions remain L-style and stratified.

The selection record is part of Project decision content.

Do not create a K-style single cross-level decision register.

Changing a slot selection is Reserved and requires an ADR.

A declared-property change that affects observable product behavior must not happen silently.

## 13. Workflows

Workflows must not hardcode selected implementations
where the capability contract provides a facet role.

They reach implementation-specific steps through facet roles.

This is a binding property of L1.

Do not build a dynamic plugin engine:
composition is static and runtime contains only selected facets.

## 14. Illustrative shape

```text
.claude/
├── capabilities/
│   ├── architecture/
│   │   ├── CONTRACT.md
│   │   └── clean-architecture/MODULE.md
│   ├── persistence/
│   │   ├── CONTRACT.md
│   │   └── ef-core/MODULE.md
│   ├── backend-testing/
│   │   ├── CONTRACT.md
│   │   └── nunit/MODULE.md
│   └── frontend/
│       ├── CONTRACT.md
│       └── angular/MODULE.md
├── rules/
│   ├── 0-core/
│   ├── 1-architecture/
│   ├── 2-technology/
│   └── 3-project/
├── skills/
├── settings.json
├── hooks/
└── scripts/
```

Contracts/manifests are maintainer metadata.
Runtime facets may physically live in normal rule/skill locations;
the manifest ties them to the module.

Do not create a second generated copy of the same text unless necessary.

## 15. Human map

Organize the map by levels,
with an additional capability view containing:

- slot;
- selected implementation;
- facets;
- level of each facet;
- loading;
- owner.

## 16. What L1 intentionally does not contain

Do not introduce:

- K `Kind:` taxonomy;
- K scope-first rule directories;
- one K cross-level decision register;
- slots outside the four agreed slots;
- dynamic multiple runtime implementations;
- changes to non-slot content merely because L1 is "more advanced" than L0.

## 17. Leakage checks

The result is no longer L1 if:

- non-slot organization no longer follows the stability-first model;
- contracts exist but implementation names still leak everywhere;
- workflows directly name implementations instead of facet roles;
- Core/Architecture name concrete leaf technologies;
- K-style Kind × Scope appears;
- new slots are added without a justified experimental reason;
- multiple implementations ship in runtime simultaneously.

## 18. Success criterion

L1 must answer two independent questions:

1. **Where does this belong by stability?** → Level.
2. **Can this concern be replaced as one module?** → Capability.

The replacement boundary must not destroy the stability hierarchy.
'@
$CandidateDocs['K0'] = @'
# Candidate K0 — Kinds × Scopes, Embedded Capabilities

## 1. Core idea

K0 organizes the instruction system by two questions:

1. **What responsibility is this?** → Kind
2. **Where does it apply?** → Scope

Technologies remain embedded.
There are no capability slots/contracts/selection mechanisms.

K0 does not use stability levels as its primary architecture.

## 2. Kinds

Use seven kinds.

### OP — Operating Policy

Agent behavior:

- precedence;
- product governance;
- decision protocol;
- completion contract;
- challenge obligation;
- Git safety;
- workflow routing.

Typically always-loaded through `CLAUDE.md`.

### DEC — Project Decisions

Accepted choices:

- architecture;
- patterns not adopted;
- stack;
- project defaults;
- conditional technologies.

Always-loaded summary, with detail left to rules/skills/ADRs.

### STD — Standards

Normative `must/default/prefer` rules for a scope.

Runtime mechanism: path-scoped rules.

### KNW — Knowledge

Technique, examples, trade-offs.

Runtime mechanism: model-invoked knowledge skills.

### WF — Workflows

Procedures, steps, stop conditions, outputs.

Runtime mechanism: workflow skills.

### ENF — Enforcement

Hooks, permissions, scripts, analyzers/assets/checks.

### IN — Product Inputs

`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature/task inputs.

Inputs may define behavior or request a decision,
but they do not become engineering policy.

## 3. Scopes

Use:

- `common`
- `backend`
- `backend-tests`
- `frontend`
- `delivery`
- `repo/meta`

Each instruction artifact has exactly one primary Kind and one Scope where applicable.

Classification headers include `Kind:` and `Scope:` plus owner/loading metadata.

## 4. Kind determines mechanism

This is a binding property of K0.

Do not create:

- `Kind: STD` content that lives only as a model-invoked knowledge skill;
- `Kind: KNW` content that acts as the authoritative path rule.

Responsibility and mechanism must match.

## 5. STD directory organization

STD rules are organized **by scope**:

```text
.claude/rules/
├── common/
├── backend/
├── backend-tests/
├── frontend/
└── delivery/
```

Within a scope, split by cohesive responsibility/trigger, for example:

```text
backend/
├── architecture.md
├── persistence.md
├── api.md
├── error-handling.md
├── csharp.md
└── security.md

backend-tests/
└── testing.md

frontend/
└── angular.md
```

Exact names are illustrative.

Do not create `0-core/1-architecture/...`.

## 6. Decision register

K0 has **one always-loaded decision register**.

It contains all project/architecture decisions:

- stable IDs;
- decision summary;
- `Details in`;
- `Affects`.

`Affects` lists dependent STD/KNW/WF/ENF artifacts
so `architecture-decision` can propagate a decision change.

The register must not become a long policy manual.
Detailed policy remains with its authoritative owner.

This single register is a defining difference between K and M/L.

## 7. Kind dependency direction

Use this conformance graph:

```text
WF → KNW → STD → DEC → OP
ENF → STD / DEC
IN → may initiate DEC change but does not override OP/DEC
```

Routing pointers may point differently when the target is reliably invocable.

Skill-private references remain private to their owning skill.

## 8. Embedded technologies

In K0, one technology **may appear across several kinds**
because the artifacts have different responsibilities.

Example for NUnit:

- DEC: selection of NUnit;
- STD: framework-specific must-rules;
- KNW: technique/examples;
- WF: scaffold/verify commands;
- ENF: test/architecture-check assets.

This is not semantic duplication if each artifact contains only its own responsibility.

There is no replacement mechanism:
NUnit → xUnit requires coordinated edits across affected kinds.

The decision register's `Affects` field should make those locations discoverable.

## 9. Loading

Kind and trigger class align:

- OP/DEC → always-loaded;
- STD → path-scoped;
- KNW → on-demand knowledge;
- WF → workflow invocation;
- ENF → event/check;
- IN → read as product input.

This is one of K0's main hypotheses:
knowing the Kind should largely tell a human how the artifact loads.

## 10. Technology-specific policy

Unlike L0, K0 does not impose technology-neutral Architecture/Core levels.

An STD rule may directly name EF Core, NUnit, Angular, etc.
when that is the correct owner for its responsibility/scope.

Do not rewrite concrete wording into abstraction merely for "stability".

## 11. Human map

The map has a clear **Kind × Scope view** showing:

- artifacts;
- owner;
- loading;
- enforcement;
- extension point.

Also show decision → `Affects` relationships.

## 12. Illustrative shape

```text
template/
├── CLAUDE.md                          # OP
├── SPECIFICATION.md                   # IN
├── CUSTOM_SETTINGS.md                 # IN
├── docs/
│   ├── architecture/
│   │   └── decision-register.md       # DEC, imported
│   └── decisions/                     # ADRs
└── .claude/
    ├── MAP.md
    ├── settings.json                  # ENF
    ├── hooks/                         # ENF
    ├── scripts/                       # ENF
    ├── rules/                         # STD, scope-first
    │   ├── common/
    │   ├── backend/
    │   ├── backend-tests/
    │   ├── frontend/
    │   └── delivery/
    ├── skills/                        # WF + KNW
    └── agents/
```

Do not create a file merely to populate a taxonomy cell.

## 13. Structural checks

Verify:

- each instruction artifact has correct `Kind`/`Scope`;
- mechanism/location matches Kind;
- STD path and `paths` are consistent with Scope;
- decision summaries exist only in the decision register;
- STD rules cite DEC IDs instead of restating decision text;
- `Affects` targets exist and stay consistent;
- procedures do not live in STD;
- normative policy does not exist only in KNW;
- no `Level:` hierarchy exists;
- no capability contracts/selection exist.

## 14. What K0 intentionally does not contain

Do not introduce:

- stability-level architecture;
- `Level:` headers;
- L-style technology-neutral rewriting;
- capability contracts;
- module manifests;
- slot selection;
- generic facet lookup;
- V2 lineage as a mandatory placement rule.

## 15. Leakage checks

The result is no longer K0 if:

- `rules/0-core/...` and ordered level dependencies appear;
- decisions are split by stability levels instead of one register;
- capability contracts/manifests appear;
- implementation names are hidden behind generic slots;
- the taxonomy exists only on paper but actual mechanisms do not follow Kind;
- V2 file names are preserved merely for lineage against Kind/Scope placement.

## 16. Success criterion

A human should be able to place new content by asking:

> "What is this — decision, standard, knowledge, workflow, enforcement, or input?"

and then:

> "Where does it apply?"

Those answers should almost automatically determine location, loading, and owner.
'@
$CandidateDocs['K1'] = @'
# Candidate K1 — Kinds × Scopes + Replaceable Capabilities

## 1. Core idea

K1 is the **full K0 Kinds × Scopes model plus replaceable capability modules**.

Three independent coordinates:

1. **Capability** — what can be replaced as one unit;
2. **Kind** — what responsibility the artifact has and therefore what mechanism it uses;
3. **Scope** — where the artifact applies.

If the capability transformation were removed,
the non-slot system should reduce conceptually to K0.

## 2. Kinds

Use the same seven kinds:

- `OP` — operating policy;
- `DEC` — project decisions;
- `STD` — path-scoped standards;
- `KNW` — knowledge/technique;
- `WF` — procedures;
- `ENF` — enforcement;
- `IN` — product inputs.

Kind determines mechanism and allowed content.

## 3. Scopes

Use:

- `common`
- `backend`
- `backend-tests`
- `frontend`
- `delivery`
- `repo/meta`

STD rules remain scope-first:

```text
.claude/rules/
├── common/
├── backend/
├── backend-tests/
├── frontend/
└── delivery/
```

Do not create a stability-level directory hierarchy.

## 4. K dependency graph

Preserve the K0 direction:

```text
WF → KNW → STD → DEC → OP
ENF → STD / DEC
```

IN may request a decision change but does not override policy itself.

## 5. Capability model

Add exactly four experimental slots:

1. `architecture` — required frame, initial implementation `clean-architecture`;
2. `persistence` — required leaf, initial implementation `ef-core`, provider variant `sqlserver`;
3. `backend-testing` — required leaf, initial implementation `nunit`;
4. `frontend` — optional leaf, initial implementation `angular`.

All other concerns remain embedded.

Each slot has:

- `CONTRACT.md`;
- selected implementation;
- `MODULE.md` manifest;
- runtime facets;
- always-loaded selection;
- leak/conformance checking.

Static composition:

- one implementation per required slot;
- zero or one per optional slot;
- unselected implementations do not enter runtime;
- dynamic plugin selection is forbidden.

## 6. Ownership precedence

Classify content in this order:

1. **Capability:** is it implementation-specific?
   - yes → the module owns it;
   - no → it belongs to the normal non-slot system;
2. **Kind:** what responsibility does it have?
   - determines mechanism/location family;
3. **Scope:** where does it apply?
   - determines path/scope directory.

Implementation-owned runtime artifacts declare:

```text
Kind: ...
Scope: ...
Capability: <slot>/<implementation>
```

Non-slot artifacts use `Capability: —` or an equally clear marker.

## 7. Decision register

Like K0, K1 has **one always-loaded decision register**.

It additionally contains a slot-selection section:

- architecture → clean-architecture;
- persistence → ef-core (sqlserver);
- backend-testing → nunit;
- frontend → angular or none.

The register stores selection and declared properties,
but does not duplicate implementation policy.

Changing a selection is Reserved.

## 8. Capability facets across kinds

One module may provide facets in several kind locations.

Example `backend-testing/nunit`:

- DEC facet → selection/decision section;
- STD facet → `rules/backend-tests/test-framework.md`;
- KNW facet → `dotnet-testing`;
- WF facet → scaffold/verify commands reached through a facet role;
- ENF facet → adapter that runs neutral architecture checks as NUnit tests.

The module is logically cohesive,
while runtime facets are physically distributed according to mechanism.

`MODULE.md` lists all facets.

## 9. Neutral policy + implementation facet

For slot concerns, separate:

- implementation-independent policy → ordinary non-slot K standard;
- implementation-specific rules → capability facets.

Examples:

```text
rules/backend-tests/testing.md          # neutral STD
rules/backend-tests/test-framework.md   # backend-testing facet

rules/backend/persistence.md            # neutral STD
rules/backend/persistence-technology.md # persistence facet

rules/backend/architecture.md           # role-level neutral STD
rules/backend/architecture-style.md     # architecture frame facet
```

Apply the same idea to frontend.

## 10. Leak rule

Outside a module and its explicit allow-list, do not hardcode the selected implementation name.

Allowed exceptions:

- selection record;
- declared properties;
- concrete trigger cues in a module-owned knowledge-skill description;
- the module's own manifest/header.

External workflows/standards refer to slot/facet roles.

Facet file names are role-based:
`test-framework.md`, not `nunit.md`.

## 11. Frame/leaf rule

Architecture is a frame.

Use stable role vocabulary.

Binding rule:

> Placement belongs to the frame; technique belongs to the leaf.

Examples:

- commit-boundary placement → architecture/clean-architecture;
- DbContext/SaveChanges technique → persistence/ef-core;
- test-project placement → architecture frame;
- NUnit adapter → backend-testing/nunit.

Unavoidable cross-slot bindings are declared with `binds:` on the dependent slot.

## 12. Persistence capability

The contract requires:

- persistence/commit-boundary binding;
- migration mechanism;
- seeding mechanism;
- provider variant;
- observable declared properties such as string/case sensitivity;
- testing implications;
- relevant workflow/enforcement facets.

SQL Server → PostgreSQL is a provider variation/change inside persistence,
not a separate slot.

EF Core → Dapper must surface a missing migration mechanism
instead of silently losing behavior.

## 13. Non-slot content

Non-slot content remains K-style:

- same Kind model;
- same Scope model;
- same owner logic;
- technologies remain embedded when the concern is not in the slot set.

Do not rewrite all K0 content into a neutral abstract style merely because K1 is "more modular".

This is critical for a clean K0 vs K1 comparison.

## 14. Workflows

A WF body may remain normal non-slot workflow content,
while implementation-specific steps are reached through facet roles.

Do not hardcode selected implementations where a contract provides a role.

Composition remains static:
do not implement runtime plugin discovery.

## 15. Human map

The map has two views.

### Kind × Scope view

Shows where policy/workflow/knowledge lives and how it loads.

### Capability view

For each slot, show:

- selected implementation;
- facets by Kind;
- scope;
- loading;
- declared bindings/properties.

This is required because one module's facets are physically spread across kind-specific locations.

## 16. Illustrative shape

```text
template/
├── CLAUDE.md
├── docs/
│   ├── architecture/
│   │   └── decision-register.md
│   └── decisions/
└── .claude/
    ├── MAP.md
    ├── capabilities/
    │   ├── architecture/
    │   │   ├── CONTRACT.md
    │   │   └── clean-architecture/MODULE.md
    │   ├── persistence/
    │   │   ├── CONTRACT.md
    │   │   └── ef-core/MODULE.md
    │   ├── backend-testing/
    │   │   ├── CONTRACT.md
    │   │   └── nunit/MODULE.md
    │   └── frontend/
    │       ├── CONTRACT.md
    │       └── angular/MODULE.md
    ├── rules/
    │   ├── common/
    │   ├── backend/
    │   ├── backend-tests/
    │   ├── frontend/
    │   └── delivery/
    ├── skills/
    ├── settings.json
    ├── hooks/
    └── scripts/
```

Do not populate all theoretical Kind × Scope × Capability cells.
Create only artifacts with a functional reason.

## 17. What K1 intentionally does not contain

Do not introduce:

- `Level:` headers;
- Core→Architecture→Technology→Project hierarchy;
- L-style stratified decisions;
- slots outside the four agreed slots;
- multiple runtime implementations;
- dynamic plugin selection;
- non-slot rewrites not required by K rules.

## 18. Leakage checks

The result is no longer K1 if:

- contracts exist but implementation names still leak across the system;
- workflows bypass facet roles;
- a facet has the wrong Kind or Scope;
- the module manifest misses facets;
- non-slot content deviates from the K model without cause;
- a Level hierarchy appears;
- extra slots are added "for symmetry";
- runtime contains unselected implementations.

## 19. Success criterion

A human should classify content by asking, in order:

1. "Does this belong to a replaceable capability?"
2. "What Kind is it?"
3. "What Scope does it apply to?"

Those answers should determine owner, location, loading, and replacement boundary.

K1 is allowed to be the most complex candidate,
but it must not be complex **without functional value**.
'@

$RunPlan = @(
    [pscustomobject]@{ Order = 1;  Candidate = "M";  Run = "Run-01" },
    [pscustomobject]@{ Order = 2;  Candidate = "L0"; Run = "Run-01" },
    [pscustomobject]@{ Order = 3;  Candidate = "L1"; Run = "Run-01" },
    [pscustomobject]@{ Order = 4;  Candidate = "K0"; Run = "Run-01" },
    [pscustomobject]@{ Order = 5;  Candidate = "K1"; Run = "Run-01" },
    [pscustomobject]@{ Order = 6;  Candidate = "M";  Run = "Run-02" },
    [pscustomobject]@{ Order = 7;  Candidate = "L0"; Run = "Run-02" },
    [pscustomobject]@{ Order = 8;  Candidate = "L1"; Run = "Run-02" },
    [pscustomobject]@{ Order = 9;  Candidate = "K0"; Run = "Run-02" },
    [pscustomobject]@{ Order = 10; Candidate = "K1"; Run = "Run-02" }
)

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

function Assert-Directory {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        throw "Required directory is missing: $Path"
    }
}

function Get-DirectoryManifestHash {
    param([string]$Root)

    $rootFull = [System.IO.Path]::GetFullPath($Root).TrimEnd("\", "/")
    $lines = New-Object System.Collections.Generic.List[string]

    Get-ChildItem -LiteralPath $rootFull -Recurse -Force -File |
        Sort-Object FullName |
        ForEach-Object {
            $relative = $_.FullName.Substring($rootFull.Length + 1).Replace("\", "/")
            $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            $lines.Add("$relative`t$hash")
        }

    $payload = [string]::Join("`n", $lines)
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($payload)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace("-", "").ToLowerInvariant()
    }
    finally {
        $sha.Dispose()
    }
}

function Assert-NoCyrillic {
    param([string]$Path)

    $text = [System.IO.File]::ReadAllText($Path)
    if ($text -match '[\u0400-\u04FF]') {
        throw "Cyrillic text found in English-only technical artifact: $Path"
    }
}

function Assert-RepositoryClean {
    $status = @(& git -C $RepoRoot status --porcelain --untracked-files=all)
    if ($status.Count -gt 0) {
        throw @"
Source repository is not clean.

Commit/stash/remove all changes before preparing the final Iteration-005 series.

$($status -join "`n")
"@
    }
}

function Assert-PolicyInputs {
    $inventoryPath = Join-Path $RepoRoot "research\policy\inventory.json"
    $sharedPath = Join-Path $RepoRoot "research\policy\shared-research-invariants.json"

    Assert-File $inventoryPath
    Assert-File $sharedPath

    try {
        $inventory = Get-Content -LiteralPath $inventoryPath -Raw | ConvertFrom-Json
    }
    catch {
        throw "inventory.json is invalid JSON: $($_.Exception.Message)"
    }

    if ([string]$inventory.schema_version -ne "0.4") {
        throw "Expected inventory schema_version 0.4, got '$($inventory.schema_version)'."
    }

    if ([int]$inventory.policy_count -ne 194) {
        throw "Expected inventory policy_count 194, got '$($inventory.policy_count)'."
    }

    $actualCount = 0
    foreach ($group in $inventory.policygroups) {
        $actualCount += @($group.policies).Count
    }
    if ($actualCount -ne 194) {
        throw "Inventory declares 194 policies but stores $actualCount."
    }

    if ([string]$inventory.coverage_policy.candidate_visibility -ne "allowed") {
        throw "Inventory candidate_visibility must be 'allowed'."
    }

    if ([string]$inventory.coverage_policy.benchmark_execution_visibility -ne "forbidden") {
        throw "Inventory benchmark_execution_visibility must be 'forbidden'."
    }

    try {
        $shared = Get-Content -LiteralPath $sharedPath -Raw | ConvertFrom-Json
    }
    catch {
        throw "shared-research-invariants.json is invalid JSON: $($_.Exception.Message)"
    }

    $ids = @($shared.invariants | ForEach-Object { [string]$_.id })
    if ($ids.Count -ne 2 -or -not ($ids -contains "GOV-017") -or -not ($ids -contains "GOV-018")) {
        throw "Expected exactly GOV-017 and GOV-018 in shared-research-invariants.json."
    }

    foreach ($invariant in $shared.invariants) {
        if ([string]$invariant.status -ne "shared_construction_constraint") {
            throw "Unexpected shared invariant status for $($invariant.id): $($invariant.status)"
        }
    }

    $baselineSha = (& git -C $RepoRoot rev-parse "HEAD:templates/v2-baseline").Trim()
    if (-not $baselineSha) {
        throw "Could not resolve templates/v2-baseline tree SHA."
    }

    if ([string]$inventory.baseline_tree_sha -ne $baselineSha) {
        throw "Inventory baseline_tree_sha '$($inventory.baseline_tree_sha)' does not match current baseline tree '$baselineSha'."
    }
}

function Copy-SourceIntoRun {
    param([string]$RunRoot)

    $sourceRoot = Join-Path $RunRoot "source"
    New-Item -ItemType Directory -Path $sourceRoot -Force | Out-Null

    Copy-Item `
        -LiteralPath (Join-Path $RepoRoot "research\policy\inventory.json") `
        -Destination (Join-Path $sourceRoot "inventory.json") `
        -Force

    Copy-Item `
        -LiteralPath (Join-Path $RepoRoot "research\policy\shared-research-invariants.json") `
        -Destination (Join-Path $sourceRoot "shared-research-invariants.json") `
        -Force

    $baselineSource = Join-Path $RepoRoot "templates\v2-baseline"
    $baselineTarget = Join-Path $sourceRoot "v2-baseline"
    New-Item -ItemType Directory -Path $baselineTarget -Force | Out-Null

    Get-ChildItem -LiteralPath $baselineSource -Force | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $baselineTarget -Recurse -Force
    }
}

function Verify-Staging {
    $expectedTaskHash = $null
    $candidateHashes = @{}
    $expectedInventoryHash = $null
    $expectedSharedHash = $null
    $expectedBaselineHash = $null

    foreach ($item in $RunPlan) {
        $runRoot = Join-Path (Join-Path $StagingRoot $item.Candidate) $item.Run
        $taskPath = Join-Path $runRoot "TASK.md"
        $candidatePath = Join-Path $runRoot "CANDIDATE.md"
        $sourceRoot = Join-Path $runRoot "source"
        $outputRoot = Join-Path $runRoot "output"

        Assert-File $taskPath
        Assert-File $candidatePath
        Assert-File (Join-Path $sourceRoot "inventory.json")
        Assert-File (Join-Path $sourceRoot "shared-research-invariants.json")
        Assert-Directory (Join-Path $sourceRoot "v2-baseline")
        Assert-Directory $outputRoot

        if (Test-Path -LiteralPath (Join-Path $runRoot "ASSIGNED_CANDIDATE.txt")) {
            throw "ASSIGNED_CANDIDATE.txt must not exist in the final structure: $runRoot"
        }

        if (@(Get-ChildItem -LiteralPath $outputRoot -Force).Count -ne 0) {
            throw "Output is not empty: $outputRoot"
        }

        Assert-NoCyrillic $taskPath
        Assert-NoCyrillic $candidatePath

        $taskHash = (Get-FileHash -LiteralPath $taskPath -Algorithm SHA256).Hash
        if ($null -eq $expectedTaskHash) { $expectedTaskHash = $taskHash }
        elseif ($taskHash -ne $expectedTaskHash) { throw "TASK.md differs between runs." }

        $candidateHash = (Get-FileHash -LiteralPath $candidatePath -Algorithm SHA256).Hash
        if (-not $candidateHashes.ContainsKey($item.Candidate)) {
            $candidateHashes[$item.Candidate] = $candidateHash
        }
        elseif ($candidateHash -ne $candidateHashes[$item.Candidate]) {
            throw "CANDIDATE.md differs between replicates for $($item.Candidate)."
        }

        $inventoryHash = (Get-FileHash -LiteralPath (Join-Path $sourceRoot "inventory.json") -Algorithm SHA256).Hash
        $sharedHash = (Get-FileHash -LiteralPath (Join-Path $sourceRoot "shared-research-invariants.json") -Algorithm SHA256).Hash
        $baselineHash = Get-DirectoryManifestHash (Join-Path $sourceRoot "v2-baseline")

        if ($null -eq $expectedInventoryHash) { $expectedInventoryHash = $inventoryHash }
        elseif ($inventoryHash -ne $expectedInventoryHash) { throw "inventory.json differs between runs." }

        if ($null -eq $expectedSharedHash) { $expectedSharedHash = $sharedHash }
        elseif ($sharedHash -ne $expectedSharedHash) { throw "shared-research-invariants.json differs between runs." }

        if ($null -eq $expectedBaselineHash) { $expectedBaselineHash = $baselineHash }
        elseif ($baselineHash -ne $expectedBaselineHash) { throw "v2-baseline differs between runs." }
    }

    return [ordered]@{
        task_sha256 = $expectedTaskHash.ToLowerInvariant()
        inventory_sha256 = $expectedInventoryHash.ToLowerInvariant()
        shared_research_invariants_sha256 = $expectedSharedHash.ToLowerInvariant()
        v2_baseline_manifest_sha256 = $expectedBaselineHash
        candidate_sha256 = [ordered]@{
            M = $candidateHashes["M"].ToLowerInvariant()
            L0 = $candidateHashes["L0"].ToLowerInvariant()
            L1 = $candidateHashes["L1"].ToLowerInvariant()
            K0 = $candidateHashes["K0"].ToLowerInvariant()
            K1 = $candidateHashes["K1"].ToLowerInvariant()
        }
    }
}

# ---------------------------------------------------------------------------
# Preflight
# ---------------------------------------------------------------------------

Assert-Directory $RepoRoot
Assert-Directory (Join-Path $RepoRoot ".git")
Assert-Directory (Join-Path $RepoRoot "templates\v2-baseline")
Assert-RepositoryClean
Assert-PolicyInputs

$sourceCommit = (& git -C $RepoRoot rev-parse HEAD).Trim()
if (-not $sourceCommit) {
    throw "Could not read source repository HEAD."
}

New-Item -ItemType Directory -Path $DestinationParent -Force | Out-Null

if (Test-Path -LiteralPath $StagingRoot) {
    Remove-Item -LiteralPath $StagingRoot -Recurse -Force
}

try {
    # -----------------------------------------------------------------------
    # Build a completely new series in staging.
    # -----------------------------------------------------------------------

    New-Item -ItemType Directory -Path $StagingRoot -Force | Out-Null

    Write-Utf8NoBom -Path (Join-Path $StagingRoot "README.md") -Content ($ReadmeContent + "`n")
    Write-Utf8NoBom -Path (Join-Path $StagingRoot "SOURCE_COMMIT.txt") -Content ($sourceCommit + "`n")

    foreach ($item in $RunPlan) {
        $candidateRoot = Join-Path $StagingRoot $item.Candidate
        $runRoot = Join-Path $candidateRoot $item.Run

        New-Item -ItemType Directory -Path $runRoot -Force | Out-Null
        New-Item -ItemType Directory -Path (Join-Path $runRoot "output") -Force | Out-Null

        Write-Utf8NoBom -Path (Join-Path $runRoot "TASK.md") -Content ($TaskContent + "`n")
        Write-Utf8NoBom -Path (Join-Path $runRoot "CANDIDATE.md") -Content ($CandidateDocs[$item.Candidate] + "`n")

        Copy-SourceIntoRun -RunRoot $runRoot
    }

    $hashes = Verify-Staging
    $manifest = [ordered]@{
        schema_version = "1.0"
        source_commit = $sourceCommit
        created_utc = [DateTime]::UtcNow.ToString("o")
        structure = "candidate/Run-01|Run-02 with TASK.md + CANDIDATE.md + source + output"
        run_count = 10
        hashes = $hashes
    } | ConvertTo-Json -Depth 8

    Write-Utf8NoBom -Path (Join-Path $StagingRoot "INPUT_HASHES.json") -Content ($manifest + "`n")

    # -----------------------------------------------------------------------
    # Only after staging verification succeeds, deal with the old 005 folder.
    # -----------------------------------------------------------------------

    $archivedTo = $null

    if (Test-Path -LiteralPath $DestinationRoot) {
        switch ($ExistingDestination) {
            "Fail" {
                throw "Destination already exists: $DestinationRoot"
            }
            "Delete" {
                Remove-Item -LiteralPath $DestinationRoot -Recurse -Force
            }
            "Archive" {
                New-Item -ItemType Directory -Path $ArchiveRoot -Force | Out-Null

                $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
                $archiveTarget = Join-Path $ArchiveRoot ("legacy-mixed-" + $stamp)
                $suffix = 1
                while (Test-Path -LiteralPath $archiveTarget) {
                    $archiveTarget = Join-Path $ArchiveRoot ("legacy-mixed-" + $stamp + "-" + $suffix)
                    $suffix++
                }

                Move-Item -LiteralPath $DestinationRoot -Destination $archiveTarget
                $archivedTo = $archiveTarget
            }
        }
    }

    Move-Item -LiteralPath $StagingRoot -Destination $DestinationRoot

    Write-Host ""
    Write-Host "Final Iteration-005 series prepared successfully."
    Write-Host ""
    Write-Host "Source repository: $RepoRoot"
    Write-Host "Source commit:     $sourceCommit"
    Write-Host "Destination:       $DestinationRoot"
    if ($archivedTo) {
        Write-Host "Previous 005:      $archivedTo"
    }
    Write-Host ""
    Write-Host "Final structure:"
    Write-Host "  M\Run-01, M\Run-02"
    Write-Host "  L0\Run-01, L0\Run-02"
    Write-Host "  L1\Run-01, L1\Run-02"
    Write-Host "  K0\Run-01, K0\Run-02"
    Write-Host "  K1\Run-01, K1\Run-02"
    Write-Host ""
    Write-Host "No ASSIGNED_CANDIDATE.txt is used."
    Write-Host ""
    Write-Host "Start with:"
    Write-Host "  $DestinationRoot\M\Run-01"
    Write-Host ""
    Write-Host "Initial prompt:"
    Write-Host '  Read `TASK.md` completely and execute the task to completion, including all required inputs, deliverables, and final self-checks.'
}
catch {
    if (Test-Path -LiteralPath $StagingRoot) {
        Remove-Item -LiteralPath $StagingRoot -Recurse -Force
    }
    throw
}
