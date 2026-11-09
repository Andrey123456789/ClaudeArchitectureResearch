# Six-way presence of the genuine extra norms and the open-decision extra, established by reading (see the
# cluster decisions for the evidence). Cluster membership alone is not presence: one fact is often split
# across several clusters. extras.py assemble applies these rows to the listed clusters.
R("RC-ENF-DEP-REMOVAL-GATE", family=None,
  title="Pre-execution gate on dependency removal (and bare update / audit fix) commands",
  present={"M1": "deny until self-attested marker", "K0": "deny until self-attested marker", "L1": "deny once, identical retry allowed",
           "K1": "block with no command route; remove manifest entries and restore instead"},
  absent={"M": "allowed; post-change reminder (file-change.mjs:66-69)", "L0": "allowed; post-command reminder (claude-hook.mjs:555-557)"},
  text_norm="Removal goes through add-dependency in all six skills (same text).",
  evidence="PROBE-HOOK-03 (HOOK_PROBE3_RESULTS.json) R1-R5; X0128, X0132, X0134, X0168.",
  task="Remove an unused package: M and L0 run the command; M1/K0 refuse until the marker; L1 refuses once; K1 refuses and the agent edits manifests.",
  clusters=["X0128", "X0132", "X0134"])
R("RC-TXT-FORCE-VOCABULARY", family=None,
  title="Force vocabulary: 'default — deviation needs a concrete reason and must be reported'",
  present={"M": "CLAUDE.md:14", "L0": "CLAUDE.md:20", "K0": "CLAUDE.md:13", "K1": "CLAUDE.md:11"},
  absent={"M1": "no vocabulary (grep)", "L1": "no vocabulary (grep)"},
  text_norm="Not in the oracle. Cross-cutting for the 55 canonical DEFAULT policies (sensitivity S-VOCAB).",
  evidence="X0259, X0554, X0556.",
  task="Departing from a stated default: four candidates require a reason and a report; M1 and L1 do not say so.",
  clusters=["X0259", "X0554", "X0556"])
R("RC-TXT-REPORT-DEPENDENCY", family="RC-TXT-FINAL-REPORT-CONTENT",
  title="Dependency report (package, version, license, checks, approval status)",
  present={"M": "add-dependency :164-167", "L0": ":59-61", "L1": ":73-75", "K0": ":97", "K1": ":82-84"},
  absent={"M1": "add-dependency has no report section (sections 1-7, Removal)"},
  text_norm="General verify report (WF-009) in all six.", evidence="X0157, X0159, X0494, X0495, X0502.",
  task="Add a package: M1 does not ask for the version/license/approval summary.",
  clusters=["X0157", "X0159", "X0494", "X0495", "X0502"])
R("RC-TXT-REPORT-DELEGATED", family="RC-TXT-FINAL-REPORT-CONTENT",
  title="Final report lists the Delegated choices made",
  present={"M": "development-workflow :122", "L0": "architecture-decision :17-19", "L1": "development-workflow :54", "K0": ":81"},
  absent={"M1": "report folded into Verify :77-78", "K1": "report :58-60 without Delegated choices"},
  text_norm="", evidence="X0284.", task="Report content only.", clusters=["X0284"])
R("RC-TXT-REPORT-SETTINGS", family="RC-TXT-FINAL-REPORT-CONTENT",
  title="custom-settings report (old -> new value, surfaces, migration, verify)",
  present={"L1": "custom-settings :49", "K1": ":44"}, absent={c: "no report step (grep)" for c in ["M", "M1", "L0", "K0"]},
  text_norm="", evidence="X0302.", task="Report content only.", clusters=["X0302"])
R("RC-TXT-REPORT-PERSISTENCE", family="RC-TXT-FINAL-REPORT-CONTENT",
  title="Persistence report (migration names, destructive operations, seeder, tests)",
  present={"L1": "ef-core workflow :32", "K1": "persistence-change :54"}, absent={c: "no report step (grep)" for c in ["M", "M1", "L0", "K0"]},
  text_norm="Migration review itself is PST-010 in all six.", evidence="X0491.", task="Report content only.", clusters=["X0491"])
R("RC-TXT-REPORT-DELIVERY", family="RC-TXT-FINAL-REPORT-CONTENT",
  title="Delivery report (stages, commands, unconfirmed hosting assumptions)",
  present={"K0": "delivery-pipeline :39"}, absent={c: "no report step (grep)" for c in ["M", "M1", "L0", "L1", "K1"]},
  text_norm="CI/CD outside practical benchmarks (v1 R19).", evidence="X0493.", task="Report content only.", clusters=["X0493"])
R("RC-TXT-REPORT-DECISION", family="RC-TXT-FINAL-REPORT-CONTENT",
  title="Recorded-decision report (record path, updated files)",
  present={"M": "architecture-decision :72-73", "L1": ":51", "K0": ":65", "K1": ":58"},
  absent={"M1": "no output step (grep)", "L0": "no output step (grep)"},
  text_norm="Unresolved Decision Requests are reported in all six.", evidence="X0499.", task="Report content only.", clusters=["X0499"])
R("RC-TXT-REVIEW-PRAISE", family="RC-TXT-FINAL-REPORT-CONTENT",
  title="No filler praise in review output",
  present={"M": "code-review :186-188", "M1": ":159-161", "L0": ":72", "K0": ":66", "K1": ":93"},
  absent={"L1": "code-review :71 without the clause"},
  text_norm="No manufactured findings in all six (WF-012).", evidence="X0509, X0511.", task="Review output tone only.", clusters=["X0509", "X0511"])
R("RC-TXT-L1-EF-FIRE-AND-FORGET", family=None,
  title="No fire-and-forget EF Core async operations (DbContext not thread-safe)",
  present={"M": "ef-core :411-413", "M1": ":414-421", "L0": ":237", "K0": ":348", "K1": ":120"},
  absent={"L1": "no such text in .claude/ or CLAUDE.md (grep)"},
  text_norm="Canonical RUN-002 covers sync-over-async only.", evidence="X0322, X0323.",
  task="Background or parallel EF Core work: five ef-core skills warn; L1's does not. Technique level.", clusters=["X0322"])
R("Q-01", family=None,
  title="Security-scan prompt: deliberate raw HTML in a server-rendered UI",
  present={c: "scan-layers reference (v3 CL15 addition)" for c in ["M", "M1", "L1", "K0", "K1"]},
  absent={"L0": "residual kept by v3 (Q-01, USER_DECISION)"},
  text_norm="", evidence="X0400.", task="Only a scan of an app with a server-rendered UI; all candidates target an Angular SPA.", clusters=["X0400"])
