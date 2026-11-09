# K1 Run-2 notes

## Sweep notes

Reverse checks conducted after all 13 batches (no first-run or Codex material consulted):

1. **Keyword scan of every NON_NORMATIVE / IMPLEMENTATION / DUPLICATE span** (`_tools/sweep.py`) for must/never/do not/only/required/Reserved/always/default/approval/blocked/error terms; each Markdown hit was re-read in context. Result: one reclassification (add-dependency line 21, a normative lead-in, relinked to RULE-K1-0160); imperative technique notes recorded as NON_NORMATIVE or DUPLICATE orphans (ef-core bulk operations, http-api 429/502 reference, swagger launch profile, dotnet-testing mock guidance, .gitignore guidance, Docker image optimization, backend-layout tree comments).
2. **Large-span review** (every NN/IM/DU span of 15+ lines, 45 spans): all are code samples, directory trees, decision-guide tables, navigation-map tables or script helper code; none hides an independent rule.
3. **Script branch review**: dispatch.cjs (PreToolUse fail-closed vs advisory Post/Stop exit codes), classify-command.cjs (verb tables, exact-version predicates, wrapper depth limit, reference-change edges), actual-state.cjs (HEAD baselining, project add/remove vs edge findings, product-input reminders, deleted-manifest findings, instruction-change trigger), check-cochange.cjs (Git-only, once-per-content-state), check-manifests.cjs (CPM, floating/range/prerelease, deny/exception lists, tests/ and lockfile warnings, ISO-dated approval rows), check-instructions.cjs (every predicate mapped to X1-X5, X11-X24, R1/R2), facet scripts. Executable defaults captured as exceptions/modality of the gate constraints and recorded as DUPLICATE orphans (fail-closed guard, HEAD baseline, once-per-content-state, thin-delegate warning).
4. **Config defaults**: settings.json (gate registration, fail-closed only for PreToolUse), Directory.Build.props (net10.0; Nullable and ImplicitUsings registered as EXTRA-K1-0049), Directory.Packages.props (CPM on, empty), .editorconfig (style values linked to RUN-009; suggestion/silent severities do not fail builds).
5. **Mixed clauses**: every MIXED segment (41) was checked to split the oracle part from the extra part (e.g. 'adopting versioning: Reserved', '`From -> To` recording', 'never add the deprecated Polly packages', 'Mapster never referenced from Domain').
6. **Hypotheses revisited**: the product-input precedence claim in MAP.md (first LINK_UNCERTAIN) was resolved to POLICY_LINKED after CLAUDE.md line 24 was read; the add-dependency 'anything else goes through architecture-decision' scope (UNCERTAIN-K1-0002) was re-examined against CLAUDE.md's five-question test and stays open.
7. **Interaction effects recorded**: the decision register ships an empty Accepted-decisions table, so under EXTRA-K1-0009 no project-reference edge (including the standard Clean Architecture scaffold references) is pre-approved; project-structure explicitly requires recording the scaffold first.

Adversarial classification rule applied consistently: a clause is EXTRA when it is binding (must/never/do not/only, or hook/checker-enforced), changes allowable outcomes, and is not entailed by a stack-neutral reading of an oracle policy; soft technique ('prefer', 'consider', examples) and technique classes the oracle itself excludes (EXC-002..EXC-018) are NON_NORMATIVE unless a binding restriction is added; workflow-specific report-content mandates beyond WF-009 are registered as EXTRA.

## Limitations

- Structural PASS from validators 11/12/13 proves coverage and referential integrity only, not semantic completeness.
- Policy statuses are judgments: all 196 policies are restated nearly verbatim in active surfaces, so all are MATCHED; strengthened modalities ('normally/should' -> 'must', e.g. API-012, API-019, TST-003) are noted in search_notes rather than downgraded.
- Hooks were analyzed statically; no candidate hook or script was executed.
- Three relations remain open (UNCERTAIN-K1-0002, -0003, -0004); they are not counted as EXTRA.
- Unused identifier gaps (EXTRA-K1-0029..0031, EXTRA-K1-0043, UNCERTAIN-K1-0001 converted to RULE-K1-0285) are intentional; IDs are local and not comparable across runs.
- Navigation-map and decision-guide tables were classified per table, not per row, after row-by-row reading.
