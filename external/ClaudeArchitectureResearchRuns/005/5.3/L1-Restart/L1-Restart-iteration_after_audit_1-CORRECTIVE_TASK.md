# L1-Restart — `iteration_after_audit_1` corrective task (phase 5.3)

## 0. Mission, authority, and hard boundaries

Make **one bounded corrective pass** on the **current, completed L1-Restart iteration-2** result. Repair the independently reproduced strict-P4 false negative: an explicitly selected concrete implementation remains accepted when a pure `Technique:` pointer is immediately followed by a same-block sentence that assigns the referred technology without repeating its name.

Use this task for execution and acceptance. Read the following existing files before editing:

1. `L1-Restart-REFINEMENT_TASK.md` — frozen strict P4/P6 contract, D1–D17, candidate identity, and stop protocol; especially Section 3.
2. `output/REFINEMENT_REPORT.md` — existing iteration-1 and iteration-2 evidence and known limits.
3. `CANDIDATE.md`, `audit/DEFECT_DOSSIER.md`, and the relevant immutable inventory/invariants.
4. `output/template/.claude/scripts/check-instructions.mjs` — particularly `parseBlocks`, `sentencesOf`, `pointerForm`, `techniquePointerViolations`, `REFERENTIAL`, and `neutralityCheck`.
5. Existing genuine Level-0/1 routing pointers in the final template (including `development-workflow`, `code-review`, and `build-fix`) and the specific original rule placements to be used for fixtures.

**Do not** copy or reset from `baseline/template/`, historical L1 iterations, other candidates, previous ChatGPT audits, or other workspaces. Continue from the current `output/template/` (86 files). The current pre-edit tree hash, using the exact command in Section 6 below, is:

`cbabd288390b3d9b7eaf3d6264b460b21465ceeb1f5f46005c606d8f4ddd486b`

Check the starting hash and capture the complete per-file inventory **once**. If it differs, stop and describe the mismatch; do not overwrite the current result. The root `baseline/`, `source/`, `audit/`, candidate/task metadata, and earlier iteration files are immutable.

**Permitted persistent edits:**

- `output/template/.claude/scripts/check-instructions.mjs` — only the bounded pure-pointer eligibility / anaphoric binding check and immediately necessary internal helpers/comments.
- The **existing** `output/REFINEMENT_REPORT.md` — append an accurate `Corrective pass — iteration_after_audit_1` section.

Do not change any of the other **85 template files**, add permanent files, change any hooks/settings/architecture/facets/skills/policies, or alter the approved platform vocabulary, skill catalog, capability selections, `binds:`, or D1–D17 semantics. Test material must live inside temporary `output/.work/` and be removed **last**.

## 1. Confirmed defect and reason it violates the already frozen contract

The current checker grants a masking exemption for the `docker` token in a valid-looking pointer sentence. It detects explicit phrases such as `Must use this technique`, but the existing `REFERENTIAL`/binding recognition does **not** link the same paragraph's *unambiguous demonstrative selection assertion* to that pointer.

Run the **real** current checker on independently reset copies of these two actual eligible files:

- `.claude/rules/0-core/engineering.md` (Level 0);
- `.claude/rules/1-architecture/frame/boundaries.md` (Level 1).

Place every fixture in its own **explicitly neutral** section or equivalent self-contained context; do not accidentally place positive controls under the existing generic `Engineering Discipline` list or normative governor.

### Mandatory initial reproduction

| Fixture text | Expected | Current known behavior |
|---|---|---|
| `### Deployment technique` + `Technique: \`docker\`.` | PASS | PASS |
| `### Deployment technique` + `Technique: \`docker\`. This is the selected deployment technology.` | **FAIL** | **incorrect PASS** |
| `### Deployment technique` + `Technique: \`docker\`. That is the chosen deployment technology.` | **FAIL** | **incorrect PASS** |
| `### Deployment technique` + `Technique: \`docker\`. Must use this technique.` | FAIL | FAIL |
| `### Deployment technique` + `Technique: \`docker\`. Must run unit tests.` | PASS | PASS |

A required FAIL is valid only if the real checker returns a **concrete-technology neutrality diagnostic naming Docker** in the injected eligible Level-0/1 artifact — not an unrelated corrupt file, missing skill or setup failure. A PASS requires zero violations and zero warnings.

The defect is in scope **without introducing a new Markdown syntax**: these are two sentences in one already supported paragraph (or a supported line-wrapped paragraph). Strict P4 was agreed before this iteration: a technology may be masked only if the *complete bounded statement and its direct governing context* are positively established as a pure, non-normative Level-2+ reference. P6 does not grant immunity when adding a sentence changes a pure pointer into a concrete technology choice.

## 2. Repair the invariant, not a single wording

Retain the existing bounded Markdown parser, six structural forms, resolved-skill target requirement, sentence segmentation, headings/ancestor handling, siblings, positive pointer grammar, and direct-vs-indirect technology checks. Work in the central masking decision: whether a candidate pointer is **actually pure after examining an immediately connected normative assertion**.

Required behavior:

1. Identify **explicit, immediate anaphoric selection/assignment** in the *same bounded block* referring to a uniquely identified technique pointer, including the reproduced `This is the selected deployment technology` and `That is the chosen deployment technology`. A lexical technology token need not appear in the following sentence.
2. Use one **bounded structural/grammatical predicate**, preferably leveraging the existing modality vocabulary, to connect a local demonstrative or definite-reference expression to a concrete selected/required/defaulted/preferred/assigned implementation. Do **not** merely append the exact phrases `This is the selected ...` and `That is the chosen ...` to a special-case string list.
3. Apply the existing fail-closed rule: if the direct context contains an explicit assertion assigning the referred technology or the local referent is ambiguous, do not mask the technology token; report the regular Level-0/1 technology-neutrality violation.
4. Keep **independent obligations** independent. `Technique: \`docker\`. Must run unit tests.` must stay PASS, as must neutral explanatory text that does not assign the technique. Merely seeing a modal word elsewhere must not indiscriminately poison every pointer.
5. Preserve immediate-sibling and parent/heading semantics already implemented: adding a neutral item must not legalize a forbidden choice; `Must use this technique` as an immediate related sibling must fail; an unrelated sibling `Must run unit tests` stays allowed in an explicitly neutral reference context.
6. Preserve genuine Level-2+ references (only when their meaning and governing context are purely referential), original `;`-separated independent clauses, and self-contained non-normative parenthesized asides. Do not silently broaden reference permissions, expand L0/L1 platform terms or downgrade any existing FAIL case.
7. Keep the **frozen grammar boundary**. No general-purpose natural-language parser, remote anaphora across sections, cross-document inference, new Markdown grammar, indefinite synonym fishing, or large vocabulary expansion. When a new assertion falls outside the positively recognized pure-reference contract, do not grant a speculative exemption.

**Engineering note:** A robust fix should test the *connected assertion and referent*, not just the presence of a keyword. If the checker cannot distinguish a new phrase within the frozen bounded grammar, report the precise scope boundary and the remaining unproven fixture; do not guess that every occurrence of `This` is normative.

## 3. Finite acceptance suite — freeze expectations before editing

Implement ONE reusable, table-driven finite harness inside `output/.work/`. Make isolated copies of `output/template/` for every test; never inject fixtures into the authoritative current template. Lock the test cases, expected verdicts, diagnostic requirements and harness checksum **before** changing the checker. First run a focused baseline proof on the unmodified candidate, then make the repair. Once the main suite is green, do not add more cases through an unbounded fuzzing campaign.

### N. Must FAIL with a technology-neutrality finding in both levels

Each negative must refer to a valid actual Level-2 skill, be placed under a non-normative eligible governor unless expressly testing a normative governor, and name the offending technology in the checker diagnostic.

N01. `Technique: \`docker\`. This is the selected deployment technology.`

N02. `Technique: \`docker\`. That is the chosen deployment technology.`

N03. `Technique: \`docker\`. It is the default deployment technology.` (immediate, unambiguous single antecedent)

N04. `Technique: \`docker\`. This must be used for deployment.` (immediate, unambiguous single antecedent)

N05. `Technique: \`swagger\`. This is the preferred API description technique.` (different technique, same invariant)

N06. `Technique: \`docker\`. This is the selected deployment technology.` with a physical line wrap between its sentences (same logical paragraph).

N07. A reference-only **heading** `### Deployment technique`, followed by the N01 paragraph (must not be legalized by the heading).

N08. A neutral parent-list/heading with `- Technique: \`docker\`.` and a directly related immediate sibling `- Must use this technique for deployment.`

N09. The N01 selection plus an unrelated neutral sibling before/after it (result still FAIL).

N10. Existing selection/requirement/default scenarios: `Selected deployment technology: Technique: \`docker\`.`, `### Selected deployment technology` + `Technique: \`docker\`.`, and `## Must use Swagger` (retain prior FAILs).

N11. An unambiguously referential sentence about **two** Level-2 techniques followed immediately by a statement that selects `this technology` without uniquely identifying which one: fail closed; do not choose an arbitrary antecedent.

The case variants must include at least one capitalization change; do not use capitalization-dependent loopholes. N11 is a strict-purity ambiguity control, not a request for generalized entity resolution.

### P. Must PASS (0 violations, 0 warnings) in both levels

P01. `### Deployment technique` + `Technique: \`docker\`.` (bare local pure reference).

P02. `### Deployment technique` + `See technique: \`docker\`.`.

P03. `### Deployment technique` + `Technique: \`swagger\`.`.

P04. `### Deployment technique` + `Technique: \`docker\`. Must run unit tests.` (independent duty).

P05. `### Deployment technique` + `Technique: \`docker\`. This section describes available deployment options.` (non-selecting description, no technology choice).

P06. `### Deployment technique` + `Technique: \`docker\`.` with one or two unrelated neutral sibling items in either order (valid P6 formatting/control).

P07. Properly labeled pure reference inside an accepted parent/nested list, including wrapping/continuation within the original six forms.

P08. Genuine pre-existing pointer patterns from the actual L1 template: `development-workflow` technique aside, `code-review` route map, and trailing `build-fix` technique footnote.

P09. Pure independent `;`-delimited reference clauses and permitted parenthesized aside, kept in their accepted contexts.

P10. Final **clean, unmodified instruction template** with all 68 artifacts: checker PASS, 0 violations, 0 warnings.

Do not reinterpret a forbidden/ambiguous reference under `Engineering Discipline` as PASS. The original strict P4/P6 contract in `L1-Restart-REFINEMENT_TASK.md` remains controlling.

### R. Preservation checks (small, representative, non-exhaustive)

- Run focused representatives of the originally frozen N01–N14 / P01–P12 / metamorphic families from the Restart specification, **without regenerating the deleted 302-case historical harness**.
- Ensure heading technology assertions, normative ancestor/sibling, case-insensitive API/technology leak, and `frame-terms` no-legalizing controls still fail appropriately.
- Verify `check-instructions.mjs` syntax and the other `.mjs` syntax; run the clean instruction checker and architecture checker (an architecture `NOT APPLICABLE` on an empty template is not a functional .NET integration pass).
- Verify four static capability slots (architecture required frame; persistence/backend-testing required leaves; frontend optional leaf), proper selected facets, enforcement hook registrations and `onFailure: "block"` without changing them. Existing `binds:` negatives must remain detectable, including removal from both contract and module; check a small controlled mutation rather than rerunning all historical suites.
- Confirm exactly 86 files in `output/template/`, **85 unchanged file hashes** and only the checker code changed. `MANIFEST.sha256` must still validate its 144 entries. The 194-policy inventory + GOV-017/GOV-018 is preserved by byte-identity of all normative/template owner files; reference the earlier report for its policy mapping, and **do not claim to have independently re-audited all 196 policy semantics** unless actually done.
- Preserve current context/always-loaded footprint (no new files) and English-only repository artifacts. Check output hygiene.

## 4. Bounded execution and stopping (mandatory)

1. Preflight: verify tree hash, source integrity and the clean template; identify the actual legitimate pointers; create ONE fixed finite harness. Prove the N01/N02 bypasses on the untouched checker, and make sure P01/P04 pass.
2. Implement **one focused repair** in `check-instructions.mjs`. Do not edit normative rules or touch runtime hooks.
3. Run the fixed suite and small preservation controls; fix any direct failure in the same bounded pass. If the required contract cannot be met within the authorized scope, return `BLOCKED` with exact cases and stop. Do not fabricate `STRICTLY_BETTER`.
4. Run **ONE final cumulative confirmation** using the **same frozen harness and oracle**. If a genuine code regression appears, at most one focused follow-up correction and one reconfirmation is permitted. Any problem with the test oracle must be resolved and documented **before** the final audit, not by silently editing expected results mid-audit.
5. Append one truthful `Corrective pass — iteration_after_audit_1` section to the existing `output/REFINEMENT_REPORT.md`: original reproduced flaw, root cause, exact change, fixed N/P/R results for both levels, regressions, previous-vs-new evidence, tree hash, unchanged-file proof, known boundaries, terminal status, and the absence of a live Desktop test if not performed.
6. Remove only temporary `output/.work/` **last**. Verify `output/` contains exactly `template/` and `REFINEMENT_REPORT.md`. Stop. A Stop-hook challenge or a previously resolved evidence question must not trigger fresh audit loops. `BLOCKED` and `NOT_PROMOTED` are legitimate final results if supported by evidence.

## 5. Explicit non-goals and success condition

- Do **not** restart from Run-02, reconstruct earlier iteration scripts, compare other candidates, try every hypothetical English paraphrase, fuzz randomly, change host settings/hooks, or adjust research policies.
- Do **not** hide technology names to make the checker pass, change expected PASS/FAIL labels after execution, or promote a tie as an improvement.
- **Promotion = `STRICTLY_BETTER` only if** the same-block anaphoric selection bypass is closed at both levels; legitimate reference pointers and unrelated obligations remain valid; all previously frozen P4/P6 semantic requirements that were in scope still hold; 85 files and all policies remain unchanged; and the final confirmation is clean.

## 6. Exact inventory/hash command

From **inside** `output/template/` under a Bash-compatible shell:

```bash
find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum -b | sha256sum
```

The pre-edit expected tree is `cbabd288390b3d9b7eaf3d6264b460b21465ceeb1f5f46005c606d8f4ddd486b`. Document this exact algorithm instead of substituting an OS-dependent file-list ordering. If using PowerShell for other tasks, preserve path and byte identities when comparing to this recorded hash.
