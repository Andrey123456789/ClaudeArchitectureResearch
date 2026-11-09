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
