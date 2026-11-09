# K1 5.3 Defect Dossier

Every item marked **MANDATORY** must be resolved before promotion.

The refinement must preserve all frozen policy semantics, trigger classes, minimum scopes, and K1 identity.

## D1 — CRITICAL — Hooks inspect the main checkout instead of the active worktree [MANDATORY]

Run-02 launches its dispatcher through `CLAUDE_PROJECT_DIR` and the dispatcher computes:

`ROOT = rootFrom(__dirname, 2)`.

That is the checkout containing the launched dispatcher, not necessarily the repository/worktree Claude is currently editing.

Independent real-Git-worktree reproduction:

1. create a main checkout from the Run-02 template;
2. create a real Git worktree;
3. put a `.csproj` with a forbidden inline PackageReference Version in the worktree;
4. direct `check-manifests.cjs` in the worktree correctly fails;
5. invoke the exact Run-02 PostToolUse command with `CLAUDE_PROJECT_DIR` pointing at the main checkout and hook input `cwd`/`file_path` pointing at the worktree;
6. hook exits 0 with no output.

The violation is silently skipped because the worktree file is outside the dispatcher's main-checkout ROOT.

Repair requirements:

- separate **launcher/config root** from **active repository/worktree root**;
- use the launcher root only to locate the hook implementation;
- resolve the active inspection root from hook input `cwd`, then safely normalize to the containing active repository/worktree when needed;
- all manifest, architecture, co-change, state, and relative-path operations must use the active root;
- prove the behavior with a real Git worktree and a nested directory inside it.

Current Claude Code explicitly documents that `${CLAUDE_PROJECT_DIR}` stays at the original project root while hook-input `cwd` follows Claude into worktrees and after `cd`.

## D2 — HIGH — Critical PreToolUse enforcement can fail open [MANDATORY]

The dependency/Reserved-change PreToolUse handler has no `onFailure: "block"`.

A missing script, dispatcher exception, malformed input, or timeout therefore can allow the guarded command to proceed on current Claude Code.

Repair requirements:

- make policy-critical PreToolUse command hooks fail closed;
- use current documented `onFailure: "block"` or an equally strong supported mechanism;
- add negative tests for missing/invalid hook target, malformed input, thrown checker error, and timeout/failure behavior where practical;
- do not make advisory Stop behavior fail closed if doing so would create loops.

## D3 — HIGH — UTF-8 BOM-prefixed hook JSON fails in Run-02 [MANDATORY]

Independent reproduction against the exact configured Run-02 PreToolUse command:

- ordinary JSON input: works;
- the same UTF-8 JSON prefixed with BOM: exit 1, `Unexpected token U+FEFF`.

The bug is in `dispatch.cjs`: it tests `raw.trim()` but passes the original `raw` to `JSON.parse`.

Run-01 tolerates the same BOM input.

Repair the parser and add BOM + CRLF + empty-input tests.

## D4 — HIGH — Dependency command classification is incomplete [MANDATORY]

The runtime policy says additions, updates, **and removals** route through `add-dependency`.

Confirmed Run-02 gaps include:

- `npm uninstall x` -> missed;
- `npm remove x` -> missed;
- global-option forms without force flags are missed:
  - `npm --prefix frontend install x`;
  - `npm --workspace app install x`;
  - `pnpm --dir frontend add x`;
  - `yarn --cwd frontend add x`;
- `dotnet remove Foo.csproj package X` -> missed.

Force/legacy-peer flags happen to be caught even in some global-option forms because the current code scans all tokens for those flags, but that does not fix ordinary package routing.

Repair with a compact token-aware/table-driven classifier:

- support package-manager global options, including options consuming the next token;
- cover additions, updates, and removals required by the runtime policy;
- keep unrelated commands passing;
- preserve exact-version enforcement for additions/updates;
- test command chains and both Bash/PowerShell tool inputs.

Do not replace this with one broad regex that creates obvious false positives.

## D5 — HIGH — Project-reference graph mutations bypass pre-execution Reserved-decision control [MANDATORY]

The always-loaded operating policy classifies changing the project reference graph as Reserved.

Confirmed Run-02 behavior:

- `dotnet add Foo.Api.csproj reference Foo.Domain.csproj` -> no PreToolUse problem;
- `dotnet remove Foo.Api.csproj reference Foo.Domain.csproj` -> no PreToolUse problem.

These mutations must be routed/blocked before execution unless the required decision approval is already satisfied by the workflow/context.

After execution, deterministic architecture/project-reference validation must still run.

Add tests for both common dotnet reference syntaxes and add/remove variants.

## D6 — HIGH — Bash/PowerShell-driven manifest changes bypass PostToolUse validation [MANDATORY]

Run-02 PostToolUse matches only:

`Edit|Write|MultiEdit`

Claude Code does not fire an Edit/Write PostToolUse hook when Bash/PowerShell rewrites a file. Shell commands can change `.csproj`, `Directory.Packages.props`, `package.json`, project references, and instruction files.

Repair requirements:

- provide deterministic post-change coverage for relevant Bash and PowerShell mutations;
- run manifest/reference/instruction checks when relevant files actually changed;
- avoid an expensive whole-repository scan after unrelated shell commands;
- preserve clear owner/workflow pointers rather than duplicating policy in hook messages.

## D7 — HIGH — The structure checker freezes the old hook serialization and does not verify corrected hook safety [MANDATORY]

`check-instructions.cjs` currently requires a shell-form command matching roughly `node ...` and extracts the dispatcher/event by parsing the command string.

That design conflicts with the current Claude Code exec form, where `command: "node"` and `args: [...]` avoid shell tokenization and safely carry `${CLAUDE_PROJECT_DIR}` as a path argument.

The checker also does not require:

- `onFailure: "block"` for the critical PreToolUse policy hook;
- active-root/worktree semantics;
- required Bash/PowerShell post-change coverage.

Repair settings and checker atomically. The checker must validate the corrected behavior/configuration, not the baseline's serialization.

## D8 — MEDIUM — Manual checker commands are current-directory relative [MANDATORY]

Runtime workflows repeatedly instruct Claude to run commands such as:

- `node .claude/scripts/check-instructions.cjs`;
- `node .claude/scripts/check-manifests.cjs`;
- `node .claude/scripts/check-cochange.cjs`.

Those fail after an ordinary `cd` into a nested project directory unless the workflow first returns to the repository root.

Use one consistent cross-platform root-aware invocation strategy. It may establish the active repository/worktree root before running the command or use another equally reliable mechanism.

Do not introduce POSIX-only shell syntax.

## D9 — MEDIUM — Stop deduplication ignores materially changed same-path content [MANDATORY]

Run-02 fingerprints only changed **paths** plus reminder IDs.

Independent reproduction:

1. modify `backend/X.Api/A.cs` without changing tests -> reminder emitted;
2. modify the same file again to different content, with the same path set -> hook-mode `check-cochange` returns no reminder.

The second change is incorrectly treated as the same state.

Repair the fingerprint so materially changed working-tree state receives a new bounded reminder while:

- `stop_hook_active` still prevents loops;
- unchanged state is not repeatedly reported;
- state remains bounded;
- worktrees use their own active Git state.

A diff/content identity, index/worktree identity, or another deterministic change-set fingerprint is acceptable.

## D10 — HIGH — Capability `Binds:` conformance is not actually enforced [MANDATORY]

K1 requires unavoidable cross-slot bindings to be declared on the dependent slot.

The selected Run-02 manifests correctly state:

- persistence/ef-core -> architecture;
- backend-testing/nunit -> architecture.

But the checker only verifies that a non-empty `Binds:` value names *some* other known slot. It does not enforce the required binding declared by the slot contract/current implementation.

Independent mutation:

- replace persistence/ef-core `Binds: architecture ...` with `Binds: —`;
- `check-instructions.cjs` still reports `0 error(s), 0 warning(s)`.

Repair requirements:

- mechanically validate contract/manifest binding obligations;
- support the current required leaf->frame bindings;
- fail when a required binding disappears or points to the wrong slot;
- keep `Binds: —` legal for a module that genuinely has no cross-slot binding;
- add negative mutation tests for persistence and backend-testing plus positive tests for unbound modules.

Do not hardcode an accidental implementation detail if the contract can express the requirement cleanly.

## D11 — HIGH — K dependency checking does not cover the complete declared K graph [MANDATORY]

Run-02 is substantially better than Run-01: it validates Markdown conformance edges among OP/DEC/STD/KNW/WF and correctly rejects a DEC -> STD dependency.

However, Candidate K1 also declares:

`ENF -> STD / DEC`

The current `RANK` excludes ENF, and `checkReferences` only derives conformance edges from Markdown artifacts. Therefore the checker cannot prove the ENF part of the candidate's dependency graph.

Repair requirements:

- preserve the working ranked check for `WF -> KNW -> STD -> DEC -> OP`;
- add a small deterministic way to validate the authoritative/policy dependencies of ENF facets against STD/DEC;
- distinguish legitimate routing/message pointers from conformance dependencies;
- add mutation tests showing an ENF conformance dependency on KNW/WF is rejected while ENF -> STD/DEC is accepted;
- do not create a large new metadata layer merely to satisfy the checker.

The goal is to validate K1's real structural predicate, not to parse arbitrary JavaScript imports as policy dependencies.

## D12 — REVIEW — Full source-based V2/policy fidelity review [MANDATORY REVIEW]

Independent lexical diagnostics slightly favor Run-02, and both reports claim complete 194+2 preservation. This is reassuring but not proof.

Perform a fresh audit against:

- `source/inventory.json`;
- `source/shared-research-invariants.json`;
- `source/v2-baseline/`.

Requirements:

- verify all 194 policies and both invariants have exactly one authoritative owner;
- preserve trigger class and minimum scope exactly;
- inspect semantic strength/conditions, not just keywords;
- restore useful V2 technique/examples if genuinely missing;
- do not restore duplicate normative ownership merely to increase lexical similarity.

## D13 — REVIEW — Preserve K1 capability value without unnecessary complexity [QUALITY REVIEW]

Run-02's generated always-loaded estimate is ~4,849 tokens, already inside the ~5k target, and its runtime corpus is smaller than Run-01's.

After mandatory fixes:

- preserve the single decision register;
- preserve exactly four slots and static composition;
- preserve role-named facets and implementation leak protection;
- preserve optional frontend removal;
- preserve the neutral-standard + implementation-facet split;
- keep non-slot content K-style rather than broadly neutralizing it;
- avoid new files/meta-layers unless they solve a demonstrated reliability or ownership problem.

No complexity reduction may weaken policy availability, routing reliability, conformance checking, or replaceability.

## Required final invariants

The promoted output must have:

- 194 inventory policies + 2 shared invariants preserved;
- trigger-role deltas = 0;
- minimum-scope misses = 0;
- unresolved broken references = 0;
- exactly seven Kinds and the K dependency model;
- exactly four capability slots;
- one selected implementation per required slot and zero/one optional frontend;
- architecture remains the frame;
- current leaf bindings declared and checked;
- no extra slots or dynamic plugin discovery;
- no stability-Level hierarchy;
- scope-first STD organization;
- one always-loaded decision register;
- external workflows use facet/role vocabulary instead of selected implementation names;
- optional frontend clearing remains valid;
- deterministic checker negative tests cover Kind direction, capability leak, Binds, hook configuration, and slot cardinality;
- Windows/Bash/PowerShell/nested-cwd/worktree behavioral tests pass;
- all JavaScript parses;
- always-loaded size remains justified and preferably near/below the baseline.
