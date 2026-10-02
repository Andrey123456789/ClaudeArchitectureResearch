# L1 — Stability-first, Replaceable Capability Modules: Design Notes

> **Research metadata.** This file is not part of any candidate's instruction context (S-19). Never copy it into a template or a benchmark project.

| | |
|---|---|
| Candidate | **L1**: Stability-first with replaceable capability modules |
| Axis A | A-L: stability-first (identical level model to L0) |
| Axis B | B1: replaceable capability modules |
| Passport | `research/candidates/L1/CORE_FEATURES.md` |
| Shared invariants | S-01…S-19, defined in `research/observations/002-candidate-space-analysis.md` §2 (hereafter "002") |
| Shared B1 definitions | 002 §3.2 vocabulary, §3.3 contract format, §3.5 composition, §7.4 binding rule, §7.5 slot set. **Identical in K1.** |
| Distinguishing predicates (002 §3.4) | P-01, P-02, P-03, P-09…P-14 **yes**; P-08 yes; P-04…P-07 **no** |
| B0 sibling | L0. Read `research/candidates/L0/DESIGN.md` first; this file describes only the differences. |
| Status | Design only. Illustrative trees, not final files. |

---

## 1. Definition: L1 = L0 + T<sub>cap</sub>(slot set)

L1 keeps **everything** in L0:

- the four levels, their order and the inputs outside them;
- the level-assignment test;
- the level and neutrality rules (P-01…P-03);
- the placement of all content outside the slot set.

L1 differs from L0 **only** by applying the capability transformation T<sub>cap</sub> to the four agreed slots (002 §7.5: `architecture`, `persistence`, `backend-testing`, and the optional `frontend`). P-14 makes this checkable: diff L0 and L1, ignore the slot content, and the remainder must be empty apart from logged glue.

**T<sub>cap</sub>, step by step, for each slot:**

1. **Identify slot content.** Find every inventory item that is specific to the current implementation (NUnit, EF Core with SQL Server, Clean Architecture, Angular).
2. **Separate the implementation-independent policy** of the concern, for example test levels or the data-access boundary. It stays exactly where L0 placed it. Usually that is level 0 or 1, which is already neutral because of P-03.
3. **Re-own** the implementation-specific content as **facets** of a module `<slot>/<impl>`.
   - Each facet **stays at the level L0 gave it.** A module may therefore contribute facets at several levels.
   - Facet files are renamed by slot and facet role, not by implementation (002 §3.5, facet naming rule).
4. **Neutralize consumers.**
   - Outside the module, replace mentions of the implementation with the slot or facet name.
   - Neutralize only what is *implementation-specific*. Commands shared by all realistic implementations stay concrete: `dotnet test` works for NUnit and xUnit alike.
5. **Write the contract** in the shared format (002 §3.3) and the module manifest.
6. **Add the selection entry** to `3-project/decisions.md`.
7. **Log every wording change** as a permitted delta (S-01).

---

## 2. Levels in L1: where contracts, frames and leaves sit

| Level | L0 content | L1 changes |
|---|---|---|
| 0 Core | Unchanged | None. Core never named a technology (P-03). |
| 1 Architecture | Clean Architecture policy | **Frame slot.** The level now holds (a) the **role vocabulary and role-level invariants**, which are the runtime-visible part of the `architecture` contract, and (b) the facets of `architecture/clean-architecture`: the role-to-type mapping, layers, persistence-boundary *placement*, entry points, patterns not adopted, layout roles. The facets keep their level-1 placement. |
| 2 Technology | Technology modules | Slot technologies (EF Core, NUnit, Angular) become **leaf modules**. Their level-2 facets are written against **role names** (the binding rule, 002 §7.4). Technologies outside the slot set (C#, ASP.NET Core, FluentValidation, Serilog, containers and CI) **stay embedded modules, unchanged from L0.** |
| 3 Project | Selection and defaults | Gains the **selection record** (slot → implementation, provider variant). Layout facets owned by the frame stay here. The data-lifecycle *policy* (seed in Development when empty) is not specific to an implementation, so it stays outside any module. The seeding *mechanism* becomes a `persistence` facet. |

**Dependency rules added by L1**, on top of P-02 and P-03:

- **Leaf → frame.** A leaf facet may depend on the *role vocabulary* (contract, level 1), but **not** on the frame implementation's terms. So the EF Core module says "commit boundary", not "`IUnitOfWork`".
- **Leaf → leaf.** No direct dependency between implementations. If one is unavoidable, declare it as `binds:` in both manifests, and count it as coupling.
- **Consumer → slot.** Outside a module, artifacts reference slots and facet roles, never implementations (the leak check, P-11).

---

## 3. Slot facets per level (expected)

| Module | Level 1 | Level 2 | Level 3 | Workflow facets | Assets / enforcement |
|---|---|---|---|---|---|
| `architecture/clean-architecture` (frame) | role mapping (always, in `overview.md`), layers, boundary placement, entry points, outcome placement, patterns not adopted | — | layout roles: projects, test-project placement | scaffold: create projects and references | **neutral** architecture-check specification (reflection) |
| `persistence/ef-core` (+ variant `sqlserver`) | — | persistence-technology rule (EF types are persistence-framework types; how to implement the commit boundary and the persistence-access role); migrations | variant: provider package, development connection default (LocalDB), **declared properties**: default string comparison, case sensitivity of uniqueness, migration mechanism | build-fix and verify notes for migrations; scaffold: provider setup | deny-list: EF InMemory for relational tests |
| `backend-testing/nunit` | — | test-framework rule (attributes, lifecycle, parallelism, test host) | test packages | scaffold: test-project templates | **adapter** that runs the neutral architecture checks as NUnit tests |
| `frontend/angular` (optional) | — (the neutral `frontend-structure.md` stays outside the module) | Angular rule; `angular` knowledge skill | Angular selection: Material, Vitest, zoneless | verify and scaffold: `ng` commands | — |

Knowledge skills owned by modules keep their shared names (S-12: `ef-core`, `dotnet-testing`, `angular`). Their descriptions carry the implementation's trigger cues (002 §3.5).

---

## 4. Expected directory and artifact organization

Illustrative tree, showing only what differs from L0. The composition strategy is CS-1, in place with manifests (002 §3.5, §13 Q5).

```text
<template root>/
├── CLAUDE.md                                  0   as L0
└── .claude/
    ├── MAP.md                                 not loaded; by level, plus a capability view (slot → facets by level)
    ├── capabilities/                          maintainer-only, never loaded
    │   ├── architecture/CONTRACT.md           frame; roles; declared properties; conformance
    │   ├── architecture/clean-architecture/MODULE.md      lists its facet files (levels 1 and 3, workflow steps, assets)
    │   ├── persistence/CONTRACT.md            leaf; required facets: commit boundary, migrations, seeding mechanism
    │   ├── persistence/ef-core/MODULE.md      variants: sqlserver
    │   ├── backend-testing/CONTRACT.md
    │   ├── backend-testing/nunit/MODULE.md
    │   ├── frontend/CONTRACT.md               optional slot
    │   └── frontend/angular/MODULE.md
    ├── rules/
    │   ├── 0-core/                            = L0
    │   ├── 1-architecture/
    │   │   ├── overview.md                    always   role vocabulary (contract, runtime part) + CA mapping and patterns
    │   │   │                                           not adopted (facet: architecture/clean-architecture)
    │   │   ├── backend-layers.md              facet: architecture/clean-architecture
    │   │   ├── persistence-boundary.md        facet: architecture/clean-architecture (placement only)
    │   │   ├── entry-points.md                facet: architecture/clean-architecture
    │   │   ├── outcomes.md                    = L0 (not specific to an implementation)
    │   │   └── frontend-structure.md          = L0 (neutral frontend policy, outside any module)
    │   ├── 2-technology/
    │   │   ├── csharp.md, aspnet-core.md, fluentvalidation.md, containers-ci.md     = L0 (embedded)
    │   │   ├── persistence-technology.md      facet: persistence/ef-core          (was ef-core.md in L0)
    │   │   ├── test-framework.md              facet: backend-testing/nunit        (was nunit.md in L0)
    │   │   └── frontend-framework.md          facet: frontend/angular             (was angular.md in L0)
    │   └── 3-project/
    │       ├── decisions.md                   always   = L0 + selection record:
    │       │                                           architecture → clean-architecture · persistence → ef-core (sqlserver)
    │       │                                           · backend-testing → nunit · frontend → angular
    │       ├── layout.md                      facet: architecture/clean-architecture (layout roles)
    │       ├── persistence-provider.md        facet: persistence/ef-core#sqlserver (declared properties, dev defaults)
    │       └── data-lifecycle.md              = L0 (policy); the mechanism moves to the persistence facet
    ├── skills/                                shared set (S-11, S-12). Module-owned skills carry a `Capability:` header.
    │                                          Workflows reach implementation-specific steps through facet roles (P-13).
    └── assets/ (scaffold)                     architecture-checks (neutral, frame) + test adapter (backend-testing facet)
```

**Expected size:** about 60–75 runtime instruction files, plus 4 contracts and 4 module manifests.

---

## 5. Ownership model

1. **Slot content** belongs to the module of its implementation. Within the module, each facet keeps its L0 level.
2. **Everything else** belongs to the same owner as in L0 (P-14).
3. **Binding content** follows the binding rule (002 §7.4): placement goes to the frame, technique to the leaf, and anything left over to the dependent slot, with `binds:`.
4. Every runtime file shows its owner in its header: `Level: … · Capability: <slot>/<impl>` or `Capability: —`. The map has two views, by level and by capability.

---

## 6. Loading strategy

- **Facets keep the trigger class their content had in L0** (S-09). A replacement module must provide facets with the same trigger classes. That is part of conformance.
- **Contracts and manifests are never loaded.** Claude sees the selection record (always), the role vocabulary (always, in the overview) and the facets (by their triggers).
- **Workflows reach implementation-specific steps through facet roles.** Example: "for the `backend-testing` slot, read its test-framework facet". This adds a hop (002 §9).

  **Open alternative:** substitute concrete values at composition time, so the runtime text names the implementation while the source text stays neutral. The decision waits on 002 §14 E1 (§13 Q5).

---

## 7. Responsibilities of skills, rules and references

These are the same as in L0, with these additions:

- **Facet rules** carry the implementation's must-rules at their level.
- **Facet knowledge skills** carry the implementation's technique. Their names are shared, and their descriptions are owned by the implementation.
- **Workflow facets** are sections or small files that workflows read through the facet role. Examples: the test-project templates for scaffolding, and the migration commands for build-fix.
- **References** stay private to one skill. A module may own a skill, and with it that skill's references.

---

## 8. Project decisions

- The **selection record** is a section of `3-project/decisions.md` (always loaded). Changing it is Reserved (R-1, R-6) and goes through `architecture-decision`.
- **Declared properties** of the selected implementations (002 §7.6), for example the default string-comparison semantics, appear in the Project-level provider facet. A change to one is a product decision (S-08).
- **Secondary decisions.** A replacement that leaves a required facet unfilled (Dapper has no migration mechanism) fails conformance, and turns into a Decision Request for the missing choice.

---

## 9. How feature and task inputs interact with policy

The same as L0 (S-08, S-06). In addition: a feature that needs a slot that is not selected (for example, the first frontend in a backend-only project), or that needs a different implementation, triggers a Decision Request. It is never satisfied by writing ad-hoc instructions.

---

## 10. Replacement and extension procedure

| Task | Procedure in L1 |
|---|---|
| Replace an implementation (CI-4 to CI-7) | 1. ADR and Decision Request. 2. Write or obtain the new module against the contract. The content comes from the shared pool (002 CF-10). 3. Remove the files listed in the old manifest, add the new ones. 4. Update the selection record. 5. Run S2 (conformance, leak check, P-01…P-03). 6. Run the slot's trigger tests. 7. Run a behavioral smoke task. |
| Add a provider variant | A new variant inside the persistence module, with declared properties. Switching is a selection change. |
| Add a new slot (e.g. `authentication`) | Check the criteria (002 §7.1), then write the contract, the first module and the selection entry; record the decision. |
| Add an embedded technology | Exactly as in L0 (a level-2 module, a level-3 selection). It is not a slot unless the criteria say so. |
| A new project rule | `3-project/` as in L0, unless it is specific to an implementation, in which case it goes into that module's level-3 facet |

---

## 11. Structural conformance (what S2 checks for L1)

- Everything L0 checks: P-01, P-02, P-03, the shared checks.
- **P-09**: one contract per slot in the agreed set.
- **P-10**: every runtime file whose header carries `Capability:` is listed in exactly one manifest, and every manifest entry exists.
- **P-11**: leak check. Implementation names (taken from the manifests) do not appear outside their module, the selection record or the declared-property facet.
- **P-12**: the selection record names exactly one implementation per required slot, and the selected modules satisfy their declared `requires`.
- **P-13**: workflows reach implementation-specific steps only through facet roles.
- **Facet-trigger parity**: each facet's trigger class equals the one its contract requires.
- **P-14**: a diff against L0 is part of the generation review, not of S2.

---

## 12. Important risks

| Risk | Detail | Indicator or test |
|---|---|---|
| Role vocabulary weakens generation | Leaves say "commit boundary" where L0 said `IUnitOfWork` | 002 §14 E1; violations on persistence tasks compared with L0 |
| Indirection in workflows | Extra hops to facet files | Tokens and tool calls per verify run compared with L0 |
| The frame contract does not fit VSA | VSA may have no separate persistence-access contract or commit boundary | CI-7: a contract revision is needed. Record it as a finding, not a failure. |
| A facet drops out silently | The new module omits a required facet | Conformance (P-10, facet parity); 002 §14 E7 |
| Contracts drift | Contracts edited more often than expected | Contract revisions per change-impact task |
| Binding growth | Every new frame implementation multiplies bindings | Count of `binds:` |
| Overhead with no benefit on ordinary tasks | The benefit appears only in replacement tasks | Behavioral suite: L1 compared with L0 (non-inferiority) |
| Convergence with L0 at runtime (002 CV-7) | With one implementation per slot, runtime differences are small | Structural distance; report it |

---

## 13. Leakage watchlist: signs that an implementation is no longer L1

- **Toward L0:**
  - implementation names outside modules (P-11 fails);
  - workflows naming NUnit or EF Core directly;
  - no contracts, or contracts that no check enforces.
- **Toward K1:** rule directories by scope or kind; a single cross-level register; `Kind:` headers.
- **Beyond the definition:**
  - slots outside the agreed set (for example, turning Serilog into a capability);
  - several implementations shipped at runtime (dynamic selection);
  - non-slot content changed relative to L0 (P-14).
