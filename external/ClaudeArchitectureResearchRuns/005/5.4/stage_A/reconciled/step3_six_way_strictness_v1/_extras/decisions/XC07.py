# XC07 X0361-X0420 (RUN-009..RUN-024, SEC-001..SEC-016). Analyst: Step 3.
A(["X0361-X0380", "X0382", "X0384-X0390", "X0392", "X0393", "X0395-X0397", "X0399", "X0401-X0406", "X0408-X0420"])
X("X0381", "SAME_NORM_DIFFERENT_PACKAGING", "Retry only plausibly transient failures (never validation, auth, permanent 404, deterministic business rejection): M, M1, L0, L1, K0 here and K1 X0383 (resilience references).", task="none")
X("X0383", "SAME_NORM_DIFFERENT_PACKAGING", "K1 copy of X0381.", task="none")
X("X0391", "REDUNDANT_DERIVED_OR_NON_NORMATIVE", "DI factory-delegate technique (throw for an unknown configuration value); the 'selection' wording is runtime implementation selection, not a capability slot.", task="none")
X("X0394", "SAME_NORM_DIFFERENT_PACKAGING", "Pipeline completion check (clean restore, builds, tests, no developer-machine state, no secrets, expected artifacts): M ci-cd :173-176, M1 :158-161, L0 delivery-pipeline :43, L1 ci-cd :97, K0 and K1 ci-cd skills (WF-003/WF-017 reading).", task="none")
X("X0398", "SAME_NORM_DIFFERENT_PACKAGING", "Same as X0203 (configuration external to images).", task="none")
X("X0400", "UNRESOLVED_OR_DECISION_DEPENDENT",
  "Q-01 (USER_DECISION, v3 CL15): the security-scan prompt 'review deliberate raw HTML handling in any server-rendered UI' is in M, M1, L1, K0 and K1 scan-layers references; L0 lacks it (residual kept by v3, not homogenized). Not decided in Step 3.",
  task="Only a security scan of an application with a server-rendered UI that emits raw HTML: five scans prompt the review, L0's does not. All study candidates target an Angular SPA, so the effect is hypothetical (v3 risk: low).",
  affects=False, presence={"L0": "ABSENT (Q-01)"}, links=["Q-01", "CL15-SCAN-RAW-HTML"])
X("X0407", "REDUNDANT_DERIVED_OR_NON_NORMATIVE", "Authorization technique (capability policies with constants); 'capability' here is an authorization capability, not a capability module. Same technique in all six authentication skills (X0403-X0406, X0408).", task="none")
