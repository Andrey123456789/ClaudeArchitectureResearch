# Approved scope and decisions

Sources: `_STAGE_A_KIT/72_APPROVAL_AND_HANDOFF_EN.md` (latest, takes precedence on CPM), `_STAGE_A_KIT/62_APPROVED_DECISIONS_AND_GATES_EN.md`, `_STAGE_A_KIT/71_CLAUDE_STEP2_PARITY_CLOSURE_TASK_EN.md`. This file is a compact index; those files are the authority.

## User approvals applied

| Topic | Decision |
|---|---|
| CPM | All six checkers verify the effective MSBuild-evaluated `ManagePackageVersionsCentrally`. K0 is not reverted to literal checks. |
| Git, HQ-01 | Pre-existing uncommitted changes before a modifying task: an authorized scoped commit, or pause for manual resolution. Headless with no standing choice stops. An explicit instruction can authorize rewriting `main` unless another policy forbids it. A generic workflow approval is not authority. No company-scale Git framework. |
| Caching, HQ-02 | Invalidation stays coherent with commit, rollback, concurrency and failure. Pre-commit invalidation only if correctness is demonstrated. |
| Versions, HQ-03 | Pinned stable by default. Floating and prerelease only through explicit, scoped authorization, and checkers honor it. |
| Headless, HQ-04 | Implement an explicitly pre-approved Reserved change; never make a new Reserved decision. |
| npm, HQ-05 | A generic `ask` or magic comment does not override the peer-bypass prohibition. |
| PI-012, HQ-06 | Classify by semantics, conditions and source authority, not by negation. Do not elevate specialized security-audit criteria into universal `MUST_NOT`. |
| Compiled queries | `RUN-008` admits measured or compelling evidence, in all candidates, with no artificial strengthening. |
| Production migrations | `WF-019` default stays. No unconditional wording may make an explicitly authorized exception impossible. Credential controls and the Production seeding prohibition stay. |
| Swagger UI, CUSTOM_SETTINGS, HTTP timeouts, security scans, fast/slow tests | Prior decisions stand. No rewrite without evidence of a real gap. |
| CI/CD | Out of practical benchmark scope. Do not expand CI. |
| Four extra claims | Candidate-specific proposals, not new common policies. |

## Explicit non-goals

No Step 3, no benchmark. No research-repository Git mutation. No network, registry or external repository. No read, list or hash of `stage_A/codex_iterative_search*`. No external publication. No edit to `inputs/`, `step2_classification/`, `step2_semantic_audit_v1/` or `step2_controlled_repair_v1/`. No homogenizing of M, L or K structures or of optional capability delivery. No new shared policy.

## Six reviewer readings to adjudicate

`R02-TASK-SCOPE`, `R02-HEADLESS-DIRTY`, `R04-RECORD-FORGERY`, `R01-COMMON-VALUE`, `R01-TRIGGERED-CLASS`, `R22-UNDER-EXTRACTION`. Results: `REVIEWER_SIX_READINGS.md`.

## How this run is organized

v1's 27 rule checkpoints stay in v1 and replay here as regression suites. v2 has its own changes and checkpoints. Order and evidence: `GATE_LOG.jsonl`, `CHECKPOINTS/`, `CHANGE_LOG.jsonl`.
