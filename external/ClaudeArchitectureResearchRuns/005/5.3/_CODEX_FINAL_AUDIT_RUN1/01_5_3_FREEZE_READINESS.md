# Audit A — Phase 5.3 freeze readiness

## Decision and authority

The current output is judged against normalized policy text, the additional normalized invariants, each candidate's own architecture, its local accepted refinement task, and the user's final strict P4 decision. Historical V2 examples and self-reported refinement PASS results cannot override the normalized corpus. A parity-only gap is not a freeze blocker.

| Candidate | Verdict | Qualification |
|---|---|---|
| M | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | No confirmed blocker; local enforcement and runtime coverage limitations. |
| M1 | BLOCKED | A-001, ARC-025 remote-HTTP exception. |
| L0 | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | Strict P4 passed; broader host/state tests not run. |
| L1-Restart | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | Strict P4 passed; PAR-003 interpretation remains uncertain. |
| K0 | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | Nested-cwd positive test remains unverified. |
| K1 | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | Advanced binds/graph tests unverified; optional manifest discrepancy. |

## Source integrity and 196-policy coverage

All six required directory/file sets were present. Each top-level CANDIDATE.md is byte-identical to its baseline/CANDIDATE.md. Baseline TASK.md is identical across six (SHA-256 in report 04). All six complete source trees have the same path/content set, including inventory and invariants. The live inventory contains ten groups and 194 unique policy IDs; the invariant file contributes exactly GOV-017 and GOV-018, both MUST, with no collision: 196 unique IDs.

The matrix is a policy-by-policy static semantic comparison with actual final-file evidence. SAME means the inspected instructions express the normalized obligation under its trigger, scope and selected stack. It does not mean an automated checker enforces the whole policy, nor that every possible conflicting example was disproved. Conditions such as persistence changes, security-sensitive changes, or frontend work remain conditional; they are not removed merely because a reusable template has no implementation yet. No row is dropped as dormant.

Text retrieval located candidate passages; retrieval scores were not verdicts. Substantive passages and surrounding owners/routers were inspected, including contrary evidence for exceptions and configuration differences. A technique mention, frontmatter description or maintainer map alone does not prove ownership. Compound passages were resolved to substantive body/decision-table anchors where needed. Limitations concerning exhaustive ownership and runtime reachability remain explicit (LIM-001/005).

All 103 rule files have a paths declaration (M 11, M1 14, L0 24, L1-Restart 19, K0 14, K1 21). This is a structural count, not proof that every glob is minimally scoped or works identically in a live host. Candidate checkers passed their own route/reference/glob/structure diagnostics. Independent removal probes for verify and fail-closed metadata were detected in all six, and missing selected persistence MODULE was detected in all three capability candidates. No actual broken critical route was independently confirmed.

## A-001 — M1 weakens the remote-HTTP boundary

**Confirmed blocker; HIGH severity; HIGH confidence.** Affected policy: ARC-025 (MUST, path-triggered backend rule).

1. **Governing hard contract:** `M1/source/inventory.json#policygroups[id=architecture].policies[id=ARC-025].normalized_policy` says: “Infrastructure translates remote HTTP responses into Application-facing abstractions; do not leak HttpResponseMessage or remote transport concerns into Application.” The common `M1/baseline/TASK.md:151` makes the inventory controlling and `:156` prohibits strengthening, weakening, adding or removing policy semantics. The current audit's explicit precedence agrees.
2. **Exact current defect:** `M1/output/template/.claude/rules/architecture.md:135` through line 137 adds “into Application contracts unless the Application explicitly models HTTP.”
3. **Reproducible static witness:** read those three lines and compare the normalized ARC-025 field. For a task adding a supplier HTTP integration, an Application interface returning `HttpResponseMessage` can claim the local exception simply because that interface explicitly models HTTP. No exceptional user approval or approved architecture change is required by this sentence.
4. **Expected / actual:** expected unconditional translation into the Application-facing abstraction under the current architecture; actual instruction explicitly permits a category of transport leak. This is a permission difference even without running a model.
5. **Material impact:** the use-case boundary may acquire remote protocol/response lifetime concerns and require HTTP-shaped testing rather than a transport-independent abstraction. This is a plausible consequence of the contradictory permission, not a claim that a generated application actually did so.

Contrary evidence was examined: M1 architecture lines 56–57 bar ASP.NET Core transport types, but that does not remove the separate remote-HTTP exception. The `httpclient-factory` skill's anti-pattern against leaking responses does not reliably cancel an explicit exception in the governing architecture rule. `M1/source/v2-baseline/.claude/skills/httpclient-factory/SKILL.md:22` contains the historical exception; that explains lineage, but normalized precedence resolves it rather than creating an unresolved source conflict. The other five candidates use the unqualified boundary (six-way citations in PAR-001).

This remains a 5.3 blocker even if Phase 5.4 is postponed. No repair was performed; a later correction would need a targeted semantic recheck before removing BLOCKED.

## Six independent architecture assessments

### M

**FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS.** `M/CANDIDATE.md:14` requires V2 lineage; `:29` excludes levels, kinds and capability machinery; `:45`, `:80`, `:124` define owner/rule/skill separation. Current flat `.claude/rules/`, the technology-stack import (`CLAUDE.md:9`), governance in CLAUDE and workflow router (`:157`) fit that identity. No capability system was demanded. Existing checker and all JavaScript syntax checks passed.

The M reference pre-hook returning success is not a confirmed defect: `M/REFINEMENT_TASK.md:91` requires detection and architecture/reference validation, while the stronger explicit before-execution requirement belongs to M1's task. M's approval policy remains in `CLAUDE.md:112`, its post hook routes reference changes (`.claude/hooks/dependency-guard.mjs:130`), and the independent post-route reconfirmation found the expected reminder. Thus the two generic pre-block expectations are NOT_APPLICABLE, with RCH-002 retained as a delivery risk. LIM-001 through LIM-007 apply.

### M1

**BLOCKED by A-001.** The four static slots, manifests, selection, frame placement versus leaf technique, and flat non-slot M organization match `M1/CANDIDATE.md:51`, `:73`, `:144`, `:247`. CLAUDE imports technology/selection and four capability decisions at lines 133–138. Selected persistence MODULE removal was detected; clean checker and syntax tests passed. Structural success does not cure ARC-025. Floating-version exception scope is separately UNVERIFIED (PAR-004), not a second confirmed blocker. LIM-001 through LIM-007 apply.

### L0

**FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS.** `L0/CANDIDATE.md:20`, `:101`, `:116`, `:175` define four levels, stable-direction conformance, technology neutrality and always-loaded decisions. Current rules are level-first, with architecture overview and project decisions imported (`CLAUDE.md:9–10`) and no capability selection system. Strict P4 passed the observed clean state and fixed lexical tests below. XML package/reference checks identified intended violations after failure events. The initial comment test also removed a real reference; its reminder was legitimate. The isolated comment-only reconfirmation passed. LIM-001 through LIM-007 apply.

### L1-Restart

**FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS.** This exact folder is the scoped L1 candidate, not the abandoned L1 branch. Four levels plus four static capability slots and architecture-frame/leaf routing were observed; the final strict no-concrete-pointer rule is documented in `.claude/INSTRUCTION_MAP.md:7`. Current CLAUDE imports adopted style, project decisions and frontend stack (`:9–11`). Missing selected MODULE was detected and strict P4 passed. PAR-003 records uncertain approval/default semantics for production migrations. Do not revive an older Docker-pointer exemption. LIM-001 through LIM-007 apply.

### K0

**FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS.** `K0/CANDIDATE.md:17`, `:74`, `:135`, `:154` define seven kinds, scopes, a decision register and conformance graph. Current scope-first standards, Kind declarations and imported DEC register (`CLAUDE.md:7`) are consistent. No capability replacement mechanism is required. Clean root checker and syntax tests passed. Two nested-cwd invocations returned empty-directory errors from the independent fixture; they do not show a broken root resolver, but the intended positive nested test remains UNVERIFIED (LIM-008). LIM-001 through LIM-007 also apply.

### K1

**FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS.** `K1/CANDIDATE.md:18`, `:54`, `:67`, `:114`, `:185` define K kinds/scopes, graph, four slots, decision selection, frame/leaf boundaries and declared binds. Current imported DEC register, scope-first STD rules and capability facets preserve these mechanisms. Clean checker/syntax and selected-module negative tests passed. Full graph/binds sabotage and all inherited K0 register-format particulars are not independently certified (LIM-005). Two optional manifest mismatches are a provenance limitation (LIM-009), not evidence that current templates were mutated during this audit or that a particular instruction violates a hard rule. LIM-001 through LIM-007 also apply.

## Strict P4 — finite common corpus

The actual L0 prohibited vocabulary contains 41 entries. Each was appended as `Technique: <term>` to one existing Level 0 file and one existing Level 1 file in temporary copies of both L0 and L1-Restart: **164/164 intended rejections**, with technology diagnostics. Two legitimate positive strings at both levels in both candidates gave **8/8 accepted** cases. Docker, Swagger, Jest, Scrutor, NuGet and EF Core are included. Corpus, commands and observations are in report 04.

Documented fixed-platform vocabulary is .NET, C#, TypeScript; maintained maps additionally explicitly describe Git repository-safety vocabulary and HTTP protocol vocabulary (`L0/output/template/.claude/INSTRUCTION_MAP.md:19`, `L1-Restart/output/template/.claude/INSTRUCTION_MAP.md:7`). HTTP/TLS/OIDC/CSRF/SQL protocol or standards words are not blanket exemptions for implementation products. ASP.NET Core and NuGet are not exempt. The positive test exercised .NET/C#/TypeScript/HTTP; it did not independently exercise every protocol word or Git. No context-sensitive Docker-pointer exception was applied. This demonstrates finite cases, not unlimited synonym recognition.

## Test interpretation and limitations

All 40 discovered JavaScript files passed syntax checks, and six pristine instruction-checker invocations passed. The finite independent suite records commands, JSON input, exit status and diagnostics, including after-failure XML cases, malformed/BOM hook input, dependency flags, routing and structural negatives. Historical refinement-report test totals are not included in independent counts.

There were 381 process invocations: 363 asserted PASS results, three assertions deemed NOT_APPLICABLE, two UNVERIFIED nested-cwd assertions, and 13 setup/observation calls also categorized NOT_APPLICABLE. Six raw harness FAIL labels are retained, not silently relabeled as successful tests. No dynamic confirmed defect survived adjudication; the confirmed blocker is static A-001.

| ID | Disposition | Meaningful unverified scope |
|---|---|---|
| LIM-001 | NOT_RUN | Real Claude host activation, tool matching, timeout/onFailure behavior and actual context loading. Direct Node invocation proves only local script behavior. |
| LIM-002 | NOT_RUN | Linked Git worktrees, committed HEAD transitions, all shell/edit/move/rename variants and UTF-16/BOM combinations. Git initialization, nested paths, malformed JSON and UTF-8 BOM were exercised. |
| LIM-003 | NOT_RUN | Stop repeated-content changes, session/HEAD/worktree identity and reminder deduplication. Only the recursive Stop guard was independently exercised. |
| LIM-004 | NOT_RUN | Full MSBuild evaluation, imported .props/.targets, XML entities/conditions and arbitrary encodings. Tests used literal .csproj and Directory.Packages.props attributes. |
| LIM-005 | UNVERIFIED | Exhaustive owner uniqueness/precedence across every technique example, all graph-negative fixtures, capability replacement/optional-frontend disabling, and removal of both sides of binds. Clean checkers and selected negatives are not exhaustive independent proofs. K1 inheritance of every K0 register-format detail was not resolved into a blocker. |
| LIM-006 | NOT_RUN | Actual .NET/Angular builds, formatter/analyzer execution, effective warning escalation, security scans, databases and production deployments. No packages installed/restored. |
| LIM-007 | NOT_RUN | Paired application-generation experiments. No observed code-quality ranking or causal quality estimate is claimed. |
| LIM-008 | UNVERIFIED | K0 nested-cwd acceptance: original and one reconfirmation reported empty fixture directories; neither isolated a root-discovery defect. No further retry. |
| LIM-009 | UNVERIFIED | K1 MANIFEST.sha256 disagrees with current GOAL_PROMPT.txt and REFINEMENT_TASK.md. The latter matched the pre-audit snapshot; the manifest's historical task version/approval chain cannot be reconstructed from hashes. Current local task is used as requested. |

PAR-003 and PAR-004 add two unresolved semantic questions, for eleven enumerated unresolved items overall. This is a reporting index, not a claim that only eleven individual behaviors could remain untested. Five provisional freeze decisions are intentionally qualified. No unconditional all-six freeze is recommended.
