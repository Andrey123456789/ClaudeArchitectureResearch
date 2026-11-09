from jdsl import C, D, P  # noqa: F401

_TESTREM = ("All six remind at Stop when production code changed without test changes (M stop-co-change.mjs:73-74, M1 stop.js:57-64, L0 claude-hook.mjs:772-774, L1 stop-cochange.mjs:63-67, K0 hook.cjs:569-572, K1 check-cochange.cjs:37-49). "
            "Scope differs: M, L0 and K0 also cover frontend production code; M1, L1 and K1 check backend code only.")

P("TST-007",
  dims=["D1 use the actual database provider when relational/provider behavior matters; Testcontainers optional; never claim fidelity from a different provider"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each test rule: M testing.md:61-64, M1 testing.md:53-57, L0 testing-principles.md:22 (+ dotnet-testing.md:15), L1 rules/0-core/testing.md:15, K0 rules/backend-tests/testing.md:30, K1 testing.md:17. M and K0 name EF Core InMemory explicitly; L1 and K1 list in-memory providers in their anti-patterns; all six skills give the same fidelity subject list.")

P("TST-008",
  dims=["D1 tests start from a known state and own their setup; no dependence on development seeding or execution order"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each rule: M testing.md:56-57 (+ persistence.md:27-29), M1 testing.md:66-67 (+ persistence-technology.md:48-50), L0 testing-principles.md:27, L1 testing.md:16, K0 testing.md:29, K1 testing.md:22. Known-state strategies are the same technique in all six skills.")

P("TST-009",
  dims=["D1 for a meaningful bug with plausible recurrence, add a regression test (fails before, passes after) unless equivalent coverage exists",
        "D2 Stop-time reminder when production code changes without test changes"],
  label="PARTIAL_PARITY_WITH_DELTA",
  same="D1 is the same default in a workflow skill of each candidate: M development-workflow:62-64, M1 development-workflow:57-59, L0 development-workflow:42, L1 development-workflow:28, K0 development-workflow:53, K1 development-workflow:42; code-review skills in all six look for it. " + _TESTREM,
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", False, [["M", "L0", "K0"], ["M1", "L1", "K1"]],
           "Frontend scope of the no-test-change reminder: present in M, L0, K0, absent in M1, L1, K1. This policy is backend-tests scoped, where all six remind; the frontend effect is recorded under the frontend testing policy.",
           root="RC-ENF-TEST-CHANGE-REMINDER-SCOPE",
           evidence={"M": ["FG-M-029803828a"], "L0": ["FG-L0-04ac048096"], "K0": ["FG-K0-c9e2e6c45b"], "M1": ["FG-M1-0e1762347a"], "L1": ["FG-L1-674df3dc2f"], "K1": ["FG-K1-c41ef97caa"]})],
  enforcement="Source-read Stop hooks; the reminder detects 'no test change', not a missing regression test.")

P("TST-010",
  dims=["D1 a manual/ad-hoc behavioral probe that uniquely demonstrated behavior is preserved as maintained automated coverage before completion unless equivalent coverage exists"],
  label="FULL_SEMANTIC_PARITY",
  cells={"L1": C(owners=["FG-L1-98dd8bf241", "FG-L1-72e0d3a273"], note="Step 2 override: no direct owner; verify:39 states the full rule (read), verify:17 the removal condition.")},
  same="Same MUST in the verify skill of each candidate: M verify:92-99, M1 verify:71-78, L0 verify:44, L1 verify:39 (with :17), K0 verify:52, K1 verify:45; dotnet-testing skills give the same conversion technique (ad-hoc request -> WebApplicationFactory test). " + _TESTREM + " The reminder points to this step in all six.")

P("TST-011",
  dims=["D1 do not generate low-value tests merely to increase coverage percentage"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST_NOT in each test rule: M testing.md:68, M1 testing.md:71-72, L0 testing-principles.md:36, L1 testing.md:17, K0 testing.md:24, K1 testing.md:28. Register item 8.7 (test priority) was settled in v1 as no text change; the 'not one test per trivial Add/Get' technique is in all six skills.")

P("TST-012",
  dims=["D1 descriptive test names communicating scenario/condition and expected behavior; follow an established convention"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default with the same MethodOrScenario_Condition_ExpectedBehavior example and convention exception in each rule: M testing.md:72-75, M1 testing.md:76-79, L0 testing-principles.md:32, L1 testing.md:18, K0 testing.md:23, K1 testing.md:27.")
