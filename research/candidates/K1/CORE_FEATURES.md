# K1 — Kinds × Scopes, Replaceable Capability Modules: Core Features

> **Research passport.** This is human-facing research metadata. It is not part of any candidate's Claude instruction context, and benchmarks must never rely on it (S-19).

| | |
|---|---|
| ID | **K1** |
| Axis A | A-K: Kinds × Scopes (identical kind and scope model to K0) |
| Axis B | B1: replaceable capability modules |
| Shared invariants | S-01…S-19 (`research/observations/002-candidate-space-analysis.md` §2) |
| Identifying predicates | P-04…P-06 (as K0), plus P-09…P-13 (contracts, manifests, leak check, selection, facet-based workflows), plus P-14 (non-slot content identical to K0) |
| Design notes | `research/candidates/K1/DESIGN.md` |

## 1. Core idea

**K0 plus the same replaceable capability modules as L1.** Three dimensions:

- **Capability**: what can be replaced as a unit;
- **Kind**: what responsibility an artifact has;
- **Scope**: where it applies.

## 2. Primary decomposition model

Unchanged from K0: 7 kinds × 6 scopes. Capability is an additional *composition* boundary. Each facet keeps the kind and scope its content had in K0.

## 3. Capability composition model

B1, identical to L1 (002 §3):

- the same four slots: `architecture` (frame), `persistence`, `backend-testing`, optional `frontend`;
- the same contract format;
- the same composition strategy;
- the same module content.

The selection lives in a **slot section of the register**.

## 4. Distinguishing features

- Headers `Kind: · Scope: · Capability:`.
- Each module supplies facets in several kinds: a DEC section, STD facet rules (`rules/<scope>/test-framework.md`), KNW skills, WF steps and ENF fragments.
- Neutral STD rules per concern sit next to the facet rules.
- **Axis precedence for ownership:** capability, then kind, then scope.
- The map has two views: the kind × scope grid and the capability view.

## 5. Main hypothesis

Because K0 spreads each technology across kinds, **capabilities give K1 a larger reduction in replacement blast radius than they give L1** (the interaction hypothesis). Whether this repays the cost of the three-dimensional model depends on how often replacements happen.

## 6. What this candidate intentionally does NOT contain

- Stability levels, or technology-neutral rewording beyond the slot boundary (L).
- Slots outside the agreed set, or several implementations at runtime.
- A contract format or composition strategy that differs from L1's.
- Any change to non-slot content relative to K0.

## 7. Expected strengths

- A small leaf blast radius (about one edit outside the module), equal to L1.
- Keeps K0's loading precision and single decision artifact.
- Ownership is explicit on all three axes.

## 8. Expected weaknesses

- **The highest complexity**: three classification decisions per artifact, about 210 possible cells, and about 18 concepts to learn.
- A module's facets are spread across kind directories, so gaps are less visible.
- Inherits L1's risks: role vocabulary and indirection, contract drift, the VSA fit.

## 9. Closest comparison candidates

**K0** (the same model without capabilities); **L1** (the same capabilities under stability-first).

## 10. Experimental factors isolated by those comparisons

- **K0 vs K1:** replaceable capabilities under Kinds × Scopes.
- **L1 vs K1:** stability-first vs Kinds × Scopes, with capabilities replaceable.
- **(K1 − K0) vs (L1 − L0):** the interaction between the axes.
