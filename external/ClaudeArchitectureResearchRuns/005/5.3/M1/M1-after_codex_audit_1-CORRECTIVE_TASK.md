# M1 / Experiment 005 / Phase 5.3 — after_codex_audit_1

## 1. Purpose and evidence

Two independent, same-input Codex freeze-readiness audits identified the **same single confirmed blocker**, A-001 / `ARC-025`, in M1. The other five candidates were assessed as ready with documented limitations. This task is a **targeted M1 correction**, not another full audit, parity alignment, or architecture redesign.

The authoritative policy is in `source/inventory.json`, `policygroups[id="architecture"].policies[id="ARC-025"].normalized_policy`:

> Infrastructure translates remote HTTP responses into Application-facing abstractions; do not leak HttpResponseMessage or remote transport concerns into Application.

`ARC-025` is `MUST`, backend-scoped, and path-triggered. M1's current owner is `output/template/.claude/rules/architecture.md`, in `## Layer Placement`. Its added exception permits a transport concern to cross into Application when Application explicitly models HTTP. That exception conflicts with the common normalized requirement; historical V2 wording, local examples, and checker PASS statuses cannot override it.

No other confirmed phase-5.3 blocker is in scope. Differences in analyzer configuration, Polly exceptions, test-host lifetime, migration wording, and other parity-only questions belong to **phase 5.4** and MUST NOT be changed here.

## 2. Working directory and read boundary

Execute with the working directory at the existing M1 candidate root, e.g.:

`C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.3\M1`

Read, in this order:

1. This corrective task and `M1-after_codex_audit_1-GOAL_PROMPT.txt`.
2. `source/inventory.json` — the exact `ARC-025` entry and its strength, scope and trigger class.
3. `CANDIDATE.md` — preservation of M1's Minimal Modular + four replaceable capability slots.
4. The current `output/template/.claude/rules/architecture.md`.
5. The relevant `output/template/.claude/skills/httpclient-factory/SKILL.md` architectural boundary (read-only corroboration, NOT an edit target).
6. The end of the current `output/REFINEMENT_REPORT.md`, to append without rewriting its history.

Original `REFINEMENT_TASK.md` and historical prompts are reference-only if consulted. In particular, their instruction to initialize `output/template/` from `baseline/template/` belongs to the original 5.3 refinement and **does not apply** to this correction. Do not open sibling candidate folders, external audit-output folders, or unrelated files for additional cleanup.

## 3. Immutable boundaries and exact permitted edits

### Allowed

- **ONE** existing runtime file:
  `output/template/.claude/rules/architecture.md` — only the exact replacement specified in §4.
- **ONE** existing report:
  `output/REFINEMENT_REPORT.md` — append one concise, clearly titled evidence section, preserving all prior report bytes as an unmodified prefix.

### Forbidden

Do not change, delete, rename or create **any other permanent file**, including:

- `baseline/`, `source/`, `audit/`, `CANDIDATE.md`, `REFINEMENT_TASK.md`, `GOAL_PROMPT.txt`, `README.md`, `PROVENANCE.json`, `MANIFEST.sha256`, all prior prompts or iteration records;
- any of the other 79 files beneath `output/template/`, including `CLAUDE.md`, `.claude/MAP.md`, capability selections/contracts/manifests, other `.claude/rules/`, `.claude/skills/`, `.claude/hooks/`, `.claude/scripts/`, `.claude/settings.json`, `docs/`, `.editorconfig`, and `.props` files;
- any layer/scope/trigger metadata, policy owner, architecture decision model, four-slot selection, `binds`, hook behavior, checker implementation, analyzer levels, dependency/version rules, or test patterns.

Do not add a second ARC-025 rule, a redundant policy document, tests committed as runtime assets, temporary dependencies, or a new iteration directory. This is a single-paragraph normative correction.

Use no temporary files unless strictly necessary. If a transient harness is required, place it only under `output/.work/` and remove it before final reporting. Never modify working-tree fixtures outside M1.

## 4. EXACT authorized replacement

Target file: `output/template/.claude/rules/architecture.md`.

**Replace this exact block, once:**

```markdown
- Infrastructure translates remote HTTP responses into Application-facing
  abstractions; do not leak `HttpResponseMessage` or remote transport concerns
  into Application contracts unless the Application explicitly models HTTP.
```

**With this exact block:**

```markdown
- Infrastructure translates remote HTTP responses into Application-facing
  abstractions; do not leak `HttpResponseMessage` or remote transport concerns
  into Application.
```

Retain the original LF line endings, BOM status, trailing newline, whitespace elsewhere, and all other bytes. Do not rewrite neighboring bullets or headings. The corrected text must prohibit transport leakage into **Application itself**, not merely into *Application contracts*, and must contain no "Application explicitly models HTTP" exception.

### Source-state guard (mandatory before modifying)

The submitted M1 archive has:

- exactly **80** regular files in `output/template/`;
- `output/template/.claude/rules/architecture.md` original SHA-256:
  `47befd19b838669482734d5bc68ba365383c78b88f42e7953452237380b65e3e`;
- exactly **one** occurrence of the old three-line block and zero occurrences of the corrected three-line block.

Before making any change, snapshot the sorted relative paths and SHA-256 of **all 80** current template files. Confirm the exact original target SHA and unique old-block occurrence. If **any** stated precondition fails, make no edits and report `BLOCKED: INPUT_STATE_MISMATCH` with actual data. Do not try alternative wording, adjust the goalposts, or repair neighboring issues.

## 5. Finite validation plan

Complete exactly the following finite checks; do not turn them into a broad re-audit:

**V1 — Canonical policy.** Independently read the actual `ARC-025` normalized policy from the JSON and show that the replacement expresses its full unconditional boundary. Confirm original `normative_strength`, `trigger_class`, `scope` are unchanged.

**V2 — Replacement identity.** Starting from the captured original target bytes, construct the expected final bytes by a **single literal block replacement** from §4. Compare the actual final file byte-for-byte to those expected bytes. A correct final target should have SHA-256:

`c2040cf8f51e6ec0a00f8b23aabea3fc9fe891557636a1143029bd2992b4537c`

If SHA does not match, mark the result BLOCKED; do not accept merely semantically equivalent prose.

**V3 — No collateral changes.** Confirm the 80-file path set is unchanged and the SHA-256 of each of the other **79** runtime files is identical to the pre-change snapshot. Do not use file modification times as proof. Confirm forbidden root/source/baseline/audit/provenance/iteration material was not touched by this task.

**V4 — Static semantic regression.** Assert all these conditions:

- canonical unqualified prohibition is present once in the target rule;
- the disallowed exception phrase is absent from the target rule;
- there is no narrowed "only Application contracts" wording in that ARC-025 bullet;
- the existing `## Layer Placement` heading and path-loaded `architecture.md` owner/front matter are unchanged;
- the `httpclient-factory` skill and all four capability slots are byte-identical (covered by V3).

**V5 — Existing checkers (smoke tests, not new enforcement).** From `output/template/` execute, without edits:

```powershell
node .claude/scripts/check-instructions.js
node .claude/scripts/check-architecture.js
node .claude/scripts/check-manifests.js
```

Record exit codes and findings, including any warnings. These checkers may not validate the semantic ARC-025 wording: V1–V4 are the deciding gates. If a checker reports a pre-existing issue unrelated to this one-paragraph edit, record it exactly and STOP as BLOCKED or with an explicit limitation as warranted; **do not fix checkers or any other file**. Do not claim a passing checker alone proves the semantic repair.

**V6 — Hygiene.** `output/` contains only `template/` and `REFINEMENT_REPORT.md`; no `output/.work/` remains and no committed/runtime fixture was added.

Do not run live Claude host sessions, generate applications, reinstall packages, repair `MANIFEST.sha256`, implement 5.4 parity changes, run a second root-cause discovery loop, or expand test matrices. One execution of the fixed smoke suite is sufficient; one targeted diagnostic rerun is allowed only if the first run has a transient execution/setup problem.

## 6. Append-only research evidence

Only after V1–V5, append one new section to `output/REFINEMENT_REPORT.md`, titled:

`## after_codex_audit_1 — ARC-025 boundary correction`

Keep every pre-existing line/byte of the report as its unmodified prefix. Include briefly:

- the independent audit finding and why the conditional exception violates the normalized common policy;
- exact filename and the one-block before/after change (or a compact summary of it);
- target SHA-256 before and after;
- 80/80 path preservation and **79/79** unchanged other runtime-file hashes;
- V1–V6 results; checker exit statuses and any unrelated pre-existing observations;
- the preserved M1 identity (flat M-style rules, four static capability slots, frame/leaf ownership and binds, triggers, hooks, skill ownership);
- documented scope limit: this fixes the shared-policy blocker; it is **not** a new audit of all 196 policies, an exhaustive runtime proof, a phase-5.4 alignment, or an unconditional certification.

Do not revise or reinterpret older report sections. If any mandatory gate fails, record it if doing so would not violate preflight immutability and conclude `BLOCKED` with precise evidence; never assert PASS against a failed gate.

## 7. Stop conditions and final response

Successful outcome: `ARC-025_CORRECTED_WITH_DOCUMENTED_LIMITATIONS`, contingent on V1–V6 and the exact target SHA. The only changed project artifacts are the target architecture rule and the append-only refinement report; two newly supplied task prompt files are user-provided inputs, not generated runtime changes.

Report a short final summary with the target before/after SHA, the 80/79 identity results, checker statuses, and any open limitations. Do **not** claim all undiscovered 5.3 issues are impossible or automatically declare a six-candidate freeze without external acceptance. STOP when the report is written and the finite validation is complete.
