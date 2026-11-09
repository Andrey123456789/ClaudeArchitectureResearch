# Phase 5.3 final independent audit — executive summary

Audit date: 2026-10-24. Object: the six current `output/template/` trees under the exact requested root. This report resumes the existing audit; it does not start another test cycle. Inputs remained read-only.

## Audit A — May 5.3 be frozen?

**Not as an unconditional six-candidate freeze. M1 is BLOCKED by one confirmed common-contract violation (A-001).** The other five candidates may be frozen with documented limitations. This is a bounded independent assessment, not certification of every historical corrective-test claim.

| Candidate | Audit A verdict | Reason / qualification |
|---|---|---|
| M | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | No confirmed blocker; policy plus post-reference routing is intentional, not a failed M1-style pre-execution contract. |
| M1 | BLOCKED | A-001: ARC-025 is weakened by an explicit HTTP-modeling exception. |
| L0 | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | Strict P4 and finite XML/hook probes passed; live-host and broader state transitions remain unverified. |
| L1-Restart | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | Strict P4 passed; migration qualifier interpretation remains uncertain (PAR-003). |
| K0 | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | No confirmed blocker; nested-cwd acceptance was obscured by empty fixture directories. |
| K1 | FREEZE_READY_WITH_DOCUMENTED_LIMITATIONS | No confirmed template blocker; optional provenance manifest has two mismatches and advanced graph/binds cases remain unverified. |

A-001 is a static semantic contradiction, not a parity-only preference: M1 permits remote HTTP transport in Application contracts when Application explicitly models HTTP, while canonical ARC-025 forbids that leak without this exception. A checker can pass while its instruction prose violates the oracle. No candidate has been repaired.

## Audit B — What belongs in 5.4?

There is **one confirmed significant parity-only gap**, PAR-002: configured diagnostic coverage/severity differs across candidates, although all retain risk-scoped verification and changed-file unused-using cleanup. The exact common analyzer/formatter threshold is **REQUIRES_RESEARCH_DECISION**. Do not choose the strictest template as the oracle.

PAR-001 cross-references the existing M1 shared-contract violation; it is not counted again as a parity-only gap. Two additional semantic questions remain **UNCERTAIN**: PAR-003 (L1-Restart production-migration default qualifier) and PAR-004 (M1 floating-version explicit-request exception). These are investigation/clarification entries, not established outcome differences. Fewer than three significant parity-only gaps were established; none were invented to fill a quota.

Three separate delivery risks are recorded: RCH-001 path/workflow loading, RCH-002 pre/post reference intervention, and RCH-003 capability-facet resolution. Preserve those architectural mechanisms and measure their effects later; no actual broken route or measured quality penalty was established by these observations.

## Counts and evidence boundaries

| Item | Count | Meaning |
|---|---:|---|
| Confirmed freeze blockers | 1 | A-001, M1 only |
| Significant parity-only findings | 1 | PAR-002; configuration observed, resulting build effects untested |
| Shared violations cross-listed in Audit B | 1 | PAR-001 = A-001, not a second blocker |
| Material delivery/reachability risk observations | 3 | RCH-001 through RCH-003; not measured defect rates |
| Open semantic questions | 2 | PAR-003 and PAR-004 |
| Other numbered verification/provenance limitations | 9 | LIM-001 through LIM-009; categories, not counts of every unrun test |
| Total enumerated unresolved items | 11 | Two semantic questions plus nine limitation categories |
| Common policies | 194 + 2 = 196 | Live counts, unique IDs, identical source trees across all six |
| Matrix records / candidate cells | 196 / 1176 | 1173 SAME, 1 DIFFERENT, 2 UNVERIFIED; static textual comparison, not 1173 runtime tests |
| Independent local command invocations | 381 | 368 asserted probes plus 13 setup/observation calls |
| Adjudicated asserted probes | 363 PASS; 3 NOT_APPLICABLE; 2 UNVERIFIED | No confirmed dynamic FAIL. Raw harness had 6 FAIL expectations, all disclosed and adjudicated in report 04. |
| Final-template files protected by hashes | 448 | Pre/post bytes and path sets identical |

## Completed and remaining work

Completed: bounded source inventory and precedence review, six architecture reviews, 196-row semantic mapping, fixed P4 corpus, syntax/clean-checker tests, finite independent hook/XML tests and one discrepancy reconfirmation, optional manifest validation, pre/post hashes, and five deliverables. No further Phase 5.3 audit execution is pending in this request.

Remaining outside this audit: correct A-001 before an unconditional six-candidate freeze; decide PAR-002's benchmark diagnostic baseline in 5.4; resolve PAR-003/004 and the numbered limitations if stronger assurance is needed. This report does not implement or initiate those tasks.

All required authoritative local files were present. M's optional MANIFEST.sha256 was absent. Two historical research citation anchors were unavailable inside the boundary; the embedded normalized invariants remain available and controlling. K1's optional manifest discrepancy is LIM-009.

See `01_5_3_FREEZE_READINESS.md` for independent verdicts, `02_5_4_REQUIREMENT_PARITY_BACKLOG.md` for six-way findings, `03_REQUIREMENT_PARITY_MATRIX.csv` for all policies, and `04_AUDIT_EVIDENCE_AND_METHOD.md` for hashes, commands, raw observations and limitations.
