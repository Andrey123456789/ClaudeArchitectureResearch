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
