# L1 — Independent audit of corrective iteration 7

**Input:** `L1_7.zip` compared directly with `L1_6(1).zip`.

## Decision

**NOT READY TO FREEZE.** The iteration-7 repair closes the previously demonstrated *single-child* P4 bypass. However, the same normative technology assignment becomes acceptable again when a parent Markdown block contains an additional child. An even clearer bypass combines a neutral technique pointer with an adjacent explicitly mandatory sibling. Both are reproducible in real Level-0 and Level-1 frame rules. The zipped output also includes leftover `output/.work/` temporary audit data.

## Independently rerun confirmation

- The archived `output/.work/iter7-definitive.mjs` executed independently on the extracted archive and returned `CLEAN` with **372/372** fixtures; original iteration-6 bypass was reproduced on a hash-verified version-6 checker.
- The independent replay found policy audit **196/196**, 0 owner/trigger/scope regressions, 0 broken references, `check-instructions` **PASS** (67 artifacts, 0 violations, 0 warnings), all `.mjs` files syntactically valid, and always-loaded text **20,581** characters.
- `check-architecture` returned **NOT APPLICABLE (no backend directory)**. It does not establish successful compilation or runtime tests.
- Direct archive comparison: both versions contain exactly **86** template files; **85** are byte-identical. Only `.claude/scripts/check-instructions.mjs` changed. The `baseline/` (88 files), `source/` (43), and `audit/` (8) trees are byte-identical.
- Recomputed template tree SHA-256 values agree with the recorded reports: iteration 6 `6d3c3ab9f9bf2142aa6e9cb0b3008d9bdfe452d81f461ebb019393bc37b3fec2`; iteration 7 `fe57cf497ce7b3495df59ca1b9354534a272d6b92b15f4d541e428bb731b7fed`.
- `MANIFEST.sha256` entries verify. The submitted ZIP does contain `output/.work/` (including audit harness files), contradicting the clean-output assertion for the archived snapshot.

## BLOCKER P4-A — adding a sibling legalizes a normative parent

Inject into either `.claude/rules/0-core/engineering.md` or `.claude/rules/1-architecture/frame/boundaries.md`:

**Control, correctly FAIL:**

```markdown
### Selected deployment technology
- Technique: `docker`.
```

**Mutation, incorrectly PASS (0 violations):**

```markdown
### Selected deployment technology
- Technique: `docker`.
- additional context.
```

A nested-list form of the same flaw also incorrectly passes:

```markdown
- Selected deployment technology:
  - Technique: `docker`.
  - additional context.
```

The additional bullet has no bearing on whether the title selects a technology. This violates the supported-format invariance and P4 (routing syntax must not waive a concrete selection).

## BLOCKER P4-B — explicit mandatory sibling ignored

This also returns **PASS (0 violations)** independently at **both Level 0 and Level 1**:

```markdown
### Deployment technique
- Technique: `docker`.
- Must use this technique for all deployments.
```

Likewise for:

```markdown
- Deployment technique:
  - Technique: `docker`.
  - Must use this technique.
```

The norm is explicit (`Must use`) and anaphorically refers to the Docker skill, yet the checker masks the technology name in one sibling and examines the obligation in another sibling without rejoining their meanings.

**Positive control, correctly PASS:**

```markdown
### Deployment technique
- Technique: `docker`.
- additional context.
```

The failures are not accidental setup failures: the checker processes all 67 artifacts and reports 0 violations for the negative mutations.

## Root cause

In the iteration-7 checker, the `stripRoutingPointers` routine collects only the nearest governors whose **entire** governed block is `pointerContent`; if a governing section/list mixes pointer content and ordinary sibling content, the heading stops being treated as a pointer label. Its wording is then tested only with the finite `NORMATIVE` regex. `Selected` and `Chosen` are not in the regex, so a mixed-content normative heading can become invisible to the purity check. Sibling obligations such as `Must use this technique` are not incorporated into the referenced pointer's semantic context.

Relevant implementation: `.claude/scripts/check-instructions.mjs` — `pointerContent`, `routingClause`, and `stripRoutingPointers` in the routing-authorization block (around lines 221–335).

**This is an unresolved P4 defect from iteration 6, not a regression relative to it.** Iteration 6 accepted even the single-child selected-heading form. Iteration 7 rejects that form but still accepts the two-child one.

## Bounded next-step acceptance criteria

Do not add an endless list of prohibited words or reconstruct the full 372-case suite. The next correction must make exemption depend on **the actual governing block's binding semantics**, not on whether unrelated siblings happen to make the governor ineligible as a label. At minimum:

1. Both P4-A and P4-B negative examples FAIL with the correct technology-neutrality diagnostic **at both Level 0 and Level 1**.
2. Adding unrelated neutral sibling bullets cannot change a forbidden selection from FAIL into PASS.
3. Retain legitimate bare `Technique: docker`, neutral subject headings, and all three real template pointer shapes (development-workflow aside, code-review routing map, build-fix footnote).
4. Preserve the existing 372-fixture matrix, all 196 policy checks, byte identity of the other 85 template files, and 20,581 always-loaded chars.
5. Run one real final confirmation, remove `output/.work/`, and stop. The checker failure and the temporary-file cleanup are separate concerns.

A corrected hygiene-test oracle is not by itself a template defect. The independently reproduced P4 bypasses **are** template defects, and are the reason for withholding READY_TO_FREEZE.

## Note on the Stop hook

The archived template's `.claude/hooks/stop-cochange.mjs` explicitly checks `stop_hook_active` and deduplicates repeated material state. Its contents alone do not establish that *this particular hook* caused the repeated completion objections seen in the transcript; a task runner or separate validation process may have been involved. Avoid attributing the loop to this internal hook without execution-level evidence.
