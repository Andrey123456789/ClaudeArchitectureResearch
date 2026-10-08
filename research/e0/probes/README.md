# E0 probe harness

Reproducible fixtures and harness for the E0 Claude Code mechanics probes (`research/e0/README.md`). Findings are in `research/observations/004-e0-mechanics-validation.md`.

## Layout

```text
probes/
├── probes.json            run definitions: fixture, prompt, role, permission mode, markers
├── fixtures/<ID>/          tiny dedicated fixtures (no V2/V3/candidate/TaskBoard content)
│   └── dot-claude/         becomes `.claude/` only inside the run workspace
├── fixtures/A1-variants/   overlay for the A1 negative control (agent without `skills:`)
└── harness/
    ├── e0.py               prepare / run / startup / collect / evaluate / summarize
    └── hook_logger.py      silent command hook: appends each hook payload to <run>/live/hooks.jsonl
```

Fixtures are stored as `dot-claude/` and `CLAUDE.fixture.md` so that no Claude Code session opened in this research repository discovers fixture rules, skills or agents. The harness renames them to `.claude/` and `CLAUDE.md` only in the run workspace.

## What one run does

1. Materializes the fixture into a fresh workspace `<workroot>/<run>-<UTC>/ws` outside the repository (default workroot: `$E0_WORKROOT` or `<tmp>/e0-runs`).
2. Writes `ws/.claude/settings.json` with observational hooks only: `SessionStart`, `InstructionsLoaded`, `UserPromptSubmit`, `Pre/PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`, `SubagentStart/Stop`, `Stop` and `SessionEnd`. The hook prints nothing, so it cannot add context.
3. Runs `git init` plus one commit with a neutral identity. This is a fresh repository with no research history and no remotes.
4. For W1, generates per-run random canaries in the parent directory and in a sibling directory of `ws`.
5. Runs the **isolation gate**: no `CLAUDE.md`, `CLAUDE.local.md` or `.claude/` in any ancestor directory, apart from the user config dir, which is recorded separately.
6. Launches a **fresh** headless process. The prompt goes in on stdin and parent-session environment variables are stripped (names are recorded, values never are):

   ```text
   claude -p --output-format stream-json --verbose --include-hook-events --model <m> --effort <e>
          --permission-mode <mode> --permission-prompts none --setting-sources user,project,local
          --max-budget-usd <n> --session-id <uuid>
   ```

7. Collects the stream (`stream.jsonl`), `stderr.txt`, `hooks.jsonl`, and the session transcript plus the subagent directory from `~/.claude/projects/*/<session-id>*`. It also records a post-run manifest, `workspace-diff.patch` and `changed-files/`.
8. Exports evidence to `research/e0/results/<env-id>/<probe>/<run>-<UTC>/`. Emails, `sk-ant-` keys and account/organization UUIDs are redacted. The raw sha256 of every file is kept in `run.json`, and the unredacted raw files stay in the workroot.
9. Runs deterministic checks and writes `checks.json`. Each check names the artifact it reads.

**Startup-only mode** (`startup`) runs the same fixture, argv and prompt. It sets `ANTHROPIC_BASE_URL=http://127.0.0.1:9` (an unroutable local port) and `CLAUDE_CODE_MAX_RETRIES=0`, so no model request can leave the machine whatever the login state. The evidence is what Claude Code assembled for the model:
- `InstructionsLoaded` hooks;
- `system/init` (tools, skills, agents, permission mode);
- the transcript's `instructions`, `skill_listing`, `agent_listing_delta` and `prompt_snapshot` records.

Startup mode never tests model behavior (triggering, adherence, tool calls, permissions).

## Evidence channels (strongest first)

| Channel | Source | Proves |
|---|---|---|
| `InstructionsLoaded` hook | `hooks.jsonl` | Claude Code loaded a memory/rule file, with `load_reason` (`session_start`, `include`, `path_glob_match`, `nested_traversal`, `compact`), `parent_file_path` and `trigger_file_path` |
| Transcript context records | `transcript/main.jsonl` attachments `instructions`, `skill_listing`, `agent_listing_delta`, `nested_memory`, `prompt_snapshot` | the exact content Claude Code put in the model's context |
| Structured tool events | `stream.jsonl` `tool_use`/`tool_result` (+ `parent_tool_use_id` for subagents), `Pre/PostToolUse` hooks, `result.permission_denials` | what Claude actually did, and what was gated |
| Workspace state | `changed-files/`, `workspace-diff.patch` | the result of the work, for example whether a rule's required header is present |
| Final reply | `result.result` | used only for random markers that cannot be guessed, never as proof of loading by itself |

## Commands

Run from the repository root. Python 3.10+ and Git are required.

```bash
# environment record (no model call)
python research/e0/probes/harness/e0.py env

# can a fresh headless process authenticate? (one minimal request when logged in)
python research/e0/probes/harness/e0.py preflight

# loading/discovery evidence without any model call
python research/e0/probes/harness/e0.py startup all

# full behavioral suite: every run in a fresh process (needs an authenticated CLI)
python research/e0/probes/harness/e0.py --expect-version 2.1.293 run all

# single run / re-evaluation / summary
python research/e0/probes/harness/e0.py run R2-write-new-match
python research/e0/probes/harness/e0.py evaluate
python research/e0/probes/harness/e0.py summarize
```

Binary selection: `--claude PATH`, or `$E0_CLAUDE`, or `claude` on PATH, otherwise the newest desktop-bundled CLI under `%APPDATA%\Claude\claude-code\*\*\claude.exe`. The desktop app updates this bundled CLI on its own: 2.1.289 became 2.1.293 during this iteration. Pin it with `--claude` and `--expect-version`.

**Authentication.** A headless child does not inherit the desktop app's session credentials. Before any behavioral run, sign in the exact CLI once from an ordinary terminal (this writes `~/.claude/.credentials.json`; `auth logout` removes it):

```bash
"C:/Users/atonkonog/AppData/Roaming/Claude/claude-code/2.1.293/83cb0bd7fed4/claude.exe" auth login
```

**Manual (interactive/desktop) sessions.**
1. `prepare RUN` prints a workspace path and the exact prompt.
2. Open a fresh session in that workspace, paste the prompt, and end the session.
3. Run `collect <run-dir> --session-id <id>`.

Manual sessions have no `stream.jsonl`, so checks fall back to hooks, the transcript and workspace files.

## Status rules (`summary.json`)

- **Behavioral runs** decide a probe whenever they exist. A run is *invalid* (and the probe INCONCLUSIVE) when any of these happen:
  - there is no result event, or the run errored or timed out;
  - a context-only prompt used tools;
  - a no-read instruction was violated before the write under test;
  - the delegation to the subagent did not happen.
- **Startup-only runs** decide only R1 and I1, because discovery and imports are resolved at session start. For R2, S1, S2 and A1 they establish the loading half only, and the probe stays INCONCLUSIVE until the behavioral runs exist. W1 startup runs only validate configuration: the mode is applied and the canaries sit outside the root.
- **E0-T1** status comes from `T1/telemetry-inventory.json`. It is LIMITED when any required field is not directly available; provider-reported cost is expected to be `TECHNICAL_UNAVAILABLE`.
- **E0-W1** classification per mode is `REACHABLE` > `PERMISSION_GATED` > `BLOCKED` > `INCONCLUSIVE`, taken from tool results and `permission_denials`.
