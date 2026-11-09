# Claude Code handoff — FAIR-02 + CP-01

## Install

Extract the **contents** of this ZIP directly into:

`C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.4\_STAGE_A_KIT\`

The ZIP deliberately does **not** contain a parent `_STAGE_A_KIT` directory. After extraction, the folder layout must be:

```text
005\5.4\
└── _STAGE_A_KIT\
    ├── 00_START_CLAUDE_EN.txt
    ├── 76_CLAUDE_FAIR02_CP01_TASK_EN.md
    ├── Benchmark_Run_Report_Contract_EN.md
    ├── 76_README_FAIR02_CP01_EN.md
    └── ide0005_probe_en\
        ├── Test-IDE0005.ps1
        ├── 76_README_FAIR02_CP01_EN.md
        ├── CONFIG_PROVENANCE_SHA256.json
        ├── Source.cs
        ├── Probe.csproj
        └── configs\
            ├── M\
            │   ├── .editorconfig
            │   └── Directory.Build.props
            └── L0\
                ├── .editorconfig
                └── Directory.Build.props
```

If there is an existing `_STAGE_A_KIT/README_EN.md`, keep a copy or rename it first: this bundle does not need to overwrite existing instructions. All other bundle names are scoped to the present task except the reused reporting-contract file.

## Start Claude

Use a **new Claude Code session** in the working directory `...\005\5.4`; no `/goal`. Paste the entire contents of `00_START_CLAUDE_EN.txt` and send. Do not run the PowerShell test manually: the Claude task includes reviewing and running it on Windows if an active .NET 10 SDK is available.

All task outputs belong in `stage_A/reconciled/benchmark_readiness_fair02_cp01_v1/`. Candidate trees, Step 2 and Step 3 are read-only. If the environment has no .NET 10 SDK, CP-01 must be recorded as NOT_RUN rather than guessed.
