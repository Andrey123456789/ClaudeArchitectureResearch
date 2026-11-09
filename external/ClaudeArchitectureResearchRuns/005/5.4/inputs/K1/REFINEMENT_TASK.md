# K1 Controlled Refinement — Iteration 005 / 5.3 (convergence-focused)

## 1. Contract and definition of completion

Refine **Candidate K1**, not its architecture concept. Use immutable K1 Run-02 to produce a **demonstrably strictly better** standalone implementation. Repair every mandatory D1–D11 defect in `audit/DEFECT_DOSSIER.md`; perform the D12 policy/V2 review and D13 value/efficiency review. Confirm there is **no regression** against any established baseline behavior or frozen research requirement. A tie, cosmetic cleanup, unproved claim or exchanged PASS/FAIL is not promotion.

This task supersedes the previous wording of this file **only as an execution/verification specification**. The frozen design, inventories and dossier are authoritative; no research metric, architecture or policy is relaxed or redefined. Execute one bounded repair program, one finite regression matrix and one complete final confirmation (repeat only if the actual template changes to repair a discovered defect). **A complete clean confirmation is the terminal condition.**

## 2. Read scope and immutable boundaries

Read in this order:

1. `CANDIDATE.md` and `audit/DEFECT_DOSSIER.md` (D1–D13, exact failure evidence and gates);
2. `audit/EXTERNAL_MECHANICS_NOTES.md`, `audit/BASELINE_SELECTION.md`, `audit/RUN_COMPARISON.md`, `audit/RUN3_DECISION.md`, `audit/evidence/INDEPENDENT_TESTS.md`;
3. `baseline/CANDIDATE.md`, `baseline/TASK.md`, `baseline/GENERATION_REPORT.md`;
4. `source/shared-research-invariants.json`, `source/inventory.json`, complete `source/v2-baseline/`;
5. actual files under `baseline/template/`, especially `.claude/settings.json`, `.claude/hooks/dispatch.cjs`, `.claude/scripts/{lib,check-instructions,check-manifests,check-cochange}.cjs`, the four selected module manifests/contracts and their facets, the decision register, MAP, skills and scoped standards.

Read all remaining template files as needed for the source-to-owner/policy audit, not as a reason for an unbounded research search. The Run-01 template is deliberately absent. Its reports are comparison evidence only, never a replacement starting point. Do not inspect/copy sibling candidates, other workspaces, online code, external transcripts or hidden evaluation data. The relevant current hook semantics are recorded in `audit/EXTERNAL_MECHANICS_NOTES.md`; do not turn this task into an open-ended documentation investigation.

Do **not** modify `baseline/`, `source/`, `audit/`, `CANDIDATE.md`, `GOAL_PROMPT.txt` or this task. Write only under `output/`.

**Starting procedure:** Ensure `output/` contains no work from a previous attempt; if it does, report the unexpected state instead of overwriting it. Copy `baseline/template/` exactly to `output/template/`, verify byte identity, record one initial tree hash/file inventory, and only then start editing. `baseline/template/` must remain unchanged. Create a single test/audit harness under `output/.work/`, **keep it until the final audit and report are done**, and remove it only last. Record one final tree hash; repeat hashes only to investigate an actual integrity failure.

## 3. Non-negotiable K1 identity and policy invariants

K1's organizing order is **Capability -> Kind -> Scope**:

- The seven Kinds are `OP`, `DEC`, `STD`, `KNW`, `WF`, `ENF`, `IN`. Kind determines mechanism/owner/loading; Scope determines applicability. Scopes remain `common`, `backend`, `backend-tests`, `frontend`, `delivery`, `repo/meta`. Standards stay scope-first under `.claude/rules/<scope>/`.
- Conformance direction is `WF -> KNW -> STD -> DEC -> OP`, additionally `ENF -> STD / DEC`. IN may request but cannot override decisions/policies. Routing messages to invocable skills are **not** conformance dependencies; legitimate skill-private boundaries remain enforced.
- There is exactly **one always-loaded decision register** and no second hierarchy. Do not introduce a Level system, Levels directories, extra Kinds/Scopes, or an artifact just to fill a Kind×Scope cell.
- Exactly four **static** capability slots: `architecture` (required frame, `clean-architecture`); `persistence` (required leaf, `ef-core` + `sqlserver` variant); `backend-testing` (required leaf, `nunit`); `frontend` (optional leaf, currently `angular`). One selected implementation per required slot, zero/one optional frontend. Every slot has `CONTRACT.md`; selected implementations have `MODULE.md` and only their selected facets. No dynamic discovery/unselected runtime implementation.
- Every facet has correct Kind/Scope/Capability ownership; role-based names and module manifest coverage are preserved. Policy independent of the selected implementation remains in the neutral non-slot K system; concrete technology stays in the owning module. External workflows use slot/facet roles; implementation names are confined to the specified allow-list. The frame owns placement, leaf modules own technique; unavoidable cross-slot bindings are explicit on dependent leaves.
- Required cross-slot obligations are substantive: **persistence -> architecture** and **backend-testing -> architecture**. They are part of K1 identity, not optional merely because a corrupted contract and manifest agree on `Binds: —`. Truly independent modules may retain `Binds: —`; optional frontend clearing must be valid without hunting unowned implementation-specific prose.
- Non-slot technologies remain embedded in their K ownership; do not globally neutralize K1 into L1/M1. Preserve all **194 inventory policies + GOV-017/GOV-018 (196)** with exactly one authoritative owner, original trigger class, minimum scope, normative strength, conditions and usable V2 technique. No policy is weakened or artificially duplicated to improve counting.

Baseline size is evidence, not a rigid output quota: 85 runtime files, 346,715 bytes and approximately 4,849 always-loaded tokens. Any growth must be justified by a concrete reliability/contract need. No generic meta-framework or extra layer for its own sake.

## 4. Engineering approach: repair causes together, not one symptom per pass

Before implementation, map D1–D11 to the underlying implementation surfaces and a **single bounded test fixture family** per surface. Repair interdependent files/config/checkers together. All newly written verification code must exercise the real generated implementation and its config (including settings/event dispatch), not a simulated checker that merely reproduces expected answers.

**Do not** treat fixing a test harness as evidence that a runtime defect is repaired. A negative fixture passes only if the correct checker/hook rejects it with a relevant diagnostic. A positive fixture passes only if the relevant checks accept it without new warnings/errors. Use isolated disposable copies per mutation; do not contaminate the authoritative template. Keep a concise results matrix with fixture, expectation, observed result, evidence and owning defect ID.

### 4.1 D1 / D2 / D3 / D7 — hook root, launching, failure and encoding are ONE system

Distinguish and explicitly model:

1. **Launcher/config root**: where stable `.claude/hooks/` code is located (may come from `${CLAUDE_PROJECT_DIR}`). Its purpose is locating implementation, **not** determining what repo is being edited.
2. **Active repository/worktree root**: derived from hook input `cwd` and appropriate Git context. Resolve nested dirs/linked worktrees, including when launcher root points to the original checkout. All Git, path normalization, package/project scanning, instruction scanning, Stop/co-change and state storage target the active root.

Use Windows-safe, path-with-spaces-safe exec-form command hooks where appropriate (`command: "node"`, `args: [...]`) with supported host interpolation and event dispatch; no POSIX-only shell quoting/globbing assumptions. Handle normal JSON stdin, UTF-8 BOM, CRLF; deterministically handle missing/empty/malformed input. Where relevant to manifest reading, support normal Windows-created encodings (including BOM-tagged UTF-16LE/BE) or fail visibly and deterministically rather than silently skipping a malformed file. Do not turn encoding discovery into a generic charset project.

Critical policy `PreToolUse` guarding dependency/project-reference commands must **fail closed** on exceptions, missing script, malformed input and host-level failure/timeout using the documented `onFailure: "block"` contract or a proven equivalent. Advisory Post/Stop behavior is not to be made blocking merely for consistency. `stop_hook_active` prevents reminder recursion.

Update `.claude/scripts/check-instructions.cjs` in the same change as `.claude/settings.json` and dispatcher semantics: it must reject incorrect dispatch arguments, missing targets, missing/mismatched event matchers, missing critical fail-closed configuration, missing required Post shell/failure coverage, and obsolete launcher assumptions. Static configuration checks alone do not prove worktree behavior: use real process-level fixtures below.

### 4.2 D4 / D5 — pre-execution mutation routing

Use a **bounded token-aware, table-driven** command classifier, not a giant permissive regex. Check relevant `tool_input` command forms used for Bash and PowerShell. Required classes:

- `dotnet add/remove [project] package`, supported variants/option positions, and `dotnet add/remove [project] reference` plus supported alternate reference syntax;
- npm `install/add/update/remove/uninstall`, pnpm `add/update/remove`, yarn `add/update/upgrade/remove`, with global options before subcommands and options consuming values (`--prefix`, `--workspace`, `--dir`, `--cwd` and supported equivalents);
- exact dependency versions for additions/updates and flags `--force` / `--legacy-peer-deps` even under global-option forms;
- commonly chained commands and shell wrappers that are in the documented fixture set;
- unrelated/read-only/restore-only commands that must not be falsely treated as dependency mutation.

Dependency changes must route through their authoritative workflow, and project-reference graph changes are **Reserved pre-execution decisions** even if the resulting graph would be structurally legal. A post-validation finding never substitutes for this pre-execution control when a documented command form can be recognized. Do not conflate missing approval with a harmless syntax warning.

### 4.3 D6 — post-execution validation must use ACTUAL state, even after failure

Command classification controls known mutations **before** execution; command text is not a trustworthy oracle for files actually changed. For Bash/PowerShell, observe active-worktree manifests/instruction files/project-reference graph after both:

- `PostToolUse` (successful shell calls);
- `PostToolUseFailure` (failed shell calls which may have had partial side effects).

Use bounded per-worktree actual-state tracking; a single first-observation baseline/scan is acceptable. Required delta cases: initial/fresh and subsequent observations; first and later HEAD transitions; same-path content rewrites; tracked/untracked additions where relevant; deletions/moves/renames; failed shell after a real partial mutation; unrelated successful or failed shell with no relevant state change; root and nested cwd including real linked worktree and nested worktree cwd. Correctly separate worktree state from main-checkout state. Do not invent deletions for excluded build directories, `node_modules`, subrepositories or excluded nested Git roots. Avoid scanning the entire repository on every unrelated command. Recover deterministically from missing/inconsistent state.

At minimum, post validations must detect prohibited inline NuGet versions under CPM, missing/floating central versions, disallowed package changes, illegal project-reference direction, Reserved reference graph modifications, and relevant instruction-structure changes. Retain correct owner/workflow pointers and readable diagnostics; do not duplicate policy prose in hook output.

### 4.4 D8 / D9 — invocation and material-state reminders

Manual instructions like `node .claude/scripts/check-instructions.cjs` must work when Claude has `cd`'d into a nested directory or linked worktree. Choose and document one **cross-platform active-root-aware** invocation convention, then update all affected skills/rules/commands consistently. Do not make these instructions accidentally target the launcher checkout.

Stop/co-change deduplication must distinguish unchanged repeated state (no new reminder) from **materially changed contents on the same paths** (new reminder allowed). Bound state size, keep Git operations read-only and per-worktree, preserve normal seed/migration/test co-change checks, avoid infinite loops with `stop_hook_active`, and do not emit reminders indefinitely on repeated identical state.

### 4.5 D10 — binding enforcement cannot be bypassed by self-consistency

Parse actual slot contracts, the selected module manifests and their facet declarations. Check consistency with **independent K1 slot obligations**, not only whether a manifest `Binds:` names any legal slot. The two frame bindings required in §3 must survive independently of mutable prose. Validate required leaf->frame direction and current reason/role, while permitting independent `Binds: —` where justified. No frame->leaf ownership cycle.

The following are distinct negative fixtures and must fail with a **binding-related** diagnostic:

- persistence module `Binds:` removed or redirected;
- backend-testing module `Binds:` removed or redirected;
- corresponding `CONTRACT.md` obligation removed but module unchanged;
- **both** contract obligation and module `Binds:` removed or redirected together (the self-consistent-violation test);
- binding target names nonexistent slot or wrong slot;
- extra static slot, second selection for a required slot, or a missing required slot/selected facet.

Positive fixtures: current baseline obligations; architecture/frontend `Binds: —` where legitimately independent; correct frame/leaf placement; expected optional frontend clearing. An optional frontend clearing fixture must remove its entire owned selection/module/facets **in an isolated copy** and verify there are no remaining unowned Angular-specific leaks; the authoritative K1 output retains angular selected.

### 4.6 D11 — complete, meaningful K conformance graph including ENF

Keep and test the working Run-02 ranked `WF -> KNW -> STD -> DEC -> OP` checker. Add **bounded authoritative ENF conformance-dependency declarations and verification** within existing K1 ownership/manifest/checker surfaces. Do not invent a separate generic policy graph service, and do not classify arbitrary JS module imports or ordinary skill/routing pointers as normative dependencies.

Mechanically validate each declared ENF facet's presence, Kind/Scope/Capability, authoritative conformance targets, and correct dependency direction (`ENF -> STD/DEC`). An ENF facet must not evade the graph simply because its conformance metadata is absent: validate declaration/completeness for every present ENF facet, including the non-slot enforcement surfaces that actually assert a policy dependency. Use existing module manifests and/or a small explicit owned declaration where feasible. Keep any new representation minimal and auditable; distinguish conformance metadata from runtime imports and routing links.

Required **discriminating** fixtures against the actual checker:

- legitimate `WF -> KNW`, `ENF -> STD` and `ENF -> DEC` accepted;
- `DEC -> STD`, reversed rank and any actual cycle rejected;
- ENF conformance target `KNW` or `WF` rejected;
- missing/invalid authoritative declaration for a required ENF facet rejected;
- removing/replacing an ENF facet or lying about its Kind/owner rejected;
- valid invocable-skill routing references are **not** mislabeled as conformance edges.

Beware false proof: a checker that validates only a list manually preselected for testing, or merely parses some declarations without enforcing their completeness, does **not** establish D11.

## 5. Finite reproducible behavioral matrix

Build ONE harness under `output/.work/`; reuse it through every repair and the final report. Tests may be organized by component but should share fixture construction, result capture and reset. Use a **real Git repository and real linked worktree**, with `GIT_CEILING_DIRECTORIES` (or equivalent containment) from the start of Git fixtures, not after noisy discovery. Include a directory with spaces. Execute generated scripts in controlled child processes with actual stdin/environment and assert exit code, diagnostics, active-root effects and relevant files; do not assume this already-running Claude session will activate newly generated hooks.

| Group | Minimum accepted evidence |
|---|---|
| Hook launch/root | root cwd; nested backend/frontend cwd; whitespace path; real linked worktree; nested worktree cwd; launcher root != active root; violation only in worktree found; main checkout unaffected |
| Input/failure/encoding | JSON, UTF-8 BOM, CRLF, valid Windows manifest encodings; malformed/empty input; missing/crashing target; critical `onFailure` static semantics and controlled-process failure; advisory/Stop non-loop |
| Pre-route | add/update/remove, global options consuming values, force flags, dotnet reference variants, chains, Bash/PowerShell inputs, safe restore/read-only commands |
| Actual state | PostToolUse + PostToolUseFailure; first/later snapshots; HEAD changes; same-file rewrites; create/delete/rename; tracked and relevant untracked changes; no relevant change; per-worktree isolation |
| Manifest/architecture | CPM inline/missing/floating version; deny/approval cases; project-reference illegal direction; Reserved change; direct Edit plus shell mutation |
| K1 Kind/Scope | seven Kinds and allowed mechanisms/scopes; ranking and reverse edges; ENF declaration/completeness and allowed/forbidden edges; routing-pointer exception |
| Capabilities | four static slots; selected-only runtime; manifest/facet/contract/Kind/Scope matching; leak rules; independent required `Binds:`; both-sides-removed test; frame/leaf separation; optional frontend clear |
| Stop | first reminder; unchanged silence; same-path material rewrite reminds; repeat silence; `stop_hook_active` silence; worktree-local state; seed/migration/testing obligations |
| Fidelity/hygiene | 196 source-based policy records; owners/triggers/minimum scopes/strength; V2 technique; references; runtime English; empty product SPECIFICATION; no sibling/external dependencies |

Negative mutation fixtures must fail **for the intended reason** (matching diagnostic category and artifact), not because the fixture accidentally breaks setup or another global invariant. Positive fixtures should not rely on suppressing a meaningful checker error. Keep all fixtures and matrix finite; no randomized indefinite fuzzing, grammar-space exploration or verifier mutation-testing once these gates pass.

## 6. Frozen-policy and K1 capability substantive audits

### 6.1 Policy fidelity: 194 + 2

Build an evidence-backed source-to-output reconciliation for all 194 `source/inventory.json` records and GOV-017/GOV-018 from `source/shared-research-invariants.json`. For each: owner (one), trigger class, minimum scope, normative strength/conditions and V2 technique availability. Use actual source wording plus output owner/routing evidence, not merely substring counts or a checker reporting `196`. Report counts for missing, duplicate normative owners, trigger-role deltas, minimum-scope misses and genuine semantic weakening/strengthening; every promotion count must be zero. A concise ledger under `.work/` is sufficient; summarize the full results in the report.

Differentiate one authoritative owner from non-normative cross-references, examples and routing summaries. Restore missing useful V2 technique only when substantive; do not duplicate rules to maximize lexical overlap.

### 6.2 Structural/capability review

Verify: Kind classification and correct mechanism, Scope applicability/path headers, one DEC register, no Level hierarchy, entire K graph, facet/manifest table completeness, contract item provider completeness, correct declared technology/variant, non-slot vs selected implementation ownership, implementation-name leak negatives, static slot count, frame/leaf boundary and independent `Binds:` obligations. Check all references, imports, facet role paths, hook targets and activation/routing. Prove optional frontend clearing in an isolated temporary copy only; do not remove it from final K1.

### 6.3 Efficiency review, not optimization campaign

Compare always-loaded character/token estimate, file count/bytes and module/decision/hook complexity with Run-02. Review duplicate wording and routing once; only alter something if substantive correctness/maintainability improves without losing trigger reliability or policy availability. No extra scaffolding, meta-layers, global vocabulary rewrites or aesthetic refactors in the absence of a concrete defect. D12/D13 are mandatory reviews; their findings do **not** create an unbounded search for hypothetical improvements.

## 7. Execution ordering and bounded convergence

1. **Establish** pristine Run-02 copy, one baseline hash and identity evidence. Summarize D1–D11 repair surfaces and plan fixtures before editing.
2. **Reproduce** a representative subset of dossier failures once against the baseline if it is cheap and diagnostic. Do not rerun the whole baseline suite after each edit.
3. **Implement together**: hook settings/dispatcher/root/encoding, pre-route vs actual-state post-events, Stop, manuals, checker settings expectations; then K1 binding/ENF graph/slot conformance. Update owner instructions for new behavior. Do not make the checker merely conform to old incorrect serialization.
4. **Run focused fixtures** for each repair. Fix concrete template defects; if a test itself is wrong, repair the test and re-evaluate the affected case without calling it a runtime regression.
5. **Run the complete documented finite matrix against the final template**, perform all policy, structure, V2, source and context reviews. Revisit all earlier PASSES, not just the newest fixes; no traded regressions.
6. **Run ONE full cumulative confirmation audit** on final template content. If and only if it reveals an actual template defect, repair that defect, rerun impacted fixtures, and repeat confirmation because template bytes changed. Once a full confirmation audit reports **zero concrete template defects**, convergence is established.
7. **Write** `output/REFINEMENT_REPORT.md` from evidence; one final file inventory/hash and hygiene/consistency check. A report-only edit does not require a new template audit. Remove `output/.work/` **last**. Check `output/` contains exactly `template/` and `REFINEMENT_REPORT.md`. **STOP IMMEDIATELY.**

### Explicit anti-loop guardrails (learned from prior 5.3 passes)

- Do **not** move/restart the already-running Claude Code session in `output/template/` or a sandbox to prove that newly written hooks fire. Controlled execution plus documented host semantics is the required evidence; claim no fresh live-host proof unless actually obtained.
- Do **not** audit the audit, test the test framework via artificial mutants after required negative fixtures pass, write a second harness, or reconstruct tests from compacted conversations/transcripts after deleting `.work/`.
- Do **not** perform repeated whole-tree hashes, re-read entire baseline repeatedly, start unbounded shell/Markdown fuzzing, or launch a broad search for new hypothetical classes once the defined gates pass.
- Do **not** make the scope bigger due solely to cosmetic review comments or to obtain stronger narrative confidence. If a concrete required gate fails, fix it; if it passes, move on.
- A new implementation trade-off without demonstrated net gain should be reverted. Never relax leak detection, K graph, policy semantics, root safety or critical failure mode to manufacture PASS.
- If a gate genuinely cannot be established within the authorized scope, report `BLOCKED` with the exact missing evidence/failing fixture; do not substitute a claimed or invented PASS. A nonpromotable completed attempt is `NOT_PROMOTED`, not `STRICTLY_BETTER`.

## 8. Strict cumulative promotion gate

Promotion requires **every** item, not an average score:

1. D1–D11 fixed with final-file evidence; D12 source fidelity and D13 efficiency/capability reviews performed.
2. All 194 policies + 2 invariants preserved: zero owner/trigger/minimum-scope/normative-strength regressions; no broken internal references.
3. Exactly K1's Capability -> Kind -> Scope, seven Kinds/six Scopes, one register, complete conformance direction including ENF, no new Levels/slots/dynamic composition.
4. All contracts/modules/facets/role references and four-slot composition checked; independent required cross-slot `Binds:` cannot be deleted from both sides to evade checks; leaf/frame and leak tests pass; optional frontend clearing passes.
5. Runtime hooks/structure checker and instructions agree; critical PreToolUse fails closed, Bash/PowerShell post-success/post-failure actual-state detection works, root/nested/worktree/Windows tests pass, content-aware Stop works without loops.
6. Pre-execution dependency/reference classification is sound for documented forms; post-validation does not solely depend on shell text; prohibited and safe mutation controls distinguish correctly.
7. No template-wide checker weakening or PASS exchange; V2 technique and policy availability no worse; added complexity justified by demonstrated benefit.
8. Complete finite final regression matrix passes, and **one complete final confirmation audit finds zero concrete template defects**.

An unproven gate is not a PASS. A tie or cosmetic-only gain is not a strict improvement.

## 9. Required final deliverables and report

Only:

```text
output/
├── template/
└── REFINEMENT_REPORT.md
```

The report must include: `STRICTLY_BETTER`, `NOT_PROMOTED` or `BLOCKED` (truthfully); baseline provenance and initial/final tree hashes; exact changed/added/deleted files; D1–D11 disposition with evidence by fixture group; D12 196-policy reconciled owners/trigger/scope/strength/V2 results; D13 cost/complexity and replacement review; K graph + ENF authoritative dependency mutation results; module/manifest/contract/facet, slot cardinality/leak/Binds including both-sides-removed negative case; optional frontend clear; Hook root/Windows/critical-failure/Bash/PowerShell-success-and-failure/state/worktree cases; dependency/reference routing; Stop content identity; before/after size, file count and always-loaded estimate; references/hygiene; actual primary and confirmation audit outcomes; intentionally reverted neutral trade-offs; known limitations.

Explain **why** the final artifact is strictly better than the immutable baseline if promoted. Do not cite a self-written test count without preserving truthful fixture-level evidence until report completion. Do not claim tests, host-hook activation, policy reconciliation or absence of regression that were not actually performed.

The task ends **immediately** after complete acceptance, report and cleanup. No extra proof campaign and no next-iteration planning inside the run.
