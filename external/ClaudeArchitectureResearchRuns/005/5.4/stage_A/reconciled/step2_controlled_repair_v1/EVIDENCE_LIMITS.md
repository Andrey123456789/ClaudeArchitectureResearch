# Evidence limits

Item 11.3 of the register. These limits apply to every result in this run.

- **Same-family reviewer.** The session that repaired the candidates is the same model family as the Step 2 classifier and the semantic auditor, and it read their notes. Agreement between them is weak evidence. The final audit in this run is a self-audit, not an independent evaluation. A separate fresh-session or human reviewer is recommended.
- **Blind readings were imperfect.** The PI-012 blind view shows the claim text written by Step 2, the methodology note had been read first, and list membership hints at the stored value. The hash log proves order of writing, not freedom from prior belief.
- **Targeted sampling.** The 79, the 230, the extension scan and the 103 were all selected by risk or by heuristic. Their counts are not an unbiased error rate and do not bound errors in the records not read.
- **Records not read.** Most of the 6,402 records were not re-read in this run. They keep their baseline classification, and a mechanical check shows their cited text still stands. A PASS on those means the bytes are unchanged, nothing more.
- **Runtime NOT_RUN.** No live Claude session, no real application, no Swagger server, no Redis or database, no CI, no package registry. Hook decisions were executed by running the hook scripts directly, not through the host. How the host applies `ask`, `deny`, exit code 2 or `onFailure` is not verified. See `FINAL_CONSISTENCY_REPORT.md`.
- **What was executed.** The candidates' own instruction, manifest, architecture and dependency checkers; pre-command hooks; Git status in disposable repositories; real MSBuild property evaluation with .NET SDK 10.0.403 for K0's CPM fixtures, without restore.
- **Models and timelines.** The Git authority table, the headless table and the cache simulation encode the approved reading. They test that fixtures and text agree. They do not prove how an agent behaves.
- **Text postconditions are tripwires.** They catch regressions of a phrase. The meaning rests on the source reviews in `POLICY_CHECKS/`.
- **Agent-writable records.** The DEP-003 exception record names package, version and manifest and shows in a diff, but a checker cannot verify who asked. The instruction text carries that duty.
- **Union bound.** This run used the Pass 1 augmented union. Codex Pass 2 was neither read nor used. Clauses outside the union, including any added by a later pass, are not covered.
