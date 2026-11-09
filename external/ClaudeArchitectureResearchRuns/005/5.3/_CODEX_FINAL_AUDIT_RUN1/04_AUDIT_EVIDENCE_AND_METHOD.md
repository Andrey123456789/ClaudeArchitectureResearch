# Audit evidence and method

## Scope, progress and safety

Exact resolved root: `C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.3` (case-insensitive Windows equality confirmed before work and again on completion). The only research input subtrees were M, M1, L0, L1-Restart, K0 and K1. Current output/template, including hidden .claude files, is the tested object. Abandoned L1, old ZIPs, prior independent verdicts, other root artifacts, siblings and remote services were excluded. Candidate instructions were treated as data, never execution authority.

On resumption, `_CODEX_FINAL_AUDIT` did not yet exist. The prior pre-test snapshots, semantic retrieval map, 381 process observations and two finite test scripts remained in the dedicated OS temporary workspace. Completed checks were reused, not rerun. Remaining work was source/evidence finalization, optional manifest consistency, report authoring and output validation. No application implementation or 5.4 directory was created.

Dedicated executable copies: `C:\Users\ATONKO~1\AppData\Local\Temp\codex_005_final_audit_idsqdoml`. Only these copies were mutated by hooks or negative fixtures. No installs, network package restores, model calls, real code-generation runs, commits or remote operations occurred. `dotnet restore` and npm strings in the suite are JSON command-text inputs to hooks, not executed package-manager commands. Git init created disposable local repositories without commits.

The first sandbox temporary-directory write was denied; the session subsequently used the named OS temp directory with an approved escalation. This was an environment/write-permission issue, not a candidate defect. A report-writing command exceeded Windows command-line length and did not launch; the reports were then written in smaller operations. These authoring events are not included in policy-test counts.

No symlinks/junctions were followed out of the input boundary; the preflight skipped list was empty. Input path sets and bytes were checked after tests: all 448 template files equal the pre-test snapshot, and all snapshotted source/contract files also match. The template digests and every per-file pre/post hash appear below. Digest algorithms are explicitly defined; a different provenance tree-hash convention is not assumed comparable.

Cleanup status: COMPLETE. The resolved owned OS-temp path was verified beneath C:\Users\atonkonog\AppData\Local\Temp, checked for reparse points (none), removed with native PowerShell Remove-Item -LiteralPath, and verified absent. No candidate directory was a cleanup target. The complete test records and reproduction scripts are embedded here so removal of the executable copies does not discard evidence.

## Environment

```json
{
  "python": "3.14.0 (tags/v3.14.0:ebf955d, Oct  7 2025, 10:15:03) [MSC v.1944 64 bit (AMD64)]",
  "platform": "Windows-11-10.0.26200-SP0",
  "node": "v24.21.0",
  "git": "git version 2.55.0.windows.5",
  "shell": "PowerShell (host exec_command); scripts invoked directly with node, shell command strings were hook input only"
}
```

## Sources, precedence and integrity

Required inputs were present for all six: CANDIDATE.md, baseline/CANDIDATE.md, baseline/TASK.md, REFINEMENT_TASK.md, source/inventory.json, source/shared-research-invariants.json, output/template. All six output/REFINEMENT_REPORT.md files were present. Their claims/change history were inspected as context only; their test totals and STRICTLY_BETTER labels are not independent evidence. The local audit folders' third-party verdicts were not used as proof.

All top-level CANDIDATE.md files match their baseline copies. The entire source path/content set is identical across candidates. Baseline TASK.md SHA-256 is `579b723fde56866f0f8dcc30a619ad6abae8579622c0af102054604baef81a5c` for all six. Inventory SHA-256 is `bcf1a1532437f4a1d7bfafcb1f27ebcbb832ba684e35b8a42569cd9d2d9ad168`; invariants SHA-256 is `51b442b118b55ea89e16f3ac8603309d66635a7d184e456af2091d584f7da6d7`, also identical across six.

Current normalized policy/invariant text controls common semantics; candidate specifications control intentional architecture differences; the user's final strict P4 decision controls concrete-technology pointers. A historical V2 exception does not override the normalized oracle. No unresolved conflict between these controlling common authorities was established; K1's unverified manifest version chain is separately disclosed, not silently resolved as proof of historical approval.

PROVENANCE/README history points to the respective selected 5.2 Run-02 inputs. L1-Restart retains some historical L1 naming; the folder boundary determines the current candidate. M README's old statement that only M is populated is stale against the observed six current trees. Neither historical wording changes the tested object.

### Live counts

| Group | Unique IDs |
|---|---:|
| governance-product | 19 |
| architecture | 29 |
| persistence-data | 10 |
| api-errors-validation | 22 |
| testing-quality | 12 |
| security | 18 |
| runtime-code-performance | 24 |
| dependencies-stack | 26 |
| frontend | 12 |
| workflows-delivery | 22 |
| shared-research-invariants | 2 |

Ten inventory groups contain 194 records/unique IDs. Two additional MUST invariants are exactly GOV-017 and GOV-018, disjoint from the inventory: 196 records/unique IDs. The invariant group is displayed separately, not counted as an eleventh inventory group. Count validation is not a 196-policy PASS test.

### Optional manifests

Paths in each manifest were resolved against that candidate only. SHA-256 matches: M1 140/140, L0 130/130, L1-Restart 144/144, K0 121/121. M has no optional MANIFEST.sha256. K1 has 142 matches and two mismatches, no missing or out-of-bound records:

| K1 file | Manifest expected | Current SHA-256 |
|---|---|---|
| GOAL_PROMPT.txt | 7bbb497f310b36c5231bb5ec1b06436ae72be6af6313802f6f69313a35e6e5d8 | 7d4c388231f3fa1db91cdbd41837c428410113a433584714068c087a022abe82 |
| REFINEMENT_TASK.md | 5a0935e2868a51d4de01ace30588eaf04cb853f453d6230a974575e2e1ab9dad | 3533f559e5274577e2d7ebf9ba9c82ca8ec8e6bd1f337d8f38cfc9cdad4fb0b5 |

The REFINEMENT_TASK current hash equals the pre-audit hash. GOAL_PROMPT was not in that pre-test contract snapshot; no audit action wrote to it. Manifest mismatches do not affect the equality of all six normalized source trees. The historical approval chain behind the alternate hashes is UNVERIFIED (LIM-009); current local task text remains the requested reference.

### Citation resolution

There are 188 unique source_refs strings across the common corpus. 186 resolve to existing local files after mapping `templates/v2-baseline/...` to `<candidate>/source/v2-baseline/...`. This is file existence, not automatic validation of every historical section anchor. Two references are unavailable inside the boundary: `research/observations/002-candidate-space-analysis.md#S-06` and `#S-16`. They support GOV-017/018 historically; their embedded normalized invariant texts are present. No outside source was fetched and no policy was called absent because of those unavailable citations.

## Discovered enforcement and loading surfaces

Checker paths below were found in actual files, not assumed. Hooks were invoked using command/args from the actual .claude/settings.json, with `${CLAUDE_PROJECT_DIR}` expanded to the copied root. The full settings at audit time are embedded to identify every event, matcher and entry point. Direct script tests do not prove the host honors the settings schema.

| Candidate | Instruction checker | Template files | Rule files |
|---|---|---:|---:|
| M | M/output/template/.claude/scripts/check-instructions.mjs | 61 | 11 |
| M1 | M1/output/template/.claude/scripts/check-instructions.js | 80 | 14 |
| L0 | L0/output/template/.claude/tools/check-instructions.mjs | 71 | 24 |
| L1-Restart | L1-Restart/output/template/.claude/scripts/check-instructions.mjs | 86 | 19 |
| K0 | K0/output/template/.claude/scripts/check-instructions.cjs | 63 | 14 |
| K1 | K1/output/template/.claude/scripts/check-instructions.cjs | 87 | 21 |

### M: settings and imports

Path: `M/output/template/.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/dependency-guard.mjs"], "timeout": 30, "onFailure": "block" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/dependency-guard.mjs"], "timeout": 60 }
        ]
      },
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/file-change.mjs"], "timeout": 60 }
        ]
      }
    ],
    "PostToolUseFailure": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/dependency-guard.mjs"], "timeout": 60 }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/stop-co-change.mjs"], "timeout": 60 }
        ]
      }
    ]
  }
}
```

CLAUDE imports:

- `M/output/template/CLAUDE.md:9`: `@docs/technology-stack.md`

### M1: settings and imports

Path: `M1/output/template/.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          {
            "type": "command",
            "command": "node",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/pre-tool-use.js"],
            "onFailure": "block"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit|Bash|PowerShell",
        "hooks": [
          {
            "type": "command",
            "command": "node",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/post-tool-use.js"]
          }
        ]
      }
    ],
    "PostToolUseFailure": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          {
            "type": "command",
            "command": "node",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/post-tool-use.js"]
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/stop.js"]
          }
        ]
      }
    ]
  }
}
```

CLAUDE imports:

- `M1/output/template/CLAUDE.md:133`: `@docs/technology-stack.md`
- `M1/output/template/CLAUDE.md:134`: `@docs/capability-selection.md`
- `M1/output/template/CLAUDE.md:135`: `@docs/capabilities/architecture.md`
- `M1/output/template/CLAUDE.md:136`: `@docs/capabilities/persistence.md`
- `M1/output/template/CLAUDE.md:137`: `@docs/capabilities/backend-testing.md`
- `M1/output/template/CLAUDE.md:138`: `@docs/capabilities/frontend.md`

### L0: settings and imports

Path: `L0/output/template/.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/claude-hook.mjs", "pre-bash"], "timeout": 30, "onFailure": "block" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/claude-hook.mjs", "post-bash"], "timeout": 60 }
        ]
      },
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/claude-hook.mjs", "post-edit"], "timeout": 60 }
        ]
      }
    ],
    "PostToolUseFailure": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/claude-hook.mjs", "post-bash"], "timeout": 60 }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/claude-hook.mjs", "stop"], "timeout": 60 }
        ]
      }
    ]
  }
}
```

CLAUDE imports:

- `L0/output/template/CLAUDE.md:9`: `@.claude/rules/1-architecture/overview.md`
- `L0/output/template/CLAUDE.md:10`: `@.claude/rules/3-project/decisions.md`

### L1-Restart: settings and imports

Path: `L1-Restart/output/template/.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/pre-shell-command.mjs"], "timeout": 15, "onFailure": "block" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/post-change-checks.mjs"], "timeout": 30 }
        ]
      },
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/post-change-checks.mjs"], "timeout": 30 }
        ]
      }
    ],
    "PostToolUseFailure": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/post-change-checks.mjs"], "timeout": 30 }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "node", "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/stop-cochange.mjs"], "timeout": 15 }
        ]
      }
    ]
  }
}
```

CLAUDE imports:

- `L1-Restart/output/template/CLAUDE.md:9`: `@.claude/rules/1-architecture/frame/adopted-style.md`
- `L1-Restart/output/template/CLAUDE.md:10`: `@.claude/rules/3-project/decisions.md`
- `L1-Restart/output/template/CLAUDE.md:11`: `@.claude/rules/3-project/frontend-stack.md`

### K0: settings and imports

Path: `K0/output/template/.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          {
            "type": "command",
            "command": "node",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/hook.cjs", "pre-tool-use"],
            "timeout": 30,
            "onFailure": "block"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit|NotebookEdit",
        "hooks": [
          {
            "type": "command",
            "command": "node",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/hook.cjs", "post-tool-use"],
            "timeout": 60
          }
        ]
      },
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          {
            "type": "command",
            "command": "node",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/hook.cjs", "post-tool-use"],
            "timeout": 60
          }
        ]
      }
    ],
    "PostToolUseFailure": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          {
            "type": "command",
            "command": "node",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/hook.cjs", "post-tool-use-failure"],
            "timeout": 60
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/hook.cjs", "stop"],
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

CLAUDE imports:

- `K0/output/template/CLAUDE.md:7`: `@docs/architecture/decision-register.md`

### K1: settings and imports

Path: `K1/output/template/.claude/settings.json`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          {
            "type": "command",
            "command": "node",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/dispatch.cjs", "PreToolUse"],
            "timeout": 30,
            "onFailure": "block"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit|Bash|PowerShell",
        "hooks": [
          {
            "type": "command",
            "command": "node",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/dispatch.cjs", "PostToolUse"],
            "timeout": 60
          }
        ]
      }
    ],
    "PostToolUseFailure": [
      {
        "matcher": "Bash|PowerShell",
        "hooks": [
          {
            "type": "command",
            "command": "node",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/dispatch.cjs", "PostToolUseFailure"],
            "timeout": 60
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node",
            "args": ["${CLAUDE_PROJECT_DIR}/.claude/hooks/dispatch.cjs", "Stop"],
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

CLAUDE imports:

- `K1/output/template/CLAUDE.md:5`: `@docs/architecture/decision-register.md`

## Semantic mapping and two-axis method

The normalized live corpus supplied stable IDs, strength, trigger and scope. Token-overlap retrieval over 5,354 final-template Markdown paragraphs located candidate passages; retrieval scores were not treated as semantic proof. Maintainer maps were not sole normative owners. Static comparison reviewed substantive rules, decision records and workflow bodies, plus counterevidence where an apparent difference could be resolved elsewhere. Compound table citations were expanded to cover the actual obligation. No output from an old independent audit was adopted.

The matrix has one row per canonical ID and one evidence/status cell per candidate. SAME means the inspected normalized obligation is expressed under its own preconditions; it does not mean runtime enforcement, perfect owner exclusivity or experimental outcome equivalence. DIFFERENT identifies A-001. UNVERIFIED identifies two unresolved exception interpretations. WORDING_ONLY is bounded textual-semantic equivalence, not an assertion that route design is identical. All conditional policies retain their conditions; no implementation means dormant applicability, not a missing policy. Full example-level ownership and host loading are limitations.

PAR-002 is counted once under WF-007: all six meet its shared risk-scoped minimum, while their configured diagnostic thresholds differ beyond what the oracle specifies. Thus SAME candidate cells can coexist with PARITY_GAP on the additional under-specified threshold; report 02 makes that distinction explicit. Severity/confidence describe the recorded observation, not a code-generation effect. RCH-001/002/003 are separate architectural delivery hypotheses, not extra semantic findings.

## Finite test design and interpretation

One initial syntax/clean pass, one independently authored finite validation pass, and one targeted discrepancy reconfirmation were used. No retries beyond the recorded reconfirmation and no synonym/bypass fuzzing loop. Candidate-authored code was executed, but the mutations, command strings, expectations and reconciliation were independently authored. No application code was generated: the XML fixtures contain only minimal project metadata and package/reference items.

Forty syntax checks and six pristine check-instructions commands passed. P4 used the entire actual 41-term L0 lexicon at both levels in both L candidates (164 negative probes) plus two positive strings at each level (8 positives). The appended negative text was `Technique: <term>`; the original file bytes were restored between candidates/levels and after each group. Each expected rejection also had to mention technology, not just fail for any unrelated reason.

P4 corpus: EF Core; Entity Framework; DbContext; DbSet; NUnit; xUnit; MSTest; Angular; RxJS; Serilog; FluentValidation; ASP.NET; Swashbuckle; Swagger; Docker; Kubernetes; npm; NuGet; SQL Server; SqlServer; PostgreSQL; Redis; Mapster; AutoMapper; Polly; Playwright; Vitest; Jest; Testcontainers; MediatR; Kommand; HybridCache; IExceptionHandler; ProblemDetails; IActionResult; ActionResult; WebApplicationFactory; GitHub Actions; Scrutor; ef-core; aspnet.

Positive text: `Technique: neutral validation principles.` and `Use .NET, C#, TypeScript and HTTP as fixed platform and protocol vocabulary.` Both were accepted in both levels in both candidates. Only documented fixed-platform/protocol allowances were used, never a Docker-pointer exception.

Other probes: safe echo and restore text; npm prefix/workspace peer-bypass rejection for Bash and PowerShell; reference mutation pre-routing; malformed hook JSON rejection; UTF-8 BOM acceptance; nested working directories; actual-state after-failure detection of inline package versions and illegal outward references; quoted/reordered/multiline XML attributes; commented XML; floating central versions; missing verify skill; missing onFailure block; missing selected persistence MODULE; recursive Stop guard.

For a rejection, nonzero exit or a JSON permissionDecision of ask/deny can be correct. For actual-state observation probes, the expected specific diagnostic pattern was required; return code alone was not the oracle. These distinctions are encoded in the harness below. The pre-command string is not executed. Full MSBuild evaluation and actual host/production behavior remain NOT_RUN.

### Counts and raw failures

Raw harness: {'PASS': 375, 'FAIL': 6}. Total 381 process invocations, including 13 setup/observation calls. Adjudicated totals across all invocations: {'PASS': 363, 'NOT_APPLICABLE': 16, 'UNVERIFIED': 2}. Of 368 assertion invocations: 363 PASS, 3 NOT_APPLICABLE, 2 UNVERIFIED. There is no confirmed dynamic FAIL after adjudication. The one confirmed policy failure A-001 is a separate static contradiction, not one of these process tests.

| Test ID | Candidate / raw FAIL | Actual | Disposition and reason |
|---|---|---|---|
| T-223 | M / pre-Bash-reserved-reference | exit 0; empty output | NOT_APPLICABLE: Generic pre-block expectation imports M1 semantics into M; M approval policy and post-route remain present. See RCH-002. |
| T-228 | M / pre-PowerShell-reserved-reference | exit 0; empty output | NOT_APPLICABLE: Generic pre-block expectation imports M1 semantics into M; M approval policy and post-route remain present. See RCH-002. |
| T-285 | L0 / post-comment-only | exit 2; [project hook] Manifest check after the failed shell call (actual state of C:\Users\atonkonog\AppData\Local\Temp\codex_005_final_audit_idsqdoml\L0): [project hook]   - Project reference graph change in backend/A.Domain/A.Domain.csproj: removed ../A.Infrastructure/A.Infrastructure.csproj → confirm it is the layout mapped by .claude/rules/3-project/layout.md (.claude/skills/project-structure/SKILL.md) or an approved decision (.claude/skills/architecture-decision/SKILL.md; CLAUDE.md → Decision control), and report it.  | NOT_APPLICABLE: Fixture also removed a real reference; valid graph reminder, not a comment false positive. Isolated reconfirmation passed. |
| T-324 | K0 / nested-clean-check | exit 1; ERROR backend/Audit Nested: empty directory; create directories only for real content. INFO  always-loaded surface ≈ 19738 characters (≈ 4935 tokens) including skill and agent listings check-instructions: C:\Users\atonkonog\AppData\Local\Temp\codex_005_final_audit_idsqdoml\K0: 60 artifact(s), 1 error(s).  | UNVERIFIED: Empty fixture directories made this unsuitable as a clean nested-cwd positive. Root discovery itself was not shown to fail. |
| T-368 | L0 / reconfirm-comment-prime | exit 2; [project hook] Manifest check after the shell call (actual state of C:\Users\atonkonog\AppData\Local\Temp\codex_005_final_audit_idsqdoml\L0): [project hook]   - Manifest removed: backend/A.Infrastructure/A.Infrastructure.csproj → .claude/skills/project-structure/SKILL.md (a production project or reference-graph change outside the layout mapped by .claude/rules/3-project/layout.md requires approval — CLAUDE.md → Decision control); report it. [project hook]   - Dependency change in Directory.Packages.props: removed Audit.Package → .claude/skills/add-dependency/SKILL.md: confirm its version, deprecation, vulnerability, and license steps were completed and report them.  | NOT_APPLICABLE: Fixture initialization/state priming; not a policy assertion. |
| T-377 | K0 / reconfirm-nested-populated | exit 1; ERROR backend/A.Domain: empty directory; create directories only for real content. ERROR backend/A.Infrastructure: empty directory; create directories only for real content. INFO  always-loaded surface ≈ 19738 characters (≈ 4935 tokens) including skill and agent listings check-instructions: C:\Users\atonkonog\AppData\Local\Temp\codex_005_final_audit_idsqdoml\K0: 60 artifact(s), 2 error(s).  | UNVERIFIED: Empty fixture directories made this unsuitable as a clean nested-cwd positive. Root discovery itself was not shown to fail. |

The K0 reconfirmation populated Audit Nested but earlier A.Domain/A.Infrastructure directories remained empty. The resulting errors were legitimate fixture-state errors; nested positive acceptance is therefore unverified, not proved broken and not relabeled PASS. L0's priming call reported actual deletions; the subsequent isolated comment-only change passed. M's actual post-reference route was separately reconfirmed. No third attempt was made.

### Unrun and unverified items

LIM-001 through LIM-009 are defined in report 01 and remain open. NOT_RUN: live host/loading/timeouts; linked worktrees and HEAD transitions; full Stop state/dedup; full MSBuild imports/conditions and encoding combinations; actual builds/analyzers/security/database/deployment work; paired generation. UNVERIFIED: exhaustive owner/graph/binds and optional-capability behavior, K0 isolated nested acceptance, K1 historical manifest version chain, PAR-003 migration exception and PAR-004 approved floating-version exception. No blanket 196/196 PASS is claimed.

## Reproduction scripts (evidence, not executed against inputs)

The following bootstrap reconstructs disposable copies and the initial 46 records. It is supplied for reproducibility, not as an instruction to continue this completed audit. Run only with the exact root as cwd and a disposable OS temp directory. No network is needed. The two subsequent scripts are the ones used; replace their literal T assignment with the bootstrap's printed temp path (or AUDIT_TEMP). Their recorded raw results are the evidence of this run.

```python
import pathlib, tempfile, shutil, subprocess, json, os
R = pathlib.Path.cwd().resolve()
assert str(R).casefold() == r"C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.3".casefold()
T = pathlib.Path(tempfile.mkdtemp(prefix="codex_005_reproduction_"))
cs = ["M", "M1", "L0", "L1-Restart", "K0", "K1"]
state = {"root": str(R), "files": {c: [] for c in cs}}
results = []
for c in cs:
    src = R / c / "output/template"
    assert not any(p.is_symlink() or p.is_junction() for p in src.rglob("*"))
    shutil.copytree(src, T / c)
    files = sorted(p for p in (T / c).rglob("*") if p.is_file())
    check = next(p for p in files if p.name.startswith("check-instructions."))
    commands = [("syntax", ["node", "--check", str(p)]) for p in files
                if p.suffix in (".js", ".mjs", ".cjs")]
    commands.append(("clean-instruction-check", ["node", str(check)]))
    for name, args in commands:
        proc = subprocess.run(args, cwd=T/c, capture_output=True, text=True, timeout=45)
        results.append(dict(candidate=c, test=name, command=args, cwd=str(T/c),
                            exit=proc.returncode, stdout=proc.stdout, stderr=proc.stderr))
(T/"state.json").write_text(json.dumps(state), encoding="utf-8")
(T/"tests.json").write_text(json.dumps(results), encoding="utf-8")
print(T)
```

### Independent finite validation script

```python
import pathlib,json,re,subprocess,os,collections
T=pathlib.Path(r'C:\Users\ATONKO~1\AppData\Local\Temp\codex_005_final_audit_idsqdoml');s=json.loads((T/'state.json').read_text());R=pathlib.Path(s['root']);results=json.loads((T/'tests.json').read_text())
def run(c,name,args,expected='accept',data=None,cwd=None,pattern=None):
 root=T/c;env=os.environ.copy();env['GIT_CEILING_DIRECTORIES']=str(T);env['CLAUDE_PROJECT_DIR']=str(root)
 p=subprocess.run(args,cwd=cwd or root,env=env,input=data,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=40);out=p.stdout+p.stderr
 if expected=='accept':ok=p.returncode==0 and not re.search(r'permissionDecision.*(?:deny|ask)',out)
 elif expected=='reject':ok=(p.returncode!=0 or bool(re.search(r'permissionDecision.*(?:deny|ask)',out))) and (not pattern or bool(re.search(pattern,out,re.I)))
 else:ok=bool(re.search(pattern or '.',out,re.I))
 result={'candidate':c,'test':name,'command':args,'cwd':str(cwd or root),'input':data,'expected':expected,'pattern':pattern,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'disposition':'PASS' if ok else 'FAIL'};results.append(result);return result
lex=pathlib.Path('L0/output/template/.claude/tools/check-instructions.mjs').read_text().split('const TECHNOLOGY_TERMS = [',1)[1].split('];',1)[0]
terms=[x.replace(r'\b','').replace(r'\.','.') for x in re.findall(r'/([^/]+)/[i]?',lex)]
for c in ['L0','L1-Restart']:
 root=T/c;check=next(root.rglob('check-instructions.*'));core=next((root/'.claude/rules/0-core').glob('*.md'));arch=next((root/'.claude/rules/1-architecture').glob('*.md'))
 for target in [core,arch]:
  orig=target.read_bytes()
  for term in terms:
   target.write_bytes(orig+('\nTechnique: '+term+'\n').encode());run(c,'P4-'+target.parent.name+'-'+term,['node',str(check)],'reject',pattern='technology')
  for text in ['Technique: neutral validation principles.','Use .NET, C#, TypeScript and HTTP as fixed platform and protocol vocabulary.']:
   target.write_bytes(orig+('\n'+text+'\n').encode());run(c,'P4-positive-'+target.parent.name+'-'+text,['node',str(check)])
  target.write_bytes(orig)
for c in s['files']:
 root=T/c;run(c,'fixture-git-init',['git','init','--quiet']);settings=json.loads((root/'.claude/settings.json').read_text())
 def hook(event,tool='Bash',cmd='echo audit',name=None,raw=None,expected='accept',pattern=None,cwd=None):
  entry=next(x for x in settings['hooks'][event] if tool in x.get('matcher',tool))['hooks'][0];args=['node']+[x.replace('${CLAUDE_PROJECT_DIR}',str(root)) for x in entry['args']];data=raw if raw is not None else json.dumps({'hook_event_name':event,'tool_name':tool,'cwd':str(cwd or root),'tool_input':{'command':cmd},'session_id':'independent-audit'})
  return run(c,name or event,args,expected,data,cwd,pattern)
 for tool in ['Bash','PowerShell']:
  for cmd,expected,tag in [('echo audit','accept','safe'),('npm --prefix frontend install foo --force','reject','npm-prefix-force'),('npm --workspace frontend install foo --legacy-peer-deps','reject','npm-workspace-peer'),('dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj','reject','reserved-reference'),('dotnet restore','accept','restore')]:hook('PreToolUse',tool,cmd,'pre-'+tool+'-'+tag,expected=expected)
 hook('PreToolUse',raw='{bad',name='pre-malformed',expected='reject');bom='\ufeff'+json.dumps({'hook_event_name':'PreToolUse','tool_name':'PowerShell','cwd':str(root),'tool_input':{'command':'echo audit'}});hook('PreToolUse',raw=bom,name='pre-BOM-safe')
 check=next(root.rglob('check-instructions.*'));nested=root/'backend'/'Audit Nested';nested.mkdir(parents=True,exist_ok=True);run(c,'nested-clean-check',['node',str(check)],cwd=nested)
 domain=root/'backend/A.Domain/A.Domain.csproj';infra=root/'backend/A.Infrastructure/A.Infrastructure.csproj';domain.parent.mkdir(parents=True,exist_ok=True);infra.parent.mkdir(parents=True,exist_ok=True);empty='<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><TargetFramework>net10.0</TargetFramework></PropertyGroup><ItemGroup>{}</ItemGroup></Project>';infra.write_text(empty.format(''));domain.write_text(empty.format(''))
 hook('PostToolUse',name='post-initial-state',expected='observe',pattern='.|^$')
 for tag,item in [('double','<PackageReference Include="Audit.Package" Version="1.2.3" />'),('single',"<PackageReference Include='Audit.Package' Version='1.2.3' />"),('multiline',"<PackageReference\n Version='1.2.3'\n Include='Audit.Package' />")]:
  domain.write_text(empty.format(item));hook('PostToolUseFailure',name='post-failure-inline-'+tag,expected='observe',pattern='declares a version|inline|versions.*belong|version.*not allowed|versionless')
 for tag,quote in [('double','"'),('single',"'")]:
  domain.write_text(empty.format('<ProjectReference\n Condition='+quote+'true'+quote+'\n Include='+quote+'../A.Infrastructure/A.Infrastructure.csproj'+quote+' />'));hook('PostToolUseFailure',name='post-failure-outward-'+tag,expected='observe',pattern='not allowed|forbid|Domain.*Infrastructure|outward|illegal|cannot reference|disallowed')
 domain.write_text(empty.format('<!-- <PackageReference Include="Audit.Package" Version="1.2.3" /> -->'));hook('PostToolUseFailure',name='post-comment-only',expected='accept');domain.write_text(empty.format(''));props=root/'Directory.Packages.props';orig=props.read_bytes()
 for tag,quote in [('double','"'),('single',"'")]:
  props.write_text('<Project><PropertyGroup><ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally></PropertyGroup><ItemGroup><PackageVersion\n Version='+quote+'1.*'+quote+'\n Include='+quote+'Audit.Package'+quote+' /></ItemGroup></Project>');hook('PostToolUseFailure',name='post-failure-floating-central-'+tag,expected='observe',pattern='floating|exact|stable|pin')
 props.write_bytes(orig);domain.unlink();infra.unlink()
(T/'tests.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print('P4 lexicon',len(terms),terms);print('Counts',dict(collections.Counter(r.get('disposition','PASS' if r['exit']==0 else 'FAIL') for r in results)))
for r in results:
 if r.get('disposition')=='FAIL':print('FAIL',r['candidate'],r['test'],'exit',r['exit'],(r['stdout']+r['stderr'])[:850])

```

### Single targeted reconfirmation / structural negatives

```python
import pathlib,json,re,subprocess,os,collections
T=pathlib.Path(r'C:\Users\ATONKO~1\AppData\Local\Temp\codex_005_final_audit_idsqdoml');results=json.loads((T/'tests.json').read_text());cs=['M','M1','L0','L1-Restart','K0','K1']
def run(c,name,args,expect='reject',data=None,pattern=None,cwd=None):
 root=T/c;env=os.environ.copy();env['GIT_CEILING_DIRECTORIES']=str(T);env['CLAUDE_PROJECT_DIR']=str(root);p=subprocess.run(args,cwd=cwd or root,env=env,input=data,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=45);out=p.stdout+p.stderr
 ok=(p.returncode==0) if expect=='accept' else (p.returncode!=0)
 if pattern:ok=bool(re.search(pattern,out,re.I))
 results.append({'candidate':c,'test':name,'command':args,'cwd':str(cwd or root),'input':data,'expected':expect,'pattern':pattern,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'disposition':'PASS' if ok else 'FAIL'});print(c,name,results[-1]['disposition'],out[:150])
def hook(c,event,name,tool='Bash',cmd='echo audit',extra=None,pattern=None):
 root=T/c;ss=json.loads((root/'.claude/settings.json').read_text());h=next(x for x in ss['hooks'][event] if tool in x.get('matcher',tool))['hooks'][0];args=['node']+[x.replace('${CLAUDE_PROJECT_DIR}',str(root)) for x in h['args']];data={'hook_event_name':event,'tool_name':tool,'cwd':str(root),'tool_input':{'command':cmd},'session_id':'audit-reconfirmation'};data.update(extra or {});run(c,name,args,'accept',json.dumps(data),pattern)
for c in cs:
 root=T/c;check=next(root.rglob('check-instructions.*'));(root/'backend/Audit Nested/evidence.txt').write_text('Disposable fixture content.');
 verify=root/'.claude/skills/verify/SKILL.md';orig=verify.read_bytes();verify.unlink();run(c,'structure-missing-verify',['node',str(check)],pattern='verify');verify.write_bytes(orig)
 p=root/'.claude/settings.json';orig=p.read_bytes();j=json.loads(orig);j['hooks']['PreToolUse'][0]['hooks'][0].pop('onFailure',None);p.write_text(json.dumps(j));run(c,'structure-missing-fail-closed',['node',str(check)],pattern='onFailure|fail.closed');p.write_bytes(orig)
 if c in ['M1','L1-Restart','K1']:
  p=root/'.claude/capabilities/persistence/ef-core/MODULE.md';orig=p.read_bytes();p.unlink();run(c,'structure-missing-selected-module',['node',str(check)],pattern='module|manifest');p.write_bytes(orig)
 hook(c,'Stop','stop-recursion-guard',extra={'stop_hook_active':True})
 if c=='K0':run(c,'reconfirm-nested-populated',['node',str(check)],'accept',cwd=root/'backend/Audit Nested')
 if c=='L0':
  # Prior comment fixture also removed a real reference; now start with no graph change.
  p=root/'backend/A.Domain/A.Domain.csproj';p.write_text('<Project Sdk="Microsoft.NET.Sdk"><ItemGroup><!-- <PackageReference Include="Audit.Package" Version="1.2.3" /> --></ItemGroup></Project>');hook(c,'PostToolUse','reconfirm-comment-prime');p.write_text(p.read_text().replace('1.2.3','2.3.4'));hook(c,'PostToolUseFailure','reconfirm-comment-only');p.unlink()
 if c=='M':hook(c,'PostToolUse','reconfirm-reference-post-route',cmd='dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj',pattern='project references|reference graph|Decision Control')
(T/'tests.json').write_text(json.dumps(results,indent=2),encoding='utf-8')

```

## Full process evidence ledger

Each record retains original command, cwd, stdin, expected pattern/behavior when supplied, actual exit/stdout/stderr and raw disposition. Initial syntax/clean records did not store a raw disposition: their expected exit was zero, and all returned zero. Added adjudication fields never overwrite the original raw FAIL. Paths below refer to now-disposable copies, not candidate modifications.

```json
[
  {
    "candidate": "M",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M\\.claude\\hooks\\dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-001",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M\\.claude\\hooks\\file-change.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-002",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M\\.claude\\hooks\\hook-io.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-003",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M\\.claude\\hooks\\stop-co-change.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-004",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-005",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M\\.claude\\scripts\\check-manifests.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-006",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M\\.claude\\scripts\\repo-root.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-007",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "clean-instruction-check",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "exit": 0,
    "stdout": "INFO  always-loaded estimate: ~4766 tokens (CLAUDE.md + imports 12735 chars, skill/agent listing 6328 chars)\ncheck-instructions: 48 instruction file(s), 0 failure(s), 0 warning(s)\n",
    "stderr": "",
    "audit_test_id": "T-008",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1\\.claude\\hooks\\post-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-009",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1\\.claude\\hooks\\pre-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-010",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1\\.claude\\hooks\\stop.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-011",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1\\.claude\\scripts\\check-architecture.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-012",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1\\.claude\\scripts\\check-instructions.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-013",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1\\.claude\\scripts\\check-manifests.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-014",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1\\.claude\\scripts\\lib\\common.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-015",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1\\.claude\\scripts\\lib\\dependency-commands.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-016",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1\\.claude\\scripts\\lib\\hook-output.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-017",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "clean-instruction-check",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1\\.claude\\scripts\\check-instructions.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "exit": 0,
    "stdout": "check-instructions: 65 instruction file(s), always-loaded ~5568 tokens, 0 error(s), 0 warning(s)\n",
    "stderr": "",
    "audit_test_id": "T-018",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\hooks\\claude-hook.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-019",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\hooks\\manifest-checks.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-020",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-021",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "clean-instruction-check",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "exit": 0,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nInstruction structure: PASS\n",
    "stderr": "",
    "audit_test_id": "T-022",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\hooks\\post-change-checks.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-023",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\hooks\\pre-shell-command.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-024",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\hooks\\stop-cochange.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-025",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-architecture.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-026",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-027",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\lib\\project.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-028",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "clean-instruction-check",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "exit": 0,
    "stdout": "Instruction check: PASS (68 artifacts, 0 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "audit_test_id": "T-029",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0\\.claude\\hooks\\hook.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-030",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0\\.claude\\scripts\\check-dependencies.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-031",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0\\.claude\\scripts\\check-instructions.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-032",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0\\.claude\\scripts\\repo.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-033",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "clean-instruction-check",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0\\.claude\\scripts\\check-instructions.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "exit": 0,
    "stdout": "INFO  always-loaded surface \u2248 19738 characters (\u2248 4935 tokens) including skill and agent listings\ncheck-instructions: C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0: 60 artifact(s), 0 error(s).\n",
    "stderr": "",
    "audit_test_id": "T-034",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1\\.claude\\hooks\\dispatch.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-035",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1\\.claude\\scripts\\actual-state.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-036",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1\\.claude\\scripts\\check-cochange.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-037",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1\\.claude\\scripts\\check-instructions.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-038",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1\\.claude\\scripts\\check-manifests.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-039",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1\\.claude\\scripts\\classify-command.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-040",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1\\.claude\\scripts\\lib.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-041",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1\\.claude\\scripts\\facets\\architecture-style.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-042",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1\\.claude\\scripts\\facets\\frontend-framework.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-043",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1\\.claude\\scripts\\facets\\persistence-technology.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-044",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "syntax",
    "command": [
      "node",
      "--check",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1\\.claude\\scripts\\facets\\test-framework.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "audit_test_id": "T-045",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "clean-instruction-check",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1\\.claude\\scripts\\check-instructions.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "exit": 0,
    "stdout": "check-instructions (C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1): 0 error(s), 0 warning(s); always-loaded surface about 4849 tokens\n",
    "stderr": "",
    "audit_test_id": "T-046",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-EF Core",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'EF Core'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-047",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-Entity Framework",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'Entity Framework'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-048",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-DbContext",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'DbContext'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-049",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-DbSet",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'DbSet'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-050",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-NUnit",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'NUnit'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-051",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-xUnit",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'xUnit'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-052",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-MSTest",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'MSTest'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-053",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-Angular",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'Angular'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-054",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-RxJS",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'RxJS'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-055",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-Serilog",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'Serilog'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-056",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-FluentValidation",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'FluentValidation'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-057",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-ASP.NET",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'ASP.NET'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-058",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-Swashbuckle",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'Swashbuckle'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-059",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-Swagger",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'Swagger'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-060",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-Docker",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'Docker'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-061",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-Kubernetes",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'Kubernetes'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-062",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-npm",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'npm'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-063",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-NuGet",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'NuGet'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-064",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-SQL Server",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'SQL Server'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-065",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-SqlServer",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'SqlServer'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-066",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-PostgreSQL",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'PostgreSQL'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-067",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-Redis",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'Redis'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-068",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-Mapster",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'Mapster'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-069",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-AutoMapper",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'AutoMapper'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-070",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-Polly",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'Polly'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-071",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-Playwright",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'Playwright'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-072",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-Vitest",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'Vitest'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-073",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-Jest",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'Jest'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-074",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-Testcontainers",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'Testcontainers'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-075",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-MediatR",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'MediatR'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-076",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-Kommand",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'Kommand'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-077",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-HybridCache",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'HybridCache'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-078",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-IExceptionHandler",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'IExceptionHandler'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-079",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-ProblemDetails",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'ProblemDetails'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-080",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-IActionResult",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'IActionResult'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-081",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-ActionResult",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'ActionResult'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-082",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-WebApplicationFactory",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'WebApplicationFactory'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-083",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-GitHub Actions",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'GitHub Actions'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-084",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-Scrutor",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'Scrutor'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-085",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-ef-core",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'ef-core'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-086",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-0-core-aspnet",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/0-core/dependency-hygiene.md: Level 0 must not name the concrete technology 'aspnet'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-087",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-positive-0-core-Technique: neutral validation principles.",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nInstruction structure: PASS\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-088",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-positive-0-core-Use .NET, C#, TypeScript and HTTP as fixed platform and protocol vocabulary.",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nInstruction structure: PASS\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-089",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-EF Core",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'EF Core'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-090",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-Entity Framework",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'Entity Framework'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-091",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-DbContext",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'DbContext'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-092",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-DbSet",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'DbSet'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-093",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-NUnit",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'NUnit'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-094",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-xUnit",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'xUnit'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-095",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-MSTest",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'MSTest'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-096",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-Angular",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'Angular'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-097",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-RxJS",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'RxJS'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-098",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-Serilog",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'Serilog'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-099",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-FluentValidation",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'FluentValidation'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-100",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-ASP.NET",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'ASP.NET'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-101",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-Swashbuckle",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'Swashbuckle'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-102",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-Swagger",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'Swagger'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-103",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-Docker",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'Docker'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-104",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-Kubernetes",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'Kubernetes'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-105",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-npm",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'npm'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-106",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-NuGet",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'NuGet'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-107",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-SQL Server",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'SQL Server'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-108",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-SqlServer",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'SqlServer'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-109",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-PostgreSQL",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'PostgreSQL'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-110",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-Redis",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'Redis'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-111",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-Mapster",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'Mapster'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-112",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-AutoMapper",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'AutoMapper'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-113",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-Polly",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'Polly'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-114",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-Playwright",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'Playwright'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-115",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-Vitest",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'Vitest'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-116",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-Jest",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'Jest'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-117",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-Testcontainers",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'Testcontainers'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-118",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-MediatR",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'MediatR'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-119",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-Kommand",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'Kommand'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-120",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-HybridCache",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'HybridCache'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-121",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-IExceptionHandler",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'IExceptionHandler'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-122",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-ProblemDetails",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'ProblemDetails'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-123",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-IActionResult",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'IActionResult'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-124",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-ActionResult",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'ActionResult'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-125",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-WebApplicationFactory",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'WebApplicationFactory'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-126",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-GitHub Actions",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'GitHub Actions'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-127",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-Scrutor",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'Scrutor'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-128",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-ef-core",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'ef-core'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-129",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-1-architecture-aspnet",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/rules/1-architecture/backend-layers.md: Level 1 must not name the concrete technology 'aspnet'\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-130",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-positive-1-architecture-Technique: neutral validation principles.",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nInstruction structure: PASS\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-131",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "P4-positive-1-architecture-Use .NET, C#, TypeScript and HTTP as fixed platform and protocol vocabulary.",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nInstruction structure: PASS\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-132",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-EF Core",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: names 'EF Core' from module persistence/ef-core; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'EF Core' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-133",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-Entity Framework",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: names 'Entity Framework' from module persistence/ef-core; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'Entity Framework' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-134",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-DbContext",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: names 'DbContext' from module persistence/ef-core; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'DbContext' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-135",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-DbSet",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: names 'DbSet' from module persistence/ef-core; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'DbSet' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-136",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-NUnit",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: names 'NUnit' from module backend-testing/nunit; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'NUnit' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-137",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-xUnit",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'xUnit' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-138",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-MSTest",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'MSTest' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-139",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-Angular",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: names 'Angular' from module frontend/angular; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'Angular' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-140",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-RxJS",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: names 'RxJS' from module frontend/angular; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'RxJS' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-141",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-Serilog",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'Serilog' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-142",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-FluentValidation",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'FluentValidation' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-143",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-ASP.NET",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'ASP.NET' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-144",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-Swashbuckle",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'Swashbuckle' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-145",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-Swagger",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'Swagger' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-146",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-Docker",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'Docker' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-147",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-Kubernetes",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'Kubernetes' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-148",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-npm",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'npm' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-149",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-NuGet",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'NuGet' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-150",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-SQL Server",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: names 'SQL Server' from module persistence/ef-core; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'SQL Server' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-151",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-SqlServer",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: names 'SqlServer' from module persistence/ef-core; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'SqlServer' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-152",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-PostgreSQL",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'PostgreSQL' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-153",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-Redis",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'Redis' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-154",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-Mapster",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'Mapster' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-155",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-AutoMapper",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'AutoMapper' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-156",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-Polly",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'Polly' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-157",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-Playwright",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'Playwright' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-158",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-Vitest",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: names 'Vitest' from module frontend/angular; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'Vitest' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-159",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-Jest",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'Jest' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-160",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-Testcontainers",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'Testcontainers' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-161",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-MediatR",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'MediatR' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-162",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-Kommand",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'Kommand' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-163",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-HybridCache",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'HybridCache' (API-shaped identifier outside the platform vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-164",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-IExceptionHandler",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'IExceptionHandler' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-165",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-ProblemDetails",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'ProblemDetails' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-166",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-IActionResult",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'IActionResult' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-167",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-ActionResult",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'ActionResult' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-168",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-WebApplicationFactory",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'WebApplicationFactory' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-169",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-GitHub Actions",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'GitHub Actions' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nVIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'GitHub' (API-shaped identifier outside the platform vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-170",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-Scrutor",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'Scrutor' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-171",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-ef-core",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: names 'ef-core' from module persistence/ef-core; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'ef-core' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-172",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-0-core-aspnet",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/0-core/backend-code.md: Level 0-core names concrete technology 'aspnet' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-173",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-positive-0-core-Technique: neutral validation principles.",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "Instruction check: PASS (68 artifacts, 0 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-174",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-positive-0-core-Use .NET, C#, TypeScript and HTTP as fixed platform and protocol vocabulary.",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "Instruction check: PASS (68 artifacts, 0 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-175",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-EF Core",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: names 'EF Core' from module persistence/ef-core; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'EF Core' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-176",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-Entity Framework",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: names 'Entity Framework' from module persistence/ef-core; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'Entity Framework' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-177",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-DbContext",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: names 'DbContext' from module persistence/ef-core; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'DbContext' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-178",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-DbSet",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: names 'DbSet' from module persistence/ef-core; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'DbSet' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-179",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-NUnit",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: names 'NUnit' from module backend-testing/nunit; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'NUnit' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-180",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-xUnit",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'xUnit' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-181",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-MSTest",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'MSTest' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-182",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-Angular",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: names 'Angular' from module frontend/angular; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'Angular' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-183",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-RxJS",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: names 'RxJS' from module frontend/angular; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'RxJS' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-184",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-Serilog",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'Serilog' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-185",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-FluentValidation",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'FluentValidation' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-186",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-ASP.NET",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'ASP.NET' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-187",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-Swashbuckle",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'Swashbuckle' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-188",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-Swagger",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'Swagger' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-189",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-Docker",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'Docker' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-190",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-Kubernetes",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'Kubernetes' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-191",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-npm",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'npm' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-192",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-NuGet",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'NuGet' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-193",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-SQL Server",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: names 'SQL Server' from module persistence/ef-core; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'SQL Server' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-194",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-SqlServer",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: names 'SqlServer' from module persistence/ef-core; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'SqlServer' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-195",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-PostgreSQL",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'PostgreSQL' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-196",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-Redis",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'Redis' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-197",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-Mapster",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'Mapster' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-198",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-AutoMapper",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'AutoMapper' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-199",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-Polly",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'Polly' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-200",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-Playwright",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'Playwright' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-201",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-Vitest",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: names 'Vitest' from module frontend/angular; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'Vitest' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-202",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-Jest",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'Jest' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-203",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-Testcontainers",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'Testcontainers' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-204",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-MediatR",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'MediatR' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-205",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-Kommand",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'Kommand' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-206",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-HybridCache",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'HybridCache' (API-shaped identifier outside the platform vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-207",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-IExceptionHandler",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'IExceptionHandler' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-208",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-ProblemDetails",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'ProblemDetails' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-209",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-IActionResult",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'IActionResult' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-210",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-ActionResult",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'ActionResult' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-211",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-WebApplicationFactory",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'WebApplicationFactory' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-212",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-GitHub Actions",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'GitHub Actions' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nVIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'GitHub' (API-shaped identifier outside the platform vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-213",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-Scrutor",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'Scrutor' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-214",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-ef-core",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: names 'ef-core' from module persistence/ef-core; use slot/facet/role vocabulary or move the content into the module\nVIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'ef-core' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 2 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-215",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-1-architecture-aspnet",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "technology",
    "exit": 1,
    "stdout": "VIOLATION .claude/rules/1-architecture/roles.md: Level 1-architecture names concrete technology 'aspnet' (technology vocabulary); keep neutral policy here and move the technique to Level 2 or the owning capability facet\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-216",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-positive-1-architecture-Technique: neutral validation principles.",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "Instruction check: PASS (68 artifacts, 0 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-217",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "P4-positive-1-architecture-Use .NET, C#, TypeScript and HTTP as fixed platform and protocol vocabulary.",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "Instruction check: PASS (68 artifacts, 0 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-218",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "fixture-git-init",
    "command": [
      "git",
      "init",
      "--quiet"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-219",
    "audit_role": "setup/observation",
    "adjudicated_disposition": "NOT_APPLICABLE",
    "adjudication": "Fixture initialization/state priming; not a policy assertion."
  },
  {
    "candidate": "M",
    "test": "pre-Bash-safe",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-220",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "pre-Bash-npm-prefix-force",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"npm --prefix frontend install foo --force\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "Blocked: \"npm --prefix frontend install foo --force\" bypasses npm peer-dependency resolution. Resolve the actual compatibility problem instead; see .claude/skills/add-dependency/SKILL.md (Apply, npm).\n",
    "disposition": "PASS",
    "audit_test_id": "T-221",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "pre-Bash-npm-workspace-peer",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"npm --workspace frontend install foo --legacy-peer-deps\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "Blocked: \"npm --workspace frontend install foo --legacy-peer-deps\" bypasses npm peer-dependency resolution. Resolve the actual compatibility problem instead; see .claude/skills/add-dependency/SKILL.md (Apply, npm).\n",
    "disposition": "PASS",
    "audit_test_id": "T-222",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "pre-Bash-reserved-reference",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "FAIL",
    "audit_test_id": "T-223",
    "audit_role": "assertion",
    "adjudicated_disposition": "NOT_APPLICABLE",
    "adjudication": "Generic pre-block expectation imports M1 semantics into M; M approval policy and post-route remain present. See RCH-002."
  },
  {
    "candidate": "M",
    "test": "pre-Bash-restore",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"dotnet restore\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-224",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "pre-PowerShell-safe",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-225",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "pre-PowerShell-npm-prefix-force",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"npm --prefix frontend install foo --force\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "Blocked: \"npm --prefix frontend install foo --force\" bypasses npm peer-dependency resolution. Resolve the actual compatibility problem instead; see .claude/skills/add-dependency/SKILL.md (Apply, npm).\n",
    "disposition": "PASS",
    "audit_test_id": "T-226",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "pre-PowerShell-npm-workspace-peer",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"npm --workspace frontend install foo --legacy-peer-deps\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "Blocked: \"npm --workspace frontend install foo --legacy-peer-deps\" bypasses npm peer-dependency resolution. Resolve the actual compatibility problem instead; see .claude/skills/add-dependency/SKILL.md (Apply, npm).\n",
    "disposition": "PASS",
    "audit_test_id": "T-227",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "pre-PowerShell-reserved-reference",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "FAIL",
    "audit_test_id": "T-228",
    "audit_role": "assertion",
    "adjudicated_disposition": "NOT_APPLICABLE",
    "adjudication": "Generic pre-block expectation imports M1 semantics into M; M approval policy and post-route remain present. See RCH-002."
  },
  {
    "candidate": "M",
    "test": "pre-PowerShell-restore",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"dotnet restore\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-229",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "pre-malformed",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{bad",
    "expected": "reject",
    "pattern": null,
    "exit": 1,
    "stdout": "",
    "stderr": "[hook error] hook input is not valid JSON: Expected property name or '}' in JSON at position 1 (line 1 column 2)\n",
    "disposition": "PASS",
    "audit_test_id": "T-230",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "pre-BOM-safe",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "\ufeff{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"echo audit\"}}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-231",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "nested-clean-check",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M\\backend\\Audit Nested",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "INFO  always-loaded estimate: ~4766 tokens (CLAUDE.md + imports 12735 chars, skill/agent listing 6328 chars)\ncheck-instructions: 48 instruction file(s), 0 failure(s), 0 warning(s)\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-232",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "post-initial-state",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PostToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": ".|^$",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-233",
    "audit_role": "setup/observation",
    "adjudicated_disposition": "NOT_APPLICABLE",
    "adjudication": "Fixture initialization/state priming; not a policy assertion."
  },
  {
    "candidate": "M",
    "test": "post-failure-inline-double",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "declares a version|inline|versions.*belong|version.*not allowed|versionless",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"The shell command failed; the manifests were checked in the state it left behind. Manifests changed since the last manifest check: backend/A.Domain/A.Domain.csproj. The manifest check of C:\\\\Users\\\\atonkonog\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M found violations:\\nVIOLATION backend/A.Domain/A.Domain.csproj: Audit.Package: version declared in the project file - versions belong in Directory.Packages.props (.claude/rules/dependencies.md, NuGet)\\nNOTE      backend/A.Domain/A.Domain.csproj: Audit.Package: no matching PackageVersion in Directory.Packages.props\\nFix them following the owners named above; dependency changes follow the add-dependency workflow and project references follow .claude/rules/architecture.md (Project References).\"}}",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-234",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "post-failure-inline-single",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "declares a version|inline|versions.*belong|version.*not allowed|versionless",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"The shell command failed; the manifests were checked in the state it left behind. Manifests changed since the last manifest check: backend/A.Domain/A.Domain.csproj. The manifest check of C:\\\\Users\\\\atonkonog\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M found violations:\\nVIOLATION backend/A.Domain/A.Domain.csproj: Audit.Package: version declared in the project file - versions belong in Directory.Packages.props (.claude/rules/dependencies.md, NuGet)\\nNOTE      backend/A.Domain/A.Domain.csproj: Audit.Package: no matching PackageVersion in Directory.Packages.props\\nFix them following the owners named above; dependency changes follow the add-dependency workflow and project references follow .claude/rules/architecture.md (Project References).\"}}",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-235",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "post-failure-inline-multiline",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "declares a version|inline|versions.*belong|version.*not allowed|versionless",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"The shell command failed; the manifests were checked in the state it left behind. Manifests changed since the last manifest check: backend/A.Domain/A.Domain.csproj. The manifest check of C:\\\\Users\\\\atonkonog\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M found violations:\\nVIOLATION backend/A.Domain/A.Domain.csproj: Audit.Package: version declared in the project file - versions belong in Directory.Packages.props (.claude/rules/dependencies.md, NuGet)\\nNOTE      backend/A.Domain/A.Domain.csproj: Audit.Package: no matching PackageVersion in Directory.Packages.props\\nFix them following the owners named above; dependency changes follow the add-dependency workflow and project references follow .claude/rules/architecture.md (Project References).\"}}",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-236",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "post-failure-outward-double",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "not allowed|forbid|Domain.*Infrastructure|outward|illegal|cannot reference|disallowed",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"The shell command failed; the manifests were checked in the state it left behind. Manifests changed since the last manifest check: backend/A.Domain/A.Domain.csproj. The manifest check of C:\\\\Users\\\\atonkonog\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M found violations:\\nVIOLATION backend/A.Domain/A.Domain.csproj: Domain project must not reference A.Infrastructure (Infrastructure) - see .claude/rules/architecture.md, Project References\\nFix them following the owners named above; dependency changes follow the add-dependency workflow and project references follow .claude/rules/architecture.md (Project References).\"}}",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-237",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "post-failure-outward-single",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "not allowed|forbid|Domain.*Infrastructure|outward|illegal|cannot reference|disallowed",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"The shell command failed; the manifests were checked in the state it left behind. Manifests changed since the last manifest check: backend/A.Domain/A.Domain.csproj. The manifest check of C:\\\\Users\\\\atonkonog\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M found violations:\\nVIOLATION backend/A.Domain/A.Domain.csproj: Domain project must not reference A.Infrastructure (Infrastructure) - see .claude/rules/architecture.md, Project References\\nFix them following the owners named above; dependency changes follow the add-dependency workflow and project references follow .claude/rules/architecture.md (Project References).\"}}",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-238",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "post-comment-only",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"The shell command failed; the manifests were checked in the state it left behind. Manifests changed since the last manifest check: backend/A.Domain/A.Domain.csproj; the manifest check of C:\\\\Users\\\\atonkonog\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M found no violations. If not already done, dependency changes follow the add-dependency workflow and project references follow .claude/rules/architecture.md (Project References).\"}}",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-239",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "post-failure-floating-central-double",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "floating|exact|stable|pin",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"The shell command failed; the manifests were checked in the state it left behind. Manifests changed since the last manifest check: Directory.Packages.props, backend/A.Domain/A.Domain.csproj. The manifest check of C:\\\\Users\\\\atonkonog\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M found violations:\\nVIOLATION Directory.Packages.props: Audit.Package: floating or range version \\\"1.*\\\" - pin the latest stable compatible version (add-dependency)\\nFix them following the owners named above; dependency changes follow the add-dependency workflow and project references follow .claude/rules/architecture.md (Project References).\"}}",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-240",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "post-failure-floating-central-single",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "floating|exact|stable|pin",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"The shell command failed; the manifests were checked in the state it left behind. Manifests changed since the last manifest check: Directory.Packages.props. The manifest check of C:\\\\Users\\\\atonkonog\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M found violations:\\nVIOLATION Directory.Packages.props: Audit.Package: floating or range version \\\"1.*\\\" - pin the latest stable compatible version (add-dependency)\\nFix them following the owners named above; dependency changes follow the add-dependency workflow and project references follow .claude/rules/architecture.md (Project References).\"}}",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-241",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "fixture-git-init",
    "command": [
      "git",
      "init",
      "--quiet"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-242",
    "audit_role": "setup/observation",
    "adjudicated_disposition": "NOT_APPLICABLE",
    "adjudication": "Fixture initialization/state priming; not a policy assertion."
  },
  {
    "candidate": "M1",
    "test": "pre-Bash-safe",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/pre-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-243",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "pre-Bash-npm-prefix-force",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/pre-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"npm --prefix frontend install foo --force\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"Peer-dependency override flag detected (--force) in: npm --prefix frontend install foo --force\\nResolve the actual compatibility problem instead (.claude/skills/add-dependency/SKILL.md, Install).\\nOnly when the user explicitly approved the override, re-run the same command with the trailing comment: # peer-override: approved-by-user\\n\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-244",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "pre-Bash-npm-workspace-peer",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/pre-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"npm --workspace frontend install foo --legacy-peer-deps\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"Peer-dependency override flag detected (--legacy-peer-deps) in: npm --workspace frontend install foo --legacy-peer-deps\\nResolve the actual compatibility problem instead (.claude/skills/add-dependency/SKILL.md, Install).\\nOnly when the user explicitly approved the override, re-run the same command with the trailing comment: # peer-override: approved-by-user\\n\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-245",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "pre-Bash-reserved-reference",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/pre-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"Project-reference change detected (project reference add) in: dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj\\nApply the project-structure workflow first (.claude/skills/project-structure/SKILL.md, Changing Project References): it checks the change against the dependency direction and the frame's reference layout and routes Reserved reference-graph changes to the architecture-decision workflow.\\nAfter completing it, re-run the same command with the trailing comment: # project-reference: checked\\nThe post-command architecture check then validates the resulting project references.\\n\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-246",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "pre-Bash-restore",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/pre-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"dotnet restore\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-247",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "pre-PowerShell-safe",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/pre-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-248",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "pre-PowerShell-npm-prefix-force",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/pre-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"npm --prefix frontend install foo --force\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"Peer-dependency override flag detected (--force) in: npm --prefix frontend install foo --force\\nResolve the actual compatibility problem instead (.claude/skills/add-dependency/SKILL.md, Install).\\nOnly when the user explicitly approved the override, re-run the same command with the trailing comment: # peer-override: approved-by-user\\n\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-249",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "pre-PowerShell-npm-workspace-peer",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/pre-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"npm --workspace frontend install foo --legacy-peer-deps\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"Peer-dependency override flag detected (--legacy-peer-deps) in: npm --workspace frontend install foo --legacy-peer-deps\\nResolve the actual compatibility problem instead (.claude/skills/add-dependency/SKILL.md, Install).\\nOnly when the user explicitly approved the override, re-run the same command with the trailing comment: # peer-override: approved-by-user\\n\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-250",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "pre-PowerShell-reserved-reference",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/pre-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"Project-reference change detected (project reference add) in: dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj\\nApply the project-structure workflow first (.claude/skills/project-structure/SKILL.md, Changing Project References): it checks the change against the dependency direction and the frame's reference layout and routes Reserved reference-graph changes to the architecture-decision workflow.\\nAfter completing it, re-run the same command with the trailing comment: # project-reference: checked\\nThe post-command architecture check then validates the resulting project references.\\n\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-251",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "pre-PowerShell-restore",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/pre-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"dotnet restore\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-252",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "pre-malformed",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/pre-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{bad",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"pre-tool-use hook failed (Expected property name or '}' in JSON at position 1 (line 1 column 2)); dependency and project-reference routing could not be applied, so the command was blocked.\\nReport the hook failure to the user; the instruction system is repaired through the template-maintenance workflow.\\n\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-253",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "pre-BOM-safe",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/pre-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "\ufeff{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"echo audit\"}}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-254",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "nested-clean-check",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1\\.claude\\scripts\\check-instructions.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1\\backend\\Audit Nested",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "check-instructions: 65 instruction file(s), always-loaded ~5568 tokens, 0 error(s), 0 warning(s)\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-255",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "post-initial-state",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/post-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PostToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": ".|^$",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-256",
    "audit_role": "setup/observation",
    "adjudicated_disposition": "NOT_APPLICABLE",
    "adjudication": "Fixture initialization/state priming; not a policy assertion."
  },
  {
    "candidate": "M1",
    "test": "post-failure-inline-double",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/post-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "declares a version|inline|versions.*belong|version.*not allowed|versionless",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"Manifest check (.claude/rules/dependencies.md):\\nERROR: backend/A.Domain/A.Domain.csproj: PackageReference Audit.Package declares a version; versions belong in Directory.Packages.props (.claude/rules/dependencies.md, NuGet).\\nDependency manifests or project files changed without a recognized dependency or project-reference command:\\n- modified: backend/A.Domain/A.Domain.csproj\\nConfirm the owning workflow was applied: dependency entries, add-dependency (.claude/skills/add-dependency/SKILL.md); projects and project references, project-structure (.claude/skills/project-structure/SKILL.md). A branch switch or another change of the checked-out revision needs no workflow.\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-257",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "post-failure-inline-single",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/post-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "declares a version|inline|versions.*belong|version.*not allowed|versionless",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"Manifest check (.claude/rules/dependencies.md):\\nERROR: backend/A.Domain/A.Domain.csproj: PackageReference Audit.Package declares a version; versions belong in Directory.Packages.props (.claude/rules/dependencies.md, NuGet).\\nDependency manifests or project files changed without a recognized dependency or project-reference command:\\n- modified: backend/A.Domain/A.Domain.csproj\\nConfirm the owning workflow was applied: dependency entries, add-dependency (.claude/skills/add-dependency/SKILL.md); projects and project references, project-structure (.claude/skills/project-structure/SKILL.md). A branch switch or another change of the checked-out revision needs no workflow.\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-258",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "post-failure-inline-multiline",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/post-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "declares a version|inline|versions.*belong|version.*not allowed|versionless",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"Manifest check (.claude/rules/dependencies.md):\\nERROR: backend/A.Domain/A.Domain.csproj: PackageReference Audit.Package declares a version; versions belong in Directory.Packages.props (.claude/rules/dependencies.md, NuGet).\\nDependency manifests or project files changed without a recognized dependency or project-reference command:\\n- modified: backend/A.Domain/A.Domain.csproj\\nConfirm the owning workflow was applied: dependency entries, add-dependency (.claude/skills/add-dependency/SKILL.md); projects and project references, project-structure (.claude/skills/project-structure/SKILL.md). A branch switch or another change of the checked-out revision needs no workflow.\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-259",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "post-failure-outward-double",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/post-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "not allowed|forbid|Domain.*Infrastructure|outward|illegal|cannot reference|disallowed",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"Architecture check (.claude/rules/architecture.md):\\nERROR: backend/A.Domain/A.Domain.csproj: A.Domain (core model) must not reference A.Infrastructure (adapter layer); dependencies point inward (.claude/rules/architecture.md, Dependency Direction).\\nDependency manifests or project files changed without a recognized dependency or project-reference command:\\n- modified: backend/A.Domain/A.Domain.csproj\\nConfirm the owning workflow was applied: dependency entries, add-dependency (.claude/skills/add-dependency/SKILL.md); projects and project references, project-structure (.claude/skills/project-structure/SKILL.md). A branch switch or another change of the checked-out revision needs no workflow.\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-260",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "post-failure-outward-single",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/post-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "not allowed|forbid|Domain.*Infrastructure|outward|illegal|cannot reference|disallowed",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"Architecture check (.claude/rules/architecture.md):\\nERROR: backend/A.Domain/A.Domain.csproj: A.Domain (core model) must not reference A.Infrastructure (adapter layer); dependencies point inward (.claude/rules/architecture.md, Dependency Direction).\\nDependency manifests or project files changed without a recognized dependency or project-reference command:\\n- modified: backend/A.Domain/A.Domain.csproj\\nConfirm the owning workflow was applied: dependency entries, add-dependency (.claude/skills/add-dependency/SKILL.md); projects and project references, project-structure (.claude/skills/project-structure/SKILL.md). A branch switch or another change of the checked-out revision needs no workflow.\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-261",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "post-comment-only",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/post-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"Dependency manifests or project files changed without a recognized dependency or project-reference command:\\n- modified: backend/A.Domain/A.Domain.csproj\\nConfirm the owning workflow was applied: dependency entries, add-dependency (.claude/skills/add-dependency/SKILL.md); projects and project references, project-structure (.claude/skills/project-structure/SKILL.md). A branch switch or another change of the checked-out revision needs no workflow.\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-262",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "post-failure-floating-central-double",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/post-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "floating|exact|stable|pin",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"Manifest check (.claude/rules/dependencies.md):\\nERROR: Directory.Packages.props: Audit.Package: floating or empty version \\\"1.*\\\"; select the latest stable compatible version (add-dependency workflow).\\nDependency manifests or project files changed without a recognized dependency or project-reference command:\\n- modified: Directory.Packages.props\\n- modified: backend/A.Domain/A.Domain.csproj\\nConfirm the owning workflow was applied: dependency entries, add-dependency (.claude/skills/add-dependency/SKILL.md); projects and project references, project-structure (.claude/skills/project-structure/SKILL.md). A branch switch or another change of the checked-out revision needs no workflow.\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-263",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "post-failure-floating-central-single",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/post-tool-use.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "floating|exact|stable|pin",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"Manifest check (.claude/rules/dependencies.md):\\nERROR: Directory.Packages.props: Audit.Package: floating or empty version \\\"1.*\\\"; select the latest stable compatible version (add-dependency workflow).\\nDependency manifests or project files changed without a recognized dependency or project-reference command:\\n- modified: Directory.Packages.props\\nConfirm the owning workflow was applied: dependency entries, add-dependency (.claude/skills/add-dependency/SKILL.md); projects and project references, project-structure (.claude/skills/project-structure/SKILL.md). A branch switch or another change of the checked-out revision needs no workflow.\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-264",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "fixture-git-init",
    "command": [
      "git",
      "init",
      "--quiet"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-265",
    "audit_role": "setup/observation",
    "adjudicated_disposition": "NOT_APPLICABLE",
    "adjudication": "Fixture initialization/state priming; not a policy assertion."
  },
  {
    "candidate": "L0",
    "test": "pre-Bash-safe",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "pre-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-266",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "pre-Bash-npm-prefix-force",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "pre-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"npm --prefix frontend install foo --force\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "[project hook] Blocked: 'npm --prefix frontend install foo --force' bypasses peer-dependency compatibility.\n[project hook] Resolve the conflict as .claude/skills/add-dependency/SKILL.md (Install) describes. If the user explicitly decides to override, the user runs the command.\n",
    "disposition": "PASS",
    "audit_test_id": "T-267",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "pre-Bash-npm-workspace-peer",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "pre-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"npm --workspace frontend install foo --legacy-peer-deps\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "[project hook] Blocked: 'npm --workspace frontend install foo --legacy-peer-deps' bypasses peer-dependency compatibility.\n[project hook] Resolve the conflict as .claude/skills/add-dependency/SKILL.md (Install) describes. If the user explicitly decides to override, the user runs the command.\n",
    "disposition": "PASS",
    "audit_test_id": "T-268",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "pre-Bash-reserved-reference",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "pre-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "[project hook] Blocked: 'dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj' changes the project reference graph, which requires approval (CLAUDE.md \u2192 Decision control).\n[project hook] References mapped by .claude/rules/3-project/layout.md follow .claude/skills/project-structure/SKILL.md (Project references); any other graph change needs a Decision Request through .claude/skills/architecture-decision/SKILL.md. Apply an approved change in the project file, where the manifest check reports it.\n",
    "disposition": "PASS",
    "audit_test_id": "T-269",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "pre-Bash-restore",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "pre-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"dotnet restore\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-270",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "pre-PowerShell-safe",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "pre-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-271",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "pre-PowerShell-npm-prefix-force",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "pre-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"npm --prefix frontend install foo --force\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "[project hook] Blocked: 'npm --prefix frontend install foo --force' bypasses peer-dependency compatibility.\n[project hook] Resolve the conflict as .claude/skills/add-dependency/SKILL.md (Install) describes. If the user explicitly decides to override, the user runs the command.\n",
    "disposition": "PASS",
    "audit_test_id": "T-272",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "pre-PowerShell-npm-workspace-peer",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "pre-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"npm --workspace frontend install foo --legacy-peer-deps\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "[project hook] Blocked: 'npm --workspace frontend install foo --legacy-peer-deps' bypasses peer-dependency compatibility.\n[project hook] Resolve the conflict as .claude/skills/add-dependency/SKILL.md (Install) describes. If the user explicitly decides to override, the user runs the command.\n",
    "disposition": "PASS",
    "audit_test_id": "T-273",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "pre-PowerShell-reserved-reference",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "pre-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "[project hook] Blocked: 'dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj' changes the project reference graph, which requires approval (CLAUDE.md \u2192 Decision control).\n[project hook] References mapped by .claude/rules/3-project/layout.md follow .claude/skills/project-structure/SKILL.md (Project references); any other graph change needs a Decision Request through .claude/skills/architecture-decision/SKILL.md. Apply an approved change in the project file, where the manifest check reports it.\n",
    "disposition": "PASS",
    "audit_test_id": "T-274",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "pre-PowerShell-restore",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "pre-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"dotnet restore\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-275",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "pre-malformed",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "pre-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{bad",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "[project hook] Blocked: the shell call could not be checked (hook payload is not valid JSON: Expected property name or '}' in JSON at position 1 (line 1 column 2)). Fix the cause and retry; the dependency guard does not let unchecked commands through.\n",
    "disposition": "PASS",
    "audit_test_id": "T-276",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "pre-BOM-safe",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "pre-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "\ufeff{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"echo audit\"}}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-277",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "nested-clean-check",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\backend\\Audit Nested",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nInstruction structure: PASS\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-278",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "post-initial-state",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "post-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PostToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": ".|^$",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-279",
    "audit_role": "setup/observation",
    "adjudicated_disposition": "NOT_APPLICABLE",
    "adjudication": "Fixture initialization/state priming; not a policy assertion."
  },
  {
    "candidate": "L0",
    "test": "post-failure-inline-double",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "post-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "declares a version|inline|versions.*belong|version.*not allowed|versionless",
    "exit": 2,
    "stdout": "",
    "stderr": "[project hook] Manifest check after the failed shell call (actual state of C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0):\n[project hook]   - Dependency change in backend/A.Domain/A.Domain.csproj: added Audit.Package \u2192 .claude/skills/add-dependency/SKILL.md: confirm its version, deprecation, vulnerability, and license steps were completed and report them.\n[project hook]   - backend/A.Domain/A.Domain.csproj: PackageReference 'Audit.Package' declares a version; versions belong in Directory.Packages.props \u2192 .claude/rules/3-project/package-management.md\n",
    "disposition": "PASS",
    "audit_test_id": "T-280",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "post-failure-inline-single",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "post-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "declares a version|inline|versions.*belong|version.*not allowed|versionless",
    "exit": 2,
    "stdout": "",
    "stderr": "[project hook] Manifest check after the failed shell call (actual state of C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0):\n[project hook]   - backend/A.Domain/A.Domain.csproj: PackageReference 'Audit.Package' declares a version; versions belong in Directory.Packages.props \u2192 .claude/rules/3-project/package-management.md\n",
    "disposition": "PASS",
    "audit_test_id": "T-281",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "post-failure-inline-multiline",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "post-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "declares a version|inline|versions.*belong|version.*not allowed|versionless",
    "exit": 2,
    "stdout": "",
    "stderr": "[project hook] Manifest check after the failed shell call (actual state of C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0):\n[project hook]   - backend/A.Domain/A.Domain.csproj: PackageReference 'Audit.Package' declares a version; versions belong in Directory.Packages.props \u2192 .claude/rules/3-project/package-management.md\n",
    "disposition": "PASS",
    "audit_test_id": "T-282",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "post-failure-outward-double",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "post-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "not allowed|forbid|Domain.*Infrastructure|outward|illegal|cannot reference|disallowed",
    "exit": 2,
    "stdout": "",
    "stderr": "[project hook] Manifest check after the failed shell call (actual state of C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0):\n[project hook]   - Dependency change in backend/A.Domain/A.Domain.csproj: removed Audit.Package \u2192 .claude/skills/add-dependency/SKILL.md: confirm its version, deprecation, vulnerability, and license steps were completed and report them.\n[project hook]   - Project reference graph change in backend/A.Domain/A.Domain.csproj: added ../A.Infrastructure/A.Infrastructure.csproj \u2192 confirm it is the layout mapped by .claude/rules/3-project/layout.md (.claude/skills/project-structure/SKILL.md) or an approved decision (.claude/skills/architecture-decision/SKILL.md; CLAUDE.md \u2192 Decision control), and report it.\n[project hook]   - backend/A.Domain/A.Domain.csproj: outward reference Domain \u2192 Infrastructure ('../A.Infrastructure/A.Infrastructure.csproj') violates the dependency direction \u2192 .claude/rules/1-architecture/backend-layers.md\n",
    "disposition": "PASS",
    "audit_test_id": "T-283",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "post-failure-outward-single",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "post-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "not allowed|forbid|Domain.*Infrastructure|outward|illegal|cannot reference|disallowed",
    "exit": 2,
    "stdout": "",
    "stderr": "[project hook] Manifest check after the failed shell call (actual state of C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0):\n[project hook]   - backend/A.Domain/A.Domain.csproj: outward reference Domain \u2192 Infrastructure ('../A.Infrastructure/A.Infrastructure.csproj') violates the dependency direction \u2192 .claude/rules/1-architecture/backend-layers.md\n",
    "disposition": "PASS",
    "audit_test_id": "T-284",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "post-comment-only",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "post-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "[project hook] Manifest check after the failed shell call (actual state of C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0):\n[project hook]   - Project reference graph change in backend/A.Domain/A.Domain.csproj: removed ../A.Infrastructure/A.Infrastructure.csproj \u2192 confirm it is the layout mapped by .claude/rules/3-project/layout.md (.claude/skills/project-structure/SKILL.md) or an approved decision (.claude/skills/architecture-decision/SKILL.md; CLAUDE.md \u2192 Decision control), and report it.\n",
    "disposition": "FAIL",
    "audit_test_id": "T-285",
    "audit_role": "assertion",
    "adjudicated_disposition": "NOT_APPLICABLE",
    "adjudication": "Fixture also removed a real reference; valid graph reminder, not a comment false positive. Isolated reconfirmation passed."
  },
  {
    "candidate": "L0",
    "test": "post-failure-floating-central-double",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "post-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "floating|exact|stable|pin",
    "exit": 2,
    "stdout": "",
    "stderr": "[project hook] Manifest check after the failed shell call (actual state of C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0):\n[project hook]   - Dependency change in Directory.Packages.props: added Audit.Package \u2192 .claude/skills/add-dependency/SKILL.md: confirm its version, deprecation, vulnerability, and license steps were completed and report them.\n[project hook]   - Directory.Packages.props [Audit.Package]: floating version '1.*' \u2192 .claude/skills/add-dependency/SKILL.md (Select the version)\n",
    "disposition": "PASS",
    "audit_test_id": "T-286",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "post-failure-floating-central-single",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "post-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "floating|exact|stable|pin",
    "exit": 2,
    "stdout": "",
    "stderr": "[project hook] Manifest check after the failed shell call (actual state of C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0):\n[project hook]   - Directory.Packages.props [Audit.Package]: floating version '1.*' \u2192 .claude/skills/add-dependency/SKILL.md (Select the version)\n",
    "disposition": "PASS",
    "audit_test_id": "T-287",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "fixture-git-init",
    "command": [
      "git",
      "init",
      "--quiet"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-288",
    "audit_role": "setup/observation",
    "adjudicated_disposition": "NOT_APPLICABLE",
    "adjudication": "Fixture initialization/state priming; not a policy assertion."
  },
  {
    "candidate": "L1-Restart",
    "test": "pre-Bash-safe",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/pre-shell-command.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-289",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "pre-Bash-npm-prefix-force",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/pre-shell-command.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"npm --prefix frontend install foo --force\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"Peer-dependency bypass flag (--force / -f / --legacy-peer-deps) detected. The add-dependency workflow requires resolving the actual compatibility problem; confirm only if the user explicitly wants this.\"}}",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-290",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "pre-Bash-npm-workspace-peer",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/pre-shell-command.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"npm --workspace frontend install foo --legacy-peer-deps\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"Peer-dependency bypass flag (--force / -f / --legacy-peer-deps) detected. The add-dependency workflow requires resolving the actual compatibility problem; confirm only if the user explicitly wants this.\"}}",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-291",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "pre-Bash-reserved-reference",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/pre-shell-command.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"Project-reference graph change detected. Changing the project reference graph is Reserved (CLAUDE.md \u00a7 Decision control) unless it implements the approved layout (architecture.layout via project-structure); confirm only with that approval. The architecture check validates the resulting graph.\"}}",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-292",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "pre-Bash-restore",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/pre-shell-command.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"dotnet restore\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-293",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "pre-PowerShell-safe",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/pre-shell-command.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-294",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "pre-PowerShell-npm-prefix-force",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/pre-shell-command.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"npm --prefix frontend install foo --force\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"Peer-dependency bypass flag (--force / -f / --legacy-peer-deps) detected. The add-dependency workflow requires resolving the actual compatibility problem; confirm only if the user explicitly wants this.\"}}",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-295",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "pre-PowerShell-npm-workspace-peer",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/pre-shell-command.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"npm --workspace frontend install foo --legacy-peer-deps\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"Peer-dependency bypass flag (--force / -f / --legacy-peer-deps) detected. The add-dependency workflow requires resolving the actual compatibility problem; confirm only if the user explicitly wants this.\"}}",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-296",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "pre-PowerShell-reserved-reference",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/pre-shell-command.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"ask\",\"permissionDecisionReason\":\"Project-reference graph change detected. Changing the project reference graph is Reserved (CLAUDE.md \u00a7 Decision control) unless it implements the approved layout (architecture.layout via project-structure); confirm only with that approval. The architecture check validates the resulting graph.\"}}",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-297",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "pre-PowerShell-restore",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/pre-shell-command.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"dotnet restore\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-298",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "pre-malformed",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/pre-shell-command.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{bad",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "Blocked by the critical dependency/project-graph hook (fails closed): Hook input is not valid JSON.\n",
    "disposition": "PASS",
    "audit_test_id": "T-299",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "pre-BOM-safe",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/pre-shell-command.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "\ufeff{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"echo audit\"}}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-300",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "nested-clean-check",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\backend\\Audit Nested",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "Instruction check: PASS (68 artifacts, 0 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-301",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "post-initial-state",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/post-change-checks.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PostToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": ".|^$",
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-302",
    "audit_role": "setup/observation",
    "adjudicated_disposition": "NOT_APPLICABLE",
    "adjudication": "Fixture initialization/state priming; not a policy assertion."
  },
  {
    "candidate": "L1-Restart",
    "test": "post-failure-inline-double",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/post-change-checks.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "declares a version|inline|versions.*belong|version.*not allowed|versionless",
    "exit": 2,
    "stdout": "",
    "stderr": "Manifest state after failed Bash call:\n- backend/A.Domain/A.Domain.csproj: PackageReference 'Audit.Package' declares a version; versions belong only in Directory.Packages.props (owner: .claude/rules/3-project/package-management.md).\n",
    "disposition": "PASS",
    "audit_test_id": "T-303",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "post-failure-inline-single",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/post-change-checks.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "declares a version|inline|versions.*belong|version.*not allowed|versionless",
    "exit": 2,
    "stdout": "",
    "stderr": "Manifest state after failed Bash call:\n- backend/A.Domain/A.Domain.csproj: PackageReference 'Audit.Package' declares a version; versions belong only in Directory.Packages.props (owner: .claude/rules/3-project/package-management.md).\n",
    "disposition": "PASS",
    "audit_test_id": "T-304",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "post-failure-inline-multiline",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/post-change-checks.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "declares a version|inline|versions.*belong|version.*not allowed|versionless",
    "exit": 2,
    "stdout": "",
    "stderr": "Manifest state after failed Bash call:\n- backend/A.Domain/A.Domain.csproj: PackageReference 'Audit.Package' declares a version; versions belong only in Directory.Packages.props (owner: .claude/rules/3-project/package-management.md).\n",
    "disposition": "PASS",
    "audit_test_id": "T-305",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "post-failure-outward-double",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/post-change-checks.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "not allowed|forbid|Domain.*Infrastructure|outward|illegal|cannot reference|disallowed",
    "exit": 2,
    "stdout": "",
    "stderr": "Manifest state after failed Bash call:\n- architecture: backend/A.Domain/A.Domain.csproj \u2192 A.Infrastructure: domain-model must not reference implementation-layer (dependency direction, .claude/rules/1-architecture/frame/boundaries.md)\n",
    "disposition": "PASS",
    "audit_test_id": "T-306",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "post-failure-outward-single",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/post-change-checks.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "not allowed|forbid|Domain.*Infrastructure|outward|illegal|cannot reference|disallowed",
    "exit": 2,
    "stdout": "",
    "stderr": "Manifest state after failed Bash call:\n- architecture: backend/A.Domain/A.Domain.csproj \u2192 A.Infrastructure: domain-model must not reference implementation-layer (dependency direction, .claude/rules/1-architecture/frame/boundaries.md)\n",
    "disposition": "PASS",
    "audit_test_id": "T-307",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "post-comment-only",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/post-change-checks.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-308",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "post-failure-floating-central-double",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/post-change-checks.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "floating|exact|stable|pin",
    "exit": 2,
    "stdout": "",
    "stderr": "Manifest state after failed Bash call:\n- Directory.Packages.props: 'Audit.Package' uses a floating or empty version '1.*'; pin the latest stable compatible version (owner: add-dependency).\n",
    "disposition": "PASS",
    "audit_test_id": "T-309",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "post-failure-floating-central-single",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/post-change-checks.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "floating|exact|stable|pin",
    "exit": 2,
    "stdout": "",
    "stderr": "Manifest state after failed Bash call:\n- Directory.Packages.props: 'Audit.Package' uses a floating or empty version '1.*'; pin the latest stable compatible version (owner: add-dependency).\n",
    "disposition": "PASS",
    "audit_test_id": "T-310",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "fixture-git-init",
    "command": [
      "git",
      "init",
      "--quiet"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-311",
    "audit_role": "setup/observation",
    "adjudicated_disposition": "NOT_APPLICABLE",
    "adjudication": "Fixture initialization/state priming; not a policy assertion."
  },
  {
    "candidate": "K0",
    "test": "pre-Bash-safe",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "pre-tool-use"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-312",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "pre-Bash-npm-prefix-force",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "pre-tool-use"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"npm --prefix frontend install foo --force\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"Dependency change detected: npm --prefix frontend install foo --force\\nRun the `add-dependency` workflow first; when its checks are complete, re-run the command with the trailing comment `# add-dependency: reviewed`.\\nThe command uses --force or --legacy-peer-deps: resolve the actual peer-dependency conflict instead (`add-dependency` \u00a7 5).\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-313",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "pre-Bash-npm-workspace-peer",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "pre-tool-use"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"npm --workspace frontend install foo --legacy-peer-deps\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"Dependency change detected: npm --workspace frontend install foo --legacy-peer-deps\\nRun the `add-dependency` workflow first; when its checks are complete, re-run the command with the trailing comment `# add-dependency: reviewed`.\\nThe command uses --force or --legacy-peer-deps: resolve the actual peer-dependency conflict instead (`add-dependency` \u00a7 5).\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-314",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "pre-Bash-reserved-reference",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "pre-tool-use"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"Project-reference graph change: dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj\\nChanging the project reference graph is Reserved (CLAUDE.md \u00a7 Decisions) unless an accepted decision already requires the reference, even when the new reference would be legal.\\nFollow `project-structure` \u00a7 Changing project references (Decision Request: `architecture-decision`), then re-run the command with the trailing comment `# project-references: approved`.\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-315",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "pre-Bash-restore",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "pre-tool-use"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"dotnet restore\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-316",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "pre-PowerShell-safe",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "pre-tool-use"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-317",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "pre-PowerShell-npm-prefix-force",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "pre-tool-use"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"npm --prefix frontend install foo --force\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"Dependency change detected: npm --prefix frontend install foo --force\\nRun the `add-dependency` workflow first; when its checks are complete, re-run the command with the trailing comment `# add-dependency: reviewed`.\\nThe command uses --force or --legacy-peer-deps: resolve the actual peer-dependency conflict instead (`add-dependency` \u00a7 5).\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-318",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "pre-PowerShell-npm-workspace-peer",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "pre-tool-use"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"npm --workspace frontend install foo --legacy-peer-deps\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"Dependency change detected: npm --workspace frontend install foo --legacy-peer-deps\\nRun the `add-dependency` workflow first; when its checks are complete, re-run the command with the trailing comment `# add-dependency: reviewed`.\\nThe command uses --force or --legacy-peer-deps: resolve the actual peer-dependency conflict instead (`add-dependency` \u00a7 5).\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-319",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "pre-PowerShell-reserved-reference",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "pre-tool-use"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"Project-reference graph change: dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj\\nChanging the project reference graph is Reserved (CLAUDE.md \u00a7 Decisions) unless an accepted decision already requires the reference, even when the new reference would be legal.\\nFollow `project-structure` \u00a7 Changing project references (Decision Request: `architecture-decision`), then re-run the command with the trailing comment `# project-references: approved`.\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-320",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "pre-PowerShell-restore",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "pre-tool-use"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"dotnet restore\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-321",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "pre-malformed",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "pre-tool-use"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{bad",
    "expected": "reject",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"[hook] the pre-command policy check could not run, so the command was blocked: hook input is not valid JSON: Expected property name or '}' in JSON at position 1 (line 1 column 2)\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-322",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "pre-BOM-safe",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "pre-tool-use"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "\ufeff{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"echo audit\"}}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-323",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "nested-clean-check",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0\\.claude\\scripts\\check-instructions.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0\\backend\\Audit Nested",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 1,
    "stdout": "ERROR backend/Audit Nested: empty directory; create directories only for real content.\nINFO  always-loaded surface \u2248 19738 characters (\u2248 4935 tokens) including skill and agent listings\ncheck-instructions: C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0: 60 artifact(s), 1 error(s).\n",
    "stderr": "",
    "disposition": "FAIL",
    "audit_test_id": "T-324",
    "audit_role": "assertion",
    "adjudicated_disposition": "UNVERIFIED",
    "adjudication": "Empty fixture directories made this unsuitable as a clean nested-cwd positive. Root discovery itself was not shown to fail."
  },
  {
    "candidate": "K0",
    "test": "post-initial-state",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "post-tool-use"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PostToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": ".|^$",
    "exit": 0,
    "stdout": "{\"decision\":\"block\",\"reason\":\"Worktree state after the shell command \u2014 C:\\\\Users\\\\atonkonog\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0:\\n[instructions] backend/Audit Nested: empty directory; create directories only for real content.\"}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-325",
    "audit_role": "setup/observation",
    "adjudicated_disposition": "NOT_APPLICABLE",
    "adjudication": "Fixture initialization/state priming; not a policy assertion."
  },
  {
    "candidate": "K0",
    "test": "post-failure-inline-double",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "post-tool-use-failure"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "declares a version|inline|versions.*belong|version.*not allowed|versionless",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"Worktree state after the failed shell command (its partial changes count) \u2014 C:\\\\Users\\\\atonkonog\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0:\\n[manifest] backend/A.Domain/A.Domain.csproj: PackageReference Audit.Package has a version; versions belong in Directory.Packages.props (rules/common/dependencies.md \u00a7 NuGet).\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-326",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "post-failure-inline-single",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "post-tool-use-failure"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "declares a version|inline|versions.*belong|version.*not allowed|versionless",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"Worktree state after the failed shell command (its partial changes count) \u2014 C:\\\\Users\\\\atonkonog\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0:\\n[manifest] backend/A.Domain/A.Domain.csproj: PackageReference Audit.Package has a version; versions belong in Directory.Packages.props (rules/common/dependencies.md \u00a7 NuGet).\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-327",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "post-failure-inline-multiline",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "post-tool-use-failure"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "declares a version|inline|versions.*belong|version.*not allowed|versionless",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"Worktree state after the failed shell command (its partial changes count) \u2014 C:\\\\Users\\\\atonkonog\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0:\\n[manifest] backend/A.Domain/A.Domain.csproj: PackageReference Audit.Package has a version; versions belong in Directory.Packages.props (rules/common/dependencies.md \u00a7 NuGet).\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-328",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "post-failure-outward-double",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "post-tool-use-failure"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "not allowed|forbid|Domain.*Infrastructure|outward|illegal|cannot reference|disallowed",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"Worktree state after the failed shell command (its partial changes count) \u2014 C:\\\\Users\\\\atonkonog\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0:\\n[manifest] backend/A.Domain/A.Domain.csproj: Domain must not reference Infrastructure (A.Infrastructure); dependencies point inward (rules/backend/architecture.md \u00a7 Dependency direction, D-01).\\n[manifest] the project references of backend/A.Domain/A.Domain.csproj changed: changing the project reference graph is Reserved (CLAUDE.md \u00a7 Decisions) \u2014 confirm it was approved and recorded (`architecture-decision`), or revert it.\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-329",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "post-failure-outward-single",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "post-tool-use-failure"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "not allowed|forbid|Domain.*Infrastructure|outward|illegal|cannot reference|disallowed",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"Worktree state after the failed shell command (its partial changes count) \u2014 C:\\\\Users\\\\atonkonog\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0:\\n[manifest] backend/A.Domain/A.Domain.csproj: Domain must not reference Infrastructure (A.Infrastructure); dependencies point inward (rules/backend/architecture.md \u00a7 Dependency direction, D-01).\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-330",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "post-comment-only",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "post-tool-use-failure"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"Worktree state after the failed shell command (its partial changes count) \u2014 C:\\\\Users\\\\atonkonog\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0:\\n[manifest] backend/A.Domain/A.Domain.csproj: PackageReference Audit.Package has a version; versions belong in Directory.Packages.props (rules/common/dependencies.md \u00a7 NuGet).\\n[manifest] the project references of backend/A.Domain/A.Domain.csproj changed: changing the project reference graph is Reserved (CLAUDE.md \u00a7 Decisions) \u2014 confirm it was approved and recorded (`architecture-decision`), or revert it.\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-331",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "post-failure-floating-central-double",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "post-tool-use-failure"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "floating|exact|stable|pin",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"Worktree state after the failed shell command (its partial changes count) \u2014 C:\\\\Users\\\\atonkonog\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0:\\n[manifest] Directory.Packages.props: Audit.Package uses a floating or range version \\\"1.*\\\"; pin the verified stable version (add-dependency \u00a7 2).\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-332",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "post-failure-floating-central-single",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "post-tool-use-failure"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "floating|exact|stable|pin",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUseFailure\",\"additionalContext\":\"Worktree state after the failed shell command (its partial changes count) \u2014 C:\\\\Users\\\\atonkonog\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0:\\n[manifest] Directory.Packages.props: Audit.Package uses a floating or range version \\\"1.*\\\"; pin the verified stable version (add-dependency \u00a7 2).\"}}\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-333",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "fixture-git-init",
    "command": [
      "git",
      "init",
      "--quiet"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-334",
    "audit_role": "setup/observation",
    "adjudicated_disposition": "NOT_APPLICABLE",
    "adjudication": "Fixture initialization/state priming; not a policy assertion."
  },
  {
    "candidate": "K1",
    "test": "pre-Bash-safe",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PreToolUse"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-335",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "pre-Bash-npm-prefix-force",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PreToolUse"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"npm --prefix frontend install foo --force\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "Blocked before execution (dependency and project-reference guard):\n- `npm --prefix frontend install foo --force`: --force/--legacy-peer-deps bypasses peer-dependency resolution -> add-dependency workflow (peer-dependency conflicts)\n- `npm --prefix frontend install foo --force`: foo without an exact version -> add-dependency workflow (version selection)\n",
    "disposition": "PASS",
    "audit_test_id": "T-336",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "pre-Bash-npm-workspace-peer",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PreToolUse"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"npm --workspace frontend install foo --legacy-peer-deps\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "Blocked before execution (dependency and project-reference guard):\n- `npm --workspace frontend install foo --legacy-peer-deps`: --force/--legacy-peer-deps bypasses peer-dependency resolution -> add-dependency workflow (peer-dependency conflicts)\n- `npm --workspace frontend install foo --legacy-peer-deps`: foo without an exact version -> add-dependency workflow (version selection)\n",
    "disposition": "PASS",
    "audit_test_id": "T-337",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "pre-Bash-reserved-reference",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PreToolUse"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "Blocked before execution (dependency and project-reference guard):\n- `dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj`: changes the project reference graph (A.Domain -> A.Infrastructure), a Reserved decision without a recorded approval -> architecture-decision workflow (approval recorded as `From -> To` in docs/architecture/decision-register.md, Accepted decisions)\n",
    "disposition": "PASS",
    "audit_test_id": "T-338",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "pre-Bash-restore",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PreToolUse"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"dotnet restore\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-339",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "pre-PowerShell-safe",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PreToolUse"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-340",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "pre-PowerShell-npm-prefix-force",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PreToolUse"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"npm --prefix frontend install foo --force\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "Blocked before execution (dependency and project-reference guard):\n- `npm --prefix frontend install foo --force`: --force/--legacy-peer-deps bypasses peer-dependency resolution -> add-dependency workflow (peer-dependency conflicts)\n- `npm --prefix frontend install foo --force`: foo without an exact version -> add-dependency workflow (version selection)\n",
    "disposition": "PASS",
    "audit_test_id": "T-341",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "pre-PowerShell-npm-workspace-peer",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PreToolUse"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"npm --workspace frontend install foo --legacy-peer-deps\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "Blocked before execution (dependency and project-reference guard):\n- `npm --workspace frontend install foo --legacy-peer-deps`: --force/--legacy-peer-deps bypasses peer-dependency resolution -> add-dependency workflow (peer-dependency conflicts)\n- `npm --workspace frontend install foo --legacy-peer-deps`: foo without an exact version -> add-dependency workflow (version selection)\n",
    "disposition": "PASS",
    "audit_test_id": "T-342",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "pre-PowerShell-reserved-reference",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PreToolUse"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj\"}, \"session_id\": \"independent-audit\"}",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "Blocked before execution (dependency and project-reference guard):\n- `dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj`: changes the project reference graph (A.Domain -> A.Infrastructure), a Reserved decision without a recorded approval -> architecture-decision workflow (approval recorded as `From -> To` in docs/architecture/decision-register.md, Accepted decisions)\n",
    "disposition": "PASS",
    "audit_test_id": "T-343",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "pre-PowerShell-restore",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PreToolUse"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"dotnet restore\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-344",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "pre-malformed",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PreToolUse"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{bad",
    "expected": "reject",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "[hook PreToolUse] blocked (fail closed): hook input is not valid JSON (Expected property name or '}' in JSON at position 1 (line 1 column 2))\n",
    "disposition": "PASS",
    "audit_test_id": "T-345",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "pre-BOM-safe",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PreToolUse"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "\ufeff{\"hook_event_name\": \"PreToolUse\", \"tool_name\": \"PowerShell\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"echo audit\"}}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-346",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "nested-clean-check",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1\\.claude\\scripts\\check-instructions.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1\\backend\\Audit Nested",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "check-instructions (C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1): 0 error(s), 0 warning(s); always-loaded surface about 4849 tokens\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-347",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "post-initial-state",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PostToolUse"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PostToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": ".|^$",
    "exit": 2,
    "stdout": "",
    "stderr": "Manifest and project-reference check:\n[error] backend/A.Domain/A.Domain.csproj: project reference graph changed without a recorded approval (Reserved): project A.Domain added -> architecture-decision workflow (record the approval as `From -> To` in docs/architecture/decision-register.md, Accepted decisions)\n[error] backend/A.Infrastructure/A.Infrastructure.csproj: project reference graph changed without a recorded approval (Reserved): project A.Infrastructure added -> architecture-decision workflow (record the approval as `From -> To` in docs/architecture/decision-register.md, Accepted decisions)\n",
    "disposition": "PASS",
    "audit_test_id": "T-348",
    "audit_role": "setup/observation",
    "adjudicated_disposition": "NOT_APPLICABLE",
    "adjudication": "Fixture initialization/state priming; not a policy assertion."
  },
  {
    "candidate": "K1",
    "test": "post-failure-inline-double",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PostToolUseFailure"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "declares a version|inline|versions.*belong|version.*not allowed|versionless",
    "exit": 2,
    "stdout": "",
    "stderr": "The failed command still changed relevant files:\nManifest and project-reference check:\n[error] backend/A.Domain/A.Domain.csproj: PackageReference \"Audit.Package\" declares a version (central package management) -> .claude/rules/backend/dependencies.md\n",
    "disposition": "PASS",
    "audit_test_id": "T-349",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "post-failure-inline-single",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PostToolUseFailure"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "declares a version|inline|versions.*belong|version.*not allowed|versionless",
    "exit": 2,
    "stdout": "",
    "stderr": "The failed command still changed relevant files:\nManifest and project-reference check:\n[error] backend/A.Domain/A.Domain.csproj: PackageReference \"Audit.Package\" declares a version (central package management) -> .claude/rules/backend/dependencies.md\n",
    "disposition": "PASS",
    "audit_test_id": "T-350",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "post-failure-inline-multiline",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PostToolUseFailure"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "declares a version|inline|versions.*belong|version.*not allowed|versionless",
    "exit": 2,
    "stdout": "",
    "stderr": "The failed command still changed relevant files:\nManifest and project-reference check:\n[error] backend/A.Domain/A.Domain.csproj: PackageReference \"Audit.Package\" declares a version (central package management) -> .claude/rules/backend/dependencies.md\n",
    "disposition": "PASS",
    "audit_test_id": "T-351",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "post-failure-outward-double",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PostToolUseFailure"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "not allowed|forbid|Domain.*Infrastructure|outward|illegal|cannot reference|disallowed",
    "exit": 2,
    "stdout": "",
    "stderr": "The failed command still changed relevant files:\nManifest and project-reference check:\n[error] backend/A.Domain/A.Domain.csproj: Domain must not reference Infrastructure (\"A.Infrastructure\") -> .claude/rules/backend/architecture-style.md\n[error] backend/A.Domain/A.Domain.csproj: project reference graph changed without a recorded approval (Reserved): A.Domain -> A.Infrastructure added -> architecture-decision workflow (record the approval as `From -> To` in docs/architecture/decision-register.md, Accepted decisions)\n",
    "disposition": "PASS",
    "audit_test_id": "T-352",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "post-failure-outward-single",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PostToolUseFailure"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "not allowed|forbid|Domain.*Infrastructure|outward|illegal|cannot reference|disallowed",
    "exit": 2,
    "stdout": "",
    "stderr": "The failed command still changed relevant files:\nManifest and project-reference check:\n[error] backend/A.Domain/A.Domain.csproj: Domain must not reference Infrastructure (\"A.Infrastructure\") -> .claude/rules/backend/architecture-style.md\n",
    "disposition": "PASS",
    "audit_test_id": "T-353",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "post-comment-only",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PostToolUseFailure"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-354",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "post-failure-floating-central-double",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PostToolUseFailure"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "floating|exact|stable|pin",
    "exit": 2,
    "stdout": "",
    "stderr": "The failed command still changed relevant files:\nManifest and project-reference check:\n[error] Directory.Packages.props: PackageVersion \"Audit.Package\" has a missing, floating, or range version \"1.*\" -> add-dependency workflow\n",
    "disposition": "PASS",
    "audit_test_id": "T-355",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "post-failure-floating-central-single",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "PostToolUseFailure"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"independent-audit\"}",
    "expected": "observe",
    "pattern": "floating|exact|stable|pin",
    "exit": 2,
    "stdout": "",
    "stderr": "The failed command still changed relevant files:\nManifest and project-reference check:\n[error] Directory.Packages.props: PackageVersion \"Audit.Package\" has a missing, floating, or range version \"1.*\" -> add-dependency workflow\n",
    "disposition": "PASS",
    "audit_test_id": "T-356",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "structure-missing-verify",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": null,
    "expected": "reject",
    "pattern": "verify",
    "exit": 1,
    "stdout": "INFO  always-loaded estimate: ~4705 tokens (CLAUDE.md + imports 12735 chars, skill/agent listing 6086 chars)\nFAIL  .claude/skills/verify: missing SKILL.md\nFAIL  .claude/MAP.md: reference `.claude/skills/verify/SKILL.md` does not resolve\ncheck-instructions: 47 instruction file(s), 2 failure(s), 0 warning(s)\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-357",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "structure-missing-fail-closed",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": null,
    "expected": "reject",
    "pattern": "onFailure|fail.closed",
    "exit": 1,
    "stdout": "INFO  always-loaded estimate: ~4766 tokens (CLAUDE.md + imports 12735 chars, skill/agent listing 6328 chars)\nFAIL  settings.json PreToolUse: the policy guard must set \"onFailure\": \"block\" so a failing or timed-out guard blocks the tool call\ncheck-instructions: 48 instruction file(s), 1 failure(s), 0 warning(s)\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-358",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "stop-recursion-guard",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/stop-co-change.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"Stop\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"audit-reconfirmation\", \"stop_hook_active\": true}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-359",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M",
    "test": "reconfirm-reference-post-route",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M/.claude/hooks/dependency-guard.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M",
    "input": "{\"hook_event_name\": \"PostToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M\", \"tool_input\": {\"command\": \"dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj\"}, \"session_id\": \"audit-reconfirmation\"}",
    "expected": "accept",
    "pattern": "project references|reference graph|Decision Control",
    "exit": 0,
    "stdout": "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUse\",\"additionalContext\":\"Manifest-changing command detected (dotnet add backend/A.Domain/A.Domain.csproj reference backend/A.Infrastructure/A.Infrastructure.csproj); the manifest check of C:\\\\Users\\\\atonkonog\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M found no violations. If not already done, confirm the project references follow .claude/rules/architecture.md (Project References) and that a changed production reference graph went through CLAUDE.md \u00a7 Decision Control.\"}}",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-360",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "structure-missing-verify",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1\\.claude\\scripts\\check-instructions.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": null,
    "expected": "reject",
    "pattern": "verify",
    "exit": 1,
    "stdout": "ERROR: .claude/skills/build-fix/SKILL.md: section reference target does not resolve: verify\nERROR: .claude/skills/ci-cd/SKILL.md: section reference target does not resolve: verify\nERROR: .claude/skills/ci-cd/SKILL.md: section reference target does not resolve: verify\nERROR: .claude/skills/code-review/SKILL.md: section reference target does not resolve: verify\nERROR: .claude/skills/custom-settings/SKILL.md: workflow reference does not resolve: verify\nERROR: .claude/skills/development-workflow/SKILL.md: workflow reference does not resolve: verify\nERROR: .claude/skills/docker/SKILL.md: section reference target does not resolve: verify\nERROR: .claude/skills/docker/SKILL.md: section reference target does not resolve: verify\nERROR: .claude/skills/dotnet-testing/SKILL.md: section reference target does not resolve: verify\nERROR: .claude/skills/persistence-change/SKILL.md: section reference target does not resolve: verify\nERROR: .claude/skills/swagger/SKILL.md: section reference target does not resolve: verify\nERROR: CLAUDE.md: routing target does not exist: verify\nERROR: .claude/skills: required workflow skill missing: verify\ncheck-instructions: 64 instruction file(s), always-loaded ~5514 tokens, 13 error(s), 0 warning(s)\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-361",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "structure-missing-fail-closed",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1\\.claude\\scripts\\check-instructions.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": null,
    "expected": "reject",
    "pattern": "onFailure|fail.closed",
    "exit": 1,
    "stdout": "ERROR: .claude/settings.json: PreToolUse hook: critical pre-tool enforcement must fail closed (onFailure: \"block\").\ncheck-instructions: 65 instruction file(s), always-loaded ~5568 tokens, 1 error(s), 0 warning(s)\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-362",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "structure-missing-selected-module",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1\\.claude\\scripts\\check-instructions.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": null,
    "expected": "reject",
    "pattern": "module|manifest",
    "exit": 1,
    "stdout": "ERROR: .claude/capabilities/persistence/ef-core/MODULE.md: manifest of the selected implementation is missing.\nERROR: docs/capabilities/persistence.md: declares Capability: persistence/ef-core, which is not selected (unselected implementations must not enter runtime).\nERROR: .claude/rules/persistence-technology.md: declares Capability: persistence/ef-core, which is not selected (unselected implementations must not enter runtime).\nERROR: .claude/skills/ef-core/SKILL.md: declares Capability: persistence/ef-core, which is not selected (unselected implementations must not enter runtime).\nERROR: .claude/skills/persistence-change/SKILL.md: declares Capability: persistence/ef-core, which is not selected (unselected implementations must not enter runtime).\nERROR: CLAUDE.md: planning facet of unselected slot persistence is still imported.\nERROR: docs/capabilities/persistence.md: slot persistence is not selected; remove its planning facet.\nERROR: .claude/skills/persistence-change/SKILL.md:34: uses frame-specific names (\"Infrastructure\") without declaring binds to the architecture frame.\ncheck-instructions: 64 instruction file(s), always-loaded ~5568 tokens, 8 error(s), 0 warning(s)\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-363",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "M1",
    "test": "stop-recursion-guard",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1/.claude/hooks/stop.js"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\M1",
    "input": "{\"hook_event_name\": \"Stop\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\M1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"audit-reconfirmation\", \"stop_hook_active\": true}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-364",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "structure-missing-verify",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "verify",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 4959 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/skills/verify/SKILL.md: missing\nerror: required skill 'verify' is missing\nerror: .claude/skills/build-fix/SKILL.md: routed workflow 'verify' does not exist\nerror: .claude/skills/custom-settings/SKILL.md: routed workflow 'verify' does not exist\nerror: .claude/skills/delivery-pipeline/SKILL.md: routed workflow 'verify' does not exist\nerror: .claude/skills/development-workflow/SKILL.md: routed workflow 'verify' does not exist\nerror: .claude/skills/git-workflow/SKILL.md: routed workflow 'verify' does not exist\nerror: .claude/skills/project-structure/SKILL.md: routed workflow 'verify' does not exist\nerror: .claude/skills/template-maintenance/SKILL.md: routed workflow 'verify' does not exist\nerror: .claude/INSTRUCTION_MAP.md: reference '.claude/skills/verify/SKILL.md' does not resolve\nerror: .claude/INSTRUCTION_MAP.md: routed workflow 'verify' does not exist\nerror: CLAUDE.md: routing target 'verify' does not exist\nInstruction structure: FAIL (12 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-365",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "structure-missing-fail-closed",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0\\.claude\\tools\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": null,
    "expected": "reject",
    "pattern": "onFailure|fail.closed",
    "exit": 1,
    "stdout": "info: always-loaded surface \u2248 5002 tokens (CLAUDE.md + imports + skill/agent listings; chars/4 estimate)\nerror: .claude/settings.json PreToolUse (Bash|PowerShell): the critical guard must fail closed (onFailure: \"block\")\nInstruction structure: FAIL (1 error(s))\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-366",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "stop-recursion-guard",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "stop"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"Stop\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"audit-reconfirmation\", \"stop_hook_active\": true}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-367",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L0",
    "test": "reconfirm-comment-prime",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "post-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PostToolUse\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"audit-reconfirmation\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 2,
    "stdout": "",
    "stderr": "[project hook] Manifest check after the shell call (actual state of C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0):\n[project hook]   - Manifest removed: backend/A.Infrastructure/A.Infrastructure.csproj \u2192 .claude/skills/project-structure/SKILL.md (a production project or reference-graph change outside the layout mapped by .claude/rules/3-project/layout.md requires approval \u2014 CLAUDE.md \u2192 Decision control); report it.\n[project hook]   - Dependency change in Directory.Packages.props: removed Audit.Package \u2192 .claude/skills/add-dependency/SKILL.md: confirm its version, deprecation, vulnerability, and license steps were completed and report them.\n",
    "disposition": "FAIL",
    "audit_test_id": "T-368",
    "audit_role": "setup/observation",
    "adjudicated_disposition": "NOT_APPLICABLE",
    "adjudication": "Fixture initialization/state priming; not a policy assertion."
  },
  {
    "candidate": "L0",
    "test": "reconfirm-comment-only",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0/.claude/hooks/claude-hook.mjs",
      "post-bash"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L0",
    "input": "{\"hook_event_name\": \"PostToolUseFailure\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"audit-reconfirmation\"}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-369",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "structure-missing-verify",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "verify",
    "exit": 1,
    "stdout": "VIOLATION .claude/skills/verify: required skill is missing\nVIOLATION .claude/skills/development-workflow/SKILL.md: references unknown skill or agent 'verify'\nVIOLATION .claude/skills/project-structure/SKILL.md: references unknown skill or agent 'verify'\nVIOLATION .claude/INSTRUCTION_MAP.md: path reference does not resolve: .claude/skills/verify/SKILL.md\nInstruction check: FAIL (67 artifacts, 4 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-370",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "structure-missing-fail-closed",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "onFailure|fail.closed",
    "exit": 1,
    "stdout": "VIOLATION .claude/settings.json: critical PreToolUse hook must set onFailure: \"block\" (fail closed on missing script, crash, malformed input, timeout)\nInstruction check: FAIL (68 artifacts, 1 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-371",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "structure-missing-selected-module",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart\\.claude\\scripts\\check-instructions.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": null,
    "expected": "reject",
    "pattern": "module|manifest",
    "exit": 1,
    "stdout": "VIOLATION .claude/capabilities/persistence/ef-core/MODULE.md: missing module manifest\nVIOLATION .claude/rules/2-technology/persistence/access.md: declares Capability 'persistence/ef-core', which is not a selected module\nVIOLATION .claude/rules/2-technology/persistence/seeding.md: declares Capability 'persistence/ef-core', which is not a selected module\nVIOLATION .claude/rules/3-project/development-database.md: declares Capability 'persistence/ef-core', which is not a selected module\nVIOLATION .claude/skills/ef-core/SKILL.md: declares Capability 'persistence/ef-core', which is not a selected module\nVIOLATION .claude/capabilities/persistence/ef-core/commands.md: declares Capability 'persistence/ef-core', which is not a selected module\nVIOLATION .claude/capabilities/persistence/ef-core/workflow.md: declares Capability 'persistence/ef-core', which is not a selected module\nVIOLATION .claude/INSTRUCTION_MAP.md: facet reference 'persistence.access' but slot 'persistence' has no module\nVIOLATION .claude/INSTRUCTION_MAP.md: facet reference 'persistence.seeding' but slot 'persistence' has no module\nVIOLATION .claude/INSTRUCTION_MAP.md: facet reference 'persistence.dev-config' but slot 'persistence' has no module\nVIOLATION .claude/INSTRUCTION_MAP.md: facet reference 'persistence.workflow' but slot 'persistence' has no module\nVIOLATION .claude/INSTRUCTION_MAP.md: facet reference 'persistence.commands' but slot 'persistence' has no module\nVIOLATION .claude/INSTRUCTION_MAP.md: facet reference 'persistence.enforcement' but slot 'persistence' has no module\nVIOLATION .claude/INSTRUCTION_MAP.md: facet reference 'persistence.knowledge' but slot 'persistence' has no module\nVIOLATION .claude/INSTRUCTION_MAP.md: facet reference 'persistence.workflow' but slot 'persistence' has no module\nVIOLATION .claude/INSTRUCTION_MAP.md: facet reference 'persistence.workflow' but slot 'persistence' has no module\nVIOLATION .claude/rules/2-technology/persistence/access.md: facet reference 'persistence.access' but slot 'persistence' has no module\nVIOLATION .claude/rules/2-technology/persistence/access.md: facet reference 'persistence.workflow' but slot 'persistence' has no module\nVIOLATION .claude/rules/2-technology/persistence/seeding.md: facet reference 'persistence.seeding' but slot 'persistence' has no module\nVIOLATION .claude/rules/2-technology/persistence/seeding.md: facet reference 'persistence.workflow' but slot 'persistence' has no module\nVIOLATION .claude/rules/3-project/development-database.md: facet reference 'persistence.dev-config' but slot 'persistence' has no module\nVIOLATION .claude/skills/ci-cd/SKILL.md: facet reference 'persistence.commands' but slot 'persistence' has no module\nVIOLATION .claude/skills/code-review/SKILL.md: facet reference 'persistence.workflow' but slot 'persistence' has no module\nVIOLATION .claude/skills/custom-settings/SKILL.md: facet reference 'persistence.workflow' but slot 'persistence' has no module\nVIOLATION .claude/skills/development-workflow/SKILL.md: facet reference 'persistence.workflow' but slot 'persistence' has no module\nVIOLATION .claude/skills/dotnet-testing/SKILL.md: facet reference 'persistence.commands' but slot 'persistence' has no module\nVIOLATION .claude/skills/dotnet-testing/SKILL.md: facet reference 'persistence.access' but slot 'persistence' has no module\nVIOLATION .claude/skills/ef-core/SKILL.md: facet reference 'persistence.knowledge' but slot 'persistence' has no module\nVIOLATION .claude/skills/ef-core/SKILL.md: facet reference 'persistence.access' but slot 'persistence' has no module\nVIOLATION .claude/skills/ef-core/SKILL.md: facet reference 'persistence.seeding' but slot 'persistence' has no module\nVIOLATION .claude/skills/ef-core/SKILL.md: facet reference 'persistence.workflow' but slot 'persistence' has no module\nVIOLATION .claude/skills/ef-core/SKILL.md: facet reference 'persistence.commands' but slot 'persistence' has no module\nVIOLATION .claude/skills/ef-core/SKILL.md: facet reference 'persistence.commands' but slot 'persistence' has no module\nVIOLATION .claude/skills/project-structure/references/baseline-packages.md: facet reference 'persistence.commands' but slot 'persistence' has no module\nVIOLATION .claude/skills/project-structure/SKILL.md: facet reference 'persistence.commands' but slot 'persistence' has no module\nVIOLATION .claude/skills/verify/SKILL.md: facet reference 'persistence.workflow' but slot 'persistence' has no module\nVIOLATION .claude/skills/verify/SKILL.md: facet reference 'persistence.workflow' but slot 'persistence' has no module\nVIOLATION .claude/capabilities/architecture/clean-architecture/layout.md: facet reference 'persistence.seeding' but slot 'persistence' has no module\nVIOLATION .claude/capabilities/persistence/CONTRACT.md: facet reference 'persistence.access' but slot 'persistence' has no module\nVIOLATION .claude/capabilities/persistence/CONTRACT.md: facet reference 'persistence.seeding' but slot 'persistence' has no module\nVIOLATION .claude/capabilities/persistence/CONTRACT.md: facet reference 'persistence.dev-config' but slot 'persistence' has no module\nVIOLATION .claude/capabilities/persistence/CONTRACT.md: facet reference 'persistence.workflow' but slot 'persistence' has no module\nVIOLATION .claude/capabilities/persistence/CONTRACT.md: facet reference 'persistence.commands' but slot 'persistence' has no module\nVIOLATION .claude/capabilities/persistence/CONTRACT.md: facet reference 'persistence.enforcement' but slot 'persistence' has no module\nVIOLATION .claude/capabilities/persistence/CONTRACT.md: facet reference 'persistence.dev-config' but slot 'persistence' has no module\nVIOLATION .claude/capabilities/persistence/ef-core/commands.md: facet reference 'persistence.commands' but slot 'persistence' has no module\nVIOLATION .claude/capabilities/persistence/ef-core/commands.md: facet reference 'persistence.workflow' but slot 'persistence' has no module\nVIOLATION .claude/capabilities/persistence/ef-core/commands.md: facet reference 'persistence.dev-config' but slot 'persistence' has no module\nVIOLATION .claude/capabilities/persistence/ef-core/workflow.md: facet reference 'persistence.workflow' but slot 'persistence' has no module\nVIOLATION .claude/capabilities/persistence/ef-core/workflow.md: facet reference 'persistence.access' but slot 'persistence' has no module\nVIOLATION .claude/capabilities/persistence/ef-core/workflow.md: facet reference 'persistence.seeding' but slot 'persistence' has no module\nVIOLATION .claude/capabilities/persistence/ef-core/workflow.md: facet reference 'persistence.commands' but slot 'persistence' has no module\nVIOLATION .claude/INSTRUCTION_MAP.md: path reference does not resolve: .claude/capabilities/persistence/ef-core/MODULE.md\nInstruction check: FAIL (67 artifacts, 53 violation(s), 0 warning(s)).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-372",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "L1-Restart",
    "test": "stop-recursion-guard",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart/.claude/hooks/stop-cochange.mjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\L1-Restart",
    "input": "{\"hook_event_name\": \"Stop\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\L1-Restart\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"audit-reconfirmation\", \"stop_hook_active\": true}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-373",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "structure-missing-verify",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0\\.claude\\scripts\\check-instructions.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": null,
    "expected": "reject",
    "pattern": "verify",
    "exit": 1,
    "stdout": "ERROR .claude/skills/verify: empty directory; create directories only for real content.\nERROR .claude/skills: required workflow \"verify\" is missing.\nERROR .claude/skills/verify: empty directory; create directories only for real content.\nERROR backend/A.Domain: empty directory; create directories only for real content.\nERROR backend/A.Infrastructure: empty directory; create directories only for real content.\nERROR .claude/skills/build-fix/SKILL.md: line 10: reference `verify` does not resolve.\nERROR .claude/skills/build-fix/SKILL.md: line 131: reference `verify` does not resolve.\nERROR .claude/skills/build-fix/SKILL.md: line 131: reference `verify` does not resolve.\nERROR .claude/skills/code-review/SKILL.md: line 10: reference `verify` does not resolve.\nERROR .claude/skills/code-review/SKILL.md: line 47: reference `verify` does not resolve.\nERROR .claude/skills/custom-settings/SKILL.md: line 42: reference `verify` does not resolve.\nERROR .claude/skills/development-workflow/SKILL.md: line 77: reference `verify` does not resolve.\nERROR .claude/skills/development-workflow/SKILL.md: line 81: reference `verify` does not resolve.\nERROR .claude/skills/dotnet-testing/SKILL.md: line 10: reference `verify` does not resolve.\nERROR .claude/skills/git-workflow/SKILL.md: line 69: reference `verify` does not resolve.\nERROR .claude/skills/project-structure/SKILL.md: line 30: reference `verify` does not resolve.\nERROR .claude/skills/swagger/SKILL.md: line 87: reference `verify` does not resolve.\nERROR CLAUDE.md: line 63: reference `verify` does not resolve.\nERROR .editorconfig: line 22: reference `.claude/skills/verify/SKILL.md` does not resolve.\nINFO  always-loaded surface \u2248 19522 characters (\u2248 4881 tokens) including skill and agent listings\ncheck-instructions: C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0: 59 artifact(s), 19 error(s).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-374",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "structure-missing-fail-closed",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0\\.claude\\scripts\\check-instructions.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": null,
    "expected": "reject",
    "pattern": "onFailure|fail.closed",
    "exit": 1,
    "stdout": "ERROR backend/A.Domain: empty directory; create directories only for real content.\nERROR backend/A.Infrastructure: empty directory; create directories only for real content.\nERROR .claude/settings.json: PreToolUse policy hook must fail closed (\"onFailure\": \"block\").\nINFO  always-loaded surface \u2248 19738 characters (\u2248 4935 tokens) including skill and agent listings\ncheck-instructions: C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0: 60 artifact(s), 3 error(s).\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-375",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "stop-recursion-guard",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0/.claude/hooks/hook.cjs",
      "stop"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0",
    "input": "{\"hook_event_name\": \"Stop\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K0\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"audit-reconfirmation\", \"stop_hook_active\": true}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-376",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K0",
    "test": "reconfirm-nested-populated",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0\\.claude\\scripts\\check-instructions.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0\\backend\\Audit Nested",
    "input": null,
    "expected": "accept",
    "pattern": null,
    "exit": 1,
    "stdout": "ERROR backend/A.Domain: empty directory; create directories only for real content.\nERROR backend/A.Infrastructure: empty directory; create directories only for real content.\nINFO  always-loaded surface \u2248 19738 characters (\u2248 4935 tokens) including skill and agent listings\ncheck-instructions: C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K0: 60 artifact(s), 2 error(s).\n",
    "stderr": "",
    "disposition": "FAIL",
    "audit_test_id": "T-377",
    "audit_role": "assertion",
    "adjudicated_disposition": "UNVERIFIED",
    "adjudication": "Empty fixture directories made this unsuitable as a clean nested-cwd positive. Root discovery itself was not shown to fail."
  },
  {
    "candidate": "K1",
    "test": "structure-missing-verify",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1\\.claude\\scripts\\check-instructions.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": null,
    "expected": "reject",
    "pattern": "verify",
    "exit": 1,
    "stdout": "[error] .claude/skills/verify/SKILL.md: required workflow is missing\n[error] .claude/MAP.md: lists a missing artifact: .claude/skills/verify/SKILL.md\ncheck-instructions (C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1): 2 error(s), 0 warning(s); always-loaded surface about 4762 tokens\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-378",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "structure-missing-fail-closed",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1\\.claude\\scripts\\check-instructions.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": null,
    "expected": "reject",
    "pattern": "onFailure|fail.closed",
    "exit": 1,
    "stdout": "[error] .claude/settings.json: PreToolUse [Bash|PowerShell] hook: policy-critical hook must fail closed (\"onFailure\": \"block\")\n[error] .claude/settings.json: PreToolUse must cover Bash with a valid hook (matcher)\n[error] .claude/settings.json: PreToolUse must cover PowerShell with a valid hook (matcher)\ncheck-instructions (C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1): 3 error(s), 0 warning(s); always-loaded surface about 4849 tokens\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-379",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "structure-missing-selected-module",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1\\.claude\\scripts\\check-instructions.cjs"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": null,
    "expected": "reject",
    "pattern": "module|manifest",
    "exit": 1,
    "stdout": "[error] .claude/capabilities/persistence: required slot has no implementation\n[error] .claude/capabilities/persistence: selected implementation \"ef-core\" has no module directory\n[error] .claude/rules/backend/persistence-technology.md: declares Capability persistence/ef-core, which is not a selected module\n[error] .claude/scripts/facets/persistence-technology.cjs: declares Capability persistence/ef-core, which is not a selected module\n[error] .claude/skills/ef-core/SKILL.md: declares Capability persistence/ef-core, which is not a selected module\n[error] .claude/skills/persistence-change/SKILL.md: declares Capability persistence/ef-core, which is not a selected module\n[error] .claude/MAP.md: lists a missing artifact: .claude/capabilities/persistence/ef-core/MODULE.md\ncheck-instructions (C:\\Users\\atonkonog\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1): 7 error(s), 0 warning(s); always-loaded surface about 4849 tokens\n",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-380",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  },
  {
    "candidate": "K1",
    "test": "stop-recursion-guard",
    "command": [
      "node",
      "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1/.claude/hooks/dispatch.cjs",
      "Stop"
    ],
    "cwd": "C:\\Users\\ATONKO~1\\AppData\\Local\\Temp\\codex_005_final_audit_idsqdoml\\K1",
    "input": "{\"hook_event_name\": \"Stop\", \"tool_name\": \"Bash\", \"cwd\": \"C:\\\\Users\\\\ATONKO~1\\\\AppData\\\\Local\\\\Temp\\\\codex_005_final_audit_idsqdoml\\\\K1\", \"tool_input\": {\"command\": \"echo audit\"}, \"session_id\": \"audit-reconfirmation\", \"stop_hook_active\": true}",
    "expected": "accept",
    "pattern": null,
    "exit": 0,
    "stdout": "",
    "stderr": "",
    "disposition": "PASS",
    "audit_test_id": "T-381",
    "audit_role": "assertion",
    "adjudicated_disposition": "PASS",
    "adjudication": "Observed the intended finite local behavior."
  }
]
```

## Input SHA-256 evidence snapshot and unchanged-after check

For each candidate the tree digest is SHA-256 of UTF-8 bytes of sorted lines `file_sha256 + two spaces + relative_path_from_template_root`, joined by LF with **no final LF**. Paths use forward slashes and case-sensitive lexical sorting; file hashes use raw bytes. It is an audit-defined digest, not necessarily the provenance tool's algorithm. Before and after path/content dictionaries are identical.

| Candidate | Files | Bytes | Before tree digest | After tree digest | Result |
|---|---:|---:|---|---|---|
| M | 61 | 373930 | ffc13d60e0400bee0e0d9c39915730a4791ab04be76444d91f88604e0a23807a | ffc13d60e0400bee0e0d9c39915730a4791ab04be76444d91f88604e0a23807a | UNCHANGED |
| M1 | 80 | 409977 | 84e8ca7ad2f147a091dcd3e37ff4d7e5c6d6b23173d0d3521f6a97bf08d2ae44 | 84e8ca7ad2f147a091dcd3e37ff4d7e5c6d6b23173d0d3521f6a97bf08d2ae44 | UNCHANGED |
| L0 | 71 | 339429 | 931a64d1f3fede560dc2f8995e1073068f7d715d622784846d18fc4ccdddd40d | 931a64d1f3fede560dc2f8995e1073068f7d715d622784846d18fc4ccdddd40d | UNCHANGED |
| L1-Restart | 86 | 349404 | e3a4ea25da60caba094b028e477cc265cf334d7a605798294aba798cae4524f7 | e3a4ea25da60caba094b028e477cc265cf334d7a605798294aba798cae4524f7 | UNCHANGED |
| K0 | 63 | 368812 | d61218dd4657051cc63f3b0838e8f729ab77cb798712c992ee57d26d4f52a4d1 | d61218dd4657051cc63f3b0838e8f729ab77cb798712c992ee57d26d4f52a4d1 | UNCHANGED |
| K1 | 87 | 400934 | d2f3d1ddf8e3e06269e233339463edc07d8072476b601e8a9acfa09091cd0383 | d2f3d1ddf8e3e06269e233339463edc07d8072476b601e8a9acfa09091cd0383 | UNCHANGED |

### Every final-template file: pre-test and post-test SHA-256

| Relative path from exact root | Pre-test SHA-256 | Post-test SHA-256 |
|---|---|---|
| K0/output/template/.claude/MAP.md | 8c5e45a0b34511d92c46ece2d261df2f2bcabdde611310e5f4a4dec970080db6 | 8c5e45a0b34511d92c46ece2d261df2f2bcabdde611310e5f4a4dec970080db6 |
| K0/output/template/.claude/agents/code-reviewer.md | c78e1ac9e06750c04637065d0a96e30d6fcf53c2de63689fccd1e81dad87ed97 | c78e1ac9e06750c04637065d0a96e30d6fcf53c2de63689fccd1e81dad87ed97 |
| K0/output/template/.claude/hooks/hook.cjs | cc6e55c8fdfd5441ce38d48784f713ff4528516a8dc7641ce9a059331420823e | cc6e55c8fdfd5441ce38d48784f713ff4528516a8dc7641ce9a059331420823e |
| K0/output/template/.claude/rules/backend-tests/testing.md | 8a8062be53ce5d104ae5a6bebf732f32c8977963b51ce94c4373102e22f0767d | 8a8062be53ce5d104ae5a6bebf732f32c8977963b51ce94c4373102e22f0767d |
| K0/output/template/.claude/rules/backend/api.md | be4c7b886307d98c8e744c295d23d9571fc6eb0fc1bc421878fdccfe41b5080f | be4c7b886307d98c8e744c295d23d9571fc6eb0fc1bc421878fdccfe41b5080f |
| K0/output/template/.claude/rules/backend/architecture.md | e09b121c3d04289654fd2bffee625966b83d89d1c248393fea8c4d9f7acfd763 | e09b121c3d04289654fd2bffee625966b83d89d1c248393fea8c4d9f7acfd763 |
| K0/output/template/.claude/rules/backend/caching.md | 8ad2ee2332e6965c8727fa157a1e1b20eee8028fdc60e0c915a0cce7a4737f66 | 8ad2ee2332e6965c8727fa157a1e1b20eee8028fdc60e0c915a0cce7a4737f66 |
| K0/output/template/.claude/rules/backend/csharp.md | dcba0a0822b5887bacf88f3b487727d050af521dfea01e214154ae7776a61d68 | dcba0a0822b5887bacf88f3b487727d050af521dfea01e214154ae7776a61d68 |
| K0/output/template/.claude/rules/backend/error-handling.md | 7b176a591d419ce26e01e8d99c4da0b84d6f5435be0cae029c75f94f708f9a0f | 7b176a591d419ce26e01e8d99c4da0b84d6f5435be0cae029c75f94f708f9a0f |
| K0/output/template/.claude/rules/backend/hosting.md | c99da721c13e228b71658aa6da1b44a448045d5c4f5ca392a9ba35eca7bd02c2 | c99da721c13e228b71658aa6da1b44a448045d5c4f5ca392a9ba35eca7bd02c2 |
| K0/output/template/.claude/rules/backend/integrations.md | dfdd1d9b314a82a57a75c5e428a07705a40461eaaa2bff1cc920fbb40e916084 | dfdd1d9b314a82a57a75c5e428a07705a40461eaaa2bff1cc920fbb40e916084 |
| K0/output/template/.claude/rules/backend/persistence.md | 35837f4dde7768ad8c68a542b16852b4b07b34d339718b447bf469954d23bf30 | 35837f4dde7768ad8c68a542b16852b4b07b34d339718b447bf469954d23bf30 |
| K0/output/template/.claude/rules/backend/security.md | 19f28614e474cb1b961718e45cc76ee2164087a2bf8576bd262f2e3841760620 | 19f28614e474cb1b961718e45cc76ee2164087a2bf8576bd262f2e3841760620 |
| K0/output/template/.claude/rules/common/dependencies.md | 34b08f489889fea3b672b68a9039d57b6c8c539b212ceb52c34a0778685f75e1 | 34b08f489889fea3b672b68a9039d57b6c8c539b212ceb52c34a0778685f75e1 |
| K0/output/template/.claude/rules/common/repository-layout.md | cbe872566373073e8344878d8fe7e06f6b57049d91ff4bce0d661a7535635ff8 | cbe872566373073e8344878d8fe7e06f6b57049d91ff4bce0d661a7535635ff8 |
| K0/output/template/.claude/rules/common/security.md | 91aed513479d08f6c8ee1eb402d585d89f7965d89178a95b8fdc5dc5b25af355 | 91aed513479d08f6c8ee1eb402d585d89f7965d89178a95b8fdc5dc5b25af355 |
| K0/output/template/.claude/rules/frontend/angular.md | c664ecc6616329fc1cf0fe396e6606eb39ebec1b5854cf9e26963f8cdbe8e603 | c664ecc6616329fc1cf0fe396e6606eb39ebec1b5854cf9e26963f8cdbe8e603 |
| K0/output/template/.claude/scripts/check-dependencies.cjs | 2a14aa061c2daf224843190038869f58610824a953b362dd8b2ab1aa37be7942 | 2a14aa061c2daf224843190038869f58610824a953b362dd8b2ab1aa37be7942 |
| K0/output/template/.claude/scripts/check-instructions.cjs | d7a4aff736b8fa4bd68a0515e1d245ea544d8c8c36122b44ed7682c1d6729f04 | d7a4aff736b8fa4bd68a0515e1d245ea544d8c8c36122b44ed7682c1d6729f04 |
| K0/output/template/.claude/scripts/repo.cjs | 11c569f44caa8764ef791d778d537537f309b8b6d566e346a1d14ca17a06f811 | 11c569f44caa8764ef791d778d537537f309b8b6d566e346a1d14ca17a06f811 |
| K0/output/template/.claude/settings.json | ed7639b7962dc821086a8a6710b7496045338485b199110843dffad81d113720 | ed7639b7962dc821086a8a6710b7496045338485b199110843dffad81d113720 |
| K0/output/template/.claude/skills/add-dependency/SKILL.md | 0a392404f0c09a1bf81e38ebad01dbd8fe6ea555e9138ce538ae21fc5c874317 | 0a392404f0c09a1bf81e38ebad01dbd8fe6ea555e9138ce538ae21fc5c874317 |
| K0/output/template/.claude/skills/angular/SKILL.md | 33f712ffbb5d91abf1543ca1158eab923da0a3fa7d41adf156e87f9cb53bec9f | 33f712ffbb5d91abf1543ca1158eab923da0a3fa7d41adf156e87f9cb53bec9f |
| K0/output/template/.claude/skills/api-versioning/SKILL.md | bd3dcf58b745785edbf12de195063c8223852f97f2b36997017eed9d0fa31072 | bd3dcf58b745785edbf12de195063c8223852f97f2b36997017eed9d0fa31072 |
| K0/output/template/.claude/skills/architecture-decision/SKILL.md | efbccf6ad19b5eadae0c887ec6c77ec00d886a159899480abf649ca5bbea47f7 | efbccf6ad19b5eadae0c887ec6c77ec00d886a159899480abf649ca5bbea47f7 |
| K0/output/template/.claude/skills/aspnet-error-handling/SKILL.md | 4e8e206f402218763ae350144cb974909a2e7a8616c331e640eabd6156e4c105 | 4e8e206f402218763ae350144cb974909a2e7a8616c331e640eabd6156e4c105 |
| K0/output/template/.claude/skills/authentication/SKILL.md | 023a0a3a4ad91b52988903accc724c685be2348c6631f2ce8f348e64216d962d | 023a0a3a4ad91b52988903accc724c685be2348c6631f2ce8f348e64216d962d |
| K0/output/template/.claude/skills/build-fix/SKILL.md | f72dc4805915821dcbf5f28ce2f962e3b49c1962aae4659f6dbf85a3084dfb8a | f72dc4805915821dcbf5f28ce2f962e3b49c1962aae4659f6dbf85a3084dfb8a |
| K0/output/template/.claude/skills/caching/SKILL.md | 65977cb233201030e7b9a6f349ac6c6dc643059b964c994e5666a8ba1dada3bf | 65977cb233201030e7b9a6f349ac6c6dc643059b964c994e5666a8ba1dada3bf |
| K0/output/template/.claude/skills/ci-cd/SKILL.md | 77c684877211e7960a639de18a0a1b7f7e89b21aee71c53d93013df45a11597c | 77c684877211e7960a639de18a0a1b7f7e89b21aee71c53d93013df45a11597c |
| K0/output/template/.claude/skills/code-review/SKILL.md | fdbc5374a5df9419eaf03a7f3a885b561dda92cc07cd72a53cf2f6603bfabb3b | fdbc5374a5df9419eaf03a7f3a885b561dda92cc07cd72a53cf2f6603bfabb3b |
| K0/output/template/.claude/skills/configuration/SKILL.md | a548368fbd93b5207ac66ea20cb9a916bbbcbefa3452a3aa17881e486271faa0 | a548368fbd93b5207ac66ea20cb9a916bbbcbefa3452a3aa17881e486271faa0 |
| K0/output/template/.claude/skills/custom-settings/SKILL.md | b4ca7e591bcfa571485d248f255ac8294c604ccb6491774239b1d583107bd9fb | b4ca7e591bcfa571485d248f255ac8294c604ccb6491774239b1d583107bd9fb |
| K0/output/template/.claude/skills/delivery-pipeline/SKILL.md | c5285298fc92ca053136ab82dcddb966d3538e59b5f1e554fd8629cb05ff7cf7 | c5285298fc92ca053136ab82dcddb966d3538e59b5f1e554fd8629cb05ff7cf7 |
| K0/output/template/.claude/skills/dependency-injection/SKILL.md | 866d94ad46019256d47ec2f101254a825ab22b435fabf0ff2f06c373a76e8425 | 866d94ad46019256d47ec2f101254a825ab22b435fabf0ff2f06c373a76e8425 |
| K0/output/template/.claude/skills/development-workflow/SKILL.md | 70296b7f863b17e6799cbf470099c32fb4e830dbb8b86359c2468d857facda0c | 70296b7f863b17e6799cbf470099c32fb4e830dbb8b86359c2468d857facda0c |
| K0/output/template/.claude/skills/docker/SKILL.md | 69de5d7d2eec1af6c489c4153dc97f5d5d43b2da7e1568cb8f4c6bc4b1706813 | 69de5d7d2eec1af6c489c4153dc97f5d5d43b2da7e1568cb8f4c6bc4b1706813 |
| K0/output/template/.claude/skills/dotnet-testing/SKILL.md | ff4ffec0b939b205ef0484d270afdf05c89698400074728e1159c65e91bd1a2d | ff4ffec0b939b205ef0484d270afdf05c89698400074728e1159c65e91bd1a2d |
| K0/output/template/.claude/skills/ef-core/SKILL.md | c975ff56339201b90745f005eb15d8e9c4cdd44a4655b40bf96b9109dc6bab46 | c975ff56339201b90745f005eb15d8e9c4cdd44a4655b40bf96b9109dc6bab46 |
| K0/output/template/.claude/skills/git-workflow/SKILL.md | 362a567d5310086364ca3f34b4f14d548b259f738797be3b96bdc1be592472eb | 362a567d5310086364ca3f34b4f14d548b259f738797be3b96bdc1be592472eb |
| K0/output/template/.claude/skills/health-check/SKILL.md | ea8bc3874aaffcf58843a04480cf0ae3a0ca332305a2764a698b782556408d8b | ea8bc3874aaffcf58843a04480cf0ae3a0ca332305a2764a698b782556408d8b |
| K0/output/template/.claude/skills/http-api/SKILL.md | 4be88938366ec54bf5911ec40338a421949bde8633f98775f7c7ae53099b41a8 | 4be88938366ec54bf5911ec40338a421949bde8633f98775f7c7ae53099b41a8 |
| K0/output/template/.claude/skills/httpclient-factory/SKILL.md | 9a21b8c49fd831801bb77501d7bfa812141d6a36d90cb5df494e193e1beb9d39 | 9a21b8c49fd831801bb77501d7bfa812141d6a36d90cb5df494e193e1beb9d39 |
| K0/output/template/.claude/skills/httpclient-factory/references/resilience.md | e873e277aa33910a20864b3117e11a9f9c5005614a7fc2bc6f41a86e3fed6396 | e873e277aa33910a20864b3117e11a9f9c5005614a7fc2bc6f41a86e3fed6396 |
| K0/output/template/.claude/skills/logging/SKILL.md | 2adb1179da408f61d35380765d7dea69545e95b4a787c22cbe3cea3fc2eb5249 | 2adb1179da408f61d35380765d7dea69545e95b4a787c22cbe3cea3fc2eb5249 |
| K0/output/template/.claude/skills/logging/references/serilog.md | 56b75576d6317ef43a14503eee872e96e70de2058cba4ddc60c6a2a1806a5060 | 56b75576d6317ef43a14503eee872e96e70de2058cba4ddc60c6a2a1806a5060 |
| K0/output/template/.claude/skills/modern-csharp/SKILL.md | 285a7f4df64706f4b18cc9c8b176492709b4a24d6c2767a1135c85a9ea8714d5 | 285a7f4df64706f4b18cc9c8b176492709b4a24d6c2767a1135c85a9ea8714d5 |
| K0/output/template/.claude/skills/project-structure/SKILL.md | 4e0b785e904db988382b406838c2e8b48f3e652d25fbd6fbee25f08747ed57fb | 4e0b785e904db988382b406838c2e8b48f3e652d25fbd6fbee25f08747ed57fb |
| K0/output/template/.claude/skills/project-structure/references/backend-layout.md | f03b377d54b55cfa70130fa9186dd30d9679802f4ea886326b3192eddf022097 | f03b377d54b55cfa70130fa9186dd30d9679802f4ea886326b3192eddf022097 |
| K0/output/template/.claude/skills/project-structure/references/baseline-setup.md | 4baa78d3571dcb6e54b1acd1784de7a624aeb84735980d0a465a775a5850cc57 | 4baa78d3571dcb6e54b1acd1784de7a624aeb84735980d0a465a775a5850cc57 |
| K0/output/template/.claude/skills/project-structure/references/solution-layout.md | 9bed7bd2b78663f45796f03e94e56e47d1c4a153faf4cf626ff3d165cf551fed | 9bed7bd2b78663f45796f03e94e56e47d1c4a153faf4cf626ff3d165cf551fed |
| K0/output/template/.claude/skills/security-scan/SKILL.md | e11ca33e4a17daa3fd2d580d520c352e691a1d98af4a009cecee8cd29cc40cdc | e11ca33e4a17daa3fd2d580d520c352e691a1d98af4a009cecee8cd29cc40cdc |
| K0/output/template/.claude/skills/security-scan/references/scan-layers.md | 57941e94fb8f2ac9ed1a24f5b5c73960a08f40b3628b54119c869f3d9d0e66dc | 57941e94fb8f2ac9ed1a24f5b5c73960a08f40b3628b54119c869f3d9d0e66dc |
| K0/output/template/.claude/skills/swagger/SKILL.md | 072cc822bc468391ccc8ce7fc59d63bcb926c33f90b66ba5a2df5d6f36b1acc1 | 072cc822bc468391ccc8ce7fc59d63bcb926c33f90b66ba5a2df5d6f36b1acc1 |
| K0/output/template/.claude/skills/template-maintenance/SKILL.md | ef13f879409884f24a464a926643edbf6408b0e408b57b1bc66938d0d59c30bb | ef13f879409884f24a464a926643edbf6408b0e408b57b1bc66938d0d59c30bb |
| K0/output/template/.claude/skills/verify/SKILL.md | 2df6184c5971f3797c97f5de8e06b346fb50f91aa64305ed925c1271024a614a | 2df6184c5971f3797c97f5de8e06b346fb50f91aa64305ed925c1271024a614a |
| K0/output/template/.editorconfig | 58d1eabb6c60b3b25999fabeef0ccbecffdc8b568f23c7f80733b06c2e2d2153 | 58d1eabb6c60b3b25999fabeef0ccbecffdc8b568f23c7f80733b06c2e2d2153 |
| K0/output/template/CLAUDE.md | a210661eb34f54fad1d064c9f1f8d86ec342a6be91f92a4e1b2e5e93fce0cc3b | a210661eb34f54fad1d064c9f1f8d86ec342a6be91f92a4e1b2e5e93fce0cc3b |
| K0/output/template/CUSTOM_SETTINGS.md | 5f6dee2f15e57e922d58b5b52ec1ce4e30f681e4e81da970fb46c2a7107a5838 | 5f6dee2f15e57e922d58b5b52ec1ce4e30f681e4e81da970fb46c2a7107a5838 |
| K0/output/template/Directory.Build.props | c448845ef17ff53b2107c2eaa498b5e2017b642ddabffe17429f8588a237c5b3 | c448845ef17ff53b2107c2eaa498b5e2017b642ddabffe17429f8588a237c5b3 |
| K0/output/template/Directory.Packages.props | 493f64de0e0b154ea64bb049ecf9dc988ec3f3fa985809b675656de20f8c6277 | 493f64de0e0b154ea64bb049ecf9dc988ec3f3fa985809b675656de20f8c6277 |
| K0/output/template/SPECIFICATION.md | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| K0/output/template/docs/architecture/decision-register.md | 79f006ddfb6605c602d434241ebb103192480ac3359ada2efc83061744480ead | 79f006ddfb6605c602d434241ebb103192480ac3359ada2efc83061744480ead |
| K1/output/template/.claude/MAP.md | 5817b2cb9d1115200a8d5b052a284d644c368ab1f570e6c99f43a8b554dd1482 | 5817b2cb9d1115200a8d5b052a284d644c368ab1f570e6c99f43a8b554dd1482 |
| K1/output/template/.claude/agents/code-reviewer.md | 544833c89c6712072817c7534997008124720e00abe0f00207384bce38042422 | 544833c89c6712072817c7534997008124720e00abe0f00207384bce38042422 |
| K1/output/template/.claude/capabilities/architecture/CONTRACT.md | cf9bb59bdeb4a7a9ee3177ef85a6175f18b4e2b7a1591b9377cde0bbe3338693 | cf9bb59bdeb4a7a9ee3177ef85a6175f18b4e2b7a1591b9377cde0bbe3338693 |
| K1/output/template/.claude/capabilities/architecture/clean-architecture/MODULE.md | 93f7083cd139238a7fc3bbe813944dbb998b7137ba8c61e934b7079f465fb722 | 93f7083cd139238a7fc3bbe813944dbb998b7137ba8c61e934b7079f465fb722 |
| K1/output/template/.claude/capabilities/backend-testing/CONTRACT.md | 2bfd693689adb1a0a2c1027fac64d1bf1947de7fdc2bee53692b8515c2623dfb | 2bfd693689adb1a0a2c1027fac64d1bf1947de7fdc2bee53692b8515c2623dfb |
| K1/output/template/.claude/capabilities/backend-testing/nunit/MODULE.md | a255335ba10f7fed5c095af87b2c6f6829f5b5c2108cf1de6c6ff5caaf37152e | a255335ba10f7fed5c095af87b2c6f6829f5b5c2108cf1de6c6ff5caaf37152e |
| K1/output/template/.claude/capabilities/frontend/CONTRACT.md | fe028befbda3b8f7fd29513c219f00393eab445e8077a953a870d1b9f7672c94 | fe028befbda3b8f7fd29513c219f00393eab445e8077a953a870d1b9f7672c94 |
| K1/output/template/.claude/capabilities/frontend/angular/MODULE.md | 959a4bad64808e3dafb14d7336ab0e2b391f7d7876b4889de022a10b226c051e | 959a4bad64808e3dafb14d7336ab0e2b391f7d7876b4889de022a10b226c051e |
| K1/output/template/.claude/capabilities/persistence/CONTRACT.md | 17bc8ae5486df1b3b794d5b77f5c4f773772bdd373d583ac418d8cc31dd68b92 | 17bc8ae5486df1b3b794d5b77f5c4f773772bdd373d583ac418d8cc31dd68b92 |
| K1/output/template/.claude/capabilities/persistence/ef-core/MODULE.md | 491e121169300dc62d07c95d560358bcd71fe654d1b478a24c82e377cbc1a0cf | 491e121169300dc62d07c95d560358bcd71fe654d1b478a24c82e377cbc1a0cf |
| K1/output/template/.claude/hooks/dispatch.cjs | ba3a55b650180e6e51d3ce0a2f5bf0ee6b4f76f9f1123a9dc3a1eaba5cd38d22 | ba3a55b650180e6e51d3ce0a2f5bf0ee6b4f76f9f1123a9dc3a1eaba5cd38d22 |
| K1/output/template/.claude/rules/backend-tests/test-framework.md | f061f818c113eb4c672dcda24b005f7bdbde8414945267dbb00e3b96dbfb33f2 | f061f818c113eb4c672dcda24b005f7bdbde8414945267dbb00e3b96dbfb33f2 |
| K1/output/template/.claude/rules/backend-tests/test-projects.md | c394e7828811a5df74fda62dc8c513e584789dade57ccf08310eb5a1d1ffe0f1 | c394e7828811a5df74fda62dc8c513e584789dade57ccf08310eb5a1d1ffe0f1 |
| K1/output/template/.claude/rules/backend-tests/testing.md | ed789af1525207c589966a34327bba21e312dc0c7ceac347e3a45d504136c1e2 | ed789af1525207c589966a34327bba21e312dc0c7ceac347e3a45d504136c1e2 |
| K1/output/template/.claude/rules/backend/api-contracts.md | a5926375911d2e42d8362d7f13cfcbfa0f81c3364efc1fdebd929946db113ff2 | a5926375911d2e42d8362d7f13cfcbfa0f81c3364efc1fdebd929946db113ff2 |
| K1/output/template/.claude/rules/backend/api.md | 4f6b10c8fc6181c62ac794814cf7601cce9c8b298f322c2912b074788556df12 | 4f6b10c8fc6181c62ac794814cf7601cce9c8b298f322c2912b074788556df12 |
| K1/output/template/.claude/rules/backend/architecture-style.md | 1358a000e71b0a2347c6df7383761bfe0f515e8cb196fa6bd9e318ae6d5785bb | 1358a000e71b0a2347c6df7383761bfe0f515e8cb196fa6bd9e318ae6d5785bb |
| K1/output/template/.claude/rules/backend/architecture.md | 59f1f9b7196b2417630f3dd05c27b61ea6acf3d7c85032075acf9cbe35274222 | 59f1f9b7196b2417630f3dd05c27b61ea6acf3d7c85032075acf9cbe35274222 |
| K1/output/template/.claude/rules/backend/coding-style.md | ab3fb616843394de10f9ec5d642cc6c2206484f6081a96d7963a9ff3f9ed60ec | ab3fb616843394de10f9ec5d642cc6c2206484f6081a96d7963a9ff3f9ed60ec |
| K1/output/template/.claude/rules/backend/dependencies.md | 562c5a810a11fdfb3abf9bb719fff08f870e5d8fc2e7a54ca0bd4195677c26e7 | 562c5a810a11fdfb3abf9bb719fff08f870e5d8fc2e7a54ca0bd4195677c26e7 |
| K1/output/template/.claude/rules/backend/operations.md | df64a1b16be637442fe8e95a6821f86224ac0a1d75bfcaf0d5ccd5059d9f4642 | df64a1b16be637442fe8e95a6821f86224ac0a1d75bfcaf0d5ccd5059d9f4642 |
| K1/output/template/.claude/rules/backend/persistence-technology.md | 3a726fb0503cf2ba8319534c80e28a411118d39f0b65e37f503ee525ffc014a6 | 3a726fb0503cf2ba8319534c80e28a411118d39f0b65e37f503ee525ffc014a6 |
| K1/output/template/.claude/rules/backend/persistence.md | e322f1314d2e6e74645f2cb93b342bc816ce54b53b7f82e65875e95f68e650ea | e322f1314d2e6e74645f2cb93b342bc816ce54b53b7f82e65875e95f68e650ea |
| K1/output/template/.claude/rules/backend/runtime.md | aaf983b678b1e7c88dab5eac278e1047bc22818b79ddd696ec69694e16fe9a68 | aaf983b678b1e7c88dab5eac278e1047bc22818b79ddd696ec69694e16fe9a68 |
| K1/output/template/.claude/rules/backend/security.md | 15c3d7fe07cf7948924bf29366d02d0fe839a4ab31f0f6d2b04082c4fd696ffa | 15c3d7fe07cf7948924bf29366d02d0fe839a4ab31f0f6d2b04082c4fd696ffa |
| K1/output/template/.claude/rules/common/dependencies.md | 16a4128dd73bfe7112b213926c11f68e1d9aa97a2cb6d86c4b2601cd9307db66 | 16a4128dd73bfe7112b213926c11f68e1d9aa97a2cb6d86c4b2601cd9307db66 |
| K1/output/template/.claude/rules/common/security.md | 4918a6023126242d929e270643a38611a0c0137442272130e5a61c8b955caac4 | 4918a6023126242d929e270643a38611a0c0137442272130e5a61c8b955caac4 |
| K1/output/template/.claude/rules/common/structure.md | d762a066d7c925bb74a49c3cd99b01ceb8283fda51b1986056fb40a8d856179a | d762a066d7c925bb74a49c3cd99b01ceb8283fda51b1986056fb40a8d856179a |
| K1/output/template/.claude/rules/frontend/dependencies.md | b44f0596bdc385caa331a9e205b61410a18582422579e12ec9128dc1d21e78ea | b44f0596bdc385caa331a9e205b61410a18582422579e12ec9128dc1d21e78ea |
| K1/output/template/.claude/rules/frontend/frontend-framework.md | ce2121143313d3d2127abc9ae0b6b96377b04dbf71069d01a46f5504fc6cefef | ce2121143313d3d2127abc9ae0b6b96377b04dbf71069d01a46f5504fc6cefef |
| K1/output/template/.claude/rules/frontend/frontend.md | baa9ca5612c76a9631114778e8240daa4f9a764d2cb05ac3ce5248893a513794 | baa9ca5612c76a9631114778e8240daa4f9a764d2cb05ac3ce5248893a513794 |
| K1/output/template/.claude/rules/frontend/security.md | 32e66cab4308930da8daff640447305d169e367bcb5e2e8ed7c7f2a1998ea577 | 32e66cab4308930da8daff640447305d169e367bcb5e2e8ed7c7f2a1998ea577 |
| K1/output/template/.claude/scripts/actual-state.cjs | 5138e905d8a18191c8ab6a30759dc8010ba60e10788a604fc64f090f5ff6545a | 5138e905d8a18191c8ab6a30759dc8010ba60e10788a604fc64f090f5ff6545a |
| K1/output/template/.claude/scripts/check-cochange.cjs | 7e0d664b43bdd71c7eb88dd327a94fa63d8c4f088bd2daefbf84f16c5b46c0d8 | 7e0d664b43bdd71c7eb88dd327a94fa63d8c4f088bd2daefbf84f16c5b46c0d8 |
| K1/output/template/.claude/scripts/check-instructions.cjs | a22c9c305f581111bcc077e4ae49016c3054e320443abd05f282ab79d29fe938 | a22c9c305f581111bcc077e4ae49016c3054e320443abd05f282ab79d29fe938 |
| K1/output/template/.claude/scripts/check-manifests.cjs | 1d704db02381c6ce9c0dd28717131f5d46f73dcb45c8ef2bdf9252381eb9a0be | 1d704db02381c6ce9c0dd28717131f5d46f73dcb45c8ef2bdf9252381eb9a0be |
| K1/output/template/.claude/scripts/classify-command.cjs | c46a12ee7a0187eb5089e2fb81df871d337b557b282052cfd840eb90b7044e85 | c46a12ee7a0187eb5089e2fb81df871d337b557b282052cfd840eb90b7044e85 |
| K1/output/template/.claude/scripts/facets/architecture-style.cjs | e1f88a4d7d52b2ff95e064ca3c002363cd55c7d920c9443d8e4573cfaa6cdbe0 | e1f88a4d7d52b2ff95e064ca3c002363cd55c7d920c9443d8e4573cfaa6cdbe0 |
| K1/output/template/.claude/scripts/facets/frontend-framework.cjs | 972ea90faaa2dcd7f581b46d53a4a91b5ccf0bbf813e02febad1bad24c3a78cf | 972ea90faaa2dcd7f581b46d53a4a91b5ccf0bbf813e02febad1bad24c3a78cf |
| K1/output/template/.claude/scripts/facets/persistence-technology.cjs | 13a101eb46f845d8bbc4716a25b851d48c4c5941c00f856095929384ea7660a5 | 13a101eb46f845d8bbc4716a25b851d48c4c5941c00f856095929384ea7660a5 |
| K1/output/template/.claude/scripts/facets/test-framework.cjs | 2a6c4eb4603af3fc1bb6961675a9ca2dc9ab06a037a05616d7a62aa9d03996eb | 2a6c4eb4603af3fc1bb6961675a9ca2dc9ab06a037a05616d7a62aa9d03996eb |
| K1/output/template/.claude/scripts/lib.cjs | f83639458289c5c58531127d3f69c8797949fe1a0f371dcd5eca79daf4e57e0e | f83639458289c5c58531127d3f69c8797949fe1a0f371dcd5eca79daf4e57e0e |
| K1/output/template/.claude/settings.json | 41a9dbde4147ecf501d7301b1e47b4610e0150b57caf1adcd99816998b87edf4 | 41a9dbde4147ecf501d7301b1e47b4610e0150b57caf1adcd99816998b87edf4 |
| K1/output/template/.claude/skills/add-dependency/SKILL.md | e7f46e6f2e559553dd4307def833e172fc40b3fa7847263667624d947176cfc0 | e7f46e6f2e559553dd4307def833e172fc40b3fa7847263667624d947176cfc0 |
| K1/output/template/.claude/skills/angular/SKILL.md | db066240e9cc0b10c671d9ff54464f9efccb58ca64ee9ec3c118767d5b7c31ff | db066240e9cc0b10c671d9ff54464f9efccb58ca64ee9ec3c118767d5b7c31ff |
| K1/output/template/.claude/skills/api-versioning/SKILL.md | a627c3b6b349c4996c7b2b0d917e0f8affe6eef35836662b870a409e7b1c1388 | a627c3b6b349c4996c7b2b0d917e0f8affe6eef35836662b870a409e7b1c1388 |
| K1/output/template/.claude/skills/architecture-decision/SKILL.md | 53f9ed14597b24078b62a0d7aa2184e23a942b65a10292cbd769d5a7832edb68 | 53f9ed14597b24078b62a0d7aa2184e23a942b65a10292cbd769d5a7832edb68 |
| K1/output/template/.claude/skills/aspnet-error-handling/SKILL.md | 99734c4095dac007d827ef805a23ccc8550931cbaee9acb4f8c4a31eebfa9a97 | 99734c4095dac007d827ef805a23ccc8550931cbaee9acb4f8c4a31eebfa9a97 |
| K1/output/template/.claude/skills/authentication/SKILL.md | 52dad0ef32dc17d1bbbb651ec2966e8c99469ae3c00d285826207a52067d11ea | 52dad0ef32dc17d1bbbb651ec2966e8c99469ae3c00d285826207a52067d11ea |
| K1/output/template/.claude/skills/build-fix/SKILL.md | 597720aa4c56a6d54054a4a520d45cc5ed23860934c6e6953e16106f45c46ed2 | 597720aa4c56a6d54054a4a520d45cc5ed23860934c6e6953e16106f45c46ed2 |
| K1/output/template/.claude/skills/caching/SKILL.md | 67472d53c196a4cc943aeade54326d85f60af9b7debc76f16f864040d0098298 | 67472d53c196a4cc943aeade54326d85f60af9b7debc76f16f864040d0098298 |
| K1/output/template/.claude/skills/ci-cd/SKILL.md | 2b7c07ebb283c3ec3d5b0a2fa03533c0e8b676613ac3dea9255626448128e0b7 | 2b7c07ebb283c3ec3d5b0a2fa03533c0e8b676613ac3dea9255626448128e0b7 |
| K1/output/template/.claude/skills/code-review/SKILL.md | ac5781aa16fdc364c2aaf5a509c12c34c3aed01ed672822735f6e426dbd3f1ee | ac5781aa16fdc364c2aaf5a509c12c34c3aed01ed672822735f6e426dbd3f1ee |
| K1/output/template/.claude/skills/configuration/SKILL.md | 9e76fee882da3f35b08bc184e82332fe637ba44fe85673af5922800e8ca5d447 | 9e76fee882da3f35b08bc184e82332fe637ba44fe85673af5922800e8ca5d447 |
| K1/output/template/.claude/skills/custom-settings/SKILL.md | 7f77d4d424158664ed03e2b59275da804138015ae5abd5fcbaf7e7c95f5c4058 | 7f77d4d424158664ed03e2b59275da804138015ae5abd5fcbaf7e7c95f5c4058 |
| K1/output/template/.claude/skills/delivery-change/SKILL.md | 65272c6960340d9665b3deec732badf947f186ef3dcdbc69bd1bf48dd4570600 | 65272c6960340d9665b3deec732badf947f186ef3dcdbc69bd1bf48dd4570600 |
| K1/output/template/.claude/skills/dependency-injection/SKILL.md | 35017a68932438479749e126ed5d512a913fe48c53f5a0d7eda7988b0b43991f | 35017a68932438479749e126ed5d512a913fe48c53f5a0d7eda7988b0b43991f |
| K1/output/template/.claude/skills/development-workflow/SKILL.md | b04fd900abd6833439c95735ea0d0df1f2009f4ca4f2b1ca25a0c56c351dd4e2 | b04fd900abd6833439c95735ea0d0df1f2009f4ca4f2b1ca25a0c56c351dd4e2 |
| K1/output/template/.claude/skills/docker/SKILL.md | 86ecdc73f9bcbe8fd7c25e7a25a4dbe371f87936f88299cd8981dd578d881190 | 86ecdc73f9bcbe8fd7c25e7a25a4dbe371f87936f88299cd8981dd578d881190 |
| K1/output/template/.claude/skills/dotnet-testing/SKILL.md | 7230bfc2d8fed8966f198c1c2903394db5da91adcffc4d1190308ff309756969 | 7230bfc2d8fed8966f198c1c2903394db5da91adcffc4d1190308ff309756969 |
| K1/output/template/.claude/skills/ef-core/SKILL.md | a5d5bc1b229c1362de522c9d53ab81c4b1b800f8a080543a855178ebdb889f9a | a5d5bc1b229c1362de522c9d53ab81c4b1b800f8a080543a855178ebdb889f9a |
| K1/output/template/.claude/skills/git-workflow/SKILL.md | 12ca8b91a726ccb6e63e780ba0c214a237603638bc4d9a309e6db747bce28b2a | 12ca8b91a726ccb6e63e780ba0c214a237603638bc4d9a309e6db747bce28b2a |
| K1/output/template/.claude/skills/health-check/SKILL.md | e4706562d402c140de7a7d23fa223bb8cf5a835c80ee5c6753af0f17e08577fc | e4706562d402c140de7a7d23fa223bb8cf5a835c80ee5c6753af0f17e08577fc |
| K1/output/template/.claude/skills/http-api/SKILL.md | fa5bf4fdcb5453aba3fd1952ccec215637dce6ce16251a1ec062b9b03072561c | fa5bf4fdcb5453aba3fd1952ccec215637dce6ce16251a1ec062b9b03072561c |
| K1/output/template/.claude/skills/httpclient-factory/SKILL.md | 62204b98e58bc367d888490692c58445a26d47cfc7274cbc9cb390ec6cba002b | 62204b98e58bc367d888490692c58445a26d47cfc7274cbc9cb390ec6cba002b |
| K1/output/template/.claude/skills/httpclient-factory/references/resilience.md | ae1838108151e5b64897eaef05d02ef6f8b0d282dd8c324007ea9781d3f3c591 | ae1838108151e5b64897eaef05d02ef6f8b0d282dd8c324007ea9781d3f3c591 |
| K1/output/template/.claude/skills/logging/SKILL.md | b11e717b5e1fabd883e2866a0940e91532a2c4bbb4ec9051eb161d47cc357fcf | b11e717b5e1fabd883e2866a0940e91532a2c4bbb4ec9051eb161d47cc357fcf |
| K1/output/template/.claude/skills/logging/references/serilog.md | 18b915b257108f315777db09744f7d9547794dfd5bd778321e65ef622f48d266 | 18b915b257108f315777db09744f7d9547794dfd5bd778321e65ef622f48d266 |
| K1/output/template/.claude/skills/modern-csharp/SKILL.md | d30ebb31c297c9e90ba278783e161107f1776823f38b61b1b84bfc1b2c0c47cb | d30ebb31c297c9e90ba278783e161107f1776823f38b61b1b84bfc1b2c0c47cb |
| K1/output/template/.claude/skills/persistence-change/SKILL.md | 7ef7ec479115061b959a67ff222b20486f3bd833f514aaf15669d5730284d455 | 7ef7ec479115061b959a67ff222b20486f3bd833f514aaf15669d5730284d455 |
| K1/output/template/.claude/skills/project-structure/SKILL.md | 0e464d3e4adef166c05a02cfb5e13f1d9712bf7a021fdf7702c2a62595c06dd5 | 0e464d3e4adef166c05a02cfb5e13f1d9712bf7a021fdf7702c2a62595c06dd5 |
| K1/output/template/.claude/skills/project-structure/references/backend-layout.md | dbfac63650a6b2a08f1bcaebc45248495cb45c2475fb58ba3bb90cacfb9bc715 | dbfac63650a6b2a08f1bcaebc45248495cb45c2475fb58ba3bb90cacfb9bc715 |
| K1/output/template/.claude/skills/project-structure/references/frontend-setup.md | b3c97fa173fc743b53ab230474a71277113ef05e09b9418f7a364bd0fd02ded9 | b3c97fa173fc743b53ab230474a71277113ef05e09b9418f7a364bd0fd02ded9 |
| K1/output/template/.claude/skills/project-structure/references/solution-layout.md | 08bfc50ad77a9685a150ec97f61f3654738b1aea75a6de8678d4c2fd5a652cac | 08bfc50ad77a9685a150ec97f61f3654738b1aea75a6de8678d4c2fd5a652cac |
| K1/output/template/.claude/skills/project-structure/references/test-setup.md | 1aa042862acae68b10f1e571e53dfb4374a59381cd9493cd7d94633610f735b7 | 1aa042862acae68b10f1e571e53dfb4374a59381cd9493cd7d94633610f735b7 |
| K1/output/template/.claude/skills/security-scan/SKILL.md | ea48b84d788cf905b1c0f149c6c121caac8d37bb1df3e3f492d07fb00fc3d200 | ea48b84d788cf905b1c0f149c6c121caac8d37bb1df3e3f492d07fb00fc3d200 |
| K1/output/template/.claude/skills/security-scan/references/scan-layers.md | e43b42b6459244caef00f781f7f4ae1c2abd0b5b54c2a881a2124fa2be468204 | e43b42b6459244caef00f781f7f4ae1c2abd0b5b54c2a881a2124fa2be468204 |
| K1/output/template/.claude/skills/swagger/SKILL.md | 55a1e6d71911b38dd0d655c817e2e18456cabdf226298e849398dc4557c9f3bd | 55a1e6d71911b38dd0d655c817e2e18456cabdf226298e849398dc4557c9f3bd |
| K1/output/template/.claude/skills/template-maintenance/SKILL.md | e1f32c99b11d137cd8369e0144e1ffa66458e33d1891766869b6be4049cda960 | e1f32c99b11d137cd8369e0144e1ffa66458e33d1891766869b6be4049cda960 |
| K1/output/template/.claude/skills/verify/SKILL.md | 00976f54c6b3c9493a45bc1d4ed40e271966e3a5e90c8d9045be69ce18596a33 | 00976f54c6b3c9493a45bc1d4ed40e271966e3a5e90c8d9045be69ce18596a33 |
| K1/output/template/.editorconfig | 1d44e455282293d11830f344a5d5a4f44777aefac160b19733a953118df1aedc | 1d44e455282293d11830f344a5d5a4f44777aefac160b19733a953118df1aedc |
| K1/output/template/CLAUDE.md | 33735cc8bf3a1f35f2119ccbaf8e6dc24b38e562bb8306d72f0450d43836ce71 | 33735cc8bf3a1f35f2119ccbaf8e6dc24b38e562bb8306d72f0450d43836ce71 |
| K1/output/template/CUSTOM_SETTINGS.md | 2e710c2f3e56a5aea99123e9454b2a30be470836c06847a965524eef9ba558c7 | 2e710c2f3e56a5aea99123e9454b2a30be470836c06847a965524eef9ba558c7 |
| K1/output/template/Directory.Build.props | c89b1f606e040670343733aa340350d8ca547399a696f47eb5e27c9217e40fb8 | c89b1f606e040670343733aa340350d8ca547399a696f47eb5e27c9217e40fb8 |
| K1/output/template/Directory.Packages.props | 877468e119a942899a24a8470f6c613d21c410697c45bf47a486261076c3c3c6 | 877468e119a942899a24a8470f6c613d21c410697c45bf47a486261076c3c3c6 |
| K1/output/template/SPECIFICATION.md | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| K1/output/template/docs/architecture/decision-register.md | 0d6a0def897b4bd4c45bc54657a3a620a71a6ea7d12f10119d694354c3dc9896 | 0d6a0def897b4bd4c45bc54657a3a620a71a6ea7d12f10119d694354c3dc9896 |
| L0/output/template/.claude/INSTRUCTION_MAP.md | f9d3c6fce26cba3e21211cba468677347fee34156bba8b6e1a10b50731959a10 | f9d3c6fce26cba3e21211cba468677347fee34156bba8b6e1a10b50731959a10 |
| L0/output/template/.claude/agents/code-reviewer.md | fb3eb0122818177bfae83cb1499fcb7874bdea05be64963c2290b3a0596f80ad | fb3eb0122818177bfae83cb1499fcb7874bdea05be64963c2290b3a0596f80ad |
| L0/output/template/.claude/hooks/claude-hook.mjs | aba46da946b8025641cf6b493dd3dda6df5f571359c909465e71cbf8e67ff2e7 | aba46da946b8025641cf6b493dd3dda6df5f571359c909465e71cbf8e67ff2e7 |
| L0/output/template/.claude/hooks/manifest-checks.mjs | b7a5ee762cd856ac04e3c7fecdf69a7a15e243a3f40e6008c63db491ff960ade | b7a5ee762cd856ac04e3c7fecdf69a7a15e243a3f40e6008c63db491ff960ade |
| L0/output/template/.claude/rules/0-core/dependency-hygiene.md | b6600b9fa58c1af6d27724361d54df8767b8aadb8e04f0d256333e4923353df5 | b6600b9fa58c1af6d27724361d54df8767b8aadb8e04f0d256333e4923353df5 |
| L0/output/template/.claude/rules/0-core/logging-principles.md | cf603df617aa6505308037f5b5316972db3975436f164b7e65d6bb82d271b21d | cf603df617aa6505308037f5b5316972db3975436f164b7e65d6bb82d271b21d |
| L0/output/template/.claude/rules/0-core/runtime-principles.md | 6654ebf9fa5290bf0ed574f26f30b8c6302b51dfbfae2320cd6c79b3fbc9921f | 6654ebf9fa5290bf0ed574f26f30b8c6302b51dfbfae2320cd6c79b3fbc9921f |
| L0/output/template/.claude/rules/0-core/security-principles.md | 58967b3a324a11026e5d6c5d41405d8cb2fb398bbab38ae2b212ccd9d137e083 | 58967b3a324a11026e5d6c5d41405d8cb2fb398bbab38ae2b212ccd9d137e083 |
| L0/output/template/.claude/rules/0-core/testing-principles.md | 727fbba8f3a5bbbfa9652ba9f418f5d528a7b6fa72502c4bb1be329ead707094 | 727fbba8f3a5bbbfa9652ba9f418f5d528a7b6fa72502c4bb1be329ead707094 |
| L0/output/template/.claude/rules/1-architecture/backend-layers.md | c590a152fc2364bf04084c8e963d794c7d05c82f01569cdc43748f79c678c8e7 | c590a152fc2364bf04084c8e963d794c7d05c82f01569cdc43748f79c678c8e7 |
| L0/output/template/.claude/rules/1-architecture/code-organization.md | 3d06c7657762e5843a30a7b863c7f3bcf9f730e98a40699334e2b51fbbd88f56 | 3d06c7657762e5843a30a7b863c7f3bcf9f730e98a40699334e2b51fbbd88f56 |
| L0/output/template/.claude/rules/1-architecture/entry-points.md | 4976b03ceadf1c21057b6c8e522ba03fe5e2d2e0909851837f7321c03360aacf | 4976b03ceadf1c21057b6c8e522ba03fe5e2d2e0909851837f7321c03360aacf |
| L0/output/template/.claude/rules/1-architecture/frontend-structure.md | edb643da5b98c224819ec2d74bf73e592047cca5f37cffc466dc64f1fef51577 | edb643da5b98c224819ec2d74bf73e592047cca5f37cffc466dc64f1fef51577 |
| L0/output/template/.claude/rules/1-architecture/outcomes.md | 36723fe284015ea9d7ef6f9c25216d8c0ddcb3118ddfd9c56f568f85ac63dd5c | 36723fe284015ea9d7ef6f9c25216d8c0ddcb3118ddfd9c56f568f85ac63dd5c |
| L0/output/template/.claude/rules/1-architecture/overview.md | d8965b54613833d28f6776d682d493182d23935240d06e5c830e89b3363977e3 | d8965b54613833d28f6776d682d493182d23935240d06e5c830e89b3363977e3 |
| L0/output/template/.claude/rules/1-architecture/persistence-boundary.md | dbc2728cebbd587bf2fcd173020a20382f715e88e1521788296b220fc7a71d9d | dbc2728cebbd587bf2fcd173020a20382f715e88e1521788296b220fc7a71d9d |
| L0/output/template/.claude/rules/2-technology/angular.md | 055686c38dced484e66fcf80f869d91acb54ab62df83c5f082a800b6b73a6794 | 055686c38dced484e66fcf80f869d91acb54ab62df83c5f082a800b6b73a6794 |
| L0/output/template/.claude/rules/2-technology/aspnet-core.md | 9f0131da0b77aaadaf0eaee788ea632e6b3178b6c38e5d9a3b95f3278dea7b1c | 9f0131da0b77aaadaf0eaee788ea632e6b3178b6c38e5d9a3b95f3278dea7b1c |
| L0/output/template/.claude/rules/2-technology/containers-ci.md | 0439fd350cb0de0ea7e6b1c93ea9a062ea86541096b832b2590e812e22588acb | 0439fd350cb0de0ea7e6b1c93ea9a062ea86541096b832b2590e812e22588acb |
| L0/output/template/.claude/rules/2-technology/csharp.md | 92b9140d79d8092184f09b1ef50d3c2b57727ba30e3758de94a6f0549052e1d8 | 92b9140d79d8092184f09b1ef50d3c2b57727ba30e3758de94a6f0549052e1d8 |
| L0/output/template/.claude/rules/2-technology/dotnet-testing.md | 573a487fccd1f8e9585b253a5c75aaf14bc1e3f90e9291fccf154dbc0a7c5b3d | 573a487fccd1f8e9585b253a5c75aaf14bc1e3f90e9291fccf154dbc0a7c5b3d |
| L0/output/template/.claude/rules/2-technology/ef-core.md | 2feeab8a8efd2ad0d2ee66c584839a672efda72ece7af21d28cce66be1578fd9 | 2feeab8a8efd2ad0d2ee66c584839a672efda72ece7af21d28cce66be1578fd9 |
| L0/output/template/.claude/rules/2-technology/fluentvalidation.md | 3d7601af455800da0c866fca82e9b76cb02fdc0f5780d5ff4922cac9b972768c | 3d7601af455800da0c866fca82e9b76cb02fdc0f5780d5ff4922cac9b972768c |
| L0/output/template/.claude/rules/2-technology/logging.md | 4c829620f35434420fee516148f71e604687617c7193091a417ad8d54bcdfafc | 4c829620f35434420fee516148f71e604687617c7193091a417ad8d54bcdfafc |
| L0/output/template/.claude/rules/3-project/data-lifecycle.md | 27828d9068a3c6a5ae9d28f079f9c033372fce03bb1a9c4c5b17018ce46f4369 | 27828d9068a3c6a5ae9d28f079f9c033372fce03bb1a9c4c5b17018ce46f4369 |
| L0/output/template/.claude/rules/3-project/decisions.md | 76eca98b122bd7f41a0f3ae295c79c3a93b4c189a629d1b6e7c4ff93466ea59d | 76eca98b122bd7f41a0f3ae295c79c3a93b4c189a629d1b6e7c4ff93466ea59d |
| L0/output/template/.claude/rules/3-project/layout.md | 201d0ad4db67b876c24cd2dcfa491f72a52ba730c32908f3c08d425a751c8745 | 201d0ad4db67b876c24cd2dcfa491f72a52ba730c32908f3c08d425a751c8745 |
| L0/output/template/.claude/rules/3-project/package-management.md | cd945be41b43b448272c7fefd7e2f1d2544d6ef9fe2a74da05183843753666f4 | cd945be41b43b448272c7fefd7e2f1d2544d6ef9fe2a74da05183843753666f4 |
| L0/output/template/.claude/settings.json | 34356567cede181ed30fce72f26e55c5ea43bfb5fb8d754f931ce37405a59976 | 34356567cede181ed30fce72f26e55c5ea43bfb5fb8d754f931ce37405a59976 |
| L0/output/template/.claude/skills/add-dependency/SKILL.md | aabd590825a8528eb0b848ea715da112587291c712a1f7278a958cc9742d7ab7 | aabd590825a8528eb0b848ea715da112587291c712a1f7278a958cc9742d7ab7 |
| L0/output/template/.claude/skills/angular/SKILL.md | 0b3c6a0e57672053b2a3fb7959e8600d237b31e4a176a54c41da873260e6ac80 | 0b3c6a0e57672053b2a3fb7959e8600d237b31e4a176a54c41da873260e6ac80 |
| L0/output/template/.claude/skills/api-versioning/SKILL.md | ab1ab8aac96b8583bcf41b011399e96b0e94eb6a884e3c009a4832e959a88b7d | ab1ab8aac96b8583bcf41b011399e96b0e94eb6a884e3c009a4832e959a88b7d |
| L0/output/template/.claude/skills/architecture-decision/SKILL.md | f24304c911ad0daed5f9deb6c2bc438f5d8850d149bd3047a084fc1df9efc9b2 | f24304c911ad0daed5f9deb6c2bc438f5d8850d149bd3047a084fc1df9efc9b2 |
| L0/output/template/.claude/skills/aspnet-error-handling/SKILL.md | 9f61ad4ea2d495dfb3ff14e87219a503af68b5279ed1d5e07bebe71fe186d968 | 9f61ad4ea2d495dfb3ff14e87219a503af68b5279ed1d5e07bebe71fe186d968 |
| L0/output/template/.claude/skills/authentication/SKILL.md | 4c1c9285be7beb3565709037efe922091cfcad094a0e8a8310bc2a9e43674f09 | 4c1c9285be7beb3565709037efe922091cfcad094a0e8a8310bc2a9e43674f09 |
| L0/output/template/.claude/skills/build-fix/SKILL.md | 0e75858fa6dd43c36e126691682d2db491eb8611ebfc6f612666a95570649e01 | 0e75858fa6dd43c36e126691682d2db491eb8611ebfc6f612666a95570649e01 |
| L0/output/template/.claude/skills/caching/SKILL.md | 08a6d5989635ca9431b0b57cce9812ac13b9106ab21aabc8093e372e454676a2 | 08a6d5989635ca9431b0b57cce9812ac13b9106ab21aabc8093e372e454676a2 |
| L0/output/template/.claude/skills/ci-cd/SKILL.md | 59a776b42a80de206fb890f8caf14f3a0b4cc3e5725c6d8859dd556847a9631d | 59a776b42a80de206fb890f8caf14f3a0b4cc3e5725c6d8859dd556847a9631d |
| L0/output/template/.claude/skills/code-review/SKILL.md | 0eeca88e51001ec6d7ed1692ca0ed210b7890ee0b4e4622f8a749f5dbdebf13a | 0eeca88e51001ec6d7ed1692ca0ed210b7890ee0b4e4622f8a749f5dbdebf13a |
| L0/output/template/.claude/skills/configuration/SKILL.md | fbaf76c2e7f000280f872efd3bcf20e8bd4ca2bdb34c94efca69e17d8c76f9b1 | fbaf76c2e7f000280f872efd3bcf20e8bd4ca2bdb34c94efca69e17d8c76f9b1 |
| L0/output/template/.claude/skills/custom-settings/SKILL.md | 7ad728703176437fff36498ceecec07902397d697741a3b133ddf3ff2cddcac9 | 7ad728703176437fff36498ceecec07902397d697741a3b133ddf3ff2cddcac9 |
| L0/output/template/.claude/skills/delivery-pipeline/SKILL.md | d8e7a2d952746590394de4dee9c319c9d54d48487c6dd2be126e0ef90751881a | d8e7a2d952746590394de4dee9c319c9d54d48487c6dd2be126e0ef90751881a |
| L0/output/template/.claude/skills/dependency-injection/SKILL.md | 3cb3dbc0e2b0ce64e009dda6b52928c72bc11af33f79e4b3f331ec3660c55ef5 | 3cb3dbc0e2b0ce64e009dda6b52928c72bc11af33f79e4b3f331ec3660c55ef5 |
| L0/output/template/.claude/skills/development-workflow/SKILL.md | 81740b792987f91db4121a6d5e675d5e6d800b9cbe77a4a3e1619b641e26dfeb | 81740b792987f91db4121a6d5e675d5e6d800b9cbe77a4a3e1619b641e26dfeb |
| L0/output/template/.claude/skills/docker/SKILL.md | 085f23a7a0929e51460ec274024f05488371df1810f84975781628d665e5e5f8 | 085f23a7a0929e51460ec274024f05488371df1810f84975781628d665e5e5f8 |
| L0/output/template/.claude/skills/dotnet-testing/SKILL.md | bad46de251dbc4d26a5b51e2f5310dcdc858735e95441a056bd628460886c37c | bad46de251dbc4d26a5b51e2f5310dcdc858735e95441a056bd628460886c37c |
| L0/output/template/.claude/skills/ef-core/SKILL.md | 989bd9a518542dcf32d9210eba887fd4edb1c4a2bb4c032dd0d58d62a2769dc8 | 989bd9a518542dcf32d9210eba887fd4edb1c4a2bb4c032dd0d58d62a2769dc8 |
| L0/output/template/.claude/skills/git-workflow/SKILL.md | 371490383337c8532cf1f80ab281d79a2ede79efb2ad0d51103c87ebb63ebbad | 371490383337c8532cf1f80ab281d79a2ede79efb2ad0d51103c87ebb63ebbad |
| L0/output/template/.claude/skills/health-check/SKILL.md | a78ef361c5970977f94ab2980cb4a62be3779d38530d2e21cfce2afe07ca81f5 | a78ef361c5970977f94ab2980cb4a62be3779d38530d2e21cfce2afe07ca81f5 |
| L0/output/template/.claude/skills/http-api/SKILL.md | 8143e3e06a0d756e3c4f8c5d4b931070d0f230f67336d9576d74a239802449ae | 8143e3e06a0d756e3c4f8c5d4b931070d0f230f67336d9576d74a239802449ae |
| L0/output/template/.claude/skills/httpclient-factory/SKILL.md | 8fc5c9fd2288c4276770747e701a2233f57bedcf53f9d55782087903a62a4078 | 8fc5c9fd2288c4276770747e701a2233f57bedcf53f9d55782087903a62a4078 |
| L0/output/template/.claude/skills/httpclient-factory/references/resilience.md | 39ec7602a1ba48fe96cc82fbe15e82c7ae5e82f7c9c796ad092a84cc6c4e16c7 | 39ec7602a1ba48fe96cc82fbe15e82c7ae5e82f7c9c796ad092a84cc6c4e16c7 |
| L0/output/template/.claude/skills/logging/SKILL.md | c651fbd2336601e2e13ce8c046c49e56ea269dc68e83228bb7ee88bdba7bbca3 | c651fbd2336601e2e13ce8c046c49e56ea269dc68e83228bb7ee88bdba7bbca3 |
| L0/output/template/.claude/skills/logging/references/serilog.md | 2e79cb400c4240681f6c880d98549f1545cb6fad144ccb667276c8fc99925639 | 2e79cb400c4240681f6c880d98549f1545cb6fad144ccb667276c8fc99925639 |
| L0/output/template/.claude/skills/modern-csharp/SKILL.md | e4c92d9afe8cd8d9dcf3b9ce631a94e756acffac17b3c06f6f4fecd54f6554ad | e4c92d9afe8cd8d9dcf3b9ce631a94e756acffac17b3c06f6f4fecd54f6554ad |
| L0/output/template/.claude/skills/project-structure/SKILL.md | 94b2a0028f63fa4310d7624ee485ae44cf9d6f2e71a6d4a870b89ffd06d79171 | 94b2a0028f63fa4310d7624ee485ae44cf9d6f2e71a6d4a870b89ffd06d79171 |
| L0/output/template/.claude/skills/project-structure/references/backend-layout.md | 156dcc87b307e316cbc42378bb85978e56ed1b21ef31a0fd9cafe1923c9a6049 | 156dcc87b307e316cbc42378bb85978e56ed1b21ef31a0fd9cafe1923c9a6049 |
| L0/output/template/.claude/skills/project-structure/references/solution-layout.md | 3fe65052fc0c2af61e86f1c0ef32d88e139c1a97f57537fd70a51a666696efe3 | 3fe65052fc0c2af61e86f1c0ef32d88e139c1a97f57537fd70a51a666696efe3 |
| L0/output/template/.claude/skills/security-scan/SKILL.md | a7674f8c56e85d7f9102dbff876205e8157222e2cf3593d6ea40e51a12f14887 | a7674f8c56e85d7f9102dbff876205e8157222e2cf3593d6ea40e51a12f14887 |
| L0/output/template/.claude/skills/security-scan/references/scan-layers.md | 3ad52189fdee742608f70aa3d46a73a5eb04fcf2c4f2282e8d809e1342f50389 | 3ad52189fdee742608f70aa3d46a73a5eb04fcf2c4f2282e8d809e1342f50389 |
| L0/output/template/.claude/skills/swagger/SKILL.md | 300b18c838e0fdb33e138261701a6306297365a4456d92aab3d5c92e1a110858 | 300b18c838e0fdb33e138261701a6306297365a4456d92aab3d5c92e1a110858 |
| L0/output/template/.claude/skills/template-maintenance/SKILL.md | fea614b02b014a262ff888264f49c9a6f191dd00e3e00c72a5c33c6b060e9dc5 | fea614b02b014a262ff888264f49c9a6f191dd00e3e00c72a5c33c6b060e9dc5 |
| L0/output/template/.claude/skills/verify/SKILL.md | efa60025fe911c14ab72080ecf10709aabf8547267ff0cd73ada77c0351ca950 | efa60025fe911c14ab72080ecf10709aabf8547267ff0cd73ada77c0351ca950 |
| L0/output/template/.claude/tools/check-instructions.mjs | c0a5dc2f8ca7c2927002517bc397275627ddd719c2506058a5eb99a32efbe8b5 | c0a5dc2f8ca7c2927002517bc397275627ddd719c2506058a5eb99a32efbe8b5 |
| L0/output/template/.editorconfig | 224af498b88f0a61a21e85f1707da700c2acdde2c58c511e6ae5e12550da244f | 224af498b88f0a61a21e85f1707da700c2acdde2c58c511e6ae5e12550da244f |
| L0/output/template/.gitignore | f9bd2d65e92ac574bcb52b249a3d4faee1663a1b01e6361365a5d82b0edd2068 | f9bd2d65e92ac574bcb52b249a3d4faee1663a1b01e6361365a5d82b0edd2068 |
| L0/output/template/CLAUDE.md | 8d3e72d521d80cf81713771d162d4319a8d7e34a52320f85e897b5c4b42165e7 | 8d3e72d521d80cf81713771d162d4319a8d7e34a52320f85e897b5c4b42165e7 |
| L0/output/template/CUSTOM_SETTINGS.md | 20d7d3e96d28ae3949d1d08cadaea401bc870caa8e53d27360e45a76bfd70080 | 20d7d3e96d28ae3949d1d08cadaea401bc870caa8e53d27360e45a76bfd70080 |
| L0/output/template/Directory.Build.props | 4c1226faa5e317d032c560e1c4c2bca6954f0c3c39261bbed8505c2853cde31f | 4c1226faa5e317d032c560e1c4c2bca6954f0c3c39261bbed8505c2853cde31f |
| L0/output/template/Directory.Packages.props | 099e294e728f3292b8c52fafb42614542faa31ea1324d088a2ee591b26408c68 | 099e294e728f3292b8c52fafb42614542faa31ea1324d088a2ee591b26408c68 |
| L0/output/template/SPECIFICATION.md | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| L1-Restart/output/template/.claude/INSTRUCTION_MAP.md | 5d8fecf6abac441ab71e1a975f7c7e00b3f9d2ee84eac270d0ce80987b11dae7 | 5d8fecf6abac441ab71e1a975f7c7e00b3f9d2ee84eac270d0ce80987b11dae7 |
| L1-Restart/output/template/.claude/agents/code-reviewer.md | a0b5cb624b81e3cceff9c262bf48940fb1bc54a2e40edd7f58d58ecbf479c739 | a0b5cb624b81e3cceff9c262bf48940fb1bc54a2e40edd7f58d58ecbf479c739 |
| L1-Restart/output/template/.claude/capabilities/architecture/CONTRACT.md | a7246fb4d102096598e3d3d835a3201a748e72d6ae4fa076ae351503508feeed | a7246fb4d102096598e3d3d835a3201a748e72d6ae4fa076ae351503508feeed |
| L1-Restart/output/template/.claude/capabilities/architecture/clean-architecture/MODULE.md | e9dc3b0793e65b1bd0399191d6af68aaf7b5092c3086bbf0e774e27075052b7a | e9dc3b0793e65b1bd0399191d6af68aaf7b5092c3086bbf0e774e27075052b7a |
| L1-Restart/output/template/.claude/capabilities/architecture/clean-architecture/check.json | e2febd623e727aa21074f61894b05002beb9fe39391f8f901d305ec43f9d0421 | e2febd623e727aa21074f61894b05002beb9fe39391f8f901d305ec43f9d0421 |
| L1-Restart/output/template/.claude/capabilities/architecture/clean-architecture/layout.md | 24d9b02adfb7890417e1653c6bed7f368102f140f5cb7d5aeb73b4436c30b3dd | 24d9b02adfb7890417e1653c6bed7f368102f140f5cb7d5aeb73b4436c30b3dd |
| L1-Restart/output/template/.claude/capabilities/backend-testing/CONTRACT.md | 21fd38db653653f6c42efde5e61802f85e1543d0d21306aab461ffad20bd2d55 | 21fd38db653653f6c42efde5e61802f85e1543d0d21306aab461ffad20bd2d55 |
| L1-Restart/output/template/.claude/capabilities/backend-testing/nunit/MODULE.md | 5f59352da1d44902e148fd58f5acc1944841b464a2511809ffac29262a2bbcad | 5f59352da1d44902e148fd58f5acc1944841b464a2511809ffac29262a2bbcad |
| L1-Restart/output/template/.claude/capabilities/backend-testing/nunit/commands.md | d9fa2b4b93dd5b81b78e093defa7697f1478fbbb37335aca72876aac9c44ad94 | d9fa2b4b93dd5b81b78e093defa7697f1478fbbb37335aca72876aac9c44ad94 |
| L1-Restart/output/template/.claude/capabilities/backend-testing/nunit/enforcement.json | 47e5b370494090774d250563825364ac77e6978966a5067fba6359cd1e1fab8e | 47e5b370494090774d250563825364ac77e6978966a5067fba6359cd1e1fab8e |
| L1-Restart/output/template/.claude/capabilities/frontend/CONTRACT.md | 6cb648069b07da65facf09d82e12bf66c3ad464632056767321997a44d94666c | 6cb648069b07da65facf09d82e12bf66c3ad464632056767321997a44d94666c |
| L1-Restart/output/template/.claude/capabilities/frontend/angular/MODULE.md | 020a56d0ae4f8369bd242515837a5436a2ab98fcf3c9167b46ac3ede5b8a6d19 | 020a56d0ae4f8369bd242515837a5436a2ab98fcf3c9167b46ac3ede5b8a6d19 |
| L1-Restart/output/template/.claude/capabilities/frontend/angular/commands.md | 114e7dedaefab13f948d7b2d1c9b39a6aa1ed5a0c811f5118f32ad0bf2e5399e | 114e7dedaefab13f948d7b2d1c9b39a6aa1ed5a0c811f5118f32ad0bf2e5399e |
| L1-Restart/output/template/.claude/capabilities/frontend/angular/enforcement.json | 26fb815c9152b77fe19379eb968345f94a1253f37a9f24cff4493e2606a0c03c | 26fb815c9152b77fe19379eb968345f94a1253f37a9f24cff4493e2606a0c03c |
| L1-Restart/output/template/.claude/capabilities/persistence/CONTRACT.md | d07bafe4b70e1f5bd3457a56f967da8c87270de640fce1ef4e4e4a00dceae558 | d07bafe4b70e1f5bd3457a56f967da8c87270de640fce1ef4e4e4a00dceae558 |
| L1-Restart/output/template/.claude/capabilities/persistence/ef-core/MODULE.md | a9ad3e7890ff886f26c7cf65a7b71a18b56d046209886d71d1c7fda389ffdb8b | a9ad3e7890ff886f26c7cf65a7b71a18b56d046209886d71d1c7fda389ffdb8b |
| L1-Restart/output/template/.claude/capabilities/persistence/ef-core/commands.md | 875d1a8d09b431a15c0653ac16837f6c190598022efe905ce74e697a049b0c3f | 875d1a8d09b431a15c0653ac16837f6c190598022efe905ce74e697a049b0c3f |
| L1-Restart/output/template/.claude/capabilities/persistence/ef-core/enforcement.json | 3022f9afa7cc2d31a2bab49ce540ad7b48480a8a756545eb52114a05a3269621 | 3022f9afa7cc2d31a2bab49ce540ad7b48480a8a756545eb52114a05a3269621 |
| L1-Restart/output/template/.claude/capabilities/persistence/ef-core/workflow.md | 3f559a76a44b54bdcd752b853403fe6d9d15b3063a2a0b6c3e0c24224cb5e264 | 3f559a76a44b54bdcd752b853403fe6d9d15b3063a2a0b6c3e0c24224cb5e264 |
| L1-Restart/output/template/.claude/hooks/manifest-policy.json | 9d14d2235d1874fbd7f6cee6f9563a0a602c8d4182a6b9bd1a71edaf7877a5e0 | 9d14d2235d1874fbd7f6cee6f9563a0a602c8d4182a6b9bd1a71edaf7877a5e0 |
| L1-Restart/output/template/.claude/hooks/post-change-checks.mjs | cab5844b5a1f6268b70cfe8ada426aa0cdc30ff65f54396ac8eb6825b6acafec | cab5844b5a1f6268b70cfe8ada426aa0cdc30ff65f54396ac8eb6825b6acafec |
| L1-Restart/output/template/.claude/hooks/pre-shell-command.mjs | f7dfdf6ab9a78689ddcaf9a9891e420980fffb9e5214d9ca83fba284f12632a0 | f7dfdf6ab9a78689ddcaf9a9891e420980fffb9e5214d9ca83fba284f12632a0 |
| L1-Restart/output/template/.claude/hooks/stop-cochange.mjs | 50bb32bb690fd140aac105f2867860f5b6f7cb2c0b246649ecfe17e12edd469a | 50bb32bb690fd140aac105f2867860f5b6f7cb2c0b246649ecfe17e12edd469a |
| L1-Restart/output/template/.claude/rules/0-core/backend-code.md | 23794ecc93cad051c586d5477bf9b6a0ede505436fc198ed5bba985af672e8b6 | 23794ecc93cad051c586d5477bf9b6a0ede505436fc198ed5bba985af672e8b6 |
| L1-Restart/output/template/.claude/rules/0-core/engineering.md | 40acd7c109a5da3b38232afd22b8d96e8fa6f7d306968ed034ca407c0278f4c3 | 40acd7c109a5da3b38232afd22b8d96e8fa6f7d306968ed034ca407c0278f4c3 |
| L1-Restart/output/template/.claude/rules/0-core/frontend.md | e93d924f471db09c8e25c306dcad7eb8d2300f08f919632cb40ecdb9efe383e4 | e93d924f471db09c8e25c306dcad7eb8d2300f08f919632cb40ecdb9efe383e4 |
| L1-Restart/output/template/.claude/rules/0-core/http-api.md | 8efc015d776757bb33c34136149c2842adf0383ed48a9ed4fba25ba3f120f8e8 | 8efc015d776757bb33c34136149c2842adf0383ed48a9ed4fba25ba3f120f8e8 |
| L1-Restart/output/template/.claude/rules/0-core/security.md | dd5079a0ff5c54292597310cbb617e52ba4a29d0a06cf726f2658bc3bda3d77e | dd5079a0ff5c54292597310cbb617e52ba4a29d0a06cf726f2658bc3bda3d77e |
| L1-Restart/output/template/.claude/rules/0-core/testing.md | 9c164e8e79ce309449cf9457a0dc3bf2de4245cdfd596168c196ba5fc87a17a2 | 9c164e8e79ce309449cf9457a0dc3bf2de4245cdfd596168c196ba5fc87a17a2 |
| L1-Restart/output/template/.claude/rules/1-architecture/frame/adopted-style.md | 74fe2817165016d4064a5224b18acb954fdc6761ada50b9c6fd24319cb4d9dc6 | 74fe2817165016d4064a5224b18acb954fdc6761ada50b9c6fd24319cb4d9dc6 |
| L1-Restart/output/template/.claude/rules/1-architecture/frame/boundaries.md | 3f17329f2488ec268eaad92d72a48b2ece33f14d6541109b905f27b32fcd3929 | 3f17329f2488ec268eaad92d72a48b2ece33f14d6541109b905f27b32fcd3929 |
| L1-Restart/output/template/.claude/rules/1-architecture/roles.md | 277703b3fe3230e7010557748d121ed68193b06a8b417a65bec11d57b957d47b | 277703b3fe3230e7010557748d121ed68193b06a8b417a65bec11d57b957d47b |
| L1-Restart/output/template/.claude/rules/2-technology/backend-libraries.md | e45e5a0bf306d93bc5479221ed7494a138affc8424e5046dd09ddd5ac4f44930 | e45e5a0bf306d93bc5479221ed7494a138affc8424e5046dd09ddd5ac4f44930 |
| L1-Restart/output/template/.claude/rules/2-technology/backend-platform.md | 36c8feada89cf40ccc17cbcc0438c9c8fdced6006ffa24807378747a36fa1055 | 36c8feada89cf40ccc17cbcc0438c9c8fdced6006ffa24807378747a36fa1055 |
| L1-Restart/output/template/.claude/rules/2-technology/backend-testing/test-framework.md | 208f8fcc7be56a36ec6fd7db93b8c1695a70c08c3674f92d954439d1e26c19a8 | 208f8fcc7be56a36ec6fd7db93b8c1695a70c08c3674f92d954439d1e26c19a8 |
| L1-Restart/output/template/.claude/rules/2-technology/frontend/framework.md | 32a046018355771dd6a2fc78104b27d59a49ede711255d06396234fcb6e973d7 | 32a046018355771dd6a2fc78104b27d59a49ede711255d06396234fcb6e973d7 |
| L1-Restart/output/template/.claude/rules/2-technology/persistence/access.md | 7bdc4e7962ff5b51c947d4d582a9d498058a185ebf2367485a75e1d8394e96ee | 7bdc4e7962ff5b51c947d4d582a9d498058a185ebf2367485a75e1d8394e96ee |
| L1-Restart/output/template/.claude/rules/2-technology/persistence/seeding.md | 37732ae58dd58fca5d17dee0089f37f767332d41b97a3775421f3b12e99da828 | 37732ae58dd58fca5d17dee0089f37f767332d41b97a3775421f3b12e99da828 |
| L1-Restart/output/template/.claude/rules/3-project/decisions.md | bab8e14542759ca71b9fff4e835d7753afa139d1d994d691f3c922d5d51495e7 | bab8e14542759ca71b9fff4e835d7753afa139d1d994d691f3c922d5d51495e7 |
| L1-Restart/output/template/.claude/rules/3-project/development-database.md | d1fb5f1c3c9ecfeed3e5f6cb5795125cdfaced57b97562dc9ece760e83fb68f0 | d1fb5f1c3c9ecfeed3e5f6cb5795125cdfaced57b97562dc9ece760e83fb68f0 |
| L1-Restart/output/template/.claude/rules/3-project/frontend-stack.md | 7aae4bd47f82299e5692b17f2533ad58de5b76b34f775923f848f2353b8f2d09 | 7aae4bd47f82299e5692b17f2533ad58de5b76b34f775923f848f2353b8f2d09 |
| L1-Restart/output/template/.claude/rules/3-project/package-management.md | aa44ae430565fe1b17680a4ae134c651693f3877d094a56c1c3a9ea756548818 | aa44ae430565fe1b17680a4ae134c651693f3877d094a56c1c3a9ea756548818 |
| L1-Restart/output/template/.claude/scripts/check-architecture.mjs | f755cf48fabe00078dd1ea3bf41097e2ca08910a743473f285732c4018614112 | f755cf48fabe00078dd1ea3bf41097e2ca08910a743473f285732c4018614112 |
| L1-Restart/output/template/.claude/scripts/check-instructions.mjs | 8171ce3941aba33d75a0b609d9d0c8a3f8761ad574b8a709209be6c219c55663 | 8171ce3941aba33d75a0b609d9d0c8a3f8761ad574b8a709209be6c219c55663 |
| L1-Restart/output/template/.claude/scripts/lib/project.mjs | 2fdf409d2aac227ab16e6986fcaa43ddb281dd2e14452aea336eda173c237a02 | 2fdf409d2aac227ab16e6986fcaa43ddb281dd2e14452aea336eda173c237a02 |
| L1-Restart/output/template/.claude/settings.json | f6f5220a9ac136b93c766cff11a46dd79536d802a8209d06b5db4612438947da | f6f5220a9ac136b93c766cff11a46dd79536d802a8209d06b5db4612438947da |
| L1-Restart/output/template/.claude/skills/add-dependency/SKILL.md | eec7686cfd4439ed6882ea8f2f3e09c09c7fbba0e645c23f5fead779fc3a6be4 | eec7686cfd4439ed6882ea8f2f3e09c09c7fbba0e645c23f5fead779fc3a6be4 |
| L1-Restart/output/template/.claude/skills/angular/SKILL.md | 0ce0c01e7f859943ea1d3420d6c221bb2491471262111c61054a6076722a0d3a | 0ce0c01e7f859943ea1d3420d6c221bb2491471262111c61054a6076722a0d3a |
| L1-Restart/output/template/.claude/skills/api-versioning/SKILL.md | 3305e507eff48b46ff3e05bf87d60210473a225b5bc63ea4cf5f6510ec31fc84 | 3305e507eff48b46ff3e05bf87d60210473a225b5bc63ea4cf5f6510ec31fc84 |
| L1-Restart/output/template/.claude/skills/architecture-decision/SKILL.md | 48c618883b0067478db7fcb1bb73040cd219fb31c84673c3f2b18eaa3b2215fd | 48c618883b0067478db7fcb1bb73040cd219fb31c84673c3f2b18eaa3b2215fd |
| L1-Restart/output/template/.claude/skills/aspnet-error-handling/SKILL.md | 9492da6a45b67efe54dcf87c2fa5836ae06d92c99a0646f8a30fafc8e47a2957 | 9492da6a45b67efe54dcf87c2fa5836ae06d92c99a0646f8a30fafc8e47a2957 |
| L1-Restart/output/template/.claude/skills/authentication/SKILL.md | 9a8fe8ffb6aad068b38778c6a0cdcf06748a32590cc85ea5f4e24bfefb288bfb | 9a8fe8ffb6aad068b38778c6a0cdcf06748a32590cc85ea5f4e24bfefb288bfb |
| L1-Restart/output/template/.claude/skills/build-fix/SKILL.md | ce0524b698735bd50f1746aea72f79f95e7300d81119a589601f0d5aace7f3ae | ce0524b698735bd50f1746aea72f79f95e7300d81119a589601f0d5aace7f3ae |
| L1-Restart/output/template/.claude/skills/caching/SKILL.md | 52bfd0e504b6160736fa461f5bac9977f68cc15fdf15ea3556ee6c66cae7d6c9 | 52bfd0e504b6160736fa461f5bac9977f68cc15fdf15ea3556ee6c66cae7d6c9 |
| L1-Restart/output/template/.claude/skills/ci-cd/SKILL.md | 112579396d90a300d6a2ba8cec2415fb1a296fdde2ecead93d727f69a4bbe469 | 112579396d90a300d6a2ba8cec2415fb1a296fdde2ecead93d727f69a4bbe469 |
| L1-Restart/output/template/.claude/skills/code-review/SKILL.md | 5cc45407429c534fe1dc053f7fffa2e1392f5150e10321ec1025838316f44b65 | 5cc45407429c534fe1dc053f7fffa2e1392f5150e10321ec1025838316f44b65 |
| L1-Restart/output/template/.claude/skills/configuration/SKILL.md | 176901e833f7bd02728290fe5619e47ed73eedcd1e6eab2b985a2efd2e934702 | 176901e833f7bd02728290fe5619e47ed73eedcd1e6eab2b985a2efd2e934702 |
| L1-Restart/output/template/.claude/skills/custom-settings/SKILL.md | 853c69cb944534e84e99ff7acdbc409182d3f8082e7cf7a562c4db5d75022fe6 | 853c69cb944534e84e99ff7acdbc409182d3f8082e7cf7a562c4db5d75022fe6 |
| L1-Restart/output/template/.claude/skills/dependency-injection/SKILL.md | 3139f3887abf763d2d2383175101f2b0890e220e6cbf223d3811cd096a74fc19 | 3139f3887abf763d2d2383175101f2b0890e220e6cbf223d3811cd096a74fc19 |
| L1-Restart/output/template/.claude/skills/development-workflow/SKILL.md | b383de1664c122a7f1ffb61400d23685bd6d40b88cd7d62c08c195eace8c45fb | b383de1664c122a7f1ffb61400d23685bd6d40b88cd7d62c08c195eace8c45fb |
| L1-Restart/output/template/.claude/skills/docker/SKILL.md | 22300b37b31f1a68b201db13c9ed4b1511e5ba9658f142b348d38b02bf7248a9 | 22300b37b31f1a68b201db13c9ed4b1511e5ba9658f142b348d38b02bf7248a9 |
| L1-Restart/output/template/.claude/skills/dotnet-testing/SKILL.md | 8893ce19b314d0ee88fb7dee1832a66e2187e28eb4b608119230424c8a45582e | 8893ce19b314d0ee88fb7dee1832a66e2187e28eb4b608119230424c8a45582e |
| L1-Restart/output/template/.claude/skills/ef-core/SKILL.md | 938608876a89b85aa74c7530ebdab4fe55d0baec5d987331ad481694e1a1d778 | 938608876a89b85aa74c7530ebdab4fe55d0baec5d987331ad481694e1a1d778 |
| L1-Restart/output/template/.claude/skills/git-workflow/SKILL.md | c0e7f9608c1a1268f75aea5ac8585892c6ec61383dae0405fbbcf21c981a94ae | c0e7f9608c1a1268f75aea5ac8585892c6ec61383dae0405fbbcf21c981a94ae |
| L1-Restart/output/template/.claude/skills/health-check/SKILL.md | 18fc78c0f070911082c032309c7d6050cc889647d5984c38b778f19a2d0bf427 | 18fc78c0f070911082c032309c7d6050cc889647d5984c38b778f19a2d0bf427 |
| L1-Restart/output/template/.claude/skills/http-api/SKILL.md | face75a5f005829be7be05ed09dffaad19603efcb6b8e2e2aa43fc403607f032 | face75a5f005829be7be05ed09dffaad19603efcb6b8e2e2aa43fc403607f032 |
| L1-Restart/output/template/.claude/skills/httpclient-factory/SKILL.md | 72ea93f5509a0d70b95962fdb2f43cdc34320714634c5f1a288e6c7a42866d07 | 72ea93f5509a0d70b95962fdb2f43cdc34320714634c5f1a288e6c7a42866d07 |
| L1-Restart/output/template/.claude/skills/httpclient-factory/references/resilience.md | 7ea3130b9cc8bdaaffc5b8f3c0b61207461e566c02985d6531cdd6d40a8dd2c6 | 7ea3130b9cc8bdaaffc5b8f3c0b61207461e566c02985d6531cdd6d40a8dd2c6 |
| L1-Restart/output/template/.claude/skills/logging/SKILL.md | caafb31b7e638af39476e495a85dc5c636cc29eb2d876cd3cd064f815f61a1d1 | caafb31b7e638af39476e495a85dc5c636cc29eb2d876cd3cd064f815f61a1d1 |
| L1-Restart/output/template/.claude/skills/logging/references/serilog.md | 0f9d3364ec4540363bc15e4ed6b40ca24620bd0f51b9aca57c3d5e8a65d4161f | 0f9d3364ec4540363bc15e4ed6b40ca24620bd0f51b9aca57c3d5e8a65d4161f |
| L1-Restart/output/template/.claude/skills/modern-csharp/SKILL.md | 9675bfdad6a7b64fe4e8a74eded30e58f8b69d4c22ea773d70d694a3bfcfba3f | 9675bfdad6a7b64fe4e8a74eded30e58f8b69d4c22ea773d70d694a3bfcfba3f |
| L1-Restart/output/template/.claude/skills/project-structure/SKILL.md | 64c0cc797bbea0e0f63e6dbcf860544900200942c3ad049c5965e15c36c2b9bc | 64c0cc797bbea0e0f63e6dbcf860544900200942c3ad049c5965e15c36c2b9bc |
| L1-Restart/output/template/.claude/skills/project-structure/references/baseline-packages.md | 309e54bf358eca1a2be138486429f28cee76de8645568c00e07de4e58e55a6cd | 309e54bf358eca1a2be138486429f28cee76de8645568c00e07de4e58e55a6cd |
| L1-Restart/output/template/.claude/skills/project-structure/references/solution-layout.md | 8b5e3f18c47beb80cb0a4cc954cd04e6ed29ad6eb8f6bd9597210a6496559b29 | 8b5e3f18c47beb80cb0a4cc954cd04e6ed29ad6eb8f6bd9597210a6496559b29 |
| L1-Restart/output/template/.claude/skills/security-scan/SKILL.md | ac92de2a7df8dd99ab6532d642bc64574c0b5447c1aa4d99464c095787a0a5cc | ac92de2a7df8dd99ab6532d642bc64574c0b5447c1aa4d99464c095787a0a5cc |
| L1-Restart/output/template/.claude/skills/security-scan/references/scan-layers.md | f58ae2aa847859891b80c6fa72f5f5f0a5a62427239f69bb29f4f742feb829f1 | f58ae2aa847859891b80c6fa72f5f5f0a5a62427239f69bb29f4f742feb829f1 |
| L1-Restart/output/template/.claude/skills/swagger/SKILL.md | 8066b9b5a8b28ebc328f2a4d73983aefc401c87ea6840866a57c075382409b56 | 8066b9b5a8b28ebc328f2a4d73983aefc401c87ea6840866a57c075382409b56 |
| L1-Restart/output/template/.claude/skills/template-maintenance/SKILL.md | 39a1d4cf8f4278b3123852e6a0d5da91a31d1e03db05fc08d843acd9eb60dd88 | 39a1d4cf8f4278b3123852e6a0d5da91a31d1e03db05fc08d843acd9eb60dd88 |
| L1-Restart/output/template/.claude/skills/verify/SKILL.md | f2ca71db5ae805d37d28faa494a0a2c1a86a087328c21d5a9066f07621a375d3 | f2ca71db5ae805d37d28faa494a0a2c1a86a087328c21d5a9066f07621a375d3 |
| L1-Restart/output/template/.editorconfig | 391a133afadc2f8e3763ef367b7da32dfaa61c8bf61567d963744b0d75f1c76a | 391a133afadc2f8e3763ef367b7da32dfaa61c8bf61567d963744b0d75f1c76a |
| L1-Restart/output/template/.gitignore | 94e1748cd177e033c64babb0a0541bc3eb6dcc86a3703ee7f9c44568b1dac864 | 94e1748cd177e033c64babb0a0541bc3eb6dcc86a3703ee7f9c44568b1dac864 |
| L1-Restart/output/template/CLAUDE.md | 6af28e0f80cfe49a8c17c53904cb597ab63998e014ed6c56cc7a52b769badb2e | 6af28e0f80cfe49a8c17c53904cb597ab63998e014ed6c56cc7a52b769badb2e |
| L1-Restart/output/template/CUSTOM_SETTINGS.md | 3292b0bab25f9ad8f1649ca9a4f3052900b90441bde3f24930b127adb494d738 | 3292b0bab25f9ad8f1649ca9a4f3052900b90441bde3f24930b127adb494d738 |
| L1-Restart/output/template/Directory.Build.props | 7d3a5993c5caff751e3bf5541b69215a29b346a3a3aee39bd14a2d733f36e684 | 7d3a5993c5caff751e3bf5541b69215a29b346a3a3aee39bd14a2d733f36e684 |
| L1-Restart/output/template/Directory.Packages.props | 74a5c16660af17a8b0ef615160d19074728d33d438c6d7e14bfeae9836c96d99 | 74a5c16660af17a8b0ef615160d19074728d33d438c6d7e14bfeae9836c96d99 |
| L1-Restart/output/template/SPECIFICATION.md | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| M/output/template/.claude/MAP.md | 19dc1d9dd1c0f237497df61f33eb100c3f8bb8a04199ec624a6214fe87d32203 | 19dc1d9dd1c0f237497df61f33eb100c3f8bb8a04199ec624a6214fe87d32203 |
| M/output/template/.claude/agents/code-reviewer.md | 874de8b7a853e13fb77d65e875829a454a88c2d936dbc3baa853c513dc6ea4a5 | 874de8b7a853e13fb77d65e875829a454a88c2d936dbc3baa853c513dc6ea4a5 |
| M/output/template/.claude/hooks/dependency-guard.mjs | 31cdfb2dc385e664b1305cbe568d7ea12f9f3f210cdcedc365c5d544f73b884a | 31cdfb2dc385e664b1305cbe568d7ea12f9f3f210cdcedc365c5d544f73b884a |
| M/output/template/.claude/hooks/file-change.mjs | 5e81a7858037206c8c1123f045dfe4753bf01040353b1a0e01419d3d58aa495b | 5e81a7858037206c8c1123f045dfe4753bf01040353b1a0e01419d3d58aa495b |
| M/output/template/.claude/hooks/hook-io.mjs | 0c65de4472e21d22786a983c07276040e900418caaa955266bcd99eea56c52f0 | 0c65de4472e21d22786a983c07276040e900418caaa955266bcd99eea56c52f0 |
| M/output/template/.claude/hooks/stop-co-change.mjs | b13b675caeafff5863bafb23033d07ed4270c0dea3c4f48b92c54180b5bac04c | b13b675caeafff5863bafb23033d07ed4270c0dea3c4f48b92c54180b5bac04c |
| M/output/template/.claude/rules/angular.md | 4afad76b5b972a44346f9bbff1623d52d38fc72b952203216ccb9d5993a7a9b0 | 4afad76b5b972a44346f9bbff1623d52d38fc72b952203216ccb9d5993a7a9b0 |
| M/output/template/.claude/rules/api.md | df9fbe2c774c275bf4a922c091473c6c3d5afa2a93a33d858d02c04ff50066d8 | df9fbe2c774c275bf4a922c091473c6c3d5afa2a93a33d858d02c04ff50066d8 |
| M/output/template/.claude/rules/architecture.md | 3affbdc8d9349fc09b90e0f93f1a160bc711369dc360f9b5968d646d3ea1712c | 3affbdc8d9349fc09b90e0f93f1a160bc711369dc360f9b5968d646d3ea1712c |
| M/output/template/.claude/rules/coding-style.md | 9be4aa8903041614504a73233a945f92f80da94655d791f017fa0625957a2eb5 | 9be4aa8903041614504a73233a945f92f80da94655d791f017fa0625957a2eb5 |
| M/output/template/.claude/rules/dependencies.md | 40927cb48e2ce7abb2fa4932706ea21e1ab936a2d513b0fb6948b259dfd415a4 | 40927cb48e2ce7abb2fa4932706ea21e1ab936a2d513b0fb6948b259dfd415a4 |
| M/output/template/.claude/rules/error-handling.md | f211e9b96af6c80033c5613ac5afa73dd5c3e70f24a34484493d5276698cec49 | f211e9b96af6c80033c5613ac5afa73dd5c3e70f24a34484493d5276698cec49 |
| M/output/template/.claude/rules/performance.md | 483f34a908cd02ad59be3a184dd5287bb2fac0bf586ef687fd132f497165a891 | 483f34a908cd02ad59be3a184dd5287bb2fac0bf586ef687fd132f497165a891 |
| M/output/template/.claude/rules/persistence.md | 68bb09fa5cfd614461774f77646a16216bdc98f121c2886f857f302f7cce0467 | 68bb09fa5cfd614461774f77646a16216bdc98f121c2886f857f302f7cce0467 |
| M/output/template/.claude/rules/repository-structure.md | 4f939dc81e4cde370a4429d55251df7fbacda320a9b9e2b866c90baee2809d2a | 4f939dc81e4cde370a4429d55251df7fbacda320a9b9e2b866c90baee2809d2a |
| M/output/template/.claude/rules/security.md | d98f39f285f05ffcf7dd987937263ed16d8c6305fc4721bd87d3854ddeb496be | d98f39f285f05ffcf7dd987937263ed16d8c6305fc4721bd87d3854ddeb496be |
| M/output/template/.claude/rules/testing.md | 2284090651fcb0012b518d3ae68bd98869fc8c60550abf6f927aa822894ef8e0 | 2284090651fcb0012b518d3ae68bd98869fc8c60550abf6f927aa822894ef8e0 |
| M/output/template/.claude/scripts/check-instructions.mjs | 03102c82ade3cf3d24afccf9b832671b158f1837b8794afe8c47677157b83c1d | 03102c82ade3cf3d24afccf9b832671b158f1837b8794afe8c47677157b83c1d |
| M/output/template/.claude/scripts/check-manifests.mjs | cedb53d362ec5051e5a1dd4b71eca4581b7ddbac90c510f54e6b1b3c90194386 | cedb53d362ec5051e5a1dd4b71eca4581b7ddbac90c510f54e6b1b3c90194386 |
| M/output/template/.claude/scripts/repo-root.mjs | 769e380d8d92425ddfc5ecb9dd65d214ceb0b323056d82e7b9c13e74c6357a41 | 769e380d8d92425ddfc5ecb9dd65d214ceb0b323056d82e7b9c13e74c6357a41 |
| M/output/template/.claude/settings.json | 66cfa8a58a81345ddffc982e4099be557837745f7ccfbb32c7886e68a97886d0 | 66cfa8a58a81345ddffc982e4099be557837745f7ccfbb32c7886e68a97886d0 |
| M/output/template/.claude/skills/add-dependency/SKILL.md | 64d6cc423bc904ce3a817501aeac9888ab31730a8992dd560edca632e50e448f | 64d6cc423bc904ce3a817501aeac9888ab31730a8992dd560edca632e50e448f |
| M/output/template/.claude/skills/angular/SKILL.md | 30b07da5e929551fbe240b04fcf8be3756dc440ed9662a22cb41673c56c5d49c | 30b07da5e929551fbe240b04fcf8be3756dc440ed9662a22cb41673c56c5d49c |
| M/output/template/.claude/skills/api-versioning/SKILL.md | bd3fe7bb3a6fdac944e0c893706e4c38346c1c6b23068ded540f777f228412b3 | bd3fe7bb3a6fdac944e0c893706e4c38346c1c6b23068ded540f777f228412b3 |
| M/output/template/.claude/skills/architecture-decision/SKILL.md | 3730f9f1b797addbfa60756289f5f946cf7185289702583982e542333b65398e | 3730f9f1b797addbfa60756289f5f946cf7185289702583982e542333b65398e |
| M/output/template/.claude/skills/aspnet-error-handling/SKILL.md | 80125bb36e31279e83408e9f31c46d6032b2edf83ae026baf6b560cbec0d594a | 80125bb36e31279e83408e9f31c46d6032b2edf83ae026baf6b560cbec0d594a |
| M/output/template/.claude/skills/authentication/SKILL.md | 562880403dc3ab4b94155f46c588f57a078109e3133609dc75dfb74b8478c3a5 | 562880403dc3ab4b94155f46c588f57a078109e3133609dc75dfb74b8478c3a5 |
| M/output/template/.claude/skills/build-fix/SKILL.md | 5e61240c683109862dad08cb6edc133b41f142d3908d2ab02eb0534e98647d30 | 5e61240c683109862dad08cb6edc133b41f142d3908d2ab02eb0534e98647d30 |
| M/output/template/.claude/skills/caching/SKILL.md | b89947910b05c790db0b4fbefe6af93cba66714d79864631ee733a430d685b75 | b89947910b05c790db0b4fbefe6af93cba66714d79864631ee733a430d685b75 |
| M/output/template/.claude/skills/ci-cd/SKILL.md | f610882412dcdd0a6bbb229c2999cba1b68d3c7ab56e5d16c08775dd908fe297 | f610882412dcdd0a6bbb229c2999cba1b68d3c7ab56e5d16c08775dd908fe297 |
| M/output/template/.claude/skills/code-review/SKILL.md | f4316fb509134bc0ccb9c08c37be0453fc6faabc5cbe5b478af032ddf6e0efa6 | f4316fb509134bc0ccb9c08c37be0453fc6faabc5cbe5b478af032ddf6e0efa6 |
| M/output/template/.claude/skills/configuration/SKILL.md | a97b130e4215ef94ca65e68ad66ce5ad400a81c4b6bcb20c468485aedb91ca22 | a97b130e4215ef94ca65e68ad66ce5ad400a81c4b6bcb20c468485aedb91ca22 |
| M/output/template/.claude/skills/custom-settings/SKILL.md | cb637ceaa146dc6d13788a8f97bb8e7485f347ab828af4055af7847f9edb9f78 | cb637ceaa146dc6d13788a8f97bb8e7485f347ab828af4055af7847f9edb9f78 |
| M/output/template/.claude/skills/dependency-injection/SKILL.md | f5d9e7580d5d02e675d9be2ecd5698b82fef7ec6e1ecf5420003b078dcecfaf8 | f5d9e7580d5d02e675d9be2ecd5698b82fef7ec6e1ecf5420003b078dcecfaf8 |
| M/output/template/.claude/skills/development-workflow/SKILL.md | 613bf6825218bc4589e0c9b419246d96b48c7dbaef66142b66abcf9f49a9c781 | 613bf6825218bc4589e0c9b419246d96b48c7dbaef66142b66abcf9f49a9c781 |
| M/output/template/.claude/skills/docker/SKILL.md | 56369fcfc34f4b94ab2c53882767670f3eef293f803843610b01e4da2b0c4479 | 56369fcfc34f4b94ab2c53882767670f3eef293f803843610b01e4da2b0c4479 |
| M/output/template/.claude/skills/dotnet-testing/SKILL.md | 8e4bd9abd8c16b89df2209a1fd9b2058016ec48aa18d1ab66f4b309619f63f5a | 8e4bd9abd8c16b89df2209a1fd9b2058016ec48aa18d1ab66f4b309619f63f5a |
| M/output/template/.claude/skills/ef-core/SKILL.md | 330080f3e286dc07c593cd1d02add2d53e7a3980a026a7bd907590ac82ea7008 | 330080f3e286dc07c593cd1d02add2d53e7a3980a026a7bd907590ac82ea7008 |
| M/output/template/.claude/skills/git-workflow/SKILL.md | 431d3f03476fec3c270db4822cd0a2155fbe8d8a08ad07b3a637b0b32272a6a5 | 431d3f03476fec3c270db4822cd0a2155fbe8d8a08ad07b3a637b0b32272a6a5 |
| M/output/template/.claude/skills/health-check/SKILL.md | 0fda1c624c7fef58e8a697a1994d7b81a4a9a66537c742eb73030b48e7d692dc | 0fda1c624c7fef58e8a697a1994d7b81a4a9a66537c742eb73030b48e7d692dc |
| M/output/template/.claude/skills/http-api/SKILL.md | 3e8f83d3de6a8108a9978a5dbb86fbaf040cca87b78c9b1ade822a7f333255b2 | 3e8f83d3de6a8108a9978a5dbb86fbaf040cca87b78c9b1ade822a7f333255b2 |
| M/output/template/.claude/skills/httpclient-factory/SKILL.md | 46144adb45731740e9ec7c1f77babcc7ccc7f006f8fae679027e14f9515628e8 | 46144adb45731740e9ec7c1f77babcc7ccc7f006f8fae679027e14f9515628e8 |
| M/output/template/.claude/skills/httpclient-factory/references/resilience.md | bb18f33909f8ec3b31b24a4e765170d7e6fea9f1cb3a04db681f19b99c33b394 | bb18f33909f8ec3b31b24a4e765170d7e6fea9f1cb3a04db681f19b99c33b394 |
| M/output/template/.claude/skills/logging/SKILL.md | e4c0e4dace478f0cd2231e2cedd228cb31e6451001e5ab78c1538b3152b1da3e | e4c0e4dace478f0cd2231e2cedd228cb31e6451001e5ab78c1538b3152b1da3e |
| M/output/template/.claude/skills/logging/references/serilog.md | 5a4c2cf8c9497afb0a43835ad71618ff6ff65df439cef9b8df05386342f3772b | 5a4c2cf8c9497afb0a43835ad71618ff6ff65df439cef9b8df05386342f3772b |
| M/output/template/.claude/skills/modern-csharp/SKILL.md | 2fbc4c0a4b7bf5c7e7c8a1942c23434445c5b23e42a7f3730bd84a5cb2e329b4 | 2fbc4c0a4b7bf5c7e7c8a1942c23434445c5b23e42a7f3730bd84a5cb2e329b4 |
| M/output/template/.claude/skills/project-structure/SKILL.md | 3d090c4e7dcb978fcdc4802a9ed575a79f05ddee1c16398953db56241eef0756 | 3d090c4e7dcb978fcdc4802a9ed575a79f05ddee1c16398953db56241eef0756 |
| M/output/template/.claude/skills/project-structure/references/backend-layout.md | ece97dca16f49d116d9bf9002f3472ff68610a8512cdcb507047c85711989229 | ece97dca16f49d116d9bf9002f3472ff68610a8512cdcb507047c85711989229 |
| M/output/template/.claude/skills/project-structure/references/solution-layout.md | bc437d8bb719c84614ea8666e9bfe6a989347794e96daf4f7345d4e3308c4887 | bc437d8bb719c84614ea8666e9bfe6a989347794e96daf4f7345d4e3308c4887 |
| M/output/template/.claude/skills/security-scan/SKILL.md | 8e9bba8217bb44a63af5774d2e4dd3ed79ed1bec424d2f01cf1a43b09cf0e4f4 | 8e9bba8217bb44a63af5774d2e4dd3ed79ed1bec424d2f01cf1a43b09cf0e4f4 |
| M/output/template/.claude/skills/security-scan/references/scan-layers.md | 914450aee2a219afc4c68ae1b1fc958151a9797805c737e6c8d0cc5fb11cfd6f | 914450aee2a219afc4c68ae1b1fc958151a9797805c737e6c8d0cc5fb11cfd6f |
| M/output/template/.claude/skills/swagger/SKILL.md | 83da7161fd1f99c2972edae3c23c88d6001075960b5aa1db8ad2346fd2220cef | 83da7161fd1f99c2972edae3c23c88d6001075960b5aa1db8ad2346fd2220cef |
| M/output/template/.claude/skills/template-maintenance/SKILL.md | a996a94711ac2af5bdeb4234bf6deec6dfdd0e4ea0ebd01737f3386c45d0a94c | a996a94711ac2af5bdeb4234bf6deec6dfdd0e4ea0ebd01737f3386c45d0a94c |
| M/output/template/.claude/skills/verify/SKILL.md | bf874c03329661cf9387eddc4b8492dc02c4722e59f0e45b1ace6c700306dd7f | bf874c03329661cf9387eddc4b8492dc02c4722e59f0e45b1ace6c700306dd7f |
| M/output/template/.editorconfig | 6f93a11256745286b1f15ccb95a3f8715739ffa9835271312fcf8bb3b3677315 | 6f93a11256745286b1f15ccb95a3f8715739ffa9835271312fcf8bb3b3677315 |
| M/output/template/CLAUDE.md | e0145262c1d622cec4001bc545552ab5f11f8e99b98355b2358d79df98f2901d | e0145262c1d622cec4001bc545552ab5f11f8e99b98355b2358d79df98f2901d |
| M/output/template/CUSTOM_SETTINGS.md | 9d30269ddf6559fb1da1ad8fcbcf8024f75eadb373542243559ee8bf49a332a4 | 9d30269ddf6559fb1da1ad8fcbcf8024f75eadb373542243559ee8bf49a332a4 |
| M/output/template/Directory.Build.props | ea04f6e318b3bcb767cd265cbca5970e1580bd543c22fffab222f999830880be | ea04f6e318b3bcb767cd265cbca5970e1580bd543c22fffab222f999830880be |
| M/output/template/Directory.Packages.props | ae5211cfccdd99d540ea3cafec7fe0d2314c2b2fec9e016ba62bd4889b2e4a01 | ae5211cfccdd99d540ea3cafec7fe0d2314c2b2fec9e016ba62bd4889b2e4a01 |
| M/output/template/SPECIFICATION.md | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| M/output/template/docs/technology-stack.md | cc3b4abee5fd8fd0f201128e684b9e1d2a643fc0e98fcce30e9d38218ffed42d | cc3b4abee5fd8fd0f201128e684b9e1d2a643fc0e98fcce30e9d38218ffed42d |
| M1/output/template/.claude/MAP.md | 78e82cfc82f7911efd159e35a53322e2597485b7fabf03157b6fe4a719fb2d1e | 78e82cfc82f7911efd159e35a53322e2597485b7fabf03157b6fe4a719fb2d1e |
| M1/output/template/.claude/agents/code-reviewer.md | c8cb071e84d1bcd3f9f7f2ff791530ce8431300a6857905e95090eb6987c55ee | c8cb071e84d1bcd3f9f7f2ff791530ce8431300a6857905e95090eb6987c55ee |
| M1/output/template/.claude/capabilities/architecture/CONTRACT.md | ae1ce99980edf8d371e18f2a9ca53b376686c82f288115b76c2a0245de20f5e6 | ae1ce99980edf8d371e18f2a9ca53b376686c82f288115b76c2a0245de20f5e6 |
| M1/output/template/.claude/capabilities/architecture/clean-architecture/MODULE.md | f41633f3a8f5b18e866d3db6ecb6f0143a8727d18137fe5405656ff35a99ddf2 | f41633f3a8f5b18e866d3db6ecb6f0143a8727d18137fe5405656ff35a99ddf2 |
| M1/output/template/.claude/capabilities/backend-testing/CONTRACT.md | 4880396b759962d6d54c88b360f1085bc6d4ad53e32e9e4eb4045bba8f3169f7 | 4880396b759962d6d54c88b360f1085bc6d4ad53e32e9e4eb4045bba8f3169f7 |
| M1/output/template/.claude/capabilities/backend-testing/nunit/MODULE.md | 8aa9b0b46a2805a767a732e99bcf35536df1d4bdf60a6682592b9de8c2f6fbb8 | 8aa9b0b46a2805a767a732e99bcf35536df1d4bdf60a6682592b9de8c2f6fbb8 |
| M1/output/template/.claude/capabilities/frontend/CONTRACT.md | 3ae15654a3eaab93344afc0e732da349124dc43468d563454366a767bf6a0c31 | 3ae15654a3eaab93344afc0e732da349124dc43468d563454366a767bf6a0c31 |
| M1/output/template/.claude/capabilities/frontend/angular/MODULE.md | 522a629deb22ce9c8cd1012528b4a0a7fb8e40ccf46022dc66beec20be7ffd6c | 522a629deb22ce9c8cd1012528b4a0a7fb8e40ccf46022dc66beec20be7ffd6c |
| M1/output/template/.claude/capabilities/persistence/CONTRACT.md | f2d54482f7b918f6d63024bf3bf25bc69da7306edd757066a22996d06a0b2be2 | f2d54482f7b918f6d63024bf3bf25bc69da7306edd757066a22996d06a0b2be2 |
| M1/output/template/.claude/capabilities/persistence/ef-core/MODULE.md | 43815c211f24a2a230510b6e44e7a4f62835914bb3f3bcbb95b895914e1b90a7 | 43815c211f24a2a230510b6e44e7a4f62835914bb3f3bcbb95b895914e1b90a7 |
| M1/output/template/.claude/hooks/post-tool-use.js | 0de60c2d7a85b955ee329da0077ebe6aec8cf5d12486f1ac4a51ad47c514df27 | 0de60c2d7a85b955ee329da0077ebe6aec8cf5d12486f1ac4a51ad47c514df27 |
| M1/output/template/.claude/hooks/pre-tool-use.js | 0191df357e55b9b5e957c00cacd608a872122d3d085b8f664a09f4280630c4a6 | 0191df357e55b9b5e957c00cacd608a872122d3d085b8f664a09f4280630c4a6 |
| M1/output/template/.claude/hooks/stop.js | 0709d980e8c9bbf6b1fda9143b6c5bea47eb658b06dd3185c5e816eed3f342a4 | 0709d980e8c9bbf6b1fda9143b6c5bea47eb658b06dd3185c5e816eed3f342a4 |
| M1/output/template/.claude/rules/api.md | 17e82d4a80dfe314d7124e21c113187acc8022205be7ee54bdf4b5972415d9b0 | 17e82d4a80dfe314d7124e21c113187acc8022205be7ee54bdf4b5972415d9b0 |
| M1/output/template/.claude/rules/architecture.md | 47befd19b838669482734d5bc68ba365383c78b88f42e7953452237380b65e3e | 47befd19b838669482734d5bc68ba365383c78b88f42e7953452237380b65e3e |
| M1/output/template/.claude/rules/coding-style.md | 2d29fc5de4409c9f6102a15f46660fe3a90e6d6ceb33a20895af5ba326a754b4 | 2d29fc5de4409c9f6102a15f46660fe3a90e6d6ceb33a20895af5ba326a754b4 |
| M1/output/template/.claude/rules/composition.md | 022f8d31a97ddbaadb483291218a35c49ad06a20ff6bf855f07409581d13d71a | 022f8d31a97ddbaadb483291218a35c49ad06a20ff6bf855f07409581d13d71a |
| M1/output/template/.claude/rules/dependencies.md | 3dbf0e722f18320634bf475e660022ad9264765eed0a81595ea244d79b111536 | 3dbf0e722f18320634bf475e660022ad9264765eed0a81595ea244d79b111536 |
| M1/output/template/.claude/rules/error-handling.md | b08d04da47943695c8f31545330b28f99a2a5dde324b145b93fa4430d54bd505 | b08d04da47943695c8f31545330b28f99a2a5dde324b145b93fa4430d54bd505 |
| M1/output/template/.claude/rules/frontend-framework.md | a98ba47cbb2b6ab84f36f9eb2008ba0506013bb40a6c63bb900b756386393696 | a98ba47cbb2b6ab84f36f9eb2008ba0506013bb40a6c63bb900b756386393696 |
| M1/output/template/.claude/rules/frontend.md | dab838e74bd2972d5ee1f324530bb658935017c31aaf4efdafe6df45fd342c43 | dab838e74bd2972d5ee1f324530bb658935017c31aaf4efdafe6df45fd342c43 |
| M1/output/template/.claude/rules/performance.md | 81123c9e5c73a22ab945b2907f56b442e1e2ebbfb888e7069dc63aee03810bc8 | 81123c9e5c73a22ab945b2907f56b442e1e2ebbfb888e7069dc63aee03810bc8 |
| M1/output/template/.claude/rules/persistence-technology.md | 834517c0a0abab382fcf7f68cd7dc42e596b47cd85c6a43c0f2ceaf08ddb64c1 | 834517c0a0abab382fcf7f68cd7dc42e596b47cd85c6a43c0f2ceaf08ddb64c1 |
| M1/output/template/.claude/rules/physical-structure.md | d50ed162aab9bfd46ff9d88130d8088a92f9754b996d7d770ce00a2321335a78 | d50ed162aab9bfd46ff9d88130d8088a92f9754b996d7d770ce00a2321335a78 |
| M1/output/template/.claude/rules/security.md | 03ea47da1500b73da0b4052096015b375e560b21ec2d1196ac809d1c504b4f68 | 03ea47da1500b73da0b4052096015b375e560b21ec2d1196ac809d1c504b4f68 |
| M1/output/template/.claude/rules/test-framework.md | 411f846c87277fa07326c361381d3dfee125c4818f35af5512060ad378f192e8 | 411f846c87277fa07326c361381d3dfee125c4818f35af5512060ad378f192e8 |
| M1/output/template/.claude/rules/testing.md | f652f51184ef08eb65696802eca20b95cad243d3a16c4997a69e0fb56e3c9752 | f652f51184ef08eb65696802eca20b95cad243d3a16c4997a69e0fb56e3c9752 |
| M1/output/template/.claude/scripts/check-architecture.js | 2821fdbc9ce2fa068ccdf8546303dd2617512fef6ff7dc7ed962f0e0d3591302 | 2821fdbc9ce2fa068ccdf8546303dd2617512fef6ff7dc7ed962f0e0d3591302 |
| M1/output/template/.claude/scripts/check-instructions.js | 98b741da768bc0b9fae40a90858348e0d8d7506708a0fd5f127d759e2915bb51 | 98b741da768bc0b9fae40a90858348e0d8d7506708a0fd5f127d759e2915bb51 |
| M1/output/template/.claude/scripts/check-manifests.js | cdefa0ea4728cbf587c825b3ef10ce21f62857d3bd208f0e64f5f7fa9df77caa | cdefa0ea4728cbf587c825b3ef10ce21f62857d3bd208f0e64f5f7fa9df77caa |
| M1/output/template/.claude/scripts/lib/common.js | a65a47552f8203d5761f7f3a1dd40c95548736e349a7f4554184818d7996eef6 | a65a47552f8203d5761f7f3a1dd40c95548736e349a7f4554184818d7996eef6 |
| M1/output/template/.claude/scripts/lib/dependency-commands.js | 62efa646f2bd289b78afa640b010692d747392caf57e0005ae5b119a5ec00aa6 | 62efa646f2bd289b78afa640b010692d747392caf57e0005ae5b119a5ec00aa6 |
| M1/output/template/.claude/scripts/lib/hook-output.js | f8a135e48ff5bd197cebb651eadf82d8802bfb97f8317498a089ad557b51c36d | f8a135e48ff5bd197cebb651eadf82d8802bfb97f8317498a089ad557b51c36d |
| M1/output/template/.claude/settings.json | 7ea3bfbc19f22a53ea491ea9dcc74f0f685c196be8e54f6bfcd4509c224f09e8 | 7ea3bfbc19f22a53ea491ea9dcc74f0f685c196be8e54f6bfcd4509c224f09e8 |
| M1/output/template/.claude/skills/add-dependency/SKILL.md | 559ab9eb214e7026a6be86630fe062b4d492e1e540ce0a7402caed0beded5940 | 559ab9eb214e7026a6be86630fe062b4d492e1e540ce0a7402caed0beded5940 |
| M1/output/template/.claude/skills/angular/SKILL.md | c23ef863d7c54a3a96a2313c39818dd8a15a55807d342550827bd4faa611f332 | c23ef863d7c54a3a96a2313c39818dd8a15a55807d342550827bd4faa611f332 |
| M1/output/template/.claude/skills/api-versioning/SKILL.md | 42e0ab731763150615bb8dcec009cf9f329bed32ad83463ebfa058631b835d5b | 42e0ab731763150615bb8dcec009cf9f329bed32ad83463ebfa058631b835d5b |
| M1/output/template/.claude/skills/architecture-decision/SKILL.md | da438e9194a15f7c2aa4a833ab9fa7b34760bd947f11ffcce30c850ec1a4eb83 | da438e9194a15f7c2aa4a833ab9fa7b34760bd947f11ffcce30c850ec1a4eb83 |
| M1/output/template/.claude/skills/aspnet-error-handling/SKILL.md | 390ed03c66e07c941c553a41a219a1c80f0c97c46e11879abaf11557cb3e3e6d | 390ed03c66e07c941c553a41a219a1c80f0c97c46e11879abaf11557cb3e3e6d |
| M1/output/template/.claude/skills/authentication/SKILL.md | ae0328872b410c53e89fb88f7fe9c23f7553c346c3da47fcf282a251b06110f8 | ae0328872b410c53e89fb88f7fe9c23f7553c346c3da47fcf282a251b06110f8 |
| M1/output/template/.claude/skills/build-fix/SKILL.md | 786ae2de6a8e194d8656b122305a00393739cc4ebbd9512a6991962814162773 | 786ae2de6a8e194d8656b122305a00393739cc4ebbd9512a6991962814162773 |
| M1/output/template/.claude/skills/caching/SKILL.md | 63667f662d9a587af2f52880f3288e7b333453ea161e2fc1998f6877448635d3 | 63667f662d9a587af2f52880f3288e7b333453ea161e2fc1998f6877448635d3 |
| M1/output/template/.claude/skills/ci-cd/SKILL.md | d401ec4219271f7e5b78e97aa049239849d69efc09616a78da96011d8762a76b | d401ec4219271f7e5b78e97aa049239849d69efc09616a78da96011d8762a76b |
| M1/output/template/.claude/skills/code-review/SKILL.md | 99d4a418e4be517c87940745cc3287bad6bd3f2634c23fd4570886f4c6a78dcd | 99d4a418e4be517c87940745cc3287bad6bd3f2634c23fd4570886f4c6a78dcd |
| M1/output/template/.claude/skills/configuration/SKILL.md | 6a73074e7ab30f915ce8a9f5f1a47a0d9df74eac8e7ba730d64d5d444dcaa796 | 6a73074e7ab30f915ce8a9f5f1a47a0d9df74eac8e7ba730d64d5d444dcaa796 |
| M1/output/template/.claude/skills/custom-settings/SKILL.md | 25d15c62c8f3d613f35ce7e5baf1f602448295eda9adc38662b38751d8dd6147 | 25d15c62c8f3d613f35ce7e5baf1f602448295eda9adc38662b38751d8dd6147 |
| M1/output/template/.claude/skills/dependency-injection/SKILL.md | 21c062236b8da570c1e8066b8c186afc17154a859ab7ff8390b77c4f7ed42716 | 21c062236b8da570c1e8066b8c186afc17154a859ab7ff8390b77c4f7ed42716 |
| M1/output/template/.claude/skills/development-workflow/SKILL.md | f5ea2951cb6e0ea2d2b48deb713954fa4421c3bdff32604075cbe02666fdb061 | f5ea2951cb6e0ea2d2b48deb713954fa4421c3bdff32604075cbe02666fdb061 |
| M1/output/template/.claude/skills/docker/SKILL.md | d7bfe18ef6cb1925e82d50fdf2cca483da7906e05da14af9f738d14d799e3676 | d7bfe18ef6cb1925e82d50fdf2cca483da7906e05da14af9f738d14d799e3676 |
| M1/output/template/.claude/skills/dotnet-testing/SKILL.md | 74f7730c96ff76a24df774a5ef49c00edef0d88db2c8b609e1e6d1cd4688d73c | 74f7730c96ff76a24df774a5ef49c00edef0d88db2c8b609e1e6d1cd4688d73c |
| M1/output/template/.claude/skills/ef-core/SKILL.md | 525cf3a7b08e10d66d0e8734d0f24d85796a42778bf8095c45e84a343efa6b46 | 525cf3a7b08e10d66d0e8734d0f24d85796a42778bf8095c45e84a343efa6b46 |
| M1/output/template/.claude/skills/git-workflow/SKILL.md | a32e536b06d3c86115c83345e48e80a83abcc2b12fe446858e7aa711dce57146 | a32e536b06d3c86115c83345e48e80a83abcc2b12fe446858e7aa711dce57146 |
| M1/output/template/.claude/skills/health-check/SKILL.md | 55d832a245a07dde050131eaa4a1fb49aeca525e4380959fd11c58320563d99f | 55d832a245a07dde050131eaa4a1fb49aeca525e4380959fd11c58320563d99f |
| M1/output/template/.claude/skills/http-api/SKILL.md | 9f1aa1b96b64eca35392efa2879046b2d65674b1b3c614a666634e23c1a10d42 | 9f1aa1b96b64eca35392efa2879046b2d65674b1b3c614a666634e23c1a10d42 |
| M1/output/template/.claude/skills/httpclient-factory/SKILL.md | c5c47fad8ebaed5cb81360ace0af3528db27f000de59a0125d4b284ab5a72021 | c5c47fad8ebaed5cb81360ace0af3528db27f000de59a0125d4b284ab5a72021 |
| M1/output/template/.claude/skills/httpclient-factory/references/resilience.md | 64c7146593bb7a10bd22274e8f81aaa4045d4ed24b708519aa35e596c27dd164 | 64c7146593bb7a10bd22274e8f81aaa4045d4ed24b708519aa35e596c27dd164 |
| M1/output/template/.claude/skills/logging/SKILL.md | fd04a4772e3a8b7d3f261a9151a510200a1a4368cd4640b9d8c54b409f17937b | fd04a4772e3a8b7d3f261a9151a510200a1a4368cd4640b9d8c54b409f17937b |
| M1/output/template/.claude/skills/logging/references/serilog.md | e2ec57d45a57a084ad57ff99d5a104f25e76266c2fcbeeda92845bee28615194 | e2ec57d45a57a084ad57ff99d5a104f25e76266c2fcbeeda92845bee28615194 |
| M1/output/template/.claude/skills/modern-csharp/SKILL.md | 5e70bb4d21ec54348caf076dec0cd6d925fe632046eae72965787fc640cf07b6 | 5e70bb4d21ec54348caf076dec0cd6d925fe632046eae72965787fc640cf07b6 |
| M1/output/template/.claude/skills/persistence-change/SKILL.md | 9b7817ffe03c7b19ad93c81a6c8462f39a6b01a2122271cd3a87c7dd3a980297 | 9b7817ffe03c7b19ad93c81a6c8462f39a6b01a2122271cd3a87c7dd3a980297 |
| M1/output/template/.claude/skills/project-structure/SKILL.md | 140a4c74cabdd0a3bbad2c293274b67eb51bd21e459b488a85ae641b5161d16d | 140a4c74cabdd0a3bbad2c293274b67eb51bd21e459b488a85ae641b5161d16d |
| M1/output/template/.claude/skills/project-structure/references/backend-layout.md | 6fc29e22beed0fa1baa8ce363a8cc5bc537ab55d877b3f249c8ade7d3e00f484 | 6fc29e22beed0fa1baa8ce363a8cc5bc537ab55d877b3f249c8ade7d3e00f484 |
| M1/output/template/.claude/skills/project-structure/references/solution-layout.md | debed515aca169b17d34fd2567c28b990ce077b88900682ffedc8b5d080c9142 | debed515aca169b17d34fd2567c28b990ce077b88900682ffedc8b5d080c9142 |
| M1/output/template/.claude/skills/security-scan/SKILL.md | afb8e9da26a75dc921bbc7481aabd33022a999a8ec4a87b74b26b13972fcc653 | afb8e9da26a75dc921bbc7481aabd33022a999a8ec4a87b74b26b13972fcc653 |
| M1/output/template/.claude/skills/security-scan/references/scan-layers.md | 2d36ae051cf2531af10cc7bd2bcb257632c236dbd2b1b8e369e29d07dc9b55e1 | 2d36ae051cf2531af10cc7bd2bcb257632c236dbd2b1b8e369e29d07dc9b55e1 |
| M1/output/template/.claude/skills/swagger/SKILL.md | ceabb98792f653174dc8009590caed3eb72e626744a681961a98cda7927d2f7a | ceabb98792f653174dc8009590caed3eb72e626744a681961a98cda7927d2f7a |
| M1/output/template/.claude/skills/template-maintenance/SKILL.md | 91e9ba6989a0ff58718d9ead9fcb71b989509c6862ed724d5a8d62e2568fa06c | 91e9ba6989a0ff58718d9ead9fcb71b989509c6862ed724d5a8d62e2568fa06c |
| M1/output/template/.claude/skills/verify/SKILL.md | b362c4d7ceb2abd772e2c779ec0c37a015c1a5b45fdcfb37e04adcd5535197bb | b362c4d7ceb2abd772e2c779ec0c37a015c1a5b45fdcfb37e04adcd5535197bb |
| M1/output/template/.editorconfig | 66b2afe11b9cc2bb23f7c11570084528e4e426ca514f5859345fb221946bd296 | 66b2afe11b9cc2bb23f7c11570084528e4e426ca514f5859345fb221946bd296 |
| M1/output/template/CLAUDE.md | a03da6d325cc03c26bc51c83c19f429fcf239b6419cf4fcde7b6c8f685181fdb | a03da6d325cc03c26bc51c83c19f429fcf239b6419cf4fcde7b6c8f685181fdb |
| M1/output/template/CUSTOM_SETTINGS.md | 125b0be16f28ec632633a2b3f7bb25f43e51d105a7277f2dd8a1ba554ce27284 | 125b0be16f28ec632633a2b3f7bb25f43e51d105a7277f2dd8a1ba554ce27284 |
| M1/output/template/Directory.Build.props | 12a91564368ec59fb260772b84d7b5286a93007cbe44b9c2847633aedee51bd1 | 12a91564368ec59fb260772b84d7b5286a93007cbe44b9c2847633aedee51bd1 |
| M1/output/template/Directory.Packages.props | 52ecf7808eb1b240b57e3eb6560eb57d0167bc61792fef9f6fdb34b31fc23016 | 52ecf7808eb1b240b57e3eb6560eb57d0167bc61792fef9f6fdb34b31fc23016 |
| M1/output/template/SPECIFICATION.md | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| M1/output/template/docs/capabilities/architecture.md | f17ee5004ee8df3ac13f0eef262cddbe45d893b9b06c14b50b57f1e5f933baf8 | f17ee5004ee8df3ac13f0eef262cddbe45d893b9b06c14b50b57f1e5f933baf8 |
| M1/output/template/docs/capabilities/backend-testing.md | 1acd968fd17308d4e6c8e19380029a7cd8f7ac8e79b3c5f91e93a37657e42592 | 1acd968fd17308d4e6c8e19380029a7cd8f7ac8e79b3c5f91e93a37657e42592 |
| M1/output/template/docs/capabilities/frontend.md | 9e36e66e52d08754bdb4153f41d5c1f4afabf86edc803e5042505283bae6dd34 | 9e36e66e52d08754bdb4153f41d5c1f4afabf86edc803e5042505283bae6dd34 |
| M1/output/template/docs/capabilities/persistence.md | bf305fee73c5c78fcad8eeeaf7c7f14954b97db47dc401075d02ea15835c62b0 | bf305fee73c5c78fcad8eeeaf7c7f14954b97db47dc401075d02ea15835c62b0 |
| M1/output/template/docs/capability-selection.md | 82d4e2e63e72986407ff475aca9c078462cc3e7a0264ac4723f7ceea333966b6 | 82d4e2e63e72986407ff475aca9c078462cc3e7a0264ac4723f7ceea333966b6 |
| M1/output/template/docs/technology-stack.md | 58ec2a08956b2c0f899ea009f1b67d9b05fb85d935a0a0c59bdf8559a3fab993 | 58ec2a08956b2c0f899ea009f1b67d9b05fb85d935a0a0c59bdf8559a3fab993 |

### Snapshotted source and contract inputs

These files were hashed before tests and compared again after. No mismatch was found. The source set is identical across candidates; candidate architecture/task/provenance files are intentionally candidate-specific.

| Relative path | Before SHA-256 | After SHA-256 |
|---|---|---|
| K0/CANDIDATE.md | 67fdac9d0806af4a154d2b79a1607d1277012029d0df6529bd3c2c62435d7a54 | 67fdac9d0806af4a154d2b79a1607d1277012029d0df6529bd3c2c62435d7a54 |
| K0/PROVENANCE.json | d442b623bc0138cc69364d292b4e60a22d08bdfb4d8964addb49503008c3a508 | d442b623bc0138cc69364d292b4e60a22d08bdfb4d8964addb49503008c3a508 |
| K0/README.md | cb1a02ec4b22d8b5f7d78b2bbd19da5171aa18ec8015fd8bd6b8480037f809cd | cb1a02ec4b22d8b5f7d78b2bbd19da5171aa18ec8015fd8bd6b8480037f809cd |
| K0/REFINEMENT_TASK.md | 38bfd3077c007a4643782028da26d79c5197425443ab4b9d7543d0c4d8054b29 | 38bfd3077c007a4643782028da26d79c5197425443ab4b9d7543d0c4d8054b29 |
| K0/baseline/CANDIDATE.md | 67fdac9d0806af4a154d2b79a1607d1277012029d0df6529bd3c2c62435d7a54 | 67fdac9d0806af4a154d2b79a1607d1277012029d0df6529bd3c2c62435d7a54 |
| K0/baseline/TASK.md | 579b723fde56866f0f8dcc30a619ad6abae8579622c0af102054604baef81a5c | 579b723fde56866f0f8dcc30a619ad6abae8579622c0af102054604baef81a5c |
| K0/source/inventory.json | bcf1a1532437f4a1d7bfafcb1f27ebcbb832ba684e35b8a42569cd9d2d9ad168 | bcf1a1532437f4a1d7bfafcb1f27ebcbb832ba684e35b8a42569cd9d2d9ad168 |
| K0/source/shared-research-invariants.json | 51b442b118b55ea89e16f3ac8603309d66635a7d184e456af2091d584f7da6d7 | 51b442b118b55ea89e16f3ac8603309d66635a7d184e456af2091d584f7da6d7 |
| K0/source/v2-baseline/.claude/agents/code-reviewer.md | 4f0f431e823eb7bb239be953d88ca74d1f9755c360d5d3d7b8355416de3528aa | 4f0f431e823eb7bb239be953d88ca74d1f9755c360d5d3d7b8355416de3528aa |
| K0/source/v2-baseline/.claude/rules/architecture.md | ced5b2a4e8e5e48a9023c89183ad9e46a637b881312e7f0d8925933ba5d40c7c | ced5b2a4e8e5e48a9023c89183ad9e46a637b881312e7f0d8925933ba5d40c7c |
| K0/source/v2-baseline/.claude/rules/coding-style.md | 48d906d335083f43a7f6c8bc62d24c34d569fbcfe04f42098623d257b1ff7390 | 48d906d335083f43a7f6c8bc62d24c34d569fbcfe04f42098623d257b1ff7390 |
| K0/source/v2-baseline/.claude/rules/dependencies.md | ced0516f065e25a36ea07d766865f26caae8d133a0bb1aca2976532ff62b6468 | ced0516f065e25a36ea07d766865f26caae8d133a0bb1aca2976532ff62b6468 |
| K0/source/v2-baseline/.claude/rules/error-handling.md | e54a59066bebc10832df82c8d818d8fa27dffd0de73706666198f5c0fcd491ea | e54a59066bebc10832df82c8d818d8fa27dffd0de73706666198f5c0fcd491ea |
| K0/source/v2-baseline/.claude/rules/performance.md | a4b54767111fefd9faae6ba7460e3abacf1ca9258ee1d265ac4eed496589c8b5 | a4b54767111fefd9faae6ba7460e3abacf1ca9258ee1d265ac4eed496589c8b5 |
| K0/source/v2-baseline/.claude/rules/security.md | d36e103f0fa842d038ba739a40e872fc768128a0a6a5474924e3b19a77640ac5 | d36e103f0fa842d038ba739a40e872fc768128a0a6a5474924e3b19a77640ac5 |
| K0/source/v2-baseline/.claude/rules/testing.md | 9c70dc874660db95c4c2032e80b575ea699ea1f514d946b36884c5c157cf0004 | 9c70dc874660db95c4c2032e80b575ea699ea1f514d946b36884c5c157cf0004 |
| K0/source/v2-baseline/.claude/skills/angular/SKILL.md | f4cf7baa3f7479f8d4df588dbbed75e96ff0c612caec199e283cdab13ccfd48e | f4cf7baa3f7479f8d4df588dbbed75e96ff0c612caec199e283cdab13ccfd48e |
| K0/source/v2-baseline/.claude/skills/api-versioning/SKILL.md | 2850c5e2f14d32aa049a1dd6b3983147bfa390d117176c8ce1f54c8eabedb892 | 2850c5e2f14d32aa049a1dd6b3983147bfa390d117176c8ce1f54c8eabedb892 |
| K0/source/v2-baseline/.claude/skills/authentication/SKILL.md | b08285e27eafd8f1b2d09a56f386c1f64a637af17dc097ecd2ffeb32c83e6191 | b08285e27eafd8f1b2d09a56f386c1f64a637af17dc097ecd2ffeb32c83e6191 |
| K0/source/v2-baseline/.claude/skills/build-fix/SKILL.md | 523ad63287ccdf6fa23941a5f6463c46e3ec17c1ed56fe6871f74e480c6ba9a2 | 523ad63287ccdf6fa23941a5f6463c46e3ec17c1ed56fe6871f74e480c6ba9a2 |
| K0/source/v2-baseline/.claude/skills/caching/SKILL.md | f4a8f3e028fc8152dfa30f2cedf30065906e3cea0189f23434dbd7487903bfd9 | f4a8f3e028fc8152dfa30f2cedf30065906e3cea0189f23434dbd7487903bfd9 |
| K0/source/v2-baseline/.claude/skills/ci-cd/SKILL.md | a914ababf5322baccea2549d55f222ee0d617c0be10c0fc37602b74472924f37 | a914ababf5322baccea2549d55f222ee0d617c0be10c0fc37602b74472924f37 |
| K0/source/v2-baseline/.claude/skills/code-review/SKILL.md | fdc0e9075d8379f9deea59174cb1b96f3f8e7a3b4085ab3c9f3ec4911b252f29 | fdc0e9075d8379f9deea59174cb1b96f3f8e7a3b4085ab3c9f3ec4911b252f29 |
| K0/source/v2-baseline/.claude/skills/configuration/SKILL.md | 340f98c96e329b770876bcd3bcfb1b84fe6c9b6477c96de767c3e24de21b2cd5 | 340f98c96e329b770876bcd3bcfb1b84fe6c9b6477c96de767c3e24de21b2cd5 |
| K0/source/v2-baseline/.claude/skills/custom-settings/SKILL.md | d4f76aeaa1597cd1ff7db33ea4d3d02fba4993cb97c8fefecdee23a0dbde6efb | d4f76aeaa1597cd1ff7db33ea4d3d02fba4993cb97c8fefecdee23a0dbde6efb |
| K0/source/v2-baseline/.claude/skills/dependency-injection/SKILL.md | bfac9b98b287bd8a0cc3a370eb521396a728b4ef8b4b53fb2e8c83282d57fade | bfac9b98b287bd8a0cc3a370eb521396a728b4ef8b4b53fb2e8c83282d57fade |
| K0/source/v2-baseline/.claude/skills/docker/SKILL.md | 801e00dd34525bafe3c53618a5f3751b228c6eb7607a06a1c3f6f2fc1197958f | 801e00dd34525bafe3c53618a5f3751b228c6eb7607a06a1c3f6f2fc1197958f |
| K0/source/v2-baseline/.claude/skills/ef-core/SKILL.md | c7120367231bd0bc3b6f92997f6f7450b9441c15604356651447d26cee67d762 | c7120367231bd0bc3b6f92997f6f7450b9441c15604356651447d26cee67d762 |
| K0/source/v2-baseline/.claude/skills/error-handling/SKILL.md | 4d514f0eec953ed9ba85d37f353ccc22b84a6137e9685e180bd2a250aa657b9d | 4d514f0eec953ed9ba85d37f353ccc22b84a6137e9685e180bd2a250aa657b9d |
| K0/source/v2-baseline/.claude/skills/git-workflow/SKILL.md | 940365f04436f41558ba951a3cd6a0dd77cc2e742314950f996962b08dc9bbc2 | 940365f04436f41558ba951a3cd6a0dd77cc2e742314950f996962b08dc9bbc2 |
| K0/source/v2-baseline/.claude/skills/health-check/SKILL.md | cb0c32f0a6bf5b7ffcac2a2d83bce3f4c236d6d89cd01fc1b5abad57a5435e8f | cb0c32f0a6bf5b7ffcac2a2d83bce3f4c236d6d89cd01fc1b5abad57a5435e8f |
| K0/source/v2-baseline/.claude/skills/http-api/SKILL.md | fd39b06310c679a0ea19ca4b86849319607f4b4abf6293106cdad08324fb8d89 | fd39b06310c679a0ea19ca4b86849319607f4b4abf6293106cdad08324fb8d89 |
| K0/source/v2-baseline/.claude/skills/httpclient-factory/SKILL.md | b6e17dcce8b801ae767545059c27a84cf425afb7c7f3fdb003cc481cd0466046 | b6e17dcce8b801ae767545059c27a84cf425afb7c7f3fdb003cc481cd0466046 |
| K0/source/v2-baseline/.claude/skills/logging/SKILL.md | cf8aa215f0f42d91c81fb0ee034b17da2841b156a4388ae372320883bda3868b | cf8aa215f0f42d91c81fb0ee034b17da2841b156a4388ae372320883bda3868b |
| K0/source/v2-baseline/.claude/skills/modern-csharp/SKILL.md | 1156651dbbb5dd51bc81a75f9236b3193198b54603ff941042b35bffce5fcc8c | 1156651dbbb5dd51bc81a75f9236b3193198b54603ff941042b35bffce5fcc8c |
| K0/source/v2-baseline/.claude/skills/project-structure/SKILL.md | d34f37f552adfbded3ec1b4b3b4c2e637a73ae36c74de14f2d67ab90528892cc | d34f37f552adfbded3ec1b4b3b4c2e637a73ae36c74de14f2d67ab90528892cc |
| K0/source/v2-baseline/.claude/skills/project-structure/references/backend-layout.md | 657c469b3be1a91827a1d78463f576d8dcfc069d70461e25097f37ba6f101650 | 657c469b3be1a91827a1d78463f576d8dcfc069d70461e25097f37ba6f101650 |
| K0/source/v2-baseline/.claude/skills/project-structure/references/solution-layout.md | 4c37997519285e15e74114adb0cb5ea26e90643750fd0c8d9d7ba75bc8eb4cbe | 4c37997519285e15e74114adb0cb5ea26e90643750fd0c8d9d7ba75bc8eb4cbe |
| K0/source/v2-baseline/.claude/skills/project-structure/references/technology-stack.md | f51d9b3e85b629b300b253555b7672a98a87cf5cb4197f593c8df3dea7962309 | f51d9b3e85b629b300b253555b7672a98a87cf5cb4197f593c8df3dea7962309 |
| K0/source/v2-baseline/.claude/skills/resilience/SKILL.md | a469c3456673622b4ca4eaa56dd05b803c18bb4c3af04e62ae6e0d784e025811 | a469c3456673622b4ca4eaa56dd05b803c18bb4c3af04e62ae6e0d784e025811 |
| K0/source/v2-baseline/.claude/skills/security-scan/SKILL.md | 4276a267d87d3611a6953c97678dd57693e4422a46dd4d0e82b8d630d02d05c2 | 4276a267d87d3611a6953c97678dd57693e4422a46dd4d0e82b8d630d02d05c2 |
| K0/source/v2-baseline/.claude/skills/security-scan/references/scan-layers.md | 4fe7396896e35e3d83f0b5c86a9046fd0278c5f38783581d0a744cb1a40fa846 | 4fe7396896e35e3d83f0b5c86a9046fd0278c5f38783581d0a744cb1a40fa846 |
| K0/source/v2-baseline/.claude/skills/serilog/SKILL.md | b3c2ab9cf5f89d5d506ffccf6140f5b06cc7b9f434206efb061ca69fa063d6d8 | b3c2ab9cf5f89d5d506ffccf6140f5b06cc7b9f434206efb061ca69fa063d6d8 |
| K0/source/v2-baseline/.claude/skills/swagger/SKILL.md | 7fe6fb21e419811282a0fe4a69b255dbe4cf39868d25932cf0cf07e1a596267d | 7fe6fb21e419811282a0fe4a69b255dbe4cf39868d25932cf0cf07e1a596267d |
| K0/source/v2-baseline/.claude/skills/testing/SKILL.md | 282c7a7185cc13992b20e6a22119dfb4803a1ebf69e4446042f9cdd343b88a9e | 282c7a7185cc13992b20e6a22119dfb4803a1ebf69e4446042f9cdd343b88a9e |
| K0/source/v2-baseline/.claude/skills/verify/SKILL.md | 38042cd665e1958a28290dcb4722aeb0ccb2f01c577a2a52203826ed237acf66 | 38042cd665e1958a28290dcb4722aeb0ccb2f01c577a2a52203826ed237acf66 |
| K0/source/v2-baseline/CLAUDE.md | 5d98d7aeedcde20ba044cc8b49cb0c4206d14fa478afca45c8a56f76e85bb4f4 | 5d98d7aeedcde20ba044cc8b49cb0c4206d14fa478afca45c8a56f76e85bb4f4 |
| K0/source/v2-baseline/CUSTOM_SETTINGS.md | 2449b93c170786e5525809aaf91ded093f2c00375defe7c349a85ad791b6ac4a | 2449b93c170786e5525809aaf91ded093f2c00375defe7c349a85ad791b6ac4a |
| K0/source/v2-baseline/SPECIFICATION.md | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| K1/CANDIDATE.md | 4c898fc26a300c04ba5948e755447146e7883b5f126b52624c173b0a53bc7a9c | 4c898fc26a300c04ba5948e755447146e7883b5f126b52624c173b0a53bc7a9c |
| K1/PROVENANCE.json | fc5ad49f7037b95beefaf248cab3cdd66dee1a09090ba5698ed336f6df140f7a | fc5ad49f7037b95beefaf248cab3cdd66dee1a09090ba5698ed336f6df140f7a |
| K1/README.md | 2c8bb5490f31d0d4d9f06f92c0c2ee952b1574bb81f87b18331b2c560e92f1e7 | 2c8bb5490f31d0d4d9f06f92c0c2ee952b1574bb81f87b18331b2c560e92f1e7 |
| K1/REFINEMENT_TASK.md | 3533f559e5274577e2d7ebf9ba9c82ca8ec8e6bd1f337d8f38cfc9cdad4fb0b5 | 3533f559e5274577e2d7ebf9ba9c82ca8ec8e6bd1f337d8f38cfc9cdad4fb0b5 |
| K1/baseline/CANDIDATE.md | 4c898fc26a300c04ba5948e755447146e7883b5f126b52624c173b0a53bc7a9c | 4c898fc26a300c04ba5948e755447146e7883b5f126b52624c173b0a53bc7a9c |
| K1/baseline/TASK.md | 579b723fde56866f0f8dcc30a619ad6abae8579622c0af102054604baef81a5c | 579b723fde56866f0f8dcc30a619ad6abae8579622c0af102054604baef81a5c |
| K1/source/inventory.json | bcf1a1532437f4a1d7bfafcb1f27ebcbb832ba684e35b8a42569cd9d2d9ad168 | bcf1a1532437f4a1d7bfafcb1f27ebcbb832ba684e35b8a42569cd9d2d9ad168 |
| K1/source/shared-research-invariants.json | 51b442b118b55ea89e16f3ac8603309d66635a7d184e456af2091d584f7da6d7 | 51b442b118b55ea89e16f3ac8603309d66635a7d184e456af2091d584f7da6d7 |
| K1/source/v2-baseline/.claude/agents/code-reviewer.md | 4f0f431e823eb7bb239be953d88ca74d1f9755c360d5d3d7b8355416de3528aa | 4f0f431e823eb7bb239be953d88ca74d1f9755c360d5d3d7b8355416de3528aa |
| K1/source/v2-baseline/.claude/rules/architecture.md | ced5b2a4e8e5e48a9023c89183ad9e46a637b881312e7f0d8925933ba5d40c7c | ced5b2a4e8e5e48a9023c89183ad9e46a637b881312e7f0d8925933ba5d40c7c |
| K1/source/v2-baseline/.claude/rules/coding-style.md | 48d906d335083f43a7f6c8bc62d24c34d569fbcfe04f42098623d257b1ff7390 | 48d906d335083f43a7f6c8bc62d24c34d569fbcfe04f42098623d257b1ff7390 |
| K1/source/v2-baseline/.claude/rules/dependencies.md | ced0516f065e25a36ea07d766865f26caae8d133a0bb1aca2976532ff62b6468 | ced0516f065e25a36ea07d766865f26caae8d133a0bb1aca2976532ff62b6468 |
| K1/source/v2-baseline/.claude/rules/error-handling.md | e54a59066bebc10832df82c8d818d8fa27dffd0de73706666198f5c0fcd491ea | e54a59066bebc10832df82c8d818d8fa27dffd0de73706666198f5c0fcd491ea |
| K1/source/v2-baseline/.claude/rules/performance.md | a4b54767111fefd9faae6ba7460e3abacf1ca9258ee1d265ac4eed496589c8b5 | a4b54767111fefd9faae6ba7460e3abacf1ca9258ee1d265ac4eed496589c8b5 |
| K1/source/v2-baseline/.claude/rules/security.md | d36e103f0fa842d038ba739a40e872fc768128a0a6a5474924e3b19a77640ac5 | d36e103f0fa842d038ba739a40e872fc768128a0a6a5474924e3b19a77640ac5 |
| K1/source/v2-baseline/.claude/rules/testing.md | 9c70dc874660db95c4c2032e80b575ea699ea1f514d946b36884c5c157cf0004 | 9c70dc874660db95c4c2032e80b575ea699ea1f514d946b36884c5c157cf0004 |
| K1/source/v2-baseline/.claude/skills/angular/SKILL.md | f4cf7baa3f7479f8d4df588dbbed75e96ff0c612caec199e283cdab13ccfd48e | f4cf7baa3f7479f8d4df588dbbed75e96ff0c612caec199e283cdab13ccfd48e |
| K1/source/v2-baseline/.claude/skills/api-versioning/SKILL.md | 2850c5e2f14d32aa049a1dd6b3983147bfa390d117176c8ce1f54c8eabedb892 | 2850c5e2f14d32aa049a1dd6b3983147bfa390d117176c8ce1f54c8eabedb892 |
| K1/source/v2-baseline/.claude/skills/authentication/SKILL.md | b08285e27eafd8f1b2d09a56f386c1f64a637af17dc097ecd2ffeb32c83e6191 | b08285e27eafd8f1b2d09a56f386c1f64a637af17dc097ecd2ffeb32c83e6191 |
| K1/source/v2-baseline/.claude/skills/build-fix/SKILL.md | 523ad63287ccdf6fa23941a5f6463c46e3ec17c1ed56fe6871f74e480c6ba9a2 | 523ad63287ccdf6fa23941a5f6463c46e3ec17c1ed56fe6871f74e480c6ba9a2 |
| K1/source/v2-baseline/.claude/skills/caching/SKILL.md | f4a8f3e028fc8152dfa30f2cedf30065906e3cea0189f23434dbd7487903bfd9 | f4a8f3e028fc8152dfa30f2cedf30065906e3cea0189f23434dbd7487903bfd9 |
| K1/source/v2-baseline/.claude/skills/ci-cd/SKILL.md | a914ababf5322baccea2549d55f222ee0d617c0be10c0fc37602b74472924f37 | a914ababf5322baccea2549d55f222ee0d617c0be10c0fc37602b74472924f37 |
| K1/source/v2-baseline/.claude/skills/code-review/SKILL.md | fdc0e9075d8379f9deea59174cb1b96f3f8e7a3b4085ab3c9f3ec4911b252f29 | fdc0e9075d8379f9deea59174cb1b96f3f8e7a3b4085ab3c9f3ec4911b252f29 |
| K1/source/v2-baseline/.claude/skills/configuration/SKILL.md | 340f98c96e329b770876bcd3bcfb1b84fe6c9b6477c96de767c3e24de21b2cd5 | 340f98c96e329b770876bcd3bcfb1b84fe6c9b6477c96de767c3e24de21b2cd5 |
| K1/source/v2-baseline/.claude/skills/custom-settings/SKILL.md | d4f76aeaa1597cd1ff7db33ea4d3d02fba4993cb97c8fefecdee23a0dbde6efb | d4f76aeaa1597cd1ff7db33ea4d3d02fba4993cb97c8fefecdee23a0dbde6efb |
| K1/source/v2-baseline/.claude/skills/dependency-injection/SKILL.md | bfac9b98b287bd8a0cc3a370eb521396a728b4ef8b4b53fb2e8c83282d57fade | bfac9b98b287bd8a0cc3a370eb521396a728b4ef8b4b53fb2e8c83282d57fade |
| K1/source/v2-baseline/.claude/skills/docker/SKILL.md | 801e00dd34525bafe3c53618a5f3751b228c6eb7607a06a1c3f6f2fc1197958f | 801e00dd34525bafe3c53618a5f3751b228c6eb7607a06a1c3f6f2fc1197958f |
| K1/source/v2-baseline/.claude/skills/ef-core/SKILL.md | c7120367231bd0bc3b6f92997f6f7450b9441c15604356651447d26cee67d762 | c7120367231bd0bc3b6f92997f6f7450b9441c15604356651447d26cee67d762 |
| K1/source/v2-baseline/.claude/skills/error-handling/SKILL.md | 4d514f0eec953ed9ba85d37f353ccc22b84a6137e9685e180bd2a250aa657b9d | 4d514f0eec953ed9ba85d37f353ccc22b84a6137e9685e180bd2a250aa657b9d |
| K1/source/v2-baseline/.claude/skills/git-workflow/SKILL.md | 940365f04436f41558ba951a3cd6a0dd77cc2e742314950f996962b08dc9bbc2 | 940365f04436f41558ba951a3cd6a0dd77cc2e742314950f996962b08dc9bbc2 |
| K1/source/v2-baseline/.claude/skills/health-check/SKILL.md | cb0c32f0a6bf5b7ffcac2a2d83bce3f4c236d6d89cd01fc1b5abad57a5435e8f | cb0c32f0a6bf5b7ffcac2a2d83bce3f4c236d6d89cd01fc1b5abad57a5435e8f |
| K1/source/v2-baseline/.claude/skills/http-api/SKILL.md | fd39b06310c679a0ea19ca4b86849319607f4b4abf6293106cdad08324fb8d89 | fd39b06310c679a0ea19ca4b86849319607f4b4abf6293106cdad08324fb8d89 |
| K1/source/v2-baseline/.claude/skills/httpclient-factory/SKILL.md | b6e17dcce8b801ae767545059c27a84cf425afb7c7f3fdb003cc481cd0466046 | b6e17dcce8b801ae767545059c27a84cf425afb7c7f3fdb003cc481cd0466046 |
| K1/source/v2-baseline/.claude/skills/logging/SKILL.md | cf8aa215f0f42d91c81fb0ee034b17da2841b156a4388ae372320883bda3868b | cf8aa215f0f42d91c81fb0ee034b17da2841b156a4388ae372320883bda3868b |
| K1/source/v2-baseline/.claude/skills/modern-csharp/SKILL.md | 1156651dbbb5dd51bc81a75f9236b3193198b54603ff941042b35bffce5fcc8c | 1156651dbbb5dd51bc81a75f9236b3193198b54603ff941042b35bffce5fcc8c |
| K1/source/v2-baseline/.claude/skills/project-structure/SKILL.md | d34f37f552adfbded3ec1b4b3b4c2e637a73ae36c74de14f2d67ab90528892cc | d34f37f552adfbded3ec1b4b3b4c2e637a73ae36c74de14f2d67ab90528892cc |
| K1/source/v2-baseline/.claude/skills/project-structure/references/backend-layout.md | 657c469b3be1a91827a1d78463f576d8dcfc069d70461e25097f37ba6f101650 | 657c469b3be1a91827a1d78463f576d8dcfc069d70461e25097f37ba6f101650 |
| K1/source/v2-baseline/.claude/skills/project-structure/references/solution-layout.md | 4c37997519285e15e74114adb0cb5ea26e90643750fd0c8d9d7ba75bc8eb4cbe | 4c37997519285e15e74114adb0cb5ea26e90643750fd0c8d9d7ba75bc8eb4cbe |
| K1/source/v2-baseline/.claude/skills/project-structure/references/technology-stack.md | f51d9b3e85b629b300b253555b7672a98a87cf5cb4197f593c8df3dea7962309 | f51d9b3e85b629b300b253555b7672a98a87cf5cb4197f593c8df3dea7962309 |
| K1/source/v2-baseline/.claude/skills/resilience/SKILL.md | a469c3456673622b4ca4eaa56dd05b803c18bb4c3af04e62ae6e0d784e025811 | a469c3456673622b4ca4eaa56dd05b803c18bb4c3af04e62ae6e0d784e025811 |
| K1/source/v2-baseline/.claude/skills/security-scan/SKILL.md | 4276a267d87d3611a6953c97678dd57693e4422a46dd4d0e82b8d630d02d05c2 | 4276a267d87d3611a6953c97678dd57693e4422a46dd4d0e82b8d630d02d05c2 |
| K1/source/v2-baseline/.claude/skills/security-scan/references/scan-layers.md | 4fe7396896e35e3d83f0b5c86a9046fd0278c5f38783581d0a744cb1a40fa846 | 4fe7396896e35e3d83f0b5c86a9046fd0278c5f38783581d0a744cb1a40fa846 |
| K1/source/v2-baseline/.claude/skills/serilog/SKILL.md | b3c2ab9cf5f89d5d506ffccf6140f5b06cc7b9f434206efb061ca69fa063d6d8 | b3c2ab9cf5f89d5d506ffccf6140f5b06cc7b9f434206efb061ca69fa063d6d8 |
| K1/source/v2-baseline/.claude/skills/swagger/SKILL.md | 7fe6fb21e419811282a0fe4a69b255dbe4cf39868d25932cf0cf07e1a596267d | 7fe6fb21e419811282a0fe4a69b255dbe4cf39868d25932cf0cf07e1a596267d |
| K1/source/v2-baseline/.claude/skills/testing/SKILL.md | 282c7a7185cc13992b20e6a22119dfb4803a1ebf69e4446042f9cdd343b88a9e | 282c7a7185cc13992b20e6a22119dfb4803a1ebf69e4446042f9cdd343b88a9e |
| K1/source/v2-baseline/.claude/skills/verify/SKILL.md | 38042cd665e1958a28290dcb4722aeb0ccb2f01c577a2a52203826ed237acf66 | 38042cd665e1958a28290dcb4722aeb0ccb2f01c577a2a52203826ed237acf66 |
| K1/source/v2-baseline/CLAUDE.md | 5d98d7aeedcde20ba044cc8b49cb0c4206d14fa478afca45c8a56f76e85bb4f4 | 5d98d7aeedcde20ba044cc8b49cb0c4206d14fa478afca45c8a56f76e85bb4f4 |
| K1/source/v2-baseline/CUSTOM_SETTINGS.md | 2449b93c170786e5525809aaf91ded093f2c00375defe7c349a85ad791b6ac4a | 2449b93c170786e5525809aaf91ded093f2c00375defe7c349a85ad791b6ac4a |
| K1/source/v2-baseline/SPECIFICATION.md | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| L0/CANDIDATE.md | 35da594d1c7e5bdd2f13c72500148e03580f0a7fe4bc5929694a317746f3020b | 35da594d1c7e5bdd2f13c72500148e03580f0a7fe4bc5929694a317746f3020b |
| L0/PROVENANCE.json | 9c5dfa66c1e321790623297ba9a2ab9fe47a4c0305a40ac8617a4fbf6caed5f3 | 9c5dfa66c1e321790623297ba9a2ab9fe47a4c0305a40ac8617a4fbf6caed5f3 |
| L0/README.md | d90dd6976893a2345d26aff2cefc20845053735ae85396395ddbd5018636deab | d90dd6976893a2345d26aff2cefc20845053735ae85396395ddbd5018636deab |
| L0/REFINEMENT_TASK.md | 3fc86404d72694d6f397d0946e8a7b6d13d1fda6242e55bff9219fc71ad29447 | 3fc86404d72694d6f397d0946e8a7b6d13d1fda6242e55bff9219fc71ad29447 |
| L0/baseline/CANDIDATE.md | 35da594d1c7e5bdd2f13c72500148e03580f0a7fe4bc5929694a317746f3020b | 35da594d1c7e5bdd2f13c72500148e03580f0a7fe4bc5929694a317746f3020b |
| L0/baseline/TASK.md | 579b723fde56866f0f8dcc30a619ad6abae8579622c0af102054604baef81a5c | 579b723fde56866f0f8dcc30a619ad6abae8579622c0af102054604baef81a5c |
| L0/source/inventory.json | bcf1a1532437f4a1d7bfafcb1f27ebcbb832ba684e35b8a42569cd9d2d9ad168 | bcf1a1532437f4a1d7bfafcb1f27ebcbb832ba684e35b8a42569cd9d2d9ad168 |
| L0/source/shared-research-invariants.json | 51b442b118b55ea89e16f3ac8603309d66635a7d184e456af2091d584f7da6d7 | 51b442b118b55ea89e16f3ac8603309d66635a7d184e456af2091d584f7da6d7 |
| L0/source/v2-baseline/.claude/agents/code-reviewer.md | 4f0f431e823eb7bb239be953d88ca74d1f9755c360d5d3d7b8355416de3528aa | 4f0f431e823eb7bb239be953d88ca74d1f9755c360d5d3d7b8355416de3528aa |
| L0/source/v2-baseline/.claude/rules/architecture.md | ced5b2a4e8e5e48a9023c89183ad9e46a637b881312e7f0d8925933ba5d40c7c | ced5b2a4e8e5e48a9023c89183ad9e46a637b881312e7f0d8925933ba5d40c7c |
| L0/source/v2-baseline/.claude/rules/coding-style.md | 48d906d335083f43a7f6c8bc62d24c34d569fbcfe04f42098623d257b1ff7390 | 48d906d335083f43a7f6c8bc62d24c34d569fbcfe04f42098623d257b1ff7390 |
| L0/source/v2-baseline/.claude/rules/dependencies.md | ced0516f065e25a36ea07d766865f26caae8d133a0bb1aca2976532ff62b6468 | ced0516f065e25a36ea07d766865f26caae8d133a0bb1aca2976532ff62b6468 |
| L0/source/v2-baseline/.claude/rules/error-handling.md | e54a59066bebc10832df82c8d818d8fa27dffd0de73706666198f5c0fcd491ea | e54a59066bebc10832df82c8d818d8fa27dffd0de73706666198f5c0fcd491ea |
| L0/source/v2-baseline/.claude/rules/performance.md | a4b54767111fefd9faae6ba7460e3abacf1ca9258ee1d265ac4eed496589c8b5 | a4b54767111fefd9faae6ba7460e3abacf1ca9258ee1d265ac4eed496589c8b5 |
| L0/source/v2-baseline/.claude/rules/security.md | d36e103f0fa842d038ba739a40e872fc768128a0a6a5474924e3b19a77640ac5 | d36e103f0fa842d038ba739a40e872fc768128a0a6a5474924e3b19a77640ac5 |
| L0/source/v2-baseline/.claude/rules/testing.md | 9c70dc874660db95c4c2032e80b575ea699ea1f514d946b36884c5c157cf0004 | 9c70dc874660db95c4c2032e80b575ea699ea1f514d946b36884c5c157cf0004 |
| L0/source/v2-baseline/.claude/skills/angular/SKILL.md | f4cf7baa3f7479f8d4df588dbbed75e96ff0c612caec199e283cdab13ccfd48e | f4cf7baa3f7479f8d4df588dbbed75e96ff0c612caec199e283cdab13ccfd48e |
| L0/source/v2-baseline/.claude/skills/api-versioning/SKILL.md | 2850c5e2f14d32aa049a1dd6b3983147bfa390d117176c8ce1f54c8eabedb892 | 2850c5e2f14d32aa049a1dd6b3983147bfa390d117176c8ce1f54c8eabedb892 |
| L0/source/v2-baseline/.claude/skills/authentication/SKILL.md | b08285e27eafd8f1b2d09a56f386c1f64a637af17dc097ecd2ffeb32c83e6191 | b08285e27eafd8f1b2d09a56f386c1f64a637af17dc097ecd2ffeb32c83e6191 |
| L0/source/v2-baseline/.claude/skills/build-fix/SKILL.md | 523ad63287ccdf6fa23941a5f6463c46e3ec17c1ed56fe6871f74e480c6ba9a2 | 523ad63287ccdf6fa23941a5f6463c46e3ec17c1ed56fe6871f74e480c6ba9a2 |
| L0/source/v2-baseline/.claude/skills/caching/SKILL.md | f4a8f3e028fc8152dfa30f2cedf30065906e3cea0189f23434dbd7487903bfd9 | f4a8f3e028fc8152dfa30f2cedf30065906e3cea0189f23434dbd7487903bfd9 |
| L0/source/v2-baseline/.claude/skills/ci-cd/SKILL.md | a914ababf5322baccea2549d55f222ee0d617c0be10c0fc37602b74472924f37 | a914ababf5322baccea2549d55f222ee0d617c0be10c0fc37602b74472924f37 |
| L0/source/v2-baseline/.claude/skills/code-review/SKILL.md | fdc0e9075d8379f9deea59174cb1b96f3f8e7a3b4085ab3c9f3ec4911b252f29 | fdc0e9075d8379f9deea59174cb1b96f3f8e7a3b4085ab3c9f3ec4911b252f29 |
| L0/source/v2-baseline/.claude/skills/configuration/SKILL.md | 340f98c96e329b770876bcd3bcfb1b84fe6c9b6477c96de767c3e24de21b2cd5 | 340f98c96e329b770876bcd3bcfb1b84fe6c9b6477c96de767c3e24de21b2cd5 |
| L0/source/v2-baseline/.claude/skills/custom-settings/SKILL.md | d4f76aeaa1597cd1ff7db33ea4d3d02fba4993cb97c8fefecdee23a0dbde6efb | d4f76aeaa1597cd1ff7db33ea4d3d02fba4993cb97c8fefecdee23a0dbde6efb |
| L0/source/v2-baseline/.claude/skills/dependency-injection/SKILL.md | bfac9b98b287bd8a0cc3a370eb521396a728b4ef8b4b53fb2e8c83282d57fade | bfac9b98b287bd8a0cc3a370eb521396a728b4ef8b4b53fb2e8c83282d57fade |
| L0/source/v2-baseline/.claude/skills/docker/SKILL.md | 801e00dd34525bafe3c53618a5f3751b228c6eb7607a06a1c3f6f2fc1197958f | 801e00dd34525bafe3c53618a5f3751b228c6eb7607a06a1c3f6f2fc1197958f |
| L0/source/v2-baseline/.claude/skills/ef-core/SKILL.md | c7120367231bd0bc3b6f92997f6f7450b9441c15604356651447d26cee67d762 | c7120367231bd0bc3b6f92997f6f7450b9441c15604356651447d26cee67d762 |
| L0/source/v2-baseline/.claude/skills/error-handling/SKILL.md | 4d514f0eec953ed9ba85d37f353ccc22b84a6137e9685e180bd2a250aa657b9d | 4d514f0eec953ed9ba85d37f353ccc22b84a6137e9685e180bd2a250aa657b9d |
| L0/source/v2-baseline/.claude/skills/git-workflow/SKILL.md | 940365f04436f41558ba951a3cd6a0dd77cc2e742314950f996962b08dc9bbc2 | 940365f04436f41558ba951a3cd6a0dd77cc2e742314950f996962b08dc9bbc2 |
| L0/source/v2-baseline/.claude/skills/health-check/SKILL.md | cb0c32f0a6bf5b7ffcac2a2d83bce3f4c236d6d89cd01fc1b5abad57a5435e8f | cb0c32f0a6bf5b7ffcac2a2d83bce3f4c236d6d89cd01fc1b5abad57a5435e8f |
| L0/source/v2-baseline/.claude/skills/http-api/SKILL.md | fd39b06310c679a0ea19ca4b86849319607f4b4abf6293106cdad08324fb8d89 | fd39b06310c679a0ea19ca4b86849319607f4b4abf6293106cdad08324fb8d89 |
| L0/source/v2-baseline/.claude/skills/httpclient-factory/SKILL.md | b6e17dcce8b801ae767545059c27a84cf425afb7c7f3fdb003cc481cd0466046 | b6e17dcce8b801ae767545059c27a84cf425afb7c7f3fdb003cc481cd0466046 |
| L0/source/v2-baseline/.claude/skills/logging/SKILL.md | cf8aa215f0f42d91c81fb0ee034b17da2841b156a4388ae372320883bda3868b | cf8aa215f0f42d91c81fb0ee034b17da2841b156a4388ae372320883bda3868b |
| L0/source/v2-baseline/.claude/skills/modern-csharp/SKILL.md | 1156651dbbb5dd51bc81a75f9236b3193198b54603ff941042b35bffce5fcc8c | 1156651dbbb5dd51bc81a75f9236b3193198b54603ff941042b35bffce5fcc8c |
| L0/source/v2-baseline/.claude/skills/project-structure/SKILL.md | d34f37f552adfbded3ec1b4b3b4c2e637a73ae36c74de14f2d67ab90528892cc | d34f37f552adfbded3ec1b4b3b4c2e637a73ae36c74de14f2d67ab90528892cc |
| L0/source/v2-baseline/.claude/skills/project-structure/references/backend-layout.md | 657c469b3be1a91827a1d78463f576d8dcfc069d70461e25097f37ba6f101650 | 657c469b3be1a91827a1d78463f576d8dcfc069d70461e25097f37ba6f101650 |
| L0/source/v2-baseline/.claude/skills/project-structure/references/solution-layout.md | 4c37997519285e15e74114adb0cb5ea26e90643750fd0c8d9d7ba75bc8eb4cbe | 4c37997519285e15e74114adb0cb5ea26e90643750fd0c8d9d7ba75bc8eb4cbe |
| L0/source/v2-baseline/.claude/skills/project-structure/references/technology-stack.md | f51d9b3e85b629b300b253555b7672a98a87cf5cb4197f593c8df3dea7962309 | f51d9b3e85b629b300b253555b7672a98a87cf5cb4197f593c8df3dea7962309 |
| L0/source/v2-baseline/.claude/skills/resilience/SKILL.md | a469c3456673622b4ca4eaa56dd05b803c18bb4c3af04e62ae6e0d784e025811 | a469c3456673622b4ca4eaa56dd05b803c18bb4c3af04e62ae6e0d784e025811 |
| L0/source/v2-baseline/.claude/skills/security-scan/SKILL.md | 4276a267d87d3611a6953c97678dd57693e4422a46dd4d0e82b8d630d02d05c2 | 4276a267d87d3611a6953c97678dd57693e4422a46dd4d0e82b8d630d02d05c2 |
| L0/source/v2-baseline/.claude/skills/security-scan/references/scan-layers.md | 4fe7396896e35e3d83f0b5c86a9046fd0278c5f38783581d0a744cb1a40fa846 | 4fe7396896e35e3d83f0b5c86a9046fd0278c5f38783581d0a744cb1a40fa846 |
| L0/source/v2-baseline/.claude/skills/serilog/SKILL.md | b3c2ab9cf5f89d5d506ffccf6140f5b06cc7b9f434206efb061ca69fa063d6d8 | b3c2ab9cf5f89d5d506ffccf6140f5b06cc7b9f434206efb061ca69fa063d6d8 |
| L0/source/v2-baseline/.claude/skills/swagger/SKILL.md | 7fe6fb21e419811282a0fe4a69b255dbe4cf39868d25932cf0cf07e1a596267d | 7fe6fb21e419811282a0fe4a69b255dbe4cf39868d25932cf0cf07e1a596267d |
| L0/source/v2-baseline/.claude/skills/testing/SKILL.md | 282c7a7185cc13992b20e6a22119dfb4803a1ebf69e4446042f9cdd343b88a9e | 282c7a7185cc13992b20e6a22119dfb4803a1ebf69e4446042f9cdd343b88a9e |
| L0/source/v2-baseline/.claude/skills/verify/SKILL.md | 38042cd665e1958a28290dcb4722aeb0ccb2f01c577a2a52203826ed237acf66 | 38042cd665e1958a28290dcb4722aeb0ccb2f01c577a2a52203826ed237acf66 |
| L0/source/v2-baseline/CLAUDE.md | 5d98d7aeedcde20ba044cc8b49cb0c4206d14fa478afca45c8a56f76e85bb4f4 | 5d98d7aeedcde20ba044cc8b49cb0c4206d14fa478afca45c8a56f76e85bb4f4 |
| L0/source/v2-baseline/CUSTOM_SETTINGS.md | 2449b93c170786e5525809aaf91ded093f2c00375defe7c349a85ad791b6ac4a | 2449b93c170786e5525809aaf91ded093f2c00375defe7c349a85ad791b6ac4a |
| L0/source/v2-baseline/SPECIFICATION.md | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| L1-Restart/CANDIDATE.md | 08b42db367553ffbcf5dd635e82c2c30ea2d25f2cf0916fb846aec6a24a624f0 | 08b42db367553ffbcf5dd635e82c2c30ea2d25f2cf0916fb846aec6a24a624f0 |
| L1-Restart/PROVENANCE.json | 301d018e307d47502c1eb55df4b16a2fa83e7702b6efe08a416d36ddc2cc9e23 | 301d018e307d47502c1eb55df4b16a2fa83e7702b6efe08a416d36ddc2cc9e23 |
| L1-Restart/README.md | f9da27b8509c4c1f25aa511f7c9f160ea5989cc3de1d2c9eacbae5926a367fe2 | f9da27b8509c4c1f25aa511f7c9f160ea5989cc3de1d2c9eacbae5926a367fe2 |
| L1-Restart/REFINEMENT_TASK.md | ac359865467401f78399355293e54ebbe50cdd239916a0ab50621489f7c8e325 | ac359865467401f78399355293e54ebbe50cdd239916a0ab50621489f7c8e325 |
| L1-Restart/baseline/CANDIDATE.md | 08b42db367553ffbcf5dd635e82c2c30ea2d25f2cf0916fb846aec6a24a624f0 | 08b42db367553ffbcf5dd635e82c2c30ea2d25f2cf0916fb846aec6a24a624f0 |
| L1-Restart/baseline/TASK.md | 579b723fde56866f0f8dcc30a619ad6abae8579622c0af102054604baef81a5c | 579b723fde56866f0f8dcc30a619ad6abae8579622c0af102054604baef81a5c |
| L1-Restart/source/inventory.json | bcf1a1532437f4a1d7bfafcb1f27ebcbb832ba684e35b8a42569cd9d2d9ad168 | bcf1a1532437f4a1d7bfafcb1f27ebcbb832ba684e35b8a42569cd9d2d9ad168 |
| L1-Restart/source/shared-research-invariants.json | 51b442b118b55ea89e16f3ac8603309d66635a7d184e456af2091d584f7da6d7 | 51b442b118b55ea89e16f3ac8603309d66635a7d184e456af2091d584f7da6d7 |
| L1-Restart/source/v2-baseline/.claude/agents/code-reviewer.md | 4f0f431e823eb7bb239be953d88ca74d1f9755c360d5d3d7b8355416de3528aa | 4f0f431e823eb7bb239be953d88ca74d1f9755c360d5d3d7b8355416de3528aa |
| L1-Restart/source/v2-baseline/.claude/rules/architecture.md | ced5b2a4e8e5e48a9023c89183ad9e46a637b881312e7f0d8925933ba5d40c7c | ced5b2a4e8e5e48a9023c89183ad9e46a637b881312e7f0d8925933ba5d40c7c |
| L1-Restart/source/v2-baseline/.claude/rules/coding-style.md | 48d906d335083f43a7f6c8bc62d24c34d569fbcfe04f42098623d257b1ff7390 | 48d906d335083f43a7f6c8bc62d24c34d569fbcfe04f42098623d257b1ff7390 |
| L1-Restart/source/v2-baseline/.claude/rules/dependencies.md | ced0516f065e25a36ea07d766865f26caae8d133a0bb1aca2976532ff62b6468 | ced0516f065e25a36ea07d766865f26caae8d133a0bb1aca2976532ff62b6468 |
| L1-Restart/source/v2-baseline/.claude/rules/error-handling.md | e54a59066bebc10832df82c8d818d8fa27dffd0de73706666198f5c0fcd491ea | e54a59066bebc10832df82c8d818d8fa27dffd0de73706666198f5c0fcd491ea |
| L1-Restart/source/v2-baseline/.claude/rules/performance.md | a4b54767111fefd9faae6ba7460e3abacf1ca9258ee1d265ac4eed496589c8b5 | a4b54767111fefd9faae6ba7460e3abacf1ca9258ee1d265ac4eed496589c8b5 |
| L1-Restart/source/v2-baseline/.claude/rules/security.md | d36e103f0fa842d038ba739a40e872fc768128a0a6a5474924e3b19a77640ac5 | d36e103f0fa842d038ba739a40e872fc768128a0a6a5474924e3b19a77640ac5 |
| L1-Restart/source/v2-baseline/.claude/rules/testing.md | 9c70dc874660db95c4c2032e80b575ea699ea1f514d946b36884c5c157cf0004 | 9c70dc874660db95c4c2032e80b575ea699ea1f514d946b36884c5c157cf0004 |
| L1-Restart/source/v2-baseline/.claude/skills/angular/SKILL.md | f4cf7baa3f7479f8d4df588dbbed75e96ff0c612caec199e283cdab13ccfd48e | f4cf7baa3f7479f8d4df588dbbed75e96ff0c612caec199e283cdab13ccfd48e |
| L1-Restart/source/v2-baseline/.claude/skills/api-versioning/SKILL.md | 2850c5e2f14d32aa049a1dd6b3983147bfa390d117176c8ce1f54c8eabedb892 | 2850c5e2f14d32aa049a1dd6b3983147bfa390d117176c8ce1f54c8eabedb892 |
| L1-Restart/source/v2-baseline/.claude/skills/authentication/SKILL.md | b08285e27eafd8f1b2d09a56f386c1f64a637af17dc097ecd2ffeb32c83e6191 | b08285e27eafd8f1b2d09a56f386c1f64a637af17dc097ecd2ffeb32c83e6191 |
| L1-Restart/source/v2-baseline/.claude/skills/build-fix/SKILL.md | 523ad63287ccdf6fa23941a5f6463c46e3ec17c1ed56fe6871f74e480c6ba9a2 | 523ad63287ccdf6fa23941a5f6463c46e3ec17c1ed56fe6871f74e480c6ba9a2 |
| L1-Restart/source/v2-baseline/.claude/skills/caching/SKILL.md | f4a8f3e028fc8152dfa30f2cedf30065906e3cea0189f23434dbd7487903bfd9 | f4a8f3e028fc8152dfa30f2cedf30065906e3cea0189f23434dbd7487903bfd9 |
| L1-Restart/source/v2-baseline/.claude/skills/ci-cd/SKILL.md | a914ababf5322baccea2549d55f222ee0d617c0be10c0fc37602b74472924f37 | a914ababf5322baccea2549d55f222ee0d617c0be10c0fc37602b74472924f37 |
| L1-Restart/source/v2-baseline/.claude/skills/code-review/SKILL.md | fdc0e9075d8379f9deea59174cb1b96f3f8e7a3b4085ab3c9f3ec4911b252f29 | fdc0e9075d8379f9deea59174cb1b96f3f8e7a3b4085ab3c9f3ec4911b252f29 |
| L1-Restart/source/v2-baseline/.claude/skills/configuration/SKILL.md | 340f98c96e329b770876bcd3bcfb1b84fe6c9b6477c96de767c3e24de21b2cd5 | 340f98c96e329b770876bcd3bcfb1b84fe6c9b6477c96de767c3e24de21b2cd5 |
| L1-Restart/source/v2-baseline/.claude/skills/custom-settings/SKILL.md | d4f76aeaa1597cd1ff7db33ea4d3d02fba4993cb97c8fefecdee23a0dbde6efb | d4f76aeaa1597cd1ff7db33ea4d3d02fba4993cb97c8fefecdee23a0dbde6efb |
| L1-Restart/source/v2-baseline/.claude/skills/dependency-injection/SKILL.md | bfac9b98b287bd8a0cc3a370eb521396a728b4ef8b4b53fb2e8c83282d57fade | bfac9b98b287bd8a0cc3a370eb521396a728b4ef8b4b53fb2e8c83282d57fade |
| L1-Restart/source/v2-baseline/.claude/skills/docker/SKILL.md | 801e00dd34525bafe3c53618a5f3751b228c6eb7607a06a1c3f6f2fc1197958f | 801e00dd34525bafe3c53618a5f3751b228c6eb7607a06a1c3f6f2fc1197958f |
| L1-Restart/source/v2-baseline/.claude/skills/ef-core/SKILL.md | c7120367231bd0bc3b6f92997f6f7450b9441c15604356651447d26cee67d762 | c7120367231bd0bc3b6f92997f6f7450b9441c15604356651447d26cee67d762 |
| L1-Restart/source/v2-baseline/.claude/skills/error-handling/SKILL.md | 4d514f0eec953ed9ba85d37f353ccc22b84a6137e9685e180bd2a250aa657b9d | 4d514f0eec953ed9ba85d37f353ccc22b84a6137e9685e180bd2a250aa657b9d |
| L1-Restart/source/v2-baseline/.claude/skills/git-workflow/SKILL.md | 940365f04436f41558ba951a3cd6a0dd77cc2e742314950f996962b08dc9bbc2 | 940365f04436f41558ba951a3cd6a0dd77cc2e742314950f996962b08dc9bbc2 |
| L1-Restart/source/v2-baseline/.claude/skills/health-check/SKILL.md | cb0c32f0a6bf5b7ffcac2a2d83bce3f4c236d6d89cd01fc1b5abad57a5435e8f | cb0c32f0a6bf5b7ffcac2a2d83bce3f4c236d6d89cd01fc1b5abad57a5435e8f |
| L1-Restart/source/v2-baseline/.claude/skills/http-api/SKILL.md | fd39b06310c679a0ea19ca4b86849319607f4b4abf6293106cdad08324fb8d89 | fd39b06310c679a0ea19ca4b86849319607f4b4abf6293106cdad08324fb8d89 |
| L1-Restart/source/v2-baseline/.claude/skills/httpclient-factory/SKILL.md | b6e17dcce8b801ae767545059c27a84cf425afb7c7f3fdb003cc481cd0466046 | b6e17dcce8b801ae767545059c27a84cf425afb7c7f3fdb003cc481cd0466046 |
| L1-Restart/source/v2-baseline/.claude/skills/logging/SKILL.md | cf8aa215f0f42d91c81fb0ee034b17da2841b156a4388ae372320883bda3868b | cf8aa215f0f42d91c81fb0ee034b17da2841b156a4388ae372320883bda3868b |
| L1-Restart/source/v2-baseline/.claude/skills/modern-csharp/SKILL.md | 1156651dbbb5dd51bc81a75f9236b3193198b54603ff941042b35bffce5fcc8c | 1156651dbbb5dd51bc81a75f9236b3193198b54603ff941042b35bffce5fcc8c |
| L1-Restart/source/v2-baseline/.claude/skills/project-structure/SKILL.md | d34f37f552adfbded3ec1b4b3b4c2e637a73ae36c74de14f2d67ab90528892cc | d34f37f552adfbded3ec1b4b3b4c2e637a73ae36c74de14f2d67ab90528892cc |
| L1-Restart/source/v2-baseline/.claude/skills/project-structure/references/backend-layout.md | 657c469b3be1a91827a1d78463f576d8dcfc069d70461e25097f37ba6f101650 | 657c469b3be1a91827a1d78463f576d8dcfc069d70461e25097f37ba6f101650 |
| L1-Restart/source/v2-baseline/.claude/skills/project-structure/references/solution-layout.md | 4c37997519285e15e74114adb0cb5ea26e90643750fd0c8d9d7ba75bc8eb4cbe | 4c37997519285e15e74114adb0cb5ea26e90643750fd0c8d9d7ba75bc8eb4cbe |
| L1-Restart/source/v2-baseline/.claude/skills/project-structure/references/technology-stack.md | f51d9b3e85b629b300b253555b7672a98a87cf5cb4197f593c8df3dea7962309 | f51d9b3e85b629b300b253555b7672a98a87cf5cb4197f593c8df3dea7962309 |
| L1-Restart/source/v2-baseline/.claude/skills/resilience/SKILL.md | a469c3456673622b4ca4eaa56dd05b803c18bb4c3af04e62ae6e0d784e025811 | a469c3456673622b4ca4eaa56dd05b803c18bb4c3af04e62ae6e0d784e025811 |
| L1-Restart/source/v2-baseline/.claude/skills/security-scan/SKILL.md | 4276a267d87d3611a6953c97678dd57693e4422a46dd4d0e82b8d630d02d05c2 | 4276a267d87d3611a6953c97678dd57693e4422a46dd4d0e82b8d630d02d05c2 |
| L1-Restart/source/v2-baseline/.claude/skills/security-scan/references/scan-layers.md | 4fe7396896e35e3d83f0b5c86a9046fd0278c5f38783581d0a744cb1a40fa846 | 4fe7396896e35e3d83f0b5c86a9046fd0278c5f38783581d0a744cb1a40fa846 |
| L1-Restart/source/v2-baseline/.claude/skills/serilog/SKILL.md | b3c2ab9cf5f89d5d506ffccf6140f5b06cc7b9f434206efb061ca69fa063d6d8 | b3c2ab9cf5f89d5d506ffccf6140f5b06cc7b9f434206efb061ca69fa063d6d8 |
| L1-Restart/source/v2-baseline/.claude/skills/swagger/SKILL.md | 7fe6fb21e419811282a0fe4a69b255dbe4cf39868d25932cf0cf07e1a596267d | 7fe6fb21e419811282a0fe4a69b255dbe4cf39868d25932cf0cf07e1a596267d |
| L1-Restart/source/v2-baseline/.claude/skills/testing/SKILL.md | 282c7a7185cc13992b20e6a22119dfb4803a1ebf69e4446042f9cdd343b88a9e | 282c7a7185cc13992b20e6a22119dfb4803a1ebf69e4446042f9cdd343b88a9e |
| L1-Restart/source/v2-baseline/.claude/skills/verify/SKILL.md | 38042cd665e1958a28290dcb4722aeb0ccb2f01c577a2a52203826ed237acf66 | 38042cd665e1958a28290dcb4722aeb0ccb2f01c577a2a52203826ed237acf66 |
| L1-Restart/source/v2-baseline/CLAUDE.md | 5d98d7aeedcde20ba044cc8b49cb0c4206d14fa478afca45c8a56f76e85bb4f4 | 5d98d7aeedcde20ba044cc8b49cb0c4206d14fa478afca45c8a56f76e85bb4f4 |
| L1-Restart/source/v2-baseline/CUSTOM_SETTINGS.md | 2449b93c170786e5525809aaf91ded093f2c00375defe7c349a85ad791b6ac4a | 2449b93c170786e5525809aaf91ded093f2c00375defe7c349a85ad791b6ac4a |
| L1-Restart/source/v2-baseline/SPECIFICATION.md | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| M/CANDIDATE.md | 883ee7d52237e764a167fca381e76871de801d862cc15492e565787419bfba5d | 883ee7d52237e764a167fca381e76871de801d862cc15492e565787419bfba5d |
| M/PROVENANCE.json | 13710ca301d974072d0aceda6113f35f0e1a8466fe070262acb6e2282313a2ce | 13710ca301d974072d0aceda6113f35f0e1a8466fe070262acb6e2282313a2ce |
| M/README.md | e7640adedddb0d89b723c7d01fc23c5ba20b52e494fa9770e4d7af3d7d637e85 | e7640adedddb0d89b723c7d01fc23c5ba20b52e494fa9770e4d7af3d7d637e85 |
| M/REFINEMENT_TASK.md | f1d523d3fd2b67ac646a77ced88bc13ffd559d6ac6c103c98bcb877726bc2c12 | f1d523d3fd2b67ac646a77ced88bc13ffd559d6ac6c103c98bcb877726bc2c12 |
| M/baseline/CANDIDATE.md | 883ee7d52237e764a167fca381e76871de801d862cc15492e565787419bfba5d | 883ee7d52237e764a167fca381e76871de801d862cc15492e565787419bfba5d |
| M/baseline/TASK.md | 579b723fde56866f0f8dcc30a619ad6abae8579622c0af102054604baef81a5c | 579b723fde56866f0f8dcc30a619ad6abae8579622c0af102054604baef81a5c |
| M/source/inventory.json | bcf1a1532437f4a1d7bfafcb1f27ebcbb832ba684e35b8a42569cd9d2d9ad168 | bcf1a1532437f4a1d7bfafcb1f27ebcbb832ba684e35b8a42569cd9d2d9ad168 |
| M/source/shared-research-invariants.json | 51b442b118b55ea89e16f3ac8603309d66635a7d184e456af2091d584f7da6d7 | 51b442b118b55ea89e16f3ac8603309d66635a7d184e456af2091d584f7da6d7 |
| M/source/v2-baseline/.claude/agents/code-reviewer.md | 4f0f431e823eb7bb239be953d88ca74d1f9755c360d5d3d7b8355416de3528aa | 4f0f431e823eb7bb239be953d88ca74d1f9755c360d5d3d7b8355416de3528aa |
| M/source/v2-baseline/.claude/rules/architecture.md | ced5b2a4e8e5e48a9023c89183ad9e46a637b881312e7f0d8925933ba5d40c7c | ced5b2a4e8e5e48a9023c89183ad9e46a637b881312e7f0d8925933ba5d40c7c |
| M/source/v2-baseline/.claude/rules/coding-style.md | 48d906d335083f43a7f6c8bc62d24c34d569fbcfe04f42098623d257b1ff7390 | 48d906d335083f43a7f6c8bc62d24c34d569fbcfe04f42098623d257b1ff7390 |
| M/source/v2-baseline/.claude/rules/dependencies.md | ced0516f065e25a36ea07d766865f26caae8d133a0bb1aca2976532ff62b6468 | ced0516f065e25a36ea07d766865f26caae8d133a0bb1aca2976532ff62b6468 |
| M/source/v2-baseline/.claude/rules/error-handling.md | e54a59066bebc10832df82c8d818d8fa27dffd0de73706666198f5c0fcd491ea | e54a59066bebc10832df82c8d818d8fa27dffd0de73706666198f5c0fcd491ea |
| M/source/v2-baseline/.claude/rules/performance.md | a4b54767111fefd9faae6ba7460e3abacf1ca9258ee1d265ac4eed496589c8b5 | a4b54767111fefd9faae6ba7460e3abacf1ca9258ee1d265ac4eed496589c8b5 |
| M/source/v2-baseline/.claude/rules/security.md | d36e103f0fa842d038ba739a40e872fc768128a0a6a5474924e3b19a77640ac5 | d36e103f0fa842d038ba739a40e872fc768128a0a6a5474924e3b19a77640ac5 |
| M/source/v2-baseline/.claude/rules/testing.md | 9c70dc874660db95c4c2032e80b575ea699ea1f514d946b36884c5c157cf0004 | 9c70dc874660db95c4c2032e80b575ea699ea1f514d946b36884c5c157cf0004 |
| M/source/v2-baseline/.claude/skills/angular/SKILL.md | f4cf7baa3f7479f8d4df588dbbed75e96ff0c612caec199e283cdab13ccfd48e | f4cf7baa3f7479f8d4df588dbbed75e96ff0c612caec199e283cdab13ccfd48e |
| M/source/v2-baseline/.claude/skills/api-versioning/SKILL.md | 2850c5e2f14d32aa049a1dd6b3983147bfa390d117176c8ce1f54c8eabedb892 | 2850c5e2f14d32aa049a1dd6b3983147bfa390d117176c8ce1f54c8eabedb892 |
| M/source/v2-baseline/.claude/skills/authentication/SKILL.md | b08285e27eafd8f1b2d09a56f386c1f64a637af17dc097ecd2ffeb32c83e6191 | b08285e27eafd8f1b2d09a56f386c1f64a637af17dc097ecd2ffeb32c83e6191 |
| M/source/v2-baseline/.claude/skills/build-fix/SKILL.md | 523ad63287ccdf6fa23941a5f6463c46e3ec17c1ed56fe6871f74e480c6ba9a2 | 523ad63287ccdf6fa23941a5f6463c46e3ec17c1ed56fe6871f74e480c6ba9a2 |
| M/source/v2-baseline/.claude/skills/caching/SKILL.md | f4a8f3e028fc8152dfa30f2cedf30065906e3cea0189f23434dbd7487903bfd9 | f4a8f3e028fc8152dfa30f2cedf30065906e3cea0189f23434dbd7487903bfd9 |
| M/source/v2-baseline/.claude/skills/ci-cd/SKILL.md | a914ababf5322baccea2549d55f222ee0d617c0be10c0fc37602b74472924f37 | a914ababf5322baccea2549d55f222ee0d617c0be10c0fc37602b74472924f37 |
| M/source/v2-baseline/.claude/skills/code-review/SKILL.md | fdc0e9075d8379f9deea59174cb1b96f3f8e7a3b4085ab3c9f3ec4911b252f29 | fdc0e9075d8379f9deea59174cb1b96f3f8e7a3b4085ab3c9f3ec4911b252f29 |
| M/source/v2-baseline/.claude/skills/configuration/SKILL.md | 340f98c96e329b770876bcd3bcfb1b84fe6c9b6477c96de767c3e24de21b2cd5 | 340f98c96e329b770876bcd3bcfb1b84fe6c9b6477c96de767c3e24de21b2cd5 |
| M/source/v2-baseline/.claude/skills/custom-settings/SKILL.md | d4f76aeaa1597cd1ff7db33ea4d3d02fba4993cb97c8fefecdee23a0dbde6efb | d4f76aeaa1597cd1ff7db33ea4d3d02fba4993cb97c8fefecdee23a0dbde6efb |
| M/source/v2-baseline/.claude/skills/dependency-injection/SKILL.md | bfac9b98b287bd8a0cc3a370eb521396a728b4ef8b4b53fb2e8c83282d57fade | bfac9b98b287bd8a0cc3a370eb521396a728b4ef8b4b53fb2e8c83282d57fade |
| M/source/v2-baseline/.claude/skills/docker/SKILL.md | 801e00dd34525bafe3c53618a5f3751b228c6eb7607a06a1c3f6f2fc1197958f | 801e00dd34525bafe3c53618a5f3751b228c6eb7607a06a1c3f6f2fc1197958f |
| M/source/v2-baseline/.claude/skills/ef-core/SKILL.md | c7120367231bd0bc3b6f92997f6f7450b9441c15604356651447d26cee67d762 | c7120367231bd0bc3b6f92997f6f7450b9441c15604356651447d26cee67d762 |
| M/source/v2-baseline/.claude/skills/error-handling/SKILL.md | 4d514f0eec953ed9ba85d37f353ccc22b84a6137e9685e180bd2a250aa657b9d | 4d514f0eec953ed9ba85d37f353ccc22b84a6137e9685e180bd2a250aa657b9d |
| M/source/v2-baseline/.claude/skills/git-workflow/SKILL.md | 940365f04436f41558ba951a3cd6a0dd77cc2e742314950f996962b08dc9bbc2 | 940365f04436f41558ba951a3cd6a0dd77cc2e742314950f996962b08dc9bbc2 |
| M/source/v2-baseline/.claude/skills/health-check/SKILL.md | cb0c32f0a6bf5b7ffcac2a2d83bce3f4c236d6d89cd01fc1b5abad57a5435e8f | cb0c32f0a6bf5b7ffcac2a2d83bce3f4c236d6d89cd01fc1b5abad57a5435e8f |
| M/source/v2-baseline/.claude/skills/http-api/SKILL.md | fd39b06310c679a0ea19ca4b86849319607f4b4abf6293106cdad08324fb8d89 | fd39b06310c679a0ea19ca4b86849319607f4b4abf6293106cdad08324fb8d89 |
| M/source/v2-baseline/.claude/skills/httpclient-factory/SKILL.md | b6e17dcce8b801ae767545059c27a84cf425afb7c7f3fdb003cc481cd0466046 | b6e17dcce8b801ae767545059c27a84cf425afb7c7f3fdb003cc481cd0466046 |
| M/source/v2-baseline/.claude/skills/logging/SKILL.md | cf8aa215f0f42d91c81fb0ee034b17da2841b156a4388ae372320883bda3868b | cf8aa215f0f42d91c81fb0ee034b17da2841b156a4388ae372320883bda3868b |
| M/source/v2-baseline/.claude/skills/modern-csharp/SKILL.md | 1156651dbbb5dd51bc81a75f9236b3193198b54603ff941042b35bffce5fcc8c | 1156651dbbb5dd51bc81a75f9236b3193198b54603ff941042b35bffce5fcc8c |
| M/source/v2-baseline/.claude/skills/project-structure/SKILL.md | d34f37f552adfbded3ec1b4b3b4c2e637a73ae36c74de14f2d67ab90528892cc | d34f37f552adfbded3ec1b4b3b4c2e637a73ae36c74de14f2d67ab90528892cc |
| M/source/v2-baseline/.claude/skills/project-structure/references/backend-layout.md | 657c469b3be1a91827a1d78463f576d8dcfc069d70461e25097f37ba6f101650 | 657c469b3be1a91827a1d78463f576d8dcfc069d70461e25097f37ba6f101650 |
| M/source/v2-baseline/.claude/skills/project-structure/references/solution-layout.md | 4c37997519285e15e74114adb0cb5ea26e90643750fd0c8d9d7ba75bc8eb4cbe | 4c37997519285e15e74114adb0cb5ea26e90643750fd0c8d9d7ba75bc8eb4cbe |
| M/source/v2-baseline/.claude/skills/project-structure/references/technology-stack.md | f51d9b3e85b629b300b253555b7672a98a87cf5cb4197f593c8df3dea7962309 | f51d9b3e85b629b300b253555b7672a98a87cf5cb4197f593c8df3dea7962309 |
| M/source/v2-baseline/.claude/skills/resilience/SKILL.md | a469c3456673622b4ca4eaa56dd05b803c18bb4c3af04e62ae6e0d784e025811 | a469c3456673622b4ca4eaa56dd05b803c18bb4c3af04e62ae6e0d784e025811 |
| M/source/v2-baseline/.claude/skills/security-scan/SKILL.md | 4276a267d87d3611a6953c97678dd57693e4422a46dd4d0e82b8d630d02d05c2 | 4276a267d87d3611a6953c97678dd57693e4422a46dd4d0e82b8d630d02d05c2 |
| M/source/v2-baseline/.claude/skills/security-scan/references/scan-layers.md | 4fe7396896e35e3d83f0b5c86a9046fd0278c5f38783581d0a744cb1a40fa846 | 4fe7396896e35e3d83f0b5c86a9046fd0278c5f38783581d0a744cb1a40fa846 |
| M/source/v2-baseline/.claude/skills/serilog/SKILL.md | b3c2ab9cf5f89d5d506ffccf6140f5b06cc7b9f434206efb061ca69fa063d6d8 | b3c2ab9cf5f89d5d506ffccf6140f5b06cc7b9f434206efb061ca69fa063d6d8 |
| M/source/v2-baseline/.claude/skills/swagger/SKILL.md | 7fe6fb21e419811282a0fe4a69b255dbe4cf39868d25932cf0cf07e1a596267d | 7fe6fb21e419811282a0fe4a69b255dbe4cf39868d25932cf0cf07e1a596267d |
| M/source/v2-baseline/.claude/skills/testing/SKILL.md | 282c7a7185cc13992b20e6a22119dfb4803a1ebf69e4446042f9cdd343b88a9e | 282c7a7185cc13992b20e6a22119dfb4803a1ebf69e4446042f9cdd343b88a9e |
| M/source/v2-baseline/.claude/skills/verify/SKILL.md | 38042cd665e1958a28290dcb4722aeb0ccb2f01c577a2a52203826ed237acf66 | 38042cd665e1958a28290dcb4722aeb0ccb2f01c577a2a52203826ed237acf66 |
| M/source/v2-baseline/CLAUDE.md | 5d98d7aeedcde20ba044cc8b49cb0c4206d14fa478afca45c8a56f76e85bb4f4 | 5d98d7aeedcde20ba044cc8b49cb0c4206d14fa478afca45c8a56f76e85bb4f4 |
| M/source/v2-baseline/CUSTOM_SETTINGS.md | 2449b93c170786e5525809aaf91ded093f2c00375defe7c349a85ad791b6ac4a | 2449b93c170786e5525809aaf91ded093f2c00375defe7c349a85ad791b6ac4a |
| M/source/v2-baseline/SPECIFICATION.md | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| M1/CANDIDATE.md | f1b209f4984ecf93b35c4552026f0b5ed85fada9d54d337c5b47b2642332bff3 | f1b209f4984ecf93b35c4552026f0b5ed85fada9d54d337c5b47b2642332bff3 |
| M1/PROVENANCE.json | 465361a2ab94da38e9b64da2cc2b4c4357481702ffbeb4007522e8fe25d4e3c8 | 465361a2ab94da38e9b64da2cc2b4c4357481702ffbeb4007522e8fe25d4e3c8 |
| M1/README.md | 8dbd28b37b2e62f611fce07a289000b6bebba7bbb6bd03d6bb027303115b7a1f | 8dbd28b37b2e62f611fce07a289000b6bebba7bbb6bd03d6bb027303115b7a1f |
| M1/REFINEMENT_TASK.md | 4c8af987ee2da08f08849c93dd7ca8fa040255b52cc0a78706d3be72721c1b0a | 4c8af987ee2da08f08849c93dd7ca8fa040255b52cc0a78706d3be72721c1b0a |
| M1/baseline/CANDIDATE.md | f1b209f4984ecf93b35c4552026f0b5ed85fada9d54d337c5b47b2642332bff3 | f1b209f4984ecf93b35c4552026f0b5ed85fada9d54d337c5b47b2642332bff3 |
| M1/baseline/TASK.md | 579b723fde56866f0f8dcc30a619ad6abae8579622c0af102054604baef81a5c | 579b723fde56866f0f8dcc30a619ad6abae8579622c0af102054604baef81a5c |
| M1/source/inventory.json | bcf1a1532437f4a1d7bfafcb1f27ebcbb832ba684e35b8a42569cd9d2d9ad168 | bcf1a1532437f4a1d7bfafcb1f27ebcbb832ba684e35b8a42569cd9d2d9ad168 |
| M1/source/shared-research-invariants.json | 51b442b118b55ea89e16f3ac8603309d66635a7d184e456af2091d584f7da6d7 | 51b442b118b55ea89e16f3ac8603309d66635a7d184e456af2091d584f7da6d7 |
| M1/source/v2-baseline/.claude/agents/code-reviewer.md | 4f0f431e823eb7bb239be953d88ca74d1f9755c360d5d3d7b8355416de3528aa | 4f0f431e823eb7bb239be953d88ca74d1f9755c360d5d3d7b8355416de3528aa |
| M1/source/v2-baseline/.claude/rules/architecture.md | ced5b2a4e8e5e48a9023c89183ad9e46a637b881312e7f0d8925933ba5d40c7c | ced5b2a4e8e5e48a9023c89183ad9e46a637b881312e7f0d8925933ba5d40c7c |
| M1/source/v2-baseline/.claude/rules/coding-style.md | 48d906d335083f43a7f6c8bc62d24c34d569fbcfe04f42098623d257b1ff7390 | 48d906d335083f43a7f6c8bc62d24c34d569fbcfe04f42098623d257b1ff7390 |
| M1/source/v2-baseline/.claude/rules/dependencies.md | ced0516f065e25a36ea07d766865f26caae8d133a0bb1aca2976532ff62b6468 | ced0516f065e25a36ea07d766865f26caae8d133a0bb1aca2976532ff62b6468 |
| M1/source/v2-baseline/.claude/rules/error-handling.md | e54a59066bebc10832df82c8d818d8fa27dffd0de73706666198f5c0fcd491ea | e54a59066bebc10832df82c8d818d8fa27dffd0de73706666198f5c0fcd491ea |
| M1/source/v2-baseline/.claude/rules/performance.md | a4b54767111fefd9faae6ba7460e3abacf1ca9258ee1d265ac4eed496589c8b5 | a4b54767111fefd9faae6ba7460e3abacf1ca9258ee1d265ac4eed496589c8b5 |
| M1/source/v2-baseline/.claude/rules/security.md | d36e103f0fa842d038ba739a40e872fc768128a0a6a5474924e3b19a77640ac5 | d36e103f0fa842d038ba739a40e872fc768128a0a6a5474924e3b19a77640ac5 |
| M1/source/v2-baseline/.claude/rules/testing.md | 9c70dc874660db95c4c2032e80b575ea699ea1f514d946b36884c5c157cf0004 | 9c70dc874660db95c4c2032e80b575ea699ea1f514d946b36884c5c157cf0004 |
| M1/source/v2-baseline/.claude/skills/angular/SKILL.md | f4cf7baa3f7479f8d4df588dbbed75e96ff0c612caec199e283cdab13ccfd48e | f4cf7baa3f7479f8d4df588dbbed75e96ff0c612caec199e283cdab13ccfd48e |
| M1/source/v2-baseline/.claude/skills/api-versioning/SKILL.md | 2850c5e2f14d32aa049a1dd6b3983147bfa390d117176c8ce1f54c8eabedb892 | 2850c5e2f14d32aa049a1dd6b3983147bfa390d117176c8ce1f54c8eabedb892 |
| M1/source/v2-baseline/.claude/skills/authentication/SKILL.md | b08285e27eafd8f1b2d09a56f386c1f64a637af17dc097ecd2ffeb32c83e6191 | b08285e27eafd8f1b2d09a56f386c1f64a637af17dc097ecd2ffeb32c83e6191 |
| M1/source/v2-baseline/.claude/skills/build-fix/SKILL.md | 523ad63287ccdf6fa23941a5f6463c46e3ec17c1ed56fe6871f74e480c6ba9a2 | 523ad63287ccdf6fa23941a5f6463c46e3ec17c1ed56fe6871f74e480c6ba9a2 |
| M1/source/v2-baseline/.claude/skills/caching/SKILL.md | f4a8f3e028fc8152dfa30f2cedf30065906e3cea0189f23434dbd7487903bfd9 | f4a8f3e028fc8152dfa30f2cedf30065906e3cea0189f23434dbd7487903bfd9 |
| M1/source/v2-baseline/.claude/skills/ci-cd/SKILL.md | a914ababf5322baccea2549d55f222ee0d617c0be10c0fc37602b74472924f37 | a914ababf5322baccea2549d55f222ee0d617c0be10c0fc37602b74472924f37 |
| M1/source/v2-baseline/.claude/skills/code-review/SKILL.md | fdc0e9075d8379f9deea59174cb1b96f3f8e7a3b4085ab3c9f3ec4911b252f29 | fdc0e9075d8379f9deea59174cb1b96f3f8e7a3b4085ab3c9f3ec4911b252f29 |
| M1/source/v2-baseline/.claude/skills/configuration/SKILL.md | 340f98c96e329b770876bcd3bcfb1b84fe6c9b6477c96de767c3e24de21b2cd5 | 340f98c96e329b770876bcd3bcfb1b84fe6c9b6477c96de767c3e24de21b2cd5 |
| M1/source/v2-baseline/.claude/skills/custom-settings/SKILL.md | d4f76aeaa1597cd1ff7db33ea4d3d02fba4993cb97c8fefecdee23a0dbde6efb | d4f76aeaa1597cd1ff7db33ea4d3d02fba4993cb97c8fefecdee23a0dbde6efb |
| M1/source/v2-baseline/.claude/skills/dependency-injection/SKILL.md | bfac9b98b287bd8a0cc3a370eb521396a728b4ef8b4b53fb2e8c83282d57fade | bfac9b98b287bd8a0cc3a370eb521396a728b4ef8b4b53fb2e8c83282d57fade |
| M1/source/v2-baseline/.claude/skills/docker/SKILL.md | 801e00dd34525bafe3c53618a5f3751b228c6eb7607a06a1c3f6f2fc1197958f | 801e00dd34525bafe3c53618a5f3751b228c6eb7607a06a1c3f6f2fc1197958f |
| M1/source/v2-baseline/.claude/skills/ef-core/SKILL.md | c7120367231bd0bc3b6f92997f6f7450b9441c15604356651447d26cee67d762 | c7120367231bd0bc3b6f92997f6f7450b9441c15604356651447d26cee67d762 |
| M1/source/v2-baseline/.claude/skills/error-handling/SKILL.md | 4d514f0eec953ed9ba85d37f353ccc22b84a6137e9685e180bd2a250aa657b9d | 4d514f0eec953ed9ba85d37f353ccc22b84a6137e9685e180bd2a250aa657b9d |
| M1/source/v2-baseline/.claude/skills/git-workflow/SKILL.md | 940365f04436f41558ba951a3cd6a0dd77cc2e742314950f996962b08dc9bbc2 | 940365f04436f41558ba951a3cd6a0dd77cc2e742314950f996962b08dc9bbc2 |
| M1/source/v2-baseline/.claude/skills/health-check/SKILL.md | cb0c32f0a6bf5b7ffcac2a2d83bce3f4c236d6d89cd01fc1b5abad57a5435e8f | cb0c32f0a6bf5b7ffcac2a2d83bce3f4c236d6d89cd01fc1b5abad57a5435e8f |
| M1/source/v2-baseline/.claude/skills/http-api/SKILL.md | fd39b06310c679a0ea19ca4b86849319607f4b4abf6293106cdad08324fb8d89 | fd39b06310c679a0ea19ca4b86849319607f4b4abf6293106cdad08324fb8d89 |
| M1/source/v2-baseline/.claude/skills/httpclient-factory/SKILL.md | b6e17dcce8b801ae767545059c27a84cf425afb7c7f3fdb003cc481cd0466046 | b6e17dcce8b801ae767545059c27a84cf425afb7c7f3fdb003cc481cd0466046 |
| M1/source/v2-baseline/.claude/skills/logging/SKILL.md | cf8aa215f0f42d91c81fb0ee034b17da2841b156a4388ae372320883bda3868b | cf8aa215f0f42d91c81fb0ee034b17da2841b156a4388ae372320883bda3868b |
| M1/source/v2-baseline/.claude/skills/modern-csharp/SKILL.md | 1156651dbbb5dd51bc81a75f9236b3193198b54603ff941042b35bffce5fcc8c | 1156651dbbb5dd51bc81a75f9236b3193198b54603ff941042b35bffce5fcc8c |
| M1/source/v2-baseline/.claude/skills/project-structure/SKILL.md | d34f37f552adfbded3ec1b4b3b4c2e637a73ae36c74de14f2d67ab90528892cc | d34f37f552adfbded3ec1b4b3b4c2e637a73ae36c74de14f2d67ab90528892cc |
| M1/source/v2-baseline/.claude/skills/project-structure/references/backend-layout.md | 657c469b3be1a91827a1d78463f576d8dcfc069d70461e25097f37ba6f101650 | 657c469b3be1a91827a1d78463f576d8dcfc069d70461e25097f37ba6f101650 |
| M1/source/v2-baseline/.claude/skills/project-structure/references/solution-layout.md | 4c37997519285e15e74114adb0cb5ea26e90643750fd0c8d9d7ba75bc8eb4cbe | 4c37997519285e15e74114adb0cb5ea26e90643750fd0c8d9d7ba75bc8eb4cbe |
| M1/source/v2-baseline/.claude/skills/project-structure/references/technology-stack.md | f51d9b3e85b629b300b253555b7672a98a87cf5cb4197f593c8df3dea7962309 | f51d9b3e85b629b300b253555b7672a98a87cf5cb4197f593c8df3dea7962309 |
| M1/source/v2-baseline/.claude/skills/resilience/SKILL.md | a469c3456673622b4ca4eaa56dd05b803c18bb4c3af04e62ae6e0d784e025811 | a469c3456673622b4ca4eaa56dd05b803c18bb4c3af04e62ae6e0d784e025811 |
| M1/source/v2-baseline/.claude/skills/security-scan/SKILL.md | 4276a267d87d3611a6953c97678dd57693e4422a46dd4d0e82b8d630d02d05c2 | 4276a267d87d3611a6953c97678dd57693e4422a46dd4d0e82b8d630d02d05c2 |
| M1/source/v2-baseline/.claude/skills/security-scan/references/scan-layers.md | 4fe7396896e35e3d83f0b5c86a9046fd0278c5f38783581d0a744cb1a40fa846 | 4fe7396896e35e3d83f0b5c86a9046fd0278c5f38783581d0a744cb1a40fa846 |
| M1/source/v2-baseline/.claude/skills/serilog/SKILL.md | b3c2ab9cf5f89d5d506ffccf6140f5b06cc7b9f434206efb061ca69fa063d6d8 | b3c2ab9cf5f89d5d506ffccf6140f5b06cc7b9f434206efb061ca69fa063d6d8 |
| M1/source/v2-baseline/.claude/skills/swagger/SKILL.md | 7fe6fb21e419811282a0fe4a69b255dbe4cf39868d25932cf0cf07e1a596267d | 7fe6fb21e419811282a0fe4a69b255dbe4cf39868d25932cf0cf07e1a596267d |
| M1/source/v2-baseline/.claude/skills/testing/SKILL.md | 282c7a7185cc13992b20e6a22119dfb4803a1ebf69e4446042f9cdd343b88a9e | 282c7a7185cc13992b20e6a22119dfb4803a1ebf69e4446042f9cdd343b88a9e |
| M1/source/v2-baseline/.claude/skills/verify/SKILL.md | 38042cd665e1958a28290dcb4722aeb0ccb2f01c577a2a52203826ed237acf66 | 38042cd665e1958a28290dcb4722aeb0ccb2f01c577a2a52203826ed237acf66 |
| M1/source/v2-baseline/CLAUDE.md | 5d98d7aeedcde20ba044cc8b49cb0c4206d14fa478afca45c8a56f76e85bb4f4 | 5d98d7aeedcde20ba044cc8b49cb0c4206d14fa478afca45c8a56f76e85bb4f4 |
| M1/source/v2-baseline/CUSTOM_SETTINGS.md | 2449b93c170786e5525809aaf91ded093f2c00375defe7c349a85ad791b6ac4a | 2449b93c170786e5525809aaf91ded093f2c00375defe7c349a85ad791b6ac4a |
| M1/source/v2-baseline/SPECIFICATION.md | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |

## Completion boundary

Five requested reports only are retained in _CODEX_FINAL_AUDIT. No candidate corrections, phase-5.4 implementation, extra audit loops or remote work are authorized by this report. Final deliverable shape/CSV and hash checks are recorded after authoring.

### Final deliverable validation

PASS: exactly the five requested filenames are present; CSV parses with 24 required columns, 196 unique policy IDs and 1,176 candidate statuses; all canonical JSON anchors resolve to matching normalized text; every candidate evidence path/line exists and each quoted passage starts at the cited current line; three embedded Python reproduction blocks parse; no unresolved table placeholders or non-English Cyrillic text remains. Matrix distribution: 192 WORDING_ONLY, one SHARED_CONTRACT_VIOLATION, one PARITY_GAP, two UNCERTAIN. Candidate cells: 1,173 SAME, one DIFFERENT, two UNVERIFIED. CSV uses quote-all fields and CRLF records. The final-template SHA-256 values were checked again during report validation and remained identical. Completed audit work is closed; the explicitly listed limitations remain unverified, not pending background work.
