# Policy Foundation

This directory is the pre-generation semantic foundation for the six-candidate experiment.

## Why it exists

M, L0, L1, K0 and K1 must differ in instruction architecture, not because one candidate accidentally receives stronger or more complete policy text.

Canonical flow:

```text
frozen V2
  -> inventory.json
  -> grouped content-pool/*
  -> candidate-specific placement/ownership
  -> parity / ownership checks
```

## Files

- `inventory.json` — machine-readable stable policy IDs, source traceability, trigger class, scope and normalized semantics.
- `content-pool/` — the same policy set grouped for human review.
- `skill-content-map.json` — separates normative policy from reusable workflow/knowledge content.

The grouped Markdown files are review views, not additional normative owners.

## Candidate-generation rules

1. Every experimental candidate receives all applicable IDs.
2. Every policy ID has exactly one runtime normative owner.
3. Pointers/check-by-reference may repeat an ID, but not its independent wording/conditions.
4. Candidate-specific neutralization, slot wording, or policy splits must be recorded in a permitted-delta log.
5. V2 remains frozen.
6. Workflow/knowledge content is shared across candidates unless the candidate architecture forces a logged representation change.

## Status

Draft for human review. Before template generation, review for omissions, accidental strengthening/weakening, and grouping mistakes.
