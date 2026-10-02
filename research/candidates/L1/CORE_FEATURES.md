# L1 — Stability-first, Replaceable Capability Modules: Core Features

> **Research passport.** This is human-facing research metadata. It is not part of any candidate's Claude instruction context, and benchmarks must never rely on it (S-19).

| | |
|---|---|
| ID | **L1** |
| Axis A | A-L: stability-first (identical level model to L0) |
| Axis B | B1: replaceable capability modules |
| Shared invariants | S-01…S-19 (`research/observations/002-candidate-space-analysis.md` §2) |
| Identifying predicates | P-01…P-03 (as L0), plus P-09…P-13 (contracts, manifests, leak check, selection record, facet-based workflows), plus P-14 (non-slot content identical to L0) |
| Design notes | `research/candidates/L1/DESIGN.md` |

## 1. Core idea

**L0 plus first-class replaceable capabilities.** Exactly L0, except that four concerns become slots with contracts and implementation modules: `architecture` (frame), `persistence`, `backend-testing`, and the optional `frontend`. The rest of the system references slots, never implementations.

## 2. Primary decomposition model

Unchanged from L0: Core → Architecture → Technology → Project, with inputs outside. Each facet of a module **keeps the level** L0 gave its content. A module may contribute facets at several levels.

## 3. Capability composition model

B1, as defined in 002 §3, and identical to K1:

- a maintainer-only **contract** per slot;
- an implementation **module** that owns its facets and lists them in a manifest;
- an always-loaded **selection record** at level 3;
- **static composition**: only selected implementations exist at runtime;
- a **leak check**.

## 4. Distinguishing features

- **Role vocabulary at level 1.** Clean Architecture becomes the `architecture/clean-architecture` frame module, which maps roles (use-case unit, commit boundary, …) to concrete types.
- **Leaves are written against roles**, not against Clean Architecture terms. Placement belongs to the frame, technique to the leaf.
- **Facet files are named by slot and role** (`test-framework.md`, not `nunit.md`). Headers carry `Level:` and `Capability:`.
- **Declared properties**, such as default string-comparison semantics, make product-behavior consequences explicit.
- **Workflows reach implementation-specific steps through facet roles.**

## 5. Main hypothesis

Contracts and modules on top of the stability-first model **reduce replacement blast radius**, especially for strong leaves (NUnit → xUnit), and surface secondary decisions (EF Core → Dapper needs a migration mechanism). Behavior on ordinary tasks is **not worse** than L0.

## 6. What this candidate intentionally does NOT contain

- Kind or scope organization, or a single cross-level register (K).
- Slots outside the agreed set (no Serilog, FluentValidation or Swashbuckle slots).
- Several implementations shipped at runtime (dynamic selection).
- Any change to non-slot content relative to L0.

## 7. Expected strengths

- The smallest blast radius for leaf replacements (about one edit outside the module).
- Secondary decisions are made explicit through contract completeness.
- Dependency inversion is a natural extension of the stability-first idea.
- A leaf's facets sit together at its level.

## 8. Expected weaknesses

- Role vocabulary and slot indirection may weaken generation (002 §14 E1).
- Contracts may drift away from implementations.
- Bindings multiply.
- The frame contract will probably need revision for VSA.
- Overhead with no benefit on tasks that never replace anything.

## 9. Closest comparison candidates

**L0** (the same model without capabilities); **K1** (the same capabilities under Kinds × Scopes).

## 10. Experimental factors isolated by those comparisons

- **L0 vs L1:** replaceable capabilities under stability-first.
- **L1 vs K1:** stability-first vs Kinds × Scopes, with capabilities replaceable.
- **(L1 − L0) vs (K1 − K0):** the interaction between the axes.
