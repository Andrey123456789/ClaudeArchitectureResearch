# E0 — Minimal Claude Code Mechanics Probe

## Status

**NOT EXECUTED in iteration 003.**

The editing environment used for this package did not expose a local Claude Code CLI, so this iteration records a reproducible probe plan instead of inventing results.

Template generation should wait for the minimum mechanics checks on the exact Claude Code version intended for the experiment.

## Required probes

| Probe | Question | Pass condition | Design affected |
|---|---|---|---|
| E0-R1 | Are rules in nested `.claude/rules/<group>/` discovered? | Nested probe affects the expected observable response | L/K directory layout |
| E0-R2 | Do path-scoped rules apply on Read/Edit/new-file work as intended? | Positive marker appears only for matching paths | S-09 / trigger model |
| E0-S1 | Is `.claude/skills/<name>/SKILL.md` discovered and triggered from description? | Skill marker appears for relevant prompt, not unrelated prompt | skill architecture |
| E0-S2 | Can private skill references be reached on demand through the owning skill? | Reference marker is retrievable only through intended flow | progressive disclosure |
| E0-A1 | Does the intended subagent skill/preload mechanism work? | Reviewer receives canonical procedure without duplicated criteria | thin reviewer agent |
| E0-I1 | Do CLAUDE.md imports work in the intended shape, including one nested import if planned? | Imported marker is available during planning | decision loading |

## Protocol

1. Freeze and record Claude Code version.
2. Run each probe in a fresh session against a tiny fixture, not a candidate template.
3. Use unique harmless markers such as `E0_BACKEND_RULE_7F2A`.
4. Save exact prompt, model, effort/permission mode, transcript and result.
5. Use positive and negative controls.
6. Do not infer loading merely from Claude saying it loaded something; require observable behavior/marker.
7. If a mechanism fails, update all affected candidate designs consistently before generation.

## Exit criterion

Iteration 004 may proceed when the physical mechanisms required by the candidate layouts have an empirical PASS, or the designs have been changed to avoid failed mechanisms.
