# Run evidence archive and `evidence.json` schema (FAIR-02), v1

A report is not evidence that the described check happened. For every measured run the harness must archive, **independently of the agent's report**:

```text
runs/<run-code>/
├── prompt.txt                 # the exact first user message (task + reporting instruction); SHA-256 in run_metadata.json
├── report.md                  # the final Run Report, extracted verbatim from the transcript
├── archive/
│   ├── transcript.jsonl       # host transcript / event log (tool calls, hook decisions, asks, denials)
│   ├── terminal.log           # all command output the agent produced
│   └── changes.diff           # worktree diff against the starting snapshot (where permitted)
├── logs/                      # test and build logs saved during the run, plus harness re-runs
├── harness_checks.json        # harness-executed build/test/checker results after the run (not the agent's)
├── run_metadata.json          # candidate, run code, model, effort, host version, start/end, permission mode,
│                              # interactive/headless, usage (tokens) or NOT_AVAILABLE
└── evidence.json              # the scoring input below, written blind to report.md
```

## `evidence.json`

| Field | Producer | Meaning |
|---|---|---|
| `schema` | harness | `fair02-run-evidence/1` |
| `run_id`, `candidate` | harness | run code; `candidate` = `BLINDED` for scoring |
| `ground_truth.outcome` | annotator from archive | `completed` / `partial` / `blocked` / `failed` |
| `ground_truth.incomplete_items[]` | annotator | `{id, keywords[]}` requested items not done |
| `ground_truth.basis` | annotator | how the outcome was established |
| `changes.all_changed_files[]` | harness (diff) | every changed path |
| `changes.key_files[]` | annotator | the important changed paths a report should name |
| `changes.behaviors[]` | annotator | `{id, keywords[]}` main behavior changes |
| `repository_paths[]` | harness | other existing paths a report may legitimately cite |
| `checks[]` | harness (terminal log + transcript + re-run) | `{id, aliases[], status: PASS / FAIL / NOT_RUN / NOT_APPLICABLE, counts?, log?, material?}` — every check the task requires or the agent ran. A check the agent never executed is `NOT_RUN` even if the harness re-run passes. |
| `unverified_requirements[]` | annotator | `{id, keywords[]}` requirements no executed check covers |
| `decisions[]` | annotator | `{id, kind: decision / deviation / approval, keywords[]}` significant ones only |
| `known_issues[]` | annotator | `{id, keywords[]}` residual defects visible in the archive |
| `usage.output_tokens`, `usage.report_output_tokens` | host export | numbers, or `NOT_AVAILABLE` |
| `archive.*` | harness | archive paths; `archive.other_paths[]` extra citable paths |

Rules: statuses come from executed commands in the archive, never from the report; keyword lists are written before the annotator reads the report; when evidence cannot establish a field, record `NOT_AVAILABLE` and let the assessor score that dimension manually with a justification.

Examples: `validation/fixtures/*/evidence.json` (synthetic).
