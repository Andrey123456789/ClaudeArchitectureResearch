# Iteration 005 / 5.2

This directory is the corrected second template-generation series.

`5.1` preserves the earlier generation state and diagnostic evidence.
`5.2` is the clean rerun series created from the same candidate/source inputs
with corrected shared experimental controls.

## Run structure

```text
5.2/
├── M/
│   ├── Run-01/
│   └── Run-02/
├── L0/
│   ├── Run-01/
│   └── Run-02/
├── L1/
│   ├── Run-01/
│   └── Run-02/
├── K0/
│   ├── Run-01/
│   └── Run-02/
├── K1/
│   ├── Run-01/
│   └── Run-02/
├── GOAL_PROMPT.txt
├── INPUT_HASHES.json
├── SOURCE_COMMIT.txt
└── README.md
```

Each run contains:

```text
Run-XX/
├── TASK.md
├── CANDIDATE.md
├── source/
│   ├── inventory.json
│   ├── shared-research-invariants.json
│   └── v2-baseline/
└── output/
```

## What changed from 5.1

The shared construction contract was tightened equally for all candidates:

- every frozen inventory `trigger_class` must be preserved exactly;
- path/workflow policy must not be promoted to always-loaded merely for convenience;
- multi-step procedures belong to workflow owners rather than `CLAUDE.md`;
- deterministic hooks/scripts must be compatible with the Windows Claude Desktop environment;
- parent/sibling workspace inspection is explicitly forbidden;
- generation runs as an autonomous Goal with repeated audit-and-repair until objective acceptance gates pass.

`CANDIDATE.md` files were not changed for these corrections.

## Execution

Use a fresh Claude Desktop Code session for every run and keep model/effort settings identical.

For every run, use **exactly the contents of `GOAL_PROMPT.txt`** as the Goal prompt.

Do not replace it with the older one-shot instruction.

The Goal must continue through draft -> audit -> repair -> audit cycles until all binding
acceptance gates in `TASK.md` pass. Once all gates pass, it must stop rather than perform
unbounded aesthetic refactoring.

Do not add candidate-specific hints and do not expose another run's output.

## Evidence rule

Do not manually repair generated output before comparative audit.
Preserve raw run output as evidence.

The construction Claude may see the run's `inventory.json`.
A later benchmark-execution Claude must not see research/evaluation material.
## Protocol amendment 5.2.1

After the completed `M/Run-01` Goal run, the absolute workspace-boundary PASS rule was found to conflate candidate-controlled experimental isolation with Claude Desktop/tool-runtime session persistence.

`M/Run-01` is preserved unchanged as raw evidence. Its original report says `NOT PASS`, but the run is post-hoc adjudicated as **VALID / PASS for comparative use** because the substantive candidate/template gates passed and no forbidden parent/sibling/network/external research information was consumed.

The remaining nine runs use an amended common `TASK.md` that distinguishes:

- experimental isolation violations — must be `0`;
- recoverable workspace-process incidents — record + remediate, non-blocking after successful remediation;
- platform-managed persistence — informational/non-blocking unless forbidden external information is later consumed or becomes a dependency.

See:

- `protocol-amendments/5.2.1-workspace-boundary-adjudication.md`
- `protocol-amendments/5.2.1-manifest.json`
- `protocol-amendments/evidence/M-Run-01-TASK-executed.md`

Do not modify the raw `M/Run-01` output/report to rewrite history.
## Protocol amendment 5.2.2

After `L0/Run-01`, the protocol was refined to preserve the useful deep audit while preventing post-convergence token loops.

`M/Run-01` and `L0/Run-01` remain unchanged raw evidence. The remaining eight runs use a bounded verification protocol:

1. primary substantive audit with policy-semantic, V2-preservation, duplication, structure, reference, enforcement, and hygiene checks;
2. repair concrete template defects;
3. confirmation audit;
4. repeat confirmation only if it identifies a new concrete template defect;
5. stop immediately after a zero-defect confirmation audit.

Meta-evidence requests, external session-log reconstruction, repeated convergence hashing, and report-only corrections do not reopen the audit unless they reveal a concrete template defect.

See `protocol-amendments/5.2.2-bounded-convergence.md` and `protocol-amendments/5.2.2-manifest.json`.
## Protocol amendment 5.2.3 — M1 extension

Iteration 5.2 was extended after the original 5×2 series with `M1/Run-01` and `M1/Run-02`.

M1 is **Minimal Modular + replaceable capabilities**: M/V2-style organization outside the capability subsystem, plus the same four static capability slots used by L1/K1.

The generated-candidate experiment is now **6 candidates × 2 independent replicates = 12 runs**: `M / M1 / L0 / L1 / K0 / K1`.

The original ten runs remain unchanged. M1 uses the current bounded-convergence TASK.md, the same frozen source corpus, and the current shared GOAL_PROMPT.txt.

See `protocol-amendments/5.2.3-m1-extension.md` and `protocol-amendments/5.2.3-manifest.json`.
