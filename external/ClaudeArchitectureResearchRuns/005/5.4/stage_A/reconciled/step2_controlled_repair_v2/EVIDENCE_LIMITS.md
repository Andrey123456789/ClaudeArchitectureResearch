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

## v2

The items above were written for v1 and still apply to v2. "This run" in them means v1 where the text names v1's rules. v2 adds these limits.

- **Same session, same family.** One session made every v2 change and wrote the final audit, in the model family that wrote the labels. Its audit is a self-audit. A fresh-session or human reviewer is still the next step.
- **Blind reread.** The sample is seeded and stratified by stored label group, with equal-sized groups, so it gives no population error rate. The reader sees the claim text. A first draw leaked the group through its order and was set aside before any reading. See `BLIND_REREAD_SUMMARY.md`.
- **An open class.** `MARKED_NEVER_SOFT_MODALITY.jsonl` lists records whose claim says "never" or "must not" at a soft modality. A word match found them, and they were not read one by one. Do not use raw `MUST_NOT` counts as a strictness measure between candidates.
- **Scope hints.** `applicability_scope_hint` is a parenthesis of the original trigger field, with its source named. Every distinct phrase was read, and 30 records were read one by one. A hint can carry the scope of the delivering workflow, which may be wider than the line.
- **Hook bad input.** The scripts ran directly on malformed, empty and commandless input. M exits 1 on an input error, so only the declared `onFailure: block` can make that a block, and no host applied it. M and M1 allow a payload with no command.
- **MSBuild.** Effective Central Package Management ran through real `dotnet msbuild` evaluation on fixtures for all six, without restore. NuGet error codes came from offline restores of fixtures. Floating detection on a version that comes from an MSBuild property is out of scope.
- **Still not run.** No live agent or host, no real application, API, Swagger UI, database, cache, registry or CI.
