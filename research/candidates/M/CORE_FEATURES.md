# M — Minimal Modular: Core Features

> **Research passport.** This is human-facing research metadata. It is not part of any candidate's Claude instruction context, and benchmarks must never rely on it (S-19).

| | |
|---|---|
| ID | **M** |
| Axis A | A-M: no meta-architecture (V2 lineage) |
| Axis B | B0: embedded capabilities |
| Shared invariants | S-01…S-19 (`research/observations/002-candidate-space-analysis.md` §2) |
| Identifying predicate | P-07: every file traces to a V2 file, or carries a defect or S-ID that justifies it |
| Design notes | `research/candidates/M/DESIGN.md` |

## 1. Core idea

**V2, plus the shared invariants, plus defect-driven refactoring.** Conventional engineering applied to V2, without a new top-level instruction architecture.

## 2. Primary decomposition model

V2's own: topic-named files under the familiar mechanisms (`CLAUDE.md`, a flat `rules/` directory with V2 names, topic skills). Each change is a local refactoring (keep, fix, split, merge, move, new) justified by a defect ID from 001 §3 or by an S-ID.

## 3. Capability composition model

Embedded. Technologies are named where they are relevant. Replacing one means grep and edit.

## 4. Distinguishing features

- **The lineage rule** (P-07), with a written justification for every structural change.
- **Decisions are always loaded from V2-lineage locations**: architecture decisions, patterns not adopted and the gate in `CLAUDE.md`; the stack in `docs/technology-stack.md` (moved out of a skill reference and imported).
- **A flat `rules/` directory** with 9 files: V2's 7, plus `persistence.md` (split out) and `angular.md` (new).
- **No placement taxonomy.** New content goes to the topically closest file that is reliably loaded.

## 5. Main hypothesis

Most of the achievable improvement over V2 comes from the shared invariants and conventional defect fixes. A new meta-architecture (L or K) adds **little behavioral benefit beyond M**. Its value, if any, shows up in maintainability and change impact.

## 6. What this candidate intentionally does NOT contain

- Stability levels, level directories or technology-neutral rewording (L).
- Kinds or scopes as a directory axis or as metadata, and a merged decision register with an "Affects" column (K).
- Capability contracts, modules, a selection record or slot references (B1).
- Any file without lineage or justification; reorganization for elegance.

## 7. Expected strengths

- The lowest learning cost: V2 users recognize every file.
- The smallest migration from V2.
- Fewest concepts of any experimental candidate (about 6 shared ones).
- A clean test of the question "is a meta-architecture needed at all?"

## 8. Expected weaknesses

- No systemic rule for placing new content, so duplication may creep back over time.
- Keeping V2 lineage keeps some coarse triggers (`performance.md` and `error-handling.md` load on every backend `.cs` file).
- `CLAUDE.md` grows.
- Replacing a technology has an unknown blast radius, and mentions are easily missed.

## 9. Closest comparison candidates

**V2** (cleanup effect); **K0** (the most similar file set; 002 CV-6); **L0**.

## 10. Experimental factors isolated by those comparisons

- **V2 vs M:** the shared bundle plus conventional cleanup (confounded unless the ablation runs).
- **M vs L0:** the value of adding a stability-first meta-architecture.
- **M vs K0:** the value of adding a Kinds × Scopes meta-architecture.
- **M vs L1 / K1:** a full meta-architecture plus capabilities, compared with neither.
