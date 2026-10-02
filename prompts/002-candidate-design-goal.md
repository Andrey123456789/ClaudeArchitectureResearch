# Goal: Define the Candidate Architecture Space

## Context

This is the second design iteration of the ClaudeArchitectureResearch project.

Before doing anything else, read:

- `research/hypothesis.md`
- `research/requirements.md`
- `prompts/001-v3-design-goal.md`
- `research/observations/001-v3-design-proposal.md`

Then inspect `templates/v2-baseline/` as needed to verify claims about the baseline.

The first design iteration proposed a Kinds × Scopes architecture.

Human review concluded that this is only one candidate, not the selected solution.

The research will compare six variants:

1. V2 — frozen baseline
2. M — Minimal Modular
3. L0 — Stability-first with embedded capabilities
4. L1 — Stability-first with replaceable capability modules
5. K0 — Kinds × Scopes with embedded capabilities
6. K1 — Kinds × Scopes with replaceable capability modules

All six variants are intentionally retained.

Do not eliminate a candidate merely because you believe another is superior.

You are encouraged to criticize weaknesses and predict failure modes, but the purpose of this iteration is to define the candidates precisely enough that they can later be implemented and compared.

---

# Primary goal

Produce precise, comparable architectural definitions for all six candidates.

The definitions must make it possible to determine later:

- what is common between candidates;
- what intentionally differs;
- which experimental factor each comparison isolates;
- whether an implementation accidentally introduced differences that do not belong to the candidate definition.

This iteration is DESIGN ONLY.

Do not modify:

- `templates/v2-baseline/`
- `templates/v3/`
- any future candidate implementation directories.

---

# 1. Common principles

Identify the principles that should be shared by all experimental candidates M, L0, L1, K0 and K1 unless a candidate definition explicitly requires otherwise.

At minimum evaluate:

- modularity;
- single source of truth;
- explicit ownership;
- separation of concerns;
- stable dependency direction;
- selective loading;
- reliable triggering;
- no silent architectural or policy overrides;
- human-readable structure;
- backend / frontend / testing scope separation where meaningful;
- measurable behavior;
- deterministic enforcement where appropriate;
- preservation of useful V2 behavior;
- Claude's ability to challenge questionable design decisions.

Do not use these shared improvements as distinguishing features between candidates.

For example, "modularity" alone must not be used as an advantage of L1 over K1: both are expected to be modular.

---

# 2. Experimental axes

Treat the following as the primary architectural axes.

## Axis A — Primary decomposition model

### Stability-first

The primary organization principle is abstraction / stability:

more fundamental and stable policy is separated from more specific and volatile policy.

The exact hierarchy is not predetermined.

A possible mental model is:

Core
→ Architecture
→ Technology / capabilities
→ Project
→ Feature / task inputs

The important characteristic is dependency direction from concrete/volatile toward abstract/stable.

### Kinds × Scopes

The primary organization principle is responsibility.

Possible kinds include:

- operating policy;
- project decisions;
- standards;
- knowledge;
- workflows;
- enforcement;
- product inputs.

Possible scopes include:

- common;
- backend;
- backend tests;
- frontend;
- delivery;
- repository/meta.

The exact taxonomy may be refined, but the defining property is that artifact responsibility and scope are primary.

---

## Axis B — Capability composition model

### Embedded capabilities

Important project choices such as:

- Clean Architecture;
- EF Core;
- NUnit;
- Angular;
- SQL Server;
- logging technology;

may be well modularized but are not governed by a generic replaceable-module mechanism.

Changing one may require coordinated edits in multiple authoritative artifacts.

### Replaceable capability modules

Important independent project choices are explicit composition units.

Examples may include:

- architecture;
- persistence;
- database;
- backend testing;
- frontend;
- API style;
- logging;
- mapping;
- caching;
- authentication;
- messaging;
- delivery.

A capability may provide several artifact types if needed.

For example a backend-testing capability may provide:

- policy;
- knowledge;
- workflows;
- scaffold assets;
- enforcement.

The core system should depend on the capability abstraction rather than unnecessarily naming one implementation.

A replacement such as:

NUnit → xUnit

or:

Clean Architecture → Vertical Slice Architecture

should have a deliberately small and measurable replacement blast radius.

Do not assume that every technology deserves its own replaceable capability.
Define criteria for when a concern is sufficiently independent and changeable to justify a capability boundary.

---

# 3. Define all six candidates

## V2 — Baseline

V2 is frozen.

Document its defining characteristics only.

Do not redesign it.

Its purpose is experimental control.

---

## M — Minimal Modular

Purpose:

Test how much improvement can be obtained by applying conventional good engineering practices to V2 without introducing a new top-level instruction architecture.

Expected characteristics include:

- preserve the general V2 mental model;
- improve cohesion;
- remove unnecessary normative duplication;
- establish clearer ownership;
- improve backend/frontend/testing separation;
- improve loading and triggering where possible;
- split large artifacts where responsibilities justify it.

M must NOT introduce:

- Stability-first as the governing meta-architecture;
- Kinds × Scopes as the governing meta-architecture;
- a general replaceable capability framework.

M may make individual concerns easier to replace as a consequence of good modular design, but replaceability is not a first-class composition mechanism.

---

## L0 — Stability-first + Embedded Capabilities

Purpose:

Test whether abstraction/stability is a sufficient primary architecture for the instruction system.

Expected characteristics:

- explicit ordering from fundamental/stable toward concrete/volatile;
- stable dependency direction;
- modularity within levels;
- clear ownership;
- Clean Architecture and technology choices remain embedded rather than participating in a generic replaceable capability system.

Do not reduce L0 to "one file per layer".

Modules should still be cohesive and may be numerous.

---

## L1 — Stability-first + Replaceable Capability Modules

Purpose:

Measure the effect of adding first-class replaceable capabilities to the Stability-first model.

L1 should preserve the primary decomposition model of L0.

The principal experimental difference between L0 and L1 must be:

Embedded capabilities
vs
Replaceable capability modules.

Examples of possible replaceable capabilities include:

- architecture;
- backend testing;
- persistence;
- database;
- frontend;
- logging.

Define how capability implementations are selected or composed without prematurely committing to a specific configuration format.

Define what a capability contract means in a Markdown/Claude Code instruction system.

---

## K0 — Kinds × Scopes + Embedded Capabilities

Purpose:

Test the first major alternative proposed in iteration 001.

Primary organization is by artifact responsibility and scope.

Expected characteristics include:

- explicit kinds;
- explicit scopes;
- responsibility determines ownership and loading mechanism;
- project decisions available when they are required;
- normative policy does not depend on an optionally triggered knowledge skill;
- workflow and knowledge skills may be distinct categories;
- product feature/task inputs are not automatically treated as instruction layers.

Capabilities remain embedded.

For example NUnit-related concerns may be distributed across:

- decision;
- standard;
- knowledge;
- workflow;

if those are their correct kinds.

There is no generic NUnit module that owns all of them as one replaceable composition unit.

---

## K1 — Kinds × Scopes + Replaceable Capability Modules

Purpose:

Measure the effect of introducing first-class replaceable capabilities into K0.

K1 retains Kinds × Scopes as its primary responsibility model.

Capability becomes an additional composition boundary.

A useful conceptual distinction may be:

- Capability: what can be replaced as a unit.
- Kind: what responsibility an artifact has.
- Scope: where it applies.

Do not assume that this three-dimensional model is beneficial.

Explicitly analyze its complexity cost.

---

# 4. Controlled comparisons

Define exactly what each direct comparison is intended to isolate.

At minimum:

V2 vs M:
    Effect of conventional modular cleanup without new meta-architecture.

L0 vs L1:
    Effect of replaceable capabilities under Stability-first.

K0 vs K1:
    Effect of replaceable capabilities under Kinds × Scopes.

L0 vs K0:
    Effect of Stability-first vs Kinds × Scopes when capabilities are embedded.

L1 vs K1:
    Effect of Stability-first vs Kinds × Scopes when capabilities are replaceable.

M vs the other candidates:
    Whether the additional meta-architecture provides enough benefit to justify its complexity.

Identify important confounding factors that implementation must avoid.

---

# 5. Capability criteria

For L1 and K1, define criteria for deciding whether something should become a replaceable capability.

Avoid both extremes:

- everything is hardcoded;
- every trivial library becomes a plugin.

Consider at least:

- independent business/engineering choice;
- realistic probability of replacement;
- meaningful policy or workflow consequences;
- multiple artifacts currently need to know the choice;
- replacement cost if not isolated;
- degree of coupling to other capabilities.

Use examples such as:

- Clean Architecture → VSA;
- NUnit → xUnit;
- SQL Server → PostgreSQL;
- EF Core → Dapper;
- Serilog → another logging configuration.

Classify examples as strong, weak or questionable capability candidates and explain why.

---

# 6. Candidate-specific CORE_FEATURES

Create a human-facing research passport for every candidate.

These files are research metadata.

They are NOT part of the candidate's Claude instruction context and must not be relied on by the candidate during benchmarks.

Create:

- `research/candidates/V2/CORE_FEATURES.md`
- `research/candidates/M/CORE_FEATURES.md`
- `research/candidates/L0/CORE_FEATURES.md`
- `research/candidates/L1/CORE_FEATURES.md`
- `research/candidates/K0/CORE_FEATURES.md`
- `research/candidates/K1/CORE_FEATURES.md`

Each file should be concise and contain:

1. Core idea
2. Primary decomposition model
3. Capability composition model
4. Distinguishing features
5. Main hypothesis
6. What this candidate intentionally does NOT contain
7. Expected strengths
8. Expected weaknesses
9. Closest comparison candidates
10. Experimental factor(s) isolated by those comparisons

Do not turn CORE_FEATURES into a long design specification.

Its purpose is for a human researcher to identify the candidate months later without confusing it with another variant.

---

# 7. Detailed design notes

Also create one design document per experimental candidate:

- `research/candidates/M/DESIGN.md`
- `research/candidates/L0/DESIGN.md`
- `research/candidates/L1/DESIGN.md`
- `research/candidates/K0/DESIGN.md`
- `research/candidates/K1/DESIGN.md`

V2 does not need a redesign document because the existing template is the definition of V2.

Each DESIGN.md should describe at a high level:

- expected directory / artifact organization;
- dependency direction;
- ownership model;
- loading strategy;
- skill/rule/reference responsibilities;
- handling of project decisions;
- how feature/task inputs interact with policy;
- expected extension points;
- important risks.

Do not write the final files of the actual template yet.

Illustrative trees are allowed.

---

# 8. Cross-candidate analysis

Create:

`research/observations/002-candidate-space-analysis.md`

It must contain:

1. Executive summary
2. Shared invariants
3. The two experimental axes
4. Candidate comparison matrix
5. Controlled comparison matrix
6. Confounding factors to avoid
7. Capability-boundary analysis
8. Expected complexity of each candidate
9. Expected loading/triggering risks
10. Expected maintainability risks
11. Expected flexibility / replacement risks
12. Cases where two candidates may converge to similar physical files despite different architectural principles
13. Questions that must be decided before implementation
14. Recommendations about which aspects need empirical tests before generation

You may state which candidates you expect to perform better or worse.

Do NOT eliminate candidates.

---

# 9. Important research constraint

Do not allow candidate-specific advantages to enter through unrelated mechanisms.

For example:

- one candidate must not receive stronger hooks while another has none;
- one candidate must not receive better architecture tests merely because its design document happens to mention them;
- one candidate must not use a better model/effort setting;
- engineering policy content should remain equivalent unless the candidate architecture inherently requires a different representation.

The goal is to compare architectural organization, not different levels of feature completeness.

---

# 10. Do not implement yet

During this task:

DO NOT modify:

- `templates/v2-baseline/`
- `templates/v3/`

DO NOT create implementation copies of M/L0/L1/K0/K1.

DO NOT run the behavioral benchmark.

DO NOT select a winner.

Stop after the candidate specifications and candidate-space analysis have been written.