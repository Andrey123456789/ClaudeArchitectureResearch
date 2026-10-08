# 004 — E0 Claude Code mechanics validation

| | |
|---|---|
| Status | **PARTIAL — gate to candidate generation NOT passed.** R1 and I1 are characterized; S1, S2, A1 and R2 are characterized only on their loading half; T1 is characterized statically; W1 is not executed. |
| Date | 2026-10-08 |
| Produced by | `prompts/004-e0-mechanics-validation.md` |
| Environment (primary) | Windows 11 Pro 10.0.26200 · Claude desktop app 2.26454.x · desktop-bundled Claude Code **2.1.293** (2.1.289 before the app restarted; both measured) · model `claude-opus-5-5`, effort `xhigh` · Python 3.14.0 · Git Bash + PowerShell |
| Harness / fixtures | `research/e0/probes/` (see its README) |
| Evidence | `research/e0/results/win32-cc2.1.293-claude-opus-5-5/` (primary) and `research/e0/results/win32-cc2.1.289-claude-opus-5-5/` (earlier build) — `summary.json`, `environment.json`, `preflight.json`, per-run raw evidence and `checks.json` |
| Templates / frozen research files changed | **None.** `templates/`, `inventory.json`, `metrics-manifest.json`, `benchmark/plan.md` and candidate `DESIGN.md` / `CORE_FEATURES.md` are untouched. |

---

## 1. Result at a glance

| Probe | Status | Evidence level | Established | Still open |
|---|---|---|---|---|
| E0-R1 nested rule dirs | **PASS** | startup context record (no model call) | Rules 1 and 2 levels below `.claude/rules/` load at session start. A file outside `.claude/rules/` does not. The negative control (group removed) shows the markers absent. | Behavioral echo by the model (optional) |
| E0-I1 `CLAUDE.md` imports | **PASS** | startup context record | Direct and nested (depth 2) `@` imports load (`include`, correct parent). A plain mention does not. The L0 shape is characterized (§5.2). | Behavioral echo (optional) |
| E0-R2 path-scoped rules | **INCONCLUSIVE** | startup (partial) | Path-scoped rules, nested or flat, are **not** loaded at startup. | Loading on Read / Edit / **new-file Write**, plus non-matching controls. **Needs model-driven tool calls.** |
| E0-S1 skill discovery and triggering | **INCONCLUSIVE** | startup (partial) | `.claude/skills/<name>/SKILL.md` is discovered. Name and description reach the model's skill listing; the body is not preloaded. Project skills named `verify` / `code-review` take over the bundled skills' slots. | Description-based triggering (3 positive runs and 1 negative) |
| E0-S2 private references | **INCONCLUSIVE** | startup (partial) | The reference and the skill body are **not** in global context, and the reference is never an `InstructionsLoaded` memory file. | Reachability through the owning skill; unrelated-task control |
| E0-A1 subagent + `skills:` preload | **INCONCLUSIVE** | startup (partial) | The project agent and its preload skill are discovered. The procedure is not in the main session's context. | Preload into the spawned subagent (positive and no-preload negative) |
| E0-T1 telemetry | **INCONCLUSIVE** | static | Artifact structure for every required field is inventoried. Cost is shown to be **derived client-side**, so provider-reported cost is `TECHNICAL_UNAVAILABLE`. | Real values and cross-checks (tokens, turns, tool calls) from authenticated headless runs |
| E0-W1 launch-root boundary | **NOT_EXECUTED** | configuration only | All 4 permission modes (`manual`→`default`, `acceptEdits`, `auto`, `bypassPermissions`) are accepted by the CLI; canaries are generated outside the root. | Classification per mode (`BLOCKED` / `PERMISSION_GATED` / `REACHABLE`) |

All 9 startup-only runs give **identical check results on 2.1.289 and 2.1.293** (0 differences).

## 2. Execution constraint encountered

The intended environment is the Claude Code build bundled with the desktop app. This session ran inside it (PID tree: desktop app → `claude-code\2.1.2xx\…\claude.exe --permission-mode auto --setting-sources user,project,local`). The CLI is not on `PATH`.

A **fresh child process of that exact binary cannot authenticate**:
- `claude auth status` → `loggedIn: false, authMethod: none`;
- a minimal headless request returns `"Not logged in · Please run /login"` (`preflight.json` in both result directories).

The desktop session receives credentials from its host (`CLAUDE_CODE_SDK_HAS_HOST_AUTH_REFRESH`), and children do not inherit them. Signing in is a credential action the user must perform. A request for it was not answered because the app was quit mid-question.

Per the prompt's execution constraint, nothing model-dependent was faked or weakened. Instead:

1. The **complete behavioral harness** exists and is self-tested. `selftest` materializes all 22 run workspaces, the isolation gate passes and no placeholders are left unresolved.
2. A **startup-only mode** was added. The same fresh process, fixture, argv and prompt run, but the model endpoint is pointed at an unroutable local port. Claude Code resolves rules, imports, the skill listing and the agent listing *before* the first model request. It records them in `InstructionsLoaded` hooks and in the transcript's `instructions` / `skill_listing` / `agent_listing_delta` attachments, which are the content it hands to the model. This is harness telemetry, not Claude's claim, and it fully decides the loading-only questions (R1, I1).
3. Probes whose question involves model behavior stay INCONCLUSIVE or NOT_EXECUTED (§9).

## 3. Method

- **Fixtures.** One tiny fixture per probe under `probes/fixtures/`; none of them is V2, V3, a candidate or TaskBoard. They are stored as `dot-claude/` and renamed to `.claude/` only in the run workspace, so this repository never auto-discovers them.
- **Markers.** Each probe file carries a random marker (`E0R1-NESTED-2CCD69`, …). W1 canaries get fresh random markers per run. A marker can only appear in context, output or files if the mechanic delivered it.
- **Controls.**
  - In-run decoys: R1's `.claude/rule-decoy/`, I1's non-`@` mention, R2's frontend rule for backend tasks.
  - Separate negative runs: R1 with the group removed, R2 with non-matching read/write, S1/S2 with unrelated tasks or context-only listing, A1 with the agent without `skills:`.
- **Fresh process per run**, launched with parent-session environment variables stripped (names recorded). The run gets a new workspace outside the repository, a fresh `git init` with no remotes or history, and an isolation gate over ancestor directories.
- **Evidence channels**, strongest first:
  1. the `InstructionsLoaded` hook (`load_reason`, `parent_file_path`, `trigger_file_path`);
  2. transcript context records;
  3. structured tool events and `permission_denials`;
  4. workspace files and diff;
  5. random markers in the reply.

  Checks name the artifact they read (`checks.json`).
- **Evidence hygiene.** Exported copies redact email addresses, `sk-ant-` keys and account/organization UUIDs; raw sha256 values are kept in `run.json`. Debug logs are never exported.

## 4. Environment facts recorded (`environment.json`)

- **OS and shells.** Windows 11 (10.0.26200). The CLI uses Git Bash for `Bash` and Windows PowerShell 5.1 for `PowerShell`.
- **User-level config is empty.** There is no `~/.claude/CLAUDE.md`, `rules/`, `skills/`, `agents/` or `settings.json`, so no user-level instruction leaks into the probes.
- **Hooks work on Windows.** Command hooks (`python …hook_logger.py`) fired for `SessionStart`, `InstructionsLoaded`, `UserPromptSubmit` and `SessionEnd`. Tool hooks are configured but untested until behavioral runs.
- **Built-in context in every headless session of this build:**
  - 26 tools;
  - 5 built-in agents (`claude`, `Explore`, `general-purpose`, `Plan`, `statusline-setup`);
  - 3 built-in plugins;
  - 18 built-in skills in `system/init` (bundled skills plus the built-in plugin skill `plugin-authoring`), of which **13 are listed to the model** (≈6.3k characters): `dataviz`, `update-config`, `keybindings-help`, `code-review`, `simplify`, `fewer-permission-prompts`, `loop`, `claude-api`, `workflow-authoring`, `run`, `plugin-authoring`, `init`, `security-review`.

## 5. Findings

### 5.1 E0-R1 — nested rule directories: PASS

Evidence: `R1/startup/R1-pos-*`, `R1-neg-*`.

| File | Positive run | Negative run (group removed) |
|---|---|---|
| `.claude/rules/r1-flat.md` | loaded, `session_start`, marker in context | loaded |
| `.claude/rules/e0-group/r1-nested.md` | **loaded, `session_start`, marker in context** | absent |
| `.claude/rules/e0-group/deeper/r1-deep.md` | **loaded, `session_start`, marker in context** | absent |
| `.claude/rule-decoy/r1-decoy.md` | absent | absent |

`.claude/rules/` is discovered recursively, to at least 2 levels. A rule file without `paths` in a subdirectory behaves exactly like a flat one. **002 Q16 is answered: rule subdirectories work.** The L axis (`rules/<level>/`) and K axis (`rules/<scope>/`) are physically viable.

### 5.2 E0-I1 — imports: PASS, plus L0-shape characterization

Evidence: `I1/startup/I1-pos-*`. The startup context holds, in order: `CLAUDE.md` (`session_start`) → `docs/decisions.md` (`include`, parent `CLAUDE.md`) → `docs/nested/details.md` (`include`, parent `docs/decisions.md`) → the two imported rule files. `docs/background.md`, which is mentioned without `@`, is absent.

- **Direct import works.** This is the M shape (`@docs/technology-stack.md`) and the K0 shape (`@docs/architecture/decision-register.md`).
- **A nested import resolves relative to the importing file, at depth 2.** The K1 option "import the module's decision text from a module file" (K1 DESIGN §DEC) is viable.
- **L0/L1 shape** (`@.claude/rules/1-architecture/overview.md` and `@.claude/rules/3-project/decisions.md`):
  - A rule-directory file **with** `paths:` that is `@`-imported is loaded **unconditionally at session start** (`include`). Its frontmatter is stripped, and exactly one copy enters context: the import overrides path scoping.
  - A rule-directory file **without** `paths:` that is also `@`-imported is loaded **once** (`include`, de-duplicated; no `session_start` duplicate).
  - Both variants work physically, with no double-loading cost. But "every rule file declares `paths`" (S-09) plus "always-loaded summaries are imported rule files" (L0/L1) leaves a `paths:` field that has no runtime effect. See decision D-E0-3.

### 5.3 E0-R2 — path-scoped rules: INCONCLUSIVE (startup half verified)

Evidence: `R2/startup/R2-read-match-*`. Neither the nested path-scoped rules (`r2-scope/backend-cs.md`, `frontend-ts.md`) nor the flat one (`r2-flat-domain.md`) is in the startup context or has an `InstructionsLoaded` event. **Path-scoped rules are conditional, as intended.**

Still unverified, and the most consequential open mechanic:
- whether a matching Read loads the rule (`path_glob_match` with `trigger_file_path`);
- whether Edit flows comply;
- whether a **new file created by Write without a prior Read** receives the rule before its content is generated (`R2-write-new-match` checks first-Write content versus later corrections);
- whether non-matching reads and writes stay clean.

S-09 assigns most must-rules to path triggers, so candidate generation must not proceed on this assumption.

### 5.4 E0-S1 — skills: INCONCLUSIVE (discovery verified), plus two configuration findings

Evidence: `S1/startup/*`.

- **Discovery.** `.claude/skills/e0-ledger-summary/SKILL.md` appears in `system/init.skills`, and its exact name and description line appear in the `skill_listing` sent to the model. The body marker is **not** in startup context, so it loads on demand only.
- **Name collision with bundled skills.** Bundled skills `code-review` (listed to the model by default) and `verify` (in `init.skills` but not listed) share names with S-11's workflow skills. With project skills of those names, `init.skills` contains each name **once** and the listing shows **only the project descriptions**: the project skill replaces the bundled one. S-11/S-12 names are therefore usable, and V2's own `code-review` / `verify` behave the same way. Which skill the *Skill tool* actually invokes is checked by the optional behavioral run `S1-collision`.
- **Bundled-skill and auto-memory controls** (`S1-config-controls`):
  - `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS=1` cuts the listing from 13 bundled skills (≈6.3k characters) to the project skills **plus the built-in plugin skill `plugin-authoring`**, which this switch does not remove (506 characters).
  - `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` removes the auto-memory path (`system/init.memory_paths` becomes null).
  - These are levers for benchmark configuration, not candidate features (D-E0-4).
- **Still open:** triggering from the description without naming the skill (`S1-pos` ×3) and the unrelated control (`S1-neg`).

### 5.5 E0-S2 — private references: INCONCLUSIVE (non-globality verified)

Evidence: `S2/startup/S2-pos-*`. The owning skill is listed. Neither `references/rates.md` (`E0S2-REF-…`) nor the skill body (`E0S2-SKILL-…`) appears in any startup context record. The reference never triggers `InstructionsLoaded`, because it is not a memory file. **A private reference does not become ordinary global policy.**

Still open: whether it is **reachable** through the owning skill (Skill call → Read of the reference → the correct tariff 63.49 needs the rate table), and whether an unrelated task never reads it.

### 5.6 E0-A1 — subagent preload: INCONCLUSIVE (discovery verified)

Evidence: `A1/startup/*`.
- `.claude/agents/e0-reviewer.md` is discovered: it is in `system/init.agents` and the agent listing shows `- e0-reviewer: Reviews Pellucid configuration files… (Tools: Read)`.
- The preload skill is listed.
- The procedure marker is **not** in the main session's context.
- This build's agent schema documents `skills: "Skills preloaded for this agent."`.

Still open: does a spawned subagent receive the procedure without reading it or carrying criteria in its definition? The checks are: the subagent output contains `E0A1-PROC-…` and `PX-482, PX-731, PX-905`; no Read or Skill call on the skill happens inside the subagent; the subagent transcript shows the preload; and the no-preload negative lacks all of these. The thin `code-reviewer` (S-11) depends on this.

### 5.7 E0-T1 — telemetry: INCONCLUSIVE (static inventory)

Evidence:
- `T1/static/desktop-session-transcript-structure.json`: structure only, no content, taken from the orchestrating desktop session;
- `T1/static/cost-computation-evidence.txt`: strings from the binary, with its sha256;
- `T1/telemetry-inventory.json`;
- `cost-state` entries in the startup-run transcripts.

| Field | Availability | Raw source | Direct / derived | Recheck | Caveat |
|---|---|---|---|---|---|
| Start/finish, elapsed | structure verified | harness `run.json` clock; `result.duration_ms` / `duration_api_ms`; ISO `timestamp` per transcript entry; hook `logged_at` | direct (elapsed = derived difference) | compare `duration_ms` with harness elapsed and with transcript first→last | harness elapsed includes process start-up |
| Input tokens | structure verified | `message.usage.input_tokens` per API message (transcript and stream); `result.usage`; `result.modelUsage` | direct | sum per-message usage **deduplicated by `message.id`** (each message appears in about 2 entries with identical usage; 0 inconsistencies) and compare with `result.usage` | subagent usage lives in `subagents/*.jsonl` |
| Output tokens | structure verified | same | direct | same | — |
| Cache-read input tokens | structure verified | `cache_read_input_tokens` | direct | same | — |
| Cache-creation input tokens | structure verified | `cache_creation_input_tokens` plus the `ephemeral_5m` / `ephemeral_1h` split | direct | same | — |
| **Provider-reported cost** | **TECHNICAL_UNAVAILABLE** | none locally | — | — | `total_cost_usd`, `modelUsage.*.costUSD` and the transcript's `cost-state.totalCostUSD` are **computed client-side** from tokens and built-in per-model price tables (four tables found in the binary, e.g. `{inputTokens:5, outputTokens:25, promptCacheWriteTokens:6.25, promptCacheWrite1hTokens:10, promptCacheReadTokens:0.5}` per MTok, with a `canonicalModel` "used for the pricing lookup"). Under subscription (claude.ai) auth there is no per-request bill; under API-key auth the authoritative figure lives outside Claude Code. |
| Assistant turns | structure verified | `result.num_turns`; unique `message.id`s | `num_turns` direct; API-call count derived | compare | the semantics differ (agentic turns vs. API calls) |
| Structured tool calls | structure verified | `tool_use` blocks (stream with `parent_tool_use_id`, transcript), `Pre/PostToolUse` hooks | direct | compare the three counts | — |

Each transcript entry also carries `requestId` (one per API message) and `effort`. The OTEL console exporter is configured in the `T1-telemetry` run but untested.

### 5.8 E0-W1 — launch-root boundary: NOT_EXECUTED

Configuration preflight (`W1/startup/*`): every mode is accepted and applied. `--permission-mode manual` is reported as `default` in `system/init`. `bypassPermissions` was applied when run together with `--allow-dangerously-skip-permissions`; whether that flag is required was not tested. Canaries are generated in the parent and sibling directories of the launch root. No tool call happened.

The classification needs model-driven tool calls. The isolation relevance is wider than the canary, because Claude Code keeps material outside the launch root:
- `~/.claude/projects/<slug>/` holds **transcripts of every previous run**, including other candidates' benchmark runs;
- per-path auto-memory lives in `~/.claude/projects/<slug>/memory/`.

If W1 is `REACHABLE` in the benchmark's permission mode, prior transcripts become reachable leakage under the isolation protocol.

## 6. Other observations

1. **Silent CLI updates.** Quitting and restarting the desktop app replaced the bundled CLI 2.1.289 with 2.1.293 (both binaries remain on disk), and this session resumed on 2.1.293. "Same Claude Code version for every candidate" (benchmark plan, S-17) is not guaranteed by the desktop app. The harness now records the binary per run and supports `--claude` and `--expect-version`.
2. **Desktop sessions differ from headless CLI sessions.** The desktop Code tab adds host-provided skills (for example the `anthropic-skills:*` set visible to the orchestrating session), MCP servers and session context. Benchmark runs in desktop sessions and in headless CLI runs are **not** the same environment.
3. **Headless sessions inject user context.** Even an unauthenticated headless child, with the parent's email and organization variables stripped, received the account email (`session_context` attachment) and organization UUID (`credential_org` attachment), presumably from the local account record in `~/.claude.json`. These are redacted in exported evidence. Isolation does not cover them, but benchmark evidence handling should redact them.
4. **InstructionsLoaded hooks and transcript `instructions` / `nested_memory` records are a cheap, deterministic trigger-suite channel** (S-13, CF-17: "files loaded per task"), usable by the benchmark harness.

## 7. Affected candidate assumptions

| Assumption (where) | E0 result | Effect | Smallest consistent adaptation |
|---|---|---|---|
| Rule subdirectories by level/scope (L0/L1 `rules/<n>-<level>/`, K0/K1 `rules/<scope>/`; 002 Q16) | R1 PASS | none | none; keep the layouts |
| Always-loaded content reached by `@` imports (S-09, S-07; M, K0, K1) | I1 PASS | none | none |
| Nested import of module decision text (K1 §DEC option) | I1 PASS | option viable | none |
| L0/L1 imported summaries live in `.claude/rules/<level>/` **and** every rule declares `paths` (S-09) | I1 characterized | `paths` on an imported rule has no runtime effect; works, but the metadata misleads | D-E0-3 |
| Skill names identical to bundled skills (`code-review`, `verify`; S-11/S-12) | S1 startup | project skill replaces the bundled listing entry | none; record it in the map. Behavioral confirmation pending |
| Knowledge skills trigger from their description (S-11/S-12; all candidates) | **open** | — | decided after behavioral S1 |
| Skill-private references (S-05d; `ef-core/references/dev-seeding.md` etc.) | non-global ✔; reachability **open** | — | decided after behavioral S2 |
| Thin `code-reviewer` preloads `code-review` (S-11; all candidates) | **open** | — | if preload fails: the agent's first step reads the skill (a routing pointer, still no copied criteria), or the review runs in the main session |
| Must-rules carried by path triggers, including new files (S-09; all candidates) | **open** | highest risk | if Write-before-Read does not load rules: (a) scaffold/new-file workflows read a sibling or the owning rule first; (b) a `PreToolUse` hook on `Write` names the owning rule; (c) move new-file-critical must-rules to the always-loaded tier within S-18 |
| Always-loaded ceiling about 5k tokens "including the skill listing" (S-18) | ≈6.3k characters of bundled listing in every session | the budget is partly consumed by non-candidate skills | D-E0-4 |
| Isolation by workspace reachability (isolation protocol) | **open** (W1), plus out-of-root transcripts and auto-memory | — | D-E0-5 |
| Pinned Claude Code version (S-17, plan) | the desktop app auto-updates | parity risk | D-E0-1 |

No candidate file was changed.

## 8. Decisions needed before candidate generation

| ID | Decision | Recommendation |
|---|---|---|
| D-E0-1 | Which Claude Code build is frozen for the research, and how is it pinned? | Freeze **2.1.293**: copy the binary to a pinned path outside the desktop app's update directory, run with `--claude <pinned> --expect-version 2.1.293`, and re-run `startup all` whenever the build changes. |
| D-E0-2 | Execution surface: headless CLI (`claude -p`) or desktop Code-tab sessions? | Headless CLI. It is reproducible, gives a full structured stream and has no host-injected skills or MCP. This requires a one-time `auth login` of the CLI. |
| D-E0-3 | L0/L1 always-loaded summaries under `.claude/rules/<level>/` | Allow, for L0/L1 only: imported summaries carry **no** `paths` and the header `Loaded: always (imported)`. The S2 checker exempts them from "every rule declares `paths`". The alternative is moving them to `docs/`, which hides the level axis. Physically, both are proven to load exactly once. |
| D-E0-4 | Benchmark context controls | Decide whether runs use `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS=1` (removes about 6k characters of non-candidate listing; `plugin-authoring` remains) and `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`. The setting must be identical for all candidates including V2, and it fixes what S-18 measures. |
| D-E0-5 | Isolation hardening, depending on W1 | Per-run unique workspace paths (auto-memory is keyed by path). If W1 is `REACHABLE` or `auto`-dependent in the chosen mode, add a separate OS user or `CLAUDE_CONFIG_DIR` per benchmark batch, so earlier transcripts are not on disk under the reachable config dir. |
| D-E0-6 | Benchmark permission mode | Pin one mode before W1 is interpreted (`acceptEdits` with `--permission-prompts none` is the harness default; this session ran `auto`). |

## 9. Limitations

- **No model behavior was observed in fresh sessions.** Triggering, path loading on tool use, preload, reference reachability, telemetry values and the boundary all wait on an authenticated CLI.
- **Startup evidence shows what Claude Code assembled for the model,** not whether the model attends to it. R1 and I1 ask only about loading, so they are decided; the optional behavioral echo runs remain.
- **One run per condition at startup.** Startup assembly is deterministic, so this is adequate, and the result is identical across two builds. Skill triggering is stochastic, so behavioral S1 uses 3 positive runs, which is a minimal existence/reliability signal, not a rate estimate.
- **The marker style is a probe convenience.** Rule bodies are deliberately tiny, so no conclusion about adherence to long policy text is drawn.
- **Character counts are not tokens.** Token-based S-18 calibration needs authenticated runs (T1 per-message usage).
- **Nested skill directories** (`.claude/skills/<group>/<name>/`) were not probed. No candidate relies on them; L0 assumes a flat skill namespace.
- **Results were re-evaluated with the final harness.** Evaluators were refined after the first startup runs (redaction, version guard, collision/config characterization). Raw evidence was re-exported from the unchanged raw run directories, and every `checks.json` was regenerated by the final `e0.py`.

## 10. Gate to the next iteration

Iteration 004 is **not complete**. Candidate generation must not rely on:
- path-triggered must-rules (R2);
- description-triggered skills (S1);
- reachability of skill references (S2);
- `skills:` preload (A1);
- telemetry values (T1);
- workspace isolation (W1).

**Next step (top-level, outside any Claude session):**

```bash
"C:/Users/atonkonog/AppData/Roaming/Claude/claude-code/2.1.293/83cb0bd7fed4/claude.exe" auth login
python research/e0/probes/harness/e0.py --expect-version 2.1.293 preflight
python research/e0/probes/harness/e0.py --expect-version 2.1.293 run all
python research/e0/probes/harness/e0.py summarize
```

`run all` runs 23 fresh sessions (21 behavioral run definitions; `S1-pos` repeats 3 times) on `claude-opus-5-5` at effort `xhigh`, with a $3 per-run budget cap. `W1-bypass` runs one session with `bypassPermissions`; its prompt touches only the generated canaries. Alternatively, run `auth login` and then ask Claude to continue Iteration 004: the harness strips parent-session variables, so it also works from inside a Claude session.

After the run:
1. interpret `summary.json`;
2. complete §5.3–§5.8;
3. take decisions D-E0-1…D-E0-6;
4. only then freeze benchmark scenarios and generate candidates.
