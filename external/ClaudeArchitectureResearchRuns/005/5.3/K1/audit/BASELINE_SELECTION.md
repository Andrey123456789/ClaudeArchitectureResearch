# Baseline Selection — K1

## Decision

Use **K1 / Run-02** as the immutable Iteration 5.3 baseline.

Do not merge Run-01 files into it. Run-01 is comparative evidence only.

## Shared architecture identity

Both raw runs independently implement the intended K1 design point:

- classification order: Capability -> Kind -> Scope;
- seven Kinds: OP, DEC, STD, KNW, WF, ENF, IN;
- scope-first STD rules rather than stability levels;
- one always-loaded decision register;
- exactly four replaceable slots;
- architecture = required frame;
- persistence, backend-testing = required leaves;
- frontend = optional leaf;
- initial selections clean-architecture / ef-core(sqlserver) / nunit / angular;
- static composition;
- contracts, module manifests, role-named facets, leak checking;
- frame/leaf rule: placement belongs to the frame, technique belongs to the leaf;
- no Level hierarchy and no extra capability slots.

The two inputs are byte-identical for TASK.md, CANDIDATE.md, and the frozen source corpus.

## Why Run-02

Run-02 is the stronger controlled-refinement starting point overall.

| Measure | Run-01 | Run-02 |
|---|---:|---:|
| runtime files | **84** | 85 |
| runtime bytes | 373,146 | **346,715** |
| Markdown files | **67** | 72 |
| rule files | **18** | 21 |
| skill entry points | 28 | 30 |
| generated always-loaded estimate | ~5,315 tokens | **~4,849 tokens** |
| generated instruction checker | PASS | PASS |
| JavaScript syntax | PASS | PASS |
| K conformance-direction mutation | **missed** | **detected** |
| BOM-prefixed hook JSON | **works** | **fails** |
| active-worktree post-edit behavior | **better** | **incorrect** |

Run-02 wins because:

1. It is materially smaller in total runtime text and below the ~5k always-loaded target.
2. Its K structural checker actually rejects an illegal DEC -> STD conformance dependency. Run-01's checker accepts the same mutation and therefore does not mechanically enforce a central K invariant.
3. Independent lexical diagnostics slightly favor Run-02 for both normalized-policy and V2 source coverage; there is no signal that the smaller corpus was bought by broad semantic loss.
4. Run-02 has clearer role-named static enforcement facets and dedicated `delivery-change` and `persistence-change` WF owners.
5. The serious Run-02 enforcement defects are localized and repairable without changing K1's architecture.

## Important Run-01 advantages that set the quality bar

Run-01 demonstrates that K1 can also provide:

- active-worktree-safe hook behavior through a cwd-upward launcher;
- PostToolUse coverage for Bash and PowerShell as well as file-edit tools;
- BOM-tolerant stdin parsing;
- explicit required leaf -> architecture binding checks in its structure checker;
- module-local workflow-facet organization.

These are evidence that stronger behavior is feasible. They are not instructions to copy Run-01 files.

## Promotion principle

The 5.3 result must fix the confirmed Run-02 defects while preserving Run-02's stronger K checker, compactness, policy fidelity, and capability boundaries.

**A tie is not an improvement.**
