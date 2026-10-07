# Policy Inventory

`inventory.json` is the frozen normative oracle for candidate-template validation.

It is prepared **before** candidate generation and used mainly **after** generation to answer:

- did any shared policy disappear?
- does any policy have more than one normative owner?
- did a candidate weaken/strengthen/change a policy's meaning?
- did one candidate gain extra normative engineering policy not shared by the others?

## Single source of truth

There is intentionally no committed `content-pool/` copy and no `skill-content-map.json`.

`inventory.json` stores each policy exactly once. `policygroups` exist for human navigation only; `related_groups` record cross-topic relevance without copying a policy.

The grouping must not determine candidate runtime structure, owner placement, loading, or dependency direction.

## What belongs in the inventory

The inventory contains normative requirements/defaults/prohibitions/decisions whose loss or semantic drift would change candidate behavior.

Pure examples, explanatory prose, private technique, and non-normative troubleshooting material may remain outside the oracle.

Current policy count: **180**.

## Use in the experiment

- Candidate-construction Claude may see the inventory to preserve content parity.
- Benchmark-execution Claude must **not** see the inventory.
- Evaluators use it for `QLT-009`, `QLT-010`, `QLT-033`, and `QLT-034`.
