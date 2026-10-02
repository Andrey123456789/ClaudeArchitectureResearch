# K1 — Kinds × Scopes, Replaceable Capability Modules: Design Notes

> **Research metadata.** This file is not part of any candidate's instruction context (S-19). Never copy it into a template or a benchmark project.

| | |
|---|---|
| Candidate | **K1**: Kinds × Scopes with replaceable capability modules |
| Axis A | A-K: Kinds × Scopes (identical kind and scope model to K0) |
| Axis B | B1: replaceable capability modules |
| Passport | `research/candidates/K1/CORE_FEATURES.md` |
| Shared invariants | S-01…S-19, defined in `research/observations/002-candidate-space-analysis.md` §2 (hereafter "002") |
| Shared B1 definitions | 002 §3.2 vocabulary, §3.3 contract format, §3.5 composition, §7.4 binding rule, §7.5 slot set. **Identical in L1.** |
| Distinguishing predicates (002 §3.4) | P-04, P-05, P-06, P-09…P-14 **yes**; P-08 yes; P-01…P-03, P-07 **no** |
| B0 sibling | K0. Read `research/candidates/K0/DESIGN.md` first; this file describes only the differences. |
| Status | Design only. Illustrative trees, not final files. |

---

## 1. Definition: K1 = K0 + T<sub>cap</sub>(slot set)

K1 keeps **everything** in K0:

- the kinds (OP, DEC, STD, KNW, WF, ENF, IN), the scopes, the classification procedure and the kind dependency graph;
- the register as the single decision artifact;
- the placement of all content outside the slot set.

K1 differs from K0 **only** by applying the same capability transformation as L1 (L1 DESIGN §1) to the same four slots: `architecture` (frame), `persistence` (leaf, with provider variants), `backend-testing` (leaf), and the optional `frontend`. P-14 makes this checkable: diff K0 and K1, ignore slot content, and nothing else may differ apart from logged glue.

### 1.1 The three-dimensional model

| Dimension | Question it answers | Decides |
|---|---|---|
| **Capability** | What can be replaced as a unit? | The module that owns the artifact. `—` for content that belongs to no slot. |
| **Kind** | What responsibility does the artifact have? | Mechanism, location and allowed content |
| **Scope** | Where does it apply? | `paths`, and the STD subdirectory |

**Axis precedence**, used when deciding ownership:

1. **Capability first.** Is the content specific to one implementation? If so, it belongs to that module.
2. **Kind second.** Which kind is it? That decides the facet type and its runtime location.
3. **Scope third.** Which paths does it apply to?

The axes do not compete, because each answers a different question. Content specific to *two* slots follows the binding rule (002 §7.4).

---

## 2. Facets per kind and scope (expected)

| Module | DEC | STD | KNW | WF facets | ENF / assets |
|---|---|---|---|---|---|
| `architecture/clean-architecture` (frame) | The register's slot section: architecture → clean-architecture; the CA summary and patterns not adopted (D-01…D-03, D-06) | `backend/architecture-style.md`: role-to-type mapping, layers, boundary placement, entry points; layout roles | — (no separate KNW planned) | scaffold: create projects and references | Neutral architecture-check specification |
| `persistence/ef-core` (+ variant `sqlserver`) | Slot entry; variant; **declared properties** (string comparison, migration mechanism) | `backend/persistence-technology.md`: EF specifics against roles; migrations | `ef-core` (+ `references/dev-seeding.md`) | build-fix and verify migration notes; scaffold provider setup | Deny-list entry: EF InMemory for relational tests |
| `backend-testing/nunit` | Slot entry (D-15 becomes the slot entry) | `backend-tests/test-framework.md` | `dotnet-testing` | scaffold test-project templates | Adapter that runs the neutral checks as NUnit tests |
| `frontend/angular` (optional) | Slot entry; D-16 | `frontend/frontend-framework.md` (Angular-specific) | `angular` | verify and scaffold `ng` steps | — |

**What stays outside the modules**, exactly as in K0:

- the neutral STD rules: `backend/architecture.md` reduced to role-level invariants, `backend/persistence.md` with the policy independent of any implementation, `backend-tests/testing.md` with test levels, determinism and naming, and the frontend structure section of `frontend/angular.md`;
- all OP content;
- non-slot DEC entries;
- non-slot KNW (logging, swagger, …) and every WF body.

---

## 3. Expected directory and artifact organization

Illustrative tree, showing only what differs from K0. The composition strategy is CS-1, in place with manifests, identical to L1 (002 CF-11).

```text
<template root>/
├── CLAUDE.md                                  OP   as K0
├── docs/architecture/decision-register.md     DEC  always   K0 entries + **Slot selection** section:
│                                                            architecture → clean-architecture · persistence → ef-core (sqlserver)
│                                                            · backend-testing → nunit · frontend → angular;
│                                                            declared properties of the selected implementations
└── .claude/
    ├── MAP.md                                 meta  kind × scope grid + capability view (slot → facets by kind)
    ├── capabilities/                          meta  maintainer-only, never loaded; contracts and manifests, identical format to L1
    │   ├── architecture/CONTRACT.md,  architecture/clean-architecture/MODULE.md
    │   ├── persistence/CONTRACT.md,   persistence/ef-core/MODULE.md
    │   ├── backend-testing/CONTRACT.md, backend-testing/nunit/MODULE.md
    │   └── frontend/CONTRACT.md,      frontend/angular/MODULE.md
    ├── rules/                                 STD
    │   ├── common/                            = K0
    │   ├── backend/
    │   │   ├── architecture.md                neutral: role-level invariants (contract vocabulary)
    │   │   ├── architecture-style.md          facet: architecture/clean-architecture
    │   │   ├── persistence.md                 neutral: data-lifecycle policy, seed co-change obligation
    │   │   ├── persistence-technology.md      facet: persistence/ef-core
    │   │   ├── api.md, error-handling.md, csharp.md, security.md     = K0 (embedded; not slot content)
    │   ├── backend-tests/
    │   │   ├── testing.md                     neutral
    │   │   └── test-framework.md              facet: backend-testing/nunit
    │   └── frontend/
    │       ├── angular.md → frontend.md       neutral frontend policy (renamed only if the rename is logged as a delta)
    │       └── frontend-framework.md          facet: frontend/angular
    ├── skills/                                shared set (S-11, S-12). KNW skills owned by a module carry `Capability:`;
    │                                          WF skills reach implementation-specific steps through facet roles (P-13).
    └── assets/ (scaffold)                     ENF: neutral architecture checks (frame) + test adapter (backend-testing)
```

**Expected size:** about 65–80 runtime instruction files, plus 4 contracts and 4 manifests.

The rename of `angular.md` in the tree is an example of a *permitted delta* that must be logged. Whether to rename at all is an implementation choice. Leaving the K0 name is simpler, and keeps P-14 cleaner.

---

## 4. Dependency direction

This is K0's kind graph plus the B1 rules shared with L1:

```text
IN ─► DEC ;  WF ─► KNW ─► STD ─► DEC ─► OP ;  ENF ─► STD, DEC          (= K0)

Leaf facets ─► contract vocabulary (roles)        never ─► the frame implementation's terms
Consumers   ─► slots and facet roles              never ─► implementation names (leak check, P-11)
Leaf ─► leaf                                      only as a declared `binds:` (counted as coupling)
```

One interaction is specific to K1. A facet's **kind** decides where it lives (for example, STD in `rules/<scope>/`), while its **capability** decides who owns it. A WF skill that belongs to no module may therefore depend on a KNW facet owned by a module. It must reference that facet by the slot's facet role, not by name.

---

## 5. Ownership model

1. **Slot content** is owned by the implementation module (capability first). Each facet keeps the kind and scope its content had in K0.
2. **Non-slot content** has the same owner as in K0 (P-14).
3. **Bindings:** placement goes to the frame, technique to the leaf, and anything left over to the dependent slot, with `binds:` (002 §7.4).
4. **Headers:** `Kind: … · Scope: … · Capability: <slot>/<impl> | —`.
5. **The map has two views:** the kind × scope grid, and a capability view listing each module's facets by kind.

---

## 6. Loading strategy

- **Facets keep their K0 trigger class** (S-09). In K0 kind and trigger class coincide, so in K1 each facet's kind fixes its trigger.
- **Contracts and manifests are never loaded.** At runtime Claude sees the register's slot section (always), the neutral STD rules and the facet STD rules (path), and the KNW facets (on demand).
- **Workflows reach implementation-specific steps through facet roles** (P-13). The option of substituting concrete values at composition time is the same open question as in L1 (002 §13 Q5).

---

## 7. Responsibilities of skills, rules and references

These are as in K0, with the following additions:

| Kind | Additional role in K1 |
|---|---|
| DEC | The slot section: selection, variants and declared properties. Implementation-specific decision text is owned by the module and lives in the register as a marked section. If nested imports work (002 §14 E0), it can be imported from a module file instead. |
| STD | A neutral rule per concern, plus a facet rule per selected implementation |
| KNW | Module-owned skills: the name is shared, the description carries the implementation's cues |
| WF | Unchanged bodies; implementation-specific steps are read from facets |
| ENF | The neutral frame check and the leaf adapter (§7.4); deny-list fragments contributed by modules |

---

## 8. Project decisions

- **The register remains the single decision artifact** (P-06). The slot section is part of it.
- Changing a selection is Reserved (R-1, R-6) and goes through `architecture-decision`.
- For a slot change, **"Affects"** becomes "the module manifest". The old module's files are removed and the new module's files added. That is why the expected blast radius outside the module is one edit (002 §11).
- **Declared properties** (002 §7.6): a change is a product decision (S-08). A replacement that leaves a required facet unfilled turns into a Decision Request.

---

## 9. How feature and task inputs interact with policy

As in K0 (IN is a kind; S-08, S-06). A feature that needs an unselected slot or a different implementation triggers a Decision Request, exactly as in L1.

---

## 10. Replacement and extension procedure

Identical to L1 DESIGN §10, so that the procedures are the same (002 CF-11). The conformance steps run K1's predicates instead of L1's.

| Task | K1-specific note |
|---|---|
| Replace an implementation | Facets land in kind locations: DEC section, STD facet files, KNW skills, WF facet sections, ENF fragments |
| Add a provider variant | DEC variant entry with declared properties, plus variant facets |
| Add a slot | Criteria (002 §7.1), then a contract, a module whose facets are classified by kind and scope, and a register entry |
| Add an embedded technology, or a project rule | Exactly as in K0 |

---

## 11. Complexity cost of the three-dimensional model

The prompt asks for this explicitly. Expected costs:

| Cost | Mechanism | Size (Expected) | Compared with |
|---|---|---|---|
| Classification effort | Three decisions per new artifact (capability, kind, scope) | +1 decision over K0 and L1; +2 over L0 | Highest of all candidates |
| Size of the cell space | 7 kinds × 6 scopes × (1 + 4 slots) = 210 cells; about 30–40 legal and used | A maintainer must know which cells are legal | L1: 4 levels × (1 + 4) = 20 cells |
| Concepts to learn | K0's taxonomy plus 8 capability concepts | About 18 concepts (002 §8) | M about 6, L1 about 17 |
| Facets spread across locations | One leaf supplies up to 5 facets in 4 kind locations | A missing facet is less visible than in L1, where a leaf's facets sit together at its level | L1 |
| Ownership conflicts across axes | For example, test-project placement: STD, scope backend-tests, owned by the frame, used by the leaf | Resolved by §1.1 and the binding rule, but those are two more rules | — |
| Map size | Two views (grid and capability) | Roughly twice K0's map | — |
| Checker size | About 20 structural rules | The largest S2 | L1 about 18 |
| Runtime overhead | Facet files, neutral wording at the slot boundary, workflow indirection | Small per task; measured | L1 (similar) |

**Is the three-dimensional model beneficial?** It is not assumed to be.

- **Benefit expected:** K0 spreads a technology across kinds, so capabilities should produce a larger reduction in replacement blast radius for K1 than for L1. This is the interaction hypothesis (002 §1).
- **Cost expected:** the highest learning and day-to-day maintenance cost of any candidate.
- **Net value** depends on how often replacements happen (002 §13 Q14).
- **What would falsify the benefit:** if CI-4 to CI-8 show K1's advantage over K0 is not larger than L1's over L0, or if CI-1, CI-3 and CI-10 show that K1's classification errors cancel out its replacement gains.

---

## 12. Structural conformance (what S2 checks for K1)

- Everything K0 checks: P-04, P-05, P-06, the shared checks, "Affects" resolution.
- Everything B1 requires, identical to L1: P-09 contracts; P-10 manifests and `Capability:` headers; P-11 leak check; P-12 selection; P-13 workflows through facet roles; facet-trigger parity.
- **K1-specific:** every facet's `Kind:` matches the facet type its contract requires, and its `Scope:` matches the contract's scope for that facet.
- **P-14** (diff against K0) belongs to the generation review.

---

## 13. Important risks

| Risk | Detail | Indicator or test |
|---|---|---|
| Classification errors in three dimensions | Wrong kind, scope or owner for new content | CI-1 and CI-3 error rates compared with K0 and L1 |
| Gaps in spread-out facets go unnoticed | A missing STD facet after replacement | Conformance; 002 §14 E7 |
| Role vocabulary and indirection | Same as L1 | 002 §14 E1 |
| Frame contract does not fit VSA | Same as L1 | CI-7 |
| The register's slot section grows | Declared properties and variants add always-loaded text | S-18; E8 |
| Maintainers bypass the structure | Overhead invites shortcuts (content placed "anywhere") | S2 overrides; drift over time |
| Convergence with L1 (002 CV-8) and with K0 at runtime (002 CV-7) | Identical modules; one implementation per slot | Structural distance; report it |

---

## 14. Leakage watchlist: signs that an implementation is no longer K1

- **Toward K0:** implementation names outside modules; workflows naming implementations; contracts that no check enforces.
- **Toward L1:** `Level:` headers; level directories; technology-neutral rewording beyond the slot boundary; stratified decision files.
- **Beyond the definition:**
  - slots outside the agreed set;
  - several implementations shipped at runtime;
  - non-slot content that differs from K0;
  - a contract format or composition strategy that differs from L1's.
