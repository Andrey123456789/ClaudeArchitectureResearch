# Replaceable Capability Framework

## Status

Draft shared definition for L1/K1. Research metadata, not runtime candidate context.

## Generic framework vs experimental sample

The **framework is generic**: any sufficiently independent, realistically replaceable project choice may become a capability.

The **first experiment intentionally implements only four representative slots**:

- `architecture` — frame capability; Clean Architecture is the initial implementation;
- `persistence` — leaf capability; EF Core with SQL Server provider variant;
- `backend-testing` — leaf capability; NUnit;
- `frontend` — optional leaf capability; Angular.

This limited slot set controls implementation cost and confounds. It does **not** mean future logging, authentication, messaging, caching, API style, mapping, database/provider, delivery, or other choices can never become capabilities.

## Qualification criteria

A concern is a strong capability candidate when several of these hold:

1. it is an independent engineering/project choice;
2. replacement is realistic over the project lifetime;
3. the choice affects policy, workflows, scaffolding, knowledge, or enforcement in several places;
4. replacement would otherwise have meaningful cross-cutting blast radius;
5. consumers can depend on a stable role/contract rather than implementation details;
6. the concern is cohesive enough to replace as one unit.

Do not create a capability merely because a library exists.

## Experimental rules

- L1 and K1 use the same slot set, contract format, composition strategy and replacement fixtures.
- Non-slot technologies remain embedded so Axis B is not contaminated.
- A capability implementation may supply decision content, normative rules, knowledge, workflow steps, and assets/enforcement.
- Runtime consumers outside the module refer to slot/facet roles rather than unnecessarily hard-coding implementation names.
- Observable product consequences are declared and may not silently change during replacement.
- One selected implementation exists per required slot in the first experiment; dynamic multi-implementation selection is out of scope.

## Frame vs leaf

Architecture is a **frame**, not an ordinary leaf. It owns placement/boundary roles that leaf capabilities may bind to. Clean Architecture -> VSA remains a deliberate stress test because it can expose a contract that only fits the initial frame.

## Interpretation

The four slots are a **test fixture for the composition mechanism**, not the full product vision.
