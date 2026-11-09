# Task: generate one runtime instruction template

## 1. Goal

Generate a **complete, standalone runtime instruction template** that implements the architecture defined in `CANDIDATE.md`.

This iteration is template generation only.

Do not:

- generate TaskBoard or any other application;
- run a benchmark;
- compare this candidate with other candidates;
- select a winner.

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
## 3. Language requirement


All programming-related and AI-instruction artifacts must be written in **English**.

This includes:

- all generated Markdown;
- Claude / AI instruction files;
- code;
- code comments;
- configuration files;
- scripts;
- technical documentation;
- `GENERATION_REPORT.md`.

Do not generate Russian text in any technical artifact.

The only allowed exception is explicit end-user interface text when a product specification requires a non-English UI. This task provides no such requirement, so the generated template must be English-only.

## 4. Required inputs

Read completely:

1. `CANDIDATE.md`;
2. `source/inventory.json`;
3. `source/shared-research-invariants.json`;
4. the **entire** `source/v2-baseline/` tree.

Use the inputs as follows:

- `source/inventory.json` is the normalized **V2-derived policy oracle**. It defines which accepted V2 policy semantics must be preserved.
- this `TASK.md`, especially Section 7, defines the **shared experimental construction contract** that applies equally to M, L0, L1, K0, and K1;
- `source/shared-research-invariants.json` contains the separately recorded research-added normative constraints. Its `source_refs` are provenance metadata only; do not attempt to recover research files that are intentionally absent from this workspace;
- `CANDIDATE.md` defines the candidate-specific organization, dependency model, ownership model, loading model, and distinguishing constraints;
- `source/v2-baseline/` is the concrete behavioral/content baseline and the source of useful wording, examples, workflows, and technique.

The inventory was created in the research repository, so its `source_refs` use paths beginning with `templates/v2-baseline/`. Inside this isolated workspace, resolve those references by replacing that prefix with `source/v2-baseline/`.

If `CANDIDATE.md` requires a layout different from V2, the V2 layout is not a constraint.

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
- create temporary files, caches, reports, or helper artifacts outside the current run workspace.

Write generated deliverables only under `output/`.

If you need temporary construction/audit material, keep it under `output/.work/` and remove `output/.work/` before final completion.

Before reading or writing a path derived programmatically, ensure its resolved absolute path remains inside the current run workspace. Treat a path that escapes the workspace as invalid even if the operating system permits access.

`output/` must be empty at the start. If it already contains a previous generated template or report, stop and report the problem.

## 6. Contract and conflict handling

All four input roles must be satisfied simultaneously.

- The inventory decides **what V2-derived normative semantics must survive**.
- Section 7 and `shared-research-invariants.json` define **shared construction requirements that must be common across all experimental candidates**.
- `CANDIDATE.md` decides **how this candidate organizes, owns, loads, and composes the instruction system within those shared constraints**.
- V2 supplies **concrete wording, examples, procedures, and technique** that should be preserved when useful.

Do not strengthen, weaken, add, or remove V2-derived normative policy merely because another design seems preferable.

Do not treat a candidate-specific organization choice as permission to violate a shared construction requirement.

If the inputs contain a genuine contradiction that cannot be resolved without changing policy semantics or violating a binding candidate rule, stop and document the contradiction instead of silently choosing one side.

## 7. Shared mandatory properties

These properties apply equally to M, L0, L1, K0, and K1. They are experimental controls, not candidate-specific design choices.

### 7.1 Content equivalence and one normative owner

Every applicable policy in `source/inventory.json` must map to exactly one authoritative normative owner in the generated template.

Every research-added constraint in `source/shared-research-invariants.json` must also have one authoritative runtime owner where runtime ownership is required.

Allowed secondary forms:

- **routing pointer** — a short pointer such as "run workflow X" or "see file Y";
- **check-by-reference** — a short yes/no checklist item that points to the authoritative owner;
- **decision summary** — only inside the candidate's designated decision-summary artifact.

Semantic restatement is forbidden: the same normative rule must not be independently reworded in multiple places.

If the candidate architecture forces a wording or placement delta, preserve the semantics and record the material delta in `GENERATION_REPORT.md`.

Do not carry research policy IDs into runtime artifacts merely for bookkeeping.

### 7.2 Explicit ownership and classification

Every human-readable instruction artifact must begin with a concise one-line classification/ownership header appropriate to the candidate.

At minimum, the header must make ownership/loading understandable. Candidate-specific fields may add level, kind, scope, or capability information where required by `CANDIDATE.md`.

The human-facing instruction map must make it possible to locate the authoritative owner of every policy.

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

A multi-step development/review/verification procedure must live in its workflow owner. Always-loaded policy may contain a short routing pointer to that workflow, but must not carry a second copy of the procedure merely for convenience.

In particular, do not place the full Development Workflow or an equivalent multi-step operating procedure in `CLAUDE.md`. `CLAUDE.md` may expose the governing policy, stop/approval boundary, and a concise pointer telling the model which workflow to run.

Pointers and check-by-reference items may cross these boundaries without becoming duplicate owners.

### 7.4 Stable dependency direction

At minimum:

- normative content may depend only on authoritative owners that load reliably;
- engineering policy must not depend on product, feature, or task inputs;
- product/feature/task inputs may request a decision change but may not silently override engineering policy;
- a skill-private reference is depended on only by its owning skill;
- the graph of conformance dependencies must be acyclic;
- routing pointers are not conformance dependencies and may point in any direction if the target is reliably invocable.

Apply any stricter candidate-specific dependency rules from `CANDIDATE.md`.

### 7.5 Trigger assignment and reliable loading

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

### 7.6 Established E0 mechanics

You may rely on these established facts:

- nested directories under `.claude/rules/` are discovered recursively to at least two levels;
- direct and nested `@` imports work;
- an explicitly imported rule is effectively always-loaded; its `paths:` field does not make that imported copy conditional.

Do not treat other unresolved mechanics as established.

Do not design the candidate around unverified behavior.

### 7.7 Product governance

Preserve the V2 product-governance semantics represented in the inventory, including:

- `SPECIFICATION.md` is authoritative for project-specific observable product behavior when non-empty;
- do not invent observable behavior that product sources do not define;
- string/case-sensitivity/collation/normalization semantics count as observable behavior when externally visible;
- `CUSTOM_SETTINGS.md` stores approved tunable project values and does not override the specification;
- material product ambiguity requires approval;
- feature/task inputs may request an engineering decision but cannot silently rewrite architecture policy.

`SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, optional feature specifications, and task prompts are product/task **inputs**, not instruction layers.

### 7.8 Decision control

Use three decision classes:

- **Decided** — already settled; follow it and do not reopen it without approval;
- **Delegated** — local, reversible, and does not materially change a boundary, dependency, accepted convention, public contract, or observable behavior;
- **Reserved** — changes an accepted architecture/stack/public-behavior decision or is materially expensive to reverse.

Reserved decisions include at least:

1. changing an already accepted project or architecture decision;
2. adopting a new architectural style/pattern such as CQRS, a mediator, Vertical Slice Architecture, event sourcing, or microservices;
3. adding a production project/layer/assembly or changing the project reference graph;
4. changing persistence boundaries or persistence technology;
5. adding a new infrastructure category such as messaging, background processing, distributed cache, search, external storage, or external identity;
6. adding a major library/framework or replacing a baseline technology;
7. introducing a project-wide convention/abstraction that other code is expected to follow;
8. changing authentication/authorization architecture;
9. making a breaking public API change or adopting API versioning;
10. defining product behavior or tunable values not defined by product sources.

For unclear cases, apply this five-question test. Any `yes` makes the decision Reserved:

1. Does it add, remove, or replace a dependency, framework, or infrastructure capability?
2. Does it change a project/layer/reference boundary?
3. Does it establish a convention that other code is expected to follow?
4. Does it change observable behavior or a public contract?
5. Would it be expensive to reverse after other code depends on it?

A Decision Request contains:

- Context;
- Options;
- Recommendation;
- Blocked;
- Proceeding with.

An explicit user instruction may count as approval, but the accepted decision must be recorded through the candidate's decision mechanism.

In an autonomous/headless run, choose only a policy-compliant non-Reserved path. Report unresolved Decision Requests explicitly instead of silently making Reserved decisions.

### 7.9 Decisions available at planning time

Planning-time context must expose:

- adopted architecture;
- architecture styles/patterns explicitly not adopted;
- approved stack;
- conditional technologies;
- project defaults needed to plan work safely.

Where this information lives is candidate-specific.

### 7.10 Shared scope taxonomy and path conventions

Use these scopes:

- `common`;
- `backend`;
- `backend-tests`;
- `frontend`;
- `delivery`;
- `repo/meta`.

Preserve the project layout convention used by the experiment:

- `backend/<Name>.<Layer>/...`;
- `frontend/<Name>.Web/...`.

An inventory policy must apply at least everywhere its declared scope requires.

Every candidate must have path-scoped frontend/Angular normative coverage. Frontend must-policy must not exist only inside the Angular knowledge skill.

### 7.11 Shared workflow and agent set

Provide these workflow responsibilities with consistent semantics across candidates:

- `project-structure` / scaffolding;
- `verify`;
- `code-review`;
- `build-fix`;
- `custom-settings`;
- `git-workflow`;
- `security-scan`;
- `add-dependency`;
- `architecture-decision`;
- `template-maintenance` — user-only; never invoked automatically by the model.

Workflow bodies own procedures, stop conditions, and output shape. They may use check-by-reference items but must not become duplicate normative owners.

Provide a thin `code-reviewer` agent that delegates to/preloads the `code-review` workflow rather than owning a second copy of review criteria.

Candidate-specific references inside workflow steps may differ only where required by the candidate architecture.

### 7.12 Shared knowledge set and skill naming

Preserve useful V2 technique through a common knowledge surface with these skill names where the corresponding content is present:

- `ef-core`;
- `http-api`;
- `aspnet-error-handling`;
- `dotnet-testing`;
- `logging`;
- `httpclient-factory`;
- `configuration`;
- `dependency-injection`;
- `caching`;
- `swagger`;
- `api-versioning`;
- `health-check`;
- `docker`;
- `ci-cd`;
- `angular`;
- `modern-csharp`;
- `authentication`.

Use identical names for materially identical knowledge content across candidates.

Knowledge-skill descriptions must be concise, trigger-first, and use concrete invocation cues rather than generic summaries.

Serilog-specific depth may be a private reference owned by `logging`.

Resilience-specific depth may be a private reference owned by `httpclient-factory`.

Do not create competing standalone `serilog` or `resilience` skills when that would duplicate the shared knowledge ownership model.

Knowledge skills are not the sole owners of normative policy.

### 7.13 Deterministic enforcement

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

### 7.14 Human-facing instruction map

Add a human-facing map of the instruction system that is **not auto-loaded**.

For every instruction artifact, the map must make these fields discoverable:

- file;
- authoritative owner/responsibility;
- scope;
- loading mechanism;
- enforcement;
- extension guidance — where related new content should be added.

Add candidate-specific classification fields required by `CANDIDATE.md`.

The organization of the map is candidate-specific.

### 7.15 Normative vocabulary

Use consistently:

- **must / must not** — violation is a defect;
- **default** — deviation requires a concrete reason and must be reported;
- **prefer / avoid** — guidance;
- **requires approval** — Reserved decision.

Avoid ambiguous words such as `normally` when it is unclear whether Claude may deviate autonomously.

### 7.16 Challenge obligation

Runtime policy must require Claude to identify material concerns in a request — for example duplication, poor cohesion, trigger problems, context cost, architecture conflict, or unnecessary complexity — and propose an alternative before implementing a questionable request.

This obligation does not authorize Claude to silently rewrite or ignore the user's requirement.

### 7.17 Execution parity

Do not hardcode model IDs, effort levels, experiment run IDs, rankings, or benchmark settings inside the runtime template.

Runtime behavior must not depend on knowing which experimental candidate or replicate produced it.

Agent/tool restrictions should be driven by runtime responsibility, not by experiment identity.

### 7.18 Always-loaded budget

Keep the always-loaded surface compact.

The experimental target is roughly **5k tokens including skill listings**, but reliability takes precedence over artificial token minimization.

Do not move critical planning-time policy out of the always-loaded surface merely to hit the target.

Actual context usage is an outcome to measure, not something to equalize by hiding required policy.

### 7.19 Preserve useful V2 behavior

Do not throw away useful V2 technique, examples, workflows, references, or operational detail simply because the inventory is the normative oracle.

Use V2 as the source of concrete non-normative material unless:

- it conflicts with accepted inventory semantics;
- it duplicates an authoritative owner;
- it conflicts with the shared construction contract;
- it conflicts with a binding candidate-specific rule;
- it is obsolete or unusable in the resulting runtime structure.

### 7.20 Research metadata stays out of runtime

`output/template/` must not contain:

- M/L0/L1/K0/K1 as research labels;
- replicate/run identifiers;
- experiment commentary;
- benchmark or metrics material;
- research-only policy IDs;
- references to this workspace;
- references to absent research files;
- `TASK.md`;
- `CANDIDATE.md`;
- `source/`;
- `GENERATION_REPORT.md`.

The result must look like a real production-ready template, not an experiment artifact.

## 8. Candidate binding and design freedom

`CANDIDATE.md` defines the binding candidate-specific architecture.

Its illustrative trees and examples are not literal file-generation scripts unless the file explicitly says otherwise.

Do not drift toward another candidate because it seems cleaner.

If several implementations are equally compliant:

1. choose the simplest one;
2. do not create a file merely for architectural symmetry;
3. do not merge distinct responsibilities merely to reduce file count;
4. do not split a file unless trigger, ownership, dependency, scope, or change-driver concerns justify the split;
5. preserve human inspectability;
6. record a meaningful design choice in `GENERATION_REPORT.md`.

Human readability is a methodology requirement.

A maintainer should be able to understand:

- where policy lives;
- where workflow lives;
- where knowledge lives;
- how to find the authoritative owner;
- how content loads;
- what is enforced mechanically;
- where a new rule belongs.

Do not trade away policy coverage or trigger reliability for superficial simplicity.

## 9. Deliverables

Create only:

```text
output/
├── template/
└── GENERATION_REPORT.md
```

### `output/template/`

A complete standalone runtime instruction template.

It must work after being copied into a future project without access to:

- `source/`;
- `TASK.md`;
- `CANDIDATE.md`;
- this research workspace.

### `output/GENERATION_REPORT.md`

Keep it concise and in English.

Record:

- the implemented candidate model;
- total runtime file count;
- final tree;
- meaningful structural choices where `CANDIDATE.md` allowed freedom;
- policy-preservation concerns, if any;
- intentionally permitted wording/placement deltas;
- unresolved ambiguity, if any;
- broken references found/fixed;
- final self-check result.

Do not assign a quality score.

Do not compare this candidate with another candidate.

## 10. Final acceptance loop

Do not treat this section as a report-only checklist. Execute it against the generated files, repair failures, and rerun the checks until all applicable items pass.

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