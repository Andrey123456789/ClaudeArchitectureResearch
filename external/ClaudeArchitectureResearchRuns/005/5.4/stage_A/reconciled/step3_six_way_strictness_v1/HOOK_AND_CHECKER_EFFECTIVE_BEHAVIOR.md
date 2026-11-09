# Hook and checker effective behavior — Stage A Step 3 (v1)

Three evidence layers are kept apart throughout:

| Layer | What it shows | Status in Step 3 |
|---|---|---|
| **Text** | What the instructions tell the agent (rules, skills, root files). | Source-read for all 196 policies × 6 candidates. |
| **Static enforcement** | What a hook script or checker returns when run directly on a fixture (allow / ask / deny / exit 2 / finding). | Executed: inherited v3 suites (`SAME_TASK_MATRIX_V3.json`, 44-suite tally) and Step 3 probes PROBE-HOOK-01/02/03 (Node v26.13.0, disposable copies under `_work/`, removed afterwards). Other checker logic is source-read only, as marked per root. |
| **Live host** | How Claude Code shows and applies those outputs to a running agent (interactive and headless). | **NOT_RUN** (Q-08). No live host, no Git command, no network, no package restore was used. |

A static `deny` or exit 2 is evidence of what the script decides, not proof that a live agent is stopped.

## 1. Registered hooks and budgets (from each `.claude/settings.json`)

| | PreToolUse (Bash/PowerShell) | PostToolUse | PostToolUseFailure | Stop |
|---|---|---|---|---|
| M | dependency-guard.mjs · 30 s · onFailure block | dependency-guard (shell) 60 s; file-change.mjs (Edit/Write/MultiEdit) 60 s | dependency-guard 60 s | stop-co-change.mjs 60 s |
| M1 | pre-tool-use.js · **no timeout** · onFailure block | post-tool-use.js (edits and shell) · no timeout | post-tool-use.js · no timeout | stop.js · no timeout |
| L0 | claude-hook.mjs pre-bash · 30 s · onFailure block | post-bash 60 s; post-edit 60 s | post-bash 60 s | stop 60 s |
| L1 | pre-shell-command.mjs · **15 s** · onFailure block | post-change-checks.mjs 30 s (edits and shell) | 30 s | stop-cochange.mjs **15 s** |
| K0 | hook.cjs pre-tool-use · 30 s · onFailure block | post-tool-use 60 s (edits incl. NotebookEdit, shell) | 60 s | stop 60 s |
| K1 | dispatch.cjs PreToolUse · 30 s · onFailure block | PostToolUse 60 s (edits and shell) | 60 s | Stop 60 s |

No candidate sets `permissions`. All six PreToolUse hooks fail closed (`onFailure: block`); post and Stop hooks are advisory on failure. Budgets are configuration facts; whether a host enforces a missing timeout (M1) or a 15 s budget (L1) differently is NOT_RUN (v3 CL01 records the same facts and their NOT_RUN status).

## 2. Static PreToolUse decisions (direct runs, each command twice with the same state)

### PROBE-HOOK-01 — dependency and project-reference commands (`HOOK_PROBE_RESULTS.json`)

| Case | M | M1 | L0 | L1 | K0 | K1 |
|---|---|---|---|---|---|---|
| P1 `npm install left-pad@1.3.0` | allow | deny/deny | allow | deny/allow | deny/deny | allow |
| P2 `dotnet add <Api> package Serilog.AspNetCore` (no version) | allow | deny | allow | deny/allow | deny | **block** |
| P3 same, `--version 8.0.3` | allow | deny | allow | deny/allow | deny | allow |
| P4 P3 + both review markers | allow | allow | allow | deny/allow | allow | allow |
| P5 `dotnet add <Application> reference <Domain>` | allow | deny | **block** | ask | deny | **block** |
| P6 `dotnet add <Application> reference <Infrastructure>` | allow | deny | **block** | ask | deny | **block** |
| P7 `dotnet add <Application> package MediatR --version 12.4.1` | allow | deny | allow | deny/allow | deny | allow |
| P8 `dotnet add <Api> package AutoMapper --version 13.0.1` | allow | deny | allow | deny/allow | deny | allow |

"deny/allow" = refused on the first run, allowed on the identical retry (L1's 30-minute window). M1 and K0 open with their self-written markers (`# add-dependency: checked`, `# add-dependency: reviewed`; references: `# project-reference: checked`, `# project-references: approved`). K1 opens a reference command only when the edge is recorded as an accepted decision in its register. Package-specific flags (MediatR, AutoMapper) come after the edit from the manifest checkers, not from these PreToolUse decisions.

### PROBE-HOOK-02 — npm peer-dependency bypass (`HOOK_PROBE2_RESULTS.json`)

All six refuse every variant on both runs: `--legacy-peer-deps`, `--force`, `npm i -f`, `npm_config_legacy_peer_deps=true …`, `npm ci --legacy-peer-deps`, `--legacy-peer-deps=true`, `npm config set legacy-peer-deps true`, and **the same commands carrying both dependency markers** (Q9, Q10). M, L0, K1 exit 2; M1, L1, K0 deny. The control (pinned install, no bypass) differs only through the install gate above. Persistent bypass through an edited `.npmrc` is caught only by L0's post-edit manifest check (source-read; DEP-025 D2).

### PROBE-HOOK-03 — removal and bare update (`HOOK_PROBE3_RESULTS.json`)

| Case | M | M1 | L0 | L1 | K0 | K1 |
|---|---|---|---|---|---|---|
| `dotnet remove <Api> package …`, `npm uninstall …` | allow | deny | allow | deny/allow | deny | block |
| bare `npm update`, `npm audit fix`, `dotnet package update` | allow | deny | allow | deny/allow | deny | block |
| control `dotnet restore` | allow | allow | allow | allow | allow | allow |

### Inherited from v3 (`SAME_TASK_MATRIX_V3.json`, not re-run)

- **Git** (PV2-01): identical in all six — `git status`, `git log`, `git -C sub status` allow; `git commit`, `git -c … commit`, `git status && git commit`, `bash -c "git clean -fd"`, `git push --force`, `git reset --hard` ask. Q-04: K0 also asks for `echo git commit -m x` (not in this matrix).
- **Malformed input**: all six refuse empty, malformed, array, number-command and no-command payloads (M1, K0 deny; others block). Blank-command edge Q-02 differs (L0, K0, K1 allow; nothing runs).
- **Manifest tasks**: floating versions without a matching exception record rejected in all six; with a matching record accepted; CPM/PackageVersion rows identical with the SDK (Q-11 differs only without it).

## 3. Material enforcement roots: text vs static vs live

Each root is counted once; the policies it bears on are listed. "Executed" = static script outputs observed; "source-read" = checker or hook code read, not run on a fixture.

| Root | Policies | Text (all six unless noted) | Static enforcement | Basis | Live host |
|---|---|---|---|---|---|
| RC-ENF-REFERENCE-CMD-GATE | ARC-020 D5, GOV-017 D5 | Reference-graph changes are Reserved | Pre-execution gate on `dotnet add/remove reference`: K1 recorded edge, L0 always block, L1 ask, M1/K0 marker; M none (reminder after) | Executed (P5, P6) | NOT_RUN |
| RC-ENF-DEP-INSTALL-GATE | DEP-004 D2 (also DEP-003/005, non-material) | add-dependency checks before install | M1/K0 marker; L1 deny once; K1 blocks only without an exact version; M, L0 allow and remind | Executed (P1–P4, R3–R5) | NOT_RUN |
| RC-ENF-INNER-LAYER | ARC-002, ARC-008, ARC-019 | Inner layers stay free of framework/EF Core | After edits, M1 flags ASP.NET Core / EF Core namespaces in inner-layer code, L1 and K1 flag the packages and framework references in inner-layer projects; M, L0, K0 rely on text and review | Source-read | NOT_RUN |
| RC-ENF-MEDIATOR-PKG | ARC-009 | No mediator/CQRS packages | M1, L0, L1 flag MediatR and Kommand; M and K0 flag MediatR only; K1 has no mediator package flag | Source-read | NOT_RUN |
| RC-ENF-TEST-REFS | ARC-028 | Fixed test-project references | M, M1, L1, K1 report an atypical test reference as a finding; K0 adds a notice; L0 none | Source-read | NOT_RUN |
| RC-ENF-COMPETING-TEST-FW | TST-001 | One test framework (NUnit) | M1, L1, K1 flag a second framework; M, L0, K0 do not | Source-read | NOT_RUN |
| RC-ENF-PKG-LISTS | DEP-002 | Use the approved library | AutoMapper flagged by K0, L0, L1 only (per-package lists differ) | Source-read | NOT_RUN |
| RC-ENF-MIGRATION-REMINDER | PST-009, PST-010 | Migration/seed co-change duties | Stop reminders differ in trigger and point in opposite directions: model change without a migration (PST-009) reminded by M1, L1, K1; changed-migration review (PST-010) reminded by M, L0, K0, K1; only K1 has both | Source-read | NOT_RUN |
| RC-ENF-IDE0005-BUILD | RUN-010 | Remove unused usings | Only L0's CLI build reports IDE0005 (EnforceCodeStyleInBuild + GenerateDocumentationFile + warning severity) | Source-read (build not run) | n/a (build tool) |
| RC-ENF-TOP-LEVEL-TESTS | DEP-024 D2 | No top-level `tests/` | L1 violation after a project-file edit; K1 warning in `verify`; others none | Source-read | NOT_RUN |
| RC-ENF-NPMRC-BYPASS | DEP-025 D2 | No peer-dependency bypass | Only L0 checks an edited `.npmrc` | Source-read; shell variants executed (PROBE-HOOK-02) | NOT_RUN |
| RC-ENF-DEP-REMOVAL-GATE (extras) | none (not canonical) | Removal goes through add-dependency (same text) | M1/K0 marker; L1 once; K1 block; M, L0 allow | Executed (PROBE-HOOK-03) | NOT_RUN |

Non-material enforcement roots (RESERVED-GRAPH, CODESTYLE-BUILD, CPM-NO-SDK, NPM-LOCKFILE, GIT-Q04, TEST-CHANGE-REMINDER-SCOPE, REVIEWER-MULTIEDIT, PKG-GITIGNORE) are recorded in `ROOT_CAUSE_SUMMARY.json`.

## 4. Stop hooks

All six register a Stop hook that blocks finishing **once per change state** and asks the agent to address each co-change reminder or say why it does not apply; none loops on its own continuation. None of them gates `verify` or `code-review` (WF-002/WF-003 have no mechanical gate in any candidate). What they remind about differs (TST-009 test-change scope; PST-009 model-without-migration; PST-010 migration review). Whether the host re-invokes the agent after a Stop block, and how often, is NOT_RUN.

## 5. Systematic pattern

M1, L1 and K1 deliver more mechanical checks through capability modules (inner-layer, competing test framework, test references, top-level tests); M and L0 rely more on reminders; K0 and M1 gate commands with self-written markers that the agent can add without any approval (the gate makes the step explicit, it does not verify it). These are architecture-specific enforcement choices, not defects. The normative text behind each root is the same in all six.

## 6. Manual reproduction procedure for live-host behavior (Q-08)

Not executed in Step 3. Intended for a separately authorized pilot. Use a disposable directory outside every research repository.

1. For candidate `<C>`, copy `stage_A/reconciled/step2_controlled_repair_v3/candidates/<C>/template/` to a new empty temporary folder. Add the four minimal project files used by `_tools/hook_probe.py` (`make_fixture`). Initialize a throw-away Git repository **inside that temporary folder only** (Git commit gating needs a work tree).
2. Start Claude Code in that folder (interactive). Ask the agent to run, one at a time, the commands of PROBE-HOOK-01 P1, P5, P6, PROBE-HOOK-02 Q1 and PROBE-HOOK-03 R1, and `git commit -m test` after creating one file. Record for each: whether the command ran, what the agent saw (reason text), and whether the user was prompted (`ask`).
3. Repeat step 2 headless (`claude -p "<instruction>"` with the same instruction), recording whether `ask` stalls, is refused or proceeds.
4. Edit a project file to add `<ProjectReference>` from Application to Infrastructure and an EF Core package to Application; record whether the PostToolUse feedback reaches the agent and whether it reacts.
5. Make a model change without a migration and end the turn; record whether the Stop hook blocks once and whether the agent addresses the reminder.
6. Temporarily rename `node` on the PATH inside a throw-away shell (or point the hook at a missing script in the copy) and run one shell command; record whether `onFailure: block` refuses it.
7. Compare every observation with the static rows in sections 2–4. Any difference is a host fact to add to the record, not a revision of the static results.

No network access is needed: the commands are refused or only classified before execution; any command that would execute a real install must be cancelled at the prompt.

## 7. What cannot be concluded

- That a live agent is actually stopped, prompted or corrected by any hook (all NOT_RUN).
- How M1's missing timeouts or L1's 15 s budgets behave under load.
- Build-time behavior of RC-ENF-IDE0005-BUILD and RC-ENF-CODESTYLE-BUILD (no build was run in Step 3).
- Anything about benchmark performance, code quality or productivity: enforcement strictness is not quality.
