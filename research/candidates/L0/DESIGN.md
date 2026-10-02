# L0 — Stability-first, Embedded Capabilities: Design Notes

> **Research metadata.** This file is not part of any candidate's instruction context (S-19). Never copy it into a template or a benchmark project.

| | |
|---|---|
| Candidate | **L0**: Stability-first with embedded capabilities |
| Axis A | A-L: stability-first |
| Axis B | B0: embedded capabilities |
| Passport | `research/candidates/L0/CORE_FEATURES.md` |
| Shared invariants | S-01…S-19, defined in `research/observations/002-candidate-space-analysis.md` §2 (hereafter "002") |
| Distinguishing predicates (002 §3.4) | P-01, P-02, P-03 **yes**; P-08 yes; P-04…P-07 and P-09…P-13 **no** |
| B1 sibling | L1 (= L0 plus the capability transformation on the slot set; P-14) |
| Status | Design only. Illustrative trees, not final files. |

---

## 1. The level model

### 1.1 Levels

Every instruction artifact has exactly one **level**. The levels are totally ordered, from the most fundamental and stable to the most specific and volatile.

| Level | Contains | May name | Changes when | Changed by |
|---|---|---|---|---|
| **0 Core** | Operating policy: precedence, decision control, product governance, completion contract, challenge obligation, Git safety. Engineering principles: simplicity, proportional complexity, behavior preservation. **Technology-neutral** principles for testing, security, logging, dependency hygiene and error exposure. | Product input files and workflow names (routing only) | Almost never | Template maintainers |
| **1 Architecture** | The adopted architecture (Clean Architecture): layer model and reference direction, domain style, use-case orchestration, entry-point responsibilities, the persistence-boundary pattern (repositories, Unit of Work), composition root, code organization and naming by role, outcome-versus-exception policy, frontend structure and data-access boundary, cross-stack contract authority, patterns not adopted. | Architecture concepts, plus the **platform** (.NET solution, project and assembly; TypeScript modules) | When the system is re-architected | Humans, via ADR |
| **2 Technology** | One **module per technology or technology cluster**: C#/.NET conventions (async, cancellation, TimeProvider); ASP.NET Core (Controllers, ProblemDetails, default status codes, Swagger in Development only); EF Core with the SQL Server provider; FluentValidation; Serilog; NUnit with WebApplicationFactory; Angular with Vitest and Material; Docker; CI. | Its own technology and those it integrates with, plus everything in levels 0–1 | On upgrade or replacement | Template maintainers; projects via ADR |
| **3 Project** | Project decisions and defaults: the approved stack and conditional technologies (the *selection*), repository layout and project naming (`<Name>.<Layer>`), test-project placement, the Development data lifecycle (seed when empty, Development only), the development environment, rules the project adds, and the workflows that rely on any of these. | Everything below | Per project, often | The project team, via ADR |
| *Inputs* (not a level) | `SPECIFICATION.md`, `CUSTOM_SETTINGS.md`, feature specs, task prompts | — | Constantly | Product owner or user |

**Why Project sits above Technology.** Technology modules are reusable knowledge of *how* to use a technology. The Project level records *which* technologies this project uses, and how this project arranges itself. A team changes the second far more often than the first. The tension 001 found (H-2: selection vs knowledge) is resolved in L0 by putting selection at level 3 and knowledge at level 2.

**The platform assumption.** The template's platform (.NET with C#, and TypeScript for the frontend) is fixed (it fails gate G2 in 002 §7.1). Levels 0 and 1 may therefore talk about projects, assemblies and references. They may not name any other technology (P-03).

### 1.2 Assigning a level

For each statement, apply these tests in order. **The level is that of the most volatile thing the statement depends on.**

1. Does it depend on project-specific selection, layout, naming or defaults? → **3 Project**
2. Does it name a technology other than the platform? → **2 Technology**
3. Does it presuppose the adopted architecture (layers, roles, boundaries)? → **1 Architecture**
4. Otherwise → **0 Core**

**Mixed statements are split.** Each part goes to its own level, and the more volatile part depends on the more stable part. Example (V2 `rules/architecture.md:28-29`, "Keep Domain free of EF Core, ASP.NET Core, HTTP, persistence…"):

- Level 1: "Domain references no persistence framework, web framework or transport types."
- Level 2 (EF Core module): "EF Core types (`DbContext`, `DbSet<T>`, EF attributes, configuration types) are persistence-framework types."
- Level 2 (ASP.NET Core module): "ASP.NET Core and HTTP types are web-framework and transport types."

Each such split is recorded in the permitted-delta log (S-01). Whether the neutral form harms generation is open: 002 §14 E2 tests it.

**Workflows** get a level like everything else. A workflow names concrete commands and layouts directly (that is what "embedded" means), so it usually sits at level 2 or 3. Core may still *route* to a workflow by name (S-05). Core owns each workflow's one-line guarantee, for example "`verify` builds, tests and reports what was not run".

---

## 2. Expected directory and artifact organization

Illustrative tree. Level numbers are shown as directory prefixes for rules. Skills share a flat namespace (assumed; 002 §14 E0), so their level appears in their header and in the map.

```text
<template root>/
├── CLAUDE.md                         0  always   operating policy, engineering principles, completion contract, workflow map
│                                                 (routing), precedence and decision control [S-06, S-08, S-16]
│                                                 @.claude/rules/1-architecture/overview.md
│                                                 @.claude/rules/3-project/decisions.md
├── SPECIFICATION.md, CUSTOM_SETTINGS.md     inputs
├── .editorconfig, Directory.Build.props, Directory.Packages.props, docs/decisions/   [S-13, S-07]
└── .claude/
    ├── MAP.md                        not loaded; organized by level, then module  [S-14]
    ├── settings.json, hooks/, scripts/      package E [S-13]
    ├── rules/
    │   ├── 0-core/
    │   │   ├── testing-principles.md         paths: backend tests, frontend specs   test levels, determinism, isolation, naming
    │   │   ├── security-principles.md        paths: code, config, containers        secrets, sensitive data, error exposure, TLS
    │   │   ├── logging-principles.md         paths: backend code                    structured, levels, no secrets, log once
    │   │   └── dependency-hygiene.md         paths: manifests                       stable versions, lockfiles, licenses (normative)
    │   ├── 1-architecture/
    │   │   ├── overview.md                   always (imported)   adopted architecture D-01…D-08, patterns not adopted,
    │   │   │                                                     architecture-specific reserved items (→ R-x in Core)
    │   │   ├── backend-layers.md             paths: backend/**   layers, reference direction, responsibilities, composition root,
    │   │   │                                                     naming by role
    │   │   ├── persistence-boundary.md       paths: Domain, Application, Infrastructure   repositories, Unit of Work, boundary
    │   │   ├── entry-points.md               paths: Api/**       thin entry points, outcome → response, contract authority
    │   │   ├── outcomes.md                   paths: backend/**   outcomes vs exceptions, central handling, validation boundaries
    │   │   └── frontend-structure.md         paths: frontend/**  feature structure, data-access boundary, no backend Domain types,
    │   │                                                         guards ≠ security, when to escalate state management
    │   ├── 2-technology/
    │   │   ├── csharp.md                     paths: backend .cs                     conventions, async, cancellation, TimeProvider
    │   │   ├── aspnet-core.md                paths: Api/**, Program.cs              Controllers, ProblemDetails, default status codes,
    │   │   │                                                                        Swagger in Development only
    │   │   ├── ef-core.md                    paths: Infrastructure/**, Program.cs, Migrations   EF types as persistence-framework
    │   │   │                                                                        types, migrations, SQL Server provider specifics
    │   │   ├── fluentvalidation.md           paths: Application/**, Api/**
    │   │   ├── nunit.md                      paths: backend tests                   framework conventions, test hosts
    │   │   ├── angular.md                    paths: frontend/**                     standalone, Signals/RxJS, Material, Vitest
    │   │   └── containers-ci.md              paths: Dockerfile*, CI yaml
    │   └── 3-project/
    │       ├── decisions.md                  always (imported)   approved stack and conditional technologies (D-09…D-23),
    │       │                                                     project defaults
    │       ├── layout.md                     paths: *.slnx, *.csproj, angular.json   repository layout, project naming,
    │       │                                                     test-project placement
    │       └── data-lifecycle.md             paths: Infrastructure/**, Program.cs    seed in Development when empty,
    │                                                             seed co-change, no automatic Production migration
    ├── skills/   (shared set, S-11 and S-12; level in header)
    │   │  level 0:  architecture-decision, custom-settings, template-maintenance (user only)
    │   │  level 2:  ef-core, http-api, aspnet-error-handling, dotnet-testing, logging (+serilog ref), httpclient-factory
    │   │            (+resilience ref), configuration, dependency-injection, caching, swagger, api-versioning, health-check,
    │   │            docker, ci-cd, angular, modern-csharp, authentication, add-dependency, security-scan, git-workflow
    │   │  level 3:  project-structure, verify, code-review, build-fix
    └── agents/code-reviewer.md       level 3 (inherits from code-review)
```

The file names and splits are illustrative. The binding properties are:

- level-first directories;
- several cohesive modules per level (L0 is **not** "one file per layer");
- technology modules at level 2;
- selection and project defaults at level 3.

**Expected size:** about 55–65 runtime instruction files. There are more rule files than in K0, because a statement with one trigger may be split across levels.

---

## 3. Dependency direction

```text
Inputs ──(may request changes to)──► 3 Project ──► 2 Technology ──► 1 Architecture ──► 0 Core
                                         │              │  ▲ (same-level references allowed,
                                         │              └──┘  e.g. ef-core → aspnet-core)
                                         └──────────────────────────────────────────────►
```

- **Level rule (P-02).** A *conformance dependency* may point only to the same level or a more stable one. Level 1 may not say "as EF Core requires…". Level 2 may say "within the persistence boundary of level 1…".
- **Neutrality rule (P-03).** Levels 0 and 1 name no technology beyond the platform.
- **Routing pointers** may point upward (S-05). Examples: Core's "run `verify`", and a level-1 rule's "Related skills: ef-core".
- **Same-level references** are allowed between technology modules that integrate (EF Core ↔ SQL Server specifics, NUnit ↔ ASP.NET Core test host), and between project files.
- **Coverage rule.** A level-2 statement that makes a level-1 constraint concrete must be path-scoped *at least as broadly* as that constraint. Otherwise the concrete form is missing while the neutral form loads (002 §9).

---

## 4. Ownership model

- **The owner is chosen by level first, then by topic module within the level.**
- An inventory item that mixes levels is split (§1.2). Each part has its own owner. The split is logged as a permitted delta.
- Within a level, modules are cohesive by topic (level 1) or by technology (level 2). **A technology's level-2 content lives in one module**. This is L0's practical advantage for technology changes compared with K0 and M.
- The map is organized by level, then by module. For every inventory item it records the owner and, for split items, its sibling parts.

---

## 5. Loading strategy

Loading follows the shared trigger assignment (S-09). The level does not decide the mechanism. Each level uses several mechanisms:

| Level | Always | Path | Hook | Workflow step | On-demand knowledge |
|---|---|---|---|---|---|
| 0 Core | `CLAUDE.md` | principle rules | H1–H4 messages name Core owners where relevant | — | — |
| 1 Architecture | `overview.md` | layer, boundary and entry-point rules | — | scaffold reads them explicitly | (none planned) |
| 2 Technology | — | technology rules | — | verify and build-fix name the commands | technology skills |
| 3 Project | `decisions.md` | layout and data-lifecycle rules | H4 (seed co-change) names `data-lifecycle.md` | project workflows | — |

**Expected effect:** one backend edit loads Core, Architecture and Technology rules together. That means more files than in K0, at a similar total token count. 002 §14 E4 tests whether splitting by level affects adherence.

---

## 6. Responsibilities of skills, rules and references

| Mechanism | Responsibility in L0 |
|---|---|
| `CLAUDE.md` | Level 0 operating policy, plus imports of the always-loaded summaries for levels 1 and 3 |
| Rules | Normative constraints at their level. At levels 0 and 1, technology-neutral wording. "Related skills" footers. |
| Workflow skills | Procedures at the level of their most volatile content. They name commands and layouts directly (embedded). |
| Knowledge skills | Technique, usually level 2. Never the only carrier of policy (S-09). |
| References | Depth private to one skill |
| Agent | Execution context; preloads `code-review` |

---

## 7. Project decisions

- **The decisions are stratified across levels:**
  - architecture decisions (D-01…D-08) and patterns not adopted → `1-architecture/overview.md`;
  - stack and project defaults (D-09…D-23) → `3-project/decisions.md`.

  Both are always loaded (S-07), and the IDs are shared.
- **Reserved classes and the protocol** live in Core (`CLAUDE.md`, S-06). The *architecture-specific* reserved items ("introducing CQRS", "Vertical Slice Architecture") are listed in the Architecture overview and point to the R-classes.
- **Changing a decision.** `architecture-decision` writes an ADR to `docs/decisions/`, edits the always-loaded summary at the decision's level, then edits that level's dependents. The map lists dependents by level, and a change can affect only the same level or more volatile ones (P-02).
- **Technology replacement** (embedded):
  - edit the level-2 module;
  - edit the selection at level 3;
  - edit every workflow that names the technology;
  - edit the scaffold assets.

  There is no slot, contract or selection mechanism.

---

## 8. How feature and task inputs interact with policy

- Inputs sit **outside** the hierarchy. They depend on every level and are depended on by none (S-05b).
- A feature spec may *request* a change at any level. The change follows the decision protocol at that level, with an ADR. It never takes effect silently (S-06, S-08).
- Tasks do not create levels. Requirement 4.1's "Feature" and "Task" layers are deliberately excluded (001 H-3).

---

## 9. Expected extension points

| To add or change | Expected edits in L0 |
|---|---|
| A project rule | `3-project/<topic>.md` (with `paths`), plus a map row |
| A technology | A new level-2 module (rule and/or knowledge skill), a selection entry in `3-project/decisions.md`, workflows that must run it, a map row |
| A decision | An ADR, plus the summary at the decision's level, plus dependents at the same or higher levels |
| An architecture principle | Level 1, technology-neutral. Concrete bindings go into the level-2 modules. |
| A frontend concern | `1-architecture/frontend-structure.md` (neutral) or `2-technology/angular.md` (Angular-specific) |
| Replace a leaf technology | Mostly local to the level-2 module, plus the level-3 selection, plus workflows and assets (about 5 files for NUnit → xUnit, 002 §11) |
| Replace the architecture | All of level 1, plus every level-2 module that uses its terms, plus project layout and scaffold (about 12–15 files) |

---

## 10. Structural conformance (what S2 checks for L0)

- The shared checks (see M DESIGN §10).
- **P-01**: every instruction file has a `Level:` header, and rule files sit in the matching `rules/<n>-<level>/` directory.
- **P-02**: conformance references go to the same or a lower level number. Reference lines are tagged (for example `Depends on:`) so they can be told apart from routing pointers.
- **P-03**: a deny-list of technology names (the stack in `decisions.md`) must not appear in levels 0 and 1, except in "Related skills" routing lines.
- **Absence checks**: no contracts, manifests or selection record (B1); no kind or scope directories (K).

---

## 11. Important risks

| Risk | Detail | Indicator or test |
|---|---|---|
| Arguments over level assignment | Seeding policy (Technology or Project?), "no automatic Production migration" (Core or Project?), HTTP status defaults (Technology or Architecture?) | Disagreements during generation; CI-1 placements |
| Neutral wording weakens generation | P-03 replaces concrete names with categories | 002 §14 E2 |
| More files per trigger | Splitting by level separates content that shares a trigger | Files and tokens per task in the trigger suite; E4 |
| Decisions split across files | Planning depends on two imports | E3; behavioral item 2 in 001 §11.3 |
| Over-abstraction | Authors write neutral text that nothing binds to | Level-0/1 sentences with no binding at level 2 |
| Frame replacement is still large | Level 1 *is* Clean Architecture | CI-7 |
| Workflows end up at level 3 | Embedding concrete commands makes most workflows volatile | Not a defect, but humans may find it surprising; document it in the map |
| Convergence with K0 (002 CV-5) | K0's "split by rate of change" approximates levels | Structural distance (002 §12.2) |

---

## 12. Leakage watchlist: signs that an implementation is no longer L0

- **Toward L1:**
  - a slot or contract file;
  - a selection record that drives which files exist;
  - workflows that enumerate "each technology module's steps" generically instead of naming them (P-13);
  - consumer-neutral rewording beyond what P-03 requires.
- **Toward K:**
  - rule directories by scope or kind;
  - a single cross-level decision register;
  - `Kind:` headers.
- **Toward M:** level directories dropped, or levels used only as labels without the P-02 and P-03 checks.
