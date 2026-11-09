# XC14 X0781-X0797 (NONE:WORKFLOW_ENFORCEMENT, M/M1). Analyst: Step 3.
_CHK = "Each candidate's skills name its own checker for relevant changes (WF-007, FULL)."

A(["X0781", "X0785", "X0786", "X0789", "X0792", "X0794", "X0797"])
for _c in ["X0782", "X0784", "X0788", "X0795"]:
    X(_c, "SAME_NORM_DIFFERENT_PACKAGING", "M/M1 name check-manifests. " + _CHK, task="none")
X("X0783", "SAME_NORM_DIFFERENT_PACKAGING", "Delegated excludes boundary, dependency, convention and contract changes in all six (GOV-017 D1).", task="none")
X("X0787", "SAME_NORM_DIFFERENT_PACKAGING", "Five-question test (conventions, expensive to reverse) in all six (GOV-017 D2).", task="none")
X("X0790", "SAME_NORM_DIFFERENT_PACKAGING", "Same as X0787 (M1).", task="none")
X("X0791", "ARCHITECTURE_SPECIFIC_DIVERGENCE", "M1 peer-bypass check. The stored claim 'unless the marker is present' is not what the script does: PROBE-HOOK-02 Q9/Q10 (`--legacy-peer-deps` / `--force` with both dependency markers) are refused in all six on both runs, as M1's add-dependency text states. Record-text discrepancy noted, not re-adjudicated; DEP-025 D1 parity holds.", task="none: refusal identical in all six", links=["DEP-025"])
X("X0793", "SAME_NORM_DIFFERENT_PACKAGING", "Decision Request format and recording an instruction counted as approval (X0267, X0270).", task="none")
X("X0796", "SAME_NORM_DIFFERENT_PACKAGING", "Verify before a PR and PR description content (X0450, X0708).", task="none")
