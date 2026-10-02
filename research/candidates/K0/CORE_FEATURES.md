# K0 — Kinds × Scopes, Embedded Capabilities: Core Features

> **Research passport.** This is human-facing research metadata. It is not part of any candidate's Claude instruction context, and benchmarks must never rely on it (S-19).

| | |
|---|---|
| ID | **K0** |
| Axis A | A-K: Kinds × Scopes |
| Axis B | B0: embedded capabilities |
| Shared invariants | S-01…S-19 (`research/observations/002-candidate-space-analysis.md` §2) |
| Identifying predicates | P-04 (one kind and one scope; the kind fixes the mechanism), P-05 (STD rules are scope-first), P-06 (a single decision register). No contracts. |
| Origin | The organization proposed in `research/observations/001-v3-design-proposal.md`; its non-organizational parts are now shared invariants |
| Design notes | `research/candidates/K0/DESIGN.md` |

## 1. Core idea

Organize the instruction system **by responsibility (kind) and applicability (scope)**. An artifact's kind decides its mechanism, location and allowed content. Technology choices stay embedded.

## 2. Primary decomposition model

7 kinds × 6 scopes.

- **Kinds:** OP operating policy, DEC project decisions, STD standards, KNW knowledge, WF workflows, ENF enforcement, IN product inputs.
- **Scopes:** common, backend, backend-tests, frontend, delivery, repo/meta.

## 3. Capability composition model

Embedded. A technology is **spread across kinds**. NUnit, for example, appears in a DEC entry, an STD rule, a KNW skill, WF steps and an ENF asset. No unit owns it as a whole.

## 4. Distinguishing features

- `Kind:` and `Scope:` headers; STD rules live in `rules/<scope>/`.
- **The kind and the trigger class coincide.** Knowing the kind tells you how the artifact loads.
- **A single decision register** (`docs/architecture/decision-register.md`, imported), with IDs, "Details in" and **"Affects"** columns.
- WF and KNW are formally distinct kinds. IN is a kind, not a layer.
- STD rules may name technologies directly. They are split only by responsibility or trigger, never for neutrality.
- The map is a kind × scope grid.

## 5. Main hypothesis

Organizing by responsibility and scope makes **ownership and loading predictable**:

- the fewest misplaced rules and loading failures;
- the fastest answer to "where is rule X, and when does it load?";
- decisions propagate reliably through "Affects".

## 6. What this candidate intentionally does NOT contain

- Stability levels, or technology-neutral rewording (L).
- Capability contracts, modules, a selection record or slot references (B1).
- V2 topic files kept merely for lineage (M).

## 7. Expected strengths

- The best expected loading precision (scope-precise STD rules, for example a persistence rule only for the persistence-related projects).
- One place for every decision.
- Clear may-contain and must-not-contain rules per kind.
- Reasonable to learn, with an explicit placement procedure.

## 8. Expected weaknesses

- Learning cost of the taxonomy.
- Some kind boundaries are fuzzy (is seeding DEC or STD?).
- The register grows, and "Affects" needs maintenance.
- Replacing an embedded technology touches 4–5 kind locations.
- Converges with M (002 CV-6).

## 9. Closest comparison candidates

**K1** (the same model with capabilities); **L0** (the other Axis A value, also embedded); **M**.

## 10. Experimental factors isolated by those comparisons

- **K0 vs K1:** replaceable capabilities under Kinds × Scopes.
- **L0 vs K0:** stability-first vs Kinds × Scopes, with capabilities embedded.
- **M vs K0:** the value of adding the Kinds × Scopes meta-architecture.
