# L1 — Independent Audit of Corrective Iteration 6

**Research phase:** 005 / 5.3  
**Candidate:** L1  
**Reviewed artifact:** `L1_6(1).zip`  
**Disposition:** **NOT READY TO FREEZE — one reproduced high-severity P4 bypass**.

## Recovered scope

Iteration 6 was intended to replace line-oriented, fixture-specific technology-neutrality routing repairs with one bounded logical-Markdown statement classifier. Its specification requires preservation of accepted D1/D3–D17 properties, 194 inventory policies + GOV-017/GOV-018, frame/leaf composition, four static capability slots, established hooks/worktree/encoding behavior, and one cumulative confirmation audit. The six supported Markdown structures include same-line, heading governance, nested bullet, list continuation, colon lead-in and paragraph continuation. Pure, non-normative references to Level-2 technique must remain accepted.

## Independently verified

- Instruction checker on the unmodified output template: `PASS (67 artifacts, 0 violations, 0 warnings)`.
- Architecture checker exits 0 but prints `NOT APPLICABLE (no backend directory)`; this is not evidence of a real C# solution build or runtime architecture conformance.
- All `.mjs` files pass `node --check`.
- Standalone output shape: `output/template/` and `output/REFINEMENT_REPORT.md`; no `output/.work/`.
- Template: **86 files**, **382,594 bytes**.
- Recalculated template checksum: `6d3c3ab9f9bf2142aa6e9cb0b3008d9bdfe452d81f461ebb019393bc37b3fec2`, exactly matching the report. Reproduce from `output/template`:
  `find . -type f -print0 | sort -z | xargs -0 sha256sum -b | sha256sum`
- Independently injected **119** cases into a temporary copy of a Level-0/Level-1 rule. All returned the expected verdict: documented transformations of Required/Default/Deployment-technique with Docker and a small Swagger subset, bare pointers, normative continuations, unrelated paragraphs, and direct technology leaks.
- Four additional independent negative mutations were correctly rejected: removal of critical `onFailure: "block"`, removal of `PostToolUseFailure`, addition of a fifth capability selection slot, and removal of the persistence-to-frame `binds:` declaration.
- The archived `REFINEMENT_REPORT.md` claims `363/363` regressions and `196/196` policies with zero owner/trigger/scope/reference issues. The 363-test harness was deleted per the agreed stopping rule and therefore was **not** independently rerun in this audit. Likewise, Windows live hook/worktree tests were not rerun.

## BLOCKER — P4: Routing syntax legalizes a concrete technology choice

Path: `.claude/scripts/check-instructions.mjs`, lines 233, 240–255, and 258–275.

In the temporary copy, the following statement was **correctly rejected**:

```markdown
Selected deployment technology: `docker`.
```

Merely adding the recognized routing label changed the checker to **PASS**:

```markdown
Selected deployment technology: Technique: `docker`.
```

The same semantic selection was also wrongly accepted when expressed through a supported heading-governs-content form:

```markdown
### Selected deployment technology
Technique: `docker`.
```

Further confirmed false negatives included:

```markdown
Chosen deployment technology: Technique: `docker`.
Deployment technology is: Technique: `docker`.
The deployment will run with: Technique: `docker`.
Technique: `docker`. This is the selected deployment technology.
```

**Root cause.** `routingClause()` excludes known normative words through a finite `NORMATIVE` regex, but `isTopic()` accepts **any** one-to-three-word prefix as a legitimate routing topic. When a normative expression lacks one of the enumerated words, the `docker` skill reference is masked, creating a false PASS. Thus routing syntax can turn a forbidden concrete technology selection into an accepted apparent pointer.

**Why this is in scope.** These samples use existing supported Markdown forms; none requires new Markdown grammar. They violate P4 (“routing syntax is not a waiver”) and the requirement that the exemption apply only to **pure non-normative** routing pointers. This is not a proposal to expand the formatting grammar or start unrestricted fuzzing.

## Recommended bounded correction

Revisit the **positive definition** of a pure routing/reference pointer. In particular, a broad arbitrary one-to-three-word prefix is not sufficient evidence that a statement is a non-normative reference. Do not simply add `selected`, `chosen`, `configured`, etc. to an endless deny-list and claim the general invariant is now established.

Keep the existing logical-statement builder and all accepted pure routing pointer cases. Add a compact property test asserting:

1. `Selected deployment technology: \`docker\`.` → FAIL
2. `Selected deployment technology: Technique: \`docker\`.` → FAIL
3. `### Selected deployment technology` followed by `Technique: \`docker\`.` → FAIL
4. `Technique: \`docker\`.` → PASS
5. `See technique: \`docker\`.` → PASS
6. `### Deployment technique` followed by `Technique: \`docker\`.` → PASS

Preserve earlier 363-case regression expectations and all untouched runtime files, and perform one cumulative confirmation audit with a strict stopping rule. Do not alter architecture, hook logic, product rules or project selection.

**Final judgment:** Iteration 6 successfully fixes the documented physical-line bypasses and passes the independent positive matrix, but the classifier's routing exception remains too permissive for P4. It should not yet be declared a frozen L1 candidate.
