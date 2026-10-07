# E0 — Claude Code Mechanics Validation

## Status

**PLANNED FOR ITERATION 004 — NOT YET EXECUTED.**

E0 is not a candidate benchmark. It empirically validates Claude Code mechanics on which the candidate layouts, benchmark isolation, and evidence collection depend.

Use the exact Claude Code build/configuration intended for the experiment.

## Required probes

| Probe | Question | Pass/evidence condition | Design affected |
|---|---|---|---|
| E0-R1 | Are rules in nested `.claude/rules/<group>/` discovered? | A fresh-session positive control shows the unique nested-rule behavior/marker; a negative control does not | L/K physical rule layout |
| E0-R2 | Do path-scoped rules apply on read/edit/new-file work as intended? | Matching-path probe observes the rule; non-matching path does not | loading/scope model |
| E0-S1 | Is `.claude/skills/<name>/SKILL.md` discovered and triggered from its description? | Relevant prompt causes unique skill behavior; unrelated control does not | skill routing |
| E0-S2 | Can private skill references be reached through the owning skill without becoming ordinary global policy? | Owning-skill probe can use the reference; unrelated control does not expose/use its unique content | progressive disclosure |
| E0-A1 | Does the intended subagent + skill/preload mechanism work in the exact Claude Code version? | Subagent produces behavior that requires its intended canonical procedure, without copying criteria into the agent definition | thin reviewer agent |
| E0-I1 | Do `CLAUDE.md` imports work in the intended shape, including a nested import if candidate designs rely on it? | Imported marker/behavior is observable in a fresh session | planning-time decision loading |
| E0-T1 | Which telemetry fields are reliably obtainable from the local Claude Code CLI/session artifacts? | Raw evidence establishes availability/unavailability of timestamps, input/output/cache tokens, provider cost, turns, and tool calls | metrics/harness |
| E0-W1 | Is the launch root actually an access boundary under the intended permission/sandbox mode? | A harmless outside-root canary establishes whether parent/sibling files are unreachable, permission-gated, or directly reachable | benchmark isolation |

## General protocol

1. Record OS, shell, Claude Code version, model, effort, permission/sandbox mode, and relevant non-secret settings.
2. Build tiny dedicated fixtures. Do not use V2, V3, M/L/K runtime templates, or TaskBoard as probe fixtures.
3. Give each probe unique harmless marker strings so results cannot be confused across probes.
4. Run each positive/negative control in a fresh Claude Code process/session when technically possible.
5. Preserve exact prompt, fixture hash, command, raw transcript/output, tool events available, and observed result.
6. Prefer deterministic file/output checks over Claude's statement that a rule/skill/reference was loaded.
7. If a nested Claude invocation is not supported or would invalidate the environment, generate exact reproducible commands and run controls as separate top-level sessions; do not fabricate PASS/FAIL.
8. Do not modify candidate definitions merely to obtain green results. Record failures/limitations and propose a consistent adaptation for later approval.
9. Do not modify `templates/v2-baseline/`, `templates/v3/`, policy inventory, metrics definitions, benchmark plan, or candidate DESIGN/CORE_FEATURES files during E0.

## E0-W1 safety

Use only a generated harmless canary outside the test root. Do not attempt to inspect unrelated user files.

Classify the result as one of:

- `BLOCKED` — outside-root access is not available;
- `PERMISSION_GATED` — access requires an explicit permission interaction;
- `REACHABLE` — outside-root canary can be read without such a gate;
- `INCONCLUSIVE` — mechanics could not be tested reliably.

This is a mechanics fact, not a security exploit exercise.

## E0-T1 telemetry inventory

At minimum, establish whether the exact environment exposes trustworthy values for:

- start/finish or equivalent elapsed timestamps;
- input tokens;
- output tokens;
- cache-read input tokens;
- cache-creation input tokens;
- provider-reported monetary cost;
- assistant turns;
- structured tool calls.

For each field record:

- availability;
- raw source/artifact;
- whether it is direct telemetry or derived;
- parsing/recheck method;
- known caveat.

`TECHNICAL_UNAVAILABLE` is a valid result. Do not reconstruct provider billing from an LLM estimate.

## Result layout

A successful Iteration 004 should leave reproducible evidence, for example:

```text
research/e0/
├── README.md
├── probes/                  # probe definitions / fixtures / harness as needed
├── results/
│   └── <environment-id>/
│       ├── summary.json
│       ├── R1/
│       ├── R2/
│       ├── S1/
│       ├── S2/
│       ├── A1/
│       ├── I1/
│       ├── T1/
│       └── W1/
└── ...
```

Exact storage may differ if a simpler auditable layout is better.

## Exit criterion

Candidate generation is not allowed to rely on an unverified mechanic.

Iteration 004 is complete when each required mechanic is:

- empirically `PASS` / supported as expected; or
- explicitly characterized as unsupported/limited and a consistent candidate-design adaptation is proposed for approval.

Raw failures are retained.
