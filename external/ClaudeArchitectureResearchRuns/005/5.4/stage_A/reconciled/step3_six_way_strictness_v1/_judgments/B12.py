from jdsl import C, D, P  # noqa: F401

P("API-017",
  dims=["D1 Swagger UI enabled in Development by default; exposed elsewhere only when deployment requirements explicitly justify it"],
  label="FULL_SEMANTIC_PARITY",
  cells={"L1": C(owners=["FG-L1-c19efcd734", "FG-L1-c05cfef211"], note="Rule backend-libraries.md:12 defers non-Development exposure to the imported decisions file, whose line :16 states the same condition.")},
  same="Same default in each owner: M docs/technology-stack.md:26-30 (imported) and rules/api.md:52-53, M1 rules/api.md:50-51, L0 rules/2-technology/aspnet-core.md:27, L1 backend-libraries.md:12 with rules/3-project/decisions.md:16 (always imported: 'expose it outside Development only when deployment requirements explicitly justify it'), K0 rules/backend/api.md:33, K1 rules/backend/api-contracts.md:20.")

P("API-018",
  dims=["D1 health checks stay cheap and deterministic: no full business workflows, no expensive or mutating database work"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each rule: M api.md:57-58, M1 api.md:55-56, L0 rules/0-core/runtime-principles.md:39, L1 rules/0-core/http-api.md:36, K0 rules/backend/hosting.md:28, K1 rules/backend/operations.md:13. health-check skills in all six give the same probe technique (lightweight DB check, no Error log per failed probe).")

P("API-019",
  dims=["D1 liveness avoids external dependencies that could cause restart loops",
        "D2 readiness may depend on capabilities required to serve traffic and reflects startup and dependency availability"],
  label="PARTIAL_PARITY_WITH_DELTA",
  same="D2 is the same in each rule (M api.md:59-63, M1 api.md:57-60, L0 runtime-principles.md:40, L1 http-api.md:37, K0 hosting.md:29, K1 operations.md:14), including 'keep readiness unhealthy until required startup work completes' in the rule (M) or the health-check skill (others). D1 states the same restart-loop condition in all six.",
  diffs=[D("D1", "NORMATIVE", "TRUE_NORMATIVE_VARIANCE", False, [["M1", "L1", "K0", "K1"], ["M", "L0"]],
           "Force of the liveness clause: M1 'must not depend', K0 'must not depend ... (by default no database or remote API checks)', K1 'must avoid' (and health-check:31 'never make the application restart because a dependency is temporarily unavailable'), L1 'Liveness avoids' in a rule file whose indicative lines are normative; M ('liveness by default avoids') and L0 ('avoids ... (default)') mark it a default that a justified design may override. Canonical says 'should normally avoid', so M and L0 are closest to canonical and the four others stricter. Only a deliberately justified liveness dependency separates them; no ordinary study task asks for one. Alternative reading: L1's indicative clause as a default would move L1 to the lower tier, which changes no conclusion.",
           evidence={"M1": ["FG-M1-62f39cfa8b"], "K0": ["FG-K0-48b2163e76"], "K1": ["FG-K1-3eab1b5305"], "L1": ["FG-L1-a7f66c4bd4"], "M": ["FG-M-ce7c14d069"], "L0": ["FG-L0-35709e3953"]})],
  cells={"M1": C(compliance="STRICTER_THAN_CANONICAL"), "K0": C(compliance="STRICTER_THAN_CANONICAL"), "K1": C(compliance="STRICTER_THAN_CANONICAL"),
         "L1": C(compliance="STRICTER_THAN_CANONICAL", note="indicative 'avoids' read as binding; see D1 alternative reading")},
  challenge="v3 stores STRONGER_AND_WEAKER_EVIDENCE for K0 and K1. Challenged side by side: their 'stronger' evidence is the MUST-form liveness clause, which M1 (and in effect L1) share; the 'weaker' evidence is health-check skill technique (lightweight DB checks, readiness cascades), present in all six. The mixed label therefore marks a force difference against M and L0's DEFAULT wording, not a K0/K1-only weakness. Approved decision 8.6 (L1 liveness kept, example not weakened) is respected: L1's no-dependency endpoint example (health-check:22) is a technique example, not a stricter rule.")

P("API-020",
  dims=["D1 publicly reachable health responses expose no secrets, credentials, connection details, stack traces or unnecessary diagnostics"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each rule: M api.md:64-65, M1 api.md:61-62, L0 rules/0-core/security-principles.md:58, L1 http-api.md:38, K0 hosting.md:30, K1 operations.md:15. 'Protect detailed diagnostics with network or authorization controls' is the same technique in all six skills.")

P("API-021",
  dims=["D1 normal client-request cancellation is not mapped to a generic 500 nor logged as an unhandled failure"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each rule: M error-handling.md:62-63, M1 error-handling.md:62-63, L0 runtime-principles.md:35, L1 http-api.md:26, K0 error-handling.md:31, K1 api.md:24. The three-way client-cancel/own-timeout/upstream-timeout distinction (approved register item 8.5) is in all six http-api skills.")

P("API-022",
  dims=["D1 deprecating an externally consumed API version: mark metadata, document the replacement, communicate a realistic timeline, keep the old version for the promised period, do not remove it without considering the support contract"],
  label="FULL_SEMANTIC_PARITY",
  same="Same procedure in a workflow skill of each candidate: M development-workflow:88-92 (+ api-versioning:121-124), M1 architecture-decision:82-90, L0 architecture-decision:45-51 (with the rule pointer entry-points.md:37), L1 development-workflow:37, K0 development-workflow:72, K1 development-workflow:44. All carry the 'do not remove without considering the published support contract' clause; L0 adds that removal is its own decision, consistent with Reserved item 9 in all six.")
