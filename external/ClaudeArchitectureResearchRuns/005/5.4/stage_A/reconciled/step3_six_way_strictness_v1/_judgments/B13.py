from jdsl import C, D, P  # noqa: F401

P("TST-001",
  dims=["D1 NUnit is the default .NET test framework; an established project keeps its deliberate framework; no second framework without a concrete reason",
        "D2 mechanical flag when a competing test framework package is added"],
  label="MEANINGFUL_DIVERGENCE",
  same="D1 is the same default with the same established-project exception in each test rule: M rules/testing.md:16-19, M1 rules/test-framework.md:13-15, L0 rules/2-technology/dotnet-testing.md:13, L1 rules/2-technology/backend-testing/test-framework.md:10, K0 rules/backend-tests/testing.md:15 (D-08), K1 rules/backend-tests/test-framework.md:10; each decision file records NUnit as Decided.",
  diffs=[D("D2", "ENFORCEMENT", "ENFORCED_BEHAVIOR_VARIANCE", True, [["M1", "L1", "K1"], ["M", "L0", "K0"]],
           "M1 check-manifests.js reads competingFrameworkPackages (xunit, xunit.v3, MSTest, TUnit …) from capabilities/backend-testing/nunit/MODULE.md:35; L1 post-change-checks.mjs:162-163 reports approvalRequiredPackages from nunit/enforcement.json:4-8 ('requires approval ... Remove it unless the user approved it'); K1 facets/test-framework.cjs flags them. M, L0 and K0 have no such check (searched all hooks and scripts for xunit/MSTest/TUnit).",
           counterexample="Same task: 'add tests for the order service'; the agent adds xunit and xunit.runner.visualstudio to a new test project. M1, L1 and K1 report a finding; M, L0 and K0 accept the manifest. Live effect of the PostToolUse finding NOT_RUN.",
           root="RC-ENF-COMPETING-TEST-FW",
           evidence={"M1": ["FG-M1-20c0d4198c"], "L1": ["FG-L1-63ba3ec344"], "K1": ["FG-K1-b996f69e13"], "M": ["FG-M-c9f13b2ced"], "L0": ["FG-L0-7f3fdec227"], "K0": ["FG-K0-9a74a46ac8"]})],
  enforcement="Source-read checker code; not executed on a shared fixture.")

P("TST-002",
  dims=["D1 choose the narrowest test level that meaningfully verifies the behavior; integration tests when wiring/persistence/HTTP is the subject; no fixed ratio"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each test rule: M testing.md:23-29, M1 testing.md:17-22, L0 rules/0-core/testing-principles.md:17, L1 rules/0-core/testing.md:10, K0 rules/backend-tests/testing.md:16, K1 rules/backend-tests/testing.md:14. Angular skills in all six give the same frontend test-target technique.")

P("TST-003",
  dims=["D1 tests verify observable behavior and survive refactoring; no private-call dependence or reproduced algorithms; interaction checks only when the interaction is the behavior"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST with the same interaction-verification exception in each rule: M testing.md:37-41, M1 testing.md:30-34, L0 testing-principles.md:21 ('unnecessarily'), L1 testing.md:11, K0 testing.md:21, K1 testing.md:15.")

P("TST-004",
  dims=["D1 tests are deterministic, order-independent and isolated from Production/Development data, uncontrolled external systems and shared mutable state"],
  label="FULL_SEMANTIC_PARITY",
  same="Same MUST in each rule: M testing.md:52-55, M1 testing.md:61-65, L0 testing-principles.md:26, L1 testing.md:12, K0 testing.md:28, K1 testing.md:21. M, M1, L1 and K0 name wall-clock time/TimeProvider explicitly and M, M1, K0 add 'never connect automated tests to Production data'; both follow from the shared determinism and isolation requirement, so they add no behavioral difference. dotnet-testing skills in all six configure an isolated Testing environment.")

P("TST-005",
  dims=["D1 for small finite input/state spaces prefer explicit declarative cases over loops, branching, LINQ or generated case machinery"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each rule: M testing.md:45-48, M1 testing.md:38-41 with test-framework.md:16-20 ([TestCase] rows), L0 testing-principles.md:31, L1 testing.md:13, K0 testing.md:22, K1 testing.md:26; 'state expected results rather than computing them' appears in M, M1, L0, L1, K1 rules and the K0 skill.")

P("TST-006",
  dims=["D1 WebApplicationFactory-based integration tests when routing, binding, middleware, auth, DI, repositories, EF Core or persistence is what the test must prove"],
  label="FULL_SEMANTIC_PARITY",
  same="Same default in each rule: M testing.md:30-33, M1 testing.md:24-26, L0 dotnet-testing.md:14, L1 testing.md:14 ('in-process host integration tests', with WebApplicationFactory in the capability commands), K0 testing.md:17, K1 testing.md:16.")
