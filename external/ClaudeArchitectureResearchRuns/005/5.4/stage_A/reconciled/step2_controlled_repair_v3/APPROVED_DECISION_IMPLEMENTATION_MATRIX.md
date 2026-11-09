# Approved decision implementation matrix (PV2-01 to PV2-04, and two corrections under approved semantics)

Authority: kit 74 Part B (approved in the task itself) and `Stage_A_Step2_Post_V2_Approved_Decisions_EN.md`. Each decision is one logical change with its own gate; checkpoints in `CHECKPOINTS/`, every attempt in `GATE_LOG.jsonl` and `GATE_ATTEMPTS/`.

## PV2-01: Git PreToolUse permission parity

Change `PV2-01-GIT-GATING`. Gate: **PASS_WITH_DOCUMENTED_NOT_RUN** after 2 attempt(s). Own suite: 480 pass, 0 fail, 3 not run. Whole cumulative run at that gate: 2801 pass, 0 fail, 25 not run.

| Approved requirement | Implementation | Check and outcome |
|---|---|---|
| M, M1, L0, L1, K1 gate repository-changing Git within their own hooks | K0 table placed once, byte-identical, in each hook (M dependency-guard.mjs, M1 dependency-commands.js, L0 claude-hook.mjs, L1 pre-shell-command.mjs, K1 classify-command.cjs); K0 untouched | source check: block byte-identical to the reference and equal to K0 apart from helper names |
| Read-only git status/diff/log run without a Git prompt | 25 read-only or non-Git fixtures | allow in all six |
| Mutations distinguished, incl. global options, wrappers, multi-command lines; no substring heuristic only | 41 Bash + 3 PowerShell mutating fixtures (-C, -c, --git-dir, bash -c, sh -c, cmd /c, pwsh/powershell -Command, env, VAR=, &, quoted git.exe path, ; && /) | ask in all six |
| Return ask; an existing more restrictive non-Git guard still denies | 3 combined lines with npm --force/--legacy-peer-deps | deny or block in all six; L1 mutation that moves the ask first is caught |
| ask is not authorization; HQ-01/GOV-015, dirty tree, headless, scoped commits, main rewrite preserved | ask reason names the explicit-request rule; git-workflow says the prompt is not authorization; R02 and C04 replay | R02/C04 suites PASS at every gate; audit interaction rows |
| No unconditional commits; dependency guards not weakened | no commit step added; C04 sweep; DEP-025 fixtures | PASS |
| Script-level decisions verified for six with common fixtures; live host separate | one matrix on six real hooks | live host ask display/answer and headless behavior NOT_RUN |

## PV2-02: Fail-closed malformed shell PreToolUse input for M and M1

Change `PV2-02-FAILCLOSED-INPUT`. Gate: **PASS_WITH_DOCUMENTED_NOT_RUN** after 2 attempt(s). Own suite: 89 pass, 0 fail, 2 not run. Whole cumulative run at that gate: 2323 pass, 0 fail, 22 not run.

| Approved requirement | Implementation | Check and outcome |
|---|---|---|
| Block malformed, empty, non-object JSON | M readInput(invalidInput) -> exit 2; M1 readStdinJson -> deny | malformed, empty, whitespace, BOM-only, array, string, number, null: blocked |
| Block missing, blank, non-string tool_input.command on shell PreToolUse | explicit checks in both hooks | no tool_input, non-object, no command, blank, empty, number, array, command under another field, PowerShell without command: blocked |
| Block inconsistent event/tool payloads when applicable | M: unhandled or missing event, missing tool_name; M1: event other than PreToolUse, missing tool_name | blocked |
| Keep valid read-only commands allowed; no command required on unrelated events | git status/diff/log, ls, Get-ChildItem, npm ci, BOM+valid JSON allowed; non-shell tool allowed; M PostToolUse without command exit 0 | PASS |
| Direct execution: exit codes and decision payloads; host onFailure untested | adversarial matrix + 5 mutations | live host application of exit 2/deny/onFailure NOT_RUN |

## PV2-03: Remove the K0-only root requirement for Directory.Packages.props

Change `PV2-03-K0-CPM-ROOT`. Gate: **PASS_WITH_DOCUMENTED_NOT_RUN** after 1 attempt(s). Own suite: 85 pass, 0 fail, 1 not run. Whole cumulative run at that gate: 2886 pass, 0 fail, 26 not run.

| Approved requirement | Implementation | Check and outcome |
|---|---|---|
| Remove the root-only mandate in checker, D-17 and rule text | check-dependencies.cjs nearest-ancestor check per project; D-17 and NuGet rule: root typical, any MSBuild-imported location valid | no "missing at the repository root" anywhere in K0; the ancestor check still rejected a non-ancestor file that MSBuild imports (completed by PV2-03B) |
| Nested positive fixtures managing all projects | nested file, two areas, nested Directory.Build.props, root (typical) | OK in all six (real MSBuild) |
| Negatives: project without effective CPM, overridden/disabled, invalid metadata, mixed layouts | project outside the nested file, nested file off, project override false, version in project, malformed XML in the nested file | ERROR in all six; a PackageVersion with no Version was OK in M1 and K0 at this gate (pre-existing, recorded as Q-10, resolved by V3-Q10) |
| Do not relax CPM, versions, floating exceptions or other guards | C01 evaluator unchanged (byte-identical in six); DEP-003 switch interaction | C01/R04/R08 suites PASS; mutation re-adding the root rule is caught |
| Registry restore | not available | NOT_RUN |

## PV2-04: Frontend-test placement parity for M

Change `PV2-04-M-FRONTEND-TESTS`. Gate: **PASS_WITH_DOCUMENTED_NOT_RUN** after 3 attempt(s). Own suite: 46 pass, 0 fail, 2 not run. Whole cumulative run at that gate: 2934 pass, 0 fail, 28 not run.

| Approved requirement | Implementation | Check and outcome |
|---|---|---|
| Add the ban to M in its normative owner, same scope/authority/modality as peers | M project-structure step 7 (the owner named by M solution-layout.md): "Never place frontend tests under `backend/`." | text present; record V3A-M-030 MUST_NOT, DEP-024 PARTIAL, PC, as M1 and K0 |
| Test acceptable and forbidden layouts | workspace colocated, workspace e2e, backend/*.spec.ts, backend ClientApp e2e, backend .cs test | same verdicts in all six (text model) |
| No extraneous layout mandates | step 7 otherwise unchanged; CLAUDE.md untouched | PASS; mutation removing the sentence is caught |
| Enforcement by a checker | no candidate has one | NOT_RUN in all six (text duty) |

## PV2-03 (completed): A central file MSBuild imports from outside the project ancestors is valid (K0, M), found after the interim review

Change `PV2-03B-CPM-IMPORT-PROVEN`. Gate: **PASS_WITH_DOCUMENTED_NOT_RUN** after 1 attempt(s). Own suite: 129 pass, 0 fail, 1 not run. Whole cumulative run at that gate: 3256 pass, 0 fail, 31 not run.

| Approved requirement | Implementation | Check and outcome |
|---|---|---|
| Allow otherwise legitimately effective central configurations, validated per project by MSBuild | K0 checkRepository and M checkProject: the static ancestor error stands only when MSBuild did not prove CPM on and a central file imported | DirectoryPackagesPropsPath layouts (one project, two projects, renamed file, nested Directory.Build.props): OK in all six; MSBuild imported true; NuGet NU1008 for a pinned project version |
| Do not relax effective CPM enforcement | evaluator unchanged; no-SDK static fallback kept in K0 and M | plain Import (the review example), path to a missing file, CPM off, pinned project version, project outside the covered path: ERROR in all six; NuGet NU1015 for the plain Import |
| Separate gated change, cumulative regression | own declaration; suite with 4 mutations; claims reworded (FG-K0-36395ffe06, FG-K0-73dd5d1170, FG-M-7f012a0fe2) | see the gate line above |
| Registry restore | offline restore against an empty local feed only | NOT_RUN |

## Q-10 (approved semantics): A PackageVersion version is read as MSBuild reads it; a missing or empty one is an error (M1, K0, M)

Change `V3-Q10-PACKAGEVERSION-VERSION`. Gate: **PASS_WITH_DOCUMENTED_NOT_RUN** after 1 attempt(s). Own suite: 160 pass, 0 fail, 1 not run. Whole cumulative run at that gate: 3416 pass, 0 fail, 32 not run.

| Approved requirement | Implementation | Check and outcome |
|---|---|---|
| Within approved semantics only (DEP-006, DEP-003, PV2-03 invalid package metadata) | checker enforcement follows the existing NuGet text; no rule text changed | source checks: rule texts unchanged |
| Missing or empty version rejected in all six | M1 missing-version error; K0 reads the child element and reports a missing version | no Version (root, nested), empty attribute, empty or self-closing child: ERROR in all six; NuGet NU1604 |
| Valid metadata accepted in all six | M and K0 read a Version child element before the attribute, as M1 does | Version child element 1.2.3: OK in all six; floating child element: ERROR in all six |
| Separate gated change, cumulative regression | own declaration; suite with 4 mutations; the PV2-03 documented-difference row now requires ERROR in all six | see the gate line above |

