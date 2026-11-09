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
