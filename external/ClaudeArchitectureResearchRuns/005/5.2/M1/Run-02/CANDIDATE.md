# Candidate M1 — Minimal Modular + Replaceable Capabilities

## 1. Core idea

M1 tests the controlled hypothesis:

> Replaceable capabilities may provide useful substitution boundaries without requiring the Stability-first or Kinds × Scopes meta-architectures.

M1 = **M + the same four replaceable capability slots used by L1/K1**.

Everything outside those slots remains Minimal Modular and V2-lineage-driven. If the capability transformation were removed, the result should reduce conceptually to Candidate M.

This fills the missing experimental matrix cell:

- M = Minimal Modular + embedded implementations;
- M1 = Minimal Modular + replaceable capabilities;
- L0 = Stability-first + embedded implementations;
- L1 = Stability-first + replaceable capabilities;
- K0 = Kinds × Scopes + embedded implementations;
- K1 = Kinds × Scopes + replaceable capabilities.

The primary controlled comparison is **M ↔ M1**.

## 2. Minimal Modular base remains binding

Preserve M's conservative design: keep V2's mental model and fix concrete defects rather than reorganizing for architectural elegance.

Every non-capability runtime artifact must remain explainable through V2 lineage. Allowed changes remain Keep, Fix in place, Split, Merge, Move, or New only when a shared requirement or one of the four capability boundaries genuinely requires it.

Do not reorganize non-slot content merely because capability modules exist.

## 3. What M1 intentionally does not introduce

Do not introduce:

- stability levels or `Level:` classification;
- Core → Architecture → Technology → Project as the primary hierarchy;
- Kinds × Scopes or `Kind:` classification;
- K scope-first rule directories or a K-style single decision register;
- L-style stratified decisions;
- capability slots beyond the four agreed slots;
- dynamic plugin discovery or runtime implementation selection;
- multiple active implementations for one slot;
- technology-neutral rewriting of unrelated non-slot content merely for future replaceability;
- broad reorganization not justified by V2 defects, shared requirements, or capability boundaries.

M1 must remain recognizably M outside the capability subsystem.

## 4. Capability model

Add exactly four experimental slots:

1. `architecture` — required **frame**, initial implementation `clean-architecture`;
2. `persistence` — required leaf, initial implementation `ef-core`, provider variant `sqlserver`;
3. `backend-testing` — required leaf, initial implementation `nunit`;
4. `frontend` — optional leaf, initial implementation `angular`.

All other concerns remain embedded.

## 5. Capability structure and static composition

Each slot has:

- maintainer-facing `CONTRACT.md`;
- selected implementation;
- implementation manifest `MODULE.md`;
- runtime facets owned by the selected implementation;
- an always-loaded selection record;
- structural leak/conformance checking.

Composition is static:

- each required slot has exactly one selected implementation;
- the optional slot has zero or one;
- unselected implementations do not appear in runtime context;
- dynamic runtime selection is forbidden.

Contracts/manifests are maintainer metadata and are not auto-loaded in normal code-generation sessions unless a maintenance/replacement workflow explicitly needs them.

Runtime facets may physically live in M's normal flat rule/skill/workflow locations. `MODULE.md` ties those facets to the module. Do not duplicate normative text merely to make a module self-contained.

## 6. Ownership precedence

Classify content in this order:

1. **Capability check:** if content is implementation-specific to one of the four slots, the selected module owns it.
2. Otherwise use normal M ownership and V2 lineage.
3. If V2 contains competing copies, choose the owner whose trigger/loading matches when the policy is needed.

Capability is an added replacement boundary, not a replacement for M's ownership model.

Implementation-owned runtime facets declare:

```text
Capability: <slot>/<implementation>
```

Do not force `Capability: —` metadata onto unrelated M artifacts.

## 7. Rules and loading

Keep M's flat topical rule organization. Capability-specific rule facets may also live in the flat rule directory, using role-based names when externally referenced, for example:

```text
architecture-style.md
persistence-technology.md
test-framework.md
frontend-framework.md
```

Do not create level-first or scope-first rule trees.

Use the same loading model as M:

- always-loaded: `CLAUDE.md`, M planning-time decision imports, and the capability selection record;
- path-loaded: flat rules;
- hook: deterministic process/co-change enforcement;
- explicit workflow read: greenfield/review/verify cases where path loading may not have happened;
- on-demand: knowledge skills;
- maintainer-only: capability contracts/manifests except during capability maintenance.

Preserve every frozen inventory `trigger_class`.

## 8. Stable vocabulary and leak rule

Outside a capability implementation and its explicit allow-list, artifacts may refer to:

- slot name;
- facet role;
- stable role vocabulary exposed by the slot contract;
- selected implementation in designated selection metadata;
- declared observable properties that belong in selection/decision metadata.

Do not hardcode the selected implementation name elsewhere merely because it is currently selected.

Allowed exceptions are the selection record, declared properties, concrete trigger cues in a module-owned knowledge skill, and the module's own manifest/header.

Facet file names used externally are role-based: `test-framework.md`, not `nunit.md`.

External workflows refer to facet roles instead of selected implementation names when the contract provides such a role.

This leak rule applies only to the four capability slots. Do not neutralize unrelated embedded M content.

## 9. Architecture is the frame capability

`architecture` is not an ordinary leaf.

Its contract defines stable architectural role vocabulary such as use-case unit, persistence-access contract, commit boundary, entry point, composition root, and test-project role.

The selected `architecture/clean-architecture` frame:

- maps those roles to Domain/Application/Infrastructure/Api;
- owns placement;
- owns Clean Architecture-specific layout and patterns-not-adopted;
- supplies the architecture-check specification/facet.

Leaf capabilities should bind to stable roles rather than hardcoding frame implementation details whenever possible.

Binding rule:

> Placement belongs to the frame; technique belongs to the leaf.

Examples:

- commit-boundary placement → architecture frame;
- `SaveChangesAsync`/DbContext technique → persistence/ef-core;
- test-project placement → architecture frame;
- NUnit attributes/adapter/commands → backend-testing/nunit.

If a leaf cannot express an integration through stable roles, the dependent module explicitly declares `binds:` coupling.

## 10. Persistence capability

The persistence contract requires explicit facets/properties for:

- persistence access / commit-boundary binding;
- migration mechanism;
- seeding mechanism;
- provider variant;
- observable string-comparison / case-sensitivity semantics;
- relational testing expectations;
- implementation-specific workflow/enforcement facets.

`ef-core` is selected; `sqlserver` is its provider variant.

EF Core → Dapper must not silently lose migration or seeding semantics. A missing required facet/property is a conformance failure / Decision Request.

SQL Server → PostgreSQL is a provider change inside persistence, not a new slot.

## 11. Backend-testing capability

Implementation-independent test policy remains normal M policy outside the module: test levels, determinism, isolation, probe-to-test, relational fidelity, and framework-neutral naming policy.

`backend-testing/nunit` supplies framework-specific rules, knowledge/technique, commands, scaffold assets, and adapters required by neutral architecture checks.

NUnit → xUnit should replace the module rather than require template-wide hunting.

## 12. Frontend capability

`frontend` is optional.

Implementation-independent frontend structural policy remains normal M policy outside the Angular module.

`frontend/angular` supplies Angular-specific framework rules, knowledge, scaffold/verify commands, and selected-technology decision content.

Removing the frontend should be possible by clearing the optional selection without hunting unrelated artifacts.

## 13. Decisions and selection

Keep M's V2-lineage planning-time decision model for normal project decisions:

- architecture defaults, approval gate, and patterns-not-adopted stay in always-loaded planning content;
- approved technology stack and conditional technologies stay in M's technology-stack decision content;
- ADR history may remain under `docs/decisions/`.

Add one small authoritative **capability selection record** for static composition, for example:

```text
docs/capability-selection.md
```

imported by `CLAUDE.md`.

It records only slot → selected implementation, optional enabled/disabled state, provider/declared properties needed for composition, and references to capability contracts/manifests.

It is not a K-style cross-system decision register and not an L-style hierarchy.

Changing a slot selection is Reserved and requires an ADR. Observable declared-property changes must not happen silently.

## 14. Skills, workflows, and references

Preserve M's V2-derived skill model:

- workflow skill = procedure;
- knowledge skill = technique;
- private references belong only to their owning skill;
- shared policy must not live only in a private reference;
- `code-reviewer` remains a thin wrapper;
- rule and skill must not independently own the same policy.

For capability-specific steps, workflows use contract/facet roles rather than hardcoding the currently selected implementation where a stable role exists.

A module-owned knowledge skill description may contain concrete trigger cues such as `NUnit` or `[TestCase]`.

Do not introduce K Kind taxonomy or L stability taxonomy for skills.

## 15. Enforcement

Use deterministic enforcement where materially useful for mechanically checkable rules.

In addition to normal M enforcement, M1 must be able to check at least:

- required slot selections exist;
- optional slot has at most one selected implementation;
- `MODULE.md` lists the implementation's runtime facets;
- required facets/properties are present;
- no unselected implementation enters runtime;
- implementation names do not leak beyond the permitted allow-list;
- external workflows do not bypass available facet roles;
- declared `binds:` relationships are consistent.

Generated enforcement must satisfy the shared Windows-compatibility requirements.

## 16. Human map

`.claude/MAP.md` keeps M's simple view and adds a capability view.

The normal M view answers what each file owns, its scope, how it loads, and how it is enforced.

For each capability, the capability view shows selected implementation, required/optional status, runtime facets, physical locations, loading, and declared bindings/properties.

Do not reorganize the map into levels or Kind × Scope.

## 17. Illustrative shape

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
│   ├── capability-selection.md
│   └── decisions/
└── .claude/
    ├── MAP.md
    ├── settings.json
    ├── hooks/
    ├── scripts/
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
    ├── rules/                  # flat M-style topical rules/facets
    ├── skills/
    └── agents/
```

This is illustrative. Do not create files merely because they appear here.

## 18. Leakage checks

The result is no longer M1 if it introduces:

- `rules/0-core`, `rules/1-architecture`, `Level:`, or the L hierarchy;
- `Kind:`, the K dependency graph, K scope-first organization, or a K decision register;
- slots outside the four agreed slots;
- dynamic plugin selection or multiple active implementations per slot;
- decorative contracts/manifests while implementation names still leak everywhere;
- workflows that hardcode selected implementations where facet roles exist;
- broad neutralization/reorganization of non-slot M content merely because M1 is more modular;
- capability machinery that changes frozen policy semantics or `trigger_class`.

## 19. Success criterion

M1 should look like:

> **a recognizable, well-refactored M/V2 system with four deliberate replacement boundaries added.**

It should not look like L1 without level labels or K1 without Kind labels.

The experiment should answer:

1. Does M1 outperform M because replaceable capabilities add real value?
2. Does M1 approach L1/K1 capability benefits with fewer files, less metadata, lower maintenance cost, and less cognitive overhead?
3. If L1/K1 outperform M1, does their extra organization provide measurable value beyond capabilities themselves?

Do not force M1 to be complex merely to make the capability experiment visible.
