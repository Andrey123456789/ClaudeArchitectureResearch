# Iteration 005 — clean final restart

This directory is the clean 5×2 template-generation series.

The previous mixed/aborted Iteration-005 directory is archived outside this directory and is not experimental evidence for this series.

## Run structure

```text
005/
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
└── K1/
    ├── Run-01/
    └── Run-02/
```

Every run contains only:

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

There is no `ASSIGNED_CANDIDATE.txt`.

`TASK.md` is byte-identical across all ten runs.
`CANDIDATE.md` is byte-identical inside each candidate pair.
All `source/` inputs are byte-identical across all ten runs.

## Execution order

Run two rounds:

```text
M/Run-01
L0/Run-01
L1/Run-01
K0/Run-01
K1/Run-01

M/Run-02
L0/Run-02
L1/Run-02
K0/Run-02
K1/Run-02
```

Use a fresh Claude Desktop Code session for every run and keep model/effort settings identical.

Start every run with exactly:

```text
Read `TASK.md` completely and execute the task to completion, including all required inputs, deliverables, and final self-checks.
```

Do not add candidate-specific hints and do not expose another run's output.

## Evidence rule

Do not manually repair a generated run before comparative audit.
Preserve raw output as evidence.

The construction Claude may see `inventory.json`.
A later benchmark-execution Claude must not see research/evaluation material.
