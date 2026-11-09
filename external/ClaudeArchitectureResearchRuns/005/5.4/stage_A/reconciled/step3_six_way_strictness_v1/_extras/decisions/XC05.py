# XC05 X0241-X0300 (GOV-005..GOV-020). Analyst: Step 3.
_REC = ("Recording an accepted decision: all six require it (GOV-017, FULL text); where and in what format differs by architecture "
        "(M/M1 docs/decisions ADR, L0 level decision summaries, L1 per-level decision file plus ADR, K0/K1 decision register plus optional ADR). ")
_FC = "Fail-closed PreToolUse handling of malformed input: PV2-02 covers M and M1, the other four fail closed by their own design (see X0225-X0229, X0142, X0146; blank-command edge Q-02)."

A(["X0243", "X0255-X0257", "X0260-X0262", "X0265", "X0266", "X0271", "X0288", "X0290", "X0293", "X0296", "X0299", "X0300"])
X("X0241", "SAME_NORM_DIFFERENT_PACKAGING", "Five-question test in every root CLAUDE.md (GOV-017 D2).", task="none")
X("X0242", "SAME_NORM_DIFFERENT_PACKAGING", _FC, task="none", links=["PV2-02"])
for _c in ["X0244", "X0245", "X0246", "X0247", "X0248", "X0249", "X0250", "X0251", "X0252", "X0253", "X0268", "X0275", "X0276", "X0281", "X0285", "X0287", "X0295"]:
    X(_c, "ARCHITECTURE_SPECIFIC_DIVERGENCE", _REC + "K1's register row is also what its reference hook reads (X0088).", task="none beyond where the record is written")
X("X0254", "SAME_NORM_DIFFERENT_PACKAGING", "Read CUSTOM_SETTINGS.md before planning: L0, L1, K0, K1 here; M development-workflow :20 '(and CUSTOM_SETTINGS.md) before planning or implementing', M1 :16 (grep).", task="none")
X("X0258", "SAME_NORM_DIFFERENT_PACKAGING", "Same as X0039 (XML comments).", task="none")
X("X0259", "GENUINE_EXTRA_NORM",
  "Force vocabulary in the always-loaded root file: 'default — deviation needs a concrete reason and must be reported' (M CLAUDE.md:14, L0 :20, K0 :13, K1 :11). M1 and L1 define no force vocabulary (grep of CLAUDE.md, rules, docs: no 'deviation', 'concrete reason ... report' or must/default definitions). Not in the oracle; cross-cutting for the 55 canonical DEFAULT policies (sensitivity S-VOCAB).",
  task="Task where the agent departs from a stated default (e.g. a class-based interceptor, a non-default status convention): M, L0, K0, K1 require a concrete reason and a report of the deviation; M1 and L1 state no such duty.",
  affects=True, presence={"M1": "ABSENT (grep)", "L1": "ABSENT (grep)"}, links=["RC-TXT-FORCE-VOCABULARY"])
X("X0263", "ARCHITECTURE_SPECIFIC_DIVERGENCE", "K0 dependency marker (DEP-004).", task="scored in P1", links=["RC-ENF-DEP-INSTALL-GATE"])
X("X0264", "ARCHITECTURE_SPECIFIC_DIVERGENCE", "K0 reference marker (ARC-020 D5).", task="scored in P1", links=["RC-ENF-REFERENCE-CMD-GATE"])
for _c in ["X0267", "X0289", "X0297"]:
    X(_c, "SAME_NORM_DIFFERENT_PACKAGING", "An explicit user instruction can approve a Reserved decision and is recorded through architecture-decision: all six (L0, L1, K0, K1 X0267; M X0289; M1 X0297).", task="none")
for _c in ["X0269", "X0273", "X0280", "X0294"]:
    X(_c, "SAME_NORM_DIFFERENT_PACKAGING", "Unresolved Decision Requests are reported in all six (M1, L0, L1, K1 X0269; M X0294; K0 X0273; K1 X0280).", task="none")
for _c in ["X0270", "X0277", "X0282", "X0291", "X0298"]:
    X(_c, "SAME_NORM_DIFFERENT_PACKAGING", "Decision Request format (Context, Options, Recommendation, Blocked, Proceeding with) in all six (GOV-017 D2).", task="none")
X("X0272", "SAME_NORM_DIFFERENT_PACKAGING", "Headless runs do not decide uncovered Reserved choices: all six (GOV-017 D3, HQ-04).", task="none")
X("X0292", "SAME_NORM_DIFFERENT_PACKAGING", "Headless pre-approval paragraph: all six (GOV-017 D3).", task="none")
X("X0274", "SAME_NORM_DIFFERENT_PACKAGING", "Breaking public contract changes are Reserved in all six (ARC-020 Reserved list).", task="none")
X("X0278", "ARCHITECTURE_SPECIFIC_DIVERGENCE", "K1 actual-state: project removal needs a recorded decision (ARC-020 D4).", task="scored in P1", links=["RC-ENF-RESERVED-GRAPH"])
X("X0279", "SAME_NORM_DIFFERENT_PACKAGING", "Do not escalate routine constrained decisions: Delegated 'decide without asking' in all six root files (GOV-017 D1; L1 X0288).", task="none")
X("X0283", "REDUNDANT_DERIVED_OR_NON_NORMATIVE", "L0 mentions rejected requests in the report; M and M1 record a rejection only when worth keeping (X0290, X0293, X0296). Procedural detail of decision recording.", task="none of consequence")
X("X0284", "GENUINE_EXTRA_NORM",
  "Final report lists Delegated choices: M development-workflow :122, L0 architecture-decision :17-19, L1 development-workflow :54, K0 :81; M1 (sections 1-6, report folded into Verify :77-78) and K1 (:58-60 'what changed and why, verify report, approvals, unresolved Decision Requests') do not ask for it.",
  task="Report content only: four candidates list the Delegated choices made; M1 and K1 do not.", affects=True,
  presence={"M1": "ABSENT (section list read)", "K1": "ABSENT (report section read)"}, links=["RC-TXT-FINAL-REPORT-CONTENT"])
X("X0286", "ARCHITECTURE_SPECIFIC_DIVERGENCE", "L1 peer-dependency bypass deny (pre-shell-command.mjs:254). The stored claim 'run only after the user confirms' does not match the current v3 line ('No confirmation, comment marker, or approval opens this route') or PROBE-HOOK-02 (deny on both runs); all six refuse the bypass (DEP-025 D1, FULL). Record-text discrepancy noted, not re-adjudicated.", task="none: same refusal in all six", links=["DEP-025"])
