# Policy Inventory

`inventory.json` is the frozen **hidden V2-only normative oracle** for candidate-template validation.

It is prepared and audited **before** candidate generation, but candidate-construction Claude must **not** see it.

Generation and evaluation deliberately use different information:

```text
candidate generation:
  CANDIDATE.md
  + frozen templates/v2-baseline/**

post-generation evaluation:
  generated candidate
  + hidden research/policy/inventory.json
```

This prevents the inventory from becoming an answer key during construction.

## Single source of truth for generation

The frozen V2 baseline is the visible source of truth from which candidate-construction Claude must recover policy intent.

The inventory is a normalized evaluation oracle derived from that baseline. It is not a construction input.

There is intentionally no committed `content-pool/` copy and no `skill-content-map.json`.

`inventory.json` stores each V2-derived policy exactly once. `policygroups` exist for human navigation only; `related_groups` record cross-topic relevance without copying policy.

The grouping must not determine candidate runtime structure, owner placement, loading, or dependency direction.

## What belongs in the inventory

The inventory contains V2-derived normative requirements, defaults, prohibitions, decisions, approval gates, and workflow obligations whose loss or semantic drift would materially change candidate behavior.

It excludes:

- research-introduced requirements;
- pure examples;
- explanatory prose;
- code samples;
- optional technique;
- troubleshooting detail;
- private knowledge that does not itself impose a material normative requirement.

Audited borderline material intentionally excluded from the oracle is recorded in `intentional_non_oracle_material`.

Current audited policy count: **194**.

## Research-shared requirements

Research-introduced constraints are not V2 policies and therefore are not part of the V2 preservation oracle.

They are stored separately in `shared-research-invariants.json` and may be expressed through the common candidate-construction task.

They are not scored as V2 policy preservation.

## Use in the experiment

- Candidate-construction Claude must **not** see `inventory.json`.
- Benchmark-execution Claude must **not** see `inventory.json`.
- Evaluators reveal/use it only after the candidate output being evaluated is frozen.
- Evaluators use it to detect missing owners, duplicate owners, semantic weakening/strengthening, and unapproved additional normative policy.
