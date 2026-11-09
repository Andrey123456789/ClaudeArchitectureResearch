# L1-Restart / phase 5.3 — `iteration_after_audit_3`

## Objective and authorized baseline

This is a **minimal, evidence-driven lexical parity correction**, not a new architectural revision or another natural-language analysis project.

Work in the existing `L1-Restart` workspace and **continue from the current `output/template/` produced by `iteration_after_audit_2`**. That template has 86 files. Never regenerate from `baseline/template/`, backport code from historical iterations, or change a different candidate. The P4 design decision has already been made: Level 0 (Core) and Level 1 (Architecture) cannot name concrete implementation technologies, including nominally non-normative `Technique: <name>` references. Only the specifically documented fixed-platform vocabulary is allowed. Concrete technologies remain permitted at the appropriate Level 2 and Level 3 locations.

The independent audit identified two concrete omissions in the implementation vocabulary:

| Concrete name | Candidate L0, Level 0/1 | Current L1, Level 0/1 | Required L1 result |
|---|---|---|---|
| `Jest` | FAIL | PASS | FAIL |
| `Scrutor` | FAIL | PASS | FAIL |

Both omissions were reproduced at **both** Core and Architecture levels. They share a single cause: the current `TECHNOLOGY_LEXICON` in `.claude/scripts/check-instructions.mjs` lacks those names; the generic API-shape detector does not reliably catch them. This is NOT a failure of the current Markdown block parser or a request to expand the parser.

### Verify starting state before modification

Read the relevant sections of the current `output/REFINEMENT_REPORT.md`, current checker, existing Level-0 and Level-1 rules, and the original research requirements sufficient to establish the scope. Record the template's file inventory once. Verify these independent identifiers before editing:

- `output/template/`: **86 files**.
- SHA-256 of `output/template/.claude/scripts/check-instructions.mjs` at the start: `d315eaba57aad4a4423b780a932572f103f7acb16d77b1b608e889c521660afc`.
- The current report records the prior template tree hash `546fd8dda79391be9f1294a14ab86add5ce4c8605b314b7f79ccb576af3a1b25` using its documented hash method. Follow the *same* method when comparing tree hashes; do not substitute a different serialization or claim a mismatch based on a different method.

If the checker hash differs, stop as `BLOCKED: baseline mismatch` and report the observed hash. Do not silently overwrite newer work.

## 1. Exact change and restrictions

The expected code change is adding **only the missing, case-insensitively matched technology names** `Jest` and `Scrutor` to the existing `TECHNOLOGY_LEXICON` in:

`output/template/.claude/scripts/check-instructions.mjs`

Preserve the current matcher and existing checks for Core/Architecture neutrality, technology tokens in frontmatter and Markdown, API-shaped identifiers, capability/facet ownership, module leakage, frame-term no-legalizing, reference validity, graph direction, and four capability slots. Do not widen any platform exception. Do not return to pure-pointer exemptions. Do not copy or merge the entire L0 vocabulary: the audit has proved these **two** mismatches; an uncontrolled merge would introduce a new design change. If existing template content becomes invalid, diagnose it and report `BLOCKED` rather than editing unrelated policy files.

**The ONLY permitted persistent changes are:**

1. `output/template/.claude/scripts/check-instructions.mjs`.
2. The existing `output/REFINEMENT_REPORT.md` (append the evidence and decision for this pass; do not replace earlier sections).

The other **85 template files must remain byte-for-byte unchanged**, and `baseline/`, `source/`, `audit/`, `CANDIDATE.md`, original root tasks, root manifests, all skills, rules, hooks, capability files, and enforcement scripts must not change. Temporary test data may exist only inside `output/.work/`; remove it after reporting. Do not leave behind a permanent test harness or supporting code.

## 2. Finite behavioral acceptance matrix

Run all fixtures against the **actual candidate checker** in independently restored isolated copies of the template. Inject into a real Level-0 rule and an eligible Level-1 architecture/frame rule without damaging headers, file paths, manifests, skills or references. Never mutate the authoritative `output/template/` for testing. Record verdict, exit code, target filename and relevant diagnostic per case.

### A. Required negative checks on BOTH levels

Each named technology must be rejected in each of these relevant bounded, already-supported Markdown shapes:

| Fixture pattern | For `Jest` | For `Scrutor` |
|---|---|---|
| Direct prescription | `Must use Jest.` | `Must use Scrutor.` |
| Pure pointer (still forbidden by P4) | ``Technique: `jest`.`` | ``Technique: `scrutor`.`` |
| Heading | `## Selected technology: Jest` | `## Selected technology: Scrutor` |
| Bullet item | `- Use Jest.` | `- Use Scrutor.` |
| Nested list | `- Selected test technique:` followed by `  - Jest` | `- Selected registration technique:` followed by `  - Scrutor` |
| Table cell | `| Tool | Jest |` | `| Tool | Scrutor |` |
| Frontmatter text or relevant rule metadata | Named technology in an appropriate nonstructural frontmatter string | Same |
| Capitalization variants | `JEST`, `jest` | `SCRUTOR`, `scrutor` |
| Wrapped paragraph / code span | `Select` newline `` `Jest`.`` | `Select` newline `` `Scrutor`.`` |

For each expected FAIL, demand a **nonzero result with a technology-neutrality diagnostic naming the relevant technology on the injected rule**. A failed setup, unknown-skill, broken reference, malformed Markdown or other incidental error **alone** is NOT a passing negative test. If a pointer fixture also generates an unknown-skill co-diagnostic, the scenario counts only if the relevant neutrality diagnostic is present; record the co-diagnostic without broadening the checker. If a frontmatter fixture must retain a specific required header shape, alter only a suitable metadata text value, not required keys or values.

Include a small pair of format-preservation controls (`**Jest**`, `` `Scrutor` ``, or `### Technique: Jest`) to verify the existing normalization pipeline still applies, without triggering an open-ended formatting campaign.

### B. Positive checks / no false blocking

- A clean `Technique:` reference **at its allowed Level-2 location** is accepted by the neutrality logic. Do not force creation of nonexistent skills; place permitted technology names in existing Level-2 guidance/test copies in a way that preserves structural checks.
- Valid Level-3 project-specific technology choices remain permitted in the current project-decision surface.
- Level 0/1 text that names **no** concrete technology still passes: `Use the selected Level-2 test technique.`, `Follow the appropriate dependency-injection guidance.`, `Must run unit tests.`
- Existing documented fixed-platform names remain permitted where already allowed (`.NET`, `C#`, `TypeScript`, `Git`, `HTTP`). Names such as `ASP.NET Core` and `NuGet` must **remain prohibited** at Level 0/1.
- Avoid unintended substring matches: `jestful` or `scrutinize` must not be classified as the separate product names `Jest` and `Scrutor` (test on existing neutral rule content without introducing unrelated failures).
- Keep `Docker`, `Swagger`, `NUnit`, `EF Core`, `ASP.NET Core` and `NuGet` forbidden at Level 0/1. Their existing negatives must not regress.
- The unmodified current output template must pass with zero checker errors and warnings.

Use a small, frozen fixture matrix recorded before edits; run it once against the unmodified checker to reproduce the real Jest/Scrutor false PASS while confirming negative/positive controls, then on the corrected checker and in the final confirmation. Do not rebuild the deleted earlier 147-case suite, and do not inflate evidence counts by counting setup errors as intended failures.

## 3. Preservation gates

Verify these items without re-running expensive unrelated integration tests:

- `node --check` on changed checker; syntax checks of all template JavaScript checker/hook modules where low-cost.
- Actual `node .claude/scripts/check-instructions.mjs` on the clean template: expected `PASS`, **68 artifacts, 0 violations, 0 warnings**.
- `check-architecture.mjs` may report `NOT APPLICABLE` on the empty template; do not represent that as a functional .NET build or integration pass.
- Existing capability constraints: four static slots (architecture required frame, persistence required leaf, backend-testing required leaf, frontend optional leaf), valid selected implementations and required `binds:`; no fifth slot. These are unchanged; one focused mechanical smoke test is sufficient.
- All 85 other template files are byte-identical, including existing hooks, D3–D15 behavior implementation, normative policy text, capability modules and decisions. Root `MANIFEST.sha256` inputs unchanged. Since the code change is limited to detection vocabulary, existing policy owners/strength/trigger/minimum scopes have not been edited.
- No regressions to D1–D17, P4/P6, the 194 inventory policies + GOV-017/GOV-018, Level 0→1→2→3 direction, and known acceptable template state. The policy evidence here is **byte identity plus previously accepted evidence**; do not claim a newly executed full 196-record semantic audit unless you actually perform it.
- English-only permanent content; no temporary test content or `output/.work/` remains. Final `output/` has exactly `template/` and `REFINEMENT_REPORT.md`.

## 4. Budget, protocol and stopping

1. Record baseline hashes/inventory once and read the local contracts.
2. Implement a single small real-checker fixture harness in `output/.work/`, with frozen expected outcomes and no self-modifying oracles. Reproduce the two misses on the untouched checker.
3. Add the two terms to the lexicon and run the finite acceptance matrix, syntax, clean checker and affected regressions.
4. Perform **one** cumulative confirmation of all gates. If and only if an actual directly related defect remains, make one targeted correction, rerun affected fixtures, and one reconfirmation. Otherwise stop.
5. Append `Corrective pass — iteration_after_audit_3` to `output/REFINEMENT_REPORT.md`. State: observed initial misses, root cause, precise changed files, fixture counts and diagnostics by level and case, clean-template checker, unchanged-file proof, prior and final hashes using the same method, policy-preservation inference, evidence inherited vs newly run, known limits, and truthful final status.
6. Remove `output/.work/` after collecting evidence. Verify output shape and **STOP**; no further exploratory tests, transcript rereading, repeated hashes, or circular Stop-hook evidence discussions.

A green finite pass may be reported as `READY_TO_FREEZE (pending independent verification)`; a failed or unverified gate must be reported as `BLOCKED` with the exact relevant evidence. Neither case authorizes a new task cycle. If an external Stop hook refuses to let the session terminate after a completed report, do not resume checks or alter the hook: state the final status once and cease work.

**Definition of done:** Jest and Scrutor cannot be used to prescribe—or merely name—a concrete technology at Core/Architecture, while the earlier conservative P4 policy and every otherwise unchanged property remain intact. This is a lexical parity patch, not a candidate redesign.
