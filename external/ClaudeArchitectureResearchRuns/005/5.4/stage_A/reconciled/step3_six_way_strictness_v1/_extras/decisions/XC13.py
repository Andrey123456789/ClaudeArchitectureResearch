# XC13 X0721-X0780 (NONE:WORKFLOW_ENFORCEMENT). Analyst: Step 3.
_CHK = "Each candidate's skills name its own checker for relevant changes (WF-007, FULL)."
_DR = "Decision Request fields, stop-until-answered and recording are in all six (GOV-017 D2/D3, X0270)."

A(["X0724", "X0726", "X0729", "X0731", "X0738", "X0741", "X0742", "X0744", "X0746", "X0748", "X0750", "X0753", "X0756", "X0759", "X0760", "X0763", "X0766", "X0770", "X0771", "X0773", "X0774", "X0776", "X0779", "X0780"])
X("X0721", "SAME_NORM_DIFFERENT_PACKAGING", "Same as X0510 (threat-modeling candidates).", task="none")
X("X0722", "REDUNDANT_DERIVED_OR_NON_NORMATIVE", "Restates DEP-020.", task="none")
X("X0723", "SAME_NORM_DIFFERENT_PACKAGING", "A scan states its limitations: all six (X0488; M security-scan :227-229 completion criteria).", task="none")
X("X0725", "SAME_NORM_DIFFERENT_PACKAGING", "Review non-goals (no rewriting working code, no personal style, no unadopted patterns): L0, L1 here; M :192-195, M1 :165-168 and K0/K1 code-review. The filler-praise clause is recorded once at X0509.", task="none beyond X0509")
X("X0727", "SAME_NORM_DIFFERENT_PACKAGING", "Same as X0279 (no approval requests for routine constrained decisions).", task="none")
X("X0728", "ARCHITECTURE_SPECIFIC_DIVERGENCE", "L1/K1 checker: ASP.NET Core in Application is an error (ARC-002).", task="scored in P1", links=["RC-ENF-INNER-LAYER", "ARC-002"])
X("X0730", "REDUNDANT_DERIVED_OR_NON_NORMATIVE", "Update the durable source of truth in the same change: derived from the canonical documentation/decision-recording policy (GOV-007, recorded in P1); M1/L0 copies at X0736.", task="scored in P1", links=["GOV-007"])
X("X0736", "REDUNDANT_DERIVED_OR_NON_NORMATIVE", "Same as X0730.", task="scored in P1", links=["GOV-007"])
for _c in ["X0732", "X0734"]:
    X(_c, "SAME_NORM_DIFFERENT_PACKAGING", "Pipeline completion check (X0394).", task="none")
X("X0733", "SAME_NORM_DIFFERENT_PACKAGING", "Same as X0254 (CUSTOM_SETTINGS.md read before planning).", task="none")
X("X0735", "SAME_NORM_DIFFERENT_PACKAGING", "Delegated definition in all six root files (GOV-017 D1).", task="none")
for _c in ["X0737", "X0740", "X0747", "X0769", "X0772"]:
    X(_c, "SAME_NORM_DIFFERENT_PACKAGING", _CHK, task="none")
X("X0739", "SAME_NORM_DIFFERENT_PACKAGING", "Decision classes and the unclear-case test (GOV-017 D1/D2).", task="none")
X("X0743", "SAME_NORM_DIFFERENT_PACKAGING", "Upgrade fallout from verified documentation (X0512).", task="none")
X("X0751", "SAME_NORM_DIFFERENT_PACKAGING", "Invalid build-fix shortcuts (any/strict mode, mismatched contracts, lockfile deletion, toolchain changes): all six build-fix skills (WF-013/WF-015 readings).", task="none")
for _c in ["X0745", "X0749", "X0758", "X0765"]:
    X(_c, "SAME_NORM_DIFFERENT_PACKAGING", _DR, task="none")
X("X0752", "REDUNDANT_DERIVED_OR_NON_NORMATIVE", "Restates DEP-020/DEP-010 package bans.", task="none")
X("X0754", "SAME_NORM_DIFFERENT_PACKAGING", "Removing a deprecated API version is a breaking public API change, Reserved in all six.", task="none")
X("X0755", "SAME_NORM_DIFFERENT_PACKAGING", "Peer-dependency bypass: no agent route in all six (DEP-025 D1, PROBE-HOOK-02); L0 adds that a user-decided override is run by the user.", task="none")
X("X0757", "REDUNDANT_DERIVED_OR_NON_NORMATIVE", "Restates DEP-020.", task="none")
X("X0761", "ARCHITECTURE_SPECIFIC_DIVERGENCE", "L0 post-command reminder that removals go through add-dependency; L0 does not gate the command (PROBE-HOOK-03 allow).", task="see RC-ENF-DEP-REMOVAL-GATE", links=["RC-ENF-DEP-REMOVAL-GATE"])
X("X0762", "REDUNDANT_DERIVED_OR_NON_NORMATIVE", "Same as X0460.", task="none")
X("X0764", "SAME_NORM_DIFFERENT_PACKAGING", "Same as X0450.", task="none")
X("X0767", "REDUNDANT_DERIVED_OR_NON_NORMATIVE", "Idempotent script as the preferred production artifact (X0552; WF-019).", task="none")
X("X0768", "ARCHITECTURE_SPECIFIC_DIVERGENCE", "L1 routes removals, tool commands and audit fixes to add-dependency (deny once, PROBE-HOOK-03).", task="see roots", links=["RC-ENF-DEP-REMOVAL-GATE", "RC-ENF-DEP-INSTALL-GATE"])
X("X0775", "SAME_NORM_DIFFERENT_PACKAGING", "Headless: no new Reserved decision; unresolved Decision Requests reported (GOV-017 D3, all six).", task="none")
X("X0777", "SAME_NORM_DIFFERENT_PACKAGING", "Same as X0267.", task="none")
X("X0778", "SAME_NORM_DIFFERENT_PACKAGING", "Same as X0131.", task="none (text)")
