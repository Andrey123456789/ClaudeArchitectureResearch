# XC09 X0481-X0540 (WF-007..WF-020). Analyst: Step 3.
_RPT = "Report/review output content (root RC-TXT-FINAL-REPORT-CONTENT, one family): changes what the agent writes in its final message, not the engineering outcome. "
_CHK = "Each candidate's skills name its own checker for relevant changes (WF-007, FULL)."

A(["X0482-X0485", "X0487-X0489", "X0496", "X0503", "X0504", "X0506", "X0514-X0517", "X0519", "X0521-X0528", "X0530-X0534", "X0536-X0540"])
X("X0481", "SAME_NORM_DIFFERENT_PACKAGING", "No automatic dependency upgrades in CI without adoption: K0 here and X0528; L0 X0529, L1 X0530, M ci-cd :122-125, M1 :105-108.", task="none")
X("X0529", "SAME_NORM_DIFFERENT_PACKAGING", "Same as X0481 (L0).", task="none")
X("X0486", "SAME_NORM_DIFFERENT_PACKAGING", "Removal follows add-dependency in all six (X0131); enforcement difference at RC-ENF-DEP-REMOVAL-GATE.", task="none (text)")
for _c in ["X0490", "X0498", "X0500", "X0501"]:
    X(_c, "SAME_NORM_DIFFERENT_PACKAGING", "Development-workflow final report core (what changed, verify report, Decision Requests) in all six; the Delegated-choices item is recorded once at X0284.", task="none beyond X0284")
X("X0491", "GENUINE_EXTRA_NORM", _RPT + "Persistence-change report (model changes, migration names with review notes calling out destructive operations, seeder update, tests): L1 ef-core workflow :32 and K1 persistence-change :54 only; no such report step in M, M1, L0, K0 (grep).",
  task="Task 'add a column': L1 and K1 report migration names and destructive-operation notes; the other four report only the general verify state (the migration review itself is PST-010 in all six).", affects=True,
  presence={"M": "ABSENT (grep)", "M1": "ABSENT (grep)", "L0": "ABSENT (grep)", "K0": "ABSENT (grep)"}, links=["RC-TXT-FINAL-REPORT-CONTENT"])
X("X0492", "SAME_NORM_DIFFERENT_PACKAGING", "Build-fix report template (initial failure, root cause, changes, builds/tests PASS/NOT RUN, remaining issues): M, M1 here; L1 build-fix :82-90, L0 :74, K0 :135, K1 :82 (WF-009 dossier).", task="none")
X("X0493", "GENUINE_EXTRA_NORM", _RPT + "Delivery report (files, stages and commands, what was verified, unconfirmed hosting assumptions): K0 delivery-pipeline :39 only (grep of the other five ci-cd/delivery skills: no report step).",
  task="CI/CD task: K0 reports stages and unconfirmed hosting assumptions; others report only the verify state. CI/CD is outside practical benchmarks (v1 extras note R19).", affects=True,
  presence={"M": "ABSENT (grep)", "M1": "ABSENT (grep)", "L0": "ABSENT (grep)", "L1": "ABSENT (grep)", "K1": "ABSENT (grep)"}, links=["RC-TXT-FINAL-REPORT-CONTENT"])
for _c in ["X0494", "X0495", "X0502"]:
    X(_c, "GENUINE_EXTRA_NORM", _RPT + "Dependency report; same fact as X0157 (M1 has no add-dependency report section).", task="see X0157", affects=True, presence={"M1": "ABSENT"}, links=["X0157", "RC-TXT-FINAL-REPORT-CONTENT"])
X("X0497", "ARCHITECTURE_SPECIFIC_DIVERGENCE", "L0 includes its hook's reference-change reports in the scaffolding report (L0 hook mechanism, ARC-020 D4).", task="none beyond P1", links=["RC-ENF-RESERVED-GRAPH"])
X("X0499", "GENUINE_EXTRA_NORM", _RPT + "Recorded-decision report (decision, record path, updated files): L1 architecture-decision :51, M :72-73 (X0294), K0 :65 (X0273), K1 :58 (X0280); M1 and L0 architecture-decision skills have no output step (grep), though both report unresolved Decision Requests (X0269).",
  task="After an approved Reserved change: four candidates report the record path and updated files; M1 and L0 do not ask for it.", affects=True,
  presence={"M1": "ABSENT (grep)", "L0": "ABSENT (grep)"}, links=["RC-TXT-FINAL-REPORT-CONTENT"])
X("X0505", "SAME_NORM_DIFFERENT_PACKAGING", "Findings ordered by severity: all six code-review skills (X0506).", task="none")
X("X0507", "SAME_NORM_DIFFERENT_PACKAGING", "Review severity scale: all six (X0506).", task="none")
X("X0508", "SAME_NORM_DIFFERENT_PACKAGING", "M1 names check-manifests.js. " + _CHK, task="none")
X("X0509", "GENUINE_EXTRA_NORM", _RPT + "'No filler praise' in review output: M :186-188, M1 :159-161, K0 :66, K1 :93 (X0511), L0 :72; L1's code-review :71 has the no-manufactured-findings rule without the praise clause (WF-012 reading).",
  task="Code review: five reviewers are told not to add filler praise; L1's is not. Output tone only.", affects=True, presence={"L1": "ABSENT (WF-012 reading)"}, links=["RC-TXT-FINAL-REPORT-CONTENT"])
X("X0511", "GENUINE_EXTRA_NORM", _RPT + "Same as X0509 (K1).", task="see X0509", affects=True, presence={"L1": "ABSENT"}, links=["X0509", "RC-TXT-FINAL-REPORT-CONTENT"])
X("X0510", "SAME_NORM_DIFFERENT_PACKAGING", "Insecure-design workflows named as threat-modeling/manual-review candidates: L0, L1 here; scan-layers references of M, M1, K0, K1 (grep 'threat model').", task="none")
X("X0512", "SAME_NORM_DIFFERENT_PACKAGING", "Never fabricate replacement APIs from memory: all six build-fix skills (L0 X0513).", task="none")
X("X0513", "SAME_NORM_DIFFERENT_PACKAGING", "Same as X0512 (L0).", task="none")
X("X0518", "SAME_NORM_DIFFERENT_PACKAGING", "No single database provider hardcoded into a generic pipeline: M, M1, L0 here, L0 X0522, K1 ci-cd :76; the ci-cd skills of all six say not to assume a particular database (e.g. M1 :19-22).", task="none")
X("X0520", "SAME_NORM_DIFFERENT_PACKAGING", "No dependence on developer-machine state: M, M1 here, L0 X0523, and the pipeline completion check of all six (X0394).", task="none")
X("X0535", "SAME_NORM_DIFFERENT_PACKAGING", "Security report shape (Scope, Limitations, Summary, Findings, Layer Results): M, M1, L0, L1 here; K0 security-scan :90/:119 and K1 :94/:117 (grep).", task="none")
