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
