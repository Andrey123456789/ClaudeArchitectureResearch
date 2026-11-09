# Experiment 005 / Phase 5.3 — final independent audit

Date: 2026-10-25. Exact root: `C:\Projects\AI Learning\ClaudeArchitectureResearchRuns\005\5.3`. Six final candidates; read-only inputs.

## Audit A — May 5.3 be frozen?

**No unconditional six-candidate freeze.** M1 has one confirmed hard-contract violation (A-001 / PAR-001). The other five are provisionally freeze-ready with the documented limitations; this is not certification of all historical acceptance scenarios.

| Candidate | Verdict | Principal qualification |
|---|---|---|
| M | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | Finite enforcement evidence; U-01–U-07 remain. |
| M1 | BLOCKED | A-001: ARC-025 exception weakens mandatory boundary. |
| L0 | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | Strict P4 passed; host/replacement conditions remain untested. |
| L1-Restart | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | Strict P4 passed; PAR-003/006 assessed separately. |
| K0 | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | A-L01 comment-only XML false positive; nonblocking limitation. |
| K1 | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | A-L02 two stale input-manifest entries; current authority available. |

## Audit B — What belongs in 5.4?

**2 confirmed material parity-only gaps**, plus **1 shared-contract violation** already counted under Audit A:

- PAR-001, HIGH: M1 adds a remote-HTTP boundary exception; canonical semantics already determine the answer.
- PAR-002, MEDIUM: M/M1/K0 require technical inexpressibility through Microsoft resilience APIs for direct Polly; L0/L1-Restart/K1 require an explicit documented exception without that added threshold.
- PAR-003, MEDIUM: L1-Restart prescribes OneTimeSetUp/OneTimeTearDown host lifetime; other five retain safe lifetime choices.

Three UNCERTAIN observations are excluded from significant-gap totals: PAR-004 diagnostic profiles, PAR-005 M1 case-table force, PAR-006 L1 production-migration exception wording. Research decisions or verification are needed, not automatic copying of the strictest candidate.

**Delivery axis:** 2 material reachability risks (RCH-001 split owner/facet loading, RCH-002 pre/post hook routing). Measure them later; do not homogenize architecture. No broken always-import was found.

## Completed and unverified work

448 final-template files inventoried/indexed; 196 unique rows with six-way evidence. 264 local subprocess fixtures: 261 PASS, 2 FAIL records for one K0 comment-parser limitation (observation plus reconfirmation), 1 NOT_APPLICABLE after neutral-fixture calibration. These are fixture dispositions, not candidate pass percentages.

Both L candidates reject all 41 representatives of the actual L0 lexicon in Core and all six named Architecture examples. All six detect tested invalid inline versions, floating central versions and outward references in single/double/multiline XML after failure. Syntax and pristine structure checks pass. K0 has a nonblocking comment false positive; K1 has two stale input-manifest entries. All 1230 snapshotted input files retain hashes; final-template sets have no additions/deletions. No candidate was changed.

**10 named unverified items:** 7 verification-limit groups U-01–U-07 plus 3 uncertain observations PAR-004–PAR-006. This counts categories, not estimated hidden defects. No essential local source is missing; one historical external citation for GOV-017/018 is unavailable inside the boundary.

The bounded audit and five deliverables are complete. Remaining items are explicitly unverified conditions, not unfinished repairs. No 5.4 implementation, generation run, remote lookup, or corrective loop is started.
