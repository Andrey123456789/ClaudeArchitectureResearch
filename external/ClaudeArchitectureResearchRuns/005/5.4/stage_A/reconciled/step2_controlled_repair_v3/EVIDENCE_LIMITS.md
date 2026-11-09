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

## v3

The items above still apply. v3 adds the limits below.

**Self-review by the same model family.**
- One model family did all of the following:
  - adjudicated the 211 Codex Pass 2 and Pass 3 records;
  - read the 86 flagged records;
  - made every v3 change, including PV2-03B and V3-Q10;
  - wrote the cold audit.
- It is the same model family that wrote the Step 2 labels, v1 and v2.
- Agreement is weak evidence. The user's interim review of 2026-11-06 was a static, archive-level check. It found the two NuGet/CPM issues that v3 then tested and corrected, but it did not re-run the suites. An independent reader (another model family or a human) is still the next step.

**Codex evidence is hypotheses.** Codex Pass 2 and Pass 3 found 0 verified clauses and 211 unresolved hypotheses. Codex itself claims no saturation: only three of its six strategy families ran. Clauses that no pass surfaced are not covered.

**Adjudication depth.**
- Every one of the 211 records was read with its cited source and the overlapping records.
- Clusters of technique tables were judged together: one reading per table, applied to each row.
- The v3 census of security-scan prompts was a targeted pattern search over one reference file per candidate, read at the hits. It is not a full re-read of those files.

**The 86 records.**
- Each was read once at source by the same reviewer. The reason codes are a reading, not a second opinion.
- The one correction (FG-M-8b2c02178e, DEFAULT to MUST_NOT) passed the full V3-D02 gate on its second attempt. The first attempt failed only on external file events (see below).
- Records that say "do not" were not in the class and were not reviewed (Q-06). Raw MUST_NOT counts stay unusable as a strictness metric.

**Hooks ran directly.**
- Every Git, malformed-input and dependency decision came from running the hook scripts on disposable copies.
- NOT_RUN: how a live Claude Code host displays `ask`, what a user answers, how the host applies `deny`, exit 2 or `onFailure`, and what a headless run does when it meets `ask`.

**Git classification limits.**
- Classification reads the command text only. No candidate classifies Git run by a script, an alias, a Git hook or another program.
- K0 also asks for `git` after an unrecognized leading word; the other five do not.

**MSBuild and NuGet.**
- The central-package fixtures ran real MSBuild 10.0.403 evaluation.
- Where NuGet's own behavior decides validity, they also ran an offline `dotnet restore` against an empty local feed. These codes come from that restore:
  - NU1008: CPM is enforced.
  - NU1015: NuGet does not apply CPM.
  - NU1604: no lower bound.
- No registry was contacted, and no real package was restored or built.

**Central package file layouts (PV2-03B).**
- What the fixtures cover:
  - root and nested ancestor files;
  - a file outside the project's ancestors named by `DirectoryPackagesPropsPath`, the SDK's own mechanism;
  - a plain `<Import>` from `Directory.Build.props` or from the project, which the SDK does not mark imported and NuGet does not treat as CPM.
- Other ways to bring in CPM are not covered: for example the private `_DirectoryPackagesPropsFile`, the `Microsoft.Build.CentralPackageVersions` SDK, or setting `CentralPackageVersionsFileImported` by hand.
- Without the .NET SDK, K0 and M still error statically where the other four report NOT_RUN (Q-11).
- No candidate checks the name of a central file imported through `DirectoryPackagesPropsPath` (Q-12).

**PackageVersion metadata (V3-Q10).**
- Static readers handle the `Version` attribute and a `Version` child element.
- A version supplied by a later `PackageVersion Update`, an item definition or a property is read only by the shared MSBuild evaluator. That evaluator checks references and floating versions, not missing versions. A version taken from an MSBuild property is still read differently by the static checkers (the v2 limit stands).

**External events.**
- Outside this session, the protected v2 convenience archive was removed, and two files were added outside the run folder: the user's archive of v3 and the interim review (EXTERNAL_EVENTS.json, ENV-01 to ENV-03).
- The v2 tree is fenced file by file and unchanged.
- The fence and R27 tolerate exactly these recorded events, and selftest negatives prove that nothing else is tolerated (Q-13).

**Still not run.** No live agent or host, and no real application, API, Swagger UI, database, cache, registry or CI.
