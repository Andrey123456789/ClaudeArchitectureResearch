# Iteration 005 preparation package

Base commit expected:

`949d4758396865ae12e2f071ca3ef058d8366091`

## What it changes

- closes Iteration 004 as **partial after scope reduction** without pretending deferred E0 probes passed;
- supersedes the old mandatory "full E0 + frozen benchmark before candidate templates" sequence;
- preserves the benchmark plan and E0 artifacts as historical/supporting methodology;
- records per-run Claude Desktop version verification instead of waiting 24–48 hours;
- clarifies `templates/v3` as a legacy scaffold;
- removes committed Python `__pycache__` and adds Python cache ignores;
- adds `prompts/005-template-generation.md`;
- adds `research/observations/005-template-generation.md` with the 5×2 run register and controlled-workspace protocol.

## Apply

1. Ensure the repository is on the expected commit and `git status` is clean.
2. From any PowerShell location inside the repository, run:

```powershell
powershell -ExecutionPolicy Bypass -File "<path-to-this-package>\apply.ps1"
```

3. Review:

```powershell
git status --short
git diff --check
git diff --stat
git diff
```

4. Commit only after review.

The script has a HEAD guard and refuses to run on a different commit or a dirty worktree.

## Important

This package does **not** create the ten Iteration-005 run workspaces. The new observation file specifies the exact allowlist and run order. Create each workspace fresh when you are ready to execute a run.

Do not run Iteration 005 from the full research-repository root.
