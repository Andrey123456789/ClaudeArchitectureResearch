# L0 — Stability-first, Embedded Capabilities: Core Features

> **Research passport.** This is human-facing research metadata. It is not part of any candidate's Claude instruction context, and benchmarks must never rely on it (S-19).

| | |
|---|---|
| ID | **L0** |
| Axis A | A-L: stability-first |
| Axis B | B0: embedded capabilities |
| Shared invariants | S-01…S-19 (`research/observations/002-candidate-space-analysis.md` §2) |
| Identifying predicates | P-01 levels; P-02 level dependency rule; P-03 Core and Architecture are technology-neutral. No contracts. |
| Design notes | `research/candidates/L0/DESIGN.md` |

## 1. Core idea

Organize the instruction system **by stability**. Fundamental policy is separated from volatile policy, and dependencies point from the volatile toward the stable. Technology choices stay embedded.

## 2. Primary decomposition model

Four ordered levels, with inputs outside the hierarchy:

**0 Core → 1 Architecture → 2 Technology → 3 Project** · *Inputs*: spec, custom settings, features, tasks.

A statement's level is that of the most volatile thing it depends on. Mixed statements are split across levels. Each level holds several cohesive modules; L0 is **not** "one file per layer".

## 3. Capability composition model

Embedded:

- each technology has a module at level 2;
- the *selection* of technologies is a level-3 decision;
- workflows name commands and technologies directly.

There are no slots, no contracts and no selection mechanism.

## 4. Distinguishing features

- A `Level:` header and level-first rule directories (`rules/0-core/`, `1-architecture/`, `2-technology/`, `3-project/`).
- **Levels 0 and 1 name no technology** beyond the .NET / TypeScript platform. A level-2 module makes each neutral constraint concrete.
- **Decisions are stratified**: the Architecture overview (D-01…D-08, patterns not adopted) and the Project decisions (stack, defaults) are both always loaded.
- Workflows sit at the level of their most volatile content, usually level 3.
- The map is organized by level, then by module.

## 5. Main hypothesis

Ordering instructions by stability, with a strict dependency direction:

- prevents silent overrides;
- keeps technology content local (one module per technology);
- makes technology changes local to levels 2 and 3;

all without loading or triggering regressions compared with M.

## 6. What this candidate intentionally does NOT contain

- Capability contracts, module manifests, a selection record, or workflows that enumerate modules generically (B1).
- Kind or scope directories, or a single cross-level decision register (K).
- "Feature" or "Task" instruction levels.

## 7. Expected strengths

- Good locality for technologies: everything about EF Core at level 2 sits in one module.
- A clear "who may depend on whom" rule, which a check can enforce.
- Aligns directly with requirements 2.2 and 2.3.
- An intuitive ordering for humans.

## 8. Expected weaknesses

- Arguments over which level something belongs to (seeding, production migrations, status codes).
- Technology-neutral wording may make generation less concrete (002 §14 E2).
- More rule files load per trigger.
- Decisions are split across two always-loaded files.
- Replacing the architecture still rewrites all of level 1.

## 9. Closest comparison candidates

**L1** (same levels, capabilities added); **K0** (the other Axis A value, also embedded); **M**.

## 10. Experimental factors isolated by those comparisons

- **L0 vs L1:** replaceable capabilities under stability-first.
- **L0 vs K0:** stability-first vs Kinds × Scopes, with capabilities embedded.
- **M vs L0:** the value of adding the stability-first meta-architecture.
